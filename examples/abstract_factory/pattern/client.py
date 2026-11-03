from pattern.factories import SerializationFactory


def write_and_read(
    factory: SerializationFactory, data: dict[str, str]
) -> dict[str, str]:
    writer = factory.create_writer()
    reader = factory.create_reader()
    text = writer.write(data)
    return reader.read(text)


def validate_and_read(factory: SerializationFactory, text: str) -> dict[str, str]:
    validator = factory.create_validator()
    reader = factory.create_reader()
    validator.validate(text)
    return reader.read(text)
