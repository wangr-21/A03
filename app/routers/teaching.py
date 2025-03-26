import asyncio

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ..services.teaching_plan import TeachingPlanGenerator

router = APIRouter()
teaching_plan_cache: dict[int, str] = {}


class GenerateTeachingPlanRequest(BaseModel):
    grade: str
    images: list[str] = Field(description="Base64编码的图片列表")


@router.post("/teaching/generate_plan")
async def generate_teaching_plan(request: GenerateTeachingPlanRequest):
    plan = await TeachingPlanGenerator().generate(request.grade, request.images)
    plan_id = hash(plan)
    teaching_plan_cache[plan_id] = plan
    asyncio.get_event_loop().call_later(3600, teaching_plan_cache.pop, plan_id)
    return {"plan": plan, "plan_id": plan_id}


@router.get("/teaching/plan_document/{plan_id}")
async def get_teaching_plan_document(plan_id: int):
    plan = teaching_plan_cache.get(plan_id)
    if plan is None:
        raise HTTPException(status_code=404, detail="未找到该教案")

    document = await TeachingPlanGenerator().convert(plan)
    return document
