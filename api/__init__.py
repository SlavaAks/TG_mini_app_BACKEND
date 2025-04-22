from fastapi import APIRouter

from . import common, products, order


def setup_routers() -> APIRouter:
    router = APIRouter()

    router.include_router(common.router)
    router.include_router(products.router)
    router.include_router(order.router)
    return router
