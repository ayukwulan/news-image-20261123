# THE WORLD TODAY — Monday 23 November 2026

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/ayukwulan/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/ayukwulan/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

A newspaper front page summing up Monday 23 November 2026 in one image:
35 verified world stories across 6 continents, a dotted world map with
12 numbered pins ("WHERE IT HAPPENED"), and a "BY THE NUMBERS" strip.

Lead story: Nvidia reinstates Jensen Huang as CEO and its shares jump
about 31%. Also on the page: Democrats clinch 258 House seats (largest
majority since 1992), COP31 ends with no deal after record-long talks,
Ukraine drones sink a Russian corvette off Benghazi, the Indonesia
factory fire (24 dead), BepiColombo reaches Mercury orbit, and more.

Every number on the page was verified against Reuters, AP, AFP, BBC,
Al Jazeera, ESA, Eurostat, or Xinhua reporting from 23 November 2026.

## How it is built

`draw.py` (Pillow, no network) draws the 1024x1024 front page and writes
`entry.png`. `main.py` (Python standard library only) copies `entry.png`
to `$MAKEFUN_OUTPUT_DIR`.

```sh
python3 draw.py
MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py
```

Running `draw.py` twice produces a byte-identical `entry.png`.
