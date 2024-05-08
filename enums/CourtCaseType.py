from enum import Enum
from typing import List


class CourtCaseType(str, Enum):
    CIVIL = 'Civil'
    CRIMINAL = 'Criminal'

    @classmethod
    def get_all(cls) -> List[str]:
        return [member.value for member in cls]

    @classmethod
    def get_by_name(cls, name: str) -> 'CourtCaseType':
        return cls[name.upper()]

    @classmethod
    def index_of(cls, name: str) -> int:
        try:
            return cls.get_all().index(cls.get_by_name(name).value)
        except (KeyError, ValueError):
            return 0
