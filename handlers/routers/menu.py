# -*- coding: utf-8 -*-
from sqlalchemy.sql import and_

from fastapi import APIRouter
from fastapi import Depends

from commons.const import *

from models.mysql import db_engine, t_menu, t_permission, t_menu_permission
from models.const import *

from handlers import tool
from handlers.item import ItemOutMenus, ItemInAddMenu, ItemInEditMenu, ItemOutOperateSuccess, ItemOutOperateFailed
from handlers.exp import MyException
from handlers.const import *

router = APIRouter(tags=[TAGS_MENU], dependencies=[Depends(tool.check_token)])


@router.get("/menu", response_model=ItemOutMenus, name='获取菜单')
async def get_menus(userinfo: dict = Depends(tool.get_userinfo_from_token)):
    # async def get_menus(userinfo: dict = Depends(tool.get_userinfo_from_token)):
    # 根据用户角色权限 + 用户组角色权限，查找该角色有哪些菜单

    item_out = ItemOutMenus()

    permission_list = tool.get_user_permission(userinfo['id'])
    menu_list = tool.get_menus_by_permission([permission.id for permission in permission_list])
    target_menus = []
    tool.menu_serialize(0, menu_list, target_menus)
    item_out.data = target_menus
    return item_out


@router.post("/menu", response_model=ItemOutOperateSuccess, name='添加菜单')
async def add_menu(item_in: ItemInAddMenu, userinfo: dict = Depends(tool.get_userinfo_from_token)):
    """
    添加菜单\n
    :param item_in:\n
    :param userinfo:\n
    :return:
    """
    # 鉴权
    if not tool.has_operation_permission(userinfo['id'], PERMISSION_MENU_ADD):
        # 没有添加菜单的权限
        raise MyException(status_code=HTTP_401_UNAUTHORIZED, detail={'code': AUTH_PERMISSION_HAVE_NOT, 'msg': 'you have not permission to operate'})

    conn = db_engine.connect()
    trans = conn.begin()

    try:

        # 1.新增菜单
        menu_val = {
            'creator': userinfo['name']
        }
        menu_val.update(item_in.dict())
        menu_sql = t_menu.insert().values(menu_val)
        menu_res = conn.execute(menu_sql)

        # 2.新增该菜单的可见权限
        permission_sql = t_permission.insert().values({
            'pid': 0,
            'code': 'PERMISSION_{}_QUERY'.format(item_in.code),
            'name': '{}菜单访问'.format(item_in.name),
            'intro': '[{}菜单访问]权限'.format(item_in.name),
            'category': 1,
            'creator': userinfo['name']
        })
        permission_res = conn.execute(permission_sql)

        # 3.绑定菜单与可见权限关系
        menu_permission_sql = t_menu_permission.insert().values({
            'menu_id': menu_res.lastrowid,
            'permission_id': permission_res.lastrowid,
            'creator': userinfo['name']
        })
        conn.execute(menu_permission_sql)

        # 4.提交事务
        trans.commit()

        return ItemOutOperateSuccess()

    except MyException as mex:
        raise mex
    except:
        trans.rollback()
        raise MyException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=ItemOutOperateFailed(code=HTTP_500_INTERNAL_SERVER_ERROR, msg='inter server error'))
    finally:
        conn.close()


