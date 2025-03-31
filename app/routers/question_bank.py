import json
import uuid
from datetime import datetime

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import and_, select

from ..db import DBSession, KnowledgePoint, MistakeRecord, Question, StudentInfo
from ..services.question_bank import QuestionBankService  # , MistakeBookService

router = APIRouter(prefix="/question_bank", tags=["question_bank"])


# 请求和响应模型
class GenerateQuestionsRequest(BaseModel):
    subject: str = Field(description="学科")
    grade: str = Field(description="年级")
    question_types: list[str] = Field(description="题型列表")
    difficulty: int = Field(ge=1, le=5, description="难度等级，1-5")
    knowledge_points: list[str] = Field(description="知识点列表")
    count: int = Field(default=5, ge=1, le=20, description="生成题目数量")


class QuestionOption(BaseModel):
    key: str = Field(description="选项键，如A、B、C、D")
    value: str = Field(description="选项内容")


class QuestionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str = Field(description="题目ID")
    title: str = Field(description="题目内容")
    question_type: str = Field(description="题型")
    subject: str = Field(description="学科")
    grade: str = Field(description="年级")
    difficulty: int = Field(description="难度等级，1-5")
    answer: str = Field(description="参考答案")
    analysis: str = Field(description="详细解析")
    options: list[QuestionOption] | None = Field(default=None, description="选择题选项")
    knowledge_points: list[str] = Field(description="相关知识点")
    created_at: str = Field(description="创建时间")


class KnowledgePointNode(BaseModel):
    id: str = Field(description="知识点ID")
    name: str = Field(description="知识点名称")
    children: list["KnowledgePointNode"] | None = Field(
        default=None, description="子知识点"
    )


class AnalyzeMistakeRequest(BaseModel):
    question_id: str = Field(description="题目ID")
    student_id: str = Field(description="学生ID")
    student_answer: str = Field(description="学生答案")


class MistakeAnalysisResponse(BaseModel):
    mistake_reason: str = Field(description="错误原因分类")
    analysis: str = Field(description="详细错误分析")
    suggestion: str = Field(description="学习建议")


class MistakeRecordResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str = Field(description="错题记录ID")
    question_id: str = Field(description="题目ID")
    student_id: str = Field(description="学生ID")
    question: QuestionResponse | None = Field(default=None, description="题目信息")
    answer: str = Field(description="学生错误答案")
    mistake_reason: str | None = Field(default=None, description="错误原因分类")
    is_resolved: bool = Field(description="是否已解决")
    resolve_times: int = Field(description="解决尝试次数")
    created_at: str = Field(description="创建时间")
    updated_at: str = Field(description="最后更新时间")


class UpdateMistakeRequest(BaseModel):
    is_resolved: bool = Field(description="是否已解决")


# 递归引用 KnowledgePointNode
KnowledgePointNode.model_rebuild()


# API端点
@router.post("/generate", response_model=list[QuestionResponse])
async def generate_questions(request: GenerateQuestionsRequest, db: DBSession):
    """生成符合条件的题目"""
    try:
        service = QuestionBankService()
        questions = await service.generate_questions(
            request.subject,
            request.grade,
            request.question_types,
            request.difficulty,
            request.knowledge_points,
            request.count,
        )

        # 保存到数据库
        for question_data in questions:
            # 解析知识点
            knowledge_point_names = question_data.pop("knowledge_points", [])
            options_json = question_data.pop("options", None)

            # 创建题目实例
            question = Question(
                id=question_data["id"],
                title=question_data["title"],
                question_type=question_data["question_type"],
                subject=question_data["subject"],
                grade=question_data["grade"],
                difficulty=question_data["difficulty"],
                answer=question_data["answer"],
                analysis=question_data.get("analysis", ""),
                options=options_json,
                created_at=question_data["created_at"],
            )

            # 关联知识点
            for kp_name in knowledge_point_names:
                # 检查知识点是否存在，不存在则创建
                query = select(KnowledgePoint).filter(
                    KnowledgePoint.name == kp_name,
                    KnowledgePoint.subject == request.subject,
                )
                result = await db.execute(query)
                knowledge_point = result.scalar_one_or_none()

                if not knowledge_point:
                    knowledge_point = KnowledgePoint(
                        id=str(uuid.uuid4()), name=kp_name, subject=request.subject
                    )
                    db.add(knowledge_point)

                question.knowledge_points.append(knowledge_point)

            db.add(question)

        await db.commit()

        # 准备返回数据
        result = []
        for q in questions:
            # 处理选项格式
            options = None
            if q.get("options"):
                if isinstance(q["options"], str):
                    try:
                        options = json.loads(q["options"])
                    except json.JSONDecodeError:
                        options = None
                else:
                    options = q["options"]

            result.append(
                {
                    "id": q["id"],
                    "title": q["title"],
                    "question_type": q["question_type"],
                    "subject": q["subject"],
                    "grade": q["grade"],
                    "difficulty": q["difficulty"],
                    "answer": q["answer"],
                    "analysis": q.get("analysis", ""),
                    "options": options,
                    "knowledge_points": q.get("knowledge_points", []),
                    "created_at": q["created_at"],
                }
            )

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"题目生成失败: {e!s}") from e


