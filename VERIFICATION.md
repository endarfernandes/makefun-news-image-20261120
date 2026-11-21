# VERIFICATION — news-image-20261120 V4 FINAL R3 (reference-layout rebuild)

Edition date: **Friday, November 20, 2026** (the bounty's date).
R3 rebuilds `v4-presspoint/` to match the LAYOUT of the reference
image the user uploaded — layout/style only, not its content.
Per the user's correction ("Baik jadikan 8 saja sesuai gambar
referensi"), the total is now **1 hero + 8 supporting = 9 stories**.

## DROPPED STORY — read first
**France seeks UNSC meeting (SECURITY COUNCIL)** — dropped from the
9 supporting stories of v4-presspoint. Reasoning: it is a direct
reaction to the hero story (the Kyiv strikes — Paris calls for an
emergency session *after the Kyiv strikes*), so it adds the least new
information of the nine; every other supporting story covers a
different subject/region. No other story was considered as weak:
Nasdaq (biggest market move of the year), Trump talks (White House
read-out), Akvan (live disaster), UK–EU reset (major deal), Myanmar
verdict (ICJ rejection), COP31 (overtime), UN chief race (stalled
poll), Angola/De Beers ($180m deal) each carry distinct news. The
8 kept stories are unchanged in headline, facts, figures, decks and
photos. The dropped photo (`unsc.jpg`) remains in `assets/` but is
not rendered; the dropped story stays documented in STORIES.md.

## Final image

- File: `v4-presspoint-r3/entry.png`
- Dimensions: 1024 × 1024 px, RGB, non-interlaced PNG
- Size: **973,322 bytes** (< 1,048,576 limit; **75,254 bytes
  headroom** — more comfortable than v4-presspoint's 36,222)
- SHA-256: `3a00c0172f94ca334c03c31c325e0068b3b196ad12d0df50800487689924df5f`
- Rendered by: `v4-presspoint-r3/render.py` (Pillow 10.2.0 + bundled
  Inter variable font, offline, no network)
- Previews: `preview-600.png` (600×600), `preview-300.png` (300×300)
- The 3×3 version of this build is preserved as `entry-3x3.png`
  (SHA `b11037c6…`, 1,011,877 bytes) with its own previews.

## Determinism

Two consecutive `python3 render.py` runs produced byte-identical
output: same size (973,322) and same SHA-256 (`3a00c017…`). No
timestamps, no randomness in the renderer.

## Layout checks (visual, full-size + 600 px + 300 px)

- Layout budget: header 0–76, hero 76–470, grid 482–968, footer
  968–1024. Renderer asserts the header row fits, hero deck ≤ 2
  lines, card headlines ≤ 2 lines, decks ≤ 3 lines, no text past
  the card bottom or past y 1024.
- Full-size review (1024×1024, viewed directly): no clipped text,
  no overlapping elements, no distorted photos. All 9 headlines and
  decks legible. Header row (date | WORLD BRIEFING | red breaking
  strip) matches the reference structure. Hero headline/deck read
  clearly over the gradient; red accent line visible under the
  deck. All 8 card photos fill their frames; chips are readable on
  the photos; headlines (16 px) and decks (11 px) fit their cards.
  Footer: globe icon, date, sources, photo-credit line and red
  diagonal slashes all visible — the credit line was verified at 2×
  zoom to be fully rendered, not clipped.
- 600×600 review: date, hero headline, all 8 card headlines and
  photos readable; layout structure clear. PASS.
- 300×300 review: date masthead, hero photo, hero headline, red
  breaking strip and the 4×2 grid structure are immediately
  recognisable; colour identity (navy date, red strip) reads
  clearly. Small decks are not meant to be read at that size. PASS.
- No fixes were needed after the first render — the first render
  passed all assertions and the visual review.

## Entrypoint test

`MAKEFUN_OUTPUT_DIR=/tmp/r3b-out python3 main.py` wrote
`entry.png` byte-identical to the workdir file (same SHA-256
`3a00c017…`). Stdlib only, no network.

## Local kit check

- Kit: the existing kit copy from v4-presspoint
  (`kit-fresh/news-image-20261120-kit`, bundle `63afd6ef…` —
  identical to the kit v4 used; no fresh kit was downloaded).
- Ran `node <kit>/cli/makefun.mjs check --kit <kit> --repo
  /tmp/r3b-kitcheck --worktree` on a throwaway sandbox copy
  (main.py + entry.png + LICENSE + docs + assets + fonts). The real
  repo was NOT touched and no git command was run.
- Result: **4 passed, 1 failed, 14 skipped, 5 checked at submission**
  (same pattern as v4 / v4-presspoint / R2).
  - Passed: competition_open (open until 2026-11-22T00:00Z),
    snapshot (20 files, 4,882,157 bytes — within intake caps),
    license_osi (MIT), entrypoint (main.py at root selects
    python3.13, which the competition accepts).
  - Failed: transcripts_present — no transcripts were supplied.
    This is the expected pre-submit state; the run record is this
    build session and is bundled at submit time.
  - Skipped (14): transcript-gate checks (no session parsed) and
    strategy_note / committed_secret (not applicable without
    --dotenv).
  - Checked at submission (5): repo_public, repo_owner,
    repo_created_after_open, commit_in_repo, duplicate_snapshot —
    all deferred to the real repo/submission step. Note:
    `repo_created_after_open` requires the repo's GitHub creation
    time to be ≥ 2026-11-20T00:00:00Z; the existing
    `makefun-news-image-20261120` repo was created 21 Nov, so it
    qualifies.

## Facts and photos

- All 9 stories are 20 Nov 2026 events from the v4 research base
  (re-verified 21 Nov ~08:25 WIB against Reuters/CNN/Finnhub),
  except story 7 (COP31 overtime), whose Friday-night development
  was verified 21 Nov ~08:55 WIB against Asia Today and EnergyDive.
  See STORIES.md. No fact, figure, headline or deck of the 8 kept
  stories changed vs v4-presspoint — verified by diffing the
  CARDS/HERO blocks against `v4-presspoint/render.py` (only the
  France entry was removed and the grid geometry changed).
- All 9 photos are the same downloaded files as v4-presspoint
  (SHA-256s re-verified after copying into `assets/` — identical).
  Licences verified from each file's Wikimedia Commons extmetadata
  at download time. No Reuters/AP/AFP/Getty image used. See
  PHOTOS.md. `unsc.jpg` is present in `assets/` but unused in this
  edition.
- **Cover-crop note (explicit):** the reference look requires
  cover-cropping every photo to its frame. The R2 no-crop rule was
  set aside per the user's reference instruction ("bikin seperti
  ini"). R2 (`v4-presspoint-r2/`) stays preserved as the uncropped
  alternative.
- Honesty notes: 1 EVENT photo (Akvan satellite), 1 PERSON portrait
  (Trump), 6 LOCATION photos, 1 SUBJECT photo (diamonds). No photo
  is presented as something it is not; the Kyiv photo is a night
  panorama of Podil, not the strike itself.

## Leaderboard QC (live, 21 Nov 2026 ~02:02 WIB, from v4-presspoint)

- Competition has **13,116 entries**. Top 10 are all 12–0–0
  (perfect provisional records, 12 matches each).
- Top-10 titles: 33–38 stories, 6–7 regions.
- **This entry is deliberately different:** 9 stories, large
  photos, date-as-masthead, generous whitespace. It is immediately
  distinguishable from v1–v4 and from the current top 10.

## Repo status

`v4-presspoint-r3/` is NOT in the repo. `repo/` still holds v3
(entry.png + render.py from v3, commit 3b7c220 era). `v4/`,
`v4-presspoint/` and `v4-presspoint-r2/` were not modified. No
commit, no push, no Google Drive update, no submit was performed
in this session.

## Quality-control self-assessment (10 criteria)

1. Photo authenticity/quality: 9/10 — all real, licensed,
   well-chosen; Antalya (coastal road) remains the weakest
   thematic match — a real Antalya photo, but it reads as a generic
   street.
2. Story strength: 9/10 — the day's genuinely biggest stories, all
   verified; dropping the France reaction story tightens the
   selection; COP31 angle is the fresh Friday-night development.
3. Visual impact at first glance: 9/10 — the reference layout is
   now matched closely: one-row header, full-bleed hero, 4×2 photo
   grid, navy footer. At 300 px the structure reads instantly.
4. Headline typography: 9/10 — Inter Black/ExtraBold is strong at
   all sizes; card headlines hold at 16 px.
5. Colour harmony: 9/10 — navy/red/blue/teal/green/orange on warm
   ivory; the coloured chips add the reference's colour rhythm.
6. Editorial composition: 9/10 — clear hierarchy (date → breaking
   strip → hero → 4×2 grid → footer), consistent card rhythm,
   generous whitespace.
7. Crop quality: 8/10 — Trump face band holds (eyes, nose, mouth);
   NYSE flag crop is flag-heavy; hero panorama crop is excellent.
8. Mobile readability: 9/10 — identity, hero and structure read at
   300 px; small decks are not meant to be read at that size.
9. Factual accuracy: 9/10 — re-verified leads; one noted figure
   conflict (Anthropic close $88.91 vs WSJ $88.30) resolved to the
   majority/CNN/Finnhub figure and documented.
10. Copyright / attribution: 9/10 — every photo licensed and
    credited in PHOTOS.md; footer carries the compact credit line.
    Attribution inside the image is a summary line only — full
    credits live in the repo docs, as the competition format
    requires.

## Remaining risks and honest assessment

- **Judge taste / story count (the main risk):** the judge is a
  pairwise image model and the leaderboard evidence is consistent
  — the current top 10 all carry 33–38 stories. This entry bets
  the other way: 9 stories with much larger photos and much more
  whitespace. Dropping to 8 supporting stories (from 9) moves
  further from the leaderboard consensus, but it matches the
  reference layout the user asked for exactly. It may win on
  first-glance impact and readability, but it covers fewer of the
  day's stories, and the judge's criterion is "best sums up the
  day's world news" — breadth is part of that. The user directed
  8 supporting stories, so this is their call, but it is a real
  counter-consensus bet, not a safe one.
- **1 MiB budget is comfortable now** (973,322 bytes; 75,254 bytes
  headroom).
- **Antalya photo** is the weakest thematic match; a better
  licensed COP-venue photo would strengthen that card.
- **Transcript gate** (thinking_reproduces ≥30%, internal target
  35%) is judged server-side from the session record; this session
  is the complete authoring transcript (single session, no child
  authoring sessions), but the coverage figure is only known after
  bundling.
- **Prize note:** the competition page says the **top 50** entries
  share $250 ($50/$30/$15/$5/$3) — the brief's "top 100" is not
  what the competition states. Rank 100 is outside the prize zone.
- If the user picks R3, the v3 kit-check/commit/push and the
  v4-vs-v3 decisions become moot — confirm with the user.
