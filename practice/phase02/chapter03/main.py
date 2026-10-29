"""Phase 02 / Chapter 03: Request Body, Pydantic 및 POST Validation."""

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI(title="Backend Chapter 03 - Request Body & Pydantic")

# DB 대신 사용하는 실습용 데이터: POST 요청으로는 이 리스트가 변경되지 않습니다.
members = [
    {"id": 1, "name": "Kim", "email": "kim@example.com", "age": 25},
    {"id": 2, "name": "Lee", "email": "lee@example.com", "age": 19},
    {"id": 3, "name": "Park", "email": "park@example.com", "age": 31},
]

courses = [
    {"id": 1, "title": "Database", "level": 1},
    {"id": 2, "title": "Frontend", "level": 2},
    {"id": 3, "title": "FastAPI", "level": 2},
]


# Pydantic 모델: Body의 필수 필드와 타입을 선언합니다.
class MemberCreate(BaseModel):
    name: str
    email: str
    age: int


class CourseCreate(BaseModel):
    title: str
    instructor: str
    capacity: int


@app.get("/")
def read_root():
    return {"message": "라면먹고갈래"}


def select_members(name: str | None = None, min_age: int | None = None):
    """회원 목록의 Query Parameter 조건을 적용합니다."""
    result = members
    if name is not None:
        keyword = name.lower()
        result = [member for member in result if keyword in member["name"].lower()]
    if min_age is not None:
        result = [member for member in result if member["age"] >= min_age]
    return result


@app.get("/members")
def get_members(name: str | None = None, min_age: int | None = None):
    return select_members(name=name, min_age=min_age)


# POST의 /members는 GET의 /members와 Method가 달라 공존합니다.
@app.post("/members", status_code=status.HTTP_201_CREATED)
def create_member(member: MemberCreate):
    # 연습용 임시 ID: 실제 저장이나 중복 방지를 보장하지 않습니다.
    return {"id": 4, "name": member.name, "email": member.email, "age": member.age}


# 고정 URL은 동적 {member_id} URL보다 먼저 선언합니다.
@app.get("/members/search/")
def search_members(name: str | None = None):
    return select_members(name=name)


@app.get("/members/filter/")
def filter_members(name: str | None = None, min_age: int | None = None):
    return select_members(name=name, min_age=min_age)


@app.get("/members/{member_id}")
def get_member(member_id: int):
    for member in members:
        if member["id"] == member_id:
            return member
    raise HTTPException(status_code=404, detail="Member not found")


@app.get("/courses")
def get_courses():
    return courses


@app.post("/courses", status_code=status.HTTP_201_CREATED)
def create_course(course: CourseCreate):
    # Chapter 02의 GET 강좌 데이터(level)와 별도인 POST Body 연습입니다.
    # DB 저장 없음. 요청을 받을 때마다 같은 학습용 ID를 반환합니다.
    return {
        "id": 4,
        "title": course.title,
        "instructor": course.instructor,
        "capacity": course.capacity,
    }


@app.get("/courses/filter/")
def filter_courses(title: str | None = None, level: int | None = None):
    result = courses
    if title is not None:
        keyword = title.lower()
        result = [course for course in result if keyword in course["title"].lower()]
    if level is not None:
        result = [course for course in result if course["level"] == level]
    return result


@app.get("/courses/{course_id}")
def get_course(course_id: int):
    for course in courses:
        if course["id"] == course_id:
            return course
    raise HTTPException(status_code=404, detail="Course not found")
