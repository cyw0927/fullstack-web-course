"""Phase 02 / Chapter 09 — PostgreSQL 회원 상세 조회와 삭제."""

import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv

# chapter09/.env만 읽으므로 작업 디렉터리에 의존하지 않습니다.
load_dotenv(Path(__file__).with_name(".env"))


def get_connection():
    """비밀번호는 Git에 올리지 않는 .env에서 가져옵니다."""
    return psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )


def find_member(member_id: int):
    """회원 조회. 튜플(id, name, email, age) 또는 None을 반환."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, name, email, age
                FROM public.members
                WHERE id = %s;
                """,
                (member_id,),
            )
            return cur.fetchone()


def delete_member_by_id(member_id: int):
    """DELETE ... RETURNING으로 삭제 성공 여부를 확인합니다.

    성공 시 commit하고 삭제 ID를 반환합니다.
    대상이 없으면 rollback 후 None을 반환합니다.
    SQL/commit 오류 시 rollback 후 예외를 다시 발생시킵니다.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                DELETE FROM public.members
                WHERE id = %s
                RETURNING id;
                """,
                (member_id,),
            )
            deleted_row = cur.fetchone()

        if deleted_row is None:
            conn.rollback()
            return None

        conn.commit()
        return deleted_row[0]
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
