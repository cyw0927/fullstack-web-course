"""Phase 02 / Chapter 07: PostgreSQL INSERT와 Transaction 실습."""

import logging

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr, Field

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

app = FastAPI(title="Chapter 07 — POST /members + Transaction")
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


@app.get("/courses", response_model=list[CourseResponse])
def get_courses():
    return [course_dict(row) for row in fetch_courses()]


@app.get("/courses/{course_id}", response_model=CourseResponse)
def get_course(course_id: int):
    row = find_course(course_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return course_dict(row)


@app.post(
    "/courses",
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
