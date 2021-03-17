# -*- coding: utf-8 -*-

from models.mysql.system import t_config, SystemEngine


VAL_TYPE_STR = 1
VAL_TYPE_INT = 2
VAL_TYPE_FLOAT = 3
VAL_TYPE_JSON = 4


class TableConfig(SystemEngine):
    table = t_config
