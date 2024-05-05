from enum import Enum
from typing import List

from enums.AiProvider import AiProvider


class AiModels(str, Enum):
    OPEN_AI_GPT_35_TURBO = 'GPT 3.5 Turbo'
    OPEN_AI_GPT_4_TURBO = 'GPT 4.0 Turbo'
    ANTHROPIC_CLAUDE_HAIKU = 'Claude Haiku'
    ANTHROPIC_CLAUDE_SONNET = 'Claude Sonnet'
    ANTHROPIC_CLAUDE_OPUS = 'Claude Opus'

    @staticmethod
    def get_all_by_provider(provider: AiProvider) -> List[str]:
        match provider:
            case AiProvider.OPEN_AI:
                return [
                    AiModels.OPEN_AI_GPT_35_TURBO.value,
                    AiModels.OPEN_AI_GPT_4_TURBO.value,
                ]
            case AiProvider.ANTHROPIC:
                return [
                    AiModels.ANTHROPIC_CLAUDE_HAIKU.value,
                    AiModels.ANTHROPIC_CLAUDE_SONNET.value,
                    AiModels.ANTHROPIC_CLAUDE_OPUS.value,
                ]

    @staticmethod
    def get_tech_name(ai_model: 'AiModels') -> str:
        match ai_model:
            case AiModels.OPEN_AI_GPT_35_TURBO:
                return 'gpt-3.5-turbo'
            case AiModels.OPEN_AI_GPT_4_TURBO:
                return 'gpt-4-turbo'
            case AiModels.ANTHROPIC_CLAUDE_HAIKU:
                return 'claude-3-haiku-20240307'
            case AiModels.ANTHROPIC_CLAUDE_SONNET:
                return 'claude-3-sonnet-20240229'
            case AiModels.ANTHROPIC_CLAUDE_OPUS:
                return 'claude-3-opus-20240229'
