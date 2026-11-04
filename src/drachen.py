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

def daten(pfad=None) -> dict:
    """Liest die Drachen-Datendatei und gibt sie als dict zurueck.
    Eingabe: optionaler Pfad zur JSON-Datei.
    Ausgabe: dict mit den geladenen Daten oder leeres dict bei Fehler."""
    if pfad is None:  # wenn kein Pfad angegeben ist
        pfad = os.path.join(spieldaten.projektwurzel(), "data", "drachen.json")  # baue den Standardpfad
    try:  # versuche die Datei zu lesen
        with open(pfad, encoding="utf-8") as datei:  # oeffne die Datei
            return json.load(datei)  # lade die JSON-Daten und gebe sie zurueck
    except (OSError, ValueError):  # Datei fehlt oder ist kein JSON
        return {}  # gebe ein leeres dict zurueck

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
        bild = figur_config.get("bild", "")  # hole den Drachenbildpfad
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
