# -*- coding: utf-8 -*-
from sqlalchemy.sql import and_
from sqlalchemy import func, select

from fastapi import APIRouter, Query, Depends

from commons.code import *

from models.mysql.system import db_engine, t_permission, t_menu_permission, t_menu
from models.mysql import *

from handlers import tool
from handlers.items.menu import *
from handlers.items import ItemOutOperateSuccess, ItemOutOperateFailed
from handlers.exp import MyException
from handlers.const import *

router = APIRouter(tags=[TAGS_MENU], dependencies=[Depends(tool.check_token)])


@router.get("/init_menu", name='初始化菜单')
async def init_menus(userinfo: dict = Depends(tool.get_userinfo_from_token)):
    permission_list = tool.get_user_permission(userinfo['id'])
    menu_list = tool.get_menus_by_permission([permission.id for permission in permission_list])
    target_menus = []
    tool.menu_serialize(0, menu_list, target_menus)
    o_menu = settings.web.o_menu

    o_menu['menuInfo'][0]['child'].extend(target_menus)
    return o_menu


@router.get("/menu", response_model=ItemOutMenuList, name='获取菜单')
async def get_menus(userinfo: dict = Depends(tool.get_userinfo_from_token), page: Optional[int] = Query(settings.web.page, description='第几页'), limit: Optional[int] = Query(settings.web.page_size, description='每页条数')):
    item_out = ItemOutMenuList()

    # 鉴权
    tool.check_operation_permission(userinfo['id'], PERMISSION_MENU_VIEW)

    with db_engine.connect() as conn:
        # 获取当前有多少数据
        count_sql = select([func.count(t_menu.c.id)]).where(t_menu.c.sub_status != TABLE_SUB_STATUS_INVALID_DEL)
        total = conn.execute(count_sql).scalar()

        # 获取分页后的用户组列表
        menu_sql = select([
            t_menu.c.id,
            t_menu.c.pid,
            t_menu.c.code,
            t_menu.c.name,
            t_menu.c.uri,
            t_menu.c.intro,
            t_menu.c.status,
            t_menu.c.sub_status,
        ]).where(t_menu.c.sub_status != TABLE_SUB_STATUS_INVALID_DEL).order_by('sort', 'id')

        if page != 0:
            menu_sql = menu_sql.limit(limit).offset((page - 1) * limit)
        menu_obj_list = conn.execute(menu_sql).fetchall()
        item_out.data = ListDataMenu(
        result=[ItemOutMenus(
            id=menu_obj.id,
            title=menu_obj.name,
            code=menu_obj.code,
            href=menu_obj.uri,
            intro=menu_obj.intro,
            status=menu_obj.status,
            sub_status=menu_obj.sub_status,
    ) for menu_obj in menu_obj_list],
        total=total,
        page=page,
        limit=limit,
    )
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
    tool.check_operation_permission(userinfo['id'], PERMISSION_MENU_ADD)

    conn = db_engine.connect()
    trans = conn.begin()

    try:
        # 查看是否已经有该code的用户组
        if not tool.is_code_unique(t_menu, item_in.code, conn):
            raise MyException(status_code=HTTP_400_BAD_REQUEST, detail={'code': MULTI_DATA, 'msg': 'code repeat'})

        # 新增菜单
        menu_val = {
            'creator': userinfo['name']
        }
        menu_val.update(item_in.dict())
        menu_sql = t_menu.insert().values(menu_val)
        menu_res = conn.execute(menu_sql)

        # 新增该菜单的可见权限
        permission_sql = t_permission.insert().values({
            'pid': 0,
            'code': 'PERMISSION_{}_QUERY'.format(item_in.code),
            'name': '{}菜单访问'.format(item_in.name),
            'intro': '[{}菜单访问]权限'.format(item_in.name),
            'category': 1,
            'creator': userinfo['name']
        })
        permission_res = conn.execute(permission_sql)

        # 绑定菜单与可见权限关系
        menu_permission_sql = t_menu_permission.insert().values({
            'menu_id': menu_res.lastrowid,
            'permission_id': permission_res.lastrowid,
            'creator': userinfo['name']
        })
        conn.execute(menu_permission_sql)

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
    tool.check_operation_permission(userinfo['id'], PERMISSION_MENU_EDIT)

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
        if item_in.name is not None and menu_obj.name != item_in.name:
            permission_dict['name'] = '{}菜单访问'.format(item_in.name)
            permission_dict['intro'] = '[{}菜单访问]权限'.format(item_in.name)

        if item_in.code is not None and menu_obj.code != item_in.code:
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
    tool.check_operation_permission(userinfo['id'], PERMISSION_MENU_DISABLE)

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
    tool.check_operation_permission(userinfo['id'], PERMISSION_MENU_ENABLE)

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
    tool.check_operation_permission(userinfo['id'], PERMISSION_MENU_DEL)

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
