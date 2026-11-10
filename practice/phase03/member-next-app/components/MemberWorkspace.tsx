
"use client";

import { useState } from "react";
import type { FormEvent } from "react";
import MemberList from "./MemberList";
import type { Member } from "../types/member";

type MemberWorkspaceProps = {
  initialMembers: Member[];
};

export default function MemberWorkspace({
  initialMembers,
}: MemberWorkspaceProps) {
  const [search, setSearch] = useState("");
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [age, setAge] = useState("");

  const filteredMembers = initialMembers.filter((member) => {
    const keyword = search.trim().toLowerCase();

    return (
      member.name.toLowerCase().includes(keyword) ||
      member.email.toLowerCase().includes(keyword)
    );
  });

  const ageNumber = Number(age);
  const validAge =
    age.trim() !== "" &&
    Number.isInteger(ageNumber) &&
    ageNumber >= 0 &&
    ageNumber <= 150;

  function handlePreview(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!name.trim() || !email.trim() || !validAge) {
      return;
    }

    // 3강: API 요청/DB 저장은 하지 않습니다.
  }

  return (
    <div>
      <section style={{ marginTop: 28 }}>
        <label
          htmlFor="member-search"
          style={{ display: "block", marginBottom: 8 }}
        >
          회원 검색 (이름 또는 이메일)
        </label>

        <input
          id="member-search"
          value={search}
          onChange={(event) => setSearch(event.target.value)}
          placeholder="예: kim"
          style={{
            width: "min(100%, 360px)",
            padding: 10,
            border: "1px solid #94a3b8",
            borderRadius: 8,
          }}
        />

        <button
          type="button"
          onClick={() => setSearch("")}
          style={{
            marginLeft: 8,
            padding: "10px 14px",
            cursor: "pointer",
          }}
        >
          초기화
        </button>
      </section>

      <MemberList members={filteredMembers} />

      <section
        style={{
          marginTop: 36,
          padding: 20,
          border: "1px solid #cbd5e1",
          borderRadius: 12,
        }}
      >
        <h2 style={{ marginTop: 0 }}>
          회원 등록 연습 (미리보기)
        </h2>

        <p style={{ color: "#64748b" }}>
          아직 저장 기능이 없습니다. 입력값만 확인합니다.
        </p>

        <form onSubmit={handlePreview}>
          <label htmlFor="member-name">이름</label>
          <input
            id="member-name"
            value={name}
            onChange={(event) => setName(event.target.value)}
            placeholder="Hong"
            required
            style={{
              display: "block",
              padding: 10,
              margin: "6px 0 16px",
              width: "min(100%, 360px)",
            }}
          />

          <label htmlFor="member-email">이메일</label>
          <input
            id="member-email"
            type="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            placeholder="hong@example.com"
            required
            style={{
              display: "block",
              padding: 10,
              margin: "6px 0 16px",
              width: "min(100%, 360px)",
            }}
          />

          <label htmlFor="member-age">나이</label>
          <input
            id="member-age"
            type="number"
            min={0}
            max={150}
            value={age}
            onChange={(event) => setAge(event.target.value)}
            placeholder="25"
            required
            style={{
              display: "block",
              padding: 10,
              margin: "6px 0 16px",
              width: "min(100%, 360px)",
            }}
          />

          <button
            type="submit"
            disabled={!name.trim() || !email.trim() || !validAge}
            style={{ padding: "10px 14px" }}
          >
            입력값 확인
          </button>
        </form>

        <p role="status" style={{ marginTop: 20 }}>
          <strong>현재 입력값:</strong>{" "}
          {name.trim() || "(이름 없음)"} /{" "}
          {email.trim() || "(이메일 없음)"} /{" "}
          {validAge
            ? ageNumber + "세"
            : "(나이 미입력 또는 범위 오류)"}
        </p>

        <p style={{ color: "#b45309", fontWeight: 600 }}>
          학습용 미리보기이며 저장되지 않습니다.
        </p>
      </section>
    </div>
  );
}
