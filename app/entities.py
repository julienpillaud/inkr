from enum import IntEnum


class MaterialStatus(IntEnum):
    INACTIVE = 0
    ACTIVE = 1
    UNKNOWN = 2


class MixtureStatus(IntEnum):
    IN_PROGRESS = 0
    ERROR = 1
    ABORTED = 2
    SUCCESS = 3


class RecipeStatus(IntEnum):
    INACTIVE = 0
    ACTIVE = 1
    UNKNOWN = 2


class RecipeVersionStatus(IntEnum):
    INACTIVE = 0
    ACTIVE = 1
