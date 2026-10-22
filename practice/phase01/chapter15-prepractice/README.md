# Chapter 15 사전 통합 실습 — Book Explorer

> 작업 기록: 2026-10-22  
> 기준: 강의자료 「15강 사전 통합 실습 — AI 바이브 코딩으로 만드는 Book Explorer」  
> 범위: 오늘 정리한 항목 1~5번 구현, 6번 DevTools 현장 검증은 후속 단계

## 파일과 역할

- `index.html`: 검색 Form, 상태 메시지, 검색 결과 목록, 도서 상세, 등록 요청 Form 등 **화면 구조**
- `style.css`: 최대 1000px 중앙 정렬, panel UI, 검색 결과 버튼, 700px 이하 단일 열 등 **디자인**
- `app.js`: **Form Event**, GET/POST API 요청, 데이터 처리, Loading/Success/Empty/Error 및 DOM 갱신

외부 라이브러리, React, 별도 Backend, 실제 DB 저장 기능은 사용하지 않습니다.

## 구현 범위 (1~5)

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
