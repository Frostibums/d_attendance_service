import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config.app import app_settings
from app.infrastructure.bus.kafka.consumer import start_kafka_consumer
from app.infrastructure.bus.kafka.producer import get_kafka_producer
from app.infrastructure.logger import setup_logging
from app.presentation.api.routes import api_router


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):  # noqa ARG001
    kafka_producer = await get_kafka_producer()
    fastapi_app.state.kafka_producer = kafka_producer

    consumer_task = asyncio.create_task(
        start_kafka_consumer(producer=kafka_producer)
    )

    yield

    await kafka_producer.stop()
    consumer_task.cancel()
    try:
        await consumer_task
    except asyncio.CancelledError:
        pass

setup_logging()
app = FastAPI(
    title=app_settings.app_name,
    lifespan=lifespan,
    debug=app_settings.debug,
)

app.include_router(api_router)
