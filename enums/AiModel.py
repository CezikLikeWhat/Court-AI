from enum import Enum
from typing import List

from enums.AiProvider import AiProvider


class AiModel(str, Enum):
    OPEN_AI_GPT_35_TURBO = 'GPT 3.5 Turbo'
    OPEN_AI_GPT_4_TURBO = 'GPT 4.0 Turbo'
    OPEN_AI_GPT_4_O = 'GPT 4.0 Omni'
    ANTHROPIC_CLAUDE_HAIKU = 'Claude Haiku'
    ANTHROPIC_CLAUDE_SONNET = 'Claude Sonnet'
    ANTHROPIC_CLAUDE_OPUS = 'Claude Opus'

    @classmethod
    def get_all_by_provider(cls, provider: AiProvider) -> List[str]:
        model_map = {
            AiProvider.OPEN_AI: [
                cls.OPEN_AI_GPT_35_TURBO.value,
                cls.OPEN_AI_GPT_4_TURBO.value,
                cls.OPEN_AI_GPT_4_O.value
            ],
            AiProvider.ANTHROPIC: [
                cls.ANTHROPIC_CLAUDE_HAIKU.value,
                cls.ANTHROPIC_CLAUDE_SONNET.value,
                cls.ANTHROPIC_CLAUDE_OPUS.value,
            ],
        }
        return model_map.get(provider, [])

    @classmethod
    def get_tech_name(cls, ai_model: 'AiModel') -> str:
        tech_name_map = {
            cls.OPEN_AI_GPT_35_TURBO: 'gpt-3.5-turbo',
            cls.OPEN_AI_GPT_4_TURBO: 'gpt-4-turbo',
            cls.OPEN_AI_GPT_4_O: 'gpt-4o',
            cls.ANTHROPIC_CLAUDE_HAIKU: 'claude-3-haiku-20240307',
            cls.ANTHROPIC_CLAUDE_SONNET: 'claude-3-sonnet-20240229',
            cls.ANTHROPIC_CLAUDE_OPUS: 'claude-3-opus-20240229',
        }
        return tech_name_map.get(ai_model, '')

    @classmethod
    def index_of(cls, model: 'AiModel', provider: AiProvider) -> int:
        try:
            return cls.get_all_by_provider(provider).index(model)
        except ValueError:
            return 0
