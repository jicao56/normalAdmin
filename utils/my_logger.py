# -*- coding: utf-8 -*-

import os
import logging
from logging import handlers
from settings import settings


log_settings = settings.log


log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')
if not os.path.exists(log_dir):
    os.mkdir(log_dir)
log_full_name = os.path.join(log_dir, log_settings.name)


class MyLogger(object):
    def __init__(
            self, 
            logger_name=log_settings.name, 
            max_bytes=log_settings.max_bytes, 
            backup_count=log_settings.backup_count,
            format=log_settings.format
    ):
        self.__log_name = logger_name
        self.__log_full_name = os.path.join(log_dir, logger_name)
        self.__max_bytes = max_bytes
        self.__backup_count = backup_count
        self.__formatter = logging.Formatter(format)

        self.__handler = handlers.RotatingFileHandler(log_full_name, maxBytes=self.__max_bytes, backupCount=self.__backup_count)
        self.__handler.setFormatter(self.__formatter)
        self.__handler.setLevel(MyLogger.get_level())

        self.__logger = logging.getLogger(self.__log_name)
        self.__logger.addHandler(self.__handler)

    @classmethod
    def get_level(cls):
        """
        获取日志输出级别
        :param env:
        :return:
        """
        if settings.env == 'dev':
            return logging.DEBUG
        elif settings.env == 'test':
            return logging.DEBUG
        elif settings.env == 'uat':
            return logging.ERROR
        elif settings.env == 'prod':
            return logging.ERROR
        else:
            return logging.DEBUG

    def info(self, msg):
        self.__logger.info(msg)

    def debug(self, msg):
        self.__logger.debug(msg)

    def warn(self, msg):
        self.__logger.warning(msg)

    def error(self, msg):
        self.__logger.error(msg)


logger = MyLogger()
__all__ = ['logger']

