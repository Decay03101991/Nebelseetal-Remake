"""S4-3: Vertraege - Nichtangriffspakt, Handelsabkommen, Durchmarsch (06.11.2026, Register 285).

Geprueft wird, was der Schnitt zusagt (docs/ABLAUF_LLM_20261106.md Schritt 3, ergaenzt um die
Entscheidungen Daniels vom 06.11.2026, 13:50 und 14:00):

  A. Die Zahlen kommen aus `data/diplomatie.json` (A-7), nicht aus dem Code.
  B. Ein laufender Pakt sperrt den Bot-Angriff UND den Diebstahl (EINE Urteilsstelle).
  C. Der Pakt laeuft bei 259.199 s noch und ist bei 259.200 s abgelaufen (drei Spieltage, R3-1).
  D. Faellt die Gunst unter 40, bricht der Pakt: Gunst genau -20, Rache genau +1.
  E. Ein Angebot unter der noetigen Gunst wird abgelehnt.
  F. Quellwache: die Angriffswege rufen `diplomatie.angriff_gesperrt`, `punkte.angreifbar`
     bleibt die EINE Punktrechnung; der Paktbruch sitzt in `_angriff_auftrag_starten`.
  G. Das Durchmarschrecht ist reine Anzeige - im Code steht keine Mechanik.
  H. Ein alter Spielstand ohne `vertraege` laedt mit einer leeren Tabelle (kein Pakt).
  I. Ein Spielerangriff auf einen Pakt-Bot ist ERLAUBT und bricht den Pakt beim Absenden.
  J. Ein Handelsabkommen bricht NICHT mit - es endet still bei Ablauf.
"""
from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b
# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.
PRUEF_ART = "fenster"
PRUEF_STUFE = 2
PRUEF_BETRIFFT = ['diplomatie', 'einheiten', 'main:*', 'punkte', 'zeitbasis']
PRUEF_DATEN = ['diplomatie.json']
# --- Ende Pruefstand-Kopf -------------------------------------------------------

import ast
import glob
import inspect
import os
import sys
import textwrap
import types

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src

import_src()
import diplomatie as D
import main
import zeitbasis

TAG = float(zeitbasis.SEKUNDEN_JE_TAG)  # ein Spieltag (R3-1: die EINE Quelle)


def _code(funktion) -> str:
    """Quelltext einer Funktion OHNE Docstring - Docstrings zaehlen nicht als Code."""
    baum = ast.parse(textwrap.dedent(inspect.getsource(funktion)))  # Funktion in einen Baum wandeln
    kopf = baum.body[0]  # der FunctionDef-Knoten
    if kopf.body and isinstance(kopf.body[0], ast.Expr) and isinstance(kopf.body[0].value, ast.Constant):
        kopf.body = kopf.body[1:]  # fuehrenden Docstring abschneiden
    return ast.unparse(baum)  # Rest als Text


def _bot(name="Testbot", gunst=50):
    """Ein Bot mit Gunst - ohne Doerfer (armeearm, damit der Diebstahl greifen kann)."""
    bot = main.BotPlayer(name=name, faction="Mensch", aggression=0.5, trading=0.5)
    bot.gunst = gunst
    return bot


def _daten(bot):
    """Die dict-Form des Bots - derselbe Weg wie im Kern."""
    return main.GameState.bot_als_dict(object(), bot)


def _pakt(bot, jetzt=0.0):
    """Bietet den Nichtangriffspakt an und gibt die dict-Form zurueck."""
    daten = _daten(bot)
    ok, grund = D.vertrag_anbieten(daten, "nichtangriff", jetzt)
    check("Pakt-Angebot bei Gunst %d angenommen" % int(bot.gunst), ok is True, str(grund))
    return daten


DIEBSTAHL = {"aktiv": True, "nur_ohne_garnison": True, "armee_schwelle": 5,
             "anteil_prozent": 10, "hoechstens_je_rohstoff": 100,
             "hoechstens_je_diebstahl": 200, "sperre_stunden": 1}


def _ziel():
    """Ein wehrloser Ort mit Vorrat - Ziel eines Diebstahls."""
    return types.SimpleNamespace(name="Wehrlos", vorraete={"holz": 100.0}, einheiten={})


abschnitt("A. Die Zahlen kommen aus der Datendatei (A-7)")
datei = D.daten()  # die echte Projektdatei
check("Schalter vertraege_aktiv ist gesetzt", D.vertraege_aktiv(datei) is True,
      str(datei.get("vertraege", {}).get("aktiv")))
