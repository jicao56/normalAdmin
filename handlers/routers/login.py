# -*- coding: utf-8 -*-
from io import BytesIO
import json
import uuid
import base64
from sqlalchemy import select
from captcha.image import ImageCaptcha
from fastapi import APIRouter

from commons.code import *
from commons.func import md5

from models.redis.system import redis_conn

from models.mysql.system import db_engine, t_account, t_user
from models.mysql import *

from handlers import tool
from handlers.items.login import ItemCaptcha, ItemInLogin, ItemOutCaptcha, ItemOutLogin, ItemLogin
from handlers.exp import MyError
from handlers.const import *

from settings.my_settings import settings_my


router = APIRouter(tags=[TAGS_LOGIN])


@router.post("/login", response_model=ItemOutLogin, name='登录')
async def login(item_in: ItemInLogin):
    # 响应模型
    item_out = ItemOutLogin()
    print(settings_my.redis_captcha_key.format(item_in.captcha_key))

    # 缓存中取验证码
    captcha_cache = redis_conn.get(settings_my.redis_captcha_key.format(item_in.captcha_key))

    if not captcha_cache:
        # 未取到验证码
        raise MyError(code=RESP_CODE_CAPTCHA_EXPIRE, msg='验证码已失效')

    # 检查验证码是否正确
    if captcha_cache != item_in.captcha_val:
        raise MyError(code=RESP_CODE_CAPTCHA_ERROR, msg='验证码错误')

    with db_engine.connect() as conn:
        # 检查账号
        account_sql = select([
            t_account.c.user_id,
            t_account.c.open_code,
            t_account.c.category,
            t_account.c.status
        ]).where(t_account.c.open_code == item_in.open_code).limit(1)
        account_res = conn.execute(account_sql).fetchone()
        if not account_res:
            # 账号不存在
            raise MyError(code=RESP_CODE_ACCOUNT_EXIST_NOT, msg='账号不存在')
        if account_res.status != TABLE_STATUS_VALID:
            # 账号无效
            raise MyError(code=RESP_CODE_ACCOUNT_EXIST_NOT, msg='账号无效')

        # 检查用户
        user_sql = select([
            t_user.c.id,
            t_user.c.name,
            t_user.c.head_img_url,
            t_user.c.mobile,
            t_user.c.password,
            t_user.c.salt,
            t_user.c.status
        ]).where(t_user.c.id == account_res.user_id).limit(1)
        user_res = conn.execute(user_sql).fetchone()
        if not user_res:
            # 用户不存在
            raise MyError(code=RESP_CODE_ACCOUNT_EXIST_NOT, msg='用户不存在')

        if user_res.status != TABLE_STATUS_VALID:
            # 用户无效
            raise MyError(code=RESP_CODE_ACCOUNT_EXIST_NOT, msg='用户无效')

        # 检查密码是否正确
        password = md5(item_in.password, user_res.salt)
        if password != user_res.password:
            # 密码不正确
            raise MyError(code=RESP_CODE_ACCOUNT_EXIST_NOT, msg='登录密码错误')

    # 所有验证项都通过

    # 存入缓存中的用户信息
    userinfo_cache = {
        'id': user_res.id,
        'open_code': account_res.open_code,
        'category': account_res.category,
        'name': user_res.name,
        'head_img_url': user_res.head_img_url,
        'mobile': user_res.mobile,
    }
    # 存入缓存中的用户信息的key，即token
    token = tool.create_token(user_res.id)
    token_key = settings_my.redis_token_key.format(token)
    redis_conn.setex(token_key, settings_my.redis_token_expire_time, json.dumps(userinfo_cache))

    # 回传的用户信息
    userinfo_back = {
        'id': user_res.id,
        'open_code': account_res.open_code,
        'name': user_res.name,
        'head_img_url': user_res.head_img_url,
        'mobile': user_res.mobile,
        'token': token,
        'expire': settings_my.redis_token_expire_time,
    }
    item_out.data = ItemLogin(**userinfo_back)
    item_out.msg = '登录成功'
    return item_out


@router.get("/captcha", response_model=ItemOutCaptcha, name='获取验证码')
async def get_captcha():
    """
    获取验证码\n
    :return: 返回的是base64编码的验证码内容
    """
    item_out = ItemOutCaptcha()
    # 随机取验证码
    code = tool.get_rand_str(settings_my.web_captcha_length)

    # 定义该验证码的缓存key
    captcha_name = uuid.uuid4()
    # 验证码入缓存，不区分大小写
    redis_conn.setex(settings_my.redis_captcha_key.format(captcha_name), settings_my.redis_captcha_expire_time, code.lower())

    # 声明验证码图形对象
    image = ImageCaptcha()

    # 生成给定字符的图像验证码
    data2 = image.create_captcha_image(code, color='red', background='white')
    buffer = BytesIO()
    data2.save(buffer, format='PNG')
    item_out.data = ItemCaptcha(
        key=str(captcha_name),
        val=base64.b64encode(buffer.getvalue()),
        expire=settings_my.redis_captcha_expire_time
    )
    return item_out


