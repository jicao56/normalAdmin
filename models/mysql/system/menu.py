# -*- coding: utf-8 -*-

from models.mysql.system import t_menu, SystemEngine

# 主页菜单
HOME = 'HOME'
# 设置菜单
SETTING = 'SETTING'
# 用户管理菜单
USER_MANAGE = 'USER_MANAGE'
# 用户组管理菜单
GROUP_MANAGE = 'GROUP_MANAGE'
# 角色管理菜单
ROLE_MANAGE = 'ROLE_MANAGE'
# 权限管理菜单
PERMISSION_MANAGE = 'PERMISSION_MANAGE'
# 系统管理菜单
CONFIG_MANAGE = 'CONFIG_MANAGE'
# 菜单管理菜单
MENU_MANAGE = 'MENU_MANAGE'
# 操作管理菜单
OPERATION_MANAGE = 'OPERATION_MANAGE'


class TableMenu(SystemEngine):
    table = t_menu
