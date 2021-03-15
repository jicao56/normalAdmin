# -*- coding: utf-8 -*-
from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.sql import and_

from fastapi import APIRouter, Query
from fastapi import Depends

from utils.my_logger import logger

from commons.code import *
from commons.funcs import chinese_to_upper_english

from models.mysql.system import db_engine, TABLE_STATUS_VALID, TABLE_STATUS_INVALID, TABLE_SUB_STATUS_VALID, \
    TABLE_SUB_STATUS_INVALID_DEL, TABLE_SUB_STATUS_INVALID_DISABLE
from models.mysql.system.permission import *

from settings.my_settings import settings_my

from handlers import tool
from handlers.items import ItemOutOperateSuccess, ItemOut
from handlers.items.permission import ListDataPermission, ItemOutPermissionList, ItemOutPermission, \
    ItemInAddPermission, ItemInEditPermission, ItemOutRolePermission, ItemRolePermission
from handlers.exp import MyError
from handlers.const import *


router = APIRouter(tags=[TAGS_PERMISSION], dependencies=[Depends(tool.check_token)])


@router.get("/permission", tags=[TAGS_PERMISSION], response_model=ItemOutPermissionList, name='获取权限')
async def get_permissions(
        userinfo: dict = Depends(tool.get_userinfo_from_token),
        page: Optional[int] = Query(settings_my.web_page, description='第几页'),
        limit: Optional[int] = Query(settings_my.web_page_size, description='每页条数'),
):
    item_out = ItemOutPermissionList()

    # 鉴权
    tool.check_operation_permission(userinfo['id'], PERMISSION_PERMISSION_VIEW)

    with db_engine.connect() as conn:

        # 获取当前有多少数据
        count_sql = select([func.count(t_permission.c.id)]).where(t_permission.c.sub_status != TABLE_SUB_STATUS_INVALID_DEL)
        total = conn.execute(count_sql).scalar()

        # 获取分页后的权限列表
        permission_sql = select([
            t_permission.c.id,
            t_permission.c.pid,
            t_permission.c.name,
            t_permission.c.code,
            t_permission.c.intro,
            t_permission.c.category,
            t_permission.c.status,
            t_permission.c.sub_status,
        ]).where(t_permission.c.sub_status != TABLE_SUB_STATUS_INVALID_DEL).order_by('sort', 'id')

        if page != 0:
            permission_sql = permission_sql.limit(limit).offset((page - 1) * limit)
        permission_obj_list = conn.execute(permission_sql).fetchall()

    item_out.data = ListDataPermission(
        result=[ItemOutPermission(
            id=permission_obj.id,
            name=permission_obj.name,
            code=permission_obj.code,
            intro=permission_obj.intro,
            category=permission_obj.category,
            status=permission_obj.status,
            sub_status=permission_obj.sub_status,
        ) for permission_obj in permission_obj_list],
        total=total,
        page=page,
        limit=limit,
    )
    return item_out


@router.get("/ptree", tags=[TAGS_PERMISSION], name='获取带父子级的权限')
async def get_permission_tree(userinfo: dict = Depends(tool.get_userinfo_from_token)):
    item_out = ItemOut()
    # 鉴权
    tool.check_operation_permission(userinfo['id'], PERMISSION_PERMISSION_VIEW)

    with db_engine.connect() as conn:
        # 获取所有权限
        permission_sql = select([
            t_permission.c.id,
            t_permission.c.pid,
            t_permission.c.name,
            t_permission.c.code,
            t_permission.c.intro,
            t_permission.c.category,
        ]).where(and_(
            t_permission.c.status == TABLE_STATUS_VALID,
            t_permission.c.sub_status == TABLE_SUB_STATUS_VALID,
        )).order_by('sort', 'id')
        permission_list = conn.execute(permission_sql).fetchall()

        # 权限序列化
        target_permission = []
        tool.permission_serialize(0, permission_list, target_permission)
        item_out.data = target_permission
        return item_out


