# -*- coding: utf-8 -*-

from pydantic import BaseModel
from typing import Optional, List

from fastapi import Body

from settings import settings

from commons.const import RESP_CODE_SUCCESS
from commons.func import REGEX_MUST_UPPER, REGEX_MOBILE, REGEX_EMAIL


class ItemIn(BaseModel):
    """
    请求参数模型
    """

    def __getattribute__(self, attr):
        attr_val = object.__getattribute__(self, attr)
        if isinstance(attr_val, str):
            attr_val = attr_val.strip()
        return attr_val


class ItemOut(BaseModel):
    """
    响应模型
    """
    code: Optional[str] = Body(RESP_CODE_SUCCESS, description='自定义状态码')
    msg: Optional[str] = Body('success', description='描述')
    data: Optional[dict] = Body({}, description='响应数据')
    extra: Optional[dict] = Body({}, description='附加数据')


class ItemOutOperateSuccess(BaseModel):
    """
    操作成功的提示
    """
    code: Optional[str] = Body(RESP_CODE_SUCCESS, description='状态码')
    msg: Optional[str] = Body('success', description='描述')


class ItemOutOperateFailed(BaseModel):
    """
    操作失败的提示
    """
    code: Optional[str] = Body('', description='状态码')
    msg: Optional[str] = Body('success', description='描述')


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


class ItemLogin(BaseModel):
    id: Optional[int] = Body(0, description='用户ID')
    open_code: Optional[str] = Body('', description='登录账号')
    name: Optional[str] = Body('', description='用户名')
    head_img_url: Optional[str] = Body('', description='用户头像')
    mobile: Optional[str] = Body('', description='用户手机号')
    token: Optional[str] = Body('', description='token')


class ItemOutLogin(ItemOut):
    data: Optional[ItemLogin]


class ItemMenu(BaseModel):
    id: Optional[int] = Body(0, description='菜单ID')
    pid: Optional[int] = Body(0, description='父级菜单ID')
    code: Optional[str] = Body('', description='菜单唯一标识')
    title: Optional[str] = Body('', description='菜单名')
    href: Optional[str] = Body('', description='菜单链接')
    intro: Optional[str] = Body('', description='菜单介绍')


class ItemMenus(ItemMenu):
    child: List[ItemMenu] = Body([], description='子菜单')


class ItemOutMenus(ItemOut):
    """
    菜单列表响应模型
    """
    code: Optional[str] = Body(RESP_CODE_SUCCESS, description='自定义状态码')
    msg: Optional[str] = Body('success', description='描述')
    data: List[ItemMenus] = Body([], description='菜单列表')


class ItemInLogin(ItemIn):
    open_code: Optional[str] = Body(..., description='登录账号')
    password: Optional[str] = Body(..., description='登录密码')
    captcha_key: Optional[str] = Body(..., description='验证码KEY')
    captcha_val: Optional[str] = Body(..., description='验证码值')


class ItemInAddMenu(ItemIn):
    pid: Optional[int] = Body(0, description='所属父级菜单ID')
    code: Optional[str] = Body(..., title='菜单唯一CODE代码', description='必需，必须大写，最大长度不超过20', min_length=1, max_length=20, regex=REGEX_MUST_UPPER)
    name: Optional[str] = Body(..., description='菜单名称，必需', min_length=1, max_length=20)
    uri: Optional[str] = Body(None, description='菜单uri', max_length=255)
    intro: Optional[str] = Body(None, description='菜单介绍', max_length=255)


class ItemInEditMenu(ItemIn):
    pid: Optional[int] = Body(None, description='所属父级菜单ID')
    code: Optional[str] = Body(None, title='菜单唯一CODE代码', description='必需，必须大写，最大长度不超过20', min_length=1, max_length=20, regex=REGEX_MUST_UPPER)
    name: Optional[str] = Body(None, description='菜单名称，必需', min_length=1, max_length=20)
    uri: Optional[str] = Body(None, description='菜单uri，必需', min_length=1, max_length=255)
    intro: Optional[str] = Body(None, description='菜单介绍', max_length=255)


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



class ListData(BaseModel):
    p: Optional[int] = Body(0, description='第几页')
    ps: Optional[int] = Body(0, description='每页条数')
    total: Optional[int] = Body(0, description='总数')


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
    data: Optional[ListDataUser]
