# 7강. POST /members + INSERT + Transaction

**강의:** 아토믹데브, 「7강. POST /members + INSERT + Transaction」  
**기준:** 사용자 제공 수업 자료 (2026-10-29 게시)  
**학습 상태:** 준비 / 로컬 실습 및 Evidence 미확인  
**이전 강의:** [6강. FastAPI와 PostgreSQL 연결](../chapter06/README.md)

> 6강에서는 회원 POST → PostgreSQL INSERT → 201 Created를 먼저 실습했습니다. 이번 7강은 그 기능을 **중복 이메일, 입력 검증, commit/rollback, DB 오류**까지 확장하는 단계입니다. 6강 성공 이력을 7강 전체 완료로 취급하지 않습니다.

## 1. API Contract — POST /members

| 구분 | 계약 |
| --- | --- |
| Method / URL | `POST /members` |
| Content-Type | `application/json` |
| Request Model | `name: str` (1~100자), `email: EmailStr`, `age: int` (0~150) |
| 정상 처리 | PostgreSQL `public.members`에 INSERT → RETURNING → commit |
| Response Model | `id: int`, `name: str`, `email: EmailStr`, `age: int` |
| 성공 상태 | `201 Created` |
| 입력 실패 | `422 Unprocessable Content` — 필드 누락/잘못된 이메일/범위 오류 |
| 중복 실패 | `409 Conflict` — 같은 이메일 |
| 서버/DB 실패 | `500 Internal Server Error` — 예상 외 오류, rollback |

정상 요청 예시:

```json
{
  "name": "홍길동",
  "email": "hong@example.com",
  "age": 27
}
```

성공 응답은 서버가 발급한 **실제 ID**를 포함하며, ID 값은 실행할 때마다 달라질 수 있습니다.

```json
{
  "id": 4,
  "name": "홍길동",
  "email": "hong@example.com",
  "age": 27
}
```

### Pydantic 입력/출력 모델 초안

```python
from pydantic import BaseModel, EmailStr, Field

class MemberCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    age: int = Field(ge=0, le=150)

class MemberResponse(MemberCreate):
    id: int
```

**패키지 주의:** `EmailStr`을 사용하려면 기존 FastAPI/Pydantic 외에 `email-validator` 패키지가 필요할 수 있습니다. 설치 명령: `python -m pip install "pydantic[email]"`.

## 2. Transaction 흐름

```text
POST /members
 → Pydantic Request Validation
   ├─ 입력 형식 오류 → 422 (INSERT 실행 전)
   └─ 정상 입력
      → PostgreSQL 연결
      → 중복 이메일 확인
      ├─ 중복 → 409 + rollback/종료
      └─ 신규 → parameterized INSERT ... RETURNING
                 → commit → 201 + MemberResponse
                   (DB 오류 → rollback → 500)
```

- **commit**: 실행한 변경을 DB에 확정합니다.
- **rollback**: 트랜잭션에서 수행한 변경을 취소합니다.
- **RETURNING**: INSERT가 생성한 ID/회원 데이터를 곧바로 반환합니다.
- **parameterized query**: SQL 문자열과 사용자 입력값을 분리하고 `%s` 바인딩을 사용합니다.
- `psycopg.connect()` 컨텍스트 매니저를 사용하면 정상 종료 시 commit, 예외 시 rollback 후 연결 종료됩니다. 강의의 명시적 `conn.commit()`, `conn.rollback()` 패턴과 둘 중 하나를 일관되게 사용해도 됩니다.

## 3. DB 실습 전에 확인할 실제 구조

6강에서 사용했던 로컬 DB는 `postgres` / `public` / `members(id, name, email, age)`입니다.

DBeaver에서 먼저 확인:

```sql
SELECT current_database(), current_schema();

SELECT column_name, data_type
FROM information_schema.columns
WHERE table_schema = 'public'
  AND table_name = 'members'
ORDER BY ordinal_position;

SELECT id, name, email, age
FROM public.members
ORDER BY id;
```

**주의:** 과거 사용자가 공유한 `CREATE TABLE`에는 `email UNIQUE`가 없을 가능성이 있습니다. 7강 중복 요청을 정확히 보호하려면 **사전 SELECT 검사만으로 충분하지 않으므로** DB의 유니크 제약조건 유무도 확인해야 합니다. 동시 요청 사이에 중복이 발생할 수 있기 때문입니다. 기존 데이터와 제약조건을 확인하기 전에 테이블을 임의로 변경하지 않습니다.

제약조건 확인:

```sql
SELECT conname, contype, pg_get_constraintdef(oid) AS definition
FROM pg_constraint
WHERE conrelid = 'public.members'::regclass;
```

중복 데이터 확인:

```sql
SELECT email, COUNT(*) AS count
FROM public.members
GROUP BY email
HAVING COUNT(*) > 1;
```

제약조건을 추가하기 전 기존 중복 데이터와 다른 코드가 받는 영향을 검토합니다. INSERT 중 유니크 충돌이 발생하면 `psycopg.errors.UniqueViolation` 등을 별도로 처리하여 `409`로 대응할 수 있습니다. 예상 외 DB 오류는 세부 연결정보/SQL을 사용자에게 노출하지 않고 로그에만 남깁니다.

