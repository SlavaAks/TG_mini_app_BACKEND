import asyncio

from aiogram import Router, F, Bot, types
from aiogram.filters import Command, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

from api.common import notify_all, set_last_updated
from bot.handlers.common import get_users_list
from bot.keyboards import main_markup
from bot.keyboards.admin import get_admin_keyboard, get_cancel_keyboard
from config_reader import config
from services.exel_parser import download_csv_file

router = Router(name='admin')

MANAGER_ID = config.MANAGER_ID


@router.message(or_f(Command("shop"), F.text == "🛍 Web App"))
async def web_app_handler(message: Message):
    await message.answer("Открыть Web App", reply_markup=main_markup)


@router.message(or_f(Command("admin"), F.text == "🛠 Admin"))
async def admin_handler(message: Message):
    if message.from_user.id in MANAGER_ID:
        await message.answer("🔧 Админ-меню:", reply_markup=get_admin_keyboard())
    else:
        await message.answer("🚫 У тебя нет доступа.")


@router.callback_query(F.data == "update_csv")
async def update_csv(callback: CallbackQuery):
    try:
        await download_csv_file()
        await notify_all('update')
        set_last_updated()
        await callback.answer("✅ CSV обновлён!")
        await callback.message.edit_text("✅ CSV обновлён!", reply_markup=get_admin_keyboard())
    except Exception as e:
        await callback.answer(f"❌ Ошибка: {str(e)}", show_alert=True)


class MailingStates(StatesGroup):
    waiting_for_message = State()


@router.callback_query(F.data == "mailing")
async def initiate_mailing(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Пожалуйста, введите сообщение для рассылки:", reply_markup=get_cancel_keyboard())
    await state.set_state(MailingStates.waiting_for_message)
    await callback.answer()


@router.callback_query(F.data == "cancel_mailing")
async def cancel_mailing(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("Рассылка отменена.")
    await callback.answer()


@router.message(MailingStates.waiting_for_message)
async def send_mailing(message: Message, state: FSMContext, bot: Bot):
    user_ids = get_users_list()
    success_count = 0
    failure_count = 0

    for user_id in user_ids:
        try:
            photo = message.photo
            if photo:
                photo = photo[-1]
                file_id = photo.file_id
                caption = message.caption if message.caption else " "
                await bot.send_photo(chat_id=user_id, photo=file_id, caption=caption)
            if message.text:
                await bot.send_message(chat_id=user_id, text=message.text)
            success_count += 1
            await asyncio.sleep(0.05)  # Пауза для соблюдения лимитов Telegram
        except Exception as e:
            failure_count += 1
            # Здесь можно добавить логирование ошибки

    await message.answer(f"Рассылка завершена.\nУспешно: {success_count}\nОшибки: {failure_count}")
    await state.clear()
