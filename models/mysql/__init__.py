# -*- coding: utf-8 -*-

# 基础引擎类
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
