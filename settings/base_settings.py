# -*- coding: utf-8 -*-

ENV_LOCAL = 'local'
ENV_DEV = 'dev'
ENV_TEST = 'test'
ENV_UAT = 'uat'
ENV_PROD = 'prod'


class BaseSettings(object):
    env = ENV_LOCAL

    web_debug = True

    # 接口ip
    web_host = '0.0.0.0'

    # 接口端口
    web_port = 9000

    # 接口启动进程数
    web_process_num = 1

    #
    # # redis服务的key过期时间
    # redis_expire = 60 * 60
    #
    # # redis服务的最大连接数
    # redis_max_conn = 1024
    #
    # # 验证码有效期
    # captcha_expire_time = 60 * 60
    #
    # # 验证码缓存key
    # captcha_key_format = "captcha_{}"
    #
    # # token有效期
    # token_expire_time = 60 * 60
    #
    # # token缓存key
    # token_key_format = 'token_{}'
    #
    # # 日志名
    # log_name = 'main.log'
    #
    # # 日志文件的最大字节数
    # log_max_bytes = 1024 * 1024 * 100
    #
    # # 日志文件最多备份数量
    # log_backup_count = 10
    #
    # # 日志打印格式
    # log_format = '[%(levelname)s][%(process)d][%(asctime)s][%(name)s][%(filename)s][%(lineno)d]: %(message)s'