@router.put("/menu/{menu_id}", response_model=ItemOutOperateSuccess, name="修改菜单")
async def edit_menu(menu_id: int, item_in: ItemInEditMenu, userinfo: dict = Depends(tool.get_userinfo_from_token)):
    """
    修改菜单\n
    :param menu_id:\n
    :param item_in:\n
    :param userinfo:\n
    :return:
    """
    # 鉴权
    if not tool.has_operation_permission(userinfo['id'], PERMISSION_MENU_EDIT):
        # 没有修改菜单的权限
        raise MyException(status_code=HTTP_401_UNAUTHORIZED,
                          detail={'code': AUTH_PERMISSION_HAVE_NOT, 'msg': 'you have not permission to operate'})

    conn = db_engine.connect()
    trans = conn.begin()

    try:
        # 查找菜单
        menu_sql = t_menu.select().where(t_menu.c.id == menu_id).limit(1).with_for_update()
        menu_obj = conn.execute(menu_sql).fetchone()
        if not menu_obj:
            raise MyException(status_code=HTTP_404_NOT_FOUND, detail={'code': HTTP_404_NOT_FOUND, 'msg': 'menu not exists'})

        # 修改菜单
        # 过滤掉空字段
        item_dict = dict((k, v) for k, v in item_in.dict().items() if v is not None)
        item_dict['editor'] = userinfo['name']
        update_menu_sql = t_menu.update().where(t_menu.c.id == menu_id).values(item_dict)
        conn.execute(update_menu_sql)

        permission_dict = {}
        if item_in.name and menu_obj.name != item_in.name:
            permission_dict['name'] = '{}菜单访问'.format(item_in.name)
            permission_dict['intro'] = '[{}菜单访问]权限'.format(item_in.name)

        if item_in.code and menu_obj.code != item_in.code:
            permission_dict['code'] = 'PERMISSION_{}_QUERY'.format(item_in.code)

        if permission_dict:
            # 因修改菜单而导致权限名称无法人眼识别，故同步修改权限

            # 从菜单-权限绑定关系中，获取权限信息
            menu_permission_sql = t_menu_permission.select().where(t_menu_permission.c.menu_id == menu_id).limit(1)
            menu_permission_obj = conn.execute(menu_permission_sql).fetchone()

            permission_dict['editor'] = userinfo['name']
            permission_sql = t_permission.update().where(t_permission.c.id == menu_permission_obj.permission_id).values(permission_dict)
            conn.execute(permission_sql)

        # 提交事务
        trans.commit()

        return ItemOutOperateSuccess()

    except MyException as mex:
        raise mex
    except:
        trans.rollback()
        raise MyException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=ItemOutOperateFailed(code=HTTP_500_INTERNAL_SERVER_ERROR, msg='inter server error'))
    finally:
        conn.close()


@router.put("/menu/{menu_id}/disable", name="禁用菜单", response_model=ItemOutOperateSuccess)
async def disable_menu(menu_id: int, userinfo: dict = Depends(tool.get_userinfo_from_token)):
    """
    禁用菜单\n
    :param menu_id:\n
    :param userinfo:\n
    :return:
    """
    # 鉴权
    if not tool.has_operation_permission(userinfo['id'], PERMISSION_MENU_DISABLE):
        # 没有禁用菜单的权限
        raise MyException(status_code=HTTP_401_UNAUTHORIZED,
                          detail={'code': AUTH_PERMISSION_HAVE_NOT, 'msg': 'you have not permission to operate'})

    conn = db_engine.connect()
    trans = conn.begin()

    try:
        # 1.查找菜单
        menu_sql = t_menu.select().where(t_menu.c.id == menu_id).limit(1).with_for_update()
        menu_obj = conn.execute(menu_sql).fetchone()
        if not menu_obj:
            raise MyException(status_code=HTTP_404_NOT_FOUND, detail={'code': HTTP_404_NOT_FOUND, 'msg': 'menu not exists'})

        # 2.修改菜单状态为禁用
        update_menu_sql = t_menu.update().where(and_(
            t_menu.c.id == menu_id,
            t_menu.c.status == TABLE_STATUS_VALID,
            t_menu.c.sub_status == TABLE_SUB_STATUS_VALID,
        )).values({
            'status': TABLE_STATUS_INVALID,
            'sub_status': TABLE_SUB_STATUS_INVALID_DISABLE
        })
        conn.execute(update_menu_sql)

        # 3.提交事务
        trans.commit()

        return ItemOutOperateSuccess()

    except MyException as mex:
        raise mex
    except:
        trans.rollback()
        raise MyException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=ItemOutOperateFailed(code=HTTP_500_INTERNAL_SERVER_ERROR, msg='inter server error'))
    finally:
        conn.close()


