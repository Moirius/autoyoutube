import streamlit as st
import sys
import os

# Ajoute le chemin racine au path pour accéder à utils/ depuis interface/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import des deux modules que tu veux garder
from ui.youtube_to_tiktok_tab import render_tab as render_yttt_tab
from ui.prompt_editor_tab import render_tab as render_prompt_tab

# Onglets
tab1, tab2 = st.tabs([
    "🎬 YouTube → TikTok",
    "📝 Prompts IA"
])

# Affichage des contenus
with tab1:
    render_yttt_tab()

with tab2:
    render_prompt_tab()
