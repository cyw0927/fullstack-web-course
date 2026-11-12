"""MATCHA HOUSE 상품 조회 업무를 담당합니다."""

from sqlalchemy.orm import Session

from app.repositories import product_repository


def get_products(db: Session):
    """Repository에서 상품 목록을 가져옵니다."""
    return product_repository.find_all(db)
