# -*- coding: utf-8 -*-
from fastapi import APIRouter, Request, Header, Depends

from commons.code import HTTP_500_INTERNAL_SERVER_ERROR
from settings.my_settings import settings_my
from handlers.const import *
from handlers.items import ItemOut
from handlers.items.config import ItemOutFavicon, ItemFavicon
from handlers.exp import MyError

from utils.my_logger import logger


router = APIRouter(tags=[TAGS_BASE])


@router.get("/captcha_required", name='登录是否需要验证码')
async def is_captcha_required():
    return ItemOut(data={"required": settings_my.captcha_required})


@router.get("/default_template", name='默认模板')
async def get_default_template():
    return ItemOut(data={"template": settings_my.web_default_template})


@router.get("/web_name", name='获取网站名称')
async def get_web_name():
    return ItemOut(data={"web_name": settings_my.web_name})


@router.get("/favicon",  name='获取网站图标')
async def get_favicon():
    """
    获取网站图标\n
    :return:
    """
    try:
        return ItemOutFavicon(data=ItemFavicon(favicon=settings_my.web_favicon))
    except MyError as me:
        logger.error(str(me))
        raise me
    except Exception as ex:
        logger.error(str(ex))
        raise MyError(code=HTTP_500_INTERNAL_SERVER_ERROR, msg='internal server error')



# async def get_ip(req: Request, head: Header):
#     """
#     根据header头中传过来的token，鉴权
#     :param token:
#     :return:
#     """
#     print(req)
#     print(head)
#
#
# @router.get("/ip",  name='ip', dependencies=[Depends(get_ip)])
# async def get_favicon():
#     """
#     获取网站图标\n
#     :return:
#     """
#
#     print(111)

