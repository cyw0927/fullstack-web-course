
import type { Member } from "../types/member";

type MemberCardProps = {
  member: Member;
};

export default function MemberCard({ member }: MemberCardProps) {
  return (
    <li
      style={{
        listStyle: "none",
        backgroundColor: "#ffffff",
        border: "1px solid #cbd5e1",
        borderRadius: 12,
        padding: 20,
      }}
    >
      <h3 style={{ color: "#0f172a", margin: "0 0 8px" }}>
        {member.name}
      </h3>

      <p style={{ color: "#334155", margin: "0 0 8px" }}>
        {member.email}
      </p>

      <p style={{ color: "#64748b", margin: 0 }}>
        나이 {member.age}세 · ID {member.member_id}
      </p>
    </li>
  );
}
