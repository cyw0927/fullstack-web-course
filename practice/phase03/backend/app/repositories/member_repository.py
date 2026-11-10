"""Member ORM 조회와 CRUD, 트랜잭션을 담당합니다."""
import logging

from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import Member

logger = logging.getLogger(__name__)


def find_all(db: Session):
    return db.scalars(select(Member).order_by(Member.member_id)).all()


def find_by_id(db: Session, member_id: int):
    return db.get(Member, member_id)


def find_by_email(db: Session, email: str, exclude_member_id: int | None = None):
    stmt = select(Member).where(Member.email == email)
    if exclude_member_id is not None:
        stmt = stmt.where(Member.member_id != exclude_member_id)
    return db.scalar(stmt)


def create_member(db: Session, name: str, email: str, age: int):
    member = Member(name=name, email=email, age=age)
    try:
        db.add(member)
        db.commit()
        db.refresh(member)
        return member
    except Exception:
        db.rollback()
        logger.exception("database error while creating member")
        raise


def update_member(db: Session, member: Member, changes: dict):
    try:
        for field, value in changes.items():
            if field == "email":
                value = str(value)
            setattr(member, field, value)
        db.commit()
        db.refresh(member)
        return member
    except Exception:
        db.rollback()
        logger.exception("database error while updating member_id=%s", member.member_id)
        raise


def delete_member(db: Session, member: Member):
    try:
        db.delete(member)
        db.commit()
    except Exception:
        db.rollback()
        logger.exception("database error while deleting member_id=%s", member.member_id)
        raise
