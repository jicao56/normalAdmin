# -*- coding: utf-8 -*-

from models.mysql.system import t_user, SystemEngine


class TableUser(SystemEngine):
    table = t_user
