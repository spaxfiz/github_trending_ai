import requests


class GitHubTrending:
    def __init__(self):
        # 使用 GitHub Trending API (非官方，但比较稳定)
        self.api_url = "https://api.gitterapp.com/repositories"

    def get_trending(self, language: str = None, since: str = "daily"):
        """
        获取 GitHub Trending 数据

        Args:
            language: 编程语言，例如 'python', 'javascript' 等
            since: 时间跨度，可选 'daily', 'weekly', 'monthly'
        """
        params = {"since": since}
        if language:
            params["language"] = language

        try:
            response = requests.get(self.api_url, params=params)
            response.raise_for_status()  # 检查请求是否成功
            return response.json()
        except requests.RequestException as e:
            print(f"获取数据失败: {e}")
            return None
