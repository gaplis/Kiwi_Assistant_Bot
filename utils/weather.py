import requests


def get_weather(city, token):
    get = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={token}&units=metric')
    return get.json()


def get_weather_5_days(city, token):
    get = requests.get(f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={token}&units=metric')
    return get.json()
