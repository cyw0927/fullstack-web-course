# Phase 03 — Next.js + FastAPI 회원관리 프로젝트

> **기준: 2026-11-11 / 6강 및 성별 필드 추가 실습까지**  
> React·TypeScript·Next.js App Router로 화면을 구성하고, FastAPI·SQLAlchemy·PostgreSQL과 연결해 실제 회원 데이터를 관리합니다.

[저장소 메인](../../README.md) · [Next.js 실행 안내](member-next-app/README.md) · [Phase 02 Backend](../phase02/README.md)

## 1. 현재까지의 학습 진행

| 단계 | 배운 내용 | 주요 구현 |
| --- | --- | --- |
| 1강 | Next.js 개발 환경·App Router | 프로젝트 생성, 첫 화면 |
| 2강 | React 컴포넌트·Props·TypeScript | `Member` 타입, `MemberList`, `MemberCard` |
| 3강 | State·Event·Form | 회원 검색 및 입력 폼 기초 |
| 4강 | FastAPI GET 연동 | 실제 회원 목록, 로딩·오류·다시 조회·검색 |
| **5강** | **CRUD 완성** | **등록 POST / 수정 PUT / 삭제 DELETE 및 재조회** |
| **6강** | **페이지 이동·회원 상세** | **`/members` → `/members/[memberId]`, `Link`, `useParams`, 상세 GET** |
| **추가 실습** | **성별 필드 확장** | **`gender`: DB 컬럼 → Backend 모델/스키마/CRUD → 프론트 목록·폼·상세** |

7~8강은 별도 후속 학습 범위이며, 이 문서는 해당 기능이 구현됐다고 주장하지 않습니다.

### 실제로 확인한 내용

- Swagger에서 전체·상세 조회, 테스트 회원 등록·수정 및 성별 응답을 확인했습니다.
- Next.js 브라우저에서 회원 검색, 등록·수정·삭제, 상세 보기 이동 및 성별 선택·표시를 실습했습니다.
- `npx tsc --noEmit`, ESLint, `npm run build`를 실행했으며, 상세 페이지의 `Suspense` 경계를 추가한 후 최종 빌드 성공 로그를 확인했습니다.
- 이 기록은 **로컬 실습 결과**이며 운영 배포·CI·자동 E2E 테스트 통과를 의미하지 않습니다.

## 2. 데이터 흐름

```text
브라우저 (Next.js / React / TypeScript, :3000)
    ↓ fetch / JSON
FastAPI (Uvicorn, :8000)
    ↓ Pydantic 입력 검증
Router → Service → Repository → SQLAlchemy
    ↓ SQL
PostgreSQL (public.members)
    ↑
GET 응답 JSON → Next.js 회원 목록·상세 화면 갱신
```

- **Frontend:** 화면, 입력 검증, 검색·상태 관리, 서버 요청
- **Backend:** 라우팅, 요청·응답 형식 검증, 중복 이메일 처리, DB 트랜잭션
- **DB:** 회원 데이터 저장 및 조회
- **DBeaver:** DB 테이블·데이터 확인에 사용하는 별도 SQL 클라이언트 (애플리케이션 실행에 필수는 아님)

## 3. 디렉터리 및 파일 역할

```text
practice/phase03/
├── README.md
├── backend/
│   ├── .env.example
│   ├── requirements.txt
│   └── app/
│       ├── main.py                     # FastAPI 앱 / CORS
│       ├── db.py                       # SQLAlchemy Engine·Session / .env
│       ├── models.py                   # public.members ORM
│       ├── schemas.py                  # Create / Update / Patch / Response
│       ├── routers/member_router.py    # HTTP 메서드와 URL
│       ├── services/member_service.py  # 업무 규칙·HTTP 오류
│       └── repositories/member_repository.py # DB CRUD / commit·rollback
└── member-next-app/
    ├── app/
    │   ├── page.tsx                    # / (메인 회원관리)
    │   ├── members/page.tsx            # /members (회원 목록·CRUD)
    │   ├── members/[memberId]/page.tsx # /members/1 (동적 상세)
    │   └── globals.css                 # UI 스타일
    ├── components/
    │   ├── MemberWorkspace.tsx         # 목록·검색·등록·수정·삭제 상태
    │   ├── MemberList.tsx              # 회원 목록
    │   ├── MemberCard.tsx              # 회원 행·상세 링크·수정·삭제
    │   └── MemberDetail.tsx            # useParams + 상세 조회
    ├── lib/members-api.ts              # fetch 기반 API 호출
    ├── types/member.ts                 # TypeScript Member 타입
    └── package.json
```

프론트엔드는 **Next.js 16.4.6 / React 19.3.0 / TypeScript**, 백엔드는 **FastAPI / Pydantic / SQLAlchemy / PostgreSQL**을 사용합니다. CSS는 자체 스타일이며 Tailwind를 필수로 사용하지 않습니다.

## 4. 로컬 실행

현재 사용자 실습 경로: `C:\dev\fullstack-web-course`. 강의 자료에 예시로 나오는 `C:\dev\phase03`이 아닙니다.

### 준비: PostgreSQL

기존 `public.members` 테이블이 있어야 합니다. 실제 스키마는 아래 형태를 기준으로 앱과 맞춥니다.

| 컬럼 | 타입/규칙 | 설명 |
| --- | --- | --- |
| `member_id` | 정수, PK | 회원 ID |
| `name` | 문자열(최대 100자), 필수 | 이름 |
| `email` | 문자열(최대 255자), UNIQUE | 이메일 |
| `age` | 정수, 필수 | 나이(요청 검증: 0~150) |
| `gender` | `VARCHAR(20)`, nullable | `M` 남성 / `F` 여성 / `NULL` 미지정 |

