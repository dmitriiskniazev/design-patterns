from dataclasses import dataclass

from provider import Provider


@dataclass
class Client:
    provider: Provider

    def operation(self) -> int:
        return self.provider.get() + 1
