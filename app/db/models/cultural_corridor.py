from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..config import Base


class TraditionalStory(Base):
    """传统故事模型"""

    __tablename__ = "traditional_stories"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    """故事ID"""
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    """故事标题"""
    dynasty: Mapped[str | None] = mapped_column(String(50))
    """朝代（如适用）"""
    period: Mapped[str | None] = mapped_column(String(100))
    """时期/年代"""
    theme: Mapped[str] = mapped_column(String(100), nullable=False)
    """主题分类"""
    content: Mapped[str] = mapped_column(Text, nullable=False)
    """故事内容"""
    moral: Mapped[str | None] = mapped_column(Text)
    """寓意或教育意义"""
    reference: Mapped[str | None] = mapped_column(Text)
    """参考来源"""
    created_at: Mapped[str] = mapped_column(String(30), nullable=False)
    """创建时间"""

    # 与跨学科案例的关系
    cross_discipline_cases: Mapped[list["CrossDisciplineCase"]] = relationship(
        back_populates="story", cascade="all, delete-orphan"
    )


class CrossDisciplineCase(Base):
    """跨学科延展案例模型"""

    __tablename__ = "cross_discipline_case"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    """案例ID"""
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    """案例标题"""
    story_id: Mapped[str | None] = mapped_column(
        String(50),
        ForeignKey(TraditionalStory.id),
    )
    """关联的传统故事ID（可选）"""
    main_discipline: Mapped[str] = mapped_column(String(50), nullable=False)
    """主要学科"""
    related_disciplines: Mapped[str] = mapped_column(Text, nullable=False)
    """相关学科，以逗号分隔"""
    suitable_grades: Mapped[str] = mapped_column(String(100), nullable=False)
    """适用年级范围"""
    content: Mapped[str] = mapped_column(Text, nullable=False)
    """案例内容"""
    teaching_objectives: Mapped[str] = mapped_column(Text, nullable=False)
    """教学目标"""
    implementation_suggestions: Mapped[str | None] = mapped_column(Text)
    """实施建议"""
    resources: Mapped[str | None] = mapped_column(Text)
    """相关资源链接，JSON格式"""
    created_at: Mapped[str] = mapped_column(String(30), nullable=False)
    """创建时间"""

    # 与传统故事的关系
    story: Mapped[TraditionalStory | None] = relationship(
        back_populates="cross_discipline_cases"
    )
