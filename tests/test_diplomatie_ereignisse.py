# -*- coding: ascii -*-
"""S4-5: Ereignisse Haug, Grom, Silra (06.11.2026, Register 288, docs/ABLAUF_LLM_20261106.md Schritt 5).

Geprueft wird, was der Schnitt zusagt:
  A. Alle Zahlen kommen aus `data/diplomatie.json` (A-7), alle Texte aus `data/story.json`.
  B. Ablauf nach 172.800 s kostet 5 Gunst; bei 172.799 s ist das Ereignis noch offen.
  C. Annahme mit 989 Holz wird abgelehnt - Bestand, Gunst und Ereignis bleiben unveraendert.
  D. Annahme mit 990 Holz bucht GENAU 990 am Ort, Gunst +5, Ereignis weg, Kontakt gebucht.
  E. Silra: der Preis ist ein Zehntel des Gold-Tagesertrags, mindestens 1 (5 -> 1, 128 -> 12).
  F. Grom: 5 Messer gegen 20 Erz (Rohstoff metall); ohne Messer wird NICHTS gebucht.
  G. Anzeige und Kern lesen dieselbe Preisfunktion (Quellwache, Muster F-04).
  H. Hoechstens ein offenes Ereignis je Bot, Haeufigkeit 3 Spieltage, Art rotiert (kein Wuerfel).
  I. Ein alter Spielstand ohne `ereignisse` laedt leer; ein neuer traegt die Liste.
  J. Echter Verlauf: der Bot-Takt legt ein Ereignis an, die App nimmt es an und bucht am Ort.

ASCII-only (Pruefdatei-Konvention).
"""
from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b
# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.
PRUEF_ART = "fenster"
PRUEF_STUFE = 2
PRUEF_BETRIFFT = ['diplomatie', 'main:*', 'story', 'wirtschaft', 'zeitbasis']
PRUEF_DATEN = ['diplomatie.json', 'story.json']
# --- Ende Pruefstand-Kopf -------------------------------------------------------

import ast
import inspect
import json
import os
import sys
import tempfile
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src

import_src()
import diplomatie as D
import main
import story
import wirtschaft
import zeitbasis

TAG = float(zeitbasis.SEKUNDEN_JE_TAG)   # ein Spieltag in Spielsekunden (R3-1: die EINE Quelle)
FRIST = 2 * TAG      # zwei Spieltage - Frist eines Ereignisses
HAEUFIG = 3 * TAG    # drei Spieltage - Abstand zweier Ereignisse desselben Bots


def _code(funktion) -> str:
    """Quelltext einer Funktion ohne Docstring (Docstrings zaehlen nicht als Code)."""
    baum = ast.parse(textwrap.dedent(inspect.getsource(funktion)))  # Funktion in einen Baum wandeln
    kopf = baum.body[0]  # der FunctionDef-Knoten
    if kopf.body and isinstance(kopf.body[0], ast.Expr) and isinstance(kopf.body[0].value, ast.Constant):
        kopf.body = kopf.body[1:]  # fuehrenden Docstring abschneiden
    return ast.unparse(baum)  # Rest als Text


def _bot(name="Haug", gunst=50, ged=None) -> dict:
    """Ein Bot in dict-Form mit Gedaechtnis - so, wie der Kern ihn fuehrt."""
    return {"name": name, "gunst": gunst, "gedaechtnis": dict(ged or {}), "vertraege": {}}


def _ort(holz=0.0, gold=0.0, waren=None) -> dict:
    """Ein Ort in dict-Form mit beiden Lagern (Rohstoffe und Werkstattwaren)."""
    return {"vorraete": {"holz": float(holz), "gold": float(gold)},
            "waren": {str(k): int(v) for k, v in (waren or {}).items()}}


def _gold_pro_tag(wert):
    """Setzt den Goldertrag eines Ortes auf einen festen TAGESWERT - gibt die alte Funktion zurueck."""
    alt = wirtschaft.siedlung_ertrag  # echte Funktion merken
    wirtschaft.siedlung_ertrag = lambda siedlung, forschung_level=None: {
        "gold": float(wert) / 24.0}  # Stundenwert, damit der Tag genau `wert` ergibt
    return alt


