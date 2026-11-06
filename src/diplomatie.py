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


# ---------------------------------------------------------------------------
# S4-3 Vertraege (06.11.2026, Ablauf Schritt 3)
# ---------------------------------------------------------------------------
# Ein Vertrag ist ein EINTRAG AM BOT (`vertraege`: Art -> {seit, bis}), kein eigenes Objekt und
# keine zweite Rechnung. Die Zahlen stehen in `data/diplomatie.json` unter "vertraege".
# ENTSCHEIDUNG Daniel 06.11.2026, 13:50 (Register 284): der Nichtangriffspakt ist EINSEITIG -
# er sperrt Angriffe des BOTS, nicht die des Spielers; ein Spielerangriff BRIcht den Pakt.

VERTRAGSARTEN = ("nichtangriff", "handel", "durchmarsch")  # die drei Arten, die die Datei fuehrt


def _vertraege_block(einst=None) -> dict:
    """Der Block "vertraege" der Datendatei (leeres dict, wenn er fehlt)."""
    quelle = einst if isinstance(einst, dict) else daten()  # uebergebene Daten oder die Datei
    block = (quelle or {}).get("vertraege")  # den Vertragsblock heraussuchen
    return block if isinstance(block, dict) else {}  # nur ein dict ist brauchbar


def vertraege_aktiv(einst=None) -> bool:
    """Sind Vertraege eingeschaltet? Ein Wort in der Datendatei entscheidet (A-7)."""
    block = _vertraege_block(einst)  # Block holen
    return bool(block.get("aktiv", False))  # ohne ausdrueckliches true sind sie aus


def art_daten(art, einst=None) -> dict:
    """Die Zahlen EINER Vertragsart (min_gunst, dauer_sekunden, ...); leer, wenn unbekannt."""
    block = _vertraege_block(einst)  # Block holen
    eintrag = block.get(str(art))  # Eintrag dieser Art
    return eintrag if isinstance(eintrag, dict) else {}  # nur ein dict ist brauchbar


def _bot_vertraege(bot_daten) -> dict:
    """Die Vertragstabelle eines Bots - EIN Speicher am Bot (dict-Form)."""
    if not isinstance(bot_daten, dict):  # ohne dict gibt es nichts zu lesen
        return {}  # dann eine leere Tabelle (kein Absturz)
    tabelle = bot_daten.get("vertraege")  # Feld am Bot
    if not isinstance(tabelle, dict):  # altes Feld oder gar keins
        tabelle = {}  # dann eine leere Tabelle
        bot_daten["vertraege"] = tabelle  # und anlegen, damit der Aufrufer schreiben kann
    return tabelle  # die Tabelle selbst (veraenderbar)


def vertrag_aktiv(bot_daten, art, jetzt, einst=None) -> bool:
    """Laeuft diese Vertragsart gerade? Abgelaufene Eintraege werden dabei entfernt.

    Eingabe: dict des Bots, Art, Spielzeit in Sekunden. Ausgabe: True, wenn `jetzt` vor `bis` liegt.
    Ein abgelaufener Eintrag wird geloescht - so gibt es keinen zweiten Zeitbegriff und keinen
    Zustand, der still weiterlaeuft.
    """
    tabelle = _bot_vertraege(bot_daten)  # Tabelle des Bots
    eintrag = tabelle.get(str(art))  # Eintrag dieser Art
    if not isinstance(eintrag, dict):  # nichts vereinbart
        return False  # dann laeuft auch nichts
    bis = _zahl(eintrag.get("bis"), 0.0)  # Ende des Vertrags
    if float(jetzt) >= bis:  # Zeit ist um
        tabelle.pop(str(art), None)  # Eintrag entfernen (Ablauf ohne Buchung)
        return False  # dann ist er nicht mehr aktiv
    return True  # er laeuft


def vertrag_anbieten(bot_daten, art, jetzt, einst=None):
    """Bietet einem Bot eine Vertragsart an. Rueckgabe: (ok, grund).

    Geprueft wird in dieser Reihenfolge: Schalter, bekannte Art, Durchmarsch (nur Anzeige),
    Gunst gegen `min_gunst`, kein doppelter laufender Vertrag. Es wird NICHTS gebucht, wenn eine
    Bedingung fehlt - der Aufrufer bucht nur bei `True`.
    """
    if not vertraege_aktiv(einst):  # Schalter aus
        return False, "vertraege_aus"  # dann kein Angebot
    art = str(art)  # Art als Text
    if art not in VERTRAGSARTEN:  # unbekannte Art
        return False, "unbekannte_art"  # dann ablehnen
    zahlen = art_daten(art, einst)  # Zahlen dieser Art
    if not zahlen:  # Art steht nicht in der Datei
        return False, "art_ohne_daten"  # dann ablehnen statt raten
    noetig = int(_zahl(zahlen.get("min_gunst"), 100))  # noetige Gunst (Vorgabe: alles)
    gunst = gunst_von(bot_daten, einst)  # jetzige Gunst
    if gunst < noetig:  # zu wenig Gunst
        return False, "gunst_zu_niedrig"  # dann ablehnen
    if vertrag_aktiv(bot_daten, art, jetzt, einst):  # schon vereinbart
        return False, "laeuft_bereits"  # dann nicht doppelt anbieten
    dauer = _zahl(zahlen.get("dauer_sekunden"), 0.0)  # Dauer in Spielsekunden
    _bot_vertraege(bot_daten)[art] = {"seit": float(jetzt), "bis": float(jetzt) + dauer,
                                      "nur_anzeige": bool(zahlen.get("nur_anzeige", False))}
    return True, "vereinbart"  # Angebot angenommen und eingetragen


