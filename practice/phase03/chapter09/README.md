# Phase 03 확장 · Chapter 09 학습 노트
## React Mini Pop-up Store — 4시간 1-Day 종합 프로젝트

> **기록일:** 2026-11-12  
> **원본 강의:** 아토믹데브, 「[Phase 03 실습 집중 8강 · 확장] Chapter 09 — 4시간 1-Day 종합 프로젝트: React Mini Pop-up Store」 (사용자가 제공한 강의안, 총 30개 Sync STEP)  
> **현재 상태 (2026-11-12):** **STEP 01~03 PASS, STEP 04 HOLD, STEP 05~12 PASS, STEP 13 코드 반영/HTTP 검증 HOLD, STEP 14 pytest PASS(5 passed, 1 warning), STEP 15 로컬 실행 대기, STEP 15~30 미진행.**
> **목적:** 나중에 이 파일만 읽어도 강의의 목표, API·DB 계약, STEP별 순서, 검증 기준, 다음 할 일을 복원할 수 있게 기록한다.

**현재 DB 구조:** 회원은 `public.members`, 매장은 `matcha_store.products` / `matcha_store.orders` / `matcha_store.order_items`에 있다. 아래 과거 STEP 05~08의 `public` DDL과 결과는 당시 이력이며 현재 실행용 SQL은 8절을 사용한다.

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
4. **상품 테마는 MATCHA HOUSE (말차 전문 팝업 카페)로 확정했다.** 디자인은 말차 그린 + 크림 화이트의 일본식 미니멀 카페 분위기. 상세 상품 및 가격은 아래 §6 참조.
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

### STEP 02 — 확정된 MVP/PRD (2026-11-12)

- **매장명/테마:** MATCHA HOUSE — 말차 전문 카페.
- **화면 방향:** 말차 그린 + 크림 화이트, 일본식 미니멀 디자인. 과도한 부가 기능은 추가하지 않는다.
- **상품:** 음료 및 디저트 7종; 상품명·가격·카테고리·재고 표시. 말차 아이스크림은 초기 재고 0개로 품절 UI를 검증한다.
- **장바구니:** React State에서 담기·제거·수량 증감, 상품별 재고 상한, 총수량 Badge 및 합계 표시. DB에 장바구니 테이블은 만들지 않는다.
- **주문:** 상품 ID와 수량만 POST, 서버가 DB 가격/재고 재확인, 단일 트랜잭션으로 주문·상세 저장과 재고 차감. 성공 201, 상품 없음 404, 재고 부족 409, 잘못된 요청 422.
- **필수 API/테이블:** `GET /products`, `POST /orders` / `products`, `orders`, `order_items`.
- **검증:** Swagger, SQL SELECT, pytest, Playwright. 기존 회원관리와 Phase 02 작업물 보존.
- **범위:** 위 항목이 최소기능제품(MVP)의 전체 범위이며 추가 결제/회원/배송 기능은 하지 않는다.

**상태: STEP 02 기획·범위 확정 PASS.** 이후 Seed 7종 DB 등록·스키마 분리 완료, 상품 GET API는 STEP 13 런타임 검증 대기.

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

### STEP 05 — MATCHA HOUSE `products` 테이블 설계 (2026-11-12)

이 STEP에서는 설계를 확정했다. **이후 사용자가 DBeaver로 기존 회원관리 DB에 products 테이블을 생성했다고 보고했다(2026-11-12).** SQL/스크린샷이나 실제 컬럼·PK·CHECK 제약·스키마는 아직 보지 못했으므로 생성 사실은 *사용자 보고*로만 기록한다. 기존 `public.members` 테이블 및 다른 회원 데이터는 변경하지 않는다. SQLAlchemy Model과 실제 DDL/테이블 검증은 **STEP 07**에서 진행한다.

| 필드 | PostgreSQL 타입 | 필수·제약 | 역할 |
| --- | --- | --- | --- |
| `id` | `BIGINT GENERATED BY DEFAULT AS IDENTITY` | `PRIMARY KEY` | 상품 고유 번호 (자동 증가) |
| `name` | `VARCHAR(120)` | `NOT NULL` | 상품명 |
| `price` | `INTEGER` | `NOT NULL`, `CHECK (price >= 0)` | 원화 정수 가격 |
| `category` | `VARCHAR(60)` | `NOT NULL` | 음료 또는 디저트 |
| `stock` | `INTEGER` | `NOT NULL`, `CHECK (stock >= 0)` | 현재 판매 가능 재고 |

**DDL 설계안(사용자가 DBeaver에서 실행했을 수 있으나 실제 실행 SQL은 미확인):**

```sql
CREATE TABLE public.products (
    id BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    price INTEGER NOT NULL CHECK (price >= 0),
    category VARCHAR(60) NOT NULL,
    stock INTEGER NOT NULL CHECK (stock >= 0)
);
```

- `id`는 상품 행의 유일한 식별자다. 가격·재고에는 음수 저장을 방지하는 제약을 둔다.
- 상품 테마는 위 §6의 MATCHA HOUSE 상품 7종(음료 3, 디저트 4; 아이스크림 재고 0).
- 매장 UI는 재고 0이면 **품절**로 표시하고 담기 버튼을 비활성화한다. DB의 `CHECK`는 음수 저장 방지 수단이고, 실제 주문의 동시 재고 초과판매 방지는 별도 트랜잭션/행 잠금으로 구현한다.
- **실제 DDL 전** 대상 DB·스키마·동명 `public.products` 테이블이 존재하는지 읽기 전용 조회하여 기존 데이터 충돌을 확인한다. 확인 없이 덮어쓰기·`DROP TABLE`·`drop_all`·DB 초기화는 하지 않는다.
- 새로운 컬럼(`image_url`, 설명, SKU 등)이나 추가 테이블은 STEP 05 필수 요구가 아니므로 넣지 않는다.

