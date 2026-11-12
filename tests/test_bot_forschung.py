# -*- coding: ascii -*-
"""Bots FORSCHEN - Stufe S-4 (03.11.2026).

Daniels Vorgabe, woertlich: die Bots sollen "mit ihren erwirtschafteten ressourcen auch
forschungsschritte durchlaufen um ihre einheiten und neue gebaeude freizuschalten". Bis heute
blieb `dorf.geforscht` auf 0, und der Kern-Tick bekam ein LEERES dict als Forschungsstand - jede
Forschungsstufe des Bots war damit fuer den Ertrag wirkungslos.

Was diese Datei beweist
-----------------------
1. Die REIHENFOLGE steht in `data/bot_forschung.json` (je Taktik eine Liste mit Zielstufe und
   Begruendung), nicht im Code; die Namen sind woertlich die von `data/research.json`.
2. Jede laufende Liste (`jetzt`) ist mit einer Bibliothek der Stufe 1 in ihrer eigenen Reihenfolge
   erfuellbar - kein Schritt wartet auf eine Bibliothek, die der Bot nie baut.
3. Ohne Bibliothek wird NICHTS gestartet und NICHTS gebucht.
4. Gestartet wird durch dieselbe Funktion wie beim Spieler (`spieloekonomie.forschung_start`):
   Voraussetzungskette geprueft (forschungspfad), Kosten aus dem DORFLAGER gebucht, Auftrag am
   ORT gesetzt. Eine Voraussetzung, die fehlt, wird NICHT uebergangen.
5. Ein Auftrag je Bibliothek: solange einer laeuft, startet kein zweiter.
6. Der Abschluss bucht genau EINMAL (Stufe steigt, Auftrag weg, fertigjournal-Zeile), ein zweiter
   Aufruf aendert nichts.
7. Ein alter Spielstand ohne Auftrag und ohne Wissensstand laedt und forscht ab 0 (kein Vorsprung).
8. Der Bot-Takt forscht wirklich (ueber `bot_doerfer_auffrischen`), und der Kern-Tick rechnet mit
   dem Wissensstand des Bots (vorher: leeres dict).
9. Nach Baukunst 1 baut der Bot auch die Gebaeude aus `nach_baukunst` - vorher nicht.

Aufruf:  python -X utf8 tests/test_bot_forschung.py
"""
from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b
# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.
PRUEF_ART = "quelltext"
PRUEF_STUFE = 1
PRUEF_BETRIFFT = ['botkern', 'einheiten', 'forschung', 'forschungspfad', 'gebaeude_wirkung', 'gelaende', 'main:*', 'spieloekonomie', 'spielschicht']
PRUEF_DATEN = ['bot_bauplan.json', 'bot_forschung.json', 'research.json']
# --- Ende Pruefstand-Kopf -------------------------------------------------------

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src

ROOT, SRC = import_src()
import botkern as BK  # noqa: E402
import forschungspfad  # noqa: E402
import gelaende  # noqa: E402
import main as M  # noqa: E402
import spielschicht  # noqa: E402

TEXT_MAIN = open(os.path.join(SRC, "main.py"), encoding="utf-8").read()
with open(os.path.join(ROOT, "data", "bot_forschung.json"), encoding="utf-8") as _f:
    PLAN = json.load(_f)
with open(os.path.join(ROOT, "data", "research.json"), encoding="utf-8") as _f:
    FORSCHUNGEN = json.load(_f)["forschungen"]
with open(os.path.join(ROOT, "data", "bot_bauplan.json"), encoding="utf-8") as _f:
    BAUPIAN = json.load(_f)
TAKTIKEN = ("Pluenderer", "Waechterin", "Bastionier", "Spaeherin", "Raecher", "Unbekannt")


def neuer_bot(name: str = "Haug", karte: str = "original-036", vorrat=None):
    """Ein Bot mit EINEM Hauptdorf; `vorrat` ueberschreibt das Lager."""
    bot = M.BotPlayer(name, BK.BOT_FRAKTIONEN.get(name, "menschlich"), 0.3, 0.5)
    dorf = M.BotDorf(name="Haupt", hauptdorf=True, karte=karte,
                     vorraete=dict(vorrat if vorrat is not None
                                   else {"holz": 5000.0, "stein": 5000.0, "nahrung": 5000.0}))
    bot.doerfer = [dorf]
    return bot, dorf


