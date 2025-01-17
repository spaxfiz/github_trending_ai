import requests
from typing import Dict, Optional
import json
from dataclasses import dataclass
from typing import List


class AIAnalyzer:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.api_url = "https://api.deepseek.com/v1/chat/completions"

    def _extract_content(self, response_json: Dict) -> Optional[str]:
        """
        从 API 响应中提取 content 内容

        Args:
            response_json: API 返回的 JSON 数据

        Returns:
            str: 提取的内容，如果提取失败则返回 None
        """
        try:
            return response_json["choices"][0]["message"]["content"]
        except (KeyError, IndexError) as e:
            print(f"提取内容失败: {e}")
            return None

    def analyze_readme(self, content: str) -> Dict:
        """使用 Deepseek API 分析 README 内容"""
        prompt = f"""请分析以下项目 README 内容，并提供：
1. 项目简短总结（100字以内的中文）
2. 技术标签（包括编程语言、框架、工具等）
3. 应用领域标签（如 AI、Web开发、数据科学等）

请以下面的 JSON 格式返回结果：
{{
    "summary": "项目总结",
    "tech_tags": ["技术1", "技术2"],
    "domain_tags": ["领域1", "领域2"]
}}

README 内容：
{content[:10000]}
"""

        try:
            response = requests.post(
                self.api_url,
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "model": "deepseek-chat",
                    "messages": [{"role": "user", "content": prompt}],
                },
            )

            if response.status_code == 200:
                result = response.json()
                ai_content = self._extract_content(result)

                if ai_content:
                    try:
                        # 解析结构化数据
                        analysis = parse_analysis_result(ai_content)
                        return {
                            "success": True,
                            "summary": analysis.summary,
                            "tech_tags": analysis.tech_tags,
                            "domain_tags": analysis.domain_tags,
                        }
                    except (json.JSONDecodeError, KeyError) as e:
                        return {"success": False, "error": f"解析响应失败: {str(e)}"}

                return {"success": False, "error": "无法获取有效响应"}

        except Exception as e:
            print(f"AI 分析失败: {e}")
            return {"success": False, "error": str(e)}


@dataclass
class ReadmeAnalysis:
    """README 分析结果的数据类"""

    summary: str
    tech_tags: List[str]
    domain_tags: List[str]


def parse_analysis_result(json_str: str) -> ReadmeAnalysis:
    """
    解析 AI 分析返回的 JSON 字符串

    Args:
        json_str: JSON 格式的字符串

    Returns:
        ReadmeAnalysis: 结构化的分析结果

    Raises:
        json.JSONDecodeError: 当 JSON 解析失败时
        KeyError: 当缺少必要字段时
    """
    try:
        # 移除 Markdown 代码块标记
        clean_json = json_str.replace("```json", "").replace("```", "").strip()

        # 解析 JSON
        data = json.loads(clean_json)

        # 转换为数据类
        return ReadmeAnalysis(
            summary=data["summary"],
            tech_tags=data["tech_tags"],
            domain_tags=data["domain_tags"],
        )

    except json.JSONDecodeError as e:
        print(f"JSON 解析失败: {e}")
        raise
    except KeyError as e:
        print(f"缺少必要字段: {e}")
        raise
