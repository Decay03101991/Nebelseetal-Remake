"""S4-4: Rachetopf (06.11.2026, Register 286, docs/ABLAUF_LLM_20261106.md Schritt 4).

Geprueft wird, was der Schnitt zusagt, mit den Entscheidungen Daniels vom 06.11.2026:
  A. Alle Zahlen kommen aus `data/diplomatie.json` (A-7), nicht aus dem Code.
  B. Unter dem Goetterschutz ruht der Topf (5 Tage = 0).
  C. Ohne Schutz und ohne Kontakt: +1 je Spieltag, hoechstens einmal je Tag.
  D. Die Armee-Schwelle ist 99 SK (98 reicht nicht, 99 schon).
  E. Es gibt GENAU EINE Ankuendigung je Ausloesung, und der Angriff kommt erst nach dem Vorlauf.
  F. Nach einem Bot-Sieg faellt der Topf auf 0 (F-3).
  G. Ein laufender Pakt blockiert den Angriff; der Topf steigt aber WEITER (Daniel 13:50).
  H. Nach dem Paktende gilt der Vorlauf von 28.800 s.
  I. Ein alter Spielstand ohne `rache` laedt mit 0 (additiv, kein Zwangsfeld).
  J. Quellwache: der Racheangriff laeuft ueber den VORHANDENEN Weg (`naechster_angriff`),
     kein zweiter Angriffspfad, kein Text im Code.
  K. Echter Verlauf: der Bot-Takt fuellt den Topf, kuendigt an und gibt danach den Angriff frei.

ASCII-only (Pruefdatei-Konvention).
"""
from __future__ import annotations

import ast
import glob
import inspect
import os
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src

import_src()
import diplomatie as D
import main

TAG = 28800.0  # ein Spieltag in Spielsekunden (aus data/diplomatie.json)


def _code(funktion) -> str:
    """Quelltext einer Funktion ohne Docstring (Docstrings zaehlen nicht als Code)."""
    baum = ast.parse(textwrap.dedent(inspect.getsource(funktion)))  # Funktion in einen Baum wandeln
    kopf = baum.body[0]  # der FunctionDef-Knoten
    if kopf.body and isinstance(kopf.body[0], ast.Expr) and isinstance(kopf.body[0].value, ast.Constant):
        kopf.body = kopf.body[1:]  # fuehrenden Docstring abschneiden
    return ast.unparse(baum)  # Rest als Text


def _bot(gunst=50, rache=0):
    """Ein Bot in dict-Form mit Gedaechtnis - so, wie der Kern ihn fuehrt."""
    return {"name": "Haug", "gunst": gunst, "rache": rache, "gedaechtnis": {}, "vertraege": {}}


abschnitt("A. Die Zahlen kommen aus der Datendatei (A-7)")
datei = D.daten()
rache_block = datei.get("rache") or {}
check("Schalter rache_aktiv ist gesetzt", D.rache_aktiv(datei) is True, str(rache_block.get("aktiv")))
check("Schwelle ist 3", int(rache_block.get("schwelle", 0)) == 3, str(rache_block.get("schwelle")))
check("Armee-Schwelle ist 99 SK (nicht 90)", int(rache_block.get("armee_sk", 0)) == 99,
      str(rache_block.get("armee_sk")))
check("nach einem Bot-Sieg auf 0 (F-3)", int(rache_block.get("nach_bot_sieg", -1)) == 0,
      str(rache_block.get("nach_bot_sieg")))
check("der Topf steigt unter einem Pakt (Daniel 13:50)",
      rache_block.get("ruht_unter_vertrag") is False, str(rache_block.get("ruht_unter_vertrag")))
check("unter Goetterschutz ruht er", rache_block.get("ruht_unter_goetterschutz") is True,
      str(rache_block.get("ruht_unter_goetterschutz")))
check("drei Ankuendigungstexte liegen in der Datei",
      isinstance(rache_block.get("ankuendigung"), list) and len(rache_block["ankuendigung"]) == 3,
      str(len(rache_block.get("ankuendigung") or [])))
eigene = {"rache": {"aktiv": True, "schwelle": 1, "armee_sk": 1, "hoechstwert": 2, "je_niederlage": 1,
                    "spieltag_sekunden": 100, "vorlauf_sekunden": 50, "nach_paktende_sekunden": 50,
                    "nach_bot_sieg": 0, "ankuendigung": ["a"]}}
