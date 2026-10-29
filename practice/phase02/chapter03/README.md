# Phase 02 Chapter 03 학습 기록

**3강:** Request Body와 Pydantic — POST 입력 데이터 구조와 Validation  
**학습 날짜:** 2026-10-29  
**목표:** Body의 필수 필드와 타입을 Pydantic으로 검증하고 정상 201 / 오류 422를 구분한다.

## POST /members Contract

| 구분 | 계약 |
| --- | --- |
| Method | POST |
| Path | /members |
| Request Body | name: str, email: str, age: int (모두 필수) |
| Success | 201 Created + 임시 ID와 입력값 |
| Failure | 필드 누락 / 잘못된 입력 → 422 |
| Database | 연결하지 않음. 실제 저장 없음 |

**정상 요청 예(JSON):**

    {"name":"Hong Gil Dong","email":"hong@example.com","age":30}

**성공 응답 예 (201):**

    {"id":4,"name":"Hong Gil Dong","email":"hong@example.com","age":30}

id 4는 **고정된 임시 학습용 값**이다. 데이터베이스 저장, 실제 ID 생성, 중복 방지 기능은 아직 없다. POST 후 GET /members는 원래 회원 3명을 반환한다.

## POST /courses Contract (개인 과제)

| 구분 | 계약 |
| --- | --- |
| Method | POST |
| Path | /courses |
| Request Body | title: str, instructor: str, capacity: int (모두 필수) |
| Success | 201 Created + 임시 ID 및 입력값 |
| Failure | title 누락 / capacity 형식 오류 등 → 422 |
| Database | 연결하지 않음. 실제 저장 없음 |

**정상 요청 예(JSON):**

    {"title":"Backend","instructor":"Park","capacity":20}

**성공 응답 예 (201):**

    {"id":4,"title":"Backend","instructor":"Park","capacity":20}

Chapter 02의 강좌 조회 데이터는 id/title/level이고 Chapter 03의 강좌 생성 Body는 title/instructor/capacity다. 서로 다른 교육용 계약이며 아직 저장 모델을 통합하지 않았다.

## Request Body란 무엇인가?

- **Path Parameter**: GET /members/3 같은 특정 자원 식별.
- **Query Parameter**: GET /members?name=kim 같은 목록 필터.
- **Request Body**: POST /members에서 새 회원 데이터의 여러 필드를 JSON으로 전달.

JSON Body를 전송할 때는 일반적으로 Content-Type: application/json을 사용한다.

## Pydantic Model이 하는 일

    class MemberCreate(BaseModel):
        name: str
        email: str
        age: int

    class CourseCreate(BaseModel):
        title: str
        instructor: str
        capacity: int

- 기본값 없이 정의된 세 필드는 모두 필수.
- FastAPI는 Body를 모델과 비교하고 **검증을 통과한 후에만** Endpoint 함수를 실행한다.
- 검증 통과 → 함수 실행 → 201, 검증 실패 → 함수 실행 전 422.
- 422의 detail 목록에서 loc(필드 위치), type(오류 유형), msg(오류 설명)를 확인한다.
- email: str은 이메일 형식 자체가 아니라 문자열 타입만 검증한다.
- Pydantic은 변환 가능한 숫자 문자열을 int로 처리할 수 있지만, not-a-number는 422가 된다.

**Request 흐름:**

    Client → POST /members + JSON Body → FastAPI / Pydantic
          ├─ Invalid → 422
          └─ Valid → create_member() → 201 + 임시 id

## 실행 방법

프로젝트 루트 C:\dev\fullstack-web-course, 기존 가상환경(.venv) 재사용:

    cd C:\dev\fullstack-web-course
    .\.venv\Scripts\Activate.ps1
    python -m pip install fastapi uvicorn httpx
    cd practice\phase02\chapter03
    python -m uvicorn main:app --reload

**주의:** Chapter 03 폴더에서 서버를 실행해야 한다. 다른 Chapter 서버가 8000 포트를 사용하고 있다면 Ctrl+C로 종료 후 실행한다.

Swagger: http://127.0.0.1:8000/docs