abschnitt("A. Zahlen aus der Datendatei, Texte aus der Story (A-7)")
datei = D.daten()
block = datei.get("ereignisse") or {}
check("Schalter ereignisse_aktiv ist gesetzt", D.ereignisse_aktiv(datei) is True,
      str(block.get("aktiv")))
check("Frist ist 172.800 s (zwei Spieltage)", D.ereignis_frist(datei) == FRIST,
      str(D.ereignis_frist(datei)))
check("Haeufigkeit ist 259.200 s (drei Spieltage)", D.ereignis_haeufigkeit(datei) == HAEUFIG,
      str(D.ereignis_haeufigkeit(datei)))
check("Annahme kostet +5 Gunst", D.ereignis_gunst_annahme(datei) == 5,
      str(D.ereignis_gunst_annahme(datei)))
check("Ablehnung/Ablauf kostet -5 Gunst", D.ereignis_gunst_ablehnung(datei) == -5,
      str(D.ereignis_gunst_ablehnung(datei)))
check("drei Arten stehen in der Datei (haug, grom, silra)",
      D.ereignis_arten(datei) == ["haug", "grom", "silra"], str(D.ereignis_arten(datei)))
check("Haug bietet ZWEI Zahlungswege (Holz ODER Gold)",
      len(D.ereignis_preis("haug", _ort())) == 2, str(len(D.ereignis_preis("haug", _ort()))))
check("Haugs Preis ist 990 Holz oder 64 Gold",
      D.ereignis_preis_text("haug", _ort()) == "990 Holz oder 64 Gold",
      D.ereignis_preis_text("haug", _ort()))
check("Grom gibt 20 Erz (Rohstoff metall)",
      D.ereignis_gegenleistung("grom")["rohstoffe"] == {"metall": 20.0},
      str(D.ereignis_gegenleistung("grom")))
eigene = {"ereignisse": {"aktiv": True, "frist_sekunden": 100, "haeufigkeit_sekunden": 200,
                         "gunst_annahme": 7, "gunst_ablehnung": -2,
                         "arten": {"haug": {"zahlungen": [{"rohstoffe": {"holz": 5}}]}}}}
check("geaenderte Frist in den Daten aendert das Urteil",
      D.ereignis_frist(eigene) == 100.0 and D.ereignis_gunst_annahme(eigene) == 7,
      str(D.ereignis_frist(eigene)))
check("der Schalter der Datei gilt", D.ereignisse_aktiv({"ereignisse": {"aktiv": False}}) is False,
      "aus")
check("diplomatie.py bleibt ASCII", all(ord(c) < 128 for c in open(os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src", "diplomatie.py"),
    encoding="utf-8").read()), "ASCII")
check("Titel und Texte stehen in data/story.json",
      bool(story.ereignis_text("haug", "titel")) and bool(story.ereignis_text("grom", "text"))
      and bool(story.ereignis_text("silra", "ablehnung")), story.ereignis_text("haug", "titel"))
check("ein Grund-Satz kommt aus der Datei", bool(story.ereignis_grund_text("bestand_fehlt")),
      story.ereignis_grund_text("bestand_fehlt"))
check("unbekannte Art liefert keinen erfundenen Text", story.ereignis_text("gibtsnicht") == "",
      repr(story.ereignis_text("gibtsnicht")))

abschnitt("B. Ablauf: bei 172.799 s offen, bei 172.800 s verfallen (Gunst -5)")
bot_b = _bot()
daten_b = []
neu_b = D.ereignis_erzeugen(daten_b, bot_b, "haug", HAEUFIG)  # Abstand ist erfuellt
check("das Ereignis ist entstanden", bool(neu_b) and len(daten_b) == 1, str(neu_b))
check("die Frist steht im Eintrag", float(neu_b.get("frist")) == HAEUFIG + FRIST,
      str(neu_b.get("frist")))
