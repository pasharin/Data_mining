import requests
import bs4
import json


headers = {'User-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                          'Version/13.1 Safari/605.1.15'}
URL = 'https://geekbrains.ru/posts'
BASE_URL = 'https://geekbrains.ru'


def get_next_page(soap:bs4.BeautifulSoup) -> str:
    ul = soap.find('ul', attrs={'class':'gb__pagination'})
    a = ul.find(lambda tag: tag.name == 'a' and tag.text == '›')
    return f'{BASE_URL}{a["href"]}' if a else None

def get_post_url(soap:bs4.BeautifulSoup) -> set:
    post_a = soap.select('div.post-items-wrapper div.post-item a')
    return set(f'{BASE_URL}{a["href"]}' for a in post_a)

def get_page(url):
    while url:
        print(url)
        response = requests.get(url, headers=headers)
        soap = bs4.BeautifulSoup(response.text, 'lxml')
        yield soap
        url = get_next_page(soap)

def get_post_info(post_url:str) -> dict:
    post_info = {'url': '', 'image': [], 'title':'', 'writer': '', 'tags':[]}
    response = requests.get(post_url, headers=headers)
    soap = bs4.BeautifulSoup(response.text, 'lxml')
    post_info['title'] = soap.select_one('article h1.blogpost-title').text
    post_info['tags'] = {item.text: f'{BASE_URL}{item["href"]}' for item in soap.select('article a.small')}
    #post_info['image'] = soap.find('article p', attrs={'scr'}).text
    post_info['image'] = soap.select_one('article div.blogpost-content p img')
    post_info['url'] = post_url
    post_info['writer'] = (soap.select_one('article div.text-lg').text), {f'{BASE_URL}{wr_url["href"]}' for wr_url in
                           soap.select('article div.col-md-5 a')}

    return post_info

def clear_file_name(url: str):
    return url.replace('/', '_')

if __name__ == '__main__':
    for_tags ={}

    for soap in get_page(URL):
        posts = get_post_url(soap)
        data_2 = [get_post_info(url) for url in posts]

        for post in data_2:
            file_name = clear_file_name(post['url'])

            for name, url in post['tags'].items():
                if not for_tags.get(name):
                    for_tags[name] = {"posts":[]}
                for_tags[name]['url'] = url
                for_tags[name]['posts'].append(post['url'])

            with open(f'{file_name}.json','w') as file:
                file.write(json.dumps(post))
    with open('tags.json', 'w') as file:
        file.write(json.dumps(for_tags))
        print(1)



'''IMG_URL = 'https://d2xzmw6cctk25h.cloudfront.net/geekbrains/public/ckeditor_assets/pictures'''
