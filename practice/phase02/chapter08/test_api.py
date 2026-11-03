"""7~8강 API Contract + Transaction 테스트 (실제 DB 대신 Mock 사용).

실행: python -m unittest -v test_api.py
이 테스트만 통과해도 실 DB INSERT 성공 증거는 아닙니다.
"""

import unittest
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

import common.db as db
from chapter08.main import app


class Chapter07ApiTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def tearDown(self):
        self.client.close()

    def test_root_message(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "라면먹고갈래"})

    @patch("chapter08.main.fetch_members", return_value=[
        (1, "Kim", "kim@example.com", 25),
        (2, "Lee", "lee@example.com", 31),
    ])
    def test_get_members_from_db_rows(self, fetch):
        response = self.client.get("/members")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.json()[0]["id"], 1)
        self.assertEqual(set(response.json()[0]), {"id", "name", "email", "age"})
        fetch.assert_called_once()

    @patch("chapter08.main.find_member", return_value=(3, "Park", "park@example.com", 28))
    def test_get_member_by_id(self, find):
        response = self.client.get("/members/3")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["email"], "park@example.com")
        find.assert_called_once_with(3)

    @patch("chapter08.main.find_member", return_value=None)
    def test_get_member_unknown_404(self, find):
        self.assertEqual(self.client.get("/members/999").status_code, 404)

    @patch("chapter08.main.find_member")
    def test_get_member_invalid_id_422(self, find):
        self.assertEqual(self.client.get("/members/abc").status_code, 422)
        find.assert_not_called()

    @patch("chapter08.main.insert_member", return_value=(3, "홍길동", "hong@example.com", 27))
    def test_post_member_201(self, insert):
        data = {"name": "홍길동", "email": "hong@example.com", "age": 27}
        response = self.client.post("/members", json=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"id": 3, **data})
        insert.assert_called_once_with("홍길동", "hong@example.com", 27)

    @patch("chapter08.main.insert_member", side_effect=db.DuplicateEmailError("duplicate"))
    def test_post_duplicate_email_409(self, insert):
        response = self.client.post("/members", json={
            "name": "Kim", "email": "kim@example.com", "age": 25
        })
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json()["detail"], "이미 등록된 이메일입니다.")

    @patch("chapter08.main.insert_member")
    def test_post_member_invalid_email_422_before_insert(self, insert):
        response = self.client.post("/members", json={
            "name": "Kim", "email": "not-email", "age": 25
        })
        self.assertEqual(response.status_code, 422)
        insert.assert_not_called()

    @patch("chapter08.main.insert_member")
    def test_post_member_out_of_range_age_422(self, insert):
        response = self.client.post("/members", json={
            "name": "Kim", "email": "kim@example.com", "age": 151
        })
        self.assertEqual(response.status_code, 422)
        insert.assert_not_called()

    @patch("chapter08.main.insert_member")
    def test_post_member_empty_name_422(self, insert):
        response = self.client.post("/members", json={
            "name": "", "email": "kim@example.com", "age": 25
        })
        self.assertEqual(response.status_code, 422)
        insert.assert_not_called()

    @patch("chapter08.main.insert_member", side_effect=RuntimeError("forced SQL error"))
    def test_post_member_db_failure_500(self, insert):
        response = self.client.post("/members", json={
            "name": "Park", "email": "park@example.com", "age": 30
        })
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json()["detail"], "회원 등록 중 오류가 발생했습니다.")
        self.assertNotIn("forced SQL error", response.text)

    @patch("chapter08.main.fetch_courses", return_value=[
        (1, "Database", "Kim", 30)
    ])
    def test_get_courses(self, fetch):
        response = self.client.get("/courses")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]["title"], "Database")

    @patch("chapter08.main.find_course", return_value=None)
    def test_missing_course_404(self, find):
        self.assertEqual(self.client.get("/courses/99").status_code, 404)

    @patch("chapter08.main.insert_course", return_value=(3, "FastAPI Basic", "Kim", 30))
    def test_post_course_201(self, insert):
        body = {"title": "FastAPI Basic", "instructor": "Kim", "capacity": 30}
        response = self.client.post("/courses", json=body)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"id": 3, **body})
        insert.assert_called_once_with("FastAPI Basic", "Kim", 30)

    @patch("chapter08.main.insert_course", side_effect=db.DuplicateCourseError("duplicate"))
    def test_post_course_duplicate_409(self, insert):
        response = self.client.post("/courses", json={
            "title": "FastAPI Basic", "instructor": "Kim", "capacity": 30
        })
        self.assertEqual(response.status_code, 409)

    @patch("chapter08.main.insert_course")
    def test_post_course_bad_capacity_422(self, insert):
        response = self.client.post("/courses", json={
            "title": "FastAPI Basic", "instructor": "Kim", "capacity": "oops"
        })
        self.assertEqual(response.status_code, 422)
        insert.assert_not_called()

    @patch("chapter08.main.insert_course", side_effect=RuntimeError("forced SQL error"))
    def test_post_course_db_failure_500(self, insert):
        response = self.client.post("/courses", json={
            "title": "FastAPI Basic", "instructor": "Kim", "capacity": 30
        })
        self.assertEqual(response.status_code, 500)

    def test_openapi_contract(self):
        schema = self.client.get("/openapi.json").json()
        self.assertIn("post", schema["paths"]["/members"])
        self.assertNotIn("/courses", schema["paths"])
        self.assertIn("201", schema["paths"]["/members"]["post"]["responses"])
        self.assertIn("MemberCreate", schema["components"]["schemas"])


class DatabaseTransactionTests(unittest.TestCase):
    def fake_connection(self):
        conn = MagicMock()
        cur = MagicMock()
        conn.cursor.return_value.__enter__.return_value = cur
        return conn, cur

    @patch("common.db.get_connection")
    def test_member_insert_commits_and_closes(self, connect):
        conn, cur = self.fake_connection()
        connect.return_value = conn
        cur.fetchone.side_effect = [
            None, (11, "Test", "test@example.com", 22)
        ]
        row = db.insert_member("Test", "test@example.com", 22)
        self.assertEqual(row[0], 11)
        self.assertEqual(cur.execute.call_count, 2)
        self.assertEqual(
            cur.execute.call_args_list[1].args[1],
            ("Test", "test@example.com", 22),
        )
        self.assertIn("%s", cur.execute.call_args_list[1].args[0])
        conn.commit.assert_called_once()
        conn.rollback.assert_not_called()
        conn.close.assert_called_once()

    @patch("common.db.get_connection")
    def test_member_duplicate_rolls_back(self, connect):
        conn, cur = self.fake_connection()
        connect.return_value = conn
        cur.fetchone.return_value = (5,)
        with self.assertRaises(db.DuplicateEmailError):
            db.insert_member("Kim", "kim@example.com", 25)
        self.assertEqual(cur.execute.call_count, 1)
        conn.rollback.assert_called_once()
        conn.commit.assert_not_called()
        conn.close.assert_called_once()

    @patch("common.db.get_connection")
    def test_member_sql_error_rolls_back(self, connect):
        conn, cur = self.fake_connection()
        connect.return_value = conn
        cur.execute.side_effect = RuntimeError("forced SQL error")
        with self.assertRaises(RuntimeError):
            db.insert_member("Kim", "kim@example.com", 25)
        conn.rollback.assert_called_once()
        conn.commit.assert_not_called()
        conn.close.assert_called_once()

    @patch("common.db.get_connection")
    def test_course_insert_commits(self, connect):
        conn, cur = self.fake_connection()
        connect.return_value = conn
        cur.fetchone.side_effect = [None, (7, "FastAPI", "Kim", 30)]
        row = db.insert_course("FastAPI", "Kim", 30)
        self.assertEqual(row[0], 7)
        self.assertEqual(cur.execute.call_args_list[1].args[1], ("FastAPI", "Kim", 30))
        conn.commit.assert_called_once()
        conn.rollback.assert_not_called()
        conn.close.assert_called_once()

    @patch("common.db.get_connection")
    def test_course_duplicate_rolls_back(self, connect):
        conn, cur = self.fake_connection()
        connect.return_value = conn
        cur.fetchone.return_value = (7,)
        with self.assertRaises(db.DuplicateCourseError):
            db.insert_course("FastAPI", "Kim", 30)
        conn.rollback.assert_called_once()
        conn.commit.assert_not_called()
        conn.close.assert_called_once()




