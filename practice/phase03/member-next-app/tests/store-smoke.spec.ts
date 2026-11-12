import { expect, test, type Page } from "@playwright/test";

// STEP 17~18의 예시 상품은 API 응답을 대체하는 테스트 데이터입니다.
const firstProduct = { id: 1, name: "아이스 말차 라떼", price: 5500, category: "음료", stock: 20 };
const secondProduct = { id: 7, name: "말차 아이스크림", price: 4500, category: "디저트", stock: 0 };

async function useExampleProducts(page: Page, products: object[]) {
  await page.route("**/products", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      headers: { "access-control-allow-origin": "*" },
      body: JSON.stringify(products),
    });
  });
}

test("STEP 17: 상품 하나의 Props가 카드에 표시된다", async ({ page }) => {
  await useExampleProducts(page, [firstProduct]);
  await page.goto("http://localhost:3000/store");
  const cards = page.locator("#menu ul > li");
  await expect(cards).toHaveCount(1);
  await expect(cards.first()).toContainText("아이스 말차 라떼");
  await expect(cards.first()).toContainText("5,500원");
  await expect(cards.first()).toContainText("음료");
  await expect(cards.first()).toContainText("남은 수량 20개");
  await expect(cards.first().getByRole("button", { name: "담기 준비 중" })).toBeDisabled();
});

test("STEP 18: 서로 다른 Props와 품절 상태를 표시한다", async ({ page }) => {
  await useExampleProducts(page, [firstProduct, secondProduct]);
  await page.goto("http://localhost:3000/store");
  const cards = page.locator("#menu ul > li");
  await expect(cards).toHaveCount(2);
  await expect(cards.nth(0)).toContainText("아이스 말차 라떼");
  await expect(cards.nth(0)).toContainText("5,500원");
  await expect(cards.nth(0)).toContainText("음료");
  await expect(cards.nth(0).locator('[class*="drinkVisual"]')).toHaveCount(1);
  await expect(cards.nth(1)).toContainText("말차 아이스크림");
  await expect(cards.nth(1)).toContainText("4,500원");
  await expect(cards.nth(1)).toContainText("디저트");
  await expect(cards.nth(1).locator('[class*="dessertVisual"]')).toHaveCount(1);
  await expect(cards.nth(1)).toContainText("SOLD OUT");
  await expect(cards.nth(1).getByRole("button", { name: "품절" })).toBeDisabled();
});

test("STEP 19: 실제 API 상품 목록과 품절을 표시한다", async ({ page }) => {
  const errors: string[] = [];
  page.on("pageerror", (error) => errors.push(error.message));
  page.on("console", (message) => {
    if (message.type() === "error" || /unique.*key|key.*unique/i.test(message.text())) {
      errors.push(message.text());
    }
  });
  const responsePromise = page.waitForResponse((response) =>
    response.url() === "http://127.0.0.1:8000/products" && response.request().method() === "GET"
  );
  await page.goto("http://localhost:3000/store");
  const response = await responsePromise;
  expect(response.status()).toBe(200);
  const products = await response.json() as { id: number; name: string; price: number; stock: number }[];
  expect(products).toHaveLength(7);
  const cards = page.locator("#menu ul > li");
  await expect(cards).toHaveCount(products.length);
  for (let index = 0; index < products.length; index++) {
    const item = products[index];
    await expect(cards.nth(index)).toContainText(item.name);
    await expect(cards.nth(index)).toContainText(`${item.price.toLocaleString("ko-KR")}원`);
    await expect(cards.nth(index)).toContainText(item.stock === 0 ? "재고 없음" : `남은 수량 ${item.stock}개`);
  }
  const soldOut = cards.filter({ has: page.getByRole("heading", { name: "말차 아이스크림" }) });
  await expect(soldOut).toContainText("SOLD OUT");
  await expect(soldOut.getByRole("button", { name: "품절" })).toBeDisabled();
  expect(errors).toEqual([]);
});

test("기존 회원 목록과 진단 GET 화면이 유지된다", async ({ page }) => {
  await page.goto("http://localhost:3000/members");
  await expect(page.getByRole("heading", { name: "회원 목록", exact: true })).toBeVisible();
  await expect(page.getByLabel("회원 검색")).toBeVisible();
  await page.goto("http://localhost:3000/diagnostics");
  await expect(page.getByRole("heading", { name: "회원관리 API 진단" })).toBeVisible();
  const responsePromise = page.waitForResponse((response) =>
    response.url() === "http://127.0.0.1:8000/members" && response.request().method() === "GET"
  );
  await page.getByRole("button", { name: "실제 회원 목록 GET 검사" }).click();
  expect((await responsePromise).status()).toBe(200);
  await expect(page.getByRole("status")).toContainText("조회 성공");
});
