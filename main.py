from typing import AsyncGenerator

import uvicorn
from aiogram import Bot
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import config_reader
from bot.handlers import setup_routers as setup_bot_routers
from api import setup_routers as setup_api_routers

from config_reader import config, init_bot


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    app.include_router(setup_api_routers())

    return app


async def lifespan(app: FastAPI) -> AsyncGenerator:
    bot, dp = init_bot()
    app.state.bot = bot
    app.state.dp = dp

    dp.include_router(setup_bot_routers())
    await bot.set_webhook(
        url=f"{config.WEBHOOK_URL}/webhook",
        allowed_updates=dp.resolve_used_update_types(),
        drop_pending_updates=True,
    )

    yield

    await bot.session.close()


app = create_app()


@app.get("/")
def root():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host=config.APP_HOST, port=config.APP_PORT)
