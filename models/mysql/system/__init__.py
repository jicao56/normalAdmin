# -*- coding: utf-8 -*-
"""
系统管理数据库
"""

from sqlalchemy import create_engine, MetaData, Table
from settings import settings
from models.mysql import BaseEngine


db_engine = create_engine(
    'mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}?charset={charset}'.format(
        user=settings.mysql.user,
        password=settings.mysql.password,
        host=settings.mysql.host,
        port=settings.mysql.port,
        db_name=settings.mysql.db_name,
        charset=settings.mysql.charset,
    ),
    encoding=settings.mysql.encoding,
    convert_unicode=settings.mysql.convert_unicode,
    echo=settings.mysql.echo,
    pool_size=settings.mysql.pool_size,
    pool_recycle=settings.mysql.pool_recycle,
    pool_pre_ping=settings.mysql.pool_pre_ping,
)

meta = MetaData(db_engine)


# 账号表。系统中，会有各种各样的登录方式，如手机号、邮箱地址、身份证号码和微信登录等。因此该表主要是用来记录每一种登录方式的信息，但不包含密码信息，因为各种登录方式都会使用同一个密码。每一条记录都会关联到唯一的一条用户记录
t_account = Table("t_account", meta, autoload=True, autoload_with=db_engine)

# 页面元素表
t_element = Table("t_element", meta, autoload=True, autoload_with=db_engine)

# 页面元素权限表。用来定义哪个权限对该页面元素可见（一对一）
t_element_permission = Table("t_element_permission", meta, autoload=True, autoload_with=db_engine)

# 文件表
t_file = Table("t_file", meta, autoload=True, autoload_with=db_engine)

# 文件权限表。用来定义文件的权限（一对一）
t_file_permission = Table("t_file_permission", meta, autoload=True, autoload_with=db_engine)

# 用户组表。虽然增加了角色表（role）后，把数据量从 100 亿降低至 10 亿，但 10 倍的数据量依然还是很多。而且大部分的用户（主体用户。如学生系统，学生就是主体）都会分配相同的角色组。用户组和角色组的区别：角色组（role）：解决的是权限的分组，减少了权限的重复分配用户组（user_group）：解决的是用户的分组，减少了用户的重复授权
t_group = Table("t_group", meta, autoload=True, autoload_with=db_engine)

# 用户组角色表。每个系统主体用户，基本都占用了所有用户的 90% 以上（既包含用户，又包含商家的系统，用户和商家同时都是主题用户）。因此，每个用户注册时，基本只需要分配一条所属的用户组，即可完成角色权限的配置。这样处理后，数据量将从 10 亿下降至 1 亿多。同时也减少了用户注册时的需批量写入数量。
t_group_role = Table("t_group_role", meta, autoload=True, autoload_with=db_engine)

# 菜单表
t_menu = Table("t_menu", meta, autoload=True, autoload_with=db_engine)

# 菜单权限表。用来定义每个菜单对应哪个权限（一对一）
t_menu_permission = Table("t_menu_permission", meta, autoload=True, autoload_with=db_engine)

# 功能操作表
t_operation = Table("t_operation", meta, autoload=True, autoload_with=db_engine)

# 功能模块操作权限表。用来定义哪个权限对该模块可操作（一对一）
t_operation_permission = Table("t_operation_permission", meta, autoload=True, autoload_with=db_engine)

# 权限表。不同的用户能操作和查看不同的功能（如页面、菜单和按钮等）。因此需要定义一张表来存储权限相关的信息。包括权限之前还有父子关系，分配了父级后，应该拥有所有的子级权限。同时权限的信息也会分配至前端页面来控制，因此需要提供一个唯一标识（code）
t_permission = Table("t_permission", meta, autoload=True, autoload_with=db_engine)

# 角色
t_role = Table("t_role", meta, autoload=True, autoload_with=db_engine)

# 角色权限表。用来定义每个角色组中有哪些权限
t_role_permission = Table("t_role_permission", meta, autoload=True, autoload_with=db_engine)

# 用户表。主要是用来记录用户的基本信息和密码信息。其中禁用状态（state）主要是在后台管理控制非法用户使用系统；密码加盐（salt）则是用于给每个用户的登录密码加一把唯一的锁，即使公司加密公钥泄露后，也不会导致全部用户的密码泄露
t_user = Table("t_user", meta, autoload=True, autoload_with=db_engine)

# 用户组成员。最终用户拥有的所有权限 = 用户个人拥有的权限（t_role_user）+该用户所在用户组拥有的权限（t_role_user_group）
t_user_group = Table("t_user_group", meta, autoload=True, autoload_with=db_engine)

# 用户角色
t_user_role = Table("t_user_role", meta, autoload=True, autoload_with=db_engine)


class SystemEngine(BaseEngine):
    """
    系统管理数据库引擎
    """

    # 数据库引擎
    db_engine = db_engine
    meta = meta

    # 表，sqlalchemy.Table类
    table: Table = None
