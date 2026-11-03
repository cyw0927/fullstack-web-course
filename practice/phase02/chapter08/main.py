"""Phase 02 / Chapter 08: PostgreSQL INSERT와 Transaction 실습."""

import logging

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr, Field, ConfigDict, model_validator

import common.db as storage

from common.db import (
    DuplicateCourseError,
    DuplicateEmailError,
    fetch_courses,
    fetch_members,
    find_course,
    find_member,
    insert_course,
    insert_member,
)

app = FastAPI(title="Chapter 08 — PUT/PATCH + UPDATE")
logger = logging.getLogger(__name__)


# API Request/Response 계약: DB가 ID를 생성하므로 입력 모델에는 ID가 없습니다.
class MemberCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    age: int = Field(ge=0, le=150)


class MemberResponse(MemberCreate):
    id: int


class CourseCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    instructor: str = Field(min_length=1, max_length=100)
    capacity: int = Field(gt=0, le=10000)


class CourseResponse(CourseCreate):
    id: int


def member_dict(row):
    # SELECT/RETURNING 순서: id, name, email, age
    return {"id": row[0], "name": row[1], "email": row[2], "age": row[3]}


def course_dict(row):
    # SELECT/RETURNING 순서: id, title, instructor, capacity
    return {"id": row[0], "title": row[1], "instructor": row[2], "capacity": row[3]}


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


@app.get("/courses", response_model=list[CourseResponse], include_in_schema=False)
def get_courses():
    return [course_dict(row) for row in fetch_courses()]


@app.get("/courses/{course_id}", response_model=CourseResponse, include_in_schema=False)
def get_course(course_id: int):
    row = find_course(course_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return course_dict(row)


@app.post(
    "/courses",
    include_in_schema=False,
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_course(course: CourseCreate):
    try:
        row = insert_course(course.title, course.instructor, course.capacity)
        return course_dict(row)
    except DuplicateCourseError as exc:
        raise HTTPException(status_code=409, detail="이미 등록된 강좌입니다.") from exc
    except Exception as exc:
        logger.exception("강좌 INSERT 또는 commit 중 오류")
        raise HTTPException(
            status_code=500,
            detail="강좌 등록 중 오류가 발생했습니다.",
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


class CourseUpdate(CourseCreate):
    """PUT: title/instructor/capacity 모두 필수."""


class CoursePatch(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str | None = Field(default=None, min_length=1, max_length=200)
    instructor: str | None = Field(default=None, min_length=1, max_length=100)
    capacity: int | None = Field(default=None, gt=0, le=10000)

    @model_validator(mode="after")
    def reject_explicit_null(self):
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


def save_course_update(course_id: int, changes: dict):
    try:
        row = storage.update_course_fields(course_id, changes)
        return course_dict(row)
    except storage.CourseNotFound as exc:
        raise HTTPException(status_code=404, detail="Course not found") from exc
    except storage.DuplicateCourseError as exc:
        raise HTTPException(status_code=409, detail="Course already exists") from exc
    except Exception as exc:
        logger.exception("강좌 UPDATE 중 DB 오류")
        raise HTTPException(status_code=500, detail="강좌 수정 중 오류가 발생했습니다.") from exc


@app.put("/members/{member_id}", response_model=MemberResponse)
def put_member(member_id: int, member: MemberUpdate):
    return save_member_update(member_id, member.model_dump())


@app.patch("/members/{member_id}", response_model=MemberResponse)
def patch_member(member_id: int, member: MemberPatch):
    changes = member.model_dump(exclude_unset=True)
    if not changes:
        raise HTTPException(status_code=400, detail="At least one field is required")
    return save_member_update(member_id, changes)


@app.put("/courses/{course_id}", response_model=CourseResponse, include_in_schema=False)
def put_course(course_id: int, course: CourseUpdate):
    return save_course_update(course_id, course.model_dump())


@app.patch("/courses/{course_id}", response_model=CourseResponse, include_in_schema=False)
def patch_course(course_id: int, course: CoursePatch):
    changes = course.model_dump(exclude_unset=True)
    if not changes:
        raise HTTPException(status_code=400, detail="At least one field is required")
    return save_course_update(course_id, changes)
