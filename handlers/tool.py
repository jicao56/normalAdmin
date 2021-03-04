# -*- coding: utf-8 -*-
import random
import json
import time
from sqlalchemy import func, select, Table
from sqlalchemy.engine.result import RowProxy
from sqlalchemy.sql import and_, or_
from fastapi import Header, Query

from commons.func import md5, is_email, is_mobile
from commons.code import *

from settings import settings

from models.redis.system import redis_conn

from models.mysql.system import db_engine, t_menu, t_permission, t_role, t_group, t_user_role, t_user_group, t_group_role, \
    t_role_permission, t_menu_permission, SystemEngine
from models.mysql import *

from handlers.exp import MyException
from handlers.items import ItemOut
from handlers.items.menu import ItemMenus


async def check_token(token: str = Header(None, description='用户token'), token2: str = Query(None, description='用户token')):
    """
    根据header头中传过来的token，鉴权
    :param token:
    :return:
    """
    if token2:
        token = token2
    elif token:
        pass
    else:
        raise MyException(status_code=HTTP_400_BAD_REQUEST,
                          detail=ItemOut(code=AUTH_TOKEN_NOT_PROVIDE, msg='token need'))

    if not token:
        raise MyException(status_code=HTTP_400_BAD_REQUEST, detail=ItemOut(code=AUTH_TOKEN_NOT_PROVIDE, msg='token need'))

    token_key = settings.redis_token_key.format(token)
    token_exist = redis_conn.exists(token_key)
    if not token_exist:
        # 取不到用户信息，token过期失效了
        raise MyException(status_code=HTTP_400_BAD_REQUEST, detail=ItemOut(code=AUTH_TOKEN_EXPIRED, msg='token expired'))

    # 更新token有效期
    redis_conn.expire(token_key, settings.redis_token_expire_time)


async def get_userinfo_from_token(token: str = Header(None, description='用户token'), token2: str = Query(None, description='用户token')):
    """
    根据header头中传过来的token，鉴权
    :param token:
    :return:
    """
    if token2:
        token = token2
    elif token:
        pass
    else:
        raise MyException(status_code=HTTP_400_BAD_REQUEST,
                          detail=ItemOut(code=AUTH_TOKEN_NOT_PROVIDE, msg='token need'))

    if not token:
        raise MyException(status_code=HTTP_400_BAD_REQUEST, detail=ItemOut(code=AUTH_TOKEN_NOT_PROVIDE, msg='token need'))
    return _get_userinfo_from_token(token)


def get_rand_str(length: int = settings.web_captcha_length):
    return ''.join(random.sample(settings.web_captcha_source, length))


# RowProxy对象转换为字典
def row_proxy_to_dict(item: RowProxy):
    """
    RowProxy对象转换为字典
    :param item:
    :return:
    """
    item_out = ItemOut()
    if not isinstance(item, RowProxy):
        item_out.code = TYPE_TRANSFER_ERR
        item_out.msg = '类型转换错误'
        raise MyException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=item_out)
    return dict(zip(item.keys(), item))


# 根据用户id创建token
def create_token(user_id: int):
    """
    根据用户id创建token
    :param user_id: 用户id
    :return:
    """
    if not user_id:
        raise MyException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=ItemOut(code=LOGIN_CREATE_TOKEN_ERROR, msg='make token error'))

    return md5(str(user_id) + str(int(time.time())))


# 从token中获取用户信息
def _get_userinfo_from_token(token: str):
    """
    从token中获取用户信息
    :param token:
    :return: dict
    """
    if not token:
        raise MyException(status_code=HTTP_400_BAD_REQUEST, detail=ItemOut(code=AUTH_TOKEN_NOT_PROVIDE, msg='token need'))

    token_key = settings.redis_token_key.format(token)
    userinfo = redis_conn.get(token_key)
    if not userinfo:
        # 取不到用户信息，token过期失效了
        raise MyException(status_code=HTTP_400_BAD_REQUEST,
                          detail=ItemOut(code=AUTH_TOKEN_EXPIRED, msg='token expired'))
    return json.loads(userinfo)


# 检查权限是否存在
def _check_permission_exists(permission_id, conn):
    """
    检查权限是否存在
    :param permission_id: 权限id
    :param conn: 数据库连接
    :return:
    """
    if not permission_id or not conn:
        return
    permission = conn.execute(select([
        t_permission.c.id,
        t_permission.c.pid,
        t_permission.c.code,
        t_permission.c.name,
        t_permission.c.intro,
        t_permission.c.category,
    ]).where(and_(
        t_permission.c.id == permission_id,
        t_permission.c.status == TABLE_STATUS_VALID
    )).limit(1)).fetchone()

    if not permission:
        raise MyException(status_code=HTTP_404_NOT_FOUND,
                          detail={'code': HTTP_404_NOT_FOUND, 'msg': 'permission is not exists'})
    else:
        return permission


# 检查权限是否存在
def check_permission_exists(permission_id, conn=None):
    """
    检查权限是否存在
    :param permission_id: 权限id
    :param conn: 数据库连接
    :return:
    """
    if conn:
        permission = _check_permission_exists(permission_id, conn)
    else:
        with db_engine.connect() as conn:
            permission = _check_permission_exists(permission_id, conn)

    return permission


