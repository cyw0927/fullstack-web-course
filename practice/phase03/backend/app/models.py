
"""실제 public.members 테이블 매핑."""

from datetime import datetime

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Identity,
    Integer,
    String,
    func,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class Member(Base):
    __tablename__ = "members"
    __table_args__ = {"schema": "public"}

    # 회원 고유 번호
    member_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    # 회원 이름
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    # 이메일 (중복 불가)
    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
    )

    # 나이
    age: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    # 성별: M(남성), F(여성), None(미지정)
    gender: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

# ========================================
# Chapter 09 — MATCHA HOUSE 상품/주문 모델
# 기존 public.members 매핑은 변경하지 않음.
#
# 주의: 이 클래스들은 DB 테이블을 생성/삭제하지 않는다.
# 실제 DB 스키마와 타입/제약을 STEP 07에서 별도 확인한다.
# ========================================


class Product(Base):
    __tablename__ = "products"
    __table_args__ = (
        CheckConstraint("price >= 0", name="ck_products_price_nonnegative"),
        CheckConstraint("stock >= 0", name="ck_products_stock_nonnegative"),
        {"schema": "public"},
    )

    id: Mapped[int] = mapped_column(
        BigInteger, Identity(always=False), primary_key=True
    )
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    category: Mapped[str] = mapped_column(String(60), nullable=False)
    stock: Mapped[int] = mapped_column(Integer, nullable=False)


class Order(Base):
    __tablename__ = "orders"
    __table_args__ = (
        CheckConstraint(
            "total_price >= 0", name="ck_orders_total_price_nonnegative"
        ),
        {"schema": "public"},
    )

    id: Mapped[int] = mapped_column(
        BigInteger, Identity(always=False), primary_key=True
    )
    total_price: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, server_default=text("'created'")
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )


class OrderItem(Base):
    __tablename__ = "order_items"
    __table_args__ = (
        CheckConstraint("quantity >= 1", name="ck_order_items_quantity_positive"),
        CheckConstraint("price >= 0", name="ck_order_items_price_nonnegative"),
        {"schema": "public"},
    )

    id: Mapped[int] = mapped_column(
        BigInteger, Identity(always=False), primary_key=True
    )
    order_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("public.orders.id"),
        nullable=False,
    )
    product_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("public.products.id"),
        nullable=False,
    )
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
