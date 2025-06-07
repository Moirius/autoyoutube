import sys
import os
sys.path.append(os.path.abspath("."))

from generators.youtube import transcriber

slug = "test_rick"  # même dossier que tu as utilisé pour download
segments = transcriber.transcribe(slug)

print(f"📄 Transcription obtenue avec {len(segments)} segments.")
