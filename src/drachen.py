# -*- coding: ascii -*-
"""Drachen des Spiels - Daten lesen, Figur oder Ruine bestimmen, Siege merken (W-14 Teil 1).

Alle Zahlen und Texte stehen in `data/drachen.json`; dieses Modul liest sie nur und haelt den
Zustand EINES Spielstands (`Zustand`). Es zeichnet nichts, oeffnet kein Fenster und schreibt
keine Datei - die Kartenanzeige und der Kampfweg rufen es auf.

Ein besiegter Drache ist eine RUINE (Daniel 04.11.2026): er verschwindet nicht, er waechst nicht
nach, und `finde` liefert ihn nicht mehr als Ziel. Das Ruinenbild steht in der Datendatei; fehlt
es, meldet `figur` einen Platzhalter.

Nichts wird erfunden: ein unbrauchbarer Eintrag wird uebergangen und in `offene_luecken()`
benannt, nie stillschweigend ersetzt.
"""
import json  # importiert das json-Modul zum Lesen der Datendatei
import os  # importiert os fuer Pfadoperationen
import spieldaten  # importiert spieldaten fuer den Projektwurzelpfad

STAND = "2026-11-04.1"  # definiert die Versionskennung des Moduls
_CACHE = {}  # Pfad -> (Aenderungszeit, Inhalt): die Datendatei wird EINMAL gelesen

def daten(pfad=None) -> dict:
    """Liest die Drachen-Datendatei und gibt sie als dict zurueck.
    Eingabe: optionaler Pfad zur JSON-Datei.
    Ausgabe: dict mit den geladenen Daten oder leeres dict bei Fehler."""
    if pfad is None:  # wenn kein Pfad angegeben ist
        pfad = os.path.join(spieldaten.projektwurzel(), "data", "drachen.json")  # baue den Standardpfad
    try:  # Zeitstempel der Datei holen
        stand = os.path.getmtime(pfad)  # Aenderungszeit als Schluessel
    except OSError:  # Datei fehlt
        return {}  # gebe ein leeres dict zurueck
    gemerkt = _CACHE.get(pfad)  # schon geladene Fassung
    if gemerkt is not None and gemerkt[0] == stand:  # unveraendert seit dem letzten Lesen
        return gemerkt[1]  # aus dem Cache - sonst liest die Bot-Schleife die Datei tausendfach
    try:  # versuche die Datei zu lesen
        with open(pfad, encoding="utf-8") as datei:  # oeffne die Datei
            inhalt = json.load(datei)  # lade die JSON-Daten
    except (OSError, ValueError):  # Datei fehlt oder ist kein JSON
        return {}  # gebe ein leeres dict zurueck
    _CACHE[pfad] = (stand, inhalt)  # merken (Pfad -> Zeitstempel, Inhalt)
    return inhalt  # an den Aufrufer

def _gueltig(eintrag) -> bool:
    """Prueft, ob ein Drachen-Eintrag alle Pflichtfelder mit korrekten Typen besitzt.
    Eingabe: ein Eintrag (dict).
    Ausgabe: True, wenn der Eintrag gueltig ist, sonst False."""
    if not isinstance(eintrag, dict):  # wenn kein dict, dann ungueltig
        return False  # gebe False zurueck
    benoetigte_felder = ("id", "welt", "name", "x", "y", "beute", "ware")  # Felder, die JEDER Eintrag braucht
    for feld in benoetigte_felder:  # iteriere ueber die Pflichtfelder
        if feld not in eintrag:  # wenn ein Feld fehlt
            return False  # dann ungueltig
    if not isinstance(eintrag["id"], str) or not isinstance(eintrag["welt"], str) or not isinstance(eintrag["name"], str):  # pruefe String-Typen
        return False  # wenn nicht string, ungueltig
    if not isinstance(eintrag["x"], int) or not isinstance(eintrag["y"], int):  # pruefe ob x und y ganze Zahlen sind
        return False  # wenn nicht int, ungueltig
    # W-14 (05.11.2026): die Verteidigung steht im Block 'verteidigung' mit 'einheiten' und 'schuppen'.
    # Ein alter Eintrag mit flachem 'einheiten'/'wall_stufe' bleibt lesbar - beides wird akzeptiert.
    block = eintrag.get("verteidigung")  # neuer Block
    einheiten = None  # zu pruefende Einheiten
    if isinstance(block, dict):  # neue Form
        einheiten = block.get("einheiten")  # Einheiten aus dem Block
        schuppen = block.get("schuppen")  # Werte, die den Wall ersetzen
        if not isinstance(schuppen, dict):  # ohne Schuppen ist der Drache nicht verteidigt
            return False  # dann ungueltig
        for feld in ("schwelle_fussttruppen", "schwelle_belagerungswaffen"):  # die beiden Vorrunden-Schwellen
            if not isinstance(schuppen.get(feld), int):  # muessen ganze Zahlen sein
                return False  # sonst ungueltig
    else:  # alte flache Form
        einheiten = eintrag.get("einheiten")  # flache Einheiten
        if not isinstance(eintrag.get("wall_stufe"), int):  # der alte Wall war Pflicht
            return False  # sonst ungueltig
    if not isinstance(einheiten, dict) or not einheiten:  # Einheiten muessen ein gefuelltes dict sein
        return False  # sonst ungueltig
    for anzahl in einheiten.values():  # iteriere ueber die Anzahlen
        if not isinstance(anzahl, int):  # wenn eine Anzahl keine ganze Zahl ist
            return False  # dann ungueltig
    for rohstoff, menge in eintrag["beute"].items():  # iteriere ueber die Beute
        if not isinstance(menge, (int, float)):  # wenn die Menge keine Zahl ist
            return False  # ungueltig
    for ware, anzahl in eintrag["ware"].items():  # iteriere ueber die Ware
        if not isinstance(anzahl, int):  # wenn die Warenanzahl keine ganze Zahl ist
            return False  # ungueltig
    return True  # sonst gueltig


