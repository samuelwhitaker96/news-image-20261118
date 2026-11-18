#!/usr/bin/env python3
"""news-image-20261118 entry: copy the pre-rendered front page to the output.

The image is rendered ahead of time by draw.py; this program only copies it,
so the grader's no-network, stdlib-only sandbox can run it and every run
writes exactly the same bytes."""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
IMAGE = "news.png"
OUT = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

SRC = os.path.join(HERE, IMAGE)
if not os.path.isfile(SRC):
    raise SystemExit("missing pre-rendered image: %s" % SRC)

os.makedirs(OUT, exist_ok=True)
shutil.copy(SRC, os.path.join(OUT, "entry.png"))
