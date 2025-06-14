# 🤖 Mode Codex / Simulation locale

Ce projet est prêt à être utilisé avec Codex ou un agent IA (sans accès Internet ou API réelles).

## 🧪 Simulation avec données mock

Utilisez les fichiers suivants pour tester sans télécharger de vidéo ni appeler l'API OpenAI :
- `mock_transcript.txt` : transcript texte simulé
- `mock_segmets.json` : segments vidéo simulés
- `mock_part1.png`, `mock_part2.png` : images utilisées à la place de vidéos

## 📦 Dépendances minimales (mode test)

Vous pouvez installer uniquement les dépendances nécessaires pour tester localement :

```bash
pip install -r requirements_mock.txt
```

Contenu du fichier `requirements_mock.txt` :

```
moviepy==1.0.3
numpy
pillow<10
tqdm
```

## ⚙️ Variables d'environnement recommandées

Pour désactiver les appels OpenAI dans vos scripts :

```bash
export MOCK_OPENAI=true
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

- Lire et améliorer les prompts (hook, titres, descriptions)
- Générer des hooks à partir du transcript mock
- Simuler la composition de clips avec des images
- Tester et améliorer la logique de tous les modules
- Ajouter des tests unitaires aux fonctions existantes
