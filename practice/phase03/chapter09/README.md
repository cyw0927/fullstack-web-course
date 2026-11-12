# Phase 03 확장 · Chapter 09 학습 노트
## React Mini Pop-up Store — 4시간 1-Day 종합 프로젝트

> **기록일:** 2026-11-12  
> **원본 강의:** 아토믹데브, 「[Phase 03 실습 집중 8강 · 확장] Chapter 09 — 4시간 1-Day 종합 프로젝트: React Mini Pop-up Store」 (사용자가 제공한 강의안, 총 30개 Sync STEP)  
> **현재 상태:** **STEP 01 IN PROGRESS / 사용자 흐름 개념 설명 제공, 이해 확인 대기(HOLD). 구현·테스트·DB 생성은 아직 하지 않음.**  
> **목적:** 나중에 이 파일만 읽어도 강의의 목표, API·DB 계약, STEP별 순서, 검증 기준, 다음 할 일을 복원할 수 있게 기록한다.

이 문서는 강의안의 **학습용 요약·재개 체크리스트**다. 강의안의 모든 예시 코드나 설명을 복제한 원문은 아니다. 강의 원문의 세부 주의사항과 예시는 사용자가 제공한 자료를 함께 참고한다.

[저장소 루트](../../../README.md) · [Phase 03 기존 회원관리 프로젝트](../README.md) · [기존 Next.js 앱](../member-next-app/README.md)

---

## 1. 배경: 이전 강의와 현재 프로젝트

- GitHub 저장소: **`https://github.com/cyw0927/fullstack-web-course`**
- 로컬 저장소: **`C:\dev\fullstack-web-course`** (강의안의 예시 `C:\dev\phase03`을 그대로 사용하지 않는다)
- 기존 Backend: `C:\dev\fullstack-web-course\practice\phase03\backend` — FastAPI + SQLAlchemy + PostgreSQL
- 기존 Frontend: `C:\dev\fullstack-web-course\practice\phase03\member-next-app` — Next.js App Router + React + TypeScript
- Phase 03 1~6강: 회원 목록·검색·CRUD·상세 페이지 구현. 성별 `M`/`F`/`null` 확장도 수행함.
- 7강: `app/diagnostics/page.tsx` 진단 화면을 GitHub에 추가함. 사용자가 `/diagnostics` 화면이 잘 작동한다고 확인함. **별도 회귀 검증·최신 빌드 PASS는 이 문서에 증빙되지 않음.**
- 8강: README 최신화는 진행했으나 `docs/evidence/RESULTS.md` 및 최종 제출 전체 검증은 **보류**.
- **Chapter 09는 기존 회원관리의 9강이 아니라, 새 주제인 'Mini Pop-up Store' 종합 실습**이다. 기존 회원관리 파일·API·DB 데이터를 덮어쓰거나 삭제하지 않는다.

### 재개 시 제일 먼저 확인할 것

1. 현재 Git 브랜치와 `git status --short`를 확인한다. 과거 Phase 02에 **미커밋 변경 및 충돌 해결 이력**이 있었으므로 `git reset --hard`·`git clean -fd`를 사용하지 않는다.
2. 기존 FastAPI의 `app.main:app`, SQLAlchemy `get_db`, PostgreSQL 연결 방식과 Next.js `package.json`·`app`·`lib`의 **실제 파일**을 먼저 읽는다.
3. 기존 앱을 유지하면서 상품 실습을 둘 **안전한 별도 경로**를 결정한다. 강의안 예시는 Next.js `/store` 라우트나 별도 `chapter09` 구조를 허용하지만, **아직 구현 위치는 확정하지 않았다**.
4. **상품 테마는 아직 선택하지 않았다.** 예: 카페, 간식, 여행 굿즈, 반려동물, 게임 굿즈. 먼저 사용자가 선택하거나 추후 원하는 테마를 확인한다.
5. 기존 DB를 초기화하거나 `drop_all` 하지 않는다. 학습용 DB/스키마와 권한을 확인한 후 필요한 테이블만 안전하게 준비한다.

