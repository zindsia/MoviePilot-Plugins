import os

import requests
from pyquery import PyQuery as pq

from app.log import logger


class JavLibrary:
    top20_url: str = 'https://www.javlibrary.com/cn/vl_mostwanted.php?page='

    def __init__(self):
        pass

    def crawling_top20(self, page):
        proxies = {
            "http": os.environ.get("HTTP_PROXY"),
            "https": os.environ.get("HTTPS_PROXY")
        }
        res = requests.get(url=f'{self.top20_url}{page}', proxies=proxies, allow_redirects=False)
        doc = pq(res.text)
        page_title = doc('head>title').text()
        codes = []
        if page_title.startswith('最想要的影片'):
            videos = doc('div.video>a').items()
            if videos:
                for video in videos:
                    code = video('a div.id').text()
                    codes.append(code)
        return codes

class Metatube:
    metatube_url: str = ''

    def __init__(self, metatube_server):
        self.metatube_url = f"{metatube_server}/v1/movies/search"

    def search(self, keyword):
        url = f"{self.metatube_url}?q={keyword}&provider=AVBASE"
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            if data['data']:
                movie = data['data'][0]
                return movie
        return None
