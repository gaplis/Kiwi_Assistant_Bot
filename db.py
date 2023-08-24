import pymysql
from config import host, port, user_db, password_db, name_db, schema


class DataBase:
    all = '*'
    u_id = 'id'
    f_name = 'first_name'
    u_name = 'username'
    language = 'language_code'
    u_city = 'city'

    def __init__(self):
        self.connection_db = None
        self.cursor = None

    def __enter__(self):
        self.connection_db = pymysql.connect(
            host=host,
            port=port,
            user=user_db,
            password=password_db,
            database=name_db,
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
        find = f"SELECT {column} FROM {name_db}.{schema} WHERE tg_id = {tg_id}"
        return self.cursor.execute(find)

    def add_user(self, tg_id, first_name, username, language_code):
        add = f"INSERT INTO {name_db}.{schema} (tg_id, first_name, username, language_code) " \
                      f"VALUES ({tg_id}, '{first_name}', '{username}', '{language_code}');"
        print('Успешно добавили данные в БД')
        return self.cursor.execute(add)

    def update_user(self, tg_id, whats_update, update_data):
        update = f"UPDATE {name_db}.{schema} SET {whats_update} = '{update_data}' WHERE tg_id = {tg_id}"
        print('Успешно обновили данные о пользователе в БД')
        return self.cursor.execute(update)