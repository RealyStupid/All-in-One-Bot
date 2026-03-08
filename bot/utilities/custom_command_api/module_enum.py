from enum import Enum

class ModuleEnum(Enum):
    TEST_ENUM = "test"
    MODERATION = "moderation"

    @classmethod
    def list(cls):
        return [m.value for m in cls]