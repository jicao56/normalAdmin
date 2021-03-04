# -*- coding: utf-8 -*-

from pydantic import BaseModel
from typing import Optional, List

from fastapi import Body

from settings import settings

from commons.func import REGEX_MOBILE, REGEX_EMAIL

from handlers.items import ItemIn, ItemOut, ListData


class ItemInBindUserRole(ItemIn):
    user_ids: List[int] = Body(..., description='用户ID列表，必需')
    role_ids: List[int] = Body(..., description='角色ID列表，必需')


class ItemInUserAddGroups(ItemIn):
    group_ids: List[int] = Body(..., description='用户组ID列表，必需')


class ItemInUserAddRoles(ItemIn):
    role_ids: List[int] = Body(..., description='角色ID列表，必需')


class ItemInBindGroupRole(ItemIn):
    role_ids: List[int] = Body(..., description='角色ID列表，必需')


class ItemInBindRolePermission(ItemIn):
    group_ids: List[int] = Body(..., description='用户组ID列表，必需')
    role_ids: List[int] = Body(..., description='角色ID列表，必需')
