"""
Nebelseetal Remake - FACH-SCHICHT (Spielebene) fuer die Oberflaeche.

Diese Schicht ist die EINZIGE Stelle, an der die Oberflaeche den Spielstand
anfasst. Statt ein gutes Dutzend Module einzeln zu rufen, ruft die GUI hier
wenige, klar benannte Aktionen. Der Spielstand ist ein **einfaches dict** --
also ohne Klassen, ohne tkinter und ohne Dateizugriff -- und laesst sich mit
``json.dumps`` speichern und wieder laden (das Speichern selbst macht die GUI).

Verbundene Kindmodule (nichts wird nachgebaut, alles wird benutzt):
  * ``spieldaten``   - die Originalwerte aus ``data/*.json``
  * ``gelaende``     - Siedlungskarte, Bau-Eignung, Bauplaetze
  * ``gebaeude_wirkung`` (W4b) - Bevoelkerung, Bibliothek, Ausbildung, Wall
  * ``wirtschaft``   - stuendlicher Rohstoffertrag aus den bebauten Feldern
  * ``forschung``    - Forschungsablauf (Stufe steigt ERST nach der Zeit)
  * ``werkstatt``    (W3)  - Waren in Warteschlangen, parallele Werkstaetten
  * ``kampfbericht`` (W2b) - Vorrunde, Mauerschaden, Beute, Bericht
  * ``punkte``       (W6)  - Forschungs-/Kriegs-/Gesamtpunkte, Sieg/Niederlage
  * ``portalraum``   (W5)  - Limbus, Koordinatenwechsel (Zusatzaktion)

Grundsaetze:
  * Nur Standardbibliothek, KEIN tkinter, KEIN Schreiben von Dateien.
  * Jede Aktion gibt ``(ok, Meldung)`` zurueck; ``ok=False`` nennt immer einen
    Grund (die Meldung) und laesst den Zustand unveraendert.
  * Erfolgreiche Aktionen haengen EIN Ereignis fuer den Reiter "Nachrichten"
    an ``zustand["ereignisse"]``. Fehlgeschlagene Aktionen tun das nicht.
  * Keine erfundenen Zahlen: was das Handbuch nicht hergibt, steht in
    ``offene_luecken()`` und wird nicht berechnet.

Aufruf der Pruefung:  python -X utf8 tests/test_spielschicht.py
"""
from __future__ import annotations

import json
import os
from functools import lru_cache
from typing import Any, Dict, List, Optional, Tuple

import auftraege  # S4-6c: Handelskarawanen und Karrenladung (Kern-Auftraege)
import botkern   # S4-6c: die EINE Preisfunktion (Handelspreis, Beschaffungskosten)
import einheiten
import forschung
import gebaeude_wirkung as GW
import gelaende
import originalkarten
import kampfbericht
import portalraum
import punkte as PUNKTE
import spieldaten
import spieloekonomie  # EINE Quelle fuer die Warenvoraussetzung (ware_voraussetzung)
import werkstatt
import wirtschaft

STAND = "2026-10-04.1"

STUNDEN_SEKUNDEN = 3600

# Startkarte: feste Saat, damit ein neuer Spielstand immer dieselbe, spielbare
# Karte hat (gleiche Saat -> gleiche Karte, wie gelaende es zusichert).
START_SAAT = 12345

# Belegter Startwert (Handbuch Seite 7): 10 Siedler, 100 Holz, 100 Steine.
START_SIEDLER = 10


# --------------------------------------------------------------------------
# Kleine Griffe
# --------------------------------------------------------------------------

@lru_cache(maxsize=1)
def _rohstoff_ids() -> Tuple[str, ...]:
    """Die neun Originalrohstoffe in der Reihenfolge von ``data/resources.json``."""
    return tuple(str(r["id"]) for r in spieldaten.rohstoffe())


@lru_cache(maxsize=1)
def _preise() -> Dict[str, Dict[str, Any]]:
    """Die Baupreise aus ``data/baupreise.json`` (EINE Quelle, wie main.baukosten)."""
    pfad = os.path.join(spieldaten.projektwurzel(), "data", "baupreise.json")
    with open(pfad, encoding="utf-8") as f:
        return json.load(f)["preise"]


@lru_cache(maxsize=1)
def _warenrezepte() -> Dict[str, Any]:
    """Die Rezepte aus ``data/warenrezepte.json`` - dieselbe Datei, die ``spieloekonomie`` liest.

    Warum das noetig ist: ``werkstatt.einreihen`` bekommt ohne Rezepte ``dauer = None``, und eine
    Ware ohne Dauer wird NIE fertig. Belegt am 05.11.2026: die Spieltest-Simulation reihte 93
    Kurzschwerter ein, keine einzige Ware kam an - im Handbuch ist nur das Schwert (20 Minuten)
    belegt, alle anderen Dauern stehen in dieser Datei.
    """
    pfad = os.path.join(spieldaten.projektwurzel(), "data", "warenrezepte.json")
    with open(pfad, encoding="utf-8") as f:
        return json.load(f)


def _baukosten(gebaeude: str, stufe: int = 1) -> Dict[str, int]:
    """Baupreis eines Gebaeudes fuer ``stufe``.

    Ausbau auf Stufe n kostet das n-fache des Grundpreises (belegte Regel in
    ``data/buildings.json`` / ``data/baupreise.json``). Es werden nur echte
    Rohstoffe und der Posten "siedler" durchgelassen -- die Datei traegt auch
    Begruendungstexte, die keine Kosten sind.
    """
    kennung = gelaende.finde_gebaeude(gebaeude) or gebaeude
    eintrag = _preise().get(kennung) or {}
    faktor = max(1, int(stufe))
    return {r: int(v) * faktor for r, v in eintrag.items()
            if (r in _rohstoff_ids() or r == "siedler") and isinstance(v, (int, float))}


def _kosten_text(kosten: Dict[str, int]) -> str:
    if not kosten:
        return "Preis offen"
    return ", ".join(f"{int(v)} {k}" for k, v in kosten.items())


def _siedlung(zustand: dict, index) -> Optional[dict]:
    """Die Siedlung zum Index -- oder None (kein Rateweg, keine Ausnahme)."""
    try:
        i = int(index)
    except (TypeError, ValueError):
        return None
    liste = zustand.get("siedlungen") or []
    if 0 <= i < len(liste):
        return liste[i]
    return None


