# -*- coding: ascii -*-
"""S3 Verwundetenheilung (06.11.2026) - die EINE Rechenstelle fuer Verwundete.

Was hinein geht: die Verluste eines Ortes, der Einheitenname, der Forschungsstand, die Spielzeit.
Was heraus kommt: die Zahl der Verwundeten (30 Prozent, abgerundet), die Heilungskosten (75 Prozent
der Kostenposten ohne Siedler und ohne Ausruestung), die Heildauer (50 Prozent der Ausbildungsdauer)
und neue Zeilen in der vorhandenen Warteschlange `ausbildung`.

Warum ein eigenes Modul: der Kern rechnet, die Anzeige liest - keine zweite Wahrheit. Alle Zahlen
stehen in `data/verwundete.json`; fehlt die Datei, gilt der Vorgabesatz (nie geraten).
Entscheidungen: docs/ENTSCHEIDUNGEN_DANIEL_20261106_GEMINI_ANTWORTEN.md Frage 6 und Runde 3 Frage 6.
"""
from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Dict

import spieloekonomie                      # Ausbildungsdauer, Kosten und Buchung (die vorhandene Stelle)

DATENDATEI = Path(__file__).resolve().parent.parent / "data" / "verwundete.json"   # Zahlen des Schnitts
VORGABE = {"aktiv": True,                  # ohne Schalter gilt: Mechanik an (Daniel hat sie beauftragt)
           "verwundeten_anteil_prozent": 30,   # 30 Prozent der Verluste werden verwundet
           "heilungskosten_prozent": 75,       # 75 Prozent der Kostenposten als Heilpreis
           "heilungsdauer_prozent": 50}        # 50 Prozent der Ausbildungsdauer als Heildauer


def regeln() -> dict:
    """Liest die Zahlen aus `data/verwundete.json`; fehlt sie, gilt der Vorgabesatz."""
    daten = dict(VORGABE)                  # mit der Vorgabe beginnen - nie mit Nullen rechnen
    try:                                   # Datei lesen kann fehlen oder kaputt sein
        roh = json.loads(DATENDATEI.read_text(encoding="utf-8"))   # JSON der Datendatei
    except (OSError, ValueError):          # keine Datei oder kein gueltiges JSON
        return daten                       # dann bleibt der Vorgabesatz stehen
    if not isinstance(roh, dict):          # eine Liste waere kein Regelsatz
        return daten                       # dann ebenfalls die Vorgabe
    for schluessel in VORGABE:             # jeden bekannten Schluessel einzeln uebernehmen
        if schluessel in roh:              # nur was wirklich in der Datei steht
            daten[schluessel] = roh[schluessel]   # Wert aus der Datei (fuehrend)
    return daten                           # fertiger Regelsatz


REGELN = regeln()                          # einmal beim Import gelesen (wie spieloekonomie.REGELN)


def aktiv() -> bool:
    """Ist die Mechanik eingeschaltet? (Schalter aus `data/verwundete.json`)."""
    return bool((regeln() or {}).get("aktiv"))   # frisch gelesen, damit ein Test umschalten kann


def anteil_verwundete(verluste) -> Dict[str, int]:
    """Rechnet aus den Verlusten eines Ortes die Verwundeten: 30 Prozent je Typ, ABGERUNDET.

    Beispiel (Vorgabe): 10 Verluste -> 3 Verwundete, 9 Verluste -> 2 (nicht 3), 1 Verlust -> 0.
    Die Funktion bucht NICHTS - sie liefert nur die Zahlen, damit der Aufrufer sie VOR dem
    Loeschen der Einheiten eintragen kann (S3: Verwundete entstehen vor der Verlustbuchung).
    """
    if not isinstance(verluste, dict):     # keine Verlustangabe uebergeben
        return {}                          # dann gibt es auch keine Verwundeten
    satz = float((regeln() or {}).get("verwundeten_anteil_prozent", 0) or 0)   # Anteil in Prozent
    if satz <= 0:                          # Mechanik ohne Anteil
        return {}                          # dann nichts erzeugen
    ergebnis: Dict[str, int] = {}          # je Einheitentyp die Zahl der Verwundeten
    for name, anzahl in verluste.items():  # jeder Einheitentyp einzeln
        try:                               # die Verlustzahl muss eine Zahl sein
            betrag = float(anzahl)         # in Fliesskomma umrechnen
        except (TypeError, ValueError):    # unbrauchbare Angabe
            continue                       # dann diesen Typ ueberspringen
        if betrag <= 0:                    # kein Verlust
            continue                       # dann auch kein Verwundeter
        anzahl_verwundet = int(math.floor(betrag * satz / 100.0))   # ABRUNDEN (Daniel, Entscheidung 6)
        if anzahl_verwundet > 0:           # nur echte Verwundete eintragen
            ergebnis[str(name)] = anzahl_verwundet   # Zaehler je Typ
    return ergebnis                        # fertige Verwundetenzahl