**기존 DB에만 성별 컬럼이 없다면** DBeaver 등에서 스키마를 확인한 뒤 다음 문장을 **한 번** 적용할 수 있습니다.

```sql
ALTER TABLE public.members
ADD COLUMN IF NOT EXISTS gender VARCHAR(20);
```

기존 회원의 성별을 이름으로 추측하여 자동 설정하지 않습니다. 기존 DB에 저장된 값은 그대로 보존하세요. SQLAlchemy 모델을 변경해도 이 DB 스키마 변경이 자동 실행되지는 않습니다.

### 터미널 1 — FastAPI

```powershell
cd C:\dev\fullstack-web-course\practice\phase03\backend

# 신규 환경에서만 가상환경 생성 및 의존성 설치
py -3 -m venv ..\.venv
& "..\.venv\Scripts\python.exe" -m pip install -r requirements.txt

# .env.example을 참고하여 backend\.env를 별도로 작성하고 DB 접속값 기입
& "..\.venv\Scripts\python.exe" -m uvicorn app.main:app --reload --port 8000
```

`backend/.env`는 Git에 올리지 않습니다. 예시 환경변수:

```dotenv
DB_HOST=localhost
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=여기에_본인_DB_암호
```

실제 비밀번호·접속 정보는 각자의 환경에 맞춥니다. API 문서: <http://127.0.0.1:8000/docs>.

### 터미널 2 — Next.js

```powershell
cd C:\dev\fullstack-web-course\practice\phase03\member-next-app
npm ci

# .env.local 파일을 만들고 아래 변수를 설정
# NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000

npm run dev
```

- <http://localhost:3000/>: 기본 회원관리 화면
- <http://localhost:3000/members>: 회원 목록·관리
- <http://localhost:3000/members/1>: 1번 회원 상세 (실제로 존재할 때)

API 서버가 켜져 있어야 실데이터가 조회됩니다. `.env.local` 변경 후에는 프론트 개발 서버를 다시 시작하세요.

## 5. API 계약

| 메서드 | 경로 | 기대 상태 / 기능 |
| --- | --- | --- |
| GET | `/members` | `200`, 회원 배열 |
| GET | `/members/{member_id}` | `200`, 회원 하나 / 없는 ID `404` |
| POST | `/members` | `201`, 신규 회원 생성 / 이메일 충돌 `409` |
| PUT | `/members/{member_id}` | `200`, 이름·이메일·나이 필수 + 성별 선택 |
| PATCH | `/members/{member_id}` | `200`, 전달된 일부 필드 수정 |
| DELETE | `/members/{member_id}` | `204`, 실제 회원 행 삭제 |

요청 검증 실패는 일반적으로 `422`로 응답합니다. `PATCH`는 명시적 `null` 입력을 거부하며 빈 변경 사항은 업무 규칙에서 거부합니다.

### 성별을 포함한 예시

```json
{
  "name": "테스트회원",
  "email": "student-test@example.com",
  "age": 25,
  "gender": "F"
}
```

- `M` = 남성, `F` = 여성, `null` = 미지정.
- **POST:** `gender`를 생략해도 등록 가능합니다.
- **PUT:** `gender`를 요청에서 **생략**하면 기존 성별을 보존합니다. 명시적으로 `null`을 보내면 미지정으로 바뀔 수 있습니다.
- **Next.js 폼:** 미지정을 선택하면 `gender: null`을 전송합니다.
- DB에는 `gender` 컬럼을 추가했지만 **소프트 삭제 컬럼은 없습니다.** DELETE는 실제 행을 지웁니다.

## 6. 프론트엔드 동작

- 회원 목록: 전체 조회, 이름·이메일 검색, 검색 초기화, 다시 조회
- 회원 등록: 이름·이메일·나이·성별 입력 → POST → GET 재조회
- 회원 수정: 기존 정보 자동 입력 → PUT → GET 재조회
- 회원 삭제: 확인창 → DELETE → GET 재조회 (**복구 기능 없음**)
- 상세 페이지: 회원별 `/members/{memberId}` 이동 → GET 상세 호출 → 목록 복귀
- 오류·로딩: 로딩 표시, API 오류 표시, 빈 목록 표시
- **Next.js 16 빌드 주의:** `useParams()`를 사용하는 `MemberDetail`을 `Suspense`로 감쌉니다. 개발 서버 정상 동작과 프로덕션 빌드 검사는 별개입니다.

## 7. 검증

```powershell
cd C:\dev\fullstack-web-course\practice\phase03\member-next-app

npx tsc --noEmit
npm run lint
npm run build
```

수동 검증은 **직접 만든 실습용 회원**으로 수행합니다.

1. Swagger GET 목록·상세, 서버 응답의 `member_id`·`gender` 확인
2. Next.js에서 테스트 회원 등록 → 목록에 나타나는지 확인
3. 그 회원의 나이·성별 수정 → 상세 페이지·DBeaver에서 확인
4. 상세 보기 → 목록 돌아가기, 검색·초기화 확인
5. 필요 시 **해당 테스트 회원만** 삭제 확인

**주의:** 이 실습의 DB DELETE는 실제 삭제입니다. 기존 회원이나 다른 사람이 만든 데이터를 지우지 마세요. Git에는 `backend/.env`, `member-next-app/.env.local`, `node_modules`, `.next`, `.venv`를 올리지 않습니다.

## 다음 학습

이후 강의에서는 오류 처리, 로딩/빈 데이터 검증, API·프론트 통합 검사를 더 강화할 예정입니다. **미구현 기능을 완료로 표시하지 않습니다.**
