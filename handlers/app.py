# -*- coding: utf-8 -*-

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from handlers.routers import base, config, login, logout, menu, user, group, role, permission, ugrp, config_developer


app = FastAPI()

# 静态文件解析
app.mount('/statics', StaticFiles(directory='statics'), name='static')

# 跨域处理
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# 业务处理
app.include_router(base.router)
app.include_router(config.router)
app.include_router(config_developer.router)
app.include_router(login.router)
app.include_router(logout.router)
app.include_router(menu.router)
app.include_router(user.router)
app.include_router(group.router)
app.include_router(role.router)
app.include_router(permission.router)
app.include_router(ugrp.router)

