# Chapter 06 학습 기록 — Flexbox와 Grid

> 강의: **6강. Flexbox와 Grid — 실제 페이지 레이아웃 구성**
>
> 실습 파일: [index.html](index.html), [style.css](style.css)
>
> 과제 파일: [dashboard.html](dashboard.html), [dashboard.css](dashboard.css)

## 학습 목표

- Flexbox의 Main Axis(주축), Cross Axis(교차축) 구분
- `display: flex`, `justify-content`, `align-items`, `gap` 적용
- `display: grid`, `grid-template-columns`, `repeat(3, 1fr)` 이해
- 한 방향 정렬과 2차원 카드 배치를 구분해서 사용

## Flexbox를 사용한 영역과 이유

| 영역 | CSS | 선택 이유 |
| --- | --- | --- |
| 상단 제목 및 메뉴 | `.site-header` / `.dashboard-header` | 왼쪽 제목·오른쪽 메뉴를 한 행에 배치 |
| 네비게이션 | `.main-nav` | 링크들을 가로로 정렬 |
| 검색 도구 | `.toolbar` / `.dashboard-toolbar` | 검색창과 버튼을 나란히 놓고 `flex: 1`로 입력창이 남은 공간 사용 |
| 카드 내부 버튼 | `.card-actions` | 상세·수정 버튼 사이 간격을 `gap`으로 조절 |
| 등록 폼 | `.register-form` | 입력 필드 및 버튼의 나란한 배치 연습 |

`flex-direction: row`일 때 Main Axis는 가로, Cross Axis는 세로다. `column`으로 바꾸면 축 방향도 바뀌므로 `justify-content`가 무조건 가로 정렬을 뜻하지는 않는다.

## Grid를 사용한 영역과 이유

- `.member-grid`: 예시 회원 3명을 카드 3열로 배치한다.
- `.dashboard-grid`: **별도 과제**의 예시 카드 6개를 3열 × 2행으로 배치한다.
- `grid-template-columns: repeat(3, 1fr)`는 사용 가능한 공간을 같은 비율의 3개 열로 나누며 `gap: 20px`로 카드 간격을 준다.
- 카드가 늘어나면 행이 자연스럽게 추가되므로 각 카드의 좌표를 직접 지정할 필요가 없다.

## 가장 이해하기 어려웠던 속성

**`justify-content`와 `align-items`의 관계:** 화면의 가로·세로가 아니라 **주축·교차축**을 기준으로 이해해야 한다.

## LLM에게 질문한 내용

**질문:** “Flexbox의 Main Axis와 Cross Axis는 무엇이 다르고, 왜 `justify-content`를 가로 정렬로만 외우면 안 되나요?”

**요점 정리:** `flex-direction: row`에서는 주축이 가로지만 `column`에서는 주축이 세로다. `justify-content`는 주축, `align-items`는 교차축 정렬을 담당한다.

## LLM 답변을 검증하거나 수정한 내용

- 강의자료의 `flex-direction: row / column` 예시와 대조하여 정렬축 설명을 정리했다.
- 레이아웃 선택 기준을 “Flexbox는 한 방향, Grid는 행과 열”로 확인했다.
- **브라우저 DevTools를 직접 확인한 결과라고 주장하지 않는다.** 아래 항목은 로컬에서 검증할 일이다.

## 실습 방법 및 검증 체크리스트

1. VS Code Live Server로 `index.html`과 `dashboard.html`을 연다.
2. F12 → Elements → `.site-header`, `.toolbar`, `.member-grid`, `.card-actions`를 선택해 Flex/Grid 표시를 확인한다.
3. `dashboard.css`의 `grid-template-columns: repeat(3, 1fr)`를 `repeat(2, 1fr)`, `1fr`로 바꿔 3열→2열→1열 배치를 확인한 후 원래대로 돌린다.
4. 대시보드 6개 카드, 툴바의 입력창/필터/버튼, 카드 내부 버튼을 확인한다.

- [x] Header와 메뉴에 Flexbox CSS 작성
- [x] 검색/필터 영역에 Flexbox CSS 작성
- [x] 카드 목록에 Grid CSS 작성
- [x] 과제 카드 6개 작성
- [x] 카드 내부 버튼에 Flexbox CSS 작성
- [ ] 로컬 브라우저에서 실제 화면 확인
- [ ] DevTools에서 Flex/Grid 표시 확인
- [ ] Grid 3열→2열→1열 비교 실험
- [ ] GitHub Pages에서 실제 렌더링 확인

## 과제 범위와 주의점

- 검색, 등록, 상세/수정 버튼은 **배치 실습용 정적 UI**다. 실제 이벤트 처리는 강의에서 Chapter 11에 연결하도록 안내한다.
- 대시보드 숫자는 **설명용 예시 데이터**이며 API나 데이터베이스와 연결되어 있지 않다.
- Chapter 05 결과물이 저장소에 없어, 기존 파일을 수정하지 않고 Chapter 06에서 독립 실행 가능한 예제를 구성했다.
- 반응형 설계는 다음 Chapter에서 자세히 다루며, 현재는 좁은 화면에서 넘침을 방지하는 최소한의 CSS만 포함한다.

### 제출 링크

[Chapter 06 Dashboard HTML](https://github.com/cyw0927/fullstack-web-course/blob/main/practice/phase01/chapter06/dashboard.html)
