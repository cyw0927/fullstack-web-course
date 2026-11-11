
"use client";

import { useEffect, useState } from "react";
import type { FormEvent } from "react";

import MemberList from "./MemberList";
import {
  createMember,
  deleteMember,
  getMembers,
  updateMember,
} from "../lib/members-api";
import type { Member } from "../types/member";

type GenderValue = "" | "M" | "F";

export default function MemberWorkspace() {
  // 1. 회원 목록 조회 상태
  const [members, setMembers] = useState<Member[]>([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState("");
  const [reloadKey, setReloadKey] = useState(0);

  // 2. 회원 등록·수정 입력값
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [age, setAge] = useState("");

  // 이번 실습에서 추가한 성별
  // "" = 미지정, "M" = 남성, "F" = 여성
  const [gender, setGender] = useState<GenderValue>("");

  // null이면 등록, 숫자이면 수정 모드
  const [editingId, setEditingId] = useState<number | null>(
    null
  );

  // 3. 요청 및 메시지 상태
  const [busy, setBusy] = useState(false);
  const [actionError, setActionError] = useState("");
  const [notice, setNotice] = useState("");

  // 4. 기존 회원 목록 조회 (GET)
  useEffect(() => {
    const controller = new AbortController();

    async function loadMembers() {
      setLoading(true);
      setLoadError("");

      try {
        const data = await getMembers(controller.signal);

        if (!controller.signal.aborted) {
          setMembers(data);
        }
      } catch (error) {
        if (!controller.signal.aborted) {
          setLoadError(
            error instanceof Error
              ? error.message
              : "회원 조회 중 오류가 발생했습니다."
          );
        }
      } finally {
        if (!controller.signal.aborted) {
          setLoading(false);
        }
      }
    }

    void loadMembers();

    return () => controller.abort();
  }, [reloadKey]);

  // 5. 회원 검색
  const keyword = search.trim().toLowerCase();

  const filteredMembers = members.filter((member) => {
    return (
      member.name.toLowerCase().includes(keyword) ||
      member.email.toLowerCase().includes(keyword)
    );
  });

  // 6. 입력값 검증
  const ageNumber = Number(age);

  const validAge =
    age.trim() !== "" &&
    Number.isInteger(ageNumber) &&
    ageNumber >= 0 &&
    ageNumber <= 150;

  const validForm =
    name.trim() !== "" &&
    email.trim() !== "" &&
    validAge;

  // 7. 입력 폼 초기화
  function clearForm() {
    setEditingId(null);
    setName("");
    setEmail("");
    setAge("");
    setGender("");
  }

  // 8. 수정 버튼: 기존 회원 정보 입력
  function startEdit(member: Member) {
    setEditingId(member.member_id);
    setName(member.name);
    setEmail(member.email);
    setAge(String(member.age));

    // 저장된 성별도 자동 선택
    setGender(
      member.gender === "M" || member.gender === "F"
        ? member.gender
        : ""
    );

    setActionError("");
    setNotice("");
  }

  // 9. 회원 등록 또는 수정 (POST / PUT)
  async function handleSubmit(
    event: FormEvent<HTMLFormElement>
  ) {
    event.preventDefault();

    if (!validForm || busy || loading) {
      return;
    }

    setBusy(true);
    setActionError("");
    setNotice("");

    let changed = false;
    const action = editingId === null ? "등록" : "수정";

    try {
      // 기존 세 필드 + 성별 추가
      const payload = {
        name: name.trim(),
        email: email.trim(),
        age: ageNumber,

        // 미지정 선택 시 DB에 NULL 저장
        gender: gender === "" ? null : gender,
      };

      if (editingId === null) {
        // POST /members
        await createMember(payload);
      } else {
        // PUT /members/{member_id}
        await updateMember(editingId, payload);
      }

      changed = true;

      // 서버 변경 후 최신 목록 재조회
      const latest = await getMembers();
      setMembers(latest);

      clearForm();

      setNotice(
        `회원 ${action} 후 목록을 다시 조회했습니다.`
      );
    } catch (error) {
      const detail =
        error instanceof Error
          ? error.message
          : "알 수 없는 오류";

      setActionError(
        changed
          ? `서버 변경은 성공했지만 목록 재조회에 실패했습니다: ${detail}`
          : `회원 ${action} 요청 실패: ${detail}`
      );
    } finally {
      setBusy(false);
    }
  }

  // 10. 기존 회원 삭제 (DELETE)
  async function handleDelete(member: Member) {
    if (busy || loading) {
      return;
    }

    const confirmed = window.confirm(
      `${member.name} 회원(ID ${member.member_id})을 삭제할까요?`
    );

    if (!confirmed) {
      return;
    }

    setBusy(true);
    setActionError("");
    setNotice("");

    let changed = false;

    try {
      await deleteMember(member.member_id);
      changed = true;

      const latest = await getMembers();
      setMembers(latest);

      if (editingId === member.member_id) {
        clearForm();
      }

      setNotice(
        "회원 삭제 후 목록을 다시 조회했습니다."
      );
    } catch (error) {
      const detail =
        error instanceof Error
          ? error.message
          : "알 수 없는 오류";

      setActionError(
        changed
          ? `서버 삭제는 성공했지만 목록 재조회에 실패했습니다: ${detail}`
          : `회원 삭제 요청 실패: ${detail}`
      );
    } finally {
      setBusy(false);
    }
  }

  // 11. 기존 대시보드 UI 유지
  return (
    <div className="member-dashboard">
      {/* 왼쪽: 회원 목록 */}
      <section
        className="panel member-panel"
        aria-labelledby="member-list-title"
      >
        <div className="panel-heading">
          <div>
            <p className="section-kicker">MEMBERS</p>

            <h2 id="member-list-title">
              회원 목록{" "}
              <span className="count-badge">
                {filteredMembers.length}
              </span>
            </h2>

            <p className="section-description">
              회원 정보를 확인하고 관리합니다.
            </p>
          </div>

          <button
            className="btn btn-secondary reload-button"
            type="button"
            disabled={loading || busy}
            onClick={() =>
              setReloadKey((value) => value + 1)
            }
          >
            <span aria-hidden="true">↻</span> 다시 조회
          </button>
        </div>

        {/* 검색 */}
        <div className="search-area">
          <label
            className="field-label"
            htmlFor="member-search"
          >
            회원 검색
          </label>

          <div className="search-controls">
            <div className="search-input-wrap">
              <span
                className="search-icon"
                aria-hidden="true"
              >
                ⌕
              </span>

              <input
                id="member-search"
                value={search}
                onChange={(event) =>
                  setSearch(event.target.value)
                }
                placeholder="이름 또는 이메일로 검색"
              />
            </div>

            <button
              className="btn btn-secondary"
              type="button"
              onClick={() => setSearch("")}
            >
              검색 초기화
            </button>
          </div>
        </div>

        {/* 회원 목록 */}
        {loading ? (
          <p className="state-message" role="status">
            회원 목록을 불러오는 중입니다...
          </p>
        ) : loadError ? (
          <p
            className="message message-error"
            role="alert"
          >
            목록 조회 오류: {loadError}
          </p>
        ) : (
          <MemberList
            members={filteredMembers}
            onEdit={startEdit}
            onDelete={(member) => {
              void handleDelete(member);
            }}
            busy={busy}
          />
        )}
      </section>

      {/* 오른쪽: 등록·수정 폼 */}
      <section
        className="panel form-panel"
        aria-labelledby="member-form-title"
      >
        <div className="form-heading">
          <p className="section-kicker">
            MEMBER DETAILS
          </p>

          <h2 id="member-form-title">
            {editingId === null
              ? "회원 등록"
              : `회원 수정 (ID ${editingId})`}
          </h2>

          <p className="section-description">
            {editingId === null
              ? "새 회원의 정보를 입력해 주세요."
              : "선택한 회원의 정보를 수정해 주세요."}
          </p>
        </div>

        <form
          className="member-form"
          onSubmit={(event) => {
            void handleSubmit(event);
          }}
        >
          {/* 이름 */}
          <div className="form-field">
            <label
              className="field-label"
              htmlFor="member-name"
            >
              이름
            </label>

            <input
              id="member-name"
              value={name}
              onChange={(event) =>
                setName(event.target.value)
              }
              placeholder="이름을 입력하세요"
              required
            />
          </div>

          {/* 이메일 */}
          <div className="form-field">
            <label
              className="field-label"
              htmlFor="member-email"
            >
              이메일
            </label>

            <input
              id="member-email"
              type="email"
              value={email}
              onChange={(event) =>
                setEmail(event.target.value)
              }
              placeholder="example@email.com"
              required
            />
          </div>

          {/* 나이 */}
          <div className="form-field">
            <label
              className="field-label"
              htmlFor="member-age"
            >
              나이
            </label>

            <input
              id="member-age"
              type="number"
              min={0}
              max={150}
              value={age}
              onChange={(event) =>
                setAge(event.target.value)
              }
              placeholder="나이를 입력하세요"
              required
            />
          </div>

          {/* 성별: 이번에 추가한 입력창 */}
          <div className="form-field">
            <label
              className="field-label"
              htmlFor="member-gender"
            >
              성별
            </label>

            <select
              id="member-gender"
              value={gender}
              onChange={(event) =>
                setGender(
                  event.target.value as GenderValue
                )
              }
              style={{
                display: "block",
                width: "100%",
                minHeight: 44,
                padding: "10px 12px",
                border: "1px solid #cbd5e1",
                borderRadius: 10,
                backgroundColor: "#ffffff",
                color: "#1b2940",
                font: "inherit",
              }}
            >
              <option value="">미지정</option>
              <option value="M">남성</option>
              <option value="F">여성</option>
            </select>
          </div>

          {/* 기존 저장 및 취소 버튼 */}
          <div className="form-actions">
            <button
              className="btn btn-primary"
              type="submit"
              disabled={!validForm || busy || loading}
            >
              {busy
                ? "처리 중..."
                : editingId === null
                  ? "회원 등록"
                  : "회원 수정 저장"}
            </button>

            <button
              className="btn btn-secondary"
              type="button"
              disabled={busy}
              onClick={clearForm}
            >
              입력 초기화 / 수정 취소
            </button>
          </div>
        </form>

        {/* 기존 성공 및 오류 메시지 */}
        {notice && (
          <p
            className="message message-success"
            role="status"
          >
            {notice}
          </p>
        )}

        {actionError && (
          <p
            className="message message-error"
            role="alert"
          >
            {actionError}
          </p>
        )}

        <p className="form-footnote">
          입력한 정보는 데이터베이스에 저장됩니다.
        </p>
      </section>
    </div>
  );
}
