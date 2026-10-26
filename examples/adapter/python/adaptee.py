class Adaptee:
    def specific_operation(self, value: int) -> int:
        return value + 1


class SecondAdaptee:
    def different_operation(self, value: int) -> int:
        return value * 2
