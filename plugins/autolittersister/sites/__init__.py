from abc import ABCMeta, abstractmethod
from typing import List

from app.log import logger


class Site(metaclass=ABCMeta):
    """
    站点基类
    """
    # 站点名称
    site_name: str = ""
    # 站点域名
    site_domain: str = ""
    # 站点API密钥
    site_api_key: str = ""
    # 站点passkey
    site_passkey: str = ""

    def __init__(self, api_key, passkey):
        self.site_api_key = api_key
        self.site_passkey = passkey
        pass

    @abstractmethod
    def search(self, keyword):
        pass

    @abstractmethod
    def get_torrent_download_url(self, torrent):
        pass

    @abstractmethod
    def is_valid(self):
        pass


class Torrent:
    id: int = 0
    site: str = ""
    code: str = ""
    size_mb: float = 0
    seeders: int = 0
    title: str = ""
    chinese: bool = False
    uc: bool = False

    cn_keywords: List[str] = ['中字', '中文字幕', '色花堂', '字幕']
    uc_keywords: List[str] = ['UC', '无码', '步兵']

    def __init__(self, id, site, code, size_mb, seeders, title):
        self.id = id
        self.site = site
        self.code = code
        self.size_mb = size_mb
        self.seeders = seeders
        self.title = title
        self.chinese = self.has_chinese(title)
        self.uc = self.has_uc(title)

    def has_chinese(self, title: str):
        has_chinese = False
        for keyword in self.cn_keywords:
            if title.find(keyword) > -1:
                has_chinese = True
                break
        return has_chinese

    def has_uc(self, title: str):
        uc = False
        for keyword in self.uc_keywords:
            if title.find(keyword) > -1:
                uc = True
                break
        return uc


def sort_torrents(torrents: List[Torrent]):
    upload_sort_list = sorted(torrents, key=lambda torrent: torrent.seeders, reverse=True)
    cn_sort_list = sorted(upload_sort_list, key=lambda torrent: torrent.chinese, reverse=True)
    uc_sort_list = sorted(cn_sort_list, key=lambda torrent: torrent.uc, reverse=True)
    return uc_sort_list


def filter_torrents(torrents: List[Torrent], max_size, min_size, only_chinese=False, only_uc=False):
    filter_list = []
    for torrent in torrents:
        size_mb = torrent.size_mb
        if not size_mb:
            continue
        if max_size:
            if size_mb > max_size:
                continue
        if min_size:
            if size_mb < min_size:
                continue
        if only_chinese:
            if not torrent.chinese:
                continue
        if only_uc:
            if not torrent.uc:
                continue
        filter_list.append(torrent)
    return filter_list
