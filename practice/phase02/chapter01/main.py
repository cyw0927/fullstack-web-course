"""Phase 02 Chapter 01: 첫 FastAPI 서버와 목록 조회 API."""

from fastapi import FastAPI

app = FastAPI()

# 이번 장에서는 DB 대신 메모리에 데이터를 둡니다.
members = [
    {"id": 1, "name": "Kim", "email": "kim@example.com"},
    {"id": 2, "name": "Lee", "email": "lee@example.com"},
]

courses = [
    {"id": 1, "title": "Database", "instructor": "Kim"},
    {"id": 2, "title": "Frontend", "instructor": "Lee"},
    {"id": 3, "title": "Backend", "instructor": "Park"},
]


@app.get("/")
def read_root():
    return {"message": "라면먹고갈래"}


@app.get("/members")
def read_members():
    return members


@app.get("/courses")
def read_courses():
    return courses
