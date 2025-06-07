from moviepy.editor import *
from moviepy.config import change_settings
from utils.logger import get_logger
from PIL import Image, ImageDraw, ImageColor
import numpy as np
import os, random

logger = get_logger(__name__)
change_settings({"IMAGEMAGICK_BINARY": "C:/Program Files/ImageMagick-7.1.1-Q16-HDRI/magick.exe"})

MODE_TEST = False

def rounded_rect_clip(width, height, radius, color=(255, 255, 255)):
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((0, 0, width, height), radius=radius, fill=color)
    return ImageClip(np.array(img))

def compose_clip(slug: str, part_filename: str, part_number: int, background_dir: str = "videos/gameplay", output_dir: str = "series") -> str:
    part_path = os.path.join(output_dir, slug, "parts", part_filename)
    hook_path = os.path.join(output_dir, slug, "hooks", f"{os.path.splitext(part_filename)[0]}.txt")
    output_path = os.path.join("videos", "exports", slug, part_filename)

    if not os.path.exists(part_path):
        logger.error(f"❌ Vidéo introuvable : {part_path}")
        raise FileNotFoundError(f"❌ Vidéo introuvable : {part_path}")

    overlay_text = "Regarde ça 👀"
    if os.path.exists(hook_path):
        with open(hook_path, "r", encoding="utf-8") as f:
            overlay_text = f.read().strip()

    logger.info(f"🎬 Composition de : {part_path}")
    target_width, target_height = (360, 640) if MODE_TEST else (720, 1280)
    half_height = target_height // 2

    # === Lire les paramètres personnalisés ===
    font_path = os.environ.get("FONT_PATH", "fonts/BebasNeue-Regular.ttf")
    hook_font_size = int(os.environ.get("HOOK_FONT_SIZE", 42))
    part_font_size = int(os.environ.get("PART_FONT_SIZE", 38))
    hook_color = os.environ.get("HOOK_COLOR", "black")
    badge_color = os.environ.get("BADGE_COLOR", "#C84628")
    part_text_color = os.environ.get("PART_TEXT_COLOR", "white")
    hook_bg_color = os.environ.get("HOOK_BG_COLOR", "#FFFFFF")
    hook_y = int(os.environ.get("HOOK_Y", 590))
    badge_y = int(os.environ.get("BADGE_Y", 640))

    badge_rgb = ImageColor.getrgb(badge_color)
    hook_bg_rgb = ImageColor.getrgb(hook_bg_color)

    # === Vidéo principale ===
    main_clip = VideoFileClip(part_path).resize(height=half_height)
    main_clip = main_clip.crop(x_center=main_clip.w // 2, width=target_width)
    clip_duration = min(main_clip.duration, 5) if MODE_TEST else main_clip.duration
    logger.info(f"🎞️ Durée finale du clip : {clip_duration:.2f}s")

    # === Fond gameplay (avec redimensionnement non déformant comme dans le 1er code) ===
    background_files = [f for f in os.listdir(background_dir) if f.endswith(('.mp4', '.mov'))]
    if not background_files:
        logger.error("❌ Aucune vidéo de gameplay trouvée.")
        raise RuntimeError("❌ Aucune vidéo de gameplay trouvée.")

    background_clip = None
    random.shuffle(background_files)

    for file in background_files:
        try:
            logger.info(f"🕹️ Test fond gameplay : {file}")
            bg = VideoFileClip(os.path.join(background_dir, file)).without_audio()
            if bg.duration < clip_duration:
                bg = bg.loop(duration=clip_duration)
            else:
                start = random.uniform(0, bg.duration - clip_duration)
                bg = bg.subclip(start, start + clip_duration)
            bg = bg.resize(height=half_height)
            bg = bg.crop(x_center=bg.w // 2, width=target_width)
            background_clip = bg
            logger.info(f"✅ Fond sélectionné : {file}")
            break
        except Exception as e:
            logger.warning(f"⚠️ Échec fond {file} : {e}")
            continue

    if background_clip is None:
        logger.error("❌ Aucun fond gameplay valide trouvé.")
        raise RuntimeError("❌ Aucun fond gameplay valide trouvé.")

    # === Empilage vertical ===
    top = main_clip.set_position(("center", 0))
    bottom = background_clip.set_position(("center", half_height))
    stacked = CompositeVideoClip([top, bottom], size=(target_width, target_height)).set_duration(clip_duration)

    # === Texte hook ===
    max_txt_width = int(target_width * 0.65)
    txt_clip = TextClip(overlay_text, fontsize=hook_font_size, font=font_path, color=hook_color, method='caption',
                        size=(max_txt_width, None)).set_duration(clip_duration)
    txt_bg = rounded_rect_clip(txt_clip.w + 30, txt_clip.h + 20, radius=12, color=hook_bg_rgb).set_duration(clip_duration)
    txt_box = CompositeVideoClip([txt_bg.set_position("center"), txt_clip.set_position("center")],
                                 size=(txt_clip.w + 30, txt_clip.h + 20)).set_duration(clip_duration)

    # === Badge "Partie X" ===
    badge_txt = TextClip(f"Partie {part_number}", fontsize=part_font_size, font=font_path, color=part_text_color, method='caption').set_duration(clip_duration)
    badge_bg = rounded_rect_clip(badge_txt.w + 26, badge_txt.h + 12, radius=10, color=badge_rgb).set_duration(clip_duration)
    badge = CompositeVideoClip([badge_bg.set_position("center"), badge_txt.set_position("center")],
                               size=(badge_txt.w + 26, badge_txt.h + 12)).set_duration(clip_duration)

    # === Groupe texte aligné ===
    group = CompositeVideoClip([
        badge.set_position((0, badge_y)),
        txt_box.set_position((badge.w + 10, hook_y))
    ], size=(badge.w + 10 + txt_box.w, max(badge.h + badge_y, txt_box.h + hook_y))).set_duration(clip_duration)

    # === Composition finale ===
    final = CompositeVideoClip([stacked, group], size=(target_width, target_height)).set_duration(clip_duration)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    final.write_videofile(output_path, codec="libx264", audio_codec="aac",
                          preset="ultrafast", threads=1, fps=15 if MODE_TEST else 24)

    logger.info(f"✅ Clip composé : {output_path}")
    logger.info(f"📁 Taille du fichier : {os.path.getsize(output_path) / (1024 * 1024):.2f} MB")

    return output_path
