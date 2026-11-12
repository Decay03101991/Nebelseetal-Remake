# -*- coding: ascii -*-
"""R3-1: EINE Tageslaenge im ganzen Projekt (07.11.2026, Befund A-1, Register 297).

Geprueft wird die Zusage des Schnitts:
  A. Es gibt genau EINE Zahl: `zeitbasis.SEKUNDEN_JE_TAG` = 86.400 s = 24 x 3.600 s.
  B. Jedes andere Modul, das eine Tageslaenge braucht, LIEST sie (`zeitbasis.SEKUNDEN_JE_TAG`)
     und schreibt keine eigene Zahl (AST-Wache ueber ganz `src/`).
  C. Die Zahl 28.800 kommt nirgends mehr vor - weder im Quelltext noch in `data/*.json`
     (das war die zweite Tageslaenge aus data/diplomatie.json).
  D. Die Datendatei fuehrt keine eigene Tageslaenge mehr, und jede Zeit darin ist ein Vielfaches
     von 86.400 s (Frist 2 Tage, Haeufigkeit 3 Tage, Vorlauf 1 Tag, Vorlauf nach Paktende 1 Tag,
     Vertragsdauer 3 Tage).
  E. Verhalten: `diplomatie.rache_tag` bucht genau an der Grenze 86.400 s den naechsten Tag,
     `ereignis_frist` ist 172.800 s, `vorlauf_sekunden` ist 86.400 s.
  F. GEGENPROBE: dieselbe Wache muss eine zweite Tageslaenge im Quelltext als Befund melden -
     sonst prueft sie nichts (eine Wache, die nie rot wird, ist keine Wache).

ASCII-only (Pruefdatei-Konvention).
"""
from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b
# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.
PRUEF_ART = "quelltext"
PRUEF_STUFE = 2
PRUEF_BETRIFFT = ['botkern', 'diplomatie', 'main:*', 'punkte', 'spieloekonomie', 'zeitbasis']
PRUEF_DATEN = ['diplomatie.json']
# --- Ende Pruefstand-Kopf -------------------------------------------------------

import ast
import glob
import inspect
import json
import os
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src

WURZEL, SRC = import_src()
import botkern as BK  # noqa: E402  (nach import_src)
import diplomatie as D  # noqa: E402
import punkte as P  # noqa: E402
import zeitbasis  # noqa: E402

TAG = 86400  # die belegte Zahl: 24 Spielstunden zu 3.600 Spielsekunden
# Namen, unter denen eine Tageslaenge im Projekt stehen KANN. Wer einen davon setzt, muss die
# EINE Quelle lesen - sonst entsteht die zweite Wahrheit wieder.
VERBOTEN = {"SEKUNDEN_JE_TAG", "SEKUNDEN_JE_SPIELTAG", "TAG_SEKUNDEN", "SPIELTAG_SEKUNDEN",
            "SEKUNDEN_PRO_TAG", "TAGESLAENGE"}


def _quelltext(pfad) -> str:
    """Eine Datei als Text lesen - Zeilenenden sind hier gleichgueltig."""
    with open(pfad, "rb") as f:
        return f.read().decode("utf-8")


def _code(funktion) -> str:
    """Quelltext einer Funktion ohne Docstring (Docstrings zaehlen nicht als Code)."""
    baum = ast.parse(textwrap.dedent(inspect.getsource(funktion)))  # Funktion in einen Baum wandeln
    kopf = baum.body[0]  # der FunctionDef-Knoten
    if kopf.body and isinstance(kopf.body[0], ast.Expr) and isinstance(kopf.body[0].value, ast.Constant):
        kopf.body = kopf.body[1:]  # fuehrenden Docstring abschneiden
    return ast.unparse(baum)  # Rest als Text


