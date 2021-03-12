# -*- coding: utf-8 -*-
"""
用户 - 用户组 - 角色 - 权限 关系处理接口
"""
from typing import List

from fastapi import APIRouter, Body, Depends, Query

from commons.code import *

from models.mysql.system import db_engine
from models.mysql.system.permission import *


from handlers import tool
from handlers.items import ItemOutOperateSuccess, ItemOutOperateFailed
from handlers.items.ugrp import ItemInBindUserGroup, ItemInBindUserRole, ItemInBindGroupRole, ItemInBindRolePermission
from handlers.const import *
from handlers.exp import MyError

from utils.my_logger import logger


router = APIRouter(tags=[TAGS_UGRP], dependencies=[Depends(tool.check_token)])


UG_ACT_BIND_USER_GROUP = 1
UG_ACT_APPEND_USER_GROUP = 2
UG_ACT = {
    UG_ACT_BIND_USER_GROUP: '绑定用户-用户组关系',
    UG_ACT_APPEND_USER_GROUP: '追加用户-用户组关系',
}
UG_ACT_DESC = '操作类型：'+';'.join(['{}:{}'.format(key, val) for key, val in UG_ACT.items()])


UR_ACT_BIND_USER_ROLE = 1
UR_ACT_APPEND_USER_ROLE = 2
UR_ACT = {
    UR_ACT_BIND_USER_ROLE: '绑定用户-角色关系',
    UR_ACT_APPEND_USER_ROLE: '追加用户-角色关系',
}
UR_ACT_DESC = '操作类型：'+';'.join(['{}:{}'.format(key, val) for key, val in UG_ACT.items()])


GR_ACT_BIND_GROUP_ROLE = 1
GR_ACT_APPEND_GROUP_ROLE = 2
GR_ACT = {
    GR_ACT_BIND_GROUP_ROLE: '绑定用户组-角色关系',
    GR_ACT_APPEND_GROUP_ROLE: '追加用户组-角色关系',
}
GR_ACT_DESC = '操作类型：'+';'.join(['{}:{}'.format(key, val) for key, val in UG_ACT.items()])


RP_ACT_BIND_ROLE_PERMISSION = 1
RP_ACT_APPEND_ROLE_PERMISSION = 2
RP_ACT = {
    RP_ACT_BIND_ROLE_PERMISSION: '绑定用户组-角色关系',
    RP_ACT_APPEND_ROLE_PERMISSION: '追加用户组-角色关系',
}
RP_ACT_DESC = '操作类型：'+';'.join(['{}:{}'.format(key, val) for key, val in UG_ACT.items()])


@router.post("/bug", tags=[TAGS_UGRP], response_model=ItemOutOperateSuccess, name="绑定用户-用户组")
async def bind_user_group(item_in: ItemInBindUserGroup, act: int = Query(1, description=UG_ACT_DESC), userinfo: dict = Depends(tool.get_userinfo_from_token)):
    """
    绑定用户-用户组\n
    :param act:\n
    :param item_in:\n
    :param userinfo:\n
    :return:
    """
    with db_engine.connect() as conn:
        # 鉴权
        tool.check_operation_permission(userinfo['id'], PERMISSION_USER_GROUP_BIND, conn=conn)

        if act not in UG_ACT.keys():
            raise MyError(code=REQ_PARAMS_ILLEGAL, msg=REQ_PARAMS[REQ_PARAMS_ILLEGAL])

        if act == UG_ACT_BIND_USER_GROUP:
            # 解绑旧的用户-用户组关系
            tool.unbind_user_group(item_in.user_ids, 0, userinfo, conn)

        # 绑定新的用户-用户组关系
        tool.bind_user_group(item_in.user_ids, item_in.group_ids, userinfo, conn)

    return ItemOutOperateSuccess()


@router.post("/bur", tags=[TAGS_UGRP], response_model=ItemOutOperateSuccess, name="绑定用户-角色")
async def bind_user_role(item_in: ItemInBindUserRole, act: int = Query(1, description=UR_ACT_DESC), userinfo: dict = Depends(tool.get_userinfo_from_token)):
    """
    绑定用户-角色\n
    :param item_in:\n
    :param act:\n
    :param userinfo:\n
    :return:
    """
    with db_engine.connect() as conn:
        # 鉴权
        tool.check_operation_permission(userinfo['id'], PERMISSION_USER_ROLE_BIND, conn)

        if act not in UR_ACT.keys():
            raise MyError(code=REQ_PARAMS_ILLEGAL, msg=REQ_PARAMS[REQ_PARAMS_ILLEGAL])

        if act == UR_ACT_BIND_USER_ROLE:
            # 解绑旧的用户-角色关系
            tool.unbind_user_role(item_in.user_ids, item_in.role_ids, userinfo, conn)

        # 绑定新的用户-角色关系
        tool.bind_user_role(item_in.user_ids, item_in.role_ids, userinfo, conn)

    return ItemOutOperateSuccess()


@router.post("/bgr", tags=[TAGS_UGRP], response_model=ItemOutOperateSuccess, name="绑定用户组-角色")
async def bind_group_role(item_in: ItemInBindGroupRole, act: int = Query(1, description=UR_ACT_DESC), userinfo: dict = Depends(tool.get_userinfo_from_token)):
    """
    绑定用户组-角色\n
    :param item_in:\n
    :param act:\n
    :param userinfo:\n
    :return:
    """
    with db_engine.connect() as conn:
        # 鉴权
        tool.check_operation_permission(userinfo['id'], PERMISSION_GROUP_ROLE_BIND, conn=conn)

        if act not in GR_ACT.keys():
            raise MyError(code=REQ_PARAMS_ILLEGAL, msg=REQ_PARAMS[REQ_PARAMS_ILLEGAL])

        if act == GR_ACT_BIND_GROUP_ROLE:
            # 解绑旧的用户组-角色关系
            tool.unbind_group_role(item_in.group_ids, item_in.role_ids, userinfo, conn)

        # 绑定新的用户组 - 角色关系
        tool.bind_group_role(item_in.group_ids, item_in.role_ids, userinfo, conn)

    return ItemOutOperateSuccess()


@router.post("/brp", tags=[TAGS_UGRP], response_model=ItemOutOperateSuccess, name="绑定角色-权限")
async def bind_role_permission(item_in: ItemInBindRolePermission, act: int = Query(1, description=UR_ACT_DESC), userinfo: dict = Depends(tool.get_userinfo_from_token)):
    """
    绑定角色-权限\n
    :param item_in:\n
    :param act:\n
    :param userinfo:\n
    :return:
    """
    with db_engine.connect() as conn:
        # 鉴权
        tool.check_operation_permission(userinfo['id'], PERMISSION_ROLE_PERMISSION_BIND, conn=conn)

        if act not in GR_ACT.keys():
            raise MyError(code=REQ_PARAMS_ILLEGAL, msg=REQ_PARAMS[REQ_PARAMS_ILLEGAL])

        if act == RP_ACT_BIND_ROLE_PERMISSION:
            # 解绑旧的角色-权限关系
            tool.unbind_role_permission(item_in.role_ids, item_in.permission_ids, userinfo, conn)

        # 绑定新的角色-权限关系
        tool.bind_role_permission(item_in.role_ids, item_in.permission_ids, userinfo, conn)

    return ItemOutOperateSuccess()
