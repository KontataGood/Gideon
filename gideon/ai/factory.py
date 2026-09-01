from gideon.ai.client import AIClient
from gideon.ai.ollama_client import OllamaClient
from gideon.ai.openai_client import OpenAIClient


class AIFactory:
    @staticmethod
    def create_client(
        provider: str,
        model: str,
        api_key: str | None = None,
    ) -> AIClient:

        provider = provider.lower()

        if provider == "ollama":
            return OllamaClient(model=model)

        if provider == "openai":
            if not api_key:
                raise RuntimeError(
                    "GIDEON_AI_API_KEY is not configured."
                )

            return OpenAIClient(
                api_key=api_key,
                model=model,
            )

        raise ValueError(
            f"Unsupported AI provider: {provider}"
        )