# -*- coding: utf-8 -*-
from fastapi import APIRouter

from models.redis.system import redis_conn

from settings.my_settings import settings_my

from models.mysql import *

from handlers.const import *

router = APIRouter(tags=[TAGS_BASE])


@router.get("/check_token/{token}", name='验证token是否有效')
async def check_token(token: str):
    if not token:
        return {'code': '40001', 'msg': '参数必传'}
    token_key = settings_my.redis_token_key.format(token)
    token_exist = redis_conn.exists(token_key)
    if not token_exist:
        return {'code': '4000', 'msg': 'token失效'}

    return {'code': '10000', 'msg': 'success'}
