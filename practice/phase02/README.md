> **공통 실행 안내 (최신):** 모든 명령은 `practice/phase02`에서 실행합니다.
> Python 환경을 활성화한 뒤 `python -m uvicorn chapter08.main:app --reload`처럼 강의 번호를 바꾸어 실행하세요. 5강은 `python -m chapter05.main`입니다. DB 설정은 `common/.env` 하나를 사용합니다. 기존 강의별 `.env`는 자동으로 읽지 않습니다. 아래 이전 안내의 개별 `db.py`, `.env`, 실행 경로는 이 안내로 대체합니다.

# Phase 02 — Backend 학습 안내

이 디렉터리는 2차 FastAPI·PostgreSQL 실습을 순서대로 정리한 곳입니다. 프론트엔드 1차 과정은 `../phase01/`에 남겨 두었습니다.

## 강의별 기록

| 실제 진행 순서 | 주제 | 기록 |
| --- | --- | --- |
| 1강 | 첫 FastAPI 서버와 GET 목록 API | [Chapter 01](chapter01/README.md) |
| 2강 | Path / Query Parameter | [Chapter 02](chapter02/README.md) |
| 3강 | Request Body와 Pydantic | [Chapter 03](chapter03/README.md) |
| 4강 | Response Model과 Status Code | [Chapter 04](chapter04/README.md) |
| 5강 | PostgreSQL 연결과 SQL 직접 실행 | [Chapter 05](chapter05/README.md) |
| 6강 | FastAPI·PostgreSQL 통합과 POST 추가 과제 | [Chapter 06](chapter06/README.md) |
| **7강** | **POST /members + INSERT + Transaction** | **[Chapter 07](chapter07/README.md)** |
| **8강** | **PUT/PATCH + UPDATE — 전체·부분 수정** | **[Chapter 08](chapter08/README.md)** |
| **9강** | **회원 삭제 DELETE + PostgreSQL** | **[Chapter 09](chapter09/README.md)** |
| **10강** | **Router / Service / Repository 계층 구조화** | **[Chapter 10](chapter10/README.md) — CRUD 구현 진행 중** |

## 7강 실습 안내

7강은 **POST /members + INSERT + Transaction**입니다. 6강에서 먼저 수행한 회원 INSERT를 확장하여 이메일 중복 409, Pydantic 422, SQL 오류 500, 트랜잭션 commit/rollback과 Course POST 과제를 연습합니다. [7강 main.py](chapter07/main.py), [db.py](chapter07/db.py), [자동 테스트](chapter07/test_api.py), [README](chapter07/README.md)와 SQL 준비 파일을 추가했습니다. 실제 DB/Swagger 수동 검증은 남아 있습니다.

## 8강 실습 안내

8강은 기존 7강의 CRUD API에서 회원·강좌 PUT/PATCH 수정으로 확장합니다. **PUT 전체 필수값, PATCH 선택 필드, 생략/명시적 null 구분, 빈 PATCH 400, 대상 없음 404, 이메일 충돌 409, 검증 오류 422**를 계약으로 구현했습니다. [8강 실행 코드](chapter08/main.py), [DB SQL 로직](chapter08/db.py), [단위 테스트](chapter08/test_api.py), [README](chapter08/README.md) 및 SQL 검증 파일을 준비했으며, 사용자 로컬 DB에 대한 최종 Evidence는 아직 확인되지 않았습니다.

## 9강 실습 안내

9강은 회원 상세 GET과 DELETE 두 엔드포인트에 집중해, **204 빈 응답 → DB SELECT 0행 → GET 404**를 직접 검증합니다. [9강 코드](chapter09/main.py), [DB 접근 코드](chapter09/db.py), [테스트](chapter09/test_api.py), [README](chapter09/README.md)가 준비되어 있으며, 실제 PostgreSQL 삭제 검증은 별도로 수행해야 합니다.

## 10강 실습 안내

10강은 회원 API를 **Router → Service → Repository → DB** 계층으로 분리하는 실습입니다. 현재 저장소의 Chapter 10은 완성된 CRUD가 아니라 직접 구현을 이어가는 출발점입니다.

- `app/main.py`: FastAPI 앱과 회원 라우터 연결
- `app/routers/members.py`: 라우터 골격이 있으며 CRUD 엔드포인트는 TODO 상태
- `app/services/member_service.py`: 업무 규칙 및 CRUD 흐름을 작성할 TODO 상태
- `app/repositories/member_repository.py`: `find_all()` 목록 조회가 준비되어 있고 나머지 DB 작업은 TODO
- `app/schemas.py`: 회원 Create / Update / Patch / Response 스키마
- `app/db.py`: `common.db`의 공통 DB 연결 재사용

