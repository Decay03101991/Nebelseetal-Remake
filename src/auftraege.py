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
    Geschwindigkeit-Formel, nur Beispielstunden),
  * die Dauer der Handlung am Ziel AKTION_DAUER_SEKUNDEN = 0,
  * der Beute-Anteil BEUTE_ANTEIL_PROZENT = 50 (der Entwurf nennt ihn selbst VORSCHLAG),
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

# VORSCHLAG: Das Handbuch nennt keine Formel aus Entfernung und Geschwindigkeit; es nennt
# nur Beispielstunden (S. 19). Hier gilt: 1 Entfernungseinheit bei Geschwindigkeit 1
# dauert eine Stunde (3600 s). Grund: die Beispielangaben des Handbuchs rechnen in Stunden.
SEKUNDEN_JE_FELD = 3600.0

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


def _schlagkraft_fussttruppen(bestand: Dict[str, int]) -> float:
    """Kampf- UND Kundschaftereinheiten (VORSCHLAG, siehe offene_luecken)."""
    return float(sum(E.angriff(n) * k for n, k in bestand.items() if E.ist_kaempfer(n)))


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


def starten(liste: Optional[List[Dict[str, Any]]], art: str, einheiten: Any,
            von: Any, nach: Any, entfernung: Any, jetzt: Any,
            fracht: Any = None) -> Tuple[bool, str]:
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
            if not vr.get("bestanden"):
                return False, str(vr.get("grund") or "Die Vorrunde wurde nicht bestanden.")
            zusatz["vorrunde"] = vr
            if isinstance(ziel.get("vorraete"), dict):
                zusatz["beute"] = KB.beute(bestand, ziel["vorraete"])

    ok_fracht, meld_fracht, saubere_fracht = _pruefe_fracht(fracht, ladung)
    if not ok_fracht:
        return False, meld_fracht

    reisezeit = reisezeit_sekunden(entf, gs)
    start = _als_zahl(jetzt)
    ankunft = start + reisezeit
    abreise = ankunft + AKTION_DAUER_SEKUNDEN
    rueckkehr = abreise + reisezeit * (HIN_UND_RUECK_FAKTOR - 1.0)

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
        "kosten": {},                     # VORSCHLAG: keine belegten Reisekosten
        "beute": dict(zusatz.get("beute") or {}),
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
    return True, (f"Auftrag '{art}' von {start_name} nach {ziel_name} gestartet "
                  f"(Reisezeit {reisezeit / 3600.0:.2f} h je Strecke, "
                  f"Rueckkehr nach {rueckkehr / 3600.0:.2f} h).")


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
            "Reisekosten (Gold/Nahrung/Mana) sind hier leer gelassen: das Handbuch nennt "
            "sie, beziffert sie aber nicht je Auftrag. Es wird kein Wert erfunden.",
        "handel_gold":
            "Beim Handeln ist kein Goldpreis erfunden. Ohne Feld 'gold_bietet' am Ziel "
            "gibt es 0 Gold; eine Ablehnung bringt die Waren zurueck (S. 20).",
        "beute_ohne_karren":
            "BELEGT (S. 23): Beute gibt es nur mit Transportkarren. Ohne Karren bleibt die "
            "Beute leer, auch wenn Vorraete uebergeben werden.",
    }
