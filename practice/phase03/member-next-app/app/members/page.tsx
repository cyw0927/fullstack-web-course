
import Link from "next/link";
import MemberWorkspace from "../../components/MemberWorkspace";

export default function MembersPage() {
  return (
    <main
      style={{
        width: "100%",
        maxWidth: 1200,
        margin: "0 auto",
        padding: "32px 24px 80px",
      }}
    >
      <header style={{ marginBottom: 32 }}>
        <p
          style={{
            color: "#2563eb",
            fontSize: 13,
            fontWeight: 700,
          }}
        >
          PHASE 03 · LESSON 06
        </p>

        <h1
          style={{
            fontSize: 36,
            color: "#0f172a",
            marginBottom: 12,
          }}
        >
          회원 목록
        </h1>

        <p style={{ color: "#64748b" }}>
          회원을 검색하고 상세 정보를 확인할 수 있습니다.
        </p>

        <p>
          <Link href="/">← 메인 화면으로 돌아가기</Link>
        </p>
      </header>

      {/* 기존 CRUD 및 성별 기능을 그대로 사용 */}
      <MemberWorkspace />
    </main>
  );
}
