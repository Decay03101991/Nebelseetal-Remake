# -*- coding: ascii -*-
"""Bots BAUEN - Stufe S-3 (03.11.2026).

Daniels Vorgabe, woertlich: die Bots sollen "je nachdem welche taktik sie verfolgen auch
dementsprechend den gebaeudebau auf ihren karten vorran treiben". Bis heute blieb `dorf.gebaut`
immer 0 - ein Bot-Dorf hatte keine Bauplaetze, keine Preise, keinen Bauweg.

Was diese Datei beweist
-----------------------
1. Der Plan steht in `data/bot_bauplan.json` (je Taktik eine Reihenfolge), nicht im Code; die
   Preise stehen NICHT dort, sondern in `data/baupreise.json`.
2. `jetzt` enthaelt nur Gebaeude, die OHNE Forschung baubar sind (Voraussetzung "keine" in
   `data/buildings.json`); alles andere steht unter `nach_baukunst` und wird nicht gebaut -
   die Forschungsregel wird NICHT umgangen (S-4 fehlt noch).
3. Gebaut wird durch DIESELBE Funktion wie beim Spieler (`spielschicht.bauen`): freies Feld,
   Gelaende-Eignung, Obergrenze je Siedlung, Preis, Abbuchung aus dem Dorflager.
4. Die Obergrenzen der Datendatei halten (2 Haeuser, 1 Bibliothek), danach baut der Bot nichts
   mehr - auch nicht bei vollem Lager.
5. Zu wenig Rohstoffe: es wird NICHTS gebaut und NICHTS abgebucht (kein negativer Bestand).
6. Ohne Karte gibt es keinen Bauplatz - die Rueckgabe ist leer statt einer Ausnahme.
7. Der Stil kommt aus `bottaktik` (Haug = Pluenderer, Brynhild = Waechterin, ...), ein fremder
   Name faellt auf den Plan "Unbekannt" zurueck.
8. Der Bot-Takt baut wirklich (ueber `bot_doerfer_auffrischen`), der Zaehler `dorf.gebaut` waechst.

Aufruf:  python -X utf8 tests/test_bot_bauen.py
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src

ROOT, SRC = import_src()
import botkern as BK  # noqa: E402
import gelaende  # noqa: E402
import main as M  # noqa: E402
import spielschicht  # noqa: E402

TEXT_MAIN = open(os.path.join(SRC, "main.py"), encoding="utf-8").read()
with open(os.path.join(ROOT, "data", "bot_bauplan.json"), encoding="utf-8") as _f:
    PLAN = json.load(_f)
with open(os.path.join(ROOT, "data", "buildings.json"), encoding="utf-8") as _f:
    GEBAEUDE = {str(g.get("id")): g for g in (json.load(_f).get("gebaeude") or [])}


def neuer_bot(name: str = "Haug", karte: str = "original-036", vorrat=None):
    """Ein Bot mit EINEM Hauptdorf; `vorrat` ueberschreibt das Lager."""
    bot = M.BotPlayer(name, BK.BOT_FRAKTIONEN.get(name, "menschlich"), 0.3, 0.5)
    dorf = M.BotDorf(name="Haupt", hauptdorf=True, karte=karte,
                     vorraete=dict(vorrat if vorrat is not None
                                   else {"holz": 500.0, "stein": 500.0, "nahrung": 100.0}))
    bot.doerfer = [dorf]
    return bot, dorf


# ==========================================================================
abschnitt("1. Der Plan steht in der Datendatei, nicht im Code")
# ==========================================================================
check("1 die Datendatei ist eingeschaltet", bool(PLAN.get("aktiv")), str(PLAN.get("aktiv")))
check("1 jede Taktik hat einen Plan", all(name in (PLAN.get("bauplaene") or {})
      for name in ("Pluenderer", "Waechterin", "Bastionier", "Spaeherin", "Raecher", "Unbekannt")),
      str(sorted((PLAN.get("bauplaene") or {}))))
check("1 es gibt Obergrenzen je Gebaeude", isinstance(PLAN.get("hoechstens"), dict)
      and bool(PLAN.get("hoechstens")), str(PLAN.get("hoechstens")))
check("1 die Datei nennt den Grund fuer die Reihenfolge", len(str(PLAN.get("warum_haus_zuerst") or "")) > 80,
      str(len(str(PLAN.get("warum_haus_zuerst") or ""))))
check("1 die Preise stehen NICHT in der Datei", "baukosten" not in PLAN and "preise" not in PLAN,
      str(sorted(PLAN)))

# ==========================================================================
abschnitt("2. Nur Gebaeude ohne Forschungsvoraussetzung werden gebaut")
# ==========================================================================
_jetzt = sorted({str(g) for zweig in (PLAN.get("bauplaene") or {}).values()
                 for g in (zweig.get("jetzt") or [])})
check("2 der Plan nennt ueberhaupt Gebaeude", bool(_jetzt), str(_jetzt))
_mit_forschung = [g for g in _jetzt
                  if "Baukunst" in str((GEBAEUDE.get(g) or {}).get("voraussetzung") or "")]
check("2 KEIN Gebaeude in 'jetzt' verlangt Baukunst (sonst waere die Forschungsregel umgangen)",
      _mit_forschung == [], str(_mit_forschung))
check("2 die Voraussetzung ist je Gebaeude belegt ('keine ...' in data/buildings.json)",
      all(str((GEBAEUDE.get(g) or {}).get("voraussetzung") or "").startswith("keine") for g in _jetzt),
      str({g: (GEBAEUDE.get(g) or {}).get("voraussetzung") for g in _jetzt}))
_nachher = sorted({str(g) for zweig in (PLAN.get("bauplaene") or {}).values()
                   for g in (zweig.get("nach_baukunst") or [])})
_gesperrt = [g for g in _nachher
             if "Baukunst" not in str((GEBAEUDE.get(g) or {}).get("voraussetzung") or "")]
check("2 die gesperrten Gebaeude stehen wirklich hinter der Forschung",
      len(_gesperrt) <= 1, str(_gesperrt))
if _gesperrt:
    befund("2 'lager' traegt in data/buildings.json die Voraussetzung 'keine belegt', die "
           "belegte Regel (regeln.ohne_forschung_baubar) nennt das Lager aber NICHT unter den "
           "ohne Forschung baubaren Gebaeuden. Der Plan laesst es deshalb vorsichtshalber hinter "
           "Baukunst (S-4) - lieber spaeter bauen als eine belegte Regel umgehen.", str(_gesperrt))

# ==========================================================================
abschnitt("3. Bauen durch den Kern: Feld, Gelaende, Preis, Abbuchung")
# ==========================================================================
bot, dorf = neuer_bot()
M.bot_doerfer_bebauen(dorf)                                  # 12 Grundanlagen, wie im Takt
_vorher_holz = float(dorf.vorraete["holz"])
_vorher_stein = float(dorf.vorraete["stein"])
_preis = {str(k): float(v) for k, v in spielschicht._baukosten("haus", 1).items()}
gebaut = M.bot_dorf_bauen(dorf, bot, 1000.0)
check("3 der erste Takt baut ein Haus", gebaut == ["haus"], str(gebaut))
check("3 das Haus kostet genau den belegten Preis (Holz und Stein aus dem Dorflager)",
      abs((_vorher_holz - float(dorf.vorraete["holz"])) - _preis.get("holz", 0.0)) < 0.01
      and abs((_vorher_stein - float(dorf.vorraete["stein"])) - _preis.get("stein", 0.0)) < 0.01,
      f"Holz -{_vorher_holz - float(dorf.vorraete['holz'])}, Preis {_preis}")
_haus_feld = [f for f, g in dorf.bauten.items() if str(g) == "haus"]
check("3 das Haus steht auf einem Feld der Karte", len(_haus_feld) == 1, str(_haus_feld))
_raster = list((dorf.karte_daten or {}).get("raster") or [])
check("3 das Feld ist fuer ein Haus erlaubt (gelaende.bau_moeglich)",
      bool(_haus_feld) and gelaende.bau_moeglich("haus", _raster[int(_haus_feld[0])])[0],
      str(_haus_feld))
check("3 kein Feld ist doppelt belegt", len(set(dorf.bauten)) == len(dorf.bauten), str(len(dorf.bauten)))

# ==========================================================================
abschnitt("4. Obergrenzen der Datendatei halten")
# ==========================================================================
_zweites = M.bot_dorf_bauen(dorf, bot, 1000.0)
_drittes = M.bot_dorf_bauen(dorf, bot, 1000.0)
_viertes = M.bot_dorf_bauen(dorf, bot, 1000.0)
check("4 das zweite Haus entsteht", _zweites == ["haus"], str(_zweites))
check("4 danach die Bibliothek (naechster Punkt der Reihenfolge)", _drittes == ["bibliothek"], str(_drittes))
check("4 dann ist Schluss - beide Obergrenzen erreicht", _viertes == [], str(_viertes))
check("4 es stehen genau zwei Haeuser und eine Bibliothek",
      sum(1 for g in dorf.bauten.values() if g == "haus") == 2
      and sum(1 for g in dorf.bauten.values() if g == "bibliothek") == 1,
      str(sorted(dorf.bauten.values())))

# ==========================================================================
abschnitt("5. Zu wenig Rohstoffe: nichts gebaut, nichts abgebucht")
# ==========================================================================
arm, armdorf = neuer_bot(vorrat={"holz": 3.0, "stein": 2.0})
M.bot_doerfer_bebauen(armdorf)
_stand = dict(armdorf.vorraete)
_leer = M.bot_dorf_bauen(armdorf, arm, 1000.0)
check("5 ohne genug Holz/Stein wird nichts gebaut", _leer == [], str(_leer))
check("5 das Lager bleibt unangetastet", armdorf.vorraete == _stand, str(armdorf.vorraete))
check("5 kein Bestand ist negativ", all(float(v) >= 0 for v in armdorf.vorraete.values()),
      str(armdorf.vorraete))

# ==========================================================================
abschnitt("6. Ohne Karte kein Bauplatz")
# ==========================================================================
ohne, ohnedorf = neuer_bot(karte="")
check("6 ein Dorf ohne Karte baut nichts (keine Ausnahme)", M.bot_dorf_bauen(ohnedorf, ohne) == [], "")
_mit_plan, _mit_dorf = neuer_bot()
M.bot_doerfer_bebauen(_mit_dorf)
check("6 der Schalter der Datendatei gilt: aus heisst aus",
      M.bot_dorf_bauen(_mit_dorf, _mit_plan, 1000.0, {"aktiv": False}) == [], "")

# ==========================================================================
abschnitt("7. Der Stil kommt aus bottaktik, ein fremder Name faellt zurueck")
# ==========================================================================
_stile = {name: M.bot_taktik_name(M.BotPlayer(name, "menschlich", 0.3, 0.5)) for name in BK.BOT_NAMEN}
check("7 jeder echte Bot traegt einen Stil aus bottaktik",
      len(set(_stile.values())) == len(_stile) and all(v for v in _stile.values()), str(_stile))
check("7 Haug ist Pluenderer, Brynhild Waechterin, Grom Bastionier",
      _stile.get("Haug") == "Pluenderer" and _stile.get("Brynhild") == "Waechterin"
      and _stile.get("Grom") == "Bastionier", str(_stile))
check("7 ein unbekannter Name faellt auf 'Unbekannt'",
      M.bot_taktik_name(M.BotPlayer("Niemand", "menschlich", 0.3, 0.5)) == "Unbekannt", "")
_unbekannt, unbekanntdorf = neuer_bot(name="Niemand")
M.bot_doerfer_bebauen(unbekanntdorf)
check("7 der Rueckfallplan baut ein Haus (kein Stillstand)",
      M.bot_dorf_bauen(unbekanntdorf, _unbekannt) == ["haus"], str(unbekanntdorf.bauten.values()))

# ==========================================================================
abschnitt("8. Der Bot-Takt baut wirklich (ueber bot_doerfer_auffrischen)")
# ==========================================================================
gs = M.GameState()
gs.settlements = [M.Settlement(name="Testdorf", map_id="kontinent", x=3, y=3,
                               id="spieler:kontinent:3:3", vorraete={"holz": 100.0, "stein": 100.0})]
bots = [M.BotPlayer(n, BK.BOT_FRAKTIONEN[n], 0.2, 0.5) for n in BK.BOT_NAMEN]
for b in bots:
    b.vorraete = {"holz": 900, "stein": 900, "nahrung": 900, "gold": 300, "siedler": 20}
    M.bot_doerfer_sicherstellen(b)
gs.bots = bots
gs.bot_doerfer_auffrischen(bots[0], 1000.0)
_gebaut_jetzt = sum(int(getattr(d, "gebaut", 0) or 0) for d in bots[0].doerfer)
check("8 der Takt baut im Dorf (Zaehler dorf.gebaut waechst)", _gebaut_jetzt >= 1, str(_gebaut_jetzt))
check("8 das Gebaeude steht wirklich im Dorf",
      any(str(g) in ("haus", "bibliothek") for d in bots[0].doerfer for g in d.bauten.values()),
      str([sorted(set(d.bauten.values())) for d in bots[0].doerfer]))
check("8 die Grundanlagen stehen weiterhin (der Bauplan ueberschreibt nichts)",
      all(len(d.bauten) >= 12 for d in bots[0].doerfer), str([len(d.bauten) for d in bots[0].doerfer]))

# ==========================================================================
abschnitt("9. Quellwache")
# ==========================================================================
check("9 der Takt ruft den Bauweg", "bot_dorf_bauen(dorf, bot, jetzt, plan)" in TEXT_MAIN,
      "main.bot_doerfer_auffrischen")
check("9 gebaut wird durch spielschicht.bauen (keine zweite Preisliste)",
      "spielschicht.bauen(zustand, 0, ziel[0], ziel[1])" in TEXT_MAIN, "main.bot_dorf_bauen")
befund("9 ehrliche Grenze (S-4): 'nach_baukunst' wird noch NICHT gebaut - die Bots forschen nicht, "
       "also duerfen sie Wall, Lager, Schmiede, Akademie und Diebesgilde nach der belegten Regel "
       "noch nicht setzen. Bis dahin unterscheiden sich die fuenf Stile beim Bauen nicht.", "")

sys.exit(bericht())
