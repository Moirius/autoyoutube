import os
from dotenv import load_dotenv
from openai import OpenAI

# Charger la clé API depuis .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("❌ Clé OPENAI_API_KEY manquante dans le fichier .env")

# Crée un client réutilisable
client = OpenAI(api_key=api_key)
