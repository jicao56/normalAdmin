# -*- coding: utf-8 -*-

from models.mysql.system import t_account, SystemEngine

# 账号类别，1-手机号；2-邮箱；3-自定义账号
CATEGORY_PHONE = 1
CATEGORY_EMAIL = 2
CATEGORY_CUSTOM = 3
CATEGORY = {
    CATEGORY_PHONE: '手机号',
    CATEGORY_EMAIL: '邮箱',
    CATEGORY_CUSTOM: '自定义',
}


class TableAccount(SystemEngine):
    table = t_account
