import os
import random
from typing import List
from moviepy.editor import VideoFileClip
from utils.logger import get_logger

logger = get_logger(__name__)

def slice_video(slug: str, min_dur=None, max_dur=None):
    import os
    min_dur = min_dur or int(os.environ.get("MIN_DUR", 45))
    max_dur = max_dur or int(os.environ.get("MAX_DUR", 75))

    """
    Découpe la vidéo original.mp4 de la série <slug> en clips aléatoires.
    Sauvegarde les clips dans series/<slug>/parts/
    """
    input_path = os.path.join("series", slug, "original.mp4")
    output_dir = os.path.join("series", slug, "parts")
    os.makedirs(output_dir, exist_ok=True)

    clip = VideoFileClip(input_path)
    duration = clip.duration

    logger.info(f"✂️ Vidéo à découper : {input_path} ({duration:.1f} secondes)")

    start = 0
    part_num = 1
    segments = []

    while start < duration:
        segment_duration = random.randint(min_dur, max_dur)
        end = min(start + segment_duration, duration)

        subclip = clip.subclip(start, end)
        output_path = os.path.join(output_dir, f"part_{part_num}.mp4")
        subclip.write_videofile(
            output_path,
            codec="libx264",
            audio_codec="aac",
            temp_audiofile="temp-audio.m4a",
            remove_temp=True,
            threads=4,
            logger=None,
            preset="ultrafast",
            fps=24,
            ffmpeg_params=["-movflags", "faststart"]
        )

        logger.info(f"🎬 Exporté : {output_path} ({end - start:.1f}s)")

        segments.append({
            "path": output_path,
            "start": start,
            "end": end
        })

        start = end
        part_num += 1

    clip.close()
    return segments
