# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, MetaData


# 状态  1-有效  2-无效
TABLE_STATUS_VALID = 1
TABLE_STATUS_INVALID = 2
TABLE_STATUS = {
    TABLE_STATUS_VALID: '有效',
    TABLE_STATUS_INVALID: '无效',
}
# 子状态  10-有效  20-无效（删除）  21-无效（禁用）
TABLE_SUB_STATUS_VALID = 10
TABLE_SUB_STATUS_INVALID_DEL = 20
TABLE_SUB_STATUS_INVALID_DISABLE = 21
TABLE_SUB_STATUS = {
    TABLE_SUB_STATUS_VALID: '有效',
    TABLE_SUB_STATUS_INVALID_DEL: '删除',
    TABLE_SUB_STATUS_INVALID_DISABLE: '禁用',
}

# 账号类别，1-手机号；2-邮箱；3-自定义账号
TABLE_ACCOUNT_CATEGORY_PHONE = 1
TABLE_ACCOUNT_CATEGORY_EMAIL = 2
TABLE_ACCOUNT_CATEGORY_CUSTOM = 3
TABLE_ACCOUNT_CATEGORY = {
    TABLE_ACCOUNT_CATEGORY_PHONE: '手机号',
    TABLE_ACCOUNT_CATEGORY_EMAIL: '邮箱',
    TABLE_ACCOUNT_CATEGORY_CUSTOM: '自定义',
}

# 权限表code码
# 菜单访问权限code码
PERMISSION_HOME_QUERY = 'PERMISSION_HOME_QUERY'
PERMISSION_SETTING_QUERY = 'PERMISSION_SETTING_QUERY'
PERMISSION_MENU_QUERY = 'PERMISSION_MENU_QUERY'
PERMISSION_OPERATION_QUERY = 'PERMISSION_OPERATION_QUERY'
PERMISSION_USER_QUERY = 'PERMISSION_USER_QUERY'
PERMISSION_GROUP_QUERY = 'PERMISSION_GROUP_QUERY'
PERMISSION_ROLE_QUERY = 'PERMISSION_ROLE_QUERY'
PERMISSION_PERMISSION_QUERY = 'PERMISSION_PERMISSION_QUERY'
# 功能操作权限code码
# 菜单操作权限
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


class BaseEngine(object):
    """
    基础引擎类
    """
    db_engine = None  # 数据库引擎
    meta = None
    table = None  # 表，sqlalchemy.Table类

    @classmethod
    def execute(cls, sql, conn=None):
        """
        执行
        :param sql: 待执行的sql
        :param conn: 连接
        :return:
        """
        if conn is None:
            # 没有从外部传入连接，在内部生成连接
            with cls.db_engine.connect() as conn:
                return conn.execute(sql)
        else:
            # 从外部传入的连接，可能是一个事务，不能立马关闭conn连接，交由外部自己处理
            return conn.execute(sql)
