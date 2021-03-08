# -*- coding: utf-8 -*-
from typing import Optional, List

from sqlalchemy import func, select
from sqlalchemy.sql import and_

from fastapi import APIRouter, Query, Depends, Body


from commons.code import *

from models.mysql.system import db_engine, t_group
from models.mysql import *

from settings.my_settings import settings_my

from handlers import tool
from handlers.items import ItemOutOperateSuccess, ItemOutOperateFailed
from handlers.items.group import ItemOutGroupList, ItemInAddGroup, ItemInEditGroup, ItemOutGroup, ListDataGroup
from handlers.exp import MyError
from handlers.const import *


router = APIRouter(tags=[TAGS_GROUP], dependencies=[Depends(tool.check_token)])


@router.get("/group", tags=[TAGS_GROUP], response_model=ItemOutGroupList, name='获取用户组')
async def get_groups(userinfo: dict = Depends(tool.get_userinfo_from_token), page: Optional[int] = Query(settings_my.web_page, description='第几页'), limit: Optional[int] = Query(settings_my.web_page_size, description='每页条数')):
    item_out = ItemOutGroupList()

    # 鉴权
    tool.check_operation_permission(userinfo['id'], PERMISSION_GROUP_VIEW)

    with db_engine.connect() as conn:
        # 获取当前有多少数据
        count_sql = select([func.count(t_group.c.id)]).where(t_group.c.sub_status != TABLE_SUB_STATUS_INVALID_DEL)
        total = conn.execute(count_sql).scalar()

        # 获取分页后的用户组列表
        group_sql = select([
            t_group.c.id,
            t_group.c.pid,
            t_group.c.name,
            t_group.c.code,
            t_group.c.intro,
            t_group.c.status,
            t_group.c.sub_status,
        ]).where(t_group.c.sub_status != TABLE_SUB_STATUS_INVALID_DEL).order_by('sort', 'id')

        if page != 0:
            group_sql = group_sql.limit(limit).offset((page - 1) * limit)
        group_obj_list = conn.execute(group_sql).fetchall()

    item_out.data = ListDataGroup(
        result=[ItemOutGroup(
        id=group_obj.id,
        name=group_obj.name,
        code=group_obj.code,
        intro=group_obj.intro,
        status=group_obj.status,
        sub_status=group_obj.sub_status,
    ) for group_obj in group_obj_list],
        total=total,
        page=page,
        limit=limit,
    )
    return item_out


@router.post("/group", tags=[TAGS_GROUP], response_model=ItemOutOperateSuccess, name='添加用户组')
async def add_group(item_in: ItemInAddGroup, userinfo: dict = Depends(tool.get_userinfo_from_token)):
    """
    添加用户组\n
    :param item_in:\n
    :param userinfo:\n
    :return:
    """

    # 鉴权
    tool.check_operation_permission(userinfo['id'], PERMISSION_GROUP_ADD)

    conn = db_engine.connect()
    trans = conn.begin()

    try:
        # 查看是否已经有该code的用户组
        if not tool.is_code_unique(t_group, item_in.code, conn):
            raise MyError(code=MULTI_DATA, msg='code repeat')

        # 新增用户组
        print('insert group start')
        group_sql = t_group.insert().values({
            'pid': item_in.pid,
            'name': item_in.name,
            'code': item_in.code,
            'intro': item_in.intro,
            'creator': userinfo['name']
        })
        group_res = conn.execute(group_sql)

        if item_in.role_id:
            # 绑定用户组 - 角色关系
            tool.bind_group_roles(group_res.lastrowid, item_in.role_ids, userinfo, conn)

        trans.commit()
        return ItemOutOperateSuccess()
    except MyError as mex:
        trans.rollback()
        raise mex
    except:
        trans.rollback()
        raise MyError(code=HTTP_500_INTERNAL_SERVER_ERROR, msg='internal server error')
    finally:
        conn.close()


@router.put("/group/{group_id}", tags=[TAGS_GROUP], response_model=ItemOutOperateSuccess, name="修改用户组")
async def edit_group(group_id: int, item_in: ItemInEditGroup, userinfo: dict = Depends(tool.get_userinfo_from_token)):
    """
    修改用户组\n
    :param group_id:\n
    :param item_in:\n
    :param userinfo:\n
    :return:
    """
    # 鉴权
    tool.check_operation_permission(userinfo['id'], PERMISSION_GROUP_EDIT)

    conn = db_engine.connect()
    trans = conn.begin()

    try:
        # 查找用户组
        group_sql = t_group.select().where(t_group.c.id == group_id).limit(1).with_for_update()
        group_obj = conn.execute(group_sql).fetchone()
        if not group_obj:
            raise MyError(code=HTTP_404_NOT_FOUND, msg='group not exists')

        # 修改用户组
        group_val = {
            'editor': userinfo['name']
        }

        if item_in.pid is not None:
            group_val['pid'] = item_in.pid
        if item_in.name is not None:
            group_val['name'] = item_in.name
        if item_in.intro is not None:
            group_val['intro'] = item_in.intro

        update_group_sql = t_group.update().where(t_group.c.id == group_id).values(group_val)
        conn.execute(update_group_sql)

        if item_in.role_ids:
            # 解绑旧的用户组-角色关系
            tool.unbind_group_roles(group_id, 0, userinfo, conn)

            # 绑定新的用户组 - 角色关系
            tool.bind_group_roles(group_id, item_in.role_ids, userinfo, conn)

        # 提交事务
        trans.commit()

        return ItemOutOperateSuccess()
    except MyError as mex:
        trans.rollback()
        raise mex
    except:
        trans.rollback()
        raise MyError(code=HTTP_500_INTERNAL_SERVER_ERROR, msg='internal server error')
    finally:
        conn.close()


