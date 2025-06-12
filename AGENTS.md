# 🤖 AGENTS.md — Guide pour Codex

## 📦 Structure du projet

Ce dépôt permet de transformer une vidéo YouTube en une série de vidéos TikTok via Streamlit, MoviePy, OpenAI et Whisper.

### Dossiers/fichiers clés :
- `main.py` : exécution du pipeline complet
- `control_center.py` : interface utilisateur principale Streamlit
- `generators/` : logique vidéo et IA :
  - `downloader.py` : téléchargement YouTube (yt-dlp)
  - `transcriber.py` : transcription Whisper
  - `slicer.py` : découpage automatique
  - `description_generator.py` : génération IA de hooks et captions
  - `composer.py` : composition finale avec MoviePy
- `ui/` ou `interface/` :
  - `youtube_to_tiktok_tab.py` : onglet principal de conversion
  - `prompt_editor_tab.py` : onglet pour modifier les prompts
- `utils/` :
  - `logger.py`, `prompts.py`, `run_summary.py` : journalisation, templates, résumé
- `tiktok_caption_generator.py` : génération CLI ou par module des captions TikTok
- `config.py`, `openai_config.py` : gestion des secrets/env
- `custom_prompts.json` : surcharge de prompts (modifié par l’interface)
- `series/` : dossier d'entrée et de traitement
- `videos/exports/` : clips TikTok produits
- `test/` : tests unitaires
- `setup_test_data.py` : génère la vidéo de test localement
- `.env` : contient les clés API et variables d’environnement. pour toi, les api est infos sensibles sont dans tes variables d'environement ou secret, rensigné dans ton interface

---

## 🧪 Tests

### Étape 1 — Créer un fichier vidéo fictif :

```bash
python setup_test_data.py
```

Cela crée un fichier `series/test_rick/original.mp4`.

### Étape 2 — Lancer les tests :

```bash
pytest tests/
```

Ou exécuter unitairement :

```bash
python tests/test_transcriber.py
```

---

## ⚙️ Setup

### Python :
- Version recommandée : `>=3.10`

### Installation des dépendances :

```bash
pip install -r requirements.txt
```

Contient notamment :
```
yt-dlp
moviepy
openai
streamlit
openai-whisper
tqdm
python-dotenv
ffmpeg-python
pillow
```

### Fichier `.env` :

```
OPENAI_API_KEY=sk-...
HOOK_GPT_MODEL=gpt-3.5-turbo
HOOK_TEMP=0.9
TIKTOK_CAPTION_MODEL=gpt-3.5-turbo
TIKTOK_CAPTION_TEMP=0.95
FONT_PATH=assets/font.ttf
HOOK_COLOR=white
```

---

## 📜 Instructions spécifiques à Codex

- ✅ Toujours lancer `setup_test_data.py` avant les tests.
- ✅ Lire les secrets/env depuis `.env` via `dotenv` ou `os.environ`.
- ✅ Utiliser les modules `logger` et `run_summary` pour les logs.
- ✅ Ne pas modifier directement les prompts : passer par `custom_prompts.json` ou `prompt_editor_tab.py`.
- ✅ En cas de modification d’interface : mettre à jour les fichiers `youtube_to_tiktok_tab.py` et `control_center.py`.

---

## 🧠 Exemples de tâches à donner à Codex

### 📌 Refacto

```text
Sépare le code de génération d'overlay texte de composer.py dans un fichier utils/overlay.py
```

### 🧪 Ajout de test

```text
Ajoute un test qui vérifie que transcriber.py produit un fichier .srt valide depuis original.mp4
```

### 🛠️ Fix

```text
Corrige un bug dans slicer.py où un segment vide génère un clip de 0s
```

### 🎨 UI

```text
Ajoute une option dans youtube_to_tiktok_tab.py pour régler le modèle OpenAI utilisé
```

---

## ✅ Setup complet que Codex peut utiliser

```bash
pip install -r requirements.txt
python setup_test_data.py
pytest tests/
```

---

## 📍 Codex CLI

Si tu préfères travailler en local avec Codex CLI :
👉 https://github.com/openai/codex#openai-codex-cli
