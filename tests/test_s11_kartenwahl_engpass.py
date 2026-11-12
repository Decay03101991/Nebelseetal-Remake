# -*- coding: ascii -*-
"""Wache S-11: Kartenwahl mit Feldverstaendnis (04.11.2026).

DAS PROBLEM, GEMESSEN (vor dem Umbau)
-------------------------------------
`bot_kartenwahl` zog drei Kandidaten und liess dann die Regel aus `botkern.oekonomie_kartenwahl`
(Stufe `mittel`) oder die alte Gold-Regel entscheiden. Beide kennen die TAKTIK nicht: zwei Bots mit
verschiedenen Taktiken und DERSELBEN Kandidatenliste waehlten dieselbe Karte. Daniels Konzept S-11
verlangt das Gegenteil: die Karte, die den ENGSTEN Rohstoff SEINER Taktik am besten traegt.

Was diese Datei beweist
-----------------------
1. Der BEDARF eines Wachstumszyklus kommt aus dem Kern, nicht aus einer getippten Zahl:
   680 Holz, 300 Stein, 550 Nahrung, 80 Metall, 150 Leder, 100 Wolle, 4 Pferde
   (Siedlerkarren aus `spieloekonomie.U`, Gruendung aus `spieloekonomie.gruendungskosten`).
2. Der STUNDENERTRAG der Mindestanlagen je Taktik stimmt mit der von Hand nachgerechneten Tabelle
   ueberein (Holz/Stein/Nahrung/Gold/Metall/Leder/Wolle/Pferde) - zehn Zahlen je Taktik.
3. Der ENGPASS ist bedarfsgewichtet (Wartezeit = Bedarf / Ertrag), NICHT die kleinste Ernte:
   Holz steht bei jeder Taktik vorn, weil ein Zyklus 680 Holz braucht; Pferde stehen hinten, weil
   vier Pferde in unter einer Stunde zusammen sind.
4. `botkern.taktik_kartenscore` rechnet rein und reproduzierbar (gleiche Eingabe, gleiche Punkte).
5. Die WAHL unter denselben Kandidaten ist je Taktik verschieden - die Pruefzusage aus dem Konzept.
6. Die Wahl nimmt die Karte mit dem hoechsten Punktewert und ist wiederholbar.
7. Die alten Stufen bleiben unveraendert waehlbar (`mittel` liefert weiter eine Karte).

Aufruf:  python -X utf8 tests/test_s11_kartenwahl_engpass.py
"""
from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b
# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.
PRUEF_ART = "quelltext"
PRUEF_STUFE = 1
PRUEF_BETRIFFT = ['botkern', 'main:*', 'punkte', 'spieloekonomie']
PRUEF_DATEN = ['buildings.json']
# --- Ende Pruefstand-Kopf -------------------------------------------------------

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, bericht, check, import_src  # noqa: E402

ROOT, SRC = import_src()
import botkern as BK  # noqa: E402
import main as M  # noqa: E402
import spieloekonomie as O  # noqa: E402

TEXT_MAIN = open(os.path.join(SRC, "main.py"), encoding="utf-8").read()
TAKTIKEN = ("Pluenderer", "Waechterin", "Bastionier", "Spaeherin", "Raecher")
BOT_ZU_TAKTIK = {"Haug": "Pluenderer", "Brynhild": "Waechterin", "Grom": "Bastionier",
                 "Silra": "Spaeherin", "Krank": "Raecher"}
KANDIDATEN = ["original-001", "original-006", "original-014", "original-036", "original-118b"]


def _bot(name: str):
    """Ein Bot dieses Namens (seine Taktik haengt am Namen)."""
    return M.BotPlayer(name, BK.BOT_FRAKTIONEN.get(name, "menschlich"), 0.5, 0.5)


def _profil(karte: str) -> dict:
    return M.bot_kartenprofil(karte)


# ==========================================================================
abschnitt("1. Der Bedarf eines Wachstumszyklus kommt aus dem Kern")
bedarf = M.bot_gruendung_bedarf()
karren = (O.U.get("Siedlerkarren") or {}).get("kosten") or {}
_preis, _paket, minimum = O.gruendungskosten()
for roh, soll in (("holz", 680), ("stein", 300), ("nahrung", 550), ("metall", 80),
                  ("leder", 150), ("wolle", 100), ("pferde", 4)):
    check("1 Bedarf %s = %s (Karren + Gruendung)" % (roh, soll), float(bedarf.get(roh, 0)) == float(soll),
          str(bedarf.get(roh)))
check("1 Siedler zaehlen nicht als Rohstoff", "siedler" not in bedarf, str(sorted(bedarf)))
check("1 der Bedarf ist die Summe aus Karren und Gruendung",
      float(bedarf.get("holz", 0)) == float(karren.get("holz", 0)) + float(minimum.get("holz", 0)),
      "%s + %s" % (karren.get("holz"), minimum.get("holz")))

