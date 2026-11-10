# Phase 03 — Next.js / React / TypeScript

Phase 03에는 프론트엔드 실습 파일을 저장합니다. TypeScript, React, Next.js를 배우고 Phase 02에서 만든 FastAPI API를 화면과 연결하는 것이 목표입니다.

- 학습 예정: TypeScript, React, Next.js
- 목표: Phase 02 FastAPI API를 재사용해 프론트엔드 화면 구성
- 이전 과정: [Phase 01](../phase01/) · [Phase 02](../phase02/)

## 1강: 개발환경 복구와 첫 회원관리 화면

Next.js App Router와 TypeScript로 첫 화면을 구성합니다. 1강에서는 API나 DB를 연결하지 않습니다. 2~8강에서도 `member-next-app` 프로젝트를 계속 사용합니다.

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
