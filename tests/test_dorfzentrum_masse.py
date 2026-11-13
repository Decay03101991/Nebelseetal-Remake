# -*- coding: ascii -*-
"""Wache: die Masse des Dorfzentrums stehen an EINER Stelle (Nr. 16, Teil A).

Daniels Entscheidungen F-56, F-58, F-59, F-65 und F-66 (Register 550/568) legen das Dorfzentrum
in Zahlen fest. Bis V_0.0.4 standen diese Zahlen verstreut in `main.py`; jetzt rechnet
`src/dorfzentrum.py` sie, und diese Datei rechnet dieselben Zahlen OHNE Fenster nach.

WAS DIESE DATEI PRUEFT
----------------------
1. FALL 1 (1037 x 589, k = 1): alle 20 Zeilen der Masstabelle aus Nr. 16, A1 - von S = 432 bis
   zur Werkstatt-Namensspalte 244. Die Sollwerte stehen von HAND hier, nicht aus dem Modul.
2. FALL 2 (1127 x 764, k = 1,2512, Rollbalken 21): S = 448, R = 658, Kopf 74, Reiterleiste 42,
   Inhaltshoehe 702, Lager 548, Einheiten 478, Werkstaetten 574, Spalten 228 / 125 / 150 / 105.
3. Die sieben Bloecke der Spalte (F-59): 74 / 57 / 55 / 100 / 370 / 58, Summe mit fuenf Luecken
   = 764. Block 5 ist der REST - mit Technikblock wird er 305, die anderen Bloecke bleiben.
4. BEFUND B1: `tkopf` ist ein PARAMETER, kein gerechneter Wert. Mit 30 (Fall 2) gilt 478 / 574,
   mit dem gemessenen 33 gilt 481 / 577 - beides bleibt unter der Inhaltshoehe 702.
5. Zeilenhoehen: `ls` ist ein Parameter. Der Startwert `round(18k)` ergaebe 23 statt der
   gemessenen 22 und damit zu hohe Tabellen - darum wird das hier ausdruecklich gezeigt.
6. F-58 und F-65: Werkstatt-Tabelle mit Zutat-Spalte, Einheitentabelle OHNE Spalte Verwundete
   (Namensspalte 244).
7. Texte: Kennzahl (F-66), Zutat "Metall 12 / 4 mit Haken", Zustand, Zahlen mit Punkt, Kleintext
   absolut 15 px (F-56), Reiter-Treffer.
8. QUELLTEXT: kein Tk, kein Zeichnen - das Modul rechnet nur.

Aufruf: python -X utf8 tests/test_dorfzentrum_masse.py
"""
from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py.
PRUEF_ART = "rechnen"
PRUEF_STUFE = 1
PRUEF_BETRIFFT = ['dorfzentrum']
PRUEF_DATEN = []
# --- Ende Pruefstand-Kopf -------------------------------------------------------

import ast
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src, messwert  # noqa: E402

ROOT, SRC = import_src()
import dorfzentrum  # noqa: E402

# Die gemessenen Zeilenhoehen aus Nr. 16, A1 (Fall 1 aus Tk-Messung mit Liberation Sans,
# Fall 2 aus den Tk-Messungen des DPI-bewussten Prozesses).
LS1 = {"text": 15, "zw": 18, "zahl": 18, "titel": 24}
LS2 = {"text": 19, "zw": 22, "zahl": 22, "titel": 30}
F1 = dorfzentrum.masse(1037, 589, k=1.0, rollbalken=17, tkopf=24, ls=LS1)
F2 = dorfzentrum.masse(1127, 764, k=1.2512, rollbalken=21, tkopf=30, ls=LS2)


