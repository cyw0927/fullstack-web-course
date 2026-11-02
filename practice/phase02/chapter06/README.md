# Phase 02 / Chapter 06 — DB 기반 FastAPI GET / POST

**수업:** 6강. FastAPI와 PostgreSQL 연결 — 실제 DB 데이터를 API로 반환하기  
**추가 실습 과제:** POST API를 이용한 회원 등록  
**학습 기간:** 2026-10-30 ~ 2026-11-02

## API Contract

| Method | Path | Request Body | Response | Status |
| --- | --- | --- | --- | --- |
| GET | / | 없음 | 라면먹고갈래 메시지 | 200 |
| GET | /members | 없음 | id, name, email, age 객체의 JSON 배열 | 200 |
| POST | /members | name: str, email: str, age: int (필수) | id, name, email, age 객체 | 201 |
| POST | /members | 필수 필드 누락, age 형식 오류 | Validation Error | 422 |

**실제 DB:** postgres 데이터베이스 / public 스키마 / public.members 테이블. 강의 PDF에 나온 member_id와 달리 실제 테이블의 키는 id이므로 강사 실습 화면 및 추가 과제에 맞춰 API 키도 id를 사용한다.

## 핵심 소스 코드 흐름

- db.py의 get_connection(): .env에 있는 DB 설정으로 연결.
- db.py의 fetch_members(): SELECT id, name, email, age FROM public.members ORDER BY id;
- db.py의 insert_member(): 매개변수화된 INSERT와 RETURNING id, name, email, age 실행.
- main.py의 MemberCreate: POST 요청에 필요한 name/email/age 검증.
- main.py의 MemberResponse: GET/POST 응답의 id/name/email/age 검증.
- main.py의 get_members(): DB Tuple 리스트를 Python dict 리스트로 변환 후 JSON 반환.
- main.py의 create_member(): DB INSERT가 성공한 경우에만 생성된 DB Row로 201 응답.

    Browser / Swagger
      → POST /members + JSON
      → Pydantic MemberCreate Validation
      → psycopg / PostgreSQL INSERT ... RETURNING
      → Tuple → Python dict
      → MemberResponse
      → JSON + 201 Created

파라미터는 SQL 문자열에 직접 이어 붙이지 않고 psycopg의 %s placeholder로 전달한다. with Connection은 작업 성공 시 Commit, 실패 시 Rollback한다.

## 실습 실행

1. .env.example을 참고해 같은 폴더의 .env를 작성한다. 비밀번호를 README나 GitHub에 넣지 않는다.
2. PostgreSQL이 실행되고 public.members에 id/name/email/age 컬럼이 있는지 확인한다.
3. 프로젝트 루트의 가상환경을 활성화한다.
4. chapter06 폴더에서 Uvicorn을 실행한다.

    cd C:\dev\fullstack-web-course
    .\.venv\Scripts\Activate.ps1
    python -m pip install fastapi uvicorn httpx "psycopg[binary]" python-dotenv
    cd practice\phase02\chapter06
    python -m uvicorn main:app --reload

Swagger UI: http://127.0.0.1:8000/docs

### POST 예시

    {
      "name": "홍길동",
      "email": "hong2026@example.com",
      "age": 30
    }

정상적으로 성공한 사용자 Swagger 캡처(2026-10-30)에는 아래 **실제 확인된 201 응답**이 보인다.

    {
      "id": 5,
      "name": "홍길동",
      "email": "hong2026@example.com",
      "age": 30
    }

※ ID는 PostgreSQL의 Identity/Sequence가 생성한다. 이후 재실행 시 5라고 가정하지 않는다.

## DB에서 확인할 Evidence

DBeaver에서 반드시 같은 PostgreSQL DB와 public 스키마를 열고 아래 SQL을 실행한다.

    SELECT id, name, email, age
    FROM public.members
    WHERE email = 'hong2026@example.com'
    ORDER BY id;

또는 API의 실제 반환 ID로 조회:

    SELECT id, name, email, age
    FROM public.members
    WHERE id = 5;

**주의:** 사용자가 공유한 DBeaver 캡처는 WHERE id = 6을 조회하여 결과가 비어 있었다. Swagger의 캡처상 생성 ID는 5였다. 이후 사용자가 ID를 다시 언급했지만, 일치하는 SELECT 결과 캡처는 제시되지 않았다. 따라서 **DB SELECT의 독립 검증은 아직 미확인**으로 유지한다.

DB에서 id/name/email/age가 Swagger 결과와 일치해야 과제 검증이 완료된다.

## 422 Validation Error Evidence

아래 요청은 age가 정수가 아니므로 Pydantic이 422를 반환해야 한다.

    {
      "name": "테스트",
      "email": "invalid@example.com",
      "age": "abc"
    }

422 발생 시 SQL INSERT 함수는 실행되지 않는다. 브라우저에서 직접 테스트한 422 캡처는 아직 제공되지 않았으므로 수동 확인이 필요하다.

## 테스트

DB 없이 API 입력/출력 계약을 확인하는 Mock 기반 테스트:

    python -m unittest -v test_api.py

test_api.py는 DB 함수를 Mock으로 대체하여 200, 201, 422, Response Model 및 OpenAPI 스키마를 검증한다. **실제 DB INSERT 성공을 증명하지 못하며**, 최종 검증은 Swagger와 DBeaver의 실제 결과로 수행한다.

## 과제 제출물 및 확인 현황

- [x] FastAPI GET/POST 회원 API 코드 준비
- [x] PostgreSQL INSERT 및 생성 데이터 RETURNING 코드 준비
- [x] 사용자가 제공한 Swagger POST 201 Created 결과 확인
- [x] Response JSON의 id, name, email, age 4개 필드 확인
- [ ] 사용자 PC의 DBeaver SELECT 결과와 Swagger 생성 데이터가 정확히 일치하는지 확인
- [ ] age = "abc"를 보내 Swagger 422 직접 확인
- [ ] Swagger 성공 화면 및 DBeaver 성공 SELECT 화면을 별도 캡처하여 제출
- [ ] 로컬 .env Git 제외 상태 최종 확인

## AI에게 질문한 내용 / 직접 확인한 부분

- FastAPI GET 결과를 DB의 Tuple로부터 JSON으로 바꾸는 방법
- 실제 테이블 컬럼 id를 MemberResponse에 맞추는 방법
- POST를 추가했는데 Swagger에서 GET만 보이는 원인
- POST로 201을 반환한 뒤 DB INSERT 성공을 증명하는 SELECT 작성법
- **직접 확인:** Swagger POST 201 Created 캡처, JSON에 id 5 및 입력 필드 포함
- **아직 확인 필요:** DBeaver 결과와 응답의 1:1 일치, 422 수동 검증

**출처:** 아토믹데브, 「6강. FastAPI와 PostgreSQL 연결 — 실제 DB 데이터를 API로 반환하기」 및 사용자가 공유한 추가 POST/INSERT 과제 지시.
