---
title: YouTube channels
lang: en
translation: de/kanaele/index
tags: [channel, youtube, overview]
---
**Six channels with about 4,000 videos** were analysed (as of November 2026, YouTube Data API v3). Videos were assigned to techniques by title keywords (→ [[en/videos/index|Videos by technique]]).

| Channel | Country | Videos | Value for fundamentals | Strengths |
|---|---|---|---|---|
| [[en/channels/black-bear-forge\|Black Bear Forge]] | USA | ~1,040 | ★★★★★ | Systematic fundamentals, toolmaking, forge welding |
| [[en/channels/black-bear-forge-ii\|Black Bear Forge II]] | USA | ~250 | ★★★★☆ | Short "Fundamentals" lessons |
| [[en/channels/christ-centered-ironworks\|Christ Centered Ironworks]] | USA | ~2,230 | ★★★★★ | Numbered lesson series, scrolls, Pro Tips |
| [[en/channels/mark-aspery\|Mark Aspery]] | UK/USA | ~130 | ★★★★★ | Curriculum (CBA/ABANA), theory, joinery |
| [[en/channels/torbjorn-ahman\|Torbjörn Åhman]] | Sweden | ~220 | ★★★☆☆ | Toolsmithing, hammers, dies |
| [[en/channels/nils-ogren\|Nils Ögren]] | Sweden | ~130 | ★★☆☆☆ | Axes, edge steel, pattern welding |

> [!info] Your own subscriptions
> The YouTube account's subscriptions can be analysed with `scripts/youtube_scan.py --subscriptions <channel-ID>` (subscriptions must be public) or `--takeout subscriptions.csv` (Google Takeout). The result appears on the page *Forging channels in my subscriptions* (`en/channels/subscriptions`). When the wiki was built, the account's subscriptions were still private, so this analysis is not included yet.

> [!warning] Note on method
> Video content descriptions are based on **titles, descriptions and playlists**, not on transcripts. YouTube blocked transcript access from the cloud environment. Use `scripts/fetch_transcripts.py` locally to fetch transcripts and store them as searchable pages under `transkripte/`.
