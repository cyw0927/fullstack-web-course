"""회원 업무 규칙과 HTTP 오류 의미를 처리하고 주요 상황을 기록합니다."""
import logging

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.repositories import member_repository as repository

logger = logging.getLogger(__name__)


def get_members(db: Session):
    members = repository.find_all(db)
    logger.info("member list requested: count=%s", len(members))
    return members


def get_member(db: Session, member_id: int):
    member = repository.find_by_id(db, member_id)
    if member is None:
        logger.warning("member not found: member_id=%s", member_id)
        raise HTTPException(status_code=404, detail="Member not found")
    return member


def create_member(db: Session, payload):
    email = str(payload.email)
    if repository.find_by_email(db, email) is not None:
        logger.warning("duplicate member email requested")
        raise HTTPException(status_code=409, detail="Email already exists")
    try:
        member = repository.create_member(db, payload.name, email, payload.age)
        logger.info("member created: member_id=%s", member.member_id)
        return member
    except IntegrityError as exc:
        logger.warning("member email conflict detected by database")
        raise HTTPException(status_code=409, detail="Email already exists") from exc


def update_member(db: Session, member_id: int, changes: dict):
    if not changes:
        raise HTTPException(status_code=400, detail="At least one field is required")
    member = get_member(db, member_id)
    if "email" in changes and repository.find_by_email(
        db, str(changes["email"]), exclude_member_id=member_id
    ) is not None:
        logger.warning("duplicate member email requested for update")
        raise HTTPException(status_code=409, detail="Email already exists")
    try:
        updated = repository.update_member(db, member, changes)
        logger.info("member updated: member_id=%s", member_id)
        return updated
    except IntegrityError as exc:
        logger.warning("member update conflict detected by database")
        raise HTTPException(status_code=409, detail="Email already exists") from exc


def delete_member(db: Session, member_id: int):
    member = get_member(db, member_id)
    repository.delete_member(db, member)
    logger.info("member deleted: member_id=%s", member_id)
