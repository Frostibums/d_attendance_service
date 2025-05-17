from datetime import datetime
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities import Attendance
from app.infrastructure.db.models.attendance import AttendanceORM


class AttendanceRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_bulk_for_event(
            self,
            event_id: UUID,
            student_ids: list[UUID]
    ) -> None:
        entries = [
            AttendanceORM(student_id=sid, event_id=event_id)
            for sid in student_ids
        ]
        self.session.add_all(entries)
        await self.session.commit()

    async def mark_attended(self, event_id: UUID, student_id: UUID) -> None:
        stmt = (
            update(AttendanceORM)
            .where(
                AttendanceORM.event_id == event_id,
                AttendanceORM.student_id == student_id,
            )
            .values(attended=True, updated_at=datetime.utcnow())
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def get_by_event(self, event_id: UUID) -> list[Attendance]:
        stmt = select(AttendanceORM).where(
            AttendanceORM.event_id == event_id
        )
        result = await self.session.scalars(stmt)
        return [a.to_domain() for a in result]

    async def get_by_student(self, student_id: UUID) -> list[Attendance]:
        stmt = select(
            AttendanceORM
        ).where(
            AttendanceORM.student_id == student_id
        ).order_by(
            AttendanceORM.id.desc()
        )
        result = await self.session.scalars(stmt)
        return [a.to_domain() for a in result]
