from typing import ClassVar, Self, final

from instance import Instance


@final
class Singleton(Instance):
    _instance: ClassVar[Singleton | None] = None

    def __new__(cls) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.value = 0
        return cls._instance

    def __init__(self) -> None:
        pass
