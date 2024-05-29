from typing import List, Tuple, Dict, Any

from app.plugins import _PluginBase


class AutoLitterSister(_PluginBase):
    plugin_name = "小姐姐自己动"
    # 插件描述
    plugin_desc = ""
    # 插件图标
    plugin_icon = "signin.png"
    # 插件版本
    plugin_version = "0.0.1"
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
        pass

    def get_page(self) -> List[dict]:
        pass

    def stop_service(self):
        pass