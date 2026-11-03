"""8강: INSERT, PUT/PATCH UPDATE와 PostgreSQL 트랜잭션 접근 함수."""

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


# ------------------------------------------------------------
# 8강: Transaction 안에서 기존 행 조회 → 중복 검사 → UPDATE
# ------------------------------------------------------------

class MemberNotFound(Exception):
    """수정하려는 회원이 DB에 존재하지 않습니다."""


class CourseNotFound(Exception):
    """수정하려는 강좌가 DB에 존재하지 않습니다."""


def _safe_set_clause(changes: dict, allowed_columns: set[str]):
    """코드에서 허용한 컬럼명만 조합하고 값은 %s로 따로 전달."""
    if not changes or not set(changes).issubset(allowed_columns):
        raise ValueError("Invalid update fields")
    return ", ".join(f"{field} = %s" for field in changes)


def update_member_fields(member_id: int, changes: dict):
    """행 잠금, 변경 대상 존재/중복 확인, UPDATE RETURNING, commit/rollback."""
    set_clause = _safe_set_clause(changes, {"name", "email", "age"})
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, name, email, age FROM public.members "
                "WHERE id = %s FOR UPDATE;",
                (member_id,),
            )
            if cur.fetchone() is None:
                raise MemberNotFound(member_id)

            if "email" in changes:
                cur.execute(
                    "SELECT id FROM public.members WHERE email = %s AND id <> %s;",
                    (str(changes["email"]), member_id),
                )
                if cur.fetchone() is not None:
                    raise DuplicateEmailError(changes["email"])

            sql = (
                f"UPDATE public.members SET {set_clause} WHERE id = %s "
                "RETURNING id, name, email, age;"
            )
            params = tuple(changes.values()) + (member_id,)
            cur.execute(sql, params)
            updated = cur.fetchone()
            if updated is None:
                raise MemberNotFound(member_id)

        conn.commit()
        return updated
    except psycopg.errors.UniqueViolation as exc:
        conn.rollback()
        if exc.diag.constraint_name in {"members_email_key", "members_email_unique_idx"}:
            raise DuplicateEmailError(changes.get("email")) from exc
        raise
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def update_course_fields(course_id: int, changes: dict):
    """강좌 수정 과제: 중복 기준은 (title, instructor) 조합."""
    set_clause = _safe_set_clause(changes, {"title", "instructor", "capacity"})
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, title, instructor, capacity FROM public.courses "
                "WHERE id = %s FOR UPDATE;",
                (course_id,),
            )
            original = cur.fetchone()
            if original is None:
                raise CourseNotFound(course_id)

            # PATCH에서 한 필드만 바꾸더라도 기존 값과 조합하여 중복 확인.
            if "title" in changes or "instructor" in changes:
                title = changes.get("title", original[1])
                instructor = changes.get("instructor", original[2])
                cur.execute(
                    "SELECT id FROM public.courses "
                    "WHERE title = %s AND instructor = %s AND id <> %s;",
                    (title, instructor, course_id),
                )
                if cur.fetchone() is not None:
                    raise DuplicateCourseError((title, instructor))

            sql = (
                f"UPDATE public.courses SET {set_clause} WHERE id = %s "
                "RETURNING id, title, instructor, capacity;"
            )
            params = tuple(changes.values()) + (course_id,)
            cur.execute(sql, params)
            updated = cur.fetchone()
            if updated is None:
                raise CourseNotFound(course_id)

        conn.commit()
        return updated
    except psycopg.errors.UniqueViolation as exc:
        conn.rollback()
        if exc.diag.constraint_name in {
            "courses_title_instructor_key", "courses_title_instructor_unique_idx"
        }:
            raise DuplicateCourseError((changes.get("title"), changes.get("instructor"))) from exc
        raise
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def check_connection():
    """현재 연결된 데이터베이스와 스키마를 확인합니다."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT current_database(), current_schema();")
            return cur.fetchone()


def delete_member_by_id(member_id: int):
    """삭제 결과를 확인하고 성공 시 commit, 실패 시 rollback합니다."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM public.members WHERE id = %s RETURNING id;", (member_id,))
            row = cur.fetchone()
        if row is None:
            conn.rollback()
            return None
        conn.commit()
        return row[0]
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
