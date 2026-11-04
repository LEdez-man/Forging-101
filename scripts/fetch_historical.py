#!/usr/bin/env python3
"""
fetch_historical.py – gemeinfreie Schmiede-Lehrbücher (Internet Archive, Project
Gutenberg) herunterladen und Abbildungen ins Wiki übernehmen.

Download public-domain blacksmithing textbooks and pull their figures into the wiki.

Lokal ausführen (die Cloud-Umgebung, in der das Wiki erstellt wurde, hatte
keinen Zugriff auf archive.org / gutenberg.org).

  python3 scripts/fetch_historical.py --list
  python3 scripts/fetch_historical.py --pdf               # alle IA-PDFs nach sources/pdf/
  python3 scripts/fetch_historical.py --gutenberg         # Ilgen + Googerty: Bilder + Galerieseiten
  python3 scripts/fetch_historical.py --render bacon-1904:45,46,120
        # einzelne PDF-Seiten als PNG nach content/assets/historic/<key>/ (benötigt pdftoppm/poppler)

Galerieseiten: content/de/quellen/abbildungen-<key>.md und content/en/sources/figures-<key>.md
Aus den Galerien können Abbildungen in Artikel übernommen werden:
  ![[assets/historic/ilgen-1912/fig23.jpg]]
"""
from __future__ import annotations

import argparse
import html
import io
import json
import re
import shutil
import subprocess
import sys
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
CONTENT = ROOT / "content"
PDF_DIR = ROOT / "sources" / "pdf"
ASSETS = CONTENT / "assets" / "historic"
UA = {"User-Agent": "forging-101-wiki/1.0 (personal study wiki)"}


def get(url: str) -> bytes:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


def sources():
    return json.load(open(DATA / "historical_sources.json", encoding="utf-8"))["sources"]


# ----------------------------------------------------------------- Internet Archive
def ia_pdf_url(ident: str) -> str | None:
    meta = json.loads(get(f"https://archive.org/metadata/{ident}"))
    pdfs = [f["name"] for f in meta.get("files", []) if f["name"].lower().endswith(".pdf")]
    if not pdfs:
        return None
    pdfs.sort(key=lambda n: ("_text" in n, len(n)))  # Original-PDF bevorzugen
    return f"https://archive.org/download/{ident}/{pdfs[0]}"


def download_pdfs(keys=None):
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    for s in sources():
        if keys and s["key"] not in keys:
            continue
        if not (s.get("ia") or s.get("pdf")):
            continue
        out = PDF_DIR / f"{s['key']}.pdf"
        if out.exists():
            print("vorhanden:", out.name)
            continue
        try:
            url = s.get("pdf") or ia_pdf_url(s["ia"])
            if not url:
                print("kein PDF:", s["key"])
                continue
            print("lade", url)
            out.write_bytes(get(url))
        except Exception as e:
            print("FEHLER", s["key"], e, file=sys.stderr)


def render_pages(spec: str):
    key, pages = spec.split(":")
    pdf = PDF_DIR / f"{key}.pdf"
    if not pdf.exists():
        download_pdfs([key])
    if not shutil.which("pdftoppm"):
        sys.exit("pdftoppm (poppler-utils) nicht gefunden")
    dest = ASSETS / key
    dest.mkdir(parents=True, exist_ok=True)
    for p in pages.split(","):
        p = int(p)
        subprocess.run(["pdftoppm", "-png", "-r", "110", "-f", str(p), "-l", str(p), "-singlefile",
                        str(pdf), str(dest / f"p{p:03d}")], check=True)
        print("→", dest / f"p{p:03d}.png")


# ----------------------------------------------------------------- Gutenberg
CAPTION_RX = re.compile(r"(Fig\.?\s*\d+[^<]{0,160})", re.I)


