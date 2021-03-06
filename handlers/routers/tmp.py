# -*- coding: utf-8 -*-
from fastapi import APIRouter

from handlers.const import *

router = APIRouter(tags=[TAGS_BASE])


@router.get('/perms')
async def set_perms():
    return {
        "code": '10000',
        "msg": "",
        "count": 19,
        "data": [
            {
                "id": 1,
                'perms': [{'id': 1, 'title': '查看'}],
                "is_menu": 1,
                "name": "首页",
                # 'label': 'index',
                "child": []
            },
            {
                "id": 1,
                "is_menu": 1,
                "name": "设置",
                'perms': [{'id': 1, 'title': '查看'}],
                "child": [
                    {
                        "id": 2,
                        "is_menu": 1,
                        "name": "用户管理",
                        "perms": [
                            {'code': "USER_CODE1", 'title': '查看'},
                            {'code': "USER_CODE2", 'title': '增加'},
                            {'code': "USER_CODE3", 'title': '更新'},
                            {'code': "USER_CODE4", 'title': '删除'},
                        ],
                    },
                    {
                        "id": 3,
                        "is_menu": 1,
                        "name": "用户组管理",
                        "perms": [
                            {'code': "GROUP_CODE1", 'title': '查看'},
                            {'code': "GROUP_CODE2", 'title': '增加'},
                            {'code': "GROUP_CODE3", 'title': '更新'},
                            {'code': "GROUP_CODE4", 'title': '删除'},
                        ],
                    },
                    {
                        "id": 3,
                        "is_menu": 1,
                        "name": "角色管理",
                        "perms": [
                            {'code': "ROLE_CODE1", 'title': '查看'},
                            {'code': "ROLE_CODE2", 'title': '增加'},
                            {'code': "ROLE_CODE3", 'title': '更新'},
                            {'code': "ROLE_CODE4", 'title': '删除'},
                        ],
                    },
                ]
            },
        ]
    }


