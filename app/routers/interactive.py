import json
from typing import Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select

from ..db import DBSession, InteractiveActivity, ScenarioSimulation
from ..services.interactive import InteractiveGenerator

router = APIRouter(prefix="/interactive", tags=["interactive"])


# 请求和响应模型
class GenerateActivityRequest(BaseModel):
    activity_type: Literal["discussion", "question", "game"] = Field(
        description="活动类型"
    )
    subject: str = Field(description="学科")
    grade: str = Field(description="年级")
    topic: str = Field(description="主题")
    duration: int = Field(default=20, ge=5, le=60, description="活动时长(分钟)")


class ActivityStep(BaseModel):
    name: str = Field(description="步骤名称")
    duration: int = Field(description="步骤时长(分钟)")
    teacher_action: str = Field(description="教师行为")
    student_action: str = Field(description="学生行为")


class ActivityEvaluation(BaseModel):
    criteria: list[str] = Field(description="评价标准")
    method: str = Field(description="评价方法描述")


class ActivityResponse(BaseModel):
    # metadata
    id: str = Field(description="活动ID")
    activity_type: str = Field(description="活动类型")
    subject: str = Field(description="学科")
    grade: str = Field(description="年级")
    duration: int = Field(description="活动时长(分钟)")
    created_at: str = Field(description="创建时间")

    # content
    title: str = Field(description="活动标题")
    description: str = Field(description="活动描述")
    preparation: list[str] = Field(description="活动准备")
    objectives: list[str] = Field(description="活动目标")
    steps: list[ActivityStep] = Field(description="活动步骤")
    evaluation: ActivityEvaluation = Field(description="活动评价")
    extensions: list[str] = Field(description="活动延伸")

    @classmethod
    def from_orm(cls, obj: InteractiveActivity):
        metadata = {
            "id": obj.id,
            "activity_type": obj.activity_type,
            "subject": obj.subject,
            "grade": obj.grade,
            "duration": obj.duration,
            "created_at": obj.created_at,
        }
        return cls.model_validate(metadata | json.loads(obj.content))


class GenerateScenarioRequest(BaseModel):
    scenario_type: Literal["historical", "literary", "scientific"] = Field(
        description="场景类型"
    )
    subject: str = Field(description="学科")
    grade: str = Field(description="年级")
    theme: str = Field(description="主题")


class ScenarioScene(BaseModel):
    name: str = Field(description="场景名称")
    description: str = Field(description="场景描述")
    visual_elements: list[str] = Field(description="视觉元素列表")
    audio_elements: list[str] = Field(description="音频元素列表")


class ScenarioCharacter(BaseModel):
    name: str = Field(description="角色名称")
    role: str = Field(description="角色身份")
    description: str = Field(description="角色描述")


class ScenarioInteractiveElement(BaseModel):
    type: str = Field(description="交互元素类型")
    description: str = Field(description="交互元素描述")
    options: list[str] = Field(description="可选操作列表")
    outcomes: list[str] = Field(description="对应结果列表")


class ScenarioTeacherGuide(BaseModel):
    setup: list[str] = Field(description="场景设置指南")
    facilitation_tips: list[str] = Field(description="引导技巧")
    reflection_questions: list[str] = Field(description="反思问题")


class ScenarioResponse(BaseModel):
    # metadata
    id: str = Field(description="场景ID")
    scenario_type: str = Field(description="场景类型")
    subject: str = Field(description="学科")
    grade: str = Field(description="年级")
    created_at: str = Field(description="创建时间")

    # content
    title: str = Field(description="场景标题")
    background: str = Field(description="背景知识")
    educational_value: str = Field(description="教育价值")
    scenes: list[ScenarioScene] = Field(description="场景列表")
    characters: list[ScenarioCharacter] = Field(description="角色列表")
    interactive_elements: list[ScenarioInteractiveElement] = Field(
        description="交互元素列表"
    )
    teacher_guide: ScenarioTeacherGuide = Field(description="教师指南")

    @classmethod
    def from_orm(cls, obj: ScenarioSimulation):
        metadata = {
            "id": obj.id,
            "scenario_type": obj.scenario_type,
            "subject": obj.subject,
            "grade": obj.grade,
            "created_at": obj.created_at,
        }
        return cls.model_validate(metadata | json.loads(obj.content))


