# main.py

import os
import re
import shutil
import argparse
from generators.youtube import downloader, transcriber, slicer, composer, description_generator
from generators.youtube.viral_analyzer import analyze_transcript
from utils.logger import get_logger

logger = get_logger(__name__)

def extract_transcript_for_clip(transcript, start_time, end_time):
    return " ".join([
        seg['text'] for seg in transcript
        if seg['start'] >= start_time and seg['end'] <= end_time
    ])

def main(youtube_url, slug):
    try:
        logger.info(f"🚀 Traitement de la vidéo : {youtube_url} (slug: {slug})")

        # 1. Télécharger
        video_path = downloader.download(youtube_url, slug)
        logger.info(f"📁 Vidéo téléchargée : {video_path}")

        # 2. Transcription
        transcript = transcriber.transcribe(video_path, slug)
        logger.info(f"📝 Transcription obtenue ({len(transcript)} segments)")

        # 3. Analyse virale
        max_segments = int(os.environ.get("MAX_SEGMENTS", 5))
        viral_segments = analyze_transcript(transcript, max_segments=max_segments)
        if not viral_segments:
            logger.warning("⚠️ Aucun segment viral détecté, fallback sur découpe aléatoire.")
            segments = slicer.slice_video(slug)
        else:
            segments = slicer.slice_video(slug, override_segments=viral_segments)

        logger.info(f"✂️ {len(segments)} clips générés")

        # 4. Génération des hooks + composition
        for idx, segment in enumerate(segments):
            part = idx + 1
            part_filename = f"part_{part}.mp4"
            transcript_chunk = extract_transcript_for_clip(transcript, segment['start'], segment['end'])

            # Hook + Caption
            caption = description_generator.generate_caption(transcript_chunk, bot_id="bot1")
            description_generator.save_caption(caption, slug, part_filename)

            # Copier le hook comme caption TikTok
            hook_path = os.path.join("series", slug, "hooks", f"part_{part}.txt")
            caption_path = os.path.join("videos", "exports", slug, f"part{part}_caption.txt")

            os.makedirs(os.path.dirname(caption_path), exist_ok=True)
            try:
                shutil.copy(hook_path, caption_path)
                logger.info(f"✅ Hook copié comme caption TikTok : {caption_path}")
            except Exception as e:
                logger.error(f"❌ Erreur lors de la copie du hook comme caption TikTok")
                logger.exception(e)

            # Composition du clip
            composer.compose_clip(
                slug=slug,
                part_filename=part_filename,
                part_number=part
            )

            logger.info(f"🎬 Clip composé : {part_filename}")

        logger.info("✅ Pipeline complété avec succès.")

    except Exception as e:
        logger.exception("❌ Pipeline échoué.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="URL YouTube à traiter")
    parser.add_argument("slug", help="Nom de série à utiliser (ex: yt_1)")
    args = parser.parse_args()

    main(args.url, args.slug)
