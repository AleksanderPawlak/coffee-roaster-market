import io

from typing import Optional, Iterable
from rest_framework.parsers import JSONParser


def parse_json_data(json_data: bytes) -> dict:
    stream = io.BytesIO(json_data)
    return JSONParser().parse(stream)


def compare_dicts(
    value: dict, expected_value: dict, exclude_fields: Optional[Iterable[str]] = None
) -> None:
    exclude_fields = exclude_fields or []
    keys = (key for key in expected_value if key not in exclude_fields)
    for key in keys:
        assert value[key] == expected_value[key]
