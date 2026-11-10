import type { Member } from "../types/member";

export async function getMembers(signal?: AbortSignal): Promise<Member[]> {
  const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL;
  if (!baseUrl) throw new Error("API 주소가 설정되지 않았습니다.");
  const response = await fetch(`${baseUrl.replace(/\/$/, "")}/members`, {
    signal,
    cache: "no-store",
  });
  if (!response.ok) throw new Error(`회원 조회에 실패했습니다. (HTTP ${response.status})`);
  const data: unknown = await response.json();
  if (!Array.isArray(data)) throw new Error("회원 목록 응답 형식이 올바르지 않습니다.");
  return data.map((item: unknown) => {
    if (typeof item !== "object" || item === null) throw new Error("회원 정보 형식이 올바르지 않습니다.");
    const value = item as Record<string, unknown>;
    const id = value.member_id ?? value.id;
    if (!Number.isInteger(id) || typeof value.name !== "string" || typeof value.email !== "string" || !Number.isInteger(value.age)) {
      throw new Error("회원 정보 형식이 올바르지 않습니다.");
    }
    return { member_id: id as number, name: value.name, email: value.email, age: value.age as number };
  });
}
