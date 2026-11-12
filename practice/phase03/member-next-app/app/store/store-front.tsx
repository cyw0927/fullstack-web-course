"use client";

import Image from "next/image";
import Link from "next/link";
import { useEffect, useState } from "react";
import styles from "./store.module.css";

type Product = {
  id: number;
  name: string;
  price: number;
  category: string;
  stock: number;
};

type ProductState =
  | { status: "loading" }
  | { status: "error"; message: string }
  | { status: "success"; products: Product[] };

async function getProducts(signal: AbortSignal): Promise<Product[]> {
  const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL;
  if (!baseUrl) throw new Error("상품 API 주소가 설정되지 않았습니다.");
  const response = await fetch(`${baseUrl.replace(/\/$/, "")}/products`, { signal, cache: "no-store" });
  if (!response.ok) throw new Error(`상품을 불러오지 못했습니다. (HTTP ${response.status})`);
  const data: unknown = await response.json();
  if (!Array.isArray(data)) throw new Error("상품 목록 응답을 확인할 수 없습니다.");
  return data.map((item: unknown) => {
    if (typeof item !== "object" || item === null) throw new Error("상품 정보 형식이 올바르지 않습니다.");
    const product = item as Record<string, unknown>;
    if (!Number.isInteger(product.id) || typeof product.name !== "string" ||
        !Number.isInteger(product.price) || typeof product.category !== "string" ||
        !Number.isInteger(product.stock) || (product.price as number) < 0 || (product.stock as number) < 0) {
      throw new Error("상품 정보 형식이 올바르지 않습니다.");
    }
    return { id: product.id as number, name: product.name, price: product.price as number, category: product.category, stock: product.stock as number };
  });
}

