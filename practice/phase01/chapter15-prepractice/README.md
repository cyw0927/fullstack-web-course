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


## 2026-10-22 이어서 — STEP 16~21 점검 및 기록

이번 점검에서는 **기존 index.html / style.css / app.js 코드를 변경하지 않았습니다.** 강의의 GET/POST 흐름을 기존 코드와 대조하고, 가상 DOM 및 가상 HTTP 응답을 제공하여 JavaScript 동작을 점검했습니다. 실제 Live Server, Chrome Network 탭, 외부 서버 응답은 이 테스트로 대체할 수 없습니다.

| 강의 단계 | 수행 내용 | 결과 |
| --- | --- | --- |
| **STEP 16** | POST의 URL, Method, Content-Type, JSON Payload, 성공/실패 처리 점검 | 가상 응답 테스트 통과. **Chrome Network 실측 미완료** |
| **STEP 17** | GET의 `docs: []` 응답 시 Empty 표시·목록 초기화 확인 | 가상 응답 테스트 통과. **브라우저에서의 수동 테스트 미완료** |
| **STEP 18** | GET HTTP 503 응답 시 Error 표시·Console Error 확인 | 가상 응답 테스트 통과. **브라우저에서의 수동 테스트 미완료** |
| **STEP 19** | 검색/상세/등록 전체 데이터 흐름을 코드와 대조 | 확인·아래에 기록 |
| **STEP 20** | API 상수·DOM ID·필수 함수·submit 리스너 구조 점검 | 정적 점검 통과 |
| **STEP 21** | 강의자료 기준 구조·상태·이벤트·API·DOM 코드 리뷰 | 수행·아래에 기록 |

### API 응답/DOM 모의 테스트 결과

외부 서버 접속 없이 **실제 app.js 내용을 가상 DOM 환경에서 실행**하고, `fetch()`의 반환값만 통제해 아래 16개 항목을 검사했습니다.

- [x] 검색 submit 리스너 1개, 등록 submit 리스너 1개
- [x] 검색 submit에서 `preventDefault()` 호출
- [x] GET 주소의 검색어, `limit=10`, `fields` 구성
- [x] GET 성공 시 도서 2권 목록 렌더링
- [x] 누락된 저자·출판연도 대체 문구
- [x] 도서 버튼 클릭 시 상세 렌더링
- [x] 결과 0권에서 Empty 상태 표시
- [x] GET 503에서 Error 상태 표시
- [x] GET 실패를 `console.error()`로 기록
- [x] 등록 submit에서 `preventDefault()` 호출
- [x] POST URL 및 Method
- [x] `Content-Type: application/json` 및 trim된 JSON Payload
- [x] POST 201에서 성공 메시지 및 Form 초기화
- [x] POST 성공 시 `books` 배열에 가짜 저장하지 않음
- [x] POST 503에서 오류 메시지 및 `console.error()`
- [x] 요청 완료 후 disabled 버튼 상태 복구

**결과: 16 / 16 통과.** 실패를 의도적으로 만들어 낸 GET/POST Error 테스트에서 Console Error가 발생한 것은 예상한 동작이며 실제 브라우저에 오류가 없음을 뜻하지 않습니다.

### STEP 16 — Chrome Network에서 실제 POST 증거 확인 (미완료)

1. Live Server에서 `index.html` 열기 → F12 → **Network** 선택.
2. 도서 등록 폼에 `Clean Code`와 `Robert C. Martin` 입력 → **등록 요청** 클릭.
3. `posts` 요청을 선택해 **Request Method = POST**인지 확인.
4. Payload에서 `{"title":"Clean Code","author":"Robert C. Martin"}`인지 확인.
5. Status Code와 Response 기록. JSONPlaceholder는 정상 상황에서 보통 **201 Created**를 응답하지만, 실제 값은 Network에서 확인하기 전까지 기록하지 않음.
6. 화면의 성공/실패 메시지와 Console의 `POST Response`를 확인.

> JSONPlaceholder의 POST 성공은 등록 흐름 학습용 모의 응답이며 실제 도서 DB 저장이 아닙니다.

### STEP 17 — Empty 상태 브라우저 테스트 (미완료)

