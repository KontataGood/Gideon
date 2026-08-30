from gideon.core.assistant import Gideon
from dotenv import load_dotenv

load_dotenv()

def main():
    gideon = Gideon()

    print(
        "Name:",
        gideon.config.get("assistant.name")
    )

    print(
        "Language:",
        gideon.config.get("assistant.language")
    )

    print(
        "Provider:",
        gideon.config.get("ai.provider")
    )

    print(
        "Model:",
        gideon.config.get("ai.model")
    )


if __name__ == "__main__":
    main()