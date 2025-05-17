import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.domain.entities import Attendance
from app.infrastructure.db.session import Base


class AttendanceORM(Base):
    __tablename__ = "attendance"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
    )
    event_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
    )
    attended = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    created_at = mapped_column(
        DateTime,
        default=datetime.utcnow,
        server_default=func.now(),
        nullable=False,
    )
    updated_at = mapped_column(
        DateTime,
        default=datetime.utcnow,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def to_domain(self) -> Attendance:
        return Attendance(
            id=self.id,
            student_id=self.student_id,
            event_id=self.event_id,
            attended=self.attended,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    @classmethod
    def from_domain(cls, attendance: Attendance) -> "AttendanceORM":
        return cls(
            id=attendance.id,
            student_id=attendance.student_id,
            event_id=attendance.event_id,
            attended=attendance.attended,
            created_at=attendance.created_at,
            updated_at=attendance.updated_at,
        )