verfall_b1 = D.ereignisse_tick(daten_b, HAEUFIG + FRIST - 1, bots=[bot_b])
check("bei 57.599 s ist es noch offen", verfall_b1 == [] and len(daten_b) == 1,
      str(verfall_b1))
check("die Gunst ist bis dahin unveraendert", bot_b["gunst"] == 50, str(bot_b["gunst"]))
verfall_b2 = D.ereignisse_tick(daten_b, HAEUFIG + FRIST, bots=[bot_b])
check("bei 172.800 s verfaellt es", len(verfall_b2) == 1, str(verfall_b2))
check("der Verfall kostet 5 Gunst", bot_b["gunst"] == 45, str(bot_b["gunst"]))
check("die Liste ist danach leer", daten_b == [], str(daten_b))
check("ein zweiter Tick bucht nichts nach",
      D.ereignisse_tick(daten_b, HAEUFIG + FRIST + 10, bots=[bot_b]) == [] and bot_b["gunst"] == 45,
      str(bot_b["gunst"]))

abschnitt("C. Annahme mit 989 Holz wird abgelehnt - nichts gebucht")
bot_c = _bot()
daten_c = []
D.ereignis_erzeugen(daten_c, bot_c, "haug", HAEUFIG)
ort_c = _ort(holz=989, gold=1000)
ok_c, grund_c = D.ereignis_annehmen(daten_c, ort_c, daten_c[0]["id"], bot_c,
                                    jetzt=HAEUFIG + 10, zahlung=0)
check("989 Holz reichen nicht", ok_c is False and grund_c == "bestand_fehlt", str(grund_c))
check("der Bestand am Ort bleibt unveraendert", ort_c["vorraete"]["holz"] == 989.0,
      str(ort_c["vorraete"]["holz"]))
check("auch das Gold bleibt unveraendert", ort_c["vorraete"]["gold"] == 1000.0,
      str(ort_c["vorraete"]["gold"]))
check("die Gunst bleibt unveraendert", bot_c["gunst"] == 50, str(bot_c["gunst"]))
check("das Ereignis bleibt offen", len(daten_c) == 1, str(len(daten_c)))
ok_c2, grund_c2 = D.ereignis_annehmen(daten_c, ort_c, daten_c[0]["id"], bot_c,
                                      jetzt=HAEUFIG + 20)
check("ohne Wunsch nimmt der Kern den ERSTEN bezahlbaren Weg (Gold)",
      ok_c2 is True and grund_c2 == "angenommen" and ort_c["vorraete"]["gold"] == 936.0,
      "%s / Gold %s" % (grund_c2, ort_c["vorraete"]["gold"]))

abschnitt("D. Annahme mit 990 Holz bucht genau 990, Gunst +5")
bot_d = _bot()
daten_d = []
D.ereignis_erzeugen(daten_d, bot_d, "haug", HAEUFIG)
ort_d = _ort(holz=1500)
ok_d, grund_d = D.ereignis_annehmen(daten_d, ort_d, daten_d[0]["id"], bot_d,
                                    jetzt=HAEUFIG + 5, zahlung=0)
check("die Annahme geht durch", ok_d is True and grund_d == "angenommen", str(grund_d))
check("genau 990 Holz sind abgebucht", ort_d["vorraete"]["holz"] == 510.0,
      str(ort_d["vorraete"]["holz"]))
check("das Gold wurde nicht angefasst", ort_d["vorraete"]["gold"] == 0.0,
      str(ort_d["vorraete"]["gold"]))
check("die Gunst steigt um 5", bot_d["gunst"] == 55, str(bot_d["gunst"]))
check("das Ereignis ist erledigt", daten_d == [], str(daten_d))
check("der Kontakt ist gebucht (Daniel 13:50: Kontakt = jede Interaktion)",
      D.letzter_kontakt(bot_d) == HAEUFIG + 5, str(D.letzter_kontakt(bot_d)))
