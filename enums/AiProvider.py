from enum import Enum
from typing import List


class AiProvider(str, Enum):
    OPEN_AI = 'OpenAI'
    ANTHROPIC = 'Anthropic'

    @staticmethod
    def get_all() -> List[str]:
        return [
            AiProvider.OPEN_AI.value,
            AiProvider.ANTHROPIC.value
        ]

    @staticmethod
    def get_by_name(name: str) -> 'AiProvider':
        match name:
            case 'OpenAI':
                return AiProvider.OPEN_AI
            case 'Anthropic':
                return AiProvider.ANTHROPIC
