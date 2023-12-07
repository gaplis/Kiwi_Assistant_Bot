import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')

HOST = os.getenv('HOST')
PORT = int(os.getenv('PORT'))
USER_DB = os.getenv('USER_DB')
PASSWORD_DB = os.getenv('PASSWORD_DB')
NAME_DB = os.getenv('NAME_DB')
TABLES_DB = {
    'USERS': 'users',
    'STATISTICS': 'statistics',
}

OPEN_WEATHER_TOKEN = os.getenv('OPEN_WEATHER_TOKEN')
