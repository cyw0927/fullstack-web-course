
import type { Member } from "../types/member";
import MemberCard from "./MemberCard";

type MemberListProps = {
  members: Member[];
};

export default function MemberList({ members }: MemberListProps) {
  return (
    <section aria-labelledby="member-list-title" style={{ marginTop: 32 }}>
      <h2 id="member-list-title" style={{ fontSize: 24, color: "#0f172a" }}>
        회원 목록 ({members.length}명)
      </h2>

      {members.length === 0 ? (
        <p style={{ color: "#64748b" }}>등록된 회원이 없습니다.</p>
      ) : (
        <ul style={{ display: "grid", gap: 12, padding: 0 }}>
          {members.map((member) => (
            <MemberCard key={member.member_id} member={member} />
          ))}
        </ul>
      )}
    </section>
  );
}
