// Chapter 08 — 혼자 해보기: 회원 이용 가능 여부 판별하기
// 수업에서 배운 배열, const, for, if, Template Literal만 사용합니다.

// 1. 회원 이름을 배열에 저장합니다.
const memberNames = ['홍길동', '김영희', '이철수', '박민지', '최준호'];

// 2. 각 회원의 나이를 같은 순서로 배열에 저장합니다.
const memberAges = [25, 19, 21, 17, 32];

// 3. 모든 회원을 반복해서 성인/미성년 여부를 판단합니다.
for (let i = 0; i < memberNames.length; i++) {
  const name = memberNames[i];
  const age = memberAges[i];
  let category;

  if (age >= 20) {
    category = '성인';
  } else {
    category = '미성년';
  }

  // 4. Template Literal로 번호, 이름, 나이, 판정 결과를 출력합니다.
  console.log(`${i + 1}. ${name} - ${age}세 - ${category}`);
}

// 5. 배열의 length로 전체 회원 수를 출력합니다.
console.log(`전체 회원 수: ${memberNames.length}`);
