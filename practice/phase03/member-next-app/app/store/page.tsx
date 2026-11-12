import type { Metadata } from "next";
import StoreFront from "./store-front";

export const metadata: Metadata = {
  title: "MATCHA HOUSE | 작은 쉼, 한 잔의 말차",
  description: "정성스러운 말차 음료와 디저트를 만나는 작은 팝업 카페",
};

export default function StorePage() {
  return <StoreFront />;
}
