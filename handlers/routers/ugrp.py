# -*- coding: utf-8 -*-
"""
用户 - 用户组 - 角色 - 权限 关系处理接口
"""


from fastapi import APIRouter
from fastapi import Depends

from commons.code import *

from models.mysql.system import db_engine
from models.mysql import *

from handlers import tool
from handlers.items import ItemOutOperateSuccess, ItemOutOperateFailed
from handlers.items.user import ItemInBindUserGroup, ItemInBindUserRole, ItemInUserAddGroups, ItemInUserAddRoles

from handlers.items.group import ItemInBindGroupRole, ItemInBindGroupUsers
from handlers.const import *


router = APIRouter(tags=[TAGS_UGRP], dependencies=[Depends(tool.check_token)])


@router.post("/user_group", tags=[TAGS_UGRP], response_model=ItemOutOperateSuccess, name="绑定用户-用户组")
async def bind_user_groups(item_in: ItemInBindUserGroup, userinfo: dict = Depends(tool.get_userinfo_from_token)):
    """
    绑定用户-用户组\n
    :param item_in:\n
    :param userinfo:\n
    :return:
    """
    with db_engine.connect() as conn:
        # 鉴权
        tool.check_operation_permission(userinfo['id'], PERMISSION_USER_GROUP_BIND, conn=conn)

        # 解绑旧的用户-用户组关系
        tool.unbind_user_groups(item_in.user_ids, 0, userinfo, conn)

        # 绑定新的用户-用户组关系
        tool.bind_user_groups(item_in.user_ids, item_in.group_ids, userinfo, conn)

    return ItemOutOperateSuccess()


@router.put("/user/{user_id}/groups", tags=[TAGS_UGRP], response_model=ItemOutOperateSuccess, name="给用户分配用户组")
async def user_init_groups(user_id: int, item_in: ItemInBindUserGroup, userinfo: dict = Depends(tool.get_userinfo_from_token)):
    """
    给用户分配用户组\n
    :param user_id:\n
    :param item_in:\n
    :param userinfo:\n
    :return:
    """
    with db_engine.connect() as conn:
        # 鉴权
        tool.check_operation_permission(userinfo['id'], PERMISSION_USER_GROUP_BIND, conn=conn)

        # 解绑旧的用户-用户组关系
        tool.unbind_user_groups(user_id, 0, userinfo, conn)

        # 绑定新的用户-用户组关系
        tool.bind_user_groups(user_id, item_in.group_ids, userinfo, conn)

    return ItemOutOperateSuccess()


@router.post("/user/{user_id}/groups", tags=[TAGS_UGRP], response_model=ItemOutOperateSuccess, name="给用户添加用户组")
async def user_add_groups(user_id: int, item_in: ItemInUserAddGroups, userinfo: dict = Depends(tool.get_userinfo_from_token)):
    """
    绑定用户-用户组\n
    :param user_id:\n
    :param item_in:\n
    :param userinfo:\n
    :return:
    """
    with db_engine.connect() as conn:
        # 鉴权
        tool.check_operation_permission(userinfo['id'], PERMISSION_USER_GROUP_BIND, conn=conn)

        # 绑定新的用户-用户组关系
        tool.bind_user_groups(user_id, item_in.group_ids, userinfo, conn)

    return ItemOutOperateSuccess()


@router.post("/user_role", tags=[TAGS_UGRP], response_model=ItemOutOperateSuccess, name="绑定用户-角色")
async def bind_user_roles(item_in: ItemInBindUserRole, userinfo: dict = Depends(tool.get_userinfo_from_token)):
    """
    绑定用户-角色\n
    :param item_in:\n
    :param userinfo:\n
    :return:
    """
    with db_engine.connect() as conn:
        # 鉴权
        tool.check_operation_permission(userinfo['id'], PERMISSION_USER_ROLE_BIND, conn)

        # 解绑旧的用户-角色关系
        tool.unbind_user_roles(item_in.user_ids, item_in.role_ids, userinfo, conn)

        # 绑定新的用户-角色关系
        tool.bind_user_roles(item_in.user_ids, item_in.role_ids, userinfo, conn)

    return ItemOutOperateSuccess()


@router.put("/user/{user_id}/roles", tags=[TAGS_UGRP], response_model=ItemOutOperateSuccess, name="给用户分配角色")
async def user_init_roles(user_id: int, item_in: ItemInUserAddRoles, userinfo: dict = Depends(tool.get_userinfo_from_token)):
    """
    给用户分配角色\n
    :param user_id:\n
    :param item_in:\n
    :param userinfo:\n
    :return:
    """
    with db_engine.connect() as conn:
        # 鉴权
        tool.check_operation_permission(userinfo['id'], PERMISSION_USER_ROLE_BIND, conn=conn)

        # 解绑旧的用户-角色关系
        tool.unbind_user_roles(user_id, 0, userinfo, conn)

        # 绑定新的用户-角色关系
        tool.bind_user_roles(user_id, item_in.role_ids, userinfo, conn)

    return ItemOutOperateSuccess()