pakt = D.art_daten("nichtangriff", datei)  # Zahlen des Pakts
check("Pakt ab Gunst 40", int(pakt.get("min_gunst")) == 40, str(pakt.get("min_gunst")))
check("Pakt dauert 259.200 Spielsekunden (drei Spieltage)", int(pakt.get("dauer_sekunden")) == 3 * TAG,
      str(pakt.get("dauer_sekunden")))
check("Bruch kostet 20 Gunst", int(pakt.get("bruch_gunst")) == -20, str(pakt.get("bruch_gunst")))
check("Bruch bucht 1 Rache", int(pakt.get("bruch_rache")) == 1, str(pakt.get("bruch_rache")))
check("Durchmarsch ist nur_anzeige", D.art_daten("durchmarsch", datei).get("nur_anzeige") is True,
      str(D.art_daten("durchmarsch", datei).get("nur_anzeige")))
check("drei Vertragsarten", D.VERTRAGSARTEN == ("nichtangriff", "handel", "durchmarsch"),
      str(D.VERTRAGSARTEN))
eigene = {"vertraege": {"aktiv": True, "nichtangriff": {"min_gunst": 10, "dauer_sekunden": 100}}}
check("geaenderte Grenze in den Daten aendert das Urteil (10 statt 40)",
      D.vertrag_anbieten({"gunst": 20, "vertraege": {}}, "nichtangriff", 0.0, eigene)[0] is True,
      "Gunst 20 reicht bei min_gunst 10")
check("ohne Schalter gibt es keinen Vertrag",
      D.vertrag_anbieten({"gunst": 90, "vertraege": {}}, "nichtangriff", 0.0,
                         {"vertraege": {"aktiv": False}})[0] is False, "aktiv false sperrt")

abschnitt("B. Ein laufender Pakt sperrt Angriff UND Diebstahl")
bot = _bot(gunst=50)                      # Bot mit Gunst 50
daten = _pakt(bot)                        # Pakt anbieten
bot.vertraege = dict(daten["vertraege"])  # Pakt am Bot-Objekt (der Weg des Kerns)
check("angriff_gesperrt meldet den Pakt", D.angriff_gesperrt(daten, 100.0) == (True, "nichtangriffspakt"),
      str(D.angriff_gesperrt(daten, 100.0)))
check("dieselbe Antwort fuer das Bot-OBJEKT (kein dict noetig)",
      D.angriff_gesperrt(bot, 100.0) == (True, "nichtangriffspakt"), str(D.angriff_gesperrt(bot, 100.0)))
check("Diebstahl faellt aus, solange der Pakt steht",
      main.bot_diebstahl(bot, _ziel(), 100.0, DIEBSTAHL) is None, "kein Bericht mit Pakt")
bot.vertraege = {}                        # Pakt weg
bericht_dieb = main.bot_diebstahl(bot, _ziel(), 100.0, DIEBSTAHL)
check("ohne Pakt stiehlt derselbe Bot (das Gate ist der Pakt, nicht die Mechanik)",
      isinstance(bericht_dieb, dict) and bericht_dieb.get("summe", 0) > 0, str(bericht_dieb))

abschnitt("C. Der Pakt laeuft genau 259.200 Sekunden (drei Spieltage)")
bot_c = _bot(gunst=50)                    # frischer Bot
daten_c = _pakt(bot_c, 0.0)               # Pakt ab Spielzeit 0
check("bei 259.199 s noch aktiv", D.vertrag_aktiv(daten_c, "nichtangriff", 3 * TAG - 1) is True)
check("bei 259.200 s abgelaufen", D.vertrag_aktiv(daten_c, "nichtangriff", 3 * TAG) is False)
check("der abgelaufene Eintrag ist entfernt", "nichtangriff" not in daten_c.get("vertraege", {}),
      str(sorted(daten_c.get("vertraege", {}))))

