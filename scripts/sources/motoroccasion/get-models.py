import json

import requests
from bs4 import BeautifulSoup

base_url = 'https://www.motoroccasion.nl/motoren'
fs_url = 'https://www.motoroccasion.nl/fs.php'
mz_url = 'https://www.motoroccasion.nl/mz.php'

mark = '18'


def get_models(mark):
    result = []

    print('start')

    response = requests.get(base_url)
    session_cookie = 'PHPSESSID=' + response.cookies.get_dict()['PHPSESSID']

    # select mark
    print(requests.get(mz_url, params={'params[br]': mark, 'params[a]': 'check'}, headers={'Cookie': session_cookie}))
    response = requests.get(fs_url, params={'s': 'mz'}, headers={'Cookie': session_cookie})

    xml = BeautifulSoup(json.loads(response.content)['types'], 'html.parser')

    models = xml.findAll('option')

    for model in models:
        code = model['value']
        name = model.contents[0]
        if code == '-1':
            continue
        else:
            result.append({'code': code, 'name': name})

    return result


print(get_models(mark))