# API端点
@router.post("/activities", response_model=ActivityResponse)
async def generate_activity(request: GenerateActivityRequest, db: DBSession):
    """生成互动教学活动"""
    try:
        metadata, content = await InteractiveGenerator().generate_activity(
            request.activity_type,
            request.subject,
            request.grade,
            request.topic,
            request.duration,
        )

        # 保存到数据库
        activity = InteractiveActivity(
            **metadata,
            content=json.dumps(content, ensure_ascii=False),
        )
        db.add(activity)
        await db.commit()
        return {**metadata, **content}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"活动生成失败: {str(e)}")


@router.post("/scenarios", response_model=ScenarioResponse)
async def generate_scenario(request: GenerateScenarioRequest, db: DBSession):
    """生成情景模拟场景"""
    try:
        metadata, content = await InteractiveGenerator().generate_scenario(
            request.scenario_type,
            request.subject,
            request.grade,
            request.theme,
        )

        # 保存到数据库
        scenario = ScenarioSimulation(
            **metadata,
            content=json.dumps(content, ensure_ascii=False),
        )
        db.add(scenario)
        await db.commit()
        return {**metadata, **content}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"场景生成失败: {str(e)}")


@router.get("/activities", response_model=list[ActivityResponse])
async def list_activities(
    db: DBSession,
    subject: str | None = None,
    grade: str | None = None,
    activity_type: str | None = None,
):
    """查询互动教学活动列表"""
    query = select(InteractiveActivity)

    if subject:
        query = query.filter(InteractiveActivity.subject == subject)
    if grade:
        query = query.filter(InteractiveActivity.grade == grade)
    if activity_type:
        query = query.filter(InteractiveActivity.activity_type == activity_type)

    result = await db.execute(query)
    activities = result.scalars().all()

    return [ActivityResponse.from_orm(activity) for activity in activities]


@router.get("/activities/{activity_id}", response_model=ActivityResponse)
async def get_activity(activity_id: str, db: DBSession):
    """获取互动教学活动详情"""
    query = select(InteractiveActivity).filter(InteractiveActivity.id == activity_id)
    result = await db.execute(query)
    activity = result.scalar_one_or_none()

    if not activity:
        raise HTTPException(status_code=404, detail="活动不存在")

    return ActivityResponse.from_orm(activity)


@router.get("/scenarios", response_model=list[ScenarioResponse])
async def list_scenarios(
    db: DBSession,
    subject: str | None = None,
    grade: str | None = None,
    scenario_type: str | None = None,
):
    """查询情景模拟场景列表"""
    query = select(ScenarioSimulation)

    if subject:
        query = query.filter(ScenarioSimulation.subject == subject)
    if grade:
        query = query.filter(ScenarioSimulation.grade == grade)
    if scenario_type:
        query = query.filter(ScenarioSimulation.scenario_type == scenario_type)

    result = await db.execute(query)
    scenarios = result.scalars().all()

    return [ScenarioResponse.from_orm(scenario) for scenario in scenarios]


@router.get("/scenarios/{scenario_id}", response_model=ScenarioResponse)
async def get_scenario(scenario_id: str, db: DBSession):
    """获取情景模拟场景详情"""
    query = select(ScenarioSimulation).filter(ScenarioSimulation.id == scenario_id)
    result = await db.execute(query)
    scenario = result.scalar_one_or_none()

    if not scenario:
        raise HTTPException(status_code=404, detail="场景不存在")

    return ScenarioResponse.from_orm(scenario)
