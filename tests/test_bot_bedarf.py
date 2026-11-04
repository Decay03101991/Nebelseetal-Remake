# -*- coding: ascii -*-
"""BEDARF JE ROHSTOFF - Stufe S-10 (03.11.2026, Daniels Entscheidung 4).

Daniels Entscheidung, woertlich: "\\"mittel\\" - ich baue dafuer zuerst einen Bedarf je Rohstoff".
Bis heute kannte das Spiel genau EINEN laufenden Verbrauch (Nahrung der Garnison, 8 je Einheit und
Spieltag). Ohne Bedarf konnte die Bot-Kartenwahl nicht auf "mittel": der Zweig in
`botkern.oekonomie_kartenwahl` nimmt die am schlechtesten gedeckte Rohstoffachse.

Was diese Datei beweist
-----------------------
1. Die Rechenregeln stehen in `data/bot_bedarf.json` (Fenster, was zaehlt, was NICHT zaehlt),
   nicht im Code; ohne Datei wird nur der BELEGTE Nahrungsbedarf gerechnet.
2. Der Bedarf wird je STUNDE gefuehrt - dieselbe Einheit wie die Ertraege der Karten, damit
   "Deckung = Rate / Bedarf" eine Zahl ohne Einheit ist.
3. Nahrung: 8 je Einheit und Spieltag / 24 (belegte Zahl, dieselbe Funktion wie im Kern).
4. Offene Ausbildungsauftraege erhoehen den Bedarf ihres Rohstoffs, FERTIGE (gebucht) nicht.
5. Offene Werkstattauftraege erhoehen den Bedarf nach ihrem Rezept (data/warenrezepte.json).
6. Nur der NAECHSTE Forschungsschritt zaehlt (ein laufender Auftrag ist bezahlt); ist die
   Zielstufe erreicht, rueckt der naechste Schritt nach.
7. `kartenwahl_stufe` steht auf "mittel" (Entscheidung 4 ist damit eingeloest), und die Kartenwahl
   bekommt den gerechneten Bedarf - ohne Bedarf faellt sie weiter auf die Gold-Regel zurueck,
   damit kein Dorf ohne Karte bleibt.

Aufruf:  python -X utf8 tests/test_bot_bedarf.py
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src

ROOT, SRC = import_src()
import botkern as BK  # noqa: E402
import einheiten  # noqa: E402
import main as M  # noqa: E402

TEXT_MAIN = open(os.path.join(SRC, "main.py"), encoding="utf-8").read()
with open(os.path.join(ROOT, "data", "bot_bedarf.json"), encoding="utf-8") as _f:
    REGELN = json.load(_f)
with open(os.path.join(ROOT, "data", "bot_wirtschaft.json"), encoding="utf-8") as _f:
    WIRTSCHAFT = json.load(_f)

# Einheiten- und Warennamen mit Umlaut kommen aus den DATEN, nie getippt (ASCII-Pruefdatei).
GOLD_EINHEIT = sorted(k for k, v in einheiten.alle().items()
                      if (v.get("kosten") or {}).get("gold") == 250)[0]
with open(os.path.join(ROOT, "data", "warenrezepte.json"), encoding="utf-8") as _f:
    REZEPTE = json.load(_f)
WARE = sorted(w for w, e in REZEPTE.items() if (e.get("kosten") or {}).get("metall"))[0]


def neuer_bot(name: str = "Haug", armee=None, karte: str = "original-036"):
    """Ein Bot mit EINEM Hauptdorf; `armee` setzt die Armee (ohne: leer)."""
    bot = M.BotPlayer(name, BK.BOT_FRAKTIONEN.get(name, "menschlich"), 0.3, 0.5)
    dorf = M.BotDorf(name="Haupt", hauptdorf=True, karte=karte,
                     vorraete={"holz": 5000.0, "stein": 5000.0, "nahrung": 5000.0})
    bot.doerfer = [dorf]
    # S-5b (03.11.2026): die Armee steht im Dorf - deshalb NACH dem Dorf setzen.
    bot.army = dict(armee or {})
    return bot, dorf


# ==========================================================================
abschnitt("1. Die Rechenregeln stehen in der Datendatei")
# ==========================================================================
check("1 die Datendatei ist eingeschaltet", bool(REGELN.get("aktiv")), str(REGELN.get("aktiv")))
check("1 das Fenster ist eine Zahl aus der Datei", float(REGELN.get("fenster_stunden") or 0) == 24.0,
      str(REGELN.get("fenster_stunden")))
check("1 die Datei begruendet das Fenster", len(str(REGELN.get("warum_fenster") or "")) > 120,
      str(len(str(REGELN.get("warum_fenster") or ""))))
check("1 die Datei sagt, was NICHT zaehlt (Bauten)", "Bauten" in str(REGELN.get("was_nicht_zaehlt") or ""),
      str(REGELN.get("was_nicht_zaehlt") or "")[:60])
check("1 die Datei nennt ihre Grenze", len(str(REGELN.get("ehrliche_grenze") or "")) > 120,
      str(len(str(REGELN.get("ehrliche_grenze") or ""))))
check("1 keine Wirtschaftszahl in der Datei (ausser dem Fenster)",
      not any(isinstance(v, (int, float)) and not isinstance(v, bool) and v != 24
              for v in REGELN.values()),
      str({k: v for k, v in REGELN.items()
           if isinstance(v, (int, float)) and not isinstance(v, bool)}))

# ==========================================================================
abschnitt("2. Nahrung: der belegte Verbrauch, in Stunden umgerechnet")
# ==========================================================================
bot, dorf = neuer_bot(armee={"x": 10})                   # 10 Einheiten, Namen egal
_bedarf = M.bot_rohstoffbedarf(bot)
check("2 10 Einheiten brauchen 80 Nahrung je Tag - also 3,3333 je Stunde",
      abs(float(_bedarf.get("nahrung", 0.0)) - 80.0 / 24.0) < 1e-6, str(_bedarf))
_leer_bot, _leer_dorf = neuer_bot()
check("2 ohne Armee kein Nahrungsposten", "nahrung" not in M.bot_rohstoffbedarf(_leer_bot),
      str(M.bot_rohstoffbedarf(_leer_bot)))

# ==========================================================================
abschnitt("3. Offene Ausbildung zaehlt, fertige nicht")
# ==========================================================================
bot, dorf = neuer_bot()
_kosten = (einheiten.alle().get(GOLD_EINHEIT) or {}).get("kosten") or {}
dorf.ausbildung = [{"einheit": GOLD_EINHEIT, "gebucht": False, "ende": 99999.0}]
_b = M.bot_rohstoffbedarf(bot)
check("3 der offene Auftrag erhoeht den Bedarf seines Rohstoffs",
      abs(float(_b.get("gold", 0.0)) - float(_kosten.get("gold", 0)) / 24.0) < 1e-6,
      f"{GOLD_EINHEIT}: {_b.get('gold')} gegen {float(_kosten.get('gold', 0)) / 24.0}")
check("3 Siedler werden mitgezaehlt (sie stehen im Kosten-Dict)",
      abs(float(_b.get("siedler", 0.0)) - float(_kosten.get("siedler", 0)) / 24.0) < 1e-6,
      str(_b.get("siedler")))
dorf.ausbildung[0]["gebucht"] = True                     # fertig = bezahlt
check("3 ein gebuchter Auftrag zaehlt NICHT", "gold" not in M.bot_rohstoffbedarf(bot),
      str(M.bot_rohstoffbedarf(bot)))

# ==========================================================================
abschnitt("4. Offene Werkstattware zaehlt nach ihrem Rezept")
# ==========================================================================
bot, dorf = neuer_bot()
_rezept = (REZEPTE.get(WARE) or {}).get("kosten") or {}
dorf.werkstaetten = {"schmiede": {"auftraege": [{"ware": WARE, "anzahl": 2}]}}
_b = M.bot_rohstoffbedarf(bot)
check("4 der Posten des Rezepts steht im Bedarf (2 Stueck, auf 24 h umgelegt)",
      abs(float(_b.get("metall", 0.0)) - 2.0 * float(_rezept.get("metall", 0)) / 24.0) < 1e-6,
      f"{WARE}: {_b.get('metall')}")
dorf.werkstaetten = {}
check("4 ohne Auftrag kein Posten", "metall" not in M.bot_rohstoffbedarf(bot),
      str(M.bot_rohstoffbedarf(bot)))

# ==========================================================================
abschnitt("5. Forschung: nur der NAECHSTE Schritt zaehlt")
# ==========================================================================
bot, dorf = neuer_bot()
_erster = M.bot_dorf_forschungsliste(bot)[0]
_b = M.bot_rohstoffbedarf(bot)
check("5 der erste Planschritt kostet Holz im Bedarf (Stufe 1 = 50 Holz / 24 h)",
      abs(float(_b.get("holz", 0.0)) - 50.0 / 24.0) < 1e-6, f"{_erster['forschung']}: {_b.get('holz')}")
dorf.forschungsauftrag = {"gebiet": str(_erster["forschung"]), "zielstufe": 1, "startzeit": 0.0,
                          "dauer_stunden": 1, "kosten": {"holz": 50}}
check("5 ein LAUFENDER Auftrag zaehlt nicht doppelt (er ist bezahlt)",
      abs(float(M.bot_rohstoffbedarf(bot).get("holz", 0.0)) - 50.0 / 24.0) < 1e-6,
      str(M.bot_rohstoffbedarf(bot).get("holz")))
bot.forschungsstaende = {str(_erster["forschung"]): int(_erster["bis_stufe"])}
# Waechterin: Baukunst bis Stufe 3 - dann kostet Stufe 2 genau 100 Holz, Stufe 3 genau 200.
_wa, _wa_dorf = neuer_bot(name="Brynhild")
_stufe1 = 50.0 / 24.0
_wa.forschungsstaende = {"Baukunst": 1}
_b2 = M.bot_rohstoffbedarf(_wa)
check("5 nach Stufe 1 rueckt die NAECHSTE Stufe derselben Forschung nach (2 = 100 Holz)",
      abs(float(_b2.get("holz", 0.0)) - 100.0 / 24.0) < 1e-6, f"{_b2.get('holz')} gegen {100.0 / 24.0}")
_wa.forschungsstaende = {"Baukunst": 3}                   # Zielstufe der ersten drei Schritte steht
_b3 = M.bot_rohstoffbedarf(_wa)
check("5 ist die Zielstufe erreicht, ruckt der NAECHSTE Planschritt nach (50 Holz Stufe 1)",
      abs(float(_b3.get("holz", 0.0)) - _stufe1) < 1e-6
      and float(_b3.get("holz", 0.0)) != float(_b2.get("holz", 0.0)),
      f"{_b3.get('holz')} gegen {_stufe1}")
check("5 ohne Datendatei bleibt nur der belegte Nahrungsbedarf",
      set(M.bot_rohstoffbedarf(bot, {"aktiv": False}).keys()) <= {"nahrung"},
      str(M.bot_rohstoffbedarf(bot, {"aktiv": False})))

# ==========================================================================
abschnitt("6. Die Kartenwahl steht auf 'mittel' und bekommt den Bedarf")
# ==========================================================================
# ENTSCHEIDUNG GEAENDERT (S-11, 04.11.2026, Register 181): Daniel hat die Kartenwahl mit
# Feldverstaendnis abgesegnet; die Stufe steht seitdem auf "engpass" (Karte nach dem Engpass der
# Taktik). Entscheidung 4 (03.11.) bleibt die BEGRUENDUNG fuer den Bedarf je Rohstoff - der wird
# weiter gebraucht und weiter gerechnet (`bot_rohstoffbedarf`), nur nicht mehr allein fuer die Wahl.
check("6 kartenwahl_stufe ist eine bekannte Stufe und gesetzt",
      str(WIRTSCHAFT.get("kartenwahl_stufe")) in ("engpass", "mittel", "schwer", "leicht"),
      str(WIRTSCHAFT.get("kartenwahl_stufe")))
check("6 die Stufe steht auf 'engpass' (S-11, Register 181)",
      str(WIRTSCHAFT.get("kartenwahl_stufe")) == "engpass", str(WIRTSCHAFT.get("kartenwahl_stufe")))
check("6 der Hinweis nennt die neue Voraussetzung (Bedarf je Rohstoff)",
      "bot_rohstoffbedarf" in str(WIRTSCHAFT.get("kartenwahl_stufe_hinweis") or ""),
      str(WIRTSCHAFT.get("kartenwahl_stufe_hinweis") or "")[:80])
check("6 die Kartenwahl bekommt den gerechneten Bedarf, kein leeres dict",
      "bot_rohstoffbedarf(bot)" in TEXT_MAIN
      and "dict(raten or {}), {}, spieloekonomie.REGELN" not in TEXT_MAIN,
      "main.bot_doerfer_karten_zuweisen")
bot, dorf = neuer_bot(armee={GOLD_EINHEIT: 4})            # Bedarf: Nahrung + naechste Forschung
vorher = dorf.karte
M.bot_doerfer_karten_zuweisen(bot)
check("6 auch mit 'mittel' bekommt das Dorf eine Karte (kein Dorf ohne Ertrag)",
      bool(dorf.karte) and dorf.karte == vorher, str(dorf.karte))
_andere, _dorf2 = neuer_bot(name="Niemand")               # ohne Armee, ohne Plaene
M.bot_doerfer_karten_zuweisen(_andere)
check("6 die Gold-Regel bleibt der Rueckfall (auch ohne Bedarf eine Karte)",
      bool(_dorf2.karte), str(_dorf2.karte))

# ==========================================================================
abschnitt("7. Quellwachen")
# ==========================================================================
check("7 der Bedarf wird gerechnet, nicht im Aufrufer erfinden",
      "def bot_rohstoffbedarf(" in TEXT_MAIN and "def bot_bedarf_einstellungen(" in TEXT_MAIN,
      "main.py")
check("7 die eine Rechenstelle fuer Nahrung bleibt spieloekonomie.tagesbedarf_nahrung",
      "spieloekonomie.tagesbedarf_nahrung(dict(getattr(bot, \"army\", None) or {}))" in TEXT_MAIN,
      "main.bot_rohstoffbedarf")
befund("7 ehrliche Grenze: der Bedarf ist eine PLANUNGSGROESSE (was das Dorf in den naechsten "
       "24 h bezahlen will), keine Messung des Verbrauchs; Bauten zaehlen bewusst nicht mit, und "
       "die Kartenwahl vergleicht ihn mit dem STUNDENERTRAG der Karte - aendert also die Kartenwahl, "
       "nicht die Wirtschaft.", "")

sys.exit(bericht())