def _fehlbetrag(zustand: dict, kosten: Dict[str, int]) -> Dict[str, int]:
    """Was fehlt, um ``kosten`` zu bezahlen (leer = bezahlbar)."""
    fehlt: Dict[str, int] = {}
    for posten, menge in kosten.items():
        if posten == "siedler":
            vorhanden = zustand.get("bevoelkerung", 0) or 0
        else:
            vorhanden = (zustand.get("ressourcen") or {}).get(posten, 0) or 0
        if vorhanden < menge:
            fehlt[posten] = int(menge - vorhanden)
    return fehlt


def _bezahlen(zustand: dict, kosten: Dict[str, int]) -> None:
    """Bucht die Kosten ab (Rohstoffe aus ``ressourcen``, Siedler aus ``bevoelkerung``)."""
    for posten, menge in kosten.items():
        if posten == "siedler":
            zustand["bevoelkerung"] = zustand.get("bevoelkerung", 0) - menge
        else:
            zustand["ressourcen"][posten] = zustand["ressourcen"].get(posten, 0) - menge


def _melde(zustand: dict, text: str, typ: str = "system", zeit: Optional[float] = None) -> dict:
    """Haengt ein Ereignis fuer den Reiter "Nachrichten" an und gibt es zurueck."""
    ereignis = {"zeit": float(zustand.get("zeit", 0.0) if zeit is None else zeit),
                "typ": typ, "text": text}
    zustand.setdefault("ereignisse", []).append(ereignis)
    return ereignis


def _forschungsstaende(zustand: dict) -> Dict[str, int]:
    """{Gebiet: Stufe} aus dem Forschungsstand (fuer wirtschaft und punkte)."""
    return {name: int(eintrag.get("stufe", 0))
            for name, eintrag in (zustand.get("forschung") or {}).items()}


# --------------------------------------------------------------------------
# Neuer Zustand
# --------------------------------------------------------------------------

def neuer_zustand(saat: int = START_SAAT) -> dict:
    """Ein frischer, serialisierbarer Spielstand.

    Enthaelt eine Start-Siedlung mit einer eigenen Siedlungskarte, die neun
    Originalrohstoffe auf ihren belegten Startwerten (100 Holz, 100 Stein, sonst
    0), 10 Siedler, einen leeren Forschungsstand (21 Originalgebiete, alle auf
    Stufe 0), leere Waren-, Einheiten- und Ereignislisten sowie einen leeren
    Werkstatt-Bestand.
    """
    karte = originalkarten.startkarte(saat, "spieler")
    siedlung = {
        "name": "Heimsiedlung",
        "map_id": "heim",
        "karte": karte,
        "bauten": {},
        "stufen": {},
    }
    ressourcen = {r: 0 for r in _rohstoff_ids()}
    ressourcen["holz"] = 100
    ressourcen["stein"] = 100
    return {
        "stand": STAND,
        "zeit": 0.0,
        "letzter_tick": None,
        "ressourcen": ressourcen,
        "bevoelkerung": float(START_SIEDLER),
        "waren": {},
        "einheiten": {},
        "siedlungen": [siedlung],
        "forschung": forschung.neuer_stand(),
        "werkstaetten": {},
        "ruf": 0,
        "seit": 0.0,
        "eigene_dimension": 0,
        "letzter_wechsel": None,
        "ereignisse": [],
        "handels_erloes": 0.0,   # S4-6c: Summe des Handels-Erloeses (0.0 = nie gehandelt)
        "letzter_handel": 0.0,   # S4-6c: Spielzeit der letzten Annahme (0.0 = nie)
        "haendler_gold": float(_handelsregel("haendler_gold", 10000.0)),  # S4-6c: Gold des Handelspartners
    }


# --------------------------------------------------------------------------
# Zeitlauf
# --------------------------------------------------------------------------

def tick(zustand: dict, jetzt: float, sekunden: float) -> dict:
    """Ein Zeitlauf: Ertrag, Siedler, fertige Forschung und fertige Waren.

    ``jetzt`` ist der aktuelle Zeitstempel in Sekunden, ``sekunden`` die seit
    dem letzten Lauf vergangene Zeit. Rueckgabe::

        {'ereignisse': [ ... ], 'geaendert': { ... }}

    Ist ``jetzt`` nicht groesser als der zuletzt verarbeitete Zeitstempel, wird
    NICHTS erneut verarbeitet (Rueckgabe leer). So werden bei zwei Aufrufen mit
    demselben Zeitstempel weder Ertrag noch Ereignisse doppelt verbucht.
    """
    try:
        jetzt = float(jetzt)
        sekunden = float(sekunden)
    except (TypeError, ValueError):
        return {"ereignisse": [], "geaendert": {}}

    letzter = zustand.get("letzter_tick")
    if letzter is not None and jetzt <= float(letzter):
        return {"ereignisse": [], "geaendert": {}}

    zustand["letzter_tick"] = jetzt
    zustand["zeit"] = jetzt
    ereignisse: List[dict] = []
    geaendert: Dict[str, Any] = {}

    siedlungen = zustand.get("siedlungen") or []
    staende = _forschungsstaende(zustand)
    dt_h = sekunden / STUNDEN_SEKUNDEN

    # 1. Rohstoffertrag aus den bebauten Feldern (wirtschaft liefert Lesefassung).
    if dt_h > 0:
        roh = wirtschaft.ertrag_gesamt(siedlungen, staende)
        neu_roh: Dict[str, float] = {}
        for name, rate in roh.items():
            schluessel = name.lower()
            if schluessel in zustand["ressourcen"] and rate:
                zustand["ressourcen"][schluessel] = round(
                    zustand["ressourcen"][schluessel] + rate * dt_h, 2)
                neu_roh[schluessel] = zustand["ressourcen"][schluessel]
        if neu_roh:
            geaendert["ressourcen"] = neu_roh

    # 2. Siedlerzuwachs bis zur Siedlergrenze (gebaeude_wirkung).
    grenze = GW.bevoelkerungsgrenze(siedlungen)
    zuwachs = GW.siedler_zuwachs_pro_stunde(siedlungen, staende) * dt_h
    alt = zustand.get("bevoelkerung", 0) or 0
    neu = min(float(grenze), alt + zuwachs) if zuwachs > 0 else alt
    if neu != alt:
        zustand["bevoelkerung"] = round(neu, 4)
        geaendert["bevoelkerung"] = zustand["bevoelkerung"]

    # 3. Abgelaufene Forschung: die Stufe steigt JETZT.
    for gebiet in forschung.abschliessen(zustand["forschung"], jetzt):
        stufe = int(zustand["forschung"][gebiet]["stufe"])
        ereignisse.append(_melde(
            zustand, f"Forschung {gebiet} auf Stufe {stufe} abgeschlossen.",
            "forschung", jetzt))
        geaendert.setdefault("forschung", {})[gebiet] = stufe

    # 4. Fertige Waren aus den Warteschlangen.
    for schluessel, schlange in (zustand.get("werkstaetten") or {}).items():
        fertig = werkstatt.fertige_waren(schlange, jetzt)
        for ware, menge in fertig.items():
            zustand["waren"][ware] = zustand["waren"].get(ware, 0) + menge
            ereignisse.append(_melde(
                zustand, f"{menge}x {ware} in der Werkstatt fertig.", "werkstatt", jetzt))
            geaendert.setdefault("waren", {})[ware] = zustand["waren"][ware]

    return {"ereignisse": ereignisse, "geaendert": geaendert}


