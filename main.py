#!/usr/bin/env python3
"""Grading entrypoint for news-image-20261120 (V4 FINAL R3 — reference-layout
rebuild, edition Friday, November 20, 2026; 1 hero + 8 supporting = 9 stories).

Copies the pre-rendered magazine cover (entry.png, produced by render.py)
to the grader's output directory. Pure standard library, no network,
deterministic: the copied file is byte-identical to entry.png in this
directory.

Reproduce the image: python3 render.py  (needs Pillow + the bundled
Inter font in fonts/; see README.md). The entrypoint itself needs
nothing but Python 3.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or (
        sys.argv[1] if len(sys.argv) > 1 else "/output"
    )
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dst)
    print("wrote", dst, os.path.getsize(dst), "bytes")


if __name__ == "__main__":
    main()
