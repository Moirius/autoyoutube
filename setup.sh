#!/bin/bash
echo "✅ Installation des dépendances locales Codex (libs/)"

pip install ./libs/numpy-1.24.4-*.whl
pip install ./libs/pillow-9.5.0-*.whl
pip install ./libs/tqdm-4.65.0-*.whl
pip install ./libs/decorator-4.4.2-*.whl     # ✅ version compatible
pip install ./libs/imageio-2.31.1-*.whl
pip install ./libs/imageio_ffmpeg-0.4.8-*.whl
pip install ./libs/python_dotenv-1.0.0-*.whl
pip install ./libs/moviepy-2.0.0-*.whl
