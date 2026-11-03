import json
import tomllib

import pytest
import yaml
from baseline.client import Format
from baseline.client import validate_and_read as baseline_validate_and_read
from baseline.client import write_and_read as baseline_write_and_read
from formats.json import JsonValidator, JsonWriter
from pattern.client import validate_and_read, write_and_read
from pattern.factories import (
    JsonFactory,
    SerializationFactory,
    TomlFactory,
    YamlFactory,
)


@pytest.mark.parametrize(
    ("format", "factory"),
    [
        (Format.JSON, JsonFactory()),
        (Format.YAML, YamlFactory()),
        (Format.TOML, TomlFactory()),
    ],
)
@pytest.mark.parametrize(
    "data",
    [
        {},
        {"message": "hello"},
        {"message": 'Привет "мир"\nВторая строка\t\\', "true": "001", "empty": ""},
    ],
)
def test_both_approaches_restore_data(
    format: Format, factory: SerializationFactory, data: dict[str, str]
) -> None:
    original = data.copy()
    text = factory.create_writer().write(data)
    assert baseline_validate_and_read(format, text) == original
    assert validate_and_read(factory, text) == original
    assert baseline_write_and_read(format, data) == original
    assert write_and_read(factory, data) == original
    assert data == original


def test_client_uses_products_from_the_supplied_factory() -> None:
    events: list[str] = []
    data = {"message": "hello"}

    class Writer:
        def write(self, value: dict[str, str]) -> str:
            assert value == data
            events.append("write")
            return "encoded"

    class Reader:
        def read(self, text: str) -> dict[str, str]:
            assert text == "encoded"
            events.append("read")
            return data

    class Factory:
        def create_validator(self) -> JsonValidator:
            return JsonValidator()

        def create_writer(self) -> Writer:
            events.append("create_writer")
            return Writer()

        def create_reader(self) -> Reader:
            events.append("create_reader")
            return Reader()

    assert write_and_read(Factory(), data) == data
    assert events == ["create_writer", "create_reader", "write", "read"]


@pytest.mark.parametrize(
    ("format", "factory", "text"),
    [
        (Format.JSON, JsonFactory(), '{"message": "hello"}'),
        (Format.YAML, YamlFactory(), "message: hello"),
        (Format.TOML, TomlFactory(), 'message = "hello"'),
    ],
)
def test_both_clients_validate_and_read(
    format: Format, factory: SerializationFactory, text: str
) -> None:
    assert baseline_validate_and_read(format, text) == {"message": "hello"}
    assert validate_and_read(factory, text) == {"message": "hello"}


@pytest.mark.parametrize(
    ("format", "factory", "text"),
    [
        (Format.JSON, JsonFactory(), '{"message": 1}'),
        (Format.JSON, JsonFactory(), "[]"),
        (Format.YAML, YamlFactory(), "message: true"),
        (Format.YAML, YamlFactory(), "- hello"),
        (Format.YAML, YamlFactory(), "1: hello"),
        (Format.YAML, YamlFactory(), ""),
        (Format.TOML, TomlFactory(), "message = 1"),
        (Format.TOML, TomlFactory(), '[message]\ntext = "hello"'),
    ],
)
def test_valid_syntax_with_wrong_structure_is_rejected(
    format: Format, factory: SerializationFactory, text: str
) -> None:
    for read in (
        lambda: baseline_validate_and_read(format, text),
        lambda: validate_and_read(factory, text),
    ):
        with pytest.raises(ValueError, match="string keys and values"):
            read()


@pytest.mark.parametrize(
    ("format", "factory", "text", "error"),
    [
        (Format.JSON, JsonFactory(), '{"message":', json.JSONDecodeError),
        (Format.YAML, YamlFactory(), "message: [", yaml.YAMLError),
        (Format.TOML, TomlFactory(), "message = [", tomllib.TOMLDecodeError),
    ],
)
def test_syntax_errors_are_not_hidden(
    format: Format, factory: SerializationFactory, text: str, error: type[Exception]
) -> None:
    with pytest.raises(error):
        baseline_validate_and_read(format, text)
    with pytest.raises(error):
        validate_and_read(factory, text)


@pytest.mark.parametrize("reject", [False, True])
def test_reader_is_called_only_after_successful_validation(reject: bool) -> None:
    events: list[str] = []

    class Validator:
        def validate(self, text: str) -> None:
            assert text == "input"
            events.append("validate")
            if reject:
                raise ValueError("rejected")

    class Reader:
        def read(self, text: str) -> dict[str, str]:
            assert text == "input"
            events.append("read")
            return {"message": "hello"}

    class Factory:
        def create_validator(self) -> Validator:
            return Validator()

        def create_reader(self) -> Reader:
            return Reader()

        def create_writer(self) -> JsonWriter:
            return JsonWriter()

    if reject:
        with pytest.raises(ValueError, match="rejected"):
            validate_and_read(Factory(), "input")
        assert events == ["validate"]
    else:
        assert validate_and_read(Factory(), "input") == {"message": "hello"}
        assert events == ["validate", "read"]
