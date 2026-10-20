# Chapter 07 학습 기록 — 반응형 웹

수업: **7강. 반응형 웹 — viewport, media query, 모바일 대응**

- [회원관리 반응형 실습](index.html) / [CSS](style.css)
- [Responsive Course Dashboard 제출 과제](dashboard.html) / [CSS](dashboard.css)

## 내가 정한 Breakpoint

| 화면 너비 | 회원 카드 / 강의 카드 | Header | 검색 도구 |
| --- | --- | --- | --- |
| 767px 이하 (Mobile) | **1열** | 세로 배치 | 세로 배치 |
| 768px ~ 1023px (Tablet) | **2열** | 가로 배치 | 가로 배치 |
| 1024px 이상 (Desktop) | **3열** | 가로 배치 | 가로 배치 |

Mobile First 방식이므로 기본 CSS를 모바일로 작성하고 `@media (min-width: 768px)`, `@media (min-width: 1024px)`에서 확장했다.

## 이 Breakpoint를 선택한 이유

강의에서 제시한 768px(태블릿 경계), 1024px(데스크톱 경계)을 기준으로 먼저 구현했다. 모든 화면에 항상 맞는 절대적인 수치가 아니라, 실제 콘텐츠가 답답해지는 폭을 DevTools에서 확인해 필요하면 조정할 수 있다.

## 모바일에서 변경한 레이아웃

- HTML의 `<meta name="viewport" content="width=device-width, initial-scale=1.0">`를 확인했다.
- `.page-container`에 `width: 90%; max-width: 1200px; margin: 0 auto;`를 적용했다.
- 회원 카드와 강의 카드의 기본 `grid-template-columns: 1fr`로 정해 좁은 화면의 가로 넘침을 줄였다.
- 헤더를 세로 정렬하고, 검색창과 버튼도 세로 배치했다.
- `box-sizing: border-box`, 입력 요소의 `max-width: 100%`, 이미지의 `max-width: 100%; height: auto`를 지정해 화면 폭을 넘지 않게 했다.
- 태블릿에서는 2열, 데스크톱에서는 3열로 그리드와 헤더 정렬을 변경했다.

## LLM에게 질문한 내용

**질문:** “Mobile First 방식에서 `min-width` Media Query로 1열 → 2열 → 3열을 적용하는 이유는 무엇인가요?”

**답변 요약:** 좁은 화면을 기본으로 구성하면 1열 배치를 따로 덮어쓰지 않아도 된다. `min-width`는 화면 폭이 지정한 값 이상일 때만 추가 규칙을 적용하므로 큰 화면으로 갈수록 2열·3열을 확장하기 좋다.

## 내가 직접 확인하고 수정한 부분

- 기존 6강 예제의 Flexbox·Grid 구조를 가져오되 7강은 새로운 `chapter07` 폴더에서 작성했다.
- 모바일에서 `flex-direction: column`, `grid-template-columns: 1fr`을 기본으로 설정했다.
- `min-width: 768px`, `min-width: 1024px`을 분리해 카드 개수를 조절하도록 수정했다.
- 강의 카드 여섯 개에 각각 강의명과 진행 상태를 표시했다.
- **아직 직접 브라우저 DevTools의 Device Toolbar에서 확인한 것은 아니다.** 아래 화면 검증은 로컬에서 진행해야 한다.

## 검증 체크리스트

- [x] viewport 메타태그 확인
- [x] 반응형 `width`, `max-width`, Grid, Flexbox, `@media`, `min-width` 작성
- [x] 대시보드 강의 카드 최소 6개 작성
- [x] 카드별 강의명·진행 상태 추가
- [ ] 375px 화면: 1열 카드, 세로 Header, 가로 스크롤 없음
- [ ] 768px 화면: 2열 카드
- [ ] 1024px 이상 화면: 3열 카드
- [ ] DevTools Elements에서 Media Query 적용 확인
- [ ] 실제 로컬 Live Server 실행 결과 확인

## 직접 실행하는 방법

VS Code에서 `practice/phase01/chapter07/index.html`과 `dashboard.html`을 각각 Live Server로 연다. Chrome에서 `F12` → Device Toolbar (Ctrl+Shift+M)로 375px, 768px, 1024px를 차례로 시험한다.

검색, 폼 등록, 카드 버튼은 **정적 UI**이다. Chapter 08부터 JavaScript 기능 학습을 진행한다.

## 제출 파일

[Chapter 07 dashboard.html](https://github.com/cyw0927/fullstack-web-course/blob/main/practice/phase01/chapter07/dashboard.html)
