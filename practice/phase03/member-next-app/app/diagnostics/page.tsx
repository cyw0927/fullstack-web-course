"use client";

import { useEffect, useRef, useState } from "react";
import Link from "next/link";

import { getMembers } from "../../lib/members-api";
import type { Member } from "../../types/member";

type CheckStatus = "idle" | "loading" | "success" | "empty" | "error";

// 7강: 실제 GET 요청과 Loading / Empty / Error를 구분하는 읽기 전용 진단 페이지
export default function DiagnosticsPage() {
  const [status, setStatus] = useState<CheckStatus>("idle");
  const [members, setMembers] = useState<Member[]>([]);
  const [error, setError] = useState("");
  const [showEmptyExample, setShowEmptyExample] = useState(false);
  const controllerRef = useRef<AbortController | null>(null);

  // 페이지 이동 시 실행 중인 요청 취소
  useEffect(() => {
    return () => {
      controllerRef.current?.abort();
    };
  }, []);

  async function runCheck() {
    // 새 요청 전에 이전 요청 취소
    controllerRef.current?.abort();
    const controller = new AbortController();
    controllerRef.current = controller;

    setStatus("loading");
    setError("");
    setMembers([]);

    try {
      // 기존 API 함수를 재사용하며 회원 정보를 변경하지 않음
      const result = await getMembers(controller.signal);
      if (controller.signal.aborted) return;

      setMembers(result);
      setStatus(result.length === 0 ? "empty" : "success");
    } catch (caught) {
      if (controller.signal.aborted) return;

      setStatus("error");
      setError(
        caught instanceof Error
          ? caught.message
          : "알 수 없는 네트워크 오류",
      );
    }
  }

  return (
    <main
      style={{
        maxWidth: 880,
        margin: "48px auto",
        padding: "0 24px 64px",
      }}
    >
      <p style={{ color: "#2563eb", fontWeight: 700 }}>
        PHASE 03 · LESSON 07
      </p>
      <h1>회원관리 API 진단</h1>
      <p>
        실제 회원 목록 GET 요청의 결과를 확인합니다.
        등록·수정·삭제 요청이나 DB 변경은 하지 않습니다.
      </p>
      <p>
        <Link href="/members">← 회원 목록으로 돌아가기</Link>
      </p>

      <button
        className="btn btn-primary"
        type="button"
        onClick={() => {
          void runCheck();
        }}
        disabled={status === "loading"}
        style={{ marginTop: 12 }}
      >
        {status === "loading" ? "조회 중..." : "실제 회원 목록 GET 검사"}
      </button>

      <section
        aria-live="polite"
        aria-labelledby="diagnostics-result-title"
        style={{
          marginTop: 24,
          border: "1px solid #cbd5e1",
          borderRadius: 12,
          padding: 20,
        }}
      >
        <h2 id="diagnostics-result-title" style={{ marginTop: 0 }}>
          실제 API 검사 결과
        </h2>

        {status === "idle" && (
          <p>아직 요청하지 않았습니다. 위 버튼을 눌러 검사하세요.</p>
        )}

        {status === "loading" && (
          <p role="status">회원 목록을 불러오는 중입니다...</p>
        )}

        {status === "empty" && (
          <p role="status">
            조회 성공: 회원 0명. 빈 목록은 정상 응답입니다.
          </p>
        )}

        {status === "success" && (
          <div role="status">
            <p>조회 성공: 회원 {members.length}명</p>
            <p>회원 ID: {members.map((member) => member.member_id).join(", ")}</p>
          </div>
        )}

        {status === "error" && (
          <div role="alert" style={{ color: "#b91c1c" }}>
            <p>회원 목록 조회에 실패했습니다.</p>
            <p>{error}</p>
            <p>F12 → Network / Console에서 요청 URL, 상태 및 CORS 메시지를 확인하세요.</p>
          </div>
        )}
      </section>

      <section style={{ marginTop: 32 }}>
        <h2>Empty 화면 연습 (서버와 무관한 예시)</h2>
        <button
          className="btn btn-secondary"
          type="button"
          onClick={() => setShowEmptyExample((value) => !value)}
        >
          {showEmptyExample ? "예시 숨기기" : "빈 목록 예시 보기"}
        </button>
        {showEmptyExample && (
          <p>예시 데이터: 회원 목록 (0명) · 등록된 회원이 없습니다.</p>
        )}
        <p style={{ color: "#64748b" }}>
          이 예시는 실제 DB에 회원이 없다는 증빙이 아닙니다.
        </p>
      </section>
    </main>
  );
}
