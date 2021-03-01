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
    mobile: Optional[str] = Body(None, description='用户手机号', min_length=11, max_length=11, regex=REGEX_MOBILE)
    email: Optional[str] = Body(None, description='邮箱', regex=REGEX_EMAIL)
    password: Optional[str] = Body(settings.web.user_default_password, description='用户密码')
    role_id: Optional[int] = Body(None, description='用户角色')
    group_id: Optional[int] = Body(None, description='用户所属组')


class ItemInEditUser(ItemIn):
    name: Optional[str] = Body(None, description='用户名，必需', min_length=1, max_length=20)
    head_img_url: Optional[str] = Body(None, description='用户头像', max_length=50)
    mobile: Optional[str] = Body(None, description='用户手机号', min_length=11, max_length=11, regex=REGEX_MOBILE)
    email: Optional[str] = Body(None, description='邮箱', regex=REGEX_EMAIL)
    password: Optional[str] = Body(None, description='用户密码')
    role_id: Optional[int] = Body(None, description='用户角色')
    group_id: Optional[int] = Body(None, description='用户所属组')


class ItemInBindUserGroup(ItemIn):
    user_id: Optional[int] = Body(..., description='用户id，必需', gt=0)
    group_id: Optional[int] = Body(..., description='用户组id，必需', gt=0)


class ItemInBindUserRole(ItemIn):
    user_id: Optional[int] = Body(..., description='用户id，必需', gt=0)
    role_id: Optional[int] = Body(..., description='角色id，必需', gt=0)


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


class ListDataUser(ListData):
    result: List[ItemOutUser]


class ItemOutUserList(ItemOut):
    """
    列表响应模型
    """
    data: Optional[ListDataUser]
