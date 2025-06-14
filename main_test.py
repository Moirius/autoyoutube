from mock_mode import transcriber, slicer
from generators.youtube import description_generator

def main_test():
    slug = "test"
    transcript = transcriber.transcribe("mock_part.mp4", slug)
    segments = slicer.slice_video(slug)

    for idx, seg in enumerate(segments):
        text = " ".join([s["text"] for s in transcript if seg["start"] <= s["start"] < seg["end"]])
        print(f"\n🧠 Prompt de description {idx+1}:")
        print(text)
        hook = description_generator.generate_hook(text)
        print(f"➡️ Hook généré : {hook}")
