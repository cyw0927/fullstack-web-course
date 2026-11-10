# Phase 03 — Next.js / React / TypeScript

Phase 03에는 프론트엔드 실습 파일을 저장합니다. TypeScript, React, Next.js를 배우고 Phase 02에서 만든 FastAPI API를 화면과 연결하는 것이 목표입니다.

- 학습 예정: TypeScript, React, Next.js
- 목표: Phase 02 FastAPI API를 재사용해 프론트엔드 화면 구성
- 이전 과정: [Phase 01](../phase01/) · [Phase 02](../phase02/)

## 1강: 개발환경 복구와 첫 회원관리 화면

Next.js App Router와 TypeScript로 첫 화면을 구성합니다. 1강에서는 API나 DB를 연결하지 않습니다. 2~8강에서도 `member-next-app` 프로젝트를 계속 사용합니다.

## 2강: React Component와 TypeScript로 회원 목록 만들기 (2026-11-10)

1강에서 생성한 `member-next-app`을 그대로 재사용하고, 샘플 회원 3명을 컴포넌트로 나누어 표시했습니다. 이번 강의는 정적 샘플 데이터로 진행하며, FastAPI·PostgreSQL 연결이나 수정은 하지 않습니다.

### 파일 및 역할

| 경로 | 역할 |
| --- | --- |
| `member-next-app/types/member.ts` | `Member` 타입 정의(`member_id`, `name`, `email`, `age`) |
| `member-next-app/components/MemberCard.tsx` | 회원 한 명의 이름·이메일·나이·ID 표시 |
| `member-next-app/components/MemberList.tsx` | `Member[]`를 받아 카드 반복 렌더링, 0명일 때 안내 |
| `member-next-app/app/page.tsx` | Kim(30), Lee(27), Park(35) 샘플 배열을 `MemberList`에 전달 |

### 배운 내용

- **Component**: 화면을 역할별로 분리(`HomePage → MemberList → MemberCard`).
- **Props**: 부모에서 자식으로 `members` 배열 및 개별 `member` 데이터를 전달.
- **TypeScript**: 회원의 필드와 데이터 타입을 정의하고 `age: "thirty"` 오류를 타입 검사로 탐지.
- **조건부 렌더링**: `members.length === 0`이면 '등록된 회원이 없습니다.'를 표시.
- **반복 렌더링**: `members.map()`과 `key={member.member_id}`를 사용.
- 강의에서는 `member_id`를 사용하지만 기존 Phase 02 DB의 컬럼은 `id`이므로, 4강 API 연동 시 실제 Swagger 응답과 비교해야 함.

### 실습 및 검증 기록

2026-11-10 실습자가 확인·보고한 결과입니다(이 README 작성 과정에서 로컬 명령을 재실행한 것은 아님).

- [x] 브라우저에 회원 목록 3명(Kim / Lee / Park) 출력.
- [x] Park 나이 `35 → 36` 수정 시 화면 즉시 반영 확인 후 `35`로 복구.
- [x] Kim의 나이를 문자열 `"thirty"`로 바꿔 TypeScript 오류 재현 후 숫자 `30`으로 복구.
- [x] 빈 배열에서 회원 목록 (0명) 및 '등록된 회원이 없습니다.' 확인 후 3명으로 복구.
- [x] `npx tsc --noEmit` 통과(사용자 보고).
- [x] `npx eslint app/page.tsx components/MemberCard.tsx components/MemberList.tsx types/member.ts` 통과(사용자 보고).
- [x] `npm run build` 통과(사용자 보고).
- [x] Phase 02 Backend 및 PostgreSQL 변경 없이 프론트엔드 실습 완료.

> 실습자는 Git 푸시 완료를 보고했으나, 이 기록 작성 직전 GitHub `main`에는 위 2강 소스 4개가 확인되지 않았습니다. 소스 코드의 원격 반영 여부는 별도로 확인이 필요합니다.

### 다음 강의

3강에서는 회원 검색창과 입력 Form을 추가하여 Event·State에 따라 화면이 바뀌는 흐름을 실습합니다. 실제 API 조회는 4강에서 진행합니다.

## 실행 환경

Next.js 실행에는 Node.js와 npm이 필요합니다. `practice/phase03/.venv`는 별도 Python 실습용이며 Next.js 실행과는 관계가 없습니다.

확인한 버전: Node.js 24.20.0, npm 11.19.0, Next.js 16.4.6. Next.js의 Node 조건(`>=20.9.0`)을 만족합니다.

## 실행

PowerShell에서 프로젝트 폴더로 이동해 개발 서버를 실행합니다.

```powershell
cd C:\dev\fullstack-web-course\practice\phase03\member-next-app
npm run dev
```

브라우저에서 <http://localhost:3000>을 엽니다.

## 검사

같은 프로젝트 폴더에서 실행합니다.

```powershell
npx tsc --noEmit
npm run lint
npm run build
```

## `next` 명령 오류 복구 기록 (2026-11-10)

프로젝트와 `node_modules/.bin/next.cmd`는 있었지만, Next.js 시작에 필요한 `@swc/helpers`가 `node_modules`에서 빠져 있었습니다. 프로젝트를 다시 만들지 않고 기존 lock 파일을 사용해 `npm install --prefer-offline`로 누락된 의존성을 복구했습니다. ESLint deprecation 안내는 시작 실패 원인이 아니었습니다.

검증 결과: `npm run dev` 기동 및 첫 화면 확인, `npx tsc --noEmit`, `npm run lint`, `npm run build` 모두 통과했습니다. 설치 시 moderate 보안 감사 경고 7건이 표시됐으며, 의존성 변경을 막기 위해 자동 `npm audit fix`는 실행하지 않았습니다.

Python 3.12.10 가상환경은 `practice/phase03/.venv`에 준비했습니다. `.venv`, `node_modules`, `.next`, TypeScript 빌드 정보는 Git에 올리지 않습니다.