def _tageslaengen_defekte(quelle: str, name: str = "<quelle>") -> list:
    """Alle Stellen, die eine EIGENE Tageslaenge setzen (AST, nicht grep).

    Erlaubt ist nur `X = zeitbasis.SEKUNDEN_JE_TAG` - jede Zahl auf der rechten Seite ist eine
    zweite Wahrheit. Rueckgabe: Liste von (Datei, Zeile, Name, Wert) - leer heisst sauber.
    """
    baum = ast.parse(quelle)  # Syntaxbaum der Quelle
    defekte = []  # Sammelliste
    for knoten in ast.walk(baum):  # jeden Knoten ansehen
        ziele = []  # Ziele dieses Knotens
        if isinstance(knoten, ast.Assign):  # einfache Zuweisung
            ziele = [z for z in knoten.targets if isinstance(z, ast.Name)]  # nur Namen
            wert = knoten.value  # rechte Seite
        elif isinstance(knoten, ast.AnnAssign) and isinstance(knoten.target, ast.Name):  # typisiert
            ziele = [knoten.target]  # das eine Ziel
            wert = knoten.value  # rechte Seite
        else:
            continue  # alles andere ist keine Zuweisung
        for ziel in ziele:  # jedes Ziel ansehen
            if ziel.id not in VERBOTEN:  # kein Tageslaengen-Name
                continue  # dann nichts zu melden
            erlaubt = (isinstance(wert, ast.Attribute) and wert.attr == "SEKUNDEN_JE_TAG"
                       and isinstance(wert.value, ast.Name) and wert.value.id == "zeitbasis")
            if not erlaubt:  # eigene Zahl statt der EINEN Quelle
                defekte.append((name, knoten.lineno, ziel.id, ast.unparse(wert)))
    return defekte  # leer = sauber


def _zahl_im_code(quelle: str, zahl, name: str = "<quelle>") -> list:
    """Alle Stellen, in denen eine Zahl als Literal im Quelltext steht (nicht in Texten).

    Geprueft werden ganze Zahlen UND Kommazahlen: `86400.0` als Divisor ist genauso eine zweite
    Tageslaenge wie `86400` (belegt: zwei Divisoren in main.py und spieloekonomie.py).
    """
    baum = ast.parse(quelle)  # Syntaxbaum
    treffer = []  # Sammelliste
    for knoten in ast.walk(baum):  # jeden Knoten ansehen
        if isinstance(knoten, ast.Constant) and isinstance(knoten.value, (int, float)) \
                and not isinstance(knoten.value, bool) and knoten.value == zahl:
            treffer.append((name, knoten.lineno, knoten.value))  # Fundstelle merken
    return treffer  # leer = die Zahl kommt nicht mehr vor


def _sekunden_werte(knoten, pfad="") -> list:
    """Alle Zahlen unter Schluesseln, die nach Zeit aussehen - (Pfad, Schluessel, Wert)."""
    werte = []  # Sammelliste
    if isinstance(knoten, dict):  # ein Block
        for schluessel, wert in knoten.items():  # jedes Paar ansehen
            neuer_pfad = "%s/%s" % (pfad, schluessel)  # Pfad fortschreiben
            if isinstance(wert, (dict, list)):  # tiefer gehen
                werte.extend(_sekunden_werte(wert, neuer_pfad))
            elif "sekunden" in str(schluessel).lower() and isinstance(wert, (int, float)) \
                    and not isinstance(wert, bool):
                werte.append((neuer_pfad, str(schluessel), wert))  # Zeitwert merken
    elif isinstance(knoten, list):  # eine Liste
        for index, wert in enumerate(knoten):  # jedes Element ansehen
            werte.extend(_sekunden_werte(wert, "%s[%d]" % (pfad, index)))
    return werte  # gefundene Zeitwerte


abschnitt("A. Es gibt genau EINE Tageslaenge")
check("zeitbasis.SEKUNDEN_JE_TAG ist 86.400 s", zeitbasis.SEKUNDEN_JE_TAG == TAG,
      str(zeitbasis.SEKUNDEN_JE_TAG))
check("die Zahl ist 24 Spielstunden zu 3.600 s (Handbuch rechnet in Stunden)",
      zeitbasis.SEKUNDEN_JE_TAG == 24 * 3600, "%d = 24 x 3600" % TAG)
check("botkern liest dieselbe Zahl", BK.SEKUNDEN_JE_TAG == zeitbasis.SEKUNDEN_JE_TAG,
      str(BK.SEKUNDEN_JE_TAG))
check("punkte liest dieselbe Zahl", P.SEKUNDEN_JE_TAG == zeitbasis.SEKUNDEN_JE_TAG,
      str(P.SEKUNDEN_JE_TAG))
