# -*- coding: utf-8 -*-

from pydantic import BaseModel
from typing import Optional, List

from fastapi import Body

from settings import settings

from commons.func import REGEX_MOBILE, REGEX_EMAIL

from handlers.items import ItemIn, ItemOut, ListData


class ItemInAddUser(ItemIn):
    name: Optional[str] = Body(..., description='用户名，必需', min_length=1, max_length=20)
    head_img_url: Optional[str] = Body(None, description='用户头像', max_length=50)
    mobile: Optional[str] = Body(None, description='用户手机号', regex=REGEX_MOBILE)
    email: Optional[str] = Body(None, description='邮箱', regex=REGEX_EMAIL)
    password: Optional[str] = Body(settings.web_user_default_password, description='用户密码')
    role_ids: List[int] = Body([], description='用户角色ID列表')
    group_ids: List[int] = Body([], description='用户所属组ID列表')


class ItemInEditUser(ItemIn):
    name: Optional[str] = Body(None, description='用户名，必需', min_length=1, max_length=20)
    head_img_url: Optional[str] = Body(None, description='用户头像', max_length=50)
    mobile: Optional[str] = Body(None, description='用户手机号', regex=REGEX_MOBILE)
    email: Optional[str] = Body(None, description='邮箱', regex=REGEX_EMAIL)
    password: Optional[str] = Body(None, description='用户密码')
    role_ids: List[int] = Body([], description='用户角色ID列表')
    group_ids: List[int] = Body([], description='用户所属组ID列表')


class ItemInBindUserGroup(ItemIn):
    user_ids: List[int] = Body(..., description='用户ID列表，必需')
    group_ids: List[int] = Body(..., description='用户组ID列表，必需')


class ItemInBindUserRole(ItemIn):
    user_ids: List[int] = Body(..., description='用户ID列表，必需')
    role_ids: List[int] = Body(..., description='角色ID列表，必需')


class ItemOutUserGroup(BaseModel):
    id: Optional[int] = Body(None, description='用户组ID')
    name: Optional[str] = Body(None, description='用户组')
    code: Optional[str] = Body('', description='用户组唯一标识')
    intro: Optional[str] = Body(None, description='用户组简介')


class ItemOutUserRole(BaseModel):
    id: Optional[int] = Body(None, description='角色ID')
    pid: Optional[int] = Body(None, description='父级角色ID')
    name: Optional[str] = Body(None, description='角色名称')
    code: Optional[str] = Body('', description='角色唯一标识')
    intro: Optional[str] = Body(None, description='角色简介')
    is_super: Optional[int] = Body(None, description='是否超管  0-否  1-是')


class ItemOutUser(BaseModel):
    """
    用户列表响应模型
    """
    id: Optional[int] = Body(0, description='用户id')
    name: Optional[str] = Body(None, description='用户名')
    head_img_url: Optional[str] = Body(None, description='用户头像')
    mobile: Optional[str] = Body(None, description='用户手机号')
    status: Optional[int] = Body(None, description='用户状态')
    sub_status: Optional[int] = Body(None, description='用户子状态')
    groups: List[ItemOutUserGroup]
    roles: List[ItemOutUserRole]


class ListDataUser(ListData):
    result: List[ItemOutUser]


class ItemOutUserList(ItemOut):
    """
    列表响应模型
    """
    data: Optional[ListDataUser]


class ItemInUserAddGroups(ItemIn):
    group_ids: List[int] = Body(..., description='用户组ID列表，必需')


class ItemInUserAddRoles(ItemIn):
    role_ids: List[int] = Body(..., description='角色ID列表，必需')