강의자료대로 `app.js` 맨 아래에 다음 두 줄을 **잠깐 추가**하고 저장해 화면이 `검색 결과가 없습니다.`로 바뀌는지 확인합니다.

```javascript
books = [];
renderBooks();
```

**확인 후 위 두 줄을 반드시 제거하여 원상 복구합니다.** 자동화된 모의 테스트에서는 `docs: []` 결과로 Empty 상태를 확인했습니다.

### STEP 18 — Error 상태 브라우저 테스트 (미완료)

`app.js`의 검색 API 주소를 **임시로만** 다음과 같이 바꿉니다.

```javascript
const SEARCH_API_URL = "https://openlibrary.org/invalid-search.json";
```

검색을 실행해 화면의 `도서를 불러오지 못했습니다.`, Console Error, Network의 실패 상태 코드를 확인합니다. **검증 직후 원래 주소 `https://openlibrary.org/search.json`으로 되돌려야 합니다.** 자동화된 모의 테스트에서는 HTTP 503을 주입해 Error 상태를 확인했습니다.

### STEP 19 — 전체 데이터 흐름 설명

**검색:** 검색어 입력 → `submit` Event → `preventDefault()` → `keyword` → `renderLoading()` → `searchBooks()` → GET → Open Library → JSON 응답 → `data.docs` → `books` 배열 → `renderBooks()` → 도서 목록 DOM.

**상세:** 도서 목록의 `button` 클릭 → click Event → 해당 `book` 객체 → `renderBookDetail(book)` → 도서 상세 DOM.

**등록:** 제목·저자 입력 → `submit` Event → `preventDefault()` → `FormData` → `{title,author}` 객체 → `JSON.stringify()` → POST → JSONPlaceholder → Response → `form-message` 피드백. 실제 DB 저장은 수행하지 않음.

### STEP 20 — 최종 구조 Checkpoint

- API 상태: `SEARCH_API_URL`, `POST_API_URL`, `books` 확인
- DOM: `searchForm`, `searchInput`, `statusMessage`, `bookList`, `bookDetail`, `bookForm`, `formMessage` 확인
- API: `searchBooks(keyword)`, `createBookRequest(book)` 확인
- Rendering: `renderLoading()`, `renderError(message)`, `renderEmpty()`, `renderBooks()`, `renderBookDetail(book)` 확인
- Event: 검색 Form·등록 Form의 submit Listener 각각 하나, 도서 버튼 click Listener 확인

### STEP 21 — 코드 리뷰 (강의 기준)

| 검토 항목 | 결과 |
| --- | --- |
| 1. 요구사항 누락 | 코드상 요구사항 대부분 반영. **실제 Network 검증 미완료** |
| 2. Event/Form | 각 submit 리스너 1개, `preventDefault()`, trim 및 `FormData` 적용 |
| 3. GET | URL/필드/응답 상태/예외 처리 반영. 외부 호출 성공 여부는 미확인 |
| 4. POST | JSON 헤더·Payload·상태 확인·성공/실패 메시지 반영. 영구 저장으로 오인하지 않음 |
| 5. JSON | `response.json()`, `Array.isArray(data.docs)`, `JSON.stringify(book)` 적용 |
| 6. DOM | 검색 목록과 상세에 `createElement()`·`textContent` 사용 |
| 7. Loading / Empty / Error | 모의 응답 기준 동작 확인. 브라우저 상태 확인 필요 |
| 8. Network | GET 및 POST 요청 각각 URL/Method/Status/Response(/Payload) 실측 필요 |
| 9. Console | 의도한 실패 테스트에서만 `console.error()` 확인. 실제 콘솔은 추후 확인 |
| 10. 수정 우선순위 | ① 실제 브라우저 GET/POST Network 검증 → ② Empty/Error 수동 시연 → ③ 확인 결과 기록 |

추가 프레임워크나 Backend는 필요하지 않으며, 이 단계에서 원본 코드를 전면 재작성할 근거도 발견되지 않았습니다. 이 기록은 **가상 테스트 합격과 실제 브라우저 실행 성공을 동일하게 취급하지 않습니다.**
