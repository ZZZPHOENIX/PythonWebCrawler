import requests
from urllib.parse import urlencode
from urllib.request import quote
import os

base_url = 'https://www.toutiao.com/search_content/?'
global index
index = 0

def single_page(keyword, page):
    headers = {
        'referer': 'https://www.toutiao.com/search/?keyword='+quote(keyword),
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3486.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }
    params = {
        'offset': 20*(page-1),
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': 20,
        'cur_tab': 3,
        'from': 'gallery'
    }
    url = base_url + urlencode(params)
    #print(url)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError:
        return None

def get_articles(json):
    #print(json)
    #print(json.keys())
    if json.get('data'):
        for item in json.get('data'):
            title = item.get('title')
            url = item.get('article_url')
            images = item.get('image_list')
            #print(images)
            #print(url)
            img_urls = []
            for img_url in images:
                temp_url = img_url.get('url')
                true_url = 'http:' + temp_url.replace('"', '').replace('list', 'origin')
                img_urls.append(true_url)
            yield {
                'title': title,
                'article_url': url,
                'image': img_urls
            }
            #print(img_urls)

def save_images(item):
    if not os.path.exists(item.get('title')):
        os.mkdir(item.get('title'))
    try:
        count = 1
        global index
        index += 1
        for img_url in item.get('image'):
            response = requests.get(img_url)
            if response.status_code == 200:
                img_path = '{0}/{1}.jpg'.format(item.get('title'), count)
                count += 1
                if not os.path.exists(img_path):
                    with open(img_path, 'wb') as file1:
                        file1.write(response.content)
                else:
                    print("Already Downloaded", img_path)
        url_path = '{0}/address.txt'.format(item.get('title'))
        with open(url_path, 'w') as file2:
            file2.write(item.get('article_url'))
        print("第"+str(index)+"组图片保存完成, 共"+str(count-1)+"幅图片")
    except requests.ConnectionError as e:
        print('Failed to Download Image, Reason: ', e.args)

def main(keyword, page):
    for i in range(1, page+1):
        content = single_page(keyword, i)
        for item in get_articles(content):
            #print(item)
            save_images(item)

if __name__ == '__main__':
    main("街拍", 10)


