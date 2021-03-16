# -*- coding: utf-8 -*-

from models.mysql.system import t_user_role, SystemEngine


class TableUserRole(SystemEngine):
    table = t_user_role