@router.put("/menu/{menu_id}/enable", name='启用菜单', response_model=ItemOutOperateSuccess)
async def enable_menu(menu_id: int, userinfo: dict = Depends(tool.get_userinfo_from_token)):
    """
    启用菜单\n
    :param menu_id:\n
    :param userinfo:\n
    :return:
    """
    # 鉴权
    if not tool.has_operation_permission(userinfo['id'], PERMISSION_MENU_ENABLE):
        # 没有启用菜单的权限
        raise MyException(status_code=HTTP_401_UNAUTHORIZED,
                          detail={'code': AUTH_PERMISSION_HAVE_NOT, 'msg': 'you have not permission to operate'})

    conn = db_engine.connect()
    trans = conn.begin()

    try:
        # 1.查找菜单
        menu_sql = t_menu.select().where(t_menu.c.id == menu_id).limit(1).with_for_update()
        menu_obj = conn.execute(menu_sql).fetchone()
        if not menu_obj:
            raise MyException(status_code=HTTP_404_NOT_FOUND, detail={'code': HTTP_404_NOT_FOUND, 'msg': 'menu not exists'})

        # 2.修改菜单状态为启用
        update_menu_sql = t_menu.update().where(and_(
            t_menu.c.id == menu_id,
            t_menu.c.status == TABLE_STATUS_INVALID,
            t_menu.c.sub_status == TABLE_SUB_STATUS_INVALID_DISABLE,
        )).values({
            'status': TABLE_STATUS_VALID,
            'sub_status': TABLE_SUB_STATUS_VALID
        })
        conn.execute(update_menu_sql)

        # 3.提交事务
        trans.commit()

        return ItemOutOperateSuccess()

    except MyException as mex:
        raise mex
    except:
        trans.rollback()
        raise MyException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=ItemOutOperateFailed(code=HTTP_500_INTERNAL_SERVER_ERROR, msg='inter server error'))
    finally:
        conn.close()


@router.delete("/menu/{menu_id}", name='删除菜单', response_model=ItemOutOperateSuccess)
async def del_menu(menu_id: int, userinfo: dict = Depends(tool.get_userinfo_from_token)):
    """
    删除菜单\n
    :param menu_id:\n
    :param userinfo:\n
    :return:
    """
    # 鉴权
    if not tool.has_operation_permission(userinfo['id'], PERMISSION_MENU_DEL):
        # 没有删除菜单的权限
        raise MyException(status_code=HTTP_401_UNAUTHORIZED,
                          detail={'code': AUTH_PERMISSION_HAVE_NOT, 'msg': 'you have not permission to operate'})

    conn = db_engine.connect()
    trans = conn.begin()

    try:
        # 1.查找菜单
        menu_sql = t_menu.select().where(t_menu.c.id == menu_id).limit(1).with_for_update()
        menu_obj = conn.execute(menu_sql).fetchone()
        if not menu_obj:
            raise MyException(status_code=HTTP_404_NOT_FOUND, detail={'code': HTTP_404_NOT_FOUND, 'msg': 'menu not exists'})

        # 2.修改菜单状态为无效（软删除）
        update_menu_sql = t_menu.update().where(and_(
            t_menu.c.id == menu_id,
            t_menu.c.sub_status != TABLE_SUB_STATUS_INVALID_DEL,
        )).values({
            'status': TABLE_STATUS_INVALID,
            'sub_status': TABLE_SUB_STATUS_INVALID_DEL
        })
        conn.execute(update_menu_sql)

        # 3.提交事务
        trans.commit()

        return ItemOutOperateSuccess()

    except MyException as mex:
        raise mex
    except:
        trans.rollback()
        raise MyException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=ItemOutOperateFailed(code=HTTP_500_INTERNAL_SERVER_ERROR, msg='inter server error'))
    finally:
        conn.close()
