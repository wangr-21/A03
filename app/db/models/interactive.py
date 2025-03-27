from sqlalchemy import String, Integer, Text
from sqlalchemy.orm import mapped_column, Mapped
from ..config import Base


class InteractiveActivity(Base):
    """互动环节模型"""

    __tablename__ = "interactive_activities"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    activity_type: Mapped[str] = mapped_column(String(20), nullable=False)
    """活动类型：'discussion', 'question', 'game', 'scenario'"""
    description: Mapped[str] = mapped_column(Text, nullable=False)
    """活动描述"""
    content: Mapped[str] = mapped_column(Text, nullable=False)
    """存储JSON格式的活动内容"""
    subject: Mapped[str] = mapped_column(String(50), nullable=False)
    """学科"""
    grade: Mapped[str] = mapped_column(String(20), nullable=False)
    """适用年级"""
    duration: Mapped[int] = mapped_column(Integer, nullable=False)
    """预计时长(分钟)"""
    created_at: Mapped[str] = mapped_column(String(30), nullable=False)
    """创建时间"""


class ScenarioSimulation(Base):
    """情景模拟沙盘模型"""

    __tablename__ = "scenario_simulations"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    scenario_type: Mapped[str] = mapped_column(String(20), nullable=False)
    """场景类型：'historical', 'literary', 'scientific'"""
    description: Mapped[str] = mapped_column(Text, nullable=False)
    """场景描述"""
    content: Mapped[str] = mapped_column(Text, nullable=False)
    """存储JSON格式的场景内容"""
    background: Mapped[str] = mapped_column(Text, nullable=False)
    """背景知识"""
    subject: Mapped[str] = mapped_column(String(50), nullable=False)
    """学科"""
    grade: Mapped[str] = mapped_column(String(20), nullable=False)
    """适用年级"""
    created_at: Mapped[str] = mapped_column(String(30), nullable=False)
    """创建时间"""
