> **공통 실행 안내 (최신):** 모든 명령은 `practice/phase02`에서 실행합니다.
> Python 환경을 활성화한 뒤 `python -m uvicorn chapter08.main:app --reload`처럼 강의 번호를 바꾸어 실행하세요. 5강은 `python -m chapter05.main`입니다. DB 설정은 `common/.env` 하나를 사용합니다. 기존 강의별 `.env`는 자동으로 읽지 않습니다. 아래 이전 안내의 개별 `db.py`, `.env`, 실행 경로는 이 안내로 대체합니다.

# 8강. PUT/PATCH + UPDATE — 전체 수정과 부분 수정

**원문:** 아토믹데브, 「8강. PUT/PATCH + UPDATE — 전체 수정과 부분 수정」 (2026-10-29).  
**작성:** 2026-11-02. **상태:** 코드·SQL·자동 테스트 작성 완료 / 사용자 로컬 PostgreSQL 수동 검증 전.  
**이전 강의:** [7강 POST + INSERT + Transaction](../chapter07/README.md)

## 1. API Contract를 먼저 구분

| Endpoint | 요청 내용 | 성공 | 실패 |
| --- | --- | --- | --- |
| `PUT /members/{member_id}` | `name, email, age` 모두 필수 | 200 + 수정된 회원 | 404, 409, 422 |
| `PATCH /members/{member_id}` | 변경할 필드만 선택 | 200 + 수정된 회원 | 빈 JSON=400, 대상 없음=404, 이메일 충돌=409, invalid/null=422 |
| `PUT /courses/{course_id}` | `title, instructor, capacity` 모두 필수 | 200 + 수정된 강좌 | 404, 409, 422 |
| `PATCH /courses/{course_id}` | 변경할 필드만 선택 | 200 + 수정된 강좌 | 400, 404, 409, 422 |

요청 유효성: `name` 1~100자, `email` 올바른 이메일, `age` 0~150. 강좌는 `title` 1~200자, `instructor` 1~100자, `capacity` 1~10000의 정수입니다.

**데이터베이스 구조 주의:** 강의 원문은 `member_id`를 쓰지만 이전 장에서 사용한 실제 테이블은 `postgres.public.members(id, name, email, age)`입니다. API URL 파라미터 이름은 `member_id`, **실제 SQL 컬럼 이름은 `id`**로 설정했습니다. 강좌도 `public.courses.id` 기준입니다.

## 2. 준비된 파일

- [main.py](main.py): 기존 GET/POST 기능 + 회원 및 강좌 PUT/PATCH, Pydantic 모델과 오류 처리
- [db.py](db.py): 기존 DB 접근 + UPDATE/RETURNING, SQL 매개변수 바인딩, 트랜잭션 commit/rollback
- [test_api.py](test_api.py): 실제 DB를 호출하지 않는 Mock 기반 API/트랜잭션 검증 **51개 테스트 정의** (실행 결과는 별도 확인 필요)
- [sql/01_preflight.sql](sql/01_preflight.sql): DB 테이블/컬럼/UNIQUE 상태 사전 확인
- [sql/02_verify_update.sql](sql/02_verify_update.sql): 수정 전후 DB SELECT 검증용
- [requirements.txt](requirements.txt): 실행 패키지 명세
- [.env.example](.env.example): 비밀번호 없는 설정 예시 / 실제 `.env`는 Git 제외
- [.gitignore](.gitignore): 비밀정보 및 캐시 파일 제외

## 3. PUT과 PATCH의 핵심 차이

`PUT /members/3`은 회원 수정 가능한 전체 데이터를 다시 보내는 계약입니다.

```json
{"name": "Kim Updated", "email": "kim-updated@example.com", "age": 31}
```

`PATCH /members/3`은 바뀌는 내용만 보냅니다.

```json
{"age": 31}
```

PATCH에서는 `name`, `email` 값이 원래 그대로여야 합니다.

| PATCH Request | 결과 | 이유 |
| --- | --- | --- |
| `{"age": 31}` | 200 | 전달한 age만 수정 |
| `{}` | 400 | 변경할 필드가 없음 |
| `{"email": null}` | 422 | 명시적 null은 이 계약에서 금지 |
| `{"age": -1}` | 422 | 입력값 범위 위반 |
| `{"email": "taken@example.com"}` | 409 | 다른 회원이 쓰는 이메일일 때 |
| `/members/999999` | 404 | 해당 회원이 없다면 |

`MemberPatch` 모델은 `model_fields_set`에서 **실제로 제출된 필드**를 확인하고, `None`이 명시적으로 제출되면 검증 오류(422)를 발생시킵니다. Endpoint는 `model_dump(exclude_unset=True)`로 **생략한 필드를 UPDATE에서 제외**합니다. `exclude_unset=True` 자체는 null을 거부하지 않습니다.

## 4. SQL 안전성과 트랜잭션

수정하려는 회원에 `SELECT ... FOR UPDATE`로 행 잠금을 걸어 존재 여부를 확인합니다. 이메일 수정 시 `WHERE email = %s AND id <> %s`로 **현재 회원 자신을 제외**하고 충돌을 검사합니다. 허용된 세 컬럼명(`name`, `email`, `age`)만 Python 코드에서 선택하며 사용자 값은 항상 `%s` placeholder로 전달합니다.

