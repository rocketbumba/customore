from enum import Enum, auto


class TaskStatus(Enum):
    COMPLETED = auto()
    PENDING = auto()

    @classmethod
    def choices(cls):
        return [(item.value, item.name) for item in cls]