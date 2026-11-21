# DESIGN — news-image-20261120 V4 FINAL R3 (reference-layout rebuild)

## Reference
The reference image the user uploaded
(`~/workspace/user/media_library/image/file_00000000ae1882078341f34fe57eba01.png`)
— a PressPoint-style square news magazine. The user said "Maksud
saya bikin seperti ini" (make it like this). **Layout and style only**
were copied: one-row header, full-bleed hero with overlaid
chip/headline/deck/red line, photo-on-top cards with chip-on-photo +
headline + deck below, navy footer bar with globe icon and red
diagonal accent. **None of the reference's content was copied**: not
its date (Saturday, November 21, 2026), not its generic/invented
headlines, not its summit-table hero photo, not its source list
("Reuters · AP · AFP · BBC"). Our edition stays Friday, November 20,
2026, with our verified 20 Nov stories and licensed photos only.
The PressPoint website (https://preesspoint.webflow.io/) was the
original design inspiration for v4-presspoint; this rebuild follows
the uploaded image's exact layout instead.

## What changed vs v4-presspoint
- **Header is now one row**, exactly like the reference: big navy
  date (Inter Black 32 px) | vertical divider | "WORLD BRIEFING" |
  red BREAKING NEWS strip on the right (label + arrow + headline),
  then a thin navy divider below. The old two-part header (micro-bar
  + full-width breaking strip) is gone.
- **Hero is full-bleed** (1024×394) with the chip, 46 px headline,
  2-line deck and thin red accent line overlaid on the photo over a
  controlled dark gradient — as in the reference. Same Kyiv photo,
  same headline/deck.
- **Stats strip DROPPED.** The reference has none; the hero goes
  straight to the grid. No fact is lost: the "3 Kyiv bridges hit"
  figure stays in the hero deck.
- **Grid is 4×2 (8 supporting stories)**, exactly like the reference
  — this supersedes the "exactly 10 stories" rule per the user's
  correction ("Baik jadikan 8 saja sesuai gambar referensi"). Total:
  **1 hero + 8 supporting = 9 stories**. Card style is the
  reference's: photo on top filling the full card width
  (cover-cropped 235×135), coloured category chip overlaid
  bottom-left ON the photo, bold headline (16 px, max 2 lines) +
  grey deck (11 px, max 3 lines) below on white. Per-story source
  lines are gone from the cards (the reference has none); all
  sources are listed in the footer, per-story sources in STORIES.md.
- **Footer is a dark navy bar**, like the reference: globe icon,
  date, "Sources: Reuters · AP · CNN · IMD · Asia Today", a
  photo-credit line, and a red diagonal accent at the right edge.
- **DROPPED story:** France seeks UNSC meeting (SECURITY COUNCIL).
  It is a direct reaction to the hero story (the Kyiv strikes), so
  the most duplicative of the 9 supporting stories. Nothing else
  changed: the 8 kept stories keep their headlines, facts, figures,
  decks and photos byte-identical to v4-presspoint.

## Geometry (1024×1024)
| Zone | y range | Content |
|------|---------|---------|
| Header | 0–76 | One row: date 32 px Black, divider, WORLD BRIEFING 11 px, red breaking strip 36 px; navy divider at y=68 |
| Hero | 76–470 | Kyiv night photo 1024×394, red chip, white ExtraBold 46 px headline + 15 px deck (2 lines) over gradient, red accent line |
| Grid | 482–968 | 4×2 cards, 235×237, 12 px gaps; photo 235×135, chip on photo, headline 16 px (max 2 lines), deck 11 px (max 3 lines) |
| Footer | 968–1024 | Navy bar: globe icon, date 13 px, sources 12 px, photo-credit line 9 px, red diagonal slashes |

## Photo crops (reference look = cover crop)
All photos are `cover()`-cropped (scale to cover, centre-x, vertical
focus `fy` per photo). This is a deliberate break from R2's no-crop
rule: the reference's photos fill their frames, and the user's
reference instruction controls. Trump uses fy 0.45 — the face band
(eyes, nose, mouth). Hero Kyiv uses fy 0.42 (skyline + river).

## Chip colours (reference approach: one strong colour per category)
- WAR (hero): red. MARKETS: blue. WASHINGTON: purple. WEATHER:
  teal. BRUSSELS: navy. JUSTICE: red. CLIMATE: green. UNITED
  NATIONS: steel blue. AFRICA: orange. White bold text on solid
  colour, always on the photo's darker corner.

## Contrast rules (enforced in the renderer)
- Dark text on ivory/white only; white text only on the red strip,
  the coloured chips, the hero gradient (alpha up to 225/255 black),
  or the navy footer bar.
- The renderer asserts: date + breaking strip fit the header row,
  hero headline ≤ content width, hero deck ≤ 2 lines, every card
  headline ≤ 2 lines, every deck ≤ 3 lines, no text past the card
  bottom or past y 1024. A violation raises instead of rendering a
  broken image.

## What this is NOT
- Not the reference image: different date, different stories,
  different photos, different sources. Only the layout language
  matches.
- Not a broadsheet: 9 stories vs the leaderboard top 10's 33–38.
  That is a deliberate differentiation bet (visual impact and
  readability over story count) — see VERIFICATION.md for the honest
  risk note.
- Not R2: R2's uncropped photos and text-above structure are
  preserved in `v4-presspoint-r2/`; the 3×3 version of this build is
  preserved as `entry-3x3.png` in this directory.
