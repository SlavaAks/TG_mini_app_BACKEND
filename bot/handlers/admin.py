from aiogram import Router, F
from aiogram.filters import Command, or_f
from aiogram.types import Message, CallbackQuery

from api.common import notify_all, set_last_updated
from bot.keyboards import main_markup
from bot.keyboards.admin import get_admin_keyboard
from config_reader import config
from services.exel_parser import download_csv_file

router = Router(name='admin')

MANAGER_ID = config.MANAGER_ID

@router.message(or_f(Command("shop"), F.text == "🛍 Web App"))
async def web_app_handler(message: Message):
    await message.answer("Открыть Web App", reply_markup=main_markup)


@router.message(or_f(Command("admin"), F.text == "🛠 Admin"))
async def admin_handler(message: Message):
    print(MANAGER_ID)
    if message.from_user.id in MANAGER_ID:
        await message.answer("🔧 Админ-меню:", reply_markup=get_admin_keyboard())
    else:
        await message.answer("🚫 У тебя нет доступа.")


@router.callback_query(F.data == "update_csv")
async def update_csv(callback: CallbackQuery):
    try:
        await download_csv_file()
        await notify_all('update')
        await set_last_updated()
        await callback.answer("✅ CSV обновлён!")
        await callback.message.edit_text("✅ CSV обновлён!", reply_markup=get_admin_keyboard())
    except Exception as e:
        await callback.answer(f"❌ Ошибка: {str(e)}", show_alert=True)
