from dataclasses import dataclass

from subject import Subject


@dataclass
class CountingProxy:
    inner: Subject
    calls: int = 0

    def operation(self) -> int:
        self.calls += 1
        return self.inner.operation()
