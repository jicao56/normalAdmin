# -*- coding: utf-8 -*-

from models.mysql.system import t_role_permission, SystemEngine


class TableRolePermission(SystemEngine):
    table = t_role_permission
