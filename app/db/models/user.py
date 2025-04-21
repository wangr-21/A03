from sqlalchemy import BLOB, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from ..config import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(
        Integer(),
        primary_key=True,
        comment="用户ID（主键）",
    )
    username: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="用户名",
    )
    password: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="加盐哈希密码",
    )

    # user info
    name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="姓名",
    )
    title: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        comment="职称",
    )
    department: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        comment="部门",
    )
    avatar: Mapped[bytes | None] = mapped_column(
        BLOB,
        nullable=True,
        comment="头像",
    )