# --------------------------------------------------------------------------------------
abschnitt("1. Fall 1 (1037 x 589, k = 1, Rollbalken 17)")
# Sollwerte von Hand aus Nr. 16, A1 und der Nachrechnung (NACHRECHNUNG_NR16.md).
for name, soll, ist in (
        ("p", 8, F1["p"]), ("g", 6, F1["g"]), ("S_min", 316, F1["s_min"]),
        ("Feld f", 57, F1["feld"]), ("Karte R", 588, F1["karte"]), ("Spalte S", 432, F1["spalte"]),
        ("Textbreite der Spalte", 416, F1["textbreite"]), ("Kopf", 59, F1["kopf"]),
        ("Reiterleiste", 34, F1["reiterleiste"]), ("Inhaltshoehe", 539, F1["innenhoehe"]),
        ("Reiterbreite", 190, F1["reiterbreite"]),
        ("Kachelbreite", 185, F1["lager"]["kachel_breite"]),
        ("Kachelhoehe", 72, F1["lager"]["kachel_hoehe"]),
        ("Kachel-Textbreite", 99, F1["lager"]["textbreite"]),
        ("Lagerhoehe (6 Reihen)", 472, F1["lager"]["hoehe"]),
        ("Einheiten-Zeile z", 26, F1["einheiten"]["zeile"]),
        ("Einheiten-Hoehe", 388, F1["einheiten"]["hoehe"]),
        ("Einheiten-Haelfte", 282, F1["einheiten"]["haelfte"]),
        ("Einheiten-Namensspalte (ohne Verwundete)", 226, F1["einheiten"]["namensspalte"]),
        ("Werkstatt-Name", 244, F1["werkstaetten"]["name"]),
        ("Werkstatt-Hoehe (17 Zeilen)", 466, F1["werkstaetten"]["hoehe"])):
    check("Fall 1: %s = %s" % (name, soll), ist == soll, "gemessen %s" % ist)

check("Fall 1: 432 + 17 + 588 = 1037 (Spalte + Rollbalken + Karte)",
      F1["spalte"] + 17 + F1["karte"] == 1037,
      "%d + 17 + %d" % (F1["spalte"], F1["karte"]))
check("Fall 1: das Lager passt ohne Rollen (472 <= 539)", F1["lager"]["hoehe"] <= F1["innenhoehe"],
      "%d <= %d" % (F1["lager"]["hoehe"], F1["innenhoehe"]))
check("Fall 1: die Einheiten passen ohne Rollen (388 <= 539)",
      F1["einheiten"]["hoehe"] <= F1["innenhoehe"],
      "%d <= %d" % (F1["einheiten"]["hoehe"], F1["innenhoehe"]))
check("Fall 1: die Werkstaetten passen ohne Rollen (466 <= 539)",
      F1["werkstaetten"]["hoehe"] <= F1["innenhoehe"],
      "%d <= %d" % (F1["werkstaetten"]["hoehe"], F1["innenhoehe"]))
check("Fall 1: die Werkstattspalten sind 100 / 120 / 84",
      (F1["werkstaetten"]["werkstatt"], F1["werkstaetten"]["zutat"],
       F1["werkstaetten"]["zustand"]) == (100, 120, 84),
      str((F1["werkstaetten"]["werkstatt"], F1["werkstaetten"]["zutat"],
           F1["werkstaetten"]["zustand"])))

# --------------------------------------------------------------------------------------
abschnitt("2. Fall 2 (1127 x 764, k = 1,2512, Rollbalken 21)")
for name, soll, ist in (
        ("p", 10, F2["p"]), ("g", 8, F2["g"]), ("S_min", 395, F2["s_min"]),
        ("Feld f", 64, F2["feld"]), ("Karte R", 658, F2["karte"]), ("Spalte S", 448, F2["spalte"]),
        ("Textbreite der Spalte", 428, F2["textbreite"]), ("Kopf", 74, F2["kopf"]),
        ("Reiterleiste", 42, F2["reiterleiste"]), ("Inhaltshoehe", 702, F2["innenhoehe"]),
        ("Reiterbreite", 212, F2["reiterbreite"]),
        ("Kachelbreite", 206, F2["lager"]["kachel_breite"]),
        ("Kachelhoehe", 83, F2["lager"]["kachel_hoehe"]),
        ("Kachel-Textbreite", 118, F2["lager"]["textbreite"]),
        ("Kachel-Textblock", 63, F2["lager"]["textblock"]),
        ("Lagerhoehe (6 Reihen)", 548, F2["lager"]["hoehe"]),
        ("Einheiten-Zeile z", 32, F2["einheiten"]["zeile"]),
        ("Einheiten-Hoehe", 478, F2["einheiten"]["hoehe"]),
        ("Einheiten-Haelfte", 314, F2["einheiten"]["haelfte"]),
        ("Einheiten-Zahlspalte", 60, F2["einheiten"]["zahlspalte"]),
        ("Einheiten-Namensspalte (ohne Verwundete)", 244, F2["einheiten"]["namensspalte"]),
        ("Werkstatt-Name", 228, F2["werkstaetten"]["name"]),
        ("Werkstatt-Spalte Werkstatt", 125, F2["werkstaetten"]["werkstatt"]),
        ("Werkstatt-Spalte Zutat", 150, F2["werkstaetten"]["zutat"]),
        ("Werkstatt-Spalte Zustand", 105, F2["werkstaetten"]["zustand"]),
        ("Werkstatt-Hoehe (17 Zeilen)", 574, F2["werkstaetten"]["hoehe"])):
    check("Fall 2: %s = %s" % (name, soll), ist == soll, "gemessen %s" % ist)

