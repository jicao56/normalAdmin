# -*- coding: utf-8 -*-
from typing import Optional, List

from sqlalchemy import func, select
from sqlalchemy.sql import and_

from fastapi import APIRouter, Query
from fastapi import Depends

from commons.code import *

from models.mysql.system import db_engine, t_role
from models.mysql import *

from settings import settings

from handlers import tool
from handlers.items import ItemOutOperateSuccess, ItemOutOperateFailed
from handlers.items.role import ListDataRole, ItemOutRoleList, ItemOutRole, ItemInAddRole, ItemInEditRole
from handlers.exp import MyException
from handlers.const import *


router = APIRouter(tags=[TAGS_ROLE], dependencies=[Depends(tool.check_token)])


@router.get("/role", tags=[TAGS_ROLE], response_model=ItemOutRoleList, name='获取角色')
async def get_roles(userinfo: dict = Depends(tool.get_userinfo_from_token), page: Optional[int] = Query(settings.web.page, description='第几页'), limit: Optional[int] = Query(settings.web.page_size, description='每页条数')):
    item_out = ItemOutRoleList()

    # 鉴权
    tool.check_operation_permission(userinfo['id'], PERMISSION_ROLE_VIEW)

    with db_engine.connect() as conn:
        # 获取当前有多少数据
        count_sql = select([func.count(t_role.c.id)])
        total = conn.execute(count_sql).scalar()

        # 获取分页后的角色列表
        role_sql = select([
            t_role.c.id,
            t_role.c.pid,
            t_role.c.name,
            t_role.c.code,
            t_role.c.intro,
            t_role.c.status,
            t_role.c.sub_status,
        ]).order_by('sort', 'id').limit(limit).offset((page - 1) * limit)
        role_obj_list = conn.execute(role_sql).fetchall()

    item_out.data = ListDataRole(
        result=[ItemOutRole(
            id=role_obj.id,
            name=role_obj.name,
            code=role_obj.code,
            intro=role_obj.intro,
            status=role_obj.status,
            sub_status=role_obj.sub_status,
        ) for role_obj in role_obj_list],
        total=total,
        page=page,
        limit=limit,
    )
    return item_out


@router.post("/role", tags=[TAGS_ROLE], response_model=ItemOutOperateSuccess, name='添加角色')
async def add_role(item_in: ItemInAddRole, userinfo: dict = Depends(tool.get_userinfo_from_token)):
    """
    添加角色\n
    :param item_in:\n
    :param userinfo:\n
    :return:
    """

    # 鉴权
    tool.check_operation_permission(userinfo['id'], PERMISSION_ROLE_ADD)

    conn = db_engine.connect()

    try:
        # 查看是否已经有该code的用户组
        if not tool.is_code_unique(t_role, item_in.code, conn):
            raise MyException(status_code=HTTP_400_BAD_REQUEST, detail={'code': MULTI_DATA, 'msg': 'code repeat'})

        # 新增角色
        role_sql = t_role.insert().values({
            'pid': item_in.pid,
            'name': item_in.name,
            'code': item_in.code,
            'intro': item_in.intro,
            'creator': userinfo['name']
        })
        conn.execute(role_sql)
        return ItemOutOperateSuccess()
    except MyException as mex:
        raise mex
    except Exception as ex:
        raise MyException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=ItemOutOperateFailed(code=HTTP_500_INTERNAL_SERVER_ERROR, msg=str(ex)))
    finally:
        conn.close()


@router.put("/role/{role_id}", tags=[TAGS_ROLE], response_model=ItemOutOperateSuccess, name="修改角色")
async def edit_role(role_id: int, item_in: ItemInEditRole, userinfo: dict = Depends(tool.get_userinfo_from_token)):
    """
    修改角色\n
    :param role_id:\n
    :param item_in:\n
    :param userinfo:\n
    :return:
    """
    # 鉴权
    tool.check_operation_permission(userinfo['id'], PERMISSION_ROLE_EDIT)

    conn = db_engine.connect()

    try:
        # 查找角色
        role_sql = t_role.select().where(t_role.c.id == role_id).limit(1).with_for_update()
        role_obj = conn.execute(role_sql).fetchone()
        if not role_obj:
            raise MyException(status_code=HTTP_404_NOT_FOUND, detail={'code': HTTP_404_NOT_FOUND, 'msg': 'role not exists'})

        # 修改角色
        data = {
            'editor': userinfo['name']
        }
        if item_in.pid is not None:
            data['pid'] = item_in.pid
        if item_in.name is not None:
            data['name'] = item_in.name
        if item_in.intro is not None:
            data['intro'] = item_in.intro

        update_role_sql = t_role.update().where(t_role.c.id == role_id).values(data)
        conn.execute(update_role_sql)
        return ItemOutOperateSuccess()
    except MyException as mex:
        raise mex
    except:
        raise MyException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=ItemOutOperateFailed(code=HTTP_500_INTERNAL_SERVER_ERROR, msg='inter server error'))
    finally:
        conn.close()


