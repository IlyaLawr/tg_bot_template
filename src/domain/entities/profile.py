from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class Profile:
    client_id: int
    name: str = ''
    registration_date: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    taps_statistics: int = 0
    about: str = 'Обычный игрок'
    photo: str = ''

    def __post_init__(self):
        if not self.name:
            self.name = f'Игрок {self.client_id}'
