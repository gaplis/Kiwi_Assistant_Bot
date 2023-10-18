
import requests


def get_timezone(city, token):
    if city is not None:
        get = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={token}')
        json_dict = get.json()
        if 'message' not in json_dict:
            return json_dict['timezone']
    return None