def alle(pfad=None) -> list:
    """Liefert alle gueltigen Drachen-Eintraege aus der Datendatei.
    Eingabe: optionaler Pfad zur Datendatei.
    Ausgabe: Liste von dicts mit gueltigen Drachen."""
    daten_dict = daten(pfad)  # lade die Datendatei
    eintraege = daten_dict.get("drachen", [])  # hole die Drachenliste
    return [eintrag for eintrag in eintraege if _gueltig(eintrag)]  # filtere gueltige Eintraege

def finde(welt, x, y, besiegt=(), pfad=None) -> dict | None:
    """Findet einen Drachen an einer Position, sofern er nicht besiegt ist.
    Eingabe: Weltkennung, x, y, optionale Menge besiegter IDs, optionaler Pfad.
    Ausgabe: das Drachen-dict oder None, wenn nichts gefunden wird."""
    try:  # versuche x und y in ganze Zahlen umzuwandeln
        xi = int(x)  # konvertiere x
        yi = int(y)  # konvertiere y
    except (TypeError, ValueError):  # wenn Umwandlung fehlschlaegt
        return None  # gebe None zurueck
    for eintrag in alle(pfad):  # iteriere ueber alle gueltigen Drachen
        if eintrag["welt"] == welt and eintrag["x"] == xi and eintrag["y"] == yi:  # wenn Position passt
            if eintrag["id"] not in besiegt:  # und nicht besiegt ist
                return eintrag  # gebe den Eintrag zurueck
    return None  # wenn nichts gefunden, None

def finde_id(kennung, pfad=None):
    """Findet einen Drachen ueber seine Kennung (W-14 Teil 2).
    Eingabe: Kennung aus der Datendatei (z.B. 'drache_d02'), optionaler Pfad.
    Ausgabe: der Eintrag oder None - ein BESIEGTER Drache wird ebenfalls geliefert."""
    for eintrag in alle(pfad):  # jeder gueltige Eintrag der Datendatei
        if eintrag["id"] == str(kennung):  # die Kennung passt genau
            return eintrag  # gefunden
    return None  # nichts gefunden


def welt_kennung(nummer):
    """Die Kennung einer Weltkarte aus ihrer Nummer (1 ergibt 'd01').
    Eingabe: die Nummer der Weltkarte als Zahl (oder Text).
    Ausgabe: die Kennung als Text; bei unbrauchbarer Eingabe der leere Text."""
    try:  # Nummer belastbar machen
        return "d%02d" % int(nummer)  # zweistellige Kennung wie in welten.json
    except (TypeError, ValueError):  # unbrauchbare Angabe
        return ""  # dann keine Kennung - der Aufrufer findet nichts


def finde_id(kennung, pfad=None):
    """Findet einen Drachen ueber seine Kennung (W-14 Teil 2).
    Eingabe: Kennung aus der Datendatei (z.B. 'drache_d02'), optionaler Pfad.
    Ausgabe: der Eintrag oder None - ein BESIEGTER Drache wird ebenfalls geliefert."""
    for eintrag in alle(pfad):  # jeder gueltige Eintrag der Datendatei
        if eintrag["id"] == str(kennung):  # die Kennung passt genau
            return eintrag  # gefunden
    return None  # nichts gefunden


def welt_kennung(nummer):
    """Die Kennung einer Weltkarte aus ihrer Nummer (1 ergibt 'd01').
    Eingabe: die Nummer der Weltkarte als Zahl (oder Text).
    Ausgabe: die Kennung als Text; bei unbrauchbarer Eingabe der leere Text."""
    try:  # Nummer belastbar machen
        return "d%02d" % int(nummer)  # zweistellige Kennung wie in welten.json
    except (TypeError, ValueError):  # unbrauchbare Angabe
        return ""  # dann keine Kennung - der Aufrufer findet nichts


def verteidiger(eintrag) -> dict:
    """Gibt die Verteidiger-Einheiten eines Drachen zurueck (Wache, nicht der Drache selbst).
    Eingabe: ein Drachen-Eintrag.
    Ausgabe: dict {Einheit: Anzahl} aus dem Block 'verteidigung'."""
    block = eintrag.get("verteidigung") if isinstance(eintrag, dict) else None  # neuer Block seit 05.11.2026
    if not isinstance(block, dict):  # alter Eintrag ohne Block
        return dict(eintrag.get("einheiten", {}) if isinstance(eintrag, dict) else {})  # flache Form als Rueckfall
    return dict(block.get("einheiten") or {})  # Kopie der Wachen

def schuppen(eintrag) -> dict:
    """Die Werte, die beim Drachen die Aufgabe des Walls uebernehmen (Schuppen).
    Eingabe: ein Drachen-Eintrag.
    Ausgabe: dict mit schwelle_fussttruppen, schwelle_belagerungswaffen, unbrechbar."""
    block = eintrag.get("verteidigung") if isinstance(eintrag, dict) else None  # Block der Verteidigung
    schuppen = (block or {}).get("schuppen") if isinstance(block, dict) else None  # Werte des Drachen
    return dict(schuppen) if isinstance(schuppen, dict) else {}  # Kopie oder leer - nichts erfunden


def schwellen(eintrag) -> tuple:
    """Die beiden Vorrunden-Schwellen des Drachen (ersetzt den Wall).
    Eingabe: ein Drachen-Eintrag.
    Ausgabe: (schwelle_fussttruppen, schwelle_belagerungswaffen) als ganze Zahlen; fehlt etwas, 0."""
    werte = schuppen(eintrag)  # die Schuppen-Werte
    fuss = werte.get("schwelle_fussttruppen")  # Schwelle der Fusstruppen
    bel = werte.get("schwelle_belagerungswaffen")  # Schwelle der Belagerungswaffen
    try:  # Zahlen erwarten, Text und None abfangen
        return (int(fuss), int(bel))  # beide Schwellen
    except (TypeError, ValueError):  # unbrauchbare Angabe
        return (0, 0)  # dann gilt keine Schwelle - der Kampf findet statt


def unbrechbar(eintrag) -> bool:
    """Kann Belagerung den Drachen beschaedigen? Ein Wall wird gebrochen, ein Drache nicht.
    Eingabe: ein Drachen-Eintrag.
    Ausgabe: True, wenn die Schuppen NICHT kleiner werden (Vorgabe: True)."""
    werte = schuppen(eintrag)  # die Schuppen-Werte
    return bool(werte.get("unbrechbar", True))  # ohne Angabe gilt: unbrechbar


