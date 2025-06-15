import os
import re
from utils.logger import get_logger
from configgpt.openai_config import client

logger = get_logger(__name__)

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


def heuristic_score(text: str) -> float:
    """Retourne un score de viralité basé uniquement sur le texte."""
    score = 0.0
    lower = text.lower()

    # Ponctuation expressive
    punct_count = text.count("!") + text.count("?")
    score += min(punct_count * 0.1, 0.3)

    # Mots clés typiques de réactions fortes
    keywords = {
        "incroyable": 0.25,
        "wow": 0.25,
        "génial": 0.2,
        "impressionnant": 0.2,
        "hilarant": 0.25,
        "surprenant": 0.2,
        "dingue": 0.2,
        "ouf": 0.2,
    }
    for word, weight in keywords.items():
        if word in lower:
            score += weight

    # Longueur et rythme
    words = len(re.findall(r"\w+", text))
    if 10 <= words <= 80:
        score += 0.2
    score += min(words / 100.0, 0.2)

    # Mise en avant (MAJUSCULES)
    if text:
        upper_ratio = sum(c.isupper() for c in text) / len(text)
        score += min(upper_ratio * 2, 0.2)

    return min(score, 1.0)

def analyze_transcript(transcript, min_score=0.65, max_segments=5):
    """Analyse la transcription et renvoie les meilleurs segments.

    Si l'API OpenAI est disponible, celle-ci est sollicitée pour noter chaque
    passage. En cas d'échec ou si l'API est désactivée, une heuristique locale
    prend le relais. Les segments sont ensuite triés par score et filtrés pour
    éviter les chevauchements.
    """
    chunks = group_transcript(transcript)
    candidates = []

    use_ai = os.getenv("MOCK_OPENAI", "false").lower() != "true"

    for chunk in chunks:
        if use_ai:
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
                    max_tokens=50,
                )

                content = response.choices[0].message.content.strip()
                logger.debug(f"📨 Réponse IA : {content}")

                match = re.search(
                    r'score[:\s]*([0-9.]+).*start[:\s]*([0-9.]+).*end[:\s]*([0-9.]+)',
                    content,
                    re.IGNORECASE,
                )
                if match:
                    score = float(match.group(1))
                    start = float(match.group(2))
                    end = float(match.group(3))
                    if score >= min_score and end > start:
                        candidates.append(
                            {
                                "score": min(score, 1),
                                "start": max(start, 0),
                                "end": end,
                            }
                        )
                        logger.info(
                            f"🧠 GPT clip validé : {start:.1f}s → {end:.1f}s (score {score:.2f})"
                        )
                    continue
                else:
                    logger.warning(
                        f"⚠️ Format inattendu de réponse IA : {content}"
                    )
            except Exception as e:
                logger.warning("❌ Erreur GPT lors de l'analyse virale")
                logger.exception(e)

        # Fallback heuristique
        score = heuristic_score(chunk["text"])
        if score >= min_score:
            candidates.append(
                {
                    "score": score,
                    "start": chunk["start"],
                    "end": chunk["end"],
                }
            )
            logger.info(
                f"✨ Heuristique clip {chunk['start']:.1f}s → {chunk['end']:.1f}s (score {score:.2f})"
            )

    # Tri par score et suppression des chevauchements
    candidates.sort(key=lambda c: c["score"], reverse=True)
    selected = []
    for cand in candidates:
        if len(selected) >= max_segments:
            break
        overlap = any(not (cand["end"] <= s["start"] or cand["start"] >= s["end"]) for s in selected)
        if not overlap:
            selected.append(cand)

    logger.info(f"✅ {len(selected)} moments viraux retenus.")
    return selected
