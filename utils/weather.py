import requests


def get_weather(city, token):
    get = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={token}&units=metric')
    return get.json()


def get_weather_5_days(city, token):
    get = requests.get(f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={token}&units=metric')
    return get.json()


weather_descriptions = {
    "Clear": "Ясно☀️",
    "Clouds": "Облачно☁️",
    "Rain": "Дождь🌧️",
    "Drizzle": "Мелкий дождь🌧️",
    "Thunderstorm": "Гроза⛈️",
    "Snow": "Снег🌨️",
    "Haze": "Лёгкий туман🌫️",
    "Mist": "Туман🌫️",
    "Fog": "Сильный туман🌫️",
    "Smoke": "Дымка🌫️",
    "Dust": "Пыльно",
    "Sand": "Песчанный фихрь",
    "Ash": "Вулканический пепел🌋",
    "Squall": "Ветренно💨",
    "Tornado": "Торнадо🌪️",
}
