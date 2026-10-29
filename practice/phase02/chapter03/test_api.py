"""Chapter 03 Request Body/Validation tests: python -m unittest -v test_api.py"""

import unittest

from fastapi.testclient import TestClient

from main import app


class Chapter03ApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_root_message_is_preserved(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "라면먹고갈래"})

    def test_member_get_list_from_chapter02(self):
        response = self.client.get("/members")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)

    def test_member_get_id_from_chapter02(self):
        self.assertEqual(self.client.get("/members/1").json()["name"], "Kim")

    def test_member_get_missing_from_chapter02(self):
        response = self.client.get("/members/99")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Member not found"})

    def test_member_get_bad_id_from_chapter02(self):
        self.assertEqual(self.client.get("/members/abc").status_code, 422)

    def test_member_query_from_chapter02(self):
        response = self.client.get("/members/filter/", params={"name": "k", "min_age": 20})
        self.assertEqual(response.status_code, 200)
        self.assertEqual([m["id"] for m in response.json()], [1, 3])

    def test_member_post_valid_returns_201_with_id(self):
        body = {"name": "Hong Gil Dong", "email": "hong@example.com", "age": 30}
        response = self.client.post("/members", json=body)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"id": 4, **body})

    def test_member_post_missing_email_returns_422(self):
        response = self.client.post("/members", json={"name": "Hong Gil Dong", "age": 30})
        self.assertEqual(response.status_code, 422)
        self.assertTrue(any(item["loc"] == ["body", "email"] for item in response.json()["detail"]))

    def test_member_post_invalid_age_returns_422(self):
        body = {"name": "Hong Gil Dong", "email": "hong@example.com", "age": "not-a-number"}
        response = self.client.post("/members", json=body)
        self.assertEqual(response.status_code, 422)
        self.assertTrue(any(item["loc"] == ["body", "age"] for item in response.json()["detail"]))

    def test_member_post_missing_name_returns_422(self):
        response = self.client.post("/members", json={"email": "hong@example.com", "age": 30})
        self.assertEqual(response.status_code, 422)
        self.assertTrue(any(item["loc"] == ["body", "name"] for item in response.json()["detail"]))

    def test_member_post_missing_body_returns_422(self):
        self.assertEqual(self.client.post("/members").status_code, 422)

    def test_course_get_list_from_chapter02(self):
        response = self.client.get("/courses")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)

    def test_course_get_detail_from_chapter02(self):
        response = self.client.get("/courses/2")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"id": 2, "title": "Frontend", "level": 2})

    def test_course_get_missing_from_chapter02(self):
        self.assertEqual(self.client.get("/courses/99").status_code, 404)

    def test_course_get_bad_id_from_chapter02(self):
        self.assertEqual(self.client.get("/courses/abc").status_code, 422)

    def test_course_query_from_chapter02(self):
        response = self.client.get("/courses/filter/", params={"level": 2})
        self.assertEqual(response.status_code, 200)
        self.assertEqual([c["id"] for c in response.json()], [2, 3])

    def test_course_post_valid_returns_201_with_id(self):
        body = {"title": "Backend", "instructor": "Park", "capacity": 20}
        response = self.client.post("/courses", json=body)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"id": 4, **body})

    def test_course_post_missing_title_returns_422(self):
        response = self.client.post("/courses", json={"instructor": "Park", "capacity": 20})
        self.assertEqual(response.status_code, 422)
        self.assertTrue(any(item["loc"] == ["body", "title"] for item in response.json()["detail"]))

    def test_course_post_invalid_capacity_returns_422(self):
        body = {"title": "Backend", "instructor": "Park", "capacity": "not-a-number"}
        response = self.client.post("/courses", json=body)
        self.assertEqual(response.status_code, 422)
        self.assertTrue(any(item["loc"] == ["body", "capacity"] for item in response.json()["detail"]))

    def test_course_post_missing_instructor_returns_422(self):
        response = self.client.post("/courses", json={"title": "Backend", "capacity": 20})
        self.assertEqual(response.status_code, 422)
        self.assertTrue(any(item["loc"] == ["body", "instructor"] for item in response.json()["detail"]))

    def test_course_post_missing_body_returns_422(self):
        self.assertEqual(self.client.post("/courses").status_code, 422)

    def test_posts_do_not_mutate_in_memory_get_lists(self):
        self.client.post("/members", json={"name": "Test", "email": "test@example.com", "age": 22})
        self.client.post("/courses", json={"title": "Test", "instructor": "X", "capacity": 10})
        self.assertEqual(len(self.client.get("/members").json()), 3)
        self.assertEqual(len(self.client.get("/courses").json()), 3)

    def test_swagger_exposes_post_and_schemas(self):
        self.assertEqual(self.client.get("/docs").status_code, 200)
        response = self.client.get("/openapi.json")
        self.assertEqual(response.status_code, 200)
        schema = response.json()
        for path, model in (("/members", "MemberCreate"), ("/courses", "CourseCreate")):
            with self.subTest(path=path):
                self.assertIn("post", schema["paths"][path])
                op = schema["paths"][path]["post"]
                self.assertIn("201", op["responses"])
                ref = op["requestBody"]["content"]["application/json"]["schema"]["$ref"]
                self.assertTrue(ref.endswith(model))
                props = schema["components"]["schemas"][model]
                self.assertEqual(set(props["required"]), {"name", "email", "age"} if model == "MemberCreate" else {"title", "instructor", "capacity"})


if __name__ == "__main__":
    unittest.main()
