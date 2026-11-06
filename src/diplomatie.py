# -*- coding: ascii -*-
"""Diplomatie der Bots - Gunst, Status (S4 Teil 1, 06.11.2026).

Dieses Modul ist die EINE Lesestelle fuer die Gunst eines Bots und fuer den Status, der daraus
folgt. Alle Zahlen und Texte stehen in `data/diplomatie.json`; hier steht keine einzige Grenze im
Code. Anzeige und Kern rufen dieselben Funktionen auf (Regel F-04, `docs/ABLAUF_LLM_20261106.md`
Schritt 1).

Bewusste Entscheidung: der STATUS wird NIE gespeichert, sondern immer aus der Gunst gerechnet. Zwei
Speicher fuer eine Groesse waeren genau der Fehler, den F-04 beschreibt.

Spaetere Teile (Vertraege, Rachetopf, Ereignisse) kommen in dieselbe Datendatei und dasselbe Modul -
ein Thema, ein Modul, eine Datei. Sie werden NICHT hier vorbereitet, sondern mit ihrem eigenen
Schnitt gebaut.
"""
import json  # importiert json zum Lesen der Datendatei
import os  # importiert os fuer Pfadoperationen
import spieldaten  # importiert spieldaten fuer den Projektwurzelpfad

STAND = "2026-11-06.1"  # Kennung dieses Modulstands (erscheint in keinem Spielstand)
_CACHE = {}  # Pfad -> (Aenderungszeit, Inhalt): die Datendatei wird EINMAL gelesen


def daten(pfad=None) -> dict:
    """Liest `data/diplomatie.json` und gibt sie als dict zurueck.

    Eingabe: optionaler Pfad (fuer Pruefungen mit eigener Datei).
    Ausgabe: dict mit den Daten; leeres dict, wenn die Datei fehlt oder kein JSON ist.
    """
    if pfad is None:  # ohne Pfad gilt die Projektdatei
        pfad = os.path.join(spieldaten.projektwurzel(), "data", "diplomatie.json")  # Standardpfad bauen
    try:  # Aenderungszeit der Datei holen
        stand = os.path.getmtime(pfad)  # Zeitstempel als Cache-Schluessel
    except OSError:  # Datei fehlt oder ist nicht lesbar
        return {}  # dann gibt es keine Daten (kein Absturz)
    gemerkt = _CACHE.get(pfad)  # schon geladene Fassung ansehen
    if gemerkt is not None and gemerkt[0] == stand:  # unveraendert seit dem letzten Lesen
        return gemerkt[1]  # aus dem Cache - die Bot-Schleife liest sonst tausendfach
    try:  # Datei oeffnen und lesen
        with open(pfad, encoding="utf-8") as datei:  # UTF-8, wie alle Datendateien
            inhalt = json.load(datei)  # JSON in ein dict wandeln
    except (OSError, ValueError):  # Lesefehler oder kaputtes JSON
        return {}  # dann keine Daten statt einer Ausnahme
    _CACHE[pfad] = (stand, inhalt)  # Ergebnis merken
    return inhalt  # an den Aufrufer geben


def _zahl(wert, standard) -> float:
    """Wandelt einen Wert in eine Zahl; Unbrauchbares ergibt den Standardwert.

    Eingabe: beliebiger Wert, Standardwert.
    Ausgabe: float. `True`/`False` gelten NICHT als Zahl (Fallstrick `int(True) == 1`).
    """
    if isinstance(wert, bool) or not isinstance(wert, (int, float)):  # Wahrheitswerte und Fremdes ablehnen
        return float(standard)  # dann den Standardwert nehmen
    return float(wert)  # sonst die Zahl selbst


def _gunst_block(einst=None) -> dict:
    """Gibt den Gunst-Block der Datendatei zurueck (oder einen leeren Block)."""
    quelle = einst if isinstance(einst, dict) else daten()  # uebergebene Daten oder die Datei lesen
    block = (quelle or {}).get("gunst")  # den Gunst-Block heraussuchen
    return block if isinstance(block, dict) else {}  # nur ein dict ist brauchbar


def aktiv(einst=None) -> bool:
    """Ist die Diplomatie eingeschaltet? Ein Wort in der Datendatei entscheidet (A-7)."""
    quelle = einst if isinstance(einst, dict) else daten()  # Datenquelle bestimmen
    return bool((quelle or {}).get("aktiv", False))  # ohne ausdrueckliches true ist sie aus


def grenzen(einst=None) -> tuple:
    """Kleinst- und Groesstwert der Gunst aus der Datendatei.

    Eingabe: optionale Daten. Ausgabe: (min, max) als ganze Zahlen.
    """
    block = _gunst_block(einst)  # Gunst-Block holen
    unten = int(_zahl(block.get("min"), 0))  # Untergrenze, Vorgabe 0
    oben = int(_zahl(block.get("max"), 100))  # Obergrenze, Vorgabe 100
    if oben < unten:  # kaputte Angaben nicht uebernehmen
        return 0, 100  # dann die Vorgaben der Datendatei
    return unten, oben  # brauchbare Grenzen


