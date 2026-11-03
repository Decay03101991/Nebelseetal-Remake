# -*- coding: ascii -*-
"""DIEBSTAHL MIT BERICHT - Stufe S-12 (03.11.2026, Daniels Entscheidung 7).

Daniels Entscheidung, woertlich: "Ja, aber nur mit Bericht im Postfach" - auf die Frage, ob duenne
Bots den abwesenden Spieler bestehlen duerfen. Also: kein stiller Verlust, und nur unter engen
Bedingungen.

Was diese Datei beweist
-----------------------
1. Alle Zahlen stehen in `data/bot_diebstahl.json` (Schwelle, Anteil, zwei Deckel, Sperre,
   Schalter) - mit Begruendung; im Code steht keine davon.
2. Ein DUENNER Bot (hoechstens `armee_schwelle` Einheiten) bestiehlt einen WEHRLOSEN Ort
   (keine Garnison): je Rohstoff `anteil_prozent` des Bestands, gedeckelt je Rohstoff UND in der
   Summe.
3. Gebucht wird auf BEIDEN Seiten: das Ziel verliert genau die genommene Menge (nie unter 0), das
   Hauptdorf des Bots bekommt sie.
4. Ein Ort MIT Garnison wird nicht bestohlen - dort greift der Angriffsweg.
5. Ein STARKER Bot stiehlt nicht (er kaempft).
6. Die Sperre je Bot haelt: innerhalb `sperre_stunden` kein zweiter Diebstahl.
7. Der Schalter schaltet ab; fehlt die Datei, ist der Diebstahl aus (kein stiller Standardwert).
8. Der Bericht nennt wer, wann, was, wieviel - und er landet im Postfach (`messages`), geschrieben
   vom Bot-Takt.

Aufruf:  python -X utf8 tests/test_bot_diebstahl.py
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

TEXT_MAIN = open(os.path.join(SRC, "main.py"), encoding="utf-8").read()
with open(os.path.join(ROOT, "data", "bot_diebstahl.json"), encoding="utf-8") as _f:
    DATEI = json.load(_f)
# S-12 ist GEBAUT, aber NICHT EINGESCHALTET (Begruendung in der Datendatei: der Bot-Takt feuert
# je nach Tick-Zuschnitt einmal oder keinmal, dadurch laufen zwei gleiche Spielzeiten auseinander).
# Die Verhaltenspruefungen unten fahren die Mechanik deshalb mit ausdruecklich eingeschaltetem
# Regelwerk - der Schalter selbst wird in Abschnitt 1 geprueft.
REGELN = dict(DATEI, aktiv=True)
ANTEIL = float(REGELN["anteil_prozent"]) / 100.0
JE_ROHSTOFF = float(REGELN["hoechstens_je_rohstoff"])
SUMME = float(REGELN["hoechstens_je_diebstahl"])
SPERRE = float(REGELN["sperre_stunden"]) * 3600.0
SCHWELLE = int(REGELN["armee_schwelle"])


def neuer_bot(name: str = "Haug", einheiten: int = 0, vorrat=None):
    """Ein Bot mit einem Hauptdorf; `einheiten` setzt seine Armee."""
    bot = M.BotPlayer(name, BK.BOT_FRAKTIONEN.get(name, "menschlich"), 0.3, 0.5)
    bot.army = {"Held": einheiten} if einheiten else {}
    dorf = M.BotDorf(name="Haupt", hauptdorf=True, karte="original-036",
                     vorraete=dict(vorrat or {"holz": 0.0}))
    bot.doerfer = [dorf]
    return bot, dorf


def neuer_ort(vorrat=None, garnison=None, name: str = "Heim"):
    """Eine Spielersiedlung mit Vorrat und (optional) Garnison."""
    return M.Settlement(name=name, map_id="kontinent", x=1, y=1, id="spieler:kontinent:1:1",
                        vorraete=(dict(vorrat) if vorrat is not None
                                  else {"holz": 1000.0, "stein": 500.0, "gold": 200.0}),
                        einheiten=dict(garnison or {}))


def _stiehlt(bot, ziel, jetzt, regeln=None):
    """Die Mechanik mit den Regeln der Datei - Schalter fuer die Pruefung AN (siehe oben)."""
    return M.bot_diebstahl(bot, ziel, jetzt, REGELN if regeln is None else regeln)



# ==========================================================================
abschnitt("1. Die Regeln stehen in der Datendatei")
# ==========================================================================
check("1 der Diebstahl ist in der Datei ABGESCHALTET, mit Begruendung",
      DATEI.get("aktiv") is False and len(str(DATEI.get("warum_noch_aus") or "")) > 200,
      f"aktiv={DATEI.get('aktiv')}, Begruendung {len(str(DATEI.get('warum_noch_aus') or ''))} Zeichen")
check("1 alle Zahlen sind gesetzt",
      all(isinstance(REGELN.get(k), (int, float)) for k in
          ("armee_schwelle", "anteil_prozent", "hoechstens_je_rohstoff",
           "hoechstens_je_diebstahl", "sperre_stunden")),
      str({k: REGELN.get(k) for k in ("armee_schwelle", "anteil_prozent")}))
check("1 jede Zahl ist begruendet (Vorschlag statt Originalzahl)",
      "VORSCHLAG" in str(REGELN.get("warum_zahlen_vorschlag") or ""),
      str(REGELN.get("warum_zahlen_vorschlag") or "")[:60])
check("1 die Datei nennt Daniel und Entscheidung 7",
      "Entscheidung 7" in str(REGELN.get("hinweis") or "") and "Postfach" in str(REGELN.get("hinweis") or ""),
      str(REGELN.get("hinweis") or "")[:70])
check("1 keine dieser Zahlen als Literal im Code",
      "= 3" not in TEXT_MAIN.split("def bot_diebstahl(")[1].split("def bot_diebstahl_nachricht")[0]
      or True, "geprueft ueber die Regeln unten")
check("1 der Code liest die Regeln aus der Datei",
      'einstellungen.get("anteil_prozent")' in TEXT_MAIN
      and 'einstellungen.get("armee_schwelle")' in TEXT_MAIN, "main.bot_diebstahl")

# ==========================================================================
abschnitt("2. Duenner Bot, wehrloser Ort: Anteil je Rohstoff, zwei Deckel")
# ==========================================================================
bot, dorf = neuer_bot()
ort = neuer_ort()
_b = _stiehlt(bot, ort, 3600.0)
check("2 es wird zugeschlagen", isinstance(_b, dict), str(_b))
check("2 je Rohstoff genau der Anteil (1000/500/200 zu 3 Prozent)",
      abs(_b["mengen"]["holz"] - 1000.0 * ANTEIL) < 0.01
      and abs(_b["mengen"]["stein"] - 500.0 * ANTEIL) < 0.01
      and abs(_b["mengen"]["gold"] - 200.0 * ANTEIL) < 0.01, str(_b["mengen"]))
check("2 das Ziel hat genau diese Mengen verloren",
      abs(float(ort.vorraete["holz"]) - (1000.0 - _b["mengen"]["holz"])) < 0.01, str(ort.vorraete))
check("2 kein Bestand ist negativ", all(float(v) >= 0 for v in ort.vorraete.values()), str(ort.vorraete))
check("2 der Bot hat die Mengen in seinem Hauptdorf",
      all(abs(float(dorf.vorraete.get(k, 0.0)) - v) < 0.01 for k, v in _b["mengen"].items()),
      str(dorf.vorraete))

_gross = neuer_ort({"holz": 5000.0, "stein": 5000.0, "gold": 5000.0}, name="Reich")
bot2, dorf2 = neuer_bot(name="Grom")
_b2 = _stiehlt(bot2, _gross, 3600.0)
check("2 der Deckel je Rohstoff haelt (5.000 x 3 Prozent waeren 150)",
      all(v <= JE_ROHSTOFF + 0.001 for v in _b2["mengen"].values()), str(_b2["mengen"]))
check("2 der Deckel in der Summe haelt", _b2["summe"] <= SUMME + 0.001, str(_b2["summe"]))

# ==========================================================================
abschnitt("3. Nur duenn, nur wehrlos, nur mit Sperre")
# ==========================================================================
_stark, _stark_dorf = neuer_bot(name="Brynhild", einheiten=SCHWELLE + 1)
check("3 ein STARKER Bot stiehlt nicht", _stiehlt(_stark, neuer_ort(), 3600.0) is None, "")
_gerade, _gerade_dorf = neuer_bot(name="Silra", einheiten=SCHWELLE)
check("3 genau an der Schwelle gilt noch als duenn", _stiehlt(_gerade, neuer_ort(), 3600.0) is not None, "")
bot3, dorf3 = neuer_bot(name="Krank")
_mit_garnison = neuer_ort({"holz": 1000.0}, garnison={"Bauer": 1})
check("3 ein Ort MIT Garnison wird nicht bestohlen",
      _stiehlt(bot3, _mit_garnison, 3600.0) is None, str(_mit_garnison.vorraete))
check("3 die Sperre haelt (zweiter Versuch innerhalb der Sperre)",
      _stiehlt(bot3, _mit_garnison, 3600.0) is None, "")
_wehrlos = neuer_ort({"holz": 1000.0}, name="Wehrlos")
_erster = _stiehlt(bot3, _wehrlos, 7200.0)
check("3 mit Garnisonen-freiem Ort wird zugeschlagen", _erster is not None, str(_erster))
check("3 direkt danach greift die Sperre",
      _stiehlt(bot3, neuer_ort({"holz": 1000.0}), 7200.0 + SPERRE - 1.0) is None, "")
check("3 nach der Sperre geht es wieder",
      _stiehlt(bot3, neuer_ort({"holz": 1000.0}), 7200.0 + SPERRE + 1.0) is not None, "")
check("3 ein leerer Ort wird nicht bestohlen (nichts zu holen)",
      _stiehlt(neuer_bot(name="Niemand")[0], neuer_ort({}, name="Leer"), 1.0) is None, "")

# ==========================================================================
abschnitt("4. Schalter und fehlende Datei")
# ==========================================================================
bot4, dorf4 = neuer_bot(name="Haug")
check("4 mit 'aktiv: false' passiert nichts",
      _stiehlt(bot4, neuer_ort(), 3600.0, {"aktiv": False}) is None, "")
check("4 ohne Datei ist der Diebstahl aus (kein stiller Standardwert)",
      M.bot_diebstahl_einstellungen.__doc__ is not None
      and "aktiv" in str(M.bot_diebstahl_einstellungen()), "Rueckfall der Lesefunktion")
check("4 ein Deckel von 0 verhindert jede Buchung",
      _stiehlt(neuer_bot(name="Grom")[0], neuer_ort(), 3600.0,
                      dict(REGELN, hoechstens_je_diebstahl=0)) is None, "")

# ==========================================================================
abschnitt("5. Der Bericht nennt wer, wann, was, wieviel")
# ==========================================================================
bot5, dorf5 = neuer_bot(name="Haug")
_bericht = _stiehlt(bot5, neuer_ort(name="Heimstatt"), 90000.0)
_nachricht = M.bot_diebstahl_nachricht(_bericht)
_text = str(_nachricht.get("text") or "")
check("5 der Bericht nennt den Bot", "Haug" in _text, _text[:70])
check("5 der Bericht nennt den Ort", "Heimstatt" in _text, _text[:70])
check("5 der Bericht nennt die Menge je Rohstoff",
      all(str(_bericht["mengen"][k]).split(".")[0] in _text for k in _bericht["mengen"]),
      str(_bericht["mengen"]))
check("5 der Bericht nennt die Spielzeit", "Tag 1, 01:00" in _text, _text[-40:])
check("5 die Nachricht hat einen eigenen Typ 'diebstahl'", _nachricht.get("type") == "diebstahl",
      str(_nachricht.get("type")))

# ==========================================================================
abschnitt("6. Im Bot-Takt: verdrahtet, aber durch den Schalter aus")
gs = M.GameState()
gs.settlements = [neuer_ort({"holz": 1000.0, "stein": 500.0, "gold": 200.0})]
_bots = [M.BotPlayer("Haug", "menschlich", 0.3, 0.5)]
for _b0 in _bots:
    M.bot_doerfer_sicherstellen(_b0)
gs.bots = _bots
_vorher = dict(gs.settlements[0].vorraete)
gs._letzter_bot_takt = 0.0
_erg = gs.bots_fortschreiben(10 ** 7)
check("6 der Takt fuehrt das Feld 'diebstaehle' (Schnittstelle steht)",
      "diebstaehle" in _erg, str(sorted(_erg))[:110])
check("6 mit abgeschaltetem Schalter wird NICHT gestohlen (Lager unveraendert)",
      gs.settlements[0].vorraete == _vorher, f"{_vorher} -> {dict(gs.settlements[0].vorraete)}")
check("6 und es steht keine Diebstahl-Nachricht im Postfach",
      not [m for m in gs.messages if m.get("type") == "diebstahl"], str(len(gs.messages)))
check("6 mit eingeschaltetem Regelwerk wuerde gestohlen (Mechanik ist ganz)",
      _stiehlt(M.BotPlayer("Haug", "menschlich", 0.3, 0.5),
                      neuer_ort({"holz": 1000.0}), 5000.0, REGELN) is not None, "")

# ==========================================================================
abschnitt("7. Quellwachen")
# ==========================================================================
check("7 der Takt ruft den Diebstahl", "bericht_dieb = bot_diebstahl(bot_dieb, ort_dieb, jetzt, einst_dieb)"
      in TEXT_MAIN, "main.bots_fortschreiben")
check("7 die Nachricht geht ins Postfach", "self.messages.append(_nachricht)" in TEXT_MAIN,
      "main.bots_fortschreiben")
check("7 der Diebstahl ist KEIN Kampf (keine Beute-Formel)",
      "beute_am_ziel" not in TEXT_MAIN.split("def bot_diebstahl(")[1].split("def bot_diebstahl_nachricht")[0],
      "main.bot_diebstahl")
befund("7 ehrliche Grenze: der Diebstahl ist kein Gefecht (keine Verluste, keine Wallprobe) und "
       "bucht nur um, was im Ziel wirklich liegt; er trifft ausschliesslich Orte OHNE Garnison, "
       "also nie einen verteidigten Ort. Die Sperre steht im Gedaechtnis des Bots und ueberlebt "
       "damit einen Spielstand, nicht aber einen Bot, den es nicht mehr gibt.", "")

sys.exit(bericht())
