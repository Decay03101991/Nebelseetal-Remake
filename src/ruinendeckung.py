# -*- coding: utf-8 -*-
"""Ruinendeckung: eine besiegte Ruine deckt die Richtung, in der sie liegt (Frage 9, Register 216).

Daniels Entscheidung (05.11.2026, Frage 9): "Die besiegte Ruine sperrt ihre Seite - kein Angriff
aus dieser Richtung." Woertlich-nah aus derselben Runde: der Spieler soll "von einer seite nicht
angegriffen werden, wenn er neben sich eine bereits besiegte ruine stellt" - die Ruine ist damit
ein taktischer Punkt, kein zweites Gefecht und keine Regeneration (Frage 3).

WAS DIESES MODUL RECHNET - und was nicht:
  * Es rechnet NUR Geometrie: aus zwei Positionen auf demselben Weltfeld wird eine von acht
    Himmelsrichtungen (N, NO, O, SO, S, SW, W, NW), und eine Ruine deckt ihren eigenen Sektor.
  * Es liest KEINE Datei und kennt keinen Spielstand. Welche Ruinen es gibt, wo sie stehen und
    ob sie besiegt sind, entscheidet der Aufrufer (`GameState.ruinendeckungen`).
  * Eine REICHWEITE nennt das Original nicht. Deshalb gilt: die Ruine deckt ihren Sektor bis zum
    Rand der Karte. Das ist eine gesetzte Regel (VORSCHLAG), keine belegte - sie steht so im
    Register und ist Daniels Entscheidung, wenn er eine Reichweite will.

EINE Stelle: liegt die Rechnung hier, koennen Kampfweg und Anzeige nicht auseinanderlaufen.
"""
from __future__ import annotations

import math

# Die acht Richtungen im Uhrzeigersinn ab Norden - Index = Sektor.
RICHTUNGEN = ("N", "NO", "O", "SO", "S", "SW", "W", "NW")

# Die ausgeschriebenen Namen fuer Anzeigetexte (echte Umlaute: Anzeige, kein Datenschluessel).
RICHTUNG_TEXT = {
    "N": "Norden", "NO": "Nordosten", "O": "Osten", "SO": "Südosten",
    "S": "Süden", "SW": "Südwesten", "W": "Westen", "NW": "Nordwesten",
}


def _winkel(dx: float, dy: float) -> float:
    """Der Winkel von der Senkrechten nach oben, im Uhrzeigersinn, in Grad (0..360).

    `dy` zeigt nach UNTEN (wie in der Spielkarte), deshalb das Minus: (0, -1) ist Norden.
    """
    return (math.degrees(math.atan2(float(dx), -float(dy))) + 360.0) % 360.0


