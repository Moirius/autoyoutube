import yt_dlp
import os
from utils.logger import get_logger

logger = get_logger(__name__)

def download(youtube_url: str, slug: str) -> str:
    """
    Télécharge une vidéo YouTube et la place dans series/{slug}/original.mp4
    """
    output_dir = os.path.join("series", slug)
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, "original.%(ext)s")

    # ✅ Définir le chemin des cookies avant l'utilisation
    yt_cookies_path = os.path.abspath(os.path.join("cookies", "cookies_yt.txt"))

    ydl_opts = {
        'format': 'bv*+ba/b',
        'outtmpl': output_path,
        'merge_output_format': 'mp4',
        'noplaylist': True,
        'quiet': True,
        'source_address': '0.0.0.0',  # force IPv4
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Accept-Language': 'en-US,en;q=0.9'
        },
    }

    # ✅ Ajouter le cookiefile si dispo
    if os.path.exists(yt_cookies_path):
        ydl_opts["cookiefile"] = yt_cookies_path
        logger.info(f"🍪 Utilisation des cookies YouTube : {yt_cookies_path}")
    else:
        logger.warning("⚠️ Fichier cookies YouTube introuvable.")

    try:
        logger.info(f"📥 Téléchargement depuis : {youtube_url}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=True)
            filename = ydl.prepare_filename(info)
            final_path = os.path.splitext(filename)[0] + ".mp4"
            logger.info(f"✅ Vidéo téléchargée : {final_path}")
            return final_path
    except Exception as e:
        logger.exception("❌ Échec du téléchargement")
        raise
