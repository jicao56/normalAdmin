# -*- coding: utf-8 -*-

from pydantic import BaseModel
from typing import Optional, List

from fastapi import Body

from commons.code import RESP_CODE_SUCCESS
from commons.funcs import chinese_to_upper_english


class ItemIn(BaseModel):
    """
    请求参数模型
    """
    sign: Optional[str] = Body(None, description='参数签名')

    def __getattribute__(self, attr):
        attr_val = object.__getattribute__(self, attr)
        if isinstance(attr_val, str):
            attr_val = attr_val.strip()

            if attr == 'code':
                if not attr_val:
                    # code没有值
                    # 取属性为name的值
                    name_val = object.__getattribute__(self, 'name')
                    if name_val:
                        # 如果有name的属性，且有值，将name值给code
                        attr_val = name_val

                # 将code值转换为大写
                attr_val = chinese_to_upper_english(attr_val)

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
    page: Optional[int] = Body(0, description='第几页')
    limit: Optional[int] = Body(0, description='每页条数')
    total: Optional[int] = Body(0, description='总数')
