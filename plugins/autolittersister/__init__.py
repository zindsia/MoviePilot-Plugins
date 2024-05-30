from typing import List, Tuple, Dict, Any

from app.plugins import _PluginBase


class AutoLitterSister(_PluginBase):
    plugin_name = "小姐姐自己动"
    # 插件描述
    plugin_desc = ""
    # 插件图标
    plugin_icon = "Melody_A.png"
    # 插件版本
    plugin_version = "0.0.3"
    # 插件作者
    plugin_author = "envyafish"
    # 作者主页
    author_url = "https://github.com/envyafish"
    # 插件配置项ID前缀
    plugin_config_prefix = "autolittersister_"
    # 加载顺序
    plugin_order = 0
    # 可使用的用户级别
    auth_level = 3

    def init_plugin(self, config: dict = None):
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
                ]
            }
        ], {
            "enabled": False,
            "notify": True,
            "mteam_api_key": "",
            "fsm_api_key": ""
        }

    def get_page(self) -> List[dict]:
        pass

    def stop_service(self):
        pass
