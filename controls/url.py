from enum import Enum
from typing import Optional


class URL(Enum):
    ORIGIN = "http://localhost:8000"
    BERT = "qa"
    UPLOAD = "uploadfile"


def url(part: Optional[URL]) -> str:
    match part:
        case URL.BERT:
            return "/".join([URL.ORIGIN.value, URL.BERT.value])
        case URL.UPLOAD:
            return "/".join([URL.ORIGIN.value, URL.UPLOAD.value])
        case _:
            return "http://localhost:8000"
