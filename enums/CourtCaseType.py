from enum import Enum


class CourtCaseType(str, Enum):
    CIVIL = 'Civil'
    CRIMINAL = 'Criminal'

    @staticmethod
    def get_all():
        return [
            CourtCaseType.CIVIL.value,
            CourtCaseType.CRIMINAL.value
        ]

    @staticmethod
    def get_by_name(name: str) -> 'CourtCaseType':
        match name:
            case 'Civil':
                return CourtCaseType.CIVIL
            case 'Criminal':
                return CourtCaseType.CRIMINAL
