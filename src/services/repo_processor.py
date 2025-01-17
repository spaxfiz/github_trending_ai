import requests
import re
from typing import Dict, List, Optional
from bs4 import BeautifulSoup
from utils.helpers import ConfigLoader


class RepoProcessor:
    def __init__(self):
        self.github_api_base = "https://api.github.com/repos"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
        }

        # 使用 ConfigLoader 获取 GitHub token
        config = ConfigLoader()
        github_token = config.get("github", "token")
        if github_token:
            self.headers["Authorization"] = f"token {github_token}"
        else:
            print("警告: GitHub token 未在配置文件中找到")

    def extract_repo_urls(self, trending_data: List[Dict]) -> List[str]:
        """提取仓库 URL"""
        return [item.get("url", "") for item in trending_data if item.get("url")]

    def get_readme_content(self, repo_url: str) -> Optional[str]:
        """获取仓库的 README 内容"""
        try:
            # 从 repo_url 中提取 owner 和 repo 名称
            parts = repo_url.split("/")
            if len(parts) >= 2:
                owner, repo = parts[-2], parts[-1]
                readme_url = f"{self.github_api_base}/{owner}/{repo}/readme"
                response = requests.get(readme_url, headers=self.headers)
                if response.status_code == 200:
                    # README 内容是 base64 编码的
                    import base64

                    content = response.json().get("content", "")
                    return base64.b64decode(content).decode("utf-8")
        except Exception as e:
            print(f"获取 README 失败: {e}")
        return None

    def clean_readme(self, content: str) -> str:
        """清洗 README 内容"""
        if not content:
            return ""

        # 使用 BeautifulSoup 清除 HTML 标签
        soup = BeautifulSoup(content, "html.parser")
        text = soup.get_text()

        # 清除常见的无关内容
        patterns_to_remove = [
            r"## Table of Contents.*?(?=##|$)",
            r"## Contributing.*?(?=##|$)",
            r"## License.*?(?=##|$)",
            r"## Installation.*?(?=##|$)",
            r"[![.*?]\(.*?\)]",
            r"\[!\[.*?\]\(.*?\)\]",
        ]

        for pattern in patterns_to_remove:
            text = re.sub(pattern, "", text, flags=re.DOTALL)

        # 清理多余的空行和空格
        text = "\n".join(line.strip() for line in text.splitlines() if line.strip())
        return text
