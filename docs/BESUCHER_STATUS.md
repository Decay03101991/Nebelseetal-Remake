# Spielstatus fuer Besucher

**Stand 31.10.2026, 05:00 — Entwicklungsstand nach der Nacht vom 30./31.10.2026. Kein Release.**

Diese Fassung ist der **aktuell geprüfte Entwicklungsstand**. Die öffentliche GitHub-Version wird
laufend nachgezogen; der neueste Prüfstand liegt im Branch **`stand-20261031`** (die `main`-Historie
ist älter und hat eine andere Wurzel — deshalb Branch + Pull Request statt Force-Push).

## Was in dieser Nacht geprüft wurde (Zahlen, nicht Behauptungen)

| Prüfung | Ergebnis |
|---|---|
| **Vollständiger Prüflauf** über ALLE Prüfdateien (`tools/sammellauf.py`) | **92 Dateien, 3.463 Prüfungen, 91 grün, 0 rot, 1 dokumentiert zurückgezogen** (`test_oekonomie_kern_unabhaengig.py`, 8×7-Raster, Nachfolger 10×10), 284 s |
| Wegzeit-/Kampf-Entwurf gegen Handbuch 2009, Vorversion 2006 und Code | `docs/PRUEFUNG_ENTWURF_WEGZEIT_KAMPF_20261031.md` — **6 falsche Aussagen des Entwurfs belegt**, Entscheidungsliste von 10 auf 5 geschrumpft |
| Zwei Bewegungssysteme im Code | `docs/audits/BEWEGUNGSSYSTEME_LANDKARTE.md` — fünf Widersprüche mit Zeilennummer |
| Original-Geschichte | **gefunden**: `docs/quellen/ORIGINAL_HINTERGRUNDGESCHICHTE.md` (Website-Archiv 11.09.2007, drei Teile) |

## Entscheidungen des Spieleigners (31.10.2026)

| Frage | Entscheidung |
|---|---|
| Quellen | **Neueste Fassung ist das Original**; wo die neuere nur Werte nennt und die ältere die Mechanik beschreibt: **Mechanik alt + Zahlen neu** |
| Reisezeit | `Dauer = 2 × Distanz / GS` (anpassbar) |
| Dimensionen | kosten **keine Zeit** (nur Mana) und werden zu **Ländereien** |
| Beute | **gestaffelt**: Mauer steht → wenig; Mauer schon eingerissen → viel; keine Verteidiger → voller Bestand bis zur Karrenladung |
| Sieg | **kein Sieg** wie im Original; stattdessen **Bewertung/Auszeichnungen** |
| Antrieb | Das Einzelspieler-Spiel muss den Antrieb, den sonst andere Spieler liefern, **selbst erzeugen** — Vorschläge werden erarbeitet |

## Spielbereiche (Ist-Stand)

| Bereich | Geprüfter Stand | Noch offen |
|---|---|---|
| 127 Originalkarten, 10×10 | Als echte Bilder aktiv; 100 Kartenfelder klickbar | 25 Raster manuell grafisch abnehmen |
| Gebäude-Menüs, Sperrmeldungen | Menüpunkte erscheinen mit ihrem Gebäude, Sperren nennen das Fehlende | Baumenü-Grafik gegen Vorlage abgleichen |
| Wirtschaft, Forschung, Ausbildung | Prüfungen grün (u. a. `test_wirtschaft`, `test_forschung`, `test_ausruestung`) | Ausbildungsdauer nach Gebäudestufe (belegt, noch nicht gebaut) |
| Kampf | Wallvorrunde, Sequenzen, Beute über Karren, Geräteverlust — geprüft | **Kampfmodell-Zusammenführung** (Forum-Original + Handbuch) und gestaffelte Beute umsetzen |
| Bewegung/Aufträge | Auftragspfad vollständig (`src/auftraege.py`), Reisezeit heute Faktor 1 | Faktor 2 setzen, Altpfad der Weltkarte ablösen |
| Punkte/Schutz | Punkte je Einheit + Wallstufe³, Gesamt = (Krieg+Forschung)/2 | **kein Sieg** mehr; Götterschutz 299 Punkte/±20 % fehlt im Code |
| Windows-EXE | letzte öffentliche Testversion **FIX04j vom 28.10.2026** | neue EXE erst nach den Umbauten; in dieser Nacht kein Build |

**Ehrlich:** die EXE im Release ist **nicht** dieser Stand. Sie stammt vom 28.10.2026.

Details: [Aktueller Entwicklungsstand](AKTUELLER_STAND.md) · [Entwicklungsprotokoll](ENTWICKLUNGSPROTOKOLL.md) ·
[Prüfregister des Originals](PRUEFREGEL_ORIGINAL.md) · [Entscheidungen](ENTSCHEIDUNGEN_E1_E5_20261031.md)