## 4. 핵심 SQL

중복 이메일 사전 확인:

```sql
SELECT id
FROM public.members
WHERE email = %s;
```

INSERT + RETURNING:

```sql
INSERT INTO public.members (name, email, age)
VALUES (%s, %s, %s)
RETURNING id, name, email, age;
```

Python의 `cur.execute(sql, (member.name, member.email, member.age))`처럼 바인딩합니다. SQL에 사용자 입력을 f-string으로 직접 삽입하지 않습니다.

## 5. 실습 순서 (직접 코딩)

1. `chapter06`의 작동한 코드, `db.py`, `.env.example`을 참고하되 기존 장은 수정하지 않고 **chapter07 별도 실습**으로 진행합니다.
2. `MemberCreate`, `MemberResponse` 모델과 201/409/422/500 Contract를 정의합니다.
3. DB UNIQUE 여부를 확인하고 사전 중복 체크, 필요시 UNIQUE 충돌 처리 방법을 결정합니다.
4. INSERT/RETURNING을 매개변수화하고 성공 시 commit, 실패 시 rollback과 연결 종료를 확인합니다.
5. Swagger `POST /members` 성공 시 201과 생성 ID를 확인합니다.
6. DBeaver SELECT로 같은 회원의 저장 여부를 확인합니다.
7. 같은 이메일로 POST하여 409, DB Row 수 불변을 확인합니다.
8. `not-email`, `age: "abc"`, 범위를 벗어난 나이로 422를 확인합니다.
9. 개발용 SQL 컬럼명을 일부러 잘못 지정해 500 + rollback + DB 불변을 확인하고 **반드시 원복**합니다.
10. `GET /members/{member_id}` 상세 조회도 구현해 생성된 회원을 확인합니다.
11. 아래 Course API 과제의 실제 테이블을 검토한 뒤 구현합니다.
12. README에 Swagger / DB / 오류 Evidence를 기록하고 .env 제외 확인 후 Git에 커밋합니다.

## 6. Course Registration 과제

`POST /courses` 요청 예시:

```json
{
  "title": "FastAPI Basic",
  "instructor": "Kim",
  "capacity": 30
}
```

- 요청 모델을 정의하고 PostgreSQL `INSERT` + `RETURNING`으로 저장합니다.
- 정상 201, 필수 입력·타입 오류 422, 중복 강좌 규칙을 명시해 409를 구현합니다.
- 예기치 못한 SQL 오류 시 rollback 및 500을 확인합니다.
- **실제 courses 테이블 존재 여부/컬럼명은 아직 미확인**입니다. 과거 DBeaver에 다른 DB의 `course_project.courses` 등이 있었지만 현재 `postgres` DB에 동일한 테이블이 있다고 가정해서는 안 됩니다.
- 실제 스키마를 확인한 다음 SQL/모델을 확정합니다.

테이블 탐색용 SQL:

```sql
SELECT table_schema, table_name
FROM information_schema.tables
WHERE table_type = 'BASE TABLE'
  AND table_name = 'courses'
ORDER BY table_schema;
```

## 7. 제출 및 Definition of Done

- [ ] POST /members에서 정상 201과 생성 ID 확인.
- [ ] DBeaver SELECT가 Swagger 결과의 id/name/email/age와 일치.
- [ ] `GET /members/{member_id}`로 실제 생성 회원 조회.
- [ ] 동일 이메일 POST 시 409 및 DB 행 개수 불변 확인.
- [ ] Pydantic 잘못된 입력에서 422 확인.
- [ ] 의도적 DB 오류에서 500과 rollback, DB 불변 확인 후 원복.
- [ ] Connection/Cursor 종료 및 parameterized query 사용 확인.
- [ ] POST /courses 요구사항/테이블 구조 확인 및 201/409/422/rollback 검증.
- [ ] `.env`가 Git에 포함되지 않는지 검사.
- [ ] 실습/검증 Evidence를 README에 반영하고 Git Commit / Push.

### 검증 SQL (실제 응답값으로 바꿔 실행)

```sql
SELECT id, name, email, age
FROM public.members
WHERE id = 123; -- 실제 Swagger 응답의 ID로 교체
```

### GitHub 제출 준비

```powershell
cd C:\dev\fullstack-web-course
git check-ignore -v practice/phase02/chapter07/.env
git status --short
git add practice/phase02/chapter07
git diff --cached --name-only
git commit -m "Complete phase02 chapter07 POST insert transaction"
git push origin main
```

> **상태 구분:** 위는 7강 실습 계획/학습 문서입니다. 사용자 로컬 PostgreSQL에서 중복 처리 및 트랜잭션을 직접 실행했다는 증거는 아직 없으므로 완료로 표시하지 않습니다. 강의 원문 자체는 6강에서 일부 실행한 POST 흐름과 별개의 7강입니다.

---

출처: 아토믹데브, 「7강. POST /members + INSERT + Transaction」 (사용자가 제공한 강의 전문).
