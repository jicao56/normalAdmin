# -*- coding: utf-8 -*-

from models.mysql.system import t_file, SystemEngine


class TableFile(SystemEngine):
    table = t_file
