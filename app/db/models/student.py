from typing import Literal

from sqlalchemy import Double, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..config import Base


class StudentInfo(Base):
    __tablename__ = "student_info"

    student_id: Mapped[str] = mapped_column(
        String(20),
        primary_key=True,
        comment="学生学号（主键）",
    )
    student_name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="学生姓名",
    )
    gender: Mapped[Literal["男", "女"]] = mapped_column(
        Enum("男", "女", name="student_info_gender_enum"),
        nullable=False,
        comment="性别",
    )

    # 建立与作业信息表的关系，并在删除学生时级联删除其所有作业
    homeworks: Mapped[list["HomeworkInfo"]] = relationship(
        "HomeworkInfo",
        back_populates="student",
        cascade="all, delete-orphan",
    )


class HomeworkInfo(Base):
    __tablename__ = "homework_info"

    student_id: Mapped[str] = mapped_column(
        String(20),
        ForeignKey(StudentInfo.student_id, ondelete="CASCADE"),
        primary_key=True,
        comment="学生学号（外键）",
    )
    homework_order: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        comment="作业次序（数字，如0、1、2等）",
    )
    homework_image_path: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="作业图片存储路径",
    )
    score: Mapped[float] = mapped_column(
        Double,
        nullable=True,
        comment="得分（后台评分，允许为空）",
    )
    comment: Mapped[str] = mapped_column(
        Text,
        nullable=True,
        comment="评语（后台评语，允许为空）",
    )

    # 建立与学生信息表的关系
    student: Mapped[list["StudentInfo"]] = relationship(
        "StudentInfo",
        back_populates="homeworks",
    )

    __table_args__ = {"comment": "学生作业信息表"}
