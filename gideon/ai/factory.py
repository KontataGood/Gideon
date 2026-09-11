from gideon.ai.client import AIClient
from gideon.ai.ollama_client import OllamaClient


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

        raise ValueError(
            f"Unsupported AI provider: {provider}"
        )
