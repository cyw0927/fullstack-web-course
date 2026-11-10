"""API 요청과 응답의 데이터 계약."""
from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator


class MemberCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    age: int = Field(ge=0, le=150)


class MemberUpdate(MemberCreate):
    """PUT은 세 필드를 모두 받아 전체 수정합니다."""


class MemberPatch(BaseModel):
    """PATCH는 전달한 필드만 수정하고 null은 거부합니다."""
    model_config = ConfigDict(extra="forbid")
    name: str | None = Field(default=None, min_length=1, max_length=100)
    email: EmailStr | None = None
    age: int | None = Field(default=None, ge=0, le=150)

    @model_validator(mode="after")
    def reject_explicit_null(self):
        for field in self.model_fields_set:
            if getattr(self, field) is None:
                raise ValueError(f"{field} cannot be null")
        return self


class MemberResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    member_id: int
    name: str
    email: EmailStr
    age: int