**Evidence:** 5개 필드, PK, price/stock 비음수 제약, 원 단위 가격, MATCHA HOUSE seed 7종 계획이 이 문서에 기록됨. **설계 PASS**. 사용자 DBeaver 생성 보고는 접수했으나 SQL/실제 DB 테이블 실재와 제약조건 검증 PASS가 아니다.

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

### STEP 06 — 주문/주문 상세 관계 설계 (2026-11-12)

**설계 목표:** 주문 1건에 여러 상품 행을 연결하고, 주문 시점 가격을 보존한다. 기존 `members` 및 사용자가 이미 생성했다고 보고한 `products`는 삭제하거나 재생성하지 않는다.

| 테이블 | 필드 | 제약/의미 |
| --- | --- | --- |
| `orders` | `id` | BIGINT IDENTITY, PK |
| `orders` | `total_price` | INTEGER NOT NULL, `>= 0`; 서버가 DB 가격으로 계산 |
| `orders` | `status` | VARCHAR(20) NOT NULL, DEFAULT `created` |
| `orders` | `created_at` | TIMESTAMPTZ NOT NULL, DEFAULT NOW() |
| `order_items` | `id` | BIGINT IDENTITY, PK |
| `order_items` | `order_id` | BIGINT NOT NULL, FK → `orders.id` |
| `order_items` | `product_id` | BIGINT NOT NULL, FK → `products.id` |
| `order_items` | `quantity` | INTEGER NOT NULL, CHECK `>= 1` |
| `order_items` | `price` | INTEGER NOT NULL, CHECK `>= 0`; **주문 당시 단가 스냅샷** |

관계: `orders 1:N order_items`, `products 1:N order_items` (각 상세 행은 상품 1개에 대응). **예시:** 주문 #1 = 말차 라떼 2개(5,500원) + 휘낭시에 1개(3,000원) → `orders` 1행 (`total_price=14000`) 및 `order_items` 2행 (`order_id=1` 공유).

**STEP 07 이후 검증을 위한 DDL 설계안 (현재 미실행):**

```sql
CREATE TABLE public.orders (
    id BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    total_price INTEGER NOT NULL CHECK (total_price >= 0),
    status VARCHAR(20) NOT NULL DEFAULT 'created',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE public.order_items (
    id BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    order_id BIGINT NOT NULL REFERENCES public.orders(id),
    product_id BIGINT NOT NULL REFERENCES public.products(id),
    quantity INTEGER NOT NULL CHECK (quantity >= 1),
    price INTEGER NOT NULL CHECK (price >= 0)
);
```

- 두 신규 테이블의 `id`/FK는 기존 `products.id`와 **동일한 BIGINT 계열인지 실제 DB 스키마 확인 후** 적용한다.
- DDL을 무조건 재실행하지 않는다. 동명 테이블이 있으면 현재 제약/컬럼부터 점검한다. 기존 DB 전체 초기화, `DROP TABLE`, `drop_all` 금지.
- 주문 생성, 상세 INSERT, 상품 재고 감소는 추후 **한 트랜잭션**에서 처리하며 최종 `commit/rollback`은 Service 담당.
- 테이블 설계는 **PASS**, 실제 DB 적용·FK 관계 확인은 **STEP 07에서 HOLD**.



### 4-2. API 응답/요청

**GET `/products` — 200 OK, JSON 배열**

