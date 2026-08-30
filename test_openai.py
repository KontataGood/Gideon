from dotenv import load_dotenv
import os

from gideon.ai.openai_client import OpenAIClient


def main():
    load_dotenv()

    api_key = os.getenv("GIDEON_AI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GIDEON_AI_API_KEY is missing."
        )

    client = OpenAIClient(
        api_key=api_key,
        model="gpt-5.2",
    )

    response = client.chat(
        messages=[
            {
                "role": "user",
                "content": "Ответь одним словом: привет",
            }
        ]
    )

    print("Response:", response)


if __name__ == "__main__":
    main()