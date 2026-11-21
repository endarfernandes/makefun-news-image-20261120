# news-image-20261120 — V4 FINAL R3 (reference-layout rebuild)

Edition: **Friday, November 20, 2026**. Exactly **9 stories
(1 hero + 8 supporting)**, all real licensed photographs — rebuilt
to match the layout of the reference image the user uploaded
(layout/style only, not its content). The France UNSC meeting story
was dropped per the user's "jadikan 8 saja sesuai gambar referensi"
(the most duplicative story — a reaction to the hero); see
VERIFICATION.md.

## Files
- `entry.png` — the final image (1024×1024, RGB, < 1 MiB).
- `entry-3x3.png` — the 3×3 version of this build, preserved.
- `render.py` — the renderer (Pillow + bundled Inter font, offline,
  deterministic). Re-run: `python3 render.py`.
- `main.py` — grading entrypoint (stdlib only): copies `entry.png`
  to `$MAKEFUN_OUTPUT_DIR/entry.png`. Test:
  `MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py`.
- `assets/` — 10 licensed photos (see PHOTOS.md); `unsc.jpg` is
  unused in this edition and kept for reference.
- `fonts/` — Inter variable font (OFL) + OFL licence.
- `STORIES.md` — the 9 stories, sources, dropped stories.
- `PHOTOS.md` — per-photo source, photographer, licence, SHA-256.
- `DESIGN.md` — design rationale and geometry.
- `VERIFICATION.md` — verification report.
- `LICENSE` — MIT.

## Assembly (after user approval — NOT done yet)
1. Copy the entry files into the repo root: `entry.png`, `main.py`,
   `LICENSE`, `render.py`, `assets/`, `fonts/`, docs. Do NOT copy
   `entry-3x3.png` or the `preview-*.png` files (convenience files,
   not part of the entry).
2. Update the repo README/VERIFICATION.
3. Run the kit check on the assembled repo.
4. Commit + push, then submit via the kit (transcript bundle).

## Status
BUILD ONLY. No commit, no push, no Google Drive update, no submit
has been performed. `v4-presspoint-r3/` is NOT in the repo; `repo/`
still holds v3. The previous `v4/`, `v4-presspoint/` and
`v4-presspoint-r2/` directories were not modified.