def feueratem(eintrag) -> dict:
    """Der Feueratem des Drachen: Verluste VOR dem Nahkampf.
    Eingabe: ein Drachen-Eintrag.
    Ausgabe: dict mit prozent_der_fusstruppen, mindestens, hoechstens_anteil (leer, wenn nicht gesetzt)."""
    block = eintrag.get("verteidigung") if isinstance(eintrag, dict) else None  # Block der Verteidigung
    atem = (block or {}).get("feueratem") if isinstance(block, dict) else None  # Werte des Atems
    return dict(atem) if isinstance(atem, dict) else {}  # Kopie oder leer


def zweite_phase(eintrag) -> dict:
    """Die ZWEITE Atemphase des Drachen (Daniels Entscheidung zur Frage 2, 05.11.2026).

    Eingabe: ein Drachen-Eintrag. Ausgabe: dict mit `aktiv`, `atem_prozent` und `unter_anteil`
    - oder ein leeres dict, wenn der Eintrag keine Phase kennt (dann kaempft die Schlacht
    wortgleich wie vorher). Die Zahlen stehen in `data/drachen.json`, nicht im Code.
    """
    block = eintrag.get("verteidigung") if isinstance(eintrag, dict) else None  # Block der Verteidigung
    regeln = (block or {}).get("zweite_phase") if isinstance(block, dict) else None  # Regeln der Phase
    if not isinstance(regeln, dict):                        # kein Block vorhanden
        return {}                                           # dann keine zweite Phase
    return {"aktiv": bool(regeln.get("aktiv", True)),       # Schalter (Vorgabe: an)
            "atem_prozent": regeln.get("atem_prozent"),     # Anteil der Nahkaempfer
            "unter_anteil": regeln.get("unter_anteil", 0.5)}  # Ausloeser: unter halber Wache


def feueratem_verluste(eintrag, anzahl_fussttruppen) -> int:
    """Wie viele Fusstruppen der Feueratem vor dem Kampf ausfallen laesst.
    Eingabe: Drachen-Eintrag und die Zahl der antretenden Fusstruppen (Ganzzahl, nie negativ).
    Ausgabe: ganze Zahl >= 0; hoechstens der Anteil aus dem Eintrag (Vorgabe die Haelfte)."""
    atem = feueratem(eintrag)  # Regel des Atems
    try:  # Anzahl belastbar machen
        anzahl = max(0, int(anzahl_fussttruppen))  # nie negativ
    except (TypeError, ValueError):  # unbrauchbare Zahl
        return 0  # dann kein Verlust
    if not atem or anzahl <= 0:  # kein Atem oder niemand da
        return 0  # nichts zu verlieren
    prozent = atem.get("prozent_der_fusstruppen", 0)  # Anteil in Prozent
    mindestens = atem.get("mindestens", 0)  # Untergrenze
    anteil = atem.get("hoechstens_anteil", 0.5)  # Obergrenze als Anteil
    try:  # Zahlen belastbar machen
        roh = int(round(anzahl * float(prozent) / 100.0))  # gerechneter Verlust
        unten = max(0, int(mindestens)) if anzahl > 0 else 0  # Untergrenze, nie mehr als die Truppe
        oben = int(float(anteil) * anzahl)  # Obergrenze aus dem Anteil
    except (TypeError, ValueError):  # unbrauchbare Angabe
        return 0  # dann kein Verlust
    return max(0, min(max(roh, unten), oben, anzahl))  # zwischen Unter- und Obergrenze


def beute(eintrag) -> dict:
    """Gibt die Beute eines Drachen zurueck.
    Eingabe: ein Drachen-Eintrag.
    Ausgabe: dict {Rohstoff: Menge}."""
    return dict(eintrag.get("beute", {}))  # gebe eine Kopie der Beute zurueck

def ware(eintrag) -> dict:
    """Gibt die Ware eines Drachen zurueck.
    Eingabe: ein Drachen-Eintrag.
    Ausgabe: dict {Warenname: Anzahl}."""
    return dict(eintrag.get("ware", {}))  # gebe eine Kopie der Ware zurueck

def verteile(zufall, felder, belegt_felder=(), pfad=None) -> dict:
    """Neue Koordinaten fuer alle Drachen - gleiche Welt, anderer Platz (Daniel 05.11.2026).

    Daniels Vorgabe: bei jedem Neubeginn sollen die Drachen woanders stehen, aber auf DENSELBEN
    Welten bleiben. Gewuerfelt wird nur auf Feldern, die das Gelaende zulaesst (nicht auf Sumpf),
    und nie zweimal auf demselben Feld; `belegt` nennt Felder, die schon jemand nutzt.
    Eingabe: ein random.Random, eine Menge belegter (welt, x, y)-Tupel, optionaler Pfad.
    Ausgabe: dict {Kennung: [x, y]}; findet ein Drache kein freies Feld, fehlt er im dict -
    der Aufrufer nimmt dann die Koordinate der Datendatei (nichts erfunden).
    """
    # Die freien Felder kommen UEBERGEBEN (Feldabbildung je Welt): das Weltbild liest nur
    # `portalraum`/`main`, und die Wache `test_weltbild_gelaende` haelt das fest.
    belegte = set()  # Kopie der belegten Felder
    for welt, x, y in (belegt_felder or ()):  # jedes uebergebene Feld
        belegte.add((str(welt), int(x), int(y)))  # vereinheitlicht merken
    ergebnis = {}  # {Kennung: [x, y]}
    for eintrag in alle(pfad):  # jeder gueltige Drache
        welt = str(eintrag["welt"])  # SEINE Welt bleibt (Daniel: gleiche Welten)
        frei = []  # alle brauchbaren Felder dieser Welt
        for x, y in (felder.get(welt) or []):  # die uebergebenen Felder dieser Welt
            if (welt, int(x), int(y)) in belegte:  # schon vergeben
                continue  # ueberspringen
            frei.append((int(x), int(y)))  # brauchbares Feld
        if not frei:  # kein Platz auf dieser Welt
            continue  # Datendatei behalten
        x, y = zufall.choice(frei)  # EIN freies Feld ziehen
        ergebnis[str(eintrag["id"])] = [int(x), int(y)]  # merken
        belegte.add((welt, int(x), int(y)))  # Feld ist jetzt vergeben
    return ergebnis  # {Kennung: [x, y]}


