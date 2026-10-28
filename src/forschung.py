"""Nebelseetal Remake — zeitlicher Ablauf der Forschung (reine Rechenlogik).

Diese Schicht haelt *nur* den Ablauf: welche Stufe ein Gebiet hat, welcher Auftrag laeuft,
wie viel Zeit noch bleibt und wann eine Stufe steigt. Sie zeichnet keine Oberflaeche und
misst keine echte Uhr — der Zeitpunkt `jetzt` wird immer als Zahl in **Sekunden**
uebergeben. Nur so ist der Ablauf ohne Wartezeiten pruefbar.

Belegte Originalregeln (Handbuch 2009, Seiten 11-13) — nicht neu erfunden, sondern aus
`src/spieldaten.py` und `data/research.json` uebernommen:
  * Kosten verdoppeln sich je Stufe: Stufe 1 = 50 Holz, dann 100, 200, 400, 800 …
    (`spieldaten.forschungs_kosten`).
  * Dauer = neue Stufe zum Quadrat, in Stunden (`spieldaten.forschungsdauer_stunden`).
  * Die Stufe steigt **erst nach Ablauf** der Forschungszeit, nicht beim Klick.
  * Voraussetzung ist eine Bibliothek.
  * Ein laufender Auftrag sperrt die GANZE Siedlung: solange eine Bibliothek forscht, ist weder
    eine weitere Forschung noch der Ausbau der Bibliothek moeglich (Handbuch S. 12, Z. 423-424).
    KORREKTUR 05.10.2026: vorher sperrte der Code nur dasselbe Gebiet — belegter Widerspruch
    gegen das Handbuch (archiv/analysen/audits/handbuch_abgleich_2026-10-05.txt, Punkt 3). Das Handbuch
    gewinnt. Solange es EINE Bibliothek gibt, heisst „die Siedlung“ faktisch „keine weitere
    Forschung“; mit mehreren Siedlungen je eigener Bibliothek gilt die Sperre je Siedlung.
  * Abbruch: die Kosten sind verloren, die Stufe steigt nicht.
  * Forschungspunkte: Stufe hoch drei.

Der Aufrufer uebergibt seine Rohstoffe als veraenderbares Mapping
`vorhandene_rohstoffe` (z. B. `{"holz": 100, ...}`). Bei erfolgreichem Start zieht
`starten()` die Kosten **aus diesem Mapping ab** (in place) und legt sie zusaetzlich im
laufenden Auftrag unter `"kosten"` ab, damit der Aufrufer die Buchung nachvollziehen kann.
Schlaegt der Start fehl, bleibt das Mapping unveraendert.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

import spieldaten

STUNDEN_IN_SEKUNDEN = 3600


# --------------------------------------------------------------- Hilfsfunktionen

def dauer_stunden(stufe: int) -> int:
    """Forschungsdauer fuer das Erreichen von `stufe`: Stufe zum Quadrat, in Stunden.

    Delegiert an die Originalregel in `spieldaten`. Fuer Stufen unter 1 gibt es nichts zu
    erforschen -> 0 Stunden.
    """
    if stufe < 1:
        return 0
    return spieldaten.forschungsdauer_stunden(stufe)


def dauer_sekunden(stufe: int) -> int:
    return dauer_stunden(stufe) * STUNDEN_IN_SEKUNDEN


def kosten(neue_stufe: int) -> Dict[str, int]:
    """Rohstoffkosten, um ein Gebiet auf `neue_stufe` zu bringen (Original: Verdopplung)."""
    return spieldaten.forschungs_kosten(neue_stufe)


def gebiete() -> List[str]:
    """Die 21 Forschungsgebiete des Originals (Schluessel von `data/research.json`)."""
    return list(spieldaten.forschungen().keys())


def neuer_stand(gebiete_liste: Optional[List[str]] = None) -> Dict[str, Dict[str, Any]]:
    """Frischer Stand: jedes Gebiet auf Stufe 0, kein laufender Auftrag.

    Ohne Argument werden alle 21 Originalforschungen angelegt.
    """
    namen = gebiete() if gebiete_liste is None else list(gebiete_liste)
    return {name: {"stufe": 0, "auftrag": None} for name in namen}


def restzeit_stunden(auftrag: Optional[Dict[str, Any]], jetzt: float) -> float:
    """Verbleibende Stunden eines Auftrags zu `jetzt` (mindestens 0, nie negativ)."""
    if not auftrag:
        return 0.0
    ende_sekunden = auftrag["startzeit"] + auftrag["dauer_stunden"] * STUNDEN_IN_SEKUNDEN
    return max(0.0, (ende_sekunden - jetzt) / STUNDEN_IN_SEKUNDEN)


def restzeit_sekunden(auftrag: Optional[Dict[str, Any]], jetzt: float) -> float:
    return restzeit_stunden(auftrag, jetzt) * STUNDEN_IN_SEKUNDEN


def naechste_stufe(stand: Dict[str, Dict[str, Any]], gebiet: str) -> int:
    return stand[gebiet]["stufe"] + 1


def naechste_kosten(stand: Dict[str, Dict[str, Any]], gebiet: str) -> Dict[str, int]:
    """Was die naechste Stufe des Gebiets kostet — zum Anzeigen, ohne zu starten."""
    return kosten(naechste_stufe(stand, gebiet))


def _fehlende_rohstoffe(kosten_dict: Dict[str, int],
                        vorhandene_rohstoffe: Dict[str, int]) -> Dict[str, int]:
    """Je Rohstoff, wie viel fehlt (nur Rohstoffe mit Fehlbetrag)."""
    fehlt: Dict[str, int] = {}
    for rohstoff, benoetigt in kosten_dict.items():
        vorhanden = vorhandene_rohstoffe.get(rohstoff, 0)
        if vorhanden < benoetigt:
            fehlt[rohstoff] = benoetigt - vorhanden
    return fehlt


# --------------------------------------------------------------- Ablauf

def starten(gebiet: str,
            stand: Dict[str, Dict[str, Any]],
            jetzt: float,
            hat_bibliothek: bool,
            vorhandene_rohstoffe: Optional[Dict[str, int]] = None) -> Tuple[bool, str]:
    """Startet die Forschung im Gebiet auf die naechste Stufe.

    Prueft (1) bekannte Gebiete, (2) Bibliothek, (3) dass im Gebiet nichts laeuft und
    (4) die Rohstoffkosten. Bei Erfolg werden die Kosten aus `vorhandene_rohstoffe`
    abgezogen und der Auftrag gesetzt — die **Stufe steigt noch nicht**, erst nach Ablauf.

    Rueckgabe: ``(ja/nein, Meldung)``. Bei einer Ablehnung nennt die Meldung den Grund
    (fehlende Bibliothek bzw. den fehlenden Rohstoff), das Mapping bleibt unveraendert.
    """
    if gebiet not in stand:
        return False, f"Unbekanntes Forschungsgebiet: {gebiet}."
    if not hat_bibliothek:
        return False, "Forschung braucht eine Bibliothek."
    # Handbuch S. 12 (Z. 423-424): Während eines Forschungsauftrags kann in dieser Siedlung
    # WEDER eine weitere Forschung erteilt noch die Bibliothek ausgebaut werden. Der Code
    # sperrte früher nur das GLEICHE Gebiet (korrigiert 05.10.2026).
    laufend = [name for name, eintrag in stand.items() if eintrag.get("auftrag") is not None]
    if laufend:
        return False, (f"In dieser Siedlung forscht bereits {laufend[0]} — "
                       f"erst nach dessen Abschluss ist eine weitere Forschung möglich "
                       f"(Handbuch S. 12).")

    neue_stufe = naechste_stufe(stand, gebiet)
    kosten_dict = kosten(neue_stufe)

    if vorhandene_rohstoffe is not None:
        fehlt = _fehlende_rohstoffe(kosten_dict, vorhandene_rohstoffe)
        if fehlt:
            teile = ", ".join(f"{menge} {rohstoff}" for rohstoff, menge in fehlt.items())
            return False, f"Zu wenig Rohstoffe für {gebiet}: es fehlen {teile}."
        for rohstoff, menge in kosten_dict.items():
            vorhandene_rohstoffe[rohstoff] = vorhandene_rohstoffe.get(rohstoff, 0) - menge

    dauer = dauer_stunden(neue_stufe)
    stand[gebiet]["auftrag"] = {
        "zielstufe": neue_stufe,
        "startzeit": jetzt,
        "dauer_stunden": dauer,
        "kosten": dict(kosten_dict),
    }
    return True, (f"Forschung {gebiet} Stufe {neue_stufe} gestartet "
                  f"({dauer} h, Kosten {kosten_dict}).")


def fortschritt(stand: Dict[str, Dict[str, Any]],
                jetzt: float) -> Dict[str, Dict[str, Any]]:
    """Zustand je Gebiet zu `jetzt`.

    Je Gebiet ein dict mit:
      ``laufend``    — laeuft gerade ein Auftrag?
      ``fertig``     — ist die Zeit abgelaufen (noch nicht abgeschlossen)?
      ``reststunden``— verbleibende Stunden (None, wenn kein Auftrag laeuft)
      ``zielstufe``  — Zielstufe des Auftrags (None ohne Auftrag)
      ``stufe``      — aktuelle Stufe des Gebiets
    """
    out: Dict[str, Dict[str, Any]] = {}
    for name, eintrag in stand.items():
        laufend = eintrag.get("auftrag")
        if laufend is None:
            out[name] = {
                "stufe": eintrag["stufe"],
                "laufend": False,
                "fertig": False,
                "reststunden": None,
                "zielstufe": None,
            }
        else:
            rest = restzeit_stunden(laufend, jetzt)
            out[name] = {
                "stufe": eintrag["stufe"],
                "laufend": True,
                "fertig": rest <= 0,
                "reststunden": rest,
                "zielstufe": laufend["zielstufe"],
            }
    return out


def abschliessen(stand: Dict[str, Dict[str, Any]], jetzt: float) -> List[str]:
    """Laesst alle Gebiete steigen, deren Forschungszeit abgelaufen ist.

    Setzt die Stufe auf die Zielstufe und entfernt den Auftrag. Gibt die Namen der
    gestiegenen Gebiete zurueck. **Mehrfach aufrufbar**: ein bereits abgeschlossenes
    Gebiet hat keinen Auftrag mehr und steigt nicht erneut.
    """
    gestiegen: List[str] = []
    for name, eintrag in stand.items():
        laufend = eintrag.get("auftrag")
        if laufend is not None and restzeit_stunden(laufend, jetzt) <= 0:
            eintrag["stufe"] = laufend["zielstufe"]
            eintrag["auftrag"] = None
            gestiegen.append(name)
    return gestiegen


def abbrechen(stand: Dict[str, Dict[str, Any]],
              jetzt: float,
              gebiet: str) -> Tuple[bool, str]:
    """Bricht einen laufenden Auftrag ab: Stufe steigt nicht, Kosten bleiben verloren.

    Der beim Start abgezogene Rohstoff wird **nicht** erstattet.
    """
    if gebiet not in stand:
        return False, f"Unbekanntes Forschungsgebiet: {gebiet}."
    if stand[gebiet]["auftrag"] is None:
        return False, f"Im Gebiet {gebiet} laeuft kein Auftrag."
    stand[gebiet]["auftrag"] = None
    return True, (f"Forschungsauftrag in {gebiet} abgebrochen — "
                  f"die aufgebrachten Rohstoffe sind verloren.")


def punkte(stand: Dict[str, Dict[str, Any]]) -> int:
    """Forschungspunkte: Stufe hoch drei, Gesamtsumme ueber alle Gebiete."""
    return sum(int(eintrag["stufe"]) ** 3 for eintrag in stand.values())


def punkte_je_gebiet(stand: Dict[str, Dict[str, Any]]) -> Dict[str, int]:
    return {name: int(eintrag["stufe"]) ** 3 for name, eintrag in stand.items()}
