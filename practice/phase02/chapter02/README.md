# Phase 02 Chapter 02 학습 기록

**수업:** 2강. Path Parameter와 Query Parameter  
**날짜:** 2026-10-29  
**목표:** URL에 포함된 값이 FastAPI 함수 인자로 들어오는 과정을 이해하고 200 / 404 / 422를 검증한다.

## Path Parameter를 사용한 API

| Method | URL | Path 입력 | 정상 응답 | 오류 응답 |
| --- | --- | --- | --- | --- |
| GET | `/members/{member_id}` | `member_id: int` | 200 + 회원 객체 1개 | 없는 ID: 404 `Member not found`, 문자 ID: 422 |
| GET | `/courses/{course_id}` | `course_id: int` | 200 + 강좌 객체 1개 | 없는 ID: 404 `Course not found`, 문자 ID: 422 |

- `/members/3`은 `member_id = 3`으로 해석되어 `get_member(3)`이 호출된다.
- `/members/99`: 정수이지만 회원이 없어 404.
- `/members/abc`: 정수 변환 실패로 함수 실행 전에 422 Validation Error.

## Query Parameter를 사용한 API

| Method | URL | Query 입력 | 예상 결과 |
| --- | --- | --- | --- |
| GET | `/members` | `name: str` 선택, `min_age: int` 선택 | 조건이 없으면 회원 3명, 있으면 필터된 배열 |
| GET | `/members/search/?name=kim` | `name` 선택 | 200 + Kim |
| GET | `/members/filter/?min_age=20` | `min_age` 선택 | 200 + Kim, Park |
| GET | `/members/filter/?name=k&min_age=20` | `name`, `min_age` 선택 | 200 + Kim, Park |
| GET | `/courses` | 없음 | 200 + 강좌 3개 |
| GET | `/courses/filter/?title=front` | `title` 선택 | 200 + Frontend |
| GET | `/courses/filter/?level=2` | `level` 선택 | 200 + Frontend, FastAPI |

**강의 실습 데이터:**

```python
members = [
    {"id": 1, "name": "Kim", "email": "kim@example.com", "age": 25},
    {"id": 2, "name": "Lee", "email": "lee@example.com", "age": 19},
    {"id": 3, "name": "Park", "email": "park@example.com", "age": 31},
]
courses = [
    {"id": 1, "title": "Database", "level": 1},
    {"id": 2, "title": "Frontend", "level": 2},
    {"id": 3, "title": "FastAPI", "level": 2},
]
```

- 데이터는 Python 리스트에 저장한다. **아직 DB를 연결하지 않는다.**
- 1강의 기본 응답 `GET /` → `{"message":"라면먹고갈래"}`를 유지했다.
- `/members`에도 선택적 Query를 추가해 강의의 Contract B (`/members?name=kim`)를 지원한다.
- `?name=k&min_age=20`과 `?min_age=20&name=k`은 같은 결과를 반환한다.
- 이름 및 강좌 제목 검색은 대소문자를 구분하지 않는다.
- `/members/search/`, `/members/filter/`, `/courses/filter/`를 동적인 `/{id}` 경로보다 먼저 등록하여 고정 경로가 ID로 잘못 인식되는 일을 방지했다.

## 두 방식을 구분한 기준

- **Path Parameter**: 회원 3번, 강좌 2번처럼 특정 자원을 식별할 때 (`/members/3`).
- **Query Parameter**: 목록에 이름·나이·레벨 등의 검색 조건을 붙일 때 (`/members?name=kim`).
- **404**: 형식이 맞는 ID이지만 대상이 없음.
- **422**: `int` 인자에 문자 등 유효하지 않은 값이 입력됨.
- **200 + []**: 검색 자체는 정상이나 조건에 맞는 결과가 없음.

## 실행 방법 (Windows PowerShell)

프로젝트 루트에 이미 있는 `.venv`를 사용한다.

```powershell
cd C:\dev\fullstack-web-course
.\.venv\Scripts\Activate.ps1
python -m pip install fastapi uvicorn httpx
cd practice\phase02\chapter02
python -m uvicorn main:app --reload
```

브라우저에서 `http://127.0.0.1:8000/docs`를 연다. Chapter 01 서버가 포트 8000을 사용 중이면 해당 서버를 `Ctrl + C`로 종료한 뒤 Chapter 02를 실행한다.

자동 테스트는 같은 폴더에서 별도 터미널을 열거나 개발 서버를 종료한 뒤 실행한다.

