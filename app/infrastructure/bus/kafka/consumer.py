import json
import logging
from uuid import UUID

from aiokafka import AIOKafkaConsumer

from app.config.kafka import kafka_settings
from app.infrastructure.bus.kafka.producer import KafkaEventProducer
from app.infrastructure.clients import ProfileServiceClient
from app.infrastructure.db.repositories.attendance import AttendanceRepository
from app.infrastructure.db.session import get_session
from app.infrastructure.di.container import Container
from app.service.attendance import AttendanceService

container: Container = Container()
logger = logging.getLogger(__name__)


class KafkaEventConsumer:
    def __init__(self, bootstrap_servers: str, group_id: str):
        self.bootstrap_servers = bootstrap_servers
        self.group_id = group_id
        self.consumer: AIOKafkaConsumer | None = None
        self.running = False

    async def start(self, service_callback_map: dict):
        self.consumer = AIOKafkaConsumer(
            "event-started", "student-recognized",
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.group_id,
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        )
        await self.consumer.start()
        self.running = True
        logger.info("Kafka consumer started")

        try:
            async for msg in self.consumer:
                topic = msg.topic
                payload = msg.value

                logger.info(f"Received message from {topic}: {payload}")

                if topic in service_callback_map:
                    try:
                        await service_callback_map[topic](payload)
                    except Exception as e:
                        logger.error(f"Error during kafka message processing: {str(e)}")
        finally:
            await self.consumer.stop()

    async def stop(self):
        if self.consumer and self.running:
            await self.consumer.stop()
            logger.info("Kafka consumer stopped")


def build_kafka_handlers(
        service: AttendanceService,
        profile_client: ProfileServiceClient,
) -> dict:
    async def handle_event_started(message: dict):
        event_id = UUID(message["event_id"])
        group_id = message["group_id"]
        logger.info(f"Handling started event with {event_id=} and {group_id=}")
        student_ids = await profile_client.get_students_by_group(group_id)
        await service.init_event_attendance(event_id, student_ids)

    async def handle_student_recognized(message: dict):
        event_id = UUID(message["event_id"])
        student_id = UUID(message["student_id"])
        await service.change_attendance(event_id, student_id, True)

    return {
        "event-started": handle_event_started,
        "student-recognized": handle_student_recognized,
    }


async def start_kafka_consumer(producer: KafkaEventProducer):
    session = await anext(get_session())
    repo = AttendanceRepository(session)
    service = AttendanceService(repo, producer)
    client = ProfileServiceClient()
    handlers = build_kafka_handlers(service, client)

    consumer = KafkaEventConsumer(
        bootstrap_servers=kafka_settings.bootstrap_servers,
        group_id="attendance-service"
    )
    await consumer.start(handlers)

