"""
Spielzeit / Zeitfaktor (Vorgabe Daniel 05.10.2026 aus dem Spielbericht).

**Der belegte Befund:** `GameState.tick(dt_seconds)` rechnete `dt_h = dt_seconds / 3600` — also
Echtzeitsekunden 1:1 als Spielsekunden. Ein Holzfäller auf Wald („4 Holz/Stunde") lieferte damit
**4 Holz in einer echten Stunde**; im Spiel war kein regelmäßiger Rohstoffeingang zu sehen.

**Die Regel:** die Handbuchformeln bleiben unangetastet — nur die Spieluhr läuft schneller.
Diese Prüfung belegt beides: die Umrechnung des Faktors UND dass der Ertrag im Spielkern genau
um den Faktor wächst, während der Ertrag **je Spielstunde** derselbe bleibt.

Aufruf:  python tests/test_spielzeit.py
"""
from __future__ import annotations

import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, ausnahme, befund, bericht, check, import_src

ROOT, SRC = import_src()
import gelaende as G
import main as M
import spielzeit as Z

PFAD = os.path.join(ROOT, "data", "spielzeit.json")
ALT = Z.faktor()
TYPEN = ("waldreich", "bergreich", "weideland", "nebelseeufer", "gemischt")


def karte_mit(art, anzahl=1):
    for typ in TYPEN:
        for saat in range(600):
            karte = G.siedlungskarte_erzeugen(saat, typ_id=typ)
            felder = [i for i, a in enumerate(karte["raster"]) if a == art]
            if len(felder) >= anzahl:
                return karte, felder
    return None, []


# ==========================================================================
# 1. Der Faktor selbst
# ==========================================================================
abschnitt("Zeitfaktor — eine Quelle, lesbar und schreibbar")

check("die Datei data/spielzeit.json gibt es", os.path.exists(PFAD), PFAD)
daten = json.load(io.open(PFAD, encoding="utf-8"))
check("sie nennt einen Faktor", isinstance(daten.get("faktor"), (int, float)), str(daten.get("faktor")))
check("sie ist als Vorschlag gekennzeichnet (nicht belegt)", daten.get("belegt") is False,
      str(daten.get("belegt")))
check("der Standard ist 180 (1 Spielstunde = 20 Sekunden)", float(Z.STANDARD_FAKTOR) == 180.0,
      str(Z.STANDARD_FAKTOR))

try:
    Z.setzen(60.0)
    check("setzen() schreibt den Faktor und liefert ihn zurück", Z.faktor() == 60.0, str(Z.faktor()))
    roh = json.load(io.open(PFAD, encoding="utf-8"))
    check("die Datei trägt den neuen Wert (nicht nur der Zwischenspeicher)",
          float(roh["faktor"]) == 60.0, str(roh.get("faktor")))
    Z.vergessen()
    check("nach vergessen() liest das Modul den Wert aus der Datei", Z.faktor() == 60.0, str(Z.faktor()))
    check("Umkehrung: eine Spielstunde dauert bei ×60 genau 60 echte Sekunden",
          abs(Z.echtzeit_fuer_spielstunden(1.0) - 60.0) < 1e-6,
          str(Z.echtzeit_fuer_spielstunden(1.0)))
    check("Spielstunden je Echtzeitsekunde: bei ×60 sind es 60/3600",
          abs(Z.spielstunden_je_echtsekunde() - 60.0 / 3600.0) < 1e-9,
          str(Z.spielstunden_je_echtsekunde()))
    check("setzen(0) wird abgewiesen (nie Stillstand)", Z.setzen(0.0) == 60.0, str(Z.faktor()))
    check("setzen('quatsch') wird abgewiesen", Z.setzen("quatsch") == 60.0, str(Z.faktor()))
finally:
    Z.setzen(ALT)
    Z.vergessen()

check("Standardtext nennt Faktor und Sekunden je Spielstunde",
      "×180" in Z.text(180.0) and "20" in Z.text(180.0), Z.text(180.0))
check("Originaltempo wird als solches benannt", "Originaltempo" in Z.text(1.0), Z.text(1.0))
check("die Stufen enthalten den aktuellen Wert und sind sortiert",
      Z.faktor() in Z.stufen() and Z.stufen() == sorted(set(Z.stufen())), str(Z.stufen()))

# ==========================================================================
# 2. Der Faktor im Spielkern — dieselbe Ernte je SPIELstunde, mehr je Echtzeitsekunde
# ==========================================================================
abschnitt("Wirkung im Kern — Ertrag je Spielstunde bleibt, Ertrag je Echtzeitsekunde steigt")

