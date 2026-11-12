# -*- coding: ascii -*-
"""Gebaeude-Optik: Menue-Icons, Menue-Hintergruende und ihre Skalierung (Auftrag B4).

Entstanden aus dem starken Modellaufruf B4 (deepseek-v4-pro, 02.11.2026,
`docs/auftraege/B4_paket_20261102.md`, Bericht `docs/audits/BERICHT_B4_20261102.md`). Der Koordinator
hat zwei Dinge korrigiert, bevor die Datei lief:
  * Die Pruefdatei benutzte `import_src("modul")` - `tests/harness.py` liefert mit `import_src()` aber
    ein Paar `(ROOT, SRC)` ohne Argument; das Modul wird danach normal importiert.
  * Das Modul las die Bilder aus `archiv/eingaben/...` - dieses Verzeichnis ist gitignored und waere in
    einer Auslieferung nicht dabei. Die Bilder liegen jetzt unter `assets/icons/gebaeude/menue/` bzw.
    `.../hintergrund/`, und die Projektwurzel kommt aus `spieldaten.projektwurzel()` (EXE-fest).

Was die Datei belegt: alle 20 Gebaeude aus `data/buildings.json` haben genau ein Icon und einen
Hintergrund, jede Datei hat die gelieferte Groesse, Skalierung erhaelt das Seitenverhaeltnis, und
unbekannte ids liefern None statt einer Ausnahme.

Aufruf:  python -X utf8 tests/test_gebaeude_optik.py
"""

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b
# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.
PRUEF_ART = "rechnen"
PRUEF_STUFE = 1
PRUEF_BETRIFFT = ['auftraege', 'gebaeude_optik', 'main:*', 'spieldaten']
PRUEF_DATEN = ['buildings.json']
# --- Ende Pruefstand-Kopf -------------------------------------------------------
import json  # Liest JSON-Daten.
import os  # Stellt Pfadfunktionen bereit.
import sys  # Stellt Systemfunktionen bereit.
import tempfile  # Erstellt temporaere Verzeichnisse.
from pathlib import Path  # Bietet Pfadobjekte.

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # Macht das Pruefgeruest importierbar.
from harness import abschnitt, befund, bericht, check, import_src  # Importiert die Test-Hilfsfunktionen.

ROOT, SRC = import_src()  # Liefert Projektwurzel und src-Pfad und haengt src in den Suchpfad.
import gebaeude_optik as gb  # Das zu pruefende Modul.

try:  # Pillow ist fuer die Bildpruefungen noetig.
    from PIL import Image  # Bildmodul.
except ImportError:  # ohne Pillow
    Image = None  # dann werden die Bildpruefungen uebersprungen.