@router.put("/group/{group_id}/disable", tags=[TAGS_GROUP], name="禁用用户组")
async def disable_group(group_id: int, userinfo: dict = Depends(tool.get_userinfo_from_token)):
    """
    禁用用户组\n
    :param group_id:\n
    :param userinfo:\n
    :return:
    """
    # 鉴权
    tool.check_operation_permission(userinfo['id'], PERMISSION_GROUP_DISABLE)

    conn = db_engine.connect()
    trans = conn.begin()

    try:
        # 查找用户组
        group_sql = t_group.select().where(t_group.c.id == group_id).limit(1).with_for_update()
        conn.execute(group_sql).fetchone()

        # 修改用户组状态为禁用
        update_group_sql = t_group.update().where(and_(
            t_group.c.id == group_id,
            t_group.c.status == TABLE_STATUS_VALID,
            t_group.c.sub_status == TABLE_SUB_STATUS_VALID,
        )).values({
            'status': TABLE_STATUS_INVALID,
            'sub_status': TABLE_SUB_STATUS_INVALID_DISABLE
        })
        conn.execute(update_group_sql)

        # 提交事务
        trans.commit()

        return ItemOutOperateSuccess()
    except MyError as mex:
        trans.rollback()
        raise mex
    except:
        trans.rollback()
        raise MyError(code=HTTP_500_INTERNAL_SERVER_ERROR, msg='internal server error')
    finally:
        conn.close()


@router.put("/group/{group_id}/enable", tags=[TAGS_GROUP], name='启用用户组')
async def enable_group(group_id: int, userinfo: dict = Depends(tool.get_userinfo_from_token)):
    """
    启用用户组\n
    :param group_id:\n
    :param userinfo:\n
    :return:
    """
    # 鉴权
    tool.check_operation_permission(userinfo['id'], PERMISSION_GROUP_ENABLE)

    conn = db_engine.connect()
    trans = conn.begin()

    try:
        # 查找用户组
        group_sql = t_group.select().where(t_group.c.id == group_id).limit(1).with_for_update()
        conn.execute(group_sql).fetchone()

        # 修改用户组状态为启用
        update_group_sql = t_group.update().where(and_(
            t_group.c.id == group_id,
            t_group.c.status == TABLE_STATUS_INVALID,
            t_group.c.sub_status == TABLE_SUB_STATUS_INVALID_DISABLE,
        )).values({
            'status': TABLE_STATUS_VALID,
            'sub_status': TABLE_SUB_STATUS_VALID
        })
        conn.execute(update_group_sql)

        # 提交事务
        trans.commit()

        return ItemOutOperateSuccess()
    except:
        trans.rollback()
        raise MyError(code=HTTP_500_INTERNAL_SERVER_ERROR, msg='internal server error')
    finally:
        conn.close()


@router.delete("/group/{group_id}", tags=[TAGS_GROUP], name='删除用户组')
async def del_group(group_id: int, userinfo: dict = Depends(tool.get_userinfo_from_token)):
    """
    删除用户组\n
    :param group_id:\n
    :param userinfo:\n
    :return:
    """
    # 鉴权
    tool.check_operation_permission(userinfo['id'], PERMISSION_GROUP_DEL)

    conn = db_engine.connect()
    trans = conn.begin()

    try:
        # 查找用户组
        group_sql = t_group.select().where(t_group.c.id == group_id).limit(1).with_for_update()
        conn.execute(group_sql).fetchone()

        # 修改用户组状态为无效（软删除）
        update_group_sql = t_group.update().where(and_(
            t_group.c.id == group_id,
            t_group.c.sub_status != TABLE_SUB_STATUS_INVALID_DEL,
        )).values({
            'status': TABLE_STATUS_INVALID,
            'sub_status': TABLE_SUB_STATUS_INVALID_DEL
        })
        conn.execute(update_group_sql)

        # 提交事务
        trans.commit()

        return ItemOutOperateSuccess()
    except:
        trans.rollback()
        raise MyError(code=HTTP_500_INTERNAL_SERVER_ERROR, msg='internal server error')
    finally:
        conn.close()
