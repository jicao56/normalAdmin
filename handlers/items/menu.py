# -*- coding: utf-8 -*-
from pydantic import BaseModel
from typing import Optional, List

from fastapi import Body

from commons.code import RESP_CODE_SUCCESS

from handlers.items import ItemIn, ItemOut, ListData


class ItemInAddMenu(ItemIn):
    pid: Optional[int] = Body(0, description='所属父级菜单ID')
    code: Optional[str] = Body(None, title='菜单唯一CODE代码')
    name: Optional[str] = Body(..., description='菜单名称，必需', min_length=1, max_length=20)
    uri: Optional[str] = Body(None, description='菜单uri', max_length=255)
    intro: Optional[str] = Body(None, description='菜单介绍', max_length=255)


class ItemInEditMenu(ItemIn):
    pid: Optional[int] = Body(None, description='所属父级菜单ID')
    code: Optional[str] = Body(None, title='菜单唯一CODE代码', description='必需，必须大写，最大长度不超过20')
    name: Optional[str] = Body(None, description='菜单名称，必需', min_length=1, max_length=20)
    uri: Optional[str] = Body(None, description='菜单uri，必需', min_length=1, max_length=255)
    intro: Optional[str] = Body(None, description='菜单介绍', max_length=255)


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
    id: Optional[int] = Body(None, description='菜单ID')
    pid: Optional[int] = Body(None, description='父级菜单ID')
    title: Optional[str] = Body(None, description='菜单名称')
    code: Optional[str] = Body('', description='菜单唯一标识')
    href: Optional[str] = Body('', description='菜单链接')
    intro: Optional[str] = Body(None, description='菜单简介')
    status: Optional[int] = Body(None, description='菜单状态')
    sub_status: Optional[int] = Body(None, description='菜单子状态')


class ListDataMenu(ListData):
    result: List[ItemOutMenus]


class ItemOutMenuList(ItemOut):
    """
    用户组列表响应模型
    """
    data: Optional[ListDataMenu]