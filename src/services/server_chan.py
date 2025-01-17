import requests
from typing import Dict, List


class ServerChanSender:
    def __init__(self, config: Dict):
        """初始化 Server酱 发送器

        Args:
            config: 包含 server_chan 配置的字典
        """
        self.send_key = config.get("server_chan", {}).get("send_key")
        if not self.send_key:
            raise ValueError("Server酱 send_key 未配置")
        self.api_url = f"https://sctapi.ftqq.com/{self.send_key}.send"

    def format_repo_message(self, repo_data: Dict) -> str:
        """格式化单个仓库的消息"""
        # 检查 AI 分析是否成功
        if not repo_data.get("success", False):
            return f"""### {repo_data.get("name", "Unknown")}
> AI 分析失败：{repo_data.get("error", "未知错误")}
[查看项目]({repo_data.get("url", "")})
"""
        # 给技术栈标签添加 ` 符号
        tech_tags = (
            f"\n**技术栈**: {'  '.join(f'`{tag}`' for tag in repo_data.get('tech_tags', []))}"
            if repo_data.get("tech_tags")
            else ""
        )
        # 给领域标签添加 ` 符号
        domain_tags = (
            f"\n**领域**:{'  '.join(f'`{tag}`' for tag in repo_data.get('domain_tags', []))}"
            if repo_data.get("domain_tags")
            else ""
        )

        return f"""### {repo_data.get("name", "Unknown")}
> {repo_data.get("summary", "")}
{tech_tags}\n{domain_tags}
[查看项目]({repo_data.get("url", "")})\n----
"""

    def format_trending_message(
        self, repos_data: List[Dict], language: str = None, since: str = "daily"
    ) -> Dict:
        """格式化完整的趋势消息"""
        time_map = {"daily": "今日", "weekly": "本周", "monthly": "本月"}
        title = f"GitHub {time_map.get(since, '今日')}趋势项目"
        if language:
            title += f" - {language}"

        # 合并所有仓库信息
        content = "\n\n".join([self.format_repo_message(repo) for repo in repos_data])

        return {"title": title, "desp": content}

    def send_message(self, message: Dict) -> bool:
        """发送消息到 Server酱"""
        try:
            # 打印消息体用于调试
            print("\n=== 发送的消息内容 ===")
            print("标题:", message.get("title"))
            print("\n正文:")
            print(message.get("desp"))
            print("==================\n")

            response = requests.post(self.api_url, data=message)
            result = response.json()

            if response.status_code != 200:
                print(f"HTTP 错误: {response.status_code}")
                print(f"错误详情: {response.text}")
                return False

            if result.get("code") != 0:
                print(f"发送失败: {result.get('message', '未知错误')}")
                return False

            print("消息发送成功")
            return True

        except requests.exceptions.RequestException as e:
            print(f"请求异常: {str(e)}")
            return False
        except Exception as e:
            print(f"未知错误: {str(e)}")
            return False
