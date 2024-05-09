import os

import anthropic
import openai
from anthropic import Anthropic


class ApiKeyValidator:

    @staticmethod
    def is_valid_open_ai_key(key: str) -> str | None:
        if os.getenv('APP_ENV') == 'debug':
            return None

        client = openai.OpenAI(api_key=key)
        try:
            client.models.list()
            return None
        except openai.APIError as e:
            if isinstance(e.body, dict):
                message = f'Error(OpenAI): {e.body['message']}'
                return message

            return 'Error(OpenAI): Unknown API error'

    @staticmethod
    def is_valid_anthropic_key(key: str) -> str | None:
        if os.getenv('APP_ENV') == 'debug':
            return None

        client = Anthropic(api_key=key)
        try:
            client.messages.create(
                max_tokens=1,
                messages=[
                    {
                        "role": "user",
                        "content": "Test",
                    }
                ],
                model="claude-instant-1.2",
            )
            return None
        except anthropic.APIError as e:
            if isinstance(e.body, dict):
                message = f'Error(Anthropic): {e.body['error']['message']}'
                return message

            return 'Error(Anthropic): Unknown API error'
