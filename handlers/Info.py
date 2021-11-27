from loader import dp

from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Command

# parse_reg
from handlers.ParseReg import get_inst_text, get_inst_value, get_nap_text, get_nap_value, get_form_text, get_form_value, get_cat_text, get_cat_value

# parse_pos
from handlers.ParsePos import get_pos

# start_command
from handlers.CommandStart import start_command

# db_commands
from handlers.db_commands import insert_db, update_db, select_db, delete_db

# state_machine
from states.statates import StateMachine

# marks
from kyeboards.marks import YesOrNoMenu, MainMenu


@dp.message_handler(state=StateMachine.VuzInfo)
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
            check_max = int(await select_db("users", "user_id", "check_max", user_id))
            if num < 1 or num > check_max:
                check_table = False

            if check_table:
                step = str(await select_db("users", "user_id", "step", user_id))
                info_id = step + '#' + user_id

                try:
                    await insert_db("info", "info_id", info_id)
                except:
                    pass

                if num == 1:
                    vuz = 0
                    await update_db("info", "info_id", "vuz", info_id, vuz)
                if num == 2:
                    vuz = 1
                    await update_db("info", "info_id", "vuz", info_id, vuz)
                if num == 3:
                    vuz = 5
                    await update_db("info", "info_id", "vuz", info_id, vuz)

                await message.answer("⚡️Отправьте номер\n"
                                     "🔹Выберите Институт/Факультет:")

                await get_inst_text(vuz, user_id, dp)

                await StateMachine.InstInfo.set()
            else:
                await message.answer("❗️Неверный формат")
        else:
            await message.answer("❗️Неверный формат")


@dp.message_handler(state=StateMachine.InstInfo)
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
            check_max = int(await select_db("users", "user_id", "check_max", user_id))
            if num < 1 or num > check_max:
                check_table = False

            if check_table:
                step = str(await select_db("users", "user_id", "step", user_id))
                info_id = step + '#' + user_id
                vuz = await select_db("info", "info_id", "vuz", info_id)

                await get_inst_value(vuz, num, user_id)

                await message.answer("⚡️Отправьте номер\n"
                                     "🔹Выберите Направление подготовки/Cпециальность:")

                inst = await select_db("info", "info_id", "inst", info_id)
                await get_nap_text(vuz, inst, user_id, dp)

                await StateMachine.NapInfo.set()
            else:
                await message.answer("❗️Неверный формат")
        else:
            await message.answer("❗️Неверный формат")


@dp.message_handler(state=StateMachine.NapInfo)
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
            check_max = int(await select_db("users", "user_id", "check_max", user_id))
            if num < 1 or num > check_max:
                check_table = False

            if check_table:
                step = str(await select_db("users", "user_id", "step", user_id))
                info_id = step + '#' + user_id
                vuz = await select_db("info", "info_id", "vuz", info_id)
                inst = await select_db("info", "info_id", "inst", info_id)

                await get_nap_value(vuz, inst, num, user_id)

                await message.answer("⚡️Отправьте номер\n"
                                     "🔹Выберите Форму обучения:")

                nap = await select_db("info", "info_id", "nap", info_id)
                await get_form_text(vuz, inst, nap, user_id, dp)

                await StateMachine.FormInfo.set()
            else:
                await message.answer("❗️Неверный формат")
        else:
            await message.answer("❗️Неверный формат")


@dp.message_handler(state=StateMachine.FormInfo)
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
            check_max = int(await select_db("users", "user_id", "check_max", user_id))
            if num < 1 or num > check_max:
                check_table = False

            if check_table:
                step = str(await select_db("users", "user_id", "step", user_id))
                info_id = step + '#' + user_id
                vuz = await select_db("info", "info_id", "vuz", info_id)
                inst = await select_db("info", "info_id", "inst", info_id)
                nap = await select_db("info", "info_id", "nap", info_id)

                await get_form_value(vuz, inst, nap, num, user_id)

                await message.answer("⚡️Отправьте номер\n"
                                     "🔹Выберите Категорию:")

                form = await select_db("info", "info_id", "form", info_id)
                await get_cat_text(vuz, inst, nap, form, user_id, dp)

                await StateMachine.CatInfo.set()
            else:
                await message.answer("❗️Неверный формат")
        else:
            await message.answer("❗️Неверный формат")