def mit_bibliothek(bot_name: str = "Haug", vorrat=None):
    """Ein Bot, dessen Hauptdorf die Grundanlagen, zwei Haeuser und die Bibliothek hat."""
    bot, dorf = neuer_bot(bot_name, vorrat=vorrat)
    M.bot_doerfer_bebauen(dorf)
    for _ in range(3):                                   # haus, haus, bibliothek (S-3-Plan)
        M.bot_dorf_bauen(dorf, bot, 0.0)
    return bot, dorf


def bibliothek_da(dorf) -> bool:
    return any(str(g) == "bibliothek" for g in (dorf.bauten or {}).values())


# ==========================================================================
abschnitt("1. Der Plan steht in der Datendatei, nicht im Code")
# ==========================================================================
check("1 die Datendatei ist eingeschaltet", bool(PLAN.get("aktiv")), str(PLAN.get("aktiv")))
check("1 jede Taktik hat eine Liste", all(isinstance((PLAN.get("plaene") or {}).get(t), dict)
      for t in TAKTIKEN), str(sorted(PLAN.get("plaene") or {})))
check("1 jeder Schritt nennt Forschung, Zielstufe und Begruendung",
      all(set(("forschung", "bis_stufe", "warum")) <= set(e)
          and len(str(e.get("warum") or "")) > 60
          for t in TAKTIKEN
          for e in ((PLAN.get("plaene") or {}).get(t) or {}).get("jetzt") or []),
      "data/bot_forschung.json")
check("1 die Forschungsnamen sind die von data/research.json (nichts erfunden)",
      sorted({str(e["forschung"]) for t in TAKTIKEN
              for zweig in [(PLAN.get("plaene") or {}).get(t) or {}]
              for e in (zweig.get("jetzt") or []) + (zweig.get("nach_bibliothek") or [])}
             - set(FORSCHUNGEN)) == [], str(sorted(FORSCHUNGEN))[:120])
check("1 keine Kosten und keine Dauer in der Datei (beides kommt aus den Spieldaten)",
      "kosten" not in PLAN and "dauer" not in PLAN, str(sorted(PLAN)))
check("1 die Datei begruendet die Reihenfolge", len(str(PLAN.get("warum_baukunst_zuerst") or "")) > 120,
      str(len(str(PLAN.get("warum_baukunst_zuerst") or ""))))

# ==========================================================================
abschnitt("2. Jede laufende Liste ist mit Bibliothek 1 erfuellbar")
# ==========================================================================
for _taktik in TAKTIKEN:
    _wissen = {}
    _offen = []
    for _e in ((PLAN.get("plaene") or {}).get(_taktik) or {}).get("jetzt") or []:
        _name, _bis = str(_e["forschung"]), max(1, int(_e["bis_stufe"]))
        for _stufe in range(_wissen.get(_name, 0) + 1, _bis + 1):
            _ok, _grund = forschungspfad.erfuellt(_name, _wissen, 1)      # Bibliothek Stufe 1
            if not _ok:
                _offen.append(f"{_name} Stufe {_stufe}: {_grund}")
            _wissen[_name] = _stufe
    check(f"2 {_taktik}: kein Schritt wartet auf eine groessere Bibliothek", _offen == [],
          str(_offen))
_bib2 = [str(e["forschung"]) for t in TAKTIKEN
         for e in (((PLAN.get("plaene") or {}).get(t) or {}).get("nach_bibliothek") or [])
         if not any(p.get("art") == "gebaeude" and int(p.get("stufe") or 0) >= 2
                    for p in (FORSCHUNGEN.get(str(e["forschung"])) or {})
                    .get("voraussetzung_struktur") or [])]
check("2 'nach_bibliothek' enthaelt nur Schritte, die wirklich Bibliothek 2+ verlangen",
      _bib2 == [], str(_bib2))

# ==========================================================================
abschnitt("3. Ohne Bibliothek kein Start, nichts gebucht")
# ==========================================================================
bot, dorf = neuer_bot()                                  # Grundanlagen, aber keine Bibliothek
M.bot_doerfer_bebauen(dorf)
check("3 das Dorf hat wirklich keine Bibliothek", not bibliothek_da(dorf), str(sorted(dorf.bauten.values())))
_stand = dict(dorf.vorraete)
check("3 ohne Bibliothek wird nichts gestartet", M.bot_dorf_forschen(dorf, bot, 0.0) == [], "")
check("3 der Auftrag bleibt leer", dorf.forschungsauftrag is None, str(dorf.forschungsauftrag))
check("3 das Lager bleibt unangetastet", dorf.vorraete == _stand, str(dorf.vorraete))

