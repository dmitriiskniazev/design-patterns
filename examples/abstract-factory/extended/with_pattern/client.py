from factory import Factory


def operation(factory: Factory) -> tuple[str, str]:
    return factory.first().operation(), factory.second().operation()
