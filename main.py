from dotenv import load_dotenv

from gideon.core.assistant import Gideon


def main():
    load_dotenv()

    gideon = Gideon()
    gideon.start()

    print()
    print("Type 'exit' or 'quit' to stop.")
    print()

    while gideon.running:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            if user_input.lower() in {"exit", "quit"}:
                break

            response = gideon.agent.process(user_input)

            print(f"Gideon: {response}")
            print()

        except KeyboardInterrupt:
            print("\n")

            break

        except Exception as e:
            print(f"Error: {e}")

    gideon.stop()


if __name__ == "__main__":
    main()