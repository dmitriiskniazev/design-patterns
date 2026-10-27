from repository import Repository


def operation(repository: Repository, key: int) -> int:
    return repository.get(key) + 1
