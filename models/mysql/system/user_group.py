# -*- coding: utf-8 -*-

from models.mysql.system import t_user_group, SystemEngine


class TableUserGroup(SystemEngine):
    table = t_user_group
