from subsystems import SubsystemA, SubsystemB


class Facade:
    def operation(self, value: int) -> int:
        intermediate = SubsystemA().operation(value)
        return SubsystemB().operation(intermediate)
