import type { Member } from "../types/member";
import MemberCard from "./MemberCard";

type MemberListProps = {
  members: Member[];
  onEdit: (member: Member) => void;
  onDelete: (member: Member) => void;
  busy: boolean;
};

export default function MemberList({ members, onEdit, onDelete, busy }: MemberListProps) {
  return members.length === 0 ? (
    <p className="state-message">표시할 회원이 없습니다.</p>
  ) : (
    <ul className="member-list" aria-label="회원 목록">
      {members.map((member) => (
        <MemberCard key={member.member_id} member={member} onEdit={onEdit} onDelete={onDelete} busy={busy} />
      ))}
    </ul>
  );
}
