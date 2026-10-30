"""Chapter 04 API 계약 테스트: python -m unittest -v test_api.py"""

import unittest

from fastapi.testclient import TestClient

from main import app, courses, members


class Chapter04ApiTests(unittest.TestCase):
    def setUp(self):
        # 각 테스트가 POST한 결과는 다음 테스트에 영향을 주지 않습니다.
        self.original_members = [item.copy() for item in members]
        self.original_courses = [item.copy() for item in courses]
        self.client = TestClient(app)

    def tearDown(self):
        members[:] = self.original_members
        courses[:] = self.original_courses
        self.client.close()

    def test_root_message(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "라면먹고갈래"})

    def test_get_members_returns_200_and_response_schema(self):
        response = self.client.get("/members")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(set(response.json()[0]), {"id", "name", "email", "age"})

    def test_get_member_returns_200(self):
        response = self.client.get("/members/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"id": 1, "name": "Kim", "email": "kim@example.com", "age": 25})

    def test_member_not_found_404(self):
        response = self.client.get("/members/999")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Member not found"})

    def test_bad_member_id_type_422(self):
        self.assertEqual(self.client.get("/members/abc").status_code, 422)

    def test_internal_member_note_is_not_exposed(self):
        self.assertIn("internal_note", members[0])
        for path in ("/members", "/members/1"):
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 200)
                self.assertNotIn("internal_note", response.text)

    def test_member_post_201_and_generated_id(self):
        body = {"name": "Park", "email": "park@example.com", "age": 28}
        response = self.client.post("/members", json=body)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"id": 3, **body})

    def test_member_post_persists_in_memory(self):
        self.client.post("/members", json={"name": "Park", "email": "park@example.com", "age": 28})
        self.assertEqual(len(self.client.get("/members").json()), 3)
        self.assertEqual(self.client.get("/members/3").json()["name"], "Park")

    def test_member_posts_assign_different_ids(self):
        first = self.client.post("/members", json={"name": "A", "email": "a@example.com", "age": 22})
        second = self.client.post("/members", json={"name": "B", "email": "b@example.com", "age": 23})
        self.assertEqual((first.json()["id"], second.json()["id"]), (3, 4))

    def test_member_missing_age_422(self):
        response = self.client.post("/members", json={"name": "Park", "email": "park@example.com"})
        self.assertEqual(response.status_code, 422)
        self.assertTrue(any(d["loc"] == ["body", "age"] for d in response.json()["detail"]))

    def test_member_bad_age_type_422(self):
        response = self.client.post("/members", json={"name": "Park", "email": "park@example.com", "age": "abc"})
        self.assertEqual(response.status_code, 422)
        self.assertTrue(any(d["loc"] == ["body", "age"] for d in response.json()["detail"]))

    def test_member_missing_email_422(self):
        response = self.client.post("/members", json={"name": "Park", "age": 28})
        self.assertEqual(response.status_code, 422)
        self.assertTrue(any(d["loc"] == ["body", "email"] for d in response.json()["detail"]))

    def test_invalid_member_post_does_not_change_list(self):
        self.client.post("/members", json={"name": "Park", "age": 28})
        self.assertEqual(len(members), 2)

    def test_get_courses_returns_200_and_response_schema(self):
        response = self.client.get("/courses")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(set(response.json()[0]), {"id", "title", "instructor"})

    def test_get_course_detail_returns_200(self):
        response = self.client.get("/courses/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"id": 1, "title": "Database", "instructor": "Kim"})

    def test_course_not_found_404(self):
        response = self.client.get("/courses/999")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Course not found"})

    def test_bad_course_id_type_422(self):
        self.assertEqual(self.client.get("/courses/abc").status_code, 422)

    def test_course_post_201_and_generated_id(self):
        body = {"title": "FastAPI", "instructor": "Park"}
        response = self.client.post("/courses", json=body)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"id": 3, **body})

    def test_course_post_persists_in_memory(self):
        self.client.post("/courses", json={"title": "FastAPI", "instructor": "Park"})
        self.assertEqual(len(self.client.get("/courses").json()), 3)
        self.assertEqual(self.client.get("/courses/3").json()["title"], "FastAPI")

    def test_course_post_missing_title_422(self):
        response = self.client.post("/courses", json={"instructor": "Park"})
        self.assertEqual(response.status_code, 422)
        self.assertTrue(any(d["loc"] == ["body", "title"] for d in response.json()["detail"]))

    def test_course_post_missing_instructor_422(self):
        response = self.client.post("/courses", json={"title": "FastAPI"})
        self.assertEqual(response.status_code, 422)
        self.assertTrue(any(d["loc"] == ["body", "instructor"] for d in response.json()["detail"]))

    def test_course_invalid_title_type_422(self):
        response = self.client.post("/courses", json={"title": [1, 2], "instructor": "Park"})
        self.assertEqual(response.status_code, 422)
        self.assertTrue(any(d["loc"] == ["body", "title"] for d in response.json()["detail"]))

    def test_invalid_course_post_does_not_change_list(self):
        self.client.post("/courses", json={"instructor": "Park"})
        self.assertEqual(len(courses), 2)

    def test_swagger_openapi_response_contract(self):
        self.assertEqual(self.client.get("/docs").status_code, 200)
        response = self.client.get("/openapi.json")
        self.assertEqual(response.status_code, 200)
        paths = response.json()["paths"]
        for resource, input_model, output_model in (
            ("members", "MemberCreate", "MemberResponse"),
            ("courses", "CourseCreate", "CourseResponse"),
        ):
            with self.subTest(resource=resource):
                listing = paths[f"/{resource}"]["get"]
                # schema lookup uses explicitly named ID path
                # 위 사용법 대신 정확한 ID 명칭을 사용합니다.
                id_field = "member_id" if resource == "members" else "course_id"
                detail = paths[f"/{resource}/{{{id_field}}}"]["get"]
                created = paths[f"/{resource}"]["post"]
                self.assertEqual(listing["responses"]["200"]["content"]["application/json"]["schema"]["items"]["$ref"].split("/")[-1], output_model)
                self.assertTrue(detail["responses"]["200"]["content"]["application/json"]["schema"]["$ref"].endswith(output_model))
                self.assertTrue(created["responses"]["201"]["content"]["application/json"]["schema"]["$ref"].endswith(output_model))
                self.assertTrue(created["requestBody"]["content"]["application/json"]["schema"]["$ref"].endswith(input_model))


if __name__ == "__main__":
    unittest.main()
