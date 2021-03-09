# -*- coding: utf-8 -*-

from models.mysql.system import t_menu, SystemEngine


HOME = 'HOME'
SETTING = 'SETTING'
MENU_MANAGE = 'MENU_MANAGE'
OPERATION_MANAGE = 'OPERATION_MANAGE'
USER_MANAGE = 'USER_MANAGE'
GROUP_MANAGE = 'GROUP_MANAGE'
ROLE_MANAGE = 'ROLE_MANAGE'
PERMISSION_MANAGE = 'PERMISSION_MANAGE'


class TableMenu(SystemEngine):
    table = t_menu
