# -*- coding: utf-8 -*-

from models.mysql.system import t_account, SystemEngine


class TableAccount(SystemEngine):
    table = t_account
