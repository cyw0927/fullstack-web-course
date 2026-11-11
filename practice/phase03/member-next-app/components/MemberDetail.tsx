
"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";

import { getMember } from "../lib/members-api";
import type { Member } from "../types/member";

export default function MemberDetail() {
  const params = useParams<{ memberId: string }>();

  const memberIdText = params.memberId;
  const memberId = Number(memberIdText);

  // 올바른 회원 ID인지 검사
  const validId =
    /^\d+$/.test(memberIdText) &&
    Number.isSafeInteger(memberId) &&
    memberId > 0;

  const [member, setMember] = useState<Member | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // 회원 상세 정보 조회
  useEffect(() => {
    if (!validId) return;

    const controller = new AbortController();

    async function loadMember() {
      setLoading(true);
      setError("");
      setMember(null);

      try {
        const data = await getMember(
          memberId,
          controller.signal
        );

        if (!controller.signal.aborted) {
          setMember(data);
        }
      } catch (caught) {
        if (!controller.signal.aborted) {
          setError(
            caught instanceof Error
              ? caught.message
              : "회원 상세 조회 오류"
          );
        }
      } finally {
        if (!controller.signal.aborted) {
          setLoading(false);
        }
      }
    }

    void loadMember();

    return () => controller.abort();
  }, [memberId, validId]);

  // 성별 코드를 한글로 변환
  const genderLabel =
    member?.gender === "M"
      ? "남성"
      : member?.gender === "F"
        ? "여성"
        : "미지정";

  return (
    <section>
      <p
        style={{
          color: "#2563eb",
          fontWeight: 700,
        }}
      >
        PHASE 03 · MEMBER DETAILS
      </p>

      <h1
        style={{
          color: "#0f172a",
          fontSize: 32,
        }}
      >
        회원 상세 정보
      </h1>

      <p>
        <Link href="/members">
          ← 회원 목록으로 돌아가기
        </Link>
      </p>

      {!validId ? (
        <p role="alert">
          올바른 회원 ID를 입력해 주세요.
        </p>
      ) : loading ? (
        <p role="status">
          회원 정보를 불러오는 중입니다...
        </p>
      ) : error ? (
        <p
          role="alert"
          style={{ color: "#b91c1c" }}
        >
          조회 오류: {error}
        </p>
      ) : member ? (
        <div
          style={{
            backgroundColor: "#ffffff",
            border: "1px solid #cbd5e1",
            borderRadius: 16,
            padding: 28,
            marginTop: 24,
          }}
        >
          <p style={{ color: "#64748b" }}>
            회원 번호 #{member.member_id}
          </p>

          <h2
            style={{
              color: "#0f172a",
              fontSize: 26,
            }}
          >
            {member.name}
          </h2>

          <p>
            <strong>이메일:</strong>{" "}
            {member.email}
          </p>

          <p>
            <strong>나이:</strong>{" "}
            {member.age}세
          </p>

          {/* 이번 실습에서 추가한 성별 */}
          <p>
            <strong>성별:</strong>{" "}
            {genderLabel}
          </p>
        </div>
      ) : (
        <p role="alert">
          회원 정보를 찾을 수 없습니다.
        </p>
      )}
    </section>
  );
}
