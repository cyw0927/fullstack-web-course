"""Chapter 06: FastAPI GET and POST using real PostgreSQL members."""

from fastapi import FastAPI, status
from pydantic import BaseModel

from db import fetch_members, insert_member

app = FastAPI(title="Backend Chapter 06 — PostgreSQL Members API")


class MemberCreate(BaseModel):
    name: str
    email: str
    age: int


class MemberResponse(BaseModel):
    id: int
    name: str
    email: str
    age: int


def to_member_dict(row):
    """Convert a four-column DB tuple into a Response Model compatible dict."""
    return {"id": row[0], "name": row[1], "email": row[2], "age": row[3]}


@app.get("/")
def read_root():
    return {"message": "라면먹고갈래"}


@app.get("/members", response_model=list[MemberResponse])
def get_members():
    rows = fetch_members()
    return [to_member_dict(row) for row in rows]


@app.post(
    "/members",
    response_model=MemberResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_member(member: MemberCreate):
    row = insert_member(member.name, member.email, member.age)
    return to_member_dict(row)
