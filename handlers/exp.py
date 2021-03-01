# -*- coding: utf-8 -*-

from fastapi import HTTPException
from commons.const import HTTP_200_OK
from handlers.items import ItemOut


class MyException(HTTPException):
    """
    自定义异常
    """
    def __init__(self, status_code=HTTP_200_OK, detail={}):
        self.status_code = status_code

        if isinstance(detail, ItemOut):
            detail = detail.dict()

        if isinstance(detail, dict):
            # 对于异常来说，只需要返回状态码和提示信息即可
            detail.pop('data', None)
            detail.pop('extra', None)
        self.detail = detail
