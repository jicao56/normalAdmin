# -*- coding: utf-8 -*-

from models.mysql.system import t_group, SystemEngine


class TableGroup(SystemEngine):
    table = t_group
