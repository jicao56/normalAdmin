# -*- coding: utf-8 -*-

from models.mysql.system import t_operation_permission, SystemEngine


class TableOperationPermission(SystemEngine):
    table = t_operation_permission
