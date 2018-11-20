import requests

base_url = 'https://www.motoroccasion.nl/motoren'
x = requests.get(base_url)
session_id = x.cookies.get_dict()['PHPSESSID']
print(x.cookies)
print(session_id)

# select mark
print(requests.get(base_url, params={'params[br]': '4', 'params[a]': 'check'}))

# select model
print(requests.get(base_url, params={'params[br]': '4', 'params[a]': 'check'}, headers={'PHPSESSID': session_id}))

# get list
result = requests.get(
    'https://www.motoroccasion.nl/mz.php',
    params={'params[search]': 'search', 'params[nr]': 'true'},
    headers={'PHPSESSID': session_id}
)

print(result)
print(result.content)