# 获取用户组
def _get_group(group_id, conn):
    """
    获取用户组
    :param group_id: 用户组id
    :param conn: 数据库连接
    :return:
    """
    if not group_id or not conn:
        return
    group = conn.execute(select([
        t_group.c.id,
        t_group.c.pid,
        t_group.c.code,
        t_group.c.name,
        t_group.c.intro,
    ]).where(and_(
        t_group.c.id == group_id,
        t_group.c.status == TABLE_STATUS_VALID
    )).limit(1)).fetchone()

    if not group:
        raise MyException(status_code=HTTP_404_NOT_FOUND,
                          detail={'code': HTTP_404_NOT_FOUND, 'msg': 'group is not exists'})
    else:
        return group


# 获取用户组
def get_group(group_id, conn=None):
    """
    获取用户组
    :param group_id: 用户组id
    :param conn: 数据库连接
    :return:
    """
    if conn:
        group = _get_group(group_id, conn)
    else:
        with db_engine.connect() as conn:
            group = _get_group(group_id, conn)

    if not group:
        raise MyException(status_code=HTTP_404_NOT_FOUND,
                          detail={'code': HTTP_404_NOT_FOUND, 'msg': 'group is not exists'})
    else:
        return group


# 获取角色
def _get_role(role_id, conn):
    """
    获取角色
    :param role_id: 角色id
    :param conn: 数据库连接
    :return:
    """
    if not role_id or not conn:
        return
    role = conn.execute(select([
        t_role.c.id,
        t_role.c.pid,
        t_role.c.code,
        t_role.c.name,
        t_role.c.intro,
        t_role.c.is_super,
    ]).where(and_(
        t_role.c.id == role_id,
        t_role.c.status == TABLE_STATUS_VALID
    )).limit(1)).fetchone()

    if not role:
        raise MyException(status_code=HTTP_404_NOT_FOUND,
                          detail={'code': HTTP_404_NOT_FOUND, 'msg': 'role is not exists'})
    else:
        return role


# 获取角色
def get_role(role_id, conn=None):
    """
    获取角色
    :param role_id: 角色id
    :param conn: 数据库连接
    :return:
    """
    if conn:
        role = _get_role(role_id, conn)
    else:
        with db_engine.connect() as conn:
            role = _get_role(role_id, conn)

    if not role:
        raise MyException(status_code=HTTP_404_NOT_FOUND,
                          detail={'code': HTTP_404_NOT_FOUND, 'msg': 'role is not exists'})
    else:
        return role


# 获取角色
def _get_roles(role_ids: list, conn):
    """
    获取角色
    :param role_ids: 角色ID列表
    :param conn: 数据库连接
    :return:
    """
    if not role_ids or not conn:
        return

    # 取具体角色信息
    sql = select([
        t_role.c.id,
        t_role.c.pid,
        t_role.c.code,
        t_role.c.name,
        t_role.c.intro,
        t_role.c.is_super,
    ]).where(t_role.c.status == TABLE_STATUS_VALID).where(t_role.c.id.in_(role_ids))
    return conn.execute(sql).fetchall()


# 获取角色
def get_roles(role_ids: list, conn=None):
    """
    获取角色
    :param role_ids: 角色ID列表
    :param conn: 数据库连接
    :return:
    """
    if conn:
        return _get_roles(role_ids, conn)
    else:
        with db_engine.connect() as conn:
            return _get_roles(role_ids, conn)


# 获取用户角色
def _get_user_roles(user_id, conn):
    """
    获取用户角色，多对多
    :param user_id:
    :param conn:
    :return:
    """
    if not user_id or not conn:
        return

    # 取用户所拥有的角色
    sql = select([
        t_user_role.c.role_id,
    ]).where(t_user_role.c.status == TABLE_STATUS_VALID)
    if isinstance(user_id, int):
        sql = sql.where(t_user_role.c.user_id == user_id)
    elif isinstance(user_id, list):
        if len(user_id) == 1:
            sql = sql.where(t_user_role.c.user_id == user_id)
        else:
            sql = sql.where(t_user_role.c.user_id.in_(user_id))

    user_roles = conn.execute(sql).fetchall()
    if user_roles:
        # 取具体角色信息
        return get_roles([item.role_id for item in user_roles], conn=conn)


# 获取用户角色
def get_user_roles(user_id, conn=None):
    """
    获取用户角色，多对多
    :param user_id: 用户id，可能是单个id，也可能是id列表
    :param conn:
    :return:
    """
    if not user_id:
        return

    if conn:
        return _get_user_roles(user_id, conn)
    else:
        with db_engine.connect() as conn:
            return _get_user_roles(user_id, conn)


# 获取用户所属组
def _get_user_groups(user_id: int, conn):
    """
    获取用户所属组，多对多
    :param user_id: 用户id
    :param conn:
    :return:
    """
    if not user_id or not conn:
        return

    # 取用户所属组的sql
    user_group_sql = select([
        t_user_group.c.group_id,
    ]).where(t_user_group.c.user_id == user_id).where(t_user_group.c.status == TABLE_STATUS_VALID)

    # 取具体用户组信息的sql
    group_sql = select([
        t_group.c.id,
        t_group.c.pid,
        t_group.c.name,
        t_group.c.code,
        t_group.c.intro,
    ]).where(t_group.c.status == TABLE_STATUS_VALID)

    # 取用户所属组
    user_groups = conn.execute(user_group_sql).fetchall()
    if user_groups:
        # 取具体用户组信息
        group_sql = group_sql.where(t_group.c.id.in_([item.group_id for item in user_groups]))
        groups = conn.execute(group_sql).fetchall()

    return groups


# 获取用户所属组
def get_user_groups(user_id: int, conn=None):
    """
    获取用户所属组，多对多
    :param user_id: 用户id
    :param conn:
    :return:
    """
    if conn:
        groups = _get_user_groups(user_id, conn)
    else:
        with db_engine.connect() as conn:
            groups = _get_user_groups(user_id, conn)

    return groups


