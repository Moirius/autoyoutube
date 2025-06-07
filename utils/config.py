import os
import json
from dotenv import load_dotenv

load_dotenv()
CONFIG_PATH = os.path.join("bots", "config.json")

def load_config():
    with open(CONFIG_PATH, encoding="utf-8") as f:
        return json.load(f)

def get_api_key():
    return os.getenv("OPENAI_API_KEY")
