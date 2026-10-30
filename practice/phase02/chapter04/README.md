# Phase 02 Chapter 04 학습 기록

**강의:** 4강. Response Model과 Status Code (아토믹데브)  
**작업 날짜:** 2026-10-30  
**목표:** 입력 계약(Request Contract)뿐 아니라 출력 계약(Response Contract)도 정의하고, 응답 JSON과 HTTP Status Code를 검증한다.

## Request Model과 Response Model의 차이

- **Request Model:** 클라이언트에서 서버로 보내는 데이터 구조를 선언한다.
- **Response Model:** 서버가 클라이언트에 돌려주기로 약속한 데이터 구조를 선언한다.
- `MemberCreate`: 필수 `name: str`, `email: str`, `age: int`.
- `MemberResponse`: 필수 `id: int`, `name: str`, `email: str`, `age: int`.
- `CourseCreate`: 필수 `title: str`, `instructor: str`.
- `CourseResponse`: 필수 `id: int`, `title: str`, `instructor: str`.
- **`id`는 Request에는 없고 Response에만 있다.** 이번 실습에서는 서버가 `len(리스트) + 1`을 이용해 임시 ID를 부여한다.

`response_model`은 Swagger 문서에 Schema를 표시할 뿐 아니라, FastAPI가 **응답 데이터를 검증하고 직렬화하며 허용된 필드만 내보내도록 하는 계약**이다. 예를 들어 저장된 Kim 회원에는 `internal_note: "VIP"`가 있지만 `MemberResponse`에 없어서 GET 응답에서는 보이지 않는다. 단, 응답 모델 설정만으로 모든 보안 문제가 해결되는 것은 아니다.

## API Contract

| Method | URL | Request | 정상 상태 | 성공 Response | 실패 상태 |
| --- | --- | --- | --- | --- | --- |
| GET | `/members` | 없음 | 200 | `MemberResponse[]` | — |
| GET | `/members/{member_id}` | 경로 정수 ID | 200 | `MemberResponse` | 존재하지 않으면 404, 잘못된 ID 타입은 422 |
| POST | `/members` | `MemberCreate` JSON | 201 | `MemberResponse` | Body 누락·타입 오류 422 |
| GET | `/courses` | 없음 | 200 | `CourseResponse[]` | — |
| GET | `/courses/{course_id}` | 경로 정수 ID | 200 | `CourseResponse` | 존재하지 않으면 404, 잘못된 ID 타입은 422 |
| POST | `/courses` | `CourseCreate` JSON | 201 | `CourseResponse` | Body 누락·타입 오류 422 |

추가로 앞선 학습에서 설정한 `GET /`의 `{"message":"라면먹고갈래"}`를 유지했다.

### POST /members Contract

**Request Body:**

```json
{
  "name": "Park",
  "email": "park@example.com",
  "age": 28
}
```

**성공 응답 예 (`201 Created`):** 초기 회원이 2명인 상태에서 실행하면 아래와 같다.

```json
{
  "id": 3,
  "name": "Park",
  "email": "park@example.com",
  "age": 28
}
```

### POST /courses Contract (혼자 해보기 과제)

**Request Body:**

```json
{
  "title": "FastAPI",
  "instructor": "Park"
}
```

**성공 응답 예 (`201 Created`):** 초기 강좌가 2개인 상태에서 실행하면 아래와 같다.

```json
{
  "id": 3,
  "title": "FastAPI",
  "instructor": "Park"
}
```

**3강과의 차이:** 3강의 CourseCreate에는 `capacity`가 포함되었지만 **4강 강의의 CourseCreate/Response 계약에는 `title`, `instructor`, `id`만 요구된다.** 따라서 이번 폴더는 4강 계약대로 별도 구성했으며 이전 Chapter의 파일은 수정하지 않았다. 또한 4강은 response_model/Status에 집중하는 독립 실습이므로 2강에서 연습한 검색·필터 URL은 이번 Chapter에는 별도로 복제하지 않았다.

## 200과 201을 어떻게 구분했는가

- **200 OK:** GET으로 목록이나 상세 데이터를 정상 조회함.
- **201 Created:** POST로 새 항목이 생성됨. 이 실습에서는 메모리 리스트에 실제로 추가하고 새 `id`를 반환함.
- **404 Not Found:** 요청한 특정 ID의 회원·강좌가 없음.
- **422 Validation Error:** Path의 타입이 맞지 않거나 POST Body에 필요한 값이 없거나 타입 오류가 발생함.

**주의:** 메모리 리스트는 PostgreSQL 같은 영속 저장소가 아니다. 서버 재시작 시 기본 데이터로 초기화되며, 단순 `len(list) + 1` 방식은 삭제/동시성까지 고려한 ID 생성기가 아니다.

## 404를 확인한 요청

| 요청 | 기대 응답 |
| --- | --- |
| `GET /members/999` | 404, `{"detail":"Member not found"}` |
| `GET /courses/999` | 404, `{"detail":"Course not found"}` |

## 422를 확인한 요청

| 요청 | 기대 응답 |
| --- | --- |
| `POST /members`, `age` 누락 | 422, `loc: ["body", "age"]` |
| `POST /members`, `age: "abc"` | 422, age 타입 오류 |
| `POST /members`, `email` 누락 | 422, email 필수값 오류 |
| `POST /courses`, `title` 누락 | 422, title 필수값 오류 |
| `POST /courses`, `instructor` 누락 | 422, instructor 필수값 오류 |
| `POST /courses`, `title: [1, 2]` | 422, title 타입 오류 |
| `GET /members/abc` 및 `GET /courses/abc` | 각각 422, Path 타입 오류 |

