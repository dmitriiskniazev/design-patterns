from dataclasses import dataclass


@dataclass
class Caretaker[T]:
    snapshot: T
