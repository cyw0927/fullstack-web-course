"""Chapter 06: PostgreSQL SELECT / INSERT helpers for FastAPI."""

import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv
from psycopg.rows import tuple_row

load_dotenv(Path(__file__).with_name(".env"))


def get_connection():
    """Open PostgreSQL connection. Read real credentials from ignored .env."""
    return psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        row_factory=tuple_row,
    )


def fetch_members():
    """Fetch every member from PostgreSQL as tuples, ordered by id."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, name, email, age
                FROM public.members
                ORDER BY id;
            """)
            return cur.fetchall()


def insert_member(name: str, email: str, age: int):
    """Insert a member and return the generated row (id, name, email, age).

    Values are passed as parameters, not interpolated into the SQL string.
    The connection context commits on success and rolls back on failure.
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO public.members (name, email, age)
                VALUES (%s, %s, %s)
                RETURNING id, name, email, age;
                """,
                (name, email, age),
            )
            created = cur.fetchone()
    return created
