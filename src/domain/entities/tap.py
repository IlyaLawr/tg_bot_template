from uuid import UUID, uuid4
from datetime import datetime
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Tap:
    id: UUID = field(default_factory=uuid4)
    timestamp: datetime = field(default_factory=datetime.now)
