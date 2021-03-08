# -*- coding: utf-8 -*-

from settings.mysql_settings import settings_mysql_system
from settings.redis_settings import settings_redis_system
from settings.my_settings import settings_my
from settings.site_settings import settings_site_system

ENV_LOCAL = 'local'
ENV_DEV = 'dev'
ENV_TEST = 'test'
ENV_UAT = 'uat'
ENV_PROD = 'prod'


# 当前环境
cur_env = ENV_LOCAL
