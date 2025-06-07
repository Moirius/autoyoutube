import sys, os
sys.path.append(os.path.abspath("."))

from generators.youtube import description_generator

transcript = "Il a ouvert le mur de sa cuisine et a trouvé un sac entier de vis."
slug = "test_rick"
part_filename = "part_1.mp4"

caption = description_generator.generate_caption(transcript, bot_id="bot1")
print("🎯 Caption générée :\n", caption)

description_generator.save_caption(caption, slug, part_filename)