bot_d2 = _bot()
daten_d2 = []
D.ereignis_erzeugen(daten_d2, bot_d2, "haug", HAEUFIG)
check("Ablehnung kostet 5 Gunst",
      D.ereignis_ablehnen(daten_d2, daten_d2[0]["id"], bot_d2, jetzt=HAEUFIG + 5) == (True, "abgelehnt")
      and bot_d2["gunst"] == 45, str(bot_d2["gunst"]))
check("nach der Ablehnung ist das Ereignis weg", daten_d2 == [], str(daten_d2))

abschnitt("E. Silra: ein Zehntel des Gold-Tagesertrags, mindestens 1")
alt_ertrag = _gold_pro_tag(5)  # duerftiger Ort: 5 Gold am Tag
try:
    preis_5 = D.ereignis_preis("silra", _ort())
finally:
    wirtschaft.siedlung_ertrag = alt_ertrag
check("bei 5 Gold am Tag faellt der Preis auf den Mindestwert 1",
      preis_5[0]["rohstoffe"]["gold"] == 1.0, str(preis_5))
alt_ertrag = _gold_pro_tag(128)  # mittleres Dorf laut V-4: 128 Gold am Tag
try:
    preis_128 = D.ereignis_preis("silra", _ort())
finally:
    wirtschaft.siedlung_ertrag = alt_ertrag
check("bei 128 Gold am Tag kostet die Auskunft 12 (V-4, abgerundet)",
      preis_128[0]["rohstoffe"]["gold"] == 12.0, str(preis_128))
bot_e = _bot("Silra")
daten_e = []
D.ereignis_erzeugen(daten_e, bot_e, "silra", HAEUFIG)
ort_e = _ort(gold=12)
_preis_e = D.ereignis_preis("silra", ort_e)  # der Preis, den der Kern gleich fragt
_ok_e, grund_e = D.ereignis_annehmen(daten_e, ort_e, daten_e[0]["id"], bot_e, jetzt=HAEUFIG)
check("mit 12 Gold ist die Auskunft bezahlbar", _ok_e is True, str(grund_e))
check("genau der Preis ist abgebucht",
      ort_e["vorraete"]["gold"] == 12.0 - float(_preis_e[0]["rohstoffe"]["gold"]),
      "%s nach Preis %s" % (ort_e["vorraete"]["gold"], _preis_e[0]["rohstoffe"]["gold"]))

abschnitt("F. Grom: 5 Messer gegen 20 Erz")
bot_f = _bot("Grom")
daten_f = []
D.ereignis_erzeugen(daten_f, bot_f, "grom", HAEUFIG)
ort_f = _ort(waren={"Messer": 5})
ok_f, grund_f = D.ereignis_annehmen(daten_f, ort_f, daten_f[0]["id"], bot_f, jetzt=HAEUFIG)
check("der Tausch geht durch", ok_f is True, str(grund_f))
check("die 5 Messer sind weg", int(ort_f["waren"].get("Messer") or 0) == 0,
      str(ort_f["waren"].get("Messer")))
check("20 Erz liegen im Rohstofflager", ort_f["vorraete"].get("metall") == 20.0,
      str(ort_f["vorraete"].get("metall")))
bot_f2 = _bot("Grom")
daten_f2 = []
D.ereignis_erzeugen(daten_f2, bot_f2, "grom", HAEUFIG)
ort_f2 = _ort(waren={"Messer": 4})
ok_f2, grund_f2 = D.ereignis_annehmen(daten_f2, ort_f2, daten_f2[0]["id"], bot_f2, jetzt=HAEUFIG)
check("4 Messer reichen nicht", ok_f2 is False and grund_f2 == "bestand_fehlt", str(grund_f2))
check("ohne Tausch liegt kein Erz im Lager", not ort_f2["vorraete"].get("metall"),
      str(ort_f2["vorraete"].get("metall")))
check("die 4 Messer bleiben liegen", ort_f2["waren"].get("Messer") == 4,
      str(ort_f2["waren"].get("Messer")))

