
"use client";

import Image from "next/image";
import Link from "next/link";
import { useEffect, useState } from "react";

import ProductCard from "../../components/ProductCard";
import type { Product } from "../../types/products";

import styles from "./store.module.css";

// 상품 목록의 로딩, 오류, 성공 상태
type ProductState =
  | { status: "loading" }
  | { status: "error"; message: string }
  | { status: "success"; products: Product[] };

// FastAPI에서 상품 데이터 가져오기
async function getProducts(
  signal: AbortSignal
): Promise<Product[]> {
  const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL;

  if (!baseUrl) {
    throw new Error("상품 API 주소가 설정되지 않았습니다.");
  }

  const response = await fetch(
    `${baseUrl.replace(/\/$/, "")}/products`,
    {
      signal,
      cache: "no-store",
    }
  );

  if (!response.ok) {
    throw new Error(
      `상품을 불러오지 못했습니다. (HTTP ${response.status})`
    );
  }

  const data: unknown = await response.json();

  if (!Array.isArray(data)) {
    throw new Error("상품 목록 응답을 확인할 수 없습니다.");
  }

  // 서버에서 받은 데이터 구조 검사
  return data.map((item: unknown) => {
    if (typeof item !== "object" || item === null) {
      throw new Error("상품 정보 형식이 올바르지 않습니다.");
    }

    const product = item as Record<string, unknown>;

    if (
      !Number.isInteger(product.id) ||
      typeof product.name !== "string" ||
      !Number.isInteger(product.price) ||
      typeof product.category !== "string" ||
      !Number.isInteger(product.stock) ||
      (product.price as number) < 0 ||
      (product.stock as number) < 0
    ) {
      throw new Error("상품 정보 형식이 올바르지 않습니다.");
    }

    return {
      id: product.id as number,
      name: product.name,
      price: product.price as number,
      category: product.category,
      stock: product.stock as number,
    };
  });
}

