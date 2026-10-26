from copy import deepcopy

from value import Value


class Prototype(Value):
    def clone(self) -> Prototype:
        return deepcopy(self)