실제 테이블은 기존 Phase 02 DB의 `public.members(id, name, email, age)`를 기준으로 하므로, 이 강의의 응답 식별자는 `member_id`가 아니라 `id`입니다. 자세한 주의사항은 [Chapter 10 README](chapter10/README.md)를 따릅니다.

```powershell
cd C:\dev\fullstack-web-course\practice\phase02
python -m uvicorn chapter10.app.main:app --reload --port 8000
```

현재 상태에서는 CRUD 라우터를 구현하기 전이므로 Swagger에 회원 엔드포인트가 보이지 않는 것이 정상입니다. **10강을 완료된 것으로 표시하지 않습니다.**

## 실습 원칙

- Python 가상환경은 프로젝트 최상위 `.venv`를 사용합니다.
- PostgreSQL 비밀번호는 `.env`에만 두고, `.gitignore`로 제외하며 `.env.example`에는 예시 값만 기재합니다.
- Swagger 응답 확인뿐 아니라 실제 SQL 결과와 비교해 API Contract의 충족 여부를 검증합니다.
- 사용자가 직접 실행하지 않은 테스트는 완료 처리하지 않으며, 코드 수정·커밋 전 기존 작업을 확인합니다.

출처: 아토믹데브의 Backend 강의 원문 (사용자가 제공한 자료).

---

## 전체 인프라 소개와 학습 로드맵

> 아토믹데브의 「Backend Overview — 전체 Fullstack 인프라와 FastAPI의 역할」 강의 자료를 바탕으로 2차 Backend 과정의 전체 구조와 학습 로드맵을 정리한 문서입니다.

**위치:** `practice/phase02/README.md`

**학습 방식:** AI 활용 바이브 코딩 + API Contract 기반 개발. AI가 초안을 만들더라도 설계, 보안, 검증과 완료 판정은 개발자가 책임집니다.

## 1. 전체 웹 서비스 구조

```text
사용자 / 브라우저
   │
   ▼
Frontend (HTML·CSS·JavaScript, 이후 React / Next.js)
   │ HTTPS / REST API / JSON
   ▼
[운영 환경의 Reverse Proxy / HTTPS 종단 — 선택 사항]
   │
   ▼
Uvicorn (ASGI 서버) + FastAPI (Backend API)
   ├─ Router / Endpoint: Method·Path를 Python 함수에 연결
   ├─ Pydantic: Request / Response Schema와 검증
   ├─ Service: 비즈니스 규칙과 권한
   └─ Repository / SQLAlchemy: 데이터 접근
   │ SQL / ORM
   ▼
PostgreSQL (데이터 영구 저장, 제약조건, 트랜잭션)
```

- **Frontend:** 화면 표시, 입력 수집, API 호출 및 결과 렌더링.
- **Backend:** 요청 처리, 입력 검증, 인증·권한, 비즈니스 로직, DB 접근, 응답 계약 보장.
- **Database:** 데이터 저장과 검색, 참조 무결성 및 트랜잭션 보장.
- **Uvicorn:** FastAPI 앱을 HTTP/ASGI 서버로 실행. 모든 배포에서 Reverse Proxy가 필수인 것은 아님.
- **원칙:** 브라우저가 DB에 직접 연결하지 않고 Backend가 데이터와 권한을 통제.

## 2. 1차 → 2차 → 3차 과정의 연결

| 교육 과정 | 주요 기술 | 실습 목표 |
| --- | --- | --- |
| 1차 Frontend | HTML / CSS / JavaScript / `fetch()` | 제공된 API 호출 및 결과 표시 |
| 2차 Backend | FastAPI / Pydantic / PostgreSQL / SQLAlchemy | API 설계, 구현, 저장, 검증 |
| 3차 Frontend 고도화 | TypeScript / React / Next.js | 2차에서 만든 동일 API를 컴포넌트 UI에 연결 |

```text
1차: Browser ── fetch() ──> 제공 API
2차: Swagger / Browser ──> FastAPI ──> PostgreSQL
3차: React / Next.js ──> 같은 FastAPI Contract ──> PostgreSQL
```

React는 Backend를 대체하지 않습니다. 화면 기술이 바뀌어도 API Contract가 유지되면 같은 Backend를 다시 사용할 수 있습니다.

## 3. 요청과 응답이 처리되는 흐름