// MATCHA HOUSE 메인 화면
export default function StoreFront() {
  const [state, setState] = useState<ProductState>({
    status: "loading",
  });

  const [requestKey, setRequestKey] = useState(0);

  // 처음 페이지를 열면 상품 목록 불러오기
  useEffect(() => {
    const controller = new AbortController();

    getProducts(controller.signal)
      .then((products) => {
        if (!controller.signal.aborted) {
          setState({
            status: "success",
            products,
          });
        }
      })
      .catch((error: unknown) => {
        if (!controller.signal.aborted) {
          setState({
            status: "error",
            message:
              error instanceof Error
                ? error.message
                : "알 수 없는 오류가 발생했습니다.",
          });
        }
      });

    return () => controller.abort();
  }, [requestKey]);

  // 상품 조회 실패 시 다시 요청
  function retry() {
    setState({ status: "loading" });
    setRequestKey((key) => key + 1);
  }

  return (
    <main className={styles.store}>
      {/* 상단 메뉴 */}
      <header className={styles.header}>
        <Link
          href="/store"
          className={styles.brand}
          aria-label="MATCHA HOUSE 홈"
        >
          <span
            className={styles.brandMark}
            aria-hidden="true"
          >
            ✳
          </span>

          <span>
            MATCHA HOUSE
            <small>THE MATCHA POP-UP</small>
          </span>
        </Link>

        <nav className={styles.nav} aria-label="주 메뉴">
          <a href="#about">ABOUT</a>
          <a href="#menu">MENU</a>
          <Link href="/members">MEMBERS</Link>
        </nav>

        <a href="#menu" className={styles.headerLink}>
          메뉴 둘러보기
          <span aria-hidden="true">↗</span>
        </a>
      </header>

      {/* 메인 브랜드 소개 */}
      <section className={styles.hero} id="about">
        <div className={styles.heroCopy}>
          <p className={styles.kicker}>
            <span />
            A LITTLE MOMENT OF CALM
          </p>

          <h1 className={styles.heroTitle}>
            A little more
            <br />
            <em>matcha,</em>
            <br />
            a little more you.
          </h1>

          <p className={styles.heroDescription}>
            바쁜 하루 속, 잠시 나를 위한 시간.
            <br />
            한 잔의 말차와 함께 천천히 쉬어가세요.
          </p>

          <a href="#menu" className={styles.heroButton}>
            우리의 메뉴 보기
            <span aria-hidden="true">↗</span>
          </a>

          <div className={styles.heroNote}>
            <span>01 / 03</span>
            <span className={styles.noteLine} />
            <span>MADE WITH CARE</span>
          </div>
        </div>

        <div className={styles.heroVisual}>
          <Image
            src="/matcha-hero.png"
            alt="말차가 담긴 도자기 찻사발과 대나무 차선"
            fill
            priority
            sizes="(max-width: 760px) 100vw, 50vw"
            className={styles.heroImage}
          />

          <div className={styles.imageLabel}>
            <span>丁寧なひととき</span>
            <strong>
              THE ART OF
              <br />
              SLOWING DOWN
            </strong>
          </div>

          <div className={styles.imageCaption}>
            A quiet ritual, made just for you.
            <span>— MATCHA HOUSE</span>
          </div>
        </div>
      </section>

      {/* 브랜드 문구 */}
      <div
        className={styles.values}
        aria-label="브랜드 소개"
      >
        <span>GOOD MATCHA, GOOD MOMENTS</span>

        <span className={styles.valueStar}>✳</span>

        <span>MADE WITH CARE</span>

        <span className={styles.valueStar}>✳</span>

        <span>A LITTLE EVERYDAY RITUAL</span>
      </div>

      {/* 상품 메뉴 */}
      <section
        className={styles.menuSection}
        id="menu"
        aria-labelledby="menu-title"
      >
        <div className={styles.sectionHead}>
          <div>
            <p className={styles.sectionKicker}>
              OUR LITTLE MENU <span>— 01</span>
            </p>

            <h2 id="menu-title">
              좋은 말차, <em>좋은 시간.</em>
            </h2>

            <p>
              마음을 담아 준비한 말차 음료와 디저트를
              만나보세요.
            </p>
          </div>

          <div className={styles.menuAside}>
            <span>THE MATCHA COLLECTION</span>

            <strong>
              Small moments,
              <br />
              beautifully made.
            </strong>
          </div>
        </div>

        {/* 상품 로딩 */}
        {state.status === "loading" && (
          <div className={styles.state} role="status">
            정성껏 준비한 메뉴를 불러오고 있어요.
          </div>
        )}

        {/* 상품 조회 오류 */}
        {state.status === "error" && (
          <div className={styles.state} role="alert">
            <strong>메뉴를 불러오지 못했어요.</strong>

            <p>{state.message}</p>

            <button
              type="button"
              className={styles.retry}
              onClick={retry}
            >
              다시 시도하기 ↻
            </button>
          </div>
        )}

        {/* 상품이 없는 경우 */}
        {state.status === "success" &&
          state.products.length === 0 && (
            <div className={styles.state}>
              지금은 준비된 메뉴가 없어요.
              잠시 후 다시 찾아주세요.
            </div>
          )}

        {/* 상품 목록 표시 */}
        {state.status === "success" &&
          state.products.length > 0 && (
            <>
              <div className={styles.menuMeta}>
                <span>
                  ALL MENU{" "}
                  <b>
                    {String(
                      state.products.length
                    ).padStart(2, "0")}
                  </b>
                </span>

                <span>오늘의 메뉴를 소개합니다</span>
              </div>

              {/* STEP 16: 별도의 ProductCard 사용 */}
              <ul className={styles.grid}>
                {state.products.map((product, index) => (
                  <ProductCard
                    key={product.id}
                    product={product}
                    index={index}
                  />
                ))}
              </ul>

              <p className={styles.cartNote}>
                장바구니와 주문 기능은 다음 실습에서
                준비할게요.
              </p>
            </>
          )}
      </section>

      {/* 하단 브랜드 문구 */}
      <section className={styles.closing}>
        <span>✳</span>

        <p>TAKE A MOMENT FOR YOURSELF</p>

        <h2>일상에 작은 쉼을 더해요.</h2>

        <a href="#about">
          처음으로 돌아가기 ↑
        </a>
      </section>

      {/* 푸터 */}
      <footer className={styles.footer}>
        <div>
          <strong>MATCHA HOUSE</strong>

          <p>Little moments, made with matcha.</p>
        </div>

        <div className={styles.footerLinks}>
          <Link href="/members">회원 관리</Link>

          <Link href="/diagnostics">API 진단</Link>

          <span>© MATCHA HOUSE</span>
        </div>
      </footer>
    </main>
  );
}
