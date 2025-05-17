from uuid import UUID

from fastapi import APIRouter, Depends

from app.presentation.api.v1.dependencies import (
    get_attendance_service,
    get_current_teacher_id,
)
from app.presentation.api.v1.schemas import AttendanceOut, MarkAttendanceIn
from app.service.attendance import AttendanceService

router = APIRouter(prefix="/attendance", tags=["Attendance"])


@router.get("/event/{event_id}", response_model=list[AttendanceOut])
async def get_attendance_by_event(
        event_id: UUID,
        service: AttendanceService = Depends(get_attendance_service),
):
    return await service.get_event_attendance(event_id)


@router.get("/student/{student_id}", response_model=list[AttendanceOut])
async def get_attendance_by_student(
        student_id: UUID,
        service: AttendanceService = Depends(get_attendance_service),
):
    return await service.get_student_attendance(student_id)


@router.patch(
    "/mark",
    dependencies=[Depends(get_current_teacher_id)],
    response_model=None,
)
async def mark_attended(
        data: MarkAttendanceIn,
        service: AttendanceService = Depends(get_attendance_service),
):
    await service.mark_student_attended(data.event_id, data.student_id)
