
"""Member ORM 조회와 CRUD, 트랜잭션을 담당합니다."""

import logging

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Member

logger = logging.getLogger(__name__)


# ========================================
# 1. GET — 전체 회원 조회
# ========================================
def find_all(db: Session):
    return db.scalars(
        select(Member).order_by(Member.member_id)
    ).all()


# ========================================
# 2. GET — 회원 한 명 조회
# ========================================
def find_by_id(db: Session, member_id: int):
    return db.get(Member, member_id)


# ========================================
# 3. 이메일 중복 확인
# ========================================
def find_by_email(
    db: Session,
    email: str,
    exclude_member_id: int | None = None,
):
    stmt = select(Member).where(Member.email == email)

    if exclude_member_id is not None:
        stmt = stmt.where(
            Member.member_id != exclude_member_id
        )

    return db.scalar(stmt)


# ========================================
# 4. POST — 신규 회원 등록
# ========================================
def create_member(
    db: Session,
    name: str,
    email: str,
    age: int,
    gender: str | None = None,
):
    # 기존 이름·이메일·나이와 함께 성별 저장
    member = Member(
        name=name,
        email=email,
        age=age,
        gender=gender,
    )

    try:
        db.add(member)
        db.commit()
        db.refresh(member)

        return member

    except Exception:
        db.rollback()
        logger.exception(
            "database error while creating member"
        )
        raise


# ========================================
# 5. PUT / PATCH — 기존 회원 수정
# ========================================
def update_member(
    db: Session,
    member: Member,
    changes: dict,
):
    try:
        # 변경할 필드만 기존 회원에 반영
        # gender도 changes에 있으면 자동 처리
        for field, value in changes.items():
            if field == "email":
                value = str(value)

            setattr(member, field, value)

        db.commit()
        db.refresh(member)

        return member

    except Exception:
        db.rollback()
        logger.exception(
            "database error while updating member_id=%s",
            member.member_id,
        )
        raise


# ========================================
# 6. DELETE — 회원 삭제
# ========================================
def delete_member(
    db: Session,
    member: Member,
):
    try:
        db.delete(member)
        db.commit()

    except Exception:
        db.rollback()
        logger.exception(
            "database error while deleting member_id=%s",
            member.member_id,
        )
        raise
