# -*- coding: utf-8 -*-

import os
import logging
from logging import handlers
from settings import settings_site_system, settings_my, cur_env, ENV_DEV, ENV_TEST, ENV_UAT, ENV_PROD


# 日志目录
log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')
if not os.path.exists(log_dir):
    os.mkdir(log_dir)

# 日志全路径
log_full_name = os.path.join(log_dir, settings_my.log_name)


# 日志级别
if cur_env == ENV_DEV:
    log_level = logging.DEBUG
elif cur_env == ENV_TEST:
    log_level = logging.DEBUG
elif cur_env == ENV_UAT:
    log_level = logging.ERROR
elif cur_env == ENV_PROD:
    log_level = logging.ERROR
else:
    log_level = logging.DEBUG


class MyLogger(object):
    handler = handlers.RotatingFileHandler(log_full_name, maxBytes=settings_my.log_max_bytes, backupCount=settings_my.log_backup_count)
    handler.setFormatter(logging.Formatter(settings_my.log_format))
    handler.setLevel(log_level)

    _logger = logging.getLogger(settings_my.log_name)
    _logger.addHandler(handler)

    @classmethod
    def info(cls, msg):
        cls._logger.info(msg)

    @classmethod
    def debug(cls, msg):
        cls._logger.debug(msg)

    @classmethod
    def warn(cls, msg):
        cls._logger.warning(msg)

    @classmethod
    def error(cls, msg):
        cls._logger.error(msg)


# 定义一个logger的变量，方便外部调用
logger = MyLogger