abschnitt("G. Anzeige und Kern lesen dieselbe Preisfunktion (F-04)")
quelle_overlay = _code(main.NebelseetalApp._ereignis_overlay)
quelle_anzeige = _code(main.NebelseetalApp._ereignisse_anzeigen)
quelle_kern = _code(D.ereignis_annehmen)
check("der Ingame-Dialog fragt diplomatie.ereignis_preis",
      "diplomatie.ereignis_preis(" in quelle_overlay, "Aufruf vorhanden")
check("die Diplomatie-Ansicht fragt diplomatie.ereignis_preis",
      "diplomatie.ereignis_preis(" in quelle_anzeige, "Aufruf vorhanden")
check("der Kern fragt dieselbe Funktion", "ereignis_preis(" in quelle_kern, "Aufruf vorhanden")
check("keine zweite Preisrechnung im Dialog",
      "0.1" not in quelle_overlay and "/ 10" not in quelle_overlay, "keine eigene Formel")
check("preis_text rechnet ueber die Preisfunktion", "ereignis_preis(" in _code(D.ereignis_preis_text),
      "Aufruf vorhanden")
check("die Anzeige bucht nichts selbst",
      "diplomatie.ereignis_annehmen(" not in quelle_anzeige
      and "diplomatie.ereignis_ablehnen(" not in quelle_anzeige, "nur Knoepfe")
check("die App bucht ueber den Kern",
      "diplomatie.ereignis_annehmen(" in _code(main.NebelseetalApp._ereignis_annehmen)
      and "diplomatie.ereignis_ablehnen(" in _code(main.NebelseetalApp._ereignis_ablehnen),
      "Aufrufe vorhanden")

abschnitt("H. Ein offenes je Bot, Haeufigkeit, Rotation")
bot_h = _bot()
daten_h = []
erst = D.ereignis_erzeugen(daten_h, bot_h, "haug", HAEUFIG)
zweit = D.ereignis_erzeugen(daten_h, bot_h, "haug", HAEUFIG + 10)
check("kein zweites offenes Ereignis je Bot", not zweit and len(daten_h) == 1,
      str(len(daten_h)))
D.ereignis_ablehnen(daten_h, erst["id"], bot_h, jetzt=HAEUFIG + 20)
zu_frueh = D.ereignis_erzeugen(daten_h, bot_h, "haug", HAEUFIG + HAEUFIG - 1)
check("vor Ablauf der Haeufigkeit kommt kein neues", not zu_frueh, str(zu_frueh))
wieder = D.ereignis_erzeugen(daten_h, bot_h, "haug", HAEUFIG + HAEUFIG)
check("nach drei Spieltagen kommt wieder eines", bool(wieder), str(wieder))
frueh = D.ereignis_erzeugen([], _bot(), "haug", TAG)
check("auch das ERSTE Ereignis wartet die Haeufigkeit ab", not frueh, str(frueh))
quelle_takt = _code(main.GameState.bots_fortschreiben)
check("der Bot-Takt legt Ereignisse an", "diplomatie.ereignis_erzeugen(" in quelle_takt,
      "Aufruf vorhanden")
check("der Bot-Takt laesst sie verfallen", "diplomatie.ereignisse_tick(" in quelle_takt,
      "Aufruf vorhanden")
# R3-2 (07.11.2026, Befund I-1): die alte Zusage "die Art rotiert ueber die Dateireihenfolge" ist
# UMGEDREHT - die Rotation ueber den BOT-INDEX war der Fehler ("Bryndhild: Grom braucht Messer").
# Die Art haengt jetzt am NAMEN; die vollstaendige Pruefung steht in tests/test_ereignis_zuordnung.py.
check("die Art kommt NICHT mehr aus der Index-Rotation (I-1)",
      "% len(_arten)" not in quelle_takt
      and "diplomatie.ereignis_art_fuer_bot(" in quelle_takt,
      "Zuordnung ueber den Botnamen")
check("der Takt meldet neue Ereignisse ins Postfach", "'type': 'ereignis'" in quelle_takt,
      "Meldung vorhanden")
check("der Dialog oeffnet hoechstens einen und nie ueber einem offenen",
      "self._overlay_offen()" in _code(main.NebelseetalApp._ereignis_overlay_pruefen),
      "Gate vorhanden")

