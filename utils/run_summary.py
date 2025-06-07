# utils/run_summary.py

from utils.logger import get_logger
logger = get_logger(__name__)

class RunSummary:
    def __init__(self):
        self.video_title = None
        self.duration = 0
        self.segments = 0
        self.chunks = 0
        self.gpt_scores = 0
        self.clips_retained = 0
        self.clips_stylized = 0
        self.total_clip_duration = 0
        self.selected_chunks = []
        self.errors = []
        self.warnings = []

    def log_error(self, msg):
        self.errors.append(msg)
        logger.error(msg)

    def log_warning(self, msg):
        self.warnings.append(msg)
        logger.warning(msg)

    def print_summary(self, log_path: str):
        print("\n" + "=" * 50)
        print("📊 Résumé exécution du bot TikTok :")
        print(f"🎥 Vidéo : {self.video_title or 'Inconnue'}")
        print(f"⏱️ Durée : {self.duration:.1f}s")
        print(f"📝 Segments transcrits : {self.segments}")
        print(f"✂️ Chunks analysés : {self.chunks}")
        print(f"🤖 Chunks scorés (GPT) : {self.gpt_scores}")
        print(f"🏆 Clips retenus : {self.clips_retained}")
        print(f"🖼️ Stylisés : {self.clips_stylized}/{self.clips_retained}")
        print(f"🕒 Durée totale clips : {self.total_clip_duration:.1f}s")
        print(f"⚠️ Avertissements : {len(self.warnings)}")
        print(f"❌ Erreurs : {len(self.errors)}")
        print(f"📁 Log complet : {log_path}")
        print("-" * 50)
        if self.selected_chunks:
            print("🧠 Segments retenus :")
            for c in self.selected_chunks:
                print(f" - [{c['start']:.1f}s → {c['end']:.1f}s] | score={c['score']:.1f}")
                print(f"   Texte : \"{c['text']}\"")
        print("=" * 50 + "\n")
