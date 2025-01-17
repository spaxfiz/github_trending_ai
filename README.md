# GitHub Trending 分析助手

## 项目简介
这是一个自动化工具，用于获取、分析和推送 GitHub Trending 项目信息。它能够自动抓取 GitHub 趋势项目，使用 AI 进行分析，并通过微信推送通知。

## 核心功能
- 🔍 获取 GitHub Trending 数据
- 📝 自动处理和清理项目 README
- 🤖 使用 AI 进行项目分析
- 📱 通过 Server酱 推送微信通知
- 📊 生成 HTML 报告

## 技术架构
项目采用管道式架构，主要包含以下组件：
- `GitHubTrending`: 获取 GitHub trending 数据
- `RepoProcessor`: 处理仓库 README 内容
- `AIAnalyzer`: 使用 Deepseek API 进行智能分析
- `ServerChanSender`: 发送微信通知
- `HTMLGenerator`: 生成 HTML 报告

## 配置说明
项目配置文件位于 `conf/` 目录下：
- `config.yaml`: 主配置文件
- `config.yaml.backup`: 配置文件备份

### 必要配置项
- Deepseek API 密钥
- Server酱配置信息

## 使用说明
主要功能通过 `TrendingPipeline` 类提供，支持以下参数：
- `language`: 指定编程语言（可选）
- `since`: 时间范围（默认：daily）
- `limit`: 处理仓库数量（默认：10）

## 开发说明
项目使用 Python 开发，主要依赖：
- Cursor
- Deepseek

## 使用说明
1. 配置 config.yaml 参考 config.yaml.backup
2. 运行 main.py
