import requests
import json
import time

URL = 'https://5ka.ru/api/v2/special_offers/'
headers = {'User-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                          'Version/13.1 Safari/605.1.15'}
CAT_URL = 'https://5ka.ru/api/v2/categories/'

def x5ka(url, params):
    result = []
    while url:
        response = requests.get(url, headers=headers, params=params) if params else requests.get(url, headers=headers)
        params = None
        data = response.json()
        result.extend(data.get('results'))
        url = data.get('next')
        time.sleep(2)
    return result
if __name__ == '__main__':
    categories = requests.get(CAT_URL, headers=headers).json()
    for cat in categories:
        cat['products'] = x5ka(URL, {'categories': cat['parent_group_code']})
        with open(f'{(cat["parent_group_name"])}.json', 'w') as f:
            f.write(json.dumps(cat))


#https://5ka.ru/api/v2/special_offers/?categories=PUI2