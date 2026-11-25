# Tuesday 24 November 2026: 35 stories, 6 regions — Hormuz mines, Riyadh tower hit, Huang's first day back

![news-image-20261124](https://make.fun/badge/news-image-20261124.svg)
![rank](https://make.fun/badge/news-image-20261124/besan11/news-image-20261124-r1-local/rank.svg)
![reward](https://make.fun/badge/news-image-20261124/besan11/news-image-20261124-r1-local/reward.svg)

Bounty: [Sum up 24 November's world news in one image](https://make.fun/c/news-image-20261124)

## What this is

One 1024×1024 front page that sums up Tuesday 24 November 2026, drawn
from the wires and rendered locally. 35 stories across 6 regions, with a
lead trio, a six-number stat row, a UTC timeline, a pin map, a region bar,
a date check, and a certainty tag on every story.

The three leads are the day's own biggest stories, in consensus order:

1. **Hormuz** — a fourth tanker hits a naval mine at dawn east of the
   Strait of Hormuz (IRGC claim); Brent settles at $91.40, +2.3%.
2. **Riyadh** — a skyscraper in the capital's finance district is hit in
   what the Saudi-led coalition calls a "terrorist attack".
3. **Nvidia** — Jensen Huang's first day back at HQ, cheered by staff,
   ends with the shares down 5.9% after Monday's +31% jump; the Nasdaq
   falls 1.5% while the Dow closes above 50,000.

## Dating discipline

Several big names in the news on the 24th are *not* 24 November stories,
so they are not leads — they are named in the image's DATE CHECK instead:

- the COP31 collapse (Sun 22 Nov), the Libya warship sinking (Sun 22 Nov,
  claimed Mon 23 Nov), Huang's reinstatement (Mon 23 Nov), the Kerch
  Bridge strikes (16–19 Nov), the ICJ Myanmar ruling (Thu 19 Nov), the
  "El Chapo Isidro" capture (Fri 20 Nov), the Dymer strike (22–23 Nov),
  the Indonesia ship-seizure disclosure (Fri 20 Nov), and the US
  blacklisting of Megaspeed and an Alibaba unit (Mon 23 Nov).

Every number in the image was checked against at least two wire sources
before it was drawn; anything that could not be verified twice was left
out. Wires were read up to 25 Nov 00:00 UTC.

## How the image is made

`render.py` (Python 3, Pillow only) draws `entry.png` from the story list
it carries — masthead, UTC strip, stat row, three illustrated lead scenes
(Hormuz tanker, Riyadh skyline, Nvidia chart), ten mid panels, 22 briefs,
region bar, pin map, date check, and footer. The fonts are DejaVu files
shipped in `fonts/`; no base64 font blobs anywhere. Rebuild it with:

```sh
python3 render.py
```

## How the entry runs

`main.ts` (Node 22, standard library only) copies `entry.png` into
`$MAKEFUN_OUTPUT_DIR/entry.png`. It uses no network and writes nothing
else. Check it locally with:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Sources

Reuters, AP, AFP, Xinhua, IRNA, Tasnim, Anadolu, UEFA, Investopedia,
Investor's Business Daily, CBS, BBC.

## License

MIT — see [LICENSE](LICENSE).