# 获取用户组与角色的关系
def _get_group_roles(group_id, conn):
    """
    获取用户组与角色的关系，多对多
    :param group_id: 用户组id，可能是单个id，也可能是id列表
    :param conn:
    :return:
    """
    if not group_id or not conn:
        return

    # 取用户组拥有的角色
    sql = select([
        t_group_role.c.role_id,
    ]).where(t_role.c.status == TABLE_STATUS_VALID)
    if isinstance(group_id, int):
        sql = sql.where(t_group_role.c.group_id == group_id)
    elif isinstance(group_id, list):
        if len(group_id) == 1:
            sql = sql.where(t_group_role.c.group_id == group_id)
        else:
            sql = sql.where(t_group_role.c.group_id.in_(group_id))

    group_roles = conn.execute(sql).fetchall()
    if group_roles:
        # 取具体角色信息
        return get_roles([item.role_id for item in group_roles], conn=conn)


# 获取用户组与角色的关系
def get_group_roles(group_id, conn=None):
    """
    获取用户组与角色的关系，多对多
    :param group_id: 用户组id，可能是单个id，也可能是id列表
    :param conn:
    :return:
    """
    if conn:
        return _get_group_roles(group_id, conn)
    else:
        with db_engine.connect() as conn:
            return _get_group_roles(group_id, conn)


# 获取用户权限
def _get_user_permission(user_id, conn):
    """
    获取用户权限
    :param user_id:
    :param conn:
    :return:
    """
    # 角色去重
    is_super = 0
    user_roles = get_user_roles(user_id, conn=conn)
    user_groups = get_user_groups(user_id, conn=conn)
    group_roles = get_group_roles([group.id for group in user_groups], conn=conn)

    target_roles = user_roles + group_roles
    roles_length = len(target_roles)
    for index, item in enumerate(target_roles[-1::-1]):
        if item.is_super:
            # 是超管，直接中断，取所有权限
            is_super = 1
            break

        if (roles_length - (index + 2)) >= 0 and item.code in [item2.code for item2 in
                                                               target_roles[roles_length - (index + 2)::-1]]:
            target_roles.pop(roles_length - index - 1)

    if is_super:
        # 有超管角色，直接从权限表中获取所有权限
        sql = select([t_permission.c.id, t_permission.c.code]).where(t_permission.c.status == TABLE_STATUS_VALID)
        permission_list = conn.execute(sql).fetchall()
    else:
        # 没有超管角色，从角色权限绑定表中获取权限
        sql = select([t_role_permission.c.permission_id.label('id')]).where(
            t_role_permission.c.role_id.in_([role.id for role in target_roles])).where(
            t_role_permission.c.status == TABLE_STATUS_VALID)
        permission_list = conn.execute(sql).fetchall()
        if permission_list:
            sql = select([t_permission.c.id, t_permission.c.code]).where(
                t_permission.c.id.in_([permission.id for permission in permission_list])).where(
                t_permission.c.status == TABLE_STATUS_VALID)
            permission_list = conn.execute(sql).fetchall()
    return permission_list


# 获取用户权限（用户的权限 + 用户所在组的权限）
def get_user_permission(user_id: int, conn=None):
    """
    获取用户权限（用户的权限 + 用户所在组的权限）
    可继续优化，不借用第三变量，通过pop或者remove直接在本地操作
    :param user_id: 用户id
    :param conn:
    :return: [RowProxy, RowProxy,]
    """
    if conn:
        return _get_user_permission(user_id, conn)
    else:
        with db_engine.connect() as conn:
            return _get_user_permission(user_id, conn)


# 根据权限获取菜单
def _get_menus_by_permission(permission_ids: list, conn):
    """
    根据权限获取菜单
    :param permission_ids:
    :param conn:
    :return:
    """
    if not permission_ids or not conn:
        return

    sql = select([
        t_menu_permission.c.menu_id,
    ]).where(
        t_menu_permission.c.permission_id.in_(permission_ids)
    ).where(
        t_user_group.c.status == TABLE_STATUS_VALID
    ).order_by('sort', 'id')
    menu_permission_list = conn.execute(sql).fetchall()
    if not menu_permission_list:
        return []

    sql = select([
        t_menu.c.id,
        t_menu.c.pid,
        t_menu.c.code,
        t_menu.c.name,
        t_menu.c.uri,
        t_menu.c.intro,
    ]).where(t_menu.c.id.in_([item.menu_id for item in menu_permission_list])).where(t_menu.c.status == TABLE_STATUS_VALID)
    return conn.execute(sql).fetchall()


# 根据权限获取菜单
def get_menus_by_permission(permission_ids: list, conn=None):
    """
    根据权限获取菜单
    :param permission_ids:
    :return:
    """
    if conn:
        return _get_menus_by_permission(permission_ids, conn)
    else:
        with db_engine.connect() as conn:
            return _get_menus_by_permission(permission_ids, conn)


# 菜单序列化
def menu_serialize(pid: int, menu_list: [RowProxy], target_list: [dict]):
    """
    菜单序列化
    :param pid:
    :param menu_list:
    :param target_list:
    :return:
    """
    # 将menu_list按pid过滤，并按id排序
    cur_menu_list = sorted(filter(lambda x: x.pid == pid, menu_list), key=lambda x: x.id)

    for menu in cur_menu_list:
        tmp_menu = ItemMenus(
            id=menu.id,
            pid=menu.pid,
            code=menu.code,
            title=menu.name,
            href=menu.uri,
            intro=menu.intro,
            child=[],
        )
        if menu.pid:
            # 不是顶级菜单
            # filter(lambda x: x.id==menu.pid, target_list)
            for item in target_list:
                if item.id == menu.pid:
                    item.child.append(tmp_menu)
                    break
        else:
            # 是顶级菜单
            target_list.append(tmp_menu)
        menu_list.remove(menu)
        menu_serialize(menu.id, menu_list, target_list)


