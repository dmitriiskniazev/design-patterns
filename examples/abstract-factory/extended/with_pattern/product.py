from dataclasses import dataclass


@dataclass(frozen=True)
class Product:
    marker: str

    def operation(self) -> str:
        return self.marker