def belohnung_mana(pfad=None) -> dict:
    """Die Manabelohnung eines besiegten Drachen (Daniel 05.11.2026).

    Daniels Vorgabe, woertlich-nah: ein fester Betrag von 4000 Mana PLUS das, was ein ausgewogenes
    Aufwands-Szenario an Mana kostet (mehrere Angriffe, Rueckzug, neuer Versuch, Weltspruenge).
    Damit sich das mitentwickelt, wird der Aufwand aus dem ECHTEN Preis eines Weltensprungs
    gerechnet (`portalraum.wechselkosten`) und nicht im Code festgeschrieben: aendert sich dort ein
    Wert oder die Zahl der Versuche in der Datendatei, zieht die Belohnung mit.
    Eingabe: optionaler Pfad zur Datendatei.
    Ausgabe: dict mit grundbetrag, versuche, sprunge, kosten_je_sprung, aufwand, summe.
    """
    import portalraum  # nur hier: der Weltensprung-Preis steht beim Portal
    block = daten(pfad).get("belohnung") or {}  # Block aus der Datendatei
    if not isinstance(block, dict):  # unbrauchbare Angabe
        block = {}  # dann gelten die Vorgaben unten
    szenario = block.get("aufwandsszenario") if isinstance(block.get("aufwandsszenario"), dict) else {}  # Szenario
    try:  # fester Betrag belastbar machen
        grund = int(block.get("mana_grundbetrag", 4000))  # Daniels Pauschale
    except (TypeError, ValueError):  # unbrauchbare Angabe
        grund = 4000  # Vorgabe
    try:  # Versuche belastbar machen
        versuche = max(1, int(szenario.get("versuche", 3)))  # drei Anlaeufe
    except (TypeError, ValueError):  # unbrauchbare Angabe
        versuche = 3  # Vorgabe
    try:  # Spruenge je Versuch belastbar machen
        je_versuch = max(1, int(szenario.get("sprunge_je_versuch", 2)))  # hin und zurueck
    except (TypeError, ValueError):  # unbrauchbare Angabe
        je_versuch = 2  # Vorgabe
    try:  # den ECHTEN Preis des Sprungs holen
        je_sprung = int(portalraum.wechselkosten())  # harte Kostenzahl des Spiels
    except (AttributeError, TypeError, ValueError):  # Preis nicht lesbar
        je_sprung = 0  # dann zaehlt nur der feste Betrag, nichts erfunden
    sprunge = int(versuche) * int(je_versuch)  # alle Weltspruenge des Szenarios
    aufwand = int(sprunge) * int(je_sprung)  # was diese Spruenge kosten
    return {"grundbetrag": grund, "versuche": versuche, "sprunge": sprunge,
            "kosten_je_sprung": je_sprung, "aufwand": aufwand,
            "summe": int(grund) + int(aufwand)}  # die ganze Belohnung


def belohnung_texte(pfad=None) -> dict:
    """Die epischen Texte zur Manabelohnung (Daniel 05.11.2026: dem Spiel entsprechend natuerlich).
    Eingabe: optionaler Pfad zur Datendatei.
    Ausgabe: dict mit titel und zeilen (Liste); leere Angaben werden nicht erfunden."""
    block = daten(pfad).get("belohnung") or {}  # Block aus der Datendatei
    if not isinstance(block, dict):  # unbrauchbare Angabe
        return {}  # dann keine Texte
    zeilen = block.get("text_zeilen") if isinstance(block.get("text_zeilen"), list) else []  # Zeilen
    return {"titel": str(block.get("text_titel") or ""),
            "zeilen": [str(z) for z in zeilen if str(z).strip()]}  # nur echte Texte


def bot_regeln(pfad=None) -> dict:
    """Wie ein Bot einen Drachen beurteilt (Daniel 05.11.2026).
    Eingabe: optionaler Pfad zur Datendatei.
    Ausgabe: dict mit schlagkraft_faktor und verluste_erwartet_prozent."""
    block = daten(pfad).get("bots") or {}  # Regeln aus der Datendatei
    if not isinstance(block, dict):  # unbrauchbare Angabe
        block = {}  # dann gelten die Vorgaben
    try:  # Sicherheitsmarge belastbar machen
        faktor = float(block.get("schlagkraft_faktor", 1.6))  # Armee muss deutlich ueber der Schwelle liegen
    except (TypeError, ValueError):  # unbrauchbare Angabe
        faktor = 1.6  # Vorgabe
    try:  # erwartete Verluste belastbar machen
        verluste = int(block.get("verluste_erwartet_prozent", 35))  # sichere Verluste in Prozent
    except (TypeError, ValueError):  # unbrauchbare Angabe
        verluste = 35  # Vorgabe
    return {"schlagkraft_faktor": faktor, "verluste_erwartet_prozent": verluste,
            # Anzeigetexte stehen in der Datendatei (diese Datei ist ASCII-only). Fehlt ein
            # Text, gilt ein kurzer neutraler Satz - nie eine Ersatzschreibweise im Code.
            "text_zu_schwach_fuss": str(block.get("text_zu_schwach_fuss") or "Drache zu stark."),
            "text_zu_schwach_belagerung": str(block.get("text_zu_schwach_belagerung")
                                              or "Drache zu stark."),
            "text_lohnt": str(block.get("text_lohnt") or "Drache lohnt."),
            "text_angegriffen": str(block.get("text_angegriffen") or "Bereits angegriffen.")}


