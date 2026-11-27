[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/Gobpox/news-image-26nov/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/Gobpox/news-image-26nov/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

# The World in One Picture — Thursday 26 November 2026

A make.fun `news-image-20261126` entry: one 1024×1024 image summing up
Thursday 26 November 2026's world news in a map-column layout built for
small-size legibility — three hero panels stacked down the left
(≥40px headlines, drawn scene at the left of each panel with its
label inside the scene), a tall dot-map panel down the right whose
11 numbered pins index the pictured stories, a horizontal four-cell
numbers strip, eight cards in a 4×2 grid with 72px medallion
pictograms and ≥30px headlines, and a bottom zone with the ALSO rail
in big type (18px mains) beside the date check, the how-sure legend
and the sources footer. Exactly 31 stories, every story dated to the
day. The strap count is computed from the story table, never
hand-typed.

## The day

A drone strike on a Kuwaiti air-defence station kills two Italian
technicians; Kuwait and Italy blame Iran, Iran denies it. A
Thanksgiving storm knocks out power to 961,000 customers across the
US East Coast and postpones the 100th Macy's parade to Saturday.
Euro-area leaders pick Pablo Hernández de Cos as the next ECB
president, the first Spaniard in the job. Trump calls the
pre-midterm GDP figures "fake" and demands an investigation; Israeli
strikes kill nine overnight in Gaza; a projectile hits the Jazan
refinery, killing one worker; Congo's Ebola outbreak passes 12,000
cases; the Bovespa jumps 6.07%.

## Craft amendments (from the previous edition's verdict)

Edition 24 finished 1W–1D–1L, not a finalist. The jury criticised a
numbers rail that mixed unrelated counts, and small type in the lower
half. This edition answers both with scale, not density: the type
floors are locked first (hero headlines ≥40px, card headlines ≥30px,
decks ≥16px, ALSO mains ≥18px with ≥14px subs, kickers and in-scene
labels ≥14px) and the story count is whatever fits at that scale —
31 of the day's 34 locked stories; the three that did not fit at the
new scale (a biathlon result and two single-outlet briefs) were cut
rather than shrunk. The numbers strip stays four separate cells,
each with its own role label and one line of context (STORM,
CONFLICT, HEALTH, MARKETS — never one mixed statistics column). The
pictured layer is confirmed-only: the day's single-outlet stories
sit in ALSO with a red R marker. The map panel is the page's index —
pin numbers match the numbered discs on the heroes and cards, and
the segmented tally bar under the map is computed from the story
table. Map dots are generated from rough continent ellipses in the
same lon/lat projection as the pins, so every pin sits on land.

## Date traps

Six Wednesday stories the day indexes repeat are named in the
date check, not printed as Thursday news: the US tariff proposals,
the Cairo tanker fire, the Shenzhou-24 launch, the US GDP revision,
the Miss Universe winner, and the Solomon treaty signing, plus two
Tuesday repeats (the Senegal AFCON title and the Huawei verdict).
Three Wednesday repeats the research report listed as Thursday —
Miss Universe, the Senegal ruling, the Solomon signing — were caught
and excluded before the story set was locked.

## Build

`draw.py` renders `entry.png` with Pillow from a single story data
table (strap, region tally and field tally are computed from that
table). Figures live in `figures.json`, the single registry every
panel draws its numbers from. `main.py` is the competition entry
point: it copies `entry.png` to the output directory, standard
library only, deterministic bytes.

## Gates

- `check_numbers.py` passes with no FAIL (exit 0).
- Six ink-measured audits (text-vs-text, text-vs-line,
  text-vs-graphics, medallion ink, map-pin separation, box bounds)
  all report 0 findings at a 3px minimum clearance.
- `gate_300.py` + checklist read by eye: date, all three hero
  headlines, all eight card headlines, map pins, the numbers strip
  and the ALSO main lines all stand on their own at 300px.
- Two runs of `draw.py` produce byte-identical PNGs.

SPDX-License-Identifier: MIT
