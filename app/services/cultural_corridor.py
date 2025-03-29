import json
import uuid
from datetime import datetime
from typing import Any

from ..constant import ASSETS_DIR
from ..db import TraditionalStory
from .utils import CompletionMessage, get_openai_client, run_sync

ASSETS_ROOT = ASSETS_DIR / "cultural_corridor"
PROMPT_GENERATE_STORY = ASSETS_ROOT / "generate_story.md"
PROMPT_GENERATE_CASE = ASSETS_ROOT / "generate_case.md"
TEMPLATE_STORY_CONTEXT = ASSETS_ROOT / "story_context.md"

DYNASTY_LIST = [
    {"name": "夏朝", "period": "约前2070年-约前1600年"},
    {"name": "商朝", "period": "约前1600年-约前1046年"},
    {"name": "西周", "period": "约前1046年-前771年"},
    {
        "name": "东周",
        "period": "前770年-前256年",
        "subdynasties": [
            {"name": "春秋时期", "period": "前770年-前476年"},
            {"name": "战国时期", "period": "前475年-前221年"},
        ],
    },
    {"name": "秦朝", "period": "前221年-前207年"},
    {
        "name": "汉朝",
        "period": "前202年-220年",
        "subdynasties": [
            {"name": "西汉", "period": "前202年-8年"},
            {"name": "新朝", "period": "8年-23年"},
            {"name": "东汉", "period": "25年-220年"},
        ],
    },
    {"name": "三国", "period": "220年-280年"},
    {
        "name": "晋朝",
        "period": "265年-420年",
        "subdynasties": [
            {"name": "西晋", "period": "265年-316年"},
            {"name": "东晋", "period": "317年-420年"},
        ],
    },
    {"name": "南北朝", "period": "420年-589年"},
    {"name": "隋朝", "period": "581年-618年"},
    {"name": "唐朝", "period": "618年-907年"},
    {"name": "五代十国", "period": "907年-979年"},
    {
        "name": "宋朝",
        "period": "960年-1279年",
        "subdynasties": [
            {"name": "北宋", "period": "960年-1127年"},
            {"name": "南宋", "period": "1127年-1279年"},
        ],
    },
    {"name": "元朝", "period": "1271年-1368年"},
    {"name": "明朝", "period": "1368年-1644年"},
    {"name": "清朝", "period": "1636年-1912年"},
    {"name": "中华民国", "period": "1912年-1949年"},
    {"name": "中华人民共和国", "period": "1949年-至今"},
]
THEME_CATEGORIES = [
    {
        "name": "神话传说",
        "subcategories": ["创世神话", "英雄传说", "神仙故事", "民间传说"],
    },
    {
        "name": "历史典故",
        "subcategories": ["帝王将相", "名人轶事", "历史事件", "成语故事"],
    },
    {
        "name": "民俗文化",
        "subcategories": ["节日故事", "民间习俗", "地方传统", "民族特色"],
    },
    {
        "name": "伦理道德",
        "subcategories": ["忠义故事", "孝道传承", "友善互助", "诚信为本"],
    },
    {
        "name": "智慧启迪",
        "subcategories": ["哲理故事", "智谋策略", "教育寓言", "处世智慧"],
    },
    {
        "name": "艺术文学",
        "subcategories": ["诗词典故", "戏曲故事", "文学渊源", "艺术传说"],
    },
]
DISCIPLINE_CATEGORIES = [
    {
        "name": "语文",
        "subcategories": ["阅读理解", "写作表达", "文学鉴赏", "古文研习"],
    },
    {
        "name": "数学",
        "subcategories": ["数与代数", "几何图形", "统计概率", "数学应用"],
    },
    {
        "name": "英语",
        "subcategories": ["语言知识", "文化背景", "交际应用", "文学欣赏"],
    },
    {
        "name": "物理",
        "subcategories": ["力学", "热学", "电磁学", "光学与现代物理"],
    },
    {
        "name": "化学",
        "subcategories": ["物质结构", "化学反应", "有机化学", "实验探究"],
    },
    {
        "name": "生物",
        "subcategories": [
            "细胞与分子",
            "生理与解剖",
            "遗传与进化",
            "生态与环境",
        ],
    },
    {
        "name": "历史",
        "subcategories": ["古代史", "近现代史", "世界史", "历史人物研究"],
    },
    {
        "name": "地理",
        "subcategories": ["自然地理", "人文地理", "区域地理", "地图应用"],
    },
    {
        "name": "政治",
        "subcategories": ["思想品德", "法律常识", "经济知识", "国情社情"],
    },
    {"name": "美术", "subcategories": ["绘画", "设计", "雕塑", "艺术欣赏"]},
    {
        "name": "音乐",
        "subcategories": ["乐理知识", "歌曲演唱", "器乐演奏", "音乐欣赏"],
    },
    {
        "name": "体育",
        "subcategories": ["球类运动", "田径项目", "体操与舞蹈", "体能训练"],
    },
    {
        "name": "信息技术",
        "subcategories": ["编程基础", "数据处理", "媒体制作", "信息素养"],
    },
    {
        "name": "综合实践",
        "subcategories": ["研究性学习", "社会实践", "创新设计", "职业体验"],
    },
]


