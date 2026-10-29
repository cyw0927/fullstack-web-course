# Phase 02 Chapter 01 학습 기록

**수업:** Backend와 API Server의 역할 — 첫 FastAPI 실행  
**학습 날짜:** 2026-10-29  
**수업 목표:** 1차 Frontend에서 호출하던 API를 FastAPI로 직접 구현하고, API Contract에 따라 검증한다.

## 내가 정의한 API Contract

| 기능 | Method | Path | Request Body | Success | Response |
| --- | --- | --- | --- | --- | --- |
| 시작 메시지 | GET | `/` | 없음 | 200 OK | `{"message": "라면먹고갈래"}` |
| 회원 목록 | GET | `/members` | 없음 | 200 OK | `id`, `name`, `email` 객체 배열 |
| 강좌 목록 (과제) | GET | `/courses` | 없음 | 200 OK | `id`, `title`, `instructor` 객체 배열, 최소 3개 |

**회원 목록 예상 Response:**

```json
[
  {"id": 1, "name": "Kim", "email": "kim@example.com"},
  {"id": 2, "name": "Lee", "email": "lee@example.com"}
]
```

**강좌 목록 예상 Response:**

```json
[
  {"id": 1, "title": "Database", "instructor": "Kim"},
  {"id": 2, "title": "Frontend", "instructor": "Lee"},
  {"id": 3, "title": "Backend", "instructor": "Park"}
]
```

강의의 예시 Response에는 강좌가 2개지만 과제 완료 조건이 **최소 3개**이므로 세 번째 강좌를 추가했다. 이번 Chapter에서는 DB 대신 Python 리스트를 사용한다.

- **Method**: 요청 방식. `GET`은 조회 요청이다.
- **Path**: `/members`와 같은 URL 경로.
- **Route**: `@app.get("/members")`처럼 Method와 Path를 Python 함수에 연결하는 규칙.
- **Response**: 서버가 반환하는 데이터. Python 리스트/딕셔너리가 JSON 응답으로 변환된다.

## Uvicorn의 역할

Uvicorn은 FastAPI 애플리케이션을 실제 **HTTP 서버로 실행**한다.

```powershell
cd C:\dev\fullstack-web-course\practice\phase02\chapter01
python -m uvicorn main:app --reload
```

- `main`: `main.py` 모듈
- `app`: 파일 안의 `app = FastAPI()` 객체
- `--reload`: 코드 저장 시 개발 서버 자동 재시작
- `Ctrl + C`: 개발 서버 종료

프로젝트 루트의 `.venv`가 이미 활성화되어 있다면 새 가상환경을 만들 필요 없다. 패키지 설치/확인:

```powershell
python -m pip install fastapi uvicorn httpx
python -m pip show fastapi
python -m pip show uvicorn
```

`httpx`는 `test_api.py`의 `TestClient` 자동 검증에 사용된다.

## FastAPI의 역할

FastAPI는 요청을 어떤 Python 함수가 처리하고 무엇을 응답할지 정하는 애플리케이션이다.

```text
Browser → HTTP Request → Uvicorn → FastAPI Route → Python Function
        ← JSON Response ←───────────────────────────────────┘
```

- `app = FastAPI()`: FastAPI 애플리케이션 생성.
- `@app.get("/")`: 기본 경로 GET 요청에 응답.
- `@app.get("/members")`: 회원 목록을 JSON 배열로 반환.
- `@app.get("/courses")`: 강좌 목록을 JSON 배열로 반환.
- Live Server가 HTML/CSS/JS 파일을 제공하는 반면, FastAPI는 Python 코드를 실행한다.

## Swagger에서 확인한 Evidence

### 앞서 사용자가 직접 확인한 내용

- Uvicorn을 실행하고 브라우저의 `GET /`에서 정상 응답을 확인했다 (터미널에도 `200 OK`).
- 사용자가 `http://127.0.0.1:8000/docs` 페이지가 정상적으로 열린다고 확인했다.
- 위 내용은 **이번 `/courses` 추가 전**에 확인한 것이므로 수정 후 재검증이 필요하다.

### 2026-10-29 자동 검증 (실제 실행 완료)

`python -m unittest -v test_api.py`로 FastAPI `TestClient` 기반 4개 검사를 실행했고 **4개 모두 통과**했다.

