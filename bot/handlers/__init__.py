from aiogram import Router

from . import common,admin

def setup_routers() -> Router:
    router = Router()

    router.include_router(common.router)
    router.include_router(admin.router)
    return router