# ==========================================================================
abschnitt("4. Start durch den Kern: Reihenfolge, Preis, Abbuchung aus dem Dorflager")
# ==========================================================================
bot, dorf = mit_bibliothek()
check("4 die Bibliothek steht (Voraussetzung jeder Forschung)", bibliothek_da(dorf),
      str(sorted(dorf.bauten.values())))
_liste = M.bot_dorf_forschungsliste(bot)
check("4 der Haug (Pluenderer) beginnt mit Baukunst", str(_liste[0]["forschung"]) == "Baukunst",
      str([e["forschung"] for e in _liste]))
_vorher = float(dorf.vorraete["holz"])
_start = M.bot_dorf_forschen(dorf, bot, 0.0)
check("4 der erste Takt startet genau den ersten Schritt", _start == ["Baukunst"], str(_start))
_a = dorf.forschungsauftrag or {}
check("4 der Auftrag haengt am ORT und nennt Gebiet, Zielstufe und Dauer",
      _a.get("gebiet") == "Baukunst" and int(_a.get("zielstufe") or 0) == 1
      and float(_a.get("dauer_stunden") or 0.0) == 1.0, str(_a))
check("4 die Kosten sind aus dem Dorflager gebucht (Stufe 1 = 50 Holz, belegte Originalregel)",
      abs((_vorher - float(dorf.vorraete["holz"])) - 50.0) < 0.01,
      f"Holz -{_vorher - float(dorf.vorraete['holz'])}")
check("4 kein Bestand ist negativ", all(float(v) >= 0 for v in dorf.vorraete.values()),
      str(dorf.vorraete))
check("4 solange der Auftrag laeuft, startet kein zweiter",
      M.bot_dorf_forschen(dorf, bot, 10.0) == [], str(dorf.forschungsauftrag))

# ==========================================================================
abschnitt("5. Die Voraussetzungskette wird NICHT uebergangen")
# ==========================================================================
_sperr_plan = {"aktiv": True, "forschungen_je_takt": 1,
               "plaene": {"Pluenderer": {"jetzt": [
                   {"forschung": "Verteidigungsanlagen", "bis_stufe": 1, "warum": "Pruefung"},
                   {"forschung": "Waffentechnik", "bis_stufe": 1, "warum": "Pruefung"},
                   {"forschung": "Baukunst", "bis_stufe": 1, "warum": "Pruefung"}]}}}
bot, dorf = mit_bibliothek()
_gesperrt = M.bot_dorf_forschen(dorf, bot, 0.0, _sperr_plan)
check("5 ein gesperrter Schritt wird uebersprungen, nicht gestartet (Baukunst kommt zuerst)",
      _gesperrt == ["Baukunst"], str(_gesperrt))
check("5 'Verteidigungsanlagen' braucht Baukunst 3 - der Kern lehnt es ab",
      forschungspfad.erfuellt("Verteidigungsanlagen", {}, 1)[0] is False,
      forschungspfad.erfuellt("Verteidigungsanlagen", {}, 1)[1])
check("5 'Waffentechnik' braucht Bibliothek 3 - der Kern lehnt es ab",
      forschungspfad.erfuellt("Waffentechnik", {}, 1)[0] is False,
      forschungspfad.erfuellt("Waffentechnik", {}, 1)[1])
check("5 gestartet wird durch spieloekonomie.forschung_start (dieselbe Funktion wie beim Spieler)",
      "spieloekonomie.forschung_start(ort, ziel, wissen" in TEXT_MAIN, "main.bot_dorf_forschen")
check("5 NICHT ueber spielschicht.forschung_starten (die kennt die Voraussetzungskette nicht)",
      "spielschicht.forschung_starten(" not in TEXT_MAIN, "main.py")

# ==========================================================================
abschnitt("6. Abschluss: genau einmal, dann der naechste Schritt")
# ==========================================================================
bot, dorf = mit_bibliothek()
M.bot_dorf_forschen(dorf, bot, 0.0)                     # Baukunst Stufe 1, 1 h
check("6 vor Ablauf steigt nichts", M.bot_dorf_forschung_abschluss(dorf, bot, 100.0) == [],
      str(bot.forschungsstaende))
