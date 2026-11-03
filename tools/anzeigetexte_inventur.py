"""Inventur der ANZEIGETEXTE: welche Strings gehen wirklich in die Oberflaeche (Schnitt T-1).

Daniels Vorgabe (03.11.2026): Ingame-Texte tragen echte Umlaute. Ein Zaehler ueber ALLE
String-Literale ist dafuer unbrauchbar (13.447 "Treffer", mitgezaehlt waren Docstrings,
Hex-Farben und JSON-Schluessel). Dieses Werkzeug trennt deshalb drei Klassen:

  A  BELEGT     das Literal steht an einer nachgewiesenen Sinkstelle (wird angezeigt)
  B  FLIESSTEXT Literal mit Leerzeichen, das weder Docstring noch Schluessel noch technisch
                ist - in diesem Projekt sind das Begruendungen, Saetze und Meldungen, die
                ueber Rueckgaben, dict-Werte und Listen in die Anzeige wandern
  C  TECHNIK    alles andere: Kennungen, JSON-Schluessel, Dateinamen, Formate, Docstrings

Sinkstellen (je Aufruf, im Code belegt):
    text=...            jedes Widget-Argument (Label, Button, Entry, Radiobutton)
    title=...           Fenstertitel
    insert(...)         Tk-Text-Widget, alle Argumente ab dem Index
    StringVar.set(...)  Textvariablen
    _log(...) _melde(...) _hinweis(...) melde(...)     Spiel-Log und Meldungen
    messages.append(...) messages/nachrichten/postfach/meldungen   Postfach
    messagebox.showinfo/showwarning/showerror(..., message)        Dialoge

Ausserdem: die ANZEIGENAMEN aus data/*.json (Gebaeude, Einheiten, Forschung, Rohstoffe,
Waren) - die Kennung bleibt ASCII, der Name wird angezeigt.

Ausgeschlossen sind Docstrings (Modul, Klasse, Funktion), Dict-Schluessel, Subscript-
Schluessel, Zeichenketten an get/getattr/hasattr/setdefault/pop, Pfade, Dateiendungen,
Hex-Farben, Formatangaben und Bezeichner.

Zwei Wortlisten (bewusst getrennt, damit nichts still verschwindet):
    ERSATZ   Stammformen echter Ersatzschreibweisen - das ist die Handlungsliste fuer T-1
    REST     Woerter mit ae/oe/ue, die auf keinen Ersatz-Stamm passen (echte Umlaute in
             Worten wie "Quelle" oder Wortteile ohne Umlaut) - nur Sichtung, kein Fehler

Aufruf:
    python -X utf8 tools/anzeigetexte_inventur.py                 # Uebersicht
    python -X utf8 tools/anzeigetexte_inventur.py --liste         # jede Fundstelle
    python -X utf8 tools/anzeigetexte_inventur.py --schreiben     # docs/ANZEIGETEXTE_INVENTUR.md
"""
from __future__ import annotations

import ast
import datetime
import io
import json
import os
import re
import sys

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Projektwurzel
SRC = os.path.join(WURZEL, "src")  # Spielcode
DATEN = os.path.join(WURZEL, "data")  # Datendateien mit Anzeigenamen
ZIEL = os.path.join(WURZEL, "docs", "ANZEIGETEXTE_INVENTUR.md")  # Ergebnistabelle