def main():  # Steuert den Testablauf.
    abschnitt("Gebaeude-Optik Modul importieren")  # Meldet den ersten Abschnitt.
    check("Modul gebaeude_optik wurde geladen", gb is not None)  # Prueft den Import.

    abschnitt("Datenkonsistenz")  # Meldet den Abschnitt zur Datenkonsistenz.
    projekt_root = Path(ROOT)  # Projektwurzel aus dem Pruefgeruest.
    daten_pfad = projekt_root / "data" / "buildings.json"  # Baut den Pfad zur Datendatei.
    with daten_pfad.open("r", encoding="utf-8") as datei:  # Oeffnet die JSON-Datei.
        bau_daten = json.load(datei)  # Laedt die Gebaeudedaten.
    ids = [eintrag["id"] for eintrag in bau_daten.get("gebaeude", [])]  # Extrahiert die Gebaeude-ids.

    check("data/buildings.json enthaelt 20 Gebaeude", len(ids) == 20)  # Prueft die Anzahl.
    check("Keine doppelten Gebaeude-ids", len(set(ids)) == len(ids))  # Prueft auf Dubletten.
    check("ICONS enthaelt genau die 20 Gebaeude-ids", set(gb.ICONS.keys()) == set(ids))  # Prueft die Icon-Schluessel.
    check("HINTERGRUENDE enthaelt genau die 20 Gebaeude-ids", set(gb.HINTERGRUENDE.keys()) == set(ids))  # Prueft die Hintergrund-Schluessel.
    check("Kein Bild ohne Gebaeude (keine Extra-keys)", len(gb.ICONS) == len(ids) and len(gb.HINTERGRUENDE) == len(ids))  # Prueft die Mengen.

    abschnitt("Dateien und Bildgroessen")  # Meldet den Abschnitt zu Dateien und Groessen.
    for bid in ids:  # Durchlaeuft alle Gebaeude-ids.
        icon_pfad = Path(gb.pfad_icon(bid))  # Baut den Icon-Pfad.
        check(f"Icon-Datei fuer {bid} existiert", icon_pfad.is_file())  # Prueft die Existenz.
        if icon_pfad.is_file():  # Oeffnet die Datei nur, wenn vorhanden.
            with Image.open(icon_pfad) as bild:  # Oeffnet das Icon.
                check(f"Icon {bid} ist ein PNG", bild.format == "PNG")  # Prueft das Format.
                check(f"Icon {bid} hat Groesse 256x256", bild.size == (256, 256))  # Prueft die Groesse.
                check(f"Icon {bid} ist RGBA", bild.mode == "RGBA")  # Prueft den Farbmodus.
        hintergrund_pfad = Path(gb.pfad_hintergrund(bid))  # Baut den Hintergrund-Pfad.
        check(f"Hintergrund-Datei fuer {bid} existiert", hintergrund_pfad.is_file())  # Prueft die Existenz.
        if hintergrund_pfad.is_file():  # Oeffnet die Datei nur, wenn vorhanden.
            with Image.open(hintergrund_pfad) as bild:  # Oeffnet den Hintergrund.
                check(f"Hintergrund {bid} ist ein PNG", bild.format == "PNG")  # Prueft das Format.
                check(f"Hintergrund {bid} hat Groesse 538x222", bild.size == (538, 222))  # Prueft die Groesse.
                check(f"Hintergrund {bid} ist RGBA (geliefert so, Register 123)", bild.mode in ("RGBA", "RGB"))  # Farbmodus wie geliefert.

    abschnitt("Skalierung und Seitenverhaeltnis")  # Meldet den Abschnitt zur Skalierung.
    test_id = ids[0]  # Waehlt die erste Gebaeude-id als Beispiel.
    kachel_bild = gb.kachel(test_id, 80)  # Erstellt eine Icon-Kachel.
    check("kachel liefert ein Bild", kachel_bild is not None)  # Prueft die Rueckgabe.
    if kachel_bild is not None:  # Prueft die Groesse nur, wenn ein Bild vorhanden ist.
        check("Icon-Kachel hat die erwartete Groesse 80x80", kachel_bild.size == (80, 80))  # Prueft die Groesse.
    hintergrund_bild = gb.hintergrund(test_id, 80)  # Skaliert den Hintergrund.
    erwartete_hoehe = round(80 * 222 / 538)  # Berechnet die erwartete Hoehe.
    check("hintergrund liefert ein Bild", hintergrund_bild is not None)  # Prueft die Rueckgabe.
    if hintergrund_bild is not None:  # Prueft die Groesse nur, wenn ein Bild vorhanden ist.
        check("Hintergrund hat die erwartete proportionale Groesse", hintergrund_bild.size == (80, erwartete_hoehe))  # Prueft die Groesse.

    abschnitt("Unbekannte Gebaeude")  # Meldet den Abschnitt fuer unbekannte ids.
    check("pfad_icon liefert None fuer unbekannte id", gb.pfad_icon("gibt_es_nicht") is None)  # Prueft die Rueckgabe.
    check("pfad_hintergrund liefert None fuer unbekannte id", gb.pfad_hintergrund("gibt_es_nicht") is None)  # Prueft die Rueckgabe.
    check("kachel liefert None fuer unbekannte id", gb.kachel("gibt_es_nicht", 80) is None)  # Prueft die Rueckgabe.
    check("hintergrund liefert None fuer unbekannte id", gb.hintergrund("gibt_es_nicht", 80) is None)  # Prueft die Rueckgabe.

    abschnitt("Fehlende Gebaeude")  # Meldet den Abschnitt zu fehlenden Icons.
    check("fehlende_gebaeude ist leer", gb.fehlende_gebaeude() == [])  # Prueft die leere Liste.
    original_ids = list(gb._IDS)  # Kopiert die urspruengliche id-Liste.
    original_icons = dict(gb.ICONS)  # Kopiert das urspruengliche Icon-Woerterbuch.
    gb._IDS = original_ids + ["test_fehlend"]  # Fuegt eine Test-id hinzu.
    gb.ICONS["test_fehlend"] = str(Path("/nicht/vorhanden/test_fehlend.png"))  # Setzt einen ungueltigen Pfad.
    fehlend = gb.fehlende_gebaeude()  # Ruft die Funktion mit manipulierten Daten auf.
    check("fehlende_gebaeude nennt die fehlende Test-id", "test_fehlend" in fehlend)  # Prueft die Rueckgabe.
    gb._IDS = original_ids  # Stellt die urspruengliche id-Liste wieder her.
    gb.ICONS = original_icons  # Stellt das urspruengliche Icon-Woerterbuch wieder her.

    abschnitt("Vorschaublatt")  # Meldet den Abschnitt zum Vorschaublatt.
    with tempfile.TemporaryDirectory() as tmp:  # Erzeugt ein temporaeres Verzeichnis.
        ziel = Path(tmp) / "vorschau.png"  # Baut den Zielpfad.
        rueckgabe = gb.vorschau_blatt(str(ziel), spalten=5)  # Erzeugt das Vorschaublatt.
        check("vorschau_blatt gibt den Zielpfad zurueck", rueckgabe == str(ziel))  # Prueft die Rueckgabe.
        check("vorschau_blatt schreibt eine Datei", ziel.is_file())  # Prueft die Existenz.
        if ziel.is_file():  # Oeffnet das Blatt nur, wenn vorhanden.
            with Image.open(ziel) as blatt:  # Oeffnet das erzeugte Bild.
                with Image.open(gb.ICONS[ids[0]]) as referenz:  # Oeffnet das erste Icon als Referenz.
                    icon_breite, icon_hoehe = referenz.size  # Liest die tatsaechliche Icon-Groesse.
                spalten = 5  # Legt die Spaltenzahl fest.
                zeilen = (len(ids) + spalten - 1) // spalten  # Berechnet die Zeilenzahl.
                erwartete_breite = spalten * icon_breite  # Berechnet die erwartete Breite.
                erwartete_hoehe = zeilen * (icon_hoehe + gb.BESCHRIFTUNGSBAND)  # Zellhoehe plus Beschriftungsband.
                check("vorschau_blatt hat die erwarteten Masse", blatt.size == (erwartete_breite, erwartete_hoehe))  # Prueft die Groesse.

    sys.exit(bericht())  # Beendet mit dem Gesamtergebnis.

if __name__ == "__main__":  # Startet den Test nur bei direkter Ausfuehrung.
    main()  # Ruft die Teststeuerung auf.