```text
Browser / Swagger → GET /members/3
  → Uvicorn (HTTP / ASGI)
  → FastAPI Routing (Method + Path)
  → 입력 추출·검증 (FastAPI + Pydantic)
  → Endpoint / Service (업무 규칙)
  → Repository / SQLAlchemy → PostgreSQL (DB 사용 시)
  → Pydantic Response Model 검증·직렬화
  → HTTP Status + JSON Response → Client
```

실제 애플리케이션에서는 미들웨어, 의존성 주입, 인증·권한, 예외 핸들러가 추가될 수 있고 구체적 처리 순서는 구현에 따라 달라집니다.

### 핵심 용어

| 용어 | 의미 |
| --- | --- |
| HTTP | 클라이언트와 서버의 요청·응답 통신 규약 |
| Endpoint | 특정 Method / URL을 처리하는 API 진입점 |
| Routing | 요청을 올바른 Python 함수와 연결 |
| Path Parameter | `/members/3`처럼 특정 자원의 ID를 지정 |
| Query Parameter | `?name=kim`처럼 검색·필터 조건 지정 |
| Request Body | 주로 POST / PUT / PATCH에서 보내는 JSON 데이터 |
| JSON | 구조화된 텍스트 기반 데이터 교환 형식 |
| Schema / DTO | 필드와 타입 및 규칙에 대한 데이터 계약 |
| Validation | 요청·응답 데이터가 계약과 맞는지 확인 |
| Serialization | Python 값을 JSON 응답에 적합하게 변환 |
| ORM | Python 객체를 이용해 DB의 데이터를 다루는 방법 |
| Transaction | 여러 DB 작업의 일관성을 보장하는 단위 |
| API Contract | Method·URL·Request·Response·Status·Error의 약속 |

## 4. 주요 Backend 기술의 역할

| 구성요소 | 역할 |
| --- | --- |
| Uvicorn | ASGI 서버 실행 |
| FastAPI | 라우팅, 엔드포인트, HTTP 요청/응답, OpenAPI / Swagger 문서화 |
| Pydantic | Request / Response 모델, 검증, 직렬화 |
| Service | 비즈니스 규칙, 권한 확인, 처리 순서 |
| Repository | DB 호출을 Endpoint에서 분리하는 계층 |
| SQLAlchemy | SQL / ORM 모델·세션·데이터 접근 |
| PostgreSQL | 영구 저장, SQL 처리, UNIQUE / FK 등 무결성, Transaction |

```text
Client JSON → Pydantic Request Model → FastAPI / Service
            → SQLAlchemy / Repository → PostgreSQL
            → Pydantic Response Model → Client JSON
```

- Pydantic은 **API 입출력 DTO** 역할에 가깝고 SQLAlchemy는 **DB 접근/ORM** 역할을 담당합니다.
- `response_model`이 외부로 내보낼 필드를 제한할 수 있지만 SQL `SELECT` 자체를 자동 최적화하지는 않습니다.
- Pydantic이 정수 타입을 검증해도 DB에 해당 FK/ID가 실제 존재하는지는 별도 확인이 필요합니다.
- 입력 Validation 실패는 보통 **422**, 출력 Response Model의 계약 위반은 서버 오류(보통 **500**)가 될 수 있습니다.

## 5. API Contract 기반 개발 루프

```text
요구사항
 → API Contract (Method / URL / Input / Output / Error)
 → Definition of Done (완료 조건)
 → AI 구현 계획
 → FastAPI / Pydantic / DB 구현
 → Swagger + Server Log + DB SELECT + TestClient 검증
 → 계약 위반 수정 / 회귀 테스트
 → Git Commit / Push
```

예시 Contract:

| API | 성공 계약 | 실패 계약 |
| --- | --- | --- |
| `GET /members` | 200 + 회원 목록 JSON | DB 오류 등 별도 처리 |
| `GET /members/3` | 200 + 회원 객체 | 없는 ID: 404, 잘못된 타입: 422 |
| `POST /members` | 201 + 생성된 회원 JSON | 입력 구조·타입 오류: 422 |

**중요:** 201 응답만으로 DB 저장을 확인했다고 단정하지 않습니다. DB에 실제 데이터가 존재하는지 SQL SELECT 및 반환값과 비교해 검증합니다.

## 6. Backend 15강 전체 로드맵

