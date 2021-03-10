# -*- coding: utf-8 -*-

from typing import List
from fastapi import Body
from handlers.items import ItemIn


class ItemInBindUserRole(ItemIn):
    user_ids: List[int] = Body([], description='用户ID列表')
    role_ids: List[int] = Body([], description='角色ID列表')


class ItemInBindUserGroup(ItemIn):
    user_ids: List[int] = Body([], description='用户ID列表')
    group_ids: List[int] = Body([], description='用户组ID列表')


class ItemInBindGroupRole(ItemIn):
    group_ids: List[int] = Body([], description='用户组ID列表')
    role_ids: List[int] = Body([], description='角色ID列表')


class ItemInBindRolePermission(ItemIn):
    role_ids: List[int] = Body([], description='角色ID列表')
    permission_ids: List[int] = Body([], description='权限ID列表')
