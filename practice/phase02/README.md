# Phase 02 — Backend 학습 안내

이 디렉터리는 2차 FastAPI·PostgreSQL 실습을 순서대로 정리한 곳입니다. 프론트엔드 1차 과정은 `../phase01/`에 남겨 두었습니다.

## 강의별 기록

| 실제 진행 순서 | 주제 | 기록 |
| --- | --- | --- |
| 1강 | 첫 FastAPI 서버와 GET 목록 API | [Chapter 01](chapter01/README.md) |
| 2강 | Path / Query Parameter | [Chapter 02](chapter02/README.md) |
| 3강 | Request Body와 Pydantic | [Chapter 03](chapter03/README.md) |
| 4강 | Response Model과 Status Code | [Chapter 04](chapter04/README.md) |
| 5강 | PostgreSQL 연결과 SQL 직접 실행 | [Chapter 05](chapter05/README.md) |
| 6강 | FastAPI·PostgreSQL 통합과 POST 추가 과제 | [Chapter 06](chapter06/README.md) |
| **7강** | **Backend Overview — 전체 Fullstack 인프라와 FastAPI의 역할** | **[Chapter 07](chapter07/README.md)** |

## 7강 자료 안내

실제 수업 순서상 7강은 **Backend Overview**입니다. 1·2·3차 Fullstack 과정의 연결, FastAPI/Uvicorn/Pydantic/SQLAlchemy/PostgreSQL 역할, API Contract 및 15강 학습 로드맵을 설명하는 개념 자료입니다.

**주의:** 원문 Overview에 수록된 별도 로드맵 표는 '07 POST + INSERT/Transaction'을 기재하고 있습니다. 원문 내용과 사용자가 제공한 **실제 7번째 자료**의 분류가 서로 다르므로, 학습자료의 원문 로드맵은 [7강 README](chapter07/README.md)에 그대로 보존하고 실제 진행 순서만 위 표에 정정했습니다.

## 실습 원칙

- Python 가상환경은 프로젝트 최상위 `.venv`를 사용합니다.
- PostgreSQL 비밀번호는 `.env`에만 두고, `.gitignore`로 제외하며 `.env.example`에는 예시 값만 기재합니다.
- Swagger 응답 확인뿐 아니라 실제 SQL 결과와 비교해 API Contract의 충족 여부를 검증합니다.
- 사용자가 직접 실행하지 않은 테스트는 완료 처리하지 않으며, 코드 수정·커밋 전 기존 작업을 확인합니다.

출처: 아토믹데브의 Backend 강의 원문 (사용자가 제공한 자료).
