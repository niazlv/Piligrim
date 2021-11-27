from data.config import userc, passc, hostc

import psycopg2.extras


async def create_db():
    conn = psycopg2.connect(dbname="postgres", user=userc, password=passc, host=hostc)

    with conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            try:
                cur.execute("CREATE TABLE users (user_id integer primary key,"
                            "user_num serial,"
                            "snls varchar,"
                            "step integer default 0,"
                            "check_max integer,"
                            "podpis integer default 0);")
            except:
                pass

            try:
                cur.execute("CREATE TABLE info (info_id varchar,"
                            "vuz integer,"
                            "inst integer,"
                            "nap integer,"
                            "form integer,"
                            "cat integer);")
            except:
                pass
            try:
                cur.execute("CREATE TABLE main (main_id varchar primary key,"
                            "sr_num serial,"
                            "vuz_name varchar,"
                            "inst_name varchar,"
                            "nap_name varchar,"
                            "form_name varchar,"
                            "cat_name varchar,"
                            "pos integer,"
                            "sogl_pos integer,"
                            "max_sogl integer);")
            except:
                pass
    conn.close()
