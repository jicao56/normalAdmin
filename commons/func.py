# -*- coding: utf-8 -*-

import hashlib
import re
from pypinyin import lazy_pinyin

# 正则：邮箱
REGEX_EMAIL = r"^(\s*|[\w!#$%&'*+/=?^_`{|}~-]+(?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.)+[\w](?:[\w-]*[\w])?)$"

# 正则：中国手机号
REGEX_MOBILE = r"^(\s*|1[3-9]\d{9})$"

# 正则：大写英文字母或者数字或者下划线
REGEX_UPPER_OR_UNDERLINE = r"^[A-Z_0-9]+$"


def md5(s: str, salt: str = ''):
    """
    md5加密
    :param s:
    :param salt:
    :return:
    """
    s = str(s)
    if salt:
        s = s + str(salt)
    m = hashlib.md5(s.encode())
    return m.hexdigest()


def is_mobile(s):
    """
    验证是否是中国手机号
    :param s:
    :return:
    """
    res = re.match(r"^1[3-9]\d{9}$", s)
    if res:
        return True
    else:
        return False


def is_email(s):
    """
    验证是不是邮箱
    :param s:
    :return:
    """
    res = re.match(REGEX_EMAIL, s)
    if res:
        return True
    else:
        return False


def chinese_to_upper_english(s):
    """
    汉子转大写英文
    :param s:
    :return:
    """
    return '_'.join(lazy_pinyin(s)).upper()