# --------------------------------------------------------------------------
# Siedlungskarte: bauen, ausbauen, abreissen
# --------------------------------------------------------------------------

def bauen(zustand: dict, siedlung_index, gebaeude: str, feld: int) -> Tuple[bool, str]:
    """Setzt ein Gebaeude auf ein freies Feld der Siedlungskarte.

    Geprueft werden: bekannte Siedlung, bekannte Gebaeudeart, Feld auf der Karte,
    freies Feld, Eignung des Gelaendes (``gelaende.bau_moeglich``), die belegte
    Obergrenze je Siedlung und die Baupreise. Bei Erfolg werden die Kosten
    abgebucht, das Feld bekommt Stufe 1 und ein Ereignis wird angelegt. Sonst
    aendert sich nichts.
    """
    s = _siedlung(zustand, siedlung_index)
    if s is None:
        return False, f"Unbekannte Siedlung (Index {siedlung_index})."
    kennung = gelaende.finde_gebaeude(gebaeude)
    if not kennung:
        return False, f"Unbekanntes Gebäude: {gebaeude}."
    karte = s.get("karte") or {}
    raster = karte.get("raster") or []
    try:
        feld_i = int(feld)
    except (TypeError, ValueError):
        return False, f"Ungültige Feldnummer: {feld}."
    if not (0 <= feld_i < len(raster)):
        return False, f"Feld {feld} liegt nicht auf der Karte."
    if str(feld_i) in (s.get("bauten") or {}):
        return False, (f"Feld {feld_i} ist bereits belegt "
                       f"({s['bauten'][str(feld_i)]}) -- erst abreissen.")
    erlaubt, warum = gelaende.bau_moeglich(kennung, raster[feld_i])
    if not erlaubt:
        return False, warum
    eintrag = gelaende.alle_gebaeude().get(kennung) or {}
    grenze = eintrag.get("max_je_siedlung")
    if isinstance(grenze, int) and grenze > 0 and GW.gebaeude_stufe(s, kennung) >= grenze:
        return False, (f"{eintrag.get('name', kennung)} gibt es höchstens {grenze}x je "
                       f"Siedlung (belegte Originalregel).")
    kosten = _baukosten(kennung, 1)
    fehlt = _fehlbetrag(zustand, kosten)
    if fehlt:
        return False, f"Zu wenig für {eintrag.get('name', kennung)}: es fehlen {_kosten_text(fehlt)}."
    _bezahlen(zustand, kosten)
    s.setdefault("bauten", {})[str(feld_i)] = kennung
    s.setdefault("stufen", {})[str(feld_i)] = 1
    _melde(zustand, f"{eintrag.get('name', kennung)} auf Feld {feld_i} gebaut "
                    f"(Kosten {_kosten_text(kosten)}).", "bau")
    return True, f"{warum} (Feld {feld_i})"


def _volk_preis_faktor(siedlung) -> float:
    """Faktor auf Gebaeudepreise aus dem Volk des Ortes (V-5, 03.11.2026) - 1,0 ohne Volk.

    Das Volk steht am Ort (Feld `volk`); die Zahlen liest `boni.py` aus `data/boni.json`. Diese
    Schicht liest die Datei nicht selbst - sie fragt die Datenschicht (wie `bottaktik`).
    """
    fraktion = str((siedlung or {}).get("volk") or "") if isinstance(siedlung, dict) else ""
    if not fraktion:
        return 1.0
    try:
        import boni
    except Exception:                                  # noqa: BLE001 - ohne Modul kein Rabatt
        return 1.0
    return boni.preis_faktor(fraktion)


def _kosten_mit_volk(kosten: Dict[str, int], siedlung) -> Dict[str, int]:
    """Ausbaupreis mit dem Volksrabatt; Siedler bleiben unangetastet (Menschen, keine Ware)."""
    preis_faktor = _volk_preis_faktor(siedlung)
    if abs(preis_faktor - 1.0) < 1e-9:
        return kosten
    return {stoff: (wert if str(stoff) == "siedler"
                    else max(0, int(round(float(wert) * preis_faktor))))
            for stoff, wert in kosten.items()}