def startwert(einst=None) -> int:
    """Der Startwert eines Bots ohne gespeicherte Gunst (aus der Datendatei)."""
    block = _gunst_block(einst)  # Gunst-Block holen
    unten, oben = grenzen(einst)  # Grenzen fuer die Klammer
    return klemmen(int(_zahl(block.get("start"), unten)), einst)  # Startwert klemmen und zurueck


def klemmen(wert, einst=None) -> int:
    """Begrenzt einen Gunstwert auf die Grenzen der Datendatei.

    Eingabe: beliebiger Wert. Ausgabe: ganze Zahl zwischen min und max.
    """
    unten, oben = grenzen(einst)  # Grenzen lesen
    zahl = int(_zahl(wert, unten))  # Zahl werden lassen (Unbrauchbares -> Untergrenze)
    return max(unten, min(oben, zahl))  # in die Grenzen einschliessen


def gunst_von(bot_daten, einst=None) -> int:
    """Liest die Gunst aus der dict-Form eines Bots; fehlt sie, gilt der Startwert.

    Eingabe: dict (Form aus `bot_als_dict`) oder Zahl. Ausgabe: ganze Zahl in den Grenzen.
    """
    if isinstance(bot_daten, dict):  # der Normalfall: die dict-Form des Kerns
        return klemmen(bot_daten.get("gunst", startwert(einst)), einst)  # Feld lesen, sonst Startwert
    return klemmen(bot_daten, einst)  # eine nackte Zahl wird ebenfalls geklemmt


def gunst_setzen(bot_daten, wert, einst=None) -> int:
    """Setzt die Gunst in der dict-Form und gibt den geklemmten Wert zurueck.

    Eingabe: dict des Bots, gewuenschter Wert. Ausgabe: der Wert, der jetzt im dict steht.
    Ist `bot_daten` kein dict, wird nur geklemmt (der Aufrufer muss das Ergebnis verwenden).
    """
    neu = klemmen(wert, einst)  # Wert in die Grenzen bringen
    if isinstance(bot_daten, dict):  # nur ein dict kann beschrieben werden
        bot_daten["gunst"] = neu  # EIN Speicher: das Feld des Bots
    return neu  # Aufrufer bekommt den tatsaechlichen Wert


def gunst_aendern(bot_daten, delta, grund="", einst=None) -> int:
    """Aendert die Gunst um `delta` und gibt den neuen Wert zurueck.

    Eingabe: dict des Bots, Aenderung (darf negativ sein), Grund als Text (nur fuer den Aufrufer).
    Ausgabe: der neue, geklemmte Wert. Der Grund wird NICHT gespeichert - er gehoert ins Protokoll
    des Aufrufers, nicht in eine zweite Buchfuehrung.
    """
    alt = gunst_von(bot_daten, einst)  # jetzigen Wert lesen
    return gunst_setzen(bot_daten, alt + int(_zahl(delta, 0)), einst)  # addieren und klemmen


def stufen(einst=None) -> list:
    """Die Statusstufen der Datendatei, aufsteigend nach ihrer Obergrenze sortiert.

    Ausgabe: Liste von dicts mit `bis`, `schluessel`, `text`; leer, wenn die Datei sie nicht nennt.
    """
    block = _gunst_block(einst)  # Gunst-Block holen
    roh = block.get("status")  # Stufenliste ansehen
    liste = []  # Ergebnisliste
    if isinstance(roh, list):  # nur eine Liste ist brauchbar
        for eintrag in roh:  # jeden Eintrag pruefen
            if not isinstance(eintrag, dict):  # Fremdes uebergehen
                continue  # naechster Eintrag
            schluessel = str(eintrag.get("schluessel") or "")  # Kennung der Stufe
            if not schluessel:  # ohne Kennung ist die Stufe wertlos
                continue  # naechster Eintrag
            liste.append({"bis": int(_zahl(eintrag.get("bis"), 0)),  # Obergrenze als Zahl
                          "schluessel": schluessel,  # Kennung fuer den Kern
                          "text": str(eintrag.get("text") or schluessel)})  # Text fuer die Anzeige
    return sorted(liste, key=lambda e: e["bis"])  # aufsteigend nach Obergrenze


def status(gunst, einst=None) -> str:
    """Der Status zu einer Gunst - derselbe Weg fuer Kern und Anzeige.

    Eingabe: Gunstwert (wird geklemmt). Ausgabe: der Schluessel der passenden Stufe
    (`feindselig`, `wachsam`, `freundlich` ...) oder ein leerer Text, wenn die Datei keine Stufen
    nennt. Dann zeigt die Anzeige die Zahl ohne Wort - es wird nichts erfunden.
    """
    wert = klemmen(gunst, einst)  # Wert in die Grenzen bringen
    liste = stufen(einst)  # Stufen aus der Datendatei
    for eintrag in liste:  # von der kleinsten Obergrenze aufwaerts
        if wert <= eintrag["bis"]:  # erste passende Stufe gewinnt
            return eintrag["schluessel"]  # ihre Kennung zurueckgeben
    return liste[-1]["schluessel"] if liste else ""  # ueber allen Grenzen: die oberste Stufe
