# -*- coding: utf-8 -*-

import os
import time

# 静态文件目录
file_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'statics')
if not os.path.exists(file_dir):
    os.mkdir(file_dir)


def upload(data, filename: str, mode: str = 'wb'):
    """
    文件上传
    :param data: 待写入的内容
    :param filename: 文件名
    :param mode: 写入模式
    :return:
    """
    ts = int(time.time())
    # 静态文件全路径
    file_full_name = os.path.join(file_dir, filename)

    # 取路径
    dir_name = os.path.dirname(file_full_name)
    if not os.path.exists(dir_name):
        # 路径不存在，新建路径
        os.makedirs(dir_name)

    if os.path.exists(file_full_name):
        # 如果已经存在该名称的文件，将原文件备份
        name, ext = os.path.splitext(file_full_name)
        os.rename(file_full_name, name + '_bak_' + str(ts) + ext)

    if isinstance(data, bytes):
        mode = 'wb'
    elif isinstance(data, str):
        mode = 'w'

    with open(file_full_name, mode) as f:
        f.write(data)