@router.post("/user/{user_id}/roles", tags=[TAGS_UGRP], response_model=ItemOutOperateSuccess, name="给用户添加角色")
async def user_add_roles(user_id: int, item_in: ItemInUserAddRoles, userinfo: dict = Depends(tool.get_userinfo_from_token)):
    """
    绑定用户-角色\n
    :param user_id:\n
    :param item_in:\n
    :param userinfo:\n
    :return:
    """
    with db_engine.connect() as conn:
        # 鉴权
        tool.check_operation_permission(userinfo['id'], PERMISSION_USER_ROLE_BIND, conn=conn)

        # 绑定新的用户-角色关系
        tool.bind_user_roles(user_id, item_in.role_ids, userinfo, conn)

    return ItemOutOperateSuccess()


@router.post("/group/{group_id}/users", tags=[TAGS_UGRP], response_model=ItemOutOperateSuccess, name="给用户组分配用户")
async def group_init_users(group_id: int, item_in: ItemInBindGroupUsers, userinfo: dict = Depends(tool.get_userinfo_from_token)):
    """
    给用户组分配用户\n
    :param group_id:\n
    :param item_in:\n
    :param userinfo:\n
    :return:
    """
    with db_engine.connect() as conn:
        # 鉴权
        tool.check_operation_permission(userinfo['id'], PERMISSION_USER_GROUP_BIND, conn=conn)

        # 解绑旧的用户-用户组关系
        tool.unbind_user_groups(item_in.user_ids, 0, userinfo, conn)

        # 绑定新的用户-用户组关系
        tool.bind_user_groups(item_in.user_ids, group_id, userinfo, conn)

    return ItemOutOperateSuccess()


@router.put("/group/{group_id}/users", tags=[TAGS_UGRP], response_model=ItemOutOperateSuccess, name="给用户组添加用户")
async def group_add_users(group_id: int, item_in: ItemInBindGroupUsers, userinfo: dict = Depends(tool.get_userinfo_from_token)):
    """
    给用户组添加用户\n
    :param group_id:\n
    :param item_in:\n
    :param userinfo:\n
    :return:
    """
    with db_engine.connect() as conn:
        # 鉴权
        tool.check_operation_permission(userinfo['id'], PERMISSION_USER_GROUP_BIND, conn=conn)

        # 绑定新的用户-用户组关系
        tool.bind_user_groups(item_in.user_ids, group_id, userinfo, conn)

    return ItemOutOperateSuccess()


@router.post("/group_role", tags=[TAGS_UGRP], response_model=ItemOutOperateSuccess, name="绑定用户组-角色")
async def bind_group_role(item_in: ItemInBindGroupRole, userinfo: dict = Depends(tool.get_userinfo_from_token)):
    """
    绑定用户组-角色\n
    :param item_in:\n
    :param userinfo:\n
    :return:
    """
    with db_engine.connect() as conn:
        # 鉴权
        tool.check_operation_permission(userinfo['id'], PERMISSION_GROUP_ROLE_BIND, conn=conn)

        # 解绑旧的用户-角色关系
        tool.unbind_group_roles(item_in.group_ids, item_in.role_ids, userinfo, conn)

        # 绑定新的用户组 - 角色关系
        tool.bind_group_roles(item_in.group_ids, item_in.role_ids, userinfo, conn)

    return ItemOutOperateSuccess()


@router.put("/group/{group_id}/roles", tags=[TAGS_UGRP], response_model=ItemOutOperateSuccess, name="给用户组分配角色")
async def group_init_roles(group_id: int, item_in: ItemInBindGroupRole, userinfo: dict = Depends(tool.get_userinfo_from_token)):
    """
    绑定用户组-角色\n
    :param group_id:\n
    :param item_in:\n
    :param userinfo:\n
    :return:
    """
    with db_engine.connect() as conn:
        # 鉴权
        tool.check_operation_permission(userinfo['id'], PERMISSION_GROUP_ROLE_BIND, conn=conn)

        # 解绑旧的用户组-角色关系
        tool.unbind_group_roles(group_id, 0, userinfo, conn)

        # 绑定新的用户组 - 角色关系
        tool.bind_group_roles(group_id, item_in.role_ids, userinfo, conn)

    return ItemOutOperateSuccess()


@router.post("/group/{group_id}/roles", tags=[TAGS_UGRP], response_model=ItemOutOperateSuccess, name="给用户组添加角色")
async def group_add_roles(group_id: int, item_in: ItemInBindGroupRole, userinfo: dict = Depends(tool.get_userinfo_from_token)):
    """
    绑定用户组-角色\n
    :param group_id:\n
    :param item_in:\n
    :param userinfo:\n
    :return:
    """
    with db_engine.connect() as conn:
        # 鉴权
        tool.check_operation_permission(userinfo['id'], PERMISSION_GROUP_ROLE_BIND, conn=conn)

        # 绑定新的用户组 - 角色关系
        tool.bind_group_roles(group_id, item_in.role_ids, userinfo, conn)

    return ItemOutOperateSuccess()


@router.put("/role/{role_id}/permissions", tags=[TAGS_UGRP], response_model=ItemOutOperateSuccess, name='绑定角色-权限')
async def role_init_permission(role_id: int, item_in: ItemInBindGroupRole, userinfo: dict = Depends(tool.get_userinfo_from_token)):
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
        return ItemOutOperateFailed(code=TYPE_TRANSFER_ERR, msg='error')
    finally:
        conn.close()
