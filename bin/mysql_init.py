# -*- coding: utf-8 -*-

"""
初始化，系统开始部署时，执行一次即可
"""
import json
from commons.funcs import md5
from models.mysql.system import *
from models.mysql.system.permission import *
from models.mysql.system.operation import *
from models.mysql.system.menu import *
from settings.my_settings import settings_my
# 数据库链接
conn = db_engine.connect()

try:
    # 添加基础配置
    config_sql = t_config.insert().values([
        {'key': settings_my.key_web_page, 'val': 1, 'val_type': 2, 'creator': 'SYS'},
        {'key': settings_my.key_web_page_size, 'val': '10', 'val_type': 2, 'creator': 'SYS'},
        {'key': settings_my.key_web_favicon, 'val': 'statics/images/favicon/favicon.ico', 'val_type': 1, 'creator': 'SYS'},
        {'key': settings_my.key_web_logo, 'val': 'statics/images/logo/logo.jpg', 'val_type': 1, 'creator': 'SYS'},
        {'key': settings_my.key_web_name, 'val': '管理后台', 'val_type': 1, 'creator': 'SYS'},
        {'key': settings_my.key_web_href, 'val': '', 'val_type': 1, 'creator': 'SYS'},
        {'key': settings_my.key_web_copyright, 'val': '', 'val_type': 1, 'creator': 'SYS'},
        # 默认模板
        {'key': settings_my.key_web_default_template, 'val': 1, 'val_type': 2, 'creator': 'SYS'},

        # 用户盐值长度
        {'key': settings_my.key_user_salt_length, 'val': 6, 'val_type': 2, 'creator': 'SYS'},
        # 用户盐值源
        {'key': settings_my.key_user_salt_source, 'val': '0123456789abcdefghijklmnopqrstuvwxyz', 'val_type': 1, 'creator': 'SYS'},

        # 用户昵称长度
        {'key': settings_my.key_user_nickname_length, 'val': 10, 'val_type': 2, 'creator': 'SYS'},
        # 用户昵称源
        {'key': settings_my.key_user_nickname_source, 'val': '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
         'val_type': 1, 'creator': 'SYS'},
        {'key': settings_my.key_user_default_password, 'val': '123456', 'val_type': 1, 'creator': 'SYS'},

        # 登录是否需要验证码
        {'key': settings_my.key_captcha_required, 'val': 1, 'val_type': 2, 'creator': 'SYS'},
        {'key': settings_my.key_captcha_expire_time, 'val': 60, 'val_type': 2, 'creator': 'SYS'},
        {'key': settings_my.key_captcha_key_format, 'val': 'captcha_{}', 'val_type': 1, 'creator': 'SYS'},
        {'key': settings_my.key_captcha_type, 'val': 1, 'val_type': 2, 'creator': 'SYS'},
        {'key': settings_my.key_captcha_length, 'val': 4, 'val_type': 2, 'creator': 'SYS'},

        {'key': settings_my.key_homeInfo, 'val': json.dumps({
                "title": "首页",
                "href": "page/welcome.html?t=1"
        }), 'val_type': 4, 'creator': 'SYS'},
        {'key': settings_my.key_menuInfo, 'val': json.dumps([
                {
                    "title": "主页",
                    "icon": "fa fa-address-book",
                    "href": "page/welcome.html?t=1",
                    "target": "_self",
                    "child": [
                        {
                            "id": 1,
                            "pid": 0,
                            "code": "INDEX",
                            "title": "主页",
                            "icon": "fa fa-address-book",
                            "href": "page/welcome.html?t=1",
                            "intro": "",
                            "child": []
                        }
                    ]
                },
            ]), 'val_type': 4, 'creator': 'SYS'},

        {'key': settings_my.key_token_expire_time, 'val': str(60*60*24*3), 'val_type': 2, 'creator': 'SYS'},
        {'key': settings_my.key_token_key_format, 'val': 'token_{}', 'val_type': 1, 'creator': 'SYS'},

        {'key': settings_my.key_log_level, 'val': 10, 'val_type': 2, 'creator': 'SYS'},
        {'key': settings_my.key_log_name, 'val': 'error.log', 'val_type': 1, 'creator': 'SYS'},
        {'key': settings_my.key_log_max_bytes, 'val': str(1024 * 1024 * 100), 'val_type': 2, 'creator': 'SYS'},
        {'key': settings_my.key_log_backup_count, 'val': '10', 'val_type': 2, 'creator': 'SYS'},
        {'key': settings_my.key_log_format, 'val': '[%(levelname)s][%(process)d][%(asctime)s][%(name)s][%(filename)s][%(lineno)d]: %(message)s', 'val_type': 1, 'creator': 'SYS'},


    ])
    config_res = conn.execute(config_sql)

    # 新增超级管理员用户
    user_sql = t_user.insert().values(
        {'name': 'root', 'salt': 'root', 'password': md5('root', 'root'), 'creator': 'SYS'})
    user_res = conn.execute(user_sql)

    # 新增超级管理员账号
    account_sql = t_account.insert().values({'user_id': user_res.lastrowid, 'open_code': 'root', 'creator': 'SYS',
                                             'category': 1})
    account_res = conn.execute(account_sql)

    # 创建超级管理员角色
    role_sql = t_role.insert().values(
        {'pid': 0, 'code': 'ROLE_SUPER_MANAGER', 'is_super': 1, 'creator': 'SYS', 'name': '超级管理员',
         'intro': '超级管理员，拥有所有权限'})
    role_res = conn.execute(role_sql)

    # 绑定超管角色和用户
    user_role_sql = t_user_role.insert().values(
        {'user_id': user_res.lastrowid, 'role_id': role_res.lastrowid, 'creator': 'SYS'})
    user_role_res = conn.execute(user_role_sql)

    # 创建超管组
    group_sql = t_group.insert().values({'name': 'root', 'code': 'GROUP_SUPER_MANAGER', 'creator': 'SYS'})
    group_res = conn.execute(group_sql)

    # 绑定超管组与超管用户
    user_group_sql = t_user_group.insert().values(
        {'group_id': group_res.lastrowid, 'user_id': user_res.lastrowid, 'creator': 'SYS'})
    conn.execute(user_group_sql)

    # 绑定超管角色与超管组
    role_group_sql = t_group_role.insert().values(
        {'group_id': group_res.lastrowid, 'role_id': role_res.lastrowid, 'creator': 'SYS'})
    role_group_res = conn.execute(role_group_sql)

    # 创建权限
    permission_list = [
        # 菜单展示相关权限
        {'pid': 0, 'code': PERMISSION_HOME_QUERY, 'name': '首页菜单访问', 'intro': '[首页]的访问权限', 'category': 1, 'creator': 'SYS', 'status': TABLE_STATUS_VALID, 'sub_status': TABLE_SUB_STATUS_VALID},
        {'pid': 0, 'code': PERMISSION_SETTING_QUERY, 'name': '设置菜单访问', 'intro': '[设置]的访问权限', 'category': 1, 'creator': 'SYS', 'status': TABLE_STATUS_VALID, 'sub_status': TABLE_SUB_STATUS_VALID},
        {'pid': 2, 'code': PERMISSION_USER_QUERY, 'name': '用户管理', 'intro': '[用户管理]的访问权限', 'category': 1, 'creator': 'SYS', 'status': TABLE_STATUS_VALID, 'sub_status': TABLE_SUB_STATUS_VALID},
        {'pid': 2, 'code': PERMISSION_GROUP_QUERY, 'name': '用户组管理', 'intro': '[用户组管理]的访问权限', 'category': 1, 'creator': 'SYS', 'status': TABLE_STATUS_VALID, 'sub_status': TABLE_SUB_STATUS_VALID},
        {'pid': 2, 'code': PERMISSION_ROLE_QUERY, 'name': '角色管理', 'intro': '[角色管理]的访问权限', 'category': 1, 'creator': 'SYS', 'status': TABLE_STATUS_VALID, 'sub_status': TABLE_SUB_STATUS_VALID},
        {'pid': 2, 'code': PERMISSION_PERMISSION_QUERY, 'name': '权限管理', 'intro': '[权限管理]的访问权限', 'category': 1, 'creator': 'SYS', 'status': TABLE_STATUS_VALID, 'sub_status': TABLE_SUB_STATUS_VALID},
        {'pid': 2, 'code': PERMISSION_CONFIG_QUERY, 'name': '系统设置', 'intro': '[系统设置]的访问权限', 'category': 1, 'creator': 'SYS', 'status': TABLE_STATUS_VALID, 'sub_status': TABLE_SUB_STATUS_VALID},
        {'pid': 2, 'code': PERMISSION_MENU_QUERY, 'name': '菜单管理', 'intro': '[菜单管理]的访问权限', 'category': 1, 'creator': 'SYS', 'status': TABLE_STATUS_INVALID, 'sub_status': TABLE_SUB_STATUS_INVALID_DEL},
        {'pid': 2, 'code': PERMISSION_OPERATION_QUERY, 'name': '操作管理', 'intro': '[操作管理]的访问权限', 'category': 1, 'creator': 'SYS', 'status': TABLE_STATUS_INVALID, 'sub_status': TABLE_SUB_STATUS_INVALID_DEL},

        # 功能操作相关权限
        # 用户的操作权限
        {'pid': 3, 'code': PERMISSION_USER_VIEW, 'name': '查看用户', 'intro': '[查看用户]的操作权限', 'category': 3,
         'creator': 'SYS', 'status': TABLE_STATUS_VALID, 'sub_status': TABLE_SUB_STATUS_VALID},
        {'pid': 3, 'code': PERMISSION_USER_ADD, 'name': '添加用户', 'intro': '[添加用户]的操作权限', 'category': 3,
         'creator': 'SYS', 'status': TABLE_STATUS_VALID, 'sub_status': TABLE_SUB_STATUS_VALID},
        {'pid': 3, 'code': PERMISSION_USER_EDIT, 'name': '修改用户', 'intro': '[修改用户]的操作权限', 'category': 3,
         'creator': 'SYS', 'status': TABLE_STATUS_VALID, 'sub_status': TABLE_SUB_STATUS_VALID},
        {'pid': 3, 'code': PERMISSION_USER_DEL, 'name': '删除用户', 'intro': '[删除用户]的操作权限', 'category': 3,
         'creator': 'SYS', 'status': TABLE_STATUS_VALID, 'sub_status': TABLE_SUB_STATUS_VALID},
        {'pid': 3, 'code': PERMISSION_USER_DISABLE, 'name': '禁用用户', 'intro': '[禁用用户]的操作权限', 'category': 3,
         'creator': 'SYS', 'status': TABLE_STATUS_VALID, 'sub_status': TABLE_SUB_STATUS_VALID},
        {'pid': 3, 'code': PERMISSION_USER_ENABLE, 'name': '启用用户', 'intro': '[启用用户]的操作权限', 'category': 3,
         'creator': 'SYS', 'status': TABLE_STATUS_VALID, 'sub_status': TABLE_SUB_STATUS_VALID},


        # 用户组的操作权限
        {'pid': 4, 'code': PERMISSION_GROUP_VIEW, 'name': '查看用户组', 'intro': '[查看用户组]的操作权限', 'category': 3,
         'creator': 'SYS', 'status': TABLE_STATUS_VALID, 'sub_status': TABLE_SUB_STATUS_VALID},
        {'pid': 4, 'code': PERMISSION_GROUP_ADD, 'name': '添加用户组', 'intro': '[添加用户组]的操作权限', 'category': 3,
         'creator': 'SYS', 'status': TABLE_STATUS_VALID, 'sub_status': TABLE_SUB_STATUS_VALID},
        {'pid': 4, 'code': PERMISSION_GROUP_EDIT, 'name': '修改用户组', 'intro': '[修改用户组]的操作权限', 'category': 3,
         'creator': 'SYS', 'status': TABLE_STATUS_VALID, 'sub_status': TABLE_SUB_STATUS_VALID},
        {'pid': 4, 'code': PERMISSION_GROUP_DEL, 'name': '删除用户组', 'intro': '[删除用户组]的操作权限', 'category': 3,
         'creator': 'SYS', 'status': TABLE_STATUS_VALID, 'sub_status': TABLE_SUB_STATUS_VALID},
        {'pid': 4, 'code': PERMISSION_GROUP_DISABLE, 'name': '禁用用户组', 'intro': '[禁用用户组]的操作权限', 'category': 3,
         'creator': 'SYS', 'status': TABLE_STATUS_VALID, 'sub_status': TABLE_SUB_STATUS_VALID},
        {'pid': 4, 'code': PERMISSION_GROUP_ENABLE, 'name': '启用用户组', 'intro': '[启用用户组]的操作权限', 'category': 3,
         'creator': 'SYS', 'status': TABLE_STATUS_VALID, 'sub_status': TABLE_SUB_STATUS_VALID},

        # 角色的操作权限
        {'pid': 5, 'code': PERMISSION_ROLE_VIEW, 'name': '查看角色', 'intro': '[查看角色]的操作权限', 'category': 3, 'creator': 'SYS', 'status': TABLE_STATUS_VALID, 'sub_status': TABLE_SUB_STATUS_VALID},
        {'pid': 5, 'code': PERMISSION_ROLE_ADD, 'name': '添加角色', 'intro': '[添加角色]的操作权限', 'category': 3, 'creator': 'SYS', 'status': TABLE_STATUS_VALID, 'sub_status': TABLE_SUB_STATUS_VALID},
        {'pid': 5, 'code': PERMISSION_ROLE_EDIT, 'name': '修改角色', 'intro': '[修改角色]的操作权限', 'category': 3,
         'creator': 'SYS', 'status': TABLE_STATUS_VALID, 'sub_status': TABLE_SUB_STATUS_VALID},
        {'pid': 5, 'code': PERMISSION_ROLE_DEL, 'name': '删除角色', 'intro': '[删除角色]的操作权限', 'category': 3, 'creator': 'SYS', 'status': TABLE_STATUS_VALID, 'sub_status': TABLE_SUB_STATUS_VALID},
        {'pid': 5, 'code': PERMISSION_ROLE_DISABLE, 'name': '禁用角色', 'intro': '[禁用角色]的操作权限', 'category': 3,
         'creator': 'SYS', 'status': TABLE_STATUS_VALID, 'sub_status': TABLE_SUB_STATUS_VALID},
        {'pid': 5, 'code': PERMISSION_ROLE_ENABLE, 'name': '启用角色', 'intro': '[启用角色]的操作权限', 'category': 3,
         'creator': 'SYS', 'status': TABLE_STATUS_VALID, 'sub_status': TABLE_SUB_STATUS_VALID},

        # 权限的操作权限
        {'pid': 6, 'code': PERMISSION_PERMISSION_VIEW, 'name': '查看权限', 'intro': '[查看权限]的操作权限', 'category': 3,
         'creator': 'SYS', 'status': TABLE_STATUS_VALID, 'sub_status': TABLE_SUB_STATUS_VALID},
        {'pid': 6, 'code': PERMISSION_PERMISSION_ADD, 'name': '添加权限', 'intro': '[添加权限]的操作权限', 'category': 3,
         'creator': 'SYS', 'status': TABLE_STATUS_VALID, 'sub_status': TABLE_SUB_STATUS_VALID},
        {'pid': 6, 'code': PERMISSION_PERMISSION_EDIT, 'name': '修改权限', 'intro': '[修改权限]的操作权限', 'category': 3,
         'creator': 'SYS', 'status': TABLE_STATUS_VALID, 'sub_status': TABLE_SUB_STATUS_VALID},
        {'pid': 6, 'code': PERMISSION_PERMISSION_DEL, 'name': '删除权限', 'intro': '[删除权限]的操作权限', 'category': 3,
         'creator': 'SYS', 'status': TABLE_STATUS_VALID, 'sub_status': TABLE_SUB_STATUS_VALID},
        {'pid': 6, 'code': PERMISSION_PERMISSION_DISABLE, 'name': '禁用权限', 'intro': '[禁用权限]的操作权限', 'category': 3,
         'creator': 'SYS', 'status': TABLE_STATUS_VALID, 'sub_status': TABLE_SUB_STATUS_VALID},
        {'pid': 6, 'code': PERMISSION_PERMISSION_ENABLE, 'name': '启用权限', 'intro': '[启用权限]的操作权限', 'category': 3,
         'creator': 'SYS', 'status': TABLE_STATUS_VALID, 'sub_status': TABLE_SUB_STATUS_VALID},


        # 绑定用户-组的权限
        {'pid': 3, 'code': PERMISSION_USER_GROUP_BIND, 'name': '绑定用户-组', 'intro': '[绑定用户-组]的操作权限', 'category': 3,
         'creator': 'SYS', 'status': TABLE_STATUS_VALID, 'sub_status': TABLE_SUB_STATUS_VALID},
        # 绑定用户-角色的权限
        {'pid': 3, 'code': PERMISSION_USER_ROLE_BIND, 'name': '绑定用户-角色', 'intro': '[绑定用户-角色]的操作权限', 'category': 3,
         'creator': 'SYS', 'status': TABLE_STATUS_VALID, 'sub_status': TABLE_SUB_STATUS_VALID},
        # 绑定组-角色的权限
        {'pid': 4, 'code': PERMISSION_GROUP_ROLE_BIND, 'name': '绑定组-角色', 'intro': '[绑定组-角色]的操作权限', 'category': 3,
         'creator': 'SYS', 'status': TABLE_STATUS_VALID, 'sub_status': TABLE_SUB_STATUS_VALID},
        # 绑定角色-权限的权限
        {'pid': 5, 'code': PERMISSION_ROLE_PERMISSION_BIND, 'name': '绑定角色-权限', 'intro': '[绑定角色-权限]的操作权限', 'category': 3,
         'creator': 'SYS', 'status': TABLE_STATUS_VALID, 'sub_status': TABLE_SUB_STATUS_VALID},

        # 查看通用配置的权限
        {'pid': 7, 'code': PERMISSION_CONFIG_VIEW, 'name': '查看通用配置', 'intro': '[查看通用配置]的操作权限', 'category': 3, 'creator': 'SYS', 'status': TABLE_STATUS_VALID, 'sub_status': TABLE_SUB_STATUS_VALID},
        # 添加通用配置的权限
        {'pid': 7, 'code': PERMISSION_CONFIG_ADD, 'name': '添加通用配置', 'intro': '[添加通用配置]的操作权限', 'category': 3, 'creator': 'SYS', 'status': TABLE_STATUS_INVALID, 'sub_status': TABLE_SUB_STATUS_INVALID_DEL},
        # 修改通用配置的权限
        {'pid': 7, 'code': PERMISSION_CONFIG_EDIT, 'name': '修改通用配置', 'intro': '[修改通用配置]的操作权限', 'category': 3, 'creator': 'SYS', 'status': TABLE_STATUS_VALID, 'sub_status': TABLE_SUB_STATUS_VALID},
        # 删除通用配置的权限
        {'pid': 7, 'code': PERMISSION_CONFIG_DEL, 'name': '删除通用配置', 'intro': '[删除通用配置]的操作权限', 'category': 3, 'creator': 'SYS', 'status': TABLE_STATUS_INVALID, 'sub_status': TABLE_SUB_STATUS_INVALID_DEL},
        # 禁用通用配置的权限
        {'pid': 7, 'code': PERMISSION_CONFIG_DISABLE, 'name': '禁用通用配置', 'intro': '[禁用通用配置]的操作权限', 'category': 3, 'creator': 'SYS', 'status': TABLE_STATUS_INVALID, 'sub_status': TABLE_SUB_STATUS_INVALID_DEL},
        # 启用通用配置的权限
        {'pid': 7, 'code': PERMISSION_CONFIG_ENABLE, 'name': '启用通用配置', 'intro': '[启用通用配置]的操作权限', 'category': 3, 'creator': 'SYS', 'status': TABLE_STATUS_INVALID, 'sub_status': TABLE_SUB_STATUS_INVALID_DEL},
        # 文件上传的权限
        {'pid': 7, 'code': PERMISSION_FILE_UPLOAD, 'name': '文件上传', 'intro': '[文件上传]的操作权限', 'category': 3,
         'creator': 'SYS', 'status': TABLE_STATUS_VALID, 'sub_status': TABLE_SUB_STATUS_VALID},
        # 文件查看的权限
        {'pid': 7, 'code': PERMISSION_FILE_VIEW, 'name': '文件查看', 'intro': '[文件查看]的操作权限', 'category': 3,
         'creator': 'SYS', 'status': TABLE_STATUS_VALID, 'sub_status': TABLE_SUB_STATUS_VALID},

        # 菜单操作权限
        {'pid': 8, 'code': PERMISSION_MENU_VIEW, 'name': '查看菜单', 'intro': '[查看菜单]的操作权限', 'category': 3,
         'creator': 'SYS', 'status': TABLE_STATUS_INVALID, 'sub_status': TABLE_SUB_STATUS_INVALID_DEL},
        {'pid': 8, 'code': PERMISSION_MENU_ADD, 'name': '添加菜单', 'intro': '[添加菜单]的操作权限', 'category': 3, 'creator': 'SYS',
         'status': TABLE_STATUS_INVALID, 'sub_status': TABLE_SUB_STATUS_INVALID_DEL},
        {'pid': 8, 'code': PERMISSION_MENU_EDIT, 'name': '修改菜单', 'intro': '[修改菜单]的操作权限', 'category': 3,
         'creator': 'SYS', 'status': TABLE_STATUS_INVALID, 'sub_status': TABLE_SUB_STATUS_INVALID_DEL},
        {'pid': 8, 'code': PERMISSION_MENU_DEL, 'name': '删除菜单', 'intro': '[删除菜单]的操作权限', 'category': 3, 'creator': 'SYS',
         'status': TABLE_STATUS_INVALID, 'sub_status': TABLE_SUB_STATUS_INVALID_DEL},
        {'pid': 8, 'code': PERMISSION_MENU_DISABLE, 'name': '禁用菜单', 'intro': '[禁用菜单]的操作权限', 'category': 3,
         'creator': 'SYS', 'status': TABLE_STATUS_INVALID, 'sub_status': TABLE_SUB_STATUS_INVALID_DEL},
        {'pid': 8, 'code': PERMISSION_MENU_ENABLE, 'name': '启用菜单', 'intro': '[启用菜单]的操作权限', 'category': 3,
         'creator': 'SYS', 'status': TABLE_STATUS_INVALID, 'sub_status': TABLE_SUB_STATUS_INVALID_DEL},

    ]
    permission_sql = t_permission.insert().values(permission_list)
    conn.execute(permission_sql)

    # 创建菜单
    menu_list = [
        {'pid': 0, 'code': HOME, 'name': '主页', 'uri': '', 'creator': 'SYS', 'status': TABLE_STATUS_VALID, 'sub_status': TABLE_SUB_STATUS_VALID},
        {'pid': 0, 'code': SETTING, 'name': '设置', 'uri': '', 'creator': 'SYS', 'status': TABLE_STATUS_VALID, 'sub_status': TABLE_SUB_STATUS_VALID},
        {'pid': 2, 'code': USER_MANAGE, 'name': '用户管理', 'uri': 'page/user.html', 'creator': 'SYS', 'status': TABLE_STATUS_VALID, 'sub_status': TABLE_SUB_STATUS_VALID},
        {'pid': 2, 'code': GROUP_MANAGE, 'name': '用户组管理', 'uri': 'page/group.html', 'creator': 'SYS', 'status': TABLE_STATUS_VALID, 'sub_status': TABLE_SUB_STATUS_VALID},
        {'pid': 2, 'code': ROLE_MANAGE, 'name': '角色管理', 'uri': 'page/role.html', 'creator': 'SYS', 'status': TABLE_STATUS_VALID, 'sub_status': TABLE_SUB_STATUS_VALID},
        {'pid': 2, 'code': PERMISSION_MANAGE, 'name': '权限管理', 'uri': 'page/permission.html', 'creator': 'SYS', 'status': TABLE_STATUS_VALID, 'sub_status': TABLE_SUB_STATUS_VALID},
        {'pid': 2, 'code': CONFIG_MANAGE, 'name': '系统设置', 'uri': 'page/system.html', 'creator': 'SYS', 'status': TABLE_STATUS_VALID, 'sub_status': TABLE_SUB_STATUS_VALID},
        {'pid': 2, 'code': MENU_MANAGE, 'name': '菜单管理', 'uri': '/setting/operation', 'creator': 'SYS', 'status': TABLE_STATUS_INVALID, 'sub_status': TABLE_SUB_STATUS_INVALID_DEL},
        {'pid': 2, 'code': OPERATION_MANAGE, 'name': '操作管理', 'uri': '/setting/operation', 'creator': 'SYS', 'status': TABLE_STATUS_INVALID, 'sub_status': TABLE_SUB_STATUS_INVALID_DEL},
    ]
    menu_sql = t_menu.insert().values(menu_list)
    conn.execute(menu_sql)

    # 菜单与权限的绑定关系
    menu_permission_list = [
        {'menu_id': 1, 'permission_id': 1, 'creator': 'SYS'},
        {'menu_id': 2, 'permission_id': 2, 'creator': 'SYS'},
        {'menu_id': 3, 'permission_id': 3, 'creator': 'SYS'},
        {'menu_id': 4, 'permission_id': 4, 'creator': 'SYS'},
        {'menu_id': 5, 'permission_id': 5, 'creator': 'SYS'},
        {'menu_id': 6, 'permission_id': 6, 'creator': 'SYS'},
        {'menu_id': 7, 'permission_id': 7, 'creator': 'SYS'},
        {'menu_id': 8, 'permission_id': 8, 'creator': 'SYS'},
        {'menu_id': 9, 'permission_id': 9, 'creator': 'SYS'},
    ]
    menu_permission_sql = t_menu_permission.insert().values(menu_permission_list)
    conn.execute(menu_permission_sql)

    # 功能操作
    operate_list = [
        # 菜单功能操作
        {'code': OPERATION_MENU_VIEW, 'name': '查看菜单', 'intro': '[查看菜单]功能', 'creator': 'SYS'},
        {'code': OPERATION_MENU_ADD, 'name': '添加菜单', 'intro': '[添加菜单]功能', 'creator': 'SYS'},
        {'code': OPERATION_MENU_EDIT, 'name': '修改菜单', 'intro': '[修改菜单]功能', 'creator': 'SYS'},
        {'code': OPERATION_MENU_DEL, 'name': '删除菜单', 'intro': '[删除菜单]功能', 'creator': 'SYS'},
        {'code': OPERATION_MENU_DISABLE, 'name': '禁用菜单', 'intro': '[禁用菜单]功能', 'creator': 'SYS'},
        {'code': OPERATION_MENU_ENABLE, 'name': '启用菜单', 'intro': '[启用菜单]功能', 'creator': 'SYS'},

        # 用户功能操作
        {'code': OPERATION_USER_VIEW, 'name': '查看用户', 'intro': '[查看用户]功能', 'creator': 'SYS'},
        {'code': OPERATION_USER_ADD, 'name': '添加用户', 'intro': '[添加用户]功能', 'creator': 'SYS'},
        {'code': OPERATION_USER_EDIT, 'name': '修改用户', 'intro': '[修改用户]功能', 'creator': 'SYS'},
        {'code': OPERATION_USER_DEL, 'name': '删除用户', 'intro': '[删除用户]功能', 'creator': 'SYS'},
        {'code': OPERATION_USER_DISABLE, 'name': '禁用用户', 'intro': '[禁用用户]功能', 'creator': 'SYS'},
        {'code': OPERATION_USER_ENABLE, 'name': '启用用户', 'intro': '[启用用户]功能', 'creator': 'SYS'},

        # 用户组功能操作
        {'code': OPERATION_GROUP_VIEW, 'name': '查看用户组', 'intro': '[查看用户组]功能', 'creator': 'SYS'},
        {'code': OPERATION_GROUP_ADD, 'name': '添加用户组', 'intro': '[添加用户组]功能', 'creator': 'SYS'},
        {'code': OPERATION_GROUP_EDIT, 'name': '修改用户组', 'intro': '[修改用户组]功能', 'creator': 'SYS'},
        {'code': OPERATION_GROUP_DEL, 'name': '删除用户组', 'intro': '[删除用户组]功能', 'creator': 'SYS'},
        {'code': OPERATION_GROUP_DISABLE, 'name': '禁用用户组', 'intro': '[禁用用户组]功能', 'creator': 'SYS'},
        {'code': OPERATION_GROUP_ENABLE, 'name': '启用用户组', 'intro': '[启用用户组]功能', 'creator': 'SYS'},

        # 角色功能操作
        {'code': OPERATION_ROLE_VIEW, 'name': '查看角色', 'intro': '[查看角色]功能', 'creator': 'SYS'},
        {'code': OPERATION_ROLE_ADD, 'name': '添加角色', 'intro': '[添加角色]功能', 'creator': 'SYS'},
        {'code': OPERATION_ROLE_EDIT, 'name': '修改角色', 'intro': '[修改角色]功能', 'creator': 'SYS'},
        {'code': OPERATION_ROLE_DEL, 'name': '删除角色', 'intro': '[删除角色]功能', 'creator': 'SYS'},
        {'code': OPERATION_ROLE_DISABLE, 'name': '禁用角色', 'intro': '[禁用角色]功能', 'creator': 'SYS'},
        {'code': OPERATION_ROLE_ENABLE, 'name': '启用角色', 'intro': '[启用角色]功能', 'creator': 'SYS'},

        # 权限功能操作
        {'code': OPERATION_PERMISSION_VIEW, 'name': '查看权限', 'intro': '[查看权限]功能', 'creator': 'SYS'},
        {'code': OPERATION_PERMISSION_ADD, 'name': '添加权限', 'intro': '[添加权限]功能', 'creator': 'SYS'},
        {'code': OPERATION_PERMISSION_EDIT, 'name': '修改权限', 'intro': '[修改权限]功能', 'creator': 'SYS'},
        {'code': OPERATION_PERMISSION_DEL, 'name': '删除权限', 'intro': '[删除权限]功能', 'creator': 'SYS'},
        {'code': OPERATION_PERMISSION_DISABLE, 'name': '禁用权限', 'intro': '[禁用权限]功能', 'creator': 'SYS'},
        {'code': OPERATION_PERMISSION_ENABLE, 'name': '启用权限', 'intro': '[启用权限]功能', 'creator': 'SYS'},

        # 给用户分配用户组的操作
        {'code': OPERATION_USER_GROUP_BIND, 'name': '给用户分配组', 'intro': '[给用户分配组]功能', 'creator': 'SYS'},

        # 给用户分配角色的操作
        {'code': OPERATION_USER_ROLE_BIND, 'name': '给用户分配角色', 'intro': '[给用户分配角色]功能', 'creator': 'SYS'},

        # 给用户组分配角色的操作
        {'code': OPERATION_ROLE_GROUP_BIND, 'name': '给用户组分配角色', 'intro': '[给用户组分配角色]功能', 'creator': 'SYS'},

        # 给角色分配权限的操作
        {'code': OPERATION_ROLE_PERMISSION_BIND, 'name': '给角色分配权限', 'intro': '[给角色分配权限]功能', 'creator': 'SYS'},

        # 通用配置功能操作
        {'code': OPERATION_CONFIG_VIEW, 'name': '查看通用配置', 'intro': '[查看通用配置]功能', 'creator': 'SYS'},
        {'code': OPERATION_CONFIG_ADD, 'name': '添加通用配置', 'intro': '[添加通用配置]功能', 'creator': 'SYS'},
        {'code': OPERATION_CONFIG_EDIT, 'name': '修改通用配置', 'intro': '[修改通用配置]功能', 'creator': 'SYS'},
        {'code': OPERATION_CONFIG_DEL, 'name': '删除通用配置', 'intro': '[删除通用配置]功能', 'creator': 'SYS'},
        {'code': OPERATION_CONFIG_DISABLE, 'name': '禁用通用配置', 'intro': '[禁用通用配置]功能', 'creator': 'SYS'},
        {'code': OPERATION_CONFIG_ENABLE, 'name': '启用通用配置', 'intro': '[启用通用配置]功能', 'creator': 'SYS'},

        # 文件操作功能操作
        # 文件上传操作
        {'code': OPERATION_FILE_UPLOAD, 'name': '文件上传', 'intro': '[文件上传]功能', 'creator': 'SYS'},
        # 文件查看功能操作
        {'code': OPERATION_FILE_VIEW, 'name': '文件查看', 'intro': '[文件查看]功能', 'creator': 'SYS'},

    ]
    operate_sql = t_operation.insert().values(operate_list)
    conn.execute(operate_sql)

    # 功能操作与权限的关系绑定
    permission_beg_index = 8
    operation_permission_list = list([{
        'operation_id': i,
        'permission_id': i + permission_beg_index,
        'creator': 'SYS'
    } for i in range(1, len(operate_list) + 1)])
    operation_permission_sql = t_operation_permission.insert().values(operation_permission_list)
    conn.execute(operation_permission_sql)

    # # 角色与权限的绑定关系
    # role_permission_list = [
    #     {'role_id': 1, 'permission_id': 1, 'creator': 'SYS'},
    #     {'role_id': 1, 'permission_id': 2, 'creator': 'SYS'},
    #     {'role_id': 1, 'permission_id': 3, 'creator': 'SYS'},
    #     {'role_id': 1, 'permission_id': 4, 'creator': 'SYS'},
    #     {'role_id': 1, 'permission_id': 5, 'creator': 'SYS'},
    #     {'role_id': 1, 'permission_id': 6, 'creator': 'SYS'},
    #     {'role_id': 1, 'permission_id': 7, 'creator': 'SYS'},
    #     {'role_id': 1, 'permission_id': 8, 'creator': 'SYS'},
    #     {'role_id': 1, 'permission_id': 9, 'creator': 'SYS'},
    #     {'role_id': 1, 'permission_id': 10, 'creator': 'SYS'},
    #     {'role_id': 1, 'permission_id': 11, 'creator': 'SYS'},
    #     {'role_id': 1, 'permission_id': 12, 'creator': 'SYS'},
    #     {'role_id': 1, 'permission_id': 13, 'creator': 'SYS'},
    #     {'role_id': 1, 'permission_id': 14, 'creator': 'SYS'},
    #     {'role_id': 1, 'permission_id': 15, 'creator': 'SYS'},
    #     {'role_id': 1, 'permission_id': 16, 'creator': 'SYS'},
    #     {'role_id': 1, 'permission_id': 17, 'creator': 'SYS'},
    # ]
    # role_permission_sql = t_role_permission.insert().values(role_permission_list)
    # conn.execute(role_permission_sql)
except Exception as ex:
    print(ex)
finally:
    conn.close()
