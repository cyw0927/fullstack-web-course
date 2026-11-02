-- 8강: Swagger PUT/PATCH 응답과 PostgreSQL 상태 비교
-- '123'은 예시이며 Swagger에서 실제 조회한 ID로 바꿔서 실행하세요.
-- UPDATE를 직접 실행하지 않고 검증용 SELECT만 제공합니다.

SELECT id, name, email, age
FROM public.members
WHERE id = 123;

-- PATCH {"age": 31} 성공 후 name/email은 그대로인지 확인
-- 200 Response JSON과 다음 결과의 네 컬럼이 모두 같아야 합니다.
SELECT id, name, email, age
FROM public.members
WHERE id = 123;

-- GET /members/123 역시 같은 결과여야 합니다.

-- 강좌 수정 과제: public.courses가 있을 경우에만 실행
-- SELECT id, title, instructor, capacity
-- FROM public.courses
-- WHERE id = 123;

-- 409/422/400 에러를 요청하기 전후 같은 ID를 조회해
-- 오류가 났을 때 데이터가 바뀌지 않는지도 비교하세요.