# Stammformen der Ersatzschreibweisen. Gesucht wird mit <stamm>..., Schreibung egal.
# Die Liste ist absichtlich BREIT: sie ist die Wache gegen Ersatzschreibweisen. Ein Stamm,
# der auch RICHTIGES Deutsch faerbt, gehoert nicht hierher (Gegenprobe: --tabelle zeigt zu
# jedem betroffenen Wort die Zielform; richtige Woerter wie Quelle, Steuer, bauen, neu
# stehen bewusst NICHT in der Liste).
ERSATZ = [
    "waehl", "auswaehl", "ausgewaehlt", "anwaehl", "gewaehlt", "waehlbar", "Gebaeu",
    "gelaend", "menue", "fuer", "ueber", "zurueck", "naechst", "uebrig",
    "koenn", "muess", "duerf", "moecht", "braeucht", "haett", "wuerde",
    "koennt", "groess", "gross", "moegl", "hoechst", "gueltig", "ungueltig",
    "zulaessig", "unzulaessig", "moeglichkeit", "aender", "veraender", "ergaenz", "erfuell",
    "entfaell", "enthaelt", "haelt", "behaelt", "gehoer", "zugehoer", "erhoe",
    "hoehe", "laeuf", "faellt", "schlaeg", "traeg", "waechst", "haeng",
    "rueck", "vorrueck", "pruef", "geloesch", "loesch", "loes", "erloes",
    "zaehl", "fuenf", "saetz", "stueck", "kaempf", "militaer", "schuetz",
    "staerk", "schwaech", "vorraet", "gebuehr", "kapazitaet", "bestaend", "staend",
    "staett", "zustaend", "voelk", "doerf", "goett", "werkstaett", "tuerm",
    "waell", "naehe", "frueh", "spaet", "laenger", "aelter", "endguelt",
    "noetig", "benoetig", "woerterbuch", "buech", "lueck", "schluess", "fluessig",
    "ausdrueck", "ankuendig", "tatsaechlich", "eigenstaendig", "abhaengig", "vollstaendig", "beschaedig",
    "aufklaer", "verfueg", "genueg", "gruen", "gruend", "zusaetzl", "regulaer",
    "woertlich", "pluender", "sued", "waehr", "waer", "bauplaetze", "eintraeg",
    "auftraeg", "vorschlaeg", "erzuernt", "haendl", "flaech", "kraeft", "maecht",
    "naecht", "taet", "faeh", "gaeng", "raeum", "schaetz", "aeuss",
    "aehnl", "erwaehn", "spaeh", "fuehr", "faell", "plaetz", "schraenk", "spaenn", "raech",
    "klaer", "kaestchen", "oekonomie",
    "schliess", "oeffn", "bevoelker", "hoer", "faehig", "aussen", "wuensch", "taeusch", "foerder", "koerper", "ernaehr", "vergroesser", "anfaeng", "unterstuetz", "haeufig", "taeglich", "fuss",
]

# Ausnahmen: Woerter, die auf einen Ersatz-Stamm passen, aber technische Kennungen sind.
# Sie zaehlen NICHT als Fundstelle: eine "Verbesserung" wuerde den Code-Bezug zerstoeren.
# Je Eintrag: (Begruendung, Schreibung genau beachten). Die Begruendung steht hier, damit die
# Ausnahme pruefbar bleibt - und wortgleich in der Pruefdatei.
AUSNAHMEN = {
    "spieloekonomie": ("Modulname des Kerns - eine Anzeige, die darauf verweist, nennt den Code", False),
    "oeokonomie-1": ("Kennzeichen eines Admin-Teststandes, kein Anzeigetext", True),
    "PRIORITAET": ("Name der Konstanten _PRIORITAET - ein Hinweistext nennt sie woertlich", True),
    "GELAENDEFARBEN": ("Name der Konstanten WELT_GELAENDEFARBEN in einem Hinweistext", True),
    "GELAENDEREIHENFOLGE": ("Name der Konstanten WELT_GELAENDEREIHENFOLGE in einem Hinweistext", True),
}


def ist_ausnahme(wort):
    """Ist dieses Wort eine technische Ausnahme (Kennung) und keine Ersatzschreibweise?"""
    for form, (_grund, genau) in AUSNAHMEN.items():  # je Ausnahme pruefen
        if genau and wort == form:  # Schreibung muss stimmen
            return True
        if not genau and wort.lower() == form.lower():  # Schreibung egal
            return True
    return False

# Technische Literale: Pfade, Dateiendungen, Formate, Hex-Farben, Bezeichner.
TECHNISCH = re.compile(
    r"^(?:[A-Za-z_][A-Za-z0-9_]*"           # reiner Bezeichner (holzfaeller, bevoelkerung)
    r"|[^A-Za-z0-9]*"                        # nichts Buchstabiges (Zeichen, Leerzeichen)
    r"|#[0-9A-Fa-f]{3,8}"                    # Hex-Farbe
    r"|%[-+ 0-9.#]*[sdfr%]"                  # Formatangabe
    r"|.*[/\\].*"                            # Pfad
    r"|.*\.(?:py|json|png|jpg|jpeg|gif|txt|md|ico|wav|mp3)$"  # Dateiname
    r")$"
)