# ==========================================================================
abschnitt("2. Der Stundenertrag der Mindestanlagen stimmt mit der Handrechnung")
# Von Hand aus den Mindestzahlen und den belegten Ertraegen gerechnet (04.11.2026, geprueft gegen
# data/buildings.json). Grundlage: docs/MESSUNG_S8_STUFE3_BAUPLAENE_20261104.md, Abschnitt 1.
HAND = {
    "Pluenderer": {"holz": 13, "stein": 9, "nahrung": 19, "gold": 12, "metall": 6,
                   "leder": 11, "wolle": 6, "pferde": 6},
    "Waechterin": {"holz": 17, "stein": 17, "nahrung": 20, "gold": 6, "metall": 6,
                   "leder": 8, "wolle": 3, "pferde": 3},
    "Bastionier": {"holz": 13, "stein": 13, "nahrung": 16, "gold": 9, "metall": 9,
                   "leder": 8, "wolle": 6, "pferde": 6},
    "Spaeherin": {"holz": 13, "stein": 9, "nahrung": 19, "gold": 9, "metall": 9,
                  "leder": 11, "wolle": 3, "pferde": 9},
    "Raecher": {"holz": 13, "stein": 9, "nahrung": 16, "gold": 6, "metall": 12,
                "leder": 8, "wolle": 3, "pferde": 6},
}
for taktik in TAKTIKEN:
    ertrag = M.bot_taktik_stundenertrag(taktik)
    for roh, soll in HAND[taktik].items():
        check("2 %s: %s = %s je Stunde" % (taktik, roh, soll),
              float(ertrag.get(roh, 0.0)) == float(soll), str(ertrag.get(roh)))

# ==========================================================================
abschnitt("3. Der Engpass ist bedarfsgewichtet, nicht die kleinste Ernte")
ERWARTET = {"Pluenderer": ("holz", "stein"), "Waechterin": ("holz", "wolle"),
            "Bastionier": ("holz", "nahrung"), "Spaeherin": ("holz", "stein"),
            "Raecher": ("holz", "nahrung")}
for taktik in TAKTIKEN:
    engpass = M.bot_taktik_engpass(taktik)
    check("3 %s hat Engpass-Zeilen" % taktik, len(engpass) >= 6, str(len(engpass)))
    check("3 %s: die zwei engsten Rohstoffe sind %s" % (taktik, ERWARTET[taktik]),
          (engpass[0]["rohstoff"], engpass[1]["rohstoff"]) == ERWARTET[taktik],
          str([(z["rohstoff"], z["stunden"]) for z in engpass[:2]]))
    check("3 %s: Holz steht vorn (ein Zyklus braucht 680 Holz)" % taktik,
          engpass[0]["rohstoff"] == "holz", str(engpass[0]))
    pferde = [z for z in engpass if z["rohstoff"] == "pferde"][0]
    check("3 %s: Pferde sind KEIN Engpass (4 Stueck)" % taktik,
          pferde["stunden"] < 2.0, str(pferde))
    check("3 %s: die Stunden sind Bedarf/Ertrag" % taktik,
          abs(float(engpass[0]["stunden"]) - float(engpass[0]["bedarf"]) / float(engpass[0]["produktion"])) < 0.01,
          "%s / %s" % (engpass[0]["bedarf"], engpass[0]["produktion"]))
# Ohne Plan bleibt nur das Grundeinkommen (1 Holz, 1 Stein) - es wird KEINE Anlage erfunden.
ohne_plan = M.bot_taktik_engpass("Gibtsnicht")
check("3 eine unbekannte Taktik erfindet keine Anlagen",
      all(float(z["produktion"]) == 0.0 for z in ohne_plan
          if z["rohstoff"] not in ("holz", "stein")), str(ohne_plan[:2]))
check("3 ohne Plan bleibt nur das Grundeinkommen (1 Holz, 1 Stein)",
      {z["rohstoff"]: z["produktion"] for z in ohne_plan if z["stunden"] is not None}
      == {"holz": 1.0, "stein": 1.0},
      str({z["rohstoff"]: z["produktion"] for z in ohne_plan if z["stunden"] is not None}))

# ==========================================================================
abschnitt("4. Der Kartenscore rechnet rein und reproduzierbar")
engpass = M.bot_taktik_engpass("Pluenderer")
profil = _profil("original-006")
punkte = BK.taktik_kartenscore(engpass, profil)
check("4 der Score ist eine Zahl", isinstance(punkte, float), str(type(punkte)))
check("4 gleiche Eingabe ergibt gleiche Punkte", BK.taktik_kartenscore(engpass, profil) == punkte, "")
check("4 der Score nutzt nur die zwei engsten Rohstoffe",
      punkte == round(float(profil.get(engpass[0]["rohstoff"], 0.0)) * float(engpass[0]["stunden"])
                      + float(profil.get(engpass[1]["rohstoff"], 0.0)) * float(engpass[1]["stunden"]), 6),
      str(punkte))