---

## 2. 만들 서비스와 사용자 흐름

**목표:** 실제 PostgreSQL 상품 데이터를 Next.js 화면에 표시하고, React 장바구니에서 수량·합계를 관리한 후, FastAPI 주문 API로 재고를 안전하게 차감하고 주문을 저장하는 작은 상점.

```text
상품 목록(GET /products)
    → 상품 카드·품절 표시
    → 장바구니에 담기 (React State)
    → 수량 변경 / 제거 / 총액 계산
    → 주문하기 버튼
    → POST /orders (product_id + quantity만 전송)
    → FastAPI가 DB 실제 가격·재고 검증
    → 트랜잭션으로 orders + order_items 저장, products.stock 감소
    → 주문 ID / 주문 완료 화면
    → PostgreSQL에서 최종 저장 결과 확인
```

### 시스템 아키텍처

```text
브라우저 (Next.js / React / TypeScript)
  ├─ ProductCard, 상품 목록, 장바구니 State
  └─ GET /products · POST /orders
                   ↓ HTTP / JSON
FastAPI Router → Service(업무 규칙) → Repository(DB 접근)
                   ↓ SQLAlchemy Session
PostgreSQL: products / orders / order_items

Backend 검증: pytest (격리된 테스트 DB/fixture)
Frontend E2E: Playwright (브라우저 + 격리된 테스트 DB)
검증 도구: Browser DevTools Network, Swagger, SQL SELECT
```

**구분:** 장바구니는 React State에 저장하고 DB에는 별도 장바구니 테이블을 만들지 않는다. 상품 카드의 합계는 표시용이다. **주문 최종 가격은 FastAPI가 DB 가격을 기준으로 재계산한다.**

---

## 3. 필수 PRD (변경하지 않을 범위)

| 영역 | 필수 기능 |
| --- | --- |
| 상품 | 상품명·가격·카테고리·재고 표시, 재고 0이면 품절 및 담기 비활성화 |
| 장바구니 | 추가·제거, 같은 상품 수량 통합, +/−, 재고 상한, 총수량 Badge, 총액 |
| 주문 | `POST /orders`, 서버 가격·재고 검증, 한 트랜잭션으로 주문·상세 저장·재고 차감 |
| API | `GET /products`, `POST /orders` **두 개가 필수** |
| DB | `products`, `orders`, `order_items` **세 테이블** |
| 검증 | Swagger, Browser/Network, PostgreSQL SELECT, pytest, Playwright |

**범위 제외:** 로그인/JWT, 실제 결제(PG), 배송, 관리자 페이지, Redux/Zustand, WebSocket, 운영 배포, 과도한 최적화. `GET /orders`는 시간이 남을 때만 선택 Challenge.

---

## 4. 고정 데이터 계약

### 4-1. PostgreSQL (테이블 3개)

#### `products`

| 필드 | 타입·제약 |
| --- | --- |
| `id` | 정수 PK (강의 예: BIGINT identity) |
| `name` | VARCHAR(120), NOT NULL |
| `price` | INTEGER, 원 단위, 0 이상 |
| `category` | VARCHAR(60), NOT NULL |
| `stock` | INTEGER, 0 이상 |

#### `orders`

| 필드 | 타입·제약 |
| --- | --- |
| `id` | 정수 PK |
| `total_price` | 서버가 계산한 원 단위 정수 |
| `status` | 문자열, 기본값 `created` |
| `created_at` | 주문 생성 시각 |

#### `order_items`

| 필드 | 타입·제약 |
| --- | --- |
| `id` | 정수 PK |
| `order_id` | FK → `orders.id` |
| `product_id` | FK → `products.id` |
| `quantity` | 정수, 1 이상 |
| `price` | 주문 시점 단가 **스냅샷** |

