from enums.AiProvider import AiProvider


class SettingsFormValidator:
    def __init__(self,
                 openai_key: str,
                 anthropic_key: str,
                 supervisor_provider: AiProvider,
                 judge_provider: AiProvider,
                 witness_provider: AiProvider,
                 defense_provider: AiProvider,
                 jury_provider: AiProvider
                 ):
        self.openai_api_key_value = openai_key
        self.anthropic_api_key_value = anthropic_key
        self.supervisor_provider = supervisor_provider
        self.judge_provider = judge_provider
        self.witness_provider = witness_provider
        self.defense_provider = defense_provider
        self.jury_provider = jury_provider

    def validate_api_key(self, key_value: str, provider: AiProvider, provider_name: AiProvider) -> str | None:
        if key_value == '' and provider == provider_name:
            return f"Selected {provider_name.value} provider, but did not provide an API key for it!"
        return None

    def validate_all(self) -> str | None:
        providers = [
            (self.openai_api_key_value, self.supervisor_provider, AiProvider.OPEN_AI),
            (self.anthropic_api_key_value, self.supervisor_provider, AiProvider.ANTHROPIC),
            (self.openai_api_key_value, self.judge_provider, AiProvider.OPEN_AI),
            (self.anthropic_api_key_value, self.judge_provider, AiProvider.ANTHROPIC),
            (self.openai_api_key_value, self.witness_provider, AiProvider.OPEN_AI),
            (self.anthropic_api_key_value, self.witness_provider, AiProvider.ANTHROPIC),
            (self.openai_api_key_value, self.defense_provider, AiProvider.OPEN_AI),
            (self.anthropic_api_key_value, self.defense_provider, AiProvider.ANTHROPIC),
            (self.openai_api_key_value, self.jury_provider, AiProvider.OPEN_AI),
            (self.anthropic_api_key_value, self.jury_provider, AiProvider.ANTHROPIC)
        ]

        for key_value, provider, provider_name in providers:
            message = self.validate_api_key(key_value, provider, provider_name)
            if message is not None:
                return message
        return None
