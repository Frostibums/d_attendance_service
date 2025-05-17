from fastapi import APIRouter

from app.presentation.api.v1.endpoints import router as attendance_router

api_router = APIRouter()

api_router.include_router(attendance_router, prefix="/attendance", tags=["Attendance"])
