#!/bin/bash

# Script de configuration pour Codex (mode mock sans Internet)
# Vérifie que les dépendances nécessaires sont installées localement

echo "✅ Chargement des modules mock pour Codex"

pip install ./libs/moviepy-1.0.3-py3-none-any.whl
pip install ./libs/pillow-9.5.0-py3-none-any.whl
pip install ./libs/numpy-1.24.4-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
pip install ./libs/tqdm-4.65.0-py3-none-any.whl
