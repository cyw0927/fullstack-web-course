
"""HTTP 요청과 Service를 연결합니다."""

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas import (
    MemberCreate,
    MemberPatch,
    MemberResponse,
    MemberUpdate,
)
from app.services import member_service


router = APIRouter(
    prefix="/members",
    tags=["members"],
)


# 1. GET — 회원 전체 조회
@router.get("", response_model=list[MemberResponse])
def get_members(db: Session = Depends(get_db)):
    return member_service.get_members(db)


# 2. GET — 회원 상세 조회
@router.get("/{member_id}", response_model=MemberResponse)
def get_member(
    member_id: int,
    db: Session = Depends(get_db),
):
    return member_service.get_member(db, member_id)


# 3. POST — 회원 등록
@router.post(
    "",
    response_model=MemberResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_member(
    payload: MemberCreate,
    db: Session = Depends(get_db),
):
    return member_service.create_member(db, payload)


# 4. PUT — 회원 정보 수정
@router.put(
    "/{member_id}",
    response_model=MemberResponse,
)
def put_member(
    member_id: int,
    payload: MemberUpdate,
    db: Session = Depends(get_db),
):
    # 성별을 생략하면 기존 성별 유지
    # 이름, 이메일, 나이는 여전히 필수
    changes = payload.model_dump(exclude_unset=True)

    return member_service.update_member(
        db,
        member_id,
        changes,
    )


# 5. PATCH — 회원 정보 일부 수정
@router.patch(
    "/{member_id}",
    response_model=MemberResponse,
)
def patch_member(
    member_id: int,
    payload: MemberPatch,
    db: Session = Depends(get_db),
):
    changes = payload.model_dump(exclude_unset=True)

    return member_service.update_member(
        db,
        member_id,
        changes,
    )


# 6. DELETE — 회원 삭제
@router.delete(
    "/{member_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
def delete_member(
    member_id: int,
    db: Session = Depends(get_db),
):
    member_service.delete_member(db, member_id)

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )
