
import { Suspense } from "react";
import MemberDetail from "../../../components/MemberDetail";

export default function MemberDetailPage() {
  return (
    <main
      style={{
        width: "100%",
        maxWidth: 1200,
        margin: "0 auto",
        padding: "32px 24px 80px",
      }}
    >
      <Suspense
        fallback={
          <p role="status">
            회원 상세 정보를 불러오는 중입니다...
          </p>
        }
      >
        <MemberDetail />
      </Suspense>
    </main>
  );
}
