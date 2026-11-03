"""회원 데이터베이스 조회 함수."""

from psycopg.rows import dict_row
from chapter10.app.db import get_connection


def find_all():
    """전체 회원을 ID 순서대로 조회합니다."""
    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT id, name, email, age
                FROM public.members
                ORDER BY id;
                """
            )
            return cur.fetchall()