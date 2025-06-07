import os
from configgpt.openai_config import client
from utils.logger import get_logger
from utils.prompts import HOOK_PROMPT_TEMPLATE

logger = get_logger(__name__)

def generate_hook(transcript_chunk: str) -> str:
    """
    Utilise l'API OpenAI pour générer un hook (phrase d'accroche) à partir d'un extrait de transcript.
    """
    prompt = HOOK_PROMPT_TEMPLATE.format(transcript_chunk=transcript_chunk)

    model = os.environ.get("HOOK_GPT_MODEL", "gpt-3.5-turbo")
    temperature = float(os.environ.get("HOOK_TEMP", 0.95))

    logger.info("🔮 Génération du hook avec OpenAI")
    logger.debug(f"📜 Prompt envoyé :\n{prompt}")
    logger.debug(f"⚙️ Modèle = {model}, Température = {temperature}")

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=40
        )
        hook_text = response.choices[0].message.content.strip('"').strip()
        logger.info(f"✅ Hook généré : {hook_text}")
        return hook_text
    except Exception as e:
        logger.warning("❌ Échec de l'appel OpenAI, hook vide.")
        logger.exception(e)
        return "Regarde ça 👀"


def generate_caption(transcript_chunk: str, bot_id: str = "bot1") -> str:
    """
    Génère une légende courte à partir du transcript. Pour l’instant, cela retourne juste le hook.
    """
    logger.info(f"🧾 Génération de caption pour {bot_id}")
    return generate_hook(transcript_chunk)


def save_caption(caption: str, slug: str, part_filename: str):
    """
    Enregistre la caption générée dans un fichier texte lié à une partie de vidéo.
    """
    hooks_dir = os.path.join("series", slug, "hooks")
    os.makedirs(hooks_dir, exist_ok=True)

    part_name, _ = os.path.splitext(part_filename)
    path = os.path.join(hooks_dir, f"{part_name}.txt")

    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(caption)
        logger.info(f"✅ Hook sauvegardé : {path}")
    except Exception as e:
        logger.error(f"❌ Impossible de sauvegarder le hook dans : {path}")
        logger.exception(e)
