#!/usr/bin/env python3
"""check_links.py – prüft Wikilinks, Bild-Embeds und DE/EN-Übersetzungspaare im content/-Ordner."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "content"
pages = {p.relative_to(ROOT).with_suffix("").as_posix(): p for p in ROOT.rglob("*.md")}
files = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*") if p.is_file()}
errors = 0
for slug, p in sorted(pages.items()):
    text = p.read_text(encoding="utf-8")
    fm = re.match(r"---\n(.*?)\n---", text, re.S)
    tr = re.search(r"^translation:\s*(\S+)", fm.group(1), re.M) if fm else None
    if tr:
        t = tr.group(1)
        if t not in pages:
            print(f"[translation] {slug} → {t} fehlt"); errors += 1
        else:
            back = re.search(r"^translation:\s*(\S+)", pages[t].read_text(encoding="utf-8"), re.M)
            if not back or back.group(1) != slug:
                print(f"[translation] {t} zeigt nicht zurück auf {slug}"); errors += 1
    for m in re.finditer(r"(!?)\[\[([^\]|#\\]+)(?:#[^\]|\\]*)?(?:\\?\|[^\]]*)?\]\]", text):
        target = m.group(2).strip()
        if m.group(1):
            if target not in files:
                print(f"[embed] {slug}: {target}"); errors += 1
        elif target not in pages and target.rstrip("/") + "/index" not in pages:
            print(f"[link] {slug}: {target}"); errors += 1
print("Fehler:", errors)
sys.exit(1 if errors else 0)
