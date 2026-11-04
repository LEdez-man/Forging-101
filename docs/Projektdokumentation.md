# Projektdokumentation: Forging 101 – Schmiede-Wiki (DE/EN)

*Stand: 4. November 2026 · Repository `LEdez-man/Forging-101`, Branch `claude/dreamy-carson-82xvti`, Commit `be6931e` (Wiki) + diese Dokumentation*

---

## 1. Auftrag

Ursprüngliche Anfrage (sinngemäß zusammengefasst):

1. Im YouTube-Konto alle abonnierten Kanäle mit Schmiedebezug finden und prüfen, ob sie Tutorials oder Anleitungen zu Schmiedetechniken enthalten. Schwerpunkt **Black Bear Forge**, außerdem **Torbjörn Åhman** („Torbjörn Ormann“), **Nils Ögren**, **Christ Centered Ironworks** und ein **britischer Schmied, der erweiterte Grundtechniken vermittelt**.
2. Ein **Quartz-Wiki** mit Querverlinkungen und eingebetteten YouTube-Videos als Referenz erstellen.
3. Transkripte notfalls im Browser auslesen.
4. Eine **zweisprachige Anleitung (DE/EN, umschaltbar)** zu den Grundtechniken schreiben: Strecken, Breiten, Spalten, Lochen, Absetzen, Spitzen. Danach fortgeschrittene Techniken, jeweils gut erläutert.
5. Grafiken aus dem Web einbinden, auch aus gemeinfreien Büchern (Internet Archive, Web-Archive-PDFs).
6. Webseiten mit Schmiedeanleitungen suchen und einbinden.
7. Artikel als **PDF und Word** exportierbar machen.
8. Die **Gestaltung auslagern**, damit sie später anpassbar ist.

Nachträge im Gesprächsverlauf:
- Frage, was für den Zugriff auf die Abos nötig ist; danach Übermittlung der Kanal-ID `UCWa4hiH0ZqUo877_zz4M87A`.
- Auftrag, gezielt nach *Practical Blacksmithing* (PDF auf archive.org) und ähnlichen Faksimiles zu suchen.
- Wunsch nach dieser Dokumentation als Markdown.

---

## 2. Ergebnis im Überblick

| Bereich | Ergebnis |
|---|---|
| Wiki-Seiten | 119 Markdown-Seiten: 59 DE, 59 EN, 1 zweisprachige Startseite |
| Handgeschriebene Artikel | je Sprache 6 Grundlagen-, 11 Technik- und 7 Fortgeschrittenen-Artikel, dazu Übersichten, Lernpfad, Quellen, Glossar, Export-Hilfe |
| Generierte Seiten | je Sprache 6 Kanalseiten, 18 Technik-Videoseiten und eine Videoübersicht |
| Grafiken | 16 schematische Technikgrafiken als SVG, jeweils DE und EN beschriftet (32 Dateien) |
| Videodaten | 4.009 Videos aus 6 Kanälen (YouTube Data API v3), nach 18 Techniken getaggt |
| Historische Quellen | 12 gemeinfreie Werke recherchiert und verlinkt |
| Exporte | Gesamtanleitung als PDF (DE 61 S.) und DOCX, jeweils DE und EN |
| Qualitätsprüfung | Quartz-Build fehlerfrei, TypeScript-Check fehlerfrei, `check_links.py` meldet 0 Fehler (Wikilinks, Bild-Embeds, Übersetzungspaare) |

---

## 3. Vorgehen und Entscheidungen

