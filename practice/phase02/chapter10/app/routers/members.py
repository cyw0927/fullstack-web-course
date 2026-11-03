"""회원 요청을 받아 서비스로 전달하는 라우터."""
from fastapi import APIRouter

router = APIRouter(prefix="/members", tags=["members"])

# TODO: GET /, GET /{member_id}, POST /, PUT /{member_id},
# PATCH /{member_id}, DELETE /{member_id}를 차례로 작성하세요.
