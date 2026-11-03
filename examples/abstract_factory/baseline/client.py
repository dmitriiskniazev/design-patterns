from enum import StrEnum

from formats.json import JsonReader, JsonValidator, JsonWriter
from formats.toml import TomlReader, TomlValidator, TomlWriter
from formats.yaml import YamlReader, YamlValidator, YamlWriter
from interfaces import Reader, Validator, Writer


class Format(StrEnum):
    JSON = "json"
    YAML = "yaml"
    TOML = "toml"


def write_and_read(format: Format, data: dict[str, str]) -> dict[str, str]:
    writer: Writer
    reader: Reader
    match format:
        case Format.JSON:
            writer, reader = JsonWriter(), JsonReader()
        case Format.YAML:
            writer, reader = YamlWriter(), YamlReader()
        case Format.TOML:
            writer, reader = TomlWriter(), TomlReader()
    text = writer.write(data)
    return reader.read(text)


def validate_and_read(format: Format, text: str) -> dict[str, str]:
    validator: Validator
    reader: Reader
    match format:
        case Format.JSON:
            validator, reader = JsonValidator(), JsonReader()
        case Format.YAML:
            validator, reader = YamlValidator(), YamlReader()
        case Format.TOML:
            validator, reader = TomlValidator(), TomlReader()
    validator.validate(text)
    return reader.read(text)