### 3.1 Zugriff auf das YouTube-Konto
- In der Cloud-Umgebung ist für `www.googleapis.com` nur ein **API-Schlüssel** hinterlegt, kein OAuth-Token. Damit sind öffentliche Daten abrufbar (Kanäle, Videos, Playlists). Die eigenen Abos (`subscriptions?mine=true`) erfordern dagegen OAuth mit dem Scope `youtube.readonly`.
- Drei Wege wurden genannt: (a) Abos öffentlich schalten und Kanal-ID übermitteln, (b) Google-Takeout-Export `subscriptions.csv`, (c) OAuth-Connector.
- Der Kanal **„Sam P.“ (@dez_man)** wurde gefunden. Die Abo-Abfrage über die Kanal-ID lieferte bei drei Versuchen jeweils **0 Einträge**. Wahrscheinlich sind die Abos noch privat.
- **Folge:** Die Auswertung stützt sich auf die genannten Kanäle. Die Abo-Auswertung ist als Skriptfunktion vorbereitet (siehe Abschnitt 6).

### 3.2 Kanalauswahl
| Kanal | Kanal-ID | Land | Videos | Rolle im Wiki |
|---|---|---|---|---|
| Black Bear Forge (John Switzer) | `UCdOM6Qc53TcWuExrnDLVjXg` | USA | 1.044 | Hauptreferenz Grundlagen („Back to Basics“, 2025) |
| Black Bear Forge II | `UCgRV2TxlJAiHaJA5i0r0ypg` | USA | 249 | Kurzlektionen „Fundamentals of Blacksmithing“ (2021) |
| Christ Centered Ironworks | `UCVZa2bQrCprFEk0kzmarilA` | USA | 2.234 | Nummerierte Lehrreihen, Rollen, Pro-Tips |
| Mark Aspery | `UCXamijMjQKpkFF2aUzCsR8Q` | UK-ausgebildet, USA | 127 | CBA/ABANA-Curriculum, Theorie, Verbindungen |
| Torbjörn Åhman | `UCSFaYYQzNMLo2U6rSNLpghg` | Schweden | 222 | Werkzeugschmieden („A Beginners Guide“, 2025) |
| Nils Ögren | `UC57chIWkBDYmbmcVRdwG2eQ` | Schweden | 133 | Äxte, Schneidlagen, Damast |

**Annahme:** Mit dem „britischen Schmied, der erweiterte Grundtechniken vermittelt“ ist vermutlich **Mark Aspery** gemeint. Er wurde in Großbritannien ausgebildet, schrieb die Buchreihe *Mastering the Fundamentals of Blacksmithing* und hat umfangreiches Videomaterial zum CBA-/ABANA-Curriculum veröffentlicht. Die Annahme ist auf der Kanalseite gekennzeichnet. Andere Kandidaten wie Alec Steele sind eher projekt- als lehrorientiert.

### 3.3 Klassifikation der Videos
- Videotitel wurden per Stichwortliste (reguläre Ausdrücke, `data/topics.json`) 18 Techniken zugeordnet.
- Sortierung: Lehrvideos zuerst (Signalwörter wie *fundamental, basic, how to, getting started, lesson, CBA Level*), danach nach Aufrufzahl. Shorts (≤ 75 s) sind ausgeblendet.
- Die wichtigsten Lehrreihen wurden manuell kuratiert und in den Artikeln eingebettet:
  - Black Bear Forge: *The Fundamentals of Blacksmithing* (Drawing Out, Upsetting, Bending, Punching, Twisting, Cutting, Forge Welding)
  - Black Bear Forge II: *Fundamentals of Blacksmithing* (7 Grundfertigkeiten)
  - Christ Centered Ironworks: *Fundamental Instruction #1–12*, *Fundamental Scroll #1–9*, *Blacksmithing Fundamentals You Need to Know*, *Fundamentals Illustrated 101/102*, *Pro Tips #1–54*
  - Mark Aspery: *Getting Started* (CBA Level I), Playlists CBA Level I–III
  - Torbjörn Åhman: *A Beginners Guide* (Zangen, Hammerwerkzeuge, Hammer)
  - Nils Ögren: *Beginner's Guide to Forging Axes*, *Hamburger Technique*