관계: `orders(1) → order_items(N) ← products(1)`. 하나의 주문에 상품 2종류를 담으면 `orders` 1행과 `order_items` 2행이 저장된다.

### 4-2. API 응답/요청

**GET `/products` — 200 OK, JSON 배열**

```json
[
  {
    "id": 1,
    "name": "초코 쿠키",
    "price": 3000,
    "category": "간식",
    "stock": 15
  }
]
```

**POST `/orders` — 가격/총액을 보내지 않음**

```json
{
  "items": [
    { "product_id": 1, "quantity": 2 }
  ]
}
```

**성공 응답 — 201 Created**

```json
{
  "id": 10,
  "total_price": 6000,
  "status": "created"
}
```

위 JSON과 수치는 **강의 설명용 예시**이며 실제 DB 테스트 결과가 아니다.

| 상황 | 기대 HTTP 코드 |
| --- | --- |
| 상품 목록 조회 성공 | `200` |
| 주문 생성 성공 | `201` |
| 상품 ID 없음 | `404` |
| 재고 부족 | `409` |
| quantity ≤ 0, 누락·타입 오류 | `422` |

중복 `product_id`가 주문 items 배열에 포함되면 **수량을 합산**하는 정책을 권장한다(강의 기준). 합산 후 재고를 검사한다. 프론트의 장바구니도 동일 상품을 한 행으로 합친다.

### 4-3. 주문·재고 안전 규칙

- 클라이언트에서 보낸 `price`·`total_price`는 신뢰하지 않는다. **DB의 `products.price`**만 사용한다.
- 주문 전체의 상품 존재·재고를 먼저 검증한다.
- 동시 주문의 초과판매를 방지하도록 **행 잠금(예: FOR UPDATE) 또는 조건부 UPDATE** 등 적절한 방법을 적용한다.
- `orders` 생성, `order_items` 생성, `products.stock` 감소를 **단일 트랜잭션**으로 처리한다.
- Repository에서 중간 `commit`하지 않고, Service 계층에서 최종 `commit` / 실패 시 `rollback`을 관리한다.
- 중간 하나라도 실패하면 **주문·상세·재고 어느 것도 부분 저장되지 않아야** 한다.

---

## 5. 30개 STEP 진도표 (Sync Board)

**원칙:** 각 STEP에서 개념 이해 → 필요한 코드 작성 → 실제 실행 → Evidence → PASS 확인 후 다음 단계. STEP 01은 개념 설명을 제공했으나 사용자 이해 확인 전이므로 HOLD, STEP 02~30은 미진행이다.

