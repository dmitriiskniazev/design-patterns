from dataclasses import dataclass, field

from product import Product


@dataclass
class Builder:
    parts: list[str] = field(default_factory=list)

    def add(self, part: str) -> None:
        self.parts.append(part)

    def build(self) -> Product:
        return Product(tuple(self.parts))
