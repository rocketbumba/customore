from enum import StrEnum, auto


class ResponseCode(StrEnum):
    SUCCESS = auto()
    INVALID_REQUEST = auto()
    UNKNOWN_ERROR = auto()
    TASK_NOT_FOUND = auto()