자동 테스트(다른 터미널 또는 서버 중지 후):

    python -m unittest -v test_api.py

## 정상 요청 Evidence

2026-10-29 별도 Python 실행 환경에서 FastAPI TestClient / unittest **23개 통과**.

    Ran 23 tests
    OK

| 요청 | 테스트 결과 |
| --- | --- |
| POST /members + 정상 JSON | 201, id: 4와 입력값 |
| POST /courses + 정상 JSON | 201, id: 4와 입력값 |
| GET /members | 200, 기존 회원 3명 |
| GET /courses | 200, 기존 강좌 3개 |
| 기존 상세 조회/필터 | 기존 200 / 404 / 422 동작 유지 |
| GET /docs, GET /openapi.json | 200, POST Endpoint 및 두 입력 스키마 존재 |

## 422 실패 요청 Evidence

| 실패 요청 | 테스트 결과 |
| --- | --- |
| 회원 email 누락 | 422, loc = ["body","email"] |
| 회원 name 누락 | 422, loc = ["body","name"] |
| 회원 age = "not-a-number" | 422, loc = ["body","age"] |
| 강좌 title 누락 | 422, loc = ["body","title"] |
| 강좌 instructor 누락 | 422, loc = ["body","instructor"] |
| 강좌 capacity = "not-a-number" | 422, loc = ["body","capacity"] |
| 두 POST Body 전체 누락 | 각각 422 |

POST 요청 뒤 GET 목록이 바뀌지 않는 것도 테스트했다.

**주의:** 위 내용은 TestClient로 자동 검증한 증거다. 사용자의 실제 Chrome에서 Swagger Execute를 누른 결과는 아직 확보하지 않았다.

### Swagger 수동 확인 체크리스트 (사용자 PC에서 미확인)

- [ ] POST /members 정상 JSON → Request URL, Request Body, Response Code 201, Response Body 확인.
- [ ] POST /members email 제거 → 422 및 email 오류 위치 확인.
- [ ] POST /members age를 "not-a-number"로 설정 → 422 및 age 오류 위치 확인.
- [ ] POST /courses 정상 JSON → 201 및 임시 ID 포함 응답 확인.
- [ ] POST /courses title 제거 → 422 확인.
- [ ] POST /courses capacity를 "not-a-number"로 설정 → 422 확인.
- [ ] 서버 터미널에 치명적인 오류가 없는지 확인.

## AI에게 질문한 내용

- Path/Query와 달리 Request Body를 언제 사용하는가?
- Pydantic으로 회원/강좌의 필수 입력을 정의하는 방법은?
- 201 Created와 422 Validation Error는 어떻게 확인하는가?
- DB 없이 임시 ID를 응답하는 방법과 한계는 무엇인가?
- 앞선 Chapter 02 조회 API를 유지하면서 POST를 추가할 수 있는가?

## AI 답변 중 내가 직접 검증한 부분

- **별도 테스트 환경에서 자동 검증:** 23개 테스트, 정상 POST 201, 잘못된 입력 422, 오류 필드 위치, 기존 GET 기능 유지, OpenAPI 스키마.
- **아직 직접 검증하지 않음:** 사용자 PC의 Swagger Execute 및 Uvicorn 터미널 로그. 해당 항목은 완료로 표시하지 않는다.

## Definition of Done

- [x] MemberCreate / CourseCreate 입력 모델과 필수 필드 정의.
- [x] POST /members 및 POST /courses 구현.
- [x] 정상 요청은 201, 응답은 임시 id 포함.
- [x] 누락 필드, 타입 오류 시 422 자동 검증.
- [x] 이전 장 GET 기능 유지 및 회귀 테스트.
- [x] README의 API Contract와 Evidence 작성.
- [ ] 사용자 로컬 Swagger Execute, 터미널 결과 확인.

**제출 폴더:** https://github.com/cyw0927/fullstack-web-course/tree/main/practice/phase02/chapter03

**다음 강의:** Response Schema와 Status Code

---

출처: 아토믹데브, 「3강. Request Body와 Pydantic — POST 입력 데이터 구조와 Validation」 (사용자가 제공한 강의 자료).