@router.get("/questions", response_model=list[QuestionResponse])
async def list_questions(
    db: DBSession,
    subject: str | None = None,
    grade: str | None = None,
    question_type: str | None = None,
    difficulty: int | None = None,
    knowledge_point: str | None = None,
):
    """查询题目列表"""
    try:
        # 构建查询条件
        query = select(Question)
        if subject:
            query.filter(Question.subject == subject)
        if grade:
            query.filter(Question.grade == grade)
        if question_type:
            query.filter(Question.question_type == question_type)
        if difficulty:
            query.filter(Question.difficulty == difficulty)

        # 知识点过滤需要单独处理
        if knowledge_point:
            kp_query = select(KnowledgePoint).filter(
                KnowledgePoint.name == knowledge_point
            )
            kp = await db.scalar(kp_query)
            if not kp:
                # 如果知识点不存在，返回空列表
                return []

            # 使用关联表过滤
            query = query.filter(
                Question.knowledge_points.any(KnowledgePoint.id == kp.id)
            )

        # 执行查询
        questions = (await db.scalars(query)).all()

        # 格式化响应
        response = []
        for q in questions:
            # 处理选项
            options = None
            if q.options:
                try:
                    options = json.loads(q.options)
                except json.JSONDecodeError:
                    options = None

            # 获取知识点名称列表
            await db.refresh(q, ["knowledge_points"])
            knowledge_point_names = [kp.name for kp in q.knowledge_points]

            response.append(
                {
                    "id": q.id,
                    "title": q.title,
                    "question_type": q.question_type,
                    "subject": q.subject,
                    "grade": q.grade,
                    "difficulty": q.difficulty,
                    "answer": q.answer,
                    "analysis": q.analysis or "",
                    "options": options,
                    "knowledge_points": knowledge_point_names,
                    "created_at": q.created_at,
                }
            )

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询失败: {e!s}") from e


@router.get("/questions/{question_id}", response_model=QuestionResponse)
async def get_question(question_id: str, db: DBSession):
    """获取题目详情"""
    query = select(Question).filter(Question.id == question_id)
    result = await db.execute(query)
    question = result.scalar_one_or_none()

    if not question:
        raise HTTPException(status_code=404, detail="题目不存在")

    # 处理选项
    options = None
    if question.options:
        try:
            options = json.loads(question.options)
        except json.JSONDecodeError:
            options = None

    # 获取知识点名称列表
    await db.refresh(question, ["knowledge_points"])
    knowledge_point_names = [kp.name for kp in question.knowledge_points]

    return {
        "id": question.id,
        "title": question.title,
        "question_type": question.question_type,
        "subject": question.subject,
        "grade": question.grade,
        "difficulty": question.difficulty,
        "answer": question.answer,
        "analysis": question.analysis or "",
        "options": options,
        "knowledge_points": knowledge_point_names,
        "created_at": question.created_at,
    }


@router.get("/knowledge_points", response_model=list[KnowledgePointNode])
async def get_knowledge_tree(subject: str):
    """获取知识点树结构"""
    try:
        return await QuestionBankService().generate_knowledge_tree(subject)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取知识点树失败: {e!s}") from e


