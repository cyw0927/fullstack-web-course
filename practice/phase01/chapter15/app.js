// Chapter 15 Member Management — 학습용 준비판
// 이 강의자료에서 API URL은 미지정이므로 JSONPlaceholder 호환 회원 API를 임시 사용합니다.
// HTML = 구조, CSS = 디자인, JavaScript = 이벤트 + 데이터 + API + DOM

// 1. API / 상태
const USERS_API_URL = "https://api.jsonplaceholder.dev/users";
let users = [];

// 2. DOM
const searchForm = document.querySelector("#search-form");
const searchInput = document.querySelector("#search-input");
const statusMessage = document.querySelector("#status-message");
const memberList = document.querySelector("#member-list");
const memberDetail = document.querySelector("#member-detail");
const memberForm = document.querySelector("#member-form");
const formMessage = document.querySelector("#form-message");

const searchButton = searchForm.querySelector('button[type="submit"]');
const registerButton = memberForm.querySelector('button[type="submit"]');

// 3. GET 요청
async function fetchUsers() {
  const response = await fetch(USERS_API_URL);
  if (!response.ok) {
    throw new Error(`회원 조회 실패 (HTTP ${response.status})`);
  }

  const data = await response.json();
  if (!Array.isArray(data)) {
    throw new Error("회원 응답이 배열 형태가 아닙니다.");
  }
  return data;
}

// 4. 화면 상태
function resetMemberDisplay() {
  memberList.replaceChildren();
  memberDetail.textContent = "회원을 선택하세요.";
}

function renderLoading() {
  resetMemberDisplay();
  statusMessage.dataset.state = "loading";
  statusMessage.textContent = "회원 정보를 불러오는 중입니다...";
}

function renderEmpty() {
  resetMemberDisplay();
  statusMessage.dataset.state = "empty";
  statusMessage.textContent = "검색 결과가 없습니다.";
}

function renderError(message) {
  resetMemberDisplay();
  statusMessage.dataset.state = "error";
  statusMessage.textContent = message;
}

// 5. 데이터 가공: filter()로 검색
function filterUsers(keyword) {
  const query = keyword.toLowerCase();
  return users.filter(user => {
    const searchable = [user.name, user.username, user.email]
      .map(value => String(value ?? "").toLowerCase());
    return searchable.some(value => value.includes(query));
  });
}

// 6. 상세 보기: 외부 데이터는 textContent로 안전하게 출력
function renderMemberDetail(user) {
  const company = typeof user.company === "object" ? user.company?.name : user.company;
  const data = [
    ["ID", user.id ?? "-"],
    ["이름", user.name || "-"],
    ["사용자명", user.username || "-"],
    ["이메일", user.email || "-"],
    ["전화번호", user.phone || "-"],
    ["도시", user.address?.city || "-"],
    ["회사", company || "-"]
  ];
  const dl = document.createElement("dl");
  dl.className = "detail-list";

  data.forEach(([label, value]) => {
    const dt = document.createElement("dt");
    const dd = document.createElement("dd");
    dt.textContent = label;
    dd.textContent = String(value);
    dl.append(dt, dd);
  });

  memberDetail.replaceChildren(dl);
}

// 7. 회원 목록 렌더링
function renderUsers(list) {
  resetMemberDisplay();

  if (list.length === 0) {
    renderEmpty();
    return;
  }

  statusMessage.dataset.state = "success";
  statusMessage.textContent = `검색 결과 ${list.length}명`;

  list.forEach(user => {
    const li = document.createElement("li");
    const button = document.createElement("button");
    const name = document.createElement("strong");
    const email = document.createElement("small");
    button.type = "button";
    button.className = "member-item";
    name.textContent = user.name || "이름 없음";
    email.textContent = user.email || "이메일 없음";
    button.append(name, email);
    button.addEventListener("click", () => renderMemberDetail(user));
    li.append(button);
    memberList.append(li);
  });
}

// 8. 검색 submit → GET → filter → render
searchForm.addEventListener("submit", async event => {
  event.preventDefault();
  const keyword = searchInput.value.trim();
  console.log("회원 검색어:", keyword);

  users = [];
  renderLoading();
  searchButton.disabled = true;
  try {
    users = await fetchUsers();
    renderUsers(filterUsers(keyword));
  } catch (error) {
    console.error("회원 조회 오류:", error);
    renderError("회원 정보를 불러오지 못했습니다.");
  } finally {
    searchButton.disabled = false;
  }
});

// 9. POST 등록 요청 — 외부 서비스는 영구 DB 저장용이 아닙니다.
async function createUserRequest(user) {
  const response = await fetch(USERS_API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(user)
  });
  if (!response.ok) {
    throw new Error(`회원 등록 요청 실패 (HTTP ${response.status})`);
  }
  return response.json();
}

// 10. 등록 submit → FormData → POST → 결과 메시지
memberForm.addEventListener("submit", async event => {
  event.preventDefault();

  const data = new FormData(memberForm);
  const name = String(data.get("name") ?? "").trim();
  const username = String(data.get("username") ?? "").trim();
  const email = String(data.get("email") ?? "").trim();

  if (!name || !username || !email) {
    formMessage.dataset.state = "error";
    formMessage.textContent = "이름, 사용자명, 이메일을 모두 입력하세요.";
    return;
  }

  const newUser = { name, username, email };
  console.log("등록 요청 데이터:", newUser);
  formMessage.dataset.state = "loading";
  formMessage.textContent = "회원 등록 요청 중...";
  registerButton.disabled = true;

  try {
    const responseData = await createUserRequest(newUser);
    console.log("POST 응답:", responseData);
    formMessage.dataset.state = "success";
    formMessage.textContent = "등록 요청이 성공했습니다. 실제 회원 DB에 저장되지는 않습니다.";
    memberForm.reset();
    // 성공한 것처럼 화면의 users 배열에 임의로 추가하지 않습니다.
  } catch (error) {
    console.error("회원 등록 요청 오류:", error);
    formMessage.dataset.state = "error";
    formMessage.textContent = "등록 요청에 실패했습니다.";
  } finally {
    registerButton.disabled = false;
  }
});
