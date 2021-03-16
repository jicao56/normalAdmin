# -*- coding: utf-8 -*-
import json
from models.mysql.system.config import t_config, VAL_TYPE_STR, VAL_TYPE_FLOAT, VAL_TYPE_JSON, VAL_TYPE_INT
from models.mysql.system import db_engine, TABLE_SUB_STATUS_INVALID_DEL
from settings.my_settings import settings_my


# 初始化自定义配置
def init_my_settings():
    with db_engine.connect() as conn:
        sql = t_config.select().where(t_config.c.sub_status != TABLE_SUB_STATUS_INVALID_DEL)
        res = conn.execute(sql).fetchall() or []

    for item in res:
        set_val_for_my_settings(item.key, item.val, item.val_type)


def set_val_for_my_settings(key: str, val: str, val_type: int):
    """
    为my_settings对象设置属性
    :param key: 属性名
    :param val: 属性值
    :param val_type: 属性值类型
    :return:
    """
    if val_type == VAL_TYPE_STR:
        setattr(settings_my, key, str(val))
    elif val_type == VAL_TYPE_INT:
        setattr(settings_my, key, int(val))
    elif val_type == VAL_TYPE_FLOAT:
        setattr(settings_my, key, float(val))
    elif val_type == VAL_TYPE_JSON:
        setattr(settings_my, key, json.loads(val))
    else:
        setattr(settings_my, key, str(val))


def del_val_for_my_settings(key: str):
    """
    删除my_settings对象的属性
    :param key: 属性名
    :return:
    """
    delattr(settings_my, key)


# 初始化自定义配置
init_my_settings()
