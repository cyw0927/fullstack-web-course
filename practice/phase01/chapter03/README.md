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

- [x] `table` 내부에 `thead`와 `tbody`가 나뉘어 있는지 확인
- [x] 한 명의 수강생 정보가 하나의 `tr`에 들어 있는지 확인
- [x] `label for`와 `input id`가 연결되어 있는지 확인
- [x] `form` 안에 제출 `button`이 있는지 확인

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
- [x] 브라우저에서 assignment.html 직접 실행 확인
- [x] 링크 정상 동작 확인
- [x] 이미지 표시 확인
- [x] DevTools Elements에서 구조 확인
- [x] GitHub에 학습 결과 반영

## 이번 점검에서 수정한 내용

실습의 GitHub 링크를 강사 저장소에서 `cyw0927/fullstack-web-course`로 변경했다. 두 표에는 `caption`과 `th scope="col"`을 추가해 표의 주제와 열 제목을 명확히 했다. 강의에 나온 공개 로드맵 이미지를 그대로 사용하며, 이미지 주소의 정상 응답과 두 페이지의 브라우저 표시를 확인했다.

## 검증 결과

- 두 HTML 문서의 태그 중첩, 제목 계층, 시멘틱 구조를 점검했다.
- 실습 표는 4열·2개 데이터 행, 과제 표는 4열·3개 데이터 행이다.
- `label for`와 `input id`가 일치하며 모든 입력란에 `name`이 있다.
- 브라우저에서 과제의 이름·이메일·관심 분야를 실제 입력해 연결을 확인했다.
- 외부 SVG 이미지는 HTTP 200으로 응답하며 두 페이지에서 표시된다.
- HTML에 CSS, JavaScript, API 또는 DB 연결을 추가하지 않았다.
- 폼 제출은 브라우저의 기본 동작만 수행하며 실제 등록이나 저장을 하지 않는다.

## 제출 전 체크리스트

- [x] assignment.html이 브라우저에서 열린다.
- [x] GitHub 링크의 목적지와 정상 응답을 확인했다.
- [x] 웹 이미지 표시와 적절한 alt를 확인했다.
- [x] table에 최소 3개 컬럼과 3개 데이터 행이 있다.
- [x] form에 이름·이메일·관심 분야·제출 버튼이 있다.
- [x] 시멘틱 태그를 사용했다.
- [x] README.md에 LLM 활용 기록을 작성했다.
- [x] Git commit을 만들었다.
- [x] GitHub에 push했다.
- [x] GitHub에서 과제 파일을 직접 열어 확인했다.

## 제출 URL

https://github.com/cyw0927/fullstack-web-course/blob/main/practice/phase01/chapter03/assignment.html

## 프로필 이미지와 웹 실행 링크

사용자가 제공한 프로필 이미지를 `images/profile.png`로 보관하고 실습과 과제에 추가했다. `alt`에는 인물과 배경의 의미를 설명했다. 과제의 과정 소개에는 강의 로드맵 이미지를 유지했다. 실습은 사용자 예시에 맞춰 Frontend Learning 영역에 프로필 이미지 하나를 표시한다.

- [과제 웹페이지](https://cyw0927.github.io/fullstack-web-course/practice/phase01/chapter03/assignment.html)
- [실습 웹페이지](https://cyw0927.github.io/fullstack-web-course/practice/phase01/chapter03/index.html)

## 실습 화면 구성 수정

사용자가 제공한 예시 화면에 맞춰 실습 index.html을 제목, Course GitHub 링크, Frontend Learning과 128×128 프로필 이미지, 회원 목록, 회원 등록 폼, footer 순서로 정리했다. 별도의 학습자 소개와 표 caption을 제거하고 CSS나 JavaScript 없이 기본 HTML 표시를 유지했다.
