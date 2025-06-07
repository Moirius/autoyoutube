import streamlit as st
import os
import subprocess
import sys
from utils.logger import get_logger

logger = get_logger("YT_Tab")

# 🔧 Spécifie ici ton exécutable Python utilisé pour lancer le pipeline
PYTHON_EXECUTABLE_PATH = r"D:\betisespython\tiktokbot\venv\Scripts\python.exe"

def run_command(label, command_list, env_vars=None):
    st.markdown(f"### ▶️ {label}")
    st.code(" ".join(command_list))

    if env_vars:
        logger.info(f"🧪 [{label}] Variables d'environnement utilisées :")
        with st.expander("📋 Paramètres utilisés (debug)"):
            for key, val in env_vars.items():
                os.environ[key] = str(val)
                st.write(f"**{key}** = {val}")
                logger.info(f"   {key} = {val}")

    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    subprocess.Popen(command_list, cwd=project_root, env=os.environ.copy())

def render_tab():
    st.header("🎬 Pipeline YouTube → TikTok")

    yt_url = st.text_input("URL YouTube")
    slug = st.text_input("Nom du projet (slug)", value="yt_1")

    st.markdown("### 🎛️ Paramètres personnalisables")
    whisper_model = st.selectbox("Modèle Whisper", ["tiny", "small", "medium", "large"], index=1)
    min_dur = st.slider("Durée minimale du clip (s)", 10, 90, 45)
    max_dur = st.slider("Durée maximale du clip (s)", 30, 150, 75)
    gpt_model = st.selectbox("Modèle GPT pour le hook", ["gpt-3.5-turbo", "gpt-4"], index=0)
    font_path = st.text_input("Police (TTF)", value="fonts/BebasNeue-Regular.ttf")
    hook_font_size = st.slider("Taille du texte hook", 24, 72, 42)
    part_font_size = st.slider("Taille du badge Partie", 24, 72, 38)
    hook_color = st.color_picker("Couleur texte hook", "#000000")
    badge_color = st.color_picker("Couleur badge Partie", "#C84628")
    part_text_color = st.color_picker("Couleur texte Partie", "#FFFFFF")
    hook_bg_color = st.color_picker("Couleur fond Hook", "#FFFFFF")
    hook_y = st.slider("Position verticale texte hook (px)", 0, 1280, 590)
    badge_y = st.slider("Position verticale badge Partie (px)", 0, 1280, 640)

    # 🔍 Tester environnement Python
    if st.button("🧪 Tester l’environnement Python"):
        test_script = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "print_env.py"))
        command = [PYTHON_EXECUTABLE_PATH, test_script]
        run_command("Test Environnement Python", command)

    # 🚀 Lancer pipeline
    if st.button("🚀 Lancer le pipeline complet"):
        yt_url_clean = yt_url.strip()
        slug_clean = slug.strip()

        if not yt_url_clean or not slug_clean:
            st.error("❗ Veuillez remplir l'URL YouTube et le nom du projet (slug).")
            return

        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        main_path = os.path.join(project_root, "main.py")

        if not os.path.exists(main_path):
            st.error(f"❌ Fichier main.py introuvable à : {main_path}")
            return

        command = [PYTHON_EXECUTABLE_PATH, main_path, yt_url_clean, slug_clean]

        env = {
            "WHISPER_MODEL": whisper_model,
            "MIN_DUR": min_dur,
            "MAX_DUR": max_dur,
            "HOOK_GPT_MODEL": gpt_model,
            "FONT_PATH": font_path,
            "HOOK_FONT_SIZE": hook_font_size,
            "PART_FONT_SIZE": part_font_size,
            "HOOK_COLOR": hook_color,
            "BADGE_COLOR": badge_color,
            "PART_TEXT_COLOR": part_text_color,
            "HOOK_BG_COLOR": hook_bg_color,
            "HOOK_Y": hook_y,
            "BADGE_Y": badge_y,
        }

        run_command("Lancement pipeline complet", command, env)