check("Fall 2: 448 + 21 + 658 = 1127 (Spalte + Rollbalken + Karte)",
      F2["spalte"] + 21 + F2["karte"] == 1127,
      "%d + 21 + %d" % (F2["spalte"], F2["karte"]))
check("Fall 2: die drei Bereiche passen ohne Rollen (548 / 478 / 574 <= 702)",
      max(F2["lager"]["hoehe"], F2["einheiten"]["hoehe"],
          F2["werkstaetten"]["hoehe"]) <= F2["innenhoehe"],
      str((F2["lager"]["hoehe"], F2["einheiten"]["hoehe"],
           F2["werkstaetten"]["hoehe"], F2["innenhoehe"])))
check("Fall 2: S = 448 ist DIESELBE Spalte wie in der Siedlungsansicht (F-57)",
      F2["spalte"] == 1127 - 21 - (10 * F2["feld"] + 18), str(F2["spalte"]))
messwert("S Fall 2", F2["spalte"], "px", "gerechnet nach Nr. 16 A1")
messwert("R Fall 2", F2["karte"], "px", "gerechnet nach Nr. 16 A1")

# --------------------------------------------------------------------------------------
abschnitt("3. Die sieben Bloecke der Spalte (F-59: kein Ortsbestand)")
_b = F2["bloecke"]
for name, soll in (("Kopf", 74), ("Naechster Schritt", 57), ("Ort", 55), ("Aktionen", 100),
                   ("Auswahl (Rest)", 370), ("Hinweis", 58)):
    check("Block %s = %d" % (name, soll), _b[name.lower().split()[0]] == soll,
          "gemessen %s" % _b.get(name.lower().split()[0]))
check("Block 5 ist der REST: 764 - 344 - 5 Luecken a 10 = 370",
      764 - (_b["kopf"] + _b["naechster"] + _b["ort"] + _b["aktionen"] + _b["hinweis"])
      - 5 * F2["p"] == 370, str(_b["auswahl"]))
check("Summe der Bloecke + fuenf Luecken fuellt die Hoehe genau",
      _b["kopf"] + _b["naechster"] + _b["ort"] + _b["aktionen"] + _b["auswahl"]
      + _b["hinweis"] + 5 * F2["p"] == 764,
      str(_b["kopf"] + _b["naechster"] + _b["ort"] + _b["aktionen"] + _b["auswahl"]
          + _b["hinweis"] + 5 * F2["p"]))
check("ohne Entwicklerbetrieb gibt es KEINEN Technikblock", _b["technik"] == 0, str(_b["technik"]))
check("kein Block heisst 'ortsbestand' (F-59)", "ortsbestand" not in _b, str(sorted(_b)))
_bt = dorfzentrum.bloecke(764, 1.2512, ls_text=19, ls_titel=30, tkopf=30, technik=True)
check("mit Technikblock: Block 7 = 55", _bt["technik"] == 55, str(_bt["technik"]))
check("mit Technikblock: Block 5 schrumpft auf 305", _bt["auswahl"] == 305, str(_bt["auswahl"]))
check("mit Technikblock bleiben die anderen Bloecke gleich",
      (_bt["kopf"], _bt["naechster"], _bt["ort"], _bt["aktionen"], _bt["hinweis"])
      == (_b["kopf"], _b["naechster"], _b["ort"], _b["aktionen"], _b["hinweis"]), "")