@router.post("/mistakes/analyze", response_model=MistakeAnalysisResponse)
async def analyze_mistake(request: AnalyzeMistakeRequest, db: DBSession):
    """分析错题"""
    # 查询题目
    query = select(Question).filter(Question.id == request.question_id)
    question = (await db.execute(query)).scalar_one_or_none()

    if not question:
        raise HTTPException(status_code=404, detail="题目不存在")

    # 查询学生
    stmt = select(StudentInfo).filter(StudentInfo.student_id == request.student_id)
    student = (await db.execute(stmt)).scalar_one_or_none()

    if not student:
        raise HTTPException(status_code=404, detail="学生不存在")

    try:
        # 转换题目为字典格式
        question_dict = {
            "id": question.id,
            "title": question.title,
            "question_type": question.question_type,
            "subject": question.subject,
            "grade": question.grade,
            "difficulty": question.difficulty,
            "answer": question.answer,
            "analysis": question.analysis or "",
            "options": question.options,
        }

        # 分析错误
        service = QuestionBankService()
        analysis_result = await service.analyze_mistake(
            question_dict, request.student_answer
        )

        # 创建或更新错题记录
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 查询是否已存在错题记录
        mistake_query = select(MistakeRecord).filter(
            MistakeRecord.student_id == request.student_id,
            MistakeRecord.question_id == request.question_id,
        )
        mistake = await db.scalar(mistake_query)

        if mistake:
            # 更新现有记录
            mistake.answer = request.student_answer
            mistake.mistake_reason = analysis_result["mistake_reason"]
            mistake.updated_at = now
        else:
            # 创建新记录
            mistake = MistakeRecord(
                id=str(uuid.uuid4()),
                question_id=request.question_id,
                student_id=request.student_id,
                answer=request.student_answer,
                mistake_reason=analysis_result["mistake_reason"],
                is_resolved=False,
                resolve_times=0,
                created_at=now,
                updated_at=now,
            )
            db.add(mistake)

        await db.commit()
        return analysis_result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"错题分析失败: {e!s}") from e


@router.get("/mistakes", response_model=list[MistakeRecordResponse])
async def list_mistakes(
    db: DBSession,
    student_id: str | None = None,
    subject: str | None = None,
    is_resolved: bool | None = None,
):
    """获取错题列表"""
    try:
        # 构建查询条件
        conditions = []
        if student_id:
            conditions.append(MistakeRecord.student_id == student_id)
        if is_resolved is not None:
            conditions.append(MistakeRecord.is_resolved == is_resolved)

        # 基本查询
        query = select(MistakeRecord)
        if conditions:
            query = query.filter(and_(*conditions))

        # 执行查询
        mistakes = (await db.scalars(query)).all()

        # 格式化响应
        response = []
        for m in mistakes:
            # 查询相关题目
            question_query = select(Question).filter(Question.id == m.question_id)
            question_result = await db.execute(question_query)
            question = question_result.scalar_one_or_none()

            # 如果指定了学科过滤且题目不属于该学科，则跳过
            if subject and question and question.subject != subject:
                continue

            # 题目字典
            question_dict = None
            if question:
                options = None
                if question.options:
                    try:
                        options = json.loads(question.options)
                    except json.JSONDecodeError:
                        options = None

                question_dict = {
                    "id": question.id,
                    "title": question.title,
                    "question_type": question.question_type,
                    "subject": question.subject,
                    "grade": question.grade,
                    "difficulty": question.difficulty,
                    "answer": question.answer,
                    "analysis": question.analysis or "",
                    "options": options,
                }

            response.append(
                {
                    "id": m.id,
                    "question_id": m.question_id,
                    "student_id": m.student_id,
                    "question": question_dict,
                    "answer": m.answer,
                    "mistake_reason": m.mistake_reason,
                    "is_resolved": m.is_resolved,
                    "resolve_times": m.resolve_times,
                    "created_at": m.created_at,
                    "updated_at": m.updated_at,
                }
            )

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询失败: {e!s}") from e


@router.patch("/mistakes/{mistake_id}", response_model=MistakeRecordResponse)
async def update_mistake(mistake_id: str, request: UpdateMistakeRequest, db: DBSession):
    """更新错题状态"""
    mistake = await db.get(MistakeRecord, mistake_id)

    if not mistake:
        raise HTTPException(status_code=404, detail="错题记录不存在")

    # 更新状态
    mistake.is_resolved = request.is_resolved
    if request.is_resolved:
        mistake.resolve_times += 1
    mistake.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    await db.commit()
    await db.refresh(mistake)
    await db.refresh(mistake, ["question"])
    return mistake
