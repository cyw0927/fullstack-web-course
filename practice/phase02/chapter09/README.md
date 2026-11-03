> **공통 실행 안내 (최신):** 모든 명령은 `practice/phase02`에서 실행합니다.
> Python 환경을 활성화한 뒤 `python -m uvicorn chapter08.main:app --reload`처럼 강의 번호를 바꾸어 실행하세요. 5강은 `python -m chapter05.main`입니다. DB 설정은 `common/.env` 하나를 사용합니다. 기존 강의별 `.env`는 자동으로 읽지 않습니다. 아래 이전 안내의 개별 `db.py`, `.env`, 실행 경로는 이 안내로 대체합니다.

# 9강. 회원 삭제 DELETE API + PostgreSQL DELETE

**강의:** 아토믹데브, 「9강. 회원 삭제 DELETE API + PostgreSQL DELETE」 (2026-10-29)  
**실습 상태:** GitHub 코드·테스트·검증 SQL 준비 / 실제 PostgreSQL 삭제 Evidence 미확인

## 이번 장은 DELETE에만 집중합니다

[8강 PUT/PATCH](../chapter08/README.md)에서 이미 수정 API를 실습했으므로, 9강 Swagger에는 **회원 상세 조회(GET)와 회원 삭제(DELETE) 두 엔드포인트만** 표시되게 했습니다. 별도 강의 폴더여서 앞 장의 코드와 데이터를 지우거나 변경하지 않습니다.

| Method | Path | 성공 | 실패 |
| --- | --- | --- | --- |
| GET | `/members/{member_id}` | 200 + 회원 JSON | 404(없음), 422(정수가 아님), 500(DB 오류) |
| DELETE | `/members/{member_id}` | **204 No Content, Body 없음** | 404(없음), 422(정수가 아님), 500(DB 오류) |

- Request Body는 없습니다. 삭제할 회원은 Path Parameter `member_id`로 지정합니다.
- 강의 SQL은 `member_id` 컬럼을 사용하지만, **사용자가 실제 사용한 PostgreSQL 테이블의 PK 컬럼은 `id`**입니다. 그러므로 SQL은 `public.members WHERE id = %s`로 작성했습니다.
- 204는 응답 본문이 없어야 합니다. `{"message": "deleted"}` 같은 JSON을 반환하지 않습니다.

## 파일

- [main.py](main.py) — GET 상세 조회, DELETE API와 HTTP 204/404/422/500
- [db.py](db.py) — PostgreSQL 연결, parameterized `DELETE ... RETURNING id`, 명시적 commit/rollback
- [test_api.py](test_api.py) — **13개 단위 테스트 작성** (Mock으로 HTTP 계약·commit/rollback 확인; 실행 전)
- [sql/verify_delete.sql](sql/verify_delete.sql) — DBeaver에서 안전하게 삭제 대상 준비/조회하는 SQL
- [requirements.txt](requirements.txt) — Python 의존성 목록
- [.env.example](.env.example) — 비밀번호가 없는 환경변수 예시
- [.gitignore](.gitignore) — 실제 `.env` 및 캐시 제외

## 어떻게 동작하나요?

```text
DELETE /members/{member_id}
  → FastAPI가 정수 Path인지 검증 (아니면 422)
  → psycopg로 PostgreSQL 연결
  → DELETE FROM public.members WHERE id = %s RETURNING id;
        ├─ 삭제된 행 반환 → conn.commit() → 204 (Body 없음)
        ├─ 반환값 None → conn.rollback() → 404
        └─ SQL/commit 오류 → conn.rollback() → 500
  → 항상 conn.close()
```

예제 SQL:

```sql
DELETE FROM public.members
WHERE id = %s
RETURNING id;
```

`%s` 값은 `cur.execute(sql, (member_id,))`처럼 별도로 전달합니다. 입력을 SQL 문자열에 직접 붙이지 않습니다.

