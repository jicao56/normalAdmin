# -*- coding: utf-8 -*-
import os
from typing import Optional
from sqlalchemy import func, select
from sqlalchemy.sql import and_
from fastapi import APIRouter, Depends, Query, File, UploadFile

from commons.code import *

from models.redis.system import redis_conn

from settings.my_settings import settings_my
from models.mysql.system import db_engine, TABLE_SUB_STATUS_INVALID_DEL, TABLE_STATUS_INVALID, TABLE_STATUS_VALID, TABLE_SUB_STATUS_VALID
from models.mysql.system.permission import *
from models.mysql.system.config import *

from handlers.exp import MyError
from handlers import tool, set_val_for_my_settings, del_val_for_my_settings
from handlers.const import *
from handlers.items.config import *
from handlers.items import ItemOutOperateSuccess, ItemOutOperateFailed

from utils.my_file import upload
from utils.my_logger import logger


router = APIRouter(tags=[TAGS_CONFIG], dependencies=[Depends(tool.check_token)])


# @router.get("/config", name='获取通用配置')
# async def get_config(userinfo: dict = Depends(tool.get_userinfo_from_token), page: Optional[int] = Query(settings_my.web_page, description='第几页'), limit: Optional[int] = Query(settings_my.web_page_size, description='每页条数')):
#     # 返回模型
#     item_out = ItemOutConfigList()
#
#     # 鉴权
#     tool.check_operation_permission(userinfo['id'], PERMISSION_CONFIG_VIEW)
#
#     with db_engine.connect() as conn:
#         # 获取当前有多少数据
#         count_sql = select([func.count(t_config.c.id)]).where(t_config.c.sub_status != TABLE_SUB_STATUS_INVALID_DEL)
#         total = conn.execute(count_sql).scalar()
#
#         # 获取分页后的通用配置列表
#         config_sql = select([
#             t_config.c.id,
#             t_config.c.key,
#             t_config.c.val,
#             t_config.c.val_type,
#             t_config.c.intro,
#             t_config.c.status,
#             t_config.c.sub_status,
#         ]).where(t_config.c.sub_status != TABLE_SUB_STATUS_INVALID_DEL).order_by('sort', 'id')
#
#         if page != 0:
#             config_sql = config_sql.limit(limit).offset((page - 1) * limit)
#         config_obj_list = conn.execute(config_sql).fetchall()
#
#     item_out.data = ListDataConfig(
#         result=[ItemOutConfig(
#             id=config_obj.id,
#             key=config_obj.key,
#             val=config_obj.val,
#             val_type=config_obj.val_type,
#             intro=config_obj.intro,
#             status=config_obj.status,
#             sub_status=config_obj.sub_status,
#         ) for config_obj in config_obj_list],
#         total=total,
#         page=page,
#         limit=limit,
#     )
#     return item_out
#
#
# @router.post("/config", response_model=ItemOutOperateSuccess, name='添加通用配置')
# async def add_config(item_in: ItemInAddConfig, userinfo: dict = Depends(tool.get_userinfo_from_token)):
#     """
#     添加通用配置\n
#     :param item_in:\n
#     :param userinfo:\n
#     :return:
#     """
#
#     # 鉴权
#     tool.check_operation_permission(userinfo['id'], PERMISSION_CONFIG_ADD)
#
#     with db_engine.connect() as conn:
#         # 查看是否已经有该code的通用配置
#         if not tool.is_code_unique(t_config, item_in.key, conn):
#             raise MyError(code=MULTI_DATA, msg='配置key重复')
#
#         # 新增通用配置
#         config_sql = t_config.insert().values({
#             'key': item_in.key,
#             'val': item_in.val,
#             'val_type': item_in.val_type,
#             'intro': item_in.intro,
#             'creator': userinfo['name']
#         })
#         conn.execute(config_sql)
#
#     # 添加属性
#     set_val_for_my_settings(item_in.key, item_in.val, item_in.val_type)
#
#     return ItemOutOperateSuccess()
#
#
# @router.put("/config/{config_id}", response_model=ItemOutOperateSuccess, name="修改通用配置")
# async def edit_config(config_id: int, item_in: ItemInEditConfig, userinfo: dict = Depends(tool.get_userinfo_from_token)):
#     """
#     修改通用配置\n
#     :param config_id:\n
#     :param item_in:\n
#     :param userinfo:\n
#     :return:
#     """
#     # 鉴权
#     tool.check_operation_permission(userinfo['id'], PERMISSION_CONFIG_EDIT)
#
#     with db_engine.connect() as conn:
#         # 查找通用配置
#         config_sql = t_config.select().where(t_config.c.id == config_id).limit(1).with_for_update()
#         config_obj = conn.execute(config_sql).fetchone()
#         if not config_obj:
#             raise MyError(code=HTTP_404_NOT_FOUND, msg='配置不存在')
#
#         # 修改通用配置
#         config_val = {
#             'editor': userinfo['name']
#         }
#
#         if item_in.val is not None:
#             config_val['val'] = item_in.val
#         if item_in.val_type is not None:
#             config_val['val_type'] = item_in.val_type
#         if item_in.intro is not None:
#             config_val['intro'] = item_in.intro
#
#         update_config_sql = t_config.update().where(t_config.c.id == config_id).values(config_val)
#         conn.execute(update_config_sql)
#
#     # 修改属性
#     if config_val.get('val') or config_val.get('val_type'):
#         set_val_for_my_settings(config_obj.key, config_val.get('val'), config_val.get('val_type'))
#
#     return ItemOutOperateSuccess()
#
#
# @router.delete("/config/{config_id}", name='删除通用配置')
# async def del_config(config_id: int, userinfo: dict = Depends(tool.get_userinfo_from_token)):
#     """
#     删除通用配置\n
#     :param config_id:\n
#     :param userinfo:\n
#     :return:
#     """
#     # 鉴权
#     tool.check_operation_permission(userinfo['id'], PERMISSION_CONFIG_DEL)
#
#     with db_engine.connect() as conn:
#         # 查找通用配置
#         config_sql = t_config.select().where(t_config.c.id == config_id).limit(1).with_for_update()
#         config = conn.execute(config_sql).fetchone()
#
#         # 修改通用配置状态为无效（软删除）
#         update_config_sql = t_config.update().where(and_(
#             t_config.c.id == config_id,
#             t_config.c.sub_status != TABLE_SUB_STATUS_INVALID_DEL,
#         )).values({
#             'status': TABLE_STATUS_INVALID,
#             'sub_status': TABLE_SUB_STATUS_INVALID_DEL
#         })
#         conn.execute(update_config_sql)
#
#     # 删除该属性
#     del_val_for_my_settings(config.key)
#
#     return ItemOutOperateSuccess()


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
        upload(data, settings_my.web_logo)

        return ItemOutLogo(data=ItemLogo(logo=settings_my.web_logo))
    except MyError as me:
        logger.error(str(me))
        raise me
    except Exception as ex:
        logger.error(str(ex))
        raise MyError(code=HTTP_500_INTERNAL_SERVER_ERROR, msg='internal server error')


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


@router.get("/sys_param", name='获取系统参数', response_model=ItemOutSysParam)
async def get_sys_param(userinfo: dict = Depends(tool.get_userinfo_from_token)):
    # 鉴权
    tool.check_operation_permission(userinfo['id'], PERMISSION_CONFIG_VIEW)

    return ItemOutSysParam(data=ItemSysParam(
        web_name=settings_my.web_name,
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
