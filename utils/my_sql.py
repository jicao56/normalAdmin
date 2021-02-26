# -*- coding: utf-8 -*-

from sqlalchemy import Table, create_engine, MetaData
from settings import settings


class Mysql(object):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self):
        self.db_engine = create_engine(
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

        self.meta = MetaData(self.db_engine)