@dp.message_handler(state=StateMachine.CatInfo)
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
            check_max = int(await select_db("users", "user_id", "check_max", user_id))
            if num < 1 or num > check_max:
                check_table = False

            if check_table:
                step = str(await select_db("users", "user_id", "step", user_id))
                info_id = step + '#' + user_id
                vuz = await select_db("info", "info_id", "vuz", info_id)
                inst = await select_db("info", "info_id", "inst", info_id)
                nap = await select_db("info", "info_id", "nap", info_id)
                form = await select_db("info", "info_id", "form", info_id)

                await get_cat_value(vuz, inst, nap, form, num, user_id)

                step = int(step) + 1
                await update_db("users", "user_id", "step", user_id, step)

                if step < 5:
                    await message.answer("📘Вы хотите добавить еще одно направление?", reply_markup=YesOrNoMenu)
                    await StateMachine.YesOrNo.set()
                else:
                    await message.answer("🔷Вы выбрали максимум направлений\n"
                                         "🔹Переходим в главное меню", reply_markup=ReplyKeyboardRemove())

                    counter_step = 0
                    step = int(await select_db("users", "user_id", "step", user_id))
                    while counter_step < step:
                        snls = str(await select_db("users", "user_id", "snls", user_id))

                        info_id = str(counter_step) + '#' + user_id
                        vuz = int(await select_db("info", "info_id", "vuz", info_id))
                        inst = int(await select_db("info", "info_id", "inst", info_id))
                        nap = int(await select_db("info", "info_id", "nap", info_id))
                        form = int(await select_db("info", "info_id", "form", info_id))
                        cat = int(await select_db("info", "info_id", "cat", info_id))

                        main_id = str(vuz) + '#' + str(inst) + '#' + str(nap) + '#' + str(form) + '#' + str(cat) + '#' + user_id

                        check_table = True
                        try:
                            await insert_db("main", "main_id", main_id)
                        except:
                            check_table = False
                            pass
                        if check_table:
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
            else:
                await message.answer("❗️Неверный формат")
        else:
            await message.answer("❗️Неверный формат")


@dp.message_handler(state=StateMachine.YesOrNo)
async def mes_state(message: Message):
    user_id = str(message.from_user.id)

    # ----- start -----
    if message.text == "/start":
        await start_command(user_id, dp)
    # -----------------

    if message.text == "Да✅":
        await message.answer("⚡️Отправьте номер\n"
                             "🔹Выберите ВУЗ:", reply_markup=ReplyKeyboardRemove())

        await message.answer("📖Список:\n"
                             "1. КФУ\n"
                             "2. Наб.Челны\n"
                             "3. Елабуга")

        await update_db("users", "user_id", "check_max", user_id, 3)

        await StateMachine.VuzInfo.set()

    if message.text == "Нет❌":
        await message.answer("🔹Переходим в главное меню", reply_markup=ReplyKeyboardRemove())

        counter_step = 0
        step = int(await select_db("users", "user_id", "step", user_id))
        while counter_step < step:
            snls = str(await select_db("users", "user_id", "snls", user_id))

            info_id = str(counter_step) + '#' + user_id
            vuz = int(await select_db("info", "info_id", "vuz", info_id))
            inst = int(await select_db("info", "info_id", "inst", info_id))
            nap = int(await select_db("info", "info_id", "nap", info_id))
            form = int(await select_db("info", "info_id", "form", info_id))
            cat = int(await select_db("info", "info_id", "cat", info_id))

            main_id = str(vuz) + '#' + str(inst) + '#' + str(nap) + '#' + str(form) + '#' + str(cat) + '#' + user_id

            check_table = True
            try:
                await insert_db("main", "main_id", main_id)
            except:
                check_table = False
                pass
            if check_table:
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