| STEP | 실습 목표 | 필수 확인 / Evidence | 상태 |
| --- | --- | --- | --- |
| 01 | 사용자 흐름 이해 | GET → cart State → POST → DB 설명 | **HOLD** (설명 제공, 이해 확인 대기) |
| 02 | PRD 및 MVP 범위 고정 | 필수 API 2개, DB 3개, 제외 기능 구분 | ☐ |
| 03 | 데이터 흐름 이해 | Router/Service/Repository 역할 설명 | ☐ |
| 04 | 개발환경 사전 검사 | Python·pytest·Node·npm·DB·Swagger·Playwright | ☐ |
| 05 | products 테이블 설계 | 5개 필드, PK, 가격·재고 제약 | ☐ |
| 06 | orders/order_items 관계 | PK/FK, 주문 1:N, 단가 스냅샷 | ☐ |
| 07 | SQLAlchemy 모델 및 DB 테이블 | 실제 DB 테이블 3개와 제약조건 SELECT 확인 | ☐ |
| 08 | 상품 Seed 6~8개 | 중복 없이 입력 후 SELECT 건수 확인 | ☐ |
| 09 | FastAPI/Swagger 실행 | 기존 서버 및 /docs 정상 접속 | ☐ |
| 10 | DB 세션 및 동일 DB 확인 | Backend와 SQL 클라이언트 조회 값 일치 | ☐ |
| 11 | Product Repository 조회 | SQLAlchemy `select(Product)`, DB 건수 확인 | ☐ |
| 12 | Product Service 조회 | Service → Repository → DB | ☐ |
| 13 | GET /products 연결 | Swagger 200 + JSON 배열 + Seed 데이터 | ☐ |
| 14 | pytest 상품 API | 200, 배열, 상품 필드·타입, 격리 fixture | ☐ |
| 15 | Next.js 개발 서버 | 기존 앱 보존, 브라우저·Console | ☐ |
| 16 | ProductCard + Product 타입 | Props, 품절 표시, 담기 버튼 설계 | ☐ |
| 17 | 카드 한 개 표시 | 브라우저에 가상 상품 1개 | ☐ |
| 18 | 같은 카드에 서로 다른 Props | 서로 다른 상품 2개 표시 | ☐ |
| 19 | map/key 상품 리스트 | 카드 6개 이상, key 경고 없음, Playwright Smoke ① | ☐ |
| 20 | TypeScript cart State | `CartItem = Product & {quantity:number}` | ☐ |
| 21 | 담기 Event 및 Badge | 담기 수량 증가, 중복 행 없음, Smoke ② | ☐ |
| 22 | 장바구니 +/− | 재고 상한, 1→0이면 제거 | ☐ |
| 23 | Derived State 합계 | `reduce`, 3000×2 + 2500×1 = 8500원 / 3개 | ☐ |
| 24 | useEffect 이해 | GET은 초기 로드, POST는 버튼 클릭 | ☐ |
| 25 | 실제 GET /products 연동 | Network 200, DB와 화면 일치, Smoke ③ | ☐ |
| 26 | Loading/Error/Empty/재시도 | 실패 후 API 복구, 재조회 확인 | ☐ |
| 27 | POST /orders 구현 | Swagger 201, DB 가격·재고, 원자적 주문 저장 | ☐ |
| 28 | 주문 pytest·rollback | 201/404/409/422, 재고, 실패 시 전부 rollback | ☐ |
| 29 | React 주문 + Playwright E2E | 주문 흐름 + Network 201 + 격리 DB 저장 | ☐ |
| 30 | 최종 통합 검증 | DB·Swagger·pytest·Playwright·주문 ID 대응 | ☐ |

### 학습 구간별 Gate

1. **B1 (01~04):** PRD·흐름 이해 + 로컬 개발환경 확인
2. **B2 (05~10):** 실제 DB 테이블 3개, Seed ≥6, SQLAlchemy/Swagger 검증
3. **B3 (11~14):** GET `/products` + pytest 통과
4. **B4 (15~26):** 상품 UI/장바구니/실제 GET, Loading/Error, Playwright Smoke ①~③
5. **B5 (27~30):** 실제 주문 저장, 재고 차감, pytest 및 Playwright E2E, SQL 최종 확인

---

## 6. Seed 상품 예시 (테마 확정 전 예시일 뿐)

강의안의 기본 예시 6개. 테마 선택 시 **이 표를 사용자 취향에 맞춰 바꿔도 되지만 필드·검증 규칙은 유지한다.**

| 상품 | 가격(원) | 카테고리 | 재고 |
| --- | ---: | --- | ---: |
| 초코 쿠키 | 3,000 | 간식 | 15 |
| 아메리카노 | 2,500 | 음료 | 20 |
| 딸기 케이크 | 5,500 | 디저트 | 8 |
| 감자칩 | 2,000 | 간식 | 12 |
| 탄산수 | 1,500 | 음료 | 25 |
| 샌드위치 | 4,500 | 식사 | 10 |

**Seed는 다시 실행해도 기존 상품이 중복되지 않도록** 기존 데이터와 식별 기준을 확인한다. Seed를 다시 넣기 위해 DB를 전부 삭제하지 않는다.

---

