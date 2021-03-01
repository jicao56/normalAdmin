# -*- coding: utf-8 -*-

from pydantic import BaseModel
from typing import Optional, List

from fastapi import Body

from settings import settings

from commons.const import RESP_CODE_SUCCESS
from commons.func import REGEX_UPPER_OR_UNDERLINE, REGEX_MOBILE, REGEX_EMAIL


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


class ListData(BaseModel):
    p: Optional[int] = Body(0, description='第几页')
    ps: Optional[int] = Body(0, description='每页条数')
    total: Optional[int] = Body(0, description='总数')
