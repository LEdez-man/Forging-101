---
title: Export als PDF & Word, Design anpassen
lang: de
translation: en/export
tags: [hilfe]
---
## Export (PDF / Word)
Alle Artikel lassen sich als **Word (.docx)** und **PDF** ausgeben. Das Skript wandelt die Quartz-/Obsidian-Syntax (Wikilinks, Bild-Embeds, Callouts, YouTube-Einbettungen) in Standard-Markdown um und erzeugt die Dateien mit **Pandoc**.

```bash
# einzelne Seite
python3 scripts/export.py content/de/techniken/strecken.md

# die komplette Anleitung „Grundtechniken“ als ein Dokument (DE oder EN)
python3 scripts/export.py --bundle de
python3 scripts/export.py --bundle en

# nur Word bzw. nur PDF
python3 scripts/export.py --bundle de --format docx
```

Ergebnis: `export/`. YouTube-Videos erscheinen im Dokument als Linkliste mit Titel.

**Voraussetzungen:** `pandoc` (≥ 3). Für PDF wahlweise **Chromium/Playwright** (beste Optik, nutzt `design/export/pdf.css`) oder **LibreOffice** (konvertiert das .docx).
**Word-Formatvorlage:** `design/export/reference.docx`. In Word öffnen, Formatvorlagen (Überschrift 1–3, Standard, Tabelle) ändern und speichern; alle künftigen Exporte übernehmen das.

Alternativ: Jede Seite im Browser über **Drucken → Als PDF speichern**. Ein Druck-Stylesheet blendet Navigation und Videos aus und schreibt Link-Adressen aus.

## Design anpassen
Alle gestalterischen Vorgaben sind vom Inhalt getrennt:

| Datei | Steuert |
|---|---|
| `design/theme.ts` | Farben (hell/dunkel), Schriften, Seitentitel |
| `design/custom.scss` | Layout-Feinheiten, Lesebreite, Abbildungen, Video-Einbettungen, Sprachumschalter, Callout-Typen (`safety`, `video`, `history`), Druck-CSS |
| `design/export/pdf.css` | Erscheinungsbild der PDF-Exporte |
| `design/export/reference.docx` | Formatvorlagen der Word-Exporte |
| `scripts/make_diagrams.py` (`PAL`) | Farben der Technik-Grafiken |
| `quartz.layout.ts` | Anordnung der Komponenten (Seitenleisten, Explorer) |

## Lokale Vorschau
```bash
npm ci
npx quartz build --serve     # http://localhost:8080
```