abschnitt("D. Gunst unter 40 bricht den Pakt (Gunst -20, Rache +1)")
bot_d = _bot(gunst=50)                    # Bot mit Gunst 50
daten_d = _pakt(bot_d, 0.0)               # Pakt anbieten
D.gunst_setzen(daten_d, 39)               # Gunst faellt unter die Bruchgrenze
vorgaenge = D.vertraege_tick(daten_d, 100.0)
check("der Tick meldet genau einen Bruch", len(vorgaenge) == 1, str(vorgaenge))
eintrag = vorgaenge[0] if vorgaenge else {}
check("Art ist der Nichtangriffspakt", eintrag.get("art") == "nichtangriff", str(eintrag.get("art")))
check("Gunst genau -20", int(eintrag.get("gunst_delta", 0)) == -20, str(eintrag.get("gunst_delta")))
check("Rache genau +1", int(eintrag.get("rache_delta", 0)) == 1, str(eintrag.get("rache_delta")))
check("Gunst steht danach bei 19", D.gunst_von(daten_d) == 19, str(D.gunst_von(daten_d)))
check("der Pakt ist danach weg", "nichtangriff" not in daten_d.get("vertraege", {}),
      str(sorted(daten_d.get("vertraege", {}))))
check("ein zweiter Tick bucht nichts mehr", D.vertraege_tick(daten_d, 200.0) == [], "leer")

abschnitt("E. Angebot unter der noetigen Gunst wird abgelehnt")
bot_e = _bot(gunst=39)                    # Gunst unter 40
ok_e, grund_e = D.vertrag_anbieten(_daten(bot_e), "nichtangriff", 0.0)
check("Angebot bei Gunst 39 wird abgelehnt", ok_e is False, str(grund_e))
check("Grund ist die Gunst", grund_e == "gunst_zu_niedrig", str(grund_e))
ok_h, grund_h = D.vertrag_anbieten(_daten(_bot(gunst=40)), "handel", 0.0)
check("Handelsabkommen ab Gunst 40 angenommen", ok_h is True, str(grund_h))
ok_d, grund_d = D.vertrag_anbieten(_daten(_bot(gunst=59)), "durchmarsch", 0.0)
check("Durchmarsch erst ab Gunst 60", ok_d is False and grund_d == "gunst_zu_niedrig", str(grund_d))

abschnitt("F. Quellwache: EINE Urteilsstelle, keine zweite Rechnung")
quelle_angriff = _code(main.NebelseetalApp._angriff_auftrag_starten)  # der Weg des Spielers
check("_angriff_auftrag_starten bricht den Pakt", "diplomatie.pakt_brechen(" in quelle_angriff,
      "Aufruf vorhanden")
check("der Bruch steht VOR dem Absenden",
      quelle_angriff.index("pakt_brechen") < quelle_angriff.index("self.state.auftrag_starten"),
      "Reihenfolge Bruch -> Start")
check("der Bruch geht ueber GameState (dort liegen bot_als_dict/bot_aus_dict)",
      "self.state.bot_als_dict(" in quelle_angriff and "self.state.bot_aus_dict(" in quelle_angriff,
      "nicht self.bot_als_dict - NebelseetalApp hat diese Methoden nicht")
quelle_bots = _code(main.GameState.bots_fortschreiben)                 # der Bot-Takt
check("der Bot-Angriff fragt den Pakt (diplomatie.angriff_gesperrt)", "diplomatie.angriff_gesperrt(" in quelle_bots,
      "Aufruf vorhanden")
check("die Punktgrenze bleibt punkte.angreifbar", "punkte.angreifbar(" in quelle_bots,
      "keine zweite Punktrechnung")
quelle_dieb = _code(main.bot_diebstahl)                                # der Diebstahl
check("der Diebstahl fragt denselben Pakt", "diplomatie.angriff_gesperrt(" in quelle_dieb,
      "Aufruf vorhanden")
quelle_raub = _code(main.GameState._bots_raubzug)                      # Bot gegen Bot
check("Bot gegen Bot bleibt ohne Paktfrage (der Pakt gilt Spieler <-> Bot)",
      "angriff_gesperrt" not in quelle_raub, "bewusst nicht enthalten")
text_main = open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                              "src", "main.py"), encoding="utf-8").read()
check("punkte.angreifbar steht genau zweimal in main.py (EINE Rechenstelle, zwei Aufrufer)",
      text_main.count("punkte.angreifbar(") == 2, str(text_main.count("punkte.angreifbar(")))

abschnitt("G. Durchmarsch ist reine Anzeige")
bot_g = _bot(gunst=70)                    # genug Gunst fuer das Recht
daten_g = _daten(bot_g)
ok_g, grund_g = D.vertrag_anbieten(daten_g, "durchmarsch", 0.0)
check("Durchmarsch ab Gunst 60 vereinbart", ok_g is True, str(grund_g))
check("der Text nennt ihn als reine Anzeige", "nur Anzeige" in D.durchmarsch_text(daten_g, 10.0),
      D.durchmarsch_text(daten_g, 10.0))