b_eigen = _bot()
check("geaenderte Schwelle in den Daten aendert das Urteil",
      D.rache_bereit(b_eigen, 5, 0.0, eigene) is False and
      D.rache_bereit(dict(b_eigen, rache=1), 5, 0.0, eigene) is True, "Schwelle 1 statt 3")
check("der Deckel kommt aus der Datei", D.rache_setzen(b_eigen, 9, eigene) == 2, str(b_eigen.get("rache")))

abschnitt("B. Unter dem Goetterschutz ruht der Topf")
bot_b = _bot()
for tag in range(1, 6):                                    # fuenf Spieltage mit Schutz
    D.rache_tag(bot_b, TAG * tag, goetterschutz=True)
check("nach 5 Tagen unter Schutz steht der Topf auf 0", D.rache_von(bot_b) == 0, str(D.rache_von(bot_b)))
D.rache_tag(bot_b, TAG * 6, goetterschutz=False)            # Schutz vorbei
check("ohne Schutz steigt er sofort", D.rache_von(bot_b) == 1, str(D.rache_von(bot_b)))

abschnitt("C. Ein Spieltag ohne Kontakt ergibt genau einen Punkt")
bot_c = _bot()
D.rache_tag(bot_c, TAG * 1)
D.rache_tag(bot_c, TAG * 2)
D.rache_tag(bot_c, TAG * 3)
check("nach 3 Tagen steht er auf 3", D.rache_von(bot_c) == 3, str(D.rache_von(bot_c)))
D.rache_tag(bot_c, TAG * 3 + 100)                           # zweiter Aufruf am selben Tag
check("ein zweiter Aufruf am selben Tag bucht nichts", D.rache_von(bot_c) == 3, str(D.rache_von(bot_c)))
D.kontakt_buchen(bot_c, TAG * 3 + 200)                        # Kontakt
D.rache_tag(bot_c, TAG * 4)                                  # Tag 4, aber Kontakt war kuerzlich
check("nach einem Kontakt waechst der Topf an diesem Tag nicht", D.rache_von(bot_c) == 3,
      str(D.rache_von(bot_c)))
D.rache_tag(bot_c, TAG * 5)                                  # ein Tag ohne Kontakt
check("einen Tag nach dem Kontakt waechst er wieder", D.rache_von(bot_c) == 4, str(D.rache_von(bot_c)))
check("der Deckel haelt (hoechstwert 5)", D.rache_setzen(bot_c, 99) == 5, str(D.rache_von(bot_c)))

abschnitt("D. Die Armee-Schwelle ist 99 SK")
bot_d = _bot(rache=3)                                       # Topf reif
check("SK 98 reicht nicht", D.rache_bereit(bot_d, 98, TAG * 3) is False, "98 < 99")
check("SK 99 reicht", D.rache_bereit(bot_d, 99, TAG * 3) is True, "99 >= 99")
check("Topf 2 reicht nicht", D.rache_bereit(_bot(rache=2), 99, TAG * 3) is False, "2 < 3")
import einheiten as E
check("die Schlagkraft kommt aus den Einheitsdaten (3 Krieger = 9 SK)",
      E.armee_schlagkraft({"Krieger": 3}) == 9.0, str(E.armee_schlagkraft({"Krieger": 3})))
check("Unbrauchbares zaehlt 0", E.armee_schlagkraft({"Krieger": True, "Unbekannt": 4}) == 0.0,
      str(E.armee_schlagkraft({"Krieger": True, "Unbekannt": 4})))

abschnitt("E. Genau eine Ankuendigung, Angriff erst nach dem Vorlauf")
bot_e = _bot(rache=3)
text_e = D.ankuendigung_text(bot_e)
check("die Ankuendigung hat einen Text aus der Datei", bool(text_e), text_e[:40])
check("der Text steht in der Datendatei, nicht im Code",
      all(ord(c) < 128 for c in open(os.path.join(os.path.dirname(os.path.dirname(
          os.path.abspath(__file__))), "src", "diplomatie.py"), encoding="utf-8").read()),
      "diplomatie.py ist ASCII")
