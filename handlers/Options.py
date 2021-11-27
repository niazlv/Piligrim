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
from kyeboards.marks import NapOptionsMenu, MainMenu


@dp.message_handler(state=StateMachine.OptionsMainButtons)
async def mes_state(message: Message):
    user_id = str(message.from_user.id)

    # ----- start -----
    if message.text == "/start":
        await start_command(user_id, dp)
    # -----------------

    # ----- back ------
    if message.text == "Отменить◀️":
        await message.answer("🔹Переходим в главное меню", reply_markup=MainMenu)
        await StateMachine.Main.set()
    # -----------------

    if message.text == "ID Абитуриента/СНИЛС🔹":
        snls = await select_db("users", "user_id", "snls", user_id)
        await message.answer(f"📘Ваш текущий ID Абитуриента/СНИЛС: {snls}", reply_markup=ReplyKeyboardRemove())

        await message.answer("🔖Пример СНИЛС: 123-456-789-10\n"
                             "🔹Введите новый ID Абитуриента/СНИЛС:")
        await StateMachine.SnlsOption.set()

    if message.text == "Направления📘":
        await message.answer("📖Список текущих направлений:", reply_markup=NapOptionsMenu)

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

            await message.answer(f"{counter_step+1}♦️Направление"
                                 f"🔹ВУЗ: {vuz_name}\n"
                                 f"🔹Институт/Факультет: {inst_name}\n"
                                 f"🔹Направление подготовки/Cпециальность: {nap_name}\n"
                                 f"🔹Форма обучения: {form_name}\n"
                                 f"🔹Категория: {cat_name}")

            counter_step += 1

        await message.answer("📘Что вы хотите сделать?")
        await StateMachine.WaitNapCommand.set()


@dp.message_handler(state=StateMachine.WaitNapCommand)
async def mes_state(message: Message):
    user_id = str(message.from_user.id)

    # ----- start -----
    if message.text == "/start":
        await start_command(user_id, dp)
    # -----------------

    # ----- back ------
    if message.text == "Отменить◀️":
        await message.answer("🔹Переходим в главное меню", reply_markup=MainMenu)
        await StateMachine.Main.set()
    # -----------------

    if message.text == "Добавить✅":
        step = int(await select_db("users", "user_id", "step", user_id))
        if step == 5:
            await message.answer("❗️Вы выбрали максимум направлений")
        else:
            await message.answer("⚡️Отправьте номер\n"
                                 "🔹Выберите ВУЗ:", reply_markup=ReplyKeyboardRemove())

            await message.answer("📖Список:\n"
                                 "1. КФУ\n"
                                 "2. Наб.Челны\n"
                                 "3. Елабуга")

            await update_db("users", "user_id", "check_max", user_id, 3)

            await StateMachine.VuzInfo.set()

    if message.text == "Удалить❌":
        await message.answer("⚡️Отправьте номер\n"
                             "🔹Выберите Направление, которое хотите удалить:", reply_markup=ReplyKeyboardRemove())
        await StateMachine.DeleteNapNum.set()


@dp.message_handler(state=StateMachine.DeleteNapNum)
async def mes_state(message: Message):
    user_id = str(message.from_user.id)

    # ----- start -----
    if message.text == "/start":
        await start_command(user_id, dp)
    # -----------------

    else:
        num = message.text
        check_num = True
        try:
            num = int(num)
        except:
            check_num = False

        if check_num:
            check_table = True
            step = int(await select_db("users", "user_id", "step", user_id))
            if num < 1 or num > step:
                check_table = False

            if check_table:
                info_id = str(num-1) + '#' + user_id
                await delete_db("info", "info_id", info_id)

                # Сдвиг
                сounter_step = 0
                delete_id = 0
                while сounter_step < step:
                    info_id = str(сounter_step) + '#' + user_id
                    try:
                        vuz = int(await select_db("info", "info_id", "vuz", info_id))
                    except:
                        сounter_step += 1
                        continue

                    new_info_id = str(delete_id) + '#' + user_id
                    await update_db("info", "info_id", "info_id", info_id, new_info_id)
                    delete_id += 1

                    сounter_step += 1

                await update_db("users", "user_id", "step", user_id, delete_id)

                await message.answer("⚡️Направление успешно удалено", reply_markup=MainMenu)

                await StateMachine.Main.set()
            else:
                await message.answer("❗️Неверный формат")
        else:
            await message.answer("❗️Неверный формат")


@dp.message_handler(state=StateMachine.SnlsOption)
async def mes_state(message: Message):
    user_id = str(message.from_user.id)

    # ----- start -----
    if message.text == "/start":
        await start_command(user_id, dp)
    # -----------------

    else:
        snls = message.text
        await update_db("users", "user_id", "snls", user_id, snls)

        counter_step = 0
        step = int(await select_db("users", "user_id", "step", user_id))
        while counter_step < step:
            info_id = str(counter_step) + '#' + user_id
            vuz = int(await select_db("info", "info_id", "vuz", info_id))
            inst = int(await select_db("info", "info_id", "inst", info_id))
            nap = int(await select_db("info", "info_id", "nap", info_id))
            form = int(await select_db("info", "info_id", "form", info_id))
            cat = int(await select_db("info", "info_id", "cat", info_id))

            main_id = str(vuz) + '#' + str(inst) + '#' + str(nap) + '#' + str(form) + '#' + str(cat) + '#' + user_id

            await get_pos(vuz, inst, nap, form, cat, snls, main_id, info_id)

            counter_step += 1

        # Сдвиг
        сounter_step = 0
        delete_id = 0
        while сounter_step < step:
            info_id = str(сounter_step) + '#' + user_id
            try:
                vuz = int(await select_db("info", "info_id", "vuz", info_id))
            except:
                сounter_step += 1
                continue

            new_info_id = str(delete_id) + '#' + user_id
            await update_db("info", "info_id", "info_id", info_id, new_info_id)
            delete_id += 1

            сounter_step += 1

        await update_db("users", "user_id", "step", user_id, delete_id)

        if delete_id == 0:
            await message.answer("❗️Вас нет в списках ни одного из направлений, попробуйте ввести еще раз")
            await start_command(user_id, dp)
        else:
            await message.answer("🌀", reply_markup=MainMenu)
            await StateMachine.Main.set()
