from uuid import UUID

from app.domain.entities import Attendance
from app.infrastructure.bus.kafka.producer import KafkaEventProducer
from app.infrastructure.db.repositories.attendance import AttendanceRepository


class AttendanceService:
    def __init__(
        self,
        repository: AttendanceRepository,
        kafka_producer: KafkaEventProducer,
    ):
        self.repository = repository
        self.kafka_producer = kafka_producer

    async def init_event_attendance(
            self,
            event_id: UUID,
            student_ids: list[UUID]
    ) -> None:
        await self.repository.create_bulk_for_event(event_id, student_ids)

    async def change_attendance(
            self,
            event_id: UUID,
            student_id: UUID,
            attended: bool = False,
    ) -> None:
        await self.repository.change_attendance(event_id, student_id, attended)
        if attended is True:
            await self.kafka_producer.send(
                topic="student-attended",
                message={
                    "student_id": str(student_id),
                    "event_id": str(event_id),
                },
            )

    async def get_event_attendance(
            self,
            event_id: UUID,
    ) -> list[Attendance]:
        return await self.repository.get_by_event(event_id)

    async def get_student_attendance(
            self,
            student_id: UUID,
    ) -> list[Attendance]:
        return await self.repository.get_by_student(student_id)
