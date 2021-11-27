from aiogram import Dispatcher
import requests

# db_commands
from handlers.db_commands import insert_db, update_db, select_db, delete_db


async def get_inst_text(vuz, user_id, dp: Dispatcher):
    async def req_appl(d):
        ids = []
        text = ""
        t = r.text.split("<tr")
        t = t[d].split('''<option value="''')[1:]
        for i in range(0, len(t)):
            ids.append(t[i][:t[i].find('">')])
            t[i] = t[i][t[i].find(('>')) + 1:]
            t[i] = t[i][:t[i].find('<')]
            text += str(i+1)+". "+t[i]+"\n"
            check_max = i + 1
        return ids, text, check_max

    url = "https://abiturient.kpfu.ru/entrant/abit_entrant_originals_list"

    param = {
        "p_open": "",
        "p_inst": vuz
    }

    r = requests.get(url, params=param)

    ids, text, check_max = await req_appl(2)

    await update_db("users", "user_id", "check_max", user_id, check_max)

    await dp.bot.send_message(user_id, f"📖Список:\n"
                              f"{text}")


async def get_inst_value(vuz, num, user_id):
    async def req_appl(d):
        ids = []
        t = r.text.split("<tr")
        t = t[d].split('''<option value="''')[1:]
        for i in range(0, len(t)):
            ids.append(t[i][:t[i].find('">')])
            t[i] = t[i][t[i].find(('>')) + 1:]
            t[i] = t[i][:t[i].find('<')]
        return ids

    url = "https://abiturient.kpfu.ru/entrant/abit_entrant_originals_list"

    param = {
        "p_open": "",
        "p_inst": vuz
    }

    r = requests.get(url, params=param)

    ids = await req_appl(2)

    inst = int(ids[num-1])

    step = str(await select_db("users", "user_id", "step", user_id))
    info_id = step + '#' + user_id
    await update_db("info", "info_id", "inst", info_id, inst)


async def get_nap_text(vuz, inst, user_id, dp: Dispatcher):
    async def req_appl(d):
        ids = []
        text = ""
        t = r.text.split("<tr")
        t = t[d].split('''<option value="''')[1:]
        for i in range(0, len(t)):
            ids.append(t[i][:t[i].find('">')])
            t[i] = t[i][t[i].find(('>')) + 1:]
            t[i] = t[i][:t[i].find('<')]
            text += str(i+1)+". "+t[i]+"\n"
            check_max = i + 1
        return ids, text, check_max

    url = "https://abiturient.kpfu.ru/entrant/abit_entrant_originals_list"

    param = {
        "p_open": "",
        "p_inst": vuz,
        "p_faculty": inst
    }
    r = requests.get(url, params=param)

    ids, text, check_max = await req_appl(3)

    await update_db("users", "user_id", "check_max", user_id, check_max)

    await dp.bot.send_message(user_id, f"📖Список:\n"
                              f"{text}")


async def get_nap_value(vuz, inst, num, user_id):
    async def req_appl(d):
        ids = []
        t = r.text.split("<tr")
        t = t[d].split('''<option value="''')[1:]
        for i in range(0, len(t)):
            ids.append(t[i][:t[i].find('">')])
            t[i] = t[i][t[i].find(('>')) + 1:]
            t[i] = t[i][:t[i].find('<')]
        return ids

    url = "https://abiturient.kpfu.ru/entrant/abit_entrant_originals_list"

    param = {
        "p_open": "",
        "p_inst": vuz,
        "p_faculty": inst
    }
    r = requests.get(url, params=param)

    ids = await req_appl(3)

    nap = int(ids[num-1])

    step = str(await select_db("users", "user_id", "step", user_id))
    info_id = step + '#' + user_id
    await update_db("info", "info_id", "nap", info_id, nap)


async def get_form_text(vuz, inst, nap, user_id, dp: Dispatcher):
    async def req_appl(d):
        ids = []
        text = ""
        t = r.text.split("<tr")
        t = t[d].split('''<option value="''')[1:]
        for i in range(0, len(t)):
            ids.append(t[i][:t[i].find('">')])
            t[i] = t[i][t[i].find(('>')) + 1:]
            t[i] = t[i][:t[i].find('<')]
            text += str(i + 1) + ". " + t[i] + "\n"
            check_max = i + 1
        return ids, text, check_max

    url = "https://abiturient.kpfu.ru/entrant/abit_entrant_originals_list"

    param = {
        "p_open": "",
        "p_inst": vuz,
        "p_faculty": inst,
        "p_speciality": nap
    }
    r = requests.get(url, params=param)

    ids, text, check_max = await req_appl(4)

    await update_db("users", "user_id", "check_max", user_id, check_max)

    await dp.bot.send_message(user_id, f"📖Список:\n"
                                       f"{text}")


async def get_form_value(vuz, inst, nap, num, user_id):
    async def req_appl(d):
        ids = []
        t = r.text.split("<tr")
        t = t[d].split('''<option value="''')[1:]
        for i in range(0, len(t)):
            ids.append(t[i][:t[i].find('">')])
            t[i] = t[i][t[i].find(('>')) + 1:]
            t[i] = t[i][:t[i].find('<')]
        return ids

    url = "https://abiturient.kpfu.ru/entrant/abit_entrant_originals_list"

    param = {
        "p_open": "",
        "p_inst": vuz,
        "p_faculty": inst,
        "p_speciality": nap
    }
    r = requests.get(url, params=param)

    ids = await req_appl(4)

    form = int(ids[num-1])

    step = str(await select_db("users", "user_id", "step", user_id))
    info_id = step + '#' + user_id
    await update_db("info", "info_id", "form", info_id, form)


async def get_cat_text(vuz, inst, nap, form, user_id, dp: Dispatcher):
    async def req_appl(d):
        ids = []
        text = ""
        t = r.text.split("<tr")
        t = t[d].split('''<option value="''')[1:]
        for i in range(0, len(t)):
            ids.append(t[i][:t[i].find('">')])
            t[i] = t[i][t[i].find(('>')) + 1:]
            t[i] = t[i][:t[i].find('<')]
            text += str(i + 1) + ". " + t[i] + "\n"
            check_max = i + 1
        return ids, text, check_max

    url = "https://abiturient.kpfu.ru/entrant/abit_entrant_originals_list"

    param = {
        "p_open": "",
        "p_inst": vuz,
        "p_faculty": inst,
        "p_speciality": nap,
        "p_typeofstudy": form
    }

    r = requests.get(url, params=param)

    ids, text, check_max = await req_appl(5)

    await update_db("users", "user_id", "check_max", user_id, check_max)

    await dp.bot.send_message(user_id, f"📖Список:\n"
                                       f"{text}")


async def get_cat_value(vuz, inst, nap, form, num, user_id):
    async def req_appl(d):
        ids = []
        t = r.text.split("<tr")
        t = t[d].split('''<option value="''')[1:]
        for i in range(0, len(t)):
            ids.append(t[i][:t[i].find('">')])
            t[i] = t[i][t[i].find(('>')) + 1:]
            t[i] = t[i][:t[i].find('<')]
        return ids

    url = "https://abiturient.kpfu.ru/entrant/abit_entrant_originals_list"

    param = {
        "p_open": "",
        "p_inst": vuz,
        "p_faculty": inst,
        "p_speciality": nap,
        "p_typeofstudy": form
    }

    r = requests.get(url, params=param)

    ids = await req_appl(5)

    cat = int(ids[num - 1] [:1])

    step = str(await select_db("users", "user_id", "step", user_id))
    info_id = step + '#' + user_id
    await update_db("info", "info_id", "cat", info_id, cat)