def bot_entscheidung(schlag_fuss, schlag_belagerung, schwellen, belohnung=0,
                     angegriffen=False, pfad=None) -> tuple:
    """Soll ein BOT einen Drachen angreifen? (Daniel 05.11.2026)

    Daniels Vorgabe: die Bots sollen verstehen, dass ein Drache Bonus (Mana und Hort) UND sichere
    Verluste bedeutet - und dass sie die TATSAECHLICHE Staerke erst sehen, wenn sie selbst
    angreifen. Bekannt ist ihnen nur, DASS schon jemand angegriffen hat (`angegriffen`).
    Eingabe: Schlagkraft der Fusstruppen, Schlagkraft der Belagerung, die beiden Schwellen,
             die Manabelohnung, ob der Drache schon einmal angegriffen wurde.
    Ausgabe: (True/False, Begruendung als Anzeigetext).
    """
    regeln = bot_regeln(pfad)  # Marge und erwartete Verluste aus der Datendatei
    faktor = float(regeln.get("schlagkraft_faktor") or 1.0)  # Sicherheitsmarge
    verluste = int(regeln.get("verluste_erwartet_prozent") or 0)  # erwartete Verluste
    try:  # Zahlen belastbar machen
        fuss = max(0, int(schlag_fuss))  # eigene Fussschlagkraft
        bel = max(0, int(schlag_belagerung))  # eigene Belagerungskraft
        s_fuss, s_bel = int(schwellen[0]), int(schwellen[1])  # Schwellen des Drachen
    except (TypeError, ValueError, IndexError):  # unbrauchbare Angabe
        return (False, "Der Drache ist unbekannt - kein Angriff.")  # nichts erfinden
    noetig_fuss = int(round(s_fuss * faktor))  # mit Marge
    noetig_bel = int(round(s_bel * faktor))  # mit Marge
    if fuss < noetig_fuss:  # zu wenig Fusstruppen
        return (False, str(regeln["text_zu_schwach_fuss"])  # Text aus der Datendatei
                .replace("{eigene}", str(fuss)).replace("{schwelle}", str(noetig_fuss)))
    if bel < noetig_bel:  # zu wenig Belagerung
        return (False, str(regeln["text_zu_schwach_belagerung"])  # Text aus der Datendatei
                .replace("{eigene}", str(bel)).replace("{schwelle}", str(noetig_bel)))
    grund = (str(regeln["text_lohnt"])  # der Satz kommt aus der Datendatei
             .replace("{mana}", str(int(belohnung or 0)))
             .replace("{verluste}", str(verluste)))
    if angegriffen:  # er weiss nur, DASS jemand angegriffen hat
        grund = grund + " " + str(regeln["text_angegriffen"])  # zweiter Satz aus den Daten
    return (True, grund)


def bedrohung(ort, besiegt=(), pfad=None) -> dict:
    """Wie nah steht der NAECHSTE offene Drache an einem Ort? NUR Anzeige (F-14 = B, 07.11.2026).

    Daniel hat am 07.11.2026 entschieden: die Meidung wird NICHT gebaut, die Meldung schon. Diese
    Funktion rechnet deshalb nichts und bucht nichts - sie nennt nur Name und Abstand.
    Eingabe: Ort (Objekt oder dict mit x, y, dimension), Menge besiegter Drachen-IDs, optionaler Pfad.
    Ausgabe: dict mit 'text' (leer, wenn keiner in Reichweite steht), 'name', 'abstand', 'x', 'y'.
    Abstand ist der Manhattan-Abstand aus |dx| + |dy| - dieselbe Rechnung wie bottaktik.entfernung.
    """
    block = daten(pfad).get("bots") or {}  # der Bot-Block der Datendatei
    if not isinstance(block, dict):  # unbrauchbare Angabe
        return {}  # dann keine Meldung
    vorlage = str(block.get("text_bedrohung") or "")  # Anzeigetext aus den Daten
    try:  # Reichweite belastbar machen
        reichweite = int(block.get("bedrohung_reichweite", 0) or 0)  # ab wann geschwiegen wird
    except (TypeError, ValueError):  # kaputte Angabe
        reichweite = 0  # dann schweigt die Meldung
    if not vorlage:  # kein Text in der Datei
        return {}  # dann wird nichts erfunden
    def _wert(name):  # liest ein Feld aus Objekt ODER dict
        if isinstance(ort, dict):  # dict-Form
            return ort.get(name)  # direkt lesen
        return getattr(ort, name, None)  # sonst vom Objekt
    try:  # Lage des Ortes
        x = int(_wert("x"))  # Spalte
        y = int(_wert("y"))  # Zeile
        nummer = int(_wert("dimension"))  # Weltnummer
    except (TypeError, ValueError):  # Ort ohne brauchbare Lage
        return {}  # dann keine Meldung
    siegel = welt_kennung(nummer)  # Kennung seiner Welt
    if not siegel:  # keine Welt bekannt
        return {}  # dann keine Meldung
    offen = [e for e in alle(pfad)  # jeder gueltige Drache
             if str(e.get("welt")) == siegel  # in DIESER Welt
             and str(e.get("id")) not in (besiegt or ())]  # und noch nicht besiegt
    if not offen:  # kein Drache in seiner Welt
        return {}  # dann keine Meldung
    naechster = None  # bester Kandidat
    for eintrag in offen:  # jeder Drache einmal
        try:  # seine Lage
            abstand = abs(x - int(eintrag.get("x"))) + abs(y - int(eintrag.get("y")))  # Manhattan
        except (TypeError, ValueError):  # Eintrag ohne Lage
            continue  # dann zaehlt er nicht
        if naechster is None or abstand < naechster[0]:  # naeher als der bisherige
            naechster = (abstand, eintrag)  # dann merken
    if naechster is None:  # keiner hatte eine Lage
        return {}  # dann keine Meldung
    abstand, eintrag = naechster  # bester Kandidat
    text = ""  # ohne Reichweite kein Satz
    if reichweite <= 0 or abstand <= reichweite:  # in Reichweite
        satz = vorlage  # der Satz aus der Datendatei
        if abstand <= 1 and str(block.get("text_bedrohung_direkt") or ""):  # direkt am Dorf
            satz = str(block.get("text_bedrohung_direkt"))  # eigener Satz statt "0 Felder"
        text = (satz.replace("{name}", str(eintrag.get("name") or ""))  # Name des Drachen
                .replace("{abstand}", str(int(abstand))))  # und der Abstand
    return {"text": text, "name": str(eintrag.get("name") or ""), "abstand": int(abstand),
            "x": int(eintrag.get("x") or 0), "y": int(eintrag.get("y") or 0)}  # alles als dict


