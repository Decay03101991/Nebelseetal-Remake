# -*- coding: ascii -*-
"""DER BLICK IN FREMDE WELTEN UND DIE DOERFER JE WELT - Stufe W-6/W-7 (03.11.2026).

Daniels Vorgabe, woertlich (Umlaute hier als ae/oe/ue, die Datei ist ASCII): "der spieler startet
in der Hauptwelt und sieht bereits die bots wenn er in die Uebersicht einer anderen welt schaut. Auch
soll er sehen wenn der bot sein zweites dorf gegruendet hat das in seiner welt bereits 2 doerfer von
ihm stehen."

Was diese Datei beweist
-----------------------
1. "Ansehen" ist NUR LESEN: die gezeigte Welt wechselt, die eigene Welt des Spielers nicht, und es
   kostet kein Mana (kein Weltensprung, keine Sperre).
2. Auf der angesehenen fremden Welt stehen GENAU die Doerfer dieser Welt (Burg + Wappen), und KEINE
   eigenen - die Zahl stimmt mit den Doerfern des Bots ueberein (W-7: "2 Doerfer von ihm").
3. Die Zeile unter der Karte nennt Bot, Fraktion und Zahl seiner Doerfer in dieser Welt.
4. Ein Klick auf ein Dorf einer fremden Welt startet KEINEN Auftrag - solange W-3 offen ist, gibt es
   dort nur eine Meldung (kein Angriff ueber die Weltgrenze).
5. Die eigene Welt zeigt weiter die eigenen Doerfer (Rueckweg ueber "einsehen" der eigenen Welt).
6. Quellwachen: das Ansehen bucht nichts, und der Klick prueft die Welt.

Aufruf:  python -X utf8 tests/test_portal_fremdblick.py
"""
from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b
# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.
PRUEF_ART = "fenster"
PRUEF_STUFE = 3
PRUEF_BETRIFFT = ['auftraege', 'main:*', 'welt']
PRUEF_DATEN = []
# --- Ende Pruefstand-Kopf -------------------------------------------------------

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src

ROOT, SRC = import_src()
sys.path[:0] = [SRC, os.path.join(ROOT, "tools")]
import main as M  # noqa: E402
import tkinter as tk  # noqa: E402
import gpt_erzeuge_startstaende as starter  # noqa: E402

TEXT_MAIN = open(os.path.join(SRC, "main.py"), encoding="utf-8").read()

# ==========================================================================
abschnitt("1. Ansehen ist nur Lesen (W-6)")
# ==========================================================================
try:
    root = tk.Tk()
    root.withdraw()
except tk.TclError as fehler:
    print("Kein Fenster moeglich (kein Desktop): %s" % fehler)
    print("Diese Pruefung braucht einen angemeldeten Windows-Desktop.")
    sys.exit(0)

app = M.NebelseetalApp(root)
app._build_main_ui()
app._volk_waehlen("menschlich")            # Spieler in Midgard, Bots in den anderen Welten
app._erste_siedlung_gruenden()
gs = app.state
gs.tick(3600.0)                            # setzt die Dorfpositionen der Bots
app._menue_auffrischen()

_eigene = int(gs.eigene_dimension)
_mana_vorher = float(gs.resources["mana"].amount)
_bot_welten = {}
for _bot in gs.bots:
    for _dorf in M.bot_doerfer_sicherstellen(_bot):
        _bot_welten.setdefault(int(_dorf.dimension), []).append((_bot.name, _dorf.name))
_fremd = next((w for w in sorted(_bot_welten) if w != _eigene), 0)
check("1 es gibt eine fremde Welt mit Bot-Doerfern", _fremd > 0, str(sorted(_bot_welten)))

app._portal_ansehen(_fremd)
check("1 die angesehene Welt ist gemerkt", int(getattr(app, "_portal_blick", 0)) == _fremd,
      str(getattr(app, "_portal_blick", None)))
check("1 die EIGENE Welt des Spielers bleibt unveraendert", int(gs.eigene_dimension) == _eigene,
      str(gs.eigene_dimension))
check("1 Ansehen kostet KEIN Mana", float(gs.resources["mana"].amount) == _mana_vorher,
      f"{_mana_vorher} -> {gs.resources['mana'].amount}")
check("1 Ansehen legt keinen Weltensprung an", not [a for a in gs.auftraege], str(len(gs.auftraege)))


def _karte():
    """Die 400x400-Zeichenflaeche des Portals (oder None).

    Seit dem Bildrahmen der Weltkarte (03.11.2026, Register 178) sitzt die Zeichenflaeche in einem
    eigenen Rahmen-Rahmen (`_kartenrahmen_bauen`) - deshalb wird der Baum DURCHSUCHT statt nur die
    direkten Kinder. Die Zusage bleibt dieselbe: es gibt genau eine Karte mit den Dorfzeichen.
    """
    def _suchen(widget):
        for kind in widget.winfo_children():
            if kind.winfo_class() == "Canvas" and kind.winfo_width() == 400 and kind.winfo_height() == 400:
                return kind
            treffer = _suchen(kind)
            if treffer is not None:
                return treffer
        return None
    return _suchen(app.content)