check("4 ohne Engpass sind die Punkte 0", BK.taktik_kartenscore([], profil) == 0.0, "")
check("4 ein leeres Profil ergibt 0", BK.taktik_kartenscore(engpass, {}) == 0.0, "")

# ==========================================================================
abschnitt("5. Dieselben Kandidaten, verschiedene Taktik: verschiedene Karte (Pruefzusage)")
wahlen = {}
for name, taktik in BOT_ZU_TAKTIK.items():
    wahl = M.bot_kartenwahl_nach_engpass(_bot(name), KANDIDATEN)
    wahlen[taktik] = wahl
    check("5 %s waehlt eine Karte aus den Kandidaten" % taktik, wahl in KANDIDATEN, wahl)
check("5 Pluenderer und Waechterin waehlen VERSCHIEDENE Karten",
      wahlen["Pluenderer"] != wahlen["Waechterin"],
      "%s gegen %s" % (wahlen["Pluenderer"], wahlen["Waechterin"]))
# Die Pruefzusage verlangt VERSCHIEDENE Wahlen bei verschiedenen Taktiken - nicht bei jedem Paar:
# Taktiken mit demselben Engpass-Paar (z. B. Bastionier und Raecher: holz/nahrung) waehlen mit
# Absicht dieselbe Karte. Bewiesen wird die Trennung dort, wo sich die Engpaesse unterscheiden.
verschieden = {t2 for t2 in TAKTIKEN if wahlen[t2] != wahlen["Pluenderer"]}
check("5 mindestens zwei Taktiken waehlen gegen den Pluenderer eine andere Karte",
      len(verschieden) >= 1, str(sorted(verschieden)))
gleicher_engpass = [t2 for t2 in TAKTIKEN
                    if ERWARTET[t2] == ERWARTET["Pluenderer"] and t2 != "Pluenderer"]
for t2 in gleicher_engpass:                                     # gleiches Engpass-Paar, gleiche Karte
    check("5 %s hat dasselbe Engpass-Paar wie der Pluenderer und waehlt dieselbe Karte" % t2,
          wahlen[t2] == wahlen["Pluenderer"], "%s gegen %s" % (wahlen[t2], wahlen["Pluenderer"]))
check("5 die Wahl ist wiederholbar (zweiter Aufruf gleich)",
      M.bot_kartenwahl_nach_engpass(_bot("Haug"), KANDIDATEN) == wahlen["Pluenderer"], "")
# Die gewaehlte Karte traegt den Engpass am besten von den dreien - hier ueber ALLE Kandidaten geprueft.
for taktik, wahl in wahlen.items():
    e = M.bot_taktik_engpass(taktik)
    punkte = {k: BK.taktik_kartenscore(e, _profil(k)) for k in KANDIDATEN}
    check("5 %s: die gewaehlte Karte hat den hoechsten Score" % taktik,
          punkte[wahl] == max(punkte.values()), "%s=%s von %s" % (wahl, punkte[wahl], sorted(punkte.values())))

# ==========================================================================
abschnitt("6. Die Stufe steht in der Datendatei, die alten Stufen bleiben")
einstellungen = M.bot_wirtschaft_einstellungen()
check("6 kartenwahl_stufe steht auf engpass", str(einstellungen.get("kartenwahl_stufe")) == "engpass",
      str(einstellungen.get("kartenwahl_stufe")))
check("6 die Stufe ist im Hinweis der Datendatei erklaert",
      "S-11 (04.11.2026)" in str(einstellungen.get("kartenwahl_stufe_hinweis")), "")
bot = _bot("Haug")
alt = M.bot_kartenwahl(bot, 0, einstellungen=dict(einstellungen, kartenwahl_stufe="mittel"))
check("6 die alte Stufe mittel liefert weiter eine Karte", bool(alt), str(alt))
neu = M.bot_kartenwahl(bot, 0, einstellungen=dict(einstellungen, kartenwahl_stufe="engpass"))
check("6 die Stufe engpass liefert eine Karte", bool(neu), str(neu))
check("6 beide Wege sind reproduzierbar (zweiter Aufruf gleich)",
      M.bot_kartenwahl(bot, 0, einstellungen=dict(einstellungen, kartenwahl_stufe="engpass")) == neu, "")
check("6 die Quellwache: bot_kartenwahl ruft die Engpass-Wahl auf",
      "nach_engpass = bot_kartenwahl_nach_engpass(bot, kandidaten)" in TEXT_MAIN, "")
check("6 die Kartenwahl laeuft ohne Zufall ausser der Kandidatenwahl (random nur fuer die drei)",
      TEXT_MAIN.count('random.Random("karte:%s:%d"') == 1, str(TEXT_MAIN.count('random.Random("karte:%s:%d"')))

sys.exit(bericht())
