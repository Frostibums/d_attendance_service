from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class Attendance(BaseModel):
    id: UUID
    student_id: UUID
    event_id: UUID
    attended: bool
    created_at: datetime
    updated_at: datetime
