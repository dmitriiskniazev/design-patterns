def validate_data(data: object) -> None:
    if not isinstance(data, dict) or not all(
        isinstance(key, str) and isinstance(value, str) for key, value in data.items()
    ):
        raise ValueError("Expected a dictionary with string keys and values")
