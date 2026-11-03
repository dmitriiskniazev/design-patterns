from typing import cast

import yaml
from validation import validate_data


class YamlReader:
    def read(self, text: str) -> dict[str, str]:
        return cast(dict[str, str], yaml.safe_load(text))


class YamlWriter:
    def write(self, data: dict[str, str]) -> str:
        return yaml.safe_dump(data, allow_unicode=True)


class YamlValidator:
    def validate(self, text: str) -> None:
        validate_data(yaml.safe_load(text))
