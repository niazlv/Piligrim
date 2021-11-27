import asyncio

from aiogram import executor
from loader import dp
import handlers

from useless.createdb import create_db

from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):

    await asyncio.sleep(10)
    await create_db()

    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
