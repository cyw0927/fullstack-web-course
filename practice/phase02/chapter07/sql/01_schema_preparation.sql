-- Chapter 07: DBeaver에서 DB 구조를 확인한 뒤 필요한 문장만 실행하세요.
-- 현재 학습 DB: postgres / public. 이 파일은 Python 실행 시 자동 적용되지 않습니다.

-- 1) 기존 회원 테이블 확인
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_schema = 'public' AND table_name = 'members'
ORDER BY ordinal_position;

-- 2) 기존 중복 이메일 확인: 결과가 있다면 먼저 처리 방침 결정
SELECT email, COUNT(*) AS duplicates
FROM public.members
GROUP BY email
HAVING COUNT(*) > 1;

-- 3) 기존 이메일 UNIQUE 인덱스/제약조건 확인
SELECT indexname, indexdef
FROM pg_indexes
WHERE schemaname = 'public' AND tablename = 'members';

-- 4) 이메일 UNIQUE가 없다면 아래를 한 번 실행 (기존 중복이 있으면 실패)
-- CREATE UNIQUE INDEX IF NOT EXISTS members_email_unique_idx
--     ON public.members (email);

-- 5) 강좌 테이블이 없다면 아래를 한 번 실행.
-- 기존 public.courses가 있다면 컬럼을 먼저 비교해야 합니다.
CREATE TABLE IF NOT EXISTS public.courses (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    instructor VARCHAR(100) NOT NULL,
    capacity INTEGER NOT NULL CHECK (capacity > 0)
);

-- 6) 기존 (title, instructor) 중복 확인
SELECT title, instructor, COUNT(*) AS duplicates
FROM public.courses
GROUP BY title, instructor
HAVING COUNT(*) > 1;

-- 7) 강좌 UNIQUE가 없다면 아래를 한 번 실행 (중복이 있으면 실패)
-- CREATE UNIQUE INDEX IF NOT EXISTS courses_title_instructor_unique_idx
--     ON public.courses (title, instructor);

-- 8) 회원/강좌 데이터 최종 조회
SELECT id, name, email, age FROM public.members ORDER BY id;
SELECT id, title, instructor, capacity FROM public.courses ORDER BY id;
