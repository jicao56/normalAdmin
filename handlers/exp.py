# -*- coding: utf-8 -*-

from fastapi import HTTPException
from commons.code import HTTP_200_OK
from handlers.items import ItemOut


class MyException(HTTPException):
    """
    自定义异常
    """
    def __init__(self, status_code=HTTP_200_OK, detail=None):
        self.status_code = status_code

        if not detail:
            self.detail = {'code': '500', 'msg': 'internal server error'}
        else:
            if isinstance(detail, ItemOut):
                detail = detail.dict()

            if isinstance(detail, dict):
                # 对于异常来说，只需要返回状态码和提示信息即可l
                detail.pop('data', None)
                detail.pop('extra', None)
            self.detail = detail


class MyError(MyException):
    """
    自定义
    """
    def __init__(self, code='', msg='', detail=None):
        super(MyError, self).__init__(detail=detail)
        if code:
            self.detail['code'] = code
        if msg:
            self.detail['msg'] = msg
