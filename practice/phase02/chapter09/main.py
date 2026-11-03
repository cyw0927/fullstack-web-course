"""Phase 02 / Chapter 09 — 회원 삭제 DELETE API.

이 장은 학습 편의를 위해 9강 핵심 엔드포인트만 보여줍니다.
이전 장의 POST/PUT/PATCH 코드는 각각 chapter07/chapter08에 보존되어 있습니다.
"""

import logging

from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel, EmailStr

import common.db as storage

app = FastAPI(title="Chapter 09 — Member DELETE")
logger = logging.getLogger(__name__)


class MemberResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: int


@app.get("/members/{member_id}", response_model=MemberResponse)
def get_member(member_id: int):
    """삭제 전에는 200, 삭제 후에는 404가 되어야 합니다."""
    try:
        row = storage.find_member(member_id)
    except Exception as exc:
        logger.exception("회원 조회 중 DB 오류")
        raise HTTPException(
            status_code=500, detail="회원 조회 중 오류가 발생했습니다."
        ) from exc

    if row is None:
        raise HTTPException(status_code=404, detail="Member not found")

    return {"id": row[0], "name": row[1], "email": row[2], "age": row[3]}


@app.delete(
    "/members/{member_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
def delete_member(member_id: int):
    """삭제 성공은 204 + 빈 응답 Body. 실제 저장 결과는 DB에서 확인하세요."""
    try:
        deleted_id = storage.delete_member_by_id(member_id)
    except Exception as exc:
        logger.exception("회원 DELETE 중 DB 오류")
        raise HTTPException(
            status_code=500, detail="회원 삭제 중 오류가 발생했습니다."
        ) from exc

    if deleted_id is None:
        raise HTTPException(status_code=404, detail="Member not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
