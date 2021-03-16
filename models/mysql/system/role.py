# -*- coding: utf-8 -*-

from models.mysql.system import t_role, SystemEngine


class TableRole(SystemEngine):
    table = t_role