# --------------------------------------------------------------------------------------
abschnitt("4. Befund B1: tkopf wird GEMESSEN, nicht gerechnet")
check("ohne tkopf ist der Wert als Startwert gekennzeichnet",
      dorfzentrum.masse(1127, 764, 1.2512, 21, ls=LS2)["tkopf_gemessen"] is False, "")
check("ohne tkopf gilt der Startwert 30 (aus ls_text 19 + round(9k))",
      dorfzentrum.masse(1127, 764, 1.2512, 21, ls=LS2)["tkopf"] == 30,
      str(dorfzentrum.masse(1127, 764, 1.2512, 21, ls=LS2)["tkopf"]))
check("mit tkopf ist der Wert als gemessen gekennzeichnet",
      F2["tkopf_gemessen"] is True, "")
_f2b = dorfzentrum.masse(1127, 764, 1.2512, 21, tkopf=33, ls=LS2)
check("GEMESSEN 33: Einheiten 481 statt 478", _f2b["einheiten"]["hoehe"] == 481,
      str(_f2b["einheiten"]["hoehe"]))
check("GEMESSEN 33: Werkstaetten 577 statt 574", _f2b["werkstaetten"]["hoehe"] == 577,
      str(_f2b["werkstaetten"]["hoehe"]))
check("auch mit 33 bleibt beides unter der Inhaltshoehe 702",
      max(_f2b["einheiten"]["hoehe"], _f2b["werkstaetten"]["hoehe"]) <= _f2b["innenhoehe"],
      str((_f2b["einheiten"]["hoehe"], _f2b["werkstaetten"]["hoehe"], _f2b["innenhoehe"])))
check("die Bloecke haengen NICHT an tkopf (nur die Tabellen)",
      _f2b["bloecke"]["auswahl"] == _b["auswahl"], "")

# --------------------------------------------------------------------------------------
abschnitt("5. Zeilenhoehen sind ein Parameter, keine Formel")
_start = dorfzentrum.masse(1127, 764, 1.2512, 21)          # ohne ls: Startwert
check("Startwert ohne Messung: round(18 x 1,2512) = 23 statt der gemessenen 22",
      _start["ls_zw"] == 23, str(_start["ls_zw"]))
check("GEGENPROBE: mit dem Startwert waere die Reiterleiste 43 statt 42",
      _start["reiterleiste"] == 43, str(_start["reiterleiste"]))
check("GEGENPROBE: mit dem Startwert waeren die Werkstaetten 591 statt 574",
      _start["werkstaetten"]["hoehe"] == 591, str(_start["werkstaetten"]["hoehe"]))
check("die gemessenen Zeilenhoehen ergeben Teil A (19 / 22 / 30)",
      (F2["ls_text"], F2["ls_zw"], F2["ls_titel"]) == (19, 22, 30),
      str((F2["ls_text"], F2["ls_zw"], F2["ls_titel"])))
check("fehlt nur 'zahl', gilt der Wert von 'zw'",
      dorfzentrum.masse(1127, 764, 1.2512, 21, ls={"text": 19, "zw": 22, "titel": 30}
                        )["einheiten"]["zeile"] == 32, "")

# --------------------------------------------------------------------------------------
abschnitt("6. Gegenproben zur Flaeche")
_rb0 = dorfzentrum.masse(1127, 764, 1.2512, 0, tkopf=30, ls=LS2)
check("Rollbalken 0: die Spalte waechst auf 469", _rb0["spalte"] == 469, str(_rb0["spalte"]))
check("Rollbalken 0: die Karte bleibt 658", _rb0["karte"] == 658, str(_rb0["karte"]))
_klein = dorfzentrum.masse(900, 600, 1.0, 17, ls=LS1)
check("kleines Fenster: das Feld faellt unter 64", _klein["feld"] < 64, str(_klein["feld"]))
check("kleines Fenster: die Spalte bleibt positiv", _klein["spalte"] > 0, str(_klein["spalte"]))
_gross = dorfzentrum.masse(1920, 1200, 1.2512, 21, tkopf=30, ls=LS2)
check("grosses Fenster: das Feld bleibt bei 64 gedeckelt", _gross["feld"] == 64,
      str(_gross["feld"]))
check("grosses Fenster: die Spalte wird breiter als 448", _gross["spalte"] > 448,
      str(_gross["spalte"]))
