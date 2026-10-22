// Run offline with Node.js: node practice/phase01/chapter15/tests/run-tests.cjs
// No npm dependencies; this is a mocked DOM/HTTP logic test, NOT real browser/Network evidence.
"use strict";
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

class MockElement {
  constructor(tag = "div") {
    this.tagName = tag;
    this.children = [];
    this.listeners = {};
    this.dataset = {};
    this._text = "";
    this.value = "";
    this.disabled = false;
    this.fields = {};
  }
  set textContent(value) {
    this._text = String(value);
    this.children = [];
  }
  get textContent() {
    return this._text + this.children.map(child => child.textContent).join("");
  }
  replaceChildren(...children) {
    this.children = children;
    this._text = "";
  }
  append(...children) {
    this.children.push(...children);
  }
  addEventListener(name, handler) {
    if (!this.listeners[name]) this.listeners[name] = [];
    this.listeners[name].push(handler);
  }
  querySelector(selector) {
    assert.equal(selector, 'button[type="submit"]');
    return this.submitButton;
  }
  async fire(name) {
    let prevented = false;
    for (const handler of this.listeners[name] || []) {
      await handler({ preventDefault() { prevented = true; } });
    }
    return prevented;
  }
  reset() {
    this.fields = {};
    this.resetCount = (this.resetCount || 0) + 1;
  }
}

class MockFormData {
  constructor(form) { this.fields = form.fields; }
  get(key) { return this.fields[key] ?? null; }
}

let assertions = 0;
function check(condition, description) {
  assert.ok(condition, description);
  assertions += 1;
}

function fixture(project, ids) {
  const html = fs.readFileSync(path.join(project, "index.html"), "utf8");
  const css = fs.readFileSync(path.join(project, "style.css"), "utf8");
  const source = fs.readFileSync(path.join(project, "app.js"), "utf8");
  check(html.includes('href="style.css"') && html.includes('src="app.js"'), "HTML links CSS and JS");
  check(css.length > 100, "CSS exists");
  for (const id of ids) check(html.includes('id="' + id + '"'), "HTML has #" + id);
  check(!source.includes(".innerHTML"), "No unsanitized innerHTML");

  const nodes = Object.fromEntries(ids.map(id => [id, new MockElement(id)]));
  const searchForm = nodes["search-form"];
  const secondForm = nodes["book-form"] || nodes["member-form"];
  searchForm.submitButton = new MockElement("button");
  secondForm.submitButton = new MockElement("button");
  const responses = [];
  const calls = [];
  const consoleErrors = [];
  const document = {
    querySelector(selector) {
      return nodes[selector.slice(1)] ?? null;
    },
    createElement(tag) {
      return new MockElement(tag);
    }
  };
  const fetch = async (url, options) => {
    calls.push({ url, options });
    assert.ok(responses.length > 0, "Fetch response not queued");
    const response = responses.shift();
    if (response.reject) throw new Error(response.reject);
    return {
      ok: response.status >= 200 && response.status < 300,
      status: response.status,
      json: async () => response.data
    };
  };
  const fakeConsole = {
    log() {},
    error(...args) { consoleErrors.push(args); }
  };
  const context = vm.createContext({ document, fetch, console: fakeConsole, FormData: MockFormData });
  vm.runInContext(source, context, { filename: path.join(project, "app.js") });
  const enqueue = (status, data) => responses.push({ status, data });
  check(searchForm.listeners.submit.length === 1, "Exactly one search submit handler");
  check(secondForm.listeners.submit.length === 1, "Exactly one register submit handler");
  return { nodes, calls, consoleErrors, enqueue };
}

