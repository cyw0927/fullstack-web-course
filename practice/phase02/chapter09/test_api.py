"""9강 회원 DELETE 단위 테스트. DB 작업은 Mock — 실제 삭제 증빙은 아님."""

import unittest
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

import db
from main import app


class DeleteApiTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def tearDown(self):
        self.client.close()

    @patch("main.storage.find_member", return_value=(11, "Test", "test@example.com", 27))
    def test_get_existing_member_returns_200(self, find):
        response = self.client.get("/members/11")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "id": 11, "name": "Test", "email": "test@example.com", "age": 27
        })
        find.assert_called_once_with(11)

    @patch("main.storage.find_member", return_value=None)
    def test_get_missing_member_returns_404(self, find):
        response = self.client.get("/members/999")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Member not found"})

    @patch("main.storage.find_member")
    def test_get_invalid_id_returns_422(self, find):
        self.assertEqual(self.client.get("/members/abc").status_code, 422)
        find.assert_not_called()

    @patch("main.storage.delete_member_by_id", return_value=11)
    def test_delete_existing_member_returns_empty_204(self, delete):
        response = self.client.delete("/members/11")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.content, b"")
        delete.assert_called_once_with(11)

    @patch("main.storage.delete_member_by_id", return_value=None)
    def test_delete_missing_member_returns_404(self, delete):
        response = self.client.delete("/members/999")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Member not found"})

    @patch("main.storage.delete_member_by_id")
    def test_delete_invalid_id_returns_422_without_sql(self, delete):
        response = self.client.delete("/members/abc")
        self.assertEqual(response.status_code, 422)
        delete.assert_not_called()

    @patch("main.storage.delete_member_by_id", side_effect=RuntimeError("secret SQL details"))
    def test_delete_db_failure_returns_500_without_leak(self, delete):
        response = self.client.delete("/members/11")
        self.assertEqual(response.status_code, 500)
        self.assertNotIn("secret SQL details", response.text)

    def test_openapi_contract(self):
        openapi = self.client.get("/openapi.json").json()
        operations = openapi["paths"]["/members/{member_id}"]
        self.assertEqual(set(operations), {"get", "delete"})
        self.assertIn("204", operations["delete"]["responses"])
        self.assertNotIn("requestBody", operations["delete"])


class DeleteDatabaseTests(unittest.TestCase):
    def mock_connection(self):
        conn = MagicMock()
        cur = MagicMock()
        conn.cursor.return_value.__enter__.return_value = cur
        return conn, cur

    @patch("db.get_connection")
    def test_delete_uses_parameterized_sql_and_commits(self, get_connection):
        conn, cur = self.mock_connection()
        get_connection.return_value = conn
        cur.fetchone.return_value = (11,)

        deleted_id = db.delete_member_by_id(11)

        self.assertEqual(deleted_id, 11)
        sql, params = cur.execute.call_args.args
        self.assertIn("DELETE FROM public.members", sql)
        self.assertIn("WHERE id = %s", sql)
        self.assertIn("RETURNING id", sql)
        self.assertEqual(params, (11,))
        conn.commit.assert_called_once_with()
        conn.rollback.assert_not_called()
        conn.close.assert_called_once_with()

    @patch("db.get_connection")
    def test_delete_not_found_rolls_back_and_closes(self, get_connection):
        conn, cur = self.mock_connection()
        get_connection.return_value = conn
        cur.fetchone.return_value = None

        result = db.delete_member_by_id(999)

        self.assertIsNone(result)
        conn.commit.assert_not_called()
        conn.rollback.assert_called_once_with()
        conn.close.assert_called_once_with()

    @patch("db.get_connection")
    def test_sql_error_rolls_back_and_closes(self, get_connection):
        conn, cur = self.mock_connection()
        get_connection.return_value = conn
        cur.execute.side_effect = RuntimeError("invalid column")

        with self.assertRaises(RuntimeError):
            db.delete_member_by_id(11)

        conn.commit.assert_not_called()
        conn.rollback.assert_called_once_with()
        conn.close.assert_called_once_with()

    @patch("db.get_connection")
    def test_commit_error_rolls_back_and_closes(self, get_connection):
        conn, cur = self.mock_connection()
        get_connection.return_value = conn
        cur.fetchone.return_value = (11,)
        conn.commit.side_effect = RuntimeError("commit failed")

        with self.assertRaises(RuntimeError):
            db.delete_member_by_id(11)

        conn.rollback.assert_called_once_with()
        conn.close.assert_called_once_with()

    @patch("db.get_connection")
    def test_fetch_member_returns_expected_tuple(self, get_connection):
        conn, cur = self.mock_connection()
        get_connection.return_value = conn
        cur.fetchone.return_value = (11, "Test", "test@example.com", 27)
        self.assertEqual(db.find_member(11), (11, "Test", "test@example.com", 27))
        self.assertEqual(cur.execute.call_args.args[1], (11,))


if __name__ == "__main__":
    unittest.main()
