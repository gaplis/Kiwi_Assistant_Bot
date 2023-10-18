import pymysql
from config import HOST, PORT, USER_DB, PASSWORD_DB, NAME_DB, TABLES_DB


class DataBase:
    ALL = '*'
    U_ID = 'id'
    TG_ID = 'tg_id'
    F_NAME = 'first_name'
    U_NAME = 'username'
    LANGUAGE = 'language_code'
    U_CITY = 'city'
    NOTIFICATIONS = 'notifications'
    TIMEZONE = 'timezone'
    STAT_ID = 'id'
    STAT_U_ID = 'user_id'
    WINS = {
        'TTT': 'ttt_wins',
        'WORDLE': 'wordle_wins',
    }
    LOSES = {
        'TTT': 'ttt_loses',
        'WORDLE': 'wordle_loses',
    }
    DRAWS = {
        'TTT': 'ttt_draws'
    }
    LEAVES = {
        'TTT': 'ttt_leaves',
        'WORDLE': 'wordle_leaves',
    }

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
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection_db.commit()
        self.connection_db.close()
        self.connection_db = self.cursor = None

    def find_user(self, tg_id, column):
        find = f"SELECT {column} FROM {NAME_DB}.{TABLES_DB['USERS']} WHERE tg_id = {tg_id};"
        return self.cursor.execute(find)

    def add_user(self, tg_id, first_name, username, language_code):
        add = f"INSERT INTO {NAME_DB}.{TABLES_DB['USERS']} (tg_id, first_name, username, language_code) " \
              f"VALUES ({tg_id}, '{first_name}', '{username}', '{language_code}');"
        return self.cursor.execute(add)

    def update_user(self, tg_id, whats_update, update_data):
        update = f"UPDATE {NAME_DB}.{TABLES_DB['USERS']} SET {whats_update} = '{update_data}' WHERE tg_id = {tg_id};"
        return self.cursor.execute(update)

    def find_statistics(self, user_id, column):
        find = f"SELECT {column} FROM {NAME_DB}.{TABLES_DB['STATISTICS']} WHERE user_id = {user_id};"
        return self.cursor.execute(find)

    def add_statistics(self, user_id):
        add = f"INSERT INTO {NAME_DB}.{TABLES_DB['STATISTICS']} (user_id) VALUES ({user_id});"
        return self.cursor.execute(add)

    def update_statistics(self, user_id, whats_update, update_data):
        update = f"UPDATE {NAME_DB}.{TABLES_DB['STATISTICS']} " \
                 f"SET {whats_update} = '{update_data}' WHERE user_id = {user_id};"
        return self.cursor.execute(update)

    def find_user_for_notifications(self, *columns):
        find = f"SELECT {', '.join(columns)} FROM {NAME_DB}.{TABLES_DB['USERS']};"
        return self.cursor.execute(find)