def gutenberg(source: dict):
    n = source["gutenberg"]
    key = source["key"]
    dest = ASSETS / key
    dest.mkdir(parents=True, exist_ok=True)
    data = None
    for url in (f"https://www.gutenberg.org/cache/epub/{n}/pg{n}-h.zip",
                f"https://www.gutenberg.org/files/{n}/{n}-h.zip"):
        try:
            data = get(url)
            break
        except Exception as e:
            print("…", url, e, file=sys.stderr)
    if data is None:
        sys.exit(f"Gutenberg #{n} nicht ladbar")
    z = zipfile.ZipFile(io.BytesIO(data))
    htm = next(nm for nm in z.namelist() if nm.endswith((".htm", ".html")))
    page = z.read(htm).decode("utf-8", "replace")
    base = str(Path(htm).parent)
    figures, chapter = [], ""
    # einfache sequenzielle Auswertung: Überschriften + <img> + Bildunterschrift
    for m in re.finditer(r"<h[1-3][^>]*>(.*?)</h[1-3]>|<img[^>]+src=\"([^\"]+)\"[^>]*>", page, re.S | re.I):
        if m.group(1):
            chapter = re.sub(r"<[^>]+>|\s+", " ", m.group(1)).strip()
            continue
        src = m.group(2)
        alt = re.search(r'alt="([^"]*)"', m.group(0))
        tail = page[m.end(): m.end() + 600]
        cap = CAPTION_RX.search(re.sub(r"<[^>]+>", " ", tail))
        caption = html.unescape((cap.group(1) if cap else (alt.group(1) if alt else "")).strip())
        member = str(Path(base) / src) if base not in ("", ".") else src
        try:
            blob = z.read(member)
        except KeyError:
            continue
        fname = Path(src).name
        (dest / fname).write_bytes(blob)
        figures.append(dict(file=fname, caption=re.sub(r"\s+", " ", caption), chapter=chapter))
    print(f"{key}: {len(figures)} Abbildungen → {dest}")
    json.dump(figures, open(dest / "figures.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    gallery(source, figures)


def gallery(s, figures):
    key = s["key"]
    for lang in ("de", "en"):
        de = lang == "de"
        path = CONTENT / "de" / "quellen" / f"abbildungen-{key}.md" if de else CONTENT / "en" / "sources" / f"figures-{key}.md"
        tr = f"en/sources/figures-{key}" if de else f"de/quellen/abbildungen-{key}"
        L = ["---", f'title: "{"Abbildungen" if de else "Figures"}: {s["author"].split(",")[0]} – {s["title"]} ({s["year"]})"',
             f"lang: {lang}", f"translation: {tr}", "tags: [quellen, historisch]" if de else "tags: [sources, historical]", "---",
             (f"Gemeinfreie Abbildungen aus {s['author']}, *{s['title']}* ({s['year']}), Project Gutenberg #{s.get('gutenberg')}. "
              "Automatisch erzeugt von `scripts/fetch_historical.py`.") if de else
             (f"Public-domain figures from {s['author']}, *{s['title']}* ({s['year']}), Project Gutenberg #{s.get('gutenberg')}. "
              "Generated by `scripts/fetch_historical.py`."), ""]
        chap = None
        for f in figures:
            if f["chapter"] != chap:
                chap = f["chapter"]
                L.append(f"## {chap or '—'}")
            L.append(f"![{f['caption'] or f['file']}](../../assets/historic/{key}/{f['file']})")
            L.append(f"*{f['caption']}*\n" if f["caption"] else "")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(L) + "\n", encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--pdf", nargs="*", metavar="KEY", help="PDFs laden (ohne KEY: alle)")
    ap.add_argument("--gutenberg", action="store_true", help="Gutenberg-Bücher mit Bildern laden")
    ap.add_argument("--render", metavar="KEY:SEITEN", action="append")
    a = ap.parse_args()
    if a.list or not (a.pdf is not None or a.gutenberg or a.render):
        for s in sources():
            where = s.get("ia") or (f"gutenberg #{s['gutenberg']}" if s.get("gutenberg") else s.get("url"))
            print(f"{s['key']:20} {s['year']}  {s['title'][:55]:55}  {where}")
    if a.pdf is not None:
        download_pdfs(a.pdf or None)
    if a.gutenberg:
        for s in sources():
            if s.get("gutenberg"):
                gutenberg(s)
    for r in a.render or []:
        render_pages(r)


if __name__ == "__main__":
    main()
