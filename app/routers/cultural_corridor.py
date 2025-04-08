import json
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field, field_validator
from sqlalchemy import and_, select

from ..db import CrossDisciplineCase, DBSession, TraditionalStory
from ..services.cultural_corridor import CulturalCorridorService

router = APIRouter(prefix="/cultural-corridor", tags=["cultural-corridor"])


class StoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str = Field(description="故事ID")
    title: str = Field(description="故事标题")
    dynasty: str | None = Field(default=None, description="朝代")
    period: str | None = Field(default=None, description="时期/年代")
    theme: str = Field(description="主题分类")
    content: str = Field(description="故事内容")
    moral: str | None = Field(default=None, description="寓意或教育意义")
    reference: str | None = Field(default=None, description="参考来源")
    created_at: str = Field(description="创建时间")


class CaseResource(BaseModel):
    type: str = Field(description="资源类型")
    title: str = Field(description="资源标题")
    url: str | None = Field(default=None, description="资源链接")
    description: str | None = Field(default=None, description="资源描述")


class CaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str = Field(description="案例ID")
    title: str = Field(description="案例标题")
    story_id: str | None = Field(default=None, description="关联的传统故事ID")
    main_discipline: str = Field(description="主要学科")
    related_disciplines: str = Field(description="相关学科，以逗号分隔")
    suitable_grades: str = Field(description="适用年级范围")
    content: str = Field(description="案例内容")
    teaching_objectives: str = Field(description="教学目标")
    implementation_suggestions: str | None = Field(default=None, description="实施建议")
    resources: list[CaseResource] | None = Field(
        default=None, description="相关资源链接"
    )
    created_at: str = Field(description="创建时间")

    @field_validator("resources", mode="before")
    @classmethod
    def validate_resources(cls, v: Any) -> list[CaseResource]:
        """验证资源格式"""
        if not isinstance(v, list):
            try:
                v = json.loads(v)
            except Exception:
                v = []
        return v


class DynastyInfo(BaseModel):
    name: str = Field(description="朝代名称")
    period: str = Field(description="时间范围")
    subdynasties: list["DynastyInfo"] = Field(default=[], description="子朝代")


class ThemeCategory(BaseModel):
    name: str = Field(description="主题类别名称")
    subcategories: list[str] = Field(description="子类别列表")


class DisciplineCategory(BaseModel):
    name: str = Field(description="学科名称")
    subcategories: list[str] = Field(description="子类别列表")


# 递归引用
DynastyInfo.model_rebuild()


# API端点
@router.get("/dynasties", response_model=list[DynastyInfo])
async def list_dynasties():
    """获取中国朝代列表（按时间顺序）"""
    return CulturalCorridorService.get_dynasty_list()


@router.get("/themes", response_model=list[ThemeCategory])
async def list_themes():
    """获取传统故事主题分类"""
    return CulturalCorridorService.get_theme_categories()


@router.get("/disciplines", response_model=list[DisciplineCategory])
async def list_disciplines():
    """获取学科分类"""
    return CulturalCorridorService.get_discipline_categories()


class GenerateStoryRequest(BaseModel):
    dynasty: str | None = Field(default=None, description="朝代")
    theme: str = Field(description="主题")
    keywords: list[str] = Field(default=[], description="关键词列表")


@router.post("/stories", response_model=StoryResponse)
async def generate_story(request: GenerateStoryRequest, db: DBSession):
    """生成传统故事"""
    try:
        story_data = await CulturalCorridorService().generate_traditional_story(
            request.dynasty,
            request.theme,
            request.keywords,
        )

        # 保存到数据库
        story = TraditionalStory(**story_data)
        db.add(story)
        await db.commit()
        return story_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"故事生成失败: {e}") from e


@router.get("/stories", response_model=list[StoryResponse])
async def list_stories(
    db: DBSession,
    dynasty: str | None = None,
    theme: str | None = None,
    keyword: str | None = None,
):
    """查询传统故事列表"""
    query = select(TraditionalStory)
    if dynasty:
        query = query.filter(TraditionalStory.dynasty == dynasty)
    if theme:
        query = query.filter(TraditionalStory.theme == theme)
    if keyword:
        query = query.filter(
            TraditionalStory.title.contains(keyword)
            | TraditionalStory.content.contains(keyword)
        )

    try:
        return (await db.scalars(query)).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询失败: {e}") from e


