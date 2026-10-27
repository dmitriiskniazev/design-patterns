from dataclasses import dataclass


@dataclass(frozen=True)
class Snapshot:
    value: int
    flag: bool


@dataclass
class Originator:
    value: int
    flag: bool

    def save(self) -> Snapshot:
        return Snapshot(self.value, self.flag)

    def restore(self, snapshot: Snapshot) -> None:
        self.value, self.flag = snapshot.value, snapshot.flag
