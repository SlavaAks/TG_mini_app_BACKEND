from pathlib import Path
from typing import List

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from aiogram import Bot, Dispatcher

ROOT_DIR = Path(__file__).resolve().parent


class Config(BaseSettings):
    BOT_TOKEN: SecretStr
    SPREADSHEET_ID: SecretStr
    MANAGER_ID: List[int]
    CHANEL_ID: SecretStr

    WEBHOOK_URL: str = "https://lawkashop.space/api"
    WEBAPP_URL: str = "https://lawkashop.space"

    APP_HOST: str = "localhost"
    APP_PORT: int = 8080

    model_config = SettingsConfigDict(
        env_file=ROOT_DIR / ".env",
        env_file_encoding="utf-8"
    )


def init_bot():
    bot = Bot(token=config.BOT_TOKEN.get_secret_value())
    dp = Dispatcher()
    return bot, dp

config = Config()