```json
[
  {
    "id": 1,
    "name": "아이스 말차 라떼",
    "price": 5500,
    "category": "음료",
    "stock": 20
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
  "total_price": 11000,
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

**진도 원칙:** 개념 학습·코드 구현·실제 실행·Evidence를 구분한다. 아래 표와 최신 검증 기록이 현재 상태이며 과거 작업 일지의 HOLD 및 public 스키마 설명은 해당 시점의 이력이다. STEP 04 전체 점검은 HOLD, STEP 13은 HTTP 증빙 대기(HOLD)이고 STEP 14는 사용자 로컬 pytest 5 passed 결과로 PASS다.

| STEP | 실습 목표 | 필수 확인 / Evidence | 상태 |
| --- | --- | --- | --- |
| 01 | 사용자 흐름 이해 | GET → cart State → POST → DB 설명 | **PASS** (개념 설명 후 사용자 다음 단계 진행 승인) |
| 02 | PRD 및 MVP 범위 고정 | 필수 API 2개, DB 3개, 제외 기능 구분 | **PASS** (MATCHA HOUSE 7종 및 범위 확정, 문서 기록) |
| 03 | 데이터 흐름 이해 | Router/Service/Repository 역할 설명 | **PASS** (실제 회원관리 코드 확인, 사용자 이해 확인) |
| 04 | 개발환경 사전 검사 | Python·pytest·Node·npm·DB·Swagger·Playwright | **HOLD** (Git과 Backend HTTP 확인; 전체 환경 검증은 보류) |
| 05 | products 테이블 설계 | 5개 필드, PK, 가격·재고 제약 | **PASS** (실제 DB 구조와 제약 확인) |
| 06 | orders/order_items 관계 | PK/FK, 주문 1:N, 단가 스냅샷 | **PASS** (실제 DB FK 확인) |
| 07 | SQLAlchemy 모델 및 DB 테이블 | 실제 DB 테이블 3개와 제약조건 SELECT 확인 | **PASS** (컬럼 타입·NULL·PK·FK·CHECK 확인; CHECK 제약 이름은 모델과 DB가 다름) |
| 08 | 상품 Seed 6~8개 | 중복 없이 입력 후 SELECT 건수 확인 | **PASS** (DBeaver INSERT RETURNING 스크린샷에서 7종 이름·가격·카테고리·재고 확인) |
| 09 | FastAPI/Swagger 실행 | 기존 서버 및 /docs 정상 접속 | **PASS** (인계 전 사전 점검에서 Swagger 및 회원 API 정상 완료 사용자 보고) |
| 10 | DB 세션 및 동일 DB 확인 | Backend와 SQL 클라이언트 조회 값 일치 | **PASS** (DBeaver와 Backend가 localhost:5432/postgres에 연결; ORM 상품 7건 조회) |
| 11 | Product Repository 조회 | SQLAlchemy `select(Product)`, DB 건수 확인 | **PASS** (읽기 전용 DB 조회 7건, 직접 SQL과 비교) |
| 12 | Product Service 조회 | Service → Repository → DB | **PASS** (Service 결과가 Repository·SQL 결과와 동일) |
| 13 | GET /products 연결 | Swagger 200 + JSON 배열 + Seed 데이터 | **HOLD** (ProductResponse/Router/main.py GitHub 반영, 실제 HTTP 200·7종 JSON·Swagger 미검증) |
| 14 | pytest 상품 API | 200, 배열, 상품 필드·타입, 격리 fixture | **PASS** (사용자 로컬 pytest 결과 `5 passed, 1 warning in 0.75s`; SQLite 인메모리 격리 테스트) |
| 15 | Next.js 개발 서버 | 기존 앱 보존, 브라우저·Console | **HOLD** (기존 member-next-app 설치 확인 전·로컬 서버 및 브라우저 콘솔 증빙 대기) |
| 16 | ProductCard + Product 타입 | Props, 품절 표시, 담기 버튼 설계 | ☐ |
| 17 | 카드 한 개 표시 | 브라우저에 가상 상품 1개 | ☐ |
| 18 | 같은 카드에 서로 다른 Props | 서로 다른 상품 2개 표시 | ☐ |
| 19 | map/key 상품 리스트 | 카드 6개 이상, key 경고 없음, Playwright Smoke ① | ☐ |
| 20 | TypeScript cart State | `CartItem = Product & {quantity:number}` | ☐ |
| 21 | 담기 Event 및 Badge | 담기 수량 증가, 중복 행 없음, Smoke ② | ☐ |
| 22 | 장바구니 +/− | 재고 상한, 1→0이면 제거 | ☐ |
| 23 | Derived State 합계 | `reduce`, 5500×2 + 3000×1 = 14000원 / 3개 | ☐ |
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

## 6. MATCHA HOUSE 상품 Seed (당시 기획안; 현재 STEP 08 PASS)

**2026-11-12 사용자 확정:** 말차 전문 팝업 카페 `MATCHA HOUSE`. 상품은 아래 7종으로 구성한다. 가격은 원 단위 정수이며 카테고리는 `음료`·`디저트` 두 종류다.

| 상품 | 가격(원) | 카테고리 | 초기 재고 |
| --- | ---: | --- | ---: |
| 아이스 말차 라떼 | 5,500 | 음료 | 20 |
| 말차 크림 라떼 | 6,500 | 음료 | 15 |
| 말차 아포가토 | 6,000 | 음료 | 12 |
| 말차 티라미수 | 7,000 | 디저트 | 8 |
| 말차 휘낭시에 | 3,000 | 디저트 | 20 |
| 말차 쿠키 | 2,500 | 디저트 | 25 |
| 말차 아이스크림 | 4,500 | 디저트 | 0 |

- 마지막 상품은 **초기 재고 0**으로 품절 상태/담기 버튼 비활성화 기능을 검증한다.
- **이 표는 계획 데이터다.** DB 테이블 생성 및 Seed INSERT/SELECT는 STEP 07~08에서 진행한다.
- Seed는 반복 실행해도 상품이 중복되지 않도록 설계한다. Seed를 다시 넣기 위해 기존 DB를 전부 삭제하지 않는다.

---

## STEP 07 과거 작업 기록 — 기존 DB와 SQLAlchemy 모델 연결 (스키마 이동 전, 현재 STEP 07 PASS)

> **과거 이력:** 이 절의 public 관련 쿼리, HOLD, 실행 대기 문구는 스키마 이동 전 기록이며 다시 실행할 지침이 아니다. 지금은 matcha_store 스키마를 사용한다.

- **사용자 확인:** DBeaver 제약조건 조회 결과 스크린샷에서 `public.products`의 `products_pkey` (PRIMARY KEY(id)), `id/name/category/price/stock` NOT NULL, `price >= 0`, `stock >= 0` CHECK를 확인했다. **products 제약조건은 스크린샷 증빙으로 확인 완료.** 이어 제공된 `information_schema.columns` 스크린샷에서 **`products.id`가 `bigint`, `is_identity=YES`**, `name/category`가 character varying, `price/stock`이 integer이며 다섯 컬럼 모두 `is_nullable=NO`임을 확인했다. 당시 첫 조회에서는 주문 테이블이 없었으나, 이후 사용자가 DBeaver에서 CREATE TABLE 구문 실행 후 `information_schema.tables` 조회 결과 **products, orders, order_items 3개가 모두 존재함을 확인**했다. `products`의 VARCHAR 길이/실제 로컬 ORM import는 아직 확인하지 않았다.
- **GitHub 코드 작성:** `practice/phase03/backend/app/models.py`에 기존 `Member`를 보존하면서 `Product`, `Order`, `OrderItem` 모델 추가. 커밋 `693ea93`. `public.products`/`public.orders`/`public.order_items` 매핑, 고정 데이터 계약(정수 원화/주문 단가 스냅샷), PK/FK, 타입, 기본값, 제약의 *예상 메타데이터*를 정의했다.
- **실행 범위:** GitHub 소스만 변경. 사용자 로컬 `C:\dev\fullstack-web-course` 동기화, 코드 import, DB 조회, `pytest` 실행 **하지 않음**. `CREATE TABLE`/`create_all`/`drop_all` 실행하지 않음.
- **주의:** SQLAlchemy에 적은 `CheckConstraint`는 **이미 생성된 DB 테이블에 자동 추가되지 않는다.** 실제 스크린샷에서 `products.id`는 BIGINT IDENTITY로 확인되어 ORM `BigInteger`/`Identity`와 기본 타입이 일치한다. 추후 VARCHAR 길이/로컬 import는 확인 필요하다. 다른 회원관리용 테이블/데이터 보존.

**남은 읽기 전용 검증 (DBeaver, 결과에서 실제 DB 이름/계정·암호를 공유할 필요 없음):**

```sql
SELECT table_name, column_name, data_type, is_nullable, is_identity
FROM information_schema.columns
WHERE table_schema = 'public'
  AND table_name IN ('products', 'orders', 'order_items')
