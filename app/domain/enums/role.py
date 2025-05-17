from enum import Enum


class Role(str, Enum):
    on_moderation = "on_moderation"
    student = "student"
    teacher = "teacher"
    admin = "admin"
    internal_service = "internal_service"
