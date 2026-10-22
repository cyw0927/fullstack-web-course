# Chapter 15 사전 통합 실습 — Book Explorer

> 작업 기록: 2026-10-22  
> 기준: 강의자료 「15강 사전 통합 실습 — AI 바이브 코딩으로 만드는 Book Explorer」  
> 범위: 강의자료 STEP 01~15를 기준으로 코드 구현·점검. STEP 12(GET Network 현장 증거)는 사용자 브라우저에서 검증 필요

## 파일과 역할

- `index.html`: 검색 Form, 상태 메시지, 검색 결과 목록, 도서 상세, 등록 요청 Form 등 **화면 구조**
- `style.css`: 최대 1000px 중앙 정렬, panel UI, 검색 결과 버튼, 700px 이하 단일 열 등 **디자인**
- `app.js`: **Form Event**, GET/POST API 요청, 데이터 처리, Loading/Success/Empty/Error 및 DOM 갱신

외부 라이브러리, React, 별도 Backend, 실제 DB 저장 기능은 사용하지 않습니다.

## 주요 구현 범위 (기존 1~5 기능)

1. **GET 도서 검색:** 검색 Form `submit` → `preventDefault()` → `searchBooks(keyword)` → Open Library Search API 요청 → JSON의 `docs` 반환. 검색어는 `encodeURIComponent`로 인코딩하며 최대 10권 조회.
2. **검색 목록:** `renderBooks()`에서 `books` 배열을 순회하고 제목, 저자, 최초 출판연도를 버튼 목록으로 출력. 저자 및 출판연도 누락값을 처리함.
3. **상세 보기:** 검색된 책 버튼 클릭 → `renderBookDetail(book)` → 제목·저자·출판연도·Open Library key 표시.
4. **POST 등록 요청:** 도서 제목·저자 Form `submit` → `FormData` → `{ title, author }` → `createBookRequest()` → JSONPlaceholder 테스트 API로 POST → 성공/실패 메시지. **응답 성공과 영구 저장은 다름**. 검색 결과 목록에 가짜로 추가하지 않음.
5. **UI 상태 처리:** GET의 Loading / Success / Empty / Error, POST의 Loading / Success / Error 상태를 메시지로 표시. 검색 상태가 바뀌면 기존 목록과 상세를 초기화함.

## API

- GET: `https://openlibrary.org/search.json?q=javascript&limit=10&fields=key,title,author_name,first_publish_year`
- POST: `https://jsonplaceholder.typicode.com/posts`

## 구현 흐름

검색: 검색어 → `submit` → GET → HTTP Response → JSON → `data.docs` → `books` → `renderBooks()` → DOM → 상세 클릭

등록: 제목/저자 → `submit` → `FormData` → JavaScript Object → `JSON.stringify()` → POST → HTTP Response → 화면 피드백

검색 Form과 등록 Form의 submit 리스너는 각각 **1개**만 등록했습니다. 외부 API에서 받은 문자열은 `createElement()`와 `textContent`를 사용해 화면에 넣었습니다.

## 검증 기록 및 다음 할 일

**구현 코드 작성 완료:** 위 1~5번.  
**실제 Live Server 실행 / Console / Network / 외부 API 성공 여부:** 아직 현장 검증하지 않았으므로 완료로 표시하지 않음.

1. 로컬 `C:\dev\fullstack-web-course\practice\phase01\chapter15-prepractice\index.html`을 Live Server로 연다.
2. 검색어 `javascript`를 입력한 뒤 F12 → Network에서 **GET**, URL, Status Code, Response의 `docs` 확인. 책 선택 시 상세 갱신 확인.
3. DevTools Network Throttling을 잠시 Slow 3G로 설정해 Loading 메시지가 보이는지 확인하고 원래대로 돌린다.
4. 빈 결과 테스트는 강의 안내대로 `books = []; renderBooks();`를 임시 실행해 확인하고 제거한다.
5. Error는 임시 잘못된 검색 URL로 요청해 실패 표시를 확인한 뒤 원래 URL을 복구한다. 외부 API 429/5xx는 내 코드 오류와 구별한다.
6. 등록 요청 시 `Clean Code` / `Robert C. Martin` 입력 후 F12 → Network에서 **POST**, JSON Payload, Status Code, Response 확인. JSONPlaceholder는 실제 DB에 저장하지 않는다.
7. Console에 예상하지 못한 오류가 없는지 확인한다.

### 이번 강의의 핵심 구별

- `submit` = 브라우저에서 발생한 Event
- `GET` / `POST` = 서버에 보낸 HTTP Method
- `Empty` = 요청 성공 + 결과 0권
- `Error` = 요청이나 데이터 처리 실패
- `POST 성공` ≠ 영구 저장

기존 장별 실습은 수정하지 않고, 강의가 지정한 별도 폴더에 독립 구성했습니다.


## 2026-10-22 추가 점검 — 강의 STEP 01~15

강의자료의 **STEP 번호**는 이 문서 앞쪽의 **주요 구현 기능 1~5번**과 다릅니다. 현재 GitHub의 최종 코드를 STEP별로 대조했습니다. 학습 과정에서 임시로 `fetch()`를 생략했던 단계는 최종 코드에 통합되어 있습니다. 실제 브라우저 실행·Network 증거가 필요한 검증은 구현과 구분했습니다.

