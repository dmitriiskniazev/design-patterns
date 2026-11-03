import json
from typing import cast

from validation import validate_data


class JsonReader:
    def read(self, text: str) -> dict[str, str]:
        return cast(dict[str, str], json.loads(text))


class JsonWriter:
    def write(self, data: dict[str, str]) -> str:
        return json.dumps(data, ensure_ascii=False)


class JsonValidator:
    def validate(self, text: str) -> None:
        validate_data(json.loads(text))
