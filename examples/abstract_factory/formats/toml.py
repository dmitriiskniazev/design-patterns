import tomllib
from typing import cast

import tomli_w
from validation import validate_data


class TomlReader:
    def read(self, text: str) -> dict[str, str]:
        return cast(dict[str, str], tomllib.loads(text))


class TomlWriter:
    def write(self, data: dict[str, str]) -> str:
        return tomli_w.dumps(data)


class TomlValidator:
    def validate(self, text: str) -> None:
        validate_data(tomllib.loads(text))
