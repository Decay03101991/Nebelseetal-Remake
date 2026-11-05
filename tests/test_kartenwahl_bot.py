# -*- coding: ascii -*-
"""Der Anschluss an `botkern.oekonomie_kartenwahl` (V-6, 03.11.2026).

Vorher: die Funktion stand fertig im Kern und hatte **keinen Aufrufer** - die Karte eines
Bot-Dorfes kam allein aus der Gold-Regel (`bot_kartenwahl`: hoechster Goldwert der drei
Kandidaten). Jetzt entscheidet die STUFE aus `data/bot_wirtschaft.json` (`kartenwahl_stufe`)
unter denselben drei Kandidaten; die Gold-Regel bleibt der Rueckfall, damit kein Dorf ohne
Karte und ohne Ertrag bleibt.

Was diese Datei beweist
-----------------------
1. Der Kern wird wirklich gerufen: der Quelltext von `main.py` nennt
   `botkern.oekonomie_kartenwahl`, und die Stufe steht in der Datendatei.
2. Die Wahl der Stufe "schwer" ist der hoechste Portfolio-Nutzen der drei Kandidaten
   (`spieloekonomie.kartennutzen`) - unabhaengig nachgerechnet.
3. Das Portfolio des Bots wirkt: dieselbe Karte ist als ZWEITE Wahl weniger wert als als erste.
4. Rueckfall: unbekannte Stufe und "leicht" (gruenden: false) liefern trotzdem eine Karte.
5. Jedes Dorf bekommt genau eine Karte, ein zweiter Lauf vergibt nichts mehr (idempotent).
6. Die Wahl ist reproduzierbar (derselbe Bot, dieselbe Dorfnummer, dieselbe Karte).

Aufruf:  python -X utf8 tests/test_kartenwahl_bot.py
"""
from __future__ import annotations

import os
import random
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, bericht, check, import_src

ROOT, SRC = import_src()
import botkern as BK  # noqa: E402
import main as M  # noqa: E402
import originalkarten as OK  # noqa: E402
import spieloekonomie as O  # noqa: E402

TEXT_MAIN = open(os.path.join(SRC, "main.py"), encoding="utf-8").read()
TEXT_BOTKERN = open(os.path.join(SRC, "botkern.py"), encoding="utf-8").read()

# ==========================================================================
# 1. Der Kern wird gerufen, die Stufe steht in der Datendatei
# ==========================================================================
abschnitt("1. Anschluss vorhanden")
check("main.py ruft botkern.oekonomie_kartenwahl",
      "botkern.oekonomie_kartenwahl(" in TEXT_MAIN)
check("botkern.py kennt die Funktion weiterhin",
      "def oekonomie_kartenwahl(" in TEXT_BOTKERN)
einst = M.bot_wirtschaft_einstellungen()
stufe = str(einst.get("kartenwahl_stufe") or "")
check("die Stufe steht in data/bot_wirtschaft.json", bool(stufe), stufe)
# ENTSCHEIDUNG GEAENDERT (S-11, 04.11.2026, Register 181): die Stufe "engpass" ist KEINE Stufe des
# Kern-Regelwerks - sie wird in `main.bot_kartenwahl_nach_engpass` gerechnet (Feldprofil x Engpass der
# Taktik) und laeuft VOR der Kern-Regel. Die Zusage dieser Wache bleibt: eine gesetzte Stufe ist
# bekannt und keine Tippfehler-Falle; `leicht`, `mittel` und `schwer` stehen weiter im Regelwerk.
BOTS_REGELN = O.REGELN.get("bots") or {}
check("die Stufe ist bekannt: im Regelwerk oder als Engpass-Stufe in main",
      stufe in BOTS_REGELN or (stufe == "engpass" and "bot_kartenwahl_nach_engpass" in TEXT_MAIN),
      str(sorted(BOTS_REGELN)) + " | stufe=" + stufe)
check("die drei Kern-Stufen stehen weiter im Regelwerk",
      {"leicht", "mittel", "schwer"} <= set(BOTS_REGELN), str(sorted(BOTS_REGELN)))
check("die Begruendung steht als Feld daneben (kein Wert ohne Quelle)",
      bool(einst.get("kartenwahl_stufe_hinweis")))

# ==========================================================================
# 2. Die Wahl der Stufe ist der hoechste Portfolio-Nutzen - nachgerechnet
# ==========================================================================
abschnitt("2. Die Stufe 'schwer' waehlt den hoechsten Portfolio-Nutzen "
         "(03.11.2026 EXPLIZIT gesetzt - Daniels Entscheidung 4 hat die Vorgabe auf 'mittel' gestellt)")
