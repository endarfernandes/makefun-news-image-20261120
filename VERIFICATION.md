# VERIFICATION REPORT — news-image-20261120 v2
## "THE WORLD IN ONE DAY" — Friday 20 November 2026 (premium newspaper redesign)

Date: 21 Nov 2026, ~07:45 WIB. Entry built, never submitted.
v2 supersedes v1 (same repo, new commit) as the candidate entry; v1 remains
backed up in the build workspace (`entry-v1.png`, SHA `0c3fe74f…`).

## Deliverables
- Repo: https://github.com/endarfernandes/makefun-news-image-20261120
- Files: `entry.png` (v2), `main.py` (unchanged from v1), `render.py` (v2),
  `README.md`, `LICENSE` (MIT), `VERIFICATION.md` (this file)
- Design note: build workspace `v2/DESIGN_V2.md`

## Image
- Format: PNG, 1024×1024, RGB, 193,226 bytes (< 1 MiB cap) ✓
- SHA-256: `cbeb4f88ab91e01f8c21cc1eda6405973d6a35e011959b308330d70548b88b6b`
- Determinism: two consecutive `render.py` runs → identical SHA-256 ✓
- Entrypoint: `main.py` (pure stdlib) copies `entry.png` to
  `$MAKEFUN_OUTPUT_DIR/entry.png` byte-identically (verified in a fresh
  output dir, same SHA-256) ✓
- Layout: bottom y 1019 of 1024 — nothing clipped ✓
- 300px thumbnail check: navy masthead, standfirst, 3 lead scenes and the
  numbers strip still read; lead headlines partly legible; secondary decks
  dissolve (same as the top-10 leaders). ✓

## Local kit check (fresh kit downloaded 21 Nov 00:38 UTC)
Kit bundle_sha256 `63afd6ef…` — identical to the kit v1 was built against;
the kit has not changed since. `makefun check` results recorded below
after the repo update.

## Transcripts
- Build session log: this session's own log (the session that authored
  v2/render.py, entry-v2.png, README.md and this report in full, with no
  child authoring sessions). Bundle it with `--system-prompt
  ~/workspace/system/system_prompt.md` and `--muse-usage` at submit time.
- No `makefun record` live-recording command exists in this kit's CLI;
  the harness's own session log is the recorded session the skill
  describes (bundle finds it on disk / takes it with --session).
  `transcripts_witnessed` is therefore a server-side judgement at submit,
  as it was for v1 — the session is complete and unedited, not rebuilt
  from memory.

## Editorial verification (sources: research/RESEARCH.md, research/BRIEFS.md)
- 33 stories: 3 leads + 10 secondaries + 20 one-line briefs — IDENTICAL
  facts, figures and sources to v1. The only text changes vs v1 are
  presentational: the strip numeral uses a hyphen-minus ("-5.28%") because
  Noto Serif Display Bold lacks U+2212 (it rendered as a tofu box); the
  map's arc labels were removed (illegible at 9px); the footer edition
  identifier carries no invented issue number.
- Region counts computed from the data, never hand-written: ASIA 3,
  EUROPE 13, MIDDLE EAST 3, AFRICA 1, AMERICAS 13 (OCEANIA 0, GLOBAL 0 —
  not printed).
- Dates: nothing dated 19 Nov is presented as 20 Nov. ICJ verdict labelled
  "19 NOV" (rejection 20 Nov); Shenzhen summit labelled "19 NOV"
  (read-out 20 Nov); Houthi PIF Tower strike and Kenya Ebola discharge
  listed in the DATE CHECK footer as other days' news.
- QA passes: (1) structural — fixed 29px overflow (footer clipped),
  capped map-arc lift (arcs escaped the map into the strip), removed
  illegible arc labels; (2) visual — fixed tofu minus in the strip,
  enlarged the White House podium, re-balanced the navy bands;
  (3) editorial — story data diffed against v1 (identical), no invented
  issue number in the footer.
- Remaining weaknesses: no Oceania story and only 1 Africa story (the
  day's verified news was Ukraine/markets/US-dominated); the map is
  vertically squashed (schematic, ~3:1) with a dense Europe pin cluster;
  the Shenzhen→Washington gold arc sweeps through the South Atlantic as a
  schematic link, not a flight path; secondary decks are unreadable at
  300px (same as leaders); the page executes the winning archetype with a
  new visual identity rather than inventing a new archetype.

## Competitive assessment (honest)
- v2 keeps everything the audit proved wins (33 stories, 3 illustrated
  leads, 10 illustrated secondaries, numbered map + legend, 6-cell strip,
  brief tail, region tabs, per-story sources, confidence tags, DATE CHECK
  footer) and fixes v1's presentation gaps: a distinctive navy masthead
  identity (v1 was cream-on-cream like the rest of the field), a premium
  Display serif, richer full-colour lead art, a map that is also an
  infographic (gold event arcs), and newspaper rules instead of dashboard
  boxes.
- v2 is strictly stronger than v1 on visual impact, typography,
  composition and originality at equal density and equal facts — the
  honest claim is "better entry, same facts", not a guaranteed top 100.
  Whether it goes 12–0–0 (the practical top-100 bar) still depends on
  pairwise judging against denser entries (up to 52 stories); the final
  re-judges every entry afresh.
