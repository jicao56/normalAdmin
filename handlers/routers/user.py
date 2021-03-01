# -*- coding: utf-8 -*-
from typing import Optional

from sqlalchemy.sql import and_
from sqlalchemy import func, select

from fastapi import APIRouter, Query
from fastapi import Depends

from commons.const import *
from commons.func import md5, REGEX_MOBILE


from settings import settings

from models.mysql import db_engine, t_user, t_account
from models.const import *

from handlers import tool
from handlers.items import ItemOutOperateSuccess, ItemOutOperateFailed
from handlers.items.user import ListDataUser, ItemInAddUser, ItemInEditUser, ItemInBindUserGroup, ItemInBindUserRole, ItemOutUserList, ItemOutUser
from handlers.exp import MyException
from handlers.const import *

router = APIRouter(tags=[TAGS_USER], dependencies=[Depends(tool.check_token)])


@router.get("/user", tags=[TAGS_USER], response_model=ItemOutUserList, name='获取用户')
async def get_users(userinfo: dict = Depends(tool.get_userinfo_from_token), p: Optional[int] = Query(settings.web.page, description='第几页'), ps: Optional[int] = Query(settings.web.page_size, description='每页条数'), name: Optional[str] = Query(None, description='用户名'), mobile: Optional[str] = Query(None, description='用户手机号', regex=REGEX_MOBILE)):
    item_out = ItemOutUserList()

    # 检查权限
    tool.check_operation_permission(userinfo['id'], PERMISSION_USER_VIEW)

    with db_engine.connect() as conn:
        # 获取当前有多少数据
        count_sql = select([func.count(t_user.c.id)])

        # 获取分页后的用户列表
        user_sql = select([
            t_user.c.id,
            t_user.c.name,
            t_user.c.head_img_url,
            t_user.c.mobile,
            t_user.c.status,
            t_user.c.sub_status,
        ])

        if name is not None:
            # 用户名过滤
            name = name.strip()
            count_sql = count_sql.where(t_user.c.name.like('%{}%'.format(name)))
            user_sql = user_sql.where(t_user.c.name.like('%{}%'.format(name)))

        if mobile is not None:
            # 用户手机号过滤
            mobile = mobile.strip()
            count_sql = count_sql.where(t_user.c.mobile.like('%{}%'.format(mobile)))
            user_sql = user_sql.where(t_user.c.mobile.like('%{}%'.format(mobile)))

        total = conn.execute(count_sql).scalar()

        user_sql = user_sql.order_by('sort', 'id').limit(ps).offset((p - 1) * ps)
        user_obj_list = conn.execute(user_sql).fetchall()

    item_out.data = ListDataUser(
        result=[ItemOutUser(
        id=user_obj.id,
        name=user_obj.name,
        head_img_url=user_obj.head_img_url,
        mobile=user_obj.mobile,
        status=user_obj.status,
        sub_status=user_obj.sub_status,
    ) for user_obj in user_obj_list],
        total=total,
        p=p,
        ps=ps,
    )
    return item_out


@router.post("/user", tags=[TAGS_USER], response_model=ItemOutOperateSuccess, name='添加用户')
async def add_user(item_in: ItemInAddUser, userinfo: dict = Depends(tool.get_userinfo_from_token)):
    """
    添加用户\n
    :param item_in:\n
    :param userinfo:\n
    :return:
    """
    # 鉴权
    tool.check_operation_permission(userinfo['id'], PERMISSION_USER_ADD)

    conn = db_engine.connect()
    trans = conn.begin()

    try:
        # 1.新增用户
        # 1.1 设置用户盐值
        user_salt = tool.get_rand_str(6)
        # 1.2 执行新增
        user_val = {
            'name': item_in.name,
            'head_img_url': item_in.head_img_url,
            'mobile': item_in.mobile,
            'email': item_in.email,
            'salt': user_salt,
            'password': md5(item_in.password, user_salt),
            'creator': userinfo['name']
        }
        user_sql = t_user.insert().values(user_val)
        user_res = conn.execute(user_sql)

        # 2.新增账号
        # 添加一个用户名的登录账号
        account_sql = t_account.insert().values({
            'user_id': user_res.lastrowid,
            'open_code': item_in.name,
            'category': TABLE_ACCOUNT_CATEGORY_CUSTOM,
            'creator': userinfo['name']
        })
        conn.execute(account_sql)

        if item_in.email:
            # 填写了邮箱，添加一个邮箱的登录账号
            account_sql = t_account.insert().values({
                'user_id': user_res.lastrowid,
                'open_code': item_in.email,
                'category': TABLE_ACCOUNT_CATEGORY_EMAIL,
                'creator': userinfo['name']
            })
            conn.execute(account_sql)

        if item_in.mobile:
            # 填写了手机号，添加一个手机号的登录账号
            account_sql = t_account.insert().values({
                'user_id': user_res.lastrowid,
                'open_code': item_in.mobile,
                'category': TABLE_ACCOUNT_CATEGORY_PHONE,
                'creator': userinfo['name']
            })
            conn.execute(account_sql)

        if item_in.role_id:
            # 3.指定了角色，绑定用户角色关系
            tool.bind_user_role(user_res.lastrowid, item_in.role_id, userinfo, conn)

        if item_in.group_id:
            # 4.指定了组，绑定用户与组关系
            tool.bind_user_group(user_res.lastrowid, item_in.group_id, userinfo, conn)

        trans.commit()
        return ItemOutOperateSuccess()
    except MyException as mex:
        trans.rollback()
        raise mex
    except Exception as ex:
        trans.rollback()
        raise MyException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=ItemOutOperateFailed(code=HTTP_500_INTERNAL_SERVER_ERROR, msg=str(ex)))
    finally:
        conn.close()


