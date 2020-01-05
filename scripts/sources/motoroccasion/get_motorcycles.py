# coding=utf-8
import requests
from bs4 import BeautifulSoup

base_url = 'https://www.motoroccasion.nl/motoren'
mz_url = 'https://www.motoroccasion.nl/mz.php'
fs_url = 'https://www.motoroccasion.nl/fs.php'


# r1150gs
# mark = '4'
# model = 'g528'
# vfr

# mark = '18'
# model = 'g129'


def get_motorcycles(manufacturer, model):
    response = requests.get(base_url)
    session_cookie = 'PHPSESSID=' + response.cookies.get_dict()['PHPSESSID']
    print(response.cookies)
    print(session_cookie)

    # select mark
    print(requests.get(mz_url, params={'params[br]': manufacturer, 'params[a]': 'check'},
                       headers={'Cookie': session_cookie}))
    print(requests.get(fs_url, params={'s': 'mz'}, headers={'Cookie': session_cookie}))
    print(requests.get(mz_url, params={'params[nr]': 'true'}, headers={'Cookie': session_cookie}))

    # select model
    print(requests.get(mz_url, params={'params[ty]': model, 'params[a]': 'check'},
                       headers={'Cookie': session_cookie}))
    print(requests.get(fs_url, params={'s': 'mz', }, headers={'Cookie': session_cookie}))

    ok = True
    result = []

    page_size = 50
    page = 0
    first_id_of_page = ''

    while ok:

        group_response = requests.get(mz_url, params={
            'params[nr]': 'true',
            'params[order]': 'default',
            'params[max]': page_size,
            'params[layout]': 'line',
            'params[every]': '10,6',
            'params[selectie]': 'all',
            'params[singleSelect]': '1',
            'params[a]': 'check',

            'params[s]': page,
            'params[c]': page_size,
        }, headers={'Cookie': session_cookie})

        print(group_response.status_code)

        parser = BeautifulSoup(group_response.content, 'html.parser')

        items = parser.findAll("div", {"class": "table line-tile"})

        if len(items) == 0:
            break
        else:
            id = str(items[0].find('img', {'class': 'line-tile-photo'})['id']).split('-')[2]
            if id == first_id_of_page:
                break
            else:
                first_id_of_page = id

        for item in items:

            id = str(item.find('img', {'class': 'line-tile-photo'})['id']).split('-')[2]

            raw_price = str(
                item.find("span", {"class": "line-tile-price"}).contents[0].encode('utf-8'))
            year_and_mileage = str(item.find("div", {"class": "line-tile-yearmls"}).contents[0])
            url = get_url(item)
            img = get_image_url(item)

            price = parse_price(raw_price)
            year_and_mileage_split = year_and_mileage.split(' ')

            year = year_and_mileage_split[0].replace(',', '')
            mileage = year_and_mileage_split[1]
            mileage_measure = year_and_mileage_split[2]

            if mileage_measure == 'Mls':
                mileage = int(mileage) * 1.6

            result.append({
                'id': id,
                'price': int(price),
                'img': 'https://www.motoroccasion.nl/' + img,
                'url': 'https://www.motoroccasion.nl/' + url,
                'year': int(year),
                'mileage': int(mileage),
                'manufacturer_code': manufacturer,
                'model_code': model
            })

        page += page_size

    print('found ' + str(len(result)) + ' motos')
    return result


def get_image_url(item):
    try:
        return item.next.next.next.next.next.next['src']
    except Exception as e:
        pass

    return ''


def get_url(item):
    try:
        return item.next.next.next.next.next['href']
    except Exception as e:
        pass

    return ''


def parse_price(raw_price):
    price = raw_price.replace('€ ', '').replace(',-', '').replace('.', '')
    result = -1
    try:
        result = int(price)
    except Exception as e:
        pass

    return result