| 강 | 주제 | 실습 핵심 | 이 저장소 진행 |
| --- | --- | --- | --- |
| 01 | Backend 구조와 첫 FastAPI | Uvicorn, Swagger, GET /members | [Chapter 01](chapter01/) |
| 02 | Path/Query Parameter | 상세 조회·검색·필터, 404/422 | [Chapter 02](chapter02/) |
| 03 | Request Body/Pydantic | POST JSON, 필수값·타입 검증 | [Chapter 03](chapter03/) |
| 04 | Response Model/Status Code | Request/Response 모델 구분, 응답 계약 | [Chapter 04](chapter04/) |
| 05 | PostgreSQL/환경설정 | psycopg, .env, 연결/Secret | [Chapter 05](chapter05/) |
| 06 | GET + SELECT | 실제 DB 조회와 Swagger 응답 비교 | [Chapter 06](chapter06/) |
| 07 | POST + INSERT/Transaction | 저장, commit / rollback | 코드·테스트 준비, 실제 DB 검증은 별도 |
| 08 | PUT/PATCH + UPDATE | 전체·부분 수정, null 정책 | 코드·테스트 준비, 실제 DB 검증은 별도 |
| 09 | DELETE + DELETE SQL | 삭제, 204/404 | 코드·테스트 준비, 실제 DB 검증은 별도 |
| 10 | Backend 계층 구조화 | Router / Service / Repository | 출발점 준비, CRUD 구현 진행 중 |
| 11 | SQLAlchemy ORM 기초 | Model, Session, SQL 관계 | 미착수 |
| 12 | ORM 기반 CRUD | ORM 작업 및 Transaction | 미착수 |
| 13 | 예외·로그·테스트 | HTTPException, TestClient | 미착수 |
| 14 | CORS·Frontend 연동·보안 | Origin, 환경 분리, Secret | 미착수 |
| 15 | AI 기반 Backend 미니 프로젝트 | Contract → DB → ORM → 테스트 → GitHub | 미착수 |

### 저장소에서 확인할 사항

- 1~6강 폴더는 이미 만들어졌으며, 코드를 직접 실행하지 않은 항목이나 수동 검증 미완료 항목은 각 Chapter README에 구분되어 있습니다.
- `chapter05`와 `chapter06`의 비밀정보 `.env`는 GitHub에 저장하지 않고 `.env.example`만 공유합니다.
- 이 Overview는 교육 내용과 학습 진행 안내 문서이며 **새로운 FastAPI Endpoint를 추가하지 않습니다.**

## 7. 학습 확인 질문

1. React로 UI를 다시 만들 때 기존 FastAPI API를 재사용할 수 있는가?
2. Pydantic이 회원 ID의 타입을 검증하면 해당 회원의 DB 존재까지 보장하는가?
3. HTTP 200 또는 201 응답만으로 실제 DB 저장을 증명할 수 있는가?
4. AI가 코드를 생성했다는 사실만으로 과제가 완료되었다고 할 수 있는가?

## 8. 개념 이해 체크리스트

- [ ] Frontend / Backend / Database의 책임을 설명할 수 있다.
- [ ] 1차 / 2차 / 3차 과정이 어떻게 연결되는지 설명할 수 있다.
- [ ] FastAPI / Uvicorn / Pydantic / SQLAlchemy / PostgreSQL을 구분할 수 있다.
- [ ] Request부터 JSON Response까지의 흐름을 설명할 수 있다.
- [ ] API Contract와 Swagger / DB / 테스트 Evidence의 필요성을 설명할 수 있다.

---

출처: 아토믹데브, 「Backend Overview — 전체 Fullstack 인프라와 FastAPI의 역할」 (사용자가 제공한 강의 자료).

## 공통 DB 모듈 및 검증

`common/.env.example`을 복사하여 `common/.env`를 만들고 DB 접속 정보를 입력합니다. 이 파일은 Git에서 제외됩니다. 환경변수는 `.env`보다 우선합니다. 기존 강의별 설정은 자동으로 옮겨지지 않으므로 필요한 설정을 직접 확인하세요.

```powershell
cd practice/phase02
# 기존 .venv가 있다면 활성화
.venv/Scripts/Activate.ps1
python -m chapter05.main
python -m uvicorn chapter06.main:app --reload
# 다른 강의는 chapter07, chapter08 또는 chapter09 사용
python -m unittest chapter06.test_api chapter07.test_api chapter08.test_api chapter09.test_api
```

8강의 강좌 API는 기존 호환성을 위해 유지하지만 Swagger에서는 숨깁니다. 테스트의 DB 동작은 모의 객체이므로 실제 DB commit/rollback의 증거가 아닙니다. 이메일 중복을 동시 요청에서도 방지하려면 DB의 email UNIQUE 제약이 필요합니다.
