import os

from gideon.ai.client import AIClient
from gideon.ai.mock_client import MockAIClient
from gideon.ai.openai_client import OpenAIClient


class AIFactory:
    """
    Создаёт AI-клиент Gideon.
    """

    @staticmethod
    def create_client(
        provider: str = "mock",
        model: str = "test",
    ) -> AIClient:

        if provider == "mock":
            return MockAIClient()

        if provider == "openai":
            api_key = os.getenv(
                "GIDEON_AI_API_KEY"
            )

            if not api_key:
                raise RuntimeError(
                    "GIDEON_AI_API_KEY is not configured."
                )

            return OpenAIClient(
                api_key=api_key,
                model=model,
            )

        raise ValueError(
            f"Unknown AI provider: {provider}"
        )