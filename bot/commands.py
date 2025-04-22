from aiogram.types import BotCommand

async def set_bot_commands(bot):
    commands = [
        BotCommand(command="start", description="Начать"),
        BotCommand(command="admin", description="Админ-панель"),
        BotCommand(command="shop", description="Открыть магазин"),
    ]
    await bot.set_my_commands(commands)