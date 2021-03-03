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
    web_port = 8000

    # 接口启动进程数
    web_process_num = 1

    # 第几页
    web_page = 1

    # 每页显示多少条数据
    web_page_size = 10

    # 验证码源
    web_captcha_source = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

    # 验证码长度
    web_captcha_length = 4

    # 用户默认密码
    web_user_default_password = '123456'

    # mysql数据库登录用户名
    mysql_user = 'root'

    # mysql数据库登录密码
    mysql_password = 'root'

    # mysql数据库地址
    mysql_host = '127.0.0.1'

    # mysql数据库端口
    mysql_port = 3306

    # mysql数据库的数据库名
    mysql_db_name = 'normal_admin'

    # mysql数据库的编码
    mysql_charset = 'utf8'
    mysql_encoding = 'utf-8'
    mysql_convert_unicode = True
    mysql_echo = True
    mysql_pool_size = 100
    mysql_pool_recycle = 360
    mysql_pool_pre_ping = True

    # redis服务地址
    redis_host = '127.0.0.1'

    # redis服务端口
    redis_port = 6379

    # redis服务登录密码
    redis_password = None

    # redis服务的key过期时间
    redis_expire = 60 * 60

    # redis服务的最大连接数
    redis_max_conn = 1024

    # 验证码有效期
    redis_captcha_expire_time = 60 * 60

    # 验证码缓存key
    redis_captcha_key = "captcha_{}"

    # token有效期
    redis_token_expire_time = 60 * 60

    # token缓存key
    redis_token_key = 'token_{}'

    # 日志名
    log_name = 'main.log'

    # 日志文件的最大字节数
    log_max_bytes = 1024 * 1024 * 100

    # 日志文件最多备份数量
    log_backup_count = 10

    # 日志打印格式
    log_format = '[%(levelname)s][%(process)d][%(asctime)s][%(name)s][%(filename)s][%(lineno)d]: %(message)s'
