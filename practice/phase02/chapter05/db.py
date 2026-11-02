"""Chapter 05: standalone PostgreSQL connection and SQL access."""

import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv

# Always read the .env next to this file, regardless of terminal location.
load_dotenv(Path(__file__).with_name(".env"))


def get_connection():
    """Open a connection using environment variables; never hard-code secrets."""
    return psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )


def check_connection():
    """Verify the actual connected database and active schema."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT current_database(), current_schema();")
            return cur.fetchone()


def fetch_members():
    """Return DB rows as tuples; this chapter does not use FastAPI yet."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, name, email
                FROM public.members
                ORDER BY id;
            """)
            return cur.fetchall()