**트랜잭션 설명:** DELETE가 실행되었다고 영구 저장이 확정되는 것은 아닙니다. 성공한 DELETE에 대해서만 `commit()`을 호출합니다. 이번 `db.py`는 `with conn`을 사용하지 않고 `try/except/finally`로 명시적으로 commit/rollback/close를 처리하므로, commit 호출을 제거하면 연결 종료 시 미확정 변경이 롤백됩니다. **실험은 삭제 전용 테스트 행으로만 하세요.**

## 실행하기

로컬 경로: `C:\dev\fullstack-web-course\practice\phase02\chapter09`

프로젝트 루트에서 `git status --short`를 먼저 확인하세요. 수정사항이 없을 때는 `git pull --ff-only origin main`으로 9강 코드를 가져옵니다. 이전 실습 파일을 수정 중이면 먼저 별도 백업하고 동기화합니다.

```powershell
cd C:\dev\fullstack-web-course\practice\phase02\chapter09
# 이미 8강에서 사용하던 접속 정보가 있으면 로컬에서만 복사
Copy-Item ..\chapter08\.env .env
# 기존에 FastAPI/psycopg를 설치한 Python 환경으로 실행
python -m uvicorn main:app --reload
```

`chapter08/.env`가 없는 경우 `.env.example`을 `.env`로 복사한 후 실제 설정을 작성하세요. 필요한 라이브러리가 누락됐을 때만 해당 Python 환경에서 `python -m pip install -r requirements.txt`를 실행합니다. 서버 주소는 `http://127.0.0.1:8000/docs`입니다.

## 실제 DB Evidence — 반드시 전후 비교

**주의: DELETE는 파괴적입니다.** 기존 김/이/홍길동/영우처럼 이미 쓰던 학습 회원 ID로 시험하지 마세요. 먼저 DBeaver에서 별도 테스트 회원을 삽입하고, `RETURNING`으로 얻은 ID만 삭제하세요.

1. [검증 SQL](sql/verify_delete.sql)을 열고 주석으로 된 실습용 `INSERT` 한 문장만 실행해 새 ID를 확보합니다. `DB_NAME=postgres` / `public.members`인지 확인합니다.
2. `GET /members/{실제 ID}` → **200**, 회원 JSON을 캡처합니다.
3. `DELETE /members/{실제 ID}` → **204**, **Response Body가 비어 있는지** 캡처합니다.
4. DBeaver에서 `SELECT id, name, email, age FROM public.members WHERE id = {실제 ID};` → **0 rows**를 확인합니다.
5. 다시 `GET /members/{실제 ID}` → **404**.
6. 같은 ID로 `DELETE` 한 번 더 요청 → **404**. 잘못된 ID `abc` → **422**.
7. SQL 컬럼명을 일부러 잘못 쓰는 500/rollback 실험은 **테스트 회원을 새로 만들고 별도로** 진행하며, 끝나면 코드를 반드시 복구합니다.

완료 조건:

```text
Swagger DELETE = 204 (Body 없음)
       ⇕
PostgreSQL SELECT = 0 rows
       ⇕
GET 상세 재조회 = 404
```

**구현 코드/Mock 테스트만으로 실제 DB에서 삭제되었다고 판단하지 않습니다.** 실제 회원을 참조하는 다른 테이블에 외래키가 있으면 DELETE가 제약조건 오류로 실패할 수 있으므로 임의의 `CASCADE`를 추가하지 않습니다.

## Definition of Done

- [x] DELETE 엔드포인트, SQL 및 단위 테스트 파일 작성
- [ ] Swagger에서 DELETE 엔드포인트 확인
- [ ] 테스트 회원 삭제 응답 204 및 빈 Body 확인
- [ ] DB SELECT 0 rows 확인
- [ ] 삭제 후 GET 404, 재삭제 404 확인
- [ ] 잘못된 ID 422 확인
- [ ] 오류 실험 후 rollback 및 복구 확인
- [ ] 테스트 파일을 실제로 실행하고 결과 기록
- [ ] `git check-ignore -v practice/phase02/chapter09/.env`로 Secret 제외 확인
- [x] GitHub에 학습용 코드 반영 (실제 실습 완료와는 별도)

---

출처: 아토믹데브, 「9강. 회원 삭제 DELETE API + PostgreSQL DELETE」 (사용자가 제공한 강의 본문).
