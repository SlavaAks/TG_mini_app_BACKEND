from pathlib import Path

from aiogram import Router
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import CommandStart
from bot.keyboards import main_markup
from config_reader import config

from db import User

router = Router(name="common")

MANAGER_ID = config.MANAGER_ID

USER_FILE_PATH = Path(__file__).resolve().parent / 'users.txt'
def get_users_list():
    try:
        with open(USER_FILE_PATH, 'r+') as f:
            data = f.read().splitlines()
            return data
    except:
        return []

def new_user(uid):
    if str(uid) not in get_users_list():
        with open(USER_FILE_PATH, 'a+') as f:
            f.write(str(uid) + '\n')

@router.message(CommandStart())
async def start(message: Message):
    user_id = message.from_user.id
    is_admin = message.from_user.id in MANAGER_ID
    new_user(user_id)
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
