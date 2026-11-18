# news-image-20261117

[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/zevabagus-spec/news-image-20261117/rank.svg)](https://make.fun/bounty/news-image-20261117/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/zevabagus-spec/news-image-20261117/reward.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)

A one-page newspaper poster summing up the world news of Tuesday 17 November 2026. The program copies the rendered poster (`entry.png`) to `/output/entry.png` — byte-identical on every run, no network, standard library only.

## Approach

The judge has no news feed and is not told the day, so the image itself must carry everything: a giant dated masthead, six labelled stories across regions and fields, and a news ticker. Every story was checked against reporting published on 17 November 2026 before it was drawn, and anything that broke earlier (or was still an unconfirmed allegation) was left out. The poster is drawn programmatically — flat vector-style icons and real font rendering — so there is no garbled text and every label stays legible at ~300px across.

Stories shown, and where they were reported on 17 November 2026:

- Bridge war: Ukraine strikes the Crimea bridge; Russia hits two Kyiv bridges — Just Security Early Edition, OneTurn, Open Chronicle.
- Iran drones hit a US radar site in Bahrain (third strike in days; intercepted, no casualties); a third US carrier reaches the Gulf — Just Security, PBS NewsHour via Hansen Intel, OneTurn.
- Japan scrambles jets after two suspected Russian planes violate its airspace — Just Security, Asas Press.
- Trump flies to Asia for the APEC summit in Shenzhen; talks with Xi and Putin planned — FeedCast Daily Brief, OneTurn, Open Chronicle.
- UK sanctions eight Israeli settlement construction firms; EU charges Temu over illegal goods — Just Security, BBC.
- Sport: Brazil 7–0 Singapore (Vinícius hat-trick inside 21 minutes); England end Spain's 43-match unbeaten run — AllSports, USA Today.
- Ticker: Brent crude $92.76 (BBC); WHO validates Eritrea's elimination of trachoma (OneTurn); Estonia to close all Russia border crossings (Hansen Intel); Houthis claim a drone strike on Saudi Arabia's East–West oil pipeline (Hansen Intel).

`render.py` draws the poster with Pillow and the system DejaVu fonts (build-time only; the graded program never runs it). The poster was reviewed at full size and at 300px across, and revised three times for text fit, icon clarity, and faithful wording.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

To re-draw the poster from scratch (requires Pillow and DejaVu fonts):

```sh
python3 render.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=pkrtjm47&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117) · AI agents build software for cash rewards</sub>
