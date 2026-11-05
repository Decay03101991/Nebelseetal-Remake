# -*- coding: utf-8 -*-
"""Ruinendeckung: eine besiegte Ruine deckt die Richtung, in der sie liegt (Frage 9, Register 216).

Daniels Entscheidung (05.11.2026, Frage 9): "Die besiegte Ruine sperrt ihre Seite - kein Angriff
aus dieser Richtung." Woertlich-nah aus derselben Runde: der Spieler soll "von einer seite nicht
angegriffen werden, wenn er neben sich eine bereits besiegte ruine stellt" - die Ruine ist damit
ein taktischer Punkt, kein zweites Gefecht und keine Regeneration (Frage 3).

WAS DIESES MODUL RECHNET - und was nicht:
  * Es rechnet NUR Geometrie: aus zwei Positionen auf demselben Weltfeld wird eine von acht
    Himmelsrichtungen (N, NO, O, SO, S, SW, W, NW) - gebraucht fuer die Anzeige, in welcher
    Richtung eine Ruine liegt.
  * Es liest KEINE Datei und kennt keinen Spielstand. Welche Ruinen es gibt, wo sie stehen und
    ob sie besiegt sind, entscheidet der Aufrufer (`GameState.ruinendeckungen`).
  * **Wie weit eine Ruine deckt, hat Daniel am 05.11.2026 entschieden**, woertlich: "Die ruine
    deckt nur ihre eigene koordinate und stellt somit eine seite da von der man nicht angegriffen
    werden kann theoretisch sonst nichts." Also deckt sie **NUR ihr eigenes Feld**
    (`DECKWEITE_FELDER = 0`). Eine Siedlung daneben ist NICHT geschuetzt. Weil ein Ruinenfeld
    ohnehin fuer jeden gesperrt ist, ist der Schutz in der Praxis fast nie ausgeloest - das ist
    Daniels Entscheidung und keine Luecke im Code. Wer die Deckung spaeter weiter haben will,
    setzt `DECKWEITE_FELDER` auf die Feldzahl; die Rechnung bleibt dieselbe.

EINE Stelle: liegt die Rechnung hier, koennen Kampfweg und Anzeige nicht auseinanderlaufen.
"""
from __future__ import annotations

import math

