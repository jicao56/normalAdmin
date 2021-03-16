# -*- coding: utf-8 -*-

import hashlib
import re
import random
from pypinyin import lazy_pinyin
from utils.my_crypto import decrypt
from settings.my_settings import settings_my

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


def get_rand_str(source: str, length: int):
    """
    获取随机字符串
    :param source:
    :param length:
    :return:
    """
    return ''.join(random.sample(source, length))


def sign_decrypt(sign, key=settings_my.crypt_key) -> dict:
    """
    签名解密
    与前端约定好加密方式，前端加密，后端解密
    默认得到的是 param1=1&param2=2&param3=3 的字符串
    再将字符串处理成json
    :param sign:
    :param key:
    :return:
    """
    res = {}
    param_str = decrypt(sign, key)
    kv_list = param_str.split('&')
    for item in kv_list:
        k, v = item.split('=')
        res[k] = v
    return res

