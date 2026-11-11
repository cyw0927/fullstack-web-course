
import Link from "next/link";
import type { Member } from "../types/member";

type MemberCardProps = {
  member: Member;
  onEdit: (member: Member) => void;
  onDelete: (member: Member) => void;
  busy: boolean;
};

export default function MemberCard({
  member,
  onEdit,
  onDelete,
  busy,
}: MemberCardProps) {
  // 성별 코드를 화면에 표시할 한글로 변환
  const genderLabel =
    member.gender === "M"
      ? "남성"
      : member.gender === "F"
        ? "여성"
        : "미지정";

  return (
    <li className="member-row">
      {/* 기존 프로필 디자인 유지 */}
      <span className="member-avatar" aria-hidden="true">
        {member.name.slice(0, 1)}
      </span>

      {/* 회원 정보 */}
      <div className="member-info">
        <h3>{member.name}</h3>

        <p className="member-email">
          {member.email}
        </p>

        <p className="member-meta">
          <span>ID {member.member_id}</span>
          <span aria-hidden="true">·</span>
          <span>{member.age}세</span>
          <span aria-hidden="true">·</span>

          {/* 이번 실습에서 추가한 성별 표시 */}
          <span>{genderLabel}</span>
        </p>
      </div>

      {/* 기존 상세·수정·삭제 기능 유지 */}
      <div className="member-actions">
        <Link
          href={`/members/${member.member_id}`}
          className="btn btn-small btn-secondary"
          style={{
            display: "inline-flex",
            alignItems: "center",
            justifyContent: "center",
            textDecoration: "none",
          }}
          aria-label={`${member.name} 회원 상세 보기`}
        >
          상세 보기
        </Link>

        <button
          className="btn btn-small btn-secondary"
          type="button"
          disabled={busy}
          onClick={() => onEdit(member)}
          aria-label={`${member.name} 회원 수정`}
        >
          수정
        </button>

        <button
          className="btn btn-small btn-danger"
          type="button"
          disabled={busy}
          onClick={() => onDelete(member)}
          aria-label={`${member.name} 회원 삭제`}
        >
          삭제
        </button>
      </div>
    </li>
  );
}