### 3.4 Transkripte
- Der direkte Abruf über `youtube-transcript-api` wurde von YouTube mit einer Bot-Prüfung (`google.com/sorry`) blockiert.
- Ein zweiter Versuch über einen Web-Fetch-Agenten ergab: Die YouTube-Seite enthielt keine Untertitelspuren, und Transkript-Dienste (youtubetranscript.com, youtube-transcript.io, tactiq.io, downsub.com) sind per Netzwerk-Policy gesperrt.
- **Folge:** Die Videoeinordnung beruht auf **Titeln, Beschreibungen und Playlists**, nicht auf dem gesprochenen Inhalt. Das ist im Wiki vermerkt. Zum Nachholen dient `scripts/fetch_transcripts.py` (lokal ausführen).
- Die fachlichen Erläuterungen in den Artikeln stammen aus Fachwissen und Fachliteratur. Sie sind keine Transkriptzusammenfassungen.

### 3.5 Historische Quellen und Webseiten
- archive.org, gutenberg.org, Wikimedia und die meisten Fachseiten waren aus der Umgebung nicht erreichbar (Proxy 403 bzw. DNS-Sperre). Deshalb wurden **keine Grafiken heruntergeladen**.
- Die Fundstellen wurden per Websuche verifiziert und in `data/historical_sources.json` sowie auf der Quellenseite erfasst.
- `scripts/fetch_historical.py` lädt die PDFs lokal und übernimmt aus den Gutenberg-Ausgaben alle Abbildungen als Galerieseiten ins Wiki.
- **Eigene Grafiken:** Die Technikabbildungen wurden stattdessen als schematische SVGs erzeugt (`scripts/make_diagrams.py`). Sie sind lizenzfrei, zweisprachig und exportfähig.

### 3.6 Technische Architektur
- **Quartz v4.5.2** wurde per `git clone` übernommen (GitHub-Webzugriff war gesperrt, Git-Protokoll nicht).
- **Zweisprachigkeit:** getrennte Bäume `content/de/` und `content/en/`. Jede Seite trägt im Frontmatter `lang` und `translation` (Slug der Gegenseite).
- **Neue Komponente `LanguageSwitch`:** zeigt den Umschalter Deutsch/English und verlinkt die Gegenseite.
- **Explorer-Erweiterung `langRoots`:** zeigt nur den Baum der aktuellen Sprache, in didaktischer Reihenfolge statt alphabetisch.
- **Linkauflösung** `absolute`, damit gleichnamige Seiten in beiden Sprachen eindeutig bleiben.
- **Gestaltung ausgelagert:** `design/theme.ts` für Farben und Schriften (Palette „Esse & Zunder“), `design/custom.scss` für Layout, Callout-Typen `safety`/`video`/`history` und Druck-CSS.
- **Export:** `scripts/export.py` wandelt die Obsidian/Quartz-Syntax in Standard-Markdown um und erzeugt DOCX und PDF mit Pandoc. Das PDF entsteht über Chromium, mit LibreOffice als Fallback. Für Word werden die SVGs in PNG gerastert.
- **Deployment:** `.github/workflows/deploy.yml` (GitHub Pages).

---

## 4. Inhaltliche Struktur des Wikis

```
Start (DE/EN-Auswahl)
├─ Grundlagen / Basics
│   Sicherheit · Werkstatt (Esse, Amboss, Hammer, Zangen) · Glühfarben · Werkstoffe
│   Hammerführung & Grundschläge · Volumenkonstanz & Zuschnitt
├─ Grundtechniken / Basic techniques
│   Strecken · Breiten · Stauchen · Spitzen · Absetzen · Kehlen · Spalten
│   Lochen/Schlitzen/Dornen · Abschroten · Biegen & Rollen · Tordieren
├─ Fortgeschritten / Advanced
│   Feuerschweißen · Verbindungen (Nieten, Bunde, Zapfen, Durchstecken)
│   Gesenke & Lufthammer · Blattwerk & Treiben · Wärmebehandlung
│   Werkzeugbau (Zangen, Durchschläge, Hämmer, Äxte) · Damast
├─ Projekte: Lernpfad mit 12 Übungsstücken
├─ YouTube-Kanäle (6 Kanalseiten, generiert)
├─ Videos nach Technik (18 Listen + Übersichtsmatrix, generiert)
├─ Quellen & Literatur
├─ Glossar DE–EN
└─ Export & Design
```

