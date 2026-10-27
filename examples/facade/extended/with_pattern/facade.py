from subsystems import SubsystemA, SubsystemB, SubsystemC


class Facade:
    def operation(self, value: int) -> int:
        intermediate = SubsystemA().operation(value)
        return SubsystemB().operation(intermediate)


class ExtendedFacade(Facade):
    def operation(self, value: int) -> int:
        return SubsystemC().operation(super().operation(value))
