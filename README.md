# Fullstack Web Course

프론트엔드 기초부터 백엔드와 풀스택 흐름까지 단계적으로 학습하기 위한 실습 저장소입니다.

## 학습 흐름

1. Frontend Basic
   - Browser / Web Server / API Server / Database의 역할
   - HTML / CSS / JavaScript 기초
   - DOM / Event / Form
   - HTTP / JSON
   - `fetch()`를 이용한 API 통신
2. Backend
   - Python / FastAPI 기반 API 서버
3. Fullstack
   - React / Next.js와 Backend 연결

## 현재 진행

### Phase 01 — Frontend Basic

#### Chapter 01
- [x] 첫 HTML 페이지 작성
- [x] 자기소개 페이지 작성
- [x] 학습 기록 작성
- [ ] Live Server로 로컬 실행 확인
- [ ] DevTools Network 탭에서 HTML GET 요청 확인

#### Chapter 02
- [x] 시멘틱 HTML 실습 페이지 작성
- [x] Member Learning Page 작성
- [x] 과제 `assignment.html` 작성
- [x] LLM 학습 기록 작성
- [ ] DevTools Elements 탭에서 HTML 트리 직접 확인

#### Chapter 03
- [x] Member Management 실습 페이지 작성
- [x] Course Registration Page 과제 작성
- [x] 링크, 웹 이미지, 표, 입력 폼 구현
- [x] LLM 학습 기록 작성
- [x] HTML 구조와 과제 조건 점검
- [x] 브라우저에서 웹 이미지 표시 확인

## 실습 구조

```text
practice/
└─ phase01/
   ├─ chapter01/
   │  ├─ index.html
   │  ├─ profile.html
   │  └─ README.md
   ├─ chapter02/
   │  ├─ index.html
   │  ├─ assignment.html
   │  └─ README.md
   └─ chapter03/
      ├─ index.html
      ├─ assignment.html
      ├─ README.md
      └─ images/
         └─ profile.png
```

## 로컬 실행

권장 로컬 위치:

```text
C:\dev\fullstack-web-course
```

저장소를 받은 뒤 VS Code에서 원하는 Chapter의 `index.html` 또는 `assignment.html`을 열고 Live Server로 실행합니다.

Chapter 01에서는 Network 탭에서 HTML GET 요청을, Chapter 02에서는 Elements 탭에서 다음 시멘틱 계층 구조를 확인합니다.

```text
body
├─ header
├─ main
│  ├─ section
│  └─ section
└─ footer
```

- [Chapter 01 학습 기록](practice/phase01/chapter01/README.md)
- [Chapter 02 학습 기록](practice/phase01/chapter02/README.md)

- [Chapter 03 학습 기록](practice/phase01/chapter03/README.md)
- [Chapter 03 실습](practice/phase01/chapter03/index.html)
- [Chapter 03 과제](practice/phase01/chapter03/assignment.html)

Chapter 03에서는 브라우저에서 로드맵 이미지가 표시되는지, 표의 제목과 데이터 행이 구분되는지, 각 입력란의 `label for`와 `input id`가 연결되는지 확인합니다. CSS, JavaScript, API, DB 연결 없이 HTML만 사용합니다.

## 웹페이지 바로가기

- [Chapter 03 수강 신청 과제](https://cyw0927.github.io/fullstack-web-course/practice/phase01/chapter03/assignment.html)
- [Chapter 03 회원 관리 실습](https://cyw0927.github.io/fullstack-web-course/practice/phase01/chapter03/index.html)

GitHub Pages에서 HTML 페이지를 바로 볼 수 있습니다. 사용자가 제공한 프로필 이미지는 두 페이지의 학습자 프로필 영역에 표시됩니다.
