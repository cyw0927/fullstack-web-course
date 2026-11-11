# Fullstack Web Course

HTML부터 데이터베이스까지, **직접 실행하고 검증하면서 배우는 풀스택 웹 개발 실습 저장소**입니다.

**현재 학습 범위 (2026-11-11):** HTML·CSS·JavaScript 기초 → Python/FastAPI·PostgreSQL → React·TypeScript·Next.js. **Phase 03 6강(회원 목록·상세 페이지) 및 성별 필드 확장 실습**까지 구현했습니다.

> 이 저장소는 강의별 실습 기록입니다. 각 장의 코드·테스트 상태는 해당 README를 기준으로 확인하세요. 일부 초기 과제는 정적 페이지이며, 현재의 DB 연동 회원관리 앱과 별개입니다.

## 학습 현황

| 과정 | 핵심 내용 | 자료 |
| --- | --- | --- |
| **Phase 01 · Frontend Basic** | HTML·시멘틱 태그·CSS 레이아웃·반응형·JavaScript·DOM·API 통신 기초 | [실습 폴더](practice/phase01/) |
| **Phase 02 · Backend** | FastAPI·Pydantic·PostgreSQL 실습. 1~9강 코드와 10강 계층 분리 실습(진행 중) | [학습 기록](practice/phase02/README.md) |
| **Phase 03 · Fullstack** | Next.js App Router, React, TypeScript, FastAPI 연동, 회원 CRUD, 동적 상세 페이지 | **[최신 진행 기록](practice/phase03/README.md)** |
| **Special · RAG** | Upstage Solar 기반 RAG 특강 준비 | [특강 자료](practice/special/rag-solar/README.md) |

### Phase 03 최근 작업

- **1~3강:** 개발 환경, 컴포넌트·Props·TypeScript, React State·이벤트·입력 폼
- **4강:** `GET /members`로 PostgreSQL의 실제 회원 목록 조회, 검색·로딩·오류 처리
- **5강:** `POST` 등록, `PUT` 수정, `DELETE` 삭제와 등록/수정 폼 연결
- **6강:** `/members` 목록 및 `/members/[memberId]` 상세 페이지, `GET /members/{member_id}`, Next.js `Link`·`useParams`
- **추가 실습:** `gender` 필드(`M`/`F`/`null`)를 DB → FastAPI → Next.js까지 연결하여 등록·수정·목록·상세에서 처리
- **UI:** 검색 패널, 회원 목록, 등록/수정 패널을 갖춘 관리자형 화면으로 정리
- **검증:** 사용자가 로컬에서 CRUD·회원 상세·성별 입출력을 확인했고, 최종 TypeScript 검사 및 Next.js 프로덕션 빌드가 성공했습니다. 실제 운영 배포는 별도입니다.

## 프로젝트 구조

```text
practice/
├── phase01/                     # HTML / CSS / JavaScript 기초
│   ├── chapter01/, chapter02/, chapter03/
│   ├── chapter06/, chapter07/, chapter08/
│   └── chapter15-prepractice/, chapter15/
├── phase02/                     # FastAPI·PostgreSQL 단계별 실습
│   ├── README.md
│   ├── common/
│   └── chapter01/ ... chapter10/
├── phase03/
│   ├── README.md                 # Phase 03 상세 강의 기록
│   ├── backend/                  # FastAPI + SQLAlchemy
│   │   ├── app/
│   │   ├── .env.example
│   │   └── requirements.txt
│   └── member-next-app/          # Next.js 16 + TypeScript
│       ├── app/
│       ├── components/
│       ├── lib/
│       ├── types/
│       └── README.md
└── special/
    └── rag-solar/
```

**참고:** Phase 01의 일부 강의 번호는 원본 실습 파일이 없는 상태라 건너뛰어져 있습니다. 폴더가 존재한다는 사실과 모든 강의를 검증했다는 의미는 다릅니다.

## Phase 03 회원관리 앱 실행 (Windows / PowerShell)

**전제 조건:** Node.js·npm, Python, PostgreSQL과 기존 `public.members` 테이블이 필요합니다. DB 생성·초기 데이터 준비는 이 프로젝트의 실행 명령만으로 자동 처리되지 않습니다.

