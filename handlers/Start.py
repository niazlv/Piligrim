from loader import dp

from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Command

# start_command
from handlers.CommandStart import start_command

# db_commands
from handlers.db_commands import insert_db, update_db, select_db, delete_db

# state_machine
from states.statates import StateMachine

# ping
from utils.pinging import ping
from loader import dp


@dp.message_handler(Command("start"))
async def command_start(message: Message):
    user_id = str(message.from_user.id)

    await start_command(user_id, dp)

    user_num = int(await select_db("users", "user_id", "user_num", user_id))
    if user_num == 1:
        await ping(dp)


@dp.message_handler(state=StateMachine.Snls)
async def mes_state(message: Message):
    user_id = str(message.from_user.id)

    # ----- start -----
    if message.text == "/start":
        await start_command(user_id, dp)
    # -----------------

    else:
        snls = message.text
        await update_db("users", "user_id", "snls", user_id, snls)

        await message.answer("⚡️Отправьте номер\n"
                             "🔹Выберите ВУЗ:")

        await message.answer("📖Список:\n"
                             "1. КФУ\n"
                             "2. Наб.Челны\n"
                             "3. Елабуга")

        await update_db("users", "user_id", "check_max", user_id, 3)

        await StateMachine.VuzInfo.set()
