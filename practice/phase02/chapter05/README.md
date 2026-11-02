# Phase 02 / Chapter 05 — PostgreSQL 연결과 DB 접근 구조

**수업:** 5강. PostgreSQL 연결과 DB 접근 구조  
**학습 기간:** 2026-10-30  
**목표:** FastAPI Endpoint를 연결하기 전에 Python/psycopg로 PostgreSQL 접속, 대상 DB/Schema 확인, SQL SELECT, Python Tuple 변환을 검증한다.

## 작업 환경과 실제 확인된 구조

- Windows + VS Code / PowerShell
- Python 가상환경: 저장소 최상위의 .venv 사용
- PostgreSQL: localhost:5432
- 학습용 Database: postgres
- 실제 사용한 Schema: public (강의 예시의 practice와 다름)
- 회원 테이블: public.members
- 실제 컬럼: id, name, email, age (강의의 member_id 대신 id)
- 기존 ai_database_book 데이터베이스와 그 여러 스키마는 이 실습에서 변경하지 않음

**확인 범위:** 사용자가 공유한 DBeaver 화면에서 public.members 테이블과 SELECT 결과가 보였음. 로컬에서 실행한 python main.py의 최종 출력 전체는 이 대화에 제시되지 않았으므로 검증 완료라고 기재하지 않음.

## 환경변수를 사용하는 이유

접속 설정과 암호를 코드에서 분리하기 위해 chapter05/.env에 설정한다. .env는 GitHub에 올리지 않고, 샘플인 .env.example만 저장한다.

    DB_HOST=localhost
    DB_PORT=5432
    DB_NAME=postgres
    DB_USER=postgres
    DB_PASSWORD=본인의_로컬_비밀번호
    DB_SCHEMA=public

프로젝트 루트 .gitignore와 Chapter 폴더 .gitignore가 .env 및 Python 캐시/가상환경을 제외한다.

**보안 확인 명령 (저장소 루트에서):**

    git check-ignore -v practice/phase02/chapter05/.env
    git status --short
    git ls-files practice/phase02/chapter05/.env

마지막 명령은 아무것도 출력하지 않아야 한다. 과거 이미 추적된 경우 .gitignore만으로 삭제되지는 않으며 별도 Git 추적 해제가 필요하다.

## 파일 역할

- db.py: .env 로드, get_connection(), check_connection(), fetch_members() 정의
- main.py: DB와 Schema 및 회원 Tuple 목록을 출력하는 독립 실행 스크립트
- sql/01_members_setup.sql: 선택적 테이블 생성/샘플 INSERT 및 조회 SQL. 이미 실습 테이블이 있으면 그대로 둬도 된다
- .env.example: 비밀번호가 아닌 예시 설정

## DB 연결 흐름

    .env → load_dotenv() → os.getenv() → psycopg.connect()
         → Connection → Cursor → execute(SQL) → fetchone()/fetchall()
         → Python Tuple → 커서/연결 정리

FastAPI는 이 단계에서 실행하지 않는다. with 구문은 연결과 커서를 안전하게 닫는다.

## 실행한 SELECT 및 정상 결과 형식

**대상 확인:**

    SELECT current_database(), current_schema();

예상 Tuple: ('postgres', 'public'). 실제 연결 결과와 반드시 대조할 것.

**회원 목록:**

    SELECT id, name, email
    FROM public.members
    ORDER BY id;

실제 DBeaver에서는 회원 테이블에 Kim, Lee 등의 행이 존재하는 것을 확인했으며, 이후 6강에서 회원 추가 실습을 진행했다. Python에서는 각 행이 (id, name, email) 모양의 Tuple로 반환된다.

**실행 방법:**

    cd C:\dev\fullstack-web-course
    .\.venv\Scripts\Activate.ps1
    python -m pip install "psycopg[binary]" python-dotenv
    cd practice\phase02\chapter05
    python main.py

## 발생했던 오류 및 해결

- 이전에 Uvicorn을 저장소 루트에서 실행해 main 모듈을 찾지 못한 경험: 각 Chapter 폴더로 이동한 후 실행.
- DBeaver에 기존 ai_database_book 스키마와 실습 테이블이 다수 있어 혼란: postgres / public을 실제 대상 DB로 선택.
- DBeaver 탐색기의 Tables 아래 새 members가 보이지 않음: Tables 폴더 새로고침 후 표시됨.
- 강의에서 member_id를 사용하더라도 현재 테이블 PK는 id이므로 실제 SQL은 id 사용.

## AI에게 질문한 내용 / 내가 직접 검증한 부분

- .gitignore를 어디에 만들고 어떻게 제외 여부를 확인하는가?
- .env를 Python에서 어떻게 읽는가? psycopg와 dotenv의 역할은?
- 왜 DB/Schema를 먼저 확인하고 SQL을 직접 실행하는가?
- DBeaver에서 테이블이 왜 보이지 않는가?
- 사용자가 공유한 화면에서 **PostgreSQL / public / members 및 행 조회를 직접 확인**함.
- 연결/SELECT Python 스크립트의 마지막 실행 출력, 오류 유도 후 복구 증거는 아직 별도 확인 필요.

## 체크리스트

- [x] psycopg/python-dotenv 설치 확인 (사용자 터미널 화면)
- [x] DB 연결 설정 파일 생성 및 Git 제외 규칙 작성
- [x] DBeaver에서 postgres / public / members 테이블 조회
- [x] 실행 가능한 연결·조회 코드 및 SQL 기록
- [ ] 로컬 python main.py의 DB/Schema/행 데이터 최종 출력 확인
- [ ] 오류 한 가지를 의도적으로 재현·복구하고 기록
- [ ] Git 작업 디렉터리에서 .env가 실제 무시되는지 다시 검증

**출처:** 아토믹데브, 「5강. PostgreSQL 연결과 DB 접근 구조」 (사용자가 공유한 강의 본문).
