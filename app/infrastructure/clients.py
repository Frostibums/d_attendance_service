import asyncio
from uuid import UUID

import httpx


class ProfileServiceClient:
    def __init__(self, base_url: str = "http://profile-service:8000"):
        self.base_url = base_url.rstrip("/")

    async def get_students_by_group(self, group_id: UUID) -> list[UUID]:
        url = f"{self.base_url}/profile/by-group/{str(group_id)}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
        response.raise_for_status()
        data = response.json()
        return [UUID(student["user_id"]) for student in data]
