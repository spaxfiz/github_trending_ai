import os
import yaml
from typing import Any


class ConfigLoader:
    _instance = None
    _config = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigLoader, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._config is None:
            self._load_config()

    def _load_config(self) -> None:
        """加载配置文件"""
        config_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "conf",
            "config.yaml",
        )
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                self._config = yaml.safe_load(f)
        except Exception as e:
            print(f"读取配置文件失败: {e}")
            self._config = {}

    def get(self, *keys: str, default: Any = None) -> Any:
        """
        获取配置项

        用法:
            config.get("github", "token")  # 获取 github.token
            config.get("some_key", default="默认值")  # 带默认值的获取
        """
        value = self._config
        for key in keys:
            if not isinstance(value, dict):
                return default
            value = value.get(key, default)
            if value is None:
                return default
        return value

    def reload(self) -> None:
        """重新加载配置"""
        self._load_config()
