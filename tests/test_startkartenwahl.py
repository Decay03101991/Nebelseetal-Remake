# -*- coding: ascii -*-
"""Startkarte des Spielers: GEZOGEN statt gewaehlt (Register 225, Daniel 05.11.2026).

WAS SICH GEANDERT HAT
---------------------
Bis 05.11.2026 zeigte das Dorfzentrum eine Wahl aus DREI Karten (A2-Vorstufe, Vorgabe Daniel
02.11.2026). Daniel hat am 05.11.2026 entschieden (Register 225): "Wir sollten die Orginaltreue
wa[h]ren. Die bots und spieler erhalten eine karte und falls sie fuer Ihren Zweck nicht gut genug
sind, muessen sie die karte loeschen, verlieren die gruendungs ressourcen und muessen neu sparen".

Original (docs/original/Spielanleitung_2005/siedeln.php.txt, Zeilen 10-13): einer neuen Siedlung
wird per Zufall eine Karte zugewiesen; niemals bekommen zwei eigene Siedlungen dieselbe; nach dem
Aufgeben darf dieselbe Karte bei einer Neugruendung wieder auftauchen.

Was diese Datei beweist
-----------------------
1. Die Datendatei nennt Ziehung und Aufgeben als Regel (keine Zahl im Code).
2. `startkarte_ziehung` liefert EINE echte Katalogkarte, reproduzierbar je Startsaat, ohne die
   Karten, die das eigene Reich schon haelt.
3. Die Startseite schreibt die gezogene Karte in den Spielstand, und die Gruendung nimmt GENAU
   diese Karte.
4. Der alte Weg (drei Kandidaten zur freien Wahl) ist aus dem Startbild verschwunden - er steht
   nur noch als Funktion fuer Vergleichsmessungen da und wird von main.py nicht mehr benutzt.

Aufruf:  python -X utf8 tests/test_startkartenwahl.py
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, bericht, check, import_src  # noqa: E402

ROOT, SRC = import_src()
import main as M  # noqa: E402
import originalkarten as O  # noqa: E402
import spieloekonomie as S  # noqa: E402

TEXT_MAIN = open(os.path.join(SRC, "main.py"), encoding="utf-8").read()

# ==========================================================================
abschnitt("1. Die Datendatei nennt die neue Regel")
# ==========================================================================

_pfad = os.path.join(ROOT, "data", "startkarte.json")
check("die Datendatei existiert", os.path.exists(_pfad), _pfad)
with open(_pfad, encoding="utf-8") as _f:
    _cfg = json.load(_f)
check("das Speicherfeld ist benannt", bool(str(_cfg.get("speicherfeld") or "")),
      str(_cfg.get("speicherfeld")))
check("die belegte Standardkarte steht weiter in der Datei",
      _cfg.get("standard_karte") == O.START_ID,
      "%s / %s" % (_cfg.get("standard_karte"), O.START_ID))
check("die Datei beschreibt die ZIEHUNG",
      "Gleichverteilt" in str(_cfg.get("_ziehung") or "")
      and "keine freie Wahl" in str(_cfg.get("_ziehung") or ""), "")
check("die Datei beschreibt das AUFGEBEN mit Quelle",
      "siedeln.php" in str(_cfg.get("_aufgeben") or ""), "")
check("die Datei nennt den Grund der Ein-Siedlung-Sperre",
      "ohne Ausweg" in str(_cfg.get("_warum_die_einsiedlungssperre") or ""), "")

# ==========================================================================
abschnitt("2. Die Ziehung: eine Karte, reproduzierbar, ohne die eigenen")
# ==========================================================================

_ids = set(O.kennungen())
_karte = S.startkarte_ziehung("nebel-probe-20261105")
check("die Ziehung liefert eine echte Katalogkarte",
      _karte.get("originalkarte_id") in _ids, str(_karte.get("originalkarte_id")))
check("die Karte bringt ihre Felder mit", bool(_karte.get("zaehlung")), "")
check("dieselbe Startsaat zieht dieselbe Karte",
      S.startkarte_ziehung("nebel-probe-20261105").get("originalkarte_id")
      == _karte.get("originalkarte_id"), "")
check("zwei verschiedene Saaten ziehen verschiedene Karten",
      S.startkarte_ziehung("nebel-anders").get("originalkarte_id")
      != _karte.get("originalkarte_id"), "")
check("eine gehaltene Karte wird nicht noch einmal gezogen",
      S.startkarte_ziehung("nebel-probe-20261105",
                           [_karte.get("originalkarte_id")]).get("originalkarte_id")
      != _karte.get("originalkarte_id"), "")
_belegt = {S.startkarte_ziehung("s-%d" % i).get("originalkarte_id") for i in range(80)}
check("die Ziehung deckt viele Karten ab (kein toter Zufall)",
      len(_belegt) > 30, "%d verschiedene Karten bei 80 Saaten" % len(_belegt))
check("jede gezogene Karte ist im Katalog", _belegt <= _ids, str(len(_belegt - _ids)))

# ==========================================================================
abschnitt("3. Die Startseite zieht und die Gruendung nimmt die Karte")
# ==========================================================================

import tkinter as tk  # noqa: E402

root = tk.Tk()
root.withdraw()
app = M.NebelseetalApp(root)
app._build_main_ui()
check("ohne Wahl zieht die Startseite beim Anzeigen der Karte",
      str(app.state.startkarte_gewaehlt) == "", app.state.startkarte_gewaehlt)
_gezogen = app._startkarte_ziehen()
check("die gezogene Kennung steht im Spielstand", app.state.startkarte_gewaehlt == _gezogen,
      app.state.startkarte_gewaehlt)
check("die Kennung ist eine echte Karte", _gezogen in _ids, _gezogen)


def _texte(app_):
    gesammelt = []

    def _durch(w):
        try:
            gesammelt.append(str(w.cget("text")))
        except Exception:                                            # noqa: BLE001
            pass
        for k in w.winfo_children():
            _durch(k)

    for k in app_.content.winfo_children():
        _durch(k)
    return gesammelt


app._switch_view(M.KARTENGRUENDUNG_ANSICHT)
app._start_schritt = "karte"                     # Schritt 3 zeigen (das Volk ist noch offen)
app._render_view()
app.content.update_idletasks()
_seite = _texte(app)
check("die Seite zeigt die gezogene Karte",
      any("Deine Karte" in t for t in _seite), str(_seite[:3]))
check("die Seite bietet die Gruendung mit dieser Karte an",
      any("Auf dieser Karte gr" in t for t in _seite), "")
app.state.spieler_fraktion = "menschlich"
app._erste_siedlung_gruenden()
check("die Siedlung entsteht", len(app.state.settlements) == 1, str(len(app.state.settlements)))
check("die Siedlung traegt die GEZOGENE Karte",
      (app.state.settlements[0].karte or {}).get("originalkarte_id") == _gezogen,
      str((app.state.settlements[0].karte or {}).get("originalkarte_id")))
root.destroy()

# ==========================================================================
abschnitt("4. Der alte Weg (drei Kandidaten) ist aus dem Startbild verschwunden")
# ==========================================================================

check("die freie Wahl steht nicht mehr in main.py",
      "startkarte_kandidaten" not in TEXT_MAIN, "")
check("die Auswahlerforderung steht nicht mehr in main.py",
      "startkarte_auswahl_erforderlich" not in TEXT_MAIN, "")
check("die alte Maske ist geloescht",
      "_startkarte_wahl_block" not in TEXT_MAIN and "Diese Karte nehmen" not in TEXT_MAIN, "")
check("die Ziehung ist die einzige Stelle, die die Startkarte setzt",
      TEXT_MAIN.count("spieloekonomie.startkarte_ziehung(") == 1,
      str(TEXT_MAIN.count("spieloekonomie.startkarte_ziehung(")))
check("ohne Ziehung gilt weiter die belegte Standardkarte (Programmweg)",
      S.startkarte_gewaehlt("", "probe").get("originalkarte_id") == O.START_ID,
      str(S.startkarte_gewaehlt("", "probe").get("originalkarte_id")))
check("der Kandidatenweg bleibt als Vergleichsfunktion erhalten",
      len(O.startkarte_kandidaten("probe")) == int(_cfg.get("anzahl_kandidaten") or 0),
      str(len(O.startkarte_kandidaten("probe"))))

bericht()
