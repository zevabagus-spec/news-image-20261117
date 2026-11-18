#!/usr/bin/env python3
"""news-image-20261117 entry: copy the rendered front page to /output/entry.png.

The image (entry.png, beside this file) is a newspaper poster summing up the
world news of Tuesday 17 November 2026. It was drawn in the build session by
render.py (Pillow + DejaVu fonts) from news reported that day; this program
only copies those exact bytes, so every run writes identical output.

Standard library only, no network. Outside the grader's container,
MAKEFUN_OUTPUT_DIR stands in for /output:

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
SRC = os.path.join(HERE, "entry.png")

if not os.path.isfile(SRC):
    raise SystemExit(f"entry image missing: {SRC}")

os.makedirs(OUT_DIR, exist_ok=True)
shutil.copyfile(SRC, os.path.join(OUT_DIR, "entry.png"))
