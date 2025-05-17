from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class EventTemplateDTO:
    title: str
    description: str | None


@dataclass
class EventDTO:
    owner_id: UUID
    template_id: UUID
    group_id: UUID
    start_time: datetime
