from dataclasses import dataclass, field

from component import Component


@dataclass
class Mediator:
    components: list[Component] = field(default_factory=list)

    def notify(self, sender: Component, value: int) -> None:
        for component in self.components:
            if component is not sender:
                component.receive(value)
