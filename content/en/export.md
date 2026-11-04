---
title: Export to PDF & Word, customizing the design
lang: en
translation: de/export
tags: [help]
---
## Export (PDF / Word)
Every article can be exported as **Word (.docx)** and **PDF**. The script converts Quartz/Obsidian syntax (wikilinks, image embeds, callouts, YouTube embeds) into standard Markdown and builds the files with **Pandoc**.

```bash
# single page
python3 scripts/export.py content/en/techniques/drawing-out.md

# the complete "basic techniques" manual as one document (DE or EN)
python3 scripts/export.py --bundle en
python3 scripts/export.py --bundle de

# Word only / PDF only
python3 scripts/export.py --bundle en --format pdf
```

Output: `export/`. YouTube videos appear as a titled link list in the document.

**Requirements:** `pandoc` (≥ 3). For PDF, either **Chromium/Playwright** (best look, uses `design/export/pdf.css`) or **LibreOffice** (converts the .docx).
**Word style template:** `design/export/reference.docx`. Open it in Word, change the styles (Heading 1–3, Normal, Table) and save; all future exports pick them up.

Alternatively: print any page in the browser to **Save as PDF**. A print stylesheet hides navigation and videos and writes out link URLs.

## Customizing the design
All design decisions are kept separate from the content:

| File | Controls |
|---|---|
| `design/theme.ts` | Colours (light/dark), fonts, site title |
| `design/custom.scss` | Layout details, reading width, figures, video embeds, language switch, callout types (`safety`, `video`, `history`), print CSS |
| `design/export/pdf.css` | Look of PDF exports |
| `design/export/reference.docx` | Styles of Word exports |
| `scripts/make_diagrams.py` (`PAL`) | Colours of the technique diagrams |
| `quartz.layout.ts` | Component arrangement (sidebars, explorer) |

## Local preview
```bash
npm ci
npx quartz build --serve     # http://localhost:8080
```
