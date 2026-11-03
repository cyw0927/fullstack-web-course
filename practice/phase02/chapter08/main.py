"""8강: 회원 PUT/PATCH와 PostgreSQL UPDATE 실습."""

import logging

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr, Field, ConfigDict, model_validator

import common.db as storage

from common.db import (
    DuplicateEmailError,
    fetch_members,
    find_member,
    insert_member,
)

from chapter08.courses import router as courses_router

app = FastAPI(title="Chapter 08 — PUT/PATCH + UPDATE")
# 강좌 과제는 기존 경로를 유지하면서 기본 문서에서는 숨깁니다.
app.include_router(courses_router, include_in_schema=False)
logger = logging.getLogger(__name__)


# API Request/Response 계약: DB가 ID를 생성하므로 입력 모델에는 ID가 없습니다.
class MemberCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    age: int = Field(ge=0, le=150)


class MemberResponse(MemberCreate):
    id: int


def member_dict(row):
    # SELECT/RETURNING 순서: id, name, email, age
    return {"id": row[0], "name": row[1], "email": row[2], "age": row[3]}


@app.get("/")
def read_root():
    return {"message": "라면먹고갈래"}


@app.get("/members", response_model=list[MemberResponse])
def get_members():
    return [member_dict(row) for row in fetch_members()]


@app.get("/members/{member_id}", response_model=MemberResponse)
def get_member(member_id: int):
    row = find_member(member_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Member not found")
    return member_dict(row)


@app.post(
    "/members",
    response_model=MemberResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_member(member: MemberCreate):
    try:
        row = insert_member(member.name, str(member.email), member.age)
        return member_dict(row)
    except DuplicateEmailError as exc:
        raise HTTPException(status_code=409, detail="이미 등록된 이메일입니다.") from exc
    except Exception as exc:
        logger.exception("회원 INSERT 또는 commit 중 오류")
        raise HTTPException(
            status_code=500,
            detail="회원 등록 중 오류가 발생했습니다.",
        ) from exc


# ------------------------------------------------------------
# 8강: PUT은 필수 3필드를 모두, PATCH는 전달된 필드만 수정
# ------------------------------------------------------------

class MemberUpdate(MemberCreate):
    """PUT: name/email/age 세 필드 모두 필수."""


class MemberPatch(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str | None = Field(default=None, min_length=1, max_length=100)
    email: EmailStr | None = None
    age: int | None = Field(default=None, ge=0, le=150)

    @model_validator(mode="after")
    def reject_explicit_null(self):
        # exclude_unset=True는 None을 자동으로 제거하지 않습니다.
        for field in self.model_fields_set:
            if getattr(self, field) is None:
                raise ValueError(f"{field} cannot be null")
        return self


def save_member_update(member_id: int, changes: dict):
    try:
        row = storage.update_member_fields(member_id, changes)
        return member_dict(row)
    except storage.MemberNotFound as exc:
        raise HTTPException(status_code=404, detail="Member not found") from exc
    except storage.DuplicateEmailError as exc:
        raise HTTPException(status_code=409, detail="Email already exists") from exc
    except Exception as exc:
        logger.exception("회원 UPDATE 중 DB 오류")
        raise HTTPException(status_code=500, detail="회원 수정 중 오류가 발생했습니다.") from exc


@app.put("/members/{member_id}", response_model=MemberResponse)
def put_member(member_id: int, member: MemberUpdate):
    return save_member_update(member_id, member.model_dump())


@app.patch("/members/{member_id}", response_model=MemberResponse)
def patch_member(member_id: int, member: MemberPatch):
    changes = member.model_dump(exclude_unset=True)
    if not changes:
        raise HTTPException(status_code=400, detail="At least one field is required")
    return save_member_update(member_id, changes)