# 判断用户是否有操作权限
def _check_operation_permission(user_id, permission_code, conn):
    """
    判断用户是否有操作权限
    :param user_id:
    :param permission_code:
    :param conn:
    :return:
    """
    permission_obj_list = get_user_permission(user_id, conn)
    if permission_code not in [item.code for item in permission_obj_list]:
        # 没有绑定用户角色的权限
        raise MyException(status_code=HTTP_401_UNAUTHORIZED,
                          detail={'code': AUTH_PERMISSION_HAVE_NOT, 'msg': 'no permission to operate'})


# 判断用户是否有操作权限
def check_operation_permission(user_id, permission_code, conn=None):
    """
    判断用户是否有操作权限
    :param user_id:
    :param permission_code:
    :return:
    """
    if conn:
        _check_operation_permission(user_id, permission_code, conn)
    else:
        with db_engine.connect() as conn:
            _check_operation_permission(user_id, permission_code, conn)


# 获取账号类型
def get_account_category(user_name):
    """
    获取账号类型
    :param user_name: 用户名
    :return:
    """
    # 1.先验证是不是匹配邮箱
    res = is_email(user_name)
    if res:
        return TABLE_ACCOUNT_CATEGORY_EMAIL

    # 2.再验证是不是匹配手机号
    res = is_mobile(user_name)
    if res:
        return TABLE_ACCOUNT_CATEGORY_PHONE

    # 如果上面都没匹配到，则默认返回自定义账号类型
    return TABLE_ACCOUNT_CATEGORY_CUSTOM


# 解绑用户-用户组
def _unbind_user_groups(user_ids, group_ids, operator_info, conn):
    """
    解绑用户-用户组
    :param user_ids: 待解绑的用户id，单个id或者列表
    :param group_ids: 待解绑的用户组id，单个id或者列表
    :param operator_info: 操作人员信息{'id':'', 'name':''}
    :param conn: 数据库链接
    :return:
    """
    if user_ids:
        # 解绑某用户的所有用户组
        sql = t_user_group.update()
        if isinstance(user_ids, int):
            sql = sql.where(t_user_group.c.user_id == user_ids)
        elif isinstance(user_ids, list):
            sql = sql.where(t_user_group.c.user_id.in_(user_ids))
        else:
            return

        sql = sql.values({
            'editor': operator_info['name'],
            'status': TABLE_STATUS_INVALID,
            'sub_status': TABLE_SUB_STATUS_INVALID_DEL,
        })
        conn.execute(sql)
    elif group_ids:
        # 解绑某用户组的所有用户
        sql = t_user_group.update()
        if isinstance(group_ids, int):
            sql = sql.where(t_user_group.c.group_id == group_ids)
        elif isinstance(group_ids, list):
            sql = sql.where(t_user_group.c.group_id.in_(group_ids))
        else:
            return

        sql = sql.values({
            'editor': operator_info['name'],
            'status': TABLE_STATUS_INVALID,
        })
        conn.execute(sql)


# 解绑用户-用户组
def unbind_user_groups(user_ids, group_ids, operator_info, conn=None):
    """
    解绑用户-用户组
    :param user_ids: 待解绑的用户id，单个id或者列表
    :param group_ids: 待解绑的用户组id，单个id或者列表
    :param operator_info: 操作人员信息{'id':'', 'name':''}
    :param conn: 数据库链接
    :return:
    """
    if not user_ids and not group_ids:
        raise MyException(status_code=HTTP_400_BAD_REQUEST,
                          detail={'code': REQ_PARAMS_NONE, 'msg': 'params can not be null'})

    if conn:
        # 解绑用户-用户组
        _unbind_user_groups(user_ids, group_ids, operator_info, conn)
    else:
        with db_engine.connect() as conn:
            # 解绑用户-用户组
            _unbind_user_groups(user_ids, group_ids, operator_info, conn)


# 绑定用户-用户组
def _bind_user_groups(user_ids, group_ids, operator_info, conn=None):
    """
    绑定用户-用户组
    :param user_ids: 待绑定的用户id，单个id或者列表
    :param group_ids: 待绑定的用户组id，单个id或者列表
    :param operator_info: 操作人员信息{'id':'', 'name':''}
    :param conn: 数据库链接
    :return:
    """
    user_id_set = set()
    group_id_set = set()
    all_user_group_list = []
    old_user_group_list = []

    sql = select([
        t_user_group.c.id,
        t_user_group.c.user_id,
        t_user_group.c.group_id,
    ])
    if isinstance(user_ids, int):
        sql = sql.where(t_user_group.c.user_id == user_ids)
        user_id_set.add(user_ids)
    elif isinstance(user_ids, list):
        sql = sql.where(t_user_group.c.user_id.in_(user_ids))
        user_id_set.update(set(user_ids))

    if isinstance(group_ids, int):
        sql = sql.where(t_user_group.c.group_id == group_ids)
        group_id_set.add(group_ids)
    elif isinstance(group_ids, list):
        sql = sql.where(t_user_group.c.group_id.in_(group_ids))
        group_id_set.update(set(group_ids))

    for user_id in user_id_set:
        for group_id in group_id_set:
            all_user_group_list.append([user_id, group_id])

    # 找出已绑定关系的记录，更新这些记录为有效
    user_group_obj_list = conn.execute(sql).fetchall()
    if user_group_obj_list:
        # 将绑定过的全部更新为有效

        update_where_and_list = []
        for user_group_obj in user_group_obj_list:
            # 更新的条件
            update_where_and_list.append(and_(
                t_user_group.c.user_id == user_group_obj.user_id,
                t_user_group.c.group_id == user_group_obj.group_id,
            ))
            old_user_group_list.append([user_group_obj.user_id, user_group_obj.group_id])

        conn.execute(t_user_group.update().where(or_(*update_where_and_list)).values({
            'editor': operator_info['name'],
            'status': TABLE_STATUS_VALID,
            'sub_status': TABLE_SUB_STATUS_VALID,
        }))

    # 取得从未绑定过的用户-角色，新增数据
    new_user_group_list = [{
        'user_id': item[0],
        'group_id': item[1],
        'creator': operator_info['name'],
    } for item in all_user_group_list if item not in old_user_group_list]
    if new_user_group_list:
        conn.execute(t_user_group.insert().values(new_user_group_list))


# 绑定用户用户组
def bind_user_groups(user_ids, group_ids, operator_info, conn=None):
    """
    绑定用户用户组
    :param user_ids: 待绑定的用户id，单个id或者列表
    :param group_ids: 待绑定的用户组id，单个id或者列表
    :param operator_info: 操作人员信息{'id':'', 'name':''}
    :param conn: 数据库链接
    :return:
    """
    # 查询用户组是否存在
    if isinstance(group_ids, int):
        get_group(group_ids)
    elif isinstance(group_ids, list):
        for group_id in group_ids:
            get_group(group_id)

    if conn:
        _bind_user_groups(user_ids, group_ids, operator_info, conn)
    else:
        with db_engine.connect() as conn:
            _bind_user_groups(user_ids, group_ids, operator_info, conn)


# 解绑用户-角色
def _unbind_user_roles(user_ids, role_ids, operator_info, conn):
    """
    解绑用户-角色
    :param user_ids: 待解绑的用户id，单个id或者列表
    :param role_ids: 待解绑的角色id，单个id或者列表
    :param operator_info: 操作人员信息{'id':'', 'name':''}
    :param conn: 数据库链接
    :return:
    """
    if user_ids:
        # 解绑某用户的所有角色
        sql = t_user_role.update()
        if isinstance(user_ids, int):
            sql = sql.where(t_user_role.c.user_id == user_ids)
        elif isinstance(user_ids, list):
            sql = sql.where(t_user_role.c.user_id.in_(user_ids))
        else:
            return

        sql = sql.values({
            'editor': operator_info['name'],
            'status': TABLE_STATUS_INVALID,
            'sub_status': TABLE_SUB_STATUS_INVALID_DEL,
        })
        conn.execute(sql)
    elif role_ids:
        # 解绑某角色的所有用户
        sql = t_user_role.update()
        if isinstance(role_ids, int):
            sql = sql.where(t_user_role.c.role_id == role_ids)
        elif isinstance(role_ids, list):
            sql = sql.where(t_user_role.c.role_id.in_(role_ids))
        else:
            return

        sql = sql.values({
            'editor': operator_info['name'],
            'status': TABLE_STATUS_INVALID,
        })
        conn.execute(sql)


# 解绑用户-角色
def unbind_user_roles(user_ids, role_ids, operator_info, conn=None):
    """
    解绑用户-角色
    :param user_ids: 待解绑的用户id，单个id或者列表
    :param role_ids: 待解绑的角色id，单个id或者列表
    :param operator_info: 操作人员信息{'id':'', 'name':''}
    :param conn: 数据库链接
    :return:
    """
    if not user_ids and not role_ids:
        raise MyException(status_code=HTTP_400_BAD_REQUEST,
                          detail={'code': REQ_PARAMS_NONE, 'msg': 'params can not be null'})

    if conn:
        # 解绑用户-角色
        _unbind_user_roles(user_ids, role_ids, operator_info, conn)
    else:
        with db_engine.connect() as conn:
            # 解绑用户-角色
            _unbind_user_roles(user_ids, role_ids, operator_info, conn)


# 绑定用户角色
def _bind_user_roles(user_ids, role_ids, operator_info, conn):
    """
    绑定用户角色
    :param user_ids: 待绑定的用户id，单个id或者列表
    :param role_ids: 待绑定的角色id，单个id或者列表
    :param operator_info: 操作人员信息{'id':'', 'name':''}
    :param conn: 数据库链接
    :return:
    """
    user_id_set = set()
    role_id_set = set()
    all_user_role_list = []
    old_user_role_list = []

    sql = select([
        t_user_role.c.id,
        t_user_role.c.user_id,
        t_user_role.c.role_id,
    ])
    if isinstance(user_ids, int):
        sql = sql.where(t_user_role.c.user_id == user_ids)
        user_id_set.add(user_ids)
    elif isinstance(user_ids, list):
        sql = sql.where(t_user_role.c.user_id.in_(user_ids))
        user_id_set.update(set(user_ids))

    if isinstance(role_ids, int):
        sql = sql.where(t_user_role.c.role_id == role_ids)
        role_id_set.add(role_ids)
    elif isinstance(role_ids, list):
        sql = sql.where(t_user_role.c.role_id.in_(role_ids))
        role_id_set.update(set(role_ids))

    for user_id in user_id_set:
        for role_id in role_id_set:
            all_user_role_list.append([user_id, role_id])

    # 找出已绑定关系的记录，更新这些记录为有效
    user_role_obj_list = conn.execute(sql).fetchall()
    if user_role_obj_list:
        # 将绑定过的全部更新为有效

        update_where_and_list = []
        for user_role_obj in user_role_obj_list:
            # 更新的条件
            update_where_and_list.append(and_(
                t_user_role.c.user_id == user_role_obj.user_id,
                t_user_role.c.role_id == user_role_obj.role_id,
            ))
            old_user_role_list.append([user_role_obj.user_id, user_role_obj.role_id])

        conn.execute(t_user_role.update().where(or_(*update_where_and_list)).values({
            'editor': operator_info['name'],
            'status': TABLE_STATUS_VALID,
            'sub_status': TABLE_SUB_STATUS_VALID,
        }))

    # 取得从未绑定过的用户-角色，新增数据
    new_user_role_list = [{
        'user_id': item[0],
        'role_id': item[1],
        'creator': operator_info['name'],
    } for item in all_user_role_list if item not in old_user_role_list]
    if new_user_role_list:
        conn.execute(t_user_role.insert().values(new_user_role_list))


