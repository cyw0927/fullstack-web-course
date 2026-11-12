
import type { Product } from "../types/products";
import styles from "../app/store/store.module.css";

type ProductCardProps = {
  product: Product;
  index: number;
  onAdd?: (product: Product) => void;
};

export default function ProductCard({
  product,
  index,
  onAdd,
}: ProductCardProps) {
  const soldOut = product.stock === 0;
  const dessert = product.category === "디저트";
  const canAdd = !soldOut && Boolean(onAdd);

  const categoryLabel =
    product.category === "음료"
      ? "MATCHA DRINK"
      : dessert
        ? "MATCHA DESSERT"
        : "MATCHA HOUSE";

  return (
    <li className={styles.product}>
      <div
        className={`${styles.productVisual} ${
          dessert ? styles.dessertVisual : styles.drinkVisual
        }`}
      >
        <span className={styles.productIndex}>
          {String(index + 1).padStart(2, "0")} / MATCHA HOUSE
        </span>

        {soldOut && (
          <span className={styles.soldOutBadge}>
            SOLD OUT · 품절
          </span>
        )}

        <div
          className={`${styles.artwork} ${
            dessert ? styles.dessertArt : styles.drinkArt
          }`}
          aria-hidden="true"
        >
          <span />
          <i />
        </div>

        <span className={styles.artCaption}>
          {dessert
            ? "A LITTLE SWEETNESS"
            : "A MOMENT FOR YOU"}
        </span>
      </div>

      <div className={styles.productBody}>
        <p className={styles.category}>
          {product.category} · {categoryLabel}
        </p>

        <h3>{product.name}</h3>

        <div className={styles.productBottom}>
          <strong>
            {product.price.toLocaleString("ko-KR")}원
          </strong>
          <span>
            {soldOut
              ? "재고 없음"
              : `남은 수량 ${product.stock}개`}
          </span>
        </div>

        <button
          className={styles.productButton}
          type="button"
          disabled={!canAdd}
          onClick={() => onAdd?.(product)}
        >
          {soldOut
            ? "품절"
            : canAdd
              ? "장바구니 담기"
              : "담기 준비 중"}
        </button>
      </div>
    </li>
  );
}
