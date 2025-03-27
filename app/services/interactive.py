import json
import uuid
from datetime import datetime

from .utils import CompletionMessage, get_openai_client, run_sync
from ..constant import ASSETS_DIR

ASSETS_ROOT = ASSETS_DIR / "interactive"
PROMPT_ACTIVITY = ASSETS_ROOT / "activity.md"
PROMPT_SCENARIO = ASSETS_ROOT / "scenario.md"


class InteractiveGenerator:
    def __init__(self) -> None:
        self.client, self.model_name = get_openai_client()

    async def generate_activity(
        self,
        activity_type: str,
        subject: str,
        grade: str,
        topic: str,
        duration: int,
    ) -> tuple[dict, dict]:
        """生成互动教学活动

        Args:
            activity_type: 活动类型，如'discussion', 'question', 'game'
            subject: 学科
            grade: 年级
            topic: 主题
            duration: 时长(分钟)

        Returns:
            dict: 生成的活动内容
        """

        # 填充模板
        prompt = (
            PROMPT_ACTIVITY.read_text(encoding="utf-8")
            .replace("{{activity_type}}", activity_type)
            .replace("{{subject}}", subject)
            .replace("{{grade}}", grade)
            .replace("{{topic}}", topic)
            .replace("{{duration}}", str(duration))
        )

        # 调用OpenAI API生成活动方案
        response = await run_sync(self.client.chat.completions.create)(
            model=self.model_name,
            messages=[CompletionMessage().text(prompt).build()],
            temperature=0.7,
        )

        content = response.choices[0].message.content

        if not content:
            raise ValueError("生成内容为空")

        # 解析生成的JSON内容
        try:
            content = content[content.index("{") : content.rindex("}") + 1]
            result: dict = json.loads(content)
        except Exception as err:
            raise ValueError("解析生成内容失败") from err

        metadata = {
            "id": str(uuid.uuid4()),
            "title": result.get("title", topic),
            "activity_type": activity_type,
            "description": result.get("description", ""),
            "subject": subject,
            "grade": grade,
            "duration": duration,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        return metadata, result

    async def generate_scenario(
        self,
        scenario_type: str,
        subject: str,
        grade: str,
        theme: str,
    ) -> tuple[dict, dict]:
        """生成情景模拟场景

        Args:
            scenario_type: 场景类型，如'historical', 'literary', 'scientific'
            subject: 学科
            grade: 年级
            theme: 主题

        Returns:
            dict: 生成的场景内容
        """

        # 填充模板
        prompt = (
            PROMPT_SCENARIO.read_text(encoding="utf-8")
            .replace("{{scenario_type}}", scenario_type)
            .replace("{{subject}}", subject)
            .replace("{{grade}}", grade)
            .replace("{{theme}}", theme)
        )

        # 调用OpenAI API生成场景
        response = await run_sync(self.client.chat.completions.create)(
            model=self.model_name,
            messages=[CompletionMessage().text(prompt).build()],
            temperature=0.7,
        )

        content = response.choices[0].message.content

        if not content:
            raise ValueError("生成内容为空")

        # 解析生成的JSON内容
        try:
            content = content[content.index("{") : content.rindex("}") + 1]
            result: dict = json.loads(content)
        except Exception as err:
            raise ValueError("解析生成内容失败") from err

        # 添加元数据
        metadata = {
            "id": str(uuid.uuid4()),
            "title": result.get("title", theme),
            "scenario_type": scenario_type,
            "description": result.get("description", ""),
            "background": result.get("background", ""),
            "subject": subject,
            "grade": grade,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        return metadata, result