check("ohne Recht kein Text", D.durchmarsch_text(_daten(_bot()), 10.0) == "", "leer")
fremde = []                               # Module, die das Recht mechanisch kennen
for pfad in sorted(glob.glob(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                          "src", "*.py"))):
    if os.path.basename(pfad) == "diplomatie.py":   # hier gehoert es hin
        continue
    if "durchmarsch" in open(pfad, encoding="utf-8").read().lower():
        fremde.append(os.path.basename(pfad))
check("kein anderes Modul kennt das Durchmarschrecht (keine Mechanik)", fremde == [], str(fremde))

abschnitt("H. Alter Spielstand ohne vertraege")
alt = {"name": "Altbot", "faction": "Mensch", "aggression": 0.5, "trading": 0.5}
bot_h = main.bot_aus_stand(dict(alt))
check("ohne Feld laedt eine leere Tabelle", bot_h.vertraege == {}, str(bot_h.vertraege))
check("ohne Feld gibt es keinen Pakt", D.angriff_gesperrt(bot_h, 0.0) == (False, ""),
      str(D.angriff_gesperrt(bot_h, 0.0)))
bot_h2 = main.bot_aus_stand(dict(alt, vertraege={"nichtangriff": {"seit": 0, "bis": int(3 * TAG)}}))
check("gespeicherter Pakt kommt zurueck",
      "nichtangriff" in bot_h2.vertraege
      and D.vertrag_aktiv(_daten(bot_h2), "nichtangriff", 10.0) is True,
      str(bot_h2.vertraege))
bot_h3 = main.bot_aus_stand(dict(alt, vertraege=None))
check("kaputter Wert (null) wird zur leeren Tabelle", bot_h3.vertraege == {}, str(bot_h3.vertraege))
bot_h2.gunst = 44                         # laufender Wert
daten_h = _daten(bot_h2)                  # hin
main.GameState.bot_aus_dict(object(), bot_h2, daten_h)   # und zurueck
check("Rundlauf traegt die Vertraege", "nichtangriff" in bot_h2.vertraege, str(bot_h2.vertraege))
main.GameState.bot_aus_dict(object(), bot_h2, {"angriffe": 1})   # Rueckschreiben OHNE das Feld
check("Rueckschreiben ohne das Feld loescht den Pakt NICHT", "nichtangriff" in bot_h2.vertraege,
      str(bot_h2.vertraege))

abschnitt("I. Spielerangriff: erlaubt, aber der Pakt bricht beim Absenden")
bot_i = _bot(gunst=50)                    # Gunst 50
daten_i = _pakt(bot_i, 0.0)               # Pakt anbieten
check("vorher sperrt der Pakt den Bot", D.angriff_gesperrt(daten_i, 500.0)[0] is True, "gesperrt")
bruch = D.pakt_brechen(daten_i, 500.0)    # der Spieler greift an
check("pakt_brechen meldet den Bruch", bruch.get("gebrochen") is True, str(bruch))
check("Gunst faellt um 20", int(bruch.get("gunst_delta", 0)) == -20, str(bruch.get("gunst_delta")))
check("Rache steigt um 1", int(bruch.get("rache_delta", 0)) == 1, str(bruch.get("rache_delta")))
check("Gunst steht danach bei 30", D.gunst_von(daten_i) == 30, str(D.gunst_von(daten_i)))
check("danach ist der Angriff NICHT verboten", D.angriff_gesperrt(daten_i, 500.0) == (False, ""),
      str(D.angriff_gesperrt(daten_i, 500.0)))
check("ohne Pakt bucht pakt_brechen nichts", D.pakt_brechen(daten_i, 600.0).get("gebrochen") is False,
      "kein zweiter Bruch")

abschnitt("J. Ein Handelsabkommen bricht nicht mit")
bot_j = _bot(gunst=60)                    # genug Gunst fuer beide Arten
daten_j = _daten(bot_j)
D.vertrag_anbieten(daten_j, "nichtangriff", 0.0)   # Pakt
D.vertrag_anbieten(daten_j, "handel", 0.0)         # Handelsabkommen
D.pakt_brechen(daten_j, 100.0)                     # der Pakt bricht
check("das Handelsabkommen bleibt bestehen", "handel" in daten_j.get("vertraege", {}),
      str(sorted(daten_j.get("vertraege", {}))))
check("es laeuft weiter", D.vertrag_aktiv(daten_j, "handel", 100.0) is True, "aktiv")
gunst_vorher = D.gunst_von(daten_j)                # Gunst vor dem Ablauf
check("bei 259.200 s ist es still zu Ende", D.vertrag_aktiv(daten_j, "handel", 3 * TAG) is False,
      "abgelaufen")
