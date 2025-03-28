import asyncio

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from ..services.teaching_plan import TeachingPlanGenerator

router = APIRouter(prefix="/teaching", tags=["teaching"])
teaching_plan_cache: dict[str, str] = {}


class GenerateTeachingPlanResponse(BaseModel):
    plan: str = Field(description="生成的教案")
    plan_id: str = Field(description="教案 ID")


@router.post("/generate_plan", response_model=GenerateTeachingPlanResponse)
async def generate_teaching_plan(
    grade: str = Form(description="年级"),
    images: list[UploadFile] = File(description="教材图片文件"),
):
    plan = await TeachingPlanGenerator().generate(
        grade, [await img.read() for img in images]
    )
    plan_id = hex(hash(plan))[2:]
    teaching_plan_cache[plan_id] = plan
    asyncio.get_event_loop().call_later(3600, teaching_plan_cache.pop, plan_id)
    return {"plan": plan, "plan_id": plan_id}


@router.get("/plan_document/{plan_id}", response_class=FileResponse)
async def get_teaching_plan_document(plan_id: str) -> FileResponse:
    plan = teaching_plan_cache.get(plan_id)
    if plan is None:
        raise HTTPException(status_code=404, detail="未找到该教案")

    document = await TeachingPlanGenerator().convert(plan)
    asyncio.get_event_loop().call_later(3600, lambda: document.unlink(missing_ok=True))
    return FileResponse(
        path=str(document.absolute()),
        filename=f"教案_{plan_id}.docx",
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )
