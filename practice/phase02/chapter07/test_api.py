"""7강 API Contract + Transaction 테스트 (실제 DB 대신 Mock 사용).

실행: python -m unittest -v test_api.py
이 테스트만 통과해도 실 DB INSERT 성공 증거는 아닙니다.
"""

import unittest
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

import db
from main import app


class Chapter07ApiTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def tearDown(self):
        self.client.close()

    def test_root_message(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "라면먹고갈래"})

    @patch("main.fetch_members", return_value=[
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

    @patch("main.find_member", return_value=(3, "Park", "park@example.com", 28))
    def test_get_member_by_id(self, find):
        response = self.client.get("/members/3")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["email"], "park@example.com")
        find.assert_called_once_with(3)

    @patch("main.find_member", return_value=None)
    def test_get_member_unknown_404(self, find):
        self.assertEqual(self.client.get("/members/999").status_code, 404)

    @patch("main.find_member")
    def test_get_member_invalid_id_422(self, find):
        self.assertEqual(self.client.get("/members/abc").status_code, 422)
        find.assert_not_called()

    @patch("main.insert_member", return_value=(3, "홍길동", "hong@example.com", 27))
    def test_post_member_201(self, insert):
        data = {"name": "홍길동", "email": "hong@example.com", "age": 27}
        response = self.client.post("/members", json=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"id": 3, **data})
        insert.assert_called_once_with("홍길동", "hong@example.com", 27)

    @patch("main.insert_member", side_effect=db.DuplicateEmailError("duplicate"))
    def test_post_duplicate_email_409(self, insert):
        response = self.client.post("/members", json={
            "name": "Kim", "email": "kim@example.com", "age": 25
        })
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json()["detail"], "이미 등록된 이메일입니다.")

    @patch("main.insert_member")
    def test_post_member_invalid_email_422_before_insert(self, insert):
        response = self.client.post("/members", json={
            "name": "Kim", "email": "not-email", "age": 25
        })
        self.assertEqual(response.status_code, 422)
        insert.assert_not_called()

    @patch("main.insert_member")
    def test_post_member_out_of_range_age_422(self, insert):
        response = self.client.post("/members", json={
            "name": "Kim", "email": "kim@example.com", "age": 151
        })
        self.assertEqual(response.status_code, 422)
        insert.assert_not_called()

    @patch("main.insert_member")
    def test_post_member_empty_name_422(self, insert):
        response = self.client.post("/members", json={
            "name": "", "email": "kim@example.com", "age": 25
        })
        self.assertEqual(response.status_code, 422)
        insert.assert_not_called()

    @patch("main.insert_member", side_effect=RuntimeError("forced SQL error"))
    def test_post_member_db_failure_500(self, insert):
        response = self.client.post("/members", json={
            "name": "Park", "email": "park@example.com", "age": 30
        })
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json()["detail"], "회원 등록 중 오류가 발생했습니다.")
        self.assertNotIn("forced SQL error", response.text)

    @patch("main.fetch_courses", return_value=[
        (1, "Database", "Kim", 30)
    ])
    def test_get_courses(self, fetch):
        response = self.client.get("/courses")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]["title"], "Database")

    @patch("main.find_course", return_value=None)
    def test_missing_course_404(self, find):
        self.assertEqual(self.client.get("/courses/99").status_code, 404)

    @patch("main.insert_course", return_value=(3, "FastAPI Basic", "Kim", 30))
    def test_post_course_201(self, insert):
        body = {"title": "FastAPI Basic", "instructor": "Kim", "capacity": 30}
        response = self.client.post("/courses", json=body)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"id": 3, **body})
        insert.assert_called_once_with("FastAPI Basic", "Kim", 30)

    @patch("main.insert_course", side_effect=db.DuplicateCourseError("duplicate"))
    def test_post_course_duplicate_409(self, insert):
        response = self.client.post("/courses", json={
            "title": "FastAPI Basic", "instructor": "Kim", "capacity": 30
        })
        self.assertEqual(response.status_code, 409)

    @patch("main.insert_course")
    def test_post_course_bad_capacity_422(self, insert):
        response = self.client.post("/courses", json={
            "title": "FastAPI Basic", "instructor": "Kim", "capacity": "oops"
        })
        self.assertEqual(response.status_code, 422)
        insert.assert_not_called()

    @patch("main.insert_course", side_effect=RuntimeError("forced SQL error"))
    def test_post_course_db_failure_500(self, insert):
        response = self.client.post("/courses", json={
            "title": "FastAPI Basic", "instructor": "Kim", "capacity": 30
        })
        self.assertEqual(response.status_code, 500)

    def test_openapi_contract(self):
        schema = self.client.get("/openapi.json").json()
        self.assertIn("post", schema["paths"]["/members"])
        self.assertIn("post", schema["paths"]["/courses"])
        self.assertIn("201", schema["paths"]["/members"]["post"]["responses"])
        self.assertIn("MemberCreate", schema["components"]["schemas"])
        self.assertIn("CourseResponse", schema["components"]["schemas"])


class DatabaseTransactionTests(unittest.TestCase):
    def fake_connection(self):
        conn = MagicMock()
        cur = MagicMock()
        conn.cursor.return_value.__enter__.return_value = cur
        return conn, cur

    @patch("db.get_connection")
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

    @patch("db.get_connection")
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

    @patch("db.get_connection")
    def test_member_sql_error_rolls_back(self, connect):
        conn, cur = self.fake_connection()
        connect.return_value = conn
        cur.execute.side_effect = RuntimeError("forced SQL error")
        with self.assertRaises(RuntimeError):
            db.insert_member("Kim", "kim@example.com", 25)
        conn.rollback.assert_called_once()
        conn.commit.assert_not_called()
        conn.close.assert_called_once()

    @patch("db.get_connection")
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

    @patch("db.get_connection")
    def test_course_duplicate_rolls_back(self, connect):
        conn, cur = self.fake_connection()
        connect.return_value = conn
        cur.fetchone.return_value = (7,)
        with self.assertRaises(db.DuplicateCourseError):
            db.insert_course("FastAPI", "Kim", 30)
        conn.rollback.assert_called_once()
        conn.commit.assert_not_called()
        conn.close.assert_called_once()


if __name__ == "__main__":
    unittest.main()
