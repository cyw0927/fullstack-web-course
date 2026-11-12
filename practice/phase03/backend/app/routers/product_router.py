"""MATCHA HOUSE 상품 목록 GET API — 기존 회원 Router와 분리."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas import ProductResponse
from app.services import product_service


router = APIRouter(
    prefix="/products",
    tags=["products"],
)


@router.get("", response_model=list[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    """실제 matcha_store.products 테이블의 상품 목록을 반환합니다."""
    return product_service.get_products(db)
