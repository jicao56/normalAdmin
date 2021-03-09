# -*- coding: utf-8 -*-

from pydantic import BaseModel
from typing import Optional, List
from fastapi import Body

from handlers.items import ItemIn, ItemOut, ListData


class ItemInAddGroup(ItemIn):
    pid: Optional[int] = Body(None, description='父级用户组ID')
    code: Optional[str] = Body(None, description='用户组CODE码', max_length=50)
    name: Optional[str] = Body(..., description='用户组，必需', min_length=1, max_length=20)
    intro: Optional[str] = Body(None, description='用户组简介')
    role_ids: List[int] = Body([], description='角色ID列表')


class ItemOutGroup(BaseModel):
    id: Optional[int] = Body(None, description='用户组ID')
    name: Optional[str] = Body(None, description='用户组')
    code: Optional[str] = Body('', description='用户组唯一标识')
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
    role_ids: List[int] = Body([], description='角色ID列表')


class ItemInBindGroupRole(ItemIn):
    group_ids: List[int] = Body(..., description='用户组ID列表，必需')
    role_ids: List[int] = Body(..., description='角色ID列表，必需')


class ItemInBindGroupUsers(ItemIn):
    user_ids: List[int] = Body(..., description='用户ID列表，必需')
