from aiogram import Router
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import CommandStart
from bot.keyboards import main_markup
from config_reader import config

from db import User

router = Router(name="common")

MANAGER_ID = int(config.MANAGER_ID.get_secret_value())


@router.message(CommandStart())
async def start(message: Message):
    is_admin = message.from_user.id == MANAGER_ID

    buttons = [[KeyboardButton(text="🛍 Web App")]]

    if is_admin:
        buttons.append([KeyboardButton(text="🛠 Admin")])

    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await message.answer("Приятных покупок!", reply_markup=keyboard)
    # await message.answer("Open Mini App!", reply_markup=main_markup)
