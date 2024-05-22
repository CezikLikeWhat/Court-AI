from enum import Enum
from typing import List


class AiProvider(str, Enum):
    OPEN_AI = 'OpenAI'
    ANTHROPIC = 'Anthropic'
    OLLAMA = 'Ollama'

    @classmethod
    def get_all(cls: 'AiProvider') -> List[str]:
        return [
            AiProvider.OPEN_AI.value,
            AiProvider.ANTHROPIC.value,
            AiProvider.OLLAMA.value
        ]

    @classmethod
    def get_by_name(cls, name: str) -> 'AiProvider':
        return cls[name.upper()]

    @classmethod
    def index_of(cls, name: str) -> int:
        try:
            provider = cls.get_by_name(name)
            return cls.get_all().index(provider.value)
        except (KeyError, ValueError):
            return 0
