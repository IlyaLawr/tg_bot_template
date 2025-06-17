from dataclasses import dataclass, field

from domain.entities.tap import Tap


@dataclass
class Game:
    id: int
    taps: list[Tap] = field(default_factory=list)


    def add_tap(self, tap: Tap):
        self.taps.append(tap)


    def result(self):
        return len(self.taps)
