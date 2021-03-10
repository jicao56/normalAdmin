# -*- coding: utf-8 -*-
from typing import Optional

from fastapi import APIRouter
from fastapi import Depends, Header

from settings.my_settings import settings_my

from models.redis.system import redis_conn

from handlers import tool
from handlers.items import ItemOutOperateSuccess
from handlers.const import *

router = APIRouter(tags=[TAGS_LOGOUT], dependencies=[Depends(tool.check_token)])


@router.get("/logout", tags=[TAGS_LOGOUT], response_model=ItemOutOperateSuccess, name='注销')
async def logout(token: Optional[str] = Header(None)):
    """
    登出/退出/注销
    :param token:
    :return:
    """
    # 缓存中删除该token
    token_key = settings_my.token_key_format.format(token)
    redis_conn.delete(token_key)

    return ItemOutOperateSuccess(msg='注销成功')