@router.put("/user/{user_id}", tags=[TAGS_USER], response_model=ItemOutOperateSuccess, name="修改用户")
async def edit_user(user_id: int, item_in: ItemInEditUser, userinfo: dict = Depends(tool.get_userinfo_from_token)):
    """
    修改用户\n
    :param user_id:\n
    :param item_in:\n
    :param userinfo:\n
    :return:
    """
    # 鉴权
    tool.check_operation_permission(userinfo['id'], PERMISSION_USER_EDIT)

    conn = db_engine.connect()
    trans = conn.begin()

    try:
        # 1.查找用户
        user_sql = t_user.select().where(t_user.c.id == user_id).limit(1).with_for_update()
        user_obj = conn.execute(user_sql).fetchone()
        if not user_obj:
            raise MyException(status_code=HTTP_404_NOT_FOUND, detail={'code': HTTP_404_NOT_FOUND, 'msg': 'user not exists'})

        # 2.修改用户
        user_val = {
            'editor': userinfo['name']
        }
        if item_in.name:
            user_val['name'] = item_in.name
        if item_in.head_img_url:
            user_val['head_img_url'] = item_in.head_img_url
        if item_in.mobile:
            user_val['mobile'] = item_in.mobile
        if item_in.email:
            user_val['email'] = item_in.email
        if item_in.password:
            user_val['password'] = item_in.password

        update_user_sql = t_user.update().where(t_user.c.id == user_id).values(user_val)
        conn.execute(update_user_sql)

        # 3.修改账号
        # 3.1 获取账号
        account_sql = t_account.select().where(t_account.c.user_id == user_obj.id).order_by('sort', 'id').with_for_update()
        account_res = conn.execute(account_sql).fetchall()
        # 3.2 遍历账号，并修改
        for account in account_res:
            if account.category == TABLE_ACCOUNT_CATEGORY_CUSTOM and item_in.name and account.open_code != item_in.name:
                # 账号类型为自定义，并且修改了用户名
                tmp_account_update_sql = t_account.update().where(t_account.c.id == account.id).values({
                    'open_code': item_in.name,
                    'editor': userinfo['name']
                })
                conn.execute(tmp_account_update_sql)

            elif account.category == TABLE_ACCOUNT_CATEGORY_PHONE and item_in.mobile and account.open_code != item_in.mobile:
                # 账号类型为手机号，并且用户修改了手机号
                tmp_account_update_sql = t_account.update().where(t_account.c.id == account.id).values({
                    'open_code': item_in.mobile,
                    'editor': userinfo['name']
                })
                conn.execute(tmp_account_update_sql)

            elif account.category == TABLE_ACCOUNT_CATEGORY_EMAIL and item_in.email and account.open_code != item_in.email:
                # 账号类型为手机号，并且用户修改了手机号
                tmp_account_update_sql = t_account.update().where(t_account.c.id == account.id).values({
                    'open_code': item_in.mobile,
                    'editor': userinfo['name']
                })
                conn.execute(tmp_account_update_sql)

        if item_in.role_id:
            # 4.指定了角色，绑定用户角色关系
            tool.bind_user_role(user_id, item_in.role_id, userinfo, conn)

        if item_in.group_id:
            # 5.指定了组，绑定用户与组关系
            tool.bind_user_group(user_id, item_in.group_id, userinfo, conn)

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


