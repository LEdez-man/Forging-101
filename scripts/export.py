#!/usr/bin/env python3
"""
export.py – Wiki-Artikel als Word (.docx) und PDF ausgeben.
Export wiki articles to Word (.docx) and PDF.

  python3 scripts/export.py content/de/techniken/strecken.md          # eine Seite
  python3 scripts/export.py content/de/techniken/*.md --format docx   # mehrere Seiten einzeln
  python3 scripts/export.py --bundle de                               # Anleitung „Grundtechniken“ als ein Dokument
  python3 scripts/export.py --bundle en --format pdf

Ausgabe: export/
Gestaltung: design/export/reference.docx (Word-Formatvorlagen), design/export/pdf.css (PDF)

Benötigt: pandoc ≥ 3. PDF: node + playwright (empfohlen) oder LibreOffice (soffice) als Fallback.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
OUT = ROOT / "export"
DESIGN = ROOT / "design" / "export"
HELPER = ROOT / "scripts" / "export_helper.cjs"

BUNDLES = {
    "de": dict(
        title="Schmieden – Grundtechniken und fortgeschrittene Techniken",
        subtitle="Anleitung mit Videoreferenzen · Forging 101",
        toc="Inhalt",
        pages=[
            "de/index", "de/grundlagen/sicherheit", "de/grundlagen/werkstatt", "de/grundlagen/gluehfarben",
            "de/grundlagen/werkstoffe", "de/grundlagen/hammerfuehrung", "de/grundlagen/volumenkonstanz",
            "de/techniken/index", "de/techniken/strecken", "de/techniken/breiten", "de/techniken/stauchen",
            "de/techniken/spitzen", "de/techniken/absetzen", "de/techniken/kehlen", "de/techniken/spalten",
            "de/techniken/lochen", "de/techniken/abschroten", "de/techniken/biegen", "de/techniken/tordieren",
            "de/fortgeschritten/index", "de/fortgeschritten/feuerschweissen", "de/fortgeschritten/verbindungen",
            "de/fortgeschritten/gesenke", "de/fortgeschritten/blattwerk", "de/fortgeschritten/waermebehandlung",
            "de/fortgeschritten/werkzeugbau", "de/fortgeschritten/damast", "de/projekte/lernpfad",
            "de/kanaele/index", "de/quellen/index", "de/glossar",
        ],
    ),
    "en": dict(
        title="Blacksmithing – Basic and Advanced Techniques",
        subtitle="A manual with video references · Forging 101",
        toc="Contents",
        pages=[
            "en/index", "en/basics/safety", "en/basics/workshop", "en/basics/heat-colours", "en/basics/materials",
            "en/basics/hammer-control", "en/basics/volume-constancy", "en/techniques/index", "en/techniques/drawing-out",
            "en/techniques/spreading", "en/techniques/upsetting", "en/techniques/tapering", "en/techniques/shouldering",
            "en/techniques/fullering", "en/techniques/splitting", "en/techniques/punching", "en/techniques/cutting",
            "en/techniques/bending", "en/techniques/twisting", "en/advanced/index", "en/advanced/forge-welding",
            "en/advanced/joinery", "en/advanced/swages-and-tooling", "en/advanced/leaves-and-repousse",
            "en/advanced/heat-treatment", "en/advanced/toolmaking", "en/advanced/pattern-welding",
            "en/projects/learning-path", "en/channels/index", "en/sources/index", "en/glossary",
        ],
    ),
}

CALLOUT_TITLES = {
    "tip": "Tipp / Tip", "warning": "Achtung / Warning", "safety": "Sicherheit / Safety", "note": "Hinweis / Note",
    "info": "Info", "history": "Historisch / Historical", "question": "Frage / Question", "video": "Video",
}


# ------------------------------------------------------------------ Markdown-Aufbereitung
def split_frontmatter(text: str):
    m = re.match(r"---\n(.*?)\n---\n?", text, re.S)
    if not m:
        return {}, text
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip().strip('"')
    return fm, text[m.end():]


def svg_to_png(svg: Path, tmp: Path) -> Path:
    """SVG für Word in PNG wandeln (Chromium → ImageMagick → Original)."""
    out = tmp / (hashlib.md5(str(svg).encode()).hexdigest()[:10] + ".png")
    if out.exists():
        return out
    if shutil.which("node") and HELPER.exists():
        r = subprocess.run(["node", str(HELPER), "svg2png", str(svg), str(out), "2"], capture_output=True, text=True)
        if r.returncode == 0 and out.exists():
            return out
    if shutil.which("convert"):
        r = subprocess.run(["convert", "-density", "160", str(svg), str(out)], capture_output=True)
        if r.returncode == 0 and out.exists():
            return out
    return svg


def convert_markdown(body: str, raster: bool, tmp: Path, lang: str) -> str:
    video_word = "Video" if lang == "en" else "Video"

    # Bild-Embeds ![[pfad|alt]]
    def embed(m):
        target, alt = m.group(1), (m.group(2) or "").strip()
        p = CONTENT / target
        if not p.exists():
            return f"*[{alt or target}]*"
        if raster and p.suffix == ".svg":
            p = svg_to_png(p, tmp)
        return f"![{alt}]({p.as_posix()})"

    body = re.sub(r"!\[\[([^\]|]+?)(?:\|([^\]]*))?\]\]", embed, body)

    # YouTube-Embeds → Linkzeile
    def yt(m):
        url = m.group(1)
        return f"▶ {video_word}: <{url}>"

    body = re.sub(r"!\[[^\]]*\]\((https://www\.youtube\.com/(?:watch\?v=|playlist\?list=)[^)]+)\)", yt, body)

    # Wikilinks [[ziel|text]] / [[ziel]] → Text (kursiv)
    def wl(m):
        target, alias = m.group(1), m.group(2)
        txt = alias if alias else target.split("/")[-1].replace("-", " ")
        return txt if txt in ("→",) else f"*{txt}*"

    body = re.sub(r"\[\[([^\]|\\]+?)(?:\\?\|([^\]]*))?\]\]", wl, body)

    # Callouts > [!typ] Titel → > **Titel**
    def callout(m):
        kind, title = m.group(1).lower(), m.group(2).strip()
        return f"> **{title or CALLOUT_TITLES.get(kind, kind.title())}**  "

    body = re.sub(r"^> \[!(\w+)\][+-]? ?(.*)$", callout, body, flags=re.M)

    # Pandoc braucht Leerzeilen vor Listen und Tabellen (Quartz/remark nicht)
    out, prev = [], ""
    for line in body.splitlines():
        starts_block = re.match(r"^(\d+\.|[-*]) |^\|", line)
        prev_block = re.match(r"^(\d+\.|[-*]) |^\||^\s+|^>", prev)
        if starts_block and prev.strip() and not prev_block:
            out.append("")
        out.append(line)
        prev = line
    return "\n".join(out)


def page_markdown(slug: str, raster: bool, tmp: Path, level_shift=False) -> tuple[str, str, str]:
    path = CONTENT / f"{slug}.md"
    fm, body = split_frontmatter(path.read_text(encoding="utf-8"))
    lang = fm.get("lang", slug.split("/")[0])
    title = fm.get("title", path.stem)
    md = convert_markdown(body, raster, tmp, lang)
    return title, md, lang


# ------------------------------------------------------------------ Ausgabe
def pandoc(md: str, out: Path, fmt: str, meta: dict, toc: bool, tmp: Path, toc_title="Inhalt"):
    src = tmp / (out.stem + f".{fmt}.md")
    src.write_text(md, encoding="utf-8")
    args = ["pandoc", str(src), "-f", "markdown+pipe_tables+autolink_bare_uris-tex_math_dollars", "--resource-path", str(ROOT)]
    for k, v in meta.items():
        args += ["-M", f"{k}={v}"]
    if toc:
        args += ["--toc", "--toc-depth=2", "-M", f"toc-title={toc_title}"]
    if fmt == "docx":
        ref = DESIGN / "reference.docx"
        if ref.exists():
            args += ["--reference-doc", str(ref)]
        args += ["-o", str(out)]
        subprocess.run(args, check=True)
        return out
    # PDF über HTML + Chromium
    html = tmp / (out.stem + ".html")
    args += ["-s", "--embed-resources", "--css", str(DESIGN / "pdf.css"), "-o", str(html)]
    subprocess.run(args, check=True)
    if shutil.which("node") and HELPER.exists():
        r = subprocess.run(["node", str(HELPER), "pdf", str(html), str(out)], capture_output=True, text=True)
        if r.returncode == 0:
            return out
        print("Chromium-PDF fehlgeschlagen:", r.stderr.strip()[:300], file=sys.stderr)
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if soffice:
        docx = out.with_suffix(".docx")
        if not docx.exists():
            pandoc(md, docx, "docx", meta, toc, tmp, toc_title)
        subprocess.run([soffice, "--headless", "--convert-to", "pdf", "--outdir", str(out.parent), str(docx)], check=True,
                       capture_output=True)
        return out
    sys.exit("Kein PDF-Weg verfügbar (node+playwright oder LibreOffice installieren).")


def export_pages(files, formats):
    OUT.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        for f in files:
            slug = Path(f).resolve().relative_to(CONTENT).with_suffix("").as_posix()
            for fmt in formats:
                title, md, lang = page_markdown(slug, fmt == "docx", tmp)
                out = OUT / f"{slug.replace('/', '_')}.{fmt}"
                pandoc(f"# {title}\n\n{md}", out, fmt, {"lang": lang, "pagetitle": title}, False, tmp)
                print("→", out.relative_to(ROOT))


def export_bundle(lang, formats):
    b = BUNDLES[lang]
    OUT.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        for fmt in formats:
            parts = []
            for slug in b["pages"]:
                title, md, _ = page_markdown(slug, fmt == "docx", tmp)
                parts.append(f"# {title}\n\n{md}\n")
            out = OUT / f"forging-101_{lang}.{fmt}"
            meta = {"title": b["title"], "subtitle": b["subtitle"], "date": date.today().isoformat(), "lang": lang}
            pandoc("\n\n".join(parts), out, fmt, meta, True, tmp, b["toc"])
            print("→", out.relative_to(ROOT))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="*")
    ap.add_argument("--bundle", choices=["de", "en"])
    ap.add_argument("--format", choices=["docx", "pdf", "both"], default="both")
    a = ap.parse_args()
    if not shutil.which("pandoc"):
        sys.exit("pandoc fehlt – https://pandoc.org/installing.html")
    formats = ["docx", "pdf"] if a.format == "both" else [a.format]
    if a.bundle:
        export_bundle(a.bundle, formats)
    if a.files:
        export_pages(a.files, formats)
    if not a.bundle and not a.files:
        ap.print_help()


if __name__ == "__main__":
    main()
