from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..services.ai_service import AIService

router = APIRouter()
ai_service = AIService()


class GenerateTeachingPlanRequest(BaseModel):
    subject: str
    grade: str
    topic: str


@router.post("/teaching/generate-plan")
async def generate_teaching_plan(request: GenerateTeachingPlanRequest):
    try:
        plan = ai_service.generate_teaching_plan(
            subject=request.subject,
            grade=request.grade,
            topic=request.topic,
        )
        return {"success": True, "data": plan}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class GenerateTeachingImageRequest(BaseModel):
    prompt: str


@router.post("/teaching/generate-image")
async def generate_teaching_image(request: GenerateTeachingImageRequest):
    try:
        image = ai_service.generate_teaching_image(request.prompt)
        return {"success": True, "data": image}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
