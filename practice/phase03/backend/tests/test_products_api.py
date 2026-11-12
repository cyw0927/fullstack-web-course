"""Chapter 09 STEP 14: GET /products API tests.

Uses a new, isolated SQLite in-memory database per test; never opens or
modifies the user's existing PostgreSQL database. This is a lightweight
API/ORM integration test, not proof of PostgreSQL-specific behavior.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import get_db
from app.main import app
from app.models import Product


@pytest.fixture
def product_api():
    """Create a temporary store schema and override the application's DB session."""
    engine = create_engine(
        "sqlite+pysqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    @event.listens_for(engine, "connect")
    def create_store_schema(dbapi_connection, _connection_record):
        # Product is explicitly mapped to schema="matcha_store".
        dbapi_connection.execute("ATTACH DATABASE ':memory:' AS matcha_store")

    Product.__table__.create(bind=engine)
    testing_session = sessionmaker(bind=engine, expire_on_commit=False)

    def override_get_db():
        with testing_session() as db:
            yield db

    app.dependency_overrides[get_db] = override_get_db
    try:
        with TestClient(app) as client:
            yield client, testing_session
    finally:
        app.dependency_overrides.pop(get_db, None)
        engine.dispose()


def seed_product(testing_session, *, product_id, name, price, category, stock):
    with testing_session.begin() as db:
        db.add(
            Product(
                id=product_id,
                name=name,
                price=price,
                category=category,
                stock=stock,
            )
        )


def test_get_products_returns_200_and_empty_array(product_api):
    client, _testing_session = product_api
    response = client.get("/products")

    assert response.status_code == 200
    assert response.json() == []


def test_get_products_returns_expected_fields_and_types(product_api):
    client, testing_session = product_api
    seed_product(
        testing_session,
        product_id=2,
        name="말차 쿠키",
        price=2500,
        category="디저트",
        stock=25,
    )
    seed_product(
        testing_session,
        product_id=1,
        name="아이스 말차 라떼",
        price=5500,
        category="음료",
        stock=20,
    )

    response = client.get("/products")

    assert response.status_code == 200
    items = response.json()
    assert [item["id"] for item in items] == [1, 2]
    assert items[0] == {
        "id": 1,
        "name": "아이스 말차 라떼",
        "price": 5500,
        "category": "음료",
        "stock": 20,
    }
    assert items[1] == {
        "id": 2,
        "name": "말차 쿠키",
        "price": 2500,
        "category": "디저트",
        "stock": 25,
    }
    for item in items:
        assert set(item) == {"id", "name", "price", "category", "stock"}
        assert isinstance(item["id"], int)
        assert isinstance(item["name"], str)
        assert isinstance(item["price"], int)
        assert isinstance(item["category"], str)
        assert isinstance(item["stock"], int)


def test_get_products_includes_sold_out_item(product_api):
    client, testing_session = product_api
    seed_product(
        testing_session,
        product_id=7,
        name="말차 아이스크림",
        price=4500,
        category="디저트",
        stock=0,
    )

    response = client.get("/products")

    assert response.status_code == 200
    assert response.json()[0]["stock"] == 0


def test_get_products_is_read_only(product_api):
    client, testing_session = product_api
    seed_product(
        testing_session,
        product_id=3,
        name="말차 티라미수",
        price=7000,
        category="디저트",
        stock=8,
    )

    response = client.get("/products")
    assert response.status_code == 200

    with testing_session() as db:
        product = db.get(Product, 3)
        assert product is not None
        assert product.stock == 8


def test_products_is_registered_in_openapi_and_members_route_preserved(product_api):
    client, _testing_session = product_api
    response = client.get("/openapi.json")

    assert response.status_code == 200
    paths = response.json()["paths"]
    assert "get" in paths["/products"]
    assert "get" in paths["/members"]