IDs = sorted(M.bot_karten_katalog())
check("der Kartenkatalog ist da (127 Originalkarten)", len(IDs) >= 100, str(len(IDs)))


def _kandidaten(name: str, index: int, anzahl: int = 0):
    """Dieselben Kandidaten, die `bot_kartenwahl` zieht (gleicher Zufall, gleicher Seed).

    Register 225 (Daniel 05.11.2026): die Zahl der gezogenen Karten steht in
    `data/bot_wirtschaft.json` (`karten_kandidaten`, jetzt 1). Die alte feste 3 haette hier
    weiter drei Kandidaten erwartet, waehrend der Code eine Karte zieht.
    """
    if not anzahl:
        anzahl = int(einst.get("karten_kandidaten") or 3)
    zufall = random.Random("karte:%s:%d" % (name, int(index)))
    return zufall.sample(IDs, min(anzahl, len(IDs)))


def _bester_nutzen(kandidaten, eigene):
    """Der Kandidat mit dem hoechsten Portfolio-Nutzen (Definition der Stufe "schwer")."""
    return max(kandidaten, key=lambda k: (O.kartennutzen(eigene, M._bot_karte_dict(k)),
                                          k.replace("original-", "")))


_bot = M.BotPlayer("Grom", "zwergisch", 0.5, 0.5, settlements=["A", "B"])
_kand0 = _kandidaten("Grom", 0)
_erwartet0 = _bester_nutzen(_kand0, [])
_gewaehlt0 = M.bot_kartenwahl(_bot, 0, einstellungen=einst, stufe="schwer")
check("erstes Dorf: genau der Kandidat mit dem hoechsten Nutzen",
      _gewaehlt0 == _erwartet0, f"{_gewaehlt0} / {_erwartet0} aus {_kand0}")

# Mit dem Portfolio des ersten Dorfes: dieselbe Karte ist als zweite weniger wert.
_eigene = [M._bot_karte_dict(_gewaehlt0)]
_kand1 = _kandidaten("Grom", 1)
_erwartet1 = _bester_nutzen(_kand1, _eigene)
_gewaehlt1 = M.bot_kartenwahl(_bot, 1, einstellungen=einst, stufe="schwer",
                              belegte=[_gewaehlt0], raten={"holz": 12.0})
check("zweites Dorf: das Portfolio des Bots fliesst ein",
      _gewaehlt1 == _erwartet1, f"{_gewaehlt1} / {_erwartet1} aus {_kand1}")
_wert_als_erste = O.kartennutzen([], M._bot_karte_dict(_gewaehlt0))
_wert_als_zweite = O.kartennutzen(_eigene, M._bot_karte_dict(_gewaehlt0))
check("dieselbe Karte ist als zweite Wahl nicht mehr wert",
      _wert_als_zweite < _wert_als_erste,
      f"{_wert_als_zweite:.4f} < {_wert_als_erste:.4f}")

# ==========================================================================
# 3. Rueckfall: kein Dorf bleibt ohne Karte
# ==========================================================================
abschnitt("3. Rueckfall auf die Gold-Regel")
_ohne_stufe = M.bot_kartenwahl(_bot, 0, einstellungen=einst, stufe="")
check("ohne Stufe waehlt die alte Gold-Regel eine Karte", bool(_ohne_stufe), _ohne_stufe)
_leicht = M.bot_kartenwahl(_bot, 0, einstellungen=einst, stufe="leicht")
check("Stufe 'leicht' (gruenden: false) liefert trotzdem eine Karte", bool(_leicht), _leicht)
_unbekannt = M.bot_kartenwahl(_bot, 0, einstellungen=einst, stufe="gibtsnicht")
check("unbekannte Stufe stuerzt nicht ab und liefert eine Karte", bool(_unbekannt), _unbekannt)
check("unbekannte Stufe = Gold-Regel", _unbekannt == _ohne_stufe, f"{_unbekannt} / {_ohne_stufe}")

# ==========================================================================
# 4. Im echten Bot: jedes Dorf eine Karte, idempotent, reproduzierbar, schnell
# ==========================================================================
abschnitt("4. Zuordnung an die Doerfer")
_b1 = M.BotPlayer("Brynhild", "menschlich", 0.5, 0.6, settlements=["A", "B", "C"])
_t0 = time.time()
_neu = M.bot_doerfer_karten_zuweisen(_b1)
_dauer = time.time() - _t0
check("jedes Dorf bekommt eine Karte", _neu == 3 and all(d.karte for d in _b1.doerfer),
      f"{_neu} / {[d.karte for d in _b1.doerfer]}")
