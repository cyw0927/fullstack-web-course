-- Chapter 09: 삭제 Evidence — DB = postgres, schema = public
-- 주의: 삭제는 되돌리기 어려우므로 기존 학습 회원(1,2,3...)을 지우지 마세요.

-- STEP 1. 실습 전 행 확인
SELECT id, name, email, age
FROM public.members
ORDER BY id;

-- STEP 2. 삭제 전용 테스트 회원을 한 명만 생성합니다.
-- 반드시 DBeaver에서 INSERT를 실행한 뒤 RETURNING의 실제 ID를 적어 두세요.
-- 같은 테스트 이메일이 이미 있다면 변경하여 사용하세요.
-- INSERT INTO public.members (name, email, age)
-- VALUES ('9강 삭제 테스트', 'chapter09-delete-20261103@example.com', 24)
-- RETURNING id, name, email, age;

-- STEP 3. Swagger GET /members/{실제 ID} → 200
-- STEP 4. Swagger DELETE /members/{실제 ID} → 204 + Body 없음

-- STEP 5. 실제 ID를 아래 999999 대신 넣어 실행 → 0 rows 기대
SELECT id, name, email, age
FROM public.members
WHERE id = 999999;

-- STEP 6. Swagger GET /members/{실제 ID} → 404
-- STEP 7. Swagger DELETE /members/{같은 ID} 다시 실행 → 404