check("6 der Auftrag laeuft weiter", isinstance(dorf.forschungsauftrag, dict), str(dorf.forschungsauftrag))
_fertig = M.bot_dorf_forschung_abschluss(dorf, bot, 3600.0)
check("6 nach Ablauf steigt Baukunst auf 1", _fertig == ["Baukunst"], str(_fertig))
check("6 der Wissensstand steht am Bot", int(M.bot_forschungsstaende(bot).get("Baukunst", 0)) == 1,
      str(bot.forschungsstaende))
check("6 der Auftrag ist geloescht", dorf.forschungsauftrag is None, str(dorf.forschungsauftrag))
check("6 die Fertigstellung steht im fertigjournal des Dorfes",
      any(e.get("art") == "forschung" and e.get("name") == "Baukunst"
          for e in (dorf.fertigjournal or [])), str((dorf.fertigjournal or [])[-2:]))
check("6 der Zaehler 'geforscht' waechst (einmal)", int(dorf.geforscht) == 1, str(dorf.geforscht))
check("6 ein zweiter Aufruf bucht NICHTS nach",
      M.bot_dorf_forschung_abschluss(dorf, bot, 4000.0) == []
      and int(M.bot_forschungsstaende(bot).get("Baukunst", 0)) == 1,
      str(bot.forschungsstaende))
_naechster = M.bot_dorf_forschen(dorf, bot, 4000.0)
check("6 der naechste Schritt der Taktik beginnt (Kriegskunst, nicht Baukunst erneut)",
      _naechster == ["Kriegskunst"], str(_naechster))

# ==========================================================================
abschnitt("7. Alter Spielstand: kein Auftrag, kein Wissensstand")
# ==========================================================================
_alt = M.BotDorf(name="Alt", hauptdorf=True)            # alle S-1-Felder auf Vorgabe
check("7 ein altes Dorf hat keinen Auftrag", _alt.forschungsauftrag is None, str(_alt.forschungsauftrag))
_alt_bot = M.BotPlayer("Haug", "menschlich", 0.3, 0.5)
_alt_bot.doerfer = [_alt]
check("7 ein alter Bot hat keinen Wissensstand", M.bot_forschungsstaende(_alt_bot) == {},
      str(getattr(_alt_bot, "forschungsstaende", "fehlt")))
check("7 der Abschluss ohne Auftrag meldet nichts und stuerzt nicht",
      M.bot_dorf_forschung_abschluss(_alt, _alt_bot, 10.0) == [], "")
_roh = json.loads(json.dumps({"name": "Haug", "faction": "menschlich", "aggression": 0.3,
                             "trading": 0.5, "doerfer": [{"name": "Alt", "hauptdorf": True}]}))
_alt2 = M.bot_aus_stand(_roh)                            # Spielstand OHNE die neuen Felder
check("7 ein Spielstand ohne die neuen Felder laedt", isinstance(_alt2.doerfer[0], M.BotDorf),
      str(_alt2.doerfer[0].name))
check("7 ... und forscht ab Stufe 0", M.bot_forschungsstaende(_alt2) == {}, "")
check("7 ... und startet ohne Bibliothek nichts", M.bot_dorf_forschen(_alt2.doerfer[0], _alt2, 5.0) == [],
      "")

# ==========================================================================
abschnitt("8. Der Bot-Takt forscht wirklich, der Kern rechnet mit dem Wissen")
# ==========================================================================
gs = M.GameState()
gs.settlements = [M.Settlement(name="Testdorf", map_id="kontinent", x=3, y=3,
                               id="spieler:kontinent:3:3", vorraete={"holz": 100.0, "stein": 100.0})]
_bots = [M.BotPlayer(n, BK.BOT_FRAKTIONEN[n], 0.2, 0.5) for n in BK.BOT_NAMEN]
for _b in _bots:
    _b.vorraete = {"holz": 9000, "stein": 9000, "nahrung": 9000, "gold": 300, "siedler": 20}
    M.bot_doerfer_sicherstellen(_b)
gs.bots = _bots
_takt_bot = _bots[0]
for _i in range(4):                                      # Grundanlagen, Haeuser, Bibliothek
    gs.bot_doerfer_auffrischen(_takt_bot, 1000.0 + _i)
