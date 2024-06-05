from typing import List, Tuple, Dict, Any

from app.log import logger
from app.plugins import _PluginBase
from plugins.autolittersister.mediaserver import Emby, Plex, Jellyfin
from plugins.autolittersister.scraper import JavLibrary, Metatube
from plugins.autolittersister.sites import Torrent, sort_torrents, filter_torrents
from plugins.autolittersister.sites.fsm import FSM
from plugins.autolittersister.sites.mteam import MTeam


class AutoLitterSister(_PluginBase):
    plugin_name = "小姐姐自己动"
    # 插件描述
    plugin_desc = ""
    # 插件图标
    plugin_icon = "Melody_A.png"
    # 插件版本
    plugin_version = "0.0.4"
    # 插件作者
    plugin_author = "envyafish"
    # 作者主页
    author_url = "https://github.com/envyafish"
    # 插件配置项ID前缀
    plugin_config_prefix = "autolittersister_"
    # 加载顺序
    plugin_order = 0
    # 可使用的用户级别
    auth_level = 2

    _enabled: bool = False,
    _notify: bool = True,
    _mteam_api_key: str = "",
    _fsm_api_key: str = "",
    _fsm_passkey: str = "",
    _metatube_url: str = "",
    _emby_server: str = "",
    _emby_api_key: str = "",
    _jellyfin_server: str = "",
    _jellyfin_api_key: str = "",
    _jellyfin_user: str = "",
    _plex_server: str = ""
    _plex_token: str = ""

    def init_plugin(self, config: dict = None):
        if config:
            self._enabled = config.get("enabled", False)
            self._notify = config.get("notify", False)
            self._mteam_api_key = config.get("mteam_api_key", "")
            self._fsm_api_key = config.get("fsm_api_key", "")
            self._fsm_passkey = config.get("fsm_passkey", "")
            self._metatube_url = config.get("metatube_url", "")
            self._emby_server = config.get("emby_server", "")
            self._emby_api_key = config.get("emby_api_key", "")
            self._jellyfin_server = config.get("jellyfin_server", "")
            self._jellyfin_api_key = config.get("jellyfin_api_key", "")
            self._jellyfin_user = config.get("jellyfin_user", "")
            self._plex_server = config.get("plex_server", "")
            self._plex_token = config.get("plex_token", "")

        pass

    def create_db(self):
        # 创建sqllite

        pass

    def get_state(self) -> bool:
        pass

    @staticmethod
    def get_command() -> List[Dict[str, Any]]:
        pass

    def get_api(self) -> List[Dict[str, Any]]:
        pass

    def get_form(self) -> Tuple[List[dict], Dict[str, Any]]:
        return [
            {
                'component': 'VForm',
                'content': [
                    {
                        'component': 'VRow',
                        'content': [
                            {
                                'component': 'VCol',
                                'props': {
                                    'cols': 12,
                                    'md': 3
                                },
                                'content': [
                                    {
                                        'component': 'VSwitch',
                                        'props': {
                                            'model': 'enabled',
                                            'label': '启用插件',
                                        }
                                    }
                                ]
                            },
                            {
                                'component': 'VCol',
                                'props': {
                                    'cols': 12,
                                    'md': 3
                                },
                                'content': [
                                    {
                                        'component': 'VSwitch',
                                        'props': {
                                            'model': 'notify',
                                            'label': '发送通知',
                                        }
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        'component': 'VRow',
                        'content': [
                            {
                                'component': 'VCol',
                                'props': {
                                    'cols': 12,
                                    'md': 12
                                },
                                'content': [
                                    {
                                        'component': 'VTextField',
                                        'props': {
                                            'model': 'mteam_api_key',
                                            'label': '馒头APIKEY',
                                        }
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        'component': 'VRow',
                        'content': [
                            {
                                'component': 'VCol',
                                'props': {
                                    'cols': 12,
                                    'md': 12
                                },
                                'content': [
                                    {
                                        'component': 'VTextField',
                                        'props': {
                                            'model': 'fsm_api_key',
                                            'label': '飞天拉面神教APIKEY',
                                        }
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        'component': 'VRow',
                        'content': [
                            {
                                'component': 'VCol',
                                'props': {
                                    'cols': 12,
                                    'md': 12
                                },
                                'content': [
                                    {
                                        'component': 'VTextField',
                                        'props': {
                                            'model': 'metatube_url',
                                            'label': 'Metatube地址',
                                        }
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        'component': 'VRow',
                        'content': [
                            {
                                'component': 'VCol',
                                'props': {
                                    'cols': 6,
                                    'md': 12
                                },
                                'content': [
                                    {
                                        'component': 'VTextField',
                                        'props': {
                                            'model': 'emby_server',
                                            'label': 'Emby地址',
                                        }
                                    }
                                ]
                            },
                            {
                                'component': 'VCol',
                                'props': {
                                    'cols': 6,
                                    'md': 12
                                },
                                'content': [
                                    {
                                        'component': 'VTextField',
                                        'props': {
                                            'model': 'emby_api_key',
                                            'label': 'Emby APIKEY',
                                        }
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        'component': 'VRow',
                        'content': [
                            {
                                'component': 'VCol',
                                'props': {
                                    'cols': 4,
                                    'md': 12
                                },
                                'content': [
                                    {
                                        'component': 'VTextField',
                                        'props': {
                                            'model': 'jellyfin_server',
                                            'label': 'Jellfin地址',
                                        }
                                    }
                                ]
                            },
                            {
                                'component': 'VCol',
                                'props': {
                                    'cols': 4,
                                    'md': 12
                                },
                                'content': [
                                    {
                                        'component': 'VTextField',
                                        'props': {
                                            'model': 'jellyfin_api_key',
                                            'label': 'Jellyfin APIKEY',
                                        }
                                    }
                                ]
                            },
                            {
                                'component': 'VCol',
                                'props': {
                                    'cols': 4,
                                    'md': 12
                                },
                                'content': [
                                    {
                                        'component': 'VTextField',
                                        'props': {
                                            'model': 'jellyfin_user',
                                            'label': 'Jeelyfin 用户',
                                        }
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        'component': 'VRow',
                        'content': [
                            {
                                'component': 'VCol',
                                'props': {
                                    'cols': 6,
                                    'md': 12
                                },
                                'content': [
                                    {
                                        'component': 'VTextField',
                                        'props': {
                                            'model': 'plex_server',
                                            'label': 'Plex地址',
                                        }
                                    }
                                ]
                            },
                            {
                                'component': 'VCol',
                                'props': {
                                    'cols': 6,
                                    'md': 12
                                },
                                'content': [
                                    {
                                        'component': 'VTextField',
                                        'props': {
                                            'model': 'plex_token',
                                            'label': 'Plex token',
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ], {
            "enabled": False,
            "notify": True,
            "mteam_api_key": "",
            "fsm_api_key": "",
            "fsm_passkey": "",
            "metatube_url": "",
            "emby_server": "",
            "emby_api_key": "",
            "jellyfin_server": "",
            "jellyfin_api_key": "",
            "jellyfin_user": "",
            "plex_server": "",
            "plex_token": ""
        }

    def get_page(self) -> List[dict]:
        pass

    def stop_service(self):
        pass


if __name__ == '__main__':
    library = JavLibrary()
    emby = Emby("", '192.168.50.198:8096')
    plex = Plex("http://192.168.50.198:32400", '')
    jellyfin = Jellyfin("", "", "")
    codes = library.crawling_top20(1)
    exist_codes = []
    for code in codes:
        if emby.is_valid():
            movie = emby.search(code)
            if movie:
                exist_codes.append(code)
                continue
        if plex.is_valid():
            movie = plex.search(code)
            if movie:
                exist_codes.append(code)
                continue
        if jellyfin.is_valid():
            movie = jellyfin.search(code)
            if movie:
                exist_codes.append(code)
                continue
    un_exist_codes = list(set(codes) - set(exist_codes))
    logger.info(f"存在的番号:{exist_codes}")
    logger.info(f"不存在的番号:{un_exist_codes}")
    fsm = FSM("", "")
    mteam = MTeam("", "")

    for code in un_exist_codes:
        torrents: List[Torrent] = []
        logger.info(f"开始搜索番号:{code}")
        if fsm.is_valid():
            fsm_torrents = fsm.search(code)
            torrents.extend(fsm_torrents)
        if mteam.is_valid():
            mteam_toorents = mteam.search(code)
            torrents.extend(mteam_toorents)
        logger.info(f"搜索到的种子列表:")
        for torrent in torrents:
            logger.info(f"站点:{torrent.site}|种子名:{torrent.title}|种子大小:{torrent.size_mb}MB")
        torrents = filter_torrents(torrents, max_size=8000, min_size=3000, only_chinese=False, only_uc=False)
        logger.info(f"过滤后种子列表:")
        for torrent in torrents:
            logger.info(f"站点:{torrent.site}|种子名:{torrent.title}|种子大小:{torrent.size_mb}MB")
        torrents = sort_torrents(torrents)
        logger.info(f"排序后种子列表:")
        for torrent in torrents:
            logger.info(f"站点:{torrent.site}|种子名:{torrent.title}|种子大小:{torrent.size_mb}MB")
        if torrents:
            torrent = torrents[0]
            download_url = mteam.get_torrent_download_url(
                torrent.id) if torrent.site == mteam.site_name else fsm.get_torrent_download_url(torrent.id)
            if download_url:
                logger.info(f"开始下载番号:{code}")
                logger.info(f"下载链接:{download_url}")