# 绑定用户角色
def bind_user_roles(user_ids, role_ids, operator_info, conn=None):
    """
    绑定用户角色
    :param user_ids: 待绑定的用户id，单个id或者列表
    :param role_ids: 待绑定的角色id，单个id或者列表
    :param operator_info: 操作人员信息{'id':'', 'name':''}
    :param conn: 数据库链接
    :return:
    """
    # 查询角色是否存在
    if isinstance(role_ids, int):
        get_role(role_ids)
    elif isinstance(role_ids, list):
        for role_id in role_ids:
            get_role(role_id)

    if conn:
        # 绑定用户-角色
        _bind_user_roles(user_ids, role_ids, operator_info, conn)
    else:
        with db_engine.connect() as conn:
            # 绑定用户-角色
            _bind_user_roles(user_ids, role_ids, operator_info, conn)


# 解绑用户组-角色
def _unbind_group_roles(group_ids, role_ids, operator_info, conn):
    """
    解绑用户组-角色
    :param group_ids: 待解绑的用户组id，单个id或者列表
    :param role_ids: 待解绑的角色id，单个id或者列表
    :param operator_info: 操作人员信息{'id':'', 'name':''}
    :param conn: 数据库链接
    :return:
    """
    if group_ids:
        # 解绑某用户组的所有角色
        sql = t_group_role.update()
        if isinstance(group_ids, int):
            sql = sql.where(t_group_role.c.group_id == group_ids)
        elif isinstance(group_ids, list):
            sql = sql.where(t_group_role.c.group_id.in_(group_ids))
        else:
            return

        sql = sql.values({
            'editor': operator_info['name'],
            'status': TABLE_STATUS_INVALID,
            'sub_status': TABLE_SUB_STATUS_INVALID_DEL,
        })
        conn.execute(sql)
    elif role_ids:
        # 解绑某角色的所有用户组
        sql = t_group_role.update()
        if isinstance(role_ids, int):
            sql = sql.where(t_group_role.c.role_id == role_ids)
        elif isinstance(role_ids, list):
            sql = sql.where(t_group_role.c.role_id.in_(role_ids))
        else:
            return

        sql = sql.values({
            'editor': operator_info['name'],
            'status': TABLE_STATUS_INVALID,
        })
        conn.execute(sql)


# 解绑用户组-角色
def unbind_group_roles(group_ids, role_ids, operator_info, conn=None):
    """
    解绑用户组-角色
    :param group_ids: 待解绑的用户组id，单个id或者列表
    :param role_ids: 待解绑的角色id，单个id或者列表
    :param operator_info: 操作人员信息{'id':'', 'name':''}
    :param conn: 数据库链接
    :return:
    """
    if not group_ids and not role_ids:
        raise MyException(status_code=HTTP_400_BAD_REQUEST,
                          detail={'code': REQ_PARAMS_NONE, 'msg': 'params can not be null'})

    if conn:
        # 解绑用户组-角色
        _unbind_group_roles(group_ids, role_ids, operator_info, conn)
    else:
        with db_engine.connect() as conn:
            # 解绑用户组-角色
            _unbind_group_roles(group_ids, role_ids, operator_info, conn)


