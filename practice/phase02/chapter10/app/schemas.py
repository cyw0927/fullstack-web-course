"""회원 API의 요청과 응답 데이터 모양을 정의합니다."""
from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator


class MemberCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    age: int = Field(ge=0, le=150)


class MemberUpdate(MemberCreate):
    """PUT: 세 필드를 모두 전달합니다."""


class MemberPatch(BaseModel):
    """PATCH: 바꿀 필드만 전달합니다. 명시적인 null은 허용하지 않습니다."""
    model_config = ConfigDict(extra="forbid")
    name: str | None = Field(default=None, min_length=1, max_length=100)
    email: EmailStr | None = None
    age: int | None = Field(default=None, ge=0, le=150)

    @model_validator(mode="after")
    def reject_null(self):
        for field in self.model_fields_set:
            if getattr(self, field) is None:
                raise ValueError(f"{field} cannot be null")
        return self


class MemberResponse(MemberCreate):
    # 실제 public.members의 컬럼과 기존 API 응답은 member_id가 아닌 id입니다.
    id: int
