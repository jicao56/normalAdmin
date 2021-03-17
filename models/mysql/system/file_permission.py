# -*- coding: utf-8 -*-

from models.mysql.system import t_file_permission, SystemEngine


class TableFilePermission(SystemEngine):
    table = t_file_permission