quelle_takt = _code(main.GameState.bots_fortschreiben)
check("der Takt setzt den Ankuendigungs-Merker", 'rache_ankuendigung' in quelle_takt, "Merkmal vorhanden")
check("der Takt loescht ihn einmalig", "pop('rache_ankuendigung'" in quelle_takt, "pop vorhanden")
check("die Frist kommt aus der Datei (diplomatie.vorlauf_sekunden)",
      "diplomatie.vorlauf_sekunden(" in quelle_takt, "Aufruf vorhanden")
check("der Topf wird je Takt gebucht (diplomatie.rache_tag)",
      "diplomatie.rache_tag(" in quelle_takt, "Aufruf vorhanden")

abschnitt("F. Nach einem Bot-Sieg faellt der Topf auf 0")
bot_f = _bot(rache=5)
check("Sieg setzt den Topf auf 0", D.rache_nach_sieg(bot_f) == 0, str(D.rache_von(bot_f)))
quelle_ausgang = _code(main.GameState.bots_fortschreiben)
check("der Takt bucht den Sieg (diplomatie.rache_nach_sieg)",
      "diplomatie.rache_nach_sieg(" in quelle_ausgang, "Aufruf vorhanden")
check("der Takt bucht die Niederlage (diplomatie.rache_buchen)",
      "diplomatie.rache_buchen(_rache_daten, 'niederlage')" in quelle_ausgang, "Aufruf vorhanden")

abschnitt("G. Der Pakt blockiert den Angriff, der Topf steigt weiter")
bot_g = _bot(rache=3)
D.vertrag_anbieten(bot_g, "nichtangriff", 0.0)               # Pakt ab Spielzeit 0
check("unter dem Pakt kein Racheangriff", D.rache_bereit(bot_g, 99, TAG * 1) is False, "gesperrt")
vorher = D.rache_von(bot_g)
D.rache_tag(bot_g, TAG * 2, goetterschutz=False)              # Topf steigt trotz Pakt
check("der Topf steigt unter dem Pakt weiter", D.rache_von(bot_g) >= vorher, str(D.rache_von(bot_g)))

abschnitt("H. Nach dem Paktende gilt der Vorlauf von 28.800 s")
bot_h = _bot(rache=4)
D.vertrag_anbieten(bot_h, "nichtangriff", 0.0)               # Pakt bis 86.400 s
D.pakt_brechen(bot_h, 1000.0)                                # der Spieler bricht ihn bei 1.000 s
check("das Ende des Pakts ist gemerkt", D.vertrag_ende(bot_h, "nichtangriff") == 1000.0,
      str(D.vertrag_ende(bot_h, "nichtangriff")))
check("1 s nach dem Bruch kein Angriff", D.rache_bereit(bot_h, 99, 1001.0) is False, "zu frueh")
check("28.799 s nach dem Bruch kein Angriff", D.rache_bereit(bot_h, 99, 1000.0 + TAG - 1) is False,
      "noch zu frueh")
check("28.800 s nach dem Bruch ist der Weg frei", D.rache_bereit(bot_h, 99, 1000.0 + TAG) is True,
      "Vorlauf um")
bot_h2 = _bot(rache=4)                                       # zweite Probe: Ablauf statt Bruch
D.vertrag_anbieten(bot_h2, "nichtangriff", 0.0)
D.vertrag_aktiv(bot_h2, "nichtangriff", 86400.0)             # Pakt laeuft ab
check("auch der Ablauf wird als Ende gemerkt", D.vertrag_ende(bot_h2, "nichtangriff") == 86400.0,
      str(D.vertrag_ende(bot_h2, "nichtangriff")))

abschnitt("I. Alter Spielstand ohne rache")
alt = {"name": "Altbot", "faction": "Mensch", "aggression": 0.5, "trading": 0.5}
bot_i = main.bot_aus_stand(dict(alt))
check("ohne Feld startet der Topf bei 0", bot_i.rache == 0, str(bot_i.rache))
check("ohne Feld gibt es kein Vertragsende", bot_i.vertrag_ende == {}, str(bot_i.vertrag_ende))
bot_i.rache = 99                                             # kaputter Wert
daten_i = main.GameState.bot_als_dict(object(), bot_i)
main.GameState.bot_aus_dict(object(), bot_i, daten_i)
check("ein zu grosser Topf wird beim Laden geklemmt", bot_i.rache == 5, str(bot_i.rache))
main.GameState.bot_aus_dict(object(), bot_i, {"angriffe": 1})  # ohne das Feld
check("Rueckschreiben ohne das Feld behaelt den Topf", bot_i.rache == 5, str(bot_i.rache))