**Aufbau eines Technikartikels:** Definition → Schemagrafik → Wirkprinzip → Werkzeuge → Arbeitsschritte → Tabelle typischer Fehler mit Ursache und Korrektur → Übungsstück → eingebettete Videos → historische Quelle → verwandte Techniken.

**Fachliche Kernaussagen, die in den Artikeln ausgeführt sind:**
- Einordnung des Handschmiedens als Freiformschmieden (DIN 8583-3) innerhalb der Fertigungsverfahren (DIN 8580).
- Materialfluss senkrecht zur schmalen Werkzeugkante: Finnenrichtung steuert Strecken versus Breiten.
- Volumenkonstanz als Grundlage der Zuschnittberechnung.
- Querschnittsverhältnis ≤ 1 : 1,5 beim Strecken (Rhombusvermeidung) und Korrektur über die lange Diagonale.
- Knickregel beim Stauchen: freie heiße Länge ≤ 2–3 × Durchmesser.
- Schlitzlänge beim Schlitzen und Dornen ≈ ½ Lochumfang.
- Kerbwirkung an scharfen Absätzen und Kehlen.
- Blausprödigkeit (200–350 °C) und Curie-Temperatur (≈ 768 °C) als Magnettest.
- Begriffsklärung Damast: Wootz-Tiegelstahl versus europäischer Schweißverbundstahl.

---

## 5. Recherchierte Quellen