_vier = dorfzentrum.lager_masse(658, 1.2512, LS2, waren=19)
check("19 Waren ergeben 7 Reihen statt 6 (keine Ware faellt still heraus)",
      _vier["reihen"] == 7, str(_vier["reihen"]))
_sechs = dorfzentrum.lager_masse(658, 1.2512, LS2, waren=17)
check("17 Waren ergeben 6 Reihen", _sechs["reihen"] == 6, str(_sechs["reihen"]))
_achtzehn = dorfzentrum.werkstaetten_masse(658, 1.2512, 30, LS2, zeilen=18)
check("18 Rezepte ergeben eine Zeile mehr (574 + 32 = 606)", _achtzehn["hoehe"] == 606,
      str(_achtzehn["hoehe"]))

# --------------------------------------------------------------------------------------
abschnitt("7. Texte - die Ansicht formatiert nur (F-66, F-58, F-65)")
check("Kennzahl im Kopf nennt BEIDE Zahlen (F-66)",
      dorfzentrum.kennzahlen_text({"vorraetig": 3, "waren_gesamt": 17,
                                   "herstellbar": 5}) == "3 von 17 vorr\u00e4tig"
      " \u00b7 5 von 17 herstellbar",
      dorfzentrum.kennzahlen_text({"vorraetig": 3, "waren_gesamt": 17, "herstellbar": 5}))
check("Kennzahl mit Nullen bleibt stehen",
      dorfzentrum.kennzahlen_text({"vorraetig": 0, "waren_gesamt": 17, "herstellbar": 0})
      == "0 von 17 vorr\u00e4tig \u00b7 0 von 17 herstellbar", "")
check("fehlende Schluessel erfinden keine Zahl",
      dorfzentrum.kennzahlen_text({"vorraetig": 2}) == "", "")
check("ohne Kennzahlen kein Text", dorfzentrum.kennzahlen_text({}) == "", "")
check("Zutat mit genug Bestand: vorhanden / noetig mit Haken",
      dorfzentrum.zutat_text("Metall", 12, 4) == "Metall 12 / 4 \u2713",
      dorfzentrum.zutat_text("Metall", 12, 4))
check("Zutat ohne Bestand: Kreuz", dorfzentrum.zutat_text("Metall", 0, 4) == "Metall 0 / 4 \u2715",
      dorfzentrum.zutat_text("Metall", 0, 4))
check("genau genug zaehlt als vorhanden (4 / 4 mit Haken)",
      dorfzentrum.zutat_text("Holz", 4, 4).endswith("\u2713"), dorfzentrum.zutat_text("Holz", 4, 4))
check("Zustand herstellbar", dorfzentrum.zustand_text(True) == "\u2713 herstellbar", "")
check("Zustand fehlt", dorfzentrum.zustand_text(False) == "\u2715 fehlt", "")
check("grosse Zahl mit Punkt", dorfzentrum.zahl_text(12345) == "12.345",
      dorfzentrum.zahl_text(12345))
check("keine sinnlose Nachkommastelle", dorfzentrum.zahl_text(1334.0) == "1334",
      dorfzentrum.zahl_text(1334.0))
check("echte Nachkommastelle bleibt", dorfzentrum.zahl_text(2.5) == "2.5",
      dorfzentrum.zahl_text(2.5))

_breiten = {"Paladinharnisch": 104, "Belagerungsturm": 162}


def _messen(text, px):
    """Stellvertreter fuer `font.measure` mit den GEMESSENEN Breiten aus Register 548."""
    assert px == 15, "F-56: Kleintext ist absolut 15 px, nicht %r" % (px,)
    return _breiten.get(text, 50)


check("F-56: 'Paladinharnisch' 104 passt in 118 (KEIN Kleintext)",
      dorfzentrum.kleintext_zu_breit("Paladinharnisch", 118, _messen) is False, "")
check("F-56: mit schrift(15) waeren es 128 px - zu breit (Gegenprobe)",
      dorfzentrum.kleintext_zu_breit("Paladinharnisch", 118,
                                     lambda t, px: 128) is True, "")
check("F-56: 'Belagerungsturm' 162 passt in 244 (Namensspalte ohne Verwundete)",
      dorfzentrum.kleintext_zu_breit("Belagerungsturm", 244, _messen) is False, "")
