# Code-Audit Nebelseetal Remake — Paket P3: Doppelte Rechenwege in Wirtschaft und Aufträgen

## Deine Rolle

Du bist Software-Architekt und prüfst einen gewachsenen Python-Code (tkinter-Spiel, deutsch
kommentiert, 18.400 Zeilen Prüfcode). Der Code ist über Monate **angebaut** worden: neue Funktionen
kamen dazu, alte blieben, Doppelungen wurden nie zusammengeführt. Deine Aufgabe ist **nicht**,
Eleganz zu predigen, sondern konkrete, umsetzbare Zusammenführungen zu benennen.

## Harte Regeln (daran wird deine Antwort gemessen)

1. **Das Spiel bleibt unser Spiel.** Kein Verhalten darf sich ändern: keine anderen Zahlen, keine
   anderen Regeln, keine andere Bedienung. Reine Struktur- und Lesbarkeitsarbeit.
2. **Jede Funktion bleibt erhalten**, solange sie aufgerufen wird. Was niemand aufruft, nennst du
   ausdrücklich als „entfernbar" mit Begründung.
3. **Der Prüfcode ist der Beweis.** Zu jedem Vorschlag gehört: welche vorhandene Prüfdatei
   (tests/*.py) muss danach grün bleiben? Wenn keine existiert, sagst du das offen.
4. **Deutsch, ASCII in Code-Kommentaren** (das Projekt hält `src/botkern.py` bewusst ASCII).
5. **Keine erfundenen Zeilenzahlen.** Wenn du eine Ersparnis schätzt, schreib „geschätzt".

## Was das Projekt über sich sagt (gemessen, nicht geschätzt)

* `src/`: 49 Dateien, 21.703 Zeilen, 17.406 Codezeilen, 904 Funktionen/Methoden.
* `main.py` allein: 7.375 Zeilen, 240 Methoden, davon 27 `_render_*`-Methoden.
* Funktionen ab 60 Zeilen: 47 (längste 205 Zeilen, `_render_settlement_map`).
* 58 Sechs-Zeilen-Blöcke stehen mehrfach identisch im Code.
* `kampf.py` (398 Z.) und `kampf_alt_handbuch_2009.py` (401 Z.) enthalten je eine
  `fuehre_schlacht` (188 bzw. 194 Zeilen) — `kampf.py` importiert die alte Fassung.
* Oberfläche: tkinter, alles in einer Klasse; Ansichten `_render_*`, Aufbau `_build_main_ui`.
* Prüfcode: `tests/` 18.418 Zeilen, 98 Dateien, Aufruf über `tools/sammellauf.py`.

## Deine Aufgabe

In `auftraege.py`, `spieloekonomie.py`, `werkstatt.py` und `kampfbericht.py` gibt es mehrfach Rechnungen für Reisezeit, Kosten, Bestand und Beute. Finde die Dubletten und schlage je eine gemeinsame Funktion vor (Name, Parameter, Rückgabe, wo sie hingehört). Wichtig: die Werte müssen exakt gleich bleiben — nenne für jede Dublette, ob die Formeln heute wirklich identisch sind oder nur ähnlich aussehen.

## Der Code

### Datei `src/auftraege.py` (638 Zeilen)

```python
"""
Nebelseetal Remake - Auftraege und Missionen (Paket WA, 04.10.2026).

Ein Auftrag ist eine Reise einer Einheitengruppe von der eigenen Siedlung zu einem
Ziel und (in der Regel) wieder zurueck. Dieses Modul fuehrt die Auftragsliste, die
Reisezeiten und die Auswertung. Den Kampf selbst baut es NICHT nach: fuer den Angriff
wird `kampfbericht.vorrunde` benutzt, fuer die Beute `kampfbericht.beute`.

BELEGT (docs/ENTWURF_AUFTRAEGE.md, Handbuch 2009):
  * vier Auftragsarten - stationieren, transportieren, handeln, angreifen,
  * eine Reise dauert Zeit, die Rueckkehr dauert genauso lange wie eine Strecke
    (S. 19: "Wenn also 2 Stunden angegeben sind, benoetigen Deine Einheiten 2 Stunden").
    Der Faktor HIN_UND_RUECK_FAKTOR = 2 bildet das ab.
  * die Ladung der Karren begrenzt, was mitgenommen werden kann (einheiten.ladung),
  * die Geschwindigkeit ist in 10-%-Schritten drosselbar (S. 20, woertlich:
    "in 10-%-Schritten drosselbar"); die Zahl steht als DROSSELUNG_SCHRITTE_PROZENT,
  * in fremden Siedlungen darf NICHT stationiert werden (S. 19),
  * transportieren nur mit Karren, handeln nur mit Handelskarawanen (Handbuch),
  * Angriff: Vorrunde gegen den Wall (Schwellen aus gebaeude_wirkung),
    Beute nur mit Transportkarren (S. 23).

NICHT belegt und darum VORSCHLAG (jeder eigene Wert mit Grund, siehe offene_luecken):
  * die Reisezeit-Formel SEKUNDEN_JE_FELD (das Handbuch nennt keine Entfernung/-
    Geschwindigkeit-Formel, nur Beispielstunden) - VORGABE Daniel 31.10.2026: Faktor 2,
    anpassbar (Registerpunkt 43),
  * die Dauer der Handlung am Ziel AKTION_DAUER_SEKUNDEN = 0,
  * der Beute-Anteil (VORGABE Daniel 31.10.2026: GESTAFFELT nach Wallzustand und Verteidigern,
    siehe kampfbericht.beute_staffel; die Prozentwerte sind Vorschlag),
  * die Wahl der langsamsten Einheit als Reisegeschwindigkeit,
  * dass eine Angreifer-Fussttruppe aus Kampf- UND Kundschaftereinheiten besteht
    (der Begriff ist im Handbuch nicht definiert).

Alle Funktionen sind rein: kein globaler Zustand, keine Datei wird geschrieben. Wie in
`werkstatt.py` fuehrt die Auftragsliste ihre Merker als Felder im Auftrag
('status', 'abgeliefert', 'angewendet'); der uebergebene Spielstand wird nie veraendert
(tiefe Kopie). Nur die Standardbibliothek plus die Projektdaten werden genutzt.
"""
from __future__ import annotations

import copy
from typing import Any, Dict, List, Optional, Tuple

import einheiten as E
import kampfbericht as KB

STAND = "2026-10-04.1"

# Die vier belegten Auftragsarten (docs/ENTWURF_AUFTRAEGE.md, Tabelle).
AUFTRAGSARTEN: Tuple[str, ...] = ("stationieren", "transportieren", "handeln", "angreifen")

# VORGABE DANIEL 31.10.2026 (Registerpunkt 43): Das Handbuch nennt KEINE Formel aus Entfernung und
# Geschwindigkeit, nur Beispielstunden (S. 19). Deshalb gilt als anpassbare Arbeitsformel:
#     Dauer (eine Strecke) = 2 * Entfernung / Geschwindigkeit  ->  2 * 3600 s je Feld und GS 1
# Grund fuer den Faktor 2: bei Spieluhr x180 waeren Wege mit Faktor 1 so kurz, dass der Verteidiger
# keine Vorwarnzeit hat. Der Faktor ist EINE Konstante und wird hier bewusst offen benannt.
SEKUNDEN_JE_FELD = 7200.0

# BELEGT: die Rueckkehr dauert so lange wie eine Strecke, zusammen also das Doppelte (S. 19).
HIN_UND_RUECK_FAKTOR = 2.0

# BELEGT: die Geschwindigkeit ist in 10-%-Schritten drosselbar (Handbuch S. 20, Z. 1191).
DROSSELUNG_SCHRITTE_PROZENT = 10
DROSSELUNG_ZITAT = "Drosselung in 10-%-Schritten (Handbuch 2009, Seite 20)"

# VORSCHLAG: Die Handlung am Ziel ist hier sofort fertig (Dauer 0). Das Handbuch nennt
# fuer stationieren/transportieren/angreifen keine Aufenthaltsdauer; handeln wartet laut
# Entwurf auf eine Bestaetigung, deren Dauer aber nicht beziffert ist. Der Zustand
# 'am_ziel' wird darum nur im Ankunftsaugenblick gezeigt.
AKTION_DAUER_SEKUNDEN = 0.0

# VORSCHLAG: Beutemenge 50 % der Lager, gedeckelt durch die Karrenladung. Der Entwurf
# selbst nennt diese Zahl ausdruecklich VORSCHLAG (docs/ENTWURF_AUFTRAEGE.md, "Was Daniel
# entscheiden muss", Punkt 3). Sie wird hier nur fuer den Angriff weitergereicht.
BEUTE_ANTEIL_PROZENT = 50


# ------------------------------------------------------------------------------ Hilfen

def _als_zahl(wert: Any, vorgabe: float = 0.0) -> float:
    try:
        return float(wert)
    except (TypeError, ValueError):
        return float(vorgabe)


def _als_int(wert: Any, vorgabe: int = 0) -> int:
    try:
        return int(float(wert))
    except (TypeError, ValueError):
        return int(vorgabe)


def _ziel_name(nach: Any) -> str:
    if isinstance(nach, dict):
        return str(nach.get("name") or "")
    return str(nach or "")


def _ziel_daten(nach: Any) -> Dict[str, Any]:
    return dict(nach) if isinstance(nach, dict) else {}


def _bestand(einheiten: Any) -> Dict[str, int]:
    """Nimmt {name: anzahl} und liefert nur brauchbare, positive Eintraege."""
    out: Dict[str, int] = {}
    if not isinstance(einheiten, dict):
        return out
    for name, anzahl in einheiten.items():
        n = _als_int(anzahl, 0)
        if n > 0:
            out[str(name)] = n
    return out


def _unbekannte(bestand: Dict[str, int]) -> List[str]:
    return sorted(n for n in bestand if n not in E.alle())


def _geschwindigkeit(bestand: Dict[str, int]) -> int:
    """Die langsamste mitgefuehrte Einheit bestimmt das Tempo (VORSCHLAG)."""
    werte = [E.geschwindigkeit(n) for n, k in bestand.items() if k > 0]
    werte = [g for g in werte if g > 0]
    return min(werte) if werte else 0


def tempo_der_gruppe(bestand: Dict[str, int]) -> int:
    """Reisegeschwindigkeit einer Truppe = langsamste mitgefuehrte Einheit.

    Oeffentlich, weil die WELTKARTE dieselbe Regel braucht (E3, Entscheidung Daniel 31.10.2026:
    "ein Bewegungssystem"). Vorher rechnete der Weltkarten-Altpfad 5 Minuten je Feld, voellig
    unabhaengig von der Einheit - zwei Formeln fuer dieselbe Sache (Register, offener Punkt H).
    """
    return _geschwindigkeit(_bestand(bestand))


def _schlagkraft_fussttruppen(bestand: Dict[str, int]) -> float:
    """Schlagkraft (SK) der Fuss- und Kundschaftertruppen (VORSCHLAG: Begriff, siehe luecken).

    BEFUND der externen Gegenpruefung (31.10.2026, Nr. 2), selbst nachgemessen: hier stand
    `E.angriff(n)` - das ist **AT**. Die Wallvorrunde in `kampf.fuehre_schlacht` prueft aber
    **SK** (Handbuch S. 21: Schwellenwerte der Fuss- und Belagerungstruppen). Weil AT weit
    hoeher liegt als SK (Kaempfer AT 40 gegen SK 2), bestand die Vorpruefung beim Auftrag
    fast immer und der Kampf scheiterte erst am Ziel. Jetzt gilt dieselbe Kennzahl wie im Kampf.
    """
    return float(sum(E.schlagkraft(n) * k for n, k in bestand.items() if E.ist_kaempfer(n)))


def _schlagkraft_belagerung(bestand: Dict[str, int]) -> float:
    return float(sum(E.schlagkraft(n) * k for n, k in bestand.items() if E.ist_belagerung(n)))


# ------------------------------------------------------------------------- Reisemodell

def reisezeit_sekunden(entfernung: Any, geschwindigkeit: Any) -> float:
    """Dauer EINER Strecke in Sekunden (Handbuch S. 19: die Dauer gilt fuer eine Strecke).

    Formel (VORSCHLAG, siehe offene_luecken['reisezeit_formel']):
        Sekunden = Entfernung / Geschwindigkeit * SEKUNDEN_JE_FELD
    Eine ungueltige (nicht positive) Geschwindigkeit liefert unendlich - der Auftrag
    kann so nicht starten; `starten` weist das vorher ab.
    """
    e = max(0.0, _als_zahl(entfernung))
    if e <= 0.0:
        return 0.0
    g = _als_zahl(geschwindigkeit)
    if g <= 0.0:
        return float("inf")
    return e / g * SEKUNDEN_JE_FELD


def ladung_der_mission(einheiten: Any) -> int:
    """Gesamte Tragefaehigkeit der mitgefuehrten Karren (einheiten.kapazitaet).

    Nur Transporteinheiten tragen; Kaempfer und Belagerungswaffen tragen nichts.
    """
    return int(max(0, sum(E.kapazitaet(n, k) for n, k in _bestand(einheiten).items())))


# ------------------------------------------------------------------------------ Arten

def auftragsarten() -> Dict[str, Dict[str, Any]]:
    """Die vier Auftragsarten mit ihren belegten Regeln und ausgewiesenen Vorschlaegen."""
    return {
        "stationieren": {
            "text": "Einheiten in einer eigenen Siedlung absetzen.",
            "belegt": ["In FREMDEN Siedlungen verboten (Handbuch S. 19); Waren nur mit Karren.",
                       "Die Einheiten bleiben danach vor Ort."],
            "vorschlag": ["Erkennung 'fremd' ueber das Feld 'fremd' am Ziel (siehe offene_luecken)."],
        },
        "transportieren": {
            "text": "Waren mit Karren zu einem Ziel bringen.",
            "belegt": ["Nur Handkarren (40), Einspaenner (100), Zweispaenner (250) - Ladung aus "
                       "den Einheitentabellen.", "Die Rueckkehr ist vorgesehen."],
            "vorschlag": ["Die Handlung am Ziel dauert 0 s (AKTION_DAUER_SEKUNDEN)."],
        },
        "handeln": {
            "text": "Waren mit einer Handelskarawane anbieten.",
            "belegt": ["Nur Handelskarawanen.", "Bei Ablehnung kehrt die Karawane MIT den Waren "
                       "zurueck, Gold wird nie uebertragen (S. 20)."],
            "vorschlag": ["Kein Goldpreis erfunden: ohne Feld 'gold_bietet' am Ziel gibt es 0 Gold."],
        },
        "angreifen": {
            "text": "Eine fremde Siedlung angreifen.",
            "belegt": ["Wall-Vorrunde, dann Kampfsequenzen (S. 21-22).",
                       "Beute NUR mit Transportkarren (S. 23, woertlich: 'Transportkarren in "
                       "seiner Angriffstruppe mitfuehrt, beginnen diese die Siedlung zu pluendern').",
                       DROSSELUNG_ZITAT],
            "vorschlag": [f"Beute {BEUTE_ANTEIL_PROZENT} % der Lager, gedeckelt durch die "
                          "Karrenladung (Entwurf, noch zu entscheiden)."],
        },
    }


def neue_liste() -> List[Dict[str, Any]]:
    """Eine leere Auftragsliste (Liste von Auftraegen)."""
    return []


# ---------------------------------------------------------------------------- starten

def _pruefe_fracht(fracht: Any, ladung: int) -> Tuple[bool, str, Dict[str, int]]:
    if fracht is None:
        return True, "", {}
    if not isinstance(fracht, dict):
        return False, "Die Fracht muss ein Verzeichnis {Ware: Menge} sein.", {}
    sauber: Dict[str, int] = {}
    for ware, menge in fracht.items():
        m = _als_int(menge, -1)
        if m < 0:
            return False, f"Die Frachtmenge fuer '{ware}' darf nicht negativ sein.", {}
        if m > 0:
            sauber[str(ware)] = m
    gesamt = sum(sauber.values())
    if gesamt > ladung:
        return (False,
                f"Ueberladen: {gesamt} Einheiten Fracht passen nicht auf {ladung} Ladeplaetze.",
                {})
    return True, "", sauber


# VORSCHLAG (Paket A2, 31.10.2026, Abschnitt "Kostentabelle"): Die Quellen nennen nur die
# RICHTUNG der Reisekosten, KEINE Zahlen - Handbuch 2009, Seite 20: "Ein Auftrag ... kostet,
# je nach Einheiten, verschiedene Mengen an Gold und Nahrung"; Drosselung: "desto weniger Gold
# ... Allerdings steigt dabei der Bedarf an Nahrung"; fremdes Ziel: Mana nach Entfernung
# (Vorversion 2006, Portal). Die drei Saetze hier sind der Vorschlag aus A2 - ausdruecklich
# KEINE Originalregel, im Spieltest zu balancieren (A2 nennt sie selbst "reine Balance-Annahme").
GOLD_JE_FELD_JE_GS = 0.1        # Gold je Einheit, Feld und GS-Punkt
NAHRUNG_JE_FELD_DURCH_GS = 0.1  # Nahrung je Einheit und Feld, geteilt durch GS
MANA_GRUND = 5.0                # Mana je Portalaktivierung, unabhaengig von der Truppenzahl
MANA_JE_FELD = 0.5              # Mana je Feld Entfernung
MANA_JE_DIMENSION = 20.0        # Mana je Dimensionsstufe (Z-Differenz)


def kosten_der_mission(einheiten: Any, entfernung: Any, geschwindigkeit: Any,
                       drosselung_prozent: Any = 0,
                       dimensionen_unterschied: Any = 0,
                       fremdes_ziel: bool = True) -> Dict[str, float]:
    """Reisekosten einer Strecke in Gold, Nahrung und Mana (alle Saetze VORSCHLAG, s. o.).

    Richtung belegt, Hoehe VORSCHLAG:
      * Gold faellt mit der Drosselung (langsamer = billiger),
      * Nahrung steigt mit der Drosselung,
      * Mana kostet nur ein FREMDES Ziel (Portal oeffnen); zwischen eigenen Siedlungen 0.
    """
    entf = max(0.0, _als_zahl(entfernung))
    gs = _als_zahl(geschwindigkeit)
    if gs <= 0.0 or entf <= 0.0:
        return {"gold": 0.0, "nahrung": 0.0, "mana": 0.0}
    drosselung = min(90.0, max(0.0, _als_zahl(drosselung_prozent)))
    tempo = 1.0 - drosselung / 100.0
    anzahl = sum(max(0, _als_int(n)) for n in (einheiten or {}).values())
    gold = GOLD_JE_FELD_JE_GS * entf * gs * tempo * max(1, anzahl)
    nahrung = NAHRUNG_JE_FELD_DURCH_GS * entf / gs / tempo * max(1, anzahl)
    mana = 0.0
    if fremdes_ziel:
        z = max(0, _als_int(dimensionen_unterschied))
        mana = MANA_GRUND + MANA_JE_FELD * entf + MANA_JE_DIMENSION * z
    return {"gold": round(gold, 2), "nahrung": round(nahrung, 2), "mana": round(mana, 2)}


def starten(liste: Optional[List[Dict[str, Any]]], art: str, einheiten: Any,
            von: Any, nach: Any, entfernung: Any, jetzt: Any,
            fracht: Any = None, drosselung_prozent: Any = 0,
            dimensionen_unterschied: Any = 0) -> Tuple[bool, str]:
    """Startet einen Auftrag und haengt ihn an `liste`. Liefert (ok, Meldung).

    `nach` ist der Zielname ODER ein Verzeichnis mit Zusatzangaben:
      {'name': str, 'fremd': bool,            # fuer stationieren
       'wall_stufe': int, 'wall_zustand_prozent': float,   # fuer angreifen
       'vorraete': {...},                      # fuer angreifen (Beute)
       'handel_akzeptiert': bool, 'gold_bietet': int}      # fuer handeln
    """
    if not isinstance(liste, list):
        return False, "Keine gueltige Auftragsliste uebergeben."
    if art not in AUFTRAGSARTEN:
        return False, f"Unbekannte Auftragsart '{art}'. Erlaubt: {', '.join(AUFTRAGSARTEN)}."

    ziel_name = _ziel_name(nach)
    start_name = str(von or "")
    if not start_name or not ziel_name:
        return False, "Start und Ziel muessen benannt sein."
    if start_name == ziel_name:
        return False, "Start und Ziel sind dieselbe Siedlung."

    entf = _als_zahl(entfernung)
    if entf <= 0.0:
        return False, "Die Entfernung muss groesser als 0 sein."

    bestand = _bestand(einheiten)
    if not bestand:
        return False, "Der Auftrag braucht mindestens eine Einheit mit Anzahl > 0."
    fremde = _unbekannte(bestand)
    if fremde:
        return False, "Unbekannte Einheit(en): " + ", ".join(fremde) + "."

    gs = _geschwindigkeit(bestand)
    if gs <= 0:
        return False, "Keine mitgefuehrte Einheit hat eine Geschwindigkeit."

    ziel = _ziel_daten(nach)
    ladung = ladung_der_mission(bestand)

    # -------------------------------------------------------------- art-spezifische Regeln
    zusatz: Dict[str, Any] = {}
    warnungen: List[str] = []    # Hinweise, die den Auftrag NICHT verhindern (z. B. Wallpruefung)
    if art == "stationieren":
        if ziel.get("fremd"):
            return False, ("Stationieren ist in fremden Siedlungen nicht moeglich "
                           "(Handbuch S. 19).")
    elif art == "transportieren":
        if not any(E.ist_transport(n) for n in bestand):
            return False, "Transportieren braucht mindestens einen Karren."
    elif art == "handeln":
        karawanen = [n for n in bestand if "Handelskarawane" in n]
        if not karawanen:
            return False, "Handeln ist nur mit Handelskarawanen moeglich."
    elif art == "angreifen":
        fuss = _schlagkraft_fussttruppen(bestand)
        bel = _schlagkraft_belagerung(bestand)
        if fuss + bel <= 0:
            return False, ("Ohne Schlagkraft kann die Vorrunde gegen den Wall nicht "
                           "bestanden werden - der Angriff wird abgelehnt.")
        if ziel.get("wall_stufe") is not None:
            vr = KB.vorrunde(fuss, bel, _als_int(ziel.get("wall_stufe")),
                             _als_zahl(ziel.get("wall_zustand_prozent"), 100.0))
            zusatz["vorrunde"] = vr
            if not vr.get("bestanden"):
                # ENTSCHEIDUNG Daniel 31.10.2026 (Frage 8): Die Wallpruefung gehoert zum KAMPF
                # (Handbuch S. 21: "Bevor ein Kampf stattfindet ..."), nicht zur Auftragserteilung.
                # Frueher wurde der Auftrag hier abgelehnt - dadurch entschied der Wallstand beim
                # Absenden, obwohl er sich bis zur Ankunft aendern kann. Jetzt startet der Auftrag
                # mit einer Warnung; entschieden wird bei Ankunft (`kampf.fuehre_schlacht` prueft
                # dieselbe Schlagkraft-Schwelle).
                warnungen.append(
                    "WARNUNG: die Schlagkraft reicht am Ziel vermutlich nicht - "
                    + str(vr.get("grund") or "die Vorrunde wuerde nicht bestanden.")
                    + " Der Auftrag startet trotzdem; entschieden wird bei Ankunft.")
            if isinstance(ziel.get("vorraete"), dict):
                # VORGABE Daniel 31.10.2026 (Registerpunkt 45): gestaffelte Beute nach Wallzustand
                # und Verteidigern, statt pauschalem Anteil. Werte sind VORSCHLAG.
                zusatz["beute"] = KB.beute_staffel(
                    bestand, ziel["vorraete"],
                    wall_zustand_vor=ziel.get("wall_zustand_prozent"),
                    verteidiger_uebrig=ziel.get("verteidiger_uebrig"))
                zusatz["beute_lage"] = KB.beute_lage(
                    ziel.get("wall_zustand_prozent"), ziel.get("verteidiger_uebrig"))

    ok_fracht, meld_fracht, saubere_fracht = _pruefe_fracht(fracht, ladung)
    if not ok_fracht:
        return False, meld_fracht

    reisezeit = reisezeit_sekunden(entf, gs)
    start = _als_zahl(jetzt)
    ankunft = start + reisezeit
    abreise = ankunft + AKTION_DAUER_SEKUNDEN
    rueckkehr = abreise + reisezeit * (HIN_UND_RUECK_FAKTOR - 1.0)

    # Reisekosten (Paket A2): ein ANGRIFF geht immer gegen eine fremde Welt (Portal), sonst
    # entscheidet das Feld 'fremd' am Ziel. Zwischen eigenen Siedlungen kostet das Portal nichts.
    fremdes_ziel = bool(ziel.get("fremd")) or art == "angreifen"
    kosten = kosten_der_mission(bestand, entf, gs, drosselung_prozent,
                                dimensionen_unterschied, fremdes_ziel=fremdes_ziel)

    eintrag: Dict[str, Any] = {
        "art": art,
        "einheiten": dict(sorted(bestand.items())),
        "von": start_name,
        "nach": ziel_name,
        "ziel": ziel,
        "fremd": bool(ziel.get("fremd")),
        "entfernung": entf,
        "geschwindigkeit": gs,
        "reisezeit": reisezeit,
        "start": start,
        "ankunft": ankunft,
        "aktion_dauer": AKTION_DAUER_SEKUNDEN,
        "rueckkehr": rueckkehr,
        "fracht": saubere_fracht,
        "ladung": ladung,
        "kosten": dict(kosten),           # VORSCHLAG-Saetze aus A2, siehe kosten_der_mission
        "beute": dict(zusatz.get("beute") or {}),
        "warnungen": list(warnungen),
        "vorrunde": zusatz.get("vorrunde"),
        "rueckgut": {},
        "gold_verdient": 0,
        "status": "hinreise",
        "abgeliefert": False,
        "angewendet": False,
    }

    if art == "handeln" and ziel.get("handel_akzeptiert") is False:
        eintrag["rueckgut"] = dict(saubere_fracht)          # Ablehnung: Waren kehren zurueck
    elif art == "handeln" and ziel.get("handel_akzeptiert") is True:
        eintrag["gold_verdient"] = max(0, _als_int(ziel.get("gold_bietet"), 0))
        eintrag["fracht"] = {}                              # verkauft: Waren bleiben am Ziel

    liste.append(eintrag)
    meldung = (f"Auftrag '{art}' von {start_name} nach {ziel_name} gestartet "
               f"(Reisezeit {reisezeit / 3600.0:.2f} h je Strecke, "
               f"Rueckkehr nach {rueckkehr / 3600.0:.2f} h).")
    if warnungen:
        meldung += " " + " ".join(warnungen)
    return True, meldung


# ------------------------------------------------------------------------ fortschritt

def _status_zeiten(eintrag: Dict[str, Any]) -> Tuple[float, float, float]:
    start = _als_zahl(eintrag.get("start"))
    rez = _als_zahl(eintrag.get("reisezeit"))
    akt = _als_zahl(eintrag.get("aktion_dauer"))
    ankunft = start + rez
    abreise = ankunft + akt
    rueck = abreise + rez * (HIN_UND_RUECK_FAKTOR - 1.0)
    return ankunft, abreise, rueck


def _status(eintrag: Dict[str, Any], jetzt: float) -> Tuple[str, float]:
    ankunft, abreise, rueck = _status_zeiten(eintrag)
    if jetzt < ankunft:
        return "hinreise", ankunft - jetzt
    if jetzt <= abreise:
        return "am_ziel", abreise - jetzt
    if jetzt < rueck:
        return "rueckreise", rueck - jetzt
    return "abgeschlossen", 0.0


def fortschritt(liste: Any, jetzt: Any) -> Dict[str, Any]:
    """Wo steht jeder Auftrag zur Zeit `jetzt`? Setzt zugleich den Merker `status`."""
    t = _als_zahl(jetzt)
    ergebnis: Dict[str, Any] = {
        "zeit": t, "gesamt": 0,
        "hinreise": [], "am_ziel": [], "rueckreise": [], "abgeschlossen": [],
        "je": [],
    }
    if not isinstance(liste, list):
        return ergebnis

    for e in liste:
        if not isinstance(e, dict):
            continue
        st, rest = _status(e, t)
        e["status"] = st
        if st == "abgeschlossen":
            e["abgeschlossen"] = True
        info = {
            "art": e.get("art"),
            "von": e.get("von"),
            "nach": e.get("nach"),
            "status": st,
            "rest_sekunden": round(max(0.0, rest), 3),
        }
        ergebnis["je"].append(info)
        ergebnis[st].append(info)
    ergebnis["gesamt"] = len(ergebnis["je"])
    return ergebnis


def angekommen(liste: Any, jetzt: Any) -> List[Dict[str, Any]]:
    """Auftraege, die ihr Ziel erreicht haben und noch nicht abgeliefert sind.

    Jeder Auftrag erscheint GENAU EINMAL: beim ersten Aufruf wird das Merkmal
    `abgeliefert` gesetzt. So wird die Fracht auch bei wiederholtem Aufruf nur einmal
    abgegeben (Handbuch S. 20: die Handlung geschieht am Ziel).
    """
    t = _als_zahl(jetzt)
    out: List[Dict[str, Any]] = []
    if not isinstance(liste, list):
        return out
    for e in liste:
        if not isinstance(e, dict):
            continue
        ankunft, _abreise, _rueck = _status_zeiten(e)
        if t >= ankunft and not e.get("abgeliefert"):
            e["abgeliefert"] = True
            out.append(e)
    return out


# ----------------------------------------------------------------------------- Bericht

def _aufzaehlung(werte: Any) -> str:
    if not isinstance(werte, dict) or not werte:
        return "keine"
    return ", ".join(f"{k} {int(_als_zahl(v))}" for k, v in sorted(werte.items()))


def bericht(eintrag: Any) -> Dict[str, Any]:
    """Der Auftragsbericht fuer den Reiter 'Nachrichten' (typ 'auftrag')."""
    e = eintrag if isinstance(eintrag, dict) else {}
    art = str(e.get("art") or "unbekannt")
    titel = f"Auftragsbericht: {art.capitalize()} {e.get('von')} -> {e.get('nach')}"
    zeilen: List[str] = [
        f"Auftragsart: {art}.",
        f"Von {e.get('von')} nach {e.get('nach')}, Entfernung "
        f"{_als_zahl(e.get('entfernung')):.0f}.",
        f"Einheiten: {_aufzaehlung(e.get('einheiten'))}.",
        f"Reisezeit je Strecke: {_als_zahl(e.get('reisezeit')) / 3600.0:.2f} h "
        f"(Rueckkehr doppelt so lang, Handbuch S. 19).",
    ]
    if e.get("ladung"):
        zeilen.append(f"Ladeplaetze: {int(_als_zahl(e.get('ladung')))}.")
    if e.get("fracht"):
        zeilen.append("Fracht: " + _aufzaehlung(e.get("fracht")) + ".")
    if e.get("beute"):
        zeilen.append("Beute: " + _aufzaehlung(e.get("beute")) + ".")
    if e.get("rueckgut"):
        zeilen.append("Zurueckgebracht: " + _aufzaehlung(e.get("rueckgut")) + ".")
    if e.get("vorrunde") and not e["vorrunde"].get("bestanden", True):
        zeilen.append("Vorrunde: " + str(e["vorrunde"].get("grund")))
    zeilen.append(f"Status: {e.get('status')}, abgeschlossen: "
                  f"{'ja' if e.get('abgeschlossen') else 'nein'}.")
    return {"titel": titel, "zeilen": zeilen, "typ": "auftrag"}


# ------------------------------------------------------------------ Spieldaten anwenden

def spieldaten_anwenden(zustand_vorher: Any, fertig: Any) -> Dict[str, Any]:
    """Wendet einen zurueckgekehrten Auftrag auf den Spielstand an (neuer Stand).

    Eingaben: {'ressourcen': {...}, 'einheiten': {...}, ...}. Der Eingabestand wird NICHT
    veraendert (tiefe Kopie). Wirkungen:
      * Beute kommt zu `ressourcen`,
      * zurueckgebrachte Waren (`rueckgut`) kommen zu `ressourcen`,
      * verdientes Gold (`gold_verdient`) kommt zum Gold,
      * ein stationierender Auftrag bleibt am Ziel: seine Einheiten gehen von `einheiten` ab,
      * kein Wert wird je negativ (Abzug mit max(0, ...)).

    Genau einmal: hat der Auftrag den Merker `angewendet`, liefert die Funktion nur eine
    Kopie des Standes zurueck. So zaehlt dieselbe Fracht nicht zweimal.
    """
    neu = copy.deepcopy(zustand_vorher) if zustand_vorher is not None else {}
    if not isinstance(neu, dict):
        neu = {}
    if not isinstance(neu.get("ressourcen"), dict):
        neu["ressourcen"] = {}
    if not isinstance(neu.get("einheiten"), dict):
        neu["einheiten"] = {}

    e = fertig if isinstance(fertig, dict) else {}
    if e.get("angewendet"):
        return neu
    # Oekonomie-Paket, Entwurf Z. 505 (hart erzwungen statt nur kommentiert): Ein EIGENTRANSPORT
    # wird ausschliesslich von `spieloekonomie.transport_fortschritt` gebucht. Diese Funktion darf
    # ihn NIE anwenden — sonst waere dieselbe Fracht zweimal gebucht. `angewendet` wird dabei
    # absichtlich NICHT gesetzt, damit `transport_fortschritt` weiterarbeiten kann.
    # Dasselbe gilt fuer einen FREMDVERTRAG (Oekonomie-Paket, Schritt 8b): er gehoert
    # `spieloekonomie.handel_abschluss` allein.
    if e.get("eigentransport") or e.get("fremdvertrag"):
        return neu

    for feld in ("beute", "rueckgut"):
        for stoff, menge in (e.get(feld) or {}).items():
            alt = _als_zahl(neu["ressourcen"].get(stoff, 0))
            neu["ressourcen"][stoff] = alt + max(0.0, _als_zahl(menge))

    gold = max(0, _als_int(e.get("gold_verdient"), 0))
    if gold:
        neu["ressourcen"]["gold"] = _als_zahl(neu["ressourcen"].get("gold", 0)) + gold

    if e.get("art") == "stationieren":
        for name, anzahl in (e.get("einheiten") or {}).items():
            alt = _als_int(neu["einheiten"].get(name, 0))
            neu["einheiten"][name] = max(0, alt - max(0, _als_int(anzahl)))

    e["angewendet"] = True
    return neu


# ------------------------------------------------------------------------ offene Luecken

def offene_luecken() -> Dict[str, str]:
    """Jeder eigene Wert mit Grund - was das Handbuch nicht hergibt, wird nicht erfunden."""
    return {
        "reisezeit_formel":
            f"Die Formel aus Entfernung und Geschwindigkeit ist VORSCHLAG "
            f"(SEKUNDEN_JE_FELD = {int(SEKUNDEN_JE_FELD)} s je Feld bei Geschwindigkeit 1). "
            "Das Handbuch (S. 19) nennt nur Beispielstunden, keine Formel.",
        "drosselung":
            f"BELEGT ist die Drosselung in {DROSSELUNG_SCHRITTE_PROZENT}-%-Schritten "
            "(Handbuch S. 20); wie sie die Reisezeit aendert, sagt das Handbuch nicht. "
            "Sie ist hier als Konstante DROSSELUNG_SCHRITTE_PROZENT abgelegt, aber nicht "
            "auf die Formel angewandt.",
        "aktion_dauer":
            f"Die Dauer der Handlung am Ziel ist VORSCHLAG "
            f"(AKTION_DAUER_SEKUNDEN = {AKTION_DAUER_SEKUNDEN:.0f}). Fuer stationieren/"
            "transportieren/angreifen nennt das Handbuch keine Aufenthaltsdauer; handeln "
            "wartet laut Entwurf auf eine Bestaetigung ohne bezifferte Dauer.",
        "beute_anteil":
            f"Der Beute-Anteil ist VORSCHLAG (BEUTE_ANTEIL_PROZENT = {BEUTE_ANTEIL_PROZENT}). "
            "Der Entwurf selbst nennt ihn ausdruecklich offen ('Was Daniel entscheiden "
            "muss', Punkt 3); das Handbuch beziffert die Beutemenge nicht.",
        "geschwindigkeit_wahl":
            "VORSCHLAG: das Tempo des Auftrags ist die langsamste mitgefuehrte Einheit "
            "(min GS). Das Handbuch nennt keine Regel fuer gemischte Gruppen.",
        "fusstruppen_begriff":
            "VORSCHLAG: als Angreifer-Fussttruppen zaehlen Kampf- UND Kundschaftereinheiten "
            "(einheiten.ist_kaempfer). Der Begriff ist im Handbuch nicht definiert.",
        "stationieren_fremd":
            "BELEGT ist das Verbot in fremden Siedlungen (S. 19). WIE ein Ziel als fremd "
            "erkannt wird, sagt das Handbuch nicht; hier entscheidet das Feld 'fremd' am "
            "Ziel. Ein reiner Zielname gilt als eigene Siedlung.",
        "kosten":
            "VORSCHLAG (Paket A2 vom 31.10.2026): Das Handbuch nennt die RICHTUNG der "
            "Reisekosten, aber keine Zahlen ('Gold und Nahrung je nach Einheiten', "
            "Drosselung: weniger Gold und mehr Nahrung, fremdes Ziel: Mana nach Entfernung). "
            "Die drei Saetze in kosten_der_mission (0,1 Gold je Feld und GS-Punkt; "
            "0,1 Nahrung je Feld durch GS; Mana 5 + 0,5 je Feld + 20 je Dimension) sind "
            "ausdruecklich VORSCHLAG und im Spieltest zu balancieren.",
        "handel_gold":
            "Beim Handeln ist kein Goldpreis erfunden. Ohne Feld 'gold_bietet' am Ziel "
            "gibt es 0 Gold; eine Ablehnung bringt die Waren zurueck (S. 20).",
        "beute_ohne_karren":
            "BELEGT (S. 23): Beute gibt es nur mit Transportkarren. Ohne Karren bleibt die "
            "Beute leer, auch wenn Vorraete uebergeben werden.",
    }

```

### Datei `src/spieloekonomie.py` (1072 Zeilen)

```python
"""Nebelseetal Remake — deterministischer Kern der Spielökonomie (Ökonomie-Paket, Schritt 2).

Quelle: `archiv/analysen/audits/entwurf_spieloekonomie_sol_2026-10-05.txt` (Abschnitt F, Schritt 2,
Codeblock Z. 237-414). Reine Rechenlogik **ohne** Oberfläche und **ohne** main-Abhängigkeit:
Karten aus festen Kontingenten, Kartenqualität (drei Achsen), Schattenpreise und die
Gründungs-Transaktion.

Bewusste Grenzen dieses Schritts (stehen so im Entwurf):
  * Der historische 8x7-Generator ist stillgelegt und separat archiviert.
    Spielkarten stammen nur aus `data/originalkarten/katalog.json`.
  * Nichts ruft dieses Modul auf. Der Ökonomiemodus wird erst nach dem letzten
    Integrationsschritt aktiviert; bis dahin läuft der Altmodus unverändert.
  * Alle Schwellen, Gewichte und Gebühren sind **VORSCHLAG** (siehe `data/spieloekonomie.json`).

Die Kontingente sind exakte Feldzahlen: `feste_karte` prüft selbst, dass sie zum Kartenmaß
passen, das Sumpfkontingent einhalten und den Mindestbesatz erfüllen — ein falscher Eintrag
fällt sofort auf, statt eine unspielbare Karte zu erzeugen.
"""
from __future__ import annotations

import copy
import hashlib
import json
import math
import random
from pathlib import Path

import auftraege
import ausruestung
import einheiten  # noqa: F401  (vom Entwurf vorgesehen; hier für spätere Schritte)
import forschung
import forschungspfad
import gebaeude_wirkung
import gelaende
import originalkarten  # GPT-OK01: neue Spielstaende verwenden Originalkarten, 10x10
import spieldaten
import werkstatt
import wirtschaft

DATEN = Path(spieldaten.projektwurzel()) / "data"


def lade(name: str) -> dict:
    return json.loads((DATEN / name).read_text(encoding="utf-8"))


REGELN = lade("spieloekonomie.json")

# BELEGT ist nur die RICHTUNG ("Je hoeher die Stufe, desto schneller"); die Zahlen fehlen in
# beiden Originalfassungen. Dieser Schalter schaltet die Stufenwirkung ab, ohne Code zu loeschen -
# er ist die eine Stelle, an der man zurueck auf "feste Dauer" kann. Siehe
# docs/audits/AUSBILDUNGSDAUER_BELEGT_20261031.md und docs/PRUEFREGEL_ORIGINAL.md (Register 53).
AUSBILDUNG_STUFENFAKTOR_AKTIV = True
G = lade("gelaende.json")
BP = lade("baupreise.json")["preise"]
U = lade("units.json")["einheiten"]
# Die freigegebenen Warenrezepte (Oekonomie-Paket, Schritt 4). Zur Laufzeit wird AUSSCHLIESSLICH
# diese eingefrorene Datei gelesen - nicht neu abgeleitet (Entwurf Z. 588). Erzeugt von
# `tools/warenrezepte_ableiten.py`.
WARENREZEPTE = lade("warenrezepte.json")


def mengen(kosten) -> dict:
    """Nur die echten Mengen eines Kosten-Eintrags (Kennzeichnungen wie ``_belegt`` fallen weg)."""
    return {k: float(v) for k, v in kosten.items()
            if isinstance(v, (int, float)) and not isinstance(v, bool)}


def gruendungskosten():
    """(Gebühr, Startpaket, Mindestbestand) aus den Regeldaten und den echten Preisen."""
    r = REGELN["gruendung"]
    haus = mengen(BP["haus"])
    preis = {k: v * r["hausmultiplikator"] for k, v in haus.items()}
    paket = {k: v * r["reserve_hausmultiplikator"] for k, v in haus.items()}
    preis["nahrung"] = U[r["karren"]]["kosten"]["nahrung"] * r["nahrung_karrenanteil"]
    paket["nahrung"] = U[r["reserve_nahrung_einheit"]]["kosten"]["nahrung"]
    minimum = {k: preis.get(k, 0) + paket.get(k, 0) for k in preis.keys() | paket.keys()}
    return preis, paket, minimum


def feste_karte(seed, eintrag: dict) -> dict:
    """Stillgelegter historischer 8x7-Generator (keine neuen Karten mehr)."""
    raise ValueError("Historische 8x7-Karten sind archiviert; originalkarten.karte(ID) verwenden")


def vorrat(seed) -> dict:
    """Der feste Kartenvorrat für Neugründungen (Koloniekarten, noch ohne Besitzer)."""
    return originalkarten.vorrat(seed)


def startkarte(seed, eigentuemer) -> dict:
    """Die private, ausgeglichene Startkarte eines Akteurs (nicht Teil des Vorrats)."""
    return originalkarten.startkarte(seed, eigentuemer)


def kapazitaeten(karte) -> dict:
    """Theoretische Stundenerträge einer Karte, Kennungen in Kleinschreibung."""
    return {k.lower(): float(v) for k, v in wirtschaft.kapazitaet({"karte": karte}).items()}


def achsen(karte) -> tuple:
    """Die drei Vergleichsachsen (Holz, Gestein, Agrar) — je die unabhängige Obergrenze."""
    n = karte["zaehlung"]
    return (n["wald"] * gelaende.ertrag_pro_stunde("holzfaeller", "wald")
            + n["steppe"] * gelaende.ertrag_pro_stunde("holzfaeller", "steppe"),
            n["berg"] * gelaende.ertrag_pro_stunde("steinmetz", "berg")
            + n["huegel"] * gelaende.ertrag_pro_stunde("steinmetz", "huegel"),
            n["grasland"] * gelaende.ertrag_pro_stunde("farm", "grasland")
            + n["steppe"] * gelaende.ertrag_pro_stunde("farm", "steppe"))


def relativ(karte) -> tuple:
    """Die drei Achsen einer Karte im Verhältnis zur Startreferenz."""
    basis = achsen(originalkarten.startkarte("referenz", "spieler"))
    return tuple(a / b for a, b in zip(achsen(karte), basis))


def _ist_originalkarten_verbund(karten: list) -> bool:
    """Nur neue, eindeutig markierte 10x10-Originalkarten; nie Legacy still umdeuten."""
    return bool(karten) and all(
        isinstance(k, dict) and k.get("originalkarte_id")
        and k.get("spalten") == 10 and k.get("zeilen") == 10
        and len(k.get("raster") or []) == 100 for k in karten)


def kartenqualitaet(karten: list) -> dict:
    """Prueft die Siedlungsgrundlage des Versorgungsziels.

    GPT-KZ01 (28.10.2026): Bei neuen Originalkarten muss man nicht die
    historischen Qualitaetsgruppen bzw. die zufaellig gezogene Zusammensetzung
    ueberlisten. Ab vier Siedlungen ist die Karten-Grundbedingung erfuellt;
    Leistung und Spezialisierung beweist erst die TATSAECHLICHE Wirtschaft in
    ``zielstatus`` (Produktion, Reserve, Transport, Forschung, Waren, Heer).
    Die drei Landschaftsachsen bleiben als Diagnose abrufbar. Fuer alte 8x7-
    Testkarten bleibt die zuvor beschlossene Portfolioregel unangetastet.
    """
    if not karten:
        return {"erfuellt": False, "mittel": (0, 0, 0), "beste": (0, 0, 0),
                "modell": "keine_karten", "siedlungen": 0}
    werte = [relativ(k) for k in karten]
    mittel = tuple(sum(w[i] for w in werte) / len(werte) for i in range(3))
    beste = tuple(max(w[i] for w in werte) for i in range(3))
    genug_orte = len(karten) >= REGELN["mindestsiedlungen"]
    if _ist_originalkarten_verbund(karten):
        # Achtung: keine Kategorie und kein theoretischer Gold-/Lederwert hier!
        # Der 24h-Produktionsplan und echte Waren-/Transportketten entscheiden.
        return {"erfuellt": genug_orte, "mittel": mittel, "beste": beste,
                "modell": "original_10x10_versorgung", "siedlungen": len(karten)}
    ok = (genug_orte and min(mittel) >= REGELN["portfoliofaktor"]
          and min(beste) >= REGELN["spezialistenfaktor"])
    return {"erfuellt": ok, "mittel": mittel, "beste": beste,
            "modell": "alt_8x7_portfolio", "siedlungen": len(karten)}


def kartennutzen(karten: list, kandidat) -> float:
    """Reproduzierbare Empfehlung nach ECHTEN Geländeerträgen (nie Katalog-Güte).

    Bei neuen Originalkarten steigt der Nutzen einer Rohstoffachse, wenn sie
    in den bisherigen Siedlungen unterversorgt ist. Hohe Potentiale bleiben
    gut, aber eine zweite Spezialkarte in derselben Achse ist weniger wertvoll
    als die erste. Keine versteckte Gewichtung der Gruppen beste/mittlere/
    schlechte. Bei Alt-Karten bleibt der frühere Entwurfsnutzen bestehen.
    """
    vorher = [relativ(k) for k in karten]
    neu = relativ(kandidat)
    if _ist_originalkarten_verbund([*karten, kandidat]):
        # Die Kopplung an die bestehende Summe verhindert künstliche
        # Spezialistenhürden bei historischen Karten. Auch für die erste Karte
        # definiert: Nenner 1.0 (keine Division durch 0).
        sums = [sum(w[i] for w in vorher) for i in range(3)]
        return sum(neu[i] / (1.0 + sums[i]) for i in range(3))
    if not vorher:
        return sum(neu)
    bedarf = [max(0, REGELN["portfoliofaktor"] * len(vorher) - sum(w[i] for w in vorher))
              + max(0, REGELN["spezialistenfaktor"] - max(w[i] for w in vorher))
              for i in range(3)]
    return sum(neu[i] * (1 + bedarf[i]) for i in range(3))


def _begrenzen(wert, grenzen):
    return min(grenzen[1], max(grenzen[0], wert))


def einzelmaximum() -> dict:
    """Bester Einzelfeldertrag je Rohstoff über alle baubaren Geländearten."""
    beste = {}
    for art in gelaende.GELAENDEARTEN:
        if not gelaende.ist_bebaubar(art):
            continue
        for kennung, geb in gelaende.alle_gebaeude().items():
            e = gelaende.ertrag_pro_stunde(kennung, art)
            if isinstance(e, (int, float)):
                e = {geb["rohstoff"]: e}
            for r, v in (e or {}).items():
                beste[r.lower()] = max(beste.get(r.lower(), 0), float(v))
    return beste


def schattenpreis(karte, rohstoff: str, bestand: float, reserve: float) -> float:
    """Lokaler Schattenpreis eines Rohstoffs in Gold (Gold selbst ist immer 1)."""
    if rohstoff == "gold":
        return 1.0
    beste = einzelmaximum()
    lokal = kapazitaeten(karte).get(rohstoff, 0)
    start = kapazitaeten(originalkarten.startkarte("preis", "spieler"))[rohstoff]
    ratio = start / lokal if lokal > 0 else math.inf
    k = _begrenzen(ratio, REGELN["kartenpreisgrenzen"])
    v = 1.0 if reserve <= 0 else _begrenzen(2 * reserve / (reserve + bestand), REGELN["vorratspreisgrenzen"])
    return beste["gold"] / beste[rohstoff] * k * v


def bezahlbar(bestand: dict, kosten: dict) -> bool:
    return all(math.isfinite(v) and v >= 0 and bestand.get(r, 0) >= v
               for r, v in kosten.items())


def buchen(bestand: dict, delta: dict) -> dict:
    """Bucht ein Delta auf einen Bestand; negative Bestände sind ein Fehler, keine Rundung."""
    neu = dict(bestand)
    for r, v in delta.items():
        if not math.isfinite(v):
            raise ValueError("Nicht endliche Buchung.")
        neu[r] = neu.get(r, 0) + v
        if neu[r] < -1e-9:
            raise ValueError("Nicht genügend Bestand: " + r)
        neu[r] = max(0.0, neu[r])
    return neu


def absicht(quelle: dict, karte_id: str, karten: list, freie: dict,
            forschung: dict, runde: int) -> dict:
    """Prüft eine Gründungsabsicht und liefert das Sperrgut (noch wird nichts gebucht)."""
    r = REGELN["gruendung"]
    if karte_id not in freie or freie[karte_id]["besitzer"] is not None:
        raise ValueError("Karte nicht frei.")
    if len(karten) >= quelle["siedlungsgrenze"]:
        raise ValueError("Siedlungsgrenze erreicht.")
    if forschung.get(r["forschung"], 0) < r["stufe"]:
        raise ValueError("Gründungsforschung fehlt.")
    if quelle["einheiten"].get(r["karren"], 0) < 1:
        raise ValueError("Siedlerkarren fehlt.")
    preis, paket, minimum = gruendungskosten()
    if not bezahlbar(quelle["vorraete"], minimum):
        raise ValueError("Lokaler Mindestbestand fehlt.")
    return {"quelle": quelle["id"], "besitzer": quelle["besitzer"], "karte_id": karte_id,
            "runde": runde, "sperrgut": minimum, "preis": preis, "paket": paket,
            "nutzen": kartennutzen(karten, freie[karte_id]["karte"])}


def vergabe(absichten: list, freie: dict, seed, runde: int) -> list:
    """Vergibt die Karten einer Runde: höherer Nutzen gewinnt, Gleichstand über SHA-256.

    Die Sortierung ist **unabhängig** von Listen- oder Klickreihenfolge; jede Kennung wird
    höchstens einmal vergeben, veraltete Absichten werden abgelehnt.
    """
    def rang(a):
        text = f"{seed}:{runde}:{a['karte_id']}:{a['besitzer']}"
        return (-a["nutzen"], hashlib.sha256(text.encode("utf-8")).hexdigest())

    ergebnis, akteure, vergeben = [], set(), set()
    for a in sorted(absichten, key=rang):
        if a["runde"] != runde or a["besitzer"] in akteure:
            raise ValueError("Unzulässige doppelte oder veraltete Absicht.")
        akteure.add(a["besitzer"])
        ok = (a["karte_id"] in freie and freie[a["karte_id"]]["besitzer"] is None
              and a["karte_id"] not in vergeben)
        ergebnis.append((a, ok))
        if ok:
            vergeben.add(a["karte_id"])
    return ergebnis


# ---------------------------------------------------------------------------
# Schritt 3 — lokale Lager und Transportbuchung (Entwurf Z. 417-505)
# ---------------------------------------------------------------------------
#
# Eine lokale Wirtschaft ist Voraussetzung, nicht Kür für: Vorräte, Waren, Einheiten und
# Werkstatt-/Bibliotheksauftrag — sie liegen JE SIEDLUNG. Gemeinsame Summen sind nur abgeleitete
# Anzeige; kein Auftrag darf damit bezahlen. „Beute gibt es nur mit Transportkarren" ist
# belegt (Handbuch S. 23) und wird von `auftraege.starten` für die Art „transportieren"
# bereits erzwungen („Transportieren braucht mindestens einen Karren.").
#
# WICHTIG für die spätere main-Anbindung (Entwurf Z. 505): `auftraege.spieldaten_anwenden`
# darf auf einen EIGENTRANSPORT niemals angewendet werden — eigene Transporte bucht
# ausschließlich `transport_fortschritt`.


def verbrauchen(ort: dict, kosten: dict, jetzt: float) -> dict:
    """Bucht Kosten aus dem LOKALEN Lager ab und schreibt die Importherkunft mit.

    Der Verbrauch wird anteilig aus dem importierten Bestand gedeckt — so belegt das
    Verbrauchsjournal, dass wirklich eine gelieferte Fracht genutzt wurde (Siegnachweis,
    Schritt 7). Reicht das lokale Lager nicht, ist das ein Fehler, keine stille Nullbuchung.
    """
    neu = copy.deepcopy(ort)
    if not bezahlbar(neu["vorraete"], kosten):
        # Daniel 30.10.2026: Die alte Meldung sagte nur "Lokales Lager reicht nicht." - bei
        # 1.137 Nahrung im Ort las der Spieler das als Anzeigefehler. Jetzt steht da, WELCHER
        # Rohstoff fehlt und um wieviel (Beispiel: "holz fehlt 62.80 (37.20 von 100)").
        import fehlbestand
        fehlt = fehlbestand.fehlbestand(neu["vorraete"], kosten)
        raise ValueError("Lokales Lager reicht nicht: "
                         + fehlbestand.text(fehlt, neu["vorraete"], kosten))
    for r, m in kosten.items():
        v = neu["vorraete"].get(r, 0)
        importiert = neu["importiert"].get(r, 0)
        genutzt = 0 if v <= 0 else m * importiert / v
        neu["vorraete"][r] = v - m
        neu["importiert"][r] = max(0, importiert - genutzt)
        if genutzt > 0:
            neu["verbrauchsjournal"].append({"zeit": jetzt, "rohstoff": r, "menge": genutzt,
                                             "ziel": ort["id"]})
    return neu


def transport_start(quelle: dict, ziel: dict, bestand: dict, fracht: dict, jetzt: float,
                    frachtkanal: str = "vorraete"):
    """Startet einen Transport zwischen EIGENEN Siedlungen. Liefert (neue_quelle, mission).

    ``frachtkanal`` ist ``"vorraete"`` (Rohstoffe) oder ``"waren"``. Importherkunft und
    Verbrauchsjournal gelten nur für Rohstoffe — der Siegnachweis zählt keine Waren.
    Jede Ablehnung wirft ``ValueError``; es wird nichts halb gebucht.
    """
    if frachtkanal not in ("vorraete", "waren"):
        raise ValueError("Unbekannter Frachtkanal.")
    if quelle["besitzer"] != ziel["besitzer"]:
        raise ValueError("Für eigene Transporte muss der Besitzer übereinstimmen.")
    if quelle["dimension"] != ziel["dimension"]:
        raise ValueError("Dimensionswechsel braucht eigene Portalregeln.")
    if not bestand or not all(type(n) is int and n > 0 for n in bestand.values()):
        raise ValueError("Ungültige Transporttruppe.")
    if any(quelle["einheiten"].get(n, 0) < m for n, m in bestand.items()):
        raise ValueError("Einheiten sind nicht am Ausgangsort.")
    if any(type(m) is not int or m < 0 for m in fracht.values()):
        raise ValueError("Fracht muss aus nichtnegativen ganzen Mengen bestehen.")
    if frachtkanal == "vorraete" and set(fracht) - set(quelle["vorraete"]):
        raise ValueError("Unbekannter Rohstoff; Waren brauchen ausdrücklich einen Warenauftrag.")
    if not bezahlbar(quelle[frachtkanal], fracht):
        raise ValueError("Fracht fehlt am Ausgangsort.")
    d = abs(quelle["x"] - ziel["x"]) + abs(quelle["y"] - ziel["y"])
    liste = []
    ok, meldung = auftraege.starten(liste, "transportieren", bestand, quelle["id"], ziel["id"],
                                    d, jetzt, fracht)
    if not ok:
        raise ValueError(meldung)
    neu = copy.deepcopy(quelle)
    anteil = {}
    for r, m in fracht.items():
        v = neu[frachtkanal][r]
        anteil[r] = (0 if (v <= 0 or frachtkanal != "vorraete")
                     else m * neu["importiert"].get(r, 0) / v)
        neu[frachtkanal][r] -= m
        if frachtkanal == "vorraete":
            neu["importiert"][r] = max(0, neu["importiert"].get(r, 0) - anteil[r])
    for n, m in bestand.items():
        neu["einheiten"][n] -= m
    mission = liste[0]
    mission.update({"eigentransport": True, "ziel_id": ziel["id"], "quelle_id": quelle["id"],
                    "frachtkanal": frachtkanal, "ursprung_import": anteil,
                    "geliefert_lokal": False, "heimgekehrt_lokal": False})
    mission["besitzer"] = quelle["besitzer"]
    return neu, mission


def transport_fortschritt(mission: dict, orte: dict, jetzt: float):
    """Bucht Ankunft und Rückkehr eines eigenen Transports **genau einmal**. (orte, mission).

    Bei Ankunft wird die Fracht am Ziel gutgeschrieben; bei Rückkehr kehrt sie (samt
    Importherkunft) zum Ausgangsort zurück. Ist der Ausgangsort verloren oder erobert, gilt
    er wie ein nicht mehr vorhandener: dann wird eine eigene Ersatzsiedlung gesucht, sonst
    bleibt die Fracht am Auftrag — **keine** Geistergutschrift.
    """
    neu = copy.deepcopy(orte)
    m = copy.deepcopy(mission)
    kanal = m.get("frachtkanal", "vorraete")
    ziel = neu.get(m["ziel_id"])
    if jetzt >= m["ankunft"] and not m["geliefert_lokal"]:
        if ziel is not None and ziel["besitzer"] == m["besitzer"]:
            for r, n in m["fracht"].items():
                ziel[kanal][r] = ziel[kanal].get(r, 0) + n
                if kanal == "vorraete":
                    # Nicht als lokaler Verbrauch werten: erst ein späterer echter Auftrag zählt.
                    ziel["importiert"][r] = ziel["importiert"].get(r, 0) + n
            m["fracht"] = {}
            if m.get("stationieren_lokal"):
                for n, k in m["einheiten"].items():
                    ziel["einheiten"][n] = ziel["einheiten"].get(n, 0) + k
                m["einheiten"] = {}
                m["heimgekehrt_lokal"] = True
        m["geliefert_lokal"] = True
    if jetzt >= m["rueckkehr"] and not m["heimgekehrt_lokal"]:
        quelle = neu.get(m["quelle_id"])
        if quelle is not None and quelle["besitzer"] != m["besitzer"]:
            quelle = None            # eroberter Ausgangsort zählt wie ein verlorener
        if quelle is None:
            quelle = next((o for _, o in sorted(neu.items()) if o["besitzer"] == m["besitzer"]),
                          None)
            m["ersatzort"] = quelle["id"] if quelle is not None else None
        if quelle is not None:
            for n, k in m["einheiten"].items():
                quelle["einheiten"][n] = quelle["einheiten"].get(n, 0) + k
            for r, k in m["fracht"].items():
                quelle[kanal][r] = quelle[kanal].get(r, 0) + k
                if kanal == "vorraete":
                    quelle["importiert"][r] = (quelle["importiert"].get(r, 0)
                                               + m["ursprung_import"].get(r, 0))
            m["fracht"] = {}
            m["heimgekehrt_lokal"] = True
        # KEINE eigene Siedlung vorhanden: Fracht und Einheiten BLEIBEN am Auftrag, und der
        # Merker bleibt AUS (Entwurf Z. 492/500: „Fracht bleibt am Auftrag und ist nicht global
        # verfuegbar"). So kann ein spaeter auftauchender eigener Ort die Fracht noch erhalten —
        # es wird nichts erfunden und an Fremde nichts verteilt.
        # Fund der unabhaengigen Abweichungspruefung (archiv/analysen/audits/pruefung_schritt3_4.md, Punkt 12).
    return neu, m


def station_start(quelle: dict, ziel: dict, bestand: dict, fracht: dict, jetzt: float):
    """Ein Transport, dessen Einheiten am Ziel bleiben (Stationierung). (neue_quelle, mission)."""
    q, m = transport_start(quelle, ziel, bestand, fracht, jetzt)
    m["stationieren_lokal"] = True
    return q, m


# ---------------------------------------------------------------------------
# Schritt 4 — Pilotrezepte, lokale Ausbildung und echte Verbrauchsbelege
# (Entwurf Z. 507-590)
# ---------------------------------------------------------------------------
#
# Die Rezepte stehen eingefroren in `data/warenrezepte.json` (erzeugt von
# `tools/warenrezepte_ableiten.py`); zur Laufzeit wird ausschliesslich diese Datei gelesen.
# Alle Dauerangaben ausser dem Schwert (1200 s, belegt) sind VORSCHLAG.


def ware_start(ort: dict, ware: str, forschung: dict, jetzt: float,
               rezepte: dict = None) -> dict:
    """Reiht eine Ware in die Werkstatt DIESER Siedlung ein. Liefert den neuen Ort.

    Geprueft werden (1) ein freigegebenes Rezept, (2) die Forschungsvoraussetzungen der Ware,
    (3) eine Werkstatt VOR ORT, (4) die Materialkosten im lokalen Lager. Die Dauer kommt aus
    dem Rezept in die Warteschlange — die einzige belegte Dauer (Schwert) bleibt unberuehrt.
    """
    neu = copy.deepcopy(ort)
    rezepte = WARENREZEPTE if rezepte is None else rezepte
    if ware not in rezepte:
        raise ValueError("Keine freigegebene Rezeptangabe.")
    rezept = rezepte[ware]
    if any(forschung.get(f, 0) < n for f, n in rezept["voraussetzungen"].items()):
        raise ValueError("Warenvoraussetzung fehlt.")
    typ = werkstatt.werkstatt_fuer(ware)
    if typ is None:
        raise ValueError("Ware gehoert zu keiner Werkstatt.")
    zahl = werkstatt.werkstaetten_bestand([neu])[typ]
    if zahl <= 0:
        raise ValueError("Werkstatt nicht in dieser Stadt.")
    neu = verbrauchen(neu, rezept["kosten"], jetzt)
    schlange = neu["werkstaetten"].setdefault(typ, werkstatt.neue_warteschlange(typ, zahl))
    schlange["werkstaetten"] = zahl
    schlange["kapazitaet"] = werkstatt.kapazitaet(zahl)
    werkstatt.fortschritt(schlange, jetzt)
    ok, meldung = werkstatt.einreihen(schlange, ware, 1, 1, rezepte)
    if not ok:
        raise ValueError(meldung)
    return neu


def ausbildung_uebersicht(ort: dict, jetzt: float) -> dict:
    """Was gerade in DIESEM Ort ausgebildet wird - mit Restzeiten und Gesamtdauer.

    Warum (Daniel 31.10.2026, eigener Spieltest): "die Handkarren werden unsichtbar produziert,
    es gibt keine Anzeige fuer den Ausbildungsstand ... eine Uebersicht, wie lange die
    Produktionszeit gesamt dauert". Die Auftraege liefen schon immer NACHEINANDER je Gebaeude
    (`ausbildung_start` beginnt bei `freie_zeit` = Ende des letzten Auftrags desselben Gebaeudes),
    aber niemand konnte das sehen.

    Rueckgabe::

        {"auftraege": [{"einheit", "gebaeude", "stufe", "start", "ende", "rest_sekunden",
                        "dauer_sekunden", "laufend", "platz"}],
         "gesamt_rest_sekunden": float,      # bis der LETZTE Auftrag fertig ist
         "anzahl": int}
    """
    try:
        jetzt = float(jetzt)
    except (TypeError, ValueError):
        jetzt = 0.0
    auftraege = []
    for eintrag in (ort.get("ausbildung") or []):
        if not isinstance(eintrag, dict):
            continue
        try:
            ende = float(eintrag.get("ende") or 0.0)
            start = float(eintrag.get("start") or 0.0)
        except (TypeError, ValueError):
            continue
        if eintrag.get("gebucht"):
            continue
        dauer = eintrag.get("dauer_sekunden")
        if dauer is None:
            dauer = max(0.0, ende - start)
        auftraege.append({
            "einheit": eintrag.get("einheit"),
            "gebaeude": eintrag.get("gebaeude"),
            "stufe": eintrag.get("stufe"),
            "start": start,
            "ende": ende,
            "dauer_sekunden": float(dauer),
            "rest_sekunden": max(0.0, ende - jetzt),
            "laufend": start <= jetzt < ende,
        })
    auftraege.sort(key=lambda a: (a["ende"], str(a["einheit"])))
    for platz, auftrag in enumerate(auftraege, start=1):
        auftrag["platz"] = platz
    gesamt = max([a["ende"] for a in auftraege], default=jetzt)
    return {"auftraege": auftraege,
            "gesamt_rest_sekunden": max(0.0, gesamt - jetzt),
            "anzahl": len(auftraege)}


def ausbildung_abbrechen(ort: dict, platz: int, jetzt: float) -> dict:
    """Einen Ausbildungsauftrag streichen - OHNE Erstattung, weil die Quelle nichts regelt.

    Belegt ist nur das Abbrechen von FORSCHUNG (Handbuch 2009, Z. 442: "Forschung abbrechen").
    Fuer die Einheitenausbildung nennt weder das Handbuch 2009 noch die Vorversion 2006 eine
    Regel zu Abbruch oder Erstattung - geprueft 31.10.2026. Deshalb: Streichen ja (der Spieler
    soll nicht in einer Warteschlange festsitzen), Erstattung nein (kein erfundener Betrag).
    Die verbrauchten Siedler, Kosten und Waren bleiben verbraucht.
    """
    liste = [a for a in (ort.get("ausbildung") or []) if isinstance(a, dict) and not a.get("gebucht")]
    liste.sort(key=lambda a: (float(a.get("ende") or 0.0), str(a.get("einheit"))))
    try:
        platz = int(platz)
    except (TypeError, ValueError):
        return {"ok": False, "grund": "Ungueltiger Platz."}
    if not 1 <= platz <= len(liste):
        return {"ok": False, "grund": f"Platz {platz} gibt es nicht (1-{len(liste)})."}
    ziel = liste[platz - 1]
    try:
        jetzt = float(jetzt)
    except (TypeError, ValueError):
        jetzt = 0.0
    if float(ziel.get("start") or 0.0) <= jetzt and jetzt < float(ziel.get("ende") or 0.0):
        return {"ok": False, "grund": "Dieser Auftrag laeuft gerade und kann nicht mehr gestrichen "
                                      "werden - nur wartende Auftraege."}
    neu = [a for a in (ort.get("ausbildung") or []) if a is not ziel]
    return {"ok": True, "grund": "", "einheit": ziel.get("einheit"), "ausbildung": neu,
            "erstattung": {}, "hinweis": "Keine Erstattung: die Quellen regeln das nicht."}


def ausbildung_start(ort: dict, name: str, forschung: dict, jetzt: float) -> dict:
    """Beginnt die Ausbildung EINER Einheit vor Ort. Liefert den neuen Ort.

    Geprueft werden (1) die Forschungsstufe der Einheit, (2) die Ausbildungsstaette VOR ORT
    (Kriegerakademie / Diebesgilde / Stellmacher), (3) genug freie Siedler, (4) die
    Ausruestung im lokalen Warenlager. Verbraucht werden Kosten, Siedler und Ausruestung —
    die Einheit selbst entsteht erst am Ende der Ausbildungszeit (`ort_tick`, Schritt 5).
    """
    eintrag = U.get(name)
    if eintrag is None:
        raise ValueError("Unbekannte Einheit: " + str(name))
    voraus = eintrag.get("voraussetzung") or {}
    if voraus and forschung.get(voraus.get("forschung"), 0) < voraus.get("stufe", 0):
        # Daniel 30.10.2026: "Einheitenforschung fehlt" sagt nicht, welche - beim Siedlerkarren
        # ist es Wagenbau. Die Meldung nennt jetzt Name, Soll- und Ist-Stufe.
        raise ValueError(
            f"Einheitenforschung fehlt: {voraus.get('forschung')} Stufe {voraus.get('stufe', 0)} "
            f"(erreicht: {forschung.get(voraus.get('forschung'), 0)}).")
    geb = gelaende.finde_gebaeude(str(eintrag.get("gebaeude") or ""))
    stufe = gebaeude_wirkung.gebaeude_stufe(ort, geb)
    if stufe <= 0:
        raise ValueError("Ausbildungsstätte fehlt vor Ort.")
    kosten = dict(eintrag.get("kosten") or {})
    siedler = kosten.pop("siedler", 0)
    if ort["bevoelkerung"] < siedler:
        raise ValueError("Freie Siedler fehlen vor Ort.")
    import ausruestung
    if ausruestung.fehlende(name, ort["waren"]):
        raise ValueError("Ausrüstung fehlt vor Ort.")
    neu = verbrauchen(ort, kosten, jetzt)
    neu["bevoelkerung"] -= siedler
    neu["waren"] = ausruestung.verbrauchen(neu["waren"], name)
    freie_zeit = max([jetzt] + [a["ende"] for a in neu["ausbildung"] if a["gebaeude"] == geb])
    # BELEGT (beide Fassungen, woertlich): "Je hoeher die Stufe, desto schneller werden die
    # entsprechenden Einheiten ausgebildet" — Vorversion 2006, einheiten.php Z. 15-16; Handbuch
    # 2009, Z. 503-504. Die ZAHLEN fehlen in beiden Fassungen (geprueft 31.10.2026, siehe
    # docs/audits/AUSBILDUNGSDAUER_BELEGT_20261031.md) - belegt ist also nur die RICHTUNG.
    # VORSCHLAG: Dauer = Grunddauer / Stufe (Stufe 1 = Grunddauer, Stufe 5 = ein Fuenftel).
    # Grund fuer die Division: sie erfuellt "je hoeher, desto schneller" monoton und ohne
    # zusaetzliche erfundene Konstante; balancieren im Spieltest.
    grunddauer = REGELN["pilot_ausbildung_minuten"] * 60
    dauer = grunddauer / max(1, int(stufe)) if AUSBILDUNG_STUFENFAKTOR_AKTIV else grunddauer
    # Pilotregel: die Grunddauer ist kein Originalwert (das Handbuch nennt keine Ausbildungsdauer).
    neu["ausbildung"].append({"einheit": name, "gebaeude": geb, "start": freie_zeit,
                              "ende": freie_zeit + dauer,
                              "dauer_sekunden": dauer, "stufe": int(stufe),
                              "gebucht": False})
    return neu


# ---------------------------------------------------------------------------
# Schritt 5 — gemeinsame Spieluhr: lokale Produktion und Fortschritt
# (Entwurf Z. 592-648)
# ---------------------------------------------------------------------------
#
# Der Ökonomiemodus hat EINE Uhr: `spielsekunden` (Spielzeit, nicht Rechnerzeit). Dieses Modul
# rechnet nur damit; `main._tick_loop` multipliziert genau einmal mit `spielzeit.faktor()`.
# Solange der Ökonomiemodus nicht aktiviert ist, ruft niemand diese Funktionen auf.


def ort_tick(ort: dict, ab: float, bis: float, forschung: dict) -> dict:
    """Einen Ort von Spielzeit `ab` bis `bis` fortschreiben. Liefert den neuen Ort.

    Produziert über `wirtschaft.ertrag_gesamt` (dieselbe Quelle wie die Anzeige), schreibt
    Siedlerzuwachs bis zur Grenze fort, holt fertige Werkstattwaren ins Lager und bucht
    abgeschlossene Ausbildungen **genau einmal** (`gebucht`). Jede Produktionsspanne landet im
    `produktionsjournal` — Grundlage des Versorgungsfensters (Schritt 7).
    """
    if bis < ab:
        raise ValueError("Spielzeit darf nicht zurücklaufen.")
    neu = copy.deepcopy(ort)
    ertrag = {k.lower(): v for k, v in wirtschaft.ertrag_gesamt([neu], forschung).items()}
    produktion = {}
    for r, rate in ertrag.items():
        menge = rate * (bis - ab) / 3600.0
        neu["vorraete"][r] = neu["vorraete"].get(r, 0) + menge
        produktion[r] = menge
    grenze = gebaeude_wirkung.bevoelkerungsgrenze([neu])
    zuwachs = gebaeude_wirkung.siedler_zuwachs_pro_stunde([neu], forschung) * (bis - ab) / 3600.0
    neu["bevoelkerung"] = min(grenze, neu["bevoelkerung"] + zuwachs)
    if bis > ab:
        neu["produktionsjournal"].append({"ab": ab, "bis": bis, "mengen": produktion})
    for schlange in neu["werkstaetten"].values():
        for ware, n in werkstatt.fertige_waren(schlange, bis).items():
            neu["waren"][ware] = neu["waren"].get(ware, 0) + n
            neu["fertigjournal"].append({"zeit": bis, "art": "ware", "name": ware})
    for a in neu["ausbildung"]:
        if not a["gebucht"] and a["ende"] <= bis:
            name = a["einheit"]
            neu["einheiten"][name] = neu["einheiten"].get(name, 0) + 1
            a["gebucht"] = True
            neu["fertigjournal"].append({"zeit": a["ende"], "art": "einheit", "name": name})
    return neu


def fensterproduktion(orte: list, jetzt: float) -> dict:
    """Tatsächlich produzierte Mengen im Versorgungsfenster (rückblickend bis `jetzt`).

    Zählt aus den `produktionsjournal`-Zeilen anteilig — eine Zeile, die nur halb ins Fenster
    reicht, zählt auch nur halb. So kann eine Momentaufnahme die Versorgung nicht vortäuschen.
    """
    start = jetzt - REGELN["versorgung_stunden"] * 3600
    out: dict = {}
    for ort in orte:
        for zeile in ort.get("produktionsjournal") or []:
            dauer = zeile["bis"] - zeile["ab"]
            anteil = max(0.0, min(jetzt, zeile["bis"]) - max(start, zeile["ab"]))
            if dauer > 0 and anteil > 0:
                for r, n in (zeile.get("mengen") or {}).items():
                    out[r] = out.get(r, 0) + n * anteil / dauer
    return out


def ereigniszeiten(orte: dict, missionen: list, jetzt: float) -> list:
    """Die Spielzeiten der NÄCHSTEN Ereignisse (Entwurf Z. 950-960).

    Ein **Ereignis** ist etwas, das den Zustand sprunghaft ändert: das Ende einer Ausbildung,
    das Ende eines Forschungsauftrags, eine fertig gewordene Werkstattware und die Ankunft oder
    Rückkehr einer Mission. Nur Zeiten **nach** `jetzt` kommen zurück — ein längst fälliges
    Ereignis wird nicht wiederholt, es wird beim nächsten Schritt ohnehin nachgebucht.
    """
    zeiten: List[float] = []
    for o in (orte or {}).values() if isinstance(orte, dict) else (orte or []):
        for a in (o.get("ausbildung") or []):
            if not a.get("gebucht") and a.get("ende") is not None:
                zeiten.append(float(a["ende"]))
        a = o.get("forschungsauftrag")
        if a:
            zeiten.append(float(a["startzeit"]) + float(a["dauer_stunden"]) * 3600.0)
        for schlange in (o.get("werkstaetten") or {}).values():
            for e in (schlange.get("einheiten") or []):
                if e.get("ende") is not None and not e.get("gemeldet"):
                    zeiten.append(float(e["ende"]))
    for m in (missionen or []):
        for feld in ("ankunft", "rueckkehr"):
            if m.get(feld):
                zeiten.append(float(m[feld]))
    return sorted(t for t in zeiten if t > jetzt)


def tick_bis(orte: dict, missionen: list, wissen: dict, jetzt: float, ende: float,
             forschung_buchen: bool = True) -> tuple:
    """Die Spieluhr in EREIGNISGRÖSSEN fortschreiben (Entwurf Z. 645-648 und Z. 961-1009).

    Ein großer Sprung (etwa eine Stunde Spielzeit) wird in die Spannen zerlegt, die die
    **Ereignisse des Zustands** vorgeben — nicht in feste Häppchen. Innerhalb jeder Spanne wird je
    Ort `ort_tick` gebucht und danach der Abschluss je Ort sowie der Fortschritt je Mission
    geprüft. Dadurch ist ein einziger großer Sprung **genau so viel** wie viele kleine Schritte:
    eine Forschung, die mitten im Fenster fertig wird, wirkt **ab ihrem Zeitpunkt** auf die
    Produktion (ohne Zerlegung wirkte sie erst am Spannenende — genau der Fehler, den der Entwurf
    verbietet: „ein großer dt ohne Ereignissplitting ist kein gleichwertiger Ersatz").

    Liefert ``(orte, missionen, wissen, zeit, ereignisse)``:
      * ``orte`` — neuer Stand je Kennung (dict)
      * ``missionen`` — fortgeschriebene Missionen (Ankunft/Rückkehr **genau einmal**)
      * ``wissen`` — der (ggf. gestiegene) Forschungsstand ``{Gebiet: Stufe}``
      * ``zeit`` — die erreichte Spielzeit (== `ende`)
      * ``ereignisse`` — die Spielzeiten, an denen wirklich gebucht wurde (Nachweis)

    **Reine Funktion:** der übergebene Zustand wird nicht verändert.
    """
    if not math.isfinite(ende) or not math.isfinite(jetzt) or ende < jetzt:
        raise ValueError("Ungültiges Tickende.")
    neu_orte = copy.deepcopy(orte) if isinstance(orte, dict) else {o["id"]: copy.deepcopy(o)
                                                                  for o in (orte or [])}
    neu_missionen = copy.deepcopy(missionen or [])
    neu_wissen = dict(wissen or {})
    ereignisse: List[float] = []

    def abrechnen(ab: float, bis: float):
        """Bucht die Spanne [ab, bis]: je Ort ernten/warten/lernen, Abschlüsse und Missionen.

        Bei `ab == bis` wird **nichts geerntet** (die Spanne ist 0), aber sehr wohl **Fälliges**
        gebucht: eine fertige Werkstattware, eine abgeschlossene Ausbildung, ein fälliger
        Forschungsabschluss und eine fällige Ankunft. Genau das braucht ein Takt OHNE Spanne,
        wenn die Uhr von außen gestellt wurde (die Prüfungen P27/P28 haben es gefunden).
        """
        nonlocal neu_orte, neu_missionen, neu_wissen
        for kennung in sorted(neu_orte):
            o = neu_orte[kennung]
            neu_orte[kennung] = ort_tick(o, ab, bis, neu_wissen)
        if forschung_buchen:
            for kennung in sorted(neu_orte):
                o = neu_orte[kennung]
                o, neu_wissen = forschung_abschluss(o, neu_wissen, bis)
                neu_orte[kennung] = o
        for i, m in enumerate(neu_missionen):
            if m.get("fremdvertrag"):
                neu_orte, neu_missionen[i] = handel_abschluss(m, neu_orte, bis)
            else:
                neu_orte, neu_missionen[i] = transport_fortschritt(m, neu_orte, bis)

    if ende == jetzt:
        abrechnen(jetzt, jetzt)
        return neu_orte, neu_missionen, neu_wissen, ende, ereignisse

    t = jetzt
    schritte = 0
    while t < ende:
        schritte += 1
        if schritte > 5000:                      # Schutz gegen eine Ereignisschleife
            raise ValueError("Zu viele Ereignisse in einer Spanne.")
        bis = min([ende] + ereigniszeiten(neu_orte, neu_missionen, t))
        abrechnen(t, bis)
        ereignisse.append(bis)
        t = bis
    return neu_orte, neu_missionen, neu_wissen, t, ereignisse


# ---------------------------------------------------------------------------
# Schritt 6 — Forschung JE SIEDLUNG: lokaler Forschungsstart statt globaler
# Bibliotheksabkürzung (Entwurf Z. 650-686)
# ---------------------------------------------------------------------------
#
# BELEGT (Handbuch 2009): die Bibliothek ist je Siedlung (Z. 404 „In jeder Siedlung kann nur eine
# einzige Bibliothek gebaut werden."), und die Sperre gilt „in der Siedlung, in der geforscht wird"
# (Z. 423-424); Z. 245 spricht von den „in den Siedlungen laufenden Forschungen" (Mehrzahl) — zwei
# Siedlungen dürfen also **verschiedene** Gebiete gleichzeitig erforschen. Der laufende Auftrag hängt
# darum am **Ort** (`ort["forschungsauftrag"]`), nicht am Spieler.
#
# Die erreichte **Stufe** bleibt in `wissen` (dem übergebenen Stand) — ob dieser Stand je Siedlung
# oder für das ganze Volk gilt, sagt das Handbuch **nicht** (Z. 104-106 „Dein Volk" gegen Z. 397
# „Deine Siedlungen"); das ist offen und in `archiv/analysen/audits/belege_forschung_je_siedlung.md` festgehalten.


def forschung_start(ort: dict, gebiet: str, wissen: dict, jetzt: float,
                    weitere_orte: list = ()) -> dict:
    """Einen Forschungsauftrag **in dieser Siedlung** erteilen. Liefert den neuen Ort.

    Prüft: keine zweite Forschung in derselben Bibliothek · bekanntes Gebiet · Voraussetzungen
    über `forschungspfad.erfuellt` (mit der Bibliotheksstufe **dieses** Ortes) · Rohstoffe.
    Die Kosten werden beim Start verbraucht; die Stufe steigt erst am Ende (`forschung_abschluss`).

    `weitere_orte` sind die übrigen **eigenen** Orte. Der Entwurf (Z. 685) verlangt ausdrücklich,
    dass dieselbe Zielstufe nicht gleichzeitig in zwei Städten läuft — sonst zahlt man zweimal und
    lernt einmal. Verschiedene Gebiete dürfen in verschiedenen Bibliotheken parallel laufen.
    """
    neu = copy.deepcopy(ort)
    if neu.get("forschungsauftrag") is not None:
        raise ValueError("Diese Bibliothek forscht bereits.")
    if gebiet not in spieldaten.forschungen():
        raise ValueError("Unbekanntes Forschungsgebiet.")
    bibliothek = gebaeude_wirkung.bibliothek_stufe([neu])
    ok, grund = forschungspfad.erfuellt(gebiet, wissen, bibliothek)
    if not ok:
        raise ValueError(grund)
    ziel = wissen.get(gebiet, 0) + 1
    for anderer in weitere_orte or ():
        a = (anderer or {}).get("forschungsauftrag")
        if a and a.get("gebiet") == gebiet and a.get("zielstufe") == ziel:
            raise ValueError(f"{gebiet} Stufe {ziel} forscht bereits eine andere Siedlung — "
                             f"zweimal dieselbe Stufe zahlt doppelt und bringt nichts.")
    kosten = forschung.kosten(ziel)
    neu = verbrauchen(neu, kosten, jetzt)
    stand = {gebiet: {"stufe": wissen.get(gebiet, 0), "auftrag": None}}
    # Material ist oben schon transaktional bezahlt → `forschung.starten` darf nichts abziehen.
    ok, grund = forschung.starten(gebiet, stand, jetzt, bibliothek > 0, None)
    if not ok:
        raise ValueError(grund)
    neu["forschungsauftrag"] = {"gebiet": gebiet, **stand[gebiet]["auftrag"]}
    return neu


def forschung_abschluss(ort: dict, wissen: dict, jetzt: float) -> tuple:
    """Eine abgelaufene Forschung **dieser Siedlung** verbuchen. Liefert ``(ort, wissen)``.

    Die Stufe steigt nur nach oben (`max`) — zweimal abschließen kann nichts doppeln —, der Auftrag
    wird gelöscht und die Fertigstellung ins `fertigjournal` geschrieben (Grundlage der Zielprüfung,
    Schritt 7).
    """
    neu, kenntnis = copy.deepcopy(ort), dict(wissen)
    a = neu.get("forschungsauftrag")
    if a and a["startzeit"] + a["dauer_stunden"] * 3600 <= jetzt:
        kenntnis[a["gebiet"]] = max(kenntnis.get(a["gebiet"], 0), a["zielstufe"])
        neu["forschungsauftrag"] = None
        neu["fertigjournal"].append({"zeit": jetzt, "art": "forschung", "name": a["gebiet"]})
    return neu, kenntnis


# ---------------------------------------------------------------------------
# Schritt 7 — Zielprüfung und Haltefenster, UNABHÄNGIG von den Originalpunkten
# (Entwurf Z. 688-715)
# ---------------------------------------------------------------------------
#
# Der Altmodus gewinnt über Punkte (`punkte.sieg_oder_niederlage`). Der Ökonomiemodus gewinnt
# über eine **versorgte Wirtschaft**: genug Original-Siedlungen, gedeckter Plan,
# gehaltene Reserve, echter
# Handel, beide Rollen, Ware **und** Forschung fertig — und das alles **ein volles
# Versorgungsfenster lang** (Haltefenster). Die Original-Punkteformeln bleiben unangetastet.
#
# Der Zweck ist ausdrücklich der **Ausschluss von Scheinsiegen**: wer nur Punkte farmt, Fracht
# sinnlos hin und her schiebt oder seine notwendige Versorgung verliert, erfüllt die Bedingungen nicht
# und verliert damit auch das Haltefenster wieder (Entwurf Z. 715).
#
# `reserve` (was ein Ort im Fenster zurücklegen WILL) wird je Ort erwartet — gesetzt wird es von
# der Aufstellung/Planung (Schritt 8/9). Fehlt es, gilt „keine Reserve gefordert": dann kann der
# Plan nicht gedeckt sein und das Ziel ist nicht erreicht (VORSCHLAG, konservativ — der Entwurf
# verlangt genau diese Strenge, damit ein Sieg nicht zufällig geschieht).


def zielstatus(orte: list, jetzt: float, haltestart=None) -> dict:
    """Sind die Bedingungen des Versorgungsziels erfüllt — und wie lange schon?

    Liefert ``sieg``, ``haltestart`` (None, wenn gerade nicht erfüllt — dann beginnt das
    Haltefenster neu), ``qualitaet``, ``deckung``, ``reserve``, ``handel``, ``armee`` und ``plan``.

    Gemessen wird **rückblickend**: die Deckung kommt aus dem tatsächlichen Produktionsjournal
    (`fensterproduktion`), der Handel aus dem Verbrauchsjournal (mindestens **zwei Rohstoffe**
    aus **zwei Orten** müssen wirklich verbraucht worden sein) — nicht aus einer Momentaufnahme.
    """
    orte = [o for o in (orte or []) if isinstance(o, dict)]
    # Ohne Orte liefert `kartenqualitaet` selbst schon `{"erfuellt": False, ...}` (eigene Zeile
    # dort) — die frühere Sonderbehandlung hier war unnötig und änderte die FORM des Feldes
    # (ohne "mittel"/"beste"). Fund der Abweichungsprüfung zu Schritt 7.
    q = kartenqualitaet([o["karte"] for o in orte])
    menge = fensterproduktion(orte, jetzt)
    plan = REGELN["plan"]
    reserviert = {r: sum((o.get("reserve") or {}).get(r, 0) for o in orte) for r in plan}
    plan_ok = bezahlbar(reserviert, plan)
    deckung = min((menge.get(r, 0) / n for r, n in plan.items() if n > 0), default=0.0)
    # VORSCHLAG (nicht belegt), bewusst vom Entwurf abweichend: der Entwurf schreibt hier
    # `all(...)` ohne die Ortsgrenze. Die Prüfung zu Schritt 7 hat dargelegt, dass das den SIEG
    # **nicht** ändert (ein leerer Verbund scheitert ohnehin an der Kartenqualität, die vier
    # Siedlungen verlangt) — die frühere Begründung „ein leerer Spielstand hätte gehalten" war
    # also falsch. Es bleibt eine **Anzeige**-Korrektur: `reserve` soll für einen Verbund ohne
    # Siedlungen nicht „gehalten" melden. Auf `ok`/`sieg` wirkt sie nicht. Daniel kann sie
    # streichen lassen; dann gilt wieder zeichengleich der Entwurf.
    reserve = bool(orte) and all(bezahlbar(o.get("vorraete") or {}, o.get("reserve") or {})
                                 for o in orte)
    ab = jetzt - REGELN["versorgung_stunden"] * 3600
    importe = {(o.get("id"), z["rohstoff"]) for o in orte
               for z in (o.get("verbrauchsjournal") or [])
               if ab < z["zeit"] <= jetzt and z["menge"] > 0}
    handel = len({r for _, r in importe}) >= 2 and len({i for i, _ in importe}) >= 2
    rollen = {einheiten.rolle(n) for o in orte for n, k in (o.get("einheiten") or {}).items()
              if k > 0}
    armee = "kaempfer" in rollen and "kundschafter" in rollen
    fertig = {z["art"] for o in orte for z in (o.get("fertigjournal") or [])}
    ok = (bool(q.get("erfuellt")) and plan_ok and deckung >= 1 and reserve and handel and armee
          and {"ware", "forschung"} <= fertig)
    start = (jetzt if haltestart is None else haltestart) if ok else None
    sieg = bool(ok and start is not None
                and jetzt - start >= REGELN["versorgung_stunden"] * 3600)
    # `plan` ist über den Entwurf hinaus — er nennt die Rückgabe ohne diesen Schlüssel, verlangt
    # aber „messbare Fehlgründe" (Z. 714). Nur eine Anzeige, keine Rechnung.
    return {"sieg": sieg, "haltestart": start, "qualitaet": q, "deckung": deckung,
            "reserve": reserve, "handel": handel, "armee": armee, "plan": plan_ok}


# ---------------------------------------------------------------------------
# Schritt 8b — bestätigter Fremdhandel: Angebot, beidseitige Sperre, Abschluss
# (Entwurf Z. 752 sowie Z. 878-940)
# ---------------------------------------------------------------------------
#
# Ein bestätigtes EINZELANGEBOT mit echter Handelskarawane — **keine** Netzfunktionen. Der alte
# `_trade`-Pfad (Gratisrohstoffe) wird dafür **nicht** weiterverwendet, sondern ersetzt.
#
# BELEGT (Handbuch 2009, Z. 1120 ff. — Zitat und Zeile in
# `archiv/analysen/audits/handbuch_abgleich_2026-10-05.txt`): Handel zwischen eigenen Siedlungen ist belegt;
# für den Handel mit Fremden nennt das Handbuch die Handelskarawane und die Rückkehr MIT den Waren
# bei Ablehnung (S. 20). Der Preis wird beim Angebot festgelegt und danach nicht mehr verhandelt.
#
# Das Wesen der Transaktion ist die **Sperre**: Kaufpreis (Gold des Käufers) und Handelsgut (Lager
# des Verkäufers) verlassen ab dem Start ihre Lager und liegen AM VERTRAG. Erst die Ankunft der
# Karawane macht das Angebot wahr; kehrt sie ohne Annahme zurück, erhält jede Seite das Ihre
# vollständig zurück — samt der **Importherkunft** (dieselbe anteilige Sperrlogik wie in
# `transport_start`). So entstehen weder Gratisgewinne noch Geistergutschriften.
#
# Der Vertrag ist eine Mission mit `fremdvertrag=True`; gebucht wird er **ausschließlich** von
# `handel_abschluss` — `auftraege.spieldaten_anwenden` lässt ihn unberührt (genau wie einen
# Eigentransport). Die Ereignisschleife (Schritt 10) unterscheidet beide Wege an diesem Merkmal.
#
# **Die Annahme ist eine Entscheidung, kein Zufall** (Handbuch S. 20, belegt in
# `auftraege.auftragsarten`: „Bei Ablehnung kehrt die Karawane MIT den Waren zurück, Gold wird nie
# uebertragen."). Der Verkäuferort hält sie im Vertragsfeld `entscheidung` fest
# (`handel_entscheiden`): `True` nimmt an, `False` lehnt ab, `None` überlässt die Entscheidung der
# Ankunft — dann nimmt der Ort an, sobald die Karawane bei ihm steht und er noch seiner ist.
# Ohne dieses Feld wäre die belegte Ablehnungsregel **nicht erreichbar** (der Entwurfscode nahm
# immer an, sobald der Verkäuferort lebte) — gefunden beim Bau dieser Prüfdatei, eigener Zusatz,
# den Daniel streichen kann.
#
# WICHTIG (Entwurf Z. 939): Der **Sieg-Handelsnachweis** bleibt ausschließlich den eigenen
# Transporten vorbehalten. Ein Fremdkauf erhöht `importiert`/`verbrauchsjournal` des Käufers
# deshalb NICHT — sonst könnte man sich den Handelsnachweis einfach kaufen.


def handel_start(kaeufer: dict, verkaeufer: dict, einheitenbestand: dict, ware: str,
                 menge: int, preis: float, kanal: str, jetzt: float):
    """Ein bestätigtes Einzelangebot starten. Liefert ``(kaeufer_neu, verkaeufer_neu, vertrag)``.

    ``kanal`` ist ``"vorraete"`` (Rohstoff) oder ``"waren"``. Geprüft wird **vor** jeder Buchung:
    Kanal und Handelsgut, positives ganzzahliges Angebot, positiver endlicher Preis, fremder
    Besitzer, gleiche Dimension, Karawane vor Ort, beidseitige Deckung (Lager **und** Gold) und
    die Rückladung der Karawane. Jede Ablehnung ist ein ``ValueError`` — es wird nichts halb
    gebucht, die übergebenen Orte bleiben unverändert.
    """
    if kanal not in ("vorraete", "waren"):
        raise ValueError("Unbekannter Frachtkanal.")
    if type(menge) is not int or menge <= 0:
        raise ValueError("Ungültige Handelsmenge.")
    if isinstance(preis, bool) or not isinstance(preis, (int, float)) or not math.isfinite(preis) \
            or preis <= 0:
        raise ValueError("Ungültiger Preis.")
    if ware == "gold":
        raise ValueError("Gold ist kein Handelsgut, sondern die Gegenleistung.")
    if kaeufer["besitzer"] == verkaeufer["besitzer"]:
        raise ValueError("Eigener Warentransport braucht keinen Kaufvertrag.")
    if kaeufer["dimension"] != verkaeufer["dimension"]:
        raise ValueError("Fremde Dimension benötigt noch unbelegte Missionstarife.")
    if not einheitenbestand or any(type(n) is not int or n <= 0
                                   for n in einheitenbestand.values()):
        raise ValueError("Ungültige Karawanentruppe.")
    if any(kaeufer["einheiten"].get(n, 0) < m for n, m in einheitenbestand.items()):
        raise ValueError("Karawane fehlt vor Ort.")
    if verkaeufer[kanal].get(ware, 0) < menge:
        raise ValueError("Angebot nicht gedeckt: dem Verkäufer fehlt die Ware.")
    gold = menge * preis
    if kaeufer["vorraete"].get("gold", 0) < gold:
        raise ValueError("Angebot nicht gedeckt: dem Käufer fehlt das Gold.")
    d = abs(kaeufer["x"] - verkaeufer["x"]) + abs(kaeufer["y"] - verkaeufer["y"])
    liste = []
    ok, grund = auftraege.starten(liste, "handeln", einheitenbestand, kaeufer["id"],
                                  verkaeufer["id"], d, jetzt, {})
    if not ok:
        raise ValueError(grund)
    # Erst nach dem Auftragskern: die Karawanenpflicht steht BELEGT in `auftraege.auftragsarten`
    # („Nur Handelskarawanen") — diese Meldung ist besser als eine selbst erfundene. Gebucht ist
    # bis hierher nichts: `starten` füllt nur die Liste, die bei einer Ablehnung verworfen wird.
    if menge > auftraege.ladung_der_mission(einheitenbestand):
        raise ValueError("Kaufmenge übersteigt die Rückladung der Karawane.")
    k, v, vertrag = copy.deepcopy(kaeufer), copy.deepcopy(verkaeufer), liste[0]

    # Gegenleistung sperren: das Gold des Käufers (mit seinem Importanteil).
    goldbestand = k["vorraete"].get("gold", 0)
    sperrgold_import = 0.0 if goldbestand <= 0 else min(
        k["importiert"].get("gold", 0), gold * k["importiert"].get("gold", 0) / goldbestand)
    k["vorraete"]["gold"] = goldbestand - gold
    k["importiert"]["gold"] = max(0.0, k["importiert"].get("gold", 0) - sperrgold_import)

    # Handelsgut sperren: die Ware des Verkäufers (mit ihrem Importanteil, nur Rohstoffkanal).
    verkauft_import = {}
    if kanal == "vorraete":
        lager = v["vorraete"].get(ware, 0)
        anteil = 0.0 if lager <= 0 else menge * v["importiert"].get(ware, 0) / lager
        verkauft_import[ware] = anteil
        v["importiert"][ware] = max(0.0, v["importiert"].get(ware, 0) - anteil)
    v[kanal][ware] = v[kanal].get(ware, 0) - menge

    for n, z in einheitenbestand.items():
        k["einheiten"][n] = k["einheiten"].get(n, 0) - z

    vertrag.update({"fremdvertrag": True, "kaeufer": k["id"], "verkaeufer": v["id"],
                    "kaeufer_owner": k["besitzer"], "verkaeufer_owner": v["besitzer"],
                    "ware": ware, "menge": menge, "preis": float(preis), "kanal": kanal,
                    "angenommen": False, "abgerechnet": False, "entscheidung": None,
                    "sperrgold": gold, "sperrgold_import": sperrgold_import,
                    "verkauft_import": verkauft_import})
    vertrag["besitzer"] = k["besitzer"]
    return k, v, vertrag


def handel_entscheiden(vertrag: dict, angenommen: bool) -> dict:
    """Die Entscheidung des Verkäuferorts festhalten (vor dem Abschluss). Liefert den Vertrag.

    ``True`` nimmt das Angebot an, ``False`` lehnt es ab (belegt, Handbuch S. 20). Ein bereits
    abgerechneter Vertrag lässt sich nicht mehr entscheiden.
    """
    neu = copy.deepcopy(vertrag)
    if neu.get("abgerechnet"):
        raise ValueError("Der Vertrag ist bereits abgerechnet.")
    neu["entscheidung"] = bool(angenommen)
    return neu


def handel_abschluss(vertrag: dict, orte: dict, jetzt: float):
    """Ankunft und Rückkehr eines Fremdvertrags buchen — **genau einmal**. ``(orte, vertrag)``.

    * **Ankunft:** nimmt der Verkäuferort an (Feld `entscheidung`; ohne Entscheidung nimmt er an,
      sobald die Karawane bei ihm steht und der Ort noch seiner ist), wandert das gesperrte Gold
      zu ihm — mit der Importherkunft. Bei Ablehnung oder verlorenem Ort bleibt alles gesperrt.
    * **Rückkehr:** bei Annahme kommt die Ware beim Käufer an, bei Ablehnung kehren Gold **und**
      Ware vollständig zurück (belegte Regel, Handbuch S. 20); die Karawane kommt in beiden
      Fällen heim.
    * Ist der **Käuferort** verloren, bleibt das Gut AM VERTRAG — keine Geistergutschrift, keine
      Schenkung an einen neuen Besitzer (Entwurf Z. 924/932).
    """
    neu, m = copy.deepcopy(orte), copy.deepcopy(vertrag)
    kaeufer, verkaeufer = neu.get(m["kaeufer"]), neu.get(m["verkaeufer"])

    if jetzt >= m["ankunft"] and not m["angenommen"]:
        if m.get("entscheidung") is not False and verkaeufer is not None \
                and verkaeufer["besitzer"] == m["verkaeufer_owner"]:
            verkaeufer["vorraete"]["gold"] = verkaeufer["vorraete"].get("gold", 0) + m["sperrgold"]
            verkaeufer["importiert"]["gold"] = (verkaeufer["importiert"].get("gold", 0)
                                               + m["sperrgold_import"])
            m["sperrgold"], m["sperrgold_import"] = 0.0, 0.0
            m["angenommen"] = True

    if jetzt >= m["rueckkehr"] and not m["abgerechnet"]:
        if kaeufer is None or kaeufer["besitzer"] != m["kaeufer_owner"]:
            return neu, m          # Gut bleibt am Vertrag; ein späterer eigener Ort kann es noch erhalten.
        if m["angenommen"]:
            kaeufer[m["kanal"]][m["ware"]] = kaeufer[m["kanal"]].get(m["ware"], 0) + m["menge"]
            # Bewusst KEIN Eintrag in `importiert`: ein Fremdkauf ist kein eigener Handelsnachweis.
        else:
            kaeufer["vorraete"]["gold"] = kaeufer["vorraete"].get("gold", 0) + m["sperrgold"]
            kaeufer["importiert"]["gold"] = (kaeufer["importiert"].get("gold", 0)
                                            + m["sperrgold_import"])
            m["sperrgold"], m["sperrgold_import"] = 0.0, 0.0
            if verkaeufer is not None and verkaeufer["besitzer"] == m["verkaeufer_owner"]:
                verkaeufer[m["kanal"]][m["ware"]] = (verkaeufer[m["kanal"]].get(m["ware"], 0)
                                                     + m["menge"])
                if m["kanal"] == "vorraete":
                    verkaeufer["importiert"][m["ware"]] = (
                        verkaeufer["importiert"].get(m["ware"], 0)
                        + m["verkauft_import"].get(m["ware"], 0))
            else:
                # Verlorenes Verkäufergut bleibt vermerkt; nicht an einen neuen Besitzer schenken.
                m["verlorenes_sperrgut"] = {m["ware"]: m["menge"]}
        for n, z in m["einheiten"].items():
            kaeufer["einheiten"][n] = kaeufer["einheiten"].get(n, 0) + z
        m["abgerechnet"] = True
    return neu, m

```

### Datei `src/werkstatt.py` (422 Zeilen)

```python
"""
Nebelseetal Remake - Waren und Werkstaetten (Paket W3, 04.10.2026).

Die 17 Waren des Originals werden in drei Werkstaetten gefertigt:

  Schmiede   -> Waffen und Ruestungen (Messer ... Magischer Paladinharnisch), 8 Waren
  Bogenbauer -> Fernwaffen (Kurzbogen ... Armbrust), 4 Waren
  Naehstube  -> Stoff- und Fellkleidung (Wollumhang ... Fellruestung), 5 Waren

BELEGT ist (Handbuch 2009, Seite 13/14; data/buildings.json; data/items.json):
  * welche Ware in welcher Werkstatt entsteht,
  * dass Waren ueber WARTSCHLANGEN laufen,
  * dass mehrere GLEICHE Werkstaetten nebeneinander fertigen - das Handbuchbeispiel
    lautet: 10 Schwerter a 20 Minuten mit ZWEI Schmieden = 100 statt 200 Minuten,
  * dass der Warenbestand im Lager geprueft wird.

NICHT belegt und darum bewusst NICHT erfunden:
  * die Fertigungsdauer jeder anderen Ware - das Handbuch nennt die 20 Minuten NUR
    fuer das Schwert-Beispiel. `dauer_sekunden` gibt fuer alle anderen Waren None
    zurueck; `dauer_belegt` ist nur fuer Schwert True.
  * der Stufen-Einfluss auf die Fertigungsdauer der Werkstaetten. Er ist hier als
    VORSCHLAG (+10 % Tempo je Stufe, wie die belegten +10 %-Stufenregeln des Spiels)
    umgesetzt und in den Meldungen als solcher gekennzeichnet.

Das Modul zeichnet nichts, aendert keine fremde Datei und nutzt nur die
Standardbibliothek plus die Projektdaten (`spieldaten`, `gelaende`).
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

import gelaende
import spieldaten

# Die drei Werkstatt-Kennungen - so heissen die Werkstaetten in data/buildings.json.
WERKSTAETTEN = ("schmiede", "bogenbauer", "naehstube")

# Die einzige BELEGTE Fertigungsdauer: das Handbuchbeispiel nennt 20 Minuten fuer ein Schwert.
BELEGTE_DAUER_SEKUNDEN: Dict[str, float] = {"Schwert": 20 * 60}

# VORSCHLAG (nicht belegt): hoehere Werkstattstufe macht schneller, +10 % Tempo je Stufe
# ueber Stufe 1 hinaus. Grundlage ist die belegte Stufenlogik des Spiels (z. B. Heilkunde
# +10 % je Stufe). In `data/...` gibt es dafuer keinen Wert; hier ist er ehrlich markiert.
STUFE_TEMPO_PROZENT = 10

# Belegte Zweitnamen aus der Quellenlage: die Auswertung fuehrt das Gebaeude als "Bogner",
# das Handbuch 2009 als "Bogenbauer" (data/buildings.json, Anmerkung). Beide sind gueltig.
WERKSTATT_ALIASE: Dict[str, str] = {
    "Bogner": "bogenbauer",
    "bogenbauer": "bogenbauer",
    "schmiede": "schmiede",
    "naehstube": "naehstube",
}


# --------------------------------------------------------------------------
# 1. Die drei Werkstaetten aus data/buildings.json
# --------------------------------------------------------------------------

def _werkstatt_eintraege() -> List[Dict[str, Any]]:
    return [g for g in spieldaten.gebaeude()
            if g.get("kategorie") == "Werkstatt" and g.get("id")]


def werkstaetten() -> Dict[str, str]:
    """{kennung: Anzeigename} der drei Werkstaetten - direkt aus data/buildings.json."""
    return {g["id"]: g.get("name") or g["id"] for g in _werkstatt_eintraege()}


def _namen_nach_kennung() -> Dict[str, str]:
    """{vergleichsname: kennung} - Anzeigename und belegte Aliase (Bogner)."""
    zu: Dict[str, str] = {}
    for kennung, anzeige in werkstaetten().items():
        zu[_vergleich(anzeige)] = kennung
    for name, kennung in WERKSTATT_ALIASE.items():
        zu.setdefault(_vergleich(name), kennung)
    return zu


def _vergleich(name: str) -> str:
    """Vergleichsform eines Werkstattnamens: klein, ohne Umlaute (wie gelaende._norm)."""
    return gelaende._norm(name)


def _werkstatt_kennung(typ: str) -> Optional[str]:
    """Eine Werkstattkennung aus Kennung ODER Anzeigename ODER belegtem Zweitnamen (Bogner)."""
    if not typ:
        return None
    kennung = gelaende.finde_gebaeude(typ)
    if kennung in werkstaetten():
        return kennung
    return _namen_nach_kennung().get(_vergleich(typ))


# --------------------------------------------------------------------------
# 2. Waren je Werkstatt (aus data/items.json) und Rueckrichtung
# --------------------------------------------------------------------------

def _waren() -> Dict[str, Dict[str, Any]]:
    return spieldaten.waren()


def waren_der_werkstatt(typ: str) -> List[str]:
    """Alle Waren einer Werkstatt in der Reihenfolge von data/items.json."""
    kennung = _werkstatt_kennung(typ)
    if not kennung:
        return []
    treffer: List[str] = []
    for ware, eintrag in _waren().items():
        name = eintrag.get("werkstatt") or ""
        ziel = _namen_nach_kennung().get(_vergleich(name))
        if ziel == kennung:
            treffer.append(ware)
    return treffer


def werkstatt_fuer(ware: str) -> Optional[str]:
    """Die Kennung der Werkstatt einer Ware - None, wenn die Ware zu keiner Werkstatt gehoert."""
    if not ware:
        return None
    eintrag = _waren().get(ware)
    if not eintrag:
        return None
    name = eintrag.get("werkstatt") or ""
    return _namen_nach_kennung().get(_vergleich(name))


# --------------------------------------------------------------------------
# 3. Dauer - nur wo belegt, sonst ehrlich None
# --------------------------------------------------------------------------

def _stufe_wert(stufe: Any) -> int:
    try:
        s = int(stufe)
    except (TypeError, ValueError):
        s = 1
    return max(1, s)


def _stufe_faktor(stufe: int) -> float:
    """Tempo-Faktor der Werkstattstufe (VORSCHLAG, siehe Modulkopf)."""
    return 1.0 + STUFE_TEMPO_PROZENT / 100.0 * (_stufe_wert(stufe) - 1)


def dauer_sekunden(ware: str, stufe: int = 1,
                   rezepte: Optional[Dict[str, Any]] = None) -> Optional[float]:
    """Fertigungsdauer in Sekunden - None, wenn weder Handbuch noch Rezept eine Dauer nennen.

    Belegt ist nur das Schwert-Beispiel mit 20 Minuten (1200 s). Fuer alle anderen Waren
    wird NICHTS geschaetzt. Hoehere Stufe verkuerzt die belegte Grunddauer (VORSCHLAG).

    ``rezepte`` (Vorgabe None = Altmodus, unveraendert): die freigegebene
    ``data/warenrezepte.json``. Wird sie uebergeben, gilt fuer Waren OHNE belegte Dauer die
    dort eingefrorene Vorschlagsdauer (Oekonomie-Paket, Schritt 4 — Entwurf Z. 588-589).
    ``dauer_belegt`` bleibt bewusst unveraendert: nur das Schwert ist belegt.
    """
    basis = BELEGTE_DAUER_SEKUNDEN.get(ware)
    if basis is None and rezepte:
        wert = (rezepte.get(ware) or {}).get("dauer")
        try:
            basis = float(wert)
        except (TypeError, ValueError):
            basis = None
    if basis is None:
        return None
    return round(basis / _stufe_faktor(stufe), 3)


def dauer_belegt(ware: str) -> bool:
    """True nur fuer Waren mit BELEGTER Dauer - das ist allein das Schwert (20 Minuten)."""
    return ware in BELEGTE_DAUER_SEKUNDEN


# --------------------------------------------------------------------------
# 4. Warteschlange: n gleiche Werkstaetten fertigen n Waren gleichzeitig
# --------------------------------------------------------------------------

def kapazitaet(anzahl_werkstaetten: int) -> int:
    """Wie viele Waren gleichzeitig fertigen - 1 Platz je Werkstatt."""
    try:
        n = int(anzahl_werkstaetten)
    except (TypeError, ValueError):
        return 0
    return max(0, n)


def neue_warteschlange(typ: str, anzahl_werkstaetten: int) -> Dict[str, Any]:
    """Ein leerer Auftragsstapel einer Werkstatt mit n parallelen Plaetzen."""
    kennung = _werkstatt_kennung(typ) or typ
    try:
        anzahl = int(anzahl_werkstaetten)
    except (TypeError, ValueError):
        anzahl = 0
    return {
        "typ": kennung,
        "werkstatt": werkstaetten().get(kennung, kennung),
        "werkstaetten": anzahl,
        "kapazitaet": kapazitaet(anzahl),
        "auftraege": [],
        "einheiten": [],
        "_basis": None,
        "_uhr": None,
    }


def einreihen(schlange: Dict[str, Any], ware: str,
              anzahl: int, stufe: int = 1,
              rezepte: Optional[Dict[str, Any]] = None) -> Tuple[bool, str]:
    """Eine Ware in die Warteschlange stellen. (ok, Meldung).

    ``rezepte`` wird an ``dauer_sekunden`` durchgereicht (Vorgabe None = Altmodus, unveraendert).
    """
    if not isinstance(schlange, dict) or "einheiten" not in schlange:
        return False, "Keine gueltige Warteschlange uebergeben."
    if ware not in _waren():
        return False, f"'{ware}' ist keine bekannte Ware."
    ziel = werkstatt_fuer(ware)
    if ziel is None:
        return False, f"'{ware}' gehoert zu keiner Werkstatt."
    if ziel != schlange.get("typ"):
        return False, (f"'{ware}' gehoert nicht in die Werkstatt "
                       f"{schlange.get('werkstatt')}.")
    try:
        menge = int(anzahl)
    except (TypeError, ValueError):
        return False, "Die Anzahl muss eine ganze Zahl sein."
    if menge <= 0:
        return False, "Die Anzahl muss groesser als 0 sein."

    s = _stufe_wert(stufe)
    dauer = dauer_sekunden(ware, s, rezepte)
    ab = schlange.get("_uhr")
    for _ in range(menge):
        schlange["einheiten"].append({
            "ware": ware, "stufe": s, "dauer": dauer, "ab": ab,
            "gemeldet": False, "start": None, "ende": None,
        })
    schlange["auftraege"].append({"ware": ware, "anzahl": menge, "stufe": s, "dauer": dauer})

    if dauer is None:
        return True, (f"{menge}x {ware} eingereiht - Dauer nicht belegt, "
                      f"die Ware wartet im Stapel.")
    return True, f"{menge}x {ware} eingereiht ({dauer / 60.0:.1f} Minuten je Stueck)."


def _fortschreiben(schlange: Dict[str, Any], jetzt: float) -> float:
    """Plant alle Einheiten ab dem Queue-Start und liefert die aktuelle Stapelzeit."""
    try:
        jetzt = float(jetzt)
    except (TypeError, ValueError):
        jetzt = 0.0
    if schlange.get("_basis") is None:
        schlange["_basis"] = jetzt
    basis = float(schlange["_basis"])
    if jetzt < basis:
        jetzt = basis
    uhr = schlange.get("_uhr")
    if uhr is None or jetzt > float(uhr):
        schlange["_uhr"] = jetzt

    n = int(schlange.get("kapazitaet") or 0)
    einheiten = schlange.get("einheiten", [])
    if n < 1:
        for e in einheiten:
            e["start"] = None
            e["ende"] = None
        return float(schlange["_uhr"])

    slots = [basis] * n
    for e in einheiten:
        i = min(range(n), key=lambda k: slots[k])          # fruehester freier Platz
        ab = e.get("ab")
        start = slots[i] if ab is None else max(slots[i], float(ab))
        e["start"] = start
        if e.get("dauer") is None:
            e["ende"] = None
            slots[i] = float("inf")                        # belegter Platz bleibt belegt
        else:
            e["ende"] = start + float(e["dauer"])
            slots[i] = e["ende"]
    return float(schlange["_uhr"])


def fortschritt(schlange: Dict[str, Any], jetzt: float) -> Dict[str, Any]:
    """Was laeuft, was ist fertig und wie lange der Stapel noch braucht."""
    t = _fortschreiben(schlange, jetzt)
    laeuft: List[Dict[str, Any]] = []
    fertig: List[Dict[str, Any]] = []
    wartend: List[Dict[str, Any]] = []
    unbelegt: List[Dict[str, Any]] = []
    enden: List[float] = []

    for e in schlange.get("einheiten", []):
        if e.get("dauer") is None:
            unbelegt.append({"ware": e["ware"], "stufe": e["stufe"]})
            continue
        start = e.get("start")
        ende = e.get("ende")
        if start is None or ende is None:          # kein Platz geplant (Kapazitaet 0)
            wartend.append({"ware": e["ware"], "stufe": e["stufe"]})
            continue
        enden.append(float(ende))
        if start <= t < ende:
            laeuft.append({"ware": e["ware"], "stufe": e["stufe"],
                           "start": start, "ende": ende,
                           "rest_sekunden": round(ende - t, 3)})
        elif ende <= t:
            fertig.append({"ware": e["ware"], "stufe": e["stufe"], "ende": ende})
        else:
            wartend.append({"ware": e["ware"], "stufe": e["stufe"]})

    if unbelegt:
        rest: Optional[float] = None
        hinweis = "Dauer nicht belegt"
    else:
        rest = round(max(0.0, (max(enden) - t) if enden else 0.0), 3)
        hinweis = ""

    return {
        "typ": schlange.get("typ"),
        "werkstatt": schlange.get("werkstatt"),
        "kapazitaet": schlange.get("kapazitaet", 0),
        "zeit": t,
        "laeuft": laeuft,
        "fertig": fertig,
        "fertig_anzahl": len(fertig),
        "wartend": wartend,
        "unbelegt": unbelegt,
        "rest_sekunden": rest,
        "hinweis": hinweis,
        "text": _fortschritt_text(schlange.get("werkstatt"), laeuft, fertig, wartend,
                                  unbelegt, rest),
    }


def _fortschritt_text(werkstatt: Any, laeuft, fertig, wartend, unbelegt,
                      rest: Optional[float]) -> str:
    teile = [f"Werkstatt {werkstatt}"]
    if laeuft:
        teile.append(f"in Arbeit: {len(laeuft)}")
    teile.append(f"fertig: {len(fertig)}")
    if wartend:
        teile.append(f"wartend: {len(wartend)}")
    if unbelegt:
        teile.append(f"ohne belegte Dauer: {len(unbelegt)} (Dauer nicht belegt)")
    if rest is None:
        teile.append("Restzeit nicht berechenbar - Dauer nicht belegt")
    else:
        teile.append(f"Restzeit {rest / 60.0:.1f} Minuten")
    return " | ".join(teile)


def fertige_waren(schlange: Dict[str, Any], jetzt: float) -> Dict[str, int]:
    """{ware: menge} - was SEIT dem letzten Aufruf fertig geworden ist."""
    t = _fortschreiben(schlange, jetzt)
    neu: Dict[str, int] = {}
    for e in schlange.get("einheiten", []):
        if e.get("dauer") is None or e.get("ende") is None:
            continue
        if e["ende"] <= t and not e.get("gemeldet"):
            e["gemeldet"] = True
            neu[e["ware"]] = neu.get(e["ware"], 0) + 1
    return neu


# --------------------------------------------------------------------------
# 5. Siedlungskarte: die gebauten Werkstaetten (wie gebaeude_wirkung.py)
# --------------------------------------------------------------------------

def _feld(objekt, name, vorgabe=None):
    if isinstance(objekt, dict):
        return objekt.get(name, vorgabe)
    return getattr(objekt, name, vorgabe)


def werkstaetten_bestand(siedlungen) -> Dict[str, int]:
    """{kennung: anzahl} der gebauten Werkstaetten ueber alle Siedlungskarten."""
    zaehlung: Dict[str, int] = {k: 0 for k in werkstaetten()}
    for siedlung in siedlungen or []:
        for _feldindex, gebaut in (_feld(siedlung, "bauten") or {}).items():
            kennung = gelaende.finde_gebaeude(gebaut)
            if kennung in zaehlung:
                zaehlung[kennung] += 1
    return zaehlung


def werkstatt_stufe(siedlung, typ: str) -> int:
    """Hoechste Ausbaustufe einer Werkstatt in EINER Siedlung (0 = nicht gebaut)."""
    kennung = _werkstatt_kennung(typ)
    if not kennung:
        return 0
    stufen = _feld(siedlung, "stufen") or {}
    beste = 0
    for feldindex, gebaut in (_feld(siedlung, "bauten") or {}).items():
        if gelaende.finde_gebaeude(gebaut) == kennung:
            try:
                beste = max(beste, int(stufen.get(str(feldindex), 1)))
            except (TypeError, ValueError):
                beste = max(beste, 1)
    return beste


# --------------------------------------------------------------------------
# 6. Lager: lesbare Bestandszeile
# --------------------------------------------------------------------------

def lager_text(bestand: Dict[str, Any]) -> str:
    """Eine lesbare Zeile des Warenbestands im Lager (Handbuch Seite 14)."""
    if not bestand:
        return "Lager: leer"
    teile: List[str] = []
    for ware in sorted(bestand):
        try:
            menge = int(bestand[ware])
        except (TypeError, ValueError):
            continue
        if menge > 0:
            teile.append(f"{menge} {ware}")
    if not teile:
        return "Lager: leer"
    return "Lager: " + ", ".join(teile)

```

### Datei `src/kampfbericht.py` (492 Zeilen)

```python
"""
Nebelseetal Remake - Kampfbericht (Paket W2b, 04.10.2026).

Ergaenzt den fertigen Kampfablauf (`src/kampf.py`) um die vier Teile des Handbuchs
(Seiten 20-23), die dort noch keine eigene, einzeln pruefbare Funktion hatten:

  1. Vorrunde      - erreicht die Schlagkraft der Fusstruppen (ab der verstaerkten Palisade,
                     Stufe 5, zusaetzlich die der Belagerungswaffen) die Schwelle des Walls?
                     Eine beschaedigte Mauer verlangt prozentual weniger.
  2. Mauerschaden  - je Belagerungswaffe ein Zufallswert aus ihrem Schadensbereich minus
                     Ausbaustufe der Mauer, vom Zustand der Mauer abgezogen.
  3. Beute         - nur so viel, wie die Karren wirklich tragen koennen.
  4. Bericht       - der Schlachtbericht fuer den Reiter 'Nachrichten'.

Es wird NICHTS erfunden: die Schwellen kommen aus `gebaeude_wirkung.wall_schwelle`,
Mauerschaden und Ladung aus `einheiten` / `data/units.json`. Wo das Handbuch schweigt,
steht das in `offene_luecken()` und im Code als ANNAHME gekennzeichnet.

Alle Funktionen sind rein: kein globaler Zustand, keine Datei wird geschrieben oder
veraendert; `spieldaten_anwenden` gibt einen NEUEN Zustand zurueck.

`kampf.py` wird NICHT nachgebaut - die Schlacht selbst bleibt dort. Dieses Modul nimmt
deren Ergebnis entgegen und bereitet es auf.
"""
from __future__ import annotations

import copy
import random
from typing import Any, Dict, Optional, Tuple

import einheiten as E
import gebaeude_wirkung as GW

STAND = "2026-10-04.1"

# ANNAHME: Das Handbuch nennt in der Vorrunde den Begriff "Fußtruppen", definiert ihn aber
# nicht. Diese Funktionen bekommen die fertige Schlagkraft uebergeben; welche Einheiten das
# sind, entscheidet der Aufrufer (in `kampf.py` sind es Nahkampf UND Fernkampf). Die engere
# Lesart (nur Nahkampf) ist damit nicht ausgeschlossen und steht in `offene_luecken()`.

AUSGANG_TEXT = {
    "angreifer": "Der Angreifer siegt",
    "verteidiger": "Der Verteidiger siegt",
    "unentschieden": "Unentschieden",
}


def _als_zahl(wert: Any, vorgabe: float = 0.0) -> float:
    """Nimmt Zahlen, Numerisches-als-Text und None; Unbrauchbares wird zur Vorgabe."""
    if wert is None:
        return float(vorgabe)
    try:
        return float(wert)
    except (TypeError, ValueError):
        return float(vorgabe)


def _als_int(wert: Any, vorgabe: int = 0) -> int:
    try:
        return int(float(wert))
    except (TypeError, ValueError):
        return int(vorgabe)


def _schwelle_wall(wall_stufe: int) -> Dict[str, Optional[int]]:
    """Die belegten Schwellenwerte einer Wallstufe (aus `gebaeude_wirkung`)."""
    if int(wall_stufe) < 1:
        return {"fusstruppen": None, "belagerungswaffen": None}
    return GW.wall_schwelle(int(wall_stufe))


# ---------------------------------------------------------------------------- 1. Vorrunde

def vorrunde(angreifer_fussttruppen_sk: float,
             angreifer_belagerung_sk: float,
             wall_stufe: int,
             wall_zustand_prozent: float = 100.0) -> Dict[str, Any]:
    """Prueft die Vorrunde nach Handbuch Seite 20/21.

    `wall_zustand_prozent` ist optional und stand nicht im geforderten Aufruf; ohne Angabe
    gilt der volle Zustand (100 %). Eine beschaedigte Mauer verlangt laut Handbuch
    "prozentual weniger" Schlagkraft - der Faktor ist Zustand/100.

    Rueckgabe:
      {'bestanden': bool, 'schwelle': {...}, 'grund': text}
      schwelle = {
        'fusstruppen':        {'nennwert', 'erforderlich', 'vorhanden', 'erreicht'},
        'belagerungswaffen':  {'nennwert', 'erforderlich', 'vorhanden', 'erreicht'|None},
        'wall_stufe', 'wall_name', 'wall_zustand_prozent', 'faktor',
      }
    """
    stufe = int(wall_stufe)
    zustand = _als_zahl(wall_zustand_prozent, 100.0)
    faktor = max(0.0, zustand) / 100.0
    fuss_sk = _als_zahl(angreifer_fussttruppen_sk)
    bel_sk = _als_zahl(angreifer_belagerung_sk)

    werte = _schwelle_wall(stufe)
    fuss_nenn = werte.get("fusstruppen")
    bel_nenn = werte.get("belagerungswaffen")

    schwelle: Dict[str, Any] = {
        "fusstruppen": {"nennwert": fuss_nenn, "erforderlich": None,
                        "vorhanden": fuss_sk, "erreicht": None},
        "belagerungswaffen": {"nennwert": bel_nenn, "erforderlich": None,
                              "vorhanden": bel_sk, "erreicht": None},
        "wall_stufe": stufe,
        "wall_name": GW.wall_name(stufe) if stufe >= 1 else None,
        "wall_zustand_prozent": zustand,
        "faktor": faktor,
    }

    if stufe < 1 or fuss_nenn is None:
        grund = ("Kein Wall vorhanden - die Vorrunde entfaellt, der Angreifer kann "
                 "vorruecken.")
        if stufe >= 1 and fuss_nenn is None:
            grund = (f"Fuer Wallstufe {stufe} nennt das Handbuch keine Schwelle - "
                     "die Vorrunde entfaellt (kein Wert erfunden).")
        return {"bestanden": True, "schwelle": schwelle, "grund": grund}

    fuss_erf = float(fuss_nenn) * faktor
    fuss_ok = fuss_sk >= fuss_erf
    schwelle["fusstruppen"]["erforderlich"] = fuss_erf
    schwelle["fusstruppen"]["erreicht"] = fuss_ok

    if bel_nenn is None:
        bel_erf = None
        bel_ok: Optional[bool] = None
    else:
        bel_erf = float(bel_nenn) * faktor
        bel_ok = bel_sk >= bel_erf
        schwelle["belagerungswaffen"]["erforderlich"] = bel_erf
        schwelle["belagerungswaffen"]["erreicht"] = bel_ok

    if not fuss_ok:
        grund = (f"Die Schlagkraft der Fusstruppen {fuss_sk:.0f} erreicht die Schwelle "
                 f"{fuss_erf:.0f} nicht - Rueckzug, keine Beute.")
        bestanden = False
    elif bel_ok is False:
        grund = (f"Fusstruppen erreichen die Schwelle {fuss_erf:.0f}, aber die Schlagkraft "
                 f"der Belagerungswaffen {bel_sk:.0f} erreicht {bel_erf:.0f} nicht - "
                 "Rueckzug, keine Beute.")
        bestanden = False
    else:
        teile = [f"Fusstruppen {fuss_sk:.0f} >= {fuss_erf:.0f}"]
        if bel_erf is not None:
            teile.append(f"Belagerungswaffen {bel_sk:.0f} >= {bel_erf:.0f}")
        grund = "Vorrunde bestanden (" + ", ".join(teile) + ")."
        bestanden = True

    return {"bestanden": bestanden, "schwelle": schwelle, "grund": grund}


# ------------------------------------------------------------------------ 2. Mauerschaden

def mauer_schaden(belagerung: Dict[str, int],
                  wall_stufe: int,
                  wall_zustand_prozent: float,
                  rng: Optional[random.Random] = None) -> Dict[str, Any]:
    """Mauerschaden nach Handbuch Seite 21/22.

    Je mitgefuehrter Belagerungswaffe wird EINZELN gewuerfelt: Zufallswert im Schadensbereich
    der Waffe minus Ausbaustufe der Mauer; ein positiver Rest geht vom Zustand ab. Der
    Zustand faellt nie unter 0 %.

    Rueckgabe:
      {'mauer_zustand_prozent', 'vorher_prozent', 'schaden_gesamt',
       'wall_stufe', 'je_waffe': {name: {'anzahl', 'wuerfe', 'rest', 'schaden'}}}
    """
    rng = rng or random.Random()
    stufe = int(wall_stufe)
    vorher = max(0.0, _als_zahl(wall_zustand_prozent, 100.0))

    je_waffe: Dict[str, Dict[str, Any]] = {}
    gesamt = 0
    for name, anzahl in (belagerung or {}).items():
        n = max(0, _als_int(anzahl))
        lo, hi = E.mauer_schaden(name)
        wuerfe, rest = [], []
        for _ in range(n):
            wurf = rng.randint(int(lo), int(hi))
            r = max(0, int(wurf) - stufe)
            wuerfe.append(int(wurf))
            rest.append(int(r))
            gesamt += int(r)
        if name not in je_waffe:
            je_waffe[name] = {"anzahl": n, "wuerfe": wuerfe, "rest": rest,
                              "schaden": sum(rest)}

    neu = max(0.0, vorher - gesamt)
    return {
        "mauer_zustand_prozent": neu,
        "vorher_prozent": vorher,
        "schaden_gesamt": gesamt,
        "wall_stufe": stufe,
        "je_waffe": je_waffe,
    }


# ------------------------------------------------------------------------------ 3. Beute

# VORGABE DANIEL 31.10.2026 (Registerpunkt 45): Die Beute wird GESTAFFELT, nicht pauschal.
# Belegt ist nur: "nur Transportkarren pluendern" (Handbuch S. 23) und "Beute ist durch die
# Ladung begrenzt". Die Prozentwerte sind VORSCHLAG und werden im Spieltest balanciert.
# Reihenfolge der Pruefung: keine Verteidiger > Wall gebrochen > Wall beschaedigt > Wall heil.
BEUTE_STAFFEL_PROZENT: Dict[str, int] = {
    "keine_verteidiger": 100,   # niemand verteidigt mehr -> der ganze Bestand darf mit
    "mauer_gebrochen": 60,      # Wall war beim Angriff schon bei 0 Prozent
    "mauer_beschaedigt": 30,    # Wall bereits (teilweise) eingerissen
    "mauer_heil": 10,           # erster erfolgreicher Angriff, Wall steht noch
}


def beute_lage(wall_zustand_vor: Any, verteidiger_uebrig: Any) -> str:
    """Welche Lage gilt fuer die Staffelung? (VORGABE Daniel, Prozentwerte VORSCHLAG)

    Keine Verteidiger mehr -> 'keine_verteidiger'; Wall bei 0 -> 'mauer_gebrochen';
    Wall unter 100 (aber ueber 0) -> 'mauer_beschaedigt'; sonst 'mauer_heil'.
    Unbekannte Angaben (None) gelten als "Wall heil, Verteidiger vorhanden" - der
    vorsichtigste Fall, damit nichts verschenkt wird.
    """
    if verteidiger_uebrig is not None:
        try:
            if int(verteidiger_uebrig) <= 0:
                return "keine_verteidiger"
        except (TypeError, ValueError):
            pass
    zustand = _als_zahl(wall_zustand_vor, 100.0)
    if zustand <= 0.0:
        return "mauer_gebrochen"
    if zustand < 99.5:          # alles unter "unversehrt" gilt als eingerissen
        return "mauer_beschaedigt"
    return "mauer_heil"


def beute_staffel(einheiten_des_siegers: Dict[str, int],
                  vorraete: Dict[str, float],
                  wall_zustand_vor: Any = None,
                  verteidiger_uebrig: Any = None) -> Dict[str, int]:
    """Beute nach Daniels Staffelung (Registerpunkt 45).

    Anteil = BEUTE_STAFFEL_PROZENT[beute_lage(...)], zusaetzlich begrenzt durch
      * die Gesamtladung der mitgefuehrten Karren und
      * den tatsaechlich vorhandenen Vorrat je Rohstoff.
    Die Verteilung auf die Rohstoffe ist anteilig nach Vorratsmenge (das Handbuch
    regelt die Aufteilung nicht).

    Beispiele (Vorschlagswerte): Wall heil, 1.000 je Rohstoff, Handkarren (Ladung 40)
    -> 10 Prozent = 100, aber nur 40 passen hinein. Ohne Verteidiger -> 100 Prozent,
    begrenzt durch Ladung. Kein Karren -> keine Beute (belegt).
    """
    kapazitaet = 0
    for name, anzahl in (einheiten_des_siegers or {}).items():
        kapazitaet += E.kapazitaet(name, max(0, _als_int(anzahl)))
    if kapazitaet <= 0:
        return {}

    vorhanden: Dict[str, int] = {}
    for stoff, menge in (vorraete or {}).items():
        m = int(max(0.0, _als_zahl(menge)))
        if m > 0:
            vorhanden[stoff] = m
    gesamt = sum(vorhanden.values())
    if gesamt <= 0:
        return {}

    anteil = BEUTE_STAFFEL_PROZENT[beute_lage(wall_zustand_vor, verteidiger_uebrig)] / 100.0
    # Anteilig heisst: gegen die WIRKLICH mitnehmbare Menge rechnen, nicht gegen die ideale.
    # Bisher stand hier `int(anteil_stoff * ziel_menge)` und danach ein Deckel `restplatz` -
    # dadurch frass der alphabetisch erste Rohstoff die ganze Ladung (Befund 31.10.2026 aus
    # `test_kampf_einhaengung`: erwartet Holz 50 / Stein 30, geliefert Holz 80 / Stein 0).
    ziel = min(kapazitaet, int(gesamt * anteil))
    if ziel <= 0:
        return {}
    genommen: Dict[str, int] = {}
    for stoff in sorted(vorhanden):
        nimm = min(int(vorhanden[stoff] / gesamt * ziel), vorhanden[stoff])
        if nimm > 0:
            genommen[stoff] = nimm
    # Rest, der durch das Abrunden liegen bleibt, nach dem groessten Bestand auffuellen -
    # nie ueber den vorhandenen Vorrat hinaus. So ist die Summe exakt und die Verteilung fair.
    rest = ziel - sum(genommen.values())
    for stoff in sorted(vorhanden, key=lambda s: (-vorhanden[s], s)):
        if rest <= 0:
            break
        platz = vorhanden[stoff] - genommen.get(stoff, 0)
        nimm = min(rest, platz)
        if nimm > 0:
            genommen[stoff] = genommen.get(stoff, 0) + nimm
            rest -= nimm
    return genommen


def beute_am_ziel(einheiten_des_siegers: Dict[str, int],
                  vorraete: Dict[str, float],
                  ausgang: Any = "angreifer",
                  wall_zustand_vor: Any = None,
                  verteidiger_uebrig: Any = None) -> Tuple[Dict[str, int], Dict[str, float]]:
    """Beute berechnen UND beim Ziel abbuchen - Rueckgabe (beute, vorraete_danach).

    Warum es diese Funktion gibt (Befund der externen Gegenpruefung, 31.10.2026, Nr. 6):
    Der Auftrags-Pfad schrieb die Beute dem Spieler gut, ohne sie beim Ziel abzuziehen -
    Gueter aus dem Nichts. Der Bot-Pfad zog ab, rechnete die Menge aber mit einer anderen
    Formel (`kampf._beute`: nur Ladungsgrenze). Jetzt gilt an EINER Stelle:

      * Beute nur bei Angreifersieg (belegt: Handbuch S. 23, Z. 1307-1315),
      * der Anteil kommt aus `beute_staffel` (Wallzustand VOR dem Kampf, ueberlebende
        Verteidiger, Ladung, vorhandener Vorrat),
      * was gutgeschrieben wird, wird beim Ziel abgebucht; kein Bestand wird negativ.
    """
    lager: Dict[str, float] = {}
    for stoff, menge in (vorraete or {}).items():
        wert = _als_zahl(menge)
        lager[str(stoff)] = max(0.0, wert)

    if str(ausgang or "") != "angreifer":
        return {}, lager

    beute_werte = dict(beute_staffel(einheiten_des_siegers, lager,
                                    wall_zustand_vor=wall_zustand_vor,
                                    verteidiger_uebrig=verteidiger_uebrig))
    for stoff, menge in beute_werte.items():
        lager[stoff] = round(max(0.0, lager.get(stoff, 0.0) - float(menge)), 2)
    return beute_werte, lager


def beute(einheiten_des_siegers: Dict[str, int],
          vorraete: Dict[str, float],
          rng: Optional[random.Random] = None) -> Dict[str, int]:
    """Was die Karren des Siegers tragen koennen (Handbuch Seite 22/23).

    Nur Transporteinheiten (Karren) tragen; Belagerungswaffen und Kaempfer tragen nichts.
    Die Beute ist ehrlich begrenzt: sie ueberschreitet weder die Gesamtkapazitaet der Karren
    noch den vorhandenen Vorrat je Rohstoff.

    ANNAHME zur Verteilung: Das Handbuch begrenzt die Beute auf die Karrenladung, nennt aber
    keine Aufteilung auf die Rohstoffe. Hier wird anteilig nach Vorratsmenge verladen
    (dieselbe Regel wie in `kampf.py.ergebnis['beute']`). `rng` wird angenommen, aber nicht
    gebraucht - die Aufteilung ist bewusst nachvollziehbar und nicht zufaellig.
    """
    del rng  # bewusst ungenutzt: die Verteilung ist nicht im Handbuch geregelt -> anteilig

    kapazitaet = 0
    for name, anzahl in (einheiten_des_siegers or {}).items():
        kapazitaet += E.kapazitaet(name, max(0, _als_int(anzahl)))

    vorhanden: Dict[str, int] = {}
    for stoff, menge in (vorraete or {}).items():
        m = int(max(0.0, _als_zahl(menge)))
        if m > 0:
            vorhanden[stoff] = m

    gesamt = sum(vorhanden.values())
    if kapazitaet <= 0 or gesamt <= 0:
        return {}

    genommen: Dict[str, int] = {}
    restplatz = kapazitaet
    for stoff in sorted(vorhanden):
        if restplatz <= 0:
            break
        anteil = vorhanden[stoff] / gesamt
        nimm = min(int(anteil * kapazitaet), vorhanden[stoff], restplatz)
        if nimm > 0:
            genommen[stoff] = nimm
            restplatz -= nimm
    return genommen


# ---------------------------------------------------------------------------- 4. Bericht

def _aufzaehlung(werte: Dict[str, int]) -> str:
    teile = [f"{name} {int(_als_zahl(anzahl))}" for name, anzahl in sorted((werte or {}).items())]
    return ", ".join(teile) if teile else "keine"


def bericht(ergebnis: Dict[str, Any]) -> Dict[str, str]:
    """Baut den Schlachtbericht fuer den Reiter 'Nachrichten'.

    Nimmt das Ergebnis aus `kampf.fuehre_schlacht` entgegen und liefert:
      {'titel': str, 'zeilen': [str, ...], 'typ': 'kampf'}
    Es wird nichts erfunden: fehlen Felder, werden sie uebergangen.
    """
    e = ergebnis or {}
    ausgang = str(e.get("ausgang", "unentschieden"))
    ausgang_text = AUSGANG_TEXT.get(ausgang, ausgang)
    titel = "Schlachtbericht: " + ausgang_text

    zeilen = [f"Ausgang: {ausgang_text}."]
    if "mauer_zustand" in e:
        zeilen.append(f"Mauerzustand danach: {_als_zahl(e.get('mauer_zustand')):.0f} %.")
    zeilen.append("Verluste Angreifer: " + _aufzaehlung(e.get("verluste_angreifer") or {}))
    zeilen.append("Verluste Verteidiger: " + _aufzaehlung(e.get("verluste_verteidiger") or {}))

    if e.get("geflohen"):
        zeilen.append("Geflohen: " + ", ".join(str(x) for x in e["geflohen"]) + ".")

    beute_ = e.get("beute") or {}
    if beute_:
        zeilen.append("Beute: " + _aufzaehlung(beute_) + ".")
    else:
        zeilen.append("Beute: keine.")

    if e.get("geraete_verloren"):
        zeilen.append("Vom Angreifer zurueckgelassen: " +
                      ", ".join(str(x) for x in e["geraete_verloren"]) + ".")
    if e.get("geraete_verloren_verteidiger"):
        zeilen.append("Vom Verteidiger zurueckgelassen: " +
                      ", ".join(str(x) for x in e["geraete_verloren_verteidiger"]) + ".")

    if e.get("unsicher"):
        zeilen.append("Offene Punkte: " + " ".join(str(x) for x in e["unsicher"]))

    for z in str(e.get("bericht") or "").split("\n"):
        if z.strip():
            zeilen.append(z.rstrip())

    return {"titel": titel, "zeilen": zeilen, "typ": "kampf"}


# ------------------------------------------------------------------ 5. Spieldaten anwenden

def spieldaten_anwenden(zustand_vorher: Dict[str, Any],
                        ergebnis: Dict[str, Any]) -> Dict[str, Any]:
    """Wendet ein Schlachtergebnis auf den Spielstand an und gibt einen NEUEN Stand zurueck.

    Der Stand gehoert dem ANGREIFER (der den Bericht liest):
      * gefundene Beute kommt zu `ressourcen`,
      * die eigenen Verluste (`verluste_angreifer`) und zurueckgelassene Geraete
        (`geraete_verloren`) gehen von `einheiten` ab,
      * der `mauer_zustand` wird als `wall_zustand_prozent` uebernommen.

    Erwartet: {'ressourcen': {stoff: menge}, 'einheiten': {name: anzahl}, ...}
    Der Eingabestand wird NICHT veraendert (tiefe Kopie).
    """
    neu = copy.deepcopy(zustand_vorher) if zustand_vorher else {}
    if not isinstance(neu.get("ressourcen"), dict):
        neu["ressourcen"] = {}
    if not isinstance(neu.get("einheiten"), dict):
        neu["einheiten"] = {}

    e = ergebnis or {}

    for stoff, menge in (e.get("beute") or {}).items():
        alt = neu["ressourcen"].get(stoff, 0) or 0
        neu["ressourcen"][stoff] = alt + int(_als_zahl(menge))

    verluste: Dict[str, int] = dict(e.get("verluste_angreifer") or {})
    for einheit in (e.get("geraete_verloren") or []):
        verluste[einheit] = _als_int(verluste.get(einheit, 0)) + 1

    for einheit, anzahl in verluste.items():
        alt = _als_int(neu["einheiten"].get(einheit, 0))
        neu["einheiten"][einheit] = max(0, alt - _als_int(anzahl))

    if "mauer_zustand" in e:
        neu["wall_zustand_prozent"] = _als_zahl(e.get("mauer_zustand"))

    return neu


# ------------------------------------------------------------------------ 6. Offene Luecken

def offene_luecken() -> Dict[str, str]:
    """Was das Handbuch zum Kampf nicht sagt - ehrliche Liste, kein erfundener Wert."""
    return {
        "fusstruppen_begriff":
            "Der Begriff 'Fußtruppen' der Vorrunde ist im Handbuch nicht definiert. "
            "kampf.py zaehlt Nahkampf- UND Fernkampfeinheiten dazu; die engere Lesart "
            "(nur Nahkampf) ist nicht ausgeschlossen.",
        "flucht_formel":
            "Zum Fliehen unter LE 5 nennt das Handbuch nur 'je niedriger der MU, desto "
            "wahrscheinlicher', aber keine Formel.",
        "beute_verteilung":
            "Die Beute ist auf die Karrenladung begrenzt, eine Aufteilung auf die Rohstoffe "
            "ist nicht geregelt. Hier gilt: anteilig nach Vorratsmenge.",
        "beute_reihenfolge":
            "In welcher Reihenfolge Rohstoffe verladen werden, ist nicht geregelt "
            "(hier alphabetisch).",
        "belagerungsturm_mauerschaden":
            "Belagerungsturm und Grosser Belagerungsturm haben Mauerschaden 0-0: sie brechen "
            "keine Mauer, tragen aber Schlagkraft zur Vorrunde bei.",
        "mauer_reparatur":
            "Ob und wie sich eine beschaedigte oder eroberte Mauer erholt, sagt das Handbuch "
            "nicht.",
        "vorrunde_wiederholung":
            "Wie viele Versuche ein Angreifer gegen den Wall hat, ist offen.",
        "geraetebeute":
            "Ob erbeutete Karren und Belagerungswaffen mitgenommen werden koennen, ist nicht "
            "geregelt.",
    }

```


## Ausgabeformat (genau so, nichts anderes)

### 1. Befund in fünf Sätzen
Was ist hier wirklich das Problem — mit Zahlen aus dem Code.

### 2. Vorschläge (Tabelle, absteigend nach Nutzen)

| # | Was | Dateien/Funktionen | Zeilen vorher → nachher | Risiko (klein/mittel/groß) | Beweis: welche Prüfdatei | Reihenfolge |
|---|---|---|---|---|---|---|

### 3. Zusammenführung im Detail
Für die zwei wichtigsten Vorschläge: welche Funktionen verschmelzen zu welcher neuen Funktion,
welche Parameter, welcher Rückgabewert, was passiert mit Sonderfällen. Kein vollständiger Code —
nur Signatur plus drei bis fünf Zeilen Kern.

### 4. Was du NICHT anfassen würdest
Und warum. (Beispiel: Zeichencode der Oberfläche, der auf Pixel wirkt.)

### 5. Ordnung
Wie sähe eine saubere Ordner-/Dateistruktur für diesen Teil aus? Namen der Dateien, was in welche
gehört, und **in welcher Reihenfolge man umzieht, ohne dass Importe brechen**.