class Chapter08MemberUpdateTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def tearDown(self):
        self.client.close()

    @patch("chapter08.main.storage.update_member_fields", return_value=(1, "새 이름", "new@example.com", 31))
    def test_put_member_200_full_update(self, update):
        payload = {"name": "새 이름", "email": "new@example.com", "age": 31}
        response = self.client.put("/members/1", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"id": 1, **payload})
        update.assert_called_once_with(1, payload)

    @patch("chapter08.main.storage.update_member_fields")
    def test_put_missing_field_is_422(self, update):
        response = self.client.put("/members/1", json={
            "name": "Kim", "email": "kim@example.com"
        })
        self.assertEqual(response.status_code, 422)
        update.assert_not_called()

    @patch("chapter08.main.storage.update_member_fields")
    def test_put_wrong_age_is_422(self, update):
        response = self.client.put("/members/1", json={
            "name": "Kim", "email": "kim@example.com", "age": -1
        })
        self.assertEqual(response.status_code, 422)
        update.assert_not_called()

    @patch("chapter08.main.storage.update_member_fields", return_value=(1, "Kim", "kim@example.com", 31))
    def test_patch_only_age_changed(self, update):
        response = self.client.patch("/members/1", json={"age": 31})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "id": 1, "name": "Kim", "email": "kim@example.com", "age": 31
        })
        update.assert_called_once_with(1, {"age": 31})

    @patch("chapter08.main.storage.update_member_fields")
    def test_patch_empty_400(self, update):
        response = self.client.patch("/members/1", json={})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "At least one field is required")
        update.assert_not_called()

    @patch("chapter08.main.storage.update_member_fields")
    def test_patch_explicit_null_422(self, update):
        for field in ("name", "email", "age"):
            with self.subTest(field=field):
                response = self.client.patch("/members/1", json={field: None})
                self.assertEqual(response.status_code, 422)
        update.assert_not_called()

    @patch("chapter08.main.storage.update_member_fields")
    def test_patch_extra_field_422(self, update):
        self.assertEqual(
            self.client.patch("/members/1", json={"admin": True}).status_code, 422
        )
        update.assert_not_called()

    @patch("chapter08.main.storage.update_member_fields")
    def test_patch_bad_email_422(self, update):
        self.assertEqual(
            self.client.patch("/members/1", json={"email": "not-email"}).status_code, 422
        )
        update.assert_not_called()

    @patch("chapter08.main.storage.update_member_fields", side_effect=db.MemberNotFound())
    def test_put_missing_id_404(self, update):
        response = self.client.put("/members/999", json={
            "name": "Kim", "email": "kim@example.com", "age": 20
        })
        self.assertEqual(response.status_code, 404)

    @patch("chapter08.main.storage.update_member_fields", side_effect=db.MemberNotFound())
    def test_patch_missing_id_404(self, update):
        self.assertEqual(
            self.client.patch("/members/999", json={"age": 31}).status_code, 404
        )

    @patch("chapter08.main.storage.update_member_fields", side_effect=db.DuplicateEmailError("dup"))
    def test_put_conflicting_email_409(self, update):
        response = self.client.put("/members/1", json={
            "name": "Kim", "email": "taken@example.com", "age": 20
        })
        self.assertEqual(response.status_code, 409)

    @patch("chapter08.main.storage.update_member_fields", side_effect=db.DuplicateEmailError("dup"))
    def test_patch_conflicting_email_409(self, update):
        self.assertEqual(
            self.client.patch("/members/1", json={"email": "taken@example.com"}).status_code,
            409
        )

    @patch("chapter08.main.storage.update_member_fields", side_effect=RuntimeError("secret SQL error"))
    def test_patch_database_error_500_without_sql_leak(self, update):
        response = self.client.patch("/members/1", json={"age": 31})
        self.assertEqual(response.status_code, 500)
        self.assertNotIn("secret SQL error", response.text)


