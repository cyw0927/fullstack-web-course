
import MemberWorkspace from "../components/MemberWorkspace";
export default function HomePage() {
  return (
    <main
      style={{
        maxWidth: 880,
        margin: "48px auto",
        padding: "0 24px",
        fontFamily: "Arial, sans-serif",
      }}
    >
      <p style={{ color: "#2563eb", fontWeight: 700 }}>
        Phase 03 · 04강 FastAPI 회원 목록 연동
      </p>

      <h1 style={{ fontSize: 36, color: "#0f172a" }}>
        회원관리 시스템
      </h1>

      <p style={{ color: "#475569" }}>
        이제 샘플 배열 대신 FastAPI의 회원 데이터를 조회합니다.
      </p>

      <MemberWorkspace />
    </main>
  );
}
