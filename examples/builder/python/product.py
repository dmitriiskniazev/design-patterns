from dataclasses import dataclass


@dataclass(frozen=True)
class Product:
    parts: tuple[str, ...]