export default function StoreFront() {
  const [state, setState] = useState<ProductState>({ status: "loading" });
  const [requestKey, setRequestKey] = useState(0);

  useEffect(() => {
    const controller = new AbortController();
    getProducts(controller.signal)
      .then((products) => { if (!controller.signal.aborted) setState({ status: "success", products }); })
      .catch((error: unknown) => {
        if (!controller.signal.aborted) setState({ status: "error", message: error instanceof Error ? error.message : "알 수 없는 오류가 발생했습니다." });
      });
    return () => controller.abort();
  }, [requestKey]);

  function retry() {
    setState({ status: "loading" });
    setRequestKey((key) => key + 1);
  }

  return (
    <main className={styles.store}>
      <header className={styles.header}>
        <Link href="/store" className={styles.brand} aria-label="MATCHA HOUSE 홈">
          <span className={styles.brandMark} aria-hidden="true">✳</span>
          <span>MATCHA HOUSE<small>THE MATCHA POP-UP</small></span>
        </Link>
        <nav className={styles.nav} aria-label="주 메뉴">
          <a href="#about">ABOUT</a><a href="#menu">MENU</a><Link href="/members">MEMBERS</Link>
        </nav>
        <a href="#menu" className={styles.headerLink}>메뉴 둘러보기 <span aria-hidden="true">↗</span></a>
      </header>

      <section className={styles.hero} id="about">
        <div className={styles.heroCopy}>
          <p className={styles.kicker}><span /> A LITTLE MOMENT OF CALM</p>
          <h1 className={styles.heroTitle}>A little more<br /><em>matcha,</em><br />a little more you.</h1>
          <p className={styles.heroDescription}>바쁜 하루 속, 잠시 나를 위한 시간.<br />한 잔의 말차와 함께 천천히 쉬어가세요.</p>
          <a className={styles.heroButton} href="#menu">우리의 메뉴 보기 <span aria-hidden="true">↗</span></a>
          <div className={styles.heroNote}><span>01 / 03</span><span className={styles.noteLine} /><span>MADE WITH CARE</span></div>
        </div>
        <div className={styles.heroVisual}>
          <Image src="/matcha-hero.png" alt="말차가 담긴 도자기 찻사발과 대나무 차선" fill priority sizes="(max-width: 760px) 100vw, 50vw" className={styles.heroImage} />
          <div className={styles.imageLabel}><span>丁寧なひととき</span><strong>THE ART OF<br />SLOWING DOWN</strong></div>
          <div className={styles.imageCaption}>A quiet ritual, made just for you. <span>— MATCHA HOUSE</span></div>
        </div>
      </section>

      <div className={styles.values} aria-label="브랜드 소개">
        <span>GOOD MATCHA, GOOD MOMENTS</span><span className={styles.valueStar}>✳</span>
        <span>MADE WITH CARE</span><span className={styles.valueStar}>✳</span>
        <span>A LITTLE EVERYDAY RITUAL</span>
      </div>

      <section className={styles.menuSection} id="menu" aria-labelledby="menu-title">
        <div className={styles.sectionHead}>
          <div><p className={styles.sectionKicker}>OUR LITTLE MENU <span>— 01</span></p><h2 id="menu-title">좋은 말차, <em>좋은 시간.</em></h2><p>마음을 담아 준비한 말차 음료와 디저트를 만나보세요.</p></div>
          <div className={styles.menuAside}><span>THE MATCHA COLLECTION</span><strong>Small moments,<br />beautifully made.</strong></div>
        </div>
        {state.status === "loading" && <div className={styles.state} role="status">정성껏 준비한 메뉴를 불러오고 있어요.</div>}
        {state.status === "error" && <div className={styles.state} role="alert"><strong>메뉴를 불러오지 못했어요.</strong><p>{state.message}</p><button type="button" className={styles.retry} onClick={retry}>다시 시도하기 ↻</button></div>}
        {state.status === "success" && state.products.length === 0 && <div className={styles.state}>지금은 준비된 메뉴가 없어요. 잠시 후 다시 찾아주세요.</div>}
        {state.status === "success" && state.products.length > 0 && <>
          <div className={styles.menuMeta}><span>ALL MENU <b>{String(state.products.length).padStart(2, "0")}</b></span><span>오늘의 메뉴를 소개합니다</span></div>
          <ul className={styles.grid}>
            {state.products.map((product, index) => {
              const soldOut = product.stock === 0;
              const dessert = product.category === "디저트";
              return <li className={styles.product} key={product.id}>
                <div className={`${styles.productVisual} ${dessert ? styles.dessertVisual : styles.drinkVisual}`}>
                  <span className={styles.productIndex}>0{index + 1} / MATCHA HOUSE</span>
                  {soldOut && <span className={styles.soldOutBadge}>SOLD OUT · 품절</span>}
                  <div className={`${styles.artwork} ${dessert ? styles.dessertArt : styles.drinkArt}`} aria-hidden="true"><span /><i /></div>
                  <span className={styles.artCaption}>{dessert ? "A LITTLE SWEETNESS" : "A MOMENT FOR YOU"}</span>
                </div>
                <div className={styles.productBody}>
                  <p className={styles.category}>{product.category} · {product.category === "음료" ? "MATCHA DRINK" : product.category === "디저트" ? "MATCHA DESSERT" : "MATCHA HOUSE"}</p>
                  <h3>{product.name}</h3>
                  <div className={styles.productBottom}><strong>{product.price.toLocaleString("ko-KR")}원</strong><span>{soldOut ? "재고 없음" : `남은 수량 ${product.stock}개`}</span></div>
                  <button className={styles.productButton} type="button" disabled aria-label={`${product.name} ${soldOut ? "품절" : "담기 준비 중"}`}>{soldOut ? "품절" : "담기 준비 중"}</button>
                </div>
              </li>;
            })}
          </ul>
          <p className={styles.cartNote}>장바구니와 주문 기능은 다음 실습에서 준비할게요.</p>
        </>}
      </section>

      <section className={styles.closing}><span>✳</span><p>TAKE A MOMENT FOR YOURSELF</p><h2>일상에 작은 쉼을 더해요.</h2><a href="#about">처음으로 돌아가기 ↑</a></section>
      <footer className={styles.footer}><div><strong>MATCHA HOUSE</strong><p>Little moments, made with matcha.</p></div><div className={styles.footerLinks}><Link href="/members">회원 관리</Link><Link href="/diagnostics">API 진단</Link><span>© MATCHA HOUSE</span></div></footer>
    </main>
  );
}
