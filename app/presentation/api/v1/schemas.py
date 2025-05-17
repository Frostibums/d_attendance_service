from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class AttendanceOut(BaseModel):
    id: UUID
    student_id: UUID
    event_id: UUID
    attended: bool
    created_at: datetime
    updated_at: datetime | None


class MarkAttendanceIn(BaseModel):
    event_id: UUID
    student_id: UUID
    attended: bool = True