@router.put("/role/{role_id}/disable", tags=[TAGS_ROLE], name="禁用角色")
async def disable_role(role_id: int, userinfo: dict = Depends(tool.get_userinfo_from_token)):
    """
    禁用角色\n
    :param role_id:\n
    :param userinfo:\n
    :return:
    """
    # 鉴权
    tool.check_operation_permission(userinfo['id'], PERMISSION_ROLE_DISABLE)

    conn = db_engine.connect()

    try:
        # 查找角色
        role_sql = t_role.select().where(t_role.c.id == role_id).limit(1).with_for_update()
        conn.execute(role_sql).fetchone()

        # 修改角色状态为禁用
        update_role_sql = t_role.update().where(and_(
            t_role.c.id == role_id,
            t_role.c.status == TABLE_STATUS_VALID,
            t_role.c.sub_status == TABLE_SUB_STATUS_VALID,
        )).values({
            'status': TABLE_STATUS_INVALID,
            'sub_status': TABLE_SUB_STATUS_INVALID_DISABLE
        })
        conn.execute(update_role_sql)
        return ItemOutOperateSuccess()
    except:
        raise MyException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=ItemOutOperateFailed(code=HTTP_500_INTERNAL_SERVER_ERROR, msg='inter server error'))
    finally:
        conn.close()


@router.put("/role/{role_id}/enable", tags=[TAGS_ROLE], name='启用角色')
async def enable_role(role_id: int, userinfo: dict = Depends(tool.get_userinfo_from_token)):
    """
    启用角色\n
    :param role_id:\n
    :param userinfo:\n
    :return:
    """
    # 鉴权
    tool.check_operation_permission(userinfo['id'], PERMISSION_ROLE_ENABLE)

    conn = db_engine.connect()

    try:
        # 查找角色
        role_sql = t_role.select().where(t_role.c.id == role_id).limit(1).with_for_update()
        conn.execute(role_sql).fetchone()

        # 修改角色状态为启用
        update_role_sql = t_role.update().where(and_(
            t_role.c.id == role_id,
            t_role.c.status == TABLE_STATUS_INVALID,
            t_role.c.sub_status == TABLE_SUB_STATUS_INVALID_DISABLE,
        )).values({
            'status': TABLE_STATUS_VALID,
            'sub_status': TABLE_SUB_STATUS_VALID
        })
        conn.execute(update_role_sql)
        return ItemOutOperateSuccess()
    except:
        raise MyException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=ItemOutOperateFailed(code=HTTP_500_INTERNAL_SERVER_ERROR, msg='inter server error'))
    finally:
        conn.close()


@router.delete("/role/{role_id}", tags=[TAGS_ROLE], name='删除角色')
async def del_user(role_id: int, userinfo: dict = Depends(tool.get_userinfo_from_token)):
    """
    删除角色\n
    :param role_id:\n
    :param userinfo:\n
    :return:
    """
    # 鉴权
    tool.check_operation_permission(userinfo['id'], PERMISSION_ROLE_DEL)

    conn = db_engine.connect()
    try:
        # 查找角色
        role_sql = t_role.select().where(t_role.c.id == role_id).limit(1).with_for_update()
        conn.execute(role_sql).fetchone()

        # 修改角色状态为无效（软删除）
        update_role_sql = t_role.update().where(and_(
            t_role.c.id == role_id,
            t_role.c.sub_status != TABLE_SUB_STATUS_INVALID_DEL,
        )).values({
            'status': TABLE_STATUS_INVALID,
            'sub_status': TABLE_SUB_STATUS_INVALID_DEL
        })
        conn.execute(update_role_sql)
        return ItemOutOperateSuccess()
    except:
        raise MyException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=ItemOutOperateFailed(code=HTTP_500_INTERNAL_SERVER_ERROR, msg='inter server error'))
    finally:
        conn.close()


@router.put("/role/{role_id}/permission", tags=[TAGS_ROLE], response_model=ItemOutOperateSuccess, name='绑定角色-权限')
async def bind_role_permission(role_id: int, item_in: List[int], userinfo: dict = Depends(tool.get_userinfo_from_token)):
    """
    绑定角色-权限\n
    :param role_id:\n
    :param item_in:\n
    :param userinfo:\n
    :return:
    """
    conn = db_engine.connect()
    trans = conn.begin()
    try:
        # 鉴权
        tool.check_operation_permission(userinfo['id'], PERMISSION_ROLE_PERMISSION_BIND)

        # 查询角色是否存在
        role = tool.get_role(role_id, conn)
        if not role.is_super:
            # 不是超级管理员，绑定权限
            for permission_id in item_in:
                # 绑定角色权限
                tool.bind_role_permission(role_id, permission_id, userinfo, conn)

            trans.commit()
        else:
            trans.rollback()

        return ItemOutOperateSuccess()
    except:
        trans.rollback()
        raise MyException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=ItemOutOperateFailed(code=HTTP_500_INTERNAL_SERVER_ERROR, msg='inter server error'))
    finally:
        conn.close()

