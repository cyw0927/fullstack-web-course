
import MemberWorkspace from "../components/MemberWorkspace";
import type { Member } from "../types/member";

const sampleMembers: Member[] = [
  { member_id: 1, name: "Kim", email: "kim@example.com", age: 30 },
  { member_id: 2, name: "Lee", email: "lee@example.com", age: 27 },
  { member_id: 3, name: "Park", email: "park@example.com", age: 35 },
];

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
        Phase 03 · 03강 Props · State · Event
      </p>

      <h1 style={{ fontSize: 36, color: "#0f172a" }}>
        회원관리 시스템
      </h1>

      <p style={{ color: "#475569" }}>
        React State로 회원 검색과 입력 폼을 실습합니다.
        실제 API 조회는 4강, DB 저장은 5강에서 진행합니다.
      </p>

      <MemberWorkspace initialMembers={sampleMembers} />
    </main>
  );
}