def ausbauen(zustand: dict, siedlung_index, feld: int) -> Tuple[bool, str]:
    """Erhoeht die Ausbaustufe eines Gebaeudes auf einem Feld um 1.

    Nur moeglich, wenn das Gebaeude auf dem Feld steht UND fuer es eine
    Ausbaustufe belegt ist (Wall 10, Bibliothek und die drei Ausbildungsstaetten
    je 5 -- ``data/gebaeude_wirkung.json``). Ausbau auf Stufe n kostet das
    n-fache des Grundpreises. Sonst aendert sich nichts.
    """
    s = _siedlung(zustand, siedlung_index)
    if s is None:
        return False, f"Unbekannte Siedlung (Index {siedlung_index})."
    try:
        feld_i = int(feld)
    except (TypeError, ValueError):
        return False, f"Ungültige Feldnummer: {feld}."
    bauten = s.get("bauten") or {}
    if str(feld_i) not in bauten:
        return False, f"Auf Feld {feld_i} steht kein Gebäude."
    kennung = gelaende.finde_gebaeude(bauten[str(feld_i)])
    if not kennung:
        return False, f"Unbekanntes Gebäude auf Feld {feld_i}."
    name = gelaende.gebaeude_name(kennung)
    hoechste = GW.max_stufe(kennung)
    if hoechste is None:
        return False, (f"Für {name} ist kein Ausbau belegt -- das Handbuch nennt "
                       f"keine Stufen.")
    aktuelle = GW.stufe_von_feld(s, str(feld_i))
    if aktuelle >= hoechste:
        return False, f"{name} hat die höchste belegte Stufe {hoechste} erreicht."
    neue = aktuelle + 1
    kosten = _kosten_mit_volk(_baukosten(kennung, neue), s)
    fehlt = _fehlbetrag(zustand, kosten)
    if fehlt:
        return False, f"Zu wenig für den Ausbau von {name}: es fehlen {_kosten_text(fehlt)}."
    _bezahlen(zustand, kosten)
    s.setdefault("stufen", {})[str(feld_i)] = neue
    _melde(zustand, f"{name} auf Feld {feld_i} auf Stufe {neue} ausgebaut "
                    f"(Kosten {_kosten_text(kosten)}).", "bau")
    return True, f"{name} ist jetzt Stufe {neue} (Feld {feld_i})."


def abreissen(zustand: dict, siedlung_index, feld: int) -> Tuple[bool, str]:
    """Reisst das Gebaeude auf einem Feld ab; das Feld wird wieder frei.

    Belegte Originalregel (``data/buildings.json``): "Ein Abriss bringt keine
    Rohstoffe zurueck; nur das Feld wird wieder frei." Es wird also nichts
    erstattet. Sonst aendert sich nichts.
    """
    s = _siedlung(zustand, siedlung_index)
    if s is None:
        return False, f"Unbekannte Siedlung (Index {siedlung_index})."
    try:
        feld_i = int(feld)
    except (TypeError, ValueError):
        return False, f"Ungültige Feldnummer: {feld}."
    bauten = s.get("bauten") or {}
    if str(feld_i) not in bauten:
        return False, f"Auf Feld {feld_i} steht kein Gebäude."
    kennung = gelaende.finde_gebaeude(bauten[str(feld_i)])
    name = gelaende.gebaeude_name(kennung) if kennung else bauten[str(feld_i)]
    del s["bauten"][str(feld_i)]
    (s.get("stufen") or {}).pop(str(feld_i), None)
    _melde(zustand, f"{name} auf Feld {feld_i} abgerissen -- keine Erstattung, "
                    f"das Feld ist wieder frei.", "bau")
    return True, f"{name} auf Feld {feld_i} abgerissen (Feld frei)."


# --------------------------------------------------------------------------
# Forschung
# --------------------------------------------------------------------------

def forschung_starten(zustand: dict, gebiet: str, jetzt: float) -> Tuple[bool, str]:
    """Startet die naechste Forschungsstufe eines Gebiets.

    Voraussetzung ist eine Bibliothek (``gebaeude_wirkung.forschung_erlaubt``).
    Die Kosten werden sofort abgebucht, die STUFE STEIGT ERST nach der
    Forschungszeit -- ``tick`` mit dem passenden Zeitstempel schliesst ab. Bei
    einer Ablehnung aendert sich nichts.
    """
    erlaubt, warum = GW.forschung_erlaubt(zustand.get("siedlungen") or [])
    if not erlaubt:
        return False, warum
    ok, meldung = forschung.starten(gebiet, zustand["forschung"], float(jetzt),
                                    True, zustand["ressourcen"])
    if ok:
        _melde(zustand, meldung, "forschung", jetzt)
    return ok, meldung


def forschung_stand(zustand: dict, jetzt: float) -> dict:
    """Forschungsstand je Gebiet; laufende Auftraege tragen ``reststunden``."""
    return forschung.fortschritt(zustand["forschung"], float(jetzt))


# --------------------------------------------------------------------------
# Ausbildung
# --------------------------------------------------------------------------

def ausbilden(zustand: dict, einheit: str) -> Tuple[bool, str]:
    """Bildet EINE Einheit aus, wenn die passende Ausbildungsstaette steht.

    Die Staette kommt aus ``gebaeude_wirkung.ausbildungsstaette`` (Feld
    "gebaeude" je Einheit in ``data/units.json``): Kriegerakademie ->
    Kampfeinheiten, Diebesgilde -> Kundschafter, Stellmacher -> Karren und
    Belagerungswaffen. Die Kosten und die ggf. noetigen Waren aus dem Lager
    werden geprueft und gebucht. Bei einer Ablehnung aendert sich nichts.
    """
    eintrag = einheiten.alle().get(einheit)
    if not eintrag:
        return False, f"Unbekannte Einheit: {einheit}."
    da, kennung, stufe = GW.ausbildungsstaette(zustand.get("siedlungen") or [], einheit)
    if not da:
        gebaeude = kennung or eintrag.get("gebaeude") or "die passende Ausbildungsstätte"
        return False, f"{einheit} braucht {gelaende.gebaeude_name(gebaeude)} -- nicht gebaut."
    waren = eintrag.get("waren") or []
    fehl_waren = [w for w in waren if (zustand.get("waren") or {}).get(w, 0) < 1]
    if fehl_waren:
        return False, f"Im Lager fehlen für {einheit}: {', '.join(fehl_waren)}."
    kosten = dict(eintrag.get("kosten") or {})
    fehlt = _fehlbetrag(zustand, kosten)
    if fehlt:
        return False, f"Zu wenig für {einheit}: es fehlen {_kosten_text(fehlt)}."
    _bezahlen(zustand, kosten)
    for w in waren:
        zustand["waren"][w] = zustand["waren"].get(w, 0) - 1
    zustand["einheiten"][einheit] = zustand["einheiten"].get(einheit, 0) + 1
    _melde(zustand, f"1x {einheit} in {gelaende.gebaeude_name(kennung)} ausgebildet "
                    f"(Stufe {stufe}, Kosten {_kosten_text(kosten)}).", "ausbildung")
    return True, f"1x {einheit} ausgebildet."


# --------------------------------------------------------------------------
# Werkstatt
# --------------------------------------------------------------------------

