import requests
from aiogram import Dispatcher

# db_commands
from handlers.db_commands import insert_db, update_db, select_db, delete_db


async def get_pos(vuz, inst, nap, form, cat, snls, main_id, info_id):
    url = "https://abiturient.kpfu.ru/entrant/abit_entrant_originals_list"

    params = {
        "p_open": "",
        "p_inst": vuz,
        "p_faculty": inst,
        "p_speciality": nap,
        "p_typeofstudy": form,
        "p_category": cat
    }

    async def get_planPriema(params, url):
        r = requests.get(url, params=params)
        t = r.text
        t = t.split("""<tr""")
        t = t[5][t[5].find("План приема: ")+13:]
        t = t[:t.find(",")]
        return int(t)

    async def sogl_poz(param, pos, url):
        r = requests.get(url, params=param)
        t = r.text
        t = t.split("""<tr""")
        t = t[9:]
        c = 0
        for i in range(pos - 1, -1, -1):
            rev = t[i].split("<td")
            rev = rev[1:]
            for z in range(0, len(rev)):
                rev[z] = rev[z][rev[z].find(('>')) + 1:rev[z].find('<')]
            if rev[len(rev) - 3][1:rev[len(rev) - 3].find("/")] == "да":
                c += 1
        return c  # возвращает позицию среди принятых согласий

    async def get_text(params, url):
        r = requests.get(url, params=params)
        text = []
        for d in range(1, 6):
            t = r.text.split("<tr")
            t = t[d].split('''<option value="''')[1:]
            for i in range(0, len(t)):
                if (t[i].find("selected >") != -1):
                    t[i] = t[i][t[i].find(" >") + 2:]
                    t[i] = t[i][:t[i].find("</")]
                    text.append(t[i])
        return text

    async def request_to_kfu(url, params):
        r = requests.get(url, params=params)
        t = r.text
        t = t.split("""<tr""")
        t = t[9:]
        return t

    async def polz(snls, t):
        for i in range(0, len(t)):
            if (t[i].find(snls) > 0):
                rev = t[i].split("<td")
                rev = rev[1:]
                for i in range(0, len(rev)):
                    rev[i] = rev[i][rev[i].find(('>')) + 1:rev[i].find('<')]
                return rev[0]

    t = await request_to_kfu(url, params)

    check_pos = True
    try:
        pos = int(await polz(snls, t))
    except:
        await delete_db("info", "info_id", info_id)
        check_pos = False

    if check_pos:
        sogl_pos = int(await sogl_poz(params, pos, url)) + 1
        max_sogl = int(await get_planPriema(params, url))

        await update_db("main", "main_id", "sogl_pos", main_id, sogl_pos)
        await update_db("main", "main_id", "max_sogl", main_id, max_sogl)
        await update_db("main", "main_id", "pos", main_id, pos)

        # получаем массив навзваний
        text = await get_text(params, url)

        vuz_name = text[0]
        await update_db("main", "main_id", "vuz_name", main_id, vuz_name)
        inst_name = text[1]
        await update_db("main", "main_id", "inst_name", main_id, inst_name)
        nap_name = text[2]
        await update_db("main", "main_id", "nap_name", main_id, nap_name)
        form_name = text[3]
        await update_db("main", "main_id", "form_name", main_id, form_name)
        cat_name = text[4]
        await update_db("main", "main_id", "cat_name", main_id, cat_name)


async def get_pos_ping(vuz, inst, nap, form, cat, snls, main_id):
    url = "https://abiturient.kpfu.ru/entrant/abit_entrant_originals_list"

    params = {
        "p_open": "",
        "p_inst": vuz,
        "p_faculty": inst,
        "p_speciality": nap,
        "p_typeofstudy": form,
        "p_category": cat
    }

    async def request_to_kfu(url, params):
        r = requests.get(url, params=params)
        t = r.text
        t = t.split("""<tr""")
        t = t[9:]
        return t

    async def sogl_poz(param, pos, url):
        t = await request_to_kfu(url,param)
        c = 0
        for i in range(pos - 1, -1, -1):
            rev = t[i].split("<td")
            rev = rev[1:]
            for z in range(0, len(rev)):
                rev[z] = rev[z][rev[z].find(('>')) + 1:rev[z].find('<')]
            if rev[len(rev) - 3][1:rev[len(rev) - 3].find("/")] == "да":
                c += 1
        return c+1  # возвращает позицию среди принятых согласий

    async def polz(snls, t):
        for i in range(0, len(t)):
            if (t[i].find(snls) > 0):
                rev = t[i].split("<td")
                rev = rev[1:]
                for i in range(0, len(rev)):
                    rev[i] = rev[i][rev[i].find(('>')) + 1:rev[i].find('<')]
                return rev[0]
    t = await request_to_kfu(url, params)
    check_pos = True
    try:
        pos = int(await polz(snls, t))
    except:
        check_pos = False
    if check_pos:
        sogl_pos = await sogl_poz(params, pos, url)
        await update_db("main", "main_id", "sogl_pos", main_id, sogl_pos)
        await update_db("main", "main_id", "pos", main_id, pos)
