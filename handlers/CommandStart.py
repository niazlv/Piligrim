from aiogram import Dispatcher
from aiogram.types import Message, ReplyKeyboardRemove

# db_commands
from handlers.db_commands import insert_db, update_db, select_db, delete_db

# state_machine
from states.statates import StateMachine


async def start_command(user_id, dp: Dispatcher):
    check_info = False
    try:
        await insert_db("users", "user_id", user_id)
    except:
        check_info = True
        pass

    # Очистка info(на всякий случай)
    if check_info:
        for counter in range(0,5):
            info_id = str(counter) + '#' + user_id
            try:
                await delete_db("info", "info_id", info_id)
            except:
                pass

    await update_db("users", "user_id", "step", user_id, 0)

    await dp.bot.send_message(user_id, "Добро пожаловать в КФУ🌟", reply_markup=ReplyKeyboardRemove())
    await dp.bot.send_message(user_id, "🔖Пример СНИЛС: 123-456-789-10\n"
                                       "🔹Введите ID Абитуриента/СНИЛС:")
    await StateMachine.Snls.set()
