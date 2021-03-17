# -*- coding: utf-8 -*-

from models.mysql.system import t_element_permission, SystemEngine


class TableElementPermission(SystemEngine):
    table = t_element_permission
