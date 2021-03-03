# -*- coding: utf-8 -*-

from fastapi import HTTPException
from commons.code import HTTP_500_INTERNAL_SERVER_ERROR
from handlers.items import ItemOut


class MyException(HTTPException):
    """
    自定义异常
    """
    def __init__(self, status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail={'code': '500', 'msg': 'internal server error'}):
        self.status_code = status_code

        if isinstance(detail, ItemOut):
            detail = detail.dict()

        if isinstance(detail, dict):
            # 对于异常来说，只需要返回状态码和提示信息即可
            detail.pop('data', None)
            detail.pop('extra', None)
        self.detail = detail
