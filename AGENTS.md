# 🤖 Mode Codex / Simulation locale

Ce projet est prêt à être utilisé avec Codex ou un agent IA (sans accès Internet ou API réelles).

## 🥪 Simulation avec données mock

Utilisez les fichiers suivants pour tester sans télécharger de vidéo ni appeler l'API OpenAI :

* `test_data/mock_transcript.txt` : transcript texte simulé
* `test_data/mock_segmets.json` : segments vidéo simulés
* `test_data/mock_part1.png`, `test_data/mock_part2.png` : images utilisées à la place de vidéos

## 📆 Installation sans accès Internet

Codex peut installer les dépendances via le script suivant :

```bash
bash setup.sh
```

Ce script installe les dépendances Python à partir des fichiers `.whl` déjà présents dans le dossier `libs/`.

## 🧱 Contenu attendu du dossier `libs/`

```
libs/
├── moviepy-1.0.3-py3-none-any.whl
├── pillow-9.5.0-py3-none-any.whl
├── numpy-1.24.x-*.whl
├── tqdm-4.65.0-py3-none-any.whl
├── decorator-4.x/5.x
├── imageio / imageio-ffmpeg
├── python-dotenv
```

Si besoin, ces fichiers peuvent être générés avec :

```bash
pip download moviepy==1.0.3 pillow==9.5.0 tqdm==4.65.0 numpy==1.24.4 decorator==5.1.1 imageio==2.31.1 imageio-ffmpeg==0.4.8 python-dotenv==1.0.0 -d libs/
```

## ⚙️ Variables d'environnement recommandées

Pour désactiver les appels OpenAI dans vos scripts :

### Sous Linux/macOS :

```bash
export MOCK_OPENAI=true
```

### Sous Windows PowerShell :

```powershell
$env:MOCK_OPENAI = "true"
```

Cela permet à `description_generator.py` d'utiliser un simulateur local au lieu de l’API OpenAI.

## 🚀 Lancement de test

Une fois les dépendances installées, vous pouvez tester le projet avec :

```bash
python main_test.py
```

Cela exécutera tout le pipeline en mode simulation (transcript mock + images).

---

## 🧠 Ce que Codex peut faire avec cet environnement :

* Lire et améliorer les prompts (hook, titres, descriptions)
* Générer des hooks à partir du transcript mock
* Simuler la composition de clips avec des images
* Tester et améliorer la logique de tous les modules
* Ajouter des tests unitaires aux fonctions existantes