def _texte(widget):
    """Alle sichtbaren Texte eines Widget-Baums (fuer die Zeile unter der Karte)."""
    raus = []
    try:
        raus.append(str(widget.cget("text")))
    except Exception:                                                  # noqa: BLE001
        pass
    for k in widget.winfo_children():
        raus.extend(_texte(k))
    return raus


root.update()
_leinwand = _karte()
check("1 die Karte ist gezeichnet", _leinwand is not None, "")
_erwartet = len(_bot_welten.get(_fremd, []))
# F-100 (13.11.2026): kein Wappen-Abzeichen mehr auf der Karte - je Dorf EIN Bild (die Burg).
# Ohne Bild faellt der Kasten ein, und der besteht aus Rechteck + zwei Linien (3 Objekte).
_je_marke = 1 if M.WAPPEN else 3
check("1 auf der fremden Welt steht JEDES Dorf dieser Welt",
      _leinwand is not None and len(_leinwand.find_withtag("portalbote")) == _erwartet * _je_marke,
      f"{len(_leinwand.find_withtag('portalbote')) if _leinwand else '?'} gegen {_erwartet * _je_marke}")
check("1 und KEIN eigenes Dorf", _leinwand is not None
      and len(_leinwand.find_withtag("portalspieler")) == 0,
      str(len(_leinwand.find_withtag("portalspieler")) if _leinwand else "?"))

# ==========================================================================
abschnitt("2. W-7: die Zeile nennt Bot, Fraktion und Zahl seiner Doerfer")
# ==========================================================================
_texte_alle = " | ".join(t for t in _texte(app.content) if t)
check("2 die Zeile 'Fremde D\u00f6rfer auf dieser Welt' steht da",
      "Fremde D\u00f6rfer auf dieser Welt" in _texte_alle, _texte_alle[:160])
_name, _ = _bot_welten[_fremd][0]
check("2 sie nennt den Bot", _name in _texte_alle, _name)
check("2 und die Zahl seiner Doerfer",
      ("%d D\u00f6rfer" % _erwartet) in _texte_alle, _erwartet)

# ==========================================================================
abschnitt("3. Klick auf ein fremdes Dorf startet KEINEN Auftrag (W-3 offen)")
# ==========================================================================
_bot, _dorf = next((b, d) for b in gs.bots for d in M.bot_doerfer_sicherstellen(b)
                   if int(d.dimension) == _fremd)
_auftraege_vorher = len(gs.auftraege)
_nachrichten_vorher = len(gs.messages)
app._bot_dorf_optionen(_bot, _dorf)
check("3 es entsteht kein Auftrag", len(gs.auftraege) == _auftraege_vorher,
      str(len(gs.auftraege)))
check("3 stattdessen steht eine Begruendung im Postfach",
      len(gs.messages) > _nachrichten_vorher
      and any("NUR ANSICHT" in str(m.get("text")) for m in gs.messages),
      str([m.get("text") for m in gs.messages][-1:])[:140])

# ==========================================================================
abschnitt("4. Zurueck auf die eigene Welt")
# ==========================================================================
app._portal_ansehen(_eigene)
root.update()
_leinwand2 = _karte()
check("4 die eigene Welt zeigt wieder die eigenen Doerfer",
      _leinwand2 is not None and len(_leinwand2.find_withtag("portalspieler")) >= 1,
      str(len(_leinwand2.find_withtag("portalspieler")) if _leinwand2 else "?"))
check("4 und keine fremden Doerfer (die stehen in ihren Welten)",
      _leinwand2 is not None and len(_leinwand2.find_withtag("portalbote"))
      == len(_bot_welten.get(_eigene, [])) * _je_marke,
      str(len(_leinwand2.find_withtag("portalbote")) if _leinwand2 else "?"))

# ==========================================================================
abschnitt("5. Quellwachen")
# ==========================================================================
# S-4b (09.11.2026): `_portal_wechsel` ist entfernt. Die Zusage bleibt, ist jetzt aber schaerfer:
# weder im Ansehen noch ueberhaupt als Methode gibt es die alte Buchstelle.
check("5 Ansehen bucht nichts (kein _portal_wechsel, weder dort noch sonst)",
      "def _portal_ansehen" in TEXT_MAIN
      and "_portal_wechsel" not in TEXT_MAIN.split("def _portal_ansehen")[1].split("def ")[0]
      and not hasattr(M.NebelseetalApp, "_portal_wechsel"),
      "main._portal_ansehen")
check("5 die Karte zeichnet die ANGESEHENE Welt",
      "self._bot_doerfer_im_raster(kante, angezeigt)" in TEXT_MAIN, "main._render_portal")
check("5 der Klick prueft die Welt des Dorfes",
      "liegt auf Weltkarte %02d - das ist NUR ANSICHT" in TEXT_MAIN, "main._bot_dorf_optionen")

befund("5 ehrliche Grenze: die Ansicht zeigt nur, was offen ist - Burg und Wappen, Position und die "
       "Zahl der Doerfer je Bot. Truppen, Wall und Vorraete kommen erst ueber einen Spionagebericht, "
       "und ein Angriff ueber die Weltgrenze ist bis zur Entscheidung W-3 gesperrt.", "")

root.destroy()
sys.exit(bericht())
