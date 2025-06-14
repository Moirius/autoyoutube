import json
from generators.youtube import description_generator
from generators.youtube.composer import compose_clip

def load_transcript():
    with open("test_data/mock_transcript.txt", encoding="utf-8") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]
    return [{"start": i * 2, "end": (i + 1) * 2, "text": line} for i, line in enumerate(lines)]

def load_segments():
    with open("test_data/mock_segmets.json", encoding="utf-8") as f:
        return json.load(f)

def main_test():
    slug = "test"
    transcript = load_transcript()
    segments = load_segments()

    for idx, seg in enumerate(segments):
        text = " ".join([s["text"] for s in transcript if seg["start"] <= s["start"] < seg["end"]])
        print(f"\n🧠 Prompt de description {idx+1}:")
        print(text)
        hook = description_generator.generate_hook(text)
        print(f"➡️ Hook généré : {hook}")

        # Optionnel : génère la vidéo
        compose_clip(
            slug=slug,
            part_filename=seg["path"].split("/")[-1],
            part_number=idx + 1,
            background_dir="videos/gameplay",
            output_dir="test_data"
        )

if __name__ == "__main__":
    main_test()
