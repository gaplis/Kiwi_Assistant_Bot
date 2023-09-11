import pymysql
from config import HOST, PORT, USER_DB, PASSWORD_DB, NAME_DB, SCHEMA_DB


class DataBase:
    ALL = '*'
    U_ID = 'id'
    F_NAME = 'first_name'
    U_NAME = 'username'
    LANGUAGE = 'language_code'
    U_CITY = 'city'

    def __init__(self):
        self.connection_db = None
        self.cursor = None

    def __enter__(self):
        self.connection_db = pymysql.connect(
            host=HOST,
            port=PORT,
            user=USER_DB,
            password=PASSWORD_DB,
            database=NAME_DB,
        )
        self.cursor = self.connection_db.cursor()
        print('Подключились к БД')
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection_db.commit()
        self.connection_db.close()
        self.connection_db = self.cursor = None
        print('Отключились от БД')

    def find_user(self, tg_id, column):
        find = f"SELECT {column} FROM {NAME_DB}.{SCHEMA_DB} WHERE tg_id = {tg_id}"
        return self.cursor.execute(find)

    def add_user(self, tg_id, first_name, username, language_code):
        add = f"INSERT INTO {NAME_DB}.{SCHEMA_DB} (tg_id, first_name, username, language_code) " \
                      f"VALUES ({tg_id}, '{first_name}', '{username}', '{language_code}');"
        print('Успешно добавили данные в БД')
        return self.cursor.execute(add)

    def update_user(self, tg_id, whats_update, update_data):
        update = f"UPDATE {NAME_DB}.{SCHEMA_DB} SET {whats_update} = '{update_data}' WHERE tg_id = {tg_id}"
        print('Успешно обновили данные о пользователе в БД')
        return self.cursor.execute(update)