```sql
UPDATE public.members
SET age = %s
WHERE id = %s
RETURNING id, name, email, age;
```

성공: `UPDATE ... RETURNING` → `conn.commit()` → 200.  
실패: `conn.rollback()` → 404/409/500 등 적절한 오류 반환. 연결은 항상 `conn.close()`로 닫습니다.

**중요:** 이메일 중복 사전 SELECT만으로는 동시 요청의 중복을 완전히 막지 못합니다. `sql/01_preflight.sql`로 UNIQUE 인덱스 여부를 확인하고, 이미 존재하는 데이터와 다른 장의 코드를 검토한 후 필요하면 인덱스를 추가해야 합니다. 강좌 중복 기준은 기존 7강과 동일하게 **같은 title과 instructor 조합**입니다.

## 5. 준비 및 실행

1. 저장소를 최신화합니다. **로컬 변경사항은 `git status --short`로 확인하고 백업한 뒤 pull**합니다.
2. `chapter08` 폴더로 이동해 기존 설치된 Python/가상환경을 선택합니다.
3. 같은 폴더에 `.env`를 준비합니다. 7강의 로컬 `.env`를 복사해도 됩니다(비밀번호를 Git에 올리지 마세요).
4. DBeaver에서 `sql/01_preflight.sql`의 조회 쿼리를 먼저 실행합니다. 기존 데이터는 임의로 수정하지 않습니다.
5. 서버를 시작하고 Swagger `/docs`에서 PUT/PATCH를 검증합니다.

```powershell
cd C:\dev\fullstack-web-course\practice\phase02\chapter08
# 필요한 라이브러리가 없을 때만:
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload
```

브라우저: `http://127.0.0.1:8000/docs`  
자동 테스트: `python -m unittest -v test_api.py`

> **환경 주의:** 이전에 실제 문제가 되었던 `No module named psycopg`는 Python 실행 환경과 라이브러리 설치 위치가 달라서 발생했습니다. 이미 패키지가 있는 Python을 정확히 선택해 서버와 테스트를 실행하면 됩니다. 강좌별로 별도 Python 설치가 필수인 것은 아닙니다.

## 6. 실습 및 Evidence 절차

1. `GET /members` 또는 `GET /members/{member_id}`로 실제 존재하는 회원 ID와 원래 값을 적습니다.
2. `PUT /members/{member_id}`에 세 값을 모두 보내 200 및 응답을 확인하고 DBeaver SELECT를 실행합니다.
3. 같은 회원에게 `PATCH {"age": 31}`을 보내고 **나이만 바뀌는지** 확인합니다.
4. `PATCH {}`의 400을 확인합니다.
5. `PATCH {"email": null}`의 422 및 DB 변화가 없음을 확인합니다.
6. 없는 회원에 대한 PUT/PATCH의 404를 확인합니다.
7. 다른 회원이 사용하는 이메일로 수정해 409를 확인합니다. 같은 회원 자신의 이메일은 중복 처리하지 않아야 합니다.
8. `GET /members/{member_id}` 재조회 결과가 Swagger 응답과 DBeaver의 Row와 일치하는지 확인합니다.
9. 강좌 수정 과제: `GET /courses`로 실존 ID를 고르고 PUT/PATCH를 실행하여 전체/부분 수정, 400/404/409/422를 검증합니다. `public.courses`가 실제로 있는지 먼저 확인합니다.
10. `python -m unittest -v test_api.py`로 계약/트랜잭션 단위 검증을 실행합니다. **Mock 테스트 통과만으로 실제 DB 검증 완료라고 판단하지 않습니다.**

## 7. Definition of Done

- [ ] PUT과 PATCH의 의미 차이를 설명할 수 있다.
- [ ] 실제 회원 PUT이 세 필드를 DB에서 수정하고 200을 반환했다.
- [ ] 회원 PATCH가 **보낸 필드만 수정**했다.
- [ ] PATCH 필드 생략 / 명시적 null 차이를 설명하고 422로 확인했다.
- [ ] 빈 PATCH {} → 400을 확인했다.
- [ ] 존재하지 않는 회원 → 404를 확인했다.
- [ ] 이메일 충돌 → 409 및 DB 불변 확인.
- [ ] SQL 값에 Parameterized Query 사용을 확인했다.
- [ ] PUT/PATCH 결과, PostgreSQL SELECT, GET 재조회가 일치한다.
- [ ] 강좌 PUT/PATCH 실습 과제 검증.
- [ ] 실제 오류 발생 시 rollback 및 연결 종료를 확인했다.
- [ ] 자동 테스트를 실제로 실행하고 결과를 기록했다.
- [x] 코드·테스트·SQL·README 작성 및 Git 반영 *(코드만 준비, 실전 검증 별도)*.
- [ ] 사용자 PC의 .env가 Git 추적 대상이 아닌지 확인했다.

원문 강의에서 강조하는 핵심은 `PUT=전체 수정`, `PATCH=부분 수정`, `생략=기존 값 유지`, `explicit null=422`입니다. 이 강의는 SQL을 작성하는 것보다 **계약과 Evidence의 일치**에 초점을 둡니다.

출처: 아토믹데브, 「8강. PUT/PATCH + UPDATE — 전체 수정과 부분 수정」 (사용자가 제공한 강의 본문).