```powershell
python -m unittest -v test_api.py
```

## Swagger에서 확인한 200 / 404 / 422

### 2026-10-29 자동 테스트 Evidence

별도 테스트 환경의 FastAPI `TestClient`에서 `python -m unittest -v test_api.py` 실행:

```text
Ran 19 tests
OK
```

확인한 대표 결과:

| 요청 | 예상/자동 검증된 결과 |
| --- | --- |
| `GET /members/1` | **200**, Kim 객체 |
| `GET /members/99` | **404**, `{"detail":"Member not found"}` |
| `GET /members/abc` | **422**, Validation Error |
| `GET /members/search/?name=kIm` | **200**, Kim 배열 |
| `GET /members/search/?name=unknown` | **200**, `[]` |
| `GET /members/filter/?min_age=20` | **200**, Kim · Park |
| `GET /courses/2` | **200**, Frontend 객체 |
| `GET /courses/99` | **404**, `{"detail":"Course not found"}` |
| `GET /courses/abc` | **422**, Validation Error |
| `GET /courses/filter/?title=front` | **200**, Frontend 배열 |
| `GET /courses/filter/?level=2` | **200**, Frontend · FastAPI 배열 |
| `GET /docs`, `GET /openapi.json` | **200**, 명세에 7개 API 경로 존재 |

19개 검사는 위 항목 외에도 Query 순서, 조합 조건, 잘못된 필터 타입, 회원 3명·강좌 3명 응답 구조, 1강 기본 응답을 확인한다.

> 자동 테스트는 실제 HTTP 요청/응답을 앱에 전달하여 검증하지만, **사용자의 Chrome에서 Swagger Execute를 누른 스크린샷이나 Network 수동 확인을 대신하지는 않는다**.

### 사용자 PC에서 직접 확인할 항목 (미확인)

- [ ] Chapter 02 서버를 실행하고 `/docs` 열기.
- [ ] Swagger `GET /members/{member_id}`의 `1`, `99`, `abc`로 **200 / 404 / 422** 확인.
- [ ] `GET /members/search/` → `name=kim`, `GET /members/filter/` → `min_age=20` 확인.
- [ ] `GET /courses/{course_id}`의 `2`, `99`, `abc`로 **200 / 404 / 422** 확인.
- [ ] `GET /courses/filter/` → `title=front`, `level=2` 확인.
- [ ] 브라우저 F12 → Network에서 Request URL, Method GET, Status Code, Response 확인.
- [ ] Uvicorn 터미널에서 치명적인 오류가 없는지 확인.

## AI에게 질문한 내용

- 특정 회원·강좌를 조회할 때 Path와 Query 중 무엇을 사용해야 하는가?
- `member_id: int`가 404와 422에 각각 어떻게 반응하는가?
- 이름·최소 나이·강좌 제목·레벨 필터는 어떤 URL로 설계해야 하는가?
- 검색 결과 0건에서 404 대신 200과 빈 배열을 반환하는 이유는 무엇인가?
- 강의 Contract를 만족하는 코드와 자동 테스트를 어떻게 설계하는가?

## AI 답변 중 직접 검증한 부분

- **자동 검증 완료:** 19개 `unittest`/`TestClient` 케이스, JSON 구조, 200/404/422, Swagger 문서 경로.
- **직접 확인 필요:** 사용자 자신의 VS Code 실행 로그, Chrome Swagger Execute 결과, DevTools Network.
- AI가 코드를 구현했다고 해서 완료가 아니다. 실제 환경에서 Method / Path / Parameter / Status / Response Body가 계약에 맞는지 확인해야 한다.

## Definition of Done

- [x] `GET /members` 200 + 회원 3명.
- [x] `GET /members/{member_id}` 상세 조회, 404, 422.
- [x] Query 이름 검색·최소 나이 필터.
- [x] `GET /courses` / `GET /courses/{course_id}` 과제.
- [x] 강좌 title/level 필터, 404, 422.
- [x] 19개 자동 검증 모두 통과.
- [x] Path / Query 설계 기준과 Response Evidence 문서화.
- [ ] 사용자 PC Swagger/Network 수동 검증.

**제출:** `practice/phase02/chapter02/`  
**다음 Chapter:** Request Body와 Pydantic 모델로 POST 요청 검증.

---

출처: 아토믹데브, 「2강. Path Parameter와 Query Parameter」 (사용자가 제공한 강의 자료).
