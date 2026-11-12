"""E1: der Handelspreis haengt am ROHSTOFF, nicht an einer Pauschale (Daniels Entscheidung 306).

Daniels Wortlaut (08.11.2026, 17:52): "zu Frage 1: Handelspreis je Rohstoff statt pauschal bitte".
Vorher nahm der Spielerhandel den Preis EINER Kampfeinheit (250 x 1,2 = 300 Gold) als Preis JEDES
Rohstoffs; die fertige Preisfunktion `botkern.oekonomie_angebot` wurde von KEINER Stelle aufgerufen
(gemessen in `docs/extern/PRUEFUNG_OPUS_20261108.md`).

Geprueft wird:
  a1  `bot_handelpreis` ist eine MODULfunktion und liest `oekonomie_angebot`/`schattenpreis`
  a2  Ankunft und BEIDE Masken fragen sie; die Pauschale steht nur noch im Bot-Takt
  b1  zwei Rohstoffe haben zwei Preise (das ist die Entscheidung selbst)
  b2  die Reserve haelt: unter der Reserve verkauft der Bot nichts, kauft aber weiter
  b3  ein knapper Bot zahlt beim Einkauf MEHR als ein satter
  b4  mehr Bestand macht den Preis nicht teurer
  b5  ohne Karte kein Absturz und derselbe Preis wie mit der Referenzkarte
  b6  das Temperament verschiebt den Preis um hoechstens +-10 Prozent
"""
from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b
# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.
PRUEF_ART = "rechnen"
PRUEF_STUFE = 2
PRUEF_BETRIFFT = ['botkern', 'main:*', 'originalkarten', 'spieloekonomie']
PRUEF_DATEN = []
# --- Ende Pruefstand-Kopf -------------------------------------------------------

import os
import sys
import ast
from pathlib import Path

WURZEL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WURZEL / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from harness import abschnitt, bericht, check                     # noqa: E402
import main as M                                                  # noqa: E402
import originalkarten                                             # noqa: E402

QUELLE = (WURZEL / "src" / "main.py").read_text(encoding="utf-8")
KARTE = originalkarten.startkarte("handelspreis", "spieler")


def _methode(name: str) -> str:
    """Quelltext EINER Methode, ueber die AST-Grenzen geschnitten."""
    for knoten in ast.walk(ast.parse(QUELLE)):
        if isinstance(knoten, ast.FunctionDef) and knoten.name == name:
            return "\n".join(QUELLE.split("\n")[knoten.lineno - 1:knoten.end_lineno])
    raise AssertionError("Methode fehlt im Quelltext: " + name)


def _bot(armee: int = 0, vorraete: dict = None, temperament: float = 0.0):
    """Ein nackter Bot mit Armee (die Armee ist der einzige BELEGTE laufende Verbrauch)."""
    bot = M.BotPlayer("Haug", "menschlich", aggression=0.3, trading=0.9)
    bot.temperament = temperament
    bot.armee = {"einheit": int(armee)}
    bot.army = {"einheit": int(armee)}
    bot.vorraete = dict(vorraete or {})
    return bot


abschnitt("1. EINE Preisfunktion (Quellstruktur)")
check("bot_handelpreis ist eine Modulfunktion, keine Methode",
      "\ndef bot_handelpreis(" in QUELLE, "nicht auf Spaltenanfang gefunden")
_rumpf = QUELLE[QUELLE.index("def bot_handelpreis("):QUELLE.index("def bot_nahrungsbedarf(")]
check("sie liest die vorhandene Preisfunktion des Kerns", "botkern.oekonomie_angebot(" in _rumpf, "fehlt")
check("der Verkaufspreis kommt aus dem Schattenpreis", "spieloekonomie.schattenpreis(" in _rumpf, "fehlt")
check("die Ankunft fragt sie", "bot_handelpreis(" in _methode("_fremdvertrag_buchen"), "fehlt")
check("die Kaufmaske fragt sie", "bot_handelpreis(" in _methode("_handel_maske"), "fehlt")
check("die Verkaufsmaske fragt sie", "bot_handelpreis(" in _methode("_verkauf_maske"), "fehlt")
check("die Pauschale steht in KEINER der drei Handelsstellen",
      "referenzpreis_aus_beschaffung(BOT_BESCHAFFUNGSKOSTEN)" not in _methode("_fremdvertrag_buchen")
      and "referenzpreis_aus_beschaffung(BOT_BESCHAFFUNGSKOSTEN)" not in _methode("_handel_maske")
      and "referenzpreis_aus_beschaffung(BOT_BESCHAFFUNGSKOSTEN)" not in _methode("_verkauf_maske"),
      "Fundstelle vorhanden")
check("sie steht nur noch im Bot-Takt (bots_tick, Daniels Entscheidung 306)",
      QUELLE.count("referenzpreis_aus_beschaffung(BOT_BESCHAFFUNGSKOSTEN)") == 1,
      str(QUELLE.count("referenzpreis_aus_beschaffung(BOT_BESCHAFFUNGSKOSTEN)")))