def figur(eintrag, besiegt=(), pfad=None) -> dict:
    """Erzeugt das Anzeige-dict fuer einen Drachen oder eine Ruine.
    Eingabe: Drachen-Eintrag, optionale Menge besiegter IDs, optionaler Pfad.
    Ausgabe: dict mit art, bild, platzhalter, name, welt, x, y."""
    daten_dict = daten(pfad)  # lade die Datendatei
    figur_config = daten_dict.get("figur", {})  # hole die Figuren-Konfiguration
    ist_besiegt = eintrag["id"] in besiegt  # pruefe ob der Drache besiegt ist
    if ist_besiegt:  # wenn besiegt
        art = "ruine"  # setze art auf ruine
        bild = figur_config.get("ruine_bild", "")  # hole den Ruinenbildpfad
        platzhalter = figur_config.get("ruine_platzhalter", False) or (bild == "")  # bestimme platzhalter
    else:  # sonst
        art = "drache"  # setze art auf drache
        bild = str(eintrag.get("bild") or figur_config.get("bild") or "")  # eigenes Bild des Drachen, sonst das allgemeine
        platzhalter = (bild == "")  # platzhalter nur wenn kein Bild vorhanden ist
    return {"art": art, "bild": bild, "platzhalter": platzhalter, "name": eintrag["name"], "welt": eintrag["welt"], "x": eintrag["x"], "y": eintrag["y"]}  # gebe das Figuren-dict zurueck

def anzeige_liste(welt, besiegt=(), pfad=None) -> list:
    """Liefert eine Liste aller Figuren einer Welt fuer die Kartenanzeige.
    Eingabe: Weltkennung, optionale Menge besiegter IDs, optionaler Pfad.
    Ausgabe: Liste von Figuren-dicts."""
    return [figur(eintrag, besiegt, pfad) for eintrag in alle(pfad) if eintrag["welt"] == welt]  # erstelle Liste von Figuren fuer die Welt

def offene_luecken() -> dict:
    """Benennt offene Punkte der Datendatei, z.B. fehlende Bilder oder unbrauchbare Eintraege.
    Eingabe: keine.
    Ausgabe: dict mit Listen fehlender Bilder und unbrauchbarer Eintraege."""
    daten_dict = daten()  # lade die Datendatei
    eintraege = daten_dict.get("drachen", [])  # hole die rohe Drachenliste
    figur_config = daten_dict.get("figur", {})  # hole die Figuren-Konfiguration
    fehlende_bilder = []  # initialisiere Liste fuer fehlende Bilder
    if not figur_config.get("bild"):  # wenn das Drachenbild fehlt
        fehlende_bilder.append("figur.bild")  # trage es ein
    if not figur_config.get("ruine_bild"):  # wenn das Ruinenbild fehlt
        fehlende_bilder.append("figur.ruine_bild")  # trage es ein
    unbrauchbare_eintraege = []  # initialisiere Liste fuer unbrauchbare Eintraege
    for index, eintrag in enumerate(eintraege):  # iteriere ueber alle Eintraege
        if not _gueltig(eintrag):  # wenn der Eintrag ungueltig ist
            unbrauchbare_eintraege.append(index)  # merke den Index
    return {"fehlende_bilder": fehlende_bilder, "unbrauchbare_eintraege": unbrauchbare_eintraege}  # gebe das Ergebnis-dict zurueck

class Zustand:
    """Verwaltet die besiegten Drachen fuer einen Spielstand."""
    def __init__(self, besiegt=()):
        """Initialisiert den Zustand mit einer Menge besiegter IDs.
        Eingabe: optionale iterierbare Menge von IDs.
        Ausgabe: keine."""
        self.besiegt = set(besiegt)  # speichere die besiegten IDs als Set

    def aus_daten(self, daten: dict) -> "Zustand":
        """Liest die besiegten Drachen aus einem Spielstand-dict.
        Eingabe: dict mit optionalem Feld 'drachen_besiegt'.
        Ausgabe: die eigene Instanz."""
        self.besiegt = set(daten.get("drachen_besiegt", []))  # lies die besiegten IDs aus dem dict
        return self  # gebe die eigene Instanz zurueck

    def als_daten(self) -> dict:
        """Gibt die besiegten Drachen als Spielstand-dict zurueck.
        Eingabe: keine.
        Ausgabe: dict {'drachen_besiegt': [ids]}."""
        return {"drachen_besiegt": list(self.besiegt)}  # gebe ein dict mit der Liste der besiegten IDs zurueck

    def besiegen(self, kennung: str) -> bool:
        """Markiert eine Drachen-ID als besiegt.
        Eingabe: die ID.
        Ausgabe: True, wenn neu, False, wenn bereits enthalten."""
        if kennung in self.besiegt:  # wenn die ID schon enthalten ist
            return False  # gebe False zurueck
        self.besiegt.add(kennung)  # fuege die ID hinzu
        return True  # gebe True zurueck, weil neu

    def ist_besiegt(self, kennung: str) -> bool:
        """Prueft, ob eine Drachen-ID als besiegt markiert ist.
        Eingabe: die ID.
        Ausgabe: True, wenn enthalten, sonst False."""
        return kennung in self.besiegt  # pruefe ob die ID enthalten ist

    def alle_besiegt(self, pfad=None) -> bool:
        """Prueft, ob alle gueltigen Drachen besiegt sind.
        Eingabe: optionaler Pfad zur Datendatei.
        Ausgabe: True, wenn alle IDs im Zustand enthalten sind, sonst False."""
        alle_ids = [eintrag["id"] for eintrag in alle(pfad)]  # sammle alle gueltigen Drachen-IDs
        if not alle_ids:  # keine Datendatei oder kein Eintrag
            return False  # dann ist nichts besiegt - nicht "alles erledigt"
        return all(id in self.besiegt for id in alle_ids)  # pruefe ob alle IDs besiegt sind


def ruine_texte(pfad=None) -> dict:
    """Die Texte fuer die gepluenderte Ruine (Daniel 05.11.2026: die Ruine bleibt pluenderbar).
    Eingabe: optionaler Pfad zur Datendatei.
    Ausgabe: dict mit titel, zeile_mit, zeile_rest, zeile_leer - leer, wenn die Datei nichts nennt."""
    block = daten(pfad).get("ruine") or {}  # Block aus der Datendatei
    if not isinstance(block, dict):  # unbrauchbare Angabe
        return {}  # dann keine erfundenen Texte
    return {str(k): str(v) for k, v in block.items() if isinstance(v, str)}  # nur Texte