check("F-56: ohne Messfunktion ist die Frage NICHT beantwortet (False, kein 'passt')",
      dorfzentrum.kleintext_zu_breit("Irgendetwas", 10, None) is False, "")
check("die Kleintextgroesse steht als Konstante 15 im Modul",
      dorfzentrum.KLEINTEXT_PX == 15, str(dorfzentrum.KLEINTEXT_PX))

# --------------------------------------------------------------------------------------
abschnitt("8. Reiter (drei Bereiche, nur anklicken)")
check("die Reihenfolge ist Lager, Werkstaetten, Einheiten",
      dorfzentrum.REITER == ("Lager", "Werkst\u00e4tten", "Einheiten"),
      str(dorfzentrum.REITER))
for x, soll in ((5, -1), (30, 0), (200, 0), (250, 1), (450, 2), (660, -1)):
    check("Klick bei x = %d waehlt Reiter %d" % (x, soll),
          dorfzentrum.reiter_treffer(x, 212, 10) == soll,
          str(dorfzentrum.reiter_treffer(x, 212, 10)))
check("die drei Reiter decken die Leiste (3 x 212 + 2 x 10 = 656 <= 658)",
      3 * F2["reiterbreite"] + 2 * F2["p"] <= F2["karte"],
      str(3 * F2["reiterbreite"] + 2 * F2["p"]))

# --------------------------------------------------------------------------------------
abschnitt("9. Quelltext: das Modul rechnet nur")
_pfad = os.path.join(SRC, "dorfzentrum.py")
with open(_pfad, "r", encoding="utf-8") as _f:
    _quelle = _f.read()
check("das Modul importiert kein tkinter",
      "import tkinter" not in _quelle and "\ntk." not in _quelle, "")
_baum = ast.parse(_quelle)
_modulnamen = set()
for _knoten in ast.walk(_baum):
    if isinstance(_knoten, ast.Import):
        _modulnamen.update(a.name for a in _knoten.names)
    elif isinstance(_knoten, ast.ImportFrom):
        _modulnamen.add(_knoten.module or "")
check("das Modul importiert ausser typing nichts",
      _modulnamen <= {"typing", "__future__"}, str(sorted(_modulnamen)))
check("die Formel steht EINMAL im Modul (p = round(8k))",
      _quelle.count("P_FAKTOR * k") == 1, str(_quelle.count("P_FAKTOR * k")))
_zahlen = {k.value for k in ast.walk(_baum)
           if isinstance(k, ast.Constant) and isinstance(k.value, int)}
check("S = 448 und R = 658 stehen NICHT als Zahl im Code (nur in Dokstring/Pruefung)",
      not ({448, 658} & _zahlen), str(sorted({448, 658} & _zahlen)))
check("das Modul enthaelt keinen Zeichenaufruf (create_, pack, grid)",
      not any(w in _quelle for w in ("create_text", "create_rectangle", ".pack(", ".grid(")), "")

# --------------------------------------------------------------------------------------
messwert("Kopf Fall 2", F2["kopf"], "px", "gerechnet nach Nr. 16 A1")
messwert("Inhaltshoehe Fall 2", F2["innenhoehe"], "px", "gerechnet nach Nr. 16 A1")
messwert("Block 5 Fall 2", F2["bloecke"]["auswahl"], "px", "Rest der Spalte")
befund("Die Knopfhoehen h_b 35 / h_b1 37 sind im Fall 2 gemessen, im Fall 1 UNBEKANNT",
       "Sie sind STARTWERTE: die Ansicht setzt den Knopf und nimmt seine echte Hoehe in Kauf "
       "(Block 2 bis 4 wachsen dann mit), Block 5 bekommt ohnehin den gemessenen REST "
       "(`_dz_rest_verteilen`). Die Sollzahlen 57 / 55 / 100 gelten also nur bei den "
       "gemessenen Fall-2-Hoehen - im Fall 1 weicht der eine oder andere Block ein paar px ab, "
       "ohne dass die Spalte rollt. Wer die Sollzahlen fuer Fall 1 braucht, misst die Knoepfe "
       "im unbewussten Prozess und traegt sie als Startwerte ein.")
raise SystemExit(bericht())
