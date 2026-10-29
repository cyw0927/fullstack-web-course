"""Chapter 02 API Contract 자동 검증: python -m unittest -v test_api.py"""

import unittest

from fastapi.testclient import TestClient

from main import app


class Chapter02ApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_root_message(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "라면먹고갈래"})

    def test_member_list_returns_three(self):
        response = self.client.get("/members")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)
        self.assertEqual(set(response.json()[0]), {"id", "name", "email", "age"})

    def test_member_detail_success_200(self):
        response = self.client.get("/members/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"id": 1, "name": "Kim", "email": "kim@example.com", "age": 25})

    def test_member_detail_not_found_404(self):
        response = self.client.get("/members/99")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Member not found"})

    def test_member_detail_invalid_type_422(self):
        response = self.client.get("/members/abc")
        self.assertEqual(response.status_code, 422)
        self.assertTrue(response.json()["detail"])

    def test_member_search_case_insensitive(self):
        response = self.client.get("/members/search/", params={"name": "kIm"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual([row["name"] for row in response.json()], ["Kim"])

    def test_member_search_unknown_is_empty_200(self):
        response = self.client.get("/members/search/", params={"name": "unknown"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_member_filter_min_age(self):
        response = self.client.get("/members/filter/", params={"min_age": 20})
        self.assertEqual(response.status_code, 200)
        self.assertEqual([row["id"] for row in response.json()], [1, 3])

    def test_member_filter_both_and_order_independent(self):
        for path in ("/members/filter/?name=k&min_age=20", "/members/filter/?min_age=20&name=k"):
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 200)
                self.assertEqual([row["id"] for row in response.json()], [1, 3])

    def test_member_list_optional_queries(self):
        response = self.client.get("/members", params={"name": "LEE", "min_age": 18})
        self.assertEqual(response.status_code, 200)
        self.assertEqual([row["id"] for row in response.json()], [2])

    def test_member_filter_invalid_age_422(self):
        response = self.client.get("/members/filter/", params={"min_age": "abc"})
        self.assertEqual(response.status_code, 422)

    def test_course_list_three(self):
        response = self.client.get("/courses")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)
        self.assertEqual(set(response.json()[0]), {"id", "title", "level"})

    def test_course_detail_success_200(self):
        response = self.client.get("/courses/2")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"id": 2, "title": "Frontend", "level": 2})

    def test_course_detail_not_found_404(self):
        response = self.client.get("/courses/99")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Course not found"})

    def test_course_detail_invalid_type_422(self):
        response = self.client.get("/courses/abc")
        self.assertEqual(response.status_code, 422)
        self.assertTrue(response.json()["detail"])

    def test_course_filter_title_case_insensitive(self):
        response = self.client.get("/courses/filter/", params={"title": "front"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual([row["id"] for row in response.json()], [2])

    def test_course_filter_level_two(self):
        response = self.client.get("/courses/filter/", params={"level": 2})
        self.assertEqual(response.status_code, 200)
        self.assertEqual([row["id"] for row in response.json()], [2, 3])

    def test_course_filter_combined_and_invalid_level(self):
        response = self.client.get("/courses/filter/", params={"title": "api", "level": 2})
        self.assertEqual(response.status_code, 200)
        self.assertEqual([row["id"] for row in response.json()], [3])
        self.assertEqual(self.client.get("/courses/filter/", params={"level": "abc"}).status_code, 422)

    def test_swagger_and_openapi(self):
        response = self.client.get("/docs")
        self.assertEqual(response.status_code, 200)
        schema_response = self.client.get("/openapi.json")
        self.assertEqual(schema_response.status_code, 200)
        schema = schema_response.json()
        expected = ("/members", "/members/{member_id}", "/members/search/", "/members/filter/",
                    "/courses", "/courses/{course_id}", "/courses/filter/")
        for path in expected:
            with self.subTest(path=path):
                self.assertIn(path, schema["paths"])
                self.assertIn("get", schema["paths"][path])


if __name__ == "__main__":
    unittest.main()
