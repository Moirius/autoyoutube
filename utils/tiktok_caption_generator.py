import os
import json
from configgpt.openai_config import client
from utils.logger import get_logger
from utils.prompts import TIKTOK_CAPTION_PROMPT_TEMPLATE  # Chargé depuis custom_prompts.json

logger = get_logger("tiktok_caption_gen")

def load_transcript_chunk(slug: str, part: int, is_ai_story: bool = False) -> str | None:
    """
    Charge uniquement le texte de la partie demandée (pour éviter de surcharger OpenAI).
    """
    if is_ai_story:
        path = f"histoires/{slug}/transcripts/part{part}_words.json"
        logger.info(f"📄 Chargement transcript IA : {path}")
        if not os.path.exists(path):
            logger.error(f"❌ Transcript IA manquant : {path}")
            return None
        with open(path, "r", encoding="utf-8") as f:
            segments = json.load(f)
        words = [w["word"] for seg in segments for w in seg.get("words", [])]
        text = " ".join(words)
        logger.info(f"✅ Transcript IA chargé ({len(text)} caractères)")
        return text
    else:
        transcript_path = f"series/{slug}/transcript.json"
        segments_path = f"series/{slug}/segments.json"

        logger.info(f"📄 Chargement transcript YouTube : {transcript_path}")
        if not os.path.exists(transcript_path) or not os.path.exists(segments_path):
            logger.error(f"❌ Fichier manquant : transcript.json ou segments.json")
            return None

        with open(transcript_path, "r", encoding="utf-8") as f:
            transcript = json.load(f)

        with open(segments_path, "r", encoding="utf-8") as f:
            segments = json.load(f)

        if part - 1 >= len(segments):
            logger.error(f"❌ Partie {part} introuvable dans segments.json")
            return None

        start = segments[part - 1]["start"]
        end = segments[part - 1]["end"]

        text = " ".join([s["text"] for s in transcript if start <= s["start"] < end])
        logger.info(f"✅ Transcript extrait pour part {part} ({len(text)} caractères)")
        return text


def generate_tiktok_caption(transcript_chunk: str, prompt_template: str = None) -> str:
    if not prompt_template:
        prompt_template = TIKTOK_CAPTION_PROMPT_TEMPLATE

    prompt = prompt_template.format(transcript_chunk=transcript_chunk)
    model = os.environ.get("TIKTOK_CAPTION_MODEL", "gpt-3.5-turbo")
    temperature = float(os.environ.get("TIKTOK_CAPTION_TEMP", 0.95))

    logger.info("🧠 Génération description TikTok avec OpenAI")
    logger.debug(f"📤 Prompt envoyé : {prompt[:500]}...")
    logger.debug(f"⚙️ Modèle : {model} | Température : {temperature}")

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=60
        )
        caption = response.choices[0].message.content.strip()
        logger.info(f"✅ Caption générée : {caption}")
        return caption
    except Exception as e:
        logger.warning("⚠️ Échec de génération de description TikTok.")
        logger.exception(e)
        return "Découvre ce moment incroyable... 👀"

def save_caption(slug: str, part: int, caption: str):
    output_path = f"videos/exports/{slug}/part{part}_caption.txt"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(caption)
        logger.info(f"💾 Caption TikTok sauvegardée dans : {output_path}")
    except Exception as e:
        logger.error(f"❌ Erreur sauvegarde caption : {output_path}")
        logger.exception(e)

def generate_and_save_caption(slug: str, part: int, is_ai_story: bool = False):
    logger.info(f"🚀 Génération TikTok caption | slug={slug} | part={part} | IA={is_ai_story}")
    transcript = load_transcript_chunk(slug, part, is_ai_story)
    if not transcript:
        logger.warning("🚫 Aucune donnée de transcript à traiter.")
        return
    caption = generate_tiktok_caption(transcript)
    save_caption(slug, part, caption)

# Utilisation en CLI
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--slug", required=True)
    parser.add_argument("--part", type=int, required=True)
    parser.add_argument("--ai", action="store_true", help="Traite comme une histoire IA")
    args = parser.parse_args()

    generate_and_save_caption(args.slug, args.part, is_ai_story=args.ai)
