# Chapter 03 학습 기록

## 가장 헷갈렸던 HTML 요소

이번 장에서는 `table`, `form`, `label`, `input`의 역할이 가장 헷갈렸다.

특히 데이터베이스의 Table과 HTML의 `<table>`은 이름은 같지만 역할이 다르다는 점을 구분해야 했다.

- Database Table: 데이터를 저장하는 구조
- HTML Table: 데이터를 화면에 보여주는 구조

또한 `label`의 `for`, `input`의 `id`, `name`이 각각 다른 역할을 가진다는 점도 중요했다.

## LLM에게 질문한 내용

### 질문 1

회원 목록을 여러 개의 `div`가 아니라 `table`로 작성하는 이유는 무엇인가?

### 답변을 통해 이해한 내용

회원 목록은 이름, 이메일, 나이처럼 같은 종류의 항목이 행과 열로 반복되는 데이터이므로 표 구조가 더 적합하다.

`table`을 사용하면 다음 관계가 명확해진다.

- `thead`: 컬럼 제목
- `tbody`: 실제 데이터
- `tr`: 한 행
- `th`: 제목 셀
- `td`: 데이터 셀

### 질문 2

HTML form에서 `id`, `name`, `label`의 차이는 무엇인가?

### 답변을 통해 이해한 내용

- `label`: 사용자에게 입력 항목의 의미를 보여준다.
- `id`: HTML 문서 안에서 요소를 구분하는 식별자이다.
- `name`: 이후 폼 데이터나 API 요청에서 입력 값을 구분하는 이름으로 사용된다.
- `label for` 값과 `input id` 값이 같으면 두 요소가 연결된다.

## 답변을 통해 새롭게 이해한 내용

`form`은 단순히 입력창을 화면에 배치하는 태그가 아니라 여러 입력 값을 하나의 영역으로 묶는 구조이다.

현재 단계에서는 HTML Form까지만 작성하며 실제 데이터 처리는 하지 않는다.

앞으로의 흐름은 다음과 같다.

```text
HTML Form
→ JavaScript
→ HTTP 요청
→ FastAPI
→ Database
```

또한 `input type`에 따라 브라우저의 입력 방식과 기본 검증이 달라질 수 있다는 점을 확인했다.

## LLM이 제안했지만 내가 수정하거나 사용하지 않은 내용

CSS를 추가해서 표와 폼을 보기 좋게 만드는 방법을 사용할 수 있지만 이번 Chapter의 목표는 HTML 구조 자체를 이해하는 것이므로 사용하지 않았다.

JavaScript로 제출 버튼 동작을 구현하는 방법도 가능하지만 아직 JavaScript와 Backend API를 연결하는 단계가 아니므로 제외했다.

## 내 과제의 HTML 구조를 한 문단으로 설명

과제 페이지는 `header`, `main`, `section`, `footer`를 사용한 시멘틱 구조로 작성했다. `header`에는 페이지 제목과 GitHub 링크를 넣었고, `main`에는 과정 소개 이미지, 수강생 정보를 보여주는 표, 수강 신청을 위한 폼을 각각 별도의 `section`으로 구성했다. 표에는 4개의 컬럼과 3개의 데이터 행을 넣었으며, 폼에는 이름, 이메일, 관심 분야 입력 요소와 제출 버튼을 포함했다.

## DevTools에서 확인할 내용

```text
main
├─ section
│  └─ img
├─ section
│  └─ table
└─ section
   └─ form
```

직접 확인할 항목:

- [ ] `table` 내부에 `thead`와 `tbody`가 나뉘어 있는지 확인
- [ ] 한 명의 수강생 정보가 하나의 `tr`에 들어 있는지 확인
- [ ] `label for`와 `input id`가 연결되어 있는지 확인
- [ ] `form` 안에 제출 `button`이 있는지 확인

## 과제 체크리스트

- [x] 페이지 제목 `Frontend Course Registration`
- [x] GitHub 링크 1개 이상
- [x] 의미 있는 이미지와 적절한 `alt`
- [x] 표에 최소 3개 이상의 컬럼
- [x] 표에 최소 3개의 데이터 행
- [x] 신청 폼에 이름 입력
- [x] 신청 폼에 이메일 입력
- [x] 신청 폼에 관심 분야 입력
- [x] 제출 버튼 포함
- [x] 시멘틱 태그 3개 이상 사용
- [x] CSS 사용 안 함
- [x] JavaScript 사용 안 함
- [x] 실제 API 전송 구현 안 함
- [x] DB 저장 구현 안 함
- [ ] 브라우저에서 assignment.html 직접 실행 확인
- [ ] 링크 정상 동작 확인
- [ ] 이미지 표시 확인
- [ ] DevTools Elements에서 구조 확인
- [x] GitHub에 학습 결과 반영
