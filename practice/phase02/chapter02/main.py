"""Phase 02 / Chapter 02: Path Parameter와 Query Parameter 실습."""

from fastapi import FastAPI, HTTPException

app = FastAPI(title="Backend Chapter 02 - Path & Query Parameters")

# 아직 DB를 연결하지 않고 Python 리스트를 사용합니다.
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


@app.get("/")
def read_root():
    return {"message": "라면먹고갈래"}


def select_members(name: str | None = None, min_age: int | None = None):
    """회원 목록을 이름/최소 나이 조건으로 좁힙니다."""
    result = members
    if name is not None:
        keyword = name.lower()
        result = [member for member in result if keyword in member["name"].lower()]
    if min_age is not None:
        result = [member for member in result if member["age"] >= min_age]
    return result


@app.get("/members")
def get_members(name: str | None = None, min_age: int | None = None):
    # 조건이 없으면 Chapter 01과 동일하게 전체 회원을 반환합니다.
    return select_members(name=name, min_age=min_age)


# 고정 경로를 {member_id}보다 먼저 등록해야 /members/search가 ID로 해석되지 않습니다.
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


# 강좌 필터도 동적 경로보다 먼저 등록합니다.
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