check("der Goetterschutz rechnet mit derselben Zahl (7 Tage = 604.800 s)",
      P.GOETTERSCHUTZ_TAGE * P.SEKUNDEN_JE_TAG == 7 * TAG, str(P.GOETTERSCHUTZ_TAGE * P.SEKUNDEN_JE_TAG))

abschnitt("B. Kein Modul schreibt eine eigene Tageslaenge (AST-Wache ueber ganz src/)")
dateien = sorted(glob.glob(os.path.join(SRC, "*.py")))  # alle Module
check("die Wache findet die Module", len(dateien) > 30, "%d Dateien" % len(dateien))
defekte = []  # Sammelliste
for pfad in dateien:  # jedes Modul pruefen
    name = os.path.basename(pfad)  # nur der Dateiname in der Meldung
    if name == "zeitbasis.py":  # hier STEHT die Zahl - hier ist sie erlaubt
        eigene = [d for d in _tageslaengen_defekte(_quelltext(pfad), name) if d[2] != "SEKUNDEN_JE_TAG"]
        defekte.extend(eigene)  # andere Namen waeren auch hier eine zweite Wahrheit
        continue  # zeitbasis selbst ist die Quelle
    defekte.extend(_tageslaengen_defekte(_quelltext(pfad), name))  # jedes andere Modul
check("kein Modul setzt eine eigene Tageslaenge", defekte == [], str(defekte[:5]))
check("zeitbasis setzt die Zahl GENAU EINMAL als Literal",
      _quelltext(os.path.join(SRC, "zeitbasis.py")).count("SEKUNDEN_JE_TAG = ") == 1,
      "eine Zuweisung")
fremde_zahl = []  # Sammelliste: Literale 86.400 ausserhalb von zeitbasis.py
for pfad in dateien:  # jedes Modul ansehen
    if os.path.basename(pfad) == "zeitbasis.py":  # hier steht die Zahl
        continue  # Absicht
    fremde_zahl.extend(_zahl_im_code(_quelltext(pfad), TAG, os.path.basename(pfad)))
check("kein Literal 86.400 ausserhalb von zeitbasis.py", fremde_zahl == [], str(fremde_zahl[:5]))
check("diplomatie.rache_tag fuehrt keine eigene Tageslaenge mehr",
      "spieltag_sekunden" not in _code(D.rache_tag)
      and "zeitbasis.SEKUNDEN_JE_TAG" in _code(D.rache_tag), "liest die EINE Quelle")
check("diplomatie.rache_bereit liest die Zahl fuer den Vorlauf nach dem Paktende",
      "zeitbasis.SEKUNDEN_JE_TAG" in _code(D.rache_bereit), "liest die EINE Quelle")

abschnitt("C. Die Zahl 28.800 kommt nirgends mehr vor")
alte_zahl = []  # Sammelliste
for pfad in dateien:  # Quelltext
    alte_zahl.extend(_zahl_im_code(_quelltext(pfad), 28800, os.path.basename(pfad)))
check("kein Literal 28.800 in src/", alte_zahl == [], str(alte_zahl[:5]))
daten_treffer = []  # Sammelliste der Datendateien
for pfad in sorted(glob.glob(os.path.join(WURZEL, "data", "*.json"))):  # jede Datendatei
    roh = _quelltext(pfad)  # Datei lesen
    if "28800" in roh:  # die alte Tageslaenge als Text
        daten_treffer.append(os.path.basename(pfad))
check("keine Datendatei fuehrt 28.800", daten_treffer == [], str(daten_treffer))

abschnitt("D. data/diplomatie.json fuehrt keine Tageslaenge, alle Zeiten sind Vielfache von 86.400")
with open(os.path.join(WURZEL, "data", "diplomatie.json"), "rb") as f:  # Datei binaer lesen
    diplomatie_daten = json.loads(f.read().decode("utf-8"))  # JSON laden
check("kein Schluessel spieltag_sekunden in der Datei",
      "spieltag_sekunden" not in json.dumps(diplomatie_daten), "keine zweite Tageslaenge")
check("die Datei nennt die EINE Quelle", "zeitbasis.py" in str(diplomatie_daten.get("_tageslaenge", "")),
      str(diplomatie_daten.get("_tageslaenge", ""))[:60])
