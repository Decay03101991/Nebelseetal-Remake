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
import wirtschaft  # S4-5: liest den Goldertrag eines Ortes (EINE Ertragsquelle)
import zeitbasis  # R3-1: die EINE Tageslaenge des Projekts (86.400 Spielsekunden)

STAND = "2026-11-07.1"  # Kennung dieses Modulstands (erscheint in keinem Spielstand)
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


def vertrag_aktiv(bot_daten, art, jetzt, einst=None, raeumen: bool = True) -> bool:
    """Laeuft diese Vertragsart gerade? Abgelaufene Eintraege werden dabei entfernt.

    Eingabe: dict des Bots, Art, Spielzeit in Sekunden. Ausgabe: True, wenn `jetzt` vor `bis` liegt.
    Ein abgelaufener Eintrag wird geloescht - so gibt es keinen zweiten Zeitbegriff und keinen
    Zustand, der still weiterlaeuft. Mit `raeumen=False` antwortet die Funktion nur, ohne den
    abgelaufenen Eintrag zu entfernen: so fragt die ANZEIGE (S4-3-Nachtrag, 08.11.2026), die beim
    Rendern nichts in den Spielstand schreiben darf.
    """
    tabelle = _bot_vertraege(bot_daten)  # Tabelle des Bots
    eintrag = tabelle.get(str(art))  # Eintrag dieser Art
    if not isinstance(eintrag, dict):  # nichts vereinbart
        return False  # dann laeuft auch nichts
    bis = _zahl(eintrag.get("bis"), 0.0)  # Ende des Vertrags
    if float(jetzt) >= bis:  # Zeit ist um
        if raeumen:  # nur der Kern raeumt auf
            tabelle.pop(str(art), None)  # Eintrag entfernen (Ablauf ohne Buchung)
            # S4-4 (06.11.2026): das ENDE bleibt gemerkt - der Rachetopf darf fruehestens
            # `nach_paktende_sekunden` nach dem Paktende feuern (Daniel 13:50).
            _ende_setzen(bot_daten, str(art), bis)  # Ende festhalten
        return False  # dann ist er nicht mehr aktiv
    return True  # er laeuft


