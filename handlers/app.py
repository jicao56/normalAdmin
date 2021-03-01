# -*- coding: utf-8 -*-

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from handlers.routers import login, logout, menu, user, group, role


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(login.router)
app.include_router(logout.router)
app.include_router(menu.router)
app.include_router(user.router)
app.include_router(group.router)
app.include_router(role.router)
