import os
import urllib.request
import shutil

def download_example_video():
    url = "https://www.youtube.com/watch?v=9ZW3uzuzuhE"
    dest_series = "series/test_rick/original.mp4"
    dest_background = "background/original.mp4"

    # Crée les répertoires
    os.makedirs(os.path.dirname(dest_series), exist_ok=True)
    os.makedirs(os.path.dirname(dest_background), exist_ok=True)

    print("📥 Téléchargement de la vidéo d'exemple...")
    urllib.request.urlretrieve(url, dest_series)
    print(f"✅ Vidéo téléchargée dans : {dest_series}")

    # Copie dans background/
    shutil.copy(dest_series, dest_background)
    print(f"✅ Vidéo également copiée dans : {dest_background}")

if __name__ == "__main__":
    download_example_video()
