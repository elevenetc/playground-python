import requests
from bs4 import BeautifulSoup

base_url = 'https://www.motoroccasion.nl/motoren'
mz_url = 'https://www.motoroccasion.nl/mz.php'
fs_url = 'https://www.motoroccasion.nl/fs.php'

print('start')

response = requests.get(base_url)
session_cookie = 'PHPSESSID=' + response.cookies.get_dict()['PHPSESSID']
print(response.cookies)
print(session_cookie)

# select mark
print(requests.get(mz_url, params={'params[br]': '4', 'params[a]': 'check'}, headers={'Cookie': session_cookie}))
print(requests.get(fs_url, params={'s': 'mz'}, headers={'Cookie': session_cookie}))
print(requests.get(mz_url, params={'params[nr]': 'true'}, headers={'Cookie': session_cookie}))

# select model
print(requests.get(mz_url, params={'params[ty]': 'g528', 'params[a]': 'check'}, headers={'Cookie': session_cookie}))
print(requests.get(fs_url, params={'s': 'mz', }, headers={'Cookie': session_cookie}))

result = requests.get(mz_url, params={'params[nr]': 'true'}, headers={'Cookie': session_cookie})
print(result.status_code)

parser = BeautifulSoup(result.content, 'html.parser')

items = parser.findAll("div", {"class": "table line-tile"})

if len(items) == 0:
    print('no moto')
else:
    print('found ' + str(len(items)) + ' motos')

    motos = []

    for item in items:
        price = str(item.find("span", {"class": "line-tile-price"}).contents[0])
        year_and_mileage = str(item.find("div", {"class": "line-tile-yearmls"}).contents[0])
        url = item.next.next.next.next.next['href']
        img = item.next.next.next.next.next.next['src']

        price = price.replace('€ ', '').replace(',-', '').replace('.', '')
        year_and_mileage = year_and_mileage.split(' ')

        year = year_and_mileage[0].replace(',', '')
        mileage = year_and_mileage[1]
        mileage_measure = year_and_mileage[2]

        if mileage_measure == 'Mls':
            mileage = int(mileage) * 1.6

        motos.append({
            'price': int(price),
            'img': 'https://www.motoroccasion.nl/' + img,
            'url': 'https://www.motoroccasion.nl/' + url,
            'year': int(year),
            'mileage': int(mileage)
        })

    print(str(motos))

# print(result)
# print(result.content)