_laeuft = [d.forschungsauftrag for d in _takt_bot.doerfer if d.forschungsauftrag]
check("8 der Bot-Takt startet eine Forschung, sobald die Bibliothek steht", bool(_laeuft),
      str(_laeuft)[:160])
check("8 es ist der erste Schritt seiner Taktik",
      bool(_laeuft) and str(_laeuft[0].get("gebiet")) == "Baukunst", str(_laeuft)[:160])
_zwei = [d for d in _takt_bot.doerfer if d.forschungsauftrag]
check("8 hoechstens EIN Auftrag je Dorf (die Bibliothek ist die Sperre)",
      len(_zwei) == len({id(d) for d in _zwei}), str(len(_zwei)))
check("8 der Kern-Tick bekommt den Wissensstand des Bots (kein leeres dict mehr)",
      "bot_forschungsstaende(bot))" in TEXT_MAIN and "ort_tick(ort, float(ab), float(bis), {})" not in TEXT_MAIN,
      "main.bot_dorf_tick")

# ==========================================================================
abschnitt("9. Nach der Forschung baut der Bot auch 'nach_baukunst'")
# ==========================================================================
bot, dorf = mit_bibliothek()
for _ in range(3):
    M.bot_dorf_bauen(dorf, bot, 0.0)                     # Obergrenzen Haus/Bibliothek erreichen
check("9 ohne Baukunst bleibt der Wall-Lager-Block gesperrt", M.bot_dorf_bauen(dorf, bot, 0.0) == [],
      str(sorted(dorf.bauten.values())))
bot.forschungsstaende = {"Baukunst": 1}
_mit = M.bot_dorf_bauen(dorf, bot, 0.0)
check("9 mit Baukunst 1 baut der Pluenderer sein Lager", _mit == ["lager"], str(_mit))
check("9 danach Schmiede und Akademie (Reihenfolge der Taktik)",
      M.bot_dorf_bauen(dorf, bot, 0.0) == ["schmiede"]
      and M.bot_dorf_bauen(dorf, bot, 0.0) == ["kriegerakademie"],
      str(sorted(dorf.bauten.values())))
check("9 danach ist Ruhe - jede Grenze steht (kein Nachlegen bei jedem Takt)",
      M.bot_dorf_bauen(dorf, bot, 0.0) == [], str(sorted(dorf.bauten.values())))
check("9 die Grenzen der Datendatei nennen die Gebaeude hinter Baukunst",
      all(g in (BAUPIAN.get("hoechstens") or {}) for g in
          ("lager", "schmiede", "kriegerakademie", "diebesgilde", "bogenbauer", "verteidigungswall")),
      str(BAUPIAN.get("hoechstens")))
check("9 der Bot baut nur, was die gemeinsame Regel erlaubt (eine Stelle fuer Spieler und Bot)",
      "gebaeude_forschung_erlaubt(g, staende)[0]" in TEXT_MAIN
      and "gebaeude_forschung_erlaubt(kennung, forschungsstaende)" in TEXT_MAIN,
      "main.bot_dorf_bauen / main.bauen_auf_karte")

# ==========================================================================
abschnitt("10. Quellwachen")
# ==========================================================================
check("10 der Takt forscht vor dem Bauen", "bot_dorf_forschen(dorf, bot, jetzt, plan_forschung)" in TEXT_MAIN,
      "main.bot_doerfer_auffrischen")
check("10 der Takt verbucht faellige Forschung genau davor",
      "bot_dorf_forschung_abschluss(dorf, bot, jetzt)" in TEXT_MAIN, "main.bot_doerfer_auffrischen")
check("10 die Bibliothek wird ueber den Kern gemessen (keine zweite Regel)",
      "gebaeude_wirkung.bibliothek_stufe([ort])" in TEXT_MAIN, "main.bot_dorf_forschen")
_befund = ("ehrliche Grenze (S-4): die Forschungen wirken ueber den Kern-Weg des Takts und ueber "
           "den Wissensstand, den bot_dorf_tick hineingibt; auf dem Vorgabe-Weg 'ertrag_weg = karte' "
           "rechnet der Bot weiter mit dem Kartenprofil, dort aendert Forschung den Ertrag NICHT. "
           "Ausserdem bleibt die Bibliothek des Bots auf Stufe 1 (Ausbauen fehlt), deshalb sind "
           "Bibliothek-2/3-Forschungen gesperrt und stehen unter 'nach_bibliothek'.")
befund("10 " + _befund, "")

sys.exit(bericht())