| 테스트 | 검증 결과 |
| --- | --- |
| `GET /` | 200, `라면먹고갈래` 응답 |
| `GET /members` | 200, 회원 2명 및 `id/name/email` 구조 일치 |
| `GET /courses` | 200, 강좌 3개 및 `id/title/instructor` 구조 일치 |
| `GET /docs`, `/openapi.json` | 200, 3개 GET Endpoint 정의 확인 |

```text
Ran 4 tests
OK
```

이는 **자동 Request/Response 검증**이지 사용자의 Chrome에서 Swagger `Execute` 버튼이나 DevTools를 누른 증거는 아니다.

### Swagger UI 수동 검증 (사용자 PC에서 남은 항목)

1. `http://127.0.0.1:8000/docs`로 접속.
2. **GET /members → Try it out → Execute**.
3. Request URL의 Path가 `/members`인지 확인.
4. Response Code가 `200`이고 Response Body가 회원 JSON 배열인지 확인.
5. **GET /courses**도 Execute하여 `200`과 강좌 3개를 확인.

### Browser / DevTools Network 수동 검증 (남은 항목)

1. `http://127.0.0.1:8000/members` 또는 `http://127.0.0.1:8000/courses`를 열기.
2. Chrome에서 `F12` → `Network` → 새로고침.
3. 요청을 클릭해 `Request URL`, `Request Method: GET`, `Status Code: 200`, `Response`를 확인.

## 발생한 오류와 해결 과정

| 증상 | 원인 | 해결 |
| --- | --- | --- |
| `Could not import module "main"` | 처음에 저장소 최상위 폴더에서 명령을 실행해 `main.py`를 찾지 못함 | `practice/phase02/chapter01`로 이동하여 실행 |
| `ERR_CONNECTION_REFUSED` | 서버가 `Shutting down`으로 종료됨 | `python -m uvicorn main:app --reload`로 재실행 |
| `Got unexpected extra arguments` | `Uvicorn running on...` 로그 문구를 명령처럼 입력함 | 정확한 실행 명령만 입력 |
| `favicon.ico 404` | 파비콘 파일 없음 | API 구현과 무관하므로 무시 가능 |
| `main.py` 반복 붙여넣기 | FastAPI 객체와 Route가 여러 차례 중복 정의됨 | 하나의 `app`과 각 Route 한 개로 정리 |

## AI에게 질문한 내용

- `main.py`는 어디에 만들고 어떻게 실행하는가?
- FastAPI, Uvicorn, `--reload`의 역할은 무엇인가?
- `Could not import module "main"` 오류는 왜 발생하는가?
- Swagger UI는 어디에서 열고 어떻게 테스트하는가?
- 기본 메시지를 `Hello FastAPI` 대신 `라면먹고갈래`로 바꾸려면?
- 회원 API와 강좌 과제를 API Contract에 맞춰 어떻게 완성하는가?

## AI 답변 중 내가 직접 검증한 부분

- 사용자가 Uvicorn의 정상 실행과 기본 응답 표시를 직접 확인함.
- 사용자가 서버 재시작 후 Swagger UI 페이지가 열린다고 직접 확인함.
- 이번 과제의 `/members`, `/courses` Request/Response 구조는 **자동 테스트로 검증 완료**.
- 수정 후 실제 Chrome의 Swagger Execute, Network 결과와 터미널 로그는 **아직 사용자 확인 전**.

## Definition of Done / 제출 체크리스트

- [x] `main.py`에 FastAPI `app` 존재
- [x] `GET /members` 구현
- [x] `GET /courses` 구현, 강좌 최소 3개
- [x] `GET /`, `GET /members`, `GET /courses`의 200 및 JSON 계약을 자동 검증
- [x] `/docs`와 OpenAPI 문서에서 Endpoint를 자동 검증
- [ ] 변경 후 Swagger `GET /members` · `GET /courses`의 `Execute`를 브라우저에서 직접 확인
- [ ] Chrome DevTools Network의 GET, 200, Response 확인
- [ ] 사용자 로컬 Uvicorn 로그에서 치명적 오류 없음 확인

**파일:** `main.py`(API), `test_api.py`(4개 자동 검사), `README.md`(학습 기록)

**제출 경로:** `practice/phase02/chapter01/`  
**GitHub:** https://github.com/cyw0927/fullstack-web-course/tree/main/practice/phase02/chapter01

## 다음 Chapter

Path Parameter `/members/{member_id}`와 Query Parameter를 사용해 회원 개별 조회 및 검색 조건을 학습한다.

---

출처: 아토믹데브, 「1강. Backend와 API Server의 역할 — 첫 FastAPI 실행」 (사용자가 제공한 강의 자료).
