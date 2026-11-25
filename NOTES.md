# Engineering notes — news-image-20261124-r1-local

## Research first, draw second

The day (Tue 24 Nov 2026) was researched from live wires before any
drawing: Reuters, AP, Anadolu, IRNA/Tasnim, UEFA, Investopedia, IBD, CBS,
BBC. Every fact and figure in the image comes from at least two sources;
single-source items are tagged REPORTED or CLAIM and carry their outlet.
Items that could not be verified twice were dropped, never invented.

## The dating trap, and how it was avoided

The 24th was a day where the loudest names were yesterday's news. The
build deliberately refused them as leads:

- COP31 collapsed Sun 22 Nov (Antalya, no deal) — the 24th only carried
  fallout. It sits in DATE CHECK, not in the leads.
- The Russian corvette Merkury was sunk off Benghazi Sun 22 Nov dawn and
  claimed Mon 23 Nov. The 24th news is Kyiv's self-defence reply
  (story 9), not the sinking.
- Nvidia reinstated Huang Mon 23 Nov (+31% that day). The 24th news is
  his first day back at HQ plus the market reversal (−5.9%), which is
  exactly how lead 3 is framed — and DATE CHECK says the reinstatement
  itself was Monday.
- Kerch Bridge strikes were 16–19 Nov; ICJ Myanmar ruling Thu 19 Nov;
  "El Chapo Isidro" captured Fri 20 Nov; Dymer strike 22–23 Nov;
  Indonesia ship seizure disclosed Fri 20 Nov; the Megaspeed/Alibaba
  blacklisting Mon 23 Nov. All ten are listed in DATE CHECK with dates.

No lead story appears in DATE CHECK as another day's story. That is the
consistency rule the final judge punished in 20261120 (Anthropic IPO).

## Selection

35 stories. Regions: Europe 10, Middle East 9, Americas 8, Asia-Pacific
5, Africa 2, Global 1 — no region above one third of the total. Stat row
(6 numbers) comes only from the top stories: 4 tankers, Brent $91.40,
Nvidia −5.9%, Dow 50,018.70, 6 killed in Gaza, ~175 migrants missing.

## Rendering

`render.py` draws the whole page with Pillow at 1024×1024. The three
lead scenes are vector-style drawings (tanker + mine burst, night skyline
with a crown flash, chip + Mon/Tue chart), each with two data chips.
The map is a hand-coded schematic (rough continent polygons, equirect
projection) with 13 numbered pins matching story numbers. Fonts are
DejaVu Sans / DejaVu Sans Bold / DejaVu Serif Bold shipped as *.ttf
files under `fonts/` — no base64 font blocks in any source file.

Two rendering bugs found by looking at the output and fixed in-session:
scene artwork (explosion burst, tallest tower, chart) first overflowed
its lead card into the stat row; it was re-scaled to stay inside the
scene box. Map pin labels in the Middle East cluster were re-staggered
three times until all 13 read cleanly.

## Verification (local, this session)

- `python3 render.py` → entry.png, PNG magic bytes 89 50 4E 47, 1024×1024.
- Size 206,733 bytes, under the 1 MiB cap.
- `main.ts` run twice with different MAKEFUN_OUTPUT_DIR values → byte-
  identical output (sha256 compared; see check below).
- A 300 px downscale was viewed: masthead, stat row, lead scenes and
  headlines stay legible; briefs blur as expected at that size, as in
  the winning entries of the previous days.

## What is not in this entry

No network at run time; `main.ts` only copies `entry.png`. No
credentials, no secrets, no environment reads. The repository holds
only the entry, its renderer, its fonts, and these notes.
