import openai
import os
from utils.logger import get_logger

logger = get_logger(__name__)
client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def group_transcript(transcript, window=90, step=45):
    """
    Regroupe la transcription en fenêtres glissantes de taille `window` avec un pas `step`.
    """
    groups = []
    max_end = transcript[-1]["end"]
    current = 0

    while current < max_end:
        chunk = [seg for seg in transcript if current <= seg["start"] < current + window]
        text = " ".join(seg["text"] for seg in chunk)
        if text.strip():
            groups.append({
                "start": current,
                "end": min(current + window, max_end),
                "text": text
            })
        current += step

    return groups

def analyze_transcript(transcript, min_score=0.65):
    """
    Analyse des fenêtres de texte pour détecter les moments forts avec GPT.
    """
    chunks = group_transcript(transcript)
    selected = []

    for chunk in chunks:
        prompt = (
            "Tu es un monteur vidéo. Évalue ce passage pour TikTok : "
            "s'il a du potentiel viral (humour, émotion, surprise), "
            "donne une note de 0 à 1, puis propose un début et une fin de clip cohérent (en secondes). "
            "Réponds seulement sous la forme : score: <score>, start: <secondes>, end: <secondes>\n\n"
            f"Texte:\n{chunk['text']}"
        )

        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=50
            )

            content = response.choices[0].message.content.strip()
            logger.debug(f"📨 Réponse IA : {content}")

            # Extraction des valeurs
            import re
            match = re.search(r'score[:\s]*([0-9.]+).*start[:\s]*([0-9.]+).*end[:\s]*([0-9.]+)', content, re.IGNORECASE)
            if match:
                score = float(match.group(1))
                start = float(match.group(2))
                end = float(match.group(3))
                if score >= min_score and end > start:
                    selected.append({
                        "score": min(score, 1),
                        "start": max(start, 0),
                        "end": end
                    })
                    logger.info(f"🧠 GPT clip validé : {start:.1f}s → {end:.1f}s (score {score:.2f})")
            else:
                logger.warning(f"⚠️ Format inattendu de réponse IA : {content}")

        except Exception as e:
            logger.warning("❌ Erreur GPT lors de l'analyse virale")
            logger.exception(e)

    logger.info(f"✅ {len(selected)} moments viraux retenus.")
    return selected