def ware_fertigen(zustand: dict, siedlung_index, ware: str, anzahl: int,
                  jetzt: float) -> Tuple[bool, str]:
    """Stellt eine Ware in die Warteschlange der passenden Werkstatt.

    Die Werkstatt (Schmiede/Bogenbauer/Naehstube) muss in dieser Siedlung
    gebaut sein; mehrere gleiche Werkstaetten fertigen parallel (belegtes
    Handbuchbeispiel: 10 Schwerter a 20 Minuten mit zwei Schmieden = 100 min).
    Die Fertigung selbst laeuft ueber ``tick``. Bei einer Ablehnung aendert sich
    nichts.

    Seit 05.11.2026 werden VORAUSSETZUNG und MATERIAL wie im GUI-Weg geprueft und bezahlt
    (Befund Register 233: vorher entstanden Waren hier umsonst und ohne Forschung, weil nur
    `spieloekonomie.ware_start_menge` die Rezeptkosten bucht). Die Voraussetzung liest dieselbe
    Funktion wie der GUI-Weg (`spieloekonomie.ware_voraussetzung`), damit es EINE Wahrheit bleibt.
    """
    s = _siedlung(zustand, siedlung_index)
    if s is None:
        return False, f"Unbekannte Siedlung (Index {siedlung_index})."
    if ware not in (spieldaten.waren() or {}):
        return False, f"Unbekannte Ware: {ware}."
    try:
        menge = int(anzahl)
    except (TypeError, ValueError):
        return False, "Die Anzahl muss eine ganze Zahl sein."
    if menge <= 0:
        return False, "Die Anzahl muss größer als 0 sein."
    rezepte = _warenrezepte()
    rezept = rezepte.get(ware) or {}
    kennung = werkstatt.werkstatt_fuer(ware)
    if not kennung:
        return False, f"Für '{ware}' ist keine Werkstatt bekannt."
    bestand = werkstatt.werkstaetten_bestand([s]).get(kennung, 0)
    if bestand < 1:
        return False, (f"Keine {gelaende.gebaeude_name(kennung)} in dieser Siedlung -- "
                       f"erst bauen.")
    # Materialkosten je Stueck aus dem Rezept, mal Menge; atomar (alles oder nichts).
    # Die Forschungsvoraussetzung steht bewusst NACH der Werkstatt: dem Spieler zuerst das
    # fehlende Gebaeude nennen, dann die fehlende Forschung (dieselbe Lesestelle wie der GUI-Weg).
    erfuellt, begruendung = spieloekonomie.ware_voraussetzung(ware, _forschungsstaende(zustand),
                                                              rezepte)
    if not erfuellt:
        return False, f"Warenvoraussetzung fehlt: {begruendung}"
    kosten = {roh: int(wert) * menge for roh, wert in (rezept.get("kosten") or {}).items()}
    fehlt = _fehlbetrag(zustand, kosten)
    if fehlt:
        return False, (f"Lokales Lager reicht nicht. Für {menge}x {ware} fehlen "
                       f"{_kosten_text(fehlt)}.")
    stufe = werkstatt.werkstatt_stufe(s, kennung) or 1
    schluessel = f"{int(siedlung_index)}:{kennung}"
    zustand.setdefault("werkstaetten", {})
    schlange = zustand["werkstaetten"].get(schluessel)
    if schlange is None:
        schlange = werkstatt.neue_warteschlange(kennung, bestand)
        zustand["werkstaetten"][schluessel] = schlange
    else:
        schlange["werkstaetten"] = bestand
        schlange["kapazitaet"] = werkstatt.kapazitaet(bestand)
    _bezahlen(zustand, kosten)                          # abbuchen, dann einreihen
    ok, meldung = werkstatt.einreihen(schlange, ware, menge, stufe, rezepte)
    if not ok:
        # Rueckbuchung: ein abgelehnter Auftrag darf nichts kosten (keine Teilabbuchung).
        for roh, wert in kosten.items():
            zustand["ressourcen"][roh] = zustand["ressourcen"].get(roh, 0) + wert
        return False, meldung
    werkstatt.fortschritt(schlange, float(jetzt))       # Uhr stellen (Startzeitpunkt)
    _melde(zustand, meldung, "werkstatt", jetzt)
    return True, meldung


# --------------------------------------------------------------------------
# Kampf
# --------------------------------------------------------------------------

def angriff(zustand: dict, ziel: dict, jetzt: float,
            rng=None) -> Tuple[bool, dict]:
    """Ein Angriff gegen ein Ziel -- ueber ``kampfbericht``.

    ``ziel`` beschreibt den Angegriffenen::

        {"wall_stufe": int, "wall_zustand_prozent": float,
         "vorraete": {rohstoff: menge}}

    Geprueft wird die Vorrunde (Wallschwellen). Ist sie bestanden, wird der
    Mauerschaden gewuerfelt, die Beute nach Karrenladung bemessen und alles ueber
    ``kampfbericht.spieldaten_anwenden`` in den Stand gebucht. Rueckgabe:
    ``(ok, {bestanden, vorrunde, mauer_schaden, beute, bericht, ergebnis})``.
    Ohne Angriffseinheiten und bei nicht bestandener Vorrunde: ``(False, ...)``
    ohne Aenderung am Zustand (der Bericht steht trotzdem im Ergebnis).
    """
    krieger: Dict[str, int] = {}
    belagerung: Dict[str, int] = {}
    for name, anzahl in (zustand.get("einheiten") or {}).items():
        if int(anzahl or 0) <= 0:
            continue
        rolle = einheiten.rolle(name)
        if rolle in ("kaempfer", "kundschafter"):
            krieger[name] = int(anzahl)
        elif rolle == "belagerung":
            belagerung[name] = int(anzahl)
    if not krieger and not belagerung:
        return False, {"bestanden": False,
                       "grund": "Keine Kämpfer und keine Belagerungswaffen vorhanden."}

    fuss = sum(einheiten.kampfstaerke(n, a) for n, a in krieger.items())
    bel = sum(einheiten.kampfstaerke(n, a) for n, a in belagerung.items())
    z = ziel or {}
    wall_stufe = int(z.get("wall_stufe", 0) or 0)
    wall_zustand = float(z.get("wall_zustand_prozent", 100.0))

    vor = kampfbericht.vorrunde(fuss, bel, wall_stufe, wall_zustand)
    ergebnis: Dict[str, Any] = {
        "ausgang": "unentschieden",
        "mauer_zustand": wall_zustand,
        "verluste_angreifer": {},
        "verluste_verteidiger": {},
        "beute": {},
        "bericht": vor["grund"],
    }

    if not vor["bestanden"]:
        ergebnis["ausgang"] = "verteidiger"
        ber = kampfbericht.bericht(ergebnis)
        return False, {"bestanden": False, "vorrunde": vor, "mauer_schaden": None,
                       "beute": {}, "bericht": ber, "ergebnis": ergebnis}

    schaden = kampfbericht.mauer_schaden(belagerung, wall_stufe, wall_zustand, rng)
    ergebnis["mauer_zustand"] = schaden["mauer_zustand_prozent"]
    beute = kampfbericht.beute(zustand.get("einheiten") or {}, z.get("vorraete") or {}, rng)
    ergebnis["beute"] = beute
    ergebnis["ausgang"] = "angreifer"
    if belagerung:
        ergebnis["belagerung"] = {n: a for n, a in belagerung.items()}

    neu = kampfbericht.spieldaten_anwenden(zustand, ergebnis)
    zustand.clear()
    zustand.update(neu)

    ber = kampfbericht.bericht(ergebnis)
    beute_text = ", ".join(f"{k} {v}" for k, v in sorted(beute.items())) or "keine"
    _melde(zustand, f"{ber['titel']} -- Beute: {beute_text}.", "kampf", jetzt)
    return True, {"bestanden": True, "vorrunde": vor, "mauer_schaden": schaden,
                  "beute": beute, "bericht": ber, "ergebnis": ergebnis}


