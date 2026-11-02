-- 아래 쿼리는 Swagger POST /members의 실제 반환 ID/이메일로 수정하여 실행.
-- 예시 이메일은 신규 실습용으로 요청한 값으로 바꿀 것.
SELECT id, name, email, age
FROM public.members
WHERE email = 'replace-me@example.com'
ORDER BY id;

-- 같은 이메일 POST 요청 전후 개수를 비교한다.
SELECT COUNT(*) AS matching_rows
FROM public.members
WHERE email = 'replace-me@example.com';

-- 강좌 POST 과제의 저장 확인
SELECT id, title, instructor, capacity
FROM public.courses
WHERE title = 'FastAPI Basic' AND instructor = 'Kim'
ORDER BY id;
