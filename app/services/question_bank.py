import json
import uuid
import random
from datetime import datetime
# from typing import List, Optional

from .utils import CompletionMessage, get_openai_client, run_sync
from ..constant import ASSETS_DIR

ASSETS_ROOT = ASSETS_DIR / "question_bank"
PROMPT_GENERATE = ASSETS_ROOT / "generate.md"
PROMPT_ANALYZE_MISTAKE = ASSETS_ROOT / "analyze_mistake.md"


class QuestionBankService:
    """题库服务"""

    def __init__(self) -> None:
        self.client, self.model_name = get_openai_client()

    async def generate_questions(
        self,
        subject: str,
        grade: str,
        question_types: list[str],
        difficulty: int,
        knowledge_points: list[str],
        count: int = 5,
    ) -> list[dict]:
        """生成题目

        Args:
            subject: 学科
            grade: 年级
            question_types: 题型列表，如['单选题', '多选题', '填空题']
            difficulty: 难度等级，1-5
            knowledge_points: 知识点列表
            count: 生成题目数量

        Returns:
            List[dict]: 生成的题目列表
        """

        # 填充模板
        prompt = (
            PROMPT_GENERATE.read_text(encoding="utf-8")
            .replace("{{subject}}", subject)
            .replace("{{grade}}", grade)
            .replace("{{question_types}}", ", ".join(question_types))
            .replace("{{difficulty}}", str(difficulty))
            .replace("{{knowledge_points}}", ", ".join(knowledge_points))
            .replace("{{count}}", str(count))
        )

        # 调用OpenAI API生成题目
        response = await run_sync(self.client.chat.completions.create)(
            model=self.model_name,
            messages=[CompletionMessage().text(prompt).build()],
            temperature=0.7,
        )

        content = response.choices[0].message.content

        if not content:
            raise ValueError("题目生成失败: 返回结果为空")

        # 解析生成的JSON内容
        try:
            content = content[content.index("[") : content.rindex("]") + 1]
            questions = json.loads(content)

            # 确保是列表格式
            if not isinstance(questions, list):
                questions = [questions]

            # 补充ID和创建时间
            for q in questions:
                q["id"] = str(uuid.uuid4())
                q["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # 将选项转换为JSON字符串
                if "options" in q and isinstance(q["options"], list):
                    q["options"] = json.dumps(q["options"], ensure_ascii=False)

        except json.JSONDecodeError:
            # 如果返回内容不是标准JSON，返回错误
            raise ValueError("题目生成失败，无法解析返回结果")

        return questions

    async def analyze_mistake(self, question: dict, student_answer: str) -> dict:
        """分析学生错误答案，提供错误原因分析

        Args:
            question: 题目信息
            student_answer: 学生的答案

        Returns:
            dict: 错误分析结果
        """

        # 准备题目信息
        question_info = f"题目：{question['title']}\n"
        if "options" in question and question["options"]:
            options = (
                json.loads(question["options"])
                if isinstance(question["options"], str)
                else question["options"]
            )
            options_text = "\n".join(
                [f"{opt['key']}. {opt['value']}" for opt in options]
            )
            question_info += f"选项：\n{options_text}\n"
        question_info += f"正确答案：{question['answer']}\n"
        question_info += f"学生答案：{student_answer}\n"

        # 填充模板
        prompt = PROMPT_ANALYZE_MISTAKE.read_text("utf-8").replace(
            "{{question_info}}", question_info
        )

        # 调用OpenAI API分析错误
        response = await run_sync(self.client.chat.completions.create)(
            model=self.model_name,
            messages=[CompletionMessage().text(prompt).build()],
            temperature=0.5,
        )

        content = response.choices[0].message.content

        if not content:
            raise ValueError("错误分析失败: 返回结果为空")

        # 解析生成的JSON内容
        try:
            content = content[content.index("{") : content.rindex("}") + 1]
            result = json.loads(content)
        except json.JSONDecodeError:
            raise ValueError("错误分析失败，无法解析返回结果")

        return result

    async def generate_knowledge_tree(self, subject: str) -> list[dict]:
        """生成指定学科的知识点树结构

        Args:
            subject: 学科名称

        Returns:
            List[dict]: 知识点树结构
        """
        # 这里应该是从数据库中查询知识点，并构建树状结构
        # 简化版本，通过硬编码返回一些常见知识点

        if subject == "语文":
            return [
                {
                    "id": str(uuid.uuid4()),
                    "name": "文学常识",
                    "children": [
                        {"id": str(uuid.uuid4()), "name": "文学体裁"},
                        {"id": str(uuid.uuid4()), "name": "古代作家"},
                        {"id": str(uuid.uuid4()), "name": "现代作家"},
                    ],
                },
                {
                    "id": str(uuid.uuid4()),
                    "name": "阅读理解",
                    "children": [
                        {"id": str(uuid.uuid4()), "name": "记叙文阅读"},
                        {"id": str(uuid.uuid4()), "name": "说明文阅读"},
                        {"id": str(uuid.uuid4()), "name": "议论文阅读"},
                        {"id": str(uuid.uuid4()), "name": "诗歌鉴赏"},
                    ],
                },
            ]
        elif subject == "数学":
            return [
                {
                    "id": str(uuid.uuid4()),
                    "name": "数与代数",
                    "children": [
                        {"id": str(uuid.uuid4()), "name": "整数与分数"},
                        {"id": str(uuid.uuid4()), "name": "方程与不等式"},
                        {"id": str(uuid.uuid4()), "name": "函数"},
                    ],
                },
                {
                    "id": str(uuid.uuid4()),
                    "name": "空间与图形",
                    "children": [
                        {"id": str(uuid.uuid4()), "name": "平面图形"},
                        {"id": str(uuid.uuid4()), "name": "立体图形"},
                        {"id": str(uuid.uuid4()), "name": "图形的变换"},
                    ],
                },
            ]
        else:
            # 返回一些通用的知识点结构
            return [
                {
                    "id": str(uuid.uuid4()),
                    "name": f"{subject}基础知识",
                    "children": [
                        {"id": str(uuid.uuid4()), "name": "基本概念"},
                        {"id": str(uuid.uuid4()), "name": "基本方法"},
                    ],
                },
                {
                    "id": str(uuid.uuid4()),
                    "name": f"{subject}应用能力",
                    "children": [
                        {"id": str(uuid.uuid4()), "name": "能力培养"},
                        {"id": str(uuid.uuid4()), "name": "实践应用"},
                    ],
                },
            ]


class MistakeBookService:
    """错题本服务"""

    async def add_mistake(self, student_id: str, question_id: str, answer: str) -> dict:
        """添加错题记录

        Args:
            student_id: 学生ID
            question_id: 题目ID
            answer: 学生错误答案

        Returns:
            dict: 错题记录信息
        """
        # 生成唯一ID
        mistake_id = str(uuid.uuid4())
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return {
            "id": mistake_id,
            "question_id": question_id,
            "student_id": student_id,
            "answer": answer,
            "mistake_reason": None,  # 待分析
            "is_resolved": False,
            "resolve_times": 0,
            "created_at": now,
            "updated_at": now,
        }

    async def update_mistake_status(self, mistake_id: str, is_resolved: bool) -> dict:
        """更新错题状态

        Args:
            mistake_id: 错题记录ID
            is_resolved: 是否已解决

        Returns:
            dict: 更新后的错题记录信息
        """
        # 实际应用中应该从数据库查询并更新
        # 这里简化处理，返回模拟数据
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return {
            "id": mistake_id,
            "is_resolved": is_resolved,
            "resolve_times": 1 if is_resolved else 0,
            "updated_at": now,
        }

    async def get_student_mistakes(
        self,
        student_id: str,
        subject: str | None = None,
        is_resolved: bool | None = None,
    ) -> list[dict]:
        """获取学生的错题列表

        Args:
            student_id: 学生ID
            subject: 过滤学科
            is_resolved: 过滤状态

        Returns:
            List[dict]: 错题记录列表
        """
        # 实际应用中应该从数据库查询
        # 这里简化处理，返回模拟数据

        # 模拟一些随机数据
        mistakes = []
        subjects = ["语文", "数学", "英语"] if not subject else [subject]
        question_types = ["单选题", "多选题", "填空题", "简答题"]

        for i in range(5):
            subj = random.choice(subjects)
            q_type = random.choice(question_types)
            resolved = (
                is_resolved if is_resolved is not None else random.choice([True, False])
            )

            mistake = {
                "id": str(uuid.uuid4()),
                "question_id": str(uuid.uuid4()),
                "student_id": student_id,
                "question": {
                    "title": f"{subj}测试题目 {i + 1}",
                    "question_type": q_type,
                    "subject": subj,
                    "difficulty": random.randint(1, 5),
                    "answer": "标准答案",
                },
                "answer": "学生错误答案",
                "mistake_reason": "概念理解错误",
                "is_resolved": resolved,
                "resolve_times": 1 if resolved else 0,
                "created_at": "2023-05-01 10:00:00",
                "updated_at": "2023-05-02 10:00:00",
            }
            mistakes.append(mistake)

        return mistakes
