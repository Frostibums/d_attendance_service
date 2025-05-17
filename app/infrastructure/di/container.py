from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config.db import db_settings
from app.infrastructure.bus.kafka.producer import KafkaEventProducer, get_kafka_producer
from app.infrastructure.db.repositories.attendance import AttendanceRepository
from app.service.attendance import AttendanceService


class Container:
    def __init__(self):
        self._engine = create_async_engine(db_settings.db_url, echo=False)
        self._sessionmaker = async_sessionmaker(self._engine, expire_on_commit=False)

    async def get_session(self) -> AsyncSession:
        async with self._sessionmaker() as session:
            yield session

    @classmethod
    async def get_producer(cls) -> KafkaEventProducer:
        return await get_kafka_producer()

    @classmethod
    def get_attendance_repo(cls, session: AsyncSession) -> AttendanceRepository:
        return AttendanceRepository(session)

    async def get_attendance_service(self, session: AsyncSession) -> AttendanceService:
        producer = await self.get_producer()
        return AttendanceService(
            repository=self.get_attendance_repo(session),
            kafka_producer=producer,
        )
