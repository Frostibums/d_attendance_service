from uuid import UUID

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.requests import Request

from app.domain.enums.role import Role
from app.infrastructure.bus.kafka.producer import KafkaEventProducer
from app.infrastructure.db.repositories.attendance import AttendanceRepository
from app.infrastructure.db.session import get_session
from app.infrastructure.security import decode_jwt_token
from app.service.attendance import AttendanceService


def get_kafka_producer(request: Request) -> KafkaEventProducer:
    return request.app.state.kafka_producer


def get_attendance_service(
        session: AsyncSession = Depends(get_session),
        producer: KafkaEventProducer = Depends(get_kafka_producer)
) -> AttendanceService:
    return AttendanceService(
        AttendanceRepository(session),
        producer,
    )


def get_jwt_payload(request: Request) -> dict:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing access token",
        )

    if token.startswith("Bearer "):
        token = token[7:]
    try:
        return decode_jwt_token(token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )


def get_current_teacher_id(payload: dict = Depends(get_jwt_payload)) -> UUID:
    if payload.get("role") not in (Role.teacher, Role.admin):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only for stuff"
        )
    return UUID(payload["sub"])


def get_current_user_id(payload: dict = Depends(get_jwt_payload)) -> UUID:
    return UUID(payload["sub"])