class Chapter08CourseUpdateTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def tearDown(self):
        self.client.close()

    @patch("chapter08.main.storage.update_course_fields", return_value=(2, "FastAPI Advanced", "Lee", 42))
    def test_put_course_200(self, update):
        payload = {"title": "FastAPI Advanced", "instructor": "Lee", "capacity": 42}
        response = self.client.put("/courses/2", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"id": 2, **payload})
        update.assert_called_once_with(2, payload)

    @patch("chapter08.main.storage.update_course_fields", return_value=(2, "FastAPI Basic", "Kim", 20))
    def test_patch_course_only_capacity(self, update):
        response = self.client.patch("/courses/2", json={"capacity": 20})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["instructor"], "Kim")
        update.assert_called_once_with(2, {"capacity": 20})

    @patch("chapter08.main.storage.update_course_fields")
    def test_patch_course_empty_400_and_null_422(self, update):
        self.assertEqual(self.client.patch("/courses/2", json={}).status_code, 400)
        for field in ("title", "instructor", "capacity"):
            self.assertEqual(self.client.patch("/courses/2", json={field: None}).status_code, 422)
        update.assert_not_called()

    @patch("chapter08.main.storage.update_course_fields")
    def test_put_course_missing_capacity_422(self, update):
        response = self.client.put("/courses/2", json={
            "title": "FastAPI Basic", "instructor": "Kim"
        })
        self.assertEqual(response.status_code, 422)
        update.assert_not_called()

    @patch("chapter08.main.storage.update_course_fields", side_effect=db.CourseNotFound())
    def test_patch_unknown_course_404(self, update):
        self.assertEqual(self.client.patch("/courses/999", json={"capacity": 20}).status_code, 404)

    @patch("chapter08.main.storage.update_course_fields", side_effect=db.DuplicateCourseError("dup"))
    def test_patch_course_conflict_409(self, update):
        self.assertEqual(
            self.client.patch("/courses/2", json={"title": "Duplicate"}).status_code, 409
        )

    def test_openapi_put_patch_available(self):
        data = self.client.get("/openapi.json").json()
        for path in ("/members/{member_id}",):
            self.assertIn("put", data["paths"][path])
            self.assertIn("patch", data["paths"][path])
        self.assertIn("MemberPatch", data["components"]["schemas"])
        self.assertNotIn("/courses/{course_id}", data["paths"])