@router.put("/user/{user_id}/disable", tags=[TAGS_USER], name="禁用用户")
async def disable_user(user_id: int, userinfo: dict = Depends(tool.get_userinfo_from_token)):
    """
    禁用用户\n
    :param user_id:\n
    :param userinfo:\n
    :return:
    """
    # 鉴权
    tool.check_operation_permission(userinfo['id'], PERMISSION_USER_DISABLE)

    conn = db_engine.connect()
    trans = conn.begin()

    try:
        # 1.查找用户
        user_sql = t_user.select().where(t_user.c.id == user_id).limit(1).with_for_update()
        conn.execute(user_sql).fetchone()

        # 2.修改用户状态为禁用
        update_user_sql = t_user.update().where(and_(
            t_user.c.id == user_id,
            t_user.c.status == TABLE_STATUS_VALID,
            t_user.c.sub_status == TABLE_SUB_STATUS_VALID,
        )).values({
            'status': TABLE_STATUS_INVALID,
            'sub_status': TABLE_SUB_STATUS_INVALID_DISABLE
        })
        conn.execute(update_user_sql)

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


@router.put("/user/{user_id}/enable", tags=[TAGS_USER], name='启用用户')
async def enable_user(user_id: int, userinfo: dict = Depends(tool.get_userinfo_from_token)):
    """
    启用用户\n
    :param user_id:\n
    :param userinfo:\n
    :return:
    """
    # 鉴权
    tool.check_operation_permission(userinfo['id'], PERMISSION_USER_ENABLE)

    conn = db_engine.connect()
    trans = conn.begin()

    try:
        # 1.查找用户
        user_sql = t_user.select().where(t_user.c.id == user_id).limit(1).with_for_update()
        conn.execute(user_sql).fetchone()

        # 2.修改用户状态为启用
        update_user_sql = t_user.update().where(and_(
            t_user.c.id == user_id,
            t_user.c.status == TABLE_STATUS_INVALID,
            t_user.c.sub_status == TABLE_SUB_STATUS_INVALID_DISABLE,
        )).values({
            'status': TABLE_STATUS_VALID,
            'sub_status': TABLE_SUB_STATUS_VALID
        })
        conn.execute(update_user_sql)

        # 3.提交事务
        trans.commit()

        return ItemOutOperateSuccess()
    except:
        trans.rollback()
        raise MyException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=ItemOutOperateFailed(code=HTTP_500_INTERNAL_SERVER_ERROR, msg='inter server error'))
    finally:
        conn.close()


@router.delete("/user/{user_id}", tags=[TAGS_USER], name='删除用户')
async def del_user(user_id: int, userinfo: dict = Depends(tool.get_userinfo_from_token)):
    """
    删除用户\n
    :param user_id:\n
    :param userinfo:\n
    :return:
    """
    # 鉴权
    tool.check_operation_permission(userinfo['id'], PERMISSION_USER_DEL)

    conn = db_engine.connect()
    trans = conn.begin()

    try:
        # 1.查找用户
        user_sql = t_user.select().where(t_user.c.id == user_id).limit(1).with_for_update()
        conn.execute(user_sql).fetchone()

        # 2.修改用户状态为无效（软删除）
        update_user_sql = t_user.update().where(and_(
            t_user.c.id == user_id,
            t_user.c.sub_status != TABLE_SUB_STATUS_INVALID_DEL,
        )).values({
            'status': TABLE_STATUS_INVALID,
            'sub_status': TABLE_SUB_STATUS_INVALID_DEL
        })
        conn.execute(update_user_sql)

        # 3.提交事务
        trans.commit()

        return ItemOutOperateSuccess()
    except:
        trans.rollback()
        raise MyException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=ItemOutOperateFailed(code=HTTP_500_INTERNAL_SERVER_ERROR, msg='inter server error'))
    finally:
        conn.close()


@router.post("/user_group", tags=[TAGS_USER], response_model=ItemOutOperateSuccess, name="绑定用户-用户组")
async def bind_user_group(item_in: ItemInBindUserGroup, userinfo: dict = Depends(tool.get_userinfo_from_token)):
    """
    绑定用户-用户组\n
    :param item_in:\n
    :param userinfo:\n
    :return:
    """
    with db_engine.connect() as conn:
        tool.bind_user_group(item_in.user_id, item_in.group_id, userinfo, conn)

    return ItemOutOperateSuccess()


@router.post("/user_role", tags=[TAGS_USER], response_model=ItemOutOperateSuccess, name="绑定用户-角色")
async def bind_user_role(item_in: ItemInBindUserRole, userinfo: dict = Depends(tool.get_userinfo_from_token)):
    """
    绑定用户-角色\n
    :param item_in:\n
    :param userinfo:\n
    :return:
    """
    with db_engine.connect() as conn:
        tool.bind_user_role(item_in.user_id, item_in.role_id, userinfo, conn)

    return ItemOutOperateSuccess()

