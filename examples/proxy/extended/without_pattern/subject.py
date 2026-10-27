from dataclasses import dataclass


@dataclass
class RealSubject:
    calls: int = 0

    def operation(self) -> int:
        self.calls += 1
        return 1
