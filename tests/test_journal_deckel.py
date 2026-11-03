# -*- coding: ascii -*-
"""JOURNAL-DECKEL - Stufe S-11 (03.11.2026, Daniels Entscheidung 9).

Daniels Entscheidung, woertlich: "Deckel 500 Zeilen je Ort, aelteste fallen weg (empfohlen)".
Das `produktionsjournal` waechst sonst unbegrenzt - eine Zeile je Ernte- und Verbrauchsspanne, bei
Spieler UND Bots gleich. Gedeckelt wird an EINER Stelle (`spieloekonomie.journal_deckeln`), und zwar
dort, wo die Zeilen entstehen.

Was diese Datei beweist
-----------------------
1. Die Zahl steht in `data/spieloekonomie.json` (`journal_max_zeilen`), nicht im Code; der Hinweis
   nennt die Entscheidung.
2. Ueber dem Deckel fallen die AELTESTEN Zeilen weg, die neuesten bleiben (600 -> 500, Zeile 599
   bleibt, Zeile 100 ist weg).
3. Unter dem Deckel aendert sich nichts; `deckel = 0` schaltet den Deckel ab (kein stiller
   Standardwert).
4. Der KERN haelt den Deckel ein: 520 Stunden-Spannen durch `ort_tick` (derselbe Weg wie beim
   Spieler, die Bots laufen ueber denselben Kern) lassen genau 500 Zeilen stehen.
5. Das Versorgungsfenster rechnet nach dem Deckeln weiter - die neuesten 24 Stunden sind vollstaendig
   vorhanden, `fensterproduktion` liefert dieselben Zahlen wie ohne Kuerzung.
6. Auch der BOT-Weg (Vorgabe `ertrag_weg = karte`) haelt den Deckel ein: dort schreibt
   `main.bot_futter_buchen` die Zeile selbst, ohne den Kern.

Aufruf:  python -X utf8 tests/test_journal_deckel.py
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src

ROOT, SRC = import_src()
import botkern as BK  # noqa: E402
import main as M  # noqa: E402
import spieloekonomie as O  # noqa: E402

TEXT_MAIN = open(os.path.join(SRC, "main.py"), encoding="utf-8").read()
TEXT_Oeko = open(os.path.join(SRC, "spieloekonomie.py"), encoding="utf-8").read()
with open(os.path.join(ROOT, "data", "spieloekonomie.json"), encoding="utf-8") as _f:
    REGELN = json.load(_f)
DECKEL = int(REGELN.get("journal_max_zeilen") or 0)


def neues_dorf(karte: str = "original-036"):
    """Ein Bot mit einem Hauptdorf samt Grundanlagen - der Kern-Form des Ortes."""
    bot = M.BotPlayer("Haug", BK.BOT_FRAKTIONEN["Haug"], 0.3, 0.5)
    dorf = M.BotDorf(name="Haupt", hauptdorf=True, karte=karte,
                     vorraete={"holz": 100.0, "stein": 100.0, "nahrung": 100.0})
    bot.doerfer = [dorf]
    M.bot_doerfer_bebauen(dorf)
    return bot, dorf


# ==========================================================================
abschnitt("1. Der Deckel steht in der Datendatei")
# ==========================================================================
check("1 die Zahl steht in data/spieloekonomie.json", DECKEL == 500, str(DECKEL))
check("1 der Hinweis nennt die Entscheidung Daniels (9)",
      "Entscheidung 9" in str(REGELN.get("journal_max_zeilen_hinweis") or ""),
      str(REGELN.get("journal_max_zeilen_hinweis") or "")[:70])
# Der Deckel-Code OHNE Docstring: die Zahl darf nur in der Datendatei stehen, nicht im Code.
_deckel_code = TEXT_Oeko.split("def journal_deckeln")[1].split("def ort_tick")[0]
_deckel_code = _deckel_code.split('"""')[2] if _deckel_code.count('"""') >= 2 else _deckel_code
check("1 keine Literalzahl im Deckel-Code (nur in der Datendatei)",
      "500" not in _deckel_code, _deckel_code.strip().split("\n")[0][:60])
check("1 der Code liest die Zahl aus den Regeln",
      'REGELN.get("journal_max_zeilen")' in _deckel_code, "spieloekonomie.journal_deckeln")

# ==========================================================================
abschnitt("2. Ueber dem Deckel fallen die AELTESTEN Zeilen weg")
# ==========================================================================
_j = [{"ab": float(i), "bis": float(i + 1), "mengen": {}} for i in range(600)]
O.journal_deckeln(_j)
check("2 600 Zeilen werden auf den Deckel gekuerzt", len(_j) == DECKEL, str(len(_j)))
check("2 die NEUESTE Zeile bleibt", _j[-1]["ab"] == 599.0, str(_j[-1]["ab"]))
check("2 die 100 aeltesten sind weg", _j[0]["ab"] == 100.0, str(_j[0]["ab"]))
check("2 die Reihenfolge bleibt aufsteigend",
      [_z["ab"] for _z in _j] == sorted(_z["ab"] for _z in _j), "ab-Folge")
_kurz = [{"ab": float(i), "bis": float(i + 1), "mengen": {}} for i in range(10)]
_vorher = list(_kurz)
O.journal_deckeln(_kurz)
check("2 unter dem Deckel aendert sich nichts", _kurz == _vorher, str(len(_kurz)))
_check = [{"ab": 1.0}] * 600
O.journal_deckeln(_check, 0)
check("2 deckel = 0 schaltet den Deckel ab (kein stiller Standardwert)", len(_check) == 600,
      str(len(_check)))
O.journal_deckeln([])
check("2 ein leeres Journal stuerzt nicht", O.journal_deckeln([]) == [], "")
check("2 ein falscher Typ wird nicht angefasst", O.journal_deckeln("kein journal") == "kein journal", "")

# ==========================================================================
abschnitt("3. Der KERN haelt den Deckel ein (Spieler wie Bots)")
# ==========================================================================
bot, dorf = neues_dorf()
ort = M.bot_dorf_als_ort(dorf, bot)
_t = 0.0
for _i in range(520):                                    # 520 Stunden-Spannen
    ort = O.ort_tick(ort, _t, _t + 3600.0, {})
    _t += 3600.0
_journal = ort["produktionsjournal"]
check("3 nach 520 Spannen stehen genau 500 Zeilen", len(_journal) == DECKEL, str(len(_journal)))
check("3 die letzte Zeile ist die letzte Spanne", abs(float(_journal[-1]["bis"]) - _t) < 1e-6,
      f"{_journal[-1]['bis']} gegen {_t}")
check("3 die erste Zeile ist NICHT die erste Spanne (die aeltesten sind weg)",
      float(_journal[0]["ab"]) > 0.0, str(_journal[0]["ab"]))

# ==========================================================================
abschnitt("4. Das Versorgungsfenster rechnet nach dem Deckeln weiter")
# ==========================================================================
_fenster = O.fensterproduktion([ort], _t)
check("4 das Fenster liefert nach der Kuerzung noch Produktion",
      bool(_fenster) and sum(float(v) for v in _fenster.values()) > 0,
      str({k: round(v, 2) for k, v in list(_fenster.items())[:4]}))
_stunden = int(REGELN.get("versorgung_stunden") or 24)
_im_fenster = [z for z in _journal if float(z["bis"]) > _t - _stunden * 3600.0]
check("4 das Fenster ist vollstaendig abgedeckt (eine Zeile je Stunde)",
      len(_im_fenster) == _stunden, f"{len(_im_fenster)} von {_stunden}")
# Gegenprobe: dieselben Zeilen OHNE Kuerzung ergeben dieselbe Summe.
_ungekuerzt = [{"ab": float(_i), "bis": float(_i + 1), "mengen": z["mengen"]}
               for _i, z in enumerate(_journal)]
check("4 die Kuerzung selbst aendert keine Zeile (nur die Anzahl)",
      all(set(z) >= {"ab", "bis", "mengen"} for z in _journal) and len(_ungekuerzt) == len(_journal),
      str(sorted(_journal[-1])))

# ==========================================================================
abschnitt("5. Auch der Bot-Weg (Vorgabe 'karte') haelt den Deckel ein")
# ==========================================================================
bot, dorf = neues_dorf()
bot.army = {"Held": 5}                                   # nur mit Armee entstehen Futterzeilen
for _i in range(520):                                    # 520 Spannen a 1 h
    M.bot_futter_buchen(bot, dorf, float(_i) * 3600.0, float(_i + 1) * 3600.0, {"holz": 1.0})
check("5 nach 520 Spannen stehen genau 500 Zeilen im Bot-Dorf",
      len(dorf.produktionsjournal) == DECKEL, str(len(dorf.produktionsjournal)))
check("5 die letzte Zeile traegt den Verbrauch der letzten Spanne",
      "verbrauch" in dorf.produktionsjournal[-1], str(sorted(dorf.produktionsjournal[-1])))

# ==========================================================================
abschnitt("6. Quellwachen")
# ==========================================================================
check("6 der Kern kuerzt im ort_tick (eine Stelle fuer Spieler und Bots)",
      "journal_deckeln(neu[\"produktionsjournal\"])" in TEXT_Oeko, "spieloekonomie.ort_tick")
check("6 der Bot-Weg kuerzt nach dem Futter-Buchen",
      "spieloekonomie.journal_deckeln(dorf.produktionsjournal)" in TEXT_MAIN, "main.bot_futter_buchen")
check("6 es gibt genau ZWEI Schreibstellen fuer das Journal (beide gedeckelt)",
      TEXT_Oeko.count("produktionsjournal\"].append(") + TEXT_MAIN.count("produktionsjournal.append(") == 2,
      str(TEXT_Oeko.count("produktionsjournal\"].append(") + TEXT_MAIN.count("produktionsjournal.append(")))
befund("6 ehrliche Grenze: gedeckelt wird NACH dem Anhaengen, und die Kuerzung betrifft nur das "
       "Journal - die Vorraete und alle anderen Buecher bleiben unberuehrt. Bei einem Deckel, der "
       "kleiner als das Versorgungsfenster waere, fehlten dem Fenster Zeilen; 500 Zeilen decken bei "
       "einem Takt je Stunde rund 20 Spieltage und damit das 24-h-Fenster vielfach.", "")

sys.exit(bericht())