class CulturalCorridorService:
    """时空走廊服务"""

    def __init__(self) -> None:
        self.client, self.model_name = get_openai_client()

    async def generate_traditional_story(
        self, dynasty: str | None, theme: str, keywords: list[str]
    ) -> dict[str, Any]:
        """生成传统故事

        Args:
            dynasty: 朝代（如适用）
            theme: 故事主题
            keywords: 相关关键词列表

        Returns:
            生成的故事内容
        """

        # 准备提示内容
        prompt = (
            PROMPT_GENERATE_STORY.read_text("utf-8")
            .replace("{{dynasty}}", dynasty or "不限")
            .replace("{{theme}}", theme)
            .replace("{{keywords}}", ", ".join(keywords))
        )

        # 调用OpenAI API
        response = await run_sync(self.client.chat.completions.create)(
            model=self.model_name,
            messages=[CompletionMessage().text(prompt).build()],
            temperature=0.7,
        )

        content = response.choices[0].message.content

        if not content:
            raise ValueError("生成故事失败: 返回结果为空")

        # 解析JSON内容
        try:
            content = content[content.index("{") : content.rindex("}") + 1]
            story_data: dict[str, Any] = json.loads(content)

            # 添加ID和创建时间
            story_data["id"] = str(uuid.uuid4())
            story_data["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # 确保包含必要字段
            story_data.setdefault("theme", theme)
            for field in "title", "dynasty", "theme", "content", "moral":
                story_data.setdefault(field, "")

            return story_data
        except Exception as err:
            raise ValueError(f"解析生成内容失败: {err}") from err

    @staticmethod
    def format_story_context(story: TraditionalStory) -> str:
        """格式化故事上下文

        Args:
            story: 传统故事对象

        Returns:
            格式化后的故事上下文
        """
        # 从模板文件读取内容并替换占位符
        return (
            TEMPLATE_STORY_CONTEXT.read_text("utf-8")
            .replace("{{title}}", story.title)
            .replace("{{dynasty}}", story.dynasty or "<朝代:无>")
            .replace("{{period}}", story.period or "<时期:无>")
            .replace("{{theme}}", story.theme)
            .replace("{{content}}", story.content)
            .replace("{{moral}}", story.moral or "无")
        )

    async def generate_cross_discipline_case(
        self,
        story_id: str | None,
        main_discipline: str,
        related_disciplines: list[str],
        suitable_grades: str,
        story_context: str | None = None,
    ) -> dict[str, Any]:
        """生成跨学科延展案例

        Args:
            story_id: 关联的传统故事ID（可选）
            main_discipline: 主要学科
            related_disciplines: 相关学科列表
            suitable_grades: 适用年级范围

        Returns:
            生成的案例内容
        """
        # 准备提示内容
        prompt = (
            PROMPT_GENERATE_CASE.read_text("utf-8")
            .replace("{{main_discipline}}", main_discipline)
            .replace("{{related_disciplines}}", ", ".join(related_disciplines))
            .replace("{{suitable_grades}}", suitable_grades)
            .replace("{{story_context}}", story_context or "无需基于特定故事")
        )

        # 调用OpenAI API
        response = await run_sync(self.client.chat.completions.create)(
            model=self.model_name,
            messages=[CompletionMessage().text(prompt).build()],
            temperature=0.7,
        )

        content = response.choices[0].message.content

        if not content:
            raise ValueError("生成案例失败: 返回结果为空")

        # 解析JSON内容
        try:
            content = content[content.index("{") : content.rindex("}") + 1]
            case_data: dict[str, Any] = json.loads(content)

            # 添加ID和创建时间
            case_data["id"] = str(uuid.uuid4())
            case_data["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            case_data["story_id"] = story_id
            case_data["main_discipline"] = main_discipline
            case_data["related_disciplines"] = ",".join(related_disciplines)
            case_data["suitable_grades"] = suitable_grades

            # 确保包含必要字段
            for field in "title", "content", "teaching_objectives":
                case_data.setdefault(field, "")

            return case_data
        except Exception as err:
            raise ValueError(f"解析生成内容失败: {err}") from err

    @staticmethod
    def get_dynasty_list() -> list[dict[str, Any]]:
        """获取中国朝代列表（按时间顺序）

        Returns:
            朝代列表，包含朝代名称和时间范围
        """
        # 返回预设的朝代列表
        return DYNASTY_LIST

    @staticmethod
    def get_theme_categories() -> list[dict[str, Any]]:
        """获取传统故事主题分类

        Returns:
            主题分类列表
        """
        # 返回预设的主题分类
        return THEME_CATEGORIES

    @staticmethod
    def get_discipline_categories() -> list[dict[str, Any]]:
        """获取学科分类

        Returns:
            学科分类列表
        """
        # 返回预设的学科分类

        return DISCIPLINE_CATEGORIES
