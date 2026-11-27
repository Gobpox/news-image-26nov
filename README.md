[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/Gobpox/news-image-26nov/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/Gobpox/news-image-26nov/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

# The World in One Picture — Thursday 26 November 2026

A make.fun `news-image-20261126` entry: one 1024×1024 image summing up
Thursday 26 November 2026's world news in the ATLAS layout — a
horizontal four-cell numbers strip under the masthead, three
full-width heroes, a full-width dot-map ribbon whose 13 numbered pins
index the stories below it, ten cards with square 54px medallion
pictograms, and a protected two-column bottom zone (ALSO rail left,
date check + how-sure legend + sources right). Exactly 34 stories,
every story dated to the day. The strap count is computed from the
story table, never hand-typed.

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
half. This edition keeps the ATLAS answer to both, in the same
structure: the numbers are a horizontal strip of four separate cells
in the masthead zone, each with its own role label and one line of
context (STORM, CONFLICT, HEALTH, MARKETS — never one mixed
statistics column), and the lower half is protected by one-line decks
everywhere, ALSO sub-lines carrying only a core figure and a source,
and one shared deck size for heroes and cards. The pictured layer is
confirmed-only: the day's seven single-outlet stories sit in ALSO
with a REPORTED chip. The map ribbon is the page's index — pin
numbers match the numbered discs on the heroes and cards, and the
segmented tally bar under the map is computed from the story table.
Map dots are generated from rough continent ellipses in the same
lon/lat projection as the pins, so every pin sits on land.

## Date traps

Nine stories the day indexes repeat from Wednesday are named in the
date check, not printed as Thursday news: the US tariff proposals,
the Cairo tanker fire, the Shenzhou-24 launch, the Cartagena siege,
the US GDP revision, the Miss Universe winner, and the Solomon
treaty signing (all Wednesday), plus the Senegal AFCON title and the
Huawei verdict (Tuesday). Three Wednesday repeats the research
report listed as Thursday — Miss Universe, the Senegal ruling, the
Solomon signing — were caught and excluded before the story set was
locked.

## Build

`draw.py` renders `entry.png` with Pillow from a single story data
table (strap, region tally and field tally are computed from that
table). Figures live in `figures.json`, the single registry every
panel draws its numbers from. `main.py` is the competition entry
point: it copies `entry.png` to the output directory, standard
library only, deterministic bytes.

## Gates

- `check_numbers.py` passes with no FAIL (exit 0).
- Seven ink-measured audits (text-vs-text, text-vs-line,
  text-vs-graphics, medallion frame clearance, masthead including
  the numbers-strip cells, date-check box) all report 0 findings at
  a 3px minimum clearance.
- `gate_300.py` + checklist read by eye: date, heroes, card
  headlines, strip numbers and map pins stand on their own at 300px.
- Two runs of `draw.py` produce byte-identical PNGs.

SPDX-License-Identifier: MIT
