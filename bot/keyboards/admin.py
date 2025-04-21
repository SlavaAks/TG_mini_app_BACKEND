from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_admin_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="📦 Обновить CSV", callback_data="update_csv")
    return builder.as_markup()
