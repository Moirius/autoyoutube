import os
from dotenv import load_dotenv

load_dotenv()

if os.getenv("MOCK_OPENAI", "false").lower() == "true":
    print("🧪 Mode MOCK : OpenAI désactivé, client simulé")
    
    class FakeOpenAI:
        def __init__(self, *args, **kwargs):
            pass

        class Chat:
            class Completions:
                @staticmethod
                def create(**kwargs):
                    print("🔁 Simulation OpenAI - prompt reçu :")
                    print(kwargs.get("messages", [{}])[0].get("content", ""))
                    class Choice:
                        message = type("msg", (), {"content": '"Ceci est un mock 👻"'})
                    return type("Resp", (), {"choices": [Choice()]})

            completions = Completions()

        chat = Chat()

    client = FakeOpenAI()
else:
    from openai import OpenAI
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("❌ Clé OPENAI_API_KEY manquante dans .env")
    client = OpenAI(api_key=api_key)
