from typing import List

import requests

from app.log import logger
from plugins.autolittersister.sites import Site, Torrent


class FSM(Site):
    site_name: str = "飞天拉面神教"
    # 站点域名
    site_domain: str = "https://api.fsm.name"
    # 站点API密钥
    site_api_key: str = ""
    # 站点passkey
    site_passkey: str = ""

    def search(self, keyword) -> List[Torrent]:
        search_url = f"{self.site_domain}/Torrents/listTorrents?keyword={keyword}&page=1&type=AV&systematics=0&tags=[]"
        headers = {
            'APITOKEN': self.site_api_key,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(search_url, headers=headers)
        if response.status_code != 200:
            logger.error(f"飞天拉面神教请求失败:{response.status_code}")
            return []
        data = response.json()
        fsm_torrents = data['data']['list']
        torrents = []
        for fsm_torrent in fsm_torrents:
            torrents.append(self.convert_torrent(keyword, fsm_torrent))
        return torrents

    def get_torrent_download_url(self, tid):
        download_url = f"{self.site_domain}/Torrents/download?tid={tid}&passkey={self.site_passkey}&source=direct"
        return download_url

    def convert_torrent(self, code, fsm_torrent):
        torrent = Torrent(
            id=fsm_torrent['tid'],
            site=self.site_name,
            code=code,
            size_mb=int(fsm_torrent['fileRawSize']) / 1024 / 1024,
            seeders=int(fsm_torrent['peers']['upload']),
            title=fsm_torrent['title']
        )
        return torrent

    def is_valid(self):
        return self.site_api_key and self.site_passkey
