from aiogram import Dispatcher

import asyncio

from handlers.ParsePos import get_pos_ping

# db_commands
from handlers.db_commands import insert_db, update_db, select_db, delete_db


async def ping(dp: Dispatcher):
    while True:
        sr_num = 1
        break_check = 0
        while True:
            try:
                main_id = str(await select_db("main", "sr_num", "main_id", sr_num))
            except:
                if break_check > 15:
                    break
                else:
                    break_check += 1
                    sr_num += 1
                    continue

            break_check = 0

            vuz = int(main_id[:main_id.find('#')])
            main_id = main_id[main_id.find('#') + 1:]
            inst = int(main_id[:main_id.find('#')])
            main_id = main_id[main_id.find('#') + 1:]
            nap = int(main_id[:main_id.find('#')])
            main_id = main_id[main_id.find('#') + 1:]
            form = int(main_id[:main_id.find('#')])
            main_id = main_id[main_id.find('#') + 1:]
            cat = int(main_id[:main_id.find('#')])
            main_id = main_id[main_id.find('#') + 1:]
            user_id = main_id

            main_id = str(await select_db("main", "sr_num", "main_id", sr_num))

            snls = str(await select_db("users", "user_id", "snls", user_id))

            await get_pos_ping(vuz, inst, nap, form, cat, snls, main_id)

            # Отправка

            podpis = int(await select_db("users", "user_id", "podpis", user_id))
            if podpis == 1:
                counter_step = 0
                step = int(await select_db("users", "user_id", "step", user_id))
                await dp.bot.send_message(user_id, "📥Подписка")
                while counter_step < step:
                    vuz_name = str(await select_db("main", "main_id", "vuz_name", main_id))
                    inst_name = str(await select_db("main", "main_id", "inst_name", main_id))
                    nap_name = str(await select_db("main", "main_id", "nap_name", main_id))
                    form_name = str(await select_db("main", "main_id", "form_name", main_id))
                    cat_name = str(await select_db("main", "main_id", "cat_name", main_id))
                    pos = str(await select_db("main", "main_id", "pos", main_id))
                    sogl_pos = str(await select_db("main", "main_id", "sogl_pos", main_id))

                    await dp.bot.send_message(user_id, f"🔹ВУЗ: {vuz_name}\n"
                                                       f"🔹Институт/Факультет: {inst_name}\n"
                                                       f"🔹Направление подготовки/Cпециальность: {nap_name}\n"
                                                       f"🔹Форма обучения: {form_name}\n"
                                                       f"🔹Категория: {cat_name}\n"
                                                       f"🔸Позиция: {pos}\n"
                                                       f"🔺Позиция среди Согласий: {sogl_pos}")

                    counter_step += 1
            sr_num += 1
        await asyncio.sleep(30)

# asyncio.run(ping())
