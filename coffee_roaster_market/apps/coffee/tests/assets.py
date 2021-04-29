import io

from rest_framework.parsers import JSONParser


def parse_json_data(json_data: bytes) -> dict:
    stream = io.BytesIO(json_data)
    return JSONParser().parse(stream)