def heilungsdauer(name: str, ausbildungsdauer=None) -> float:
    """Heildauer einer Einheit: 50 Prozent der Ausbildungsdauer (Stufe 1: 1200 s -> 600 s).

    Wird die Dauer der Staette uebergeben (`spieloekonomie.ausbildung_grenzen`), gilt sie mit
    ihrem Stufenfaktor; ohne Angabe gilt die belegte Grunddauer (20 Minuten).
    """
    dauer = 0.0                                                # Ausgangswert
    try:                                                       # die uebergebene Dauer hat Vorrang
        dauer = float(ausbildungsdauer or 0.0)                 # Dauer der Staette (Stufe)
    except (TypeError, ValueError):                            # unbrauchbare Angabe
        dauer = 0.0                                            # dann die Grunddauer nehmen
    if dauer <= 0:                                             # ohne Dauer
        dauer = float(spieloekonomie.REGELN.get("pilot_ausbildung_minuten", 20) or 20) * 60.0   # 20 min
    satz = float((regeln() or {}).get("heilungsdauer_prozent", 0) or 0)   # Anteil in Prozent
    return dauer * satz / 100.0                                # 50 Prozent davon


def heilungskosten(name: str) -> Dict[str, float]:
    """Heilpreis einer Einheit: 75 Prozent ALLER Kostenposten, ohne `siedler` und ohne `waren`."""
    eintrag = spieloekonomie.U.get(name) or {}                 # Einheit aus data/units.json
    kosten = dict(eintrag.get("kosten") or {})                 # alle Kostenposten der Einheit
    kosten.pop("siedler", None)                                # Siedler sterben nicht, sie kehren zurueck
    satz = float((regeln() or {}).get("heilungskosten_prozent", 0) or 0)   # Anteil in Prozent
    ergebnis: Dict[str, float] = {}                            # Preis je Rohstoff
    for rohstoff, betrag in kosten.items():                    # jeden Posten einzeln rechnen
        try:                                                   # der Posten muss eine Zahl sein
            wert = float(betrag)                               # in Fliesskomma wandeln
        except (TypeError, ValueError):                        # unbrauchbarer Posten
            continue                                           # dann ueberspringen
        if wert <= 0:                                          # ein Nullposten kostet nichts
            continue                                           # dann nicht auffuehren
        ergebnis[str(rohstoff)] = round(wert * satz / 100.0, 2)   # 75 Prozent, auf zwei Stellen
    return ergebnis                                            # fertiger Heilpreis