# 绑定用户组角色
def _bind_group_roles(group_ids, role_ids, operator_info, conn):
    """
    绑定用户组角色
    :param group_ids: 待绑定的用户组id，单个id或者列表
    :param role_ids: 待绑定的角色id，单个id或者列表
    :param operator_info: 操作人员信息{'id':'', 'name':''}
    :param conn: 数据库链接
    :return:
    """
    group_id_set = set()
    role_id_set = set()
    all_group_role_list = []
    old_group_role_list = []

    sql = select([
        t_group_role.c.id,
        t_group_role.c.group_id,
        t_group_role.c.role_id,
    ])
    if isinstance(group_ids, int):
        sql = sql.where(t_group_role.c.group_id == group_ids)
        group_id_set.add(group_ids)
    elif isinstance(group_ids, list):
        sql = sql.where(t_group_role.c.group_id.in_(group_ids))
        group_id_set.update(set(group_ids))

    if isinstance(role_ids, int):
        sql = sql.where(t_group_role.c.role_id == role_ids)
        role_id_set.add(role_ids)
    elif isinstance(role_ids, list):
        sql = sql.where(t_group_role.c.role_id.in_(role_ids))
        role_id_set.update(set(role_ids))

    for group_id in group_id_set:
        for role_id in role_id_set:
            all_group_role_list.append([group_id, role_id])

    # 找出已绑定关系的记录，更新这些记录为有效
    group_role_obj_list = conn.execute(sql).fetchall()
    if group_role_obj_list:
        # 将绑定过的全部更新为有效

        update_where_and_list = []
        for group_role_obj in group_role_obj_list:
            # 更新的条件
            update_where_and_list.append(and_(
                t_group_role.c.group_id == group_role_obj.group_id,
                t_group_role.c.role_id == group_role_obj.role_id,
            ))
            old_group_role_list.append([group_role_obj.group_id, group_role_obj.role_id])

        conn.execute(t_group_role.update().where(or_(*update_where_and_list)).values({
            'editor': operator_info['name'],
            'status': TABLE_STATUS_VALID,
            'sub_status': TABLE_SUB_STATUS_VALID,
        }))

    # 取得从未绑定过的用户组-角色，新增数据
    new_group_role_list = [{
        'group_id': item[0],
        'role_id': item[1],
        'creator': operator_info['name'],
    } for item in all_group_role_list if item not in old_group_role_list]
    if new_group_role_list:
        conn.execute(t_group_role.insert().values(new_group_role_list))


# 绑定用户组角色
def bind_group_roles(group_ids, role_ids, operator_info, conn=None):
    """
    绑定用户组角色
    :param group_ids: 待绑定的用户组id，单个id或者列表
    :param role_ids: 待绑定的角色id，单个id或者列表
    :param operator_info: 操作人员信息{'id':'', 'name':''}
    :param conn: 数据库链接
    :return:
    """
    # 查询角色是否存在
    if isinstance(role_ids, int):
        get_role(role_ids)
    elif isinstance(role_ids, list):
        for role_id in role_ids:
            get_role(role_id)

    if conn:
        # 绑定用户组-角色
        _bind_group_roles(group_ids, role_ids, operator_info, conn)
    else:
        with db_engine.connect() as conn:
            # 绑定用户组-角色
            _bind_group_roles(group_ids, role_ids, operator_info, conn)











# # 解绑角色-权限
# def _unbind_role_permission(role_ids, permission_ids, operator_info, conn):
#     """
#     解绑角色-权限
#     :param role_ids: 待解绑的角色id，单个id或者列表
#     :param permission_ids: 待解绑的权限id，单个id或者列表
#     :param operator_info: 操作人员信息{'id':'', 'name':''}
#     :param conn: 数据库链接
#     :return:
#     """
#     if permission_ids:
#         # 解绑某权限的所有角色
#         sql = t_group_role.update()
#         if isinstance(permission_ids, int):
#             sql = sql.where(t_group_role.c.permission_id == permission_ids)
#         elif isinstance(permission_ids, list):
#             sql = sql.where(t_group_role.c.permission_id.in_(permission_ids))
#         else:
#             return
#
#         sql = sql.values({
#             'editor': operator_info['name'],
#             'status': TABLE_STATUS_INVALID,
#             'sub_status': TABLE_SUB_STATUS_INVALID_DEL,
#         })
#         conn.execute(sql)
#     elif role_ids:
#         # 解绑某角色的所有权限
#         sql = t_group_role.update()
#         if isinstance(role_ids, int):
#             sql = sql.where(t_group_role.c.role_id == role_ids)
#         elif isinstance(role_ids, list):
#             sql = sql.where(t_group_role.c.role_id.in_(role_ids))
#         else:
#             return
#
#         sql = sql.values({
#             'editor': operator_info['name'],
#             'status': TABLE_STATUS_INVALID,
#         })
#         conn.execute(sql)
#
#
# # 解绑角色-权限
# def unbind_role_permission(permission_ids, role_ids, operator_info, conn=None):
#     """
#     解绑角色-权限
#     :param permission_ids: 待解绑的权限id，单个id或者列表
#     :param role_ids: 待解绑的角色id，单个id或者列表
#     :param operator_info: 操作人员信息{'id':'', 'name':''}
#     :param conn: 数据库链接
#     :return:
#     """
#     if not permission_ids and not role_ids:
#         raise MyException(status_code=HTTP_400_BAD_REQUEST,
#                           detail={'code': REQ_PARAMS_NONE, 'msg': 'params can not be null'})
#
#     if conn:
#         # 解绑角色-权限
#         _unbind_role_permission(permission_ids, role_ids, operator_info, conn)
#     else:
#         with db_engine.connect() as conn:
#             # 解绑角色-权限
#             _unbind_role_permission(permission_ids, role_ids, operator_info, conn)
#
#
# # 绑定权限角色
# def _bind_role_permission(permission_ids, role_ids, operator_info, conn):
#     """
#     绑定权限角色
#     :param permission_ids: 待绑定的权限id，单个id或者列表
#     :param role_ids: 待绑定的角色id，单个id或者列表
#     :param operator_info: 操作人员信息{'id':'', 'name':''}
#     :param conn: 数据库链接
#     :return:
#     """
#     permission_id_set = set()
#     role_id_set = set()
#     all_group_role_list = []
#     old_group_role_list = []
#
#     sql = select([
#         t_group_role.c.id,
#         t_group_role.c.permission_id,
#         t_group_role.c.role_id,
#     ])
#     if isinstance(permission_ids, int):
#         sql = sql.where(t_group_role.c.permission_id == permission_ids)
#         permission_id_set.add(permission_ids)
#     elif isinstance(permission_ids, list):
#         sql = sql.where(t_group_role.c.permission_id.in_(permission_ids))
#         permission_id_set.update(set(permission_ids))
#
#     if isinstance(role_ids, int):
#         sql = sql.where(t_group_role.c.role_id == role_ids)
#         role_id_set.add(role_ids)
#     elif isinstance(role_ids, list):
#         sql = sql.where(t_group_role.c.role_id.in_(role_ids))
#         role_id_set.update(set(role_ids))
#
#     for permission_id in permission_id_set:
#         for role_id in role_id_set:
#             all_group_role_list.append([permission_id, role_id])
#
#     # 找出已绑定关系的记录，更新这些记录为有效
#     group_role_obj_list = conn.execute(sql).fetchall()
#     if group_role_obj_list:
#         # 将绑定过的全部更新为有效
#
#         update_where_and_list = []
#         for group_role_obj in group_role_obj_list:
#             # 更新的条件
#             update_where_and_list.append(and_(
#                 t_group_role.c.permission_id == group_role_obj.permission_id,
#                 t_group_role.c.role_id == group_role_obj.role_id,
#             ))
#             old_group_role_list.append([group_role_obj.permission_id, group_role_obj.role_id])
#
#         conn.execute(t_group_role.update().where(or_(*update_where_and_list)).values({
#             'editor': operator_info['name'],
#             'status': TABLE_STATUS_VALID,
#             'sub_status': TABLE_SUB_STATUS_VALID,
#         }))
#
#     # 取得从未绑定过的角色-权限，新增数据
#     new_group_role_list = [{
#         'permission_id': item[0],
#         'role_id': item[1],
#         'creator': operator_info['name'],
#     } for item in all_group_role_list if item not in old_group_role_list]
#     if new_group_role_list:
#         conn.execute(t_group_role.insert().values(new_group_role_list))
#
#
# # 绑定权限角色
# def bind_role_permission(role_ids, permission_ids, operator_info, conn=None):
#     """
#     绑定角色-权限
#     :param role_ids: 待绑定的角色id，单个id或者列表
#     :param permission_ids: 待绑定的权限id，单个id或者列表
#     :param operator_info: 操作人员信息{'id':'', 'name':''}
#     :param conn: 数据库链接
#     :return:
#     """
#     # 查询角色是否存在
#     if isinstance(role_ids, int):
#         get_permission(role_ids)
#     elif isinstance(role_ids, list):
#         for role_id in role_ids:
#             get_role(role_id)
#
#     if conn:
#         # 绑定角色-权限
#         _bind_role_permission(permission_ids, role_ids, operator_info, conn)
#     else:
#         with db_engine.connect() as conn:
#             # 绑定角色-权限
#             _bind_role_permission(permission_ids, role_ids, operator_info, conn)












