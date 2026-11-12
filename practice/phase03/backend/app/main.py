"""13강 Member API와 14강 CORS 설정을 함께 제공합니다."""
import logging
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.member_router import router as member_router
from app.routers.product_router import router as product_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

# 쉼표로 구분된 정확한 Frontend Origin만 허용합니다. 전체 허용(*)은 쓰지 않습니다.
allowed_origins = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5500,http://127.0.0.1:5500,http://localhost:3000,http://127.0.0.1:3000",
    ).split(",")
    if origin.strip()
]

app = FastAPI(title="Chapter 13 — Member API and Chapter 14 CORS")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type"],
)
app.include_router(member_router)
app.include_router(product_router)
