"""Spieltest-Simulation: laesst das Remake OHNE Fenster spielen und protokolliert den Lauf.

Warum: Ein grosses Modell kann die tkinter-Oberflaeche nicht bedienen. Es kann aber sehr gut
BALANCE und SPIELGEFUEHL beurteilen, wenn es einen echten, nachvollziehbaren Spielverlauf sieht -
Rohstoffe ueber die Zeit, was ein Bau kostet, wann die erste Forschung fertig ist, wie ein Angriff
ausgeht, wie viele Punkte nach X Spieltagen dastehen. Genau das erzeugt dieses Werkzeug:
`docs/audits/SPIELTEST_LOG_<datum>.md`.

Es spielt mit einer einfachen, dokumentierten "Spielerpolitik" (kein Anspruch auf Optimalitaet):
  * alle 20 Spielminuten ein Schritt,
  * zuerst produzierende Gebaeude bauen, dann ausbauen,
  * Forschung starten, wenn bezahlbar,
  * Einheiten ausbilden, wenn Gold und Siedler da sind,
  * ab Spieltag 2 einmal angreifen.

Aufruf:
    python -X utf8 tools/spieltest_simulation.py            # 6 Spieltage
    python -X utf8 tools/spieltest_simulation.py --tage 10
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import random
import re
import subprocess
import sys

HIER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HIER, "src"))

import spielschicht as S            # noqa: E402
import einheiten as E               # noqa: E402
import gelaende as GE              # noqa: E402
import postfach as PF              # noqa: E402  (Ruhm-Stufen: EINE Lesestelle, kein zweiter Leser)

SPIELTAG = 86400                    # Spielsekunden je Tag (Handbuch: 1 Tag = 24 Spielstunden)
SCHRITT = 1200                      # 20 Spielminuten je Schritt
# Reihenfolge der Spielerpolitik. GOLDMINE und eine Ausbildungsstaette gehoeren zwingend
# dazu: ohne Gold gibt es keine Einheit, ohne Ausbildungsstaette keinen Kampf - fehlen sie,
# sieht der Lauf aus wie ein Spielfehler (erster Versuch 31.10.2026 baute 10x Holzfäller).
# Reihenfolge nach der BELEGTEN Kette (nachgemessen 31.10.2026): Holzfäller -> BIBLIOTHEK
# (sonst keine Forschung) -> Forschung Baukunst -> Goldmine/Farm/Kriegerakademie.
# Die Bibliothek gehoert deshalb nach vorn, nicht ans Ende.
GEBAEUDE_REIHENFOLGE = ("holzfäller", "bibliothek", "farm", "goldmine", "kriegerakademie",
                        "schafszucht", "stellmacher", "steinmetz", "erzmine", "jaeger",
                        "schmiede", "naehstube", "haus")
# Befund 05.11.2026: der frueher letzte Eintrag hiess "wohnhaus" - `gelaende.finde_gebaeude`
# kennt nur "haus" und gab None zurueck, das Haus wurde also NIE gebaut (stiller Fehler).
# Ebenfalls neu in der Kette: Schafszucht (Wolle), Stellmacher (Handkarren), Schmiede und
# Naehstube (Waren fuer Kaempfer). Ohne diese vier entstehen keine Einheiten und kein Kampf -
# der erste 6-Tage-Lauf am 05.11.2026 endete mit 0 Einheiten und 0 Kaempfen.


# Spielstile: derselbe Lauf, anderes Verhalten (Daniel 05.11.2026: "ein bis zwei Laeufe mit
# verschiedenem Verhalten"). "breit" baut die ganze Kette und greift ab Spieltag 2 alle zwei Tage
# an; "krieg" zieht Militaer und Werkstaetten nach vorn, bildet vier Kaempfer und greift taeglich an.
STILE = {
    "breit": {
        "kette": GEBAEUDE_REIHENFOLGE,
        "ziele": (("Bürgerwehr", 2), ("Kämpfer", 2), ("Handkarren", 1)),
        "angriff_ab": 2.0,
        "angriff_abstand": 2.0,
    },
    "krieg": {
        "kette": ("holzfäller", "bibliothek", "goldmine", "schmiede", "naehstube",
                  "kriegerakademie", "stellmacher", "farm", "erzmine", "schafszucht",
                  "steinmetz", "jaeger", "haus"),
        "ziele": (("Kämpfer", 4), ("Bürgerwehr", 2), ("Handkarren", 1)),
        "angriff_ab": 2.0,
        "angriff_abstand": 1.0,
    },
}


def _feld_fuer(siedlung: dict, gebaeude: str) -> int:
    """Erstes freies Feld, auf dem DIESES Gebaeude ueberhaupt stehen darf.

    Ohne diese Pruefung baut die Simulation auf das erstbeste Feld und die Farm landet im
    Wald - dann sieht der Lauf aus wie ein Spielfehler, obwohl nur die Politik dumm war.
    """
    belegt = set(int(k) for k in (siedlung.get("bauten") or {}))
    karte = siedlung.get("karte") or {}
    raster = karte.get("raster") or []
    for i, gel in enumerate(raster):
        if i in belegt:
            continue
        try:
            # WICHTIG: bau_moeglich liefert ein TUPEL (erlaubt, Begruendung). Ein blosses
            # `if GE.bau_moeglich(...)` ist deshalb IMMER wahr - dann landet jedes Gebaeude auf
            # Feld 0 im Wald und der ganze Lauf scheitert (Fehler vom 31.10.2026).
            ergebnis = GE.bau_moeglich(gebaeude, gel)
            erlaubt = ergebnis[0] if isinstance(ergebnis, tuple) else bool(ergebnis)
        except Exception:                      # noqa: BLE001
            continue
        if erlaubt:
            return i
    return -1


def _freies_feld(siedlung: dict) -> int:
    """Erstes unbelegtes Feld der Siedlungskarte (Feldzaehlung kommt aus der Karte selbst)."""
    belegt = set(int(k) for k in (siedlung.get("bauten") or {}))
    karte = siedlung.get("karte") or {}
    anzahl = karte.get("bauplaetze") or karte.get("felder") or 0
    try:
        anzahl = int(anzahl)
    except (TypeError, ValueError):
        anzahl = 0
    for i in range(max(0, anzahl)):
        if i not in belegt:
            return i
    return -1


MAX_TICK_FEHLER_FOLGE = 200      # erst bei Dauerfehler abbrechen (Skip-Mechanik, Daniel 05.11.2026)


def _versuch(aktion, *args):
    """Fuehrt eine Spieleraktion aus und meldet (ok, text) - nie eine Ausnahme nach aussen."""
    try:
        return aktion(*args)
    except Exception as fehler:                     # noqa: BLE001
        return False, f"{type(fehler).__name__}: {fehler}"


def _notiere_fehler(log: dict, art: str, grund: str) -> None:
    """Zaehlt einen Fehlversuch MIT Grund - gleicher Grund wird gezaehlt, nicht wiederholt.

    Warum: ein stiller Fehlversuch ist der Grund, warum ein Lauf am 05.11.2026 mit 0 Einheiten
    und 0 Kaempfen endete, ohne dass im Bericht stand, woran es lag. Der Bericht soll die
    Engstelle nennen, nicht nur ihr Ergebnis.
    """
    eintrag = log.setdefault("fehlschlaege", {}).setdefault(art, {})
    schluessel = str(grund)[:200]
    eintrag[schluessel] = eintrag.get(schluessel, 0) + 1


FORSCHUNGSZIELE = (("Schmiedekunst", 1), ("Waffentechnik", 3), ("Nähen", 1), ("Nähkunst", 1),
                   ("Rüstungsbau", 2), ("Felderwirtschaft", 2), ("Kriegskunst", 2),
                   ("Baukunst", 2), ("Verteidigungsanlagen", 2))


def _erzeuger_je_rohstoff() -> dict:
    """{Rohstoff klein: Gebaeudekennung} aus ``data/buildings.json`` - EINE Quelle, keine Handliste.

    Wird von der Engpass-Regel gebraucht: fehlt beim Bauen ein Rohstoff, wird sein Erzeuger
    nachgezogen (hoechstens 3). Ohne die Regel sah ein Lauf am 05.11.2026 wie ein Balancing-Fehler
    aus (Holz 0, "es fehlen 77 holz"), obwohl die Politik nur nicht nachgebaut hatte.
    """
    with open(os.path.join(HIER, "data", "buildings.json"), encoding="utf-8") as f:
        eintraege = json.load(f)["gebaeude"]
    karte = {}
    for eintrag in eintraege:
        roh = str(eintrag.get("rohstoff") or "").strip().lower()
        kennung = eintrag.get("id")
        if roh and kennung and eintrag.get("kategorie") == "Produktion":
            karte.setdefault(roh, kennung)
    return karte


def _ware_in_arbeit(zustand: dict, ware: str) -> bool:
    """Laeuft diese Ware schon in einer Werkstatt? Verhindert Dutzende gleiche Auftraege.

    Ohne die Pruefung reihte die Politik am 05.11.2026 in zwei Spieltagen 93 Kurzschwerter ein,
    weil die Ware erst nach ihrer Fertigungsdauer im Lager liegt und der naechste Schritt sie
    wieder "fehlend" fand.
    """
    for schlange in (zustand.get("werkstaetten") or {}).values():
        for eintrag in (schlange.get("einheiten") or []):
            if eintrag.get("ware") == ware and not eintrag.get("gemeldet"):
                return True
    return False


def _meilensteine_aus_zustand(log: dict, zustand: dict, jetzt: float) -> None:
    """Ersten Zeitpunkt je Meilenstein aus dem ZUSTAND lesen - nicht aus dem Aktionsprotokoll.

    Der Zustand ist die Wahrheit: ein Gebaeude steht dort, sobald es gebaut ist, eine Ware
    liegt dort, sobald sie FERTIG ist. Wer stattdessen den Auftrag zaehlt, misst einen Wunsch
    und nicht ein Ergebnis (die Ware wird erst nach ihrer Fertigungsdauer geliefert).
    Einmal gesetzt, bleibt der Wert stehen (`setdefault`) - der ERSTE Zeitpunkt zaehlt.
    """
    tag = round(float(jetzt) / SPIELTAG, 3)
    ist = log["meilensteine"]
    siedlung = (zustand.get("siedlungen") or [{}])[0]
    bauten = {str(v) for v in (siedlung.get("bauten") or {}).values()}
    haus, bibliothek = GE.finde_gebaeude("haus"), GE.finde_gebaeude("bibliothek")
    if haus and haus in bauten:                     # erstes Haus der Siedlung
        ist.setdefault("tag_erstes_haus", tag)
    if bibliothek and bibliothek in bauten:         # erste Bibliothek (Voraussetzung Forschung)
        ist.setdefault("tag_erste_bibliothek", tag)
    if any(int(v or 0) > 0 for v in (zustand.get("waren") or {}).values()):
        ist.setdefault("tag_erste_ware", tag)       # erste WARE IM LAGER, nicht im Auftrag
    if any(int(v or 0) > 0 and E.rolle(n) in ("kaempfer", "kundschafter")
           for n, v in (zustand.get("einheiten") or {}).items()):
        ist.setdefault("tag_erster_krieger", tag)   # erste Kampfeinheit im Heer


def _handelspunkte(zustand: dict, jetzt: float):
    """Handelspunkte der Partie - oder `None`, solange es keinen Zaehler gibt.

    Befund G-8: `gold_erloes` wird im Spiel nirgends geschrieben, die Kennzahl hat also keine
    Quelle. Schritt 6 des Ablaufs baut den Zaehler `handels_erloes` ein; hier wird er dann
    ohne Aenderung gelesen. Bis dahin steht `null` im Blatt - eine 0 waere eine Behauptung.
    """
    if "handels_erloes" not in (zustand or {}):
        return None                                 # Zaehler existiert noch nicht: NICHT GEMESSEN
    try:
        import punkte as P                          # dieselbe Rechenstelle wie die Anzeige
        return float(P.handelspunkte(zustand.get("handels_erloes"),
                                     zustand.get("letzter_handel"), jetzt))
    except Exception:                               # noqa: BLE001 - eine Kennzahl bricht nie den Lauf
        return None


def spielen(tage: float, saat: int = 7, stil: str = "breit") -> dict:
    # Stil bestimmt Baukette, Ausbildungsziele und Angriffstakt - derselbe Lauf, anderes Verhalten.
    stil_daten = STILE.get(stil) or STILE["breit"]
    kette = stil_daten["kette"]                       # Reihenfolge der Gebaeude
    ziele = stil_daten["ziele"]                       # Zielzahl je Einheit
    angriff_ab = float(stil_daten["angriff_ab"])      # ab welchem Spieltag angegriffen wird
    angriff_abstand = float(stil_daten["angriff_abstand"])   # Spieltage zwischen zwei Gefechten
    zustand = S.neuer_zustand(saat)
    jetzt = 0.0
    # Fester Zufall fuer den GANZEN Lauf (Schritt 2 des Ablaufs): ohne ihn wuerfelt jedes
    # Gefecht neu und zwei Laeufe mit demselben Startwert sind nicht vergleichbar - dann ist
    # keine Vorher-Zahl etwas wert. `S.angriff` nimmt den Generator als `rng` entgegen.
    zufall = random.Random(saat)
    random.seed(saat)                               # auch globale Zufallswege festlegen
    # Daniel 05.11.2026: ein gescheiterter Schritt beendet den Lauf NICHT. Jede Stelle, an der
    # etwas uebersprungen werden musste, landet mit Tag, Stelle und Grund in `uebersprungen`.
    log = {"schritte": [], "ereignisse": [], "bauten": [], "forschungen": [],
           "ausbildung": [], "kaempfe": [], "uebersprungen": [], "fehlschlaege": {},
           "meilensteine": {}, "ausgaben": {}, "leerlauf_schritte": 0,
           "_letzter_tag": -1, "_tick_fehler_folge": 0}
    ziel_tag = tage * SPIELTAG
    angegriffen = False
    letzter_angriff = -99.0                         # Spieltag des letzten Gefechts (Abstand 2 Tage)
    gesperrt = set()                                # Gebaeude, deren Obergrenze erreicht ist
    ohne_ausbau = set()                             # Gebaeudearten ohne belegte Ausbaustufen
    erzeuger = _erzeuger_je_rohstoff()              # Rohstoff -> Gebaeude, das ihn erzeugt
    engpass = None                                  # Rohstoff, der zuletzt beim Bauen fehlte
    while jetzt < ziel_tag:
        jetzt += SCHRITT
        try:                                        # EIN Spielschritt
            S.tick(zustand, jetzt, SCHRITT)         # Spielzeit vorruecken und buchen
            log["_tick_fehler_folge"] = 0           # geglueckt: Zaehler zuruecksetzen
        except Exception as fehler:                 # noqa: BLE001 - JEDER Fehler wird protokolliert
            # Skip-Mechanik (Daniel 05.11.2026): NICHT abbrechen. Der Schritt wird uebersprungen,
            # die Stelle steht im Bericht, das Spiel laeuft weiter - ein langer Lauf mit
            # protokollierten Luecken ist mehr wert als ein sauberer Abbruch nach Seite 1.
            log["uebersprungen"].append((round(jetzt / SPIELTAG, 2), "tick",
                                         f"{type(fehler).__name__}: {fehler}"))
            log["ereignisse"].append(f"{jetzt / SPIELTAG:.2f} Takt-Fehler uebersprungen: {fehler}")
            log["_tick_fehler_folge"] = int(log.get("_tick_fehler_folge") or 0) + 1
            if log["_tick_fehler_folge"] >= MAX_TICK_FEHLER_FOLGE:
                # Abbruch NUR bei Dauerfehler: dann ist der Zustand unbrauchbar und jede weitere
                # Zeile waere erfunden. Die Zahl der Fehler steht im Bericht.
                log["ereignisse"].append(
                    "Abbruch: %d Takt-Fehler in Folge - der Zustand ist nicht mehr belastbar."
                    % log["_tick_fehler_folge"])
                break                               # Ende der Schleife, Bericht folgt trotzdem
            continue                                # sonst: naechster Schritt

        # Kennzahlen (Ablauf Schritt 2): Stand der Reichskasse VOR den Aktionen dieses Schritts.
        # Der Takt hat eben produziert; was danach abgeht, ist eine Ausgabe - damit braucht das
        # Kennzahlenblatt keine zweite Buchfuehrung und keine geratenen Preise.
        _kasse_vor_aktionen = dict(zustand.get("ressourcen") or {})
        erfolg = False                              # hat dieser Schritt etwas bewirkt?

        # Bauen (hoechstens ein Versuch je Schritt), sonst ausbauen.
        siedlung = (zustand.get("siedlungen") or [{}])[0]
        feld = _freies_feld(siedlung)
        gebaut = False
        # WICHTIG: `bauten` speichert die Kennung OHNE Umlaut ('holzfaeller', 'jaeger').
        # Ein Vergleich mit dem Anzeigenamen ('holzfäller') trifft nie zu - dann baut die
        # Politik zehnmal dasselbe Gebaeude und der Lauf sieht aus wie ein Spielfehler.
        # Genau das ist am 31.10.2026 passiert (erster Lauf: 10x Holzfäller).
        vorhanden = {}
        for was in (siedlung.get("bauten") or {}).values():
            vorhanden[str(was)] = vorhanden.get(str(was), 0) + 1
        if feld >= 0:
            gruende_bau = []                        # warum ein Bau NICHT ging (Grundbilanz)
            # Engpass-Regel zuerst: fehlt seit dem letzten Schritt ein Rohstoff, wird sein
            # Erzeuger nachgezogen (hoechstens 3 Stueck). Das ist echtes Spielerverhalten und
            # verhindert, dass ein reiner Politikfehler als Balancing-Befund im Bericht landet.
            if engpass:
                kennung_erz = erzeuger.get(engpass)
                if kennung_erz and vorhanden.get(GE.finde_gebaeude(kennung_erz), 0) < 3:
                    feld_erz = _feld_fuer(siedlung, kennung_erz)
                    if feld_erz >= 0:
                        ok_erz, text_erz = _versuch(S.bauen, zustand, 0, kennung_erz, feld_erz)
                        if ok_erz:
                            log["bauten"].append((round(jetzt / SPIELTAG, 2),
                                                  f"{GE.gebaeude_name(kennung_erz)} "
                                                  f"(Engpass {engpass})"))
                            gebaut = True
                            erfolg = True               # dieser Schritt hat gebaut
                            engpass = None
            for gebaeude in kette:
                if gebaut:                          # Engpass-Bau hat schon gegriffen
                    break
                if gebaeude in gesperrt:            # "hoechstens 1x je Siedlung" - nicht wieder
                    continue                        # versuchen, sonst steht der Grund 268x im Lauf
                # Ausgewogen bauen: je Gebaeude hoechstens 2, sonst baut die Politik nur
                # Holzfäller (und die Simulation zeigt ein verzerrtes Bild).
                if vorhanden.get(GE.finde_gebaeude(gebaeude), 0) >= 2:
                    continue
                feld_geb = _feld_fuer(siedlung, gebaeude)
                if feld_geb < 0:
                    gruende_bau.append(f"{gebaeude}: kein passendes Feld frei")
                    continue
                ok, text = _versuch(S.bauen, zustand, 0, gebaeude, feld_geb)
                if ok:
                    log["bauten"].append((round(jetzt / SPIELTAG, 2), gebaeude))
                    gebaut = True
                    erfolg = True                   # dieser Schritt hat gebaut
                    break
                if "höchstens" in str(text):
                    gesperrt.add(gebaeude)          # Obergrenze erreicht - dauerhaft auslassen
                # Fehlbetrag merken: daraus entsteht im naechsten Schritt die Engpass-Regel.
                treffer = re.search(r"es fehlen \d+ ([a-zA-ZäöüÄÖÜß]+)", str(text))
                if treffer:
                    engpass = treffer.group(1).lower()
                gruende_bau.append(f"{gebaeude}: {text}")
            if not gebaut:
                # Der Grund des ZULETZT versuchten Gebaeudes ist der naechste in der Kette -
                # die frueheren scheitern meist nur an "schon 2x gebaut".
                _notiere_fehler(log, "bauen", gruende_bau[-1] if gruende_bau
                                else "alle Gebaeude der Kette stehen (je 2) oder sind gesperrt")
        if not gebaut and (siedlung.get("bauten") or {}):
            for feld_nr in sorted(int(k) for k in siedlung["bauten"]):
                art = str(siedlung["bauten"].get(str(feld_nr), ""))
                if art in ohne_ausbau:              # "kein Ausbau belegt" - Grund einmal notieren
                    continue                        # reicht; 1.100 Wiederholungen helfen niemandem
                ok, text = _versuch(S.ausbauen, zustand, 0, feld_nr)
                if ok:
                    log["bauten"].append((round(jetzt / SPIELTAG, 2), f"ausbau Feld {feld_nr}"))
                    erfolg = True                   # dieser Schritt hat ausgebaut
                    break
                if "kein Ausbau belegt" in str(text):
                    ohne_ausbau.add(art)
                _notiere_fehler(log, "ausbauen", text)

        # Forschung - Ziele statt Reihenfolge: erst die Stufen, die eine Einheit freischalten
        # (Schmiedekunst 1 -> Waffentechnik 3, Nähen 1 -> Nähkunst 1, Rüstungsbau 2), dann Wirtschaft.
        # So entsteht der Kämpfer früh statt am Rand der Messzeit. Fehlversuche mit Grund.
        if not S.forschung_stand(zustand, jetzt).get("laeuft"):
            stand_f = {n: int((e or {}).get("stufe", 0))
                       for n, e in (zustand.get("forschung") or {}).items()}
            for gebiet, ziel in FORSCHUNGSZIELE:
                if stand_f.get(gebiet, 0) >= ziel:
                    continue                    # Zielstufe dieser Forschung steht schon
                ok, text = _versuch(S.forschung_starten, zustand, gebiet, jetzt)
                if ok:
                    log["forschungen"].append((round(jetzt / SPIELTAG, 2), gebiet))
                    erfolg = True                   # dieser Schritt hat geforscht
                    break
                _notiere_fehler(log, "forschung", f"{gebiet}: {text}")
                break                           # ein Forschungsversuch je Spielschritt

        # Ausbildung - Zielzahlen klein und dokumentiert, damit der Lauf KAEMPFE erreicht: ohne
        # Kaempfer und ohne Karren gibt es keinen Angriff (erster Lauf 05.11.2026 endete 0/0).
        # Der frueher feste Griff nach "Kämpfer" scheiterte immer an fehlender Ware (Kurzschwert,
        # Lederrüstung), und weil nach einem Erfolg abgebrochen wurde, kam der Handkarren nie an
        # die Reihe. Jetzt: je Schritt EIN erfolgreicher Versuch, Zielzahlen je Einheit (Stil).
        for einheit, soll in ziele:
            if int((zustand.get("einheiten") or {}).get(einheit, 0) or 0) >= soll:
                continue                        # Zielzahl dieser Einheit ist erreicht
            ok, text = _versuch(S.ausbilden, zustand, einheit)
            if ok:
                log["ausbildung"].append((round(jetzt / SPIELTAG, 2), einheit))
                erfolg = True                       # dieser Schritt hat ausgebildet
                break                           # hoechstens EINE Ausbildung je Spielschritt
            _notiere_fehler(log, "ausbildung", f"{einheit}: {text}")
            # Fehlt die Ware, wird sie in der Werkstatt in Auftrag gegeben (der echte Spielweg
            # zu einer Einheit: Werkstatt -> Ware -> Akademie -> Einheit).
            eintrag = E.alle().get(einheit) or {}
            for ware in (eintrag.get("waren") or []):
                if int((zustand.get("waren") or {}).get(ware, 0) or 0) < 1:
                    if _ware_in_arbeit(zustand, ware):
                        break                   # laeuft schon - nicht ein zweites Mal bestellen
                    ok_w, text_w = _versuch(S.ware_fertigen, zustand, 0, ware, 1, jetzt)
                    if ok_w:
                        log["ereignisse"].append(f"{jetzt / SPIELTAG:.2f} Ware in Auftrag: {ware}")
                        erfolg = True               # dieser Schritt hat eine Ware bestellt
                    else:
                        _notiere_fehler(log, "ware", f"{ware}: {text_w}")
                    break                       # eine Ware je Einheit und Schritt

        # Angriffe: der erste ab Spieltag 2, sobald Kaempfer dastehen; danach hoechstens alle
        # `angriff_abstand` Spieltage ein weiterer. Daniel 05.11.2026: ein Angriff OHNE Karren ist
        # erlaubt - die Beute ist dann 0 (Karrenladung ist die Grenze, belegt im Handbuch).
        if jetzt >= angriff_ab * SPIELTAG and (jetzt / SPIELTAG - letzter_angriff) >= angriff_abstand:
            krieger = {n: int(v) for n, v in (zustand.get("einheiten") or {}).items()
                       if int(v or 0) > 0 and E.rolle(n) in ("kaempfer", "kundschafter")}
            karren = {n: int(v) for n, v in (zustand.get("einheiten") or {}).items()
                      if int(v or 0) > 0 and E.rolle(n) == "karren"}
            if krieger:
                ziel = {"name": "Bot-Siedlung", "wall_stufe": 1, "wall_zustand_prozent": 100.0,
                        "vorraete": {"holz": 400.0, "stein": 300.0, "nahrung": 250.0}}
                # Der feste Generator geht als `rng` mit: sonst wuerfelt der Kern bei jedem
                # Gefecht neu und derselbe Startwert ergibt zwei verschiedene Kennzahlen.
                ok, ergebnis = _versuch(S.angriff, zustand, ziel, jetzt, zufall)
                _ergebnis = (ergebnis or {}).get("ergebnis") or {}
                log["kaempfe"].append({
                    "tag": round(jetzt / SPIELTAG, 2), "ok": ok,
                    "ausgang": _ergebnis.get("ausgang"),
                    "beute": (ergebnis or {}).get("beute"),
                    # Verluste kommen aus dem Gefechtsergebnis (EINE Quelle, kein Nachrechnen).
                    "verluste": _ergebnis.get("verluste_angreifer") or {},
                    "vorrunde": (ergebnis or {}).get("bestanden"),
                    "truppen": dict(krieger, **karren)})
                if ok:                                  # nur ein GEFOCHTENES Gefecht zaehlt
                    log["meilensteine"].setdefault("tag_erstes_gefecht",
                                                   round(jetzt / SPIELTAG, 3))
                    erfolg = True                       # dieser Schritt hat gekaempft
                angegriffen = True
                letzter_angriff = jetzt / SPIELTAG     # Abstand zum naechsten Gefecht
            else:
                # Ohne Kaempfer oder ohne Karren gibt es keinen Angriff - der Grund gehoert in
                # den Bericht, sonst sieht der Lauf aus, als waere Kämpfen nicht implementiert.
                _notiere_fehler(log, "angriff",
                                f"keine Kaempfer ({sum(krieger.values())}) / "
                                f"keine Karren ({sum(karren.values())})")

        # Kennzahlen (Ablauf Schritt 2) - Ausgaben, Leerlauf, Meilensteine ----------------
        # Ausgaben: der Unterschied der Reichskasse zu Beginn des Schritts. Gezaehlt wird nur
        # der ABGANG (> 0) - Beute und Ernte sind kein Negativ-Ausgang und wuerden die Summe
        # sonst kleiner machen, als sie ist.
        _kasse_nach_aktionen = dict(zustand.get("ressourcen") or {})
        for rohstoff, vorher in _kasse_vor_aktionen.items():
            abgang = float(vorher or 0) - float(_kasse_nach_aktionen.get(rohstoff, 0) or 0)
            if abgang > 0:
                log["ausgaben"][rohstoff] = round(
                    float(log["ausgaben"].get(rohstoff, 0.0)) + abgang, 2)
        if not erfolg:                              # nichts gebaut, geforscht, gelernt, gekaempft
            log["leerlauf_schritte"] = int(log["leerlauf_schritte"]) + 1
        _meilensteine_aus_zustand(log, zustand, jetzt)

        tag_rund = int(jetzt // SPIELTAG)
        if tag_rund > log["_letzter_tag"]:
            try:                                    # Punkte sind eine ANZEIGE - nie ein Abbruchgrund
                stand = S.punkte(zustand, jetzt)    # Punktestand des Tages
            except Exception as fehler:             # noqa: BLE001
                log["uebersprungen"].append((round(jetzt / SPIELTAG, 2), "punkte",
                                             f"{type(fehler).__name__}: {fehler}"))
                stand = {}                          # dann ohne Zahlen weiter

            log["_letzter_tag"] = tag_rund
            log["schritte"].append({
                "tag": tag_rund, "ressourcen": dict(zustand.get("ressourcen") or {}),
                "punkte": stand.get("gesamtpunkte"), "krieg": stand.get("kriegspunkte"),
                "forschung": stand.get("forschungspunkte"),
                "einheiten": dict(zustand.get("einheiten") or {}),
                "bauten": len(siedlung.get("bauten") or {})})

    try:                                            # Abschlussstand - nie ein Abbruchgrund
        _punkte = S.punkte(zustand, jetzt)          # Punktestand am Ende
    except Exception as fehler:                     # noqa: BLE001
        log["uebersprungen"].append((round(jetzt / SPIELTAG, 2), "punkte-ende",
                                     f"{type(fehler).__name__}: {fehler}"))
        _punkte = {}                                # dann ohne Zahlen weiter
    log["ende"] = {"tag": round(jetzt / SPIELTAG, 2),
                   "ressourcen": dict(zustand.get("ressourcen") or {}),
                   "punkte": _punkte,
                   "einheiten": dict(zustand.get("einheiten") or {}),
                   "handelspunkte": _handelspunkte(zustand, jetzt),
                   "uebersprungen": len(log["uebersprungen"])}
    return log


def bericht(log: dict, tage: float, stil: str = "breit") -> str:
    z = []
    z.append(f"# Spieltest-Simulation — {tage:g} Spieltage, ohne Fenster gefahren (Stil {stil})")
    z.append("")
    z.append(f"**Erzeugt:** {datetime.datetime.now():%d.%m.%Y %H:%M} von `tools/spieltest_simulation.py` "
             "— reine Spiellogik (`src/spielschicht.py`), keine Oberflaeche.")
    _stil = STILE.get(stil) or STILE["breit"]
    z.append(f"**Spielerpolitik (dokumentiert, nicht optimal):** Stil **{stil}** — alle 20 Spielminuten "
             f"ein Schritt; Baukette {', '.join(_stil['kette'])}; Forschung wenn bezahlbar; "
             f"Ausbildungsziele {', '.join('%d %s' % (n, e) for e, n in _stil['ziele'])}; "
             f"Angriff ab Spieltag {_stil['angriff_ab']:g}, danach alle "
             f"{_stil['angriff_abstand']:g} Spieltage.")
    z.append("**Hinweis zur Saat:** die Startkarte ist FEST (Register 229) - `--saat` wirkt in diesem\n"
             "Lauf also nicht, solange keine zweite Siedlung gegruendet wird. Unterschiedliche Verlaeufe\n"
             "entstehen ueber `--stil` (breit/krieg) und `--tage`.")
    z.append("")
    z.append("## Tagesbilanzen")
    z.append("")
    z.append("| Spieltag | Holz | Stein | Nahrung | Gold | Mana | Krieg | Forschung | Gesamt | Einheiten | Gebaeude |")
    z.append("|---|---|---|---|---|---|---|---|---|---|---|")
    for s in log["schritte"]:
        r = s.get("ressourcen") or {}
        z.append(f"| {s['tag']} | {r.get('holz', 0):.0f} | {r.get('stein', 0):.0f} | "
                 f"{r.get('nahrung', 0):.0f} | {r.get('gold', 0):.0f} | {r.get('mana', 0):.0f} | "
                 f"{s.get('krieg')} | {s.get('forschung')} | **{s.get('punkte')}** | "
                 f"{sum(s.get('einheiten', {}).values())} | {s.get('bauten')} |")
    z.append("")
    z.append("## Gebaut (Spieltag, was)")
    z.append("")
    if log["bauten"]:
        z.append(", ".join(f"T{t} {was}" for t, was in log["bauten"][:40]))
    else:
        z.append("_nichts gebaut — entweder fehlten Rohstoffe oder alle Felder waren belegt._")
    z.append("")
    z.append("## Forschung")
    z.append("")
    z.append(", ".join(f"T{t} {was}" for t, was in log["forschungen"][:20]) or "_keine gestartet_")
    z.append("")
    z.append("## Ausbildung")
    z.append("")
    z.append(", ".join(f"T{t} {was}" for t, was in log["ausbildung"][:20]) or "_keine_")
    z.append("")
    z.append("## Kaempfe")
    z.append("")
    if log["kaempfe"]:
        for k in log["kaempfe"]:
            z.append(f"* Tag {k['tag']}: Truppen {k['truppen']} -> Ausgang **{k['ausgang']}**, "
                     f"Vorrunde bestanden: {k['vorrunde']}, Beute {k['beute']}")
    else:
        z.append("_kein Kampf zustande gekommen (keine Kaempfer oder keine Karren)._")
    z.append("")
    e = log["ende"]
    z.append("## Ende")
    z.append("")
    z.append(f"* Spieltag {e['tag']}")
    z.append(f"* Punkte: {e['punkte']}")
    z.append(f"* Einheiten: {e['einheiten'] or '{}'}")
    z.append(f"* Rohstoffe: {e['ressourcen']}")
    z.append("")
    z.append("## Uebersprungene Schritte (der Lauf wurde NICHT abgebrochen)")
    z.append("")
    uebersprungen = log.get("uebersprungen") or []
    if uebersprungen:
        z.append(f"**{len(uebersprungen)} Stelle(n)** konnten nicht ausgefuehrt werden und wurden "
                 "uebersprungen - der Verlauf laeuft danach weiter (Daniel 05.11.2026: lieber ein "
                 "langer Lauf mit Luecken als ein kurzer Abbruch).")
        z.append("")
        z.append("| Spieltag | Stelle | Grund |")
        z.append("|---|---|---|")
        for tag, stelle, grund in uebersprungen[:25]:
            z.append(f"| {tag} | {stelle} | {str(grund)[:180]} |")
        if len(uebersprungen) > 25:
            z.append("")
            z.append(f"_... und {len(uebersprungen) - 25} weitere (gleiche Form)._")
    else:
        z.append("_keine - jeder Schritt liess sich ausfuehren._")
    z.append("")
    z.append("## Fehlversuche mit Grund (Grundbilanz)")
    z.append("")
    fehl = log.get("fehlschlaege") or {}
    if fehl:
        z.append("Was die Spielerpolitik versucht hat und WARUM es nicht ging - gleiche Gruende "
                 "werden gezaehlt. Ohne diesen Abschnitt sieht ein Lauf mit 0 Einheiten wie ein "
                 "Spielfehler aus, obwohl nur eine Ware oder eine Werkstatt fehlte.")
        z.append("")
        z.append("| Stelle | Anzahl | Grund |")
        z.append("|---|---|---|")
        zeilen = []
        for art, gruende in fehl.items():
            for grund, anzahl in gruende.items():
                zeilen.append((anzahl, art, grund))
        for anzahl, art, grund in sorted(zeilen, reverse=True)[:14]:
            z.append(f"| {art} | {anzahl} | {str(grund)[:170]} |")
    else:
        z.append("_keine - jede Spieleraktion liess sich ausfuehren._")
    z.append("")
    z.append("## Was ein Pruefer daraus ablesen kann")
    z.append("")
    z.append("* **Tempo:** wie viele Spieltage bis zum ersten Gebaeude, zur ersten Forschung, "
             "zum ersten Kampf?")
    z.append("* **Engstelle:** welcher Rohstoff bremst (Tabelle oben)? ")
    z.append("* **Stillstand:** gibt es Tage ohne einen einzigen Bau? Warum?")
    z.append("* **Kampf:** Vorrunde bestanden? Beute in brauchbarer Hoehe? Truppenverlust?")
    z.append("* **Punkte:** wachsen sie plausibel (Krieg + Forschung)/2?")
    return "\n".join(z) + "\n"


# ---------------------------------------------------------------------------
# Kennzahlenblatt (Ablauf Schritt 2, 06.11.2026)
# ---------------------------------------------------------------------------
# Warum: ab dem Rachetopf (Schritt 4) veraendert jeder Umbau das Spielgefuehl, und ohne eine
# Vorher-Zahl ist "besser" nur ein Gefuehl. Das Blatt ist GENAU EINE Zeile je Partie mit
# immer denselben Pflichtschluesseln; ein nicht erreichter Meilenstein steht als `null`,
# nicht als 0 - sonst ist "nicht erreicht" von "bei Tag 0 erreicht" nicht zu unterscheiden.

KENNZAHLEN_PFLICHT = (
    "startwert", "stand", "daten_hash",
    "tag_erstes_haus", "tag_erste_bibliothek", "tag_erste_ware",
    "tag_erster_krieger", "tag_erstes_gefecht", "ruhm_stufe",
    "ausgaben", "leerlauf_sek", "fehlschlaege", "handelspunkte",
    "beute_je_feldzug", "verluste_je_gefecht",
    "abstand_meilensteine_max",
)

KENNZAHLEN_ORDNER = ("docs", "balancing")            # der EINE Ablageort des Blattes


def startwert(saat: int, stil: str, tage: float) -> dict:
    """Der Startwert ist die VOLLE Eingabe des Laufs - Saat, Stil UND Laenge.

    Ohne Laenge und Stil waere "gleicher Startwert" eine halbe Wahrheit: zwei Laeufe ueber
    6 und 12 Spieltage haben verschiedene Zahlen, obwohl die Saat gleich ist.
    """
    return {"saat": int(saat), "stil": str(stil), "tage": float(tage)}


def daten_hash(wurzel: str = HIER) -> str:
    """Ein Fingerabdruck ueber ALLE Datendateien in `data/` (Name und Inhalt, sortiert).

    Damit ist belegt, ob zwei Zeilen denselben Datenstand messen: aendert sich eine Zahl in
    `data/`, aendert sich der Hash - auch wenn niemand daran denkt, ihn zu erneuern.
    """
    ordner = os.path.join(wurzel, "data")           # alle Spieldaten liegen hier
    teile = []                                      # je Datei eine Zeile "Name:Pruffsumme"
    for name in sorted(os.listdir(ordner)):         # sortiert = gleicher Hash bei gleichem Inhalt
        pfad = os.path.join(ordner, name)
        if not (name.endswith(".json") and os.path.isfile(pfad)):
            continue                                # nur Datendateien, keine Unterordner
        with open(pfad, "rb") as f:
            teile.append(name + ":" + hashlib.sha256(f.read()).hexdigest())
    gesamt = hashlib.sha256("\n".join(teile).encode("utf-8")).hexdigest()
    return "sha256:" + gesamt[:32]                  # 128 Bit reichen fuer einen Vergleich


def _git(wurzel: str, *args: str):
    """Ein lesender git-Aufruf - gibt None zurueck, wenn git fehlt oder meckert.

    Lesend heisst: `rev-parse` und `status` aendern nichts. Fehlt git (oder ist es kein
    Repository), bleibt der Wert `None` - das Blatt behauptet dann keinen Stand.
    """
    try:
        aus = subprocess.run(["git", "-C", wurzel, *args], capture_output=True,
                             text=True, timeout=30)
        return aus.stdout.strip() if aus.returncode == 0 else None
    except Exception:                               # noqa: BLE001 - ohne git bleibt der Stand leer
        return None


def stand(wurzel: str = HIER) -> dict:
    """Der Code-Stand der Messung: Kopf-Commit und ob der Arbeitsbaum sauber war.

    Zwei Zeilen sind nur vergleichbar, wenn beide denselben Code messen. Ein schmutziger
    Baum (ungespeicherte Aenderung) ist ausdruecklich KEIN sauberer Stand.
    """
    kopf = _git(wurzel, "rev-parse", "--short", "HEAD")
    schmutz = _git(wurzel, "status", "--porcelain")
    return {"kopf": kopf, "sauber": None if schmutz is None else (schmutz == "")}


def _abstand_meilensteine(meilensteine: dict, tage: float) -> float:
    """Laengste Strecke ohne neuen Meilenstein in Spieltagen - das Spielgefuehl-Mass.

    Ohne diese Zahl sieht ein Lauf, in dem nach Tag 3 nichts mehr passiert, genauso aus wie
    einer mit gleichmaessigem Fortschritt (die Meilensteine sind dann alle gesetzt).
    """
    punkte = sorted(float(w) for w in (meilensteine or {}).values()
                    if isinstance(w, (int, float)))
    grenzen = [0.0] + punkte + [float(tage)]        # Anfang und Ende gehoeren dazu
    return round(max(b - a for a, b in zip(grenzen, grenzen[1:])), 3)


def _fehlschlag_gruppen(fehl: dict, grenze: int = 20) -> list:
    """Die Fehlversuche nach BEDEUTUNG gruppiert: Zahlen im Grund werden zu `#`.

    Warum: derselbe Grund taucht mit hunderten Nachkommastellen auf ("es fehlen 78.4 holz",
    "es fehlen 79 holz") und macht aus dem Blatt eine Zahlenwand (gemessen 06.11.2026: eine
    Zeile ueber 100 KB). Gruppiert bleibt sichtbar, WORAN der Lauf haengt; die genaue Menge
    steht im Spieltest-Log. Sortiert nach Anzahl, dann alphabetisch - also deterministisch.
    """
    summen = {}                                     # (Aktion, gruppierter Grund) -> Anzahl
    for art, gruende in (fehl or {}).items():
        for grund, anzahl in (gruende or {}).items():
            schluessel = (str(art), re.sub(r"\d+(?:[.,]\d+)?", "#", str(grund)))
            summen[schluessel] = summen.get(schluessel, 0) + int(anzahl)
    liste = [[art, grund, anzahl] for (art, grund), anzahl in summen.items()]
    return sorted(liste, key=lambda z: (-z[2], z[0], z[1]))[:grenze]


def kennzahlen(log: dict, tage: float, saat: int, stil: str,
               wurzel: str = HIER) -> dict:
    """Die Kennzahlenzeile aus EINEM Lauf - reine Ableitung, keine zweite Messung.

    Alles kommt aus dem Laufprotokoll (`log`) und dem Zustand am Ende; nur `stand` und
    `daten_hash` beschreiben die Umgebung. Der Zeitstempel gehoert NICHT in die Zeile,
    sonst waeren zwei Laeufe mit demselben Startwert nie identisch (Wache 2).
    """
    m = log.get("meilensteine") or {}               # erste Zeitpunkte je Meilenstein
    kaempfe = log.get("kaempfe") or []
    ende = log.get("ende") or {}
    punkte = ende.get("punkte") or {}
    # Ruhm-Stufe aus DERSELBEN Lesestelle wie die Anzeige (`postfach.rang`), nicht nachgebaut.
    ruhm = None
    if punkte.get("gesamtpunkte") is not None:
        try:
            ruhm = int(PF.rang(punkte.get("gesamtpunkte")).get("stufe") or 0)
        except Exception:                           # noqa: BLE001 - Kennzahl bricht nie den Lauf
            ruhm = None
    fehl = log.get("fehlschlaege") or {}
    return {
        "startwert": startwert(saat, stil, tage),
        "stand": stand(wurzel),
        "daten_hash": daten_hash(wurzel),
        "tag_erstes_haus": m.get("tag_erstes_haus"),
        "tag_erste_bibliothek": m.get("tag_erste_bibliothek"),
        "tag_erste_ware": m.get("tag_erste_ware"),
        "tag_erster_krieger": m.get("tag_erster_krieger"),
        "tag_erstes_gefecht": m.get("tag_erstes_gefecht"),
        "ruhm_stufe": ruhm,
        "ausgaben": dict(log.get("ausgaben") or {}),
        "leerlauf_sek": int(log.get("leerlauf_schritte") or 0) * SCHRITT,
        "fehlschlaege": _fehlschlag_gruppen(fehl),
        "handelspunkte": ende.get("handelspunkte"),
        "beute_je_feldzug": [dict(k.get("beute") or {}) for k in kaempfe if k.get("ok")],
        "verluste_je_gefecht": [dict(k.get("verluste") or {}) for k in kaempfe if k.get("ok")],
        "abstand_meilensteine_max": _abstand_meilensteine(m, tage),
    }


def _kennzahlen_markdown(zeilen: list, wann: datetime.datetime) -> str:
    """Die lesbare Fassung des Blattes: eine Tabelle, eine Zeile je Partie.

    Die Legende steht darunter, weil eine Zahl ohne Bedeutung im Blatt niemand liest.
    """
    z = [f"# Kennzahlenblatt - {wann:%d.%m.%Y %H:%M}", ""]
    z.append("Erzeugt von `tools/spieltest_simulation.py --kennzahlen`. Eine Zeile je Partie, "
             "dieselben Schluessel bei jedem Lauf. `-` heisst **nicht erreicht oder nicht "
             "gemessen** (im JSONL steht dort `null`), nicht `0`. Die Rechenwege stehen in "
             "`docs/balancing/README_KENNZAHLEN.md`.")
    z.append("")
    z.append("| # | Stand | Saat/Stil/Tage | Haus | Bibliothek | Ware | Krieger | Gefecht | "
             "Ruhm | Leerlauf s | Handelspunkte | Beute (Feldzuege) | Verluste (Gefechte) | "
             "groesste Luecke |")
    z.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")

    def _t(wert):
        """Ein Meilenstein als Tageszahl oder als Strich (nicht erreicht = nicht 0)."""
        return "-" if wert is None else f"{float(wert):g}"

    for i, zeile in enumerate(zeilen, start=1):
        sw = zeile.get("startwert") or {}
        st = zeile.get("stand") or {}
        kopf = st.get("kopf") or "?"
        schmutz = "" if st.get("sauber") in (True, None) else "*"
        beute = sum(sum(v for v in (b or {}).values() if isinstance(v, (int, float)))
                    for b in (zeile.get("beute_je_feldzug") or []))
        verluste = sum(sum(v for v in (b or {}).values() if isinstance(v, (int, float)))
                       for b in (zeile.get("verluste_je_gefecht") or []))
        hp = zeile.get("handelspunkte")
        z.append(f"| {i} | {kopf}{schmutz} | {sw.get('saat')}/{sw.get('stil')}/"
                 f"{sw.get('tage'):g} | {_t(zeile.get('tag_erstes_haus'))} | "
                 f"{_t(zeile.get('tag_erste_bibliothek'))} | {_t(zeile.get('tag_erste_ware'))} | "
                 f"{_t(zeile.get('tag_erster_krieger'))} | {_t(zeile.get('tag_erstes_gefecht'))} | "
                 f"{'-' if zeile.get('ruhm_stufe') is None else zeile.get('ruhm_stufe')} | "
                 f"{zeile.get('leerlauf_sek')} | {'-' if hp is None else f'{float(hp):.2f}'} | "
                 f"{beute:g} in {len(zeile.get('beute_je_feldzug') or [])} | "
                 f"{verluste:g} in {len(zeile.get('verluste_je_gefecht') or [])} | "
                 f"{zeile.get('abstand_meilensteine_max'):g} |")
    z.append("")
    z.append("## Legende")
    z.append("")
    z.append("| Schluessel | Bedeutung | Quelle im Werkzeug |")
    z.append("|---|---|---|")
    z.append("| `startwert` | Saat, Stil und Laenge des Laufs - die volle Eingabe | `startwert()` |")
    z.append("| `stand` | Kopf-Commit und ob der Arbeitsbaum sauber war (`*` = schmutzig) | `git rev-parse`/`status` |")
    z.append("| `daten_hash` | Pruefsumme ueber alle `data/*.json` - belegt den Datenstand | `daten_hash()` |")
    z.append("| `tag_*` | Spieltag des ERSTEN Ereignisses; `null` = nie erreicht | `_meilensteine_aus_zustand` |")
    z.append("| `ruhm_stufe` | Ruhm-Stufe zum Endpunktestand | `postfach.rang` (EINE Lesestelle) |")
    z.append("| `ausgaben` | je Rohstoff die Summe der Abbuchungen in Spielschritten | Reichskasse vor/nach den Aktionen |")
    z.append("| `leerlauf_sek` | Spielsekunden ohne eine einzige erfolgreiche Aktion | `leerlauf_schritte x 1200` |")
    z.append("| `fehlschlaege` | Aktion, Grund, Anzahl - die haeufigsten Gruende; Zahlen im Grund sind `#` (gruppiert) | `_fehlschlag_gruppen` |")
    z.append("| `handelspunkte` | Handelspunkte am Ende; `null`, solange der Zaehler fehlt (G-8) | `_handelspunkte` |")
    z.append("| `beute_je_feldzug` | Beute je GEFOCHTENEM Gefecht | `log['kaempfe']` |")
    z.append("| `verluste_je_gefecht` | eigene Verluste je Gefecht | Gefechtsergebnis |")
    z.append("| `abstand_meilensteine_max` | laengste Strecke ohne neuen Meilenstein (Spieltage) | `_abstand_meilensteine` |")
    z.append("")
    z.append("**Determinismus:** der Lauf bekommt EINEN festen Zufallsgenerator (`random.Random(saat)`) "
             "und gibt ihn an jedes Gefecht weiter. Zwei Laeufe mit demselben `startwert` und "
             "demselben `stand` ergeben darum dieselbe Zeile.")
    return "\n".join(z) + "\n"


def kennzahlen_schreiben(zeile: dict, wurzel: str = HIER, wann=None) -> dict:
    """Eine Partie ins Kennzahlenblatt schreiben: JSONL (eine Zeile je Partie) + Markdown.

    Geschrieben wird AUSSCHLIESSLICH unter `docs/balancing/` - das Werkzeug fasst `data/` und
    `src/` nicht an (Wache 5 in `tests/test_kennzahlenblatt.py`). Eine Zeile ohne
    Pflichtschluessel wird abgelehnt, nicht ergaenzt: eine halbe Zeile im Blatt ist schlimmer
    als keine.
    """
    ordner = os.path.join(wurzel, *KENNZAHLEN_ORDNER)   # der EINE Ablageort
    os.makedirs(ordner, exist_ok=True)                  # Ordner darf fehlen (erster Lauf)
    fehlend = [k for k in KENNZAHLEN_PFLICHT if k not in zeile]
    if fehlend:                                         # Pflicht erfuellt oder gar nicht
        raise ValueError("Kennzahlenzeile ohne Pflichtschluessel: " + ", ".join(fehlend))
    jetzt = wann or datetime.datetime.now()             # Zeitstempel NUR fuer Dateinamen/Kopf
    pfad = os.path.join(ordner, "kennzahlen.jsonl")     # eine Zeile je Partie, angehaengt
    with open(pfad, "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(zeile, ensure_ascii=False, sort_keys=True) + "\n")
    zeilen = []                                         # alles wieder einlesen: die Tabelle
    with open(pfad, encoding="utf-8") as f:             # zeigt IMMER den ganzen Bestand
        for linie in f:
            linie = linie.strip()
            if linie:
                zeilen.append(json.loads(linie))
    md_pfad = os.path.join(ordner, f"KENNZAHLEN_{jetzt:%Y-%m-%d}.md")
    with open(md_pfad, "w", encoding="utf-8", newline="\n") as f:
        f.write(_kennzahlen_markdown(zeilen, jetzt))
    return {"jsonl": pfad, "markdown": md_pfad, "zeilen": len(zeilen)}


def main() -> int:
    tage = 6.0
    if "--tage" in sys.argv:
        tage = float(sys.argv[sys.argv.index("--tage") + 1])
    saat = 7
    if "--saat" in sys.argv:
        saat = int(sys.argv[sys.argv.index("--saat") + 1])
    stil = "breit"
    if "--stil" in sys.argv:
        stil = sys.argv[sys.argv.index("--stil") + 1]
    log = spielen(tage, saat, stil)
    text = bericht(log, tage, stil)
    ziel = os.path.join(HIER, "docs", "audits",
                        f"SPIELTEST_LOG_{datetime.datetime.now():%Y%m%d_%H%M}.md")
    with open(ziel, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    print(text)
    print(f"\nGESCHRIEBEN: {ziel}")
    # Kennzahlenblatt (Ablauf Schritt 2): nur auf Anforderung, damit ein normaler Lauf das
    # Blatt nicht mit Zeilen fuellt, die niemand auswertet.
    if "--kennzahlen" in sys.argv:
        zeile = kennzahlen(log, tage, saat, stil)
        ablage = kennzahlen_schreiben(zeile)
        # Kurzfassung auf der Konsole: die VOLLE Zeile steht im JSONL, hier nur die Eckwerte.
        kurz = {k: zeile.get(k) for k in ("startwert", "stand", "daten_hash", "tag_erstes_haus",
                                          "tag_erster_krieger", "tag_erstes_gefecht",
                                          "ruhm_stufe", "leerlauf_sek", "handelspunkte",
                                          "abstand_meilensteine_max")}
        print("KENNZAHLEN: " + json.dumps(kurz, ensure_ascii=False, sort_keys=True))
        print(f"KENNZAHLENBLATT: {ablage['jsonl']} ({ablage['zeilen']} Zeile(n) gesamt), "
              f"{ablage['markdown']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
