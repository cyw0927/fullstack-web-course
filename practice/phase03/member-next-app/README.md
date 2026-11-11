# Member Next App — Phase 03 회원관리

**Next.js 16.4.6 + React 19.3.0 + TypeScript**로 만든 Fullstack Web Course의 회원관리 프론트엔드입니다. 자체 CSS로 구성한 관리자형 UI이며, 별도 FastAPI·PostgreSQL 서버와 연결합니다.

[저장소 메인](../../../README.md) · [Phase 03 전체 학습 기록](../README.md)

## 현재 구현된 기능

- **회원 목록:** FastAPI `GET /members`, 로딩·오류·빈 목록 표시, 이름/이메일 검색 및 다시 조회
- **회원 등록:** `POST /members` — 이름·이메일·나이·성별 입력
- **회원 수정:** `PUT /members/{member_id}` — 기존 입력값 자동 채우기
- **회원 삭제:** `DELETE /members/{member_id}` — 확인창 후 **실제 DB 삭제**
- **회원 상세:** 목록의 `상세 보기` 링크에서 `/members/[memberId]`로 이동, `GET /members/{member_id}` 호출
- **성별:** `M`(남성), `F`(여성), `null`(미지정) 목록·폼·상세 지원
- **관리 화면:** 검색·회원 목록·입력 패널을 분리한 UI, 버튼 활성화 상태 및 성공/실패 안내

> 현재 회원 데이터는 정적 배열이 아닌 **실제 PostgreSQL**에서 조회합니다. 초기 강의의 샘플 회원 3명 설명은 과거 실습 기록이며, 현재 앱의 최종 동작과는 다릅니다.

## 폴더 구조

```text
member-next-app/
├── app/
│   ├── page.tsx                      # / : 메인 회원관리
│   ├── members/
│   │   ├── page.tsx                  # /members : 목록·CRUD
│   │   └── [memberId]/page.tsx       # /members/1 : 상세 페이지
│   └── globals.css                   # 관리자 UI 스타일
├── components/
│   ├── MemberWorkspace.tsx           # 검색·조회·CRUD 폼/상태
│   ├── MemberList.tsx                # 회원 리스트
│   ├── MemberCard.tsx                # 회원 정보·상세 링크·수정·삭제
│   └── MemberDetail.tsx              # 회원별 GET 상세
├── lib/members-api.ts                # FastAPI fetch 함수들
├── types/member.ts                   # Member 타입
├── package.json
└── README.md
```

## 실행 (Windows / PowerShell)

**먼저 FastAPI와 PostgreSQL이 정상 실행 중인지 확인하세요.**

### 1. Backend 실행 (별도 터미널)

```powershell
cd C:\dev\fullstack-web-course\practice\phase03\backend

# backend\.env에 실제 DB 설정이 있어야 합니다.
& "..\.venv\Scripts\python.exe" -m uvicorn app.main:app --reload --port 8000
```

환경을 새로 설치하는 방법은 [Phase 03 README](../README.md#4-로컬-실행)를 확인하세요.

### 2. Frontend 실행

```powershell
cd C:\dev\fullstack-web-course\practice\phase03\member-next-app

npm ci
npm run dev
```

실행 전 `member-next-app/.env.local` 파일에 아래 설정이 필요합니다.

```dotenv
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000
```

`.env.local`은 Git에 올리지 않습니다. 값 수정 후에는 `npm run dev`를 다시 시작하세요.

### 3. 접속

| 화면 | 주소 |
| --- | --- |
| 메인 | <http://localhost:3000/> |
| 회원 목록·CRUD | <http://localhost:3000/members> |
| 특정 회원 상세 | <http://localhost:3000/members/1> (실제 존재하는 ID 기준) |
| FastAPI Swagger | <http://127.0.0.1:8000/docs> |

## API와 TypeScript 데이터

`lib/members-api.ts`의 함수:

| 함수 | HTTP 요청 | 역할 |
| --- | --- | --- |
| `getMembers()` | `GET /members` | 회원 배열 조회 |
| `getMember(id)` | `GET /members/{id}` | 회원 한 명 조회 |
| `createMember(body)` | `POST /members` | 신규 등록 |
| `updateMember(id, body)` | `PUT /members/{id}` | 기존 회원 수정 |
| `deleteMember(id)` | `DELETE /members/{id}` | 회원 삭제 |

회원 타입은 `member_id: number`, `name: string`, `email: string`, `age: number`, `gender?: "M" | "F" | null`입니다.

등록·수정 후에는 `getMembers()`를 다시 호출해 최신 목록을 표시합니다. 상세 조회 `getMember()`는 별도의 단일 회원 JSON을 받습니다.

**성별 주의:** 등록·수정 폼에서 미지정을 선택하면 `gender: null`을 보내며, DB의 기존 성별을 유지하려면 편집 폼에 자동 채워진 값을 그대로 두세요.

## 코드 검사 및 빌드

```powershell
cd C:\dev\fullstack-web-course\practice\phase03\member-next-app

npx tsc --noEmit
npm run lint
npm run build
```

2026-11-11 로컬 실습에서 최종 TypeScript·ESLint·프로덕션 빌드 성공을 확인했습니다. `/members/[memberId]`는 Next.js 16의 `useParams()` 런타임 데이터 제약으로 `Suspense` 경계를 사용합니다.

## 안전 및 문제 해결

- **회원 삭제는 소프트 삭제가 아닙니다.** 실제 DB 행이 삭제되므로 직접 만든 테스트 회원으로만 실습하세요.
- `Failed to fetch`: FastAPI 실행 여부·포트·`NEXT_PUBLIC_API_BASE_URL` 확인
- CORS 오류: 브라우저 Origin이 FastAPI의 허용 Origin(기본 `localhost:3000` 포함)에 있는지 확인
- `404` 상세 조회: 실제 존재하는 `member_id`인지 확인
- `422`: 나이·이메일·성별 형식 확인 (`gender`는 `M`/`F`/`null`)
- `409`: 이메일 중복 확인
- `npm run build`에서 `useParams()` 오류: `app/members/[memberId]/page.tsx`의 `Suspense` 적용 확인
- 실제 DB 구조는 백엔드 `app/models.py`와 일치해야 하며, `gender` 컬럼은 별도로 생성해야 합니다.
- `.env.local`, 실제 DB 접속정보, `node_modules`, `.next`는 Git에 올리지 않습니다.

이 저장소는 학습용으로, 실제 운영 서비스에 필요한 인증·권한·백업 및 복구 기능까지 제공하는 것은 아닙니다.
