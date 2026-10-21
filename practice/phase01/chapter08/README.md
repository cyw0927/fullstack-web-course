# Chapter 08 학습 기록 — JavaScript 시작

수업: **8강. JavaScript 시작 — 변수, 자료형, 연산자, 조건문, 반복문**

## 이번 장에서 이해한 개념

- **JavaScript:** HTML 구조와 CSS 표현 다음에 데이터 저장, 계산, 조건 판단, 반복 처리를 담당한다.
- **`const` / `let`:** 값을 다시 할당하지 않으면 `const`, 값이 바뀌면 `let`.
- **자료형:** `string`, `number`, `boolean`, `undefined`. `typeof`로 확인한다.
- **연산자:** 산술(`+`, `-`, `*`, `/`), 비교(`>=`, `===`), 논리(`&&`, `||`, `!`).
- **조건문:** `if / else`로 회원의 나이와 활성 상태를 판단한다.
- **반복문:** `for`는 번호(인덱스)까지 필요할 때, `for...of`는 배열의 각 값을 간단히 처리할 때 사용한다.
- **Template Literal:** 백틱과 `${값}`을 이용해 문자열에 변수 값을 넣는다.

## 가장 어려웠던 코드

```javascript
for (let i = 0; i < members.length; i++) {
  console.log(`${i + 1}번 회원: ${members[i]}`);
}
```

배열의 인덱스는 **0부터 시작**하지만 사용자에게 보여주는 순번은 **1부터 시작**하므로 `i + 1`을 출력한다. `i < members.length` 조건이 마지막 회원을 넘어가지 않게 한다.

## LLM에게 질문한 내용

**질문:** “회원 이름 배열을 반복할 때 `for`와 `for...of`는 무엇이 다르고, 언제 선택하나요?”

**코드 구성에 반영한 답변:** `for...of`는 값을 직접 순회하므로 회원 이름을 나열할 때 간단하다. `for`는 `i`로 인덱스에 접근할 수 있어 이름과 나이의 같은 위치를 함께 조회하거나 순번을 출력할 때 편하다.

## LLM 답변에서 내가 직접 검증한 내용

코드 수준으로 다음 조건을 확인했다. **브라우저 Console의 실제 실행 여부는 로컬에서 검증할 항목**으로 남겨둔다.

- `app.js`에 강의의 `memberName='홍길동'`, `age=27`, `active=true` 조건을 반영했다.
- `age >= 20 && active`가 참이면 “이용 가능한 성인 회원” 문구가 출력되도록 했다.
- `for...of`와 `for`를 각각 사용했다.
- 오류 학습용 `console.log(memberEmail)`은 기본 실행을 방해하지 않도록 **주석으로** 두었다. 직접 해제해 오류 종류·파일·줄 번호를 관찰할 수 있다.
- `assignment.js`에는 이름 5개, 나이 5개, 성인/미성년 판단, 전체 인원 출력, Template Literal을 반영했다.

## 조건문과 반복문의 차이를 내 말로 설명

조건문은 “이 사람이 20세 이상인가?”처럼 **한 번의 판단**을 내리는 갈림길이다. 반복문은 여러 회원을 하나씩 꺼내 **같은 판단을 반복**하게 한다. 따라서 과제에서는 반복문 **안에** 조건문을 넣었다.

## 폴더와 실행 방법

```text
practice/phase01/chapter08/
├── index.html       # 기본 실습 — app.js 연결
├── app.js           # 변수/자료형/연산자/조건문/반복문
├── assignment.js    # 제출 대상: 회원 5명 성인·미성년 판정
├── assignment.html  # 추가: assignment.js를 별도로 실행하는 페이지
└── README.md
```

VS Code Live Server에서 `index.html`을 열고 **F12 → Console**로 실습 결과를 확인한다. 과제 결과는 `assignment.html`을 열어 확인하면 된다. 이번 강의는 DOM을 직접 변경하지 않으므로 **브라우저 화면이 거의 바뀌지 않는 것이 정상**이다.

### 과제 Console 예상 결과

```text
1. 홍길동 - 25세 - 성인
2. 김영희 - 19세 - 미성년
3. 이철수 - 21세 - 성인
4. 박민지 - 17세 - 미성년
5. 최준호 - 32세 - 성인
전체 회원 수: 5
```

## 제출 전 확인

- [x] `index.html`에서 `app.js` 연결 코드 작성
- [x] `assignment.js`에 회원 5명, 조건문, 반복문 구현
- [x] Template Literal 및 전체 회원 수 출력 코드 작성
- [ ] 로컬 브라우저 Console에서 `app.js` 결과 직접 확인
- [ ] 로컬 브라우저 Console에서 `assignment.js` 결과 직접 확인
- [ ] 주석을 해제해 ReferenceError를 관찰하고 다시 주석 처리
- [ ] GitHub에서 제출 파일을 직접 열어 확인

**제출 링크:** [assignment.js](https://github.com/cyw0927/fullstack-web-course/blob/main/practice/phase01/chapter08/assignment.js)
