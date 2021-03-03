# -*- coding: utf-8 -*-

import redis
from settings import settings


class SystemRedis(object):
    def __init__(self, host=settings.redis_host, port=settings.redis_port, password=settings.redis_password, max_conn=settings.redis_max_conn):
        self.__host = host
        self.__port = port
        self.__password = password
        self.__max_conn = max_conn
        self.__pool = redis.ConnectionPool(host=self.__host, port=self.__port, max_connections=self.__max_conn, decode_responses=True)

        self.__conn = redis.Redis(connection_pool=self.__pool)

    def __call__(self, *args, **kwargs):
        return self.__conn


redis_conn = SystemRedis()()
