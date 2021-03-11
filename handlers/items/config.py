# -*- coding: utf-8 -*-

from pydantic import BaseModel
from typing import Optional, List
from fastapi import Body

from handlers.items import ItemIn, ItemOut, ListData


class ItemInAddConfig(ItemIn):
    key: Optional[str] = Body(..., description='配置key，必需')
    val: Optional[str] = Body(..., description='配置值')
    val_type: Optional[int] = Body(1, description='值类型：1-字符串  2-整型  3-浮点型  4-json')
    intro: Optional[str] = Body(None, description='简介')


class ItemInEditConfig(ItemIn):
    val: Optional[str] = Body(None, description='配置值')
    val_type: Optional[int] = Body(None, description='值类型：1-字符串  2-整型  3-浮点型  4-json')
    intro: Optional[str] = Body(None, description='简介')


class ItemOutConfig(BaseModel):
    id: Optional[int] = Body(..., description='配置ID')
    key: Optional[str] = Body(..., description='配置key，必需')
    val: Optional[str] = Body('', description='配置值')
    val_type: Optional[int] = Body(None, description='值类型：1-字符串  2-整型  3-浮点型  4-json')
    intro: Optional[str] = Body(None, description='简介')
    status: Optional[int] = Body(None, description='用户组状态')
    sub_status: Optional[int] = Body(None, description='用户组子状态')


class ListDataConfig(ListData):
    result: List[ItemOutConfig]


class ItemOutConfigList(ItemOut):
    """
    用户组列表响应模型
    """
    data: Optional[ListDataConfig]


class ItemLogo(BaseModel):
    logo: str = Body(..., description='logo')


class ItemOutLogo(ItemOut):
    data: ItemLogo


class ItemSysParam(BaseModel):
    web_name: Optional[str] = Body(None, description='网站名称')
    web_logo: Optional[str] = Body(None, description='网站logo')
    token_expire_time: Optional[int] = Body(3600, description='值类型：1-字符串  2-整型  3-浮点型  4-json')
    captcha_required: Optional[int] = Body(1, description='登录是否需要验证码：1-需要；2-不需要')
    captcha_type: Optional[int] = Body(1, description='验证码类型：1-纯数字；2：纯英文；3-数字加英文')
    web_copyright: Optional[str] = Body(None, description='版权信息')


class ItemOutSysParam(ItemOut):
    data: ItemSysParam
