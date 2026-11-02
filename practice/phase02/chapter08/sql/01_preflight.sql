-- 8강: 기존 PostgreSQL 데이터와 무결성 조건 점검 (읽기 전용)
-- DBeaver에서 postgres DB의 public schema를 선택하고 실행하세요.

SELECT current_database() AS database_name, current_schema() AS active_schema;

SELECT table_schema, table_name
FROM information_schema.tables
WHERE table_schema = 'public' AND table_name IN ('members', 'courses')
ORDER BY table_name;

SELECT table_name, column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_schema = 'public' AND table_name IN ('members', 'courses')
ORDER BY table_name, ordinal_position;

SELECT indexname, indexdef
FROM pg_indexes
WHERE schemaname = 'public' AND tablename IN ('members', 'courses')
ORDER BY tablename, indexname;

-- 중복 이메일 / 강좌 조합 확인: 결과가 있으면 먼저 중복 해소 필요
SELECT email, COUNT(*) AS duplicate_count
FROM public.members
GROUP BY email
HAVING COUNT(*) > 1;

-- courses가 존재할 때만 실행
-- SELECT title, instructor, COUNT(*) AS duplicate_count
-- FROM public.courses
-- GROUP BY title, instructor
-- HAVING COUNT(*) > 1;

-- UNIQUE 인덱스가 없는 경우에만 기존 데이터 확인 후 수동으로 주석 해제:
-- CREATE UNIQUE INDEX IF NOT EXISTS members_email_unique_idx
--     ON public.members (email);
-- CREATE UNIQUE INDEX IF NOT EXISTS courses_title_instructor_unique_idx
--     ON public.courses (title, instructor);

-- ※ 인덱스 변경은 트랜잭션/다른 실습 코드에도 영향을 줄 수 있습니다.
