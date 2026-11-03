# 10강: Backend 구조화 실습

이번 폴더는 **직접 완성하는 출발점**입니다. 현재 앱과 라우터, 회원 스키마는 준비되어 있지만 회원 목록 조회 SQL은 작성되어 있으며, 회원 CRUD 엔드포인트와 서비스 및 나머지 SQL은 아직 구현하지 않았습니다.

요청 흐름: `Router → Service → Repository → DB`, 데이터 형태: `schemas.py`.

- `app/main.py`: 앱을 만들고 라우터를 연결합니다.
- `app/routers/members.py`: URL, HTTP 응답과 서비스를 연결합니다.
- `app/services/member_service.py`: 회원 존재·중복 등 업무 규칙을 작성합니다.
- `app/repositories/member_repository.py`: PostgreSQL 조회·저장·수정·삭제를 작성합니다.
- `app/schemas.py`: 요청과 응답 데이터의 형태를 정의합니다.
- `app/db.py`: 기존 `common/db.py`의 연결 함수를 가져옵니다.

## 실행

`practice/phase02` 폴더에서 실행합니다. 기존 Python 환경과 `common/.env`를 사용합니다.

```powershell
python -m uvicorn chapter10.app.main:app --reload --port 8000
```

브라우저에서 http://127.0.0.1:8000/docs 를 엽니다. 아직 회원 API를 작성하기 전이므로 Swagger에 회원 엔드포인트가 보이지 않는 것이 정상입니다. 8000번 포트가 이미 사용 중이면 다른 포트를 지정하세요.

실제 회원 테이블은 `public.members(id, name, email, age)`입니다. 강의 예시의 `member_id` 대신 `id`를 사용해야 기존 DB 및 API 응답과 맞습니다. `common/.env`는 Git에 올리지 않습니다. 실제 DB를 수정하는 실습은 테스트 데이터로만 진행하세요.
