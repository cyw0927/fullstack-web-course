"""MATCHA HOUSE 상품 목록의 DB 조회를 담당합니다."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Product


def find_all(db: Session):
    """상품을 ID 순서대로 조회합니다."""
    return db.scalars(select(Product).order_by(Product.id)).all()