def _stuecke(knoten):
    """Liefert die Literal-Textstuecke eines Ausdrucks als [(knoten, text), ...].

    Behandelt Konstanten, f-Strings, Verkettung mit + und %, Ternaeroperatoren,
    Tupel/Listen und .format(...). Innere Aufrufe werden NICHT mitgelesen - sie sind
    ein eigenes Argument und keine Anzeige.
    """
    if isinstance(knoten, ast.Constant):  # einzelnes Literal
        if isinstance(knoten.value, str):  # nur Text, keine Zahl
            return [(knoten, knoten.value)]
        return []
    if isinstance(knoten, ast.JoinedStr):  # f-String: nur die festen Teile
        return [(stueck, stueck.value) for stueck in knoten.values
                if isinstance(stueck, ast.Constant) and isinstance(stueck.value, str)]
    if isinstance(knoten, ast.BinOp) and isinstance(knoten.op, (ast.Add, ast.Mod)):
        return _stuecke(knoten.left) + _stuecke(knoten.right)  # "a" + "b" / "a %s" % x
    if isinstance(knoten, ast.IfExp):  # "a" if x else "b"
        return _stuecke(knoten.body) + _stuecke(knoten.orelse)
    if isinstance(knoten, (ast.Tuple, ast.List)):
        teile = []
        for element in knoten.elts:
            teile.extend(_stuecke(element))
        return teile
    if isinstance(knoten, ast.Call) and isinstance(knoten.func, ast.Attribute):
        if knoten.func.attr == "format":  # "a {}".format(x)
            return _stuecke(knoten.func.value)
    return []


def _name_des_aufrufs(knoten):
    """Liefert den Namen einer aufgerufenen Funktion (Name oder letztes Attribut)."""
    if isinstance(knoten, ast.Name):
        return knoten.id
    if isinstance(knoten, ast.Attribute):
        return knoten.attr
    return ""


def _ist_stringvar(wert):
    """Erkennt StringVar(...) und Namen, die auf eine Textvariable deuten."""
    if isinstance(wert, ast.Call) and "StringVar" in _name_des_aufrufs(wert.func):
        return True
    if isinstance(wert, ast.Name):
        return "var" in wert.id.lower()
    if isinstance(wert, ast.Attribute):
        return "var" in wert.attr.lower()
    return False


def _sinken(aufruf):
    """Liefert [(art, [(knoten, text), ...]), ...] fuer einen Aufruf-Knoten."""
    treffer = []
    for kw in aufruf.keywords:  # text=... und title=...
        if kw.arg in ("text", "title"):
            treffer.append((kw.arg + "=", _stuecke(kw.value)))
    name = _name_des_aufrufs(aufruf.func)  # Name der aufgerufenen Funktion
    methode = aufruf.func if isinstance(aufruf.func, ast.Attribute) else None  # Objekt vor dem Punkt
    if name in ("_log", "log", "_melde", "melde", "_hinweis", "hinweis", "_meldung"):
        for arg in aufruf.args:
            treffer.append((name + "(...)", _stuecke(arg)))
    elif name == "insert" and len(aufruf.args) >= 2:  # Tk-Text: insert("end", "...")
        for arg in aufruf.args[1:]:
            treffer.append(("insert(...)", _stuecke(arg)))
    elif name == "set" and methode is not None and _ist_stringvar(methode.value):  # StringVar.set
        for arg in aufruf.args:
            treffer.append(("StringVar.set", _stuecke(arg)))
    elif name == "append" and methode is not None and aufruf.args:  # Postfach
        quelle = _name_des_aufrufs(methode.value).lower()  # Name der Liste
        if any(wort in quelle for wort in ("message", "nachricht", "postfach", "meldung")):
            for arg in aufruf.args:
                treffer.append(("messages.append", _stuecke(arg)))
    elif name in ("showinfo", "showwarning", "showerror") and len(aufruf.args) >= 2:
        for arg in aufruf.args[1:]:  # (title, message) - beide werden angezeigt
            treffer.append(("messagebox", _stuecke(arg)))
    return [(art, teile) for art, teile in treffer if teile]  # leere Sinks verwerfen


