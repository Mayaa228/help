import sqlite3
from peremenie import DB_NAME, TABLE_NAME


def create_db(database_name=DB_NAME):
    connection = sqlite3.connect(database_name)
    connection.close()



def execute_query(sql_query, data=None, db_path=DB_NAME):
    with sqlite3.connect(db_path) as connection:
        cursor = connection.cursor()
        if data:
            cursor.execute(sql_query, data)
        else:
            cursor.execute(sql_query)
        connection.commit()



def execute_selection_query(sql_query, data=None, db_path=DB_NAME):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    if data:
        cursor.execute(sql_query, data)
    else:
        cursor.execute(sql_query)
    rows = cursor.fetchall()
    connection.close()
    return rows



def create_table(table_name):
    sql_query = f'CREATE TABLE IF NOT EXISTS {table_name}' \
                f'(id INTEGER PRIMARY KEY,' \
                f'user_id INTEGER,' \
                f'text TEXT,' \
                f'tts_symbols INTEGER,' \
                f'stt_bloki INTEGER)'
    execute_query(sql_query)



def insert_stt(user_id, stt_bloki):
    sql_query = f'''
    INSERT INTO {TABLE_NAME}
    (user_id, stt_bloki)
    VALUES (?, ?)'''
    execute_query(sql_query, [user_id, stt_bloki])

#не бейте лень

def insert_tts(user_id, text, tts_symbols):
    sql_query = f'''
    INSERT INTO {TABLE_NAME}
    (user_id, text, tts_symbols)
    VALUES (?, ?, ?)'''
    execute_query(sql_query, [user_id, text, tts_symbols])


def count_bloks(user_id):
    sql_query = f'''
    SELECT SUM(stt_bloki)
    FROM {TABLE_NAME}
    WHERE user_id = '{user_id}'
    GROUP BY user_id '''
    data = execute_selection_query(sql_query)

    if data:
        return data[0][0]
    return 0

def count_symbobl(user_id):
    sql_query = f'''
    SELECT SUM(tts_symbols)
    FROM {TABLE_NAME}
    WHERE user_id = '{user_id}'
    GROUP BY user_id '''
    data = execute_selection_query(sql_query)

    if data:
        return data[0][0]
    return 0


def prepare_db():
    create_db()
    create_table(TABLE_NAME)
