"""Phase 02 / Chapter 04: Response Model과 HTTP Status Code 실습.

이 챕터는 데이터베이스 대신 메모리 리스트를 사용합니다.
"""

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI(title="Backend Chapter 04 - Response Model & Status Code")


# Request Body의 필수 필드: 서버로 보내는 정보에는 id가 없습니다.
class MemberCreate(BaseModel):
    name: str
    email: str
    age: int


# Response Body의 공개 필드: 서버가 id를 포함해 반환합니다.
class MemberResponse(BaseModel):
    id: int
    name: str
    email: str
    age: int


class CourseCreate(BaseModel):
    title: str
    instructor: str


class CourseResponse(BaseModel):
    id: int
    title: str
    instructor: str


# DB 대신 리스트에 임시 저장합니다. 서버를 재시작하면 처음 상태로 돌아갑니다.
members = [
    {"id": 1, "name": "Kim", "email": "kim@example.com", "age": 25, "internal_note": "VIP"},
    {"id": 2, "name": "Lee", "email": "lee@example.com", "age": 31},
]

courses = [
    {"id": 1, "title": "Database", "instructor": "Kim"},
    {"id": 2, "title": "Frontend", "instructor": "Lee"},
]


@app.get("/")
def read_root():
    return {"message": "라면먹고갈래"}


@app.get(
    "/members",
    response_model=list[MemberResponse],
    status_code=status.HTTP_200_OK,
)
def get_members():
    return members


@app.get(
    "/members/{member_id}",
    response_model=MemberResponse,
    status_code=status.HTTP_200_OK,
)
def get_member(member_id: int):
    for member in members:
        if member["id"] == member_id:
            return member
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Member not found",
    )


@app.post(
    "/members",
    response_model=MemberResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_member(member: MemberCreate):
    new_member = {
        "id": len(members) + 1,  # 삭제 기능이 없는 교육용 리스트에서만 사용하는 단순 ID
        "name": member.name,
        "email": member.email,
        "age": member.age,
    }
    members.append(new_member)
    return new_member


@app.get(
    "/courses",
    response_model=list[CourseResponse],
    status_code=status.HTTP_200_OK,
)
def get_courses():
    return courses


@app.get(
    "/courses/{course_id}",
    response_model=CourseResponse,
    status_code=status.HTTP_200_OK,
)
def get_course(course_id: int):
    for course in courses:
        if course["id"] == course_id:
            return course
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Course not found",
    )


@app.post(
    "/courses",
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_course(course: CourseCreate):
    new_course = {
        "id": len(courses) + 1,
        "title": course.title,
        "instructor": course.instructor,
    }
    courses.append(new_course)
    return new_course