def _docstring_knoten(baum):
    """Sammelt die Knoten aller Docstrings (Modul, Klasse, Funktion)."""
    knoten = []  # gefundene Docstring-Konstanten
    for element in ast.walk(baum):
        if not isinstance(element, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        rumpf = getattr(element, "body", [])
        if rumpf and isinstance(rumpf[0], ast.Expr) and isinstance(rumpf[0].value, ast.Constant):
            if isinstance(rumpf[0].value.value, str):  # erste Anweisung ist ein Text
                knoten.append(rumpf[0].value)
    return {id(k) for k in knoten}


def _schluessel_knoten(baum):
    """Sammelt Dict-Schluessel, Subscript-Schluessel und Schluessel-Argumente."""
    knoten = set()  # ids der technischen Zeichenketten
    for element in ast.walk(baum):
        if isinstance(element, ast.Dict):  # {"schluessel": wert}
            for teil in element.keys:
                if teil is None:
                    continue
                for k, _t in _stuecke(teil):
                    knoten.add(id(k))
        elif isinstance(element, ast.Subscript):  # daten["schluessel"]
            for k, _t in _stuecke(element.slice):
                knoten.add(id(k))
        elif isinstance(element, ast.Call):  # dict.get("schluessel"), getattr(obj, "feld")
            name = _name_des_aufrufs(element.func)
            if name in ("get", "getattr", "hasattr", "setdefault", "pop", "index",
                        "startswith", "endswith", "replace", "split", "rsplit", "join",
                        "strip", "format", "match", "search", "find", "count", "partition"):
                for arg in element.args[1:]:
                    for k, _t in _stuecke(arg):
                        knoten.add(id(k))
                for kw in element.keywords:
                    for k, _t in _stuecke(kw.value):
                        knoten.add(id(k))
        elif isinstance(element, ast.Compare):  # Vergleich: Text ist hier BEDEUTUNG, keine Anzeige
            for teil in [element.left] + element.comparators:
                for k, _t in _stuecke(teil):
                    knoten.add(id(k))
    return knoten


# Code-Bezuege IM Anzeigetext: eine Meldung darf auf `einheiten.ist_kaempfer` oder
# `data/bot_gruendung.json` verweisen - dort MUSS der Name ASCII bleiben, sonst zeigt die
# Anzeige einen Namen, den es im Code nicht gibt. Diese Muster werden vor der Wortpruefung
# durch Platzhalter ersetzt (schuetzen/entschuetzen) und zaehlen nicht als Ersatzschreibweise.
# Code-Bezuege IM Anzeigetext: eine Meldung darf auf `einheiten.ist_kaempfer` oder
# `data/bot_gruendung.json` verweisen - dort MUSS der Name ASCII bleiben, sonst zeigt die
# Anzeige einen Namen, den es im Code nicht gibt. Diese Muster werden vor der Wortpruefung
# durch Platzhalter ersetzt (schuetzen/entschuetzen) und zaehlen nicht als Ersatzschreibweise.
#
# EIN Muster mit Alternativen statt fuenf Durchgaengen: sonst zieht die Unterstrich-Regel
# den Anker der Punkt-Regel weg (belegt 03.11.2026: `gelaende.alle_gebaeude` wurde zu
# `gelände.alle_gebaeude`, weil `alle_gebaeude` vorher zum Platzhalter wurde).
SCHUTZ_MUSTER = [
    r"(?<=\.)[A-Za-z][A-Za-z0-9_]*",  # Feld/Attribut nach einem Punkt
    r"[A-Za-z_][A-Za-z0-9_]*(?=\.[A-Za-z_])",  # Modul vor einem Punkt (gelaende.alle)
    r"[A-Za-z_][A-Za-z0-9_]*(?=\()",  # Funktionsname DIREKT vor einer Klammer
    r"[A-Za-z_][A-Za-z0-9_]*\.(?:py|json|md|txt|png|jpg)",  # Dateiname
    r"[A-Za-z0-9]*_[A-Za-z0-9_]*",  # Bezeichner mit Unterstrich
]
SCHUTZ_REGEX = re.compile("|".join(SCHUTZ_MUSTER))  # linke Alternative gewinnt

PLATZHALTER = "~~%d~~"  # Kennzeichen fuer geschuetzte Stellen: keine Buchstaben, kein Punkt


def schuetzen(text):
    """Blendet Code-Bezuege aus einem Anzeigetext aus. Rueckgabe: (Text, Tabelle).

    Geschuetzt werden (a) die Kennungen aus AUSNAHMEN und (b) Code-Bezuege nach Muster:
    Bezeichner mit Unterstrich, Modul/Feld nach einem Punkt, Funktionsnamen vor einer
    Klammer, Dateinamen. Der Platzhalter enthaelt weder Buchstaben noch Punkt noch
    Unterstrich, damit er von keinem Muster erneut getroffen wird.
    """
    geschuetzt = {}  # Platzhalter -> Original

    def _merken(treffer):
        """Legt das Original ab und gibt den Platzhalter zurueck."""
        platzhalter = PLATZHALTER % len(geschuetzt)  # laufende Nummer
        geschuetzt[platzhalter] = treffer.group(0)  # Original merken
        return platzhalter

    for wort, (_grund, genau) in AUSNAHMEN.items():  # (a) Kennungen aus der Ausnahmeliste
        flags = 0 if genau else re.IGNORECASE  # Schreibung genau oder egal
        text = re.sub(re.escape(wort), _merken, text, flags=flags)
    text = SCHUTZ_REGEX.sub(_merken, text)  # (b) Code-Bezuege in EINEM Durchgang
    return text, geschuetzt


def entschuetzen(text, geschuetzt):
    """Setzt die geschuetzten Code-Bezuege zurueck."""
    for platzhalter, original in geschuetzt.items():
        text = text.replace(platzhalter, original)
    return text


def _muster():
    """Baut die zwei Suchmuster: Ersatzschreibweise und alles andere mit ae/oe/ue.

    Das Wort darf mit dem Stamm BEGINNEN oder ihn IM WORT tragen: deutsche Zusammensetzungen
    (Spielstaende, Funktionsgebaeude, Waldlaeufer) tragen den Stamm in der Mitte. Gemeldet wird
    immer das GANZE Wort, nicht der Stamm.
    """
    ersatz = re.compile(
        r"\b[A-Za-z]*(?:" + "|".join(sorted(ERSATZ, key=len, reverse=True)) + r")[A-Za-z]*\b",
        re.IGNORECASE,
    )
    rest = re.compile(r"\b[A-Za-z]*(?:ae|oe|ue|Ae|Oe|Ue)[A-Za-z]*\b")
    return ersatz, rest


ERSATZ_MUSTER, REST_MUSTER = _muster()


def _klasse(text, ist_sinke):
    """Ordnet ein Literal einer Klasse zu: A (belegt), B (Fliesstext), C (Technik)."""
    if ist_sinke:
        return "A"  # an einer Sinkstelle - wird angezeigt
    if TECHNISCH.match(text):
        return "C"  # Bezeichner, Pfad, Format
    if " " in text.strip() or len(text.strip()) > 3:  # Satz oder Beschriftung
        return "B"
    return "C"


def _dateien():
    """Alle Python-Dateien unter src/ alphabetisch."""
    return sorted(f for f in os.listdir(SRC) if f.endswith(".py"))


def _json_anzeigenamen():
    """Liest die Anzeigenamen aus data/*.json (Kennung bleibt ASCII, Name wird gezeigt)."""
    namen = []
    zuordnung = [
        ("buildings.json", ("gebaeude",), ("name", "anzeige")),
        ("units.json", ("einheiten",), ("name", "anzeige")),
        ("research.json", ("forschung",), ("name", "anzeige")),
        ("resources.json", ("rohstoffe",), ("name", "anzeige")),
        ("items.json", ("waren",), ("name", "anzeige")),
    ]
    for dateiname, schluessel, felder in zuordnung:
        pfad = os.path.join(DATEN, dateiname)  # Pfad der Datendatei
        if not os.path.exists(pfad):
            continue
        daten = json.load(io.open(pfad, encoding="utf-8-sig"))
        liste = daten
        for stufe in schluessel:  # in die Liste hineinlaufen
            if isinstance(liste, dict) and stufe in liste:
                liste = liste[stufe]
        if isinstance(liste, dict):  # dict: Kennung -> Eintrag
            liste = list(liste.values())
        if not isinstance(liste, list):
            continue
        for eintrag in liste:
            if not isinstance(eintrag, dict):
                continue
            for feld in felder:
                wert = eintrag.get(feld)
                if isinstance(wert, str) and wert.strip():
                    namen.append((dateiname, eintrag.get("id") or eintrag.get("kennung") or "",
                                  feld, wert))
    return namen


def _pruefe_quelle(quelle, dateiname):
    """Prueft EINEN Quelltext auf Ersatzschreibweisen in Anzeigetexten.

    Rueckgabe: (Funde, Zaehler, Sichtung). Herausgezogen aus `sammle()`, damit die
    Pruefdatei eine ERFUNDENE Quelle vorlegen kann - die Gegenprobe der Wache.
    """
    baum = ast.parse(quelle, filename=dateiname)
    ausschluss = _docstring_knoten(baum) | _schluessel_knoten(baum)  # keine Anzeige
    sinken = {}  # id(Knoten) -> Sink-Art
    for knoten in ast.walk(baum):
        if isinstance(knoten, ast.Call):
            for art, teile in _sinken(knoten):
                for k, _text in teile:
                    sinken.setdefault(id(k), art)
    funde = []  # [(Klasse, datei, zeile, art, wort, text)]
    rest = []  # [(datei, zeile, art, wort, text)]
    zaehler = {"A": 0, "B": 0, "stellen": 0}
    for knoten in ast.walk(baum):
        if not isinstance(knoten, ast.Constant) or not isinstance(knoten.value, str):
            continue
        if id(knoten) in ausschluss:  # Docstring oder Schluessel
            continue
        text = knoten.value  # der Literaltext
        if not re.search(r"[A-Za-z]", text):  # keine Buchstaben: keine Anzeige
            continue
        art = sinken.get(id(knoten), "ohne Sinke")  # Sink-Art oder Kennzeichen
        klasse = _klasse(text, art != "ohne Sinke")
        if klasse == "C":  # Technik zaehlt nicht als Anzeige
            continue
        zeile = getattr(knoten, "lineno", 0)
        if klasse == "A":
            zaehler["A"] += 1
        else:
            zaehler["B"] += 1
        geprueft, geschuetzt = schuetzen(text)  # Code-Bezuege ausblenden
        for treffer in ERSATZ_MUSTER.finditer(geprueft):  # Ersatzschreibweise darin
            if ist_ausnahme(treffer.group(0)):  # technische Ausnahme (Kennung)
                continue
            funde.append((klasse, dateiname, zeile, art, treffer.group(0), text.strip()))
            zaehler["stellen"] += 1
        ohne_ersatz = ERSATZ_MUSTER.sub(" ", geprueft)  # Ersatz-Woerter ausblenden
        for treffer in REST_MUSTER.finditer(ohne_ersatz):  # Sichtung
            rest.append((dateiname, zeile, art, treffer.group(0), text.strip()))
    return funde, zaehler, rest


def pruefe_quelle(quelle, dateiname="<quelle>"):
    """Prueft einen Quelltext und liefert NUR die Fundstellen (fuer die Pruefdatei)."""
    funde, _zaehler, _rest = _pruefe_quelle(quelle, dateiname)
    return funde


def umlaute_nur_in_texten(quelle):
    """Prueft, dass Nicht-ASCII NUR in String-Literalen steht (Anzeigetexte).

    Daniel 03.11.2026: die ASCII-Regel fuer `.py` gilt fuer CODE und KOMMENTARE; Anzeigetexte
    tragen echte Umlaute. Diese Funktion macht die Regel pruefbar: sie liefert jede Stelle
    mit Nicht-ASCII AUSSERHALB eines Literals als (Zeile, Spalte, Zeichen).

    `ast` zaehlt Spalten in UTF-8-BYTES - deshalb wird die Byte-Spalte des Zeichens gebildet
    und mit den Literal-Grenzen verglichen (belegt 03.11.2026).
    """
    baum = ast.parse(quelle)  # Syntaxfehler meldet der Aufrufer
    erlaubt = []  # [(start_zeile, start_spalte, ende_zeile, ende_spalte)] in Bytes
    for knoten in ast.walk(baum):
        if isinstance(knoten, ast.Constant) and isinstance(knoten.value, str):
            if getattr(knoten, "end_lineno", None) is None:
                continue
            erlaubt.append((knoten.lineno, knoten.col_offset,
                            knoten.end_lineno, knoten.end_col_offset))
    treffer = []  # Stellen ausserhalb der Literale
    for nummer, zeile in enumerate(quelle.splitlines(keepends=True), start=1):
        for index, zeichen in enumerate(zeile):
            if ord(zeichen) < 128:  # ASCII ist immer in Ordnung
                continue
            spalte = len(zeile[:index].encode("utf-8"))  # Byte-Spalte wie in ast
            if not any((l, s) <= (nummer, spalte) < (el, e) for l, s, el, e in erlaubt):
                treffer.append((nummer, spalte, zeichen))
    return treffer


def sammle():
    """Fuehrt die Inventur aus und liefert das Ergebnis als dict."""
    alle_funde = []  # [(Klasse, datei, zeile, art, wort, text)]
    rest_funde = []  # [(datei, zeile, art, wort, text)]
    je_datei = {}  # datei -> {"A": n, "B": n, "stellen": n}
    for dateiname in _dateien():
        pfad = os.path.join(SRC, dateiname)  # voller Pfad
        quelle = io.open(pfad, encoding="utf-8").read()
        funde, zaehler, rest = _pruefe_quelle(quelle, dateiname)  # eine Datei pruefen
        alle_funde.extend(funde)  # Fundstellen sammeln
        rest_funde.extend(rest)  # Sichtung sammeln
        je_datei[dateiname] = zaehler
    json_namen = []  # Anzeigenamen aus data/ mit Ersatzschreibweise
    for dateiname, kennung, feld, wert in _json_anzeigenamen():
        if ERSATZ_MUSTER.search(wert):
            json_namen.append((dateiname, kennung, feld, wert))
    return {"je_datei": je_datei, "funde": alle_funde, "rest": rest_funde, "json": json_namen}


def _summen(ergebnis):
    """Summiert die Klassen A und B und die Fundstellen ueber alle Dateien."""
    a = sum(z["A"] for z in ergebnis["je_datei"].values())
    b = sum(z["B"] for z in ergebnis["je_datei"].values())
    stellen = sum(z["stellen"] for z in ergebnis["je_datei"].values())
    return a, b, stellen


def bericht(ergebnis, mit_liste=False):
    """Gibt die Uebersicht (und auf Wunsch jede Fundstelle) auf stdout aus."""
    a, b, stellen = _summen(ergebnis)
    print("ANZEIGETEXTE-INVENTUR (Schnitt T-1)")
    print("%-28s %8s %10s %9s" % ("Datei", "A belegt", "B Fliesst.", "Ersatz"))
    print("-" * 60)
    for dateiname, zahlen in ergebnis["je_datei"].items():  # je Datei eine Zeile
        if zahlen["stellen"]:
            print("%-28s %8d %10d %9d" % (dateiname, zahlen["A"], zahlen["B"], zahlen["stellen"]))
    print("-" * 60)
    print("%-28s %8d %10d %9d" % ("SUMME", a, b, stellen))
    print()
    print("Anzeigenamen aus data/ mit Ersatzschreibweise:", len(ergebnis["json"]))
    for dateiname, kennung, feld, wert in ergebnis["json"]:
        print("   %-14s %-24s %-8s %s" % (dateiname, kennung, feld, wert))
    print()
    print("Restliche Woerter mit ae/oe/ue (kein Ersatz-Stamm):",
          len({f[3] for f in ergebnis["rest"]}))
    if mit_liste:  # jede Fundstelle mit Zeile und Sinke
        print()
        print("FUNDSTELLEN Ersatzschreibweise:")
        for klasse, datei, zeile, art, wort, text in ergebnis["funde"]:
            print("   [%s] %s:%s (%s) %s | %s" % (klasse, datei, zeile, art, wort, text[:110]))
        print()
        print("FUNDSTELLEN Rest (nur zur Sichtung):")
        for datei, zeile, art, wort, text in ergebnis["rest"]:
            print("   %s:%s (%s) %s | %s" % (datei, zeile, art, wort, text[:110]))


def _kuerzen(text, grenze):
    """Kuerzt einen Text fuer die Tabelle und schuetzt die Pipe."""
    text = " ".join(text.split())  # Zeilenumbrueche zu Leerzeichen
    text = text.replace("|", "\\|")  # Tabellenzeichen maskieren
    return text if len(text) <= grenze else text[: grenze - 1] + "..."


def _heute():
    """Datum aus dem System, nie geraten."""
    return datetime.date.today().strftime("%d.%m.%Y")


def dokument(ergebnis):
    """Schreibt die Inventur als Markdown-Dokument nach docs/."""
    a, b, stellen = _summen(ergebnis)
    teile = []
    teile.append("# Anzeigetexte-Inventur (Schnitt T-1, Stand %s)\n" % _heute())
    teile.append(
        "Erzeugt von `tools/anzeigetexte_inventur.py`. Gezaehlt werden zwei Klassen von "
        "Texten: **A belegt** steht an einer nachgewiesenen Sinkstelle (Widget-`text=`, "
        "Fenstertitel, `insert(`, `StringVar.set`, `_log(`/`_melde(`, `messages.append(`, "
        "Dialoge), **B Fliesstext** ist ein Satz- oder Beschriftungsliteral ausserhalb dieser "
        "Sinkstellen, das in diesem Projekt ueber Rueckgaben, dict-Werte und Listen in die "
        "Anzeige wandert. Docstrings, JSON-Schluessel, Pfade, Dateiendungen, Hex-Farben und "
        "Bezeichner sind ausgeschlossen - deshalb ist diese Zahl eine Messung, keine Schaetzung.\n"
    )
    teile.append("## Uebersicht je Datei\n")
    teile.append("| Datei | A belegt | B Fliesstext | Ersatzschreibweisen |")
    teile.append("|---|---|---|---|")
    for dateiname, zahlen in sorted(ergebnis["je_datei"].items(), key=lambda z: z[1]["stellen"]):
        teile.append("| `%s` | %d | %d | **%d** |"
                     % (dateiname, zahlen["A"], zahlen["B"], zahlen["stellen"]))
    teile.append("| **Summe** | **%d** | **%d** | **%d** |" % (a, b, stellen))
    teile.append("")
    teile.append("## Anzeigenamen aus `data/`\n")
    if ergebnis["json"]:
        teile.append("| Datei | Kennung | Feld | Anzeigename |")
        teile.append("|---|---|---|---|")
        for dateiname, kennung, feld, wert in ergebnis["json"]:
            teile.append("| `%s` | `%s` | %s | %s |" % (dateiname, kennung, feld, wert))
    else:
        teile.append("Keine Ersatzschreibweise in den Anzeigenamen der Datendateien.")
    teile.append("")
    teile.append("## Fundstellen (Ersatzschreibweise)\n")
    if ergebnis["funde"]:
        teile.append("| Klasse | Datei:Zeile | Sinkstelle | Wort | Text |")
        teile.append("|---|---|---|---|---|")
        for klasse, datei, zeile, art, wort, text in ergebnis["funde"]:
            teile.append("| %s | `%s:%s` | `%s` | %s | %s |"
                         % (klasse, datei, zeile, art, wort, _kuerzen(text, 130)))
    else:
        teile.append("Keine Fundstelle - die Anzeigetexte tragen echte Umlaute.")
    teile.append("")
    teile.append("## Restliche Woerter mit ae/oe/ue (Sichtung, kein Ersatz-Stamm)\n")
    reste = {}
    for datei, zeile, art, wort, text in ergebnis["rest"]:
        reste[wort] = reste.get(wort, 0) + 1
    if reste:
        teile.append("Diese Woerter enthalten ae/oe/ue, passen aber auf keinen Ersatz-Stamm. "
                     "Sie werden nur gezeigt, damit nichts unbemerkt bleibt - echte Umlaute "
                     "wie in `Quelle` oder Wortteile ohne Umlaut sind hier richtig.\n")
        teile.append("| Wort | Vorkommen |")
        teile.append("|---|---|")
        for wort, anzahl in sorted(reste.items(), key=lambda w: (-w[1], w[0])):
            teile.append("| %s | %d |" % (wort, anzahl))
    else:
        teile.append("Keine.")
    teile.append("")
    text = "\n".join(teile)
    io.open(ZIEL, "w", encoding="utf-8", newline="\n").write(text)
    return ZIEL


def main(argv):
    """Kommandozeile: ohne Flag Uebersicht, --liste Fundstellen, --schreiben Dokument."""
    ergebnis = sammle()
    bericht(ergebnis, mit_liste="--liste" in argv)
    if "--schreiben" in argv:
        pfad = dokument(ergebnis)
        print("\nGeschrieben:", pfad)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
