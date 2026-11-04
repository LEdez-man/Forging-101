#!/usr/bin/env python3
"""
fetch_transcripts.py – YouTube-Transkripte (automatische oder manuelle Untertitel)
für die Lehrvideos des Wikis laden und als durchsuchbare Wiki-Seiten ablegen.

Fetch YouTube transcripts for the wiki's teaching videos and store them as
searchable wiki pages.

Hinweis: In der Cloud-Umgebung, in der das Wiki erstellt wurde, blockierte
YouTube den Abruf (Bot-Prüfung). Lokal ausführen:

  pip install youtube-transcript-api
  python3 scripts/fetch_transcripts.py                    # alle Lehrvideos mit Technikbezug (Standard: max. 150)
  python3 scripts/fetch_transcripts.py --topic strecken   # nur eine Technik
  python3 scripts/fetch_transcripts.py --ids _J47QI2L36w TUJ4PCihX24
  python3 scripts/fetch_transcripts.py --limit 400

Ausgabe:
  data/transcripts/<videoId>.json        Rohdaten (Segmente mit Zeitstempel)
  content/transkripte/<videoId>.md       Wiki-Seite mit Zeitstempel-Links (Quartz-Volltextsuche!)
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from youtube_scan import load_topics, tag  # noqa: E402

DATA = ROOT / "data"
OUT_JSON = DATA / "transcripts"
OUT_MD = ROOT / "content" / "transkripte"


def candidates(topic=None, limit=150):
    topics = load_topics()
    chans = json.load(open(DATA / "channels.json", encoding="utf-8"))["channels"]
    vids = []
    for c in chans:
        d = json.load(open(DATA / "videos" / f"{c['slug']}.json", encoding="utf-8"))
        tag(d["videos"], topics)
        for v in d["videos"]:
            if v["short"] or not v["topics"]:
                continue
            if topic and topic not in v["topics"]:
                continue
            v["channel"] = c["name"]
            v["prio"] = c.get("priority", 3)
            vids.append(v)
    vids.sort(key=lambda v: (not v["tutorial"], v["prio"], -v["views"]))
    return vids[:limit]


def ts(sec: float) -> str:
    sec = int(sec)
    return f"{sec // 60}:{sec % 60:02d}"


def fetch(video_id: str):
    from youtube_transcript_api import YouTubeTranscriptApi

    api = YouTubeTranscriptApi()
    tl = api.list(video_id)
    try:
        t = tl.find_manually_created_transcript(["en", "en-GB", "en-US", "de", "sv"])
    except Exception:
        t = tl.find_transcript(["en", "en-GB", "en-US", "de", "sv"])
    segs = t.fetch()
    return t.language_code, t.is_generated, [dict(start=s.start, text=s.text) for s in segs]


def to_md(v, lang, generated, segs):
    title = v["title"].replace('"', "'")
    L = ["---", f'title: "Transkript: {title}"', "tags: [transkript, " + ", ".join(v.get("topics", [])) + "]", "---",
         f"**Kanal:** {v.get('channel','')} · **Video:** [youtube.com/watch?v={v['id']}](https://www.youtube.com/watch?v={v['id']})"
         f" · **Sprache:** {lang}{' (automatisch erzeugt)' if generated else ''}", "",
         f"![](https://www.youtube.com/watch?v={v['id']})", ""]
    # zu Absätzen von ~45 s bündeln
    para, start = [], None
    for s in segs:
        if start is None:
            start = s["start"]
        para.append(re.sub(r"\s+", " ", s["text"]).strip())
        if s["start"] - start > 45:
            L.append(f"[{ts(start)}](https://www.youtube.com/watch?v={v['id']}&t={int(start)}s) " + " ".join(para) + "\n")
            para, start = [], None
    if para:
        L.append(f"[{ts(start)}](https://www.youtube.com/watch?v={v['id']}&t={int(start)}s) " + " ".join(para) + "\n")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--topic")
    ap.add_argument("--ids", nargs="*")
    ap.add_argument("--limit", type=int, default=150)
    ap.add_argument("--sleep", type=float, default=1.5, help="Pause zwischen Abrufen (Rate-Limit)")
    a = ap.parse_args()
    OUT_JSON.mkdir(parents=True, exist_ok=True)
    OUT_MD.mkdir(parents=True, exist_ok=True)
    vids = candidates(a.topic, 10**6 if a.ids else a.limit)
    if a.ids:
        vids = [v for v in vids if v["id"] in a.ids] + [dict(id=i, title=i, topics=[]) for i in a.ids if i not in {v["id"] for v in vids}]
    ok = 0
    for v in vids:
        if (OUT_JSON / f"{v['id']}.json").exists():
            continue
        try:
            lang, gen, segs = fetch(v["id"])
        except Exception as e:
            print("–", v["id"], type(e).__name__, str(e)[:120], file=sys.stderr)
            continue
        json.dump(dict(video=v["id"], lang=lang, generated=gen, segments=segs), open(OUT_JSON / f"{v['id']}.json", "w", encoding="utf-8"), ensure_ascii=False)
        (OUT_MD / f"{v['id']}.md").write_text(to_md(v, lang, gen, segs), encoding="utf-8")
        ok += 1
        print("✔", v["id"], v["title"][:70])
        time.sleep(a.sleep)
    print(f"{ok} neue Transkripte")


if __name__ == "__main__":
    main()
