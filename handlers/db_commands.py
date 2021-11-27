from data.config import userc, passc, hostc
import psycopg2.extras


conn = psycopg2.connect(dbname="postgres", user=userc, password=passc, host=hostc)


async def insert_db(table, key, value):
    with conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute(f"INSERT INTO {table} ({key}) VALUES (%s)", (value,))


async def update_db(table, wherekey, key, valuewhere, valuekey):
    with conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute(f"UPDATE {table} SET {key} = %s WHERE {wherekey} =%s", (valuekey, valuewhere))


async def select_db(table, wherekey, key, valuewhere):
    with conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute(f"SELECT * FROM {table} WHERE {wherekey} = %s;", (valuewhere,))
            return cur.fetchone()[f"{key}"]


async def delete_db(table, wherekey, valuewhere):
    with conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute(f"DELETE FROM {table} WHERE {wherekey} = %s;", (valuewhere,))


# update_db("info", "my_name", "money", username, "1000")
# insert_db("info", "my_name", username)
# select_db("info", "my_name", "lover", username)
# delete_db("spisok", "id", index)