참고로 `email: str`은 문자 여부만 검사한다. 이메일 주소 형식까지 검증하는 모델은 아직 사용하지 않았다.

## Swagger에서 확인한 Response Schema

Swagger URL: http://127.0.0.1:8000/docs

Swagger **Schemas**에서 `MemberCreate`, `MemberResponse`, `CourseCreate`, `CourseResponse`를 확인한다. POST는 Request Body에 Create 모델이, **201 Response**에 Response 모델이 연결되어야 한다. GET 목록은 Response 모델의 배열이어야 한다.

### 자동 검증 Evidence (실제 실행 완료)

2026-10-30 별도 Python 환경에서 FastAPI `TestClient`를 이용한 `unittest`를 실행했다.

```text
Ran 24 tests
OK
```

24개의 테스트에서 다음을 확인했다.

- GET 회원·강좌 목록/상세 **200**와 Response 필드 구조.
- POST 회원·강좌 생성 **201**, 임시 ID 부여, 같은 실행 세션 내 GET 재조회 성공.
- 없는 회원/강좌 조회 **404**, 잘못된 ID 형식 **422**.
- POST 필수 필드 누락, 잘못된 타입 **422**와 오류 필드 위치.
- 잘못된 POST는 메모리 리스트를 변경하지 않음.
- `MemberResponse`에 없는 `internal_note`가 GET 응답에서 필터링됨.
- `/docs`, `/openapi.json` 접근 성공 및 요청/응답 Schema의 모델 연결 확인.

위 항목은 **테스트 클라이언트를 사용한 자동 검증 결과**이다. 사용자의 Chrome에서 Swagger Execute를 수행한 직접 증거는 아니다.

### 사용자 PC Swagger 수동 확인 (미확인)

- [ ] GET `/members`에서 200과 회원 2명 JSON 확인.
- [ ] GET `/members/1`에서 200, MemberResponse 구조 확인.
- [ ] POST `/members`에서 Park Body → 201, id 3 응답 확인.
- [ ] POST 후 GET `/members`에 Park가 추가되었는지 확인.
- [ ] GET `/members/999` → 404, `detail` 확인.
- [ ] POST `/members`에서 age 누락 → 422, 오류 `loc` 확인.
- [ ] POST `/courses`에서 정상 Body → 201, id 반환 확인.
- [ ] GET `/courses`, `/courses/{course_id}` → 200, CourseResponse 구조 확인.
- [ ] GET `/courses/999` → 404 / 잘못된 POST Body → 422 확인.
- [ ] Swagger `Schemas`에서 Create/Response 모델을 비교하고 서버 로그에 치명적인 오류가 없는지 확인.

## 실행 방법

프로젝트 루트의 기존 `.venv`를 사용한다. 1~3강 서버가 포트 8000을 사용 중이면 먼저 해당 터미널에서 `Ctrl + C`로 종료한다.

```powershell
cd C:\dev\fullstack-web-course
.\.venv\Scripts\Activate.ps1
python -m pip install fastapi uvicorn httpx
cd practice\phase02\chapter04
python -m uvicorn main:app --reload
```

테스트 실행 (다른 터미널 또는 서버 종료 후):

```powershell
cd C:\dev\fullstack-web-course\practice\phase02\chapter04
python -m unittest -v test_api.py
```

`Could not import module "main"` 오류가 나면 터미널이 `chapter04` 폴더에 있는지 확인한다.

## AI에게 요청한 리뷰 내용

- MemberCreate와 MemberResponse가 분리되어 있는가?
- GET 목록·상세에 응답 모델이 지정되었는가?
- POST 성공은 201이며 생성된 id가 포함되는가?
- 존재하지 않는 ID는 404, 잘못된 입력은 422인가?
- CourseCreate와 CourseResponse가 강의에 적힌 계약에 맞는가?
- 출력에서 `internal_note`가 제외되는가?

## AI 답변 중 내가 직접 검증한 부분

- **자동으로 검증된 부분:** 상태 코드, 입력 오류, 출력 필드, 임시 리스트 저장, Schema, 비공개 내부 필드 제거 등 24개 테스트.
- **아직 직접 확인할 부분:** 사용자 자신의 VS Code/Uvicorn 로그, Swagger 화면에서의 Request/Response 실행 결과.

## Definition of Done

- [x] MemberCreate / MemberResponse 역할 분리 및 response_model 적용.
- [x] CourseCreate / CourseResponse 구현 및 response_model 적용.
- [x] GET 200, POST 201, 없는 자원 404, 잘못된 입력 422 자동 검증.
- [x] Swagger OpenAPI 응답 계약 자동 검증 및 README 기록.
- [x] 메모리 리스트에 생성 후 다시 조회할 수 있도록 구현.
- [ ] 사용자 PC에서 Swagger Response Body와 Schemas 수동 확인.

**제출 경로:** `practice/phase02/chapter04/`  
**저장소:** https://github.com/cyw0927/fullstack-web-course/tree/main/practice/phase02/chapter04

**다음 강의:** PostgreSQL 연결과 DB 접근 구조.

---

출처: 아토믹데브, 「4강. Response Model과 Status Code」 (사용자가 제공한 강의 자료).
