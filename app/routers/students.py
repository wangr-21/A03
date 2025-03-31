from collections.abc import Iterable
from typing import Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, field_validator
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from ..db import DBSession, StudentInfo
from ._depends import StudentFromId
from .homework import HomeworkResponse

router = APIRouter(prefix="/students", tags=["students"])


class StudentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    student_id: str
    student_name: str
    gender: Literal["男", "女"]
    homeworks: list[HomeworkResponse] = []

    @field_validator("homeworks", mode="after")
    @classmethod
    def sort_homeworks(cls, v: Iterable[HomeworkResponse]) -> list[HomeworkResponse]:
        return sorted(v, key=lambda hw: hw.homework_order)


@router.get("/", response_model=list[StudentResponse])
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
    students = (await db.scalars(stmt)).all()
    for student in students:
        await db.refresh(student, ["homeworks"])

    return students


class CreateStudentRequest(BaseModel):
    student_id: str
    student_name: str
    gender: Literal["男", "女"]


@router.post("/", response_model=StudentResponse)
async def create_student(db: DBSession, request: CreateStudentRequest):
    """创建新的学生记录"""
    try:
        data = request.model_dump()
        db.add(StudentInfo(**data))
        await db.commit()
    except IntegrityError as e:
        raise HTTPException(status_code=409, detail="学号已存在，请使用其他学号") from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"添加学生信息失败: {e!s}") from e
    else:
        return data


@router.get("/{student_id}", response_model=StudentResponse)
async def get_student(db: DBSession, student: StudentFromId):
    """获取指定学生的信息及其所有作业信息"""
    await db.refresh(student, ["homeworks"])
    return student


@router.delete("/{student_id}", response_model=None)
async def delete_student(db: DBSession, student: StudentFromId):
    """删除学生信息及其关联的所有作业"""
    try:
        # 由于设置了级联删除，删除学生时会自动删除其所有作业
        await db.delete(student)
        await db.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除失败: {e!s}") from e
