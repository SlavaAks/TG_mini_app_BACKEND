from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from api.common import notify_update
from bot.keyboards.admin import get_admin_keyboard
from config_reader import config
from services.exel_parser import download_csv_file

router = Router(name='admin')

MANAGER_ID = int(config.MANAGER_ID.get_secret_value())


@router.message(F.text == "/admin")
async def admin_menu(message: Message):
    if message.from_user.id == MANAGER_ID:
        await message.answer("🔧 Админ-меню:", reply_markup=get_admin_keyboard())
    else:
        await message.answer("🚫 У тебя нет доступа.")


@router.callback_query(F.data == "update_csv")
async def update_csv(callback: CallbackQuery):
    try:
        await download_csv_file()
        await notify_update()
        await callback.answer("✅ CSV обновлён!")
        await callback.message.edit_text("✅ CSV обновлён!", reply_markup=get_admin_keyboard())
    except Exception as e:
        await callback.answer(f"❌ Ошибка: {str(e)}", show_alert=True)

