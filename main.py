# -*- coding: utf-8 -*-

import uvicorn

from settings.site_settings import settings_site_system
from handlers.app import app


if __name__ == '__main__':
    uvicorn.run(app=app, host=settings_site_system.web_host, port=settings_site_system.web_port)

