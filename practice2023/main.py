import psycopg2
from config import host, user, password, db_name
from create_table import create_table
import pandas as pd

try:
    # подлючение к БД
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name,
    )

    cursor = connection.cursor()

    # проверка существования таблицы в БД
    cursor.execute("""SELECT * from information_schema.tables
                    WHERE table_name=%s""", ('dop_results',))
    answer = bool(cursor.rowcount)

    # если таблица отсутствует, то вызывается функция для ее создания
    if answer is False:
        create_table(cursor, connection)
        print('[INFO] Таблица создана!')

    else:
        print('[INFO] Таблица уже существует в PostgreSQL')

    query = """SELECT id_stand, id_test, id_version, input_rate, ierrors
            FROM dop_results"""
    data = pd.read_sql_query(query, connection)

except Exception as _ex:
    print('[INFO] Error while working with PostgreSQL', _ex)

finally:
    if connection:
        connection.close()
        print('[INFO] PostgreSQL connection closed')
