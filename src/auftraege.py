"""
Nebelseetal Remake - Auftraege und Missionen (Paket WA, 04.10.2026).

Ein Auftrag ist eine Reise einer Einheitengruppe von der eigenen Siedlung zu einem
Ziel und (in der Regel) wieder zurueck. Dieses Modul fuehrt die Auftragsliste, die
Reisezeiten und die Auswertung. Den Kampf selbst baut es NICHT nach: fuer den Angriff
wird `kampfbericht.vorrunde` benutzt, fuer die Beute `kampfbericht.beute`.

BELEGT (docs/ENTWURF_AUFTRAEGE.md, Handbuch 2009, Fanpage 2007):
  * fuenf Auftragsarten - stationieren, transportieren, handeln, angreifen und (seit
    02.11.2026, Stufe B-5) spionieren,
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
  * Spionage (Fanpage 2007, Auftraege.html): ein Bericht nennt Karte, Ressourcen und
    stationierte Einheiten eines fremden Dorfes; schnelle Einheiten machen Spione schneller.
    Reisende sind die Kundschafter der Diebesgilde (data/units.json, Kategorie Kundschafter);
    wieviel ein Bericht aufdeckt, rechnet `spionage.aufklaerungswert` aus ihren Werten
    SI (Sinnesschaerfe) und HE (Heimlichkeit) - Vorgabe Daniel 02.11.2026.

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
import hilfen
import spionage as SP   # B-5: Aufklaerungswert aus den Werten der Spionageeinheiten

STAND = "2026-10-04.1"

# Die belegten Auftragsarten (docs/ENTWURF_AUFTRAEGE.md, Tabelle) plus die am 02.11.2026 von Daniel
# beauftragte fuenfte Art 'spionieren' (Stufe B-5, Postfach und Spionage).
AUFTRAGSARTEN: Tuple[str, ...] = ("stationieren", "transportieren", "handeln", "angreifen",
                                  "spionieren")

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

# Die Umrechner standen hier UND in `kampfbericht.py` doppelt (Code-Audit 31.10.2026, Befund P3
# Vorschlag 1). Jetzt gibt es eine Fassung an einem Ort: `hilfen.py`. Die privaten Namen bleiben
# als Verweis bestehen, damit der restliche Code dieser Datei unveraendert lesbar ist.
_als_zahl = hilfen.als_zahl
_als_int = hilfen.als_int
_aufzaehlung = hilfen.aufzaehlung


def _ziel_name(nach: Any) -> str:
    if isinstance(nach, dict):
        return str(nach.get("name") or "")
    return str(nach or "")


def _ziel_daten(nach: Any) -> Dict[str, Any]:
    return dict(nach) if isinstance(nach, dict) else {}


def _bestand(einheiten: Any) -> Dict[str, int]:
    """Nimmt {name: anzahl} und liefert nur brauchbare, positive Eintraege.

    Die Filterregel steht seit dem Code-Audit 31.10.2026 in `hilfen.positive_ganze_werte`
    (dieselbe Regel brauchen die Beutefunktionen fuer die Vorraete).
    """
    return hilfen.positive_ganze_werte(einheiten)


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

def reisezeit_sekunden(entfernung: Any, geschwindigkeit: Any, faktor: Any = 1.0) -> float:
    """Dauer EINER Strecke in Sekunden (Handbuch S. 19: die Dauer gilt fuer eine Strecke).

    Formel (VORSCHLAG, siehe offene_luecken['reisezeit_formel']):
        Sekunden = Entfernung / Geschwindigkeit * SEKUNDEN_JE_FELD
    Eine ungueltige (nicht positive) Geschwindigkeit liefert unendlich - der Auftrag
    kann so nicht starten; `starten` weist das vorher ab.

    V-5 (03.11.2026): `faktor` ist der Zeitfaktor aus dem Volk/Taktikboni
    (`boni.reisezeitfaktor`: +5 % schneller = 1/1,05). Ohne Angabe bleibt es bei 1,0 - dann rechnet
    die Funktion genau wie vorher.
    """
    e = max(0.0, _als_zahl(entfernung))
    if e <= 0.0:
        return 0.0
    g = _als_zahl(geschwindigkeit)
    if g <= 0.0:
        return float("inf")
    zeitfaktor = _als_zahl(faktor)
    if zeitfaktor <= 0.0:                                   # kaputter Faktor
        zeitfaktor = 1.0                                   # dann keine Wirkung (kein Erfinden)
    return e / g * SEKUNDEN_JE_FELD * zeitfaktor


def _reise_zeiten(start: Any, reisezeit: Any,
                  aktion_dauer: Any) -> Tuple[float, float, float]:
    """(Ankunft, Abreise, Rueckkehr) - EINE Rechnung fuer `starten` und `_status_zeiten`.

    Vorher rechneten beide Stellen dieselbe Kette getrennt (Code-Audit 31.10.2026, Befund P3
    Vorschlag 3); laufen sie auseinander, zeigt der Bericht andere Zeiten als der Auftrag
    wirklich braucht. Der Rueckweg kostet so viel wie der Hinweg (HIN_UND_RUECK_FAKTOR).
    """
    s = _als_zahl(start)
    r = _als_zahl(reisezeit)
    a = _als_zahl(aktion_dauer)
    ankunft = s + r
    abreise = ankunft + a
    rueck = abreise + r * (HIN_UND_RUECK_FAKTOR - 1.0)
    return ankunft, abreise, rueck


def ladung_der_mission(einheiten: Any, forschung: Any = None) -> int:
    """Gesamte Tragefaehigkeit der mitgefuehrten Karren (MIT Wagenbau-Bonus).

    Nur Transporteinheiten tragen; Kaempfer und Belagerungswaffen tragen nichts. Der Name
    bleibt oeffentlich (main.py, spieloekonomie und Pruefdateien rufen ihn), die Rechnung steht
    seit dem Code-Audit 31.10.2026 an EINER Stelle: `einheiten.ladung_der_gruppe`.
    `forschung` ist die flache Stufenkarte `{Gebiet: Stufe}` - ohne sie rechnet die Ladung OHNE
    Wagenbau-Bonus (Daniels Entscheidung 2, Register 73).
    """
    return E.ladung_der_gruppe(einheiten, forschung)


# ------------------------------------------------------------------------------ Arten

def auftragsarten() -> Dict[str, Dict[str, Any]]:
    """Die fuenf Auftragsarten mit ihren belegten Regeln und ausgewiesenen Vorschlaegen."""
    return {
        "stationieren": {
            "text": "Einheiten in einer eigenen Siedlung absetzen.",
            "belegt": ["In FREMDEN Siedlungen verboten (Handbuch S. 19); Waren nur mit Karren.",
                       "Die Einheiten bleiben danach vor Ort."],
            "vorschlag": ["Erkennung 'fremd' über das Feld 'fremd' am Ziel (siehe offene_luecken)."],
        },
        "transportieren": {
            "text": "Waren mit Karren zu einem Ziel bringen.",
            "belegt": ["Nur Handkarren (40), Einspänner (100), Zweispänner (250) - Ladung aus "
                       "den Einheitentabellen.", "Die Rückkehr ist vorgesehen."],
            "vorschlag": ["Die Handlung am Ziel dauert 0 s (AKTION_DAUER_SEKUNDEN)."],
        },
        "handeln": {
            "text": "Waren mit einer Handelskarawane anbieten.",
            "belegt": ["Nur Handelskarawanen.", "Bei Ablehnung kehrt die Karawane MIT den Waren "
                       "zurück, Gold wird nie übertragen (S. 20)."],
            "vorschlag": ["Kein Goldpreis erfunden: ohne Feld 'gold_bietet' am Ziel gibt es 0 Gold."],
        },
        "angreifen": {
            "text": "Eine fremde Siedlung angreifen.",
            "belegt": ["Wall-Vorrunde, dann Kampfsequenzen (S. 21-22).",
                       "Beute NUR mit Transportkarren (S. 23, wörtlich: 'Transportkarren in "
                       "seiner Angriffstruppe mitführt, beginnen diese die Siedlung zu plündern').",
                       DROSSELUNG_ZITAT],
            "vorschlag": [f"Beute {BEUTE_ANTEIL_PROZENT} % der Lager, gedeckelt durch die "
                          "Karrenladung (Entwurf, noch zu entscheiden)."],
        },
        "spionieren": {
            "text": "Ein fremdes Dorf ausspionieren und einen Bericht ins Postfach legen.",
            "belegt": ["Fanpage 2007 (Auftraege.html): der Spionagebericht nennt Karte, "
                       "Ressourcen und stationierte Einheiten; schnelle Einheiten machen Spione "
                       "schneller.",
                       "Reisende sind die Kundschafter der Diebesgilde (Streuner, Gauner, Dieb, "
                       "Meisterdieb, Kundschafter, Waldlaeufer - data/units.json).",
                       "VORGABE Daniel 02.11.2026: eine Spionage ist es NUR, wenn die gesamte "
                       "Truppenauswahl aus Spionageeinheiten besteht - sonst ist es ein Angriff.",
                       "In ein EIGENES Dorf wird nicht spioniert; Dörfer werden nie eingenommen "
                       "(Vorgabe Daniel 02.11.2026), Spionage ändert keinen Besitz."],
            "vorschlag": ["Wie viel der Bericht aufdeckt, rechnet spionage.aufklaerungswert aus "
                          "den Werten SI und HE der mitgeschickten Spionageeinheiten; die "
                          "Schwellen je Berichtsteil und die Gueltigkeitsfrist stehen in "
                          "data/spionage.json (VORSCHLAG, Handbuch beziffert SI/HE nicht)."],
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
            return False, f"Die Frachtmenge für '{ware}' darf nicht negativ sein.", {}
        if m > 0:
            sauber[str(ware)] = m
    gesamt = sum(sauber.values())
    if gesamt > ladung:
        return (False,
                f"Überladen: {gesamt} Einheiten Fracht passen nicht auf {ladung} Ladeplätze.",
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
            dimensionen_unterschied: Any = 0, forschung: Any = None,
            reise_faktor: Any = 1.0) -> Tuple[bool, str]:
    """Startet einen Auftrag und haengt ihn an `liste`. Liefert (ok, Meldung).

    `nach` ist der Zielname ODER ein Verzeichnis mit Zusatzangaben:
      {'name': str, 'fremd': bool,            # fuer stationieren
       'wall_stufe': int, 'wall_zustand_prozent': float,   # fuer angreifen
       'vorraete': {...},                      # fuer angreifen (Beute)
       'handel_akzeptiert': bool, 'gold_bietet': int}      # fuer handeln
    """
    if not isinstance(liste, list):
        return False, "Keine gültige Auftragsliste übergeben."
    if art not in AUFTRAGSARTEN:
        return False, f"Unbekannte Auftragsart '{art}'. Erlaubt: {', '.join(AUFTRAGSARTEN)}."

    ziel_name = _ziel_name(nach)
    start_name = str(von or "")
    if not start_name or not ziel_name:
        return False, "Start und Ziel müssen benannt sein."
    if start_name == ziel_name:
        return False, "Start und Ziel sind dieselbe Siedlung."

    entf = _als_zahl(entfernung)
    if entf <= 0.0:
        return False, "Die Entfernung muss größer als 0 sein."

    bestand = _bestand(einheiten)
    if not bestand:
        return False, "Der Auftrag braucht mindestens eine Einheit mit Anzahl > 0."
    fremde = _unbekannte(bestand)
    if fremde:
        return False, "Unbekannte Einheit(en): " + ", ".join(fremde) + "."

    gs = _geschwindigkeit(bestand)
    if gs <= 0:
        return False, "Keine mitgeführte Einheit hat eine Geschwindigkeit."

    ziel = _ziel_daten(nach)
    ladung = ladung_der_mission(bestand, forschung)

    # -------------------------------------------------------------- art-spezifische Regeln
    zusatz: Dict[str, Any] = {}
    warnungen: List[str] = []    # Hinweise, die den Auftrag NICHT verhindern (z. B. Wallpruefung)
    if art == "stationieren":
        if ziel.get("fremd"):
            return False, ("Stationieren ist in fremden Siedlungen nicht möglich "
                           "(Handbuch S. 19).")
    elif art == "transportieren":
        if not any(E.ist_transport(n) for n in bestand):
            return False, "Transportieren braucht mindestens einen Karren."
    elif art == "handeln":
        karawanen = [n for n in bestand if "Handelskarawane" in n]
        if not karawanen:
            return False, "Handeln ist nur mit Handelskarawanen möglich."
    elif art == "angreifen":
        fuss = _schlagkraft_fussttruppen(bestand)                            # Angriffskraft Fusstruppen
        bel = _schlagkraft_belagerung(bestand)                               # Angriffskraft Belagerung
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
                    + str(vr.get("grund") or "die Vorrunde würde nicht bestanden.")
                    + " Der Auftrag startet trotzdem; entschieden wird bei Ankunft.")
            if isinstance(ziel.get("vorraete"), dict):
                # VORGABE Daniel 31.10.2026 (Registerpunkt 45): gestaffelte Beute nach Wallzustand
                # und Verteidigern, statt pauschalem Anteil. Werte sind VORSCHLAG.
                zusatz["beute"] = KB.beute_staffel(
                    bestand, ziel["vorraete"],
                    wall_zustand_vor=ziel.get("wall_zustand_prozent"),
                    verteidiger_uebrig=ziel.get("verteidiger_uebrig"),
                    forschung=forschung)
                zusatz["beute_lage"] = KB.beute_lage(
                    ziel.get("wall_zustand_prozent"), ziel.get("verteidiger_uebrig"))
    elif art == "spionieren":
        # B-5 (Vorgabe Daniel 02.11.2026): Spionage reist mit SPIONAGEEINHEITEN - den Kundschaftern
        # der Diebesgilde. Kaempfer und Karren duerfen mit, klaeren aber nichts auf.
        if not ziel.get("fremd"):
            return False, ("Spionage gibt es nur gegen ein FREMDES Dorf - ein eigenes Dorf "
                           "braucht keinen Bericht.")
        kundschafter = SP.spionageeinheiten(bestand)                         # nur Spionageeinheiten
        if not kundschafter:
            return False, ("Spionage braucht Spionageeinheiten - die Kundschafter der "
                           "Diebesgilde (Streuner, Gauner, Dieb, Meisterdieb, Kundschafter, "
                           "Waldläufer).")
        # VORGABE Daniel 02.11.2026: "Eine Spionage ist es nur dann, wenn die gesamte
        # Truppenauswahl nur aus Spionageeinheiten besteht." Also ist eine GEMISCHTE Truppe keine
        # Spionage - sie wird abgelehnt, nicht stillschweigend auf die Kundschafter gekuerzt.
        keine_spione = sorted(n for n in bestand if not E.ist_kundschafter(n))
        if keine_spione:
            return False, ("Spionage geht NUR mit Spionageeinheiten - in der Auswahl stehen: "
                           + ", ".join(keine_spione) + ". Ohne sie ist es ein Angriff, "
                           "keine Spionage.")
        zusatz["aufklaerung"] = SP.aufklaerungswert(kundschafter)            # SI + HE der Truppe
        if zusatz["aufklaerung"] <= 0:
            return False, "Die mitgeschickten Einheiten haben keinen Aufklärungswert."
        # ANALOG zur Wall-Vorrunde (`kampfbericht.vorrunde`) und aus demselben Grund wie die
        # Wallpruefung (Entscheidung Daniel 31.10.2026, Frage 8): die Abwehr des Dorfes kann sich
        # bis zur Ankunft aendern. Beim Absenden wird nur GEWARNT, entschieden wird bei Ankunft.
        abwehr = SP.abwehr_eines_dorfes(ziel.get("wall_stufe"),
                                        ziel.get("wall_zustand_prozent"))
        if zusatz["aufklaerung"] < abwehr:
            warnungen.append(
                "WARNUNG: die Aufklärung (%d) liegt unter der Abwehr des Dorfes (%d) - der "
                "Spionageauftrag kann abprallen. Entschieden wird bei Ankunft."
                % (int(zusatz["aufklaerung"]), int(round(abwehr))))

    ok_fracht, meld_fracht, saubere_fracht = _pruefe_fracht(fracht, ladung)
    if not ok_fracht:
        return False, meld_fracht

    reisezeit = reisezeit_sekunden(entf, gs, reise_faktor)
    start = _als_zahl(jetzt)
    ankunft, abreise, rueckkehr = _reise_zeiten(start, reisezeit, AKTION_DAUER_SEKUNDEN)

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
        # B-5: Aufklaerungswert der mitgeschickten Spionageeinheiten (SI+HE) - 0 fuer alle anderen
        # Arten. Daran entscheidet sich bei Ankunft, ob der Wall ueberwunden wird.
        "aufklaerung": int(zusatz.get("aufklaerung") or 0),
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
               f"Rückkehr nach {rueckkehr / 3600.0:.2f} h).")
    if warnungen:
        meldung += " " + " ".join(warnungen)
    return True, meldung


# ------------------------------------------------------------------------ fortschritt

def _status_zeiten(eintrag: Dict[str, Any]) -> Tuple[float, float, float]:
    return _reise_zeiten(eintrag.get("start"), eintrag.get("reisezeit"),
                         eintrag.get("aktion_dauer"))


def _status(eintrag: Dict[str, Any], jetzt: float) -> Tuple[str, float]:
    ankunft, abreise, rueck = _status_zeiten(eintrag)
    if jetzt < ankunft:
        return "hinreise", ankunft - jetzt
    if jetzt <= abreise:
        return "am_ziel", abreise - jetzt
    if jetzt < rueck:
        return "rueckreise", rueck - jetzt
    return "abgeschlossen", 0.0


def stand(eintrag: Any, jetzt: Any) -> Tuple[str, float]:
    """Phase und Restzeit EINES Auftrags - die oeffentliche Fassung von `_status` (M-1).

    Gebraucht von der Marsch-Anzeige auf der Weltkarte (Registerpunkt 140): dort ist die GROBE
    Restlaufzeit sichtbar, die Phase entscheidet ueber die Richtung der Linie. Reine Rechnung auf
    der Spieluhr (`state.spielsekunden`), keine zweite Zeitbasis.
    """
    return _status(eintrag if isinstance(eintrag, dict) else {}, _als_zahl(jetzt))


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


def laufende(liste: Any, jetzt: Any) -> List[Dict[str, Any]]:
    """Auftraege, die GERADE unterwegs sind (Hinreise, am Ziel oder Rueckreise).

    Quelle der Regel (Daniel 01.11.2026, docs/KONZEPT_SECHS_DOERFER_20261101.md Anhang 2,
    "Umzug mit laufenden Auftraegen"): "ein weltenwechsel ist fuer das dorf gar nicht
    moeglich solange auftraege einheiten truppen oder sonst was unterwegs ist auch handel
    z. b." - Handel laeuft ebenfalls als Auftrag (Art "handel"), deshalb genuegt EINE Liste.

    Abgeschlossene Auftraege zaehlen NICHT. Rueckgabe in Dateireihenfolge, nichts wird
    veraendert (kein `status`-Merker, anders als in `fortschritt`).
    """
    t = _als_zahl(jetzt)
    out: List[Dict[str, Any]] = []
    if not isinstance(liste, list):
        return out
    for e in liste:
        if not isinstance(e, dict):
            continue
        if _status(e, t)[0] != "abgeschlossen":
            out.append(e)
    return out


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
    return hilfen.aufzaehlung(werte)


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
        f"(Rückkehr doppelt so lang, Handbuch S. 19).",
    ]
    if e.get("ladung"):
        zeilen.append(f"Ladeplätze: {int(_als_zahl(e.get('ladung')))}.")
    if e.get("fracht"):
        zeilen.append("Fracht: " + _aufzaehlung(e.get("fracht")) + ".")
    if e.get("beute"):
        zeilen.append("Beute: " + _aufzaehlung(e.get("beute")) + ".")
    if e.get("verluste"):
        # B-5: ein abgewehrter Spionageauftrag verliert Einheiten - die Zeile nennt sie.
        zeilen.append("Verluste: " + _aufzaehlung(e.get("verluste")) + ".")
    if e.get("rueckgut"):
        zeilen.append("Zurückgebracht: " + _aufzaehlung(e.get("rueckgut")) + ".")
    if e.get("art") == "spionieren":
        # B-5: der Bericht des AUFTRAGS nennt die Aufklaerung; der Spionagebericht selbst kommt als
        # eigene Nachricht (spionage.bericht_nachricht) - nur bei ueberwundenem Wall.
        zeilen.append("Aufklärung der Spionageeinheiten: %d." % int(_als_zahl(e.get("aufklaerung"))))
        if e.get("abgewehrt"):
            zeilen.append("Der Wall hat den Auftrag abgewehrt - kein Bericht, die Einheiten sind "
                          "auf dem Rückweg (Verluste siehe Nachricht).")
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
            "(Handbuch S. 20); wie sie die Reisezeit ändert, sagt das Handbuch nicht. "
            "Sie ist hier als Konstante DROSSELUNG_SCHRITTE_PROZENT abgelegt, aber nicht "
            "auf die Formel angewandt.",
        "aktion_dauer":
            f"Die Dauer der Handlung am Ziel ist VORSCHLAG "
            f"(AKTION_DAUER_SEKUNDEN = {AKTION_DAUER_SEKUNDEN:.0f}). Fuer stationieren/"
            "transportieren/angreifen nennt das Handbuch keine Aufenthaltsdauer; handeln "
            "wartet laut Entwurf auf eine Bestaetigung ohne bezifferte Dauer.",
        "beute_anteil":
            f"Der Beute-Anteil ist VORSCHLAG (BEUTE_ANTEIL_PROZENT = {BEUTE_ANTEIL_PROZENT}). "
            "Der Entwurf selbst nennt ihn ausdrücklich offen ('Was Daniel entscheiden "
            "muss', Punkt 3); das Handbuch beziffert die Beutemenge nicht.",
        "geschwindigkeit_wahl":
            "VORSCHLAG: das Tempo des Auftrags ist die langsamste mitgeführte Einheit "
            "(min GS). Das Handbuch nennt keine Regel für gemischte Gruppen.",
        "fusstruppen_begriff":
            "VORSCHLAG: als Angreifer-Fußtruppen zählen Kampf- UND Kundschaftereinheiten "
            "(einheiten.ist_kaempfer). Der Begriff ist im Handbuch nicht definiert.",
        "stationieren_fremd":
            "BELEGT ist das Verbot in fremden Siedlungen (S. 19). WIE ein Ziel als fremd "
            "erkannt wird, sagt das Handbuch nicht; hier entscheidet das Feld 'fremd' am "
            "Ziel. Ein reiner Zielname gilt als eigene Siedlung.",
        "kosten":
            "VORSCHLAG (Paket A2 vom 31.10.2026): Das Handbuch nennt die RICHTUNG der "
            "Reisekosten, aber keine Zahlen ('Gold und Nahrung je nach Einheiten', "
            "Drosselung: weniger Gold und mehr Nahrung, fremdes Ziel: Mana nach Entfernung). "
            "Die drei Sätze in kosten_der_mission (0,1 Gold je Feld und GS-Punkt; "
            "0,1 Nahrung je Feld durch GS; Mana 5 + 0,5 je Feld + 20 je Dimension) sind "
            "ausdrücklich VORSCHLAG und im Spieltest zu balancieren.",
        "handel_gold":
            "Beim Handeln ist kein Goldpreis erfunden. Ohne Feld 'gold_bietet' am Ziel "
            "gibt es 0 Gold; eine Ablehnung bringt die Waren zurück (S. 20).",
        "beute_ohne_karren":
            "BELEGT (S. 23): Beute gibt es nur mit Transportkarren. Ohne Karren bleibt die "
            "Beute leer, auch wenn Vorräte übergeben werden.",
    }
