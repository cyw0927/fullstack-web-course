"""10강: FastAPI 앱과 라우터를 연결합니다."""
from fastapi import FastAPI
from chapter10.app.routers import members

app = FastAPI(title="Chapter 10 — Backend 구조화")
app.include_router(members.router)