ORDER BY table_name, ordinal_position;

SELECT c.relname AS table_name, p.conname AS constraint_name,
       CASE p.contype
         WHEN 'p' THEN 'PRIMARY KEY'
         WHEN 'f' THEN 'FOREIGN KEY'
         WHEN 'c' THEN 'CHECK'
         ELSE p.contype::text
       END AS constraint_type,
       pg_get_constraintdef(p.oid) AS definition
FROM pg_constraint p
JOIN pg_class c ON c.oid = p.conrelid
JOIN pg_namespace n ON n.oid = c.relnamespace
WHERE n.nspname = 'public'
  AND c.relname IN ('products', 'orders', 'order_items')
ORDER BY c.relname, p.contype, p.conname;
```

사용자가 DBeaver에서 세 테이블 존재를 확인했다. STEP 07의 남은 검증은 (1) orders/order_items PK·FK·CHECK 제약 조회, (2) products VARCHAR 길이 포함 실제 컬럼 정의와 ORM 일치 확인, (3) GitHub models.py를 로컬에 안전하게 반영한 뒤 읽기 전용 import/메타데이터 확인이다. 이 항목까지 끝나야 **STEP 07 PASS** 처리한다. 현재 테이블 존재 및 products 타입·주요 제약은 확인됐으나 전체 STEP은 HOLD.

### STEP 07 당시 주문 테이블 SQL (실행 완료 이력; 다시 실행 금지)

초기 조회에서는 `products`만 존재했으나, 이후 사용자가 아래 DDL을 DBeaver에서 실행했고 세 테이블 존재 조회 결과를 확인했다. **주문 테이블 CREATE 작업은 사용자 수행이며 AI는 DB에 직접 접속하거나 DDL을 실행하지 않았다.**

```sql
-- 기존 products/members는 손대지 않는다.
-- DBeaver에서 현재 DB가 기존 학습용 postgres인지 확인 후 실행.
BEGIN;

