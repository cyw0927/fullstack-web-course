
"""API 요청과 응답의 데이터 계약."""

from typing import Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    model_validator,
)


# 성별은 M(남성), F(여성)만 허용
Gender = Literal["M", "F"]


# ========================================
# 1. POST — 회원 등록
# ========================================
class MemberCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    age: int = Field(ge=0, le=150)

    # 기존 프론트엔드와 호환되도록 선택 입력
    gender: Gender | None = None


# ========================================
# 2. PUT — 회원 정보 전체 수정
# ========================================
class MemberUpdate(MemberCreate):
    """
    이름, 이메일, 나이는 필수입니다.
    성별은 기존 요청과의 호환성을 위해 선택 입력입니다.
    """


# ========================================
# 3. PATCH — 회원 정보 일부 수정
# ========================================
class MemberPatch(BaseModel):
    """전달한 필드만 수정하며 명시적인 null은 거부합니다."""

    model_config = ConfigDict(extra="forbid")

    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )

    email: EmailStr | None = None

    age: int | None = Field(
        default=None,
        ge=0,
        le=150,
    )

    gender: Gender | None = None

    @model_validator(mode="after")
    def reject_explicit_null(self):
        for field in self.model_fields_set:
            if getattr(self, field) is None:
                raise ValueError(f"{field} cannot be null")

        return self


# ========================================
# 4. GET — 회원 정보 응답
# ========================================
class MemberResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    member_id: int
    name: str
    email: EmailStr
    age: int

    # 기존 회원에게 값이 없을 수도 있음
    gender: Gender | None = None
