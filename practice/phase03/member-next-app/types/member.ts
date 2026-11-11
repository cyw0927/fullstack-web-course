
export type Member = {
  // 회원 고유 번호
  member_id: number;

  // 회원 이름
  name: string;

  // 이메일
  email: string;

  // 나이
  age: number;

  // 성별: M(남성), F(여성), null(미지정)
  // 기존 프론트엔드와 호환되도록 선택적 필드로 처리
  gender?: "M" | "F" | null;
};
