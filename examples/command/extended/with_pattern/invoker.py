from dataclasses import dataclass, field

from command import Command


@dataclass
class Invoker:
    history: list[Command] = field(default_factory=list)

    def run(self, command: Command) -> None:
        command.execute()
        self.history.append(command)

    def undo(self) -> None:
        self.history.pop().undo()