CREATE TABLE public.orders (
    id BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    total_price INTEGER NOT NULL
        CONSTRAINT ck_orders_total_price_nonnegative CHECK (total_price >= 0),
    status VARCHAR(20) NOT NULL DEFAULT 'created',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE public.order_items (
    id BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    order_id BIGINT NOT NULL REFERENCES public.orders(id),
    product_id BIGINT NOT NULL REFERENCES public.products(id),
    quantity INTEGER NOT NULL
        CONSTRAINT ck_order_items_quantity_positive CHECK (quantity >= 1),
    price INTEGER NOT NULL
        CONSTRAINT ck_order_items_price_nonnegative CHECK (price >= 0)
);

COMMIT;
```

- 만약 다른 학습 작업에서 이미 두 테이블을 만든 경우에는 재실행하지 말고 스키마부터 비교한다. 동일 이름 테이블이 이미 있으면 `CREATE TABLE`이 오류로 멈추며 기존 테이블을 삭제하거나 덮어쓰지 않는다.
- **완료:** 위 테이블 존재 조회에서 3행 확인(사용자 보고). **남음:** 위 제약 조회에서 orders/order_items PK·FK·CHECK 점검 및 ORM 로컬 검증.
- `products` 상품 데이터는 STEP 08에서 넣는다. 이 단계는 **테이블 생성 및 스키마 검증**만 수행한다.

---

## STEP 08 과거 상품 Seed 등록 이력 (현재 PASS)

> **과거 이력:** 최초 public.products에 상품 7개를 삽입한 기록이다. 데이터는 이후 matcha_store.products로 옮겨 보존했으므로 Seed INSERT를 다시 실행하지 않는다.

사용자가 DBeaver에서 `products`, `orders`, `order_items` 세 테이블이 모두 존재한다고 확인했다. STEP 08에서는 **먼저 현재 products 행을 읽기 전용 SELECT로 확인**해 기존 데이터를 보존한다. 기존 상품이 있으면 중복 삽입하지 않고 누락 상품만 추가한다. 이름이 같지만 가격/카테고리가 다른 행이 있으면 자동 수정하지 말고 사용자에게 확인한다.

**사용자 결과 (2026-11-12):** `SELECT id, name, price, category, stock FROM public.products ORDER BY id;` 실행 결과 **0행**. 기존 상품 데이터가 없으므로 7종을 등록할 수 있다.

현재 상품 목록 확인 SQL:

```sql
SELECT id, name, price, category, stock
FROM public.products
ORDER BY id;
```

Seed 목표(원 단위 INTEGER, 총 7종):

| 상품 | 가격 | 카테고리 | 재고 |
| --- | ---: | --- | ---: |
| 아이스 말차 라떼 | 5500 | 음료 | 20 |
| 말차 크림 라떼 | 6500 | 음료 | 15 |
| 말차 아포가토 | 6000 | 음료 | 12 |
| 말차 티라미수 | 7000 | 디저트 | 8 |
| 말차 휘낭시에 | 3000 | 디저트 | 20 |
| 말차 쿠키 | 2500 | 디저트 | 25 |
| 말차 아이스크림 | 4500 | 디저트 | 0 |

**당시 사용한 DBeaver Seed SQL (기록용이며 다시 실행하지 않음):**

```sql
INSERT INTO public.products (name, price, category, stock)
SELECT seed.name, seed.price, seed.category, seed.stock
FROM (VALUES
    ('아이스 말차 라떼', 5500, '음료', 20),
    ('말차 크림 라떼', 6500, '음료', 15),
    ('말차 아포가토', 6000, '음료', 12),
    ('말차 티라미수', 7000, '디저트', 8),
    ('말차 휘낭시에', 3000, '디저트', 20),
    ('말차 쿠키', 2500, '디저트', 25),
    ('말차 아이스크림', 4500, '디저트', 0)
) AS seed(name, price, category, stock)
WHERE NOT EXISTS (
    SELECT 1 FROM public.products AS existing
    WHERE existing.name = seed.name
)
RETURNING id, name, price, category, stock;
```

- `WHERE NOT EXISTS`는 같은 상품명이 이미 있으면 해당 상품을 추가하지 않는다. 기존 상품의 가격·재고를 덮어쓰지 않는다.
- DBeaver 상단이 Auto 모드이면 별도 `BEGIN`/`COMMIT`을 붙이지 말고 이 INSERT 문장만 실행한다.
- 실행 후 아래 SELECT로 총 7행과 아이스크림 재고 0을 확인한다. 동명 상품의 기존 정보가 목표값과 다르면 자동 수정하지 말고 확인한다.

```sql
SELECT id, name, price, category, stock
FROM public.products
ORDER BY id;
```

이후 사용자가 DBeaver INSERT RETURNING 화면으로 **7종 등록을 확인했고 STEP 08 PASS** 처리했다. 당시의 미실행 안내는 더 이상 현재 상태가 아니다.

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

### STEP 04 — 설치 반복 없이 확인할 항목 (2026-11-12)

**GitHub에서 확인된 설정 (코드 정적 확인, 로컬 실행 PASS가 아님)**

- `backend/app/main.py`: FastAPI `app.main:app`, 기존 `/members` Router, localhost:3000 허용 CORS 설정 존재.
- `backend/app/db.py`: `backend/.env`에서 `DB_*` 로드, SQLAlchemy Engine/Session 구성. 실제 비밀번호·DB 연결 가능 여부는 미확인.
- `member-next-app/package.json`: Next.js `16.4.6`, React `19.3.0`, `dev/build/lint` 스크립트 존재. 현재 커밋의 manifest에는 `@playwright/test` 또는 `playwright` 의존성이 등록돼 있지 않음. 사용자가 설치 완료를 보고했지만 프로젝트 로컬 사용 가능 여부는 확인 필요.
- `backend/requirements.txt`: FastAPI, Uvicorn, SQLAlchemy, psycopg, dotenv 등 존재. pytest 의존성은 명시돼 있지 않으나 사용자 사전 설치 보고가 있음.
- 기존 `member-next-app`에서 회원관리 API 주소는 `NEXT_PUBLIC_API_BASE_URL`로 설정, 기본 개발 서버 포트는 3000. `/diagnostics`의 이전 정상 접속은 과거 사용자 보고이지 이번 STEP 04의 새 실행 증빙은 아님.

**현재 로컬 미확인:** `git status`, Python 가상환경/환경설정 파일 실재, 현재 Swagger 및 GET `/members` DB 연동 HTTP 200, Next.js 진단 페이지 HTTP 200, Playwright 실행 파일 및 Chromium 캐시. 이들은 **실제 PC의 읽기 전용 출력으로만 확인**한다. 프로그램/브라우저를 재설치하거나 DB 쓰기 작업을 하지 않는다.

**최소 PowerShell 점검 (설치/DB 변경 없음):**

```powershell
$root = 'C:\dev\fullstack-web-course'
$phase = Join-Path $root 'practice\phase03'
git -C $root branch --show-current
git -C $root status --short

[pscustomobject]@{
  PythonVenv = Test-Path (Join-Path $phase '.venv\Scripts\python.exe')
  BackendEnv = Test-Path (Join-Path $phase 'backend\.env')
  FrontendEnv = Test-Path (Join-Path $phase 'member-next-app\.env.local')
  FrontendNodeModules = Test-Path (Join-Path $phase 'member-next-app\node_modules')
  PlaywrightLocalCmd = Test-Path (Join-Path $phase 'member-next-app\node_modules\.bin\playwright.cmd')
  BrowserCacheFolder = Test-Path (Join-Path $env:LOCALAPPDATA 'ms-playwright')
} | Format-List

foreach ($url in @(
  'http://127.0.0.1:8000/docs',
  'http://127.0.0.1:8000/members',
  'http://localhost:3000/diagnostics'
)) {
  try {
    $response = Invoke-WebRequest -Uri $url -Method GET -TimeoutSec 5 -UseBasicParsing
    Write-Output "$url : HTTP $($response.StatusCode)"
  } catch {
    Write-Output "$url : OFFLINE / ERROR $($_.Exception.Message)"
  }
}
```

주의: `BackendEnv`/`FrontendEnv`는 **존재 여부만** 표시하며 파일 내용과 비밀번호는 공유하지 않는다. 서버가 꺼져 있어 HTTP 접속이 실패한 경우 곧바로 환경 실패로 단정하지 않고 기존 실행 명령으로 켠 뒤 재확인한다. 프론트 HTML 200만으로 DB 연동을 검증했다고 판단하지 않는다. 현재 STEP 04는 **HOLD (로컬 출력 대기)**.

---


## 스키마 분리 검증 — 2026-11-12 (최신)

회원관리와 매장 테이블을 분리해 기존 `public.members`를 유지한다. 기존 상품·주문 테이블을 삭제하거나 다시 만들지 않고 한 트랜잭션에서 `ALTER TABLE ... SET SCHEMA matcha_store`로 이동했다.

```text
postgres
├─ public.members
├─ matcha_store.products
├─ matcha_store.orders
└─ matcha_store.order_items
```

- 이동 전 스키마 부재 및 세 원본 테이블을 확인했다. 이동 전후 테이블 객체 ID, 전체 행의 해시, PK/FK/CHECK 제약을 비교하고 모두 같을 때 커밋했다. 상품 7건, 주문 0건, 주문 상세 0건, 회원 14건이 보존됐다. `expense_app`과 `practice` 스키마도 존재한다.
- `OrderItem.order_id → matcha_store.orders.id`, `product_id → matcha_store.products.id`를 DB에서 확인했다. Identity 컬럼과 컬럼 타입·길이·NULL 허용 여부도 로컬 SQLAlchemy 모델과 비교했다.
- CHECK 조건의 **내용은 일치**하지만 이름은 다르다. DB는 예를 들어 `products_price_check`, 모델은 `ck_products_price_nonnegative`를 사용한다. 기존 제약을 유지했으며 이후 마이그레이션 도구를 쓸 때 이름 차이를 검토한다.
- DBeaver의 연결 정보는 `localhost:5432/postgres`이며 새로고침한 트리에 `matcha_store`가 표시됐다. Backend SQLAlchemy Session도 같은 호스트·포트·DB에 연결해 상품 7건을 조회했다. DBeaver 화면에서 이동 후 상품별 행을 다시 조회하지는 않았으며, 행 보존은 DB 트랜잭션 내부 비교로 검증했다.
- FastAPI `TestClient`에서 `GET /members`는 200·14건, `/openapi.json`은 200이었다. 별도 포트의 Uvicorn을 실제 실행해 HTTP `GET /members` 200·14건과 `GET /docs` 200도 확인했다. Swagger UI에서 별도 조작은 하지 않았다.
- **STEP 07 PASS**, **STEP 10 PASS**. STEP 04의 전체 환경 검사는 별도 HOLD. 당시 다음 단계는 **STEP 11 Product Repository 조회 구현**이었다. 이후 진행은 STEP 11~12 기록을 참고한다.

---

## 8. SQL 조회용 Evidence (현재 스키마)

```sql
SELECT current_database(), current_schema(), current_user;
SELECT table_schema, table_name FROM information_schema.tables
WHERE table_schema IN ('public', 'matcha_store')
  AND table_name IN ('members', 'products', 'orders', 'order_items')
ORDER BY table_schema, table_name;
SELECT id, name, price, category, stock FROM matcha_store.products ORDER BY id;
SELECT COUNT(*) AS product_count FROM matcha_store.products;
SELECT id, total_price, status, created_at FROM matcha_store.orders ORDER BY id DESC LIMIT 5;
SELECT id, order_id, product_id, quantity, price FROM matcha_store.order_items ORDER BY id DESC LIMIT 10;
```

접속 비밀번호나 회원 개인정보는 로그·스크린샷·Git에 올리지 않는다.

---

## 9. 다음에 다시 시작할 때의 작업 지침 (AI/Claude/Codex 인계 겸용)

> 우리는 `cyw0927/fullstack-web-course`의 **Phase 03 확장 Chapter 09: React Mini Pop-up Store**를 공부한다.  
> 현재 진도는 **STEP 01~03, 05~12 PASS; STEP 04 HOLD; STEP 13 GitHub 구현 완료/HTTP 증빙 대기; STEP 14 로컬 pytest PASS(5 passed), STEP 15 기존 Next.js 실행 확인 대기; STEP 15~30 미진행**이다. STEP 07의 CHECK 제약 이름 차이는 스키마 분리 검증 기록을 따른다.
> 이 `practice/phase03/chapter09/README.md`를 먼저 읽고, 기존 Phase 03 회원관리 코드·설정·Git 상태를 확인하라.  
> 로컬 저장소는 `C:\dev\fullstack-web-course`이고, Backend `practice/phase03/backend`, Frontend `practice/phase03/member-next-app`가 있다.  
> 회원관리(1~7강) 구현을 보존하고 `/members`·`/diagnostics`와 충돌하지 않는 별도 상품 실습 경로를 계획하라. 다른 미커밋 Phase 02 작업도 건드리지 마라.  
> 상품 테마는 MATCHA HOUSE로 확정했고, 실제 DB 연결/격리 여부는 STEP 04 이후 확인한다. STEP 03은 사용자 이해 확인 후 PASS로 마쳤다. STEP 04에서 기존 환경의 실제 실행 상태와 미확인 항목을 점검한다. 구현 단계에서는 **코드 → 실행 → Swagger/Network/DB/pytest/Playwright Evidence → PASS** 순서를 지켜라.  
> 사용자에게 긴 대화 내용을 다시 요구하지 말고 이 문서의 데이터 계약을 우선하되, 강의안과 실제 코드에 차이가 있으면 그 차이를 명시하고 검증하라.  
> 이미 구현하지 않은 기능이나 실행하지 않은 테스트를 완료로 표시하지 마라.

### 즉시 시작할 다음 행동

- [x] STEP 01: 상품 조회 → 장바구니 → 주문 → DB 사용자 흐름 학습
- [x] STEP 02: MATCHA HOUSE 테마 및 7종 상품·필수 API 2개·DB 3개·제외 기능 확정
- [x] STEP 03: 기존 회원관리의 Router/Service/Repository 계층 확인, 사용자 이해 확인 후 PASS
- [ ] STEP 04: 전체 개발환경 검증은 보류 (기존 사용자 경로 확인 보고)
- [x] STEP 04 일부: 로컬 git status 및 Backend HTTP 응답 확인
- [x] STEP 05: products 5개 필드·PK·CHECK/DDL 설계; DBeaver 사용자 생성 보고 접수, 실제 구조 미확인
- [x] STEP 06: orders/order_items PK·FK·1:N·주문 가격 스냅샷 설계
- [x] STEP 07: ORM import, DB 실제 타입/PK/FK/CHECK 확인 (CHECK 이름 차이 기록)
- [x] STEP 10: DBeaver와 Backend 연결 대상 확인, ORM 상품 7건 조회
- [x] STEP 11: Product Repository에서 상품 목록 조회 및 실제 DB 결과 비교
- [x] STEP 12: Product Service에서 Repository 호출 및 결과 비교
- [ ] STEP 13: 코드 구현은 완료; 로컬 HTTP 200·7종 응답·Swagger·members 회귀 검증 후 PASS
- [x] 상품 테마 결정: MATCHA HOUSE
- [ ] 실제 구현 폴더/라우트 검토
- [ ] DB/Backend/Frontend에 대한 **변경 전 백업 및 영향 범위 확인**
- [ ] STEP 05 이후에는 Gate마다 사용자에게 실제 검증 결과를 설명

### 진행 기록 (시점별 이력; 최신 진행 상태는 상단 표 참고)

| 일자 | 진행 내용 | 검증 상태 |
| --- | --- | --- |
| 2026-11-12 | Work의 스키마 분리·DB/ORM 비교 및 동일 DB 확인 결과를 최신 상태로 반영 | **STEP 07·10 PASS (Work 증빙 기록)** |
| 2026-11-12 | Product Repository·Service GitHub 반영 및 Work의 상품 7건 조회 검증 확인 | **STEP 11·12 PASS** |
| 2026-11-12 | GET /products Router·Pydantic 응답·main.py 등록 완료, pytest 격리 테스트 5개 및 테스트 의존성 문서 GitHub 반영 | **STEP 13·14 구현 완료 / HTTP·pytest 미실행(HOLD)** |
| 2026-11-12 | STEP 14: 사용자 로컬에서 pytest 상품 API 5개 실행, 5 passed/1 warning/0.75s 결과 전달. 경고는 Starlette TestClient httpx 사용 관련 deprecation | **PASS (로컬 실행 결과)** |
| 2026-11-12 | STEP 15: 기존 Next.js member-next-app 개발 서버/브라우저/Console 확인 시작 | **HOLD (사용자 실행 결과 대기)** |
| 2026-11-12 | 사용자 제공 9강 강의안 기반으로 이 학습 노트 기록 및 GitHub 반영 | **문서만 완료; 구현·실행 전부 HOLD** |
| 2026-11-12 | STEP 01: GET → React 장바구니 State → POST → FastAPI 검증 → PostgreSQL 단일 트랜잭션 흐름 학습 후 사용자 다음 단계 진행 의사 확인 | **학습 PASS (코드/실행 없음)** |
| 2026-11-12 | STEP 02: MATCHA HOUSE 말차 전문 카페, 제품 7종(품절 1종), 필수 UI/장바구니/주문·API 2개·DB 3개·제외 범위와 테스트 기준 확정 | **기획 PASS (Seed/구현/테스트 없음)** |
| 2026-11-12 | STEP 03: 기존 `backend/app/routers/member_router.py`, `services/member_service.py`, `repositories/member_repository.py`에서 요청→Service→DB 조회 흐름을 확인해 설명. 기존 회원 Repository는 commit 수행하나 신규 주문은 Service가 전체 commit/rollback을 관리하는 설계를 적용할 예정 | **개념 학습 PASS (사용자 확인, 코드·실행 없음)** |
| 2026-11-12 | STEP 04: GitHub 설정 점검 후 사용자 보고에서 파일·설치 경로 항목 전부 True 확인. git status 및 HTTP 응답 코드 출력은 받지 못함 | **HOLD (실행·DB 연결 확정 불가)** |
| 2026-11-12 | STEP 05: MATCHA HOUSE products 5필드 및 PK/CHECK 설계. 사용자가 이후 DBeaver에서 기존 회원 DB에 products를 생성했다고 보고했으나 실제 SQL과 제약은 미확인 | **설계 PASS / DB 실재·제약 확인 HOLD** |
| 2026-11-12 | STEP 06: 주문 1:N 상세 및 상품 FK, 주문 당시 단가 스냅샷, orders/order_items 2개 테이블의 PK·CHECK·기본값·DDL 설계 | **설계 PASS / DB 생성 미실행** |
| 2026-11-12 | STEP 07: DBeaver 스크린샷으로 products의 PK/NOT NULL/CHECK와 BIGINT IDENTITY, VARCHAR/INTEGER 타입 확인. 이후 사용자가 DDL 실행 후 products/orders/order_items 3개 테이블 존재 확인 | **테이블 존재 및 products 기본 스키마 확인 / 주문 테이블 제약·ORM 로컬 검증 대기 (HOLD)** |
| 2026-11-12 | STEP 08: DBeaver INSERT RETURNING 스크린샷으로 7종 상품, 원화 정수 가격, 카테고리, 재고(아이스크림 0) 확인 | **PASS (실제 DB INSERT 결과 증빙)** |
| 2026-11-12 | STEP 09: 인계 전 사전 점검에서 기존 FastAPI Swagger 및 회원 API가 정상 동작했다고 사용자가 보고한 사실을 재사용. 설치/서버 점검 반복 생략 | **PASS (사용자 사전점검 보고 기반; 이번 turn 새 HTTP 출력은 아님)** |
| 2026-11-12 | STEP 10: Backend SQLAlchemy Session이 DBeaver와 동일한 PostgreSQL DB에 연결되는지 확인 예정 | **HOLD (DB 식별 결과 대기)** |

---

**최종 완료의 기준:** products/orders/order_items 실재, Seed 상품 6개 이상, GET 200, POST 201, DB 재고 차감과 원자성, pytest PASS, Playwright PASS, Browser/Network 증거 및 SQL 결과가 모두 확인되어야 한다. AI 코드 작성이나 문서만으로는 완료가 아니다.


## STEP 13 — GET /products API 연결 (GitHub 코드 반영, 실행 검증 대기)

- `backend/app/schemas.py`: `ProductResponse` 추가 (id/name/price/category/stock, Pydantic ORM 응답 매핑).
- `backend/app/routers/product_router.py`: GET `/products`가 Product Service를 호출하도록 연결.
- `backend/app/main.py`: 기존 `member_router`는 그대로 보존하고 `product_router`를 추가 등록.
- **현재 미검증:** 로컬 파일 동기화, FastAPI 실행, Swagger `/docs`, `GET /products` HTTP 200·상품 7개 JSON, 기존 `/members` 회귀 테스트. 실제 실행 결과 없이는 PASS로 기록하지 않는다.

**실행 검증 (Windows PowerShell, 기존 미커밋 파일 보존 및 Git 상태 확인 후):**

```powershell
git -C C:\dev\fullstack-web-course status --short
git -C C:\dev\fullstack-web-course log -1 --oneline
# 기존 미커밋 변경을 보존한 뒤 안전하게 최신 main을 동기화한다.
Set-Location C:\dev\fullstack-web-course\practice\phase03\backend
& '..\.venv\Scripts\python.exe' -m uvicorn app.main:app --reload
```

다른 PowerShell에서 실행:

```powershell
$items = Invoke-RestMethod http://127.0.0.1:8000/products
"상품 건수: $(@($items).Count)"
$items | Format-Table id, name, price, category, stock
Invoke-WebRequest http://127.0.0.1:8000/docs -UseBasicParsing | Select-Object StatusCode
Invoke-WebRequest http://127.0.0.1:8000/members -UseBasicParsing | Select-Object StatusCode
```

**STEP 13 PASS 조건:** GET `/products` 200·7종(필드 5개, 품절 stock=0), Swagger 표시, 기존 `/members` 200. **현재 HOLD.**

---

## STEP 14 — pytest 상품 조회 API (사용자 로컬 실행 PASS)

- `backend/tests/test_products_api.py`: `get_db` 의존성을 SQLite 인메모리 DB로 오버라이드하여 기존 PostgreSQL 데이터를 절대 변경하지 않는 5개 테스트.
- 확인 범위: 빈 목록 200/배열, 상품 필드·타입·정렬, 품절상품 재고 0, GET 이후 재고 불변, OpenAPI의 상품 및 회원 경로.
- `backend/requirements-test.txt`: pytest/httpx 테스트용 의존성 별도 명시. **설치/실행은 아직 하지 않았다.**
- SQLite 테스트는 FastAPI→SQLAlchemy 통합을 검증하지만 PostgreSQL 전용 동시성/트랜잭션까지 검증하지는 않는다. 주문 단계에는 별도 테스트용 PostgreSQL 환경이 필요하다.

**실행 검증 (기존 테스트 패키지가 설치된 경우 재설치 불필요):**

```powershell
Set-Location C:\dev\fullstack-web-course\practice\phase03\backend
& '..\.venv\Scripts\python.exe' -m pytest tests/test_products_api.py -q
```

**STEP 14 결과:** 사용자 로컬 PowerShell에서 `5 passed, 1 warning in 0.75s` 확인. 경고는 StarletteDeprecationWarning(`httpx` 관련)이며 테스트 실패가 아니다. 이 테스트는 격리 SQLite DB를 사용하고 운영 PostgreSQL에 연결하지 않도록 의존성을 교체한다. **PASS**.

---

## STEP 15 — 기존 Next.js 개발 서버 확인 (HOLD)

- 기존 `practice/phase03/member-next-app`을 유지하고 새 프로젝트나 패키지 설치를 반복하지 않는다.
- 로컬 Git 미커밋 변경은 보존한다. Next.js가 설치된 기존 로컬 경로에서 `npm run dev`로 구동한다.
- 브라우저 `http://localhost:3000/`, `/members`, `/diagnostics`를 열고 개발자도구 Console 오류 유무를 확인한다. 기존 회원 데이터 삭제·수정 테스트는 하지 않는다.
- **PASS 조건:** Next.js 서버 Ready, 실제 브라우저에서 기존 화면 표시, 콘솔 치명적 오류 없음. 환경 및 페이지 확인 전까지 HOLD.

---

## STEP 11~12 상품 조회 구현 — 2026-11-12

- `backend/app/repositories/product_repository.py`: `find_all(db)`이 `matcha_store.products`를 SQLAlchemy `select(Product)`로 ID 순서대로 조회한다.
- `backend/app/services/product_service.py`: `get_products(db)`가 Repository를 호출해 결과를 전달한다.
- 실제 PostgreSQL 읽기 전용 트랜잭션에서 Repository, Service 및 직접 SQL의 ID·이름·가격·분류·재고를 비교했고 7건이 일치했다.
- STEP 13의 `GET /products` Router는 아직 연결하지 않았다. 기존 회원 API와 DB 데이터는 변경하지 않았다.
