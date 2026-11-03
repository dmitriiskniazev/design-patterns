from typing import Protocol

from formats.json import JsonReader, JsonValidator, JsonWriter
from formats.toml import TomlReader, TomlValidator, TomlWriter
from formats.yaml import YamlReader, YamlValidator, YamlWriter
from interfaces import Reader, Validator, Writer


class SerializationFactory(Protocol):
    def create_writer(self) -> Writer: ...
    def create_reader(self) -> Reader: ...
    def create_validator(self) -> Validator: ...


class JsonFactory:
    def create_writer(self) -> JsonWriter:
        return JsonWriter()

    def create_reader(self) -> JsonReader:
        return JsonReader()

    def create_validator(self) -> JsonValidator:
        return JsonValidator()


class YamlFactory:
    def create_writer(self) -> YamlWriter:
        return YamlWriter()

    def create_reader(self) -> YamlReader:
        return YamlReader()

    def create_validator(self) -> YamlValidator:
        return YamlValidator()


class TomlFactory:
    def create_writer(self) -> TomlWriter:
        return TomlWriter()

    def create_reader(self) -> TomlReader:
        return TomlReader()

    def create_validator(self) -> TomlValidator:
        return TomlValidator()