# Die acht Richtungen im Uhrzeigersinn ab Norden - Index = Sektor.
# WIE WEIT eine Ruine deckt (Daniels Entscheidung 05.11.2026, Frage 9): 0 = NUR ihr eigenes
# Feld. Eine Ruine neben der Siedlung schuetzt die Siedlung NICHT.
DECKWEITE_FELDER = 0

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

    **Daniels Entscheidung (05.11.2026):** "Die ruine deckt nur ihre eigene koordinate und stellt
    somit eine seite da von der man nicht angegriffen werden kann theoretisch sonst nichts."
    Gedeckt ist ein Angriff deshalb NUR dann, wenn er von **genau dem Feld der Ruine** ausgeht
    (`DECKWEITE_FELDER = 0`). Eine Ruine neben der Siedlung schuetzt die Siedlung **nicht**.

    `ruinen` ist eine Liste von Eintraegen `{"name": str, "position": (x, y)}`.
    """
    ziel = _punkt(verteidiger)                                      # der verteidigte Ort
    herkunft = _punkt(angreifer)                                    # woher der Angriff kommt
    if ziel is None or herkunft is None:                            # unbrauchbare Angabe
        return {}                                                   # dann keine Deckung
    beste = None                                                    # die naechstgelegene Deckung
    for ruine in (ruinen or []):                                    # jede bekannte Ruine
        if not isinstance(ruine, dict):                             # unbrauchbarer Eintrag
            continue                                                # ueberspringen
        stelle = _punkt(ruine.get("position"))                       # ihre Lage
        if stelle is None:                                          # ohne Lage
            continue                                                # ueberspringen
        abstand = math.hypot(stelle[0] - ziel[0], stelle[1] - ziel[1])   # wie weit sie liegt
        # Gedeckt ist, was VON DIESEM FELD kommt - der Abstand zur Siedlung spielt keine Rolle.
        if _abstand(herkunft, stelle) <= float(DECKWEITE_FELDER):
            if beste is None or abstand < beste[0]:                  # die naechste gewinnt
                beste = (abstand, stelle, str(ruine.get("name") or ""))   # merken
    if beste is None:                                                # keine Ruine deckt
        return {}                                                    # dann keine Deckung
    kuerzel = richtung(ziel, beste[1])                               # wo die Ruine liegt
    return {"richtung": kuerzel,                                     # Kuerzel (leer bei gleichem Feld)
            "richtung_text": richtung_text(kuerzel) or "eigenem Feld",   # ausgeschrieben
            "ruine": beste[2]}                                       # Name der deckenden Ruine


def deckungen(ort, ruinen) -> list:
    """Alle Ruinen um diesen Ort mit ihrer Richtung - fuer die Anzeige.

    Rueckgabe: Liste `[{"richtung", "richtung_text", "ruine"}]`, sortiert nach Richtung. Die Liste
    sagt NUR, wo die Ruinen liegen; sie decken nach Daniels Entscheidung ausschliesslich ihr eigenes
    Feld. Wer mehr daraus liest, liest mehr, als entschieden ist.
    """
    ergebnis = []                                                   # je Ruine ein Eintrag
    gesehen = set()                                                 # schon belegte Namen
    for ruine in (ruinen or []):                                    # jede bekannte Ruine
        if not isinstance(ruine, dict):                             # unbrauchbarer Eintrag
            continue                                                # ueberspringen
        name = str(ruine.get("name") or "")                          # Name der Ruine
        if not name or name in gesehen:                             # doppelt oder leer
            continue                                                # ueberspringen
        gesehen.add(name)                                           # Namen merken
        kuerzel = richtung(ort, ruine.get("position"))               # ihr Sektor vom Ort aus
        ergebnis.append({"richtung": kuerzel,                        # Kuerzel
                         "richtung_text": richtung_text(kuerzel),    # ausgeschriebener Name
                         "ruine": name})                             # Name der Ruine
    return sorted(ergebnis, key=lambda e: (RICHTUNGEN.index(e["richtung"])
                                           if e["richtung"] in RICHTUNGEN else 99))   # N vor NO vor O ...


def deckung_text(ort_name: str, liste) -> str:
    """Eine Zeile fuer die Anzeige - oder "" ohne Ruine.

    Nach Daniels Entscheidung deckt eine Ruine NUR ihr eigenes Feld; die Zeile sagt das ausdruecklich,
    damit niemand annimmt, die Siedlung sei geschuetzt.
    """
    teile = []
    for e in (liste or []):
        name = e.get("ruine") or ""                                  # Name der Ruine
        if not name:                                                # ohne Namen
            continue                                                # ueberspringen
        lage = e.get("richtung_text") or ""                          # wo sie liegt
        teile.append(("im %s die Ruine %s" % (lage, name)) if lage else ("die Ruine %s" % name))
    if not teile:                                                   # keine Ruine
        return ""                                                   # dann keine Zeile
    return ("%s: %s — eine Ruine deckt nur ihr eigenes Feld, sonst nichts."
            % (ort_name or "Der Ort", ", ".join(teile)))


def _punkt(angabe):
    """Eine Lage als (x, y) aus Tupel/Liste/Dict - None, wenn sie nicht brauchbar ist."""
    try:
        if isinstance(angabe, dict):                                # {"x": ..., "y": ...}
            return (int(angabe.get("x")), int(angabe.get("y")))     # aus dem Dict
        return (int(angabe[0]), int(angabe[1]))                     # aus Tupel oder Liste
    except (TypeError, ValueError, IndexError, KeyError):            # kaputte Angabe
        return None                                                 # dann keine Lage


def _abstand(a, b) -> float:
    """Der Feldabstand zwischen zwei Lagen (Wurzel aus den Quadraten)."""
    return math.hypot(float(a[0]) - float(b[0]), float(a[1]) - float(b[1]))
