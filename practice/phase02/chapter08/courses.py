"""8강 독립 과제: 강좌 API. 기본 Swagger에서는 숨깁니다."""
import logging
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field, ConfigDict, model_validator
import common.db as storage
from common.db import DuplicateCourseError, fetch_courses, find_course, insert_course

router = APIRouter()
logger = logging.getLogger(__name__)

class CourseCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    instructor: str = Field(min_length=1, max_length=100)
    capacity: int = Field(gt=0, le=10000)


class CourseResponse(CourseCreate):
    id: int


def course_dict(row):
    # SELECT/RETURNING 순서: id, title, instructor, capacity
    return {"id": row[0], "title": row[1], "instructor": row[2], "capacity": row[3]}


@router.get("/courses", response_model=list[CourseResponse])
def get_courses():
    return [course_dict(row) for row in fetch_courses()]


@router.get("/courses/{course_id}", response_model=CourseResponse)
def get_course(course_id: int):
    row = find_course(course_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return course_dict(row)


@router.post(
    "/courses",
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_course(course: CourseCreate):
    try:
        row = insert_course(course.title, course.instructor, course.capacity)
        return course_dict(row)
    except DuplicateCourseError as exc:
        raise HTTPException(status_code=409, detail="이미 등록된 강좌입니다.") from exc
    except Exception as exc:
        logger.exception("강좌 INSERT 또는 commit 중 오류")
        raise HTTPException(
            status_code=500,
            detail="강좌 등록 중 오류가 발생했습니다.",
        ) from exc


class CourseUpdate(CourseCreate):
    """PUT: title/instructor/capacity 모두 필수."""


class CoursePatch(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str | None = Field(default=None, min_length=1, max_length=200)
    instructor: str | None = Field(default=None, min_length=1, max_length=100)
    capacity: int | None = Field(default=None, gt=0, le=10000)

    @model_validator(mode="after")
    def reject_explicit_null(self):
        for field in self.model_fields_set:
            if getattr(self, field) is None:
                raise ValueError(f"{field} cannot be null")
        return self


def save_course_update(course_id: int, changes: dict):
    try:
        row = storage.update_course_fields(course_id, changes)
        return course_dict(row)
    except storage.CourseNotFound as exc:
        raise HTTPException(status_code=404, detail="Course not found") from exc
    except storage.DuplicateCourseError as exc:
        raise HTTPException(status_code=409, detail="Course already exists") from exc
    except Exception as exc:
        logger.exception("강좌 UPDATE 중 DB 오류")
        raise HTTPException(status_code=500, detail="강좌 수정 중 오류가 발생했습니다.") from exc


@router.put("/courses/{course_id}", response_model=CourseResponse)
def put_course(course_id: int, course: CourseUpdate):
    return save_course_update(course_id, course.model_dump())


@router.patch("/courses/{course_id}", response_model=CourseResponse)
def patch_course(course_id: int, course: CoursePatch):
    changes = course.model_dump(exclude_unset=True)
    if not changes:
        raise HTTPException(status_code=400, detail="At least one field is required")
    return save_course_update(course_id, changes)
