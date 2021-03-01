# -*- coding: utf-8 -*-

from pydantic import BaseModel
from typing import Optional, List

from fastapi import Body

from commons.func import REGEX_UPPER_OR_UNDERLINE

from handlers.items import ItemIn, ItemOut, ListData


class ItemInAddGroup(ItemIn):
    pid: Optional[int] = Body(None, description='父级用户组ID')
    name: Optional[str] = Body(..., description='用户组，必需', min_length=1, max_length=20)
    code: Optional[str] = Body(..., description='用户组CODE码', max_length=50, regex=REGEX_UPPER_OR_UNDERLINE)
    intro: Optional[str] = Body(None, description='用户组简介')
    role_id: Optional[int] = Body(None, description='用户角色')


class ItemOutGroup(BaseModel):
    id: Optional[int] = Body(None, description='用户组ID')
    name: Optional[str] = Body(None, description='用户组')
    code: Optional[str] = Body(None, description='用户组唯一标识')
    intro: Optional[str] = Body(None, description='用户组简介')
    status: Optional[int] = Body(None, description='用户组状态')
    sub_status: Optional[int] = Body(None, description='用户组子状态')


class ListDataGroup(ListData):
    result: List[ItemOutGroup]


class ItemOutGroupList(ItemOut):
    """
    用户组列表响应模型
    """
    data: Optional[ListDataGroup]


class ItemInEditGroup(ItemIn):
    pid: Optional[int] = Body(None, description='父级用户组ID')
    name: Optional[str] = Body(None, description='用户组', min_length=1, max_length=20)
    intro: Optional[str] = Body(None, description='用户组简介')
    role_id: Optional[int] = Body(None, description='用户角色')


class ItemInBindGroupRole(ItemIn):
    group_id: Optional[int] = Body(..., description='用户组ID，必需')
    role_id: Optional[int] = Body(..., description='角色ID，必需')