### 5.1 Historische Lehrbücher (gemeinfrei)
| Werk | Fundstelle | Status |
|---|---|---|
| Richardson (Hrsg.): *Practical Blacksmithing*, Bd. I (1889) | [archive.org/details/practicalblacksm01richuoft](https://archive.org/details/practicalblacksm01richuoft) | verifiziert |
| Richardson (Hrsg.): *Practical Blacksmithing*, Bd. II (1889) | [archive.org/details/gri_33125007986793](https://archive.org/details/gri_33125007986793) | verifiziert; Bd. III/IV nur als Reprint gefunden |
| Bacon: *Forge-Practice (Elementary)* (1904) | [archive.org/details/forgepracticeele00baco](https://archive.org/details/forgepracticeele00baco) | verifiziert |
| Bacon: *Forge-Practice and Heat Treatment of Steel* (1919) | [archive.org/details/forgepracticehea00bacorich](https://archive.org/details/forgepracticehea00bacorich) | verifiziert |
| Ilgen: *Forge Work* (1912) | [Project Gutenberg #53854](https://gutenberg.org/ebooks/53854) | verifiziert, mit Abbildungen |
| Googerty: *Practical Forging and Art Smithing* (1915) | [Project Gutenberg #69488](https://gutenberg.org/ebooks/69488) | verifiziert |
| Harcourt: *Elementary Forge Practice* (1917) | [Open Library](https://openlibrary.org/works/OL7586567W), IA `elementaryforgepractice00harciala` | verifiziert |
| Sallows: *The Blacksmith's Guide* (1907) | [PDF](https://ia600503.us.archive.org/17/items/blacksmithsguide01sall/blacksmithsguide01sall.pdf) | verifiziert |
| Friese: *Farm Blacksmithing* (1921) | [archive.org/details/farmblacksmithi00friegoog](https://archive.org/details/farmblacksmithi00friegoog) | verifiziert |
| Holmstrom: *Standard Blacksmithing …* | [archive.org/details/standardblacksmi00holm](https://archive.org/details/standardblacksmi00holm) | Titel und Jahr prüfen |
| Holmstrom & Holford: *American Blacksmithing …* (1916) | IA `americanblacksmi1916holm` | Identifier aus PDF-Kopfzeile, prüfen |
| Hefner-Alteneck: *Eisenwerke oder Ornamente der Schmiedekunst …* | [AMAD (Open Access)](https://www.amad.org/jspui/handle/123456789/67883) | verifiziert |

Ein gemeinfreies **deutschsprachiges Lehrbuch zur Handschmiedetechnik** wurde auf archive.org nicht gefunden.

### 5.2 Moderne Fachliteratur (im Wiki genannt)
- **Englischsprachig:** Aspery, *Mastering the Fundamentals of Blacksmithing* I–III · Andrews, *Edge of the Anvil* · Bealer, *The Art of Blacksmithing* · Weygers, *The Complete Modern Blacksmith* · Streeter, *Professional Smithing* · Sims, *The Backyard Blacksmith*.
- **Deutschsprachig:** Schmirler, *Werk und Werkzeug des Kunstschmieds* · Kühn, *Geschmiedetes Eisen* · Hundeshagen, *Der Schmied am Amboß* · Phleps, *Schmiedekunst* (1949) · *Fachkunde Metall* / *Tabellenbuch Metall* · Zeitschrift *Hephaistos*.
- **Normen:** DIN 8580, DIN 8583-3, DIN EN ISO 4063 (Prozess 43 = Schmiedeschweißen), DIN EN 10027.

### 5.3 Webseiten
[anvilfire iForge](https://anvilfire.com/iForge/tutors.php) (u. a. [Punching Holes](https://anvilfire.com/iForge/tutor/jdpunch/index.htm)), [anvilfire eBooks – Googerty](https://anvilfire.com/eBooks/Hand_Forging_and_Wrought-Iron), [I Forge Iron](https://www.iforgeiron.com/), [ABANA](https://abana.org/), [BABA](https://www.baba.org.uk/), [Wikibooks – Down'n'dirty Blacksmithing](https://en.wikibooks.org/wiki/Down%27n%27dirty_Blacksmithing), [Chest of Books – Shop Practice](https://www.chestofbooks.com/crafts/machinery/Shop-Practice-V2/Simple-Bend-Forcing.html) sowie die Websites der Kanäle.

### 5.4 Schulen und Strömungen (Einordnung im Wiki)
- Europäische Zunft- und Kunstschmiedetradition; heute der Ausbildungsberuf Metallbauer/-in, Fachrichtung Metallgestaltung.
- **Blacksmithing Revival** ab den 1970er-Jahren (ABANA 1973, BABA 1978). Black Bear Forge, Christ Centered Ironworks und Mark Aspery stehen in dieser Linie.
- **Skandinavische Werkzeugschmiede-Tradition** (Bezug u. a. Mästermyr-Fund). Torbjörn Åhman und Nils Ögren gehören dazu.
- **Stand der Didaktik:** Kompetenzstufen-Curricula (ABANA/CBA Level I–III) mit festen Prüfstücken und Videolehre mit einer Technik je Lektion.

---

## 6. Bedienung (Kurzreferenz)

```bash
npm ci
npx quartz build --serve                         # Vorschau http://localhost:8080
python3 scripts/check_links.py                   # Links & Übersetzungspaare prüfen

python3 scripts/export.py --bundle de            # Gesamtanleitung DOCX + PDF → export/
python3 scripts/export.py content/de/techniken/strecken.md --format pdf

python3 scripts/make_diagrams.py                 # Grafiken neu erzeugen (Farben: PAL)

export YOUTUBE_API_KEY=…
python3 scripts/youtube_scan.py --fetch          # Videodaten aktualisieren
python3 scripts/youtube_scan.py --subscriptions UCWa4hiH0ZqUo877_zz4M87A
python3 scripts/youtube_scan.py --takeout subscriptions.csv

pip install youtube-transcript-api
python3 scripts/fetch_transcripts.py --limit 150

python3 scripts/fetch_historical.py --list
python3 scripts/fetch_historical.py --gutenberg --pdf
python3 scripts/fetch_historical.py --render bacon-1904:45,46
```

### Design anpassen
| Datei | Steuert |
|---|---|
| `design/theme.ts` | Farben (hell/dunkel), Schriften, Seitentitel |
| `design/custom.scss` | Lesebreite, Abbildungen, Video-Einbettungen, Sprachumschalter, Callouts, Druck |
| `design/export/pdf.css` | PDF-Layout |
| `design/export/reference.docx` | Word-Formatvorlagen (in Word bearbeiten und speichern) |
| `scripts/make_diagrams.py` (`PAL`) | Grafikfarben |
| `quartz.layout.ts` | Anordnung der Komponenten, Explorer-Reihenfolge |

---

## 7. Einschränkungen und offene Punkte

| # | Punkt | Ursache | Lösungsweg |
|---|---|---|---|
| 1 | Eigene Abos nicht ausgewertet | Abos privat bzw. Einstellung noch nicht wirksam (API liefert 0) | Abos öffentlich schalten, dann `youtube_scan.py --subscriptions …`; oder Takeout-CSV |
| 2 | Keine Transkripte | YouTube-Bot-Sperre in der Cloud; Transkriptdienste gesperrt | `fetch_transcripts.py` lokal ausführen |
| 3 | Keine historischen Abbildungen eingebunden | archive.org und gutenberg.org gesperrt | `fetch_historical.py` lokal oder Hosts in den Umgebungseinstellungen freigeben |
| 4 | Annahme Mark Aspery als „britischer Schmied“ | Name im Auftrag nicht genannt | bei Bedarf in `data/channels.json` ergänzen |
| 5 | Quartz-Bedienelemente auf EN-Seiten teils deutsch | globale `locale` in Quartz | bei Bedarf Locale je Seite in Quartz erweitern |
| 6 | Inhalte von Webseiten nur punktuell übernommen | Seiten nicht abrufbar; Urheberrecht | Verlinkung im Quellenteil; Zitate mit Quellenangabe ergänzen |
| 7 | Holmstrom-Titel nicht vollständig verifiziert | nur indirekte Fundstelle | vor Nutzung auf archive.org prüfen |
| 8 | GitHub Pages noch nicht aktiviert | Repository-Einstellung | Settings → Pages → Source: GitHub Actions; Branch nach `main` mergen |

### Empfohlene nächste Schritte
1. Abos öffentlich schalten und den Abo-Scan ausführen. Relevante neue Kanäle in `data/channels.json` aufnehmen.
2. Transkripte lokal laden. Danach lassen sich Artikel gezielt mit Zitaten und Zeitstempeln aus den Videos anreichern.
3. Historische Abbildungen laden und die passenden Figuren aus Ilgen und Googerty in die Technikartikel übernehmen.
4. Das Design in `design/` an die eigenen Vorstellungen anpassen.
5. Den Branch nach `main` mergen und GitHub Pages aktivieren.

---

## 8. Dateien dieses Projekts

| Pfad | Inhalt |
|---|---|
| `content/` | Wiki-Inhalte (DE/EN), Grafiken |
| `design/` | Gestaltung (Website, PDF, Word) |
| `data/` | Kanal- und Technikkonfiguration, Videocache, historische Quellen |
| `scripts/` | Scan-, Export-, Grafik- und Prüfskripte |
| `quartz/components/LanguageSwitch.tsx` | Sprachumschalter |
| `.github/workflows/deploy.yml` | Veröffentlichung über GitHub Pages |
| `docs/Projektdokumentation.md` | dieses Dokument |
| `export/` (nicht versioniert) | erzeugte PDF- und DOCX-Dateien |
