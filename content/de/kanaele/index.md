---
title: YouTube-Kanäle
lang: de
translation: en/channels/index
tags: [kanal, youtube, übersicht]
---
Ausgewertet wurden **sechs Kanäle mit rund 4.000 Videos** (Stand: November 2026, YouTube Data API v3). Die Videos wurden über Titel-Stichwörter den Techniken zugeordnet (→ [[de/videos/index|Videos nach Technik]]).

| Kanal | Land | Videos | Lehrwert für Grundtechniken | Stärken |
|---|---|---|---|---|
| [[de/kanaele/black-bear-forge\|Black Bear Forge]] | USA | ~1.040 | ★★★★★ | Systematische Grundlagen, Werkzeugbau, Feuerschweißen |
| [[de/kanaele/black-bear-forge-ii\|Black Bear Forge II]] | USA | ~250 | ★★★★☆ | Kurzlektionen „Fundamentals“ |
| [[de/kanaele/christ-centered-ironworks\|Christ Centered Ironworks]] | USA | ~2.230 | ★★★★★ | Nummerierte Lehrreihen, Rollen, Pro-Tips |
| [[de/kanaele/mark-aspery\|Mark Aspery]] | UK/USA | ~130 | ★★★★★ | Curriculum (CBA/ABANA), Theorie, Verbindungen |
| [[de/kanaele/torbjorn-ahman\|Torbjörn Åhman]] | Schweden | ~220 | ★★★☆☆ | Werkzeugschmieden, Hämmer, Gesenke |
| [[de/kanaele/nils-ogren\|Nils Ögren]] | Schweden | ~130 | ★★☆☆☆ | Äxte, Schneidlagen, Damast |

> [!info] Eigene Abos
> Die Abonnements des YouTube-Kontos können mit `scripts/youtube_scan.py --subscriptions <Kanal-ID>` (Abos müssen öffentlich sein) oder `--takeout subscriptions.csv` (Google Takeout) ausgewertet werden. Das Ergebnis erscheint auf der Seite *Schmiede-Kanäle in meinen Abos* (`de/kanaele/abos`). Beim Erstellen des Wikis waren die Abos des Kontos noch privat, daher liegt diese Auswertung noch nicht vor.

> [!warning] Methodischer Hinweis
> Die Inhaltsbeschreibungen der Videos beruhen auf **Titeln, Beschreibungen und Playlists**, nicht auf Transkripten. YouTube hat den Transkriptabruf aus der Cloud-Umgebung blockiert. Mit `scripts/fetch_transcripts.py` lassen sich die Transkripte lokal nachladen und als durchsuchbare Seiten unter `transkripte/` ablegen.
