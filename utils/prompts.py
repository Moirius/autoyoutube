# utils/prompts.py
import json
from utils.logger import get_logger

logger = get_logger("prompts")

# === PROMPTS PAR DÉFAUT ===

HOOK_PROMPT_TEMPLATE = """
Tu es un expert en création de vidéos virales sur TikTok.
À partir d’une transcription, génère un HOOK de 4 à 6 mots maximum, au ton humoristique, dans le style TikTok (parfois absurde, parfois accrocheur).
Ton objectif est d’intriguer, surprendre ou faire rire, tout en restant court et cliquable.

Voici la transcription :
{transcript_chunk}

Exemples de bons hooks :
- "Ce qu’Ikea ne vous dira jamais"
- "J’ai failli perdre un doigt à cause de ça"
- "Pourquoi il a mis des vis dans son canapé ?"
- "L’astuce débile qui a tout changé"
- "Même les vendeurs étaient choqués"

Génère maintenant un seul hook TikTok accrocheur :
"""

CAPTION_PROMPT_TEMPLATE = """
Tu es un créateur de contenu TikTok.

Voici un extrait de la transcription d'une vidéo. Génére une **description TikTok courte** (1 phrase max), engageante et adaptée à la plateforme (avec emojis ou hashtags si pertinent).

Transcript :
"{transcript_chunk}"

→ Ta réponse :
""".strip()

STORY_PROMPT_TEMPLATE = """
You are writing a suspense, horror or mystery story in the first person for TikTok.

The story must be split into {num_parts} parts.
Generate only part {current_part} now.

⟶ First line = short and catchy story title (do NOT write “Part X”)
⟶ Then skip a line and write the immersive story narration (plain text, 90–120 words).

Do NOT include:
- Hashtags, labels, or brackets
- Camera directions or Voiceover:
- Rhetorical asides or "you"

✅ End on an **in-world cliffhanger** (e.g. a sound, a discovery).
""".strip()

STORY_CONTINUATION_TEMPLATE = """Here is the story so far:

{text_so_far}

Continue with part {current_part}, still in first person.

⟶ Do NOT repeat the title.
⟶ Ignore the original title and continue the narrative seamlessly.
⟶ Do NOT include Voiceover:, stage directions, hashtags, labels or brackets.
⟶ Use plain narrated text only. {ending_instruction}

✅ End on an in-story cliffhanger (90–120 words).
""".strip()

TIKTOK_CAPTION_PROMPT_TEMPLATE = """
Tu es un créateur de contenu TikTok.

Voici un extrait de la transcription d’une vidéo. Génére une description TikTok courte (1 seule phrase), percutante, engageante, qui donne envie de regarder jusqu’au bout. Tu peux utiliser des emojis ou des hashtags si c’est pertinent.

Transcript :
"{transcript_chunk}"

→ Donne uniquement la description finale, sans intro ni explication.
""".strip()

# === CHARGEMENT PERSONNALISÉ ===

try:
    with open("custom_prompts.json", "r", encoding="utf-8") as f:
        custom = json.load(f)
        STORY_PROMPT_TEMPLATE = custom.get("STORY_PROMPT_TEMPLATE", STORY_PROMPT_TEMPLATE)
        STORY_CONTINUATION_TEMPLATE = custom.get("STORY_CONTINUATION_TEMPLATE", STORY_CONTINUATION_TEMPLATE)
        HOOK_PROMPT_TEMPLATE = custom.get("HOOK_PROMPT_TEMPLATE", HOOK_PROMPT_TEMPLATE)
        CAPTION_PROMPT_TEMPLATE = custom.get("CAPTION_PROMPT_TEMPLATE", CAPTION_PROMPT_TEMPLATE)
        TIKTOK_CAPTION_PROMPT_TEMPLATE = custom.get("TIKTOK_CAPTION_PROMPT_TEMPLATE", TIKTOK_CAPTION_PROMPT_TEMPLATE)
        logger.info("📥 Prompts personnalisés chargés depuis custom_prompts.json")
except FileNotFoundError:
    logger.info("📄 Aucun fichier custom_prompts.json trouvé — utilisation des prompts par défaut")
