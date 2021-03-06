# -*- coding: utf-8 -*-

from sqlalchemy.sql import and_
from models.mysql import TABLE_SUB_STATUS_INVALID_DEL
from models.mysql.system import t_user, SystemEngine


class TableUser(SystemEngine):
    table = t_user

