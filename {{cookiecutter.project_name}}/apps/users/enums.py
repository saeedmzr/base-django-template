from enum import Enum

class UserRoleEnum(Enum):
    ADMIN = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"

    @classmethod
    def choices(cls):
        return [(role.value, role.name.title()) for role in cls]
