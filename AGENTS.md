# 🤖 Mode Codex / Simulation locale

Ce projet est prêt à être utilisé avec Codex ou un agent IA (avec ou sans appel aux API réelles).

## 🥪 Simulation avec données mock

Utilisez les fichiers suivants pour tester sans télécharger de vidéo ni appeler l'API OpenAI :

- `test_data/mock_transcript.txt` : transcript texte simulé  
- `test_data/mock_segments.json` : segments vidéo simulés  
- `test_data/test/parts/mock_part1.png`, `test_data/test/parts/mock_part2.png` : images utilisées à la place de vidéos

## 📦 Installation automatique via Internet (recommandé)

Le projet peut être exécuté dans Codex avec un environnement connecté à Internet. Les dépendances sont automatiquement installées depuis PyPI via le script suivant :

```bash
bash setup.sh
````

Ce script utilise le fichier `requirements_mock.txt` pour installer les bibliothèques suivantes :

* `moviepy`
* `numpy`
* `pillow`
* `imageio`
* `imageio-ffmpeg`
* `tqdm`
* `decorator`
* `python-dotenv`
* `openai`
* etc.

### 📎 Remarque

Assurez-vous que **l’accès Internet est activé dans Codex** (via l’option "Network Access") avant d'exécuter `bash setup.sh`.

## ⚙️ Variables d’environnement recommandées

Pour désactiver les appels OpenAI dans vos scripts (mode simulation locale) :

### Sous Linux/macOS :

```bash
export MOCK_OPENAI=true
```

### Sous Windows PowerShell :

```powershell
$env:MOCK_OPENAI = "true"
```

Cela permet à `description_generator.py` d’utiliser un simulateur local au lieu de l’API OpenAI.

## 🚀 Lancement de test

Une fois les dépendances installées, vous pouvez tester le projet avec :

```bash
python main_test.py
```

Cela exécutera tout le pipeline en mode simulation (transcript mock + images).

---

## 🧠 Ce que Codex peut faire avec cet environnement :

* Lire et améliorer les prompts (hooks, titres, descriptions)
* Générer des hooks à partir du transcript simulé
* Simuler la composition de clips avec des images
* Tester et améliorer la logique des modules
* Ajouter des tests unitaires aux fonctions

