# Dokumenten- und Quellenpruefung (Konsolidierung 28.10.2026)

Dies ist ein **aus Dateiinhalt und SHA-256 erstellter Index** der vorhandenen Dokumente. Die Inhalte wurden technisch eingelesen und nach aktuellen, urspruenglichen und historischen Dokumenten eingeordnet. Das ist keine individuelle fachliche Validierung jeder Bildseite oder jeder alten Behauptung.

- **218** textbasierte Dokumente/Quellen im ersten Pruefdurchgang erfasst; davon 11 damalige Hauptdokumente, 75 Quellen bzw. Originaltexte und 127 im Archiv.
- **6** Gruppen bytegleicher Textdateien; Duplikate nicht pauschal geloescht.
- Besonderheit: `Nebelseetal_Spielanleitung_2009.odt` war in Wirklichkeit eine PDF, exakt identisch zur `.pdf`. Die falsch benannte Datei ist nun im Archiv, die PDF bleibt die fuehrende Quelle.
- **Quellenkorrektur:** Die PDF mit Dateinamen `...2009.pdf` traegt innen das Datum **01.09.2006**. Dateiname und inhaltlicher Stand sind daher nicht gleichzusetzen.

## Aktuelle Dokumente (fuehrend)

- [`docs/AGENTEN_PLAN.md`](AGENTEN_PLAN.md) — Agenten- und Modellplan
- [`docs/AKTUELLER_STAND.md`](AKTUELLER_STAND.md) — Nebelseetal Remake – aktueller Entwicklungsstand
- [`docs/BAUMENUE_ABGLEICH.md`](BAUMENUE_ABGLEICH.md) — Originalreferenz: Gebaeude-Baumenue (Gamestar2)
- [`docs/BESUCHER_STATUS.md`](BESUCHER_STATUS.md) — Spielstatus fuer Besucher
- [`docs/BILDINVENTAR.md`](BILDINVENTAR.md) — Bildinventar und Altlastenpruefung
- [`docs/ENTWICKLUNGSPROTOKOLL.md`](ENTWICKLUNGSPROTOKOLL.md) — Entwicklungsprotokoll — Nebelseetal Remake
- [`docs/HERMES_UEBERGABE_AKTUELL.md`](HERMES_UEBERGABE_AKTUELL.md) — EINZIGE AKTUELLE UEBERGABE FUER HERMES
- [`docs/LEHREN.md`](LEHREN.md) — Lehren aus der Sitzung vom 04.10.2026
- [`docs/ORDNUNG.md`](ORDNUNG.md) — Verbindliche Projektordnung
- [`docs/SPIEL_TESTEN.md`](SPIEL_TESTEN.md) — Nebelseetal ausprobieren (experimentell)
- [`docs/WEG_ZUR_EXE.md`](WEG_ZUR_EXE.md) — Weg zur fertigen .exe — Zieldefinition und Prüfmaßstab

- [`docs/QUELLEN_UND_DOKUMENTE.md`](QUELLEN_UND_DOKUMENTE.md) — dieser aktuelle Quellenindex (nach der Erstinventur erstellt)
- [`docs/WINDOWS_EXE_HERSTELLUNG.md`](WINDOWS_EXE_HERSTELLUNG.md) — aktuelle Windows-Bauanleitung (nach der Erstinventur erstellt)

## Originalquellen und direkte Referenzen
Die Originalquellen sind Nachweise, **keine zweite aktive Projekt-Roadmap**.

- `docs/original/00_QUELLEN.md` — Quellen der Originaldaten
- `docs/original/GPT_NE01_Funde/TutorialundBeschreibung_einesSpielers(1).odt` — Tutorial
- `docs/original/GPT_NE01_Funde/WeitereWerteKampfsystem.odt` — Wissenswertes
- `docs/original/Nebelseetal_Spielanleitung_2009.pdf` — Nebelseetal Online
- `docs/original/ORIGINAL_Einheiten_Waren_Rohstoffe.md` — Originaldaten: Einheiten, Waren, Rohstoffe, Forschung
- `docs/original/ORIGINAL_Kampf_und_Punkte.md` — Originaldaten: Kampf, Aufträge, Punkte, Schutz
- `docs/original/ORIGINAL_Werte_Einheiten.md` — Original-Werte der 28 Einheiten
- `docs/original/assets_website/QUELLEN.md` — Original-Assets der Website nebelseetal.de
- `docs/original/karten/QUELLEN.md` — Quellen: Originalbilder Nebelseetal (web.archive.org)
- `docs/original/karten/QUELLEN_COMMONCRAWL.md` — Quellen: Common Crawl — Bildsuche Nebelseetal.de
- `docs/original/karten/QUELLEN_WEB.md` — WEB-QUELLEN — Nebelseetal (Karten, Screenshots, Gelände)
- `docs/original/karten/commoncrawl/README.md` — Common Crawl — Funde für Nebelseetal.de
- `docs/original/karten_sammlung_odt/Karten_BesteKarten.odt` — Siedlungskartenübersicht
- `docs/original/karten_sammlung_odt/Karten_MittlereKarten.odt` — Siedlungskartenübersicht
- `docs/original/karten_sammlung_odt/Karten_SchlechteKarten.odt` — Siedlungskartenübersicht
- `docs/quellen/Das_Kampfsystem_Neu_Original.odt` — Das Kampfsystem
- `docs/quellen/Tutorial_eines_Spielers_Original_28-10-2026.odt` — Tutorial
- `docs/quellen/WeitereWerteKampfsystem_Original_28-10-2026.odt` — Wissenswertes

## Historische Inhalte / Archiv

Weitere 127 indexierte, bereits archivierte Textdokumente bleiben fuer Rueckverfolgung erhalten. Sie sind nicht gegenueber der einzigen aktuellen Fassung massgeblich.
`archiv/manifeste/DOKUMENTE_VOLLINVENTAR.json` enthaelt alle Dateipfade, Inhaltstitel, Bytegroessen und SHA-256, damit Hermes alte Befunde auf neue Entscheidungen zurueckverfolgen kann.

## Prioritaet bei Widerspruechen

1. Verifizierter aktueller Quellcode und Tests dieser Kopie, **vorbehaltlich Hermes-Abnahme**.
2. `docs/ENTWICKLUNGSPROTOKOLL.md` als einzige Fortschrittschronik; `docs/AKTUELLER_STAND.md` als Kurzuebersicht.
3. Original-Handbuch, authentische Quellseiten/Bilder und Datenwerte als Regelnachweis; klare Kennzeichnung bei Remake-Vorschlaegen.
4. Archivtexte und alte GPT-Zusammenfassungen nur als Historie, nicht als Anweisung.

## Noch manuell zu pruefen

- Originalrechte und Bildlizenzen vor oeffentlicher Distribution.
- 25 grafisch offene Originalkarten.
- GUI-Abnahme des historischen Baumenues; Screenshot ist kein implementiertes Bedienfenster.
- Alle Abweichungen von Regeldaten und alten Testannahmen im spielbaren Durchlauf.


**Nachtrag Originalkarten-Umstellung:** Das fruehere Vollinventar in `archiv/manifeste/DOKUMENTE_VOLLINVENTAR.json` ist eine Bestandsaufnahme **vor** der Originalgrafik-Umstellung. Die jetzt gueltigen Pfade, Status und Skills stehen in `docs/AKTUELLER_STAND.md`, `docs/KARTEN_NUR_ORIGINALE.md`, `docs/HERMES_KONTROLLE_UND_SKILLS.md`. Die aktuellen 127 aufbereiteten Bildgrafiken sind in `data/originalkarten/grafik_manifest.json` inventarisiert.
