#!/bin/bash
echo "✅ Installation des dépendances locales Codex (libs/)"

pip install ./libs/numpy-1.24.4-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
pip install ./libs/pillow-9.5.0-py3-none-any.whl
pip install ./libs/tqdm-4.65.0-py3-none-any.whl
pip install ./libs/moviepy-1.0.3-py3-none-any.whl
pip install ./libs/decorator-5.1.1-py3-none-any.whl
pip install ./libs/imageio-2.31.1-py3-none-any.whl
pip install ./libs/imageio_ffmpeg-0.4.8-py3-none-manylinux2010_x86_64.whl
pip install ./libs/python_dotenv-1.0.0-py3-none-any.whl
