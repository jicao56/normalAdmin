# -*- coding: utf-8 -*-

from models.mysql.system import t_group_role, SystemEngine


class TableGroupRole(SystemEngine):
    table = t_group_role