# 绑定角色-权限
def _bind_role_permission(role_id, permission_id, operator_info, conn):
    """
    绑定角色-权限
    :param role_id: 待绑定的角色id
    :param permission_id: 待绑定的权限id
    :param operator_info: 操作人员信息{'id':'', 'name':''}
    :param conn: 数据库链接
    :return:
    """
    # 查找当前角色是否绑定过该权限
    role_permission_obj = conn.execute(select([
        t_role_permission.c.id,
        t_role_permission.c.role_id,
        t_role_permission.c.permission_id,
        t_role_permission.c.status,
    ]).where(and_(
        t_role_permission.c.role_id == role_id,
        t_role_permission.c.permission_id == permission_id,
    )).limit(1)).fetchone()
    if role_permission_obj:
        # 已经绑定过
        if role_permission_obj.status != TABLE_STATUS_VALID:
            # 当前绑定关系已经无效了，将其改为有效
            conn.execute(t_role_permission.update().where(t_role_permission.c.id == role_permission_obj.id).values({
                'status': TABLE_STATUS_VALID,
                'sub_status': TABLE_SUB_STATUS_VALID,
                'editor': operator_info['name'],
            }))
    else:
        # 从未给角色绑定过该权限
        conn.execute(t_role_permission.insert().values({
            'role_id': role_id,
            'permission_id': permission_id,
            'creator': operator_info['name'],
        }))


# 绑定角色-权限
def bind_role_permission(role_id, permission_id, operator_info, conn):
    """
    绑定角色-权限
    :param role_id: 待绑定的角色id
    :param permission_id: 待绑定的权限id
    :param operator_info: 操作人员信息{'id':'', 'name':''}
    :param conn: 数据库链接
    :return:
    """
    if conn:
        _bind_role_permission(role_id, permission_id, operator_info, conn)
    else:
        with db_engine.connect() as conn:
            _bind_role_permission(role_id, permission_id, operator_info, conn)


# 检测表的有效的唯一字段是否唯一
def _is_code_unique(table: Table, code: str, conn):
    """
    检测表的有效的唯一字段是否唯一
    :param table: 表对象
    :param code: 字段名
    :param conn: 数据库连接
    :return:
    """
    sql = select([table.c.id]).where(and_(
        table.c.code == code,
        table.c.status == TABLE_STATUS_VALID
    )).limit(1)
    res = conn.execute(sql).fetchone()
    if res:
        return False
    else:
        return True


# 检测表的有效的唯一字段是否唯一
def is_code_unique(table: Table, code: str, conn=None):
    """
    检测表的有效的唯一字段是否唯一
    :param table: 表对象
    :param code: 字段名
    :param conn: 数据库连接
    :return:
    """
    if conn:
        return _is_code_unique(table, code, conn)
    else:
        with db_engine.connect() as conn:
            return _is_code_unique(table, code, conn)