check("der Ablauf kostet KEINE Gunst", D.gunst_von(daten_j) == gunst_vorher,
      "%d -> %d" % (gunst_vorher, D.gunst_von(daten_j)))
check("der Tick meldet keinen Bruch fuer das Handelsabkommen",
      not any(v.get("art") == "handel" for v in D.vertraege_tick(daten_j, 3 * TAG)),
      "kein Vorgang")

abschnitt("K. Echter Verlauf: der Spieler greift einen Pakt-Bot an")
root = None
app = None
try:
    import tkinter as tk                                     # Oberflaeche nur fuer diesen Abschnitt
    root = tk.Tk()                                           # unsichtbares Fenster
    root.withdraw()                                          # nichts auf dem Schirm
    app = main.NebelseetalApp(root)                           # die echte App
    app._build_main_ui()                                     # Oberflaeche aufbauen
    st = app.state                                            # der Spielzustand
    app._erste_siedlung_gruenden()                            # echter Start (belegte Werte)
    ort = st.aktive_siedlung()                                # die eine Siedlung
    ort.einheiten = {"Krieger": 5}                            # Fixture: kleines Heer im Ortslager
    ort.vorraete = {"gold": 900.0, "nahrung": 900.0}          # Reisekosten bezahlbar
    haug = main.BotPlayer(name="Haug", faction="menschlich", aggression=0.5, trading=0.5)
    haug.doerfer = [main.BotDorf(name="Haugsdorf 1", hauptdorf=True, dimension=1, herkunftswelt=1)]
    for _d in haug.doerfer:                                   # Garnison und Lager des Ziels
        _d.einheiten = {"Krieger": 1}
        _d.vorraete = {"holz": 200.0}
        _d.wall_stufe = 0
        _d.wall_zustand = 100.0
    st.bots = [haug]                                          # diese Partie hat einen Bot
    haug.gunst = 50                                           # Gunst fuer den Pakt
    haug.vertraege = {"nichtangriff": {"seit": 0.0, "bis": 3 * TAG}}   # laufender Pakt (drei Spieltage)
    dorf = haug.doerfer[0]

    def _angreifen() -> bool:
        """EINEN Angriff ueber den EINEN Auftragsweg absenden (ohne Marsch zu Ende zu fahren)."""
        return app._angriff_auftrag_starten(
            str(dorf.name), dict(haug.army or {}), wall_stufe=0, wall_zustand=100.0,
            vorrat_ziel=haug, entfernung=2.0, truppen=dict(ort.einheiten),
            dorf_name=str(dorf.name))

    ok_k = _angreifen()                                       # der Spieler sendet den Angriff ab
    check("der Angriff wird NICHT verboten", ok_k is True, str(ok_k))
    check("der Pakt ist nach dem Absenden gebrochen", "nichtangriff" not in haug.vertraege,
          str(sorted(haug.vertraege)))
    check("die Gunst ist um 20 gefallen", int(haug.gunst) == 30, str(haug.gunst))
    pakt_texte = [m for m in st.messages if m.get("type") == "diplomatie"]
    check("genau EINE Meldung zum Paktbruch", len(pakt_texte) == 1, str(len(pakt_texte)))
    check("die Meldung nennt Bot und Bruch",
          bool(pakt_texte) and "Pakt mit Haug gebrochen" in str(pakt_texte[0].get("text")),
          str(pakt_texte[0].get("text")) if pakt_texte else "keine")
    ort.einheiten = {"Krieger": 5}                            # Nachschub: das Heer ist beim Marsch
    ok_k2 = _angreifen()                                      # zweiter Angriff ohne Pakt
    check("der zweite Angriff startet ebenfalls (kein Verbot)", ok_k2 is True, str(ok_k2))
    check("dabei entsteht KEIN zweiter Paktbruch",
          len([m for m in st.messages if m.get("type") == "diplomatie"]) == 1,
          str(len([m for m in st.messages if m.get("type") == "diplomatie"])))
finally:
    if app is not None and getattr(app, "root", None) is not None:
        pass                                                  # nichts schliessen, was nicht offen ist
    if root is not None:                                      # Fenster wieder abraeumen
        try:
            root.destroy()                                    # Zerstoeren gibt die Ressourcen frei
        except Exception:                                     # bereits zerstoert
            pass                                              # dann nichts weiter tun

sys.exit(bericht())
