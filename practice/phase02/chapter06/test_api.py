"""Offline contract tests. Mocks DB calls; NOT proof of a real INSERT.

Run in chapter06: python -m unittest -v test_api.py
"""

import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from chapter06.main import app

client = TestClient(app)


class MemberApiContractTests(unittest.TestCase):
    def test_read_root(self):
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "라면먹고갈래"})

    @patch("chapter06.main.fetch_members", return_value=[])
    def test_get_empty_list(self, fake_fetch):
        response = client.get("/members")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])
        fake_fetch.assert_called_once_with()

    @patch("chapter06.main.fetch_members", return_value=[
        (1, "Kim", "kim@example.com", 25),
        (2, "Lee", "lee@example.com", 31),
    ])
    def test_get_member_list(self, fake_fetch):
        response = client.get("/members")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [
            {"id": 1, "name": "Kim", "email": "kim@example.com", "age": 25},
            {"id": 2, "name": "Lee", "email": "lee@example.com", "age": 31},
        ])
        fake_fetch.assert_called_once_with()

    @patch("chapter06.main.insert_member", return_value=(5, "홍길동", "hong2026@example.com", 30))
    def test_post_members_returns_201(self, fake_insert):
        payload = {"name": "홍길동", "email": "hong2026@example.com", "age": 30}
        response = client.post("/members", json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"id": 5, **payload})
        fake_insert.assert_called_once_with("홍길동", "hong2026@example.com", 30)

    @patch("chapter06.main.insert_member")
    def test_post_missing_age_returns_422(self, fake_insert):
        response = client.post("/members", json={"name": "A", "email": "a@example.com"})
        self.assertEqual(response.status_code, 422)
        fake_insert.assert_not_called()

    @patch("chapter06.main.insert_member")
    def test_post_bad_age_returns_422(self, fake_insert):
        response = client.post("/members", json={
            "name": "A", "email": "a@example.com", "age": "not-a-number",
        })
        self.assertEqual(response.status_code, 422)
        fake_insert.assert_not_called()

    @patch("chapter06.main.insert_member")
    def test_post_missing_email_returns_422(self, fake_insert):
        response = client.post("/members", json={"name": "A", "age": 20})
        self.assertEqual(response.status_code, 422)
        fake_insert.assert_not_called()

    def test_openapi_get_post_and_schemas(self):
        schema = client.get("/openapi.json").json()
        self.assertIn("get", schema["paths"]["/members"])
        self.assertIn("post", schema["paths"]["/members"])
        self.assertIn("201", schema["paths"]["/members"]["post"]["responses"])
        self.assertIn("MemberCreate", schema["components"]["schemas"])
        self.assertIn("MemberResponse", schema["components"]["schemas"])


if __name__ == "__main__":
    unittest.main()
