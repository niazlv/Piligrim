from loader import dp

from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Command

# parse_pos
from handlers.ParsePos import get_pos

# start_command
from handlers.CommandStart import start_command

# db_commands
from handlers.db_commands import insert_db, update_db, select_db, delete_db

# state_machine
from states.statates import StateMachine

# marks
from kyeboards.marks import OptionsMenu, YesOrNoMenu, MainMenu


@dp.message_handler(state=StateMachine.Main)
async def mes_state(message: Message):
    user_id = str(message.from_user.id)

    # ----- start -----
    if message.text == "/start":
        await start_command(user_id, dp)
    # -----------------

    if message.text == "Получить данные📘":
        counter_step = 0
        step = int(await select_db("users", "user_id", "step", user_id))
        while counter_step < step:
            info_id = str(counter_step) + '#' + user_id
            vuz = str(await select_db("info", "info_id", "vuz", info_id))
            inst = str(await select_db("info", "info_id", "inst", info_id))
            nap = str(await select_db("info", "info_id", "nap", info_id))
            form = str(await select_db("info", "info_id", "form", info_id))
            cat = str(await select_db("info", "info_id", "cat", info_id))

            main_id = vuz + '#' + inst + '#' + nap + '#' + form + '#' + cat + '#' + user_id

            vuz_name = str(await select_db("main", "main_id", "vuz_name", main_id))
            inst_name = str(await select_db("main", "main_id", "inst_name", main_id))
            nap_name = str(await select_db("main", "main_id", "nap_name", main_id))
            form_name = str(await select_db("main", "main_id", "form_name", main_id))
            cat_name = str(await select_db("main", "main_id", "cat_name", main_id))
            pos = str(await select_db("main", "main_id", "pos", main_id))
            sogl_pos = str(await select_db("main", "main_id", "sogl_pos", main_id))
            max_sogl = str(await select_db("main", "main_id", "max_sogl", main_id))

            await message.answer(f"🔹ВУЗ: {vuz_name}\n"
                                 f"🔹Институт/Факультет: {inst_name}\n"
                                 f"🔹Направление подготовки/Cпециальность: {nap_name}\n"
                                 f"🔹Форма обучения: {form_name}\n"
                                 f"🔹Категория: {cat_name}\n"
                                 f"🔸Позиция: {pos}\n"
                                 f"🔺Позиция среди Согласий: {sogl_pos}/{max_sogl}")

            counter_step += 1

    if message.text == "Подписка📥":
        await message.answer("📥Вы хотите получать данные о своих направлениях каждые 30 минут?", reply_markup=YesOrNoMenu)
        await StateMachine.Podpis.set()

    if message.text == "Настройки🌀":
        await message.answer("🌀Что вы хотите изменить?", reply_markup=OptionsMenu)
        await StateMachine.OptionsMainButtons.set()


@dp.message_handler(state=StateMachine.Podpis)
async def mes_state(message: Message):
    user_id = str(message.from_user.id)

    # ----- start -----
    if message.text == "/start":
        await start_command(user_id, dp)
    # -----------------

    if message.text == "Да✅":
        await update_db("users", "user_id", "podpis", user_id, 1)
        await message.answer("🔔Подписка включена", reply_markup=MainMenu)
        await StateMachine.Main.set()

    if message.text == "Нет❌":
        await update_db("users", "user_id", "podpis", user_id, 0)
        await message.answer("🔕Подписка выключена", reply_markup=MainMenu)
        await StateMachine.Main.set()
