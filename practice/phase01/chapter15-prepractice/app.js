// Book Explorer — Chapter 15 사전 통합 실습
// HTML: 구조 / CSS: 디자인 / JavaScript: Event, API, 데이터, DOM

// 1. API 주소 및 현재 검색 결과
const SEARCH_API_URL = "https://openlibrary.org/search.json";
const POST_API_URL = "https://jsonplaceholder.typicode.com/posts";
let books = [];

// 2. HTML 요소 연결 (강의자료에 지정된 ID 유지)
const searchForm = document.querySelector("#search-form");
const searchInput = document.querySelector("#search-input");
const statusMessage = document.querySelector("#status-message");
const bookList = document.querySelector("#book-list");
const bookDetail = document.querySelector("#book-detail");
const bookForm = document.querySelector("#book-form");
const formMessage = document.querySelector("#form-message");

const searchButton = searchForm.querySelector('button[type="submit"]');
const registerButton = bookForm.querySelector('button[type="submit"]');

// 3. GET 요청: 검색어로 도서 검색 후 JSON의 docs 배열 반환
async function searchBooks(keyword) {
  const url = `${SEARCH_API_URL}?q=${encodeURIComponent(keyword)}&limit=10&fields=key,title,author_name,first_publish_year`;
  const response = await fetch(url);

  if (!response.ok) {
    throw new Error(`도서 검색 HTTP 오류: ${response.status}`);
  }

  const data = await response.json();
  if (!Array.isArray(data.docs)) {
    throw new Error("검색 응답에 docs 배열이 없습니다.");
  }

  return data.docs;
}

// 4. 화면 상태 관리: Loading / Empty / Error
function resetBookDisplay() {
  bookList.replaceChildren();
  bookDetail.textContent = "도서를 선택하세요.";
}

function renderLoading() {
  resetBookDisplay();
  statusMessage.dataset.state = "loading";
  statusMessage.textContent = "도서를 검색하는 중입니다...";
}

function renderError(message) {
  resetBookDisplay();
  statusMessage.dataset.state = "error";
  statusMessage.textContent = message;
}

function renderEmpty() {
  resetBookDisplay();
  statusMessage.dataset.state = "empty";
  statusMessage.textContent = "검색 결과가 없습니다.";
}

// 값이 누락된 Open Library 필드 처리
function getAuthors(book) {
  return Array.isArray(book.author_name) && book.author_name.length > 0
    ? book.author_name.join(", ")
    : "저자 정보 없음";
}

function getYear(book) {
  return book.first_publish_year ?? "-";
}

// 5. 목록 렌더링: 외부 API 데이터는 innerHTML 대신 textContent
function renderBooks() {
  bookList.replaceChildren();

  if (books.length === 0) {
    renderEmpty();
    return;
  }

  statusMessage.dataset.state = "success";
  statusMessage.textContent = `검색 결과 ${books.length}권`;

  books.forEach(book => {
    const item = document.createElement("li");
    const button = document.createElement("button");
    const title = document.createElement("strong");
    const summary = document.createElement("span");

    button.type = "button";
    button.className = "book-item";
    title.textContent = book.title || "제목 없음";
    summary.textContent = `저자: ${getAuthors(book)} / 최초 출판연도: ${getYear(book)}`;

    button.append(title, summary);
    button.addEventListener("click", () => renderBookDetail(book));
    item.append(button);
    bookList.append(item);
  });
}

// 6. 도서 상세 렌더링
function renderBookDetail(book) {
  const details = [
    ["제목", book.title || "-"],
    ["저자", getAuthors(book)],
    ["최초 출판연도", getYear(book)],
    ["Open Library key", book.key || "-"]
  ];

  const list = document.createElement("dl");
  list.className = "book-detail-list";

  details.forEach(([label, value]) => {
    const term = document.createElement("dt");
    const description = document.createElement("dd");
    term.textContent = label;
    description.textContent = String(value);
    list.append(term, description);
  });

  bookDetail.replaceChildren(list);
}

// 7. 검색 Form Event — submit Listener는 하나만!
searchForm.addEventListener("submit", async event => {
  event.preventDefault();
  const keyword = searchInput.value.trim();

  if (!keyword) {
    statusMessage.dataset.state = "empty";
    statusMessage.textContent = "검색어를 입력하세요.";
    return;
  }

  books = [];
  renderLoading();
  searchButton.disabled = true;

  try {
    books = await searchBooks(keyword);
    renderBooks();
  } catch (error) {
    console.error("도서 검색 실패:", error);
    renderError("도서를 불러오지 못했습니다.");
  } finally {
    searchButton.disabled = false;
  }
});

// 8. POST 요청: 테스트 API이므로 실제 DB 영구 저장 X
async function createBookRequest(book) {
  const response = await fetch(POST_API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(book)
  });

  if (!response.ok) {
    throw new Error(`도서 등록 HTTP 오류: ${response.status}`);
  }

  return response.json();
}

// 9. 등록 Form Event — submit Listener는 하나만!
bookForm.addEventListener("submit", async event => {
  event.preventDefault();

  const formData = new FormData(bookForm);
  const title = String(formData.get("title") ?? "").trim();
  const author = String(formData.get("author") ?? "").trim();

  if (!title || !author) {
    formMessage.dataset.state = "error";
    formMessage.textContent = "제목과 저자를 입력하세요.";
    return;
  }

  const bookRequest = { title, author };
  formMessage.dataset.state = "loading";
  formMessage.textContent = "등록 요청 중...";
  registerButton.disabled = true;

  try {
    const result = await createBookRequest(bookRequest);
    console.log("POST Response:", result);
    formMessage.dataset.state = "success";
    formMessage.textContent = "등록 요청이 성공했습니다. (실제 DB 저장 아님)";
    bookForm.reset();
    // JSONPlaceholder는 저장하지 않으므로 books 배열에 추가하지 않습니다.
  } catch (error) {
    console.error("도서 등록 요청 실패:", error);
    formMessage.dataset.state = "error";
    formMessage.textContent = "등록 요청에 실패했습니다.";
  } finally {
    registerButton.disabled = false;
  }
});
