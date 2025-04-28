from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_admin_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="📦 Обновить CSV", callback_data="update_csv")
    builder.button(text="📩 Создать пост-рассылку", callback_data="mailing")
    return builder.as_markup()


def get_cancel_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="❌ Отменить рассылку", callback_data="cancel_mailing")
    return builder.as_markup()
