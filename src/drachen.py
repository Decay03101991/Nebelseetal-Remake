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
    benoetigte_felder = ("id", "welt", "name", "x", "y", "wall_stufe", "einheiten", "beute", "ware")  # definiere die Pflichtfelder
    for feld in benoetigte_felder:  # iteriere ueber die Pflichtfelder
        if feld not in eintrag:  # wenn ein Feld fehlt
            return False  # dann ungueltig
    if not isinstance(eintrag["id"], str) or not isinstance(eintrag["welt"], str) or not isinstance(eintrag["name"], str):  # pruefe String-Typen
        return False  # wenn nicht string, ungueltig
    if not isinstance(eintrag["x"], int) or not isinstance(eintrag["y"], int):  # pruefe ob x und y ganze Zahlen sind
        return False  # wenn nicht int, ungueltig
    if not isinstance(eintrag["wall_stufe"], int):  # pruefe wall_stufe
        return False  # wenn nicht int, ungueltig
    if not isinstance(eintrag["einheiten"], dict):  # pruefe ob einheiten ein dict ist
        return False  # wenn nicht, ungueltig
    for anzahl in eintrag["einheiten"].values():  # iteriere ueber die Anzahlen
        if not isinstance(anzahl, int):  # wenn eine Anzahl keine ganze Zahl ist
            return False  # dann ungueltig
    for rohstoff, menge in eintrag["beute"].items():  # iteriere ueber die Beute
        if not isinstance(menge, (int, float)):  # wenn die Menge keine Zahl ist
            return False  # ungueltig
    for ware, anzahl in eintrag["ware"].items():  # iteriere ueber die Ware
        if not isinstance(anzahl, int):  # wenn die Warenanzahl keine ganze Zahl ist
            return False  # ungueltig
    if "wall_zustand" in eintrag:  # wenn wall_zustand vorhanden ist
        if not isinstance(eintrag["wall_zustand"], (int, float)):  # und keine Zahl ist
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
    """Gibt das Verteidiger-dict eines Drachen zurueck.
    Eingabe: ein Drachen-Eintrag.
    Ausgabe: dict {Einheit: Anzahl}."""
    return dict(eintrag.get("einheiten", {}))  # gebe eine Kopie des Verteidiger-dicts zurueck

def wall(eintrag) -> tuple:
    """Liefert Wallstufe und Wallzustand eines Drachen.
    Eingabe: ein Drachen-Eintrag.
    Ausgabe: Tupel (wall_stufe, wall_zustand)."""
    wall_stufe = eintrag.get("wall_stufe")  # hole wall_stufe aus dem Eintrag
    wall_zustand = eintrag.get("wall_zustand")  # hole wall_zustand aus dem Eintrag
    if wall_stufe is None:  # wenn wall_stufe fehlt
        daten_dict = daten()  # lade die Datendatei
        wall_stufe = daten_dict.get("standard_wall_stufe")  # hole Standardwert
    if wall_zustand is None:  # wenn wall_zustand fehlt
        daten_dict = daten()  # lade die Datendatei erneut
        wall_zustand = daten_dict.get("standard_wall_zustand")  # hole Standardwert
    return (wall_stufe, wall_zustand)  # gebe Tupel zurueck

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