def heilung_grenzen(ort: dict, name: str, forschung) -> dict:
    """Wie viele verwundete Einheiten dieser Art der Ort JETZT heilen kann - die EINE Rechenstelle.

    Geprueft werden: Verwundete vor Ort, die Ausbildungsstaette (dieselbe wie fuer die Ausbildung),
    die Forschung der Einheit und das Ortslager. Rueckgabe nennt jede Bedingung EINZELN.
    """
    leer = {"einheit": name, "moeglich": 0, "kosten_je": {}, "dauer_je": 0.0,
            "gebaeude": None, "stufe": 0, "verwundet": 0, "hindernisse": []}   # Grundform
    if not isinstance(ort, dict):                    # kein Ort uebergeben
        leer["hindernisse"].append("Kein Ort ausgewaehlt.")   # ehrlicher Grund
        return leer                                  # dann nichts moeglich
    feld = ort.get("verwundete") or {}               # Verwundete dieses Ortes
    verwundet = int(feld.get(name, 0) or 0) if isinstance(feld, dict) else 0   # Zahl je Einheit
    leer["verwundet"] = max(0, verwundet)            # nie negativ anzeigen
    try:                                             # die Ausbildung liefert Gebaeude, Stufe, Dauer
        grenzen = spieloekonomie.ausbildung_grenzen(ort, name, forschung or {})
    except (ValueError, KeyError, TypeError) as fehler:   # unbekannte Einheit
        leer["hindernisse"].append(str(fehler))      # Grund nennen
        return leer                                  # dann nichts moeglich
    leer["gebaeude"] = grenzen.get("gebaeude")       # dieselbe Staette wie die Ausbildung
    leer["stufe"] = int(grenzen.get("stufe") or 0)   # Ausbaustufe der Staette
    kosten = heilungskosten(name)                    # 75 Prozent der Kostenposten
    dauer = heilungsdauer(name, grenzen.get("dauer_je"))   # 50 Prozent der Dauer DIESER Staette
    leer["kosten_je"] = kosten                       # Preis je geheilter Einheit
    leer["dauer_je"] = dauer                         # Dauer je geheilter Einheit
    if grenzen.get("hindernis"):                     # Staette oder Forschung fehlt
        leer["hindernisse"].append(str(grenzen["hindernis"]))   # Grund der Ausbildung uebernehmen
    if verwundet <= 0:                               # niemand verwundet
        leer["hindernisse"].append("Keine Verwundeten dieser Art vor Ort.")   # dann nichts zu heilen
    vorraete = ort.get("vorraete") or {}             # Ortslager
    for rohstoff, betrag in sorted(kosten.items()):  # jeder Kostenposten einzeln pruefen
        bestand = float(vorraete.get(rohstoff, 0) or 0)   # Bestand dieses Rohstoffs
        if bestand < betrag:                         # reicht nicht
            leer["hindernisse"].append("%s fehlt %.2f (%.2f von %.2f)."
                                       % (rohstoff, betrag - bestand, bestand, betrag))   # Betrag nennen
    moeglich = max(0, verwundet)                     # hoechstens alle Verwundeten
    if grenzen.get("hindernis"):                     # ohne Staette keine Heilung
        moeglich = 0                                 # dann null
    else:                                            # Staette steht
        for rohstoff, betrag in kosten.items():      # je Posten die bezahlbare Menge
            if betrag > 0:                           # nur echte Kosten begrenzen
                moeglich = min(moeglich, int(float(vorraete.get(rohstoff, 0) or 0) // betrag))
    leer["moeglich"] = int(moeglich)                 # was JETZT bezahlbar ist
    return leer                                      # fertige Grenzen


def heilung_start_menge(ort: dict, name: str, forschung, jetzt: float, menge: int = 1) -> dict:
    """Reiht `menge` Heilungen in die vorhandene Warteschlange ein - alles oder nichts.

    Gebucht werden die Heilungskosten aus dem ORTSLAGER (`spieloekonomie.verbrauchen`) und die
    Verwundeten vor Ort; die Einheit selbst entsteht am Ende der Heildauer in `einheiten`.
    Rueckgabe wie `spieloekonomie.ausbildung_start_menge`: Ort, Anzahl, Dauer, Ende, Meldung.
    """
    menge = int(menge or 0)                          # Menge als ganze Zahl
    if menge < 1:                                    # ohne Menge nichts tun
        raise ValueError("Die Menge muss mindestens 1 sein.")   # ehrlicher Fehler
    grenzen = heilung_grenzen(ort, name, forschung or {})   # dieselben Grenzen wie die Anzeige
    if grenzen["hindernisse"]:                       # irgendeine Bedingung offen
        raise ValueError(" ".join(grenzen["hindernisse"]))   # alle Gruende nennen, nicht nur einen
    if menge > grenzen["moeglich"]:                  # mehr verlangt als bezahlbar
        raise ValueError("Es lassen sich jetzt nur %d von %s heilen."
                         % (grenzen["moeglich"], name))   # Zahl nennen
    kosten = {r: float(m) * menge for r, m in grenzen["kosten_je"].items()}   # Preis fuer die Menge
    neu = spieloekonomie.verbrauchen(ort, kosten, float(jetzt or 0.0))       # atomar abbuchen
    feld = dict(neu.get("verwundete") or {})         # Verwundete des Ortes
    feld[name] = max(0, int(feld.get(name, 0) or 0) - menge)   # geheilte abziehen (nie negativ)
    neu["verwundete"] = {k: int(v) for k, v in feld.items() if int(v) > 0}   # nur echte Zahlen
    geb = grenzen.get("gebaeude")                    # dieselbe Staette as die Ausbildung
    freie_zeit = max([float(jetzt or 0.0)] + [float(a.get("ende") or 0.0)
                                              for a in (neu.get("ausbildung") or [])
                                              if isinstance(a, dict) and a.get("gebaeude") == geb])   # hinten anstellen
    dauer = float(grenzen["dauer_je"])               # Heildauer je Einheit
    for _ in range(menge):                           # je Einheit eine Zeile
        neu.setdefault("ausbildung", []).append({"einheit": name, "gebaeude": geb,
                                                 "start": freie_zeit, "ende": freie_zeit + dauer,
                                                 "dauer_sekunden": dauer,
                                                 "stufe": int(grenzen["stufe"] or 0),
                                                 "gebucht": False, "heilung": True})   # Kennzeichen
        freie_zeit += dauer                          # naechste Einheit beginnt danach
    return {"ort": neu, "anzahl": menge, "einheit": name, "dauer_je": dauer,
            "ende": freie_zeit, "rest_sekunden": max(0.0, freie_zeit - float(jetzt or 0.0)),
            "kosten": kosten}                        # Ergebnis wie bei der Ausbildung
