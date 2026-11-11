
"""회원 업무 규칙과 HTTP 오류 의미를 처리하고 주요 상황을 기록합니다."""

import logging

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.repositories import member_repository as repository

logger = logging.getLogger(__name__)


# ========================================
# 1. GET — 전체 회원 조회
# ========================================
def get_members(db: Session):
    members = repository.find_all(db)

    logger.info(
        "member list requested: count=%s",
        len(members),
    )

    return members


# ========================================
# 2. GET — 회원 한 명 조회
# ========================================
def get_member(db: Session, member_id: int):
    member = repository.find_by_id(db, member_id)

    if member is None:
        logger.warning(
            "member not found: member_id=%s",
            member_id,
        )
        raise HTTPException(
            status_code=404,
            detail="Member not found",
        )

    return member


# ========================================
# 3. POST — 신규 회원 등록
# ========================================
def create_member(db: Session, payload):
    email = str(payload.email)

    # 이메일 중복 검사
    if repository.find_by_email(db, email) is not None:
        logger.warning("duplicate member email requested")
        raise HTTPException(
            status_code=409,
            detail="Email already exists",
        )

    try:
        # 6강 이후 확장: gender도 함께 전달
        member = repository.create_member(
            db,
            payload.name,
            email,
            payload.age,
            payload.gender,
        )

        logger.info(
            "member created: member_id=%s",
            member.member_id,
        )

        return member

    except IntegrityError as exc:
        logger.warning(
            "member email conflict detected by database"
        )
        raise HTTPException(
            status_code=409,
            detail="Email already exists",
        ) from exc


# ========================================
# 4. PUT / PATCH — 회원 정보 수정
# ========================================
def update_member(
    db: Session,
    member_id: int,
    changes: dict,
):
    if not changes:
        raise HTTPException(
            status_code=400,
            detail="At least one field is required",
        )

    member = get_member(db, member_id)

    # 이메일 변경 시 중복 검사
    if (
        "email" in changes
        and repository.find_by_email(
            db,
            str(changes["email"]),
            exclude_member_id=member_id,
        )
        is not None
    ):
        logger.warning(
            "duplicate member email requested for update"
        )
        raise HTTPException(
            status_code=409,
            detail="Email already exists",
        )

    try:
        # gender가 changes에 있으면 함께 수정
        updated = repository.update_member(
            db,
            member,
            changes,
        )

        logger.info(
            "member updated: member_id=%s",
            member_id,
        )

        return updated

    except IntegrityError as exc:
        logger.warning(
            "member update conflict detected by database"
        )
        raise HTTPException(
            status_code=409,
            detail="Email already exists",
        ) from exc


# ========================================
# 5. DELETE — 회원 삭제
# ========================================
def delete_member(db: Session, member_id: int):
    member = get_member(db, member_id)

    repository.delete_member(db, member)

    logger.info(
        "member deleted: member_id=%s",
        member_id,
    )

"""회원 업무 규칙과 HTTP 오류 의미를 처리하고 주요 상황을 기록합니다."""

import logging

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.repositories import member_repository as repository

logger = logging.getLogger(__name__)


# ========================================
# 1. GET — 전체 회원 조회
# ========================================
def get_members(db: Session):
    members = repository.find_all(db)

    logger.info(
        "member list requested: count=%s",
        len(members),
    )

    return members


# ========================================
# 2. GET — 회원 한 명 조회
# ========================================
def get_member(db: Session, member_id: int):
    member = repository.find_by_id(db, member_id)

    if member is None:
        logger.warning(
            "member not found: member_id=%s",
            member_id,
        )
        raise HTTPException(
            status_code=404,
            detail="Member not found",
        )

    return member


# ========================================
# 3. POST — 신규 회원 등록
# ========================================
def create_member(db: Session, payload):
    email = str(payload.email)

    # 이메일 중복 검사
    if repository.find_by_email(db, email) is not None:
        logger.warning("duplicate member email requested")
        raise HTTPException(
            status_code=409,
            detail="Email already exists",
        )

    try:
        # 6강 이후 확장: gender도 함께 전달
        member = repository.create_member(
            db,
            payload.name,
            email,
            payload.age,
            payload.gender,
        )

        logger.info(
            "member created: member_id=%s",
            member.member_id,
        )

        return member

    except IntegrityError as exc:
        logger.warning(
            "member email conflict detected by database"
        )
        raise HTTPException(
            status_code=409,
            detail="Email already exists",
        ) from exc


# ========================================
# 4. PUT / PATCH — 회원 정보 수정
# ========================================
def update_member(
    db: Session,
    member_id: int,
    changes: dict,
):
    if not changes:
        raise HTTPException(
            status_code=400,
            detail="At least one field is required",
        )

    member = get_member(db, member_id)

    # 이메일 변경 시 중복 검사
    if (
        "email" in changes
        and repository.find_by_email(
            db,
            str(changes["email"]),
            exclude_member_id=member_id,
        )
        is not None
    ):
        logger.warning(
            "duplicate member email requested for update"
        )
        raise HTTPException(
            status_code=409,
            detail="Email already exists",
        )

    try:
        # gender가 changes에 있으면 함께 수정
        updated = repository.update_member(
            db,
            member,
            changes,
        )

        logger.info(
            "member updated: member_id=%s",
            member_id,
        )

        return updated

    except IntegrityError as exc:
        logger.warning(
            "member update conflict detected by database"
        )
        raise HTTPException(
            status_code=409,
            detail="Email already exists",
        ) from exc


# ========================================
# 5. DELETE — 회원 삭제
# ========================================
def delete_member(db: Session, member_id: int):
    member = get_member(db, member_id)

    repository.delete_member(db, member)

    logger.info(
        "member deleted: member_id=%s",
        member_id,
    )
