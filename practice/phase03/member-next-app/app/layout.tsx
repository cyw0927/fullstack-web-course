import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "회원관리 시스템 | Phase 03",
  description: "React, Next.js, TypeScript로 만드는 회원관리 실습",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="ko">
      <body>{children}</body>
    </html>
  );
}