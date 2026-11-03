from enum import StrEnum


class Storage(StrEnum):
    DICT = "dict"
    LIST = "list"


def operation(
    storage: Storage, key: int, mapping: dict[int, int], pairs: list[tuple[int, int]]
) -> int:
    match storage:
        case Storage.DICT:
            return mapping[key] + 1
        case Storage.LIST:
            return next(value for stored_key, value in pairs if stored_key == key) + 1


if __name__ == "__main__":
    print(operation(Storage.LIST, 1, {}, [(1, 2)]))