def spionage_erlaubt(pfad=None) -> tuple:
    """Laesst sich ein Drache ausspaehen? (Daniel 05.11.2026: nein)
    Eingabe: optionaler Pfad zur Datendatei.
    Ausgabe: (False, Grund) - der Grund kommt aus der Datendatei, nie aus dem Code."""
    block = daten(pfad).get("spionage") or {}  # Regel aus der Datendatei
    erlaubt = bool(block.get("erlaubt", False)) if isinstance(block, dict) else False  # Vorgabe: nicht erlaubt
    grund = str(block.get("grund") or "") if isinstance(block, dict) else ""  # Begruendung der Daten
    return (erlaubt, grund)  # Antwortpaar


def angriffs_hinweis(pfad=None) -> str:
    """Der kurze Hinweis fuer den Spieler, bevor er einen Drachen angreift.
    Eingabe: optionaler Pfad zur Datendatei.
    Ausgabe: der Text aus `angriffshinweis` (leer, wenn die Datei keinen nennt)."""
    return str(daten(pfad).get("angriffshinweis") or "")  # Text wortgetreu aus den Daten


def beute_anteil(zerstoerte_verteidiger, verteidiger_gesamt, beute, letzter_schlag=False,
                 pfad=None) -> dict:
    """Der Beuteanteil EINES Angriffs - nach Leistung, nicht nach dem letzten Schlag allein.

    Daniels Regel (05.11.2026): "nur der der die letzte truppe beim drachen vernichtet bekommt alle
    ressourcen", zugleich aber: kein gut getimter billiger Angriff darf alles nehmen. Beides zusammen
    geht nicht - deshalb gilt (VORSCHLAG, in der Datendatei umschaltbar):
      * jeder Angriff bucht sofort den Anteil, der seinen zerstoerten Verteidigern entspricht,
      * wer den letzten Schlag setzt, bekommt einen Bonus obendrauf,
      * niemand bekommt mehr als der Vorrat hergibt.
    Eingabe: zerstoerte Verteidiger, Verteidiger insgesamt, Beute-dict, letzter Schlag (bool).
    Ausgabe: dict {Rohstoff: Menge} - ganze Zahlen, nie negativ, nie mehr als die Beute.
    """
    regel = daten(pfad).get("beute_regel") or {}  # Regeln aus der Datendatei
    try:  # Zahlen belastbar machen
        zerstoert = max(0, int(zerstoerte_verteidiger))  # eigene Leistung
        gesamt = max(0, int(verteidiger_gesamt))  # Verteidiger zu Beginn
    except (TypeError, ValueError):  # unbrauchbare Angabe
        return {}  # dann keine Beute
    if gesamt <= 0 or zerstoert <= 0 or not isinstance(beute, dict):  # nichts passiert
        return {}  # dann keine Beute
    anteil = min(1.0, zerstoert / float(gesamt))  # Anteil an der Verteidigung
    if isinstance(regel, dict) and regel.get("anteil_nach_verlusten") is False:  # Regel abgeschaltet
        anteil = 1.0 if letzter_schlag else 0.0  # dann gilt der reine letzte Schlag
    if letzter_schlag:  # Bonus fuer den, der den Drachen faellt
        try:  # Prozentwert belastbar machen
            bonus = float(regel.get("bonus_letzter_schlag_prozent", 0) or 0) / 100.0  # Bonus als Anteil
        except (TypeError, ValueError):  # unbrauchbar
            bonus = 0.0  # dann kein Bonus
        anteil = min(1.0, anteil + max(0.0, bonus))  # Bonus obendrauf, hoechstens alles
    ergebnis = {}  # was dieser Angriff bekommt
    for stoff, menge in beute.items():  # jeder Rohstoff der Beute
        try:  # Menge belastbar machen
            vorrat = max(0, int(menge))  # ganzer Vorrat
        except (TypeError, ValueError):  # unbrauchbar
            continue  # diesen Stoff ueberspringen
        teil = int(vorrat * anteil)  # anteiliger Betrag, abgerundet
        if teil > 0:  # nur was wirklich da ist
            ergebnis[str(stoff)] = min(teil, vorrat)  # nie mehr als der Vorrat
    return ergebnis  # Anteil dieses Angriffs


def bericht(ergebnis, ueberlebende_angreifer, verteidiger_einheiten=None, naechster_angriff=None,
            pfad=None) -> dict:
    """Der Kampfbericht eines Drachenkampfs (Daniel 05.11.2026: episch, aber ehrlich).

    Regel: Ueberlebt auch nur EINE Einheit, nennt der Bericht die Verteidiger mit Einheiten - dann ist
    der Kampf aufgeklaert. Kehrt niemand zurueck, kennt der Bericht NUR die eigenen Verluste und die
    ZAHL der Verteidiger, nicht ihre Art: "was dort stand, weiss niemand zu sagen".
    Eingabe: Ergebnis von `kampf.fuehre_schlacht`, Zahl der ueberlebenden Angreifer, Verteidiger-dict
             (nur fuer den aufgeklaerten Fall), optional der naechste moegliche Angriff.
    Ausgabe: dict {titel, zeilen, typ} - die Texte stammen aus `bericht` der Datendatei.
    """
    daten_dict = daten(pfad)  # Datendatei
    texte = daten_dict.get("bericht") or {}  # Textbausteine
    texte = texte if isinstance(texte, dict) else {}
    e = ergebnis or {}  # Schlachtergebnis
    ausgang = str(e.get("ausgang") or "")  # Ausgang der Schlacht
    gewonnen = ausgang == "angreifer"  # hat der Angreifer gesiegt?
    titel = str(texte.get("titel_sieg" if gewonnen else "titel_niederlage") or "")  # Ueberschrift
    zeilen = []  # Zeilen des Berichts
    try:  # Ueberlebende belastbar machen
        ueberlebt = max(0, int(ueberlebende_angreifer))  # Zahl der Heimkehrer
    except (TypeError, ValueError):  # unbrauchbare Angabe
        ueberlebt = 0  # dann gilt: keiner kam zurueck
    if ueberlebt > 0 and isinstance(verteidiger_einheiten, dict) and verteidiger_einheiten:  # aufgeklaert
        namen = ", ".join("%d %s" % (int(v), k) for k, v in sorted(verteidiger_einheiten.items()) if int(v) > 0)
        vorlage = str(texte.get("zeile_gegner_mit_namen") or "")  # Vorlage NUR aus der Datendatei
        if vorlage:  # ohne Vorlage keine erfundene Zeile
            zeilen.append(vorlage.replace("{einheiten}", namen))  # Einheiten einsetzen
    else:  # niemand kam zurueck: keine Auskunft ueber die Art
        anzahl = sum(int(v) for v in (verteidiger_einheiten or {}).values() if int(v) > 0) if isinstance(verteidiger_einheiten, dict) else 0
        vorlage = str(texte.get("zeile_gegner_ohne_namen") or "")  # Vorlage NUR aus der Datendatei
        if vorlage:  # ohne Vorlage keine erfundene Zeile
            zeilen.append(vorlage.replace("{anzahl}", str(anzahl)))  # Zahl einsetzen
        hinweis = str(texte.get("hinweis_ohne_ueberlebende") or "")  # der ehrliche Zusatz
        if hinweis:  # nur wenn die Daten einen nennen
            zeilen.append(hinweis)  # hinten anhaengen
    if naechster_angriff is not None:  # Ausblick, wenn der Aufrufer ihn kennt
        zeilen.append(str(naechster_angriff))  # als eigene Zeile
    return {"titel": titel, "zeilen": zeilen, "typ": "kampf"}  # fertiger Bericht


