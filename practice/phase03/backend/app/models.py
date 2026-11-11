
"""실제 public.members 테이블 매핑."""

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class Member(Base):
    __tablename__ = "members"
    __table_args__ = {"schema": "public"}

    # 회원 고유 번호
    member_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    # 회원 이름
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    # 이메일 (중복 불가)
    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
    )

    # 나이
    age: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    # 성별: M(남성), F(여성), None(미지정)
    gender: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )
