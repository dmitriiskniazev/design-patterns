from dataclasses import dataclass


@dataclass(frozen=True)
class Snapshot:
    value: int


@dataclass
class Originator:
    value: int

    def save(self) -> Snapshot:
        return Snapshot(self.value)

    def restore(self, snapshot: Snapshot) -> None:
        self.value = snapshot.value
