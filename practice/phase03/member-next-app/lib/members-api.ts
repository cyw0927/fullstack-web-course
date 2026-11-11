
import type { Member } from "../types/member";

// FastAPI 회원 API 경로
const MEMBERS_PATH = "/members";

// 회원 등록·수정 시 서버에 보내는 데이터
// gender는 선택 입력이므로 기존 CRUD 요청과 호환됨
export type MemberPayload = Pick<
  Member,
  "name" | "email" | "age" | "gender"
>;

// API 서버 주소 생성
function apiUrl(path: string): string {
  const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL;

  if (!baseUrl) {
    throw new Error("API 서버 주소가 설정되지 않았습니다.");
  }

  return baseUrl.replace(/\/$/, "") + path;
}

// HTTP 요청 성공 여부 확인
async function requireOk(response: Response): Promise<void> {
  if (!response.ok) {
    throw new Error(
      `회원 API 요청 실패: HTTP ${response.status}`
    );
  }
}

// FastAPI 응답을 Member 타입으로 변환
function parseMember(data: unknown): Member {
  if (typeof data !== "object" || data === null) {
    throw new Error("회원 정보 형식이 올바르지 않습니다.");
  }

  const value = data as Record<string, unknown>;

  // 기존 4강의 ID 호환성 유지
  const id = value.member_id ?? value.id;

  if (
    !Number.isInteger(id) ||
    typeof value.name !== "string" ||
    typeof value.email !== "string" ||
    !Number.isInteger(value.age)
  ) {
    throw new Error("회원 정보 형식이 올바르지 않습니다.");
  }

  // 새로 추가된 성별 검증
  const gender = value.gender;

  if (
    gender !== undefined &&
    gender !== null &&
    gender !== "M" &&
    gender !== "F"
  ) {
    throw new Error("회원 성별 형식이 올바르지 않습니다.");
  }

  return {
    member_id: id as number,
    name: value.name,
    email: value.email,
    age: value.age as number,
    gender: gender === "M" || gender === "F"
      ? gender
      : null,
  };
}

// ========================================
// 1. GET — 회원 전체 목록 조회
// ========================================
export async function getMembers(
  signal?: AbortSignal
): Promise<Member[]> {
  const response = await fetch(apiUrl(MEMBERS_PATH), {
    signal,
    cache: "no-store",
  });

  await requireOk(response);

  const data: unknown = await response.json();

  if (!Array.isArray(data)) {
    throw new Error(
      "회원 목록 응답 형식이 올바르지 않습니다."
    );
  }

  return data.map(parseMember);
}

// ========================================
// 2. POST — 회원 등록
// ========================================
export async function createMember(
  body: MemberPayload
): Promise<void> {
  const response = await fetch(apiUrl(MEMBERS_PATH), {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });

  await requireOk(response);
}

// ========================================
// 3. PUT — 회원 정보 수정
// ========================================
export async function updateMember(
  memberId: number,
  body: MemberPayload
): Promise<void> {
  const response = await fetch(
    apiUrl(`${MEMBERS_PATH}/${memberId}`),
    {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    }
  );

  await requireOk(response);
}

// ========================================
// 4. DELETE — 회원 삭제
// ========================================
export async function deleteMember(
  memberId: number
): Promise<void> {
  const response = await fetch(
    apiUrl(`${MEMBERS_PATH}/${memberId}`),
    {
      method: "DELETE",
    }
  );

  // HTTP 204는 응답 본문이 없음
  await requireOk(response);
}

// ========================================
// 5. GET — 회원 상세 조회 (6강)
// ========================================
export async function getMember(
  memberId: number,
  signal?: AbortSignal
): Promise<Member> {
  const response = await fetch(
    apiUrl(`${MEMBERS_PATH}/${memberId}`),
    {
      signal,
      cache: "no-store",
    }
  );

  await requireOk(response);

  const data: unknown = await response.json();

  return parseMember(data);
}