## 7. 중요한 React·테스트 개념

### React

- `Product` 타입: `id:number, name:string, price:number, category:string, stock:number`
- `ProductCard`: 상품 정보와 `onAdd(product)` 콜백을 Props로 받아 표시
- `map()`으로 목록 렌더링, `key={product.id}`
- `CartItem = Product & {quantity:number}`
- `useState<CartItem[]>([])`로 하나의 상위 컴포넌트에서 cart State 소유
- 담기 버튼 → Event → `setCart` 불변 업데이트 → React 재렌더
- Badge: **서로 다른 상품 종류가 아니라 수량 합계**.
- Derived State: `totalCount = cart.reduce((s,i)=>s+i.quantity,0)`, `totalPrice = cart.reduce((s,i)=>s+i.price*i.quantity,0)`. 별도 중복 state로 저장하지 않는다.
- 재고 `stock=0`이면 담기 불가, 수량 +는 stock 초과 불가, 수량 1에서 −를 누르면 항목 제거
- `useEffect`는 초기 상품 **GET**에 사용, 주문 **POST**는 사용자가 버튼을 누를 때만 실행
- API의 Loading/Success/Empty/Error를 구분하고 실패 시 재시도 가능하게 구현
- 주문 중 버튼 비활성화로 중복 주문 방지, 실패 시 cart 내용 보존

### pytest (Backend)

필수 항목:
1. GET `/products`: 200, JSON 배열, 필수 필드/타입
2. POST `/orders` 정상: 201, DB 금액 기준, 주문·상세 생성, 재고 감소
3. 없는 상품: 404 및 DB 변화 없음
4. 재고 부족: 409 및 DB 변화 없음
5. quantity 잘못됨: 422 및 DB 변화 없음
6. 다중 상품 중 한 품목 실패: **전체 rollback**, 정상 상품의 재고도 그대로
7. 중복 product_id: 합산 정책과 재고 검증
8. 기존 GET API 회귀 검증

테스트는 **실습 운영 DB와 분리된 DB/Session/fixture**로 수행한다. 단순 Mock 통과를 실제 DB 검증으로 주장하지 않는다.

### Playwright (브라우저 E2E)

- Smoke ①: 상품 목록 화면 / 카드 표시
- Smoke ②: 장바구니 담기 → Badge 0→1
- Smoke ③: 실제 GET API 200 + 상품 카드 표시
- 최종 E2E: 상품 목록 → 담기 → 수량 2 → 주문 클릭 → POST 201 → 완료 화면·주문 ID → SQL에서 orders/order_items/재고 확인

**주문 테스트는 재고를 감소시키므로 격리 DB와 테스트별 Seed/상태 복원 방법 필수**. 임의 `sleep`보다 Playwright의 locator 자동 대기를 사용한다.

### 점검 명령 예시 (실제 설치 상태 확인 후 실행)

```powershell
# 개발환경 확인
python --version
node --version
npm --version
git --version
python -m pytest --version
npx playwright --version

# 실제 구현 이후, 각 프로젝트 루트에서 실행
python -m pytest -q
npx playwright test
npx tsc --noEmit
npm run lint
npm run build
```

`npx playwright --version`은 의존성 설치를 유도할 수 있으므로 기존 환경과 패키지 상태를 먼저 확인한다. 필요할 때만 테스트 의존성/Chromium을 설치한다. **명령을 아직 실행하지 않았으므로 현재는 전부 HOLD**.

---

## 8. SQL 조회용 Evidence (실제 실습용 DB에서만)

```sql
-- 실제 연결 DB와 스키마 확인
SELECT current_database() AS db_name, current_schema() AS schema_name;

-- 테이블 실재 확인
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
  AND table_name IN ('products', 'orders', 'order_items')
ORDER BY table_name;

-- 상품 목록 / 건수
SELECT id, name, price, category, stock
FROM products ORDER BY id;
SELECT COUNT(*) AS product_count FROM products;

-- 주문 성공 후 응답 ID와 맞춰서 조회
SELECT id, total_price, status, created_at
FROM orders ORDER BY id DESC LIMIT 5;

SELECT id, order_id, product_id, quantity, price
FROM order_items ORDER BY id DESC LIMIT 10;

SELECT id, name, price, stock
FROM products ORDER BY id;
```

