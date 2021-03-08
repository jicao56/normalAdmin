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
        if item.val_type == VAL_TYPE_STR:
            setattr(settings_my, item.key, str(item.val))
        elif item.val_type == VAL_TYPE_INT:
            setattr(settings_my, item.key, int(item.val))
        elif item.val_type == VAL_TYPE_FLOAT:
            setattr(settings_my, item.key, float(item.val))
        elif item.val_type == VAL_TYPE_JSON:
            setattr(settings_my, item.key, json.loads(item.val))


# 初始化自定义配置
init_my_settings()
