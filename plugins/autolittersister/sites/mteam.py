from typing import List

import requests

from app.log import logger
from plugins.autolittersister.sites import Site, Torrent


class MTeam(Site):
    site_name: str = "馒头"
    # 站点域名
    site_domain: str = "https://kp.m-team.cc"
    # 站点API密钥
    site_api_key: str = ""

    def search(self, keyword) -> List[Torrent]:
        reqPayload = {
            "mode": "adult",
            "categories": ["410", "429"],
            "visible": 1,
            "keyword": keyword,
            "pageNumber": 1,
            "pageSize": 100
        }
        headers = {
            'x-api-key': self.site_api_key,
        }
        response = requests.post(f"{self.site_domain}/api/torrent/search", json=reqPayload, headers=headers)
        if response.status_code != 200:
            logger.error(f"馒头请求失败:{response.status_code}")
            return []
        data = response.json()
        if int(data['code']) == 1:
            logger.error(f"馒头搜索报错:{data['message']}")
            return []
        if int(data['code']) == 0:
            mteam_torrents = data['data']['data']
            torrents = []
            for mteam_torrent in mteam_torrents:
                torrents.append(self.convert_torrent(keyword, mteam_torrent))
            return torrents
        return []

    def get_torrent_download_url(self, id):
        reqPayload = {
            "id": id
        }
        headers = {
            'x-api-key': self.site_api_key,
        }
        response = requests.post(f"{self.site_domain}/api/torrent/genDlToken", data=reqPayload, headers=headers)
        data = response.json()
        if data['code'] == 1:
            logger.error(f"馒头获取下载链接报错:{data['message']}")
            return None
        logger.info(f"馒头获取下载链接结果:{data}")
        return data['data']

    def convert_torrent(self, code, mteam_torrent):
        torrent = Torrent(
            id=mteam_torrent['id'],
            site=self.site_name,
            code=code,
            size_mb=int(mteam_torrent['size']) / 1024 / 1024,
            seeders=int(mteam_torrent['status']['seeders']),
            title=f"{mteam_torrent['name']} {mteam_torrent['smallDescr']}"
        )
        return torrent

    def is_valid(self):
        return self.site_api_key
