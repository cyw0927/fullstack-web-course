"""Chapter 01 API Contract 자동 검증: python -m unittest -v test_api.py"""

import unittest

from fastapi.testclient import TestClient

from main import app


class ApiContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_root_message(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "라면먹고갈래"})

    def test_members_contract(self):
        response = self.client.get("/members")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [
            {"id": 1, "name": "Kim", "email": "kim@example.com"},
            {"id": 2, "name": "Lee", "email": "lee@example.com"},
        ])

    def test_courses_contract(self):
        response = self.client.get("/courses")
        self.assertEqual(response.status_code, 200)
        courses = response.json()
        self.assertGreaterEqual(len(courses), 3)
        self.assertEqual(courses[:2], [
            {"id": 1, "title": "Database", "instructor": "Kim"},
            {"id": 2, "title": "Frontend", "instructor": "Lee"},
        ])
        self.assertEqual([item["id"] for item in courses], [1, 2, 3])
        for course in courses:
            self.assertEqual(set(course), {"id", "title", "instructor"})
            self.assertIsInstance(course["id"], int)
            self.assertIsInstance(course["title"], str)
            self.assertIsInstance(course["instructor"], str)

    def test_swagger_ui_and_openapi(self):
        response = self.client.get("/docs")
        self.assertEqual(response.status_code, 200)
        spec = self.client.get("/openapi.json")
        self.assertEqual(spec.status_code, 200)
        for path in ("/", "/members", "/courses"):
            self.assertIn("get", spec.json()["paths"][path])


if __name__ == "__main__":
    unittest.main()