async function testBookExplorer() {
  const dir = path.resolve(__dirname, "..", "..", "chapter15-prepractice");
  const app = fixture(dir, [
    "search-form", "search-input", "status-message", "book-list",
    "book-detail", "book-form", "form-message"
  ]);
  const e = app.nodes;
  const docs = [
    { key: "/works/OL1W", title: "JavaScript Basics", author_name: ["A", "B"], first_publish_year: 2024 },
    { key: "/works/OL2W", title: "Untitled", author_name: [] }
  ];

  e["search-input"].value = "  javascript  ";
  app.enqueue(200, { docs });
  check(await e["search-form"].fire("submit"), "Book search prevents default");
  check(app.calls[0].url ===
    "https://openlibrary.org/search.json?q=javascript&limit=10&fields=key,title,author_name,first_publish_year",
    "Book GET URL");
  check(e["book-list"].children.length === 2, "Book list has 2 items");
  check(e["status-message"].textContent === "검색 결과 2권", "Book success state");
  check(e["book-list"].children[1].textContent.includes("저자 정보 없음"),
    "Missing author fallback");
  await e["book-list"].children[0].children[0].fire("click");
  check(e["book-detail"].textContent.includes("/works/OL1W"), "Book detail click works");

  app.enqueue(200, { docs: [] });
  await e["search-form"].fire("submit");
  check(e["status-message"].dataset.state === "empty", "Book empty state");
  app.enqueue(503, {});
  await e["search-form"].fire("submit");
  check(e["status-message"].dataset.state === "error", "Book error state");

  e["book-form"].fields = { title: " Clean Code ", author: " Robert C. Martin " };
  app.enqueue(201, { id: 101 });
  check(await e["book-form"].fire("submit"), "Book register prevents default");
  const post = app.calls.at(-1);
  check(post.url === "https://jsonplaceholder.typicode.com/posts" && post.options.method === "POST",
    "Book POST URL/method");
  check(JSON.stringify(JSON.parse(post.options.body)) === JSON.stringify({
    title: "Clean Code", author: "Robert C. Martin"
  }), "Book POST payload");
  check(e["form-message"].dataset.state === "success" && e["book-form"].resetCount === 1,
    "Book POST success/reset");

  e["book-form"].fields = { title: "Fail", author: "Tester" };
  app.enqueue(503, {});
  await e["book-form"].fire("submit");
  check(e["form-message"].dataset.state === "error", "Book POST failure");
  check(app.consoleErrors.length === 2, "Expected book errors logged");
  check(!e["search-form"].submitButton.disabled && !e["book-form"].submitButton.disabled,
    "Book submit buttons restored");
}

async function testMemberManagement() {
  const dir = path.resolve(__dirname, "..");
  const app = fixture(dir, [
    "search-form", "search-input", "status-message", "member-list",
    "member-detail", "member-form", "form-message"
  ]);
  const e = app.nodes;
  const members = [
    { id: 1, name: "Leanne Graham", username: "Bret", email: "leanne@example.com",
      address: { city: "Gwenborough" }, company: { name: "Acme" } },
    { id: 2, name: "Ervin Howell", username: "Antonette", email: "ervin@example.com" }
  ];

  e["search-input"].value = "";
  app.enqueue(200, members);
  check(await e["search-form"].fire("submit"), "Member search prevents default");
  check(app.calls[0].url === "https://api.jsonplaceholder.dev/users", "Member GET URL");
  check(e["member-list"].children.length === 2, "Member list renders");
  await e["member-list"].children[0].children[0].fire("click");
  check(e["member-detail"].textContent.includes("Gwenborough"), "Member detail click");

  e["search-input"].value = "ANTONETTE";
  app.enqueue(200, members);
  await e["search-form"].fire("submit");
  check(e["member-list"].children.length === 1, "Case insensitive member filtering");

  e["search-input"].value = "no-results";
  app.enqueue(200, members);
  await e["search-form"].fire("submit");
  check(e["status-message"].dataset.state === "empty", "Member empty state");

  app.enqueue(503, {});
  await e["search-form"].fire("submit");
  check(e["status-message"].dataset.state === "error", "Member GET error state");

  e["member-form"].fields = {
    name: " 홍길동 ", username: " hong123 ", email: " hong@example.com "
  };
  app.enqueue(201, { id: 11 });
  check(await e["member-form"].fire("submit"), "Member register prevents default");
  const post = app.calls.at(-1);
  check(post.options.method === "POST" && post.url === "https://api.jsonplaceholder.dev/users",
    "Member POST URL/method");
  check(JSON.stringify(JSON.parse(post.options.body)) === JSON.stringify({
    name: "홍길동", username: "hong123", email: "hong@example.com"
  }), "Member POST payload is trimmed");
  check(e["form-message"].dataset.state === "success" && e["member-form"].resetCount === 1,
    "Member POST success/reset");

  e["member-form"].fields = { name: "Fail", username: "fail", email: "fail@example.com" };
  app.enqueue(503, {});
  await e["member-form"].fire("submit");
  check(e["form-message"].dataset.state === "error", "Member POST error state");
  check(app.consoleErrors.length === 2, "Expected member errors logged");
  check(!e["search-form"].submitButton.disabled && !e["member-form"].submitButton.disabled,
    "Member submit buttons restored");
}

(async () => {
  await testBookExplorer();
  await testMemberManagement();
  console.log("PASS: " + assertions + " offline assertions across Book Explorer & Member Management.");
  console.log("NOTE: Mocked DOM/fetch only; validate actual Live Server + DevTools Network separately.");
})().catch(error => {
  console.error("FAIL:", error);
  process.exitCode = 1;
});