def _vertrag_bedingungen(bot_daten, art, jetzt, einst=None) -> tuple:
    """Prueft ein Vertragsangebot, OHNE etwas zu buchen - EINE Pruefstelle fuer Kern und Anzeige.

    Rueckgabe: (ok, grund). Geprueft wird in dieser Reihenfolge: Schalter, bekannte Art, Zahlen der
    Art, Gunst gegen `min_gunst`, kein laufender Vertrag derselben Art. Die Gruende sind Kennungen;
    der Satz dazu steht in `data/diplomatie.json` unter `vertraege._gruende`
    (`vertrag_grund_text`). `vertrag_anbieten` bucht nur bei `True`, der Knopf in der Ansicht fragt
    dieselbe Funktion ueber `pakt_anbietbar` (Muster F-04: eine Rechenstelle, keine zweite Grenze
    in der Anzeige). Der Vertrag wird hier NICHT aufgeraeumt (`raeumen=False`), damit das Rendern
    den Spielstand nicht veraendert.
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
    if gunst_von(bot_daten, einst) < noetig:  # zu wenig Gunst
        return False, "gunst_zu_niedrig"  # dann ablehnen
    if vertrag_aktiv(bot_daten, art, jetzt, einst, raeumen=False):  # schon vereinbart
        return False, "laeuft_bereits"  # dann nicht doppelt anbieten
    return True, "anbietbar"  # Angebot waere moeglich


def vertrag_anbieten(bot_daten, art, jetzt, einst=None):
    """Bietet einem Bot eine Vertragsart an. Rueckgabe: (ok, grund).

    Geprueft wird in `_vertrag_bedingungen` (Schalter, bekannte Art, Durchmarsch als reine Anzeige,
    noetige Gunst aus der Datendatei, kein doppelter laufender Vertrag). Es wird NICHTS gebucht,
    wenn eine Bedingung fehlt - der Aufrufer bucht nur bei `True`.
    """
    ok, grund = _vertrag_bedingungen(bot_daten, art, jetzt, einst)  # die EINE Pruefstelle
    if not ok:  # eine Bedingung fehlt
        return False, grund  # dann nichts buchen
    zahlen = art_daten(art, einst)  # Zahlen dieser Art (oben schon geprueft)
    dauer = _zahl(zahlen.get("dauer_sekunden"), 0.0)  # Dauer in Spielsekunden
    _bot_vertraege(bot_daten)[str(art)] = {"seit": float(jetzt), "bis": float(jetzt) + dauer,
                                           "nur_anzeige": bool(zahlen.get("nur_anzeige", False))}
    return True, "vereinbart"  # Angebot angenommen und eingetragen


def pakt_anbietbar(bot_daten, jetzt, einst=None) -> tuple:
    """Darf der Spieler diesem Bot den Nichtangriffspakt anbieten? (ok, grund) fuer den Knopf.

    S4-3-Nachtrag (08.11.2026, Daniels Entscheidung 1): der Pakt hatte keinen Spielweg. Der Knopf
    in der Ansicht fragt hier - dieselbe Pruefung, die `vertrag_anbieten` beim Buchen macht, also
    keine zweite Grenze in der Oberflaeche. Nichts wird dabei gebucht.
    """
    return _vertrag_bedingungen(bot_daten, "nichtangriff", jetzt, einst)


def vertrag_grund_text(grund: str) -> str:
    """Der Satz zu einem Vertragsgrund aus `data/diplomatie.json` (leer, wenn unbekannt).

    Die Saetze stehen in der Datendatei (`vertraege._gruende`), damit keine Spielermeldung im Code
    liegt. Ein unbekannter Grund ergibt einen leeren Text - der Aufrufer erfindet dann nichts.
    """
    texte = _vertraege_block().get("_gruende")  # der Textblock der Datendatei
    if not isinstance(texte, dict):  # keine Texte hinterlegt
        return ""  # dann kein Satz
    return str(texte.get(str(grund)) or "")  # den Satz zum Grund zurueckgeben


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
            _ende_setzen(bot_daten, art, float(jetzt))  # S4-4: Ende fuer die Rache merken
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
    _ende_setzen(bot_daten, "nichtangriff", float(jetzt))  # S4-4: Ende fuer die Rache merken
    gunst_aendern(bot_daten, abzug, "paktbruch_durch_spieler", einst)  # EINMAL abziehen
    return {"gebrochen": True, "gunst_delta": abzug, "rache_delta": rache}  # Buchung melden


def durchmarsch_text(bot_daten, jetzt, einst=None) -> str:
    """Der Anzeigetext fuer das Durchmarschrecht - reine Anzeige, KEINE Mechanik.

    Daniels Entscheidung 06.11.2026 (Register 284): das Recht hat keine Wirkung; der Text nennt es
    darum ausdruecklich als reine Anzeige, damit niemand eine Mechanik dahinter vermutet.
    """
    if not vertrag_aktiv(bot_daten, "durchmarsch", jetzt, einst):  # kein Recht vereinbart
        return ""  # dann nichts anzeigen
    # Der Text steht in der Datendatei (Regel: kein Spieltext im Code). Fehlt er, wird nichts
    # erfunden - dann bleibt die Zeile leer.
    return str(art_daten("durchmarsch", einst).get("text") or "")  # Text aus data/diplomatie.json

# ---------------------------------------------------------------------------
# S4-4 Rachetopf (06.11.2026, Ablauf Schritt 4)
# ---------------------------------------------------------------------------
# EIN Topf je Bot. Niederlagen und Funkstille fuellen ihn; ab `schwelle` folgt GENAU EINE
# Ankuendigung, angegriffen wird erst ab `armee_sk` Schlagkraft - und nie waehrend eines Pakts.
# Ablage: der Topf steht als Feld `rache` am Bot; `letzter_kontakt`, `rache_tag_nr` und
# `rache_ankuendigung` liegen im GEDaeCHTNIS des Bots (dieselbe Tabelle wie seine Taktik-Erinnerung,
# damit kein drittes Feld entsteht). Alle Zahlen stehen in `data/diplomatie.json` unter "rache".


def _rache_block(einst=None) -> dict:
    """Der Block "rache" der Datendatei (leeres dict, wenn er fehlt)."""
    quelle = einst if isinstance(einst, dict) else daten()  # uebergebene Daten oder die Datei lesen
    block = (quelle or {}).get("rache")  # den Rache-Block heraussuchen
    return block if isinstance(block, dict) else {}  # nur ein dict ist brauchbar


def _block_zahl(block: dict, name: str, standard: float) -> float:
    """Eine Zahl aus dem Rache-Block; Unbrauchbares ergibt den Standardwert."""
    return _zahl((block or {}).get(name), standard)  # ueber `_zahl` (bool zaehlt nicht als Zahl)


def rache_aktiv(einst=None) -> bool:
    """Ist der Rachetopf eingeschaltet? Ein Wort in der Datendatei entscheidet (A-7)."""
    return bool(_rache_block(einst).get("aktiv", False))  # ohne ausdrueckliches true ist er aus


def rache_von(bot_daten, einst=None) -> int:
    """Der aktuelle Topf eines Bots, geklemmt auf 0..hoechstwert.

    Eingabe: dict (Form aus `bot_als_dict`) oder ein Bot-Objekt. Ausgabe: ganze Zahl.
    """
    block = _rache_block(einst)  # Zahlen holen
    oben = int(_block_zahl(block, "hoechstwert", 5))  # Obergrenze des Topfs
    roh = bot_daten.get("rache", 0) if isinstance(bot_daten, dict) else getattr(bot_daten, "rache", 0)
    return max(0, min(oben, int(_zahl(roh, 0))))  # in 0..hoechstwert einschliessen


def rache_setzen(bot_daten, wert, einst=None) -> int:
    """Setzt den Topf (geklemmt) und gibt den tatsaechlichen Wert zurueck."""
    oben = int(_block_zahl(_rache_block(einst), "hoechstwert", 5))  # Obergrenze lesen
    neu = max(0, min(oben, int(_zahl(wert, 0))))  # Wert in die Grenzen bringen
    if isinstance(bot_daten, dict):  # nur ein dict kann beschrieben werden
        bot_daten["rache"] = neu  # EIN Speicher: das Feld am Bot
    return neu  # Aufrufer bekommt den echten Wert


def rache_buchen(bot_daten, grund="niederlage", einst=None) -> int:
    """Erhoeht den Topf um `je_niederlage` (eine Niederlage oder ein Tag Funkstille).

    Eingabe: dict des Bots, Grund als Text (nur fuer den Aufrufer - er wird NICHT gespeichert).
    Ausgabe: der neue Topf.
    """
    schritt = int(_block_zahl(_rache_block(einst), "je_niederlage", 1))  # Zuwachs aus der Datei
    return rache_setzen(bot_daten, rache_von(bot_daten, einst) + schritt, einst)  # addieren, klemmen


def rache_nach_sieg(bot_daten, einst=None) -> int:
    """Nach einem gewonnenen Bot-Angriff faellt der Topf auf `nach_bot_sieg` (Daniel, F-3)."""
    wert = int(_block_zahl(_rache_block(einst), "nach_bot_sieg", 0))  # Zielwert aus der Datei
    return rache_setzen(bot_daten, wert, einst)  # setzen (meist 0)


def _gedaechtnis(bot_daten) -> dict:
    """Das Gedaechtnis des Bots als dict - wird bei Bedarf angelegt (kein Absturz)."""
    if not isinstance(bot_daten, dict):  # ohne dict gibt es kein Gedaechtnis
        return {}  # dann eine leere Tabelle
    ged = bot_daten.get("gedaechtnis")  # Feld ansehen
    if not isinstance(ged, dict):  # altes Feld oder gar keins
        ged = {}  # dann eine leere Tabelle
        bot_daten["gedaechtnis"] = ged  # und anlegen, damit der Aufrufer schreiben kann
    return ged  # die Tabelle selbst (veraenderbar)


def kontakt_buchen(bot_daten, jetzt, einst=None) -> float:
    """Merkt eine Interaktion mit dem Bot (Handel, Geschenk, Kampf, Ereignis).

    Daniels Entscheidung 06.11.2026, 13:50 (Register 284): Kontakt ist JEDE Interaktion. Wer den Bot
    beschenkt oder mit ihm handelt, haelt den Topf ruhig - darum setzt jeder Kontakt den Zaehler neu.
    """
    ged = _gedaechtnis(bot_daten)  # Gedaechtnis holen
    ged["letzter_kontakt"] = float(jetzt)  # Zeitpunkt der Interaktion
    return float(jetzt)  # Aufrufer bekommt den Wert zurueck


def letzter_kontakt(bot_daten, einst=None) -> float:
    """Spielzeit der letzten Interaktion; 0.0 heisst: noch keine."""
    if not isinstance(bot_daten, dict):  # ohne dict nichts zu lesen
        return 0.0  # dann keine Interaktion
    ged = bot_daten.get("gedaechtnis")  # Gedaechtnis ansehen
    if not isinstance(ged, dict):  # kein brauchbares Gedaechtnis
        return 0.0  # dann keine Interaktion
    return float(_zahl(ged.get("letzter_kontakt"), 0.0))  # Zeitpunkt zurueckgeben


def rache_tag(bot_daten, jetzt, goetterschutz=False, einst=None) -> int:
    """Ein Spieltag ohne Kontakt fuellt den Topf um 1 - hoechstens EINMAL je Spieltag.

    Eingabe: dict des Bots, Spielzeit, ob der Goetterschutz laeuft.
    Ausgabe: der Topf danach. Unter Goetterschutz ruht der Topf (VORSCHLAG, Befund G-1); unter
    einem Pakt steigt er WEITER (Daniel 13:50: der Pakt kauft Zeit, nicht Ruhe).
    """
    if not rache_aktiv(einst):  # Schalter aus
        return rache_von(bot_daten, einst)  # dann nichts buchen
    block = _rache_block(einst)  # Zahlen holen
    if goetterschutz and bool(block.get("ruht_unter_goetterschutz", True)):  # Schutz laeuft
        return rache_von(bot_daten, einst)  # dann ruht der Topf
    tag_sekunden = max(1.0, float(zeitbasis.SEKUNDEN_JE_TAG))  # Laenge eines Spieltags (EINE Quelle, R3-1)
    tag = int(float(jetzt) // tag_sekunden)  # laufende Spieltag-Nummer
    ged = _gedaechtnis(bot_daten)  # Gedaechtnis holen
    if int(_zahl(ged.get("rache_tag_nr"), -1)) == tag:  # dieser Tag ist schon gebucht
        return rache_von(bot_daten, einst)  # dann kein zweiter Punkt am selben Tag
    ged["rache_tag_nr"] = tag  # Tag als gebucht merken
    letzter = letzter_kontakt(bot_daten, einst)  # letzte Interaktion
    if letzter > 0 and float(jetzt) - letzter < tag_sekunden:  # Kontakt innerhalb des Tages
        return rache_von(bot_daten, einst)  # dann keine Funkstille
    return rache_buchen(bot_daten, "funkstille", einst)  # sonst einen Punkt buchen


def _ende_setzen(bot_daten, art, wert) -> None:
    """Merkt, WANN ein Vertrag geendet hat (fuer den Vorlauf nach dem Paktende)."""
    if not isinstance(bot_daten, dict):  # ohne dict nichts zu merken
        return  # dann fertig
    tabelle = bot_daten.get("vertrag_ende")  # Feld ansehen
    if not isinstance(tabelle, dict):  # altes Feld oder gar keins
        tabelle = {}  # dann eine leere Tabelle
        bot_daten["vertrag_ende"] = tabelle  # und anlegen
    tabelle[str(art)] = float(_zahl(wert, 0.0))  # Ende dieser Art festhalten


def vertrag_ende(bot_daten, art, einst=None):
    """Spielzeit, zu der diese Vertragsart geendet hat - `None`, wenn sie nie lief."""
    if not isinstance(bot_daten, dict):  # ohne dict nichts zu lesen
        return None  # dann unbekannt
    tabelle = bot_daten.get("vertrag_ende")  # Feld ansehen
    if not isinstance(tabelle, dict) or str(art) not in tabelle:  # kein Ende vermerkt
        return None  # dann unbekannt
    return float(_zahl(tabelle.get(str(art)), 0.0))  # Zeitpunkt zurueckgeben


def rache_bereit(bot_daten, armee_sk, jetzt, einst=None) -> bool:
    """Darf dieser Bot jetzt aus Rache angreifen? Rueckgabe: True/False.

    Vier Bedingungen, jede aus der Datendatei: Topf mindestens `schwelle`, Armee mindestens
    `armee_sk` Schlagkraft, KEIN laufender Nichtangriffspakt und mindestens `nach_paktende_sekunden`
    seit dem Ende des letzten Pakts.
    """
    if not rache_aktiv(einst):  # Schalter aus
        return False  # dann kein Racheangriff
    block = _rache_block(einst)  # Zahlen holen
    if rache_von(bot_daten, einst) < int(_block_zahl(block, "schwelle", 3)):  # Topf zu klein
        return False  # dann noch nicht
    if float(_zahl(armee_sk, 0.0)) < _block_zahl(block, "armee_sk", 99.0):  # Armee zu schwach
        return False  # dann kein Angriff (die Armee kommt zuerst)
    if vertrag_aktiv(bot_daten, "nichtangriff", jetzt, einst):  # Pakt laeuft noch
        return False  # dann kein Angriff (Daniel 13:50)
    ende = vertrag_ende(bot_daten, "nichtangriff", einst)  # wann endete der letzte Pakt?
    if ende is not None:  # es gab einen Pakt
        if float(jetzt) < ende + _block_zahl(block, "nach_paktende_sekunden", float(zeitbasis.SEKUNDEN_JE_TAG)):  # zu frueh
            return False  # dann erst nach dem Vorlauf
    return True  # alle Bedingungen erfuellt


def vorlauf_sekunden(einst=None) -> float:
    """Wartezeit zwischen Ankuendigung und Angriff (aus der Datendatei, Vorgabe 1 Spieltag)."""
    return _block_zahl(_rache_block(einst), "vorlauf_sekunden", float(zeitbasis.SEKUNDEN_JE_TAG))  # Zahl aus data/diplomatie.json


def ankuendigung_text(bot_daten, einst=None) -> str:
    """Der Drohbrief-Text zur jetzigen Topfstufe - oder "", wenn die Datei keinen nennt."""
    block = _rache_block(einst)  # Zahlen holen
    texte = block.get("ankuendigung")  # Textliste ansehen
    if not isinstance(texte, list) or not texte:  # keine Texte hinterlegt
        return ""  # dann nichts erfinden
    topf = rache_von(bot_daten, einst)  # jetzige Stufe
    stufe = max(1, min(len(texte), topf))  # Stufe 1 bis Anzahl der Texte
    return str(texte[stufe - 1])  # Text dieser Stufe

# ---------------------------------------------------------------------------
# S4-5 Ereignisse: Haug, Grom, Silra (06.11.2026, Ablauf Schritt 5)
# ---------------------------------------------------------------------------
# Drei Bot-Ereignisse mit Frist. Die Zahlen (Preise, Frist, Haeufigkeit, Gunstwirkung) stehen in
# `data/diplomatie.json` unter "ereignisse"; jeder sichtbare Satz steht in `data/story.json` unter
# "ereignisse". Dieses Modul rechnet und bucht - es entscheidet nichts und zeigt nichts an.
#
# EIN Speicher: die offenen Ereignisse liegen als Liste [{id, art, bot, erzeugt, frist}] im
# Spielstand (GameState.ereignisse). Der Preis steht NICHT im Eintrag, sondern wird bei jeder Frage
# neu aus der Datendatei und dem ZAHLENDEN ORT gerechnet - eine Rechenstelle fuer Anzeige und
# Buchung (Muster F-04): `ereignis_preis`.


def _ereignisse_block(einst=None) -> dict:
    """Der Block "ereignisse" der Datendatei (leeres dict, wenn er fehlt)."""
    quelle = einst if isinstance(einst, dict) else daten()  # uebergebene Daten oder die Datei lesen
    block = (quelle or {}).get("ereignisse")  # den Ereignis-Block heraussuchen
    return block if isinstance(block, dict) else {}  # nur ein dict ist brauchbar


def ereignisse_aktiv(einst=None) -> bool:
    """Sind Ereignisse eingeschaltet? Ein Wort in der Datendatei entscheidet (A-7)."""
    return bool(_ereignisse_block(einst).get("aktiv", False))  # ohne ausdrueckliches true sind sie aus


def ereignis_arten(einst=None) -> list:
    """Die Ereignisarten der Datei in ihrer Reihenfolge (Liste der Kennungen).

    Ausgabe: Liste von Kennungen, z. B. ["haug", "grom", "silra"]; leer, wenn die Datei keine nennt.
    Die Reihenfolge ist nur noch die ANZEIGE-Reihenfolge - zugeordnet wird ueber den Botnamen
    (`ereignis_art_fuer_bot`), nicht ueber den Index (R3-2, Befund I-1).
    """
    arten = _ereignisse_block(einst).get("arten")  # Arten-Block ansehen
    if not isinstance(arten, dict):  # keine Arten hinterlegt
        return []  # dann gibt es nichts zu erzeugen
    return [str(k) for k, v in arten.items() if isinstance(v, dict)]  # nur Arten MIT Angaben


def _normal(text) -> str:
    """Ein Name fuer den Vergleich: ohne Leerraum an den Raendern, in Kleinschreibung."""
    return str(text or "").strip().casefold()  # " Haug " und "haug" sind derselbe Bot


def ereignis_art_fuer_bot(bot, einst=None) -> str:
    """Die Ereignisart, die zu DIESEM Bot gehoert - oder "" (dieser Bot hat kein Ereignis).

    Befund I-1 (dritte Modellrunde, geprueft 07.11.2026): der Takt waehlte die Art ueber den
    Bot-INDEX (`_index % len(_arten)`). Damit bekam der zweite Bot die zweite Art, egal wie er
    heisst - die Meldung las dann "Brynhild: Grom braucht Messer". Die Art haengt jetzt am NAMEN:
    gesucht wird die Art, deren Feld `name` dem Botnamen entspricht (fehlt `name`, gilt der
    Schluessel selbst). Ein Bot ohne passende Art bekommt KEIN Ereignis - nichts erfinden.
    """
    name = _normal(bot.get("name") if isinstance(bot, dict) else getattr(bot, "name", ""))  # Botname
    if not name:  # ohne Namen nicht zuordenbar
        return ""  # dann kein Ereignis
    arten = _ereignisse_block(einst).get("arten")  # Arten-Block der Datei
    if not isinstance(arten, dict):  # keine Arten hinterlegt
        return ""  # dann kein Ereignis
    for art, angaben in arten.items():  # jede Art ansehen
        if not isinstance(angaben, dict):  # unbrauchbarer Eintrag
            continue  # dann weiter
        if _normal(angaben.get("name") or art) == name:  # Name passt (Rueckfall: Schluessel)
            return str(art)  # diese Art gehoert dem Bot
    return ""  # kein Treffer: dieser Bot hat kein Ereignis


def ereignis_daten(art, einst=None) -> dict:
    """Die Angaben EINER Ereignisart (Zahlungen, Gegenleistung); leer, wenn die Datei sie nicht fuehrt."""
    arten = _ereignisse_block(einst).get("arten")  # Arten-Block ansehen
    eintrag = arten.get(str(art)) if isinstance(arten, dict) else None  # Eintrag dieser Art
    return eintrag if isinstance(eintrag, dict) else {}  # nur ein dict ist brauchbar


def ereignis_frist(einst=None) -> float:
    """Frist eines Ereignisses in Spielsekunden (Vorgabe zwei Spieltage = 2 x 86.400 s, R3-1)."""
    return _block_zahl(_ereignisse_block(einst), "frist_sekunden", 2 * float(zeitbasis.SEKUNDEN_JE_TAG))  # Zahl aus der Datei


def ereignis_haeufigkeit(einst=None) -> float:
    """Mindestabstand zweier Ereignisse desselben Bots in Spielsekunden (Vorgabe drei Spieltage)."""
    return _block_zahl(_ereignisse_block(einst), "haeufigkeit_sekunden", 3 * float(zeitbasis.SEKUNDEN_JE_TAG))  # Zahl aus der Datei


def ereignis_gunst_annahme(einst=None) -> int:
    """Gunstwirkung einer Annahme (Vorgabe +5)."""
    return int(_block_zahl(_ereignisse_block(einst), "gunst_annahme", 5.0))  # ganze Zahl aus der Datei


def ereignis_gunst_ablehnung(einst=None) -> int:
    """Gunstwirkung einer Ablehnung ODER eines Ablaufs (Vorgabe -5)."""
    return int(_block_zahl(_ereignisse_block(einst), "gunst_ablehnung", -5.0))  # Zahl aus der Datei


def _ort_lager(ort, name) -> dict:
    """Liest ein Lager eines Ortes (`vorraete` oder `waren`) - Objekt ODER dict, nie None.

    Ohne dieses Lesen muesste jede Buchstelle selbst zwischen Settlement-Objekt und dict
    unterscheiden; genau daraus entstehen zwei Wahrheiten ueber denselben Bestand.
    """
    if isinstance(ort, dict):  # dict-Form (Pruefungen, Kern)
        lager = ort.get(name)  # Lager aus dem dict holen
    else:  # Settlement-Objekt des Spiels
        lager = getattr(ort, name, None)  # Lager als Feld lesen
    return lager if isinstance(lager, dict) else {}  # nur ein dict ist brauchbar


def _lager_setzen(ort, name, bestand) -> None:
    """Schreibt ein Lager zurueck - in ein Objekt oder ein dict; ohne Ziel passiert nichts."""
    if isinstance(ort, dict):  # dict-Form
        ort[name] = dict(bestand)  # Lager als Schluessel setzen
    elif ort is not None:  # Settlement-Objekt
        setattr(ort, name, dict(bestand))  # Lager als Feld setzen


def _rohstoff_name(kennung) -> str:
    """Anzeigename eines Rohstoffs aus `data/resources.json`; ohne Eintrag die Kennung selbst."""
    for eintrag in (spieldaten.rohstoffe() or []):  # die EINE Lesestelle der neun Rohstoffe
        if str(eintrag.get("id")) == str(kennung):  # passende Kennung gefunden
            return str(eintrag.get("name") or kennung)  # Anzeigename zurueckgeben
    return str(kennung)  # sonst die Kennung selbst - nichts erfinden


def _zahl_lesbar(menge) -> str:
    """Eine Menge lesbar machen: 990.0 -> "990", 1.5 -> "1.5" (keine erfundene Rundung)."""
    zahl = float(_zahl(menge, 0.0))  # Zahl werden lassen (Unbrauchbares wird 0)
    if zahl.is_integer():  # ganze Menge
        return str(int(zahl))  # ohne Nachkommastellen
    return ("%.2f" % zahl).rstrip("0").rstrip(".")  # sonst hoechstens zwei Stellen, ohne Nullen


def gold_tagesertrag(ort, einst=None) -> float:
    """Der Goldertrag eines Ortes an EINEM Spieltag (Stundenertrag x Zeitraum aus der Datei).

    Der Ertrag kommt aus `wirtschaft.siedlung_ertrag` - derselben Funktion, die Dorfuebersicht und
    Kopfzeile lesen. Kein zweiter Rechenweg fuer denselben Ertrag (Befund G-3: die Zahl muss
    nachrechenbar bleiben).
    """
    stunden = _block_zahl(_ereignisse_block(einst), "ertrag_zeitraum_stunden", 24.0)  # Zeitraum
    ertrag = wirtschaft.siedlung_ertrag(ort) if ort is not None else {}  # Stundenertrag des Ortes
    return float(_zahl((ertrag or {}).get("gold"), 0.0)) * stunden  # Gold je Stunde mal Zeitraum


def _menge(wert, tagesertrag) -> float:
    """Loest einen Betrag aus der Datei auf: feste Zahl ODER Anteil vom Tagesertrag.

    Eingabe: Zahl oder dict {"anteil_vom_ertrag": 0.1, "mindest": 1}.
    Ausgabe: Menge als float. Ein Anteil wird ABGERUNDET (V-4: 128 Gold am Tag ergeben 12, nicht
    13) und danach auf `mindest` angehoben - so steht es in der Quelle.
    """
    if isinstance(wert, dict):  # Anteil statt fester Zahl
        anteil = _zahl(wert.get("anteil_vom_ertrag"), 0.0)  # Anteil des Tagesertrags
        mindest = _zahl(wert.get("mindest"), 0.0)  # Untergrenze aus der Datei
        return max(mindest, float(int(anteil * float(tagesertrag))))  # abrunden, dann anheben
    return float(_zahl(wert, 0.0))  # feste Menge aus der Datei


def ereignis_preis(art, ort=None, einst=None) -> list:
    """Die moeglichen Zahlungen einer Ereignisart, aufgeloest fuer DIESEN Ort.

    Eingabe: Art, Ort (Settlement-Objekt oder dict) und optionale Daten.
    Ausgabe: Liste von Zahlungen; jede ist ein dict {"rohstoffe": {...}, "waren": {...}}.
    Das ist die EINE Preisfunktion - Anzeige und Buchung fragen BEIDE hier (Muster F-04).
    """
    angaben = ereignis_daten(art, einst)  # Angaben dieser Art
    tagesertrag = gold_tagesertrag(ort, einst)  # Gold-Tagesertrag des zahlenden Ortes
    ergebnis = []  # die aufgeloesten Zahlungswege
    for eintrag in (angaben.get("zahlungen") or []):  # jeden angebotenen Weg einmal
        if not isinstance(eintrag, dict):  # unbrauchbarer Eintrag
            continue  # dann ueberspringen statt raten
        zahlung = {"rohstoffe": {}, "waren": {}}  # eine Zahlung kann beide Lager treffen
        for lager in ("rohstoffe", "waren"):  # beide Lager durchgehen
            betraege = eintrag.get(lager)  # Betraege dieses Lagers
            if not isinstance(betraege, dict):  # nichts in diesem Lager
                continue  # dann weiter mit dem anderen Lager
            for kennung, wert in betraege.items():  # jede Position einzeln
                zahlung[lager][str(kennung)] = _menge(wert, tagesertrag)  # Betrag aufloesen
        if zahlung["rohstoffe"] or zahlung["waren"]:  # nur eine ECHTE Zahlung aufnehmen
            ergebnis.append(zahlung)  # Weg an die Liste
    return ergebnis  # alle Wege, die die Datei anbietet


def ereignis_gegenleistung(art, einst=None) -> dict:
    """Was der Spieler bei einer Annahme bekommt (dict mit "rohstoffe"/"waren"; leer = nichts)."""
    roh = ereignis_daten(art, einst).get("gegenleistung")  # Angaben der Gegenleistung
    ergebnis = {"rohstoffe": {}, "waren": {}}  # beide Lager, damit keine Stelle raten muss
    if not isinstance(roh, dict):  # keine Gegenleistung vereinbart
        return ergebnis  # dann bleibt beides leer
    for lager in ("rohstoffe", "waren"):  # beide Lager durchgehen
        betraege = roh.get(lager)  # Betraege dieses Lagers
        if isinstance(betraege, dict):  # brauchbare Angaben
            ergebnis[lager] = {str(k): float(_zahl(v, 0.0)) for k, v in betraege.items()}  # fest
    return ergebnis  # die Gegenleistung in beiden Lagern


def ereignis_weg_text(art, index, ort=None, einst=None) -> str:
    """Der Text EINES Zahlungswegs, z. B. "990 Holz" oder "5 Messer" ("" wenn es ihn nicht gibt).

    Zahlen kommen aus `_zahl_lesbar`, Rohstoffnamen aus `data/resources.json`, Warennamen sind die
    Kennungen aus `data/items.json`. Kein Spieltext im Code.
    """
    block = _ereignisse_block(einst)  # fuer den Positions-Trenner
    trenner_pos = str(block.get("trenner_position") or " + ")  # Trenner zwischen zwei Positionen
    optionen = ereignis_preis(art, ort, einst)  # alle Wege, EINE Rechenstelle
    if not isinstance(index, int) or isinstance(index, bool):  # kein brauchbarer Index
        return ""  # dann kein Text
    if index < 0 or index >= len(optionen):  # Weg gibt es nicht
        return ""  # dann kein Text
    zahlung = optionen[index]  # der gewuenschte Weg
    stuecke = []  # je Position ein Stueck
    for kennung, menge in list(zahlung["rohstoffe"].items()):  # Rohstoffe zuerst
        stuecke.append("%s %s" % (_zahl_lesbar(menge), _rohstoff_name(kennung)))  # "990 Holz"
    for kennung, menge in list(zahlung["waren"].items()):  # dann die Werkstattwaren
        stuecke.append("%s %s" % (_zahl_lesbar(menge), str(kennung)))  # "5 Messer"
    return trenner_pos.join(stuecke)  # Positionen dieses Weges verbinden


def ereignis_preis_text(art, ort=None, einst=None) -> str:
    """Die Zahlungen als lesbarer Satz, z. B. "990 Holz oder 64 Gold".

    Der Trenner zwischen zwei Wegen kommt aus der Datendatei ("trenner") - kein Anzeigetext im
    Code. Die einzelnen Wege baut `ereignis_weg_text` (dieselbe Zeichenregel wie die Knoepfe).
    """
    trenner = str(_ereignisse_block(einst).get("trenner") or " / ")  # Trenner zwischen zwei Wegen
    anzahl = len(ereignis_preis(art, ort, einst))  # wie viele Wege die Datei anbietet
    teile = []  # je Weg ein Teil
    for index in range(anzahl):  # jeden Weg einmal
        stueck = ereignis_weg_text(art, index, ort, einst)  # Text dieses Weges
        if stueck:  # nur einen echten Weg zeigen
            teile.append(stueck)  # Weg an die Liste
    return trenner.join(teile)  # die Wege mit dem Trenner verbinden


def _bezahlbar(zahlung, ort) -> bool:
    """Sind ALLE Positionen einer Zahlung am Ort vorhanden (beide Lager, atomar geprueft)?"""
    for lager in ("rohstoffe", "waren"):  # beide Lager durchgehen
        feld = "vorraete" if lager == "rohstoffe" else "waren"  # Feldname am Ort
        bestand = _ort_lager(ort, feld)  # Lager des Ortes lesen
        for kennung, menge in (zahlung.get(lager) or {}).items():  # jede Position einzeln
            if float(_zahl(bestand.get(kennung), 0.0)) < float(menge):  # zu wenig am Ort
                return False  # dann ist die Zahlung nicht moeglich
    return True  # alle Positionen sind gedeckt


def ereignis_finden(daten, kennung) -> dict:
    """Das Ereignis mit dieser Kennung - {} wenn es keines gibt (kein Absturz)."""
    for eintrag in (daten or []):  # die offene Liste durchgehen
        if isinstance(eintrag, dict) and str(eintrag.get("id")) == str(kennung):  # Kennung passt
            return eintrag  # gefunden
    return {}  # keines mit dieser Kennung


def ereignis_offen_fuer(daten, bot_name, einst=None) -> dict:
    """Das offene Ereignis EINES Bots - {} wenn keines laeuft (hoechstens EINES je Bot)."""
    for eintrag in (daten or []):  # die offene Liste durchgehen
        if isinstance(eintrag, dict) and str(eintrag.get("bot")) == str(bot_name):  # dieser Bot
            return eintrag  # das erste offene Ereignis dieses Bots
    return {}  # nichts offen


def ereignis_erzeugen(daten, bot, art, jetzt, einst=None) -> dict:
    """Legt EIN Ereignis fuer EINEN Bot an. Rueckgabe: der Eintrag oder {} (nichts angelegt).

    Geprueft wird in dieser Reihenfolge: Schalter, bekannte Art, kein zweites offenes Ereignis,
    Haeufigkeit (Abstand seit dem letzten Ereignis dieses Bots). Fehlt eine Bedingung, wird NICHTS
    angelegt - der Aufrufer meldet nur, was wirklich entstanden ist.
    """
    leer = {}  # der ruhige Fall
    if not ereignisse_aktiv(einst):  # Schalter aus
        return leer  # dann kein Ereignis
    if not isinstance(daten, list) or not isinstance(bot, dict):  # ohne Liste und Bot kein Ereignis
        return leer  # dann nichts anlegen
    art = str(art)  # Art als Text
    if not ereignis_daten(art, einst):  # Art steht nicht in der Datei
        return leer  # dann nichts erfinden
    name = str(bot.get("name") or "")  # Name des Bots
    if not name:  # ohne Namen laesst sich das Ereignis nicht zuordnen
        return leer  # dann kein Ereignis
    if ereignis_offen_fuer(daten, name, einst):  # schon eines offen
        return leer  # dann kein zweites
    ged = _gedaechtnis(bot)  # Gedaechtnis des Bots (legt es bei Bedarf an)
    letzte = _zahl(ged.get("ereignis_seit"), 0.0)  # Spielzeit des letzten Ereignisses (0 = keins)
    if float(jetzt) - letzte < ereignis_haeufigkeit(einst):  # Abstand noch nicht erreicht
        return leer  # dann erst nach der Haeufigkeitsfrist (auch das ERSTE wartet sie ab)
    eintrag = {"id": "%s-%d-%d" % (art, int(float(jetzt)), len(daten)),  # eindeutige Kennung
               "art": art, "bot": name,  # Art und Besitzer
               "erzeugt": float(jetzt),  # Spielzeit der Entstehung
               "frist": float(jetzt) + ereignis_frist(einst)}  # Spielzeit des Ablaufs
    daten.append(eintrag)  # EIN Speicher: die Liste im Spielstand
    ged["ereignis_seit"] = float(jetzt)  # Haeufigkeit ab jetzt rechnen
    return eintrag  # der neue Eintrag


def _zahlung_waehlen(optionen, ort, zahlung) -> int:
    """Waehlt den Zahlungsweg: den verlangten (Index oder dict) oder den ERSTEN bezahlbaren.

    Ausgabe: Index in `optionen`; -1, wenn es keinen Weg gibt. Ohne Wunsch wird der erste
    bezahlbare genommen (der Spieler waehlt in der Anzeige, das Kern-Urteil bleibt dasselbe).
    """
    if not optionen:  # keine Zahlungswege
        return -1  # dann nichts zu waehlen
    if isinstance(zahlung, bool):  # ein Wahrheitswert ist kein Index
        zahlung = None  # dann wie "kein Wunsch" behandeln
    if isinstance(zahlung, int) and 0 <= zahlung < len(optionen):  # Index aus der Anzeige
        return zahlung  # genau dieser Weg
    if isinstance(zahlung, dict):  # ein Weg als dict
        for i, option in enumerate(optionen):  # die Wege vergleichen
            if option == zahlung:  # identischer Weg
                return i  # gefunden
        return -1  # so einen Weg gibt es nicht
    for i, option in enumerate(optionen):  # ohne Wunsch: der erste bezahlbare Weg
        if _bezahlbar(option, ort):  # dieser Weg ist gedeckt
            return i  # dann diesen nehmen
    return 0  # nichts gedeckt: der erste Weg wird versucht (die Buchung sagt dann ehrlich ab)


def ereignis_annehmen(daten, ort, kennung, bot, jetzt=None, zahlung=None, einst=None):
    """Nimmt ein Ereignis an und bucht ATOMAR am Ort. Rueckgabe: (ok, grund).

    Reihenfolge: Schalter, Ereignis vorhanden, nicht abgelaufen, Zahlungsweg, Bestand am ORT.
    Fehlt etwas, wird NICHTS gebucht und das Ereignis bleibt offen (keine Teilbuchung).
    Bei Erfolg: Zahlung abziehen, Gegenleistung gutschreiben, Ereignis entfernen, Gunst +5 und
    Kontakt buchen (Daniel 13:50: Kontakt = jede Interaktion).
    """
    if not ereignisse_aktiv(einst):  # Schalter aus
        return False, "ereignisse_aus"  # dann keine Annahme
    eintrag = ereignis_finden(daten, kennung)  # Ereignis suchen
    if not eintrag:  # gibt es nicht (mehr)
        return False, "unbekannt"  # dann ablehnen
    if jetzt is not None and float(jetzt) >= float(_zahl(eintrag.get("frist"), 0.0)):  # Frist um
        return False, "abgelaufen"  # dann nicht mehr annehmen
    if ort is None:  # ohne Ort gibt es kein Lager
        return False, "kein_ort"  # dann nicht buchen
    art = str(eintrag.get("art") or "")  # Art des Ereignisses
    optionen = ereignis_preis(art, ort, einst)  # die EINE Preisfunktion
    index = _zahlung_waehlen(optionen, ort, zahlung)  # Weg waehlen
    if index < 0:  # kein Weg vorhanden
        return False, "kein_preis"  # dann nicht buchen
    gewaehlt = optionen[index]  # der gewaehlte Weg
    if not _bezahlbar(gewaehlt, ort):  # Bestand am Ort reicht nicht
        return False, "bestand_fehlt"  # dann NICHTS buchen (atomar)
    gegen = ereignis_gegenleistung(art, einst)  # was zurueckkommt
    neu = {}  # die neuen Lager, erst rechnen, dann einsetzen
    for lager, feld in (("rohstoffe", "vorraete"), ("waren", "waren")):  # beide Lager
        bestand = dict(_ort_lager(ort, feld))  # Kopie des Lagers
        for kennung_x, menge in (gewaehlt.get(lager) or {}).items():  # die Zahlung abbuchen
            bestand[kennung_x] = float(_zahl(bestand.get(kennung_x), 0.0)) - float(menge)  # minus
        for kennung_x, menge in (gegen.get(lager) or {}).items():  # die Gegenleistung gutschreiben
            bestand[kennung_x] = float(_zahl(bestand.get(kennung_x), 0.0)) + float(menge)  # plus
        neu[feld] = bestand  # neues Lager merken
    _lager_setzen(ort, "vorraete", neu["vorraete"])  # Rohstofflager einsetzen
    _lager_setzen(ort, "waren", neu["waren"])  # Warenlager einsetzen
    daten.remove(eintrag)  # Ereignis ist erledigt
    gunst_aendern(bot, ereignis_gunst_annahme(einst), "ereignis_annahme", einst)  # Gunst +5
    kontakt_buchen(bot, float(jetzt) if jetzt is not None else 0.0, einst)  # Interaktion zaehlt
    return True, "angenommen"  # gebucht


def ereignis_ablehnen(daten, kennung, bot, jetzt=None, einst=None):
    """Lehnt ein Ereignis ab: Gunst -5, Ereignis weg, Kontakt gebucht. Rueckgabe: (ok, grund)."""
    if not ereignisse_aktiv(einst):  # Schalter aus
        return False, "ereignisse_aus"  # dann nichts tun
    eintrag = ereignis_finden(daten, kennung)  # Ereignis suchen
    if not eintrag:  # gibt es nicht (mehr)
        return False, "unbekannt"  # dann ablehnen
    daten.remove(eintrag)  # Ereignis ist erledigt
    gunst_aendern(bot, ereignis_gunst_ablehnung(einst), "ereignis_ablehnung", einst)  # Gunst -5
    kontakt_buchen(bot, float(jetzt) if jetzt is not None else 0.0, einst)  # Interaktion zaehlt
    return True, "abgelehnt"  # gebucht


def ereignisse_tick(daten, jetzt, bots=None, einst=None) -> list:
    """Laesst abgelaufene Ereignisse verfallen (Frist um, Gunst -5). Rueckgabe: die Vorgaenge.

    Eingabe: die Ereignisliste des Spielstands, die Spielzeit, optional die Bot-dicts (dann wird
    die Gunst HIER gebucht) und optionale Daten.
    Ausgabe: Liste [{"id", "art", "bot", "gunst_delta"}]; leer, wenn nichts abgelaufen ist.
    Ein abgelaufenes Ereignis kann nicht mehr angenommen werden - es verschwindet in diesem Tick.
    """
    vorgaenge = []  # was dieser Tick verfallen laesst
    if not ereignisse_aktiv(einst):  # Schalter aus
        return vorgaenge  # dann verfaellt nichts
    grenze = ereignis_gunst_ablehnung(einst)  # Ablauf kostet dasselbe wie eine Ablehnung
    tabelle = {str(b.get("name")): b for b in (bots or []) if isinstance(b, dict)}  # Bot-Nachschlag
    for eintrag in list(daten or []):  # jedes offene Ereignis ansehen
        if not isinstance(eintrag, dict):  # unbrauchbarer Eintrag
            continue  # dann ueberspringen
        if float(jetzt) < float(_zahl(eintrag.get("frist"), 0.0)):  # Frist noch nicht um
            continue  # dann bleibt es offen
        daten.remove(eintrag)  # Ereignis verfaellt
        bot = tabelle.get(str(eintrag.get("bot")))  # der Bot dazu
        if bot is not None:  # Bot bekannt
            gunst_aendern(bot, grenze, "ereignis_ablauf", einst)  # Gunst -5 buchen
        vorgaenge.append({"id": str(eintrag.get("id")),  # Kennung des Ereignisses
                          "art": str(eintrag.get("art")),  # Art
                          "bot": str(eintrag.get("bot")),  # Bot
                          "gunst_delta": grenze})  # was er kostet
    return vorgaenge  # die Verfaelle dieses Ticks

# ------------------------------------------------------------------ Bot-Diplomatie (S4-7)
# Zwei Themen, zwei Dateien: `data/diplomatie.json` traegt Gunst, Vertraege, Rache und Ereignisse,
# `data/bot_diplomatie.json` traegt seit S4-7 Spionage und Reaktion der Bots. Der Drache bleibt in
# `data/drachen.json` (W-14) - hier steht keine zweite Drachenzahl.
def botdaten(pfad=None) -> dict:
    """Liest `data/bot_diplomatie.json` (S4-7) - EINE Lesestelle fuer die Bot-Regeln.

    Eingabe: optionaler Pfad (fuer Pruefungen mit eigener Datei).
    Ausgabe: dict mit den Daten; leeres dict, wenn die Datei fehlt oder kein JSON ist.
    """
    if pfad is None:  # ohne Pfad gilt die Projektdatei
        pfad = os.path.join(spieldaten.projektwurzel(), "data", "bot_diplomatie.json")  # Standardpfad
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


def bot_spionage_regeln(pfad=None) -> dict:
    """Der Spionage-Block der Bot-Diplomatie; ein ausgeschalteter oder fehlender Block sperrt sie.

    Eingabe: optionaler Pfad zur Datendatei.
    Ausgabe: dict mit `aktiv` und den Anzeigetexten; leeres dict heisst: keine Spaehung.
    """
    block = botdaten(pfad).get("spionage") or {}  # der Themenblock
    return block if isinstance(block, dict) else {}  # nur ein dict gilt

