"""PostgreSQL 접근 함수: 중복 검사, parameterized INSERT, commit/rollback."""

import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv
from psycopg.rows import tuple_row

load_dotenv(Path(__file__).with_name(".env"))


class DuplicateEmailError(Exception):
    """현재 DB에 같은 이메일이 존재합니다."""


class DuplicateCourseError(Exception):
    """현재 DB에 같은 제목/강사 조합이 존재합니다."""


def get_connection():
    return psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        row_factory=tuple_row,
    )


def fetch_members():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, name, email, age FROM public.members ORDER BY id;"
            )
            return cur.fetchall()


def find_member(member_id: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, name, email, age FROM public.members WHERE id = %s;",
                (member_id,),
            )
            return cur.fetchone()


def fetch_courses():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, title, instructor, capacity FROM public.courses ORDER BY id;"
            )
            return cur.fetchall()


def find_course(course_id: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, title, instructor, capacity FROM public.courses WHERE id = %s;",
                (course_id,),
            )
            return cur.fetchone()


def insert_member(name: str, email: str, age: int):
    """중복 이메일 거부 → INSERT RETURNING → commit; 실패 시 rollback."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id FROM public.members WHERE email = %s;",
                (email,),
            )
            if cur.fetchone() is not None:
                raise DuplicateEmailError(email)

            cur.execute(
                """
                INSERT INTO public.members (name, email, age)
                VALUES (%s, %s, %s)
                RETURNING id, name, email, age;
                """,
                (name, email, age),
            )
            created = cur.fetchone()

        conn.commit()
        return created
    except psycopg.errors.UniqueViolation as exc:
        conn.rollback()
        # DB UNIQUE 인덱스는 동시 요청의 중복까지 막아 줍니다.
        if exc.diag.constraint_name in {
            "members_email_key", "members_email_unique_idx"
        }:
            raise DuplicateEmailError(email) from exc
        raise
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def insert_course(title: str, instructor: str, capacity: int):
    """중복 기준: 동일한 (title, instructor) 조합."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id FROM public.courses
                WHERE title = %s AND instructor = %s;
                """,
                (title, instructor),
            )
            if cur.fetchone() is not None:
                raise DuplicateCourseError((title, instructor))

            cur.execute(
                """
                INSERT INTO public.courses (title, instructor, capacity)
                VALUES (%s, %s, %s)
                RETURNING id, title, instructor, capacity;
                """,
                (title, instructor, capacity),
            )
            created = cur.fetchone()

        conn.commit()
        return created
    except psycopg.errors.UniqueViolation as exc:
        conn.rollback()
        if exc.diag.constraint_name in {
            "courses_title_instructor_key",
            "courses_title_instructor_unique_idx",
        }:
            raise DuplicateCourseError((title, instructor)) from exc
        raise
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
