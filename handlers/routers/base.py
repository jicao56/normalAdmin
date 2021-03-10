# -*- coding: utf-8 -*-
from typing import Optional
from sqlalchemy import func, select
from sqlalchemy.sql import and_
from fastapi import APIRouter


from settings.my_settings import settings_my
from handlers.const import *
from handlers.items import ItemOut


router = APIRouter(tags=[TAGS_BASE])


@router.get("/captcha_required", name='登录是否需要验证码')
async def login_captcha_required():
    return ItemOut(data={"required": settings_my.login_captcha_required})


@router.get("/default_template", name='默认模板')
async def get_default_template():
    return ItemOut(data={"template": settings_my.web_default_template})