check("keine Karte doppelt im Reich des Bots",
      len({d.karte for d in _b1.doerfer}) == 3, str([d.karte for d in _b1.doerfer]))
check("ein zweiter Lauf vergibt nichts mehr (idempotent)",
      M.bot_doerfer_karten_zuweisen(_b1) == 0)
_b2 = M.BotPlayer("Brynhild", "menschlich", 0.5, 0.6, settlements=["A", "B", "C"])
M.bot_doerfer_karten_zuweisen(_b2)
check("dieselbe Wahl bei demselben Bot (reproduzierbar)",
      [d.karte for d in _b1.doerfer] == [d.karte for d in _b2.doerfer],
      f"{[d.karte for d in _b1.doerfer]} / {[d.karte for d in _b2.doerfer]}")
check("drei Doerfer in unter zwei Sekunden (kein Warten im Bot-Takt)",
      _dauer < 2.0, f"{_dauer:.2f} s")

# ==========================================================================
# 5. Die Regel aendert wirklich etwas (Gegenprobe gegen die reine Gold-Regel)
# ==========================================================================
abschnitt("5. Gegenprobe: mit EINER Karte URTEILT die Regel, statt zu waehlen (Register 225)")
# Register 225 (Daniel 05.11.2026): die Bots ziehen EINE Karte. Eine Wahl unter Kandidaten gibt es
# damit nicht mehr - die Regel wirkt als URTEIL (`main.bot_kartenurteil`: Punktzahl der Karte gegen
# den Durchschnitt aller Karten derselben Taktik). Die frueher hier stehende Gegenprobe "die Regel
# waehlt bei mindestens einem der fuenf Bots eine andere Karte" konnte mit einer Karte nicht mehr
# greifen (0 von 5) - sie ist umgehaengt, nicht geloescht: geprueft wird jetzt das Urteil.
_bot5 = M.BotPlayer("Haug", "menschlich", 0.5, 0.5, settlements=["A"])
_regel = M.bot_kartenwahl(_bot5, 0, einstellungen=einst, stufe=stufe)
_gold = M.bot_kartenwahl(_bot5, 0, einstellungen=einst, stufe="")
check("mit einer Karte liefern Regel und Gold-Weg dieselbe Karte", _regel == _gold,
      f"{_regel} / {_gold}")
_urteil = M.bot_kartenurteil(_bot5, _regel)
check("das Urteil rechnet gegen den Durchschnitt der Taktik",
      _urteil["durchschnitt"] > 0 and _urteil["karte"] == _regel,
      f"{_urteil['karte']} / Durchschnitt {_urteil['durchschnitt']:.3f}")
check("gut_genug folgt aus Punktzahl und Durchschnitt",
      _urteil["gut_genug"] == (_urteil["punkte"] >= _urteil["durchschnitt"]),
      f"{_urteil['punkte']:.3f} gegen {_urteil['durchschnitt']:.3f}")

# ==========================================================================
# 6. Die Stufe 'mittel' (Vorgabe seit 03.11.2026, Daniels Entscheidung 4)
# ==========================================================================
abschnitt("6. Stufe 'mittel': die am schlechtesten gedeckte Rohstoffachse entscheidet")
_free = {k: {"besitzer": None, "karte": M._bot_karte_dict(k)} for k in _kand0}
# Bedarf nur fuer Holz, Ertrag fast nichts: Holz ist damit die schlechteste Deckung.
_mittel = BK.oekonomie_kartenwahl("mittel", [], _free, {"holz": 1.0}, {"holz": 10.0}, O.REGELN)
_erwartet_mittel = max(_kand0, key=lambda k: (O.kapazitaeten(M._bot_karte_dict(k)).get("holz", 0),
                                              k.replace("original-", "")))
check("'mittel' nimmt die Karte mit der meisten Kapazitaet auf der Mangel-Achse",
      _mittel == _erwartet_mittel, f"{_mittel} / {_erwartet_mittel} aus {_kand0}")
check("'mittel' ohne Bedarf liefert None (der Aufrufer faellt dann auf die Gold-Regel zurueck)",
      BK.oekonomie_kartenwahl("mittel", [], _free, {"holz": 1.0}, {}, O.REGELN) is None, "")
check("der Bedarf kommt aus main.bot_rohstoffbedarf, nicht aus einer zweiten Formel",
      "bot_rohstoffbedarf(bot)" in TEXT_MAIN and "def bot_rohstoffbedarf(" in TEXT_MAIN,
      "main.py")

bericht()