@router.get("/rperm", tags=[TAGS_PERMISSION], name='角色所拥有的权限')
async def get_role_permissions(
        userinfo: dict = Depends(tool.get_userinfo_from_token),
        role_id: Optional[int] = Query(..., description='角色id'),
):
    item_out = ItemOut()
    # 鉴权
    tool.check_operation_permission(userinfo['id'], PERMISSION_PERMISSION_VIEW)

    with db_engine.connect() as conn:
        # 获取当前角色有哪些权限pid: Optional[int] = Body(None, description='父级权限ID')
        #     id: Optional[int] = Body(None, description='权限ID')
        #     name: Optional[str] = Body(None, description='权限')
        #     code: Optional[str] = Body(None, description='权限唯一标识')
        #     intro: Optional[str] = Body(None, description='权限简介')
        #     category: Optional[int] = Body(None, description='权限类别  1-菜单访问权限；2-页面元素可见性权限；3-功能模块操作权限；4-文件修改权限；')
        role = tool.get_role(role_id, conn)
        role_permission_obj_list = tool.get_role_permission(role, conn, [PERMISSION_CATEGORY_OPERATION])
        role_permissions = [ItemRolePermission(
            pid=tmp_obj.pid,
            id=tmp_obj.id,
            name=tmp_obj.name,
            code=tmp_obj.code,
            intro=tmp_obj.intro,
            category=tmp_obj.category,
        ) for tmp_obj in role_permission_obj_list]
        item_out.data = role_permissions
        return item_out


@router.post("/permission", tags=[TAGS_PERMISSION], response_model=ItemOutOperateSuccess, name='添加权限')
async def add_permission(item_in: ItemInAddPermission, userinfo: dict = Depends(tool.get_userinfo_from_token)):
    """
    添加权限\n
    :param item_in:\n
    :param userinfo:\n
    :return:
    """
    # 鉴权
    tool.check_operation_permission(userinfo['id'], PERMISSION_PERMISSION_ADD)

    conn = db_engine.connect()

    try:
        # 查看是否已经有该code的权限
        if not tool.is_code_unique(t_permission, item_in.code, conn):
            raise MyError(code=MULTI_DATA, msg='code repeat')

        # 新增权限
        permission_sql = t_permission.insert().values({
            'pid': item_in.pid,
            'name': item_in.name,
            'code': item_in.code if item_in.code else chinese_to_upper_english(item_in.name),
            'intro': item_in.intro,
            'category': item_in.category,
            'creator': userinfo['name']
        })
        conn.execute(permission_sql)
        return ItemOutOperateSuccess()
    except MyError as me:
        logger.error(str(me))
        raise me
    except Exception as ex:
        logger.error(str(ex))
        raise MyError(code=HTTP_500_INTERNAL_SERVER_ERROR, msg='internal server error')
    finally:
        conn.close()


@router.put("/permission/{permission_id}", tags=[TAGS_PERMISSION], response_model=ItemOutOperateSuccess, name="修改权限")
async def edit_permission(permission_id: int, item_in: ItemInEditPermission, userinfo: dict = Depends(tool.get_userinfo_from_token)):
    """
    修改权限\n
    :param permission_id:\n
    :param item_in:\n
    :param userinfo:\n
    :return:
    """
    # 鉴权
    tool.check_operation_permission(userinfo['id'], PERMISSION_PERMISSION_EDIT)

    conn = db_engine.connect()

    try:
        # 查找权限
        permission_sql = t_permission.select().where(t_permission.c.id == permission_id).limit(1).with_for_update()
        permission_obj = conn.execute(permission_sql).fetchone()
        if not permission_obj:
            raise MyError(code=HTTP_404_NOT_FOUND, msg='permission not exists')

        # 修改权限
        data = {
            'editor': userinfo['name']
        }
        if item_in.pid is not None:
            data['pid'] = item_in.pid
        if item_in.name is not None:
            data['name'] = item_in.name
        if item_in.intro is not None:
            data['intro'] = item_in.intro

        update_permission_sql = t_permission.update().where(t_permission.c.id == permission_id).values(data)
        conn.execute(update_permission_sql)
        return ItemOutOperateSuccess()
    except MyError as me:
        logger.error(str(me))
        raise me
    except Exception as ex:
        logger.error(str(ex))
        raise MyError(code=HTTP_500_INTERNAL_SERVER_ERROR, msg='internal server error')
    finally:
        conn.close()