### 1. 백엔드 — FastAPI

```powershell
cd C:\dev\fullstack-web-course\practice\phase03\backend

# 최초 환경 구성 시에만 사용
py -3 -m venv ..\.venv
& "..\.venv\Scripts\python.exe" -m pip install -r requirements.txt

# .env.example을 참고해 backend\.env에 실제 DB 접속값 설정
# 기존 .env 파일은 덮어쓰지 마세요.
& "..\.venv\Scripts\python.exe" -m uvicorn app.main:app --reload --port 8000
```

- Swagger: <http://127.0.0.1:8000/docs>
- DB 환경변수: `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`
- 비밀번호는 `.env`에만 보관하고 커밋하지 않습니다.

### 2. 프론트엔드 — Next.js

**별도 터미널**에서 실행합니다.

```powershell
cd C:\dev\fullstack-web-course\practice\phase03\member-next-app
npm ci

# member-next-app\.env.local에 다음 값 설정
# NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000

npm run dev
```

- 메인: <http://localhost:3000/>
- 회원 목록·관리: <http://localhost:3000/members>
- 회원 상세 예시: <http://localhost:3000/members/1> (실제 존재하는 ID 기준)

`NEXT_PUBLIC_API_BASE_URL`이 없거나 백엔드가 실행되지 않으면 회원 조회가 실패합니다. 환경변수를 변경했다면 Next.js 개발 서버를 다시 시작하세요.

### 3. 타입·정적 분석·빌드 검사

```powershell
cd C:\dev\fullstack-web-course\practice\phase03\member-next-app

npx tsc --noEmit
npm run lint
npm run build
```

Next.js 16의 동적 상세 페이지는 `useParams()`를 사용하는 클라이언트 컴포넌트를 `Suspense`로 감싸 프로덕션 빌드에 대응합니다. 로컬 브라우저 동작과 빌드 성공은 별도로 검증합니다.

## 현재 회원 API

| 메서드 | 경로 | 용도 |
| --- | --- | --- |
| GET | `/members` | 전체 회원 조회 |
| GET | `/members/{member_id}` | 회원 상세 조회 |
| POST | `/members` | 회원 등록 (`201`) |
| PUT | `/members/{member_id}` | 회원 전체 기본 정보 수정 |
| PATCH | `/members/{member_id}` | 전달한 필드만 수정 |
| DELETE | `/members/{member_id}` | 회원 실제 삭제 (`204`) |

회원 데이터: `member_id`, `name`, `email`, `age`, `gender`. 성별은 `M`(남성), `F`(여성), `null`(미지정)이며, 기존 API 호출과의 호환성을 위해 선택 항목입니다. 상세 내용은 [Phase 03 README](practice/phase03/README.md)를 참고하세요.

**중요:** 현재 DELETE는 **소프트 삭제가 아니라 실제 행 삭제**입니다. 기존 데이터를 대상으로 테스트하지 말고 본인이 만든 테스트 회원만 사용하세요. 또한 DBeaver에서 직접 추가한 DB 컬럼은 Git에 자동 반영되지 않으므로 다른 환경에서 실행할 때 스키마를 별도로 맞춰야 합니다.

## 상세 문서·빠른 링크

- [Phase 01 실습 파일](practice/phase01/)
- [Phase 02 Backend 학습 기록](practice/phase02/README.md)
- [Phase 03 Fullstack 강의별 정리](practice/phase03/README.md)
- [Next.js 회원관리 앱 실행 안내](practice/phase03/member-next-app/README.md)
- [회원 API Swagger (로컬 실행 시)](http://127.0.0.1:8000/docs)
- [정적 HTML 수강 신청 과제 (GitHub Pages)](https://cyw0927.github.io/fullstack-web-course/practice/phase01/chapter03/assignment.html)

---

학습용 저장소로, 비밀키·실제 고객 데이터·개인정보를 Git에 올리지 않습니다. 작성 시점의 코드와 실제 실행 환경이 다를 수 있으므로 최신 소스 및 Swagger 응답을 우선하세요.
