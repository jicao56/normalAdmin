# -*- coding: utf-8 -*-

import hashlib
import re


REGEX_EMAIL = r"[\w!#$%&'*+/=?^_`{|}~-]+(?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.)+[\w](?:[\w-]*[\w])?"
REGEX_MOBILE = r"^1[3-9]\d{9}$"
REGEX_MUST_UPPER = r"^[A-Z]+$"


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


