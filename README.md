# Forging 101 – Schmiede-Wiki (DE/EN)

Zweisprachiges [Quartz](https://quartz.jzhao.xyz)-Wiki zu den Grundtechniken und fortgeschrittenen Techniken des Schmiedens. Es enthält:

- **Artikel** zu Grundlagen, 11 Grundtechniken (Strecken, Breiten, Stauchen, Spitzen, Absetzen, Kehlen, Spalten, Lochen, Abschroten, Biegen, Tordieren) und 7 fortgeschrittenen Themen, jeweils auf Deutsch und Englisch, mit Umschalter auf jeder Seite.
- **16 schematische Technikgrafiken** (SVG, DE/EN) aus `scripts/make_diagrams.py`.
- **Eingebettete YouTube-Lehrvideos** von Black Bear Forge (I/II), Christ Centered Ironworks, Mark Aspery, Torbjörn Åhman und Nils Ögren. Kanal- und Technik-Videoseiten werden aus rund 4.000 Videos automatisch erzeugt.
- **Quellenteil** mit gemeinfreien historischen Lehrbüchern (Richardson, Bacon, Ilgen, Googerty, Harcourt, Sallows …), Fachliteratur und Webseiten.
- **Export** jeder Seite oder der gesamten Anleitung nach Word (.docx) und PDF.

## Struktur
```
content/            Wiki-Inhalte (Markdown)
  de/ en/           Sprachbäume; Frontmatter `lang` + `translation` verknüpft die Seitenpaare
  assets/diagrams/  generierte SVG-Grafiken
design/             ALLES Gestalterische (hier anpassen)
  theme.ts          Farben, Schriften, Seitentitel
  custom.scss       Layout, Komponenten, Callouts, Druck-CSS
  export/           pdf.css + reference.docx für Exporte
data/               channels.json, topics.json, historical_sources.json, videos/*.json (Cache)
scripts/            youtube_scan.py, fetch_transcripts.py, fetch_historical.py,
                    make_diagrams.py, export.py, check_links.py
quartz/             Quartz v4.5 (+ Komponente LanguageSwitch, Explorer-Sprachfilter)
```

## Befehle
```bash
npm ci                                    # Abhängigkeiten
npx quartz build --serve                  # Vorschau auf http://localhost:8080

python3 scripts/export.py --bundle de     # Anleitung als DOCX + PDF → export/
python3 scripts/check_links.py            # Links & Übersetzungspaare prüfen
python3 scripts/make_diagrams.py          # Grafiken neu erzeugen

export YOUTUBE_API_KEY=…                  # YouTube Data API v3
python3 scripts/youtube_scan.py --fetch   # Videodaten aktualisieren, Seiten neu erzeugen
python3 scripts/youtube_scan.py --subscriptions UCWa4hiH0ZqUo877_zz4M87A   # eigene Abos (öffentlich)
python3 scripts/youtube_scan.py --takeout subscriptions.csv              # oder Google-Takeout

pip install youtube-transcript-api
python3 scripts/fetch_transcripts.py      # Transkripte → content/transkripte/

python3 scripts/fetch_historical.py --gutenberg --pdf   # historische Bücher + Abbildungsgalerien
```

## Veröffentlichung
`.github/workflows/deploy.yml` baut die Seite bei jedem Push auf `main` und veröffentlicht sie über GitHub Pages (Repository-Einstellungen → Pages → Source: GitHub Actions). Die `baseUrl` steht in `quartz.config.ts`.

## Lizenz
Quartz: MIT (siehe `LICENSE.txt`). Eigene Texte und Grafiken: zur persönlichen Nutzung. Videos und historische Werke gehören ihren jeweiligen Urhebern bzw. sind gemeinfrei.