zeiten = _sekunden_werte(diplomatie_daten)  # alle Zeitwerte der Datei
check("die Wache findet die Zeitwerte der Datei", len(zeiten) >= 5, str(len(zeiten)))
nicht_vielfach = [z for z in zeiten if float(z[2]) % TAG != 0]  # Vielfache pruefen
check("jede Zeit ist ein Vielfaches von 86.400 s", nicht_vielfach == [], str(nicht_vielfach))
check("Frist ist zwei Spieltage", float(diplomatie_daten["ereignisse"]["frist_sekunden"]) == 2 * TAG,
      str(diplomatie_daten["ereignisse"]["frist_sekunden"]))
check("Haeufigkeit ist drei Spieltage",
      float(diplomatie_daten["ereignisse"]["haeufigkeit_sekunden"]) == 3 * TAG,
      str(diplomatie_daten["ereignisse"]["haeufigkeit_sekunden"]))
check("Vorlauf ist ein Spieltag", float(diplomatie_daten["rache"]["vorlauf_sekunden"]) == TAG,
      str(diplomatie_daten["rache"]["vorlauf_sekunden"]))
check("Vorlauf nach dem Paktende ist ein Spieltag",
      float(diplomatie_daten["rache"]["nach_paktende_sekunden"]) == TAG,
      str(diplomatie_daten["rache"]["nach_paktende_sekunden"]))
check("die Vertragsdauer ist drei Spieltage",
      all(int(diplomatie_daten["vertraege"][art]["dauer_sekunden"]) == 3 * TAG
          for art in ("nichtangriff", "handel", "durchmarsch")),
      str([diplomatie_daten["vertraege"][a]["dauer_sekunden"] for a in ("nichtangriff", "handel", "durchmarsch")]))

abschnitt("E. Verhalten an der Grenze: ein Spieltag sind 86.400 s")
bot = {"name": "Haug", "gunst": 50, "rache": 0, "gedaechtnis": {}, "vertraege": {}}  # Bot in dict-Form
D.rache_tag(bot, TAG - 1)  # letzte Sekunde von Tag 0
check("in der letzten Sekunde von Tag 0 gibt es einen Punkt", D.rache_von(bot) == 1, str(D.rache_von(bot)))
D.rache_tag(bot, TAG - 1)  # derselbe Tag noch einmal
check("kein zweiter Punkt am selben Tag", D.rache_von(bot) == 1, str(D.rache_von(bot)))
D.rache_tag(bot, TAG)  # erste Sekunde von Tag 1
check("mit 86.400 s beginnt der naechste Tag (zweiter Punkt)", D.rache_von(bot) == 2,
      str(D.rache_von(bot)))
check("die Frist eines Ereignisses ist 172.800 s (zwei Spieltage)", D.ereignis_frist() == 2 * TAG,
      str(D.ereignis_frist()))
check("der Mindestabstand ist 259.200 s (drei Spieltage)", D.ereignis_haeufigkeit() == 3 * TAG,
      str(D.ereignis_haeufigkeit()))
check("der Vorlauf der Rache ist 86.400 s", D.vorlauf_sekunden() == TAG, str(D.vorlauf_sekunden()))

abschnitt("F. GEGENPROBE: eine zweite Tageslaenge wird gemeldet")
probe_nummer = _tageslaengen_defekte("SEKUNDEN_JE_TAG = 28800\n", "probe_zahl.py")  # Zahl statt Quelle
check("eine eigene Zahl wird gemeldet", len(probe_nummer) == 1 and probe_nummer[0][3] == "28800",
      str(probe_nummer))
probe_quelle = _tageslaengen_defekte("SEKUNDEN_JE_TAG = zeitbasis.SEKUNDEN_JE_TAG\n", "probe_ok.py")
check("das Lesen der EINEN Quelle ist erlaubt", probe_quelle == [], str(probe_quelle))
probe_zahl = _zahl_im_code("def f():\n    return 28800\n", 28800, "probe_f.py")  # Literal in Funktion
check("ein Literal 28.800 wird gemeldet", len(probe_zahl) == 1, str(probe_zahl))

sys.exit(bericht())