abschnitt("I. Alter Spielstand ohne ereignisse laedt leer")
st = main.GameState()
pfad = os.path.join(tempfile.gettempdir(), "nebel_test_s45_save.json")
st.save(pfad)
roh = json.load(open(pfad, encoding="utf-8"))
check("der Spielstand traegt das Feld ereignisse", "ereignisse" in roh, str(len(roh)))
roh.pop("ereignisse")  # ein Stand von vor S4-5
json.dump(roh, open(pfad, "w", encoding="utf-8"), ensure_ascii=False)
st_alt = main.GameState()
geladen = st_alt.load(pfad)
check("der alte Stand laedt ohne Fehler", geladen is True, str(geladen))
check("ohne Feld beginnt die Liste leer", st_alt.ereignisse == [], str(st_alt.ereignisse))
st_alt.ereignisse = [{"id": "haug-1-0", "art": "haug", "bot": "Haug",
                      "erzeugt": 0.0, "frist": FRIST}]
st_alt.save(pfad)
st_neu = main.GameState()
st_neu.load(pfad)
check("ein neuer Stand traegt das offene Ereignis wieder",
      len(st_neu.ereignisse) == 1 and st_neu.ereignisse[0].get("art") == "haug",
      str(st_neu.ereignisse))
os.remove(pfad)

abschnitt("J. Echter Verlauf: Takt legt an, App nimmt an, Ort ist gebucht")
root = None
app = None
try:
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    app = main.NebelseetalApp(root)
    app._build_main_ui()
    st_app = app.state
    app._erste_siedlung_gruenden()
    haug = main.BotPlayer(name="Haug", faction="menschlich", aggression=0.5, trading=0.5)
    haug.doerfer = [main.BotDorf(name="Haugsdorf 1", hauptdorf=True, dimension=1, herkunftswelt=1)]
    haug.doerfer[0].vorraete = {"holz": 500.0, "stein": 500.0, "nahrung": 500.0}
    haug.doerfer[0].wall_stufe = 0
    haug.doerfer[0].wall_zustand = 100.0
    st_app.bots = [haug]
    st_app.noob_protection = True                       # kein Bot-Angriff in dieser Probe
    st_app.ereignisse = []
    st_app._letzter_bot_takt = 0.0
    st_app.bots_fortschreiben(HAEUFIG)                  # erster Takt nach drei Spieltagen
    check("der Takt hat ein Ereignis angelegt", len(st_app.ereignisse) == 1,
          str(st_app.ereignisse))
    check("die Meldung steht im Postfach",
          any(m.get("type") == "ereignis" for m in st_app.messages), "Meldung vorhanden")
    eintrag = st_app.ereignisse[0]
    ort_app = st_app.aktive_siedlung()
    ort_app.vorraete["holz"] = 2000.0                   # genug fuer Weg 0 (990 Holz)
    _art_app = str(eintrag.get("art") or "")
    _holz_vorher = float(ort_app.vorraete.get("holz") or 0.0)
    ok_app = app._ereignis_annehmen(eintrag, 0)
    check("die App nimmt das Ereignis an", ok_app is True, str(ok_app))
    check("das Ereignis ist danach weg", st_app.ereignisse == [], str(st_app.ereignisse))
    _preis = D.ereignis_preis(_art_app, ort_app, None)[0]["rohstoffe"]
    _holz_weg = _holz_vorher - float(ort_app.vorraete.get("holz") or 0.0)
    check("am Ort ist genau der Preis abgebucht", _holz_weg == float(_preis.get("holz") or 0.0),
          "weg %s, Preis %s" % (_holz_weg, _preis))
    check("die Gunst des Bots ist gestiegen", haug.gunst > 50, str(haug.gunst))
    check("der Satz aus der Datei steht im Postfach",
          any(story.ereignis_text(_art_app, "annahme") == m.get("text")
              for m in st_app.messages), "Satz gefunden")
finally:
    if root is not None:
        try:
            root.destroy()
        except Exception:
            pass

sys.exit(bericht())
