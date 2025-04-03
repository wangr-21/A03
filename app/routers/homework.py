import uuid
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import select

from ..constant import UPLOAD_DIR
from ..db import DBSession, HomeworkInfo, StudentInfo
from ..services import fleep
from ..services.homework import generate_homework_feedback
from ._depends import StudentFromId

router = APIRouter(prefix="/homework", tags=["homework"])

HOMEWORK_UPLOAD_DIR = UPLOAD_DIR / "homeworks"
HOMEWORK_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


async def save_homework_image(file: UploadFile) -> Path:
    """保存上传的作业图片并返回相对路径"""
    # 检查文件格式
    info = fleep.get(head := await file.read(256))
    if not info.mime or not any("image" in mime for mime in info.mime):
        raise HTTPException(status_code=400, detail="文件格式不正确")

    # 生成唯一文件名
    filename = f"{uuid.uuid4()}.{info.extension[0]}"
    file_path = HOMEWORK_UPLOAD_DIR / filename
    file_path.write_bytes(head + await file.read())
    return file_path.relative_to(Path.cwd())


class HomeworkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    student_id: str = Field(description="学生学号")
    homework_order: int = Field(description="作业次序")
    # homework_image_path: str = Field(description="作业图片路径")
    score: float | None = Field(default=None, description="作业评分")
    comment: str | None = Field(default=None, description="作业评语")


@router.post("/", response_model=HomeworkResponse)
async def create_homework(
    db: DBSession,
    student_id: str,
    homework_order: int,
    homework_file: UploadFile = File(),
):
    """上传学生作业"""

    # 检查学生是否存在
    student = await db.scalar(
        select(StudentInfo).filter(StudentInfo.student_id == student_id)
    )
    if not student:
        raise HTTPException(status_code=404, detail="未找到该学生，请先添加学生信息")

    # 检查是否已存在该学生的该次作业
    stmt = select(HomeworkInfo).filter(
        HomeworkInfo.student_id == student_id,
        HomeworkInfo.homework_order == homework_order,
    )
    if await db.scalar(stmt):
        raise HTTPException(
            status_code=409,
            detail=f"该学生的第 {homework_order} 次作业已存在",
        )

    # 保存作业图片
    image_path = await save_homework_image(homework_file)

    # 使用AI服务生成评分和评语
    score, comment = await generate_homework_feedback(image_path)

    # 创建作业记录
    homework = HomeworkInfo(
        student_id=student_id,
        homework_order=homework_order,
        homework_image_path=image_path.as_posix(),
        score=score,
        comment=comment,
    )

    db.add(homework)
    await db.commit()
    await db.refresh(homework)
    return homework


@router.put("/{student_id}/{homework_order}", response_model=HomeworkResponse)
async def update_homework(
    db: DBSession,
    student_id: str,
    homework_order: int,
    homework_file: UploadFile | None = File(None),
):
    """更新学生作业"""
    if homework_file is None:
        raise HTTPException(status_code=400, detail="未上传新文件")

    stmt = select(HomeworkInfo).filter(
        HomeworkInfo.student_id == student_id,
        HomeworkInfo.homework_order == homework_order,
    )

    if not (homework := await db.scalar(stmt)):
        raise HTTPException(status_code=404, detail="未找到该作业记录")

    # 删除旧文件
    (Path.cwd() / homework.homework_image_path).unlink(missing_ok=True)

    # 保存新文件
    image_path = await save_homework_image(homework_file)
    homework.homework_image_path = image_path.as_posix()

    # 重新生成评分和评语
    homework.score, homework.comment = await generate_homework_feedback(image_path)
    await db.commit()
    await db.refresh(homework)
    return homework


@router.get("/{student_id}", response_model=list[HomeworkResponse])
async def get_student_homeworks(db: DBSession, student: StudentFromId):
    """
    获取指定学生的所有作业信息
    """

    await db.refresh(student, ["homeworks"])
    return sorted(student.homeworks, key=lambda hw: hw.homework_order)


@router.get("/{student_id}/{homework_order}", response_model=HomeworkResponse)
async def get_student_homework_by_order(
    db: DBSession,
    student_id: str,
    homework_order: int,
):
    """
    获取指定学生的特定次序作业信息
    """

    stmt = select(HomeworkInfo).filter(
        HomeworkInfo.student_id == student_id,
        HomeworkInfo.homework_order == homework_order,
    )

    if not (homework := await db.scalar(stmt)):
        raise HTTPException(
            status_code=404,
            detail=f"未找到学号为 {student_id} 的学生的第 {homework_order} 次作业",
        )

    return homework