@router.delete("/permission/{permission_id}", tags=[TAGS_PERMISSION], name='删除权限')
async def del_permission(permission_id: int, userinfo: dict = Depends(tool.get_userinfo_from_token)):
    """
    删除权限\n
    :param permission_id:\n
    :param userinfo:\n
    :return:
    """
    # 鉴权
    tool.check_operation_permission(userinfo['id'], PERMISSION_PERMISSION_DEL)

    conn = db_engine.connect()
    try:
        # 查找权限
        permission_sql = t_permission.select().where(t_permission.c.id == permission_id).limit(1).with_for_update()
        permission_obj = conn.execute(permission_sql).fetchone()
        if not permission_obj:
            raise MyError(code=HTTP_404_NOT_FOUND, msg='权限不存在')

        # 判断状态
        if permission_obj.sub_status == TABLE_SUB_STATUS_INVALID_DEL:
            # 已经是删除状态
            raise MyError(code=HTTP_404_NOT_FOUND, msg='权限已删除，无法删除')

        # 修改权限状态为无效（软删除）
        update_permission_sql = t_permission.update().where(and_(
            t_permission.c.id == permission_id,
            t_permission.c.sub_status != TABLE_SUB_STATUS_INVALID_DEL,
        )).values({
            'status': TABLE_STATUS_INVALID,
            'sub_status': TABLE_SUB_STATUS_INVALID_DEL
        })
        conn.execute(update_permission_sql)
        return ItemOutOperateSuccess()
    except MyError as me:
        logger.error(str(me))
        raise me
    except Exception as ex:
        logger.error(str(ex))
        raise MyError(code=HTTP_500_INTERNAL_SERVER_ERROR, msg='internal server error')
    finally:
        conn.close()


@router.put("/permission/{permission_id}/disable", tags=[TAGS_PERMISSION], name="禁用权限")
async def disable_permission(permission_id: int, userinfo: dict = Depends(tool.get_userinfo_from_token)):
    """
    禁用权限\n
    :param permission_id:\n
    :param userinfo:\n
    :return:
    """
    # 鉴权
    tool.check_operation_permission(userinfo['id'], PERMISSION_PERMISSION_DISABLE)

    conn = db_engine.connect()

    try:
        # 查找权限
        permission_sql = t_permission.select().where(t_permission.c.id == permission_id).limit(1).with_for_update()
        permission_obj = conn.execute(permission_sql).fetchone()
        if not permission_obj:
            raise MyError(code=HTTP_404_NOT_FOUND, msg='权限不存在')

        # 判断状态
        if permission_obj.status != TABLE_STATUS_VALID:
            # 不是有效状态，无法禁用
            raise MyError(code=HTTP_404_NOT_FOUND, msg='权限无效，无法禁用')

        # 修改权限状态为禁用
        update_permission_sql = t_permission.update().where(and_(
            t_permission.c.id == permission_id,
            t_permission.c.status == TABLE_STATUS_VALID,
            t_permission.c.sub_status == TABLE_SUB_STATUS_VALID,
        )).values({
            'status': TABLE_STATUS_INVALID,
            'sub_status': TABLE_SUB_STATUS_INVALID_DISABLE
        })
        conn.execute(update_permission_sql)
        return ItemOutOperateSuccess()
    except MyError as me:
        logger.error(str(me))
        raise me
    except Exception as ex:
        logger.error(str(ex))
        raise MyError(code=HTTP_500_INTERNAL_SERVER_ERROR, msg='internal server error')
    finally:
        conn.close()


@router.put("/permission/{permission_id}/enable", tags=[TAGS_PERMISSION], name='启用权限')
async def enable_permission(permission_id: int, userinfo: dict = Depends(tool.get_userinfo_from_token)):
    """
    启用权限\n
    :param permission_id:\n
    :param userinfo:\n
    :return:
    """
    # 鉴权
    tool.check_operation_permission(userinfo['id'], PERMISSION_PERMISSION_ENABLE)

    conn = db_engine.connect()

    try:
        # 查找权限
        permission_sql = t_permission.select().where(t_permission.c.id == permission_id).limit(1).with_for_update()
        permission_obj = conn.execute(permission_sql).fetchone()
        if not permission_obj:
            raise MyError(code=HTTP_404_NOT_FOUND, msg='权限不存在')

        # 判断状态
        if permission_obj.status == TABLE_STATUS_VALID or permission_obj.sub_status != TABLE_SUB_STATUS_INVALID_DISABLE:
            # 不是禁用状态，无法启用
            raise MyError(code=HTTP_404_NOT_FOUND, msg='权限不是禁用状态，无法启用')

        # 修改权限状态为启用
        update_permission_sql = t_permission.update().where(and_(
            t_permission.c.id == permission_id,
            t_permission.c.status == TABLE_STATUS_INVALID,
            t_permission.c.sub_status == TABLE_SUB_STATUS_INVALID_DISABLE,
        )).values({
            'status': TABLE_STATUS_VALID,
            'sub_status': TABLE_SUB_STATUS_VALID
        })
        conn.execute(update_permission_sql)
        return ItemOutOperateSuccess()
    except MyError as me:
        logger.error(str(me))
        raise me
    except Exception as ex:
        logger.error(str(ex))
        raise MyError(code=HTTP_500_INTERNAL_SERVER_ERROR, msg='internal server error')
    finally:
        conn.close()


