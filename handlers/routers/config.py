# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends, File, UploadFile

from commons.code import *

from settings.my_settings import settings_my
from models.mysql.system import db_engine, TABLE_STATUS_VALID, TABLE_SUB_STATUS_VALID
from models.mysql.system.permission import *
from models.mysql.system.config import *

from handlers.exp import MyError
from handlers import tool, set_val_for_my_settings
from handlers.const import *
from handlers.items.config import *
from handlers.items import ItemOutOperateSuccess

from utils.my_file import upload
from utils.my_logger import logger


router = APIRouter(tags=[TAGS_CONFIG], dependencies=[Depends(tool.check_token)])


@router.get("/logo", response_model=ItemOutLogo, name='获取logo')
async def get_logo(userinfo: dict = Depends(tool.get_userinfo_from_token)):
    """
    获取logo\n
    :param userinfo:\n
    :return:
    """
    # 鉴权
    tool.check_operation_permission(userinfo['id'], PERMISSION_FILE_VIEW)

    try:
        return ItemOutLogo(data=ItemLogo(logo=settings_my.web_logo))
    except MyError as me:
        logger.error(str(me))
        raise me
    except Exception as ex:
        logger.error(str(ex))
        raise MyError(code=HTTP_500_INTERNAL_SERVER_ERROR, msg='internal server error')


@router.post("/logo", response_model=ItemOutOperateSuccess, name='上传logo')
async def upload_logo(file: UploadFile = File(..., description='网站logo'), userinfo: dict = Depends(tool.get_userinfo_from_token)):
    """
    上传logo\n
    :param file:\n
    :param userinfo:\n
    :return:
    """
    # 鉴权
    tool.check_operation_permission(userinfo['id'], PERMISSION_FILE_UPLOAD)

    try:
        data = await file.read()
        filename = settings_my.web_logo or 'images/logo/logo.jpg'
        upload(data, filename)

        # 设置配置
        set_val_for_my_settings('web_logo', filename, VAL_TYPE_STR)
        return ItemOutLogo(data=ItemLogo(logo=filename))
    except MyError as me:
        logger.error(str(me))
        raise me
    except Exception as ex:
        logger.error(str(ex))
        raise MyError(code=HTTP_500_INTERNAL_SERVER_ERROR, msg='internal server error')


@router.get("/favicon", response_model=ItemOutFavicon, name='获取网站图标')
async def get_favicon(userinfo: dict = Depends(tool.get_userinfo_from_token)):
    """
    获取网站图标\n
    :param userinfo:\n
    :return:
    """
    # 鉴权
    tool.check_operation_permission(userinfo['id'], PERMISSION_FILE_VIEW)

    try:
        return ItemOutFavicon(data=ItemFavicon(favicon=settings_my.web_favicon))
    except MyError as me:
        logger.error(str(me))
        raise me
    except Exception as ex:
        logger.error(str(ex))
        raise MyError(code=HTTP_500_INTERNAL_SERVER_ERROR, msg='internal server error')


@router.post("/favicon", response_model=ItemOutOperateSuccess, name='上传网站图标')
async def upload_favicon(file: UploadFile = File(..., description='网站图标'), userinfo: dict = Depends(tool.get_userinfo_from_token)):
    """
    上传网站图标\n
    :param file:\n
    :param userinfo:\n
    :return:
    """
    # 鉴权
    tool.check_operation_permission(userinfo['id'], PERMISSION_FILE_UPLOAD)

    try:
        data = await file.read()
        filename = settings_my.web_favicon or 'images/ico/favicon.ico'
        upload(data, filename)

        # 设置配置
        set_val_for_my_settings('web_favicon', filename, VAL_TYPE_STR)

        return ItemOutFavicon(data=ItemFavicon(favicon=filename))
    except MyError as me:
        logger.error(str(me))
        raise me
    except Exception as ex:
        logger.error(str(ex))
        raise MyError(code=HTTP_500_INTERNAL_SERVER_ERROR, msg='internal server error')


@router.get("/sys_param", name='获取系统参数', response_model=ItemOutSysParam)
async def get_sys_param(userinfo: dict = Depends(tool.get_userinfo_from_token)):
    # 鉴权
    tool.check_operation_permission(userinfo['id'], PERMISSION_CONFIG_VIEW)

    return ItemOutSysParam(data=ItemSysParam(
        web_name=settings_my.web_name,
        web_favicon=settings_my.web_favicon,
        web_logo=settings_my.web_logo,
        token_expire_time=settings_my.token_expire_time,
        captcha_required=settings_my.captcha_required,
        captcha_type=settings_my.captcha_type,
        web_copyright=settings_my.web_copyright,
    ))


@router.post("/sys_param", name='设置系统参数', response_model=ItemOutSysParam)
async def get_sys_param(item_in: ItemSysParam, userinfo: dict = Depends(tool.get_userinfo_from_token)):
    # 鉴权
    tool.check_operation_permission(userinfo['id'], PERMISSION_CONFIG_EDIT)

    insert_list = []
    update_list = []
    conn = db_engine.connect()

    try:
        # 查找通用配置
        for key, val in item_in.__dict__.items():
            if val:
                if isinstance(val, str):
                    val_type = VAL_TYPE_STR
                elif isinstance(val, int):
                    val_type = VAL_TYPE_INT
                else:
                    val_type = VAL_TYPE_STR

                config_sql = t_config.select().where(t_config.c.key == key).limit(1).with_for_update()
                config_obj = conn.execute(config_sql).fetchone()
                if not config_obj:
                    # 配置不存在，新增
                    insert_list.append({
                        'key': key,
                        'val': val,
                        'val_type': val_type,
                        'creator': userinfo['name']
                    })
                else:
                    # 配置存在，更新
                    update_list.append({
                        'id': config_obj.id,
                        'key': key,
                        'val': val,
                        'val_type': val_type,
                        'editor': userinfo['name'],
                        'status': TABLE_STATUS_VALID,
                        'sub_status': TABLE_SUB_STATUS_VALID
                    })

        if insert_list:
            # 新增配置
            update_config_sql = t_config.insert().values(insert_list)
            conn.execute(update_config_sql)
            # 修改配置属性值
            for config in insert_list:
                set_val_for_my_settings(config.get('key'), config.get('val'), config.get('val_type'))

        for config in update_list:
            update_config_sql = t_config.update().where(t_config.c.id == config.pop('id')).values(config)
            conn.execute(update_config_sql)
            # 修改配置属性值
            set_val_for_my_settings(config.get('key'), config.get('val'), config.get('val_type'))

        return ItemOutSysParam(data=ItemSysParam(
            web_name=settings_my.web_name,
            web_favicon=settings_my.web_favicon,
            web_logo=settings_my.web_logo,
            token_expire_time=settings_my.token_expire_time,
            captcha_required=settings_my.captcha_required,
            captcha_type=settings_my.captcha_type,
            web_copyright=settings_my.web_copyright,
        ))
    except Exception as ex:
        logger.error(str(ex))
        raise MyError(code=HTTP_500_INTERNAL_SERVER_ERROR, msg='internal server error')
    finally:
        conn.close()
