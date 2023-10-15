from bs4 import BeautifulSoup
import requests
import pyshorteners

# ToDo: Убирать ссылки из получаемого текста
def get_search_data(query):
    q = query.replace(' ', '+')

    google_url = f"https://google.ru/search?q={q}"
    get = requests.get(google_url)
    soup = BeautifulSoup(get.text, features="lxml")
    find_main = soup.find(id="main")
    find_next_element = find_main.next_element
    find_next_block = find_next_element.find_next_sibling()

    for _ in range(7):
        find_next_block = find_next_block.find_next_sibling()

    list_data = []
    for _ in range(3):
        find_next_block = find_next_block.find_next_sibling()

        href = find_next_block.find('a').get('href')
        short_url = pyshorteners.Shortener().clckru.short(f'https://google.ru{href}')

        enter_the_block = find_next_block.next_element.next_element.find_next_sibling()
        text = f'{enter_the_block.text[:-6]}...'

        result_search = {
            'url': short_url,
            'text': text,
        }
        list_data.append(result_search)
    list_data.append({
        'url': google_url,
        'text': 'Поиск в Google',
    })

    return list_data
