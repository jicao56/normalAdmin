# -*- coding: utf-8 -*-

from pydantic import BaseModel
from typing import Optional, List

from fastapi import Body

from commons.func import REGEX_UPPER_OR_UNDERLINE

from handlers.items import ItemIn, ItemOut, ListData


class ItemInAddPermission(ItemIn):
    pid: Optional[int] = Body(None, description='父级权限ID')
    name: Optional[str] = Body(..., description='权限，必需', max_length=20)
    code: Optional[str] = Body(..., description='权限CODE码', max_length=50, regex=REGEX_UPPER_OR_UNDERLINE)
    intro: Optional[str] = Body(None, description='权限简介')
    category: Optional[int] = Body(1, description='权限类别  1-菜单访问权限；2-页面元素可见性权限；3-功能模块操作权限；4-文件修改权限；')


class ItemOutPermission(BaseModel):
    id: Optional[int] = Body(None, description='权限ID')
    name: Optional[str] = Body(None, description='权限')
    code: Optional[str] = Body(None, description='权限唯一标识')
    intro: Optional[str] = Body(None, description='权限简介')
    category: Optional[int] = Body(None, description='权限类别  1-菜单访问权限；2-页面元素可见性权限；3-功能模块操作权限；4-文件修改权限；')
    status: Optional[int] = Body(None, description='权限状态')
    sub_status: Optional[int] = Body(None, description='权限子状态')


class ListDataPermission(ListData):
    result: List[ItemOutPermission]


class ItemOutPermissionList(ItemOut):
    """
    权限列表响应模型
    """
    data: Optional[ListDataPermission]


class ItemInEditPermission(ItemIn):
    pid: Optional[int] = Body(None, description='父级权限ID')
    name: Optional[str] = Body(None, description='权限', min_length=1, max_length=20)
    intro: Optional[str] = Body(None, description='权限简介')
    category: Optional[int] = Body(None, description='权限类别  1-菜单访问权限；2-页面元素可见性权限；3-功能模块操作权限；4-文件修改权限；')


class ItemInBindGroupPermission(ItemIn):
    group_id: Optional[int] = Body(..., description='权限ID，必需')
    permission_id: Optional[int] = Body(..., description='权限ID，必需')