현재 테이블 미생성 단계에서 SQL을 실행하면 실패할 수 있다. **STEP 07 이후**에 실습용 DB에서 확인한다. 개인정보, DB 비밀번호, 전체 접속 문자열은 로그·스크린샷·Git에 올리지 않는다.

---

## 9. 다음에 다시 시작할 때의 작업 지침 (AI/Claude/Codex 인계 겸용)

> 우리는 `cyw0927/fullstack-web-course`의 **Phase 03 확장 Chapter 09: React Mini Pop-up Store**를 공부한다.  
> 현재 진도는 **STEP 01 개념 설명 제공, 사용자 이해 확인 대기(HOLD)**이며, STEP 02~30은 미진행이다. 구현·실행·테스트는 전부 미실행이다.  
> 이 `practice/phase03/chapter09/README.md`를 먼저 읽고, 기존 Phase 03 회원관리 코드·설정·Git 상태를 확인하라.  
> 로컬 저장소는 `C:\dev\fullstack-web-course`이고, Backend `practice/phase03/backend`, Frontend `practice/phase03/member-next-app`가 있다.  
> 회원관리(1~7강) 구현을 보존하고 `/members`·`/diagnostics`와 충돌하지 않는 별도 상품 실습 경로를 계획하라. 다른 미커밋 Phase 02 작업도 건드리지 마라.  
> 상품 테마/실습용 DB를 확정한 후 STEP 01부터 진행하고, 한 단계씩 **코드 → 실행 → Swagger/Network/DB/pytest/Playwright Evidence → PASS** 순서를 지켜라.  
> 사용자에게 긴 대화 내용을 다시 요구하지 말고 이 문서의 데이터 계약을 우선하되, 강의안과 실제 코드에 차이가 있으면 그 차이를 명시하고 검증하라.  
> 이미 구현하지 않은 기능이나 실행하지 않은 테스트를 완료로 표시하지 마라.

### 즉시 시작할 다음 행동

- [ ] STEP 01: 사용자 이해 확인 후 PASS 여부 기록 (현재 HOLD)
- [ ] STEP 02~03: PRD·MVP 및 계층 구분 요약
- [ ] STEP 04: 현재 로컬 Git 상태와 Python·Node·DB·Swagger·pytest·Playwright 환경 **실측**
- [ ] 상품 테마 결정 및 실제 구현 폴더/라우트 검토
- [ ] DB/Backend/Frontend에 대한 **변경 전 백업 및 영향 범위 확인**
- [ ] STEP 05 이후에는 Gate마다 사용자에게 실제 검증 결과를 설명

### 진행 기록

| 일자 | 진행 내용 | 검증 상태 |
| --- | --- | --- |
| 2026-11-12 | 사용자 제공 9강 강의안 기반으로 이 학습 노트 기록 및 GitHub 반영 | **문서만 완료; 구현·실행 전부 HOLD** |
| 2026-11-12 | STEP 01: GET → React 장바구니 State → POST → FastAPI 서버 검증 → PostgreSQL 단일 트랜잭션 흐름 안내. 사용자 이해 확인 전; 코드/DB/테스트 변경 없음 | **학습 이해 확인 대기(HOLD)** |

---

**최종 완료의 기준:** products/orders/order_items 실재, Seed 상품 6개 이상, GET 200, POST 201, DB 재고 차감과 원자성, pytest PASS, Playwright PASS, Browser/Network 증거 및 SQL 결과가 모두 확인되어야 한다. AI 코드 작성이나 문서만으로는 완료가 아니다.
