# -*- coding: utf-8 -*-

from pydantic import BaseModel
from typing import Optional, List

from fastapi import Body

from handlers.items import ItemIn, ItemOut


class ItemCaptcha(BaseModel):
    """
    验证码模型
    """
    key: Optional[str] = Body('', description='验证码key')
    val: Optional[bytes] = Body(b'', description='验证码值')
    expire: Optional[int] = Body(0, description='过期时间')


class ItemOutCaptcha(ItemOut):
    """
    验证码响应模型
    """
    data: Optional[ItemCaptcha]


class ItemInLogin(ItemIn):
    open_code: Optional[str] = Body(..., description='登录账号')
    password: Optional[str] = Body(..., description='登录密码')
    captcha_key: Optional[str] = Body(..., description='验证码KEY')
    captcha_val: Optional[str] = Body(..., description='验证码值')



class ItemLogin(BaseModel):
    id: Optional[int] = Body(0, description='用户ID')
    open_code: Optional[str] = Body('', description='登录账号')
    name: Optional[str] = Body('', description='用户名')
    head_img_url: Optional[str] = Body('', description='用户头像')
    mobile: Optional[str] = Body('', description='用户手机号')
    token: Optional[str] = Body('', description='token')


class ItemOutLogin(ItemOut):
    data: Optional[ItemLogin]
