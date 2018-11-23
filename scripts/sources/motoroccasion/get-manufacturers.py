import json

import requests
from bs4 import BeautifulSoup

base_url = 'https://www.motoroccasion.nl/motoren'
fs_url = 'https://www.motoroccasion.nl/fs.php'


def get_manufacturers():
    result = []

    print('start')

    response = requests.get(base_url)
    session_cookie = 'PHPSESSID=' + response.cookies.get_dict()['PHPSESSID']

    response = requests.get(fs_url, params={'s': 'mz'}, headers={'Cookie': session_cookie})

    print(response.status_code)

    xml = BeautifulSoup(json.loads(response.content)['brands'], 'html.parser')

    favourite_and_others = xml.findAll('optgroup')

    for group in favourite_and_others:
        manufacturers = group.findAll('option')
        for manufacturer in manufacturers:
            code = manufacturer['value']
            name = manufacturer.contents[0]
            result.append({'code': code, 'name': name})

    return result


print(get_manufacturers())
