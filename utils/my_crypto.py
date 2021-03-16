# -*- coding: utf-8 -*-
"""
加解密
"""
import base64

from Crypto.Cipher import AES


def __add_to_16(s):
    """
    补足字符串长度为16的倍数
    :param s:
    :return:
    """
    while len(s) % 16 != 0:
        s += (16 - len(s) % 16) * chr(16 - len(s) % 16)

    # 返回bytes
    return str.encode(s)


def encrypt(s: str, key: str):
    """
    加密
    :param s: 待加密明文
    :param key: 秘钥
    :return:
    """
    # 初始化加密器，本例采用ECB加密模式
    aes = AES.new(str.encode(key), AES.MODE_ECB)
    return str(base64.encodebytes(aes.encrypt(__add_to_16(s))), encoding='utf8').replace('\n', '')


def decrypt(s: str, key: str) -> str:
    """
    解密
    :param s: 待解密密文
    :param key: 秘钥
    :return:
    """
    # 初始化加密器，本例采用ECB加密模式
    aes = AES.new(str.encode(key), AES.MODE_ECB)

    # 解密
    decrypted_text = aes.decrypt(base64.decodebytes(bytes(s, encoding='utf8'))).decode("utf8")

    # 去除多余补位
    decrypted_text = decrypted_text[:-ord(decrypted_text[-1])]

    return decrypted_text
