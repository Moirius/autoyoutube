import streamlit as st
import os
import json

# Chemin absolu vers custom_prompts.json dans le dossier interface
PROMPT_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "custom_prompts.json"))

DEFAULT_PROMPTS = {
    "STORY_PROMPT_TEMPLATE": """Write a suspense, horror or mystery story in the first person, split into {num_parts} parts.
Only generate part {current_part} now. Be immersive, emotional and engaging. Don't use titles, hashtags or labels.""",

    "STORY_CONTINUATION_TEMPLATE": """Here is the story so far:

{text_so_far}

Now generate part {current_part}, continuing naturally. Avoid repetition and maintain suspense.""",

    "TIKTOK_CAPTION_PROMPT_TEMPLATE": """Tu es un créateur de contenu TikTok.

Voici un extrait de la transcription d’une vidéo. Génére une description TikTok courte (1 seule phrase), percutante, engageante, qui donne envie de regarder jusqu’au bout. Tu peux utiliser des emojis ou des hashtags si c’est pertinent.

Transcript :
"{transcript_chunk}"

→ Donne uniquement la description finale, sans intro ni explication."""
}

def load_prompts():
    if os.path.exists(PROMPT_FILE):
        with open(PROMPT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return DEFAULT_PROMPTS.copy()

def save_prompts(prompts):
    with open(PROMPT_FILE, "w", encoding="utf-8") as f:
        json.dump(prompts, f, indent=2, ensure_ascii=False)

def render_tab():
    st.header("📝 Modifier les Prompts IA")

    prompts = load_prompts()

    st.markdown("#### 🎬 Prompt de départ (première partie)")
    prompts["STORY_PROMPT_TEMPLATE"] = st.text_area(
        "Prompt de départ",
        value=prompts.get("STORY_PROMPT_TEMPLATE", ""),
        height=200
    )

    st.markdown("#### 🔁 Prompt de continuation (parties suivantes)")
    prompts["STORY_CONTINUATION_TEMPLATE"] = st.text_area(
        "Prompt de continuation",
        value=prompts.get("STORY_CONTINUATION_TEMPLATE", ""),
        height=200
    )

    st.markdown("#### 🎯 Prompt pour description TikTok")
    prompts["TIKTOK_CAPTION_PROMPT_TEMPLATE"] = st.text_area(
        "Prompt de description TikTok",
        value=prompts.get("TIKTOK_CAPTION_PROMPT_TEMPLATE", ""),
        height=250
    )
    
    st.markdown("#### 🎣 Prompt de HOOK TikTok")
    prompts["HOOK_PROMPT_TEMPLATE"] = st.text_area(
        "Prompt de hook TikTok",
        value=prompts.get("HOOK_PROMPT_TEMPLATE", ""),
        height=250
    )

    

    if st.button("💾 Enregistrer les prompts"):
        save_prompts(prompts)
        st.success("✅ Prompts enregistrés avec succès dans `interface/custom_prompts.json`.")
