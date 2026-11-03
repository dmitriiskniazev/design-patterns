from dataclasses import dataclass

from subject import Subject


@dataclass
class CachedProxy:
    inner: Subject
    cached: int | None = None

    def operation(self) -> int:
        if self.cached is None:
            self.cached = self.inner.operation()
        return self.cached