def transport_bedarf(menge, forschung=None, pfad=None) -> dict:
    """Wie viel Ladung eine Beute braucht und welcher Wagenpark sie traegt (Daniel 05.11.2026).

    Die Beute muss abtransportiert werden - ohne genug Karren bleibt der Rest liegen. Diese Funktion
    rechnet den BEDARF aus: erst die noetige Ladung (Summe der Beute), dann EINEN Wagenpark, der sie
    traegt (groesste Karren zuerst). Das ist ein VORSCHLAG, nicht das Optimum: wer es genauer
    plant, nimmt weniger grosse Karren. Der Wagenbau-Bonus gilt, weil
    `einheiten.ladung_der_gruppe` ihn selbst rechnet - eine Rechenstelle, keine zweite.
    Eingabe: Beute-dict und optional der Forschungsstand {Gebiet: Stufe}.
    Ausgabe: dict mit ladung (noetig), karren ({Name: Anzahl}), rest (Ladung, die offen bleibt).
    """
    import einheiten as E  # das Einheitenmodul rechnet die Ladung (auch mit Wagenbau-Bonus)
    daten_dict = daten(pfad)  # Datendatei
    block = daten_dict.get("transport") or {}  # Regeln des Transports
    reihenfolge = block.get("reihenfolge") if isinstance(block, dict) else None  # gewuenschte Reihenfolge
    if not isinstance(reihenfolge, list) or not reihenfolge:  # keine Reihenfolge in den Daten
        reihenfolge = []  # keine feste Liste im Code: die Namen stehen in data/units.json
    if not isinstance(menge, dict):  # unbrauchbare Beute
        return {"ladung": 0, "karren": {}, "rest": 0}  # dann nichts zu tragen
    summe = 0  # benoetigte Ladung
    for wert in menge.values():  # jeder Posten der Beute
        try:  # Zahl belastbar machen
            summe += max(0, int(wert))  # aufaddieren
        except (TypeError, ValueError):  # unbrauchbarer Posten
            continue  # ueberspringen
    if not reihenfolge:  # keine Reihenfolge in den Daten und keine im Code
        reihenfolge = sorted(E.alle(), key=lambda n: -E.ladung_der_gruppe({n: 1}, forschung))  # groesste zuerst
        reihenfolge = [n for n in reihenfolge if E.rolle(n) == "karren"]  # nur Karren tragen
    karren = {}  # gewaehlter Wagenpark
    rest = summe  # was noch zu tragen ist
    for name in reihenfolge:  # groesste Karren zuerst
        eins = E.ladung_der_gruppe({name: 1}, forschung)  # Ladung EINES solchen Karrens (mit Bonus)
        if eins <= 0:  # unbekannter Karren
            continue  # ueberspringen
        anzahl = rest // eins  # wie viele ganze Karren noetig sind
        if anzahl > 0:  # nur wenn noetig
            karren[name] = int(anzahl)  # eintragen
            rest -= int(anzahl) * eins  # Rest verkleinern
    if rest > 0:  # ein letzter, kleiner Karren fuer den Rest
        for name in sorted(reihenfolge, key=lambda n: E.ladung_der_gruppe({n: 1}, forschung)):
            eins = E.ladung_der_gruppe({name: 1}, forschung)  # Ladung dieses Karrens
            if eins >= rest:  # passt der Rest hinein?
                karren[name] = int(karren.get(name, 0)) + 1  # einen dazunehmen
                rest = 0  # alles getragen
                break  # fertig
    return {"ladung": int(summe), "karren": karren, "rest": int(rest)}  # Bedarf und Luecke


def transport_text(menge, forschung=None, pfad=None) -> str:
    """Der Satz fuer den Spieler: welche Ladung sein Anteil braucht und welche Karren dafuer.
    Eingabe: Beute-dict, optional der Forschungsstand.
    Ausgabe: Text aus `transport.hinweis` mit eingesetzter Ladung und Karrenliste."""
    daten_dict = daten(pfad)  # Datendatei
    block = daten_dict.get("transport") or {}  # Regel des Transports
    vorlage = str(block.get("hinweis") or "") if isinstance(block, dict) else ""  # Satz aus den Daten
    bedarf = transport_bedarf(menge, forschung, pfad)  # der Bedarf
    liste = ", ".join("%d %s" % (anzahl, name) for name, anzahl in sorted(bedarf["karren"].items()))
    if not liste:  # keine Karren noetig
        liste = "keine Karren"  # klarer Text
    return vorlage.replace("{ladung}", str(bedarf["ladung"])).replace("{karren}", liste)  # fertiger Satz