abschnitt("2. Je Rohstoff ein Preis (die Entscheidung selbst)")
_satt = _bot(armee=0, vorraete={"holz": 400, "stein": 400, "gold": 900})
_holz = M.bot_handelpreis(_satt, "holz", KARTE, "kauf")
_stein = M.bot_handelpreis(_satt, "stein", KARTE, "kauf")
check("Holz und Stein haben NICHT denselben Preis",
      _holz["preis"] is not None and _stein["preis"] is not None and _holz["preis"] != _stein["preis"],
      "Holz %s, Stein %s" % (_holz["preis"], _stein["preis"]))
check("beide Preise sind positive Zahlen", float(_holz["preis"]) > 0 and float(_stein["preis"]) > 0,
      "%s / %s" % (_holz["preis"], _stein["preis"]))
check("die Pauschale 300 kommt nicht mehr heraus", float(_holz["preis"]) != 300.0, str(_holz["preis"]))

abschnitt("3. Die Reserve haelt (kein Verkauf auf Kosten der Versorgung)")
_knapp = _bot(armee=10, vorraete={"nahrung": 5})
check("unter der Reserve verkauft der Bot nichts",
      M.bot_handelpreis(_knapp, "nahrung", KARTE, "kauf")["preis"] is None,
      str(M.bot_handelpreis(_knapp, "nahrung", KARTE, "kauf")))
check("kaufen darf er trotzdem (dann zahlt er)",
      M.bot_handelpreis(_knapp, "nahrung", KARTE, "verkauf")["preis"] is not None,
      str(M.bot_handelpreis(_knapp, "nahrung", KARTE, "verkauf")))
_voll = _bot(armee=10, vorraete={"nahrung": 5000})
check("ueber der Reserve verkauft er wieder",
      M.bot_handelpreis(_voll, "nahrung", KARTE, "kauf")["preis"] is not None,
      str(M.bot_handelpreis(_voll, "nahrung", KARTE, "kauf")))

abschnitt("4. Ein knapper Bot zahlt mehr als ein satter")
_knapp_preis = float(M.bot_handelpreis(_knapp, "nahrung", KARTE, "verkauf")["preis"])
_satt_preis = float(M.bot_handelpreis(_voll, "nahrung", KARTE, "verkauf")["preis"])
check("der knappe Bot zahlt mehr", _knapp_preis > _satt_preis,
      "knapp %s gegen satt %s" % (_knapp_preis, _satt_preis))

abschnitt("5. Mehr Bestand macht den Preis nicht teurer")
_viel = _bot(armee=10, vorraete={"nahrung": 50000})
_p_viel = float(M.bot_handelpreis(_viel, "nahrung", KARTE, "verkauf")["preis"])
check("mehr Bestand senkt oder haelt den Preis", _p_viel <= _satt_preis,
      "viel %s gegen satt %s" % (_p_viel, _satt_preis))

abschnitt("6. Ohne Karte kein Absturz (neutrale Referenz)")
_ohne = M.bot_handelpreis(_satt, "holz", None, "kauf")
_mit = M.bot_handelpreis(_satt, "holz", originalkarten.startkarte("preis", "spieler"), "kauf")
check("ohne Karte kommt ein Preis", _ohne.get("preis") is not None, str(_ohne))
check("ohne Karte gilt der neutrale Faktor (derselbe Preis)",
      float(_ohne["preis"]) == float(_mit["preis"]), "%s gegen %s" % (_ohne["preis"], _mit["preis"]))

abschnitt("7. Das Temperament verschiebt hoechstens +-10 Prozent")
_b_plus = _bot(armee=10, vorraete={"nahrung": 5000}, temperament=1.0)
_b_minus = _bot(armee=10, vorraete={"nahrung": 5000}, temperament=-1.0)
_p_plus = float(M.bot_handelpreis(_b_plus, "nahrung", KARTE, "kauf")["preis"])
_p_minus = float(M.bot_handelpreis(_b_minus, "nahrung", KARTE, "kauf")["preis"])
check("+1 hebt den Preis", _p_plus > _p_minus, "%s gegen %s" % (_p_plus, _p_minus))
check("die Spanne bleibt bei 20 Prozent", abs(_p_plus - _p_minus) <= 0.21 * _p_plus,
      "%s gegen %s" % (_p_plus, _p_minus))

abschnitt("8. Unbekanntes bleibt harmlos")
check("ein Rohstoff ohne Bestand liefert eine Antwort statt eines Absturzes",
      isinstance(M.bot_handelpreis(_satt, "gibtsnicht", KARTE, "kauf"), dict), "kein dict")
check("Gold hat einen Preis", M.bot_handelpreis(_satt, "gold", KARTE, "kauf")["preis"] is not None,
      str(M.bot_handelpreis(_satt, "gold", KARTE, "kauf")))

sys.exit(bericht())