karte, felder = karte_mit("wald", anzahl=1)
if karte is None:
    befund("keine Waldkarte gefunden — der Vergleich konnte nicht laufen")
else:
    feld = felder[0]
    versuch = M.GameState()
    versuch.settlements = []
    s = M.Settlement(name="Zeitprobe", map_id="test", karte=karte)
    ok, meldung = M.bauen_auf_karte(s, "holzfaeller", feld)
    check("Holzfäller auf Wald gebaut", ok is True, meldung)
    versuch.settlements.append(s)
    ertrag = versuch.stundenertrag()
    je_stunde = float(ertrag.get("holz", 0.0))
    check("der Ertrag JE SPIELSTUNDE ist die Handbuchzahl 4", abs(je_stunde - 4.0) < 1e-9,
          str(je_stunde))

    # Bei ×180 ist eine Echtzeitsekunde 180 Spielsekunden = 0,05 Spielstunden.
    versuch.resources["holz"].amount = 0.0
    versuch.tick(1.0 * Z.STANDARD_FAKTOR)
    nach_einer_echten_sekunde = float(versuch.resources["holz"].amount)
    check("nach EINER echten Sekunde bei ×180 sind 4 × 0,05 = 0,2 Holz da",
          abs(nach_einer_echten_sekunde - 0.2) < 1e-9, str(nach_einer_echten_sekunde))

    # Zum Vergleich: ohne Faktor (Originaltempo) bringt dieselbe echte Minute fast nichts —
    # und weil der Kern auf zwei Stellen rundet, zeigt die Kopfzeile dort sogar 0.
    versuch.resources["holz"].amount = 0.0
    versuch.tick(1.0)
    ohne_sekunde = float(versuch.resources["holz"].amount)
    check("im Originaltempo rundet EINE echte Sekunde auf 0,00 Holz — genau der Befund Daniels",
          ohne_sekunde == 0.0, str(ohne_sekunde))

    versuch.resources["holz"].amount = 0.0
    versuch.tick(60.0)
    ohne_minute = float(versuch.resources["holz"].amount)
    check("im Originaltempo bringt eine echte Minute 4/60 = 0,07 Holz", abs(ohne_minute - 0.07) < 1e-9,
          str(ohne_minute))
    check("der Eingang ist damit rund 180-mal so hoch (die Rundung auf zwei Stellen eingerechnet)",
          abs(12.0 / ohne_minute - 180.0) < 10.0,
          f"×180: 12,00 Holz je echter Minute · ×1: {ohne_minute} Holz je echter Minute "
          f"(Verhältnis {12.0 / ohne_minute:.0f}-fach)")

    # 20 echte Sekunden bei ×180 = genau eine Spielstunde → genau die Handbuchzahl.
    versuch.resources["holz"].amount = 0.0
    versuch.tick(20.0 * Z.STANDARD_FAKTOR)
    check("20 echte Sekunden bei ×180 sind eine Spielstunde — genau 4 Holz",
          abs(float(versuch.resources["holz"].amount) - 4.0) < 1e-9,
          str(versuch.resources["holz"].amount))

    # Eine echte Minute bei ×180 = drei Spielstunden → dreimal die Handbuchzahl.
    versuch.resources["holz"].amount = 0.0
    versuch.tick(60.0 * Z.STANDARD_FAKTOR)
    check("eine echte Minute bei ×180 sind drei Spielstunden — 12 Holz",
          abs(float(versuch.resources["holz"].amount) - 12.0) < 1e-9,
          str(versuch.resources["holz"].amount))

# ==========================================================================
# 3. Die Spieluhr läuft mit — ein Spieltag braucht bei ×180 nur 8 echte Minuten
# ==========================================================================
abschnitt("Tageszähler — der Tag vergeht in erreichbarer Zeit")

versuch2 = M.GameState()
versuch2.settlements = []
tag_vorher = versuch2.day
versuch2.tick(86400.0)                      # genau ein Spieltag Spielzeit
check("ein Spieltag Spielzeit schaltet den Tag weiter", versuch2.day == tag_vorher + 1,
      f"{tag_vorher} -> {versuch2.day}")
echtzeit = Z.echtzeit_fuer_spielstunden(24.0)
check("bei ×180 sind das 480 echte Sekunden (8 Minuten)", abs(echtzeit - 480.0) < 1e-6,
      f"{echtzeit:g} s")

bericht()
