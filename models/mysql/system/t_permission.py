# -*- coding: utf-8 -*-

from models.mysql.system import t_permission, SystemEngine


class TablePermission(SystemEngine):
    table = t_permission