def vertraege_tick(bot_daten, jetzt, einst=None) -> list:
    """Prueft EINEN Bot: gebrochene Vertraege buchen, abgelaufene entfernen.

    Rueckgabe: Liste der Vorgaenge `[{"art", "grund", "gunst_delta", "rache_delta"}]` - der
    Aufrufer bucht die Rache, weil es den Rachetopf erst mit Schritt 4 gibt (noch kein Feld).
    Regeln: faellt die Gunst unter `bruch_unter_gunst`, bricht der Pakt (Gunst-Abzug + Rache);
    ein abgelaufener Vertrag bricht NICHT, er endet einfach.
    """
    tabelle = _bot_vertraege(bot_daten)  # Tabelle des Bots
    vorgaenge = []  # was in diesem Tick passiert ist
    grenze = int(_zahl(_vertraege_block(einst).get("bruch_unter_gunst"), 0))  # Bruchgrenze
    for art in list(tabelle):  # jede laufende Art einmal ansehen
        if not vertrag_aktiv(bot_daten, art, jetzt, einst):  # schon abgelaufen
            continue  # dann ist nichts zu tun
        zahlen = art_daten(art, einst)  # Zahlen dieser Art
        if gunst_von(bot_daten, einst) < grenze and art == "nichtangriff":  # Pakt gebrochen
            abzug = int(_zahl(zahlen.get("bruch_gunst"), 0))  # Gunst-Abzug aus der Datei
            rache = int(_zahl(zahlen.get("bruch_rache"), 0))  # Rache-Buchung aus der Datei
            tabelle.pop(art, None)  # Vertrag ist beendet
            gunst_aendern(bot_daten, abzug, "vertragsbruch", einst)  # EINMAL abziehen
            vorgaenge.append({"art": art, "grund": "vertragsbruch",  # Vorgang melden
                              "gunst_delta": abzug, "rache_delta": rache})
    return vorgaenge  # der Aufrufer bucht die Rache (Schritt 4)


def angriff_gesperrt(bot_daten, jetzt, einst=None) -> tuple:
    """Darf dieser BOT den Spieler angreifen? Rueckgabe: (gesperrt, grund).

    Das ist die EINE Stelle fuer die Vertragssperre; `punkte.angreifbar` bleibt die einzige
    Rechenstelle der Punktgrenzen (Befund G-1). Die Sperre ist eine VORBEDINGUNG, keine zweite
    Rechnung - der Aufrufer fragt beides und sperrt, wenn eine der beiden Antworten sperrt.
    """
    if not vertraege_aktiv(einst):  # Schalter aus
        return False, ""  # dann sperrt der Vertrag nichts
    if not isinstance(bot_daten, dict):  # ohne dict pruefen wir an der dict-Form des Bots
        bot_daten = {"gunst": getattr(bot_daten, "gunst", startwert(einst)),
                     "vertraege": dict(getattr(bot_daten, "vertraege", {}) or {})}
    if vertrag_aktiv(bot_daten, "nichtangriff", jetzt, einst):  # laufender Pakt
        return True, "nichtangriffspakt"  # dann kein Angriff dieses Bots
    return False, ""  # sonst frei


def pakt_brechen(bot_daten, jetzt, einst=None) -> dict:
    """Der SPIELER greift einen Bot mit Pakt an: der Pakt bricht. Rueckgabe: Buchung.

    ENTSCHEIDUNG Daniel 06.11.2026, 13:50 (Register 284): kein Verbot, sondern ein Bruch - Gunst
    sinkt um `bruch_gunst`, die Rache steigt um `bruch_rache` (gebucht vom Aufrufer, Schritt 4).
    Ohne laufenden Pakt passiert nichts (dann `{"gebrochen": False}`).
    """
    leer = {"gebrochen": False, "gunst_delta": 0, "rache_delta": 0}  # der ruhige Fall
    if not vertraege_aktiv(einst):  # Schalter aus
        return leer  # dann bricht auch nichts
    if not vertrag_aktiv(bot_daten, "nichtangriff", jetzt, einst):  # kein Pakt
        return leer  # dann nichts zu brechen
    zahlen = art_daten("nichtangriff", einst)  # Zahlen des Pakts
    abzug = int(_zahl(zahlen.get("bruch_gunst"), 0))  # Gunst-Abzug
    rache = int(_zahl(zahlen.get("bruch_rache"), 0))  # Rache-Buchung
    _bot_vertraege(bot_daten).pop("nichtangriff", None)  # Pakt ist beendet
    gunst_aendern(bot_daten, abzug, "paktbruch_durch_spieler", einst)  # EINMAL abziehen
    return {"gebrochen": True, "gunst_delta": abzug, "rache_delta": rache}  # Buchung melden


def durchmarsch_text(bot_daten, jetzt, einst=None) -> str:
    """Der Anzeigetext fuer das Durchmarschrecht - reine Anzeige, KEINE Mechanik.

    Daniels Entscheidung 06.11.2026 (Register 284): das Recht hat keine Wirkung; der Text nennt es
    darum ausdruecklich als reine Anzeige, damit niemand eine Mechanik dahinter vermutet.
    """
    if vertrag_aktiv(bot_daten, "durchmarsch", jetzt, einst):  # Recht vereinbart
        return "Durchmarsch gewaehrt (nur Anzeige - keine Mechanik)"  # Text fuer die Ansicht
    return ""  # sonst nichts anzeigen
