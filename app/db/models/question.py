from typing import Optional

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..config import Base

# 题目与知识点多对多关联表
question_knowledge_association = Table(
    "question_knowledge_association",
    Base.metadata,
    Column("question_id", String(50), ForeignKey("questions.id")),
    Column("knowledge_point_id", String(50), ForeignKey("knowledge_points.id")),
)


class Question(Base):
    """题目模型"""

    __tablename__ = "questions"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    """题干"""
    question_type: Mapped[str] = mapped_column(String(20), nullable=False)
    """题型：单选、多选、填空、简答等"""
    subject: Mapped[str | None] = mapped_column(String(20))
    """学科"""
    grade: Mapped[str | None] = mapped_column(String(20))
    """年级"""
    difficulty: Mapped[int | None] = mapped_column(Integer)
    """难度等级：1-5"""
    answer: Mapped[str] = mapped_column(Text, nullable=False)
    """参考答案"""
    analysis: Mapped[str | None] = mapped_column(Text)
    """解析"""
    options: Mapped[str | None] = mapped_column(Text)
    """选择题选项，JSON格式"""
    created_at: Mapped[str | None] = mapped_column(String(30))
    """创建时间"""

    # 与知识点的多对多关系
    knowledge_points: Mapped[list["KnowledgePoint"]] = relationship(
        "KnowledgePoint",
        secondary=question_knowledge_association,
        back_populates="questions",
    )

    # 与错题的一对多关系
    mistake_records: Mapped[list["MistakeRecord"]] = relationship(
        "MistakeRecord",
        back_populates="question",
    )


class KnowledgePoint(Base):
    """知识点模型"""

    __tablename__ = "knowledge_points"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    """知识点名称"""
    subject: Mapped[str | None] = mapped_column(String(20))
    """所属学科"""
    parent_id: Mapped[str | None] = mapped_column(
        String(50), ForeignKey("knowledge_points.id"), nullable=True
    )
    """父知识点ID"""
    level: Mapped[int] = mapped_column(Integer, default=1)
    """知识点层级"""

    # 与题目的多对多关系
    questions: Mapped[list["Question"]] = relationship(
        "Question",
        secondary=question_knowledge_association,
        back_populates="knowledge_points",
    )

    # 自引用关系，用于树形知识点结构
    children: Mapped[list["KnowledgePoint"]] = relationship(
        "KnowledgePoint",
        back_populates="parent",
    )
    parent: Mapped[Optional["KnowledgePoint"]] = relationship(
        "KnowledgePoint",
        back_populates="children",
        remote_side=[id],
    )


class MistakeRecord(Base):
    """错题记录模型"""

    __tablename__ = "mistake_records"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    question_id: Mapped[str] = mapped_column(
        String(50), ForeignKey("questions.id"), nullable=False
    )
    student_id: Mapped[str] = mapped_column(
        String(50), ForeignKey("student_info.student_id"), nullable=False
    )
    answer: Mapped[str | None] = mapped_column(Text)
    """学生的错误答案"""
    mistake_reason: Mapped[str | None] = mapped_column(String(100))
    """错误原因分类"""
    is_resolved: Mapped[bool] = mapped_column(Boolean, default=False)
    """是否已解决"""
    resolve_times: Mapped[int] = mapped_column(Integer, default=0)
    """解决尝试次数"""
    created_at: Mapped[str | None] = mapped_column(String(30))
    """创建时间"""
    updated_at: Mapped[str | None] = mapped_column(String(30))
    """最后更新时间"""

    # 关联关系
    question: Mapped["Question"] = relationship(
        Question, back_populates="mistake_records"
    )
