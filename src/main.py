from services.trending_pipeline import TrendingPipeline
from utils.helpers import ConfigLoader


def main():
    """主程序入口函数"""
    config = ConfigLoader()

    pipeline = TrendingPipeline(
        deepseek_api_key=config.get("deepseek", "api_key"),
        server_chan_config={
            "server_chan": {"send_key": config.get("server_chan", "send_key")}
        },
    )

    # 运行流程
    pipeline.run(language="", since="daily", limit=10)


if __name__ == "__main__":
    main()