@router.get('/perms_menus')
async def perms_menus():
    return {
        "code": '10000',
        "msg": "",
        "count": 19,
        "data": [
            {
                "authorityId": 1,
                "authorityName": "系统管理",
                "orderNumber": 1,
                "menuUrl": None,
                "menuIcon": "layui-icon-set",
                "createTime": "2018/06/29 11:05:41",
                "authority": None,
                "checked": 0,
                "updateTime": "2018/07/13 09:13:42",
                "isMenu": 0,
                "parentId": -1
            },
            {
                "authorityId": 2,
                "authorityName": "用户管理",
                "orderNumber": 2,
                "menuUrl": "system/user",
                "menuIcon": None,
                "createTime": "2018/06/29 11:05:41",
                "authority": None,
                "checked": 0,
                "updateTime": "2018/07/13 09:13:42",
                "isMenu": 0,
                "parentId": 1
            },
            {
                "authorityId": 3,
                "authorityName": "查询用户",
                "orderNumber": 3,
                "menuUrl": "",
                "menuIcon": "",
                "createTime": "2018/07/21 13:54:16",
                "authority": "user:view",
                "checked": 0,
                "updateTime": "2018/07/21 13:54:16",
                "isMenu": 1,
                "parentId": 2
            },
            {
                "authorityId": 4,
                "authorityName": "添加用户",
                "orderNumber": 4,
                "menuUrl": None,
                "menuIcon": None,
                "createTime": "2018/06/29 11:05:41",
                "authority": "user:add",
                "checked": 0,
                "updateTime": "2018/07/13 09:13:42",
                "isMenu": 1,
                "parentId": 2
            },
            {
                "authorityId": 5,
                "authorityName": "修改用户",
                "orderNumber": 5,
                "menuUrl": None,
                "menuIcon": None,
                "createTime": "2018/06/29 11:05:41",
                "authority": "user:edit",
                "checked": 0,
                "updateTime": "2018/07/13 09:13:42",
                "isMenu": 1,
                "parentId": 2
            },
            {
                "authorityId": 6,
                "authorityName": "删除用户",
                "orderNumber": 6,
                "menuUrl": None,
                "menuIcon": None,
                "createTime": "2018/06/29 11:05:41",
                "authority": "user:delete",
                "checked": 0,
                "updateTime": "2018/07/13 09:13:42",
                "isMenu": 1,
                "parentId": 2
            },
            {
                "authorityId": 7,
                "authorityName": "角色管理",
                "orderNumber": 7,
                "menuUrl": "system/role",
                "menuIcon": None,
                "createTime": "2018/06/29 11:05:41",
                "authority": None,
                "checked": 0,
                "updateTime": "2018/07/13 09:13:42",
                "isMenu": 0,
                "parentId": 1
            },
            {
                "authorityId": 8,
                "authorityName": "查询角色",
                "orderNumber": 8,
                "menuUrl": "",
                "menuIcon": "",
                "createTime": "2018/07/21 13:54:59",
                "authority": "role:view",
                "checked": 0,
                "updateTime": "2018/07/21 13:54:58",
                "isMenu": 1,
                "parentId": 7
            },
            {
                "authorityId": 9,
                "authorityName": "添加角色",
                "orderNumber": 9,
                "menuUrl": "",
                "menuIcon": "",
                "createTime": "2018/06/29 11:05:41",
                "authority": "role:add",
                "checked": 0,
                "updateTime": "2018/07/13 09:13:42",
                "isMenu": 1,
                "parentId": 7
            },
            {
                "authorityId": 10,
                "authorityName": "修改角色",
                "orderNumber": 10,
                "menuUrl": "",
                "menuIcon": "",
                "createTime": "2018/06/29 11:05:41",
                "authority": "role:edit",
                "checked": 0,
                "updateTime": "2018/07/13 09:13:42",
                "isMenu": 1,
                "parentId": 7
            },
            {
                "authorityId": 11,
                "authorityName": "删除角色",
                "orderNumber": 11,
                "menuUrl": "",
                "menuIcon": "",
                "createTime": "2018/06/29 11:05:41",
                "authority": "role:delete",
                "checked": 0,
                "updateTime": "2018/07/13 09:13:42",
                "isMenu": 1,
                "parentId": 7
            },
            {
                "authorityId": 12,
                "authorityName": "角色权限管理",
                "orderNumber": 12,
                "menuUrl": "",
                "menuIcon": "",
                "createTime": "2018/06/29 11:05:41",
                "authority": "role:auth",
                "checked": 0,
                "updateTime": "2018/07/13 15:27:18",
                "isMenu": 1,
                "parentId": 7
            },
            {
                "authorityId": 13,
                "authorityName": "权限管理",
                "orderNumber": 13,
                "menuUrl": "system/authorities",
                "menuIcon": None,
                "createTime": "2018/06/29 11:05:41",
                "authority": None,
                "checked": 0,
                "updateTime": "2018/07/13 15:45:13",
                "isMenu": 0,
                "parentId": 1
            },
            {
                "authorityId": 14,
                "authorityName": "查询权限",
                "orderNumber": 14,
                "menuUrl": "",
                "menuIcon": "",
                "createTime": "2018/07/21 13:55:57",
                "authority": "authorities:view",
                "checked": 0,
                "updateTime": "2018/07/21 13:55:56",
                "isMenu": 1,
                "parentId": 13
            },
            {
                "authorityId": 15,
                "authorityName": "添加权限",
                "orderNumber": 15,
                "menuUrl": "",
                "menuIcon": "",
                "createTime": "2018/06/29 11:05:41",
                "authority": "authorities:add",
                "checked": 0,
                "updateTime": "2018/06/29 11:05:41",
                "isMenu": 1,
                "parentId": 13
            },
            {
                "authorityId": 16,
                "authorityName": "修改权限",
                "orderNumber": 16,
                "menuUrl": "",
                "menuIcon": "",
                "createTime": "2018/07/13 09:13:42",
                "authority": "authorities:edit",
                "checked": 0,
                "updateTime": "2018/07/13 09:13:42",
                "isMenu": 1,
                "parentId": 13
            },
            {
                "authorityId": 17,
                "authorityName": "删除权限",
                "orderNumber": 17,
                "menuUrl": "",
                "menuIcon": "",
                "createTime": "2018/06/29 11:05:41",
                "authority": "authorities:delete",
                "checked": 0,
                "updateTime": "2018/06/29 11:05:41",
                "isMenu": 1,
                "parentId": 13
            },
            {
                "authorityId": 18,
                "authorityName": "登录日志",
                "orderNumber": 18,
                "menuUrl": "system/loginRecord",
                "menuIcon": None,
                "createTime": "2018/06/29 11:05:41",
                "authority": None,
                "checked": 0,
                "updateTime": "2018/06/29 11:05:41",
                "isMenu": 0,
                "parentId": 1
            },
            {
                "authorityId": 19,
                "authorityName": "查询登录日志",
                "orderNumber": 19,
                "menuUrl": "",
                "menuIcon": "",
                "createTime": "2018/07/21 13:56:43",
                "authority": "loginRecord:view",
                "checked": 0,
                "updateTime": "2018/07/21 13:56:43",
                "isMenu": 1,
                "parentId": 18
            }
        ]
    }