# --------------------------------------------------------------------------
# Handel mit einem fremden Haendler (S4-6c, 07.11.2026, Register 292)
# --------------------------------------------------------------------------
# Die Messschicht hatte BISHER weder Handel noch Bots: das Kennzahlenblatt zeigte `handelspunkte`
# als `null`, weil der Zaehler `handels_erloes` im Spielstand nie entstand. Diese Funktion
# schliesst die Luecke - sie benutzt DEN KERN (`spieloekonomie.handel_start` mit
# `karawane_seite="verkaeufer"` und `spieloekonomie.handel_abschluss`) und baut KEINE zweite
# Preisrechnung: der Preis kommt aus `botkern.handelspreis`, also derselben Funktion wie im Spiel.
# Der Spieler VERKAUFT, der fremde Haendler KAUFT und zahlt - die Richtung hat Daniel am
# 07.11.2026 mit Antwort A auf Frage F-12 entschieden (der Erloes gehoert dem Verkaeufer).
#
# VEREINFACHUNG der Messschicht (bewusst, nicht im Spiel): es gibt keinen Bot mit eigener
# Wirtschaft. Der Haendler ist darum ein Handelspartner mit einem festen Goldvorrat
# (`data/handelsmessung.json`) und einem festen Abstand; er nimmt an, weil der Kern beim Verkauf
# den Verkaeufer (den Spieler) annehmen laesst. Ankunft und Rueckkehr werden SOFORT abgerechnet -
# die Reisezeit steht im Vertrag und im Zeitstempel, aber der Lauf wartet nicht auf sie. Das ist
# der einzige Unterschied zum App-Weg; gebucht wird nach DENSELBEN Regeln (`abgerechnet` genau
# einmal, `erloes` auf den Verkaeufer).

@lru_cache(maxsize=1)
def _handelsregeln() -> Dict[str, Any]:
    """Die Regeln der Messschicht aus ``data/handelsmessung.json`` (fehlt die Datei: leeres dict)."""
    pfad = os.path.join(spieldaten.projektwurzel(), "data", "handelsmessung.json")
    try:
        with open(pfad, encoding="utf-8") as f:
            daten = json.load(f)
    except (OSError, ValueError):
        return {}
    return daten if isinstance(daten, dict) else {}


def _handelsregel(name: str, vorgabe):
    """EIN Regelwert - fehlt er in der Datei, gilt die Vorgabe aus dem Code (nie raten)."""
    wert = _handelsregeln().get(name, vorgabe)
    return vorgabe if wert is None else wert


def _schwellenpreis() -> float:
    """Der Handels-Schwellenpreis JE EINHEIT - ``botkern.handelspreis``, Temperament 0,0.

    Kein zweiter Preisweg und keine abgeschriebene Zahl: die Beschaffungskosten stehen als
    ``botkern.BESCHAFFUNGSKOSTEN`` an EINER Stelle (dieselbe, die das Spiel liest), und
    `referenzpreis_aus_beschaffung`/`handelspreis` sind die belegten Funktionen dazu.
    """
    referenz = botkern.referenzpreis_aus_beschaffung(botkern.BESCHAFFUNGSKOSTEN)
    return float(botkern.handelspreis(referenz, 0.0))


def _handels_felder(zustand: dict) -> None:
    """Zieht die Handelsfelder in einen ALTEN Stand nach (Ladewache, idempotent).

    Ein Spielstand von vor dem 07.11.2026 traegt die Felder nicht; ohne sie muesste jede
    Lesestelle `get` mit Vorgabe rufen. `letzter_handel = 0.0` heisst NIE gehandelt (dieselbe
    Lesart wie im App-Spielstand).
    """
    if not isinstance(zustand, dict):
        return
    zustand.setdefault("handels_erloes", 0.0)
    zustand.setdefault("letzter_handel", 0.0)
    if "haendler_gold" not in zustand:                          # alter Stand: frischer Partner
        zustand["haendler_gold"] = float(_handelsregel("haendler_gold", 10000.0))


def _karawanen(zustand: dict) -> Dict[str, int]:
    """Die Handelskarawanen im Reichsheer als ``{Name: Anzahl}`` (nur diese duerfen handeln)."""
    return {str(n): int(a) for n, a in (zustand.get("einheiten") or {}).items()
            if int(a or 0) > 0 and "Handelskarawane" in str(n)}


def _spieler_ort(zustand: dict) -> dict:
    """Der eigene Ort als dict, wie ihn ``spieloekonomie.handel_start`` erwartet.

    Die Messschicht kennt keine Ortslager: das Reichslager IST das Lager des Ortes. `importiert`
    bleibt leer - die Messschicht fuehrt keine Importherkunft, und der Kern liest sie mit `get`.
    """
    return {
        "id": "spieler",                                       # Kennung in den `orte` des Kerns
        "besitzer": "spieler",                                  # eigener Besitz
        "dimension": int(zustand.get("eigene_dimension", 0) or 0),   # gleiche Weltkarte
        "x": 0,                                                 # Messschicht ohne Koordinaten
        "y": 0,                                                 # Messschicht ohne Koordinaten
        "vorraete": dict(zustand.get("ressourcen") or {}),      # das Reichslager
        "waren": dict(zustand.get("waren") or {}),              # Fertigwaren
        "importiert": {},                                       # keine Importherkunft
        "einheiten": dict(zustand.get("einheiten") or {}),      # das Reichsheer
    }


def _haendler_ort(zustand: dict, gold: float) -> dict:
    """Der fremde Haendler als dict - festes Gold, keine Einheiten, kein Lager."""
    return {
        "id": "haendler",                                       # Kennung in den `orte` des Kerns
        "besitzer": "fremd",                                    # fremder Besitz (Kern verlangt das)
        "dimension": int(zustand.get("eigene_dimension", 0) or 0),   # gleiche Weltkarte
        "x": int(_handelsregel("abstand_felder", 6)),           # Abstand -> Reisezeit
        "y": 0,                                                 # Messschicht ohne Koordinaten
        "vorraete": {"gold": float(gold)},                      # sein Gold ist die Gegenleistung
        "waren": {},                                            # er verkauft nichts
        "importiert": {},                                       # keine Importherkunft
        "einheiten": {},                                        # er faehrt nicht selbst
    }


