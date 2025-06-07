import sys
import os
sys.path.append(os.path.abspath("."))

from generators.youtube import slicer

slug = "test_rick"
segments = slicer.slice_video(slug)

print(f"✅ {len(segments)} clips créés.")