def richtung(von, nach) -> str:
    """Die Himmelsrichtung von `von` nach `nach` als Kuerzel - "" bei unbrauchbarer Angabe.

    Acht Sektoren zu je 45 Grad; die Grenze liegt bei 22,5 Grad um jede Himmelsrichtung, damit
    eine Position genau im Osten auch "O" heisst und nicht "NO".
    """
    try:
        x1, y1 = float(von[0]), float(von[1])                      # Ausgangspunkt
        x2, y2 = float(nach[0]), float(nach[1])                    # Zielpunkt
    except (TypeError, ValueError, IndexError, KeyError):          # kaputte oder fehlende Angabe
        return ""                                                  # dann keine Richtung
    if x1 == x2 and y1 == y2:                                      # derselbe Punkt
        return ""                                                  # hat keine Richtung
    sektor = int((( _winkel(x2 - x1, y2 - y1) + 22.5) % 360.0) // 45.0)   # 0..7
    return RICHTUNGEN[sektor]                                      # Kuerzel zurueck


def richtung_text(kuerzel: str) -> str:
    """Der ausgeschriebene Name einer Richtung ("NO" -> "Nordosten"); Unbekanntes bleibt leer."""
    return RICHTUNG_TEXT.get(str(kuerzel or "").upper(), "")


def deckung(verteidiger, angreifer, ruinen) -> dict:
    """Deckt eine Ruine den Angriff auf `verteidiger` ab? Gibt die Deckung zurueck oder {}.

    `ruinen` ist eine Liste von Eintraegen `{"name": str, "position": (x, y)}` - mehr braucht die
    Rechnung nicht. Gedeckt ist ein Angriff, wenn eine Ruine im SELBEN Sektor liegt wie der
    Angreifer (gesehen vom verteidigten Ort). Mehrere Deckungen: die naechstgelegene gewinnt,
    damit die Anzeige einen klaren Namen nennen kann.
    """
    seite_angreifer = richtung(verteidiger, angreifer)              # aus welcher Richtung kommt er
    if not seite_angreifer:                                         # keine Richtung bestimmbar
        return {}                                                   # dann keine Deckung
    treffer = []                                                    # welche Ruine deckt
    for ruine in (ruinen or []):                                    # jede bekannte Ruine
        if not isinstance(ruine, dict):                             # unbrauchbarer Eintrag
            continue                                                # ueberspringen
        stelle = ruine.get("position")                              # ihre Lage
        if richtung(verteidiger, stelle) != seite_angreifer:        # anderer Sektor
            continue                                                # deckt nicht
        try:                                                        # Abstand fuer die Auswahl
            abstand = math.hypot(float(stelle[0]) - float(verteidiger[0]),
                                 float(stelle[1]) - float(verteidiger[1]))
        except (TypeError, ValueError, IndexError):                 # unbrauchbare Lage
            continue                                                # ueberspringen
        treffer.append((abstand, str(ruine.get("name") or "")))     # Abstand und Name merken
    if not treffer:                                                 # keine Ruine im Sektor
        return {}                                                   # dann keine Deckung
    treffer.sort()                                                  # naechstgelegene zuerst
    return {"richtung": seite_angreifer,
            "richtung_text": richtung_text(seite_angreifer),
            "ruine": treffer[0][1]}                                 # Name der deckenden Ruine


def deckungen(ort, ruinen) -> list:
    """ALLE Richtungen, die dieser Ort durch Ruinen deckt - fuer die Anzeige.

    Rueckgabe: Liste `[{"richtung", "richtung_text", "ruine"}]`, sortiert nach Richtung. Eine
    Ruine auf demselben Feld wie der Ort deckt nichts (sie kann nicht "aus einer Richtung" kommen).
    """
    ergebnis = []                                                   # je Sektor hoechstens eine Deckung
    gesehen = set()                                                 # schon belegte Sektoren
    for ruine in (ruinen or []):                                    # jede bekannte Ruine
        if not isinstance(ruine, dict):                             # unbrauchbarer Eintrag
            continue                                                # ueberspringen
        kuerzel = richtung(ort, ruine.get("position"))              # ihr Sektor vom Ort aus
        if not kuerzel or kuerzel in gesehen:                       # unbrauchbar oder schon belegt
            continue                                                # ueberspringen
        gesehen.add(kuerzel)                                        # Sektor merken
        ergebnis.append({"richtung": kuerzel,                       # Kuerzel
                         "richtung_text": richtung_text(kuerzel),   # ausgeschriebener Name
                         "ruine": str(ruine.get("name") or "")})    # Name der Ruine
    return sorted(ergebnis, key=lambda e: RICHTUNGEN.index(e["richtung"]))   # N vor NO vor O ...


def deckung_text(ort_name: str, liste) -> str:
    """Eine Zeile fuer die Anzeige ("Gedeckt: Norden durch die Ruine X, ...") - oder "".

    Ohne Deckung kommt der LEERE Text zurueck; die Anzeige zeigt dann keine Zeile. Kein Satz
    ueber eine Deckung, die es nicht gibt.
    """
    teile = ["%s durch die Ruine %s" % (e.get("richtung_text") or e.get("richtung") or "",
                                        e.get("ruine") or "")
             for e in (liste or []) if e.get("richtung")]
    if not teile:                                                   # nichts gedeckt
        return ""                                                   # dann keine Zeile
    return "%s ist gedeckt: %s." % (ort_name or "Der Ort", ", ".join(teile))
