from typing import Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, field_validator
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from ..db import DBSession, HomeworkInfo, StudentInfo

router = APIRouter(tags=["students"])


class HomeworkResp(BaseModel):
    student_id: str
    homework_order: int
    homework_image_path: str
    score: float | None = None
    comment: str | None = None

    class Config:
        from_attributes = True


class StudentResp(BaseModel):
    student_id: str
    student_name: str
    gender: str
    homeworks: list[HomeworkResp] = []

    @field_validator("student_id")
    def student_id_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("学生学号不能为空")
        return v

    @field_validator("student_name")
    def student_name_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("学生姓名不能为空")
        return v

    @field_validator("gender")
    def gender_valid(cls, v):
        if v not in ["男", "女"]:
            raise ValueError('性别必须是"男"或"女"')
        return v

    class Config:
        from_attributes = True


@router.get("/students", response_model=list[StudentResp])
async def get_students(
    db: DBSession,
    student_name: str | None = None,
    gender: str | None = None,
):
    """
    根据姓名和性别筛选学生及其作业信息
    作业按照次序升序排序展示
    """

    stmt = select(StudentInfo)
    if student_name:
        stmt = stmt.filter(StudentInfo.student_name.like(f"%{student_name}%"))
    if gender:
        stmt = stmt.filter(StudentInfo.gender == gender)

    # 获取符合条件的学生
    students = (await db.execute(stmt)).scalars().all()

    result = []
    for student in students:
        item: dict[str, object] = {
            "student_id": student.student_id,
            "student_name": student.student_name,
            "gender": student.gender,
        }
        stmt = select(HomeworkInfo).filter(
            HomeworkInfo.student_id == student.student_id
        )
        homeworks = (await db.execute(stmt)).scalars().all()
        item["homeworks"] = sorted(homeworks, key=lambda hw: hw.homework_order)
        result.append(item)

    return result


class CreateStudentRequest(BaseModel):
    student_id: str
    student_name: str
    gender: Literal["男", "女"]


@router.post("/students")
async def create_student(db: DBSession, request: CreateStudentRequest):
    """创建新的学生记录"""
    try:
        student = StudentInfo(
            student_id=request.student_id,
            student_name=request.student_name,
            gender=request.gender,
        )
        db.add(student)
        await db.commit()
        return {"message": "学生信息添加成功", "student_id": request.student_id}

    except IntegrityError:
        raise HTTPException(status_code=409, detail="学号已存在，请使用其他学号")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"添加学生信息失败: {str(e)}")


@router.delete("/students/{student_id}")
async def delete_student(db: DBSession, student_id: str):
    """删除学生信息及其关联的所有作业"""
    stmt = select(StudentInfo).filter(StudentInfo.student_id == student_id)
    if not (student := (await db.execute(stmt)).scalar()):
        raise HTTPException(status_code=404, detail="未找到该学生")

    try:
        # 由于设置了级联删除，删除学生时会自动删除其所有作业
        await db.delete(student)
        await db.commit()
        return {"message": "学生信息及相关作业已成功删除"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除失败: {str(e)}")
