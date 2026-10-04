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

import einheiten
import forschung
import gebaeude_wirkung as GW
import gelaende
import kampfbericht
import portalraum
import punkte as PUNKTE
import spieldaten
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
    karte = gelaende.siedlungskarte_erzeugen(saat)
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
        return False, f"Unbekanntes Gebaeude: {gebaeude}."
    karte = s.get("karte") or {}
    raster = karte.get("raster") or []
    try:
        feld_i = int(feld)
    except (TypeError, ValueError):
        return False, f"Ungueltige Feldnummer: {feld}."
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
        return False, (f"{eintrag.get('name', kennung)} gibt es hoechstens {grenze}x je "
                       f"Siedlung (belegte Originalregel).")
    kosten = _baukosten(kennung, 1)
    fehlt = _fehlbetrag(zustand, kosten)
    if fehlt:
        return False, f"Zu wenig fuer {eintrag.get('name', kennung)}: es fehlen {_kosten_text(fehlt)}."
    _bezahlen(zustand, kosten)
    s.setdefault("bauten", {})[str(feld_i)] = kennung
    s.setdefault("stufen", {})[str(feld_i)] = 1
    _melde(zustand, f"{eintrag.get('name', kennung)} auf Feld {feld_i} gebaut "
                    f"(Kosten {_kosten_text(kosten)}).", "bau")
    return True, f"{warum} (Feld {feld_i})"


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
        return False, f"Ungueltige Feldnummer: {feld}."
    bauten = s.get("bauten") or {}
    if str(feld_i) not in bauten:
        return False, f"Auf Feld {feld_i} steht kein Gebaeude."
    kennung = gelaende.finde_gebaeude(bauten[str(feld_i)])
    if not kennung:
        return False, f"Unbekanntes Gebaeude auf Feld {feld_i}."
    name = gelaende.gebaeude_name(kennung)
    hoechste = GW.max_stufe(kennung)
    if hoechste is None:
        return False, (f"Fuer {name} ist kein Ausbau belegt -- das Handbuch nennt "
                       f"keine Stufen.")
    aktuelle = GW.stufe_von_feld(s, str(feld_i))
    if aktuelle >= hoechste:
        return False, f"{name} hat die hoechste belegte Stufe {hoechste} erreicht."
    neue = aktuelle + 1
    kosten = _baukosten(kennung, neue)
    fehlt = _fehlbetrag(zustand, kosten)
    if fehlt:
        return False, f"Zu wenig fuer den Ausbau von {name}: es fehlen {_kosten_text(fehlt)}."
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
        return False, f"Ungueltige Feldnummer: {feld}."
    bauten = s.get("bauten") or {}
    if str(feld_i) not in bauten:
        return False, f"Auf Feld {feld_i} steht kein Gebaeude."
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
        gebaeude = kennung or eintrag.get("gebaeude") or "die passende Ausbildungsstaette"
        return False, f"{einheit} braucht {gelaende.gebaeude_name(gebaeude)} -- nicht gebaut."
    waren = eintrag.get("waren") or []
    fehl_waren = [w for w in waren if (zustand.get("waren") or {}).get(w, 0) < 1]
    if fehl_waren:
        return False, f"Im Lager fehlen fuer {einheit}: {', '.join(fehl_waren)}."
    kosten = dict(eintrag.get("kosten") or {})
    fehlt = _fehlbetrag(zustand, kosten)
    if fehlt:
        return False, f"Zu wenig fuer {einheit}: es fehlen {_kosten_text(fehlt)}."
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
    """
    s = _siedlung(zustand, siedlung_index)
    if s is None:
        return False, f"Unbekannte Siedlung (Index {siedlung_index})."
    if ware not in (spieldaten.waren() or {}):
        return False, f"Unbekannte Ware: {ware}."
    kennung = werkstatt.werkstatt_fuer(ware)
    if not kennung:
        return False, f"Fuer '{ware}' ist keine Werkstatt bekannt."
    bestand = werkstatt.werkstaetten_bestand([s]).get(kennung, 0)
    if bestand < 1:
        return False, (f"Keine {gelaende.gebaeude_name(kennung)} in dieser Siedlung -- "
                       f"erst bauen.")
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
    ok, meldung = werkstatt.einreihen(schlange, ware, anzahl, stufe)
    if not ok:
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
                       "grund": "Keine Kaempfer und keine Belagerungswaffen vorhanden."}

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
# Punkte
# --------------------------------------------------------------------------

def punkte(zustand: dict, jetzt: float) -> dict:
    """Alle Punktarten aus ``src/punkte.py``.

    Forschungspunkte (Stufe hoch drei), Kriegspunkte (Einheitenwerte + Wallstufe
    hoch drei), Gesamtpunktzahl (halbe Summe), Ruf, Goetterschutz und die
    vorgeschlagene Sieg-/Niederlagelage.
    """
    staende = _forschungsstaende(zustand)
    einh = zustand.get("einheiten") or {}
    wall = GW.wall_stufe(zustand.get("siedlungen") or [])
    gesamt = PUNKTE.gesamtpunkte(staende, einh, wall)
    lage, grund = PUNKTE.sieg_oder_niederlage({
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
        "werkstatt_dauer": ("Nur fuer das Schwert ist die Fertigungsdauer belegt (20 Min). "
                            "Andere Waren laufen ohne Dauer in der Warteschlange."),
        "baukunst": ("Die Forschung 'Baukunst' als Bauvoraussetzung wird nicht geprueft: "
                     "die 21 Originalforschungen sind zwar im Spiel, aber die Zuordnung "
                     "je Gebaeude ist noch offen."),
        "kampfverluste": ("Verluste einzelner Einheiten rechnet der (nicht eingebundene) "
                          "Kampfablauf; 'angriff' nutzt Vorrunde, Mauerschaden und Beute "
                          "aus kampfbericht."),
        "portal_mana_je_siedlung": ("portalwechsel nimmt das Mana aus dem gemeinsamen "
                                    "Vorrat; der Stand fuehrt kein Mana je Siedlung."),
        "gebaeude_wirkung_luecken": GW.luecken(),
        "kampfbericht_luecken": kampfbericht.offene_luecken(),
    }
    return luecken
