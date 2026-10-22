# Chapter 15 개인 프로젝트 준비판 — Member Management

> 2026-10-22 작업 기록  
> **강의자료에서 확인된 사항:** Chapter 15에서는 앞선 Book Explorer 사전 실습의 흐름을 회원 관리(Member Management) 개인 프로젝트에 독립 적용한다. GET/POST, List/Detail/Input, 상태 처리, DevTools 검증, GitHub 제출이 학습 흐름이다.  
> **강의자료에 없는 사항:** Chapter 15 본 과제의 상세 명세, 공식 회원 API, 정확한 폴더명, 요구 필드, 제출 규칙. 아래 구현은 본 과제 명세가 제공되기 전까지 사용하는 **임시 학습용 예시**다.

## 사용 방법

로컬 `C:\dev\fullstack-web-course\practice\phase01\chapter15\index.html`을 VS Code Live Server로 연다.

- 조회: 검색어를 비우고 **회원 조회**를 누르면 GET /users로 전체 회원을 요청한다.
- 검색: 이름·사용자명·이메일을 입력하고 조회를 누르면 GET으로 받은 회원 데이터에서 `filter()`로 조건을 적용한다.
- 상세: 목록의 회원을 클릭하면 ID, 이름, 사용자명, 이메일, 전화번호, 도시, 회사를 확인한다.
- 등록: 이름, 사용자명, 이메일을 채워 제출하면 POST /users 요청을 보내고 성공/실패 메시지를 표시한다. **이 API 응답은 영구 저장을 보장하지 않는다.**
- 상태: Loading / Success / Empty / Error.

## 파일별 역할

| 파일 | 역할 |
| --- | --- |
| `index.html` | 시멘틱 HTML, 검색·목록·상세·등록 Form 구조 |
| `style.css` | 1000px 중앙 정렬, 데스크톱 2열/모바일 1열 UI |
| `app.js` | Form Event, async/await, GET/POST, 배열 필터, DOM 렌더링, 상태 및 오류 처리 |

React·Backend·데이터베이스·외부 라이브러리는 사용하지 않는다. 외부 API 데이터는 `innerHTML` 대신 `textContent`로 화면에 표시한다.

## API (공식 과제 지정이 아닌 임시 선택)

- `GET https://api.jsonplaceholder.dev/users`
- `POST https://api.jsonplaceholder.dev/users`

이 엔드포인트는 학습용 JSONPlaceholder API 문서에 회원 조회와 생성 요청으로 안내되어 있다.
공식 자료: https://jsonplaceholder.dev/api/users

서버 조회 결과를 클라이언트에서 검색하며, 등록에 성공해도 조회 목록에 새 회원을 임의 추가하지 않는다. 기존 Chapter 09 실습의 `age`와 `isActive`는 이 임시 API 기본 필드에 없으므로 만들어 넣지 않는다.

## 구현 흐름

조회: 검색어 입력 → submit Event → `preventDefault()` → `fetchUsers()` → GET → JSON 회원 배열 → `filterUsers()` → `renderUsers()` → 회원 클릭 → `renderMemberDetail()`

등록: Form 입력 → submit Event → `FormData` → JS Object → `JSON.stringify()` → POST → Response → `form-message`

## 구현 체크

- [x] 회원 조회·검색 Form과 DOM 연결
- [x] GET 요청, JSON Array 확인, 실패 처리
- [x] 검색 결과 List, 선택 항목 Detail
- [x] 회원 등록 Form과 JSON POST 요청
- [x] Loading / Empty / Error / Success 피드백
- [x] 검색 submit/등록 submit 이벤트 각각 1개
- [x] 모바일 700px 이하 1열 CSS
- [ ] Live Server에서 실제 동작 확인
- [ ] Network에서 GET URL / Method / Status / Response 확인
- [ ] Network에서 POST Method / Payload / Status / Response 확인
- [ ] Empty 및 Error 화면 직접 확인
- [ ] 강사의 **Chapter 15 본 과제 상세 지침** 확보 후 요구사항 최종 대조

## DevTools 확인 팁

1. F12 → Network에서 검색 실행: `users` GET 응답의 배열 내용 확인.
2. 회원 목록 클릭: 오른쪽 상세 카드의 변화 확인.
3. 회원 등록 요청 실행: `users` POST Payload가 `name`, `username`, `email`인지 확인.
4. 실패 테스트는 API 주소를 임시로 잘못 바꿔 확인하고 원래 주소로 복구한다.
5. Console에 의도하지 않은 오류가 없는지 확인한다.

**현재 작업 결과는 GitHub 코드 구현이며 실제 브라우저/외부 API 호출의 성공을 의미하지 않는다.** 강의 본 과제의 정확한 지침이 들어오면 이 준비판의 명세 차이를 먼저 확인한다.


## 2026-10-22 자동 로직 테스트

GitHub 반영 전, 실제 `app.js`를 가상 DOM 객체 및 가상 `fetch()` 응답으로 실행해 검사했습니다. **18개 항목 중 18개 통과.** 이는 정적 파일의 브라우저 렌더링이나 실제 서버 통신이 성공했음을 입증하지 않습니다.

- [x] 검색 / 등록 submit 리스너 각 1개
- [x] 회원 GET URL 및 2명 목록 출력
- [x] GET 성공 결과 메시지
- [x] 회원 클릭 시 도시 및 회사 등 상세 표시
- [x] 이름 / 사용자명 / 이메일 필터 (대소문자 무시)
- [x] 검색 결과 0명 → Empty
- [x] GET 실패(HTTP 503) → Error + Console Error
- [x] POST URL 및 Method
- [x] POST JSON 요청 본문의 입력 공백 제거
- [x] POST 성공 → Success 및 Form 초기화
- [x] POST 성공을 실제 회원 목록에 임의로 저장하지 않음
- [x] POST 실패(HTTP 503) → Error + Console Error
- [x] 요청 완료 후 버튼 disabled 복구
- [x] 외부 문자열을 `innerHTML`로 삽입하지 않음

**추가 현장 검증:** Live Server 실행, 실제 GET/POST Network의 URL·Method·Status·Response/Payload, 콘솔 오류 유무. 본 과제 공식 명세를 확보하면 API 및 필드가 맞는지 재확인합니다.
