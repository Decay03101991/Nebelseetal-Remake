# -*- coding: utf-8 -*-
"""Wache: ein gescheiterter Spielschritt beendet den Spieltest NICHT (Skip-Mechanik).

Daniel 05.11.2026, woertlich-nah: "scheitert ein Spielstand schon am Anfang an einem Test, muss das
Modell Fehler ingame ueberspringen und weiterspielen koennen, statt den Lauf zu beenden ... lieber ein
langer Lauf mit uebersprungenen Fehlern (und protokollierten Stellen) als ein kurzer, sauberer
Abbruch."

Was diese Datei beweist
-----------------------
1. Wirft `spielschicht.tick` regelmaessig eine Ausnahme, laeuft die Simulation trotzdem bis zum
   Zieltagesdatum - sie bricht NICHT nach dem ersten Fehler ab.
2. Jede uebersprungene Stelle steht mit Tag, Stelle und Grund im Log.
3. Der Bericht hat einen eigenen Abschnitt dafuer und nennt die Zahl.
4. Gegenprobe: ohne Fehler ist die Liste leer und der Abschnitt sagt das ausdruecklich.
5. Dauerfehler (ueber MAX_TICK_FEHLER_FOLGE in Folge) beendet den Lauf - dann ist der Zustand
   unbrauchbar, und das steht als Grund im Log.

Aufruf:  python -X utf8 tests/test_spieltest_skip.py
"""
from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b
# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.
PRUEF_ART = "rechnen"
PRUEF_STUFE = 1
PRUEF_BETRIFFT = ['spielschicht']
PRUEF_DATEN = []
# --- Ende Pruefstand-Kopf -------------------------------------------------------

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, bericht, check, import_src  # noqa: E402

ROOT, SRC = import_src()
sys.path.insert(0, os.path.join(ROOT, "tools"))
import spieltest_simulation as SIM  # noqa: E402

ORIGINAL_TICK = SIM.S.tick


def _tick_mit_fehler(jeder: int):
    """Ein tick, der bei jedem n-ten Aufruf eine Ausnahme wirft - sonst der echte tick."""
    zaehler = {"n": 0}

    def tick(*args, **kwargs):
        zaehler["n"] += 1
        if zaehler["n"] % jeder == 0:
            raise RuntimeError("Probe-Fehler an Schritt %d" % zaehler["n"])
        return ORIGINAL_TICK(*args, **kwargs)

    return tick


# ==========================================================================
abschnitt("1. Mit Fehlern: der Lauf haelt durch und protokolliert die Stellen")
# ==========================================================================

SIM.S.tick = _tick_mit_fehler(3)                      # jeder dritte Schritt scheitert
try:
    log = SIM.spielen(1.0, saat=7)
finally:
    SIM.S.tick = ORIGINAL_TICK                        # Messapparat zurueckstellen

uebersprungen = log.get("uebersprungen") or []
check("1 der Lauf hat uebersprungene Stellen gesammelt", len(uebersprungen) > 5,
      "%d Stellen" % len(uebersprungen))
check("1 jede Stelle nennt Tag, Stelle und Grund",
      all(len(eintrag) == 3 and eintrag[1] and eintrag[2] for eintrag in uebersprungen),
      str(uebersprungen[:2]))
check("1 die Gruende sind die echten Ausnahmen",
      all("Probe-Fehler" in str(eintrag[2]) or "RuntimeError" in str(eintrag[2])
          for eintrag in uebersprungen), str(uebersprungen[:2]))
check("1 der Lauf ist NICHT nach dem ersten Fehler abgebrochen",
      float(log["ende"]["tag"]) >= 0.9, "Ende bei Tag %s" % log["ende"]["tag"])
check("1 das Ende nennt die Zahl der Uebersprungenen",
      int(log["ende"].get("uebersprungen") or 0) == len(uebersprungen),
      str(log["ende"].get("uebersprungen")))
check("1 der Lauf hat trotz Fehlern Tagesbilanzen",
      len(log["schritte"]) >= 1, str(len(log["schritte"])))

text = SIM.bericht(log, 1.0)
check("1 der Bericht hat den Abschnitt", "Uebersprungene Schritte" in text, "")
check("1 der Bericht sagt, dass NICHT abgebrochen wurde",
      "NICHT abgebrochen" in text, "")
check("1 der Bericht nennt die Zahl der Stellen",
      "%d Stelle" % len(uebersprungen) in text, text.split("Uebersprungene Schritte")[1][:120])
check("1 der Bericht listet die Stellen als Tabelle",
      "| Spieltag | Stelle | Grund |" in text, "")

# ==========================================================================
abschnitt("2. Gegenprobe: ohne Fehler ist die Liste leer")
# ==========================================================================

log2 = SIM.spielen(1.0, saat=7)
check("2 ohne Fehler gibt es keine uebersprungenen Stellen",
      (log2.get("uebersprungen") or []) == [], str(log2.get("uebersprungen"))[:120])
text2 = SIM.bericht(log2, 1.0)
check("2 der Bericht sagt es ausdruecklich",
      "keine - jeder Schritt liess sich ausfuehren" in text2, "")

# ==========================================================================
abschnitt("3. Dauerfehler beendet den Lauf - und nennt den Grund")
# ==========================================================================

SIM.S.tick = _tick_mit_fehler(1)                      # JEDER Schritt scheitert
try:
    # Vier Spieltage, damit die Folge-Schwelle sicher erreicht wird (1 Tag = 72 Schritte).
    log3 = SIM.spielen(4.0, saat=7)
finally:
    SIM.S.tick = ORIGINAL_TICK

check("3 bei Dauerfehler bricht der Lauf ab (Zustand unbrauchbar)",
      len(log3.get("uebersprungen") or []) >= SIM.MAX_TICK_FEHLER_FOLGE,
      "%d Fehler" % len(log3.get("uebersprungen") or []))
check("3 der Abbruchgrund steht im Log",
      any("nicht mehr belastbar" in str(e) for e in log3.get("ereignisse") or []),
      str((log3.get("ereignisse") or [])[-1:]))
check("3 der Bericht entsteht trotzdem", bool(SIM.bericht(log3, 1.0)))

# ==========================================================================
abschnitt("4. Quellwache: kein blankes break nach einem Tick-Fehler")
# ==========================================================================

quelltext = open(os.path.join(ROOT, "tools", "spieltest_simulation.py"), encoding="utf-8").read()
check("4 die Skip-Mechanik ist im Werkzeug benannt",
      "MAX_TICK_FEHLER_FOLGE" in quelltext and "NICHT abbrechen" in quelltext, "")
check("4 der Berichtsabschnitt steht im Werkzeug",
      "Uebersprungene Schritte" in quelltext, "")

sys.exit(bericht())
