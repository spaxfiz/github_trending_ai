from typing import Dict
from .github_trending import GitHubTrending
from .repo_processor import RepoProcessor
from .ai_analyzer import AIAnalyzer
from .server_chan import ServerChanSender
from .html_generator import HTMLGenerator


class TrendingPipeline:
    def __init__(self, deepseek_api_key: str, server_chan_config: Dict):
        self.trending = GitHubTrending()
        self.processor = RepoProcessor()
        self.analyzer = AIAnalyzer(deepseek_api_key)
        self.wechat = ServerChanSender(server_chan_config)
        self.html_generator = HTMLGenerator()

    def run(self, language: str = None, since: str = "daily", limit: int = 10):
        """运行完整的处理流程"""
        # 1. 获取 trending 数据
        trending_data = self.trending.get_trending(language, since)
        if not trending_data:
            print("没有获取到 trending 数据")
            return

        # 限制处理数量
        trending_data = trending_data[:limit]
        total = len(trending_data)

        processed_repos = []

        for i, repo in enumerate(trending_data, 1):
            print(f"处理第 {i} 个仓库，共 {total} 个")
            try:
                # 2. 获取并处理 README
                readme = self.processor.get_readme_content(repo["url"])
                if not readme:
                    continue

                cleaned_readme = self.processor.clean_readme(readme)

                # 3. AI 分析
                analysis = self.analyzer.analyze_readme(cleaned_readme)

                # 4. 合并数据
                repo_data = {**repo, **analysis}
                processed_repos.append(repo_data)
                # break
            except Exception as e:
                print(f"处理仓库 {repo.get('url')} 失败: {e}")

        # 发送汇总消息
        if processed_repos:
            message = self.wechat.format_trending_message(
                processed_repos, language, since
            )
            self.wechat.send_message(message)

            # 生成 HTML 报告
            html_file = self.html_generator.generate_html(processed_repos)
            print(f"HTML 报告已生成：{html_file}")
