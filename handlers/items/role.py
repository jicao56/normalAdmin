# -*- coding: utf-8 -*-

from pydantic import BaseModel
from typing import Optional, List

from fastapi import Body

from commons.func import REGEX_UPPER_OR_UNDERLINE

from handlers.items import ItemIn, ItemOut, ListData


class ItemInAddRole(ItemIn):
    pid: Optional[int] = Body(None, description='父级角色ID')
    name: Optional[str] = Body(..., description='角色，必需', max_length=20)
    code: Optional[str] = Body(..., description='角色CODE码', max_length=50, regex=REGEX_UPPER_OR_UNDERLINE)
    intro: Optional[str] = Body(None, description='角色简介')


class ItemInBindRolePermission(ItemIn):
    permission_id: Optional[int] = Body(..., description='权限ID')


class ItemOutRole(BaseModel):
    id: Optional[int] = Body(None, description='角色ID')
    name: Optional[str] = Body(None, description='角色')
    code: Optional[str] = Body(None, description='角色唯一标识')
    intro: Optional[str] = Body(None, description='角色简介')
    status: Optional[int] = Body(None, description='角色状态')
    sub_status: Optional[int] = Body(None, description='角色子状态')


class ListDataRole(ListData):
    result: List[ItemOutRole]


class ItemOutRoleList(ItemOut):
    """
    角色列表响应模型
    """
    data: Optional[ListDataRole]


class ItemInEditRole(ItemIn):
    pid: Optional[int] = Body(None, description='父级角色ID')
    name: Optional[str] = Body(None, description='角色', min_length=1, max_length=20)
    intro: Optional[str] = Body(None, description='角色简介')


class ItemInBindGroupRole(ItemIn):
    group_id: Optional[int] = Body(..., description='角色ID，必需')
    role_id: Optional[int] = Body(..., description='角色ID，必需')
