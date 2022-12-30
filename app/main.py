import logging

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dataclasses import asdict

from app.core.events.event import startup_app_event, shutdown_app_event
from app.core.settings.setting import get_env, AppSettings
from app.routes import index, fortune, auth
from app.common import config
from app.database import conn


def create_app():
    env_setting = get_env()
    c = config.conf()
    app = FastAPI()
    conf_dict = asdict(c)
    conn.db.init_app(app, env_setting, **conf_dict)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(index.router)
    app.include_router(auth.router, tags=['oauth'], prefix='/oauth')
    app.include_router(fortune.router, tags=['fortune'], prefix='/fortune')

    @app.on_event("startup")
    async def startup_event():
        return startup_app_event(env_setting)

    @app.on_event("shutdown")
    async def shutdown_event():
        return shutdown_app_event()

    return app


main_app = create_app()

if __name__ == '__main__':
    uvicorn.run('main:main_app', host='localhost', port=8000, reload=True)