@router.get("/stories/{story_id}", response_model=StoryResponse)
async def get_story(story_id: str, db: DBSession):
    """获取传统故事详情"""
    story = await db.get(TraditionalStory, story_id)

    if not story:
        raise HTTPException(status_code=404, detail="故事不存在")

    return story


class GenerateCaseRequest(BaseModel):
    story_id: str | None = Field(default=None, description="关联的传统故事ID")
    main_discipline: str = Field(description="主要学科")
    related_disciplines: list[str] = Field(description="相关学科列表")
    suitable_grades: str = Field(description="适用年级范围")


@router.post("/cases", response_model=CaseResponse)
async def generate_case(request: GenerateCaseRequest, db: DBSession):
    """生成跨学科延展案例"""
    try:
        # 如果指定了关联故事，验证故事是否存在
        if request.story_id:
            story = await db.get(TraditionalStory, request.story_id)
            if not story:
                raise HTTPException(status_code=404, detail="关联的故事不存在")

            story_context = CulturalCorridorService.format_story_context(story)
        else:
            story_context = None

        case_data = await CulturalCorridorService().generate_cross_discipline_case(
            request.story_id,
            request.main_discipline,
            request.related_disciplines,
            request.suitable_grades,
            story_context,
        )

        # 保存到数据库
        case = CrossDisciplineCase(
            id=case_data["id"],
            title=case_data["title"],
            story_id=case_data.get("story_id"),
            main_discipline=case_data["main_discipline"],
            related_disciplines=case_data["related_disciplines"],
            suitable_grades=case_data["suitable_grades"],
            content=case_data["content"],
            teaching_objectives="\n".join(case_data["teaching_objectives"]),
            implementation_suggestions=case_data.get("implementation_suggestions"),
            resources=json.dumps(case_data.get("resources", []), ensure_ascii=False),
            created_at=case_data["created_at"],
        )

        db.add(case)
        await db.commit()
        await db.refresh(case)
        return case

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"案例生成失败: {e}") from e


@router.get("/cases", response_model=list[CaseResponse])
async def list_cases(
    db: DBSession,
    story_id: str | None = None,
    main_discipline: str | None = None,
    related_discipline: str | None = None,
    suitable_grade: str | None = None,
):
    """查询跨学科案例列表"""
    try:
        # 构建查询条件
        conditions = []
        if story_id:
            conditions.append(CrossDisciplineCase.story_id == story_id)
        if main_discipline:
            conditions.append(CrossDisciplineCase.main_discipline == main_discipline)
        if related_discipline:
            conditions.append(
                CrossDisciplineCase.related_disciplines.contains(related_discipline)
            )
        if suitable_grade:
            conditions.append(
                CrossDisciplineCase.suitable_grades.contains(suitable_grade)
            )

        # 基本查询
        query = select(CrossDisciplineCase)
        if conditions:
            query = query.filter(and_(*conditions))

        # 执行查询
        return (await db.scalars(query)).all()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询失败: {e}") from e


@router.get("/cases/{case_id}", response_model=CaseResponse)
async def get_case(case_id: str, db: DBSession):
    """获取跨学科案例详情"""
    case = await db.get(CrossDisciplineCase, case_id)
    if case is None:
        raise HTTPException(status_code=404, detail="案例不存在")

    return case


@router.get("/stories/{story_id}/cases", response_model=list[CaseResponse])
async def get_story_cases(story_id: str, db: DBSession):
    """获取与特定传统故事关联的所有跨学科案例"""
    # 检查故事是否存在
    story = await db.get(TraditionalStory, story_id)
    if story is None:
        raise HTTPException(status_code=404, detail="故事不存在")

    await db.refresh(story, ["cross_discipline_cases"])
    return story.cross_discipline_cases
