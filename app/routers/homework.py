import uuid
from pathlib import Path

import fleep
from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import select

from ..constant import UPLOAD_DIR
from ..db import DBSession, HomeworkInfo, StudentInfo
from ..services.homework import generate_homework_feedback

router = APIRouter(prefix="/homework", tags=["homework"])


async def save_homework_image(file: UploadFile) -> Path:
    """保存上传的作业图片并返回相对路径"""
    # 检查文件格式
    info = fleep.get(head := await file.read(256))
    if not info.mime or not any("image" in mime for mime in info.mime):
        raise HTTPException(status_code=400, detail="文件格式不正确")

    # 生成唯一文件名
    filename = f"{uuid.uuid4()}.{info.extension[0]}"
    file_path = UPLOAD_DIR / filename
    file_path.write_bytes(head + await file.read())
    return file_path.relative_to(Path.cwd())


@router.post("/")
async def create_homework(
    db: DBSession,
    student_id: str,
    homework_order: int,
    homework_file: UploadFile = File(),
):
    """上传学生作业"""

    # 检查学生是否存在
    stmt = select(StudentInfo).filter(StudentInfo.student_id == student_id)
    student = (await db.execute(stmt)).scalar()
    if not student:
        return JSONResponse(
            status_code=404, content={"message": "未找到该学生，请先添加学生信息"}
        )

    # 检查是否已存在该学生的该次作业
    stmt = select(HomeworkInfo).filter(
        HomeworkInfo.student_id == student_id,
        HomeworkInfo.homework_order == homework_order,
    )

    if (await db.execute(stmt)).scalar():
        return JSONResponse(
            status_code=409,
            content={"message": f"该学生的第{homework_order}次作业已存在"},
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
    return {
        "message": "作业上传成功",
        "student_id": student_id,
        "homework_order": homework_order,
        "score": score,
        "comment": comment,
    }


@router.put("/{student_id}/{homework_order}")
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

    if not (homework := (await db.execute(stmt)).scalar()):
        raise HTTPException(status_code=404, detail="未找到该作业记录")

    # 删除旧文件
    old_path = Path.cwd() / homework.homework_image_path
    old_path.unlink(missing_ok=True)

    # 保存新文件
    image_path = await save_homework_image(homework_file)
    homework.homework_image_path = image_path.as_posix()

    # 重新生成评分和评语
    score, comment = await generate_homework_feedback(image_path)
    homework.score = score
    homework.comment = comment
    response = {
        "message": "作业更新成功",
        "score": score,
        "comment": comment,
    }

    await db.commit()
    return response


class HomeworkResponse(BaseModel):
    student_id: str
    homework_order: int
    homework_image_path: str
    score: float | None = None
    comment: str | None = None

    class Config:
        from_attributes = True


@router.get("/{student_id}", response_model=list[HomeworkResponse])
async def get_student_homeworks(db: DBSession, student_id: str):
    """
    获取指定学生的所有作业信息
    """
    stmt = select(StudentInfo).filter(StudentInfo.student_id == student_id)
    student = (await db.execute(stmt)).scalar()
    if not student:
        raise HTTPException(status_code=404, detail="未找到该学生")

    homework_stmt = (
        select(HomeworkInfo)
        .filter(HomeworkInfo.student_id == student_id)
        .order_by(HomeworkInfo.homework_order)
    )

    return (await db.execute(homework_stmt)).scalars().all()


@router.get(
    "/{student_id}/{homework_order}",
    response_model=HomeworkResponse,
)
async def get_student_homework_by_order(
    db: DBSession,
    student_id: str,
    homework_order: int,
):
    """
    获取指定学生的特定次序作业信息
    """
    # 直接查询特定作业
    stmt = select(HomeworkInfo).filter(
        HomeworkInfo.student_id == student_id,
        HomeworkInfo.homework_order == homework_order,
    )

    homework = (await db.execute(stmt)).scalar()

    if not homework:
        raise HTTPException(
            status_code=404,
            detail=f"未找到学号为 {student_id} 的学生的第 {homework_order} 次作业",
        )

    return homework
