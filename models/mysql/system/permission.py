# -*- coding: utf-8 -*-

from models.mysql.system import t_permission, SystemEngine

# 权限类型
PERMISSION_CATEGORY_MENU = 1
PERMISSION_CATEGORY_ELEMENT = 2
PERMISSION_CATEGORY_OPERATION = 3
PERMISSION_CATEGORY_FILE = 4
PERMISSION_CATEGORY = {
    PERMISSION_CATEGORY_MENU: '菜单访问权限',
    PERMISSION_CATEGORY_ELEMENT: '页面元素可见性权限',
    PERMISSION_CATEGORY_OPERATION: '功能模块操作权限',
    PERMISSION_CATEGORY_FILE: '文件修改权限',
}

# 权限表code码
# 菜单访问权限code码
# 主页访问权限
PERMISSION_HOME_QUERY = 'PERMISSION_HOME_QUERY'
# 设置访问权限
PERMISSION_SETTING_QUERY = 'PERMISSION_SETTING_QUERY'
# 菜单管理访问权限
PERMISSION_MENU_QUERY = 'PERMISSION_MENU_QUERY'
# 操作管理访问权限
PERMISSION_OPERATION_QUERY = 'PERMISSION_OPERATION_QUERY'
# 用户管理访问权限
PERMISSION_USER_QUERY = 'PERMISSION_USER_QUERY'
# 用户组管理访问权限
PERMISSION_GROUP_QUERY = 'PERMISSION_GROUP_QUERY'
# 角色管理访问权限
PERMISSION_ROLE_QUERY = 'PERMISSION_ROLE_QUERY'
# 权限管理访问权限
PERMISSION_PERMISSION_QUERY = 'PERMISSION_PERMISSION_QUERY'
# 系统配置访问权限
PERMISSION_CONFIG_QUERY = 'PERMISSION_CONFIG_QUERY'
# 功能操作权限code码
# 菜单操作权限
PERMISSION_MENU_VIEW = 'PERMISSION_MENU_VIEW'
PERMISSION_MENU_ADD = 'PERMISSION_MENU_ADD'
PERMISSION_MENU_EDIT = 'PERMISSION_MENU_EDIT'
PERMISSION_MENU_DEL = 'PERMISSION_MENU_DEL'
PERMISSION_MENU_DISABLE = 'PERMISSION_MENU_DISABLE'
PERMISSION_MENU_ENABLE = 'PERMISSION_MENU_DISABLE'
# 权限的操作权限
PERMISSION_PERMISSION_VIEW = 'PERMISSION_PERMISSION_VIEW'
PERMISSION_PERMISSION_ADD = 'PERMISSION_PERMISSION_ADD'
PERMISSION_PERMISSION_EDIT = 'PERMISSION_PERMISSION_EDIT'
PERMISSION_PERMISSION_DEL = 'PERMISSION_PERMISSION_DEL'
PERMISSION_PERMISSION_DISABLE = 'PERMISSION_PERMISSION_DISABLE'
PERMISSION_PERMISSION_ENABLE = 'PERMISSION_PERMISSION_ENABLE'
# 用户的操作权限
PERMISSION_USER_VIEW = 'PERMISSION_USER_VIEW'
PERMISSION_USER_ADD = 'PERMISSION_USER_ADD'
PERMISSION_USER_EDIT = 'PERMISSION_USER_EDIT'
PERMISSION_USER_DEL = 'PERMISSION_USER_DEL'
PERMISSION_USER_DISABLE = 'PERMISSION_USER_DISABLE'
PERMISSION_USER_ENABLE = 'PERMISSION_USER_ENABLE'
# 用户组的操作权限
PERMISSION_GROUP_VIEW = 'PERMISSION_GROUP_VIEW'
PERMISSION_GROUP_ADD = 'PERMISSION_GROUP_ADD'
PERMISSION_GROUP_EDIT = 'PERMISSION_GROUP_EDIT'
PERMISSION_GROUP_DEL = 'PERMISSION_GROUP_DEL'
PERMISSION_GROUP_DISABLE = 'PERMISSION_GROUP_DISABLE'
PERMISSION_GROUP_ENABLE = 'PERMISSION_GROUP_ENABLE'
# 角色的操作权限
PERMISSION_ROLE_VIEW = 'PERMISSION_ROLE_VIEW'
PERMISSION_ROLE_ADD = 'PERMISSION_ROLE_ADD'
PERMISSION_ROLE_EDIT = 'PERMISSION_ROLE_EDIT'
PERMISSION_ROLE_DEL = 'PERMISSION_ROLE_DEL'
PERMISSION_ROLE_DISABLE = 'PERMISSION_ROLE_DISABLE'
PERMISSION_ROLE_ENABLE = 'PERMISSION_ROLE_ENABLE'
# 用户分配用户组的权限
PERMISSION_USER_GROUP_BIND = 'PERMISSION_USER_GROUP_BIND'
# 给用户分配角色的权限
PERMISSION_USER_ROLE_BIND = 'PERMISSION_USER_ROLE_BIND'
# 给用户组分配角色的权限
PERMISSION_GROUP_ROLE_BIND = 'PERMISSION_GROUP_ROLE_BIND'
# 给角色分配权限的权限
PERMISSION_ROLE_PERMISSION_BIND = 'PERMISSION_ROLE_PERMISSION_BIND'

# 基本配置
PERMISSION_CONFIG_VIEW = 'PERMISSION_CONFIG_VIEW'
PERMISSION_CONFIG_ADD = 'PERMISSION_CONFIG_ADD'
PERMISSION_CONFIG_EDIT = 'PERMISSION_CONFIG_EDIT'
PERMISSION_CONFIG_DEL = 'PERMISSION_CONFIG_DEL'
PERMISSION_CONFIG_DISABLE = 'PERMISSION_CONFIG_DISABLE'
PERMISSION_CONFIG_ENABLE = 'PERMISSION_CONFIG_ENABLE'

# 文件处理
# 文件上传
PERMISSION_FILE_UPLOAD = 'PERMISSION_FILE_UPLOAD'
# 文件查看
PERMISSION_FILE_VIEW = 'PERMISSION_FILE_VIEW'


class TablePermission(SystemEngine):
    table = t_permission
