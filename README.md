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

## Chapter 06 — Flexbox와 Grid

6강 자료를 기준으로 독립 실행 가능한 실습과 과제를 추가했습니다. **4·5강은 현재 저장소에 없는 상태**라 임의로 작성하지 않았습니다.

- [6강 회원관리 레이아웃 실습](practice/phase01/chapter06/index.html)
- [6강 대시보드 과제 (6개 카드)](practice/phase01/chapter06/dashboard.html)
- [6강 학습 기록과 검증 항목](practice/phase01/chapter06/README.md)

실행: `practice/phase01/chapter06/index.html` 또는 `dashboard.html`을 Live Server로 엽니다.
검색·등록·상세 버튼은 정적 배치 실습용 UI이며 DB/이벤트는 연결되지 않았습니다.

## Chapter 07 — 반응형 웹

7강 Mobile First 실습 및 독립 대시보드 과제를 추가했습니다.

- [7강 반응형 회원관리 실습](practice/phase01/chapter07/index.html)
- [7강 Responsive Course Dashboard (6개 강의 카드)](practice/phase01/chapter07/dashboard.html)
- [7강 README 및 화면 크기별 검증 방법](practice/phase01/chapter07/README.md)

기본 1열, 768px 이상 2열, 1024px 이상 3열로 바뀝니다. Chrome DevTools Device Toolbar에서 375/768/1024px를 직접 시험하세요.

**로컬에서 별도 작성 중인 6강 하위 폴더** (`CSSGrid/`, `flexbox/`, `member/`)의 미추적 파일은 이번 커밋에서 건드리지 않았습니다.

## Chapter 08 — JavaScript 기초

강의 8강의 **변수, 자료형, 연산자, 조건문, 반복문**을 회원관리 Console 예제로 학습합니다. 이 장에서는 DOM 이벤트나 실제 화면 업데이트를 구현하지 않습니다.

- [8강 기본 실습](practice/phase01/chapter08/index.html) · [app.js](practice/phase01/chapter08/app.js)
- [8강 독립 과제 실행 페이지](practice/phase01/chapter08/assignment.html)
- [8강 제출 파일 assignment.js](practice/phase01/chapter08/assignment.js)
- [8강 학습 기록](practice/phase01/chapter08/README.md)

Live Server에서 각 HTML 파일을 열고 **F12 → Console** 탭을 확인하세요. 다른 강의 폴더는 수정하지 않았습니다.


## Chapter 15 — 통합 실습 및 개인 프로젝트 준비

- [Book Explorer 사전 통합 실습](practice/phase01/chapter15-prepractice/index.html) · [단계별 검증 기록](practice/phase01/chapter15-prepractice/README.md)
- [Member Management 개인 프로젝트 준비판](practice/phase01/chapter15/index.html) · [작업 기록과 명세 유의사항](practice/phase01/chapter15/README.md)

Chapter 15 개인 프로젝트는 현재 제공된 사전 실습 자료에 상세 API 명세가 없어 **회원 GET/POST를 사용하는 임시 학습판**으로 시작했습니다. 공식 본 과제 자료를 받으면 이를 기준으로 보완합니다. 실제 Live Server·Network 검증은 별도로 필요합니다.


### Chapter 15 재현 가능한 테스트 및 제출 체크

- [오프라인 자동 검사 (Node.js, 외부 패키지 불필요)](practice/phase01/chapter15/tests/run-tests.cjs)
- [브라우저 GET/POST 검증과 최종 제출 체크리스트](practice/phase01/chapter15/FINAL_CHECKLIST.md)

두 실습의 DOM·API 로직을 가상 응답으로 실행하는 **53개 검사 통과**를 확인했습니다. 외부 API 실제 통신 및 DevTools 스크린샷은 사용자 브라우저에서 직접 확인해야 합니다. 회원관리 페이지는 강의 본 과제 명세가 제공되지 않은 **학습용 준비판**입니다.