class Chapter08SqlTransactionTests(unittest.TestCase):
    def fake_db(self):
        conn = MagicMock()
        cur = MagicMock()
        conn.cursor.return_value.__enter__.return_value = cur
        return conn, cur

    @patch("common.db.get_connection")
    def test_put_member_commit_and_parameterized_update(self, connect):
        conn, cur = self.fake_db()
        connect.return_value = conn
        cur.fetchone.side_effect = [
            (3, "Kim", "kim@example.com", 20), None,
            (3, "Updated", "new@example.com", 21)
        ]
        changes = {"name": "Updated", "email": "new@example.com", "age": 21}
        row = db.update_member_fields(3, changes)
        self.assertEqual(row[1], "Updated")
        self.assertEqual(cur.execute.call_count, 3)
        sql, params = cur.execute.call_args.args
        self.assertIn("UPDATE public.members", sql)
        self.assertIn("RETURNING id, name, email, age", sql)
        self.assertEqual(params, ("Updated", "new@example.com", 21, 3))
        conn.commit.assert_called_once()
        conn.rollback.assert_not_called()
        conn.close.assert_called_once()

    @patch("common.db.get_connection")
    def test_patch_only_age_updates_one_column(self, connect):
        conn, cur = self.fake_db()
        connect.return_value = conn
        cur.fetchone.side_effect = [
            (3, "Kim", "kim@example.com", 20),
            (3, "Kim", "kim@example.com", 31)
        ]
        db.update_member_fields(3, {"age": 31})
        self.assertEqual(cur.execute.call_count, 2)
        sql, params = cur.execute.call_args.args
        self.assertIn("SET age = %s", sql)
        self.assertNotIn("SET name =", sql)
        self.assertEqual(params, (31, 3))
        conn.commit.assert_called_once()

    @patch("common.db.get_connection")
    def test_missing_member_rollback(self, connect):
        conn, cur = self.fake_db()
        connect.return_value = conn
        cur.fetchone.return_value = None
        with self.assertRaises(db.MemberNotFound):
            db.update_member_fields(999, {"age": 22})
        conn.rollback.assert_called_once()
        conn.commit.assert_not_called()
        conn.close.assert_called_once()

    @patch("common.db.get_connection")
    def test_email_conflict_excludes_self(self, connect):
        conn, cur = self.fake_db()
        connect.return_value = conn
        cur.fetchone.side_effect = [
            (3, "Kim", "kim@example.com", 20),
            (4,)
        ]
        with self.assertRaises(db.DuplicateEmailError):
            db.update_member_fields(3, {"email": "taken@example.com"})
        self.assertEqual(
            cur.execute.call_args.args[1],
            ("taken@example.com", 3),
        )
        conn.rollback.assert_called_once()
        conn.commit.assert_not_called()

    @patch("common.db.get_connection")
    def test_update_error_rolls_back(self, connect):
        conn, cur = self.fake_db()
        connect.return_value = conn
        cur.fetchone.return_value = (3, "Kim", "kim@example.com", 20)
        cur.execute.side_effect = [None, RuntimeError("bad UPDATE")]
        with self.assertRaises(RuntimeError):
            db.update_member_fields(3, {"age": 31})
        conn.rollback.assert_called_once()
        conn.commit.assert_not_called()
        conn.close.assert_called_once()

    @patch("common.db.get_connection")
    def test_course_partial_title_checks_combined_fields(self, connect):
        conn, cur = self.fake_db()
        connect.return_value = conn
        cur.fetchone.side_effect = [
            (7, "Before", "Kim", 30), None,
            (7, "After", "Kim", 30)
        ]
        row = db.update_course_fields(7, {"title": "After"})
        self.assertEqual(row[1], "After")
        self.assertEqual(
            cur.execute.call_args_list[1].args[1], ("After", "Kim", 7)
        )
        sql, params = cur.execute.call_args.args
        self.assertIn("SET title = %s", sql)
        self.assertEqual(params, ("After", 7))
        conn.commit.assert_called_once()

    @patch("common.db.get_connection")
    def test_course_missing_rolls_back(self, connect):
        conn, cur = self.fake_db()
        connect.return_value = conn
        cur.fetchone.return_value = None
        with self.assertRaises(db.CourseNotFound):
            db.update_course_fields(9, {"capacity": 33})
        conn.rollback.assert_called_once()
        conn.commit.assert_not_called()

    def test_column_allowlist_rejects_untrusted_field(self):
        with self.assertRaises(ValueError):
            db._safe_set_clause({"age;DROP TABLE public.members": 20}, {"age"})
        with self.assertRaises(ValueError):
            db._safe_set_clause({}, {"age"})


if __name__ == "__main__":
    unittest.main()
