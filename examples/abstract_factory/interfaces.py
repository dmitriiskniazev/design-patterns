from typing import Protocol


class Reader(Protocol):
    def read(self, text: str) -> dict[str, str]: ...


class Writer(Protocol):
    def write(self, data: dict[str, str]) -> str: ...


class Validator(Protocol):
    def validate(self, text: str) -> None: ...
