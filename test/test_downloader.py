import sys
import os

sys.path.append(os.path.abspath("."))  # <- ajoute tiktokbot/ au path

from generators.youtube import downloader


# Lien test
video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
slug = "test_rick"

path = downloader.download(video_url, slug)
print(f"✅ Vidéo téléchargée à : {path}")
