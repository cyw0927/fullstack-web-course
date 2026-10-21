// Chapter 08 — JavaScript 기초 실습
// 실행: index.html을 Live Server로 열고 F12 → Console을 확인합니다.

// STEP 03. const(재할당하지 않을 값)와 기본 자료형
const memberName = '홍길동';
const age = 27;
const active = true;

console.log(memberName); // 홍길동
console.log(age);        // 27
console.log(active);     // true

// 자료형 확인: String, Number, Boolean
console.log(typeof memberName); // string
console.log(typeof age);        // number
console.log(typeof active);     // boolean

// let: 나중에 값이 바뀔 때 사용
let memberCount = 3;
memberCount = 4;
console.log('현재 회원 수:', memberCount); // 4

// 산술 / 비교 / 논리 연산자
console.log('10 + 3 =', 10 + 3);
console.log('age >= 20:', age >= 20);
console.log('age === 27:', age === 27);
console.log('age >= 20 && active:', age >= 20 && active);

// STEP 04. if / else 조건문
if (age >= 20 && active) {
  console.log(`${memberName}님은 이용 가능한 성인 회원입니다.`);
} else {
  console.log(`${memberName}님은 이용 조건을 확인해야 합니다.`);
}

// STEP 05. for...of: 배열에서 값을 하나씩 꺼내기
const members = ['홍길동', '김영희', '이철수'];
for (const member of members) {
  console.log(`회원: ${member}`);
}

// STEP 06. for: 배열의 인덱스(0부터 시작)를 이용해 번호와 함께 출력
for (let i = 0; i < members.length; i++) {
  console.log(`${i + 1}번 회원: ${members[i]}`);
}

// STEP 07. 오류 관찰은 직접 실습할 때만 아래 주석을 해제하세요.
// console.log(memberEmail); // ReferenceError: memberEmail is not defined
// 오류가 발생하면 종류, 파일, 줄 번호를 먼저 확인합니다.