def verkauf_an_haendler(zustand: dict, jetzt: float) -> Tuple[bool, dict]:
    """Einen UEBERSCHUSS an einen fremden Haendler verkaufen - der Handels-Schritt der Messschicht.

    Ablauf (alles ueber den Kern, nichts nachgebaut):

    1. Ohne Handelskarawane gibt es keinen Handel (belegte Regel: nur Handelskarawanen handeln).
    2. Verkauft wird der Rohstoff mit dem groessten Ueberschuss ueber dem Mindestvorrat; Gold
       selbst nie (es ist die Gegenleistung).
    3. Die Menge ist begrenzt durch Ueberschuss, Karrenladung und das Gold des Haendlers.
    4. ``spieloekonomie.handel_start`` sperrt Ware und Gold; ``handel_abschluss`` bucht Ankunft
       (Gold fliesst) und Rueckkehr (Karre heim) - hier sofort, siehe Vereinfachung oben.
    5. Gebucht wird ``handels_erloes`` und ``letzter_handel`` GENAU EINMAL je Vertrag, nach
       denselben Regeln wie im App-Weg (`_fremdvertrag_buchen`).

    Rueckgabe ``(ok, {ware, menge, preis, erloes, karawane, ankunft, meldung})``. Bei ``ok=False``
    bleibt der Zustand unveraendert und ``grund`` nennt den Grund.
    """
    _handels_felder(zustand)                                   # alte Staende nachziehen
    karawanen = _karawanen(zustand)                             # nur Handelskarawanen handeln
    if not karawanen:
        return False, {"grund": "Keine Handelskarawane im Reichsheer."}
    bestand = zustand.get("ressourcen") or {}                   # das Reichslager
    mindest = float(_handelsregel("mindestvorrat", 200))         # was im Lager bleiben soll
    ueber = {str(r): float(m) - mindest for r, m in bestand.items()
             if str(r) in _rohstoff_ids() and str(r) != "gold" and float(m) - mindest >= 1.0}
    if not ueber:                                               # nichts ueber dem Mindestvorrat
        return False, {"grund": "Kein Rohstoff über dem Mindestvorrat."}
    ware = max(ueber, key=lambda r: ueber[r])                    # groesster Ueberschuss zuerst
    preis = _schwellenpreis()                                    # EINE Preisfunktion
    if preis <= 0:                                               # ohne Preis kein Handel
        return False, {"grund": "Kein Schwellenpreis verfügbar."}
    gold = float(zustand.get("haendler_gold") or 0.0)             # Gold des Handelspartners
    if gold <= 0.0:                                               # er ist leergekauft
        return False, {"grund": "Der Handelshaushalt ist leer."}
    ladung = int(auftraege.ladung_der_mission(karawanen, _forschungsstaende(zustand)))
    menge = int(min(ueber[ware], float(ladung), gold // preis))
    if menge < 1:                                                # Ueberschuss oder Gold zu klein
        return False, {"grund": "Menge unter 1: Überschuss oder Gold des Händlers zu klein."}
    verkaeufer = _spieler_ort(zustand)                            # der Spieler verkauft
    kaeufer = _haendler_ort(zustand, gold)                        # der Haendler kauft
    try:                                                          # der KERN entscheidet und sperrt
        kaeufer_neu, verkaeufer_neu, vertrag = spieloekonomie.handel_start(
            kaeufer, verkaeufer, karawanen, ware, menge, preis, "vorraete", float(jetzt),
            forschung=_forschungsstaende(zustand), karawane_seite="verkaeufer")
    except ValueError as fehler:                                  # Grund aus dem Kern, nichts gebucht
        return False, {"grund": str(fehler)}
    vertrag["richtung"] = "verkauf"                               # Buchstelle erkennt die Richtung
    vertrag["von"] = "Heimsiedlung"                               # Absender (Meldung)
    vertrag["nach"] = "Fremder Händler"                           # Empfaenger (Meldung)
    orte = {"spieler": verkaeufer_neu, "haendler": kaeufer_neu}   # beide Seiten fuer den Abschluss
    neu, m = spieloekonomie.handel_abschluss(vertrag, orte, float(vertrag["ankunft"]))
    neu, m = spieloekonomie.handel_abschluss(m, neu, float(m["rueckkehr"]))
    spieler_neu = (neu or {}).get("spieler") or verkaeufer_neu    # Ergebnis des Spielerorts
    zustand["ressourcen"] = dict(spieler_neu.get("vorraete") or {})   # Lager zurueckschreiben
    zustand["waren"] = dict(spieler_neu.get("waren") or {})           # Waren zurueckschreiben
    zustand["einheiten"] = dict(spieler_neu.get("einheiten") or {})   # Karre ist heim
    zustand["haendler_gold"] = float((kaeufer_neu.get("vorraete") or {}).get("gold") or 0.0)
    erloes = float(m.get("erloes") or 0.0)                        # Einnahme des Verkaeufers
    gebucht = False                                               # wurde der Zaehler erhoeht
    if m.get("abgerechnet") and m.get("angenommen") and erloes > 0.0:
        zustand["handels_erloes"] = float(zustand.get("handels_erloes") or 0.0) + erloes
        zustand["letzter_handel"] = float(m.get("ankunft") or jetzt)
        gebucht = True
    meldung = (f"{menge}x {str(ware).capitalize()} an einen fremden Händler verkauft: "
               f"{erloes:g} Gold eingenommen ({preis:g} je Stück).")
    _melde(zustand, meldung, "handel", jetzt)                     # Ereignis fuer die Nachrichten
    return True, {"ware": ware, "menge": menge, "preis": preis, "erloes": erloes,
                  "karawane": dict(karawanen), "ankunft": float(m.get("ankunft") or jetzt),
                  "gebucht": gebucht, "meldung": meldung}


# --------------------------------------------------------------------------
# Punkte
# --------------------------------------------------------------------------

def punkte(zustand: dict, jetzt: float) -> dict:
    """Alle Punktarten aus ``src/punkte.py``.

    Forschungspunkte (Stufe hoch drei), Kriegspunkte (Einheitenwerte + Wallstufe
    hoch drei), Gesamtpunktzahl (halbe Summe), Ruf, Goetterschutz und den
    Spielausgang (kein Sieg - E5, Niederlage nur ohne Siedlung und Einheit).
    """
    staende = _forschungsstaende(zustand)
    einh = zustand.get("einheiten") or {}
    wall = GW.wall_stufe(zustand.get("siedlungen") or [])
    gesamt = PUNKTE.gesamtpunkte(staende, einh, wall)
    lage, grund = PUNKTE.spielausgang({
        "siedlungen": zustand.get("siedlungen") or [],
        "einheiten": einh,
        "punkte": gesamt,
    })
    return {
        "forschungspunkte": PUNKTE.forschungspunkte(staende),
        "kriegspunkte": PUNKTE.kriegspunkte(einh, wall),
        "gesamtpunkte": gesamt,
        "ruf": PUNKTE.rufpunkte(zustand.get("ruf", 0)),
        "wall_stufe": wall,
        "goetterschutz": PUNKTE.goetterschutz_aktiv(zustand.get("seit", 0.0), float(jetzt)),
        "lage": lage,
        "lage_grund": grund,
    }


# --------------------------------------------------------------------------
# Portal (Zusatz, Paket W5)
# --------------------------------------------------------------------------

def portalwechsel(zustand: dict, nach_dimension, jetzt: float) -> Tuple[bool, str]:
    """Verschiebungsritual in eine andere Dimension (``portalraum``, W5).

    ZAEHLWEISE-HINWEIS (Schnitt S-2b, 01.11.2026): dieser Zustand fuehrt
    ``eigene_dimension`` als INDEX 0..19 (``neuer_zustand`` setzt 0), waehrend der
    Spielstand in ``main.py`` die 1-basierte NUMMER aus der Kennung fuehrt (d04 -> 4).
    ``portalraum`` rechnet ebenfalls mit dem Index, deshalb bleibt es hier beim Index -
    nicht "vereinheitlichen", ohne den Aufrufer mitzuziehen.

    Belegt: 5.000 Mana aus EINER Siedlung, hoechstens einmal je 24 Stunden. Das
    Mana wird hier aus dem gemeinsamen Rohstoffvorrat genommen (der Stand fuehrt
    kein Mana je Siedlung). Bei einer Ablehnung aendert sich nichts.
    """
    von = int(zustand.get("eigene_dimension", 0) or 0)
    mana = (zustand.get("ressourcen") or {}).get("mana", 0) or 0
    erlaubt, meldung = portalraum.wechsel_erlaubt(
        von, nach_dimension, mana, zustand.get("letzter_wechsel"), float(jetzt))
    if not erlaubt:
        return False, meldung
    try:
        gebucht = portalraum.nach_wechsel(mana, float(jetzt))
    except ValueError as e:
        return False, str(e)
    zustand["ressourcen"]["mana"] = gebucht["mana"]
    zustand["letzter_wechsel"] = gebucht["letzter_wechsel"]
    zustand["eigene_dimension"] = int(nach_dimension)
    _melde(zustand, meldung, "portal", jetzt)
    return True, meldung


# --------------------------------------------------------------------------
# Nachrichten und offene Luecken
# --------------------------------------------------------------------------

def ereignisse(zustand: dict) -> list:
    """Alle Ereignisse fuer den Reiter "Nachrichten" (neueste zuletzt)."""
    return list(zustand.get("ereignisse") or [])


def offene_luecken() -> dict:
    """Was diese Schicht NICHT kann -- ehrliche Liste, kein erfundener Ersatz.

    Enthaelt die Luecken der eingebundenen Kindmodule sowie die Aktionen, die
    absichtlich fehlen (z. B. Auftraege, solange ``src/auftraege.py`` fehlt).
    """
    luecken: Dict[str, Any] = {
        "auftraege": ("src/auftraege.py ist noch nicht vorhanden -- 'auftrag_starten' "
                      "ist darum NICHT eingebaut (nichts erfunden)."),
        "ausbildungsdauer": ("Das Handbuch nennt keine Ausbildungsdauer; ausbilden ist "
                             "darum sofort (keine erfundene Wartezeit)."),
        "werkstatt_dauer": ("Nur für das Schwert ist die Fertigungsdauer belegt (20 Min). "
                            "Andere Waren laufen ohne Dauer in der Warteschlange."),
        "baukunst": ("Die Forschung 'Baukunst' als Bauvoraussetzung wird nicht geprüft: "
                     "die 21 Originalforschungen sind zwar im Spiel, aber die Zuordnung "
                     "je Gebäude ist noch offen."),
        "kampfverluste": ("Verluste einzelner Einheiten rechnet der (nicht eingebundene) "
                          "Kampfablauf; 'angriff' nutzt Vorrunde, Mauerschaden und Beute "
                          "aus kampfbericht."),
        "portal_mana_je_siedlung": ("portalwechsel nimmt das Mana aus dem gemeinsamen "
                                    "Vorrat; der Stand führt kein Mana je Siedlung."),
        "gebaeude_wirkung_luecken": GW.luecken(),
        "kampfbericht_luecken": kampfbericht.offene_luecken(),
    }
    return luecken