| 강의 단계 | 요구사항 및 확인 지점 | 현재 상태 |
| --- | --- | --- |
| STEP 01 | AI 구현 계획: 파일별 역할, 화면, GET/POST 흐름, 함수, 구현 순서, 검증 항목 | 문서화 완료 (아래 설계 및 기존 섹션) |
| STEP 02 | `chapter15-prepractice/`에 HTML/CSS/JS 파일 생성 | 작성 완료 |
| STEP 03 | 검색/목록/상세/등록의 HTML 구조 및 지정된 ID | 작성 완료 |
| STEP 04 | 중앙 1000px, panel, 700px 이하 1열 반응형 CSS | 작성 완료 |
| STEP 05 | `querySelector()`로 7개 DOM 요소 연결, API 상수, `books` 상태 | 작성 완료 |
| STEP 06 | 검색 `submit`, `preventDefault()`, `trim()`, 검색어 Console 출력 | 최종 핸들러에 통합·콘솔 출력 반영 |
| STEP 07 | `searchBooks(keyword)`: GET, 인코딩, HTTP 확인, JSON, `docs` | 작성 완료 |
| STEP 08 | `renderLoading()`, `renderError()`, `renderEmpty()` | 작성 완료 |
| STEP 09 | `renderBooks()`: 결과 수·버튼 생성·저자·연도·안전한 DOM | 작성 완료 |
| STEP 10 | `renderBookDetail(book)`: 제목·저자·연도·key | 작성 완료 |
| STEP 11 | 검색 submit → Loading → GET → 목록/오류 렌더링, 리스너 1개 | 작성 완료 |
| **STEP 12** | **F12 Network에서 GET의 URL·Method·Status·Response 증거 확인** | **미검증: 사용자 브라우저에서 수행 필요** |
| STEP 13 | 등록 submit → FormData → `{title,author}` → Console 출력 | 최종 핸들러에 통합·콘솔 출력 반영 |
| STEP 14 | `createBookRequest(book)`: JSON POST, `response.ok`, 결과 반환 | 작성 완료 |
| STEP 15 | 등록 submit → POST → 성공/실패 안내·Console·Form reset, 리스너 1개 | 작성 완료 |

### STEP 01 — 구현 설계 기록

1. **파일 책임:** `index.html` 화면 구조, `style.css` 디자인, `app.js` 이벤트/API/DOM 처리.
2. **화면 구성:** 검색 Form → 상태 메시지 → 도서 목록과 상세 → 도서 등록 Form → 등록 결과 메시지.
3. **GET 흐름:** 검색어 → Form submit → `searchBooks()` → Open Library → `docs` 배열 → `renderBooks()` → 목록 클릭 시 `renderBookDetail()`.
4. **POST 흐름:** 제목·저자 → Form submit → `FormData` → `createBookRequest()` → JSONPlaceholder → 응답에 따른 메시지. **영구 저장하지 않음.**
5. **함수 목록:** `searchBooks()`, `renderLoading()`, `renderError()`, `renderEmpty()`, `renderBooks()`, `renderBookDetail()`, `createBookRequest()`.
6. **구현 순서:** HTML → CSS → DOM 요소 선택 → 검색 Event → GET → 상태/목록/상세 → 등록 Event → POST.
7. **검증 체크:** Live Server 실행, Network GET/POST 증거, 목록과 상세, Loading/Empty/Error, Console 오류 유무.

### STEP 12 — 직접 확인할 GET Network Evidence

브라우저에서 Live Server로 `index.html` 실행 → F12 → **Network** → 검색어 `javascript` 검색 → `search.json` 요청 선택 후 아래를 확인합니다.

- [ ] Request URL: `https://openlibrary.org/search.json?q=javascript&limit=10&fields=key,title,author_name,first_publish_year`
- [ ] Request Method: **GET**
- [ ] Status Code: 실제 응답값 기록 (정상 응답이라면 2xx, 실패 시 429/5xx 등의 상태를 확인)
- [ ] Response / Preview의 `docs` 배열 확인
- [ ] 검색 목록 표시, 버튼 클릭 후 상세가 나오는지 확인
- [ ] Console에 예상하지 못한 JavaScript 오류가 없는지 확인

**STEP 12 검증은 아직 완료로 체크하지 않습니다.** API가 응답했다는 사실과 사용자의 브라우저 DevTools에서 증거를 직접 확인했다는 사실은 구별합니다.

### STEP 15 — POST 핸들러 흐름 확인

`book-form`의 `submit` 리스너는 1개이며, `event.preventDefault()` → `FormData` → 공백 제거 → `bookRequest` 생성 및 Console 출력 → "등록 요청 중..." → `await createBookRequest(bookRequest)` → 성공 메시지·POST Response Console·Form reset / 실패 메시지·Console Error의 순서입니다. 응답 성공 시에도 검색 결과의 `books` 배열에 새 책을 추가하지 않습니다.

**추후 단계:** STEP 16에서는 POST Network의 Method, Payload, Status, Response를 브라우저에서 직접 검증합니다.