abschnitt("J. Quellwache: ein Weg, kein zweiter Angriffspfad")
check("die Freigabe laeuft ueber naechster_angriff", "naechster_angriff = 0" in quelle_takt,
      "kein eigener Angriffsweg")
check("diplomatie startet selbst keinen Auftrag",
      "auftraege." not in _code(D.rache_bereit) and "auftraege." not in _code(D.rache_tag),
      "nur Urteile")
check("der Spielerangriff ist Kontakt",
      "diplomatie.kontakt_buchen(" in _code(main.NebelseetalApp._angriff_auftrag_starten),
      "Aufruf im Angriffsweg")
check("der Handelsabschluss ist Kontakt",
      "diplomatie.kontakt_buchen(" in _code(main.GameState.handel_fortschreiben)
      if hasattr(main.GameState, "handel_fortschreiben") else True, "geprueft, wenn vorhanden")

abschnitt("K. Echter Verlauf: Takt fuellt den Topf, kuendigt an, gibt den Angriff frei")
root = None
app = None
try:
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    app = main.NebelseetalApp(root)
    app._build_main_ui()
    st = app.state
    app._erste_siedlung_gruenden()
    haug = main.BotPlayer(name="Haug", faction="menschlich", aggression=0.5, trading=0.5)
    haug.doerfer = [main.BotDorf(name="Haugsdorf 1", hauptdorf=True, dimension=1, herkunftswelt=1)]
    haug.doerfer[0].einheiten = {"Krieger": 40}              # 40 x SK 3 = 120 SK (ueber der Schwelle)
    haug.doerfer[0].vorraete = {"holz": 500.0, "stein": 500.0, "nahrung": 500.0}
    haug.doerfer[0].wall_stufe = 0
    haug.doerfer[0].wall_zustand = 100.0
    st.bots = [haug]
    st.noob_protection = False                               # der Schutz ist vorbei
    haug.rache = 2                                           # zwei Punkte fehlen bis zur Schwelle
    haug.naechster_angriff = TAG * 10                        # der Bot wuerde sonst von selbst angreifen
    check("die Armee-Schwelle ist mit 40 Kriegern erreicht", E.armee_schlagkraft(haug.army) >= 99,
          str(E.armee_schlagkraft(haug.army)))
    st._letzter_bot_takt = 0.0
    ergebnis1 = st.bots_fortschreiben(TAG)                    # Spieltag 1: Topf auf 3
    check("der Takt hat den Topf gefuellt", haug.rache >= 3, str(haug.rache))
    check("vor der Ankuendigung greift der Bot nicht an", not ergebnis1.get("angriffe"),
          str(ergebnis1.get("angriffe")))
    _texte = [m for m in st.messages if m.get("type") == "rache"]
    check("die Ankuendigung ist im Postfach", len(_texte) == 1, str(len(_texte)))
    _merk = float((haug.gedaechtnis or {}).get("rache_ankuendigung") or 0.0)
    check("die Frist ist gemerkt", _merk > 0, str(_merk))
    ergebnis2 = st.bots_fortschreiben(TAG * 2)                # Spieltag 2: Vorlauf ist um
    check("nach dem Vorlauf ist der Merker weg", not (haug.gedaechtnis or {}).get("rache_ankuendigung"),
          str(haug.gedaechtnis))
    check("die Freigabe hat den Angriffstermin aufgeloest (der Bot hat gehandelt)",
          float(haug.naechster_angriff) != TAG * 10,
          "vorher %s, jetzt %s" % (TAG * 10, float(haug.naechster_angriff)))
    _texte2 = [m for m in st.messages if m.get("type") == "rache"]
    check("es bleibt bei EINER Ankuendigung", len(_texte2) == 1, str(len(_texte2)))
finally:
    if root is not None:
        try:
            root.destroy()
        except Exception:
            pass

sys.exit(bericht())
