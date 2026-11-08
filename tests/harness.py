"""Kleiner Pruefrahmen ohne Zusatzpakete.

Unterscheidet bewusst zwei Dinge:
  FEHLER  = etwas ist kaputt (Ausnahme, falsche Anzahl) -> muss behoben werden
  BEFUND  = bekannte Luecke im Ist-Stand -> wird gemeldet, faerbt aber nicht rot
Damit ein gruener Lauf nicht faelschlich "alles fertig" bedeutet.
"""
from __future__ import annotations

import json
import os
import platform
import sys
import time
import traceback

_START = time.time()                          # Beginn des Laufs (fuer die Dauer im Messwert)
_MESSWERTE: "dict[str, dict]" = {}            # gemessene Zahlen dieser Pruefdatei
# Daniel 08.11.2026, 00:25: Messwerte sind Daten, nicht Prosa - jede Pruefdatei legt ihre Zahlen
# mit Zeitstempel ab, damit spaetere, detailliertere Pruefungen sie wiederfinden und verwerten.
MESSWERTE_ORDNER = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                "docs", "audits", "messwerte")

_fehler: list[str] = []
_befunde: list[str] = []
_ok: list[str] = []


def check(name: str, cond: bool, detail: str = "") -> bool:
    if cond:
        _ok.append(name)
        print(f"  OK     {name}" + (f" — {detail}" if detail else ""))
    else:
        _fehler.append(f"{name} {detail}".strip())
        print(f"  FEHLER {name}" + (f" — {detail}" if detail else ""))
    return bool(cond)


def befund(name: str, detail: str = "") -> None:
    """Bekannte Luecke: melden, nicht als Fehler zaehlen."""
    _befunde.append(f"{name} {detail}".strip())
    print(f"  BEFUND {name}" + (f" — {detail}" if detail else ""))


def abschnitt(titel: str) -> None:
    print(f"\n=== {titel} ===")


def ausnahme(name: str, fn):
    """Fuehrt fn aus und meldet eine Ausnahme als Fehler statt abzustuerzen."""
    try:
        return fn()
    except Exception as e:
        _fehler.append(f"{name}: {e!r}")
        print(f"  FEHLER {name} — Ausnahme {e!r}")
        traceback.print_exc()
        return None


def angriff_mit_marsch(app, ziel_name: str, verteidiger, wall_stufe: int = 0,
                       wall_zustand: float = 100.0, vorraete=None,
                       verteidiger_karren=None, vorrat_ziel=None, entfernung=None):
    """Einen Angriff als AUFTRAG starten und bis zur Heimkehr laufen lassen.

    ENTSCHEIDUNG 1 (Daniel, 01.11.2026): es gibt keinen Sofortangriff mehr - jeder Angriff
    reist. Dieser Helfer bildet den Marsch in der Pruefung ab, ohne eine Zeit zu erfinden: er
    springt genau auf die Rueckkehrzeit des Auftrags und laesst den Kern buchen
    (Ankunft -> `kampf_am_ziel`, Rueckkehr -> `einsatz_zurueck`).

    Rueckgabe wie beim Start: True, wenn der Auftrag wirklich unterwegs ist. Ohne Truppen
    oder bei fehlender Siedlung kommt False zurueck und es wird nichts gebucht.
    """
    ok = app._angriff_auftrag_starten(ziel_name, verteidiger, wall_stufe=wall_stufe,
                                      wall_zustand=wall_zustand, vorraete=vorraete,
                                      verteidiger_karren=verteidiger_karren,
                                      vorrat_ziel=vorrat_ziel, entfernung=entfernung)
    if not ok:
        return ok
    eintrag = app.state.auftraege[-1]
    ende = float(eintrag.get("rueckkehr") or eintrag.get("ankunft") or 0.0) + 1.0
    app.state.spielsekunden = max(float(app.state.spielsekunden), ende)
    app.state.auftraege_fortschreiben(app.state.spielsekunden)
    return ok


def messwert(name: str, wert, einheit: str = "", quelle: str = "") -> None:
    """Eine GEMESSENE Zahl unter einem Namen festhalten (Daniel 08.11.2026, 00:25).

    Was hier landet, geht mit Zeitstempel in `docs/audits/messwerte/<datei>_<JJJJMMTT_HHMM>.json`
    und in den Index daneben. Regel: keine Zahl erfinden - gemessen, aus einer Datendatei gelesen
    oder ausdruecklich als VORSCHLAG benannt (dann `quelle="VORSCHLAG"`).
    """
    _MESSWERTE[str(name)] = {"wert": wert, "einheit": str(einheit), "quelle": str(quelle)}


def messwerte() -> "dict[str, dict]":
    """Die bisher festgehaltenen Messwerte dieser Pruefdatei (Kopie)."""
    return {k: dict(v) for k, v in _MESSWERTE.items()}


def _messwert_dateiname() -> str:
    """Der Name der laufenden Pruefdatei ohne Endung (fuer die Messwerte-Datei)."""
    pfad = os.path.basename(sys.argv[0] or "") or "pruefung"   # z. B. test_baseline.py
    return pfad[:-3] if pfad.endswith(".py") else pfad          # ohne .py


def _messwerte_schreiben() -> str:
    """Schreibt die Messwerte als JSON mit Zeitstempel und traegt sie in den Index ein.

    Rueckgabe: der Pfad der geschriebenen Datei oder "" wenn es nicht ging. Ein Fehler beim
    Schreiben macht NIE eine Pruefung rot - die Zahlen sind ein Nebenprodukt, kein Pruefgegenstand.
    Geschrieben wird atomar (temporaere Datei, dann `os.replace`); der Index wird nach demselben
    Muster fortgeschrieben, damit zwei gleichzeitige Laeufe keine halbe Datei hinterlassen.
    """
    try:
        os.makedirs(MESSWERTE_ORDNER, exist_ok=True)           # Ordner darf fehlen
        stempel = time.strftime("%Y%m%d_%H%M")                 # Zeitstempel im Dateinamen
        name = "%s_%s.json" % (_messwert_dateiname(), stempel)  # eine Datei je Lauf
        ziel = os.path.join(MESSWERTE_ORDNER, name)            # voller Pfad
        daten = {"datei": _messwert_dateiname(),               # welche Pruefdatei
                 "zeit": time.strftime("%Y-%m-%dT%H:%M:%S"),   # wann (Ortszeit)
                 "zeit_unix": round(time.time(), 3),           # wann (maschinenlesbar)
                 "dauer_s": round(time.time() - _START, 3),    # wie lange der Lauf dauerte
                 "python": platform.python_version(),          # womit gerechnet wurde
                 "rechner": platform.node(),                   # auf welchem Rechner
                 "bestanden": len(_ok), "fehler": len(_fehler), "befunde": len(_befunde),
                 "pruefungen": list(_ok),                      # die Namen der gruenen Pruefungen
                 "fehlernamen": list(_fehler),                 # die Namen der roten
                 "befundnamen": list(_befunde),                # die Namen der Befunde
                 "messwerte": messwerte()}                     # die gemessenen Zahlen selbst
        _atomar_schreiben(ziel, json.dumps(daten, ensure_ascii=False, indent=1))
        _index_fortschreiben(name, daten)                      # Index daneben
        return ziel
    except Exception as fehler:                                # Schreiben ist Nebenprodukt
        print("  HINWEIS Messwerte nicht geschrieben: %r" % (fehler,))
        return ""


def _atomar_schreiben(ziel: str, text: str) -> None:
    """Schreibt eine Textdatei ueber eine temporaere Datei (kein halber Inhalt)."""
    temp = ziel + ".tmp"
    with open(temp, "w", encoding="utf-8") as datei:
        datei.write(text)
    for versuch in range(5):                                   # Windows: Umbenennen kann kurz haengen
        try:
            os.replace(temp, ziel)
            return
        except OSError:
            time.sleep(0.05 * (versuch + 1))
    os.replace(temp, ziel)                                     # letzter Versuch: Fehler sichtbar


def _index_sperre(wartezeit: float = 15.0):
    """Sperrdatei fuer den Index (O_EXCL), damit parallele Laeufe keinen Eintrag verlieren.

    Grund (gemessen 08.11.2026, Schritt 12): der Index wird gelesen, ergaenzt und neu geschrieben.
    Ohne Sperre lesen zwei gleichzeitige Laeufe denselben alten Stand und der zweite Schreibvorgang
    loescht den Eintrag des ersten - beim parallelen Sammellauf gingen so die meisten Eintraege
    verloren. Die Sperre ist eine eigene Datei neben dem Index; sie wird im `finally` immer
    freigegeben, und eine liegengebliebene Sperre eines abgestuerzten Laufs wird nach `wartezeit`
    Sekunden uebernommen (das Schreiben selbst dauert Millisekunden).
    """
    import contextlib

    @contextlib.contextmanager
    def _halter():
        sperre = os.path.join(MESSWERTE_ORDNER, "index.sperre")
        ende = time.time() + wartezeit
        while True:
            try:
                griff = os.open(sperre, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                os.close(griff)
                break
            except FileExistsError:                            # ein anderer Lauf schreibt gerade
                if time.time() > ende:                         # alte Sperre: uebernehmen
                    try:
                        os.remove(sperre)
                    except OSError:
                        pass
                    continue
                time.sleep(0.02)
            except OSError:                                    # Ordner fehlt o. ae.: ohne Sperre
                break
        try:
            yield
        finally:
            try:
                os.remove(sperre)
            except OSError:
                pass

    return _halter()


def _index_fortschreiben(name: str, daten: dict) -> None:
    """Traegt den Lauf in `docs/audits/messwerte/index.json` ein (neuester Stand je Pruefdatei)."""
    pfad = os.path.join(MESSWERTE_ORDNER, "index.json")
    eintrag = {k: daten.get(k) for k in ("datei", "zeit", "bestanden", "fehler", "befunde",
                                        "dauer_s")}
    eintrag["datei_im_ordner"] = name                          # welche Datei die Zahlen traegt
    with _index_sperre():                                      # parallele Laeufe: einer nach dem anderen
        for versuch in range(5):                               # kurze Schreibfehler: nochmal
            try:
                index = {}
                if os.path.isfile(pfad):                       # Index schon da
                    with open(pfad, "r", encoding="utf-8") as datei:
                        index = json.load(datei) or {}
                dateien = index.get("dateien") if isinstance(index, dict) else None
                dateien = dateien if isinstance(dateien, dict) else {}
                dateien[str(daten.get("datei"))] = eintrag      # neuester Stand dieser Datei
                neu = {"stand": time.strftime("%Y-%m-%dT%H:%M:%S"),
                       "wozu": ("Messwerte je Pruefdatei, neuester Lauf. Geschrieben von "
                                "tests/harness.bericht() (Daniel 08.11.2026, 00:25)."),
                       "dateien": dateien}
                _atomar_schreiben(pfad, json.dumps(neu, ensure_ascii=False, indent=1))
                return
            except Exception:                                   # naechster Versuch
                time.sleep(0.05 * (versuch + 1))


def bericht() -> int:
    print("\n" + "=" * 58)
    print(f"ERGEBNIS: {len(_ok)} bestanden, {len(_fehler)} Fehler, {len(_befunde)} Befunde")
    _messwert_pfad = _messwerte_schreiben()                      # Zahlen mit Zeitstempel ablegen
    if _messwert_pfad:                                           # sichtbar machen, wo sie liegen
        print(f"Messwerte: {_messwert_pfad}")
    if _befunde:
        print("\nBefunde (bekannte Luecken, kein Fehler):")
        for b in _befunde:
            print("  -", b)
    if _fehler:
        print("\nFehler (muessen behoben werden):")
        for f in _fehler:
            print("  -", f)
    print("=" * 58)
    return 1 if _fehler else 0


# Projektwurzel und src in den Suchpfad
def projektwurzel():
    import os
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def import_src():
    import os
    root = projektwurzel()
    src = os.path.join(root, "src")
    for p in (root, src):
        if p not in sys.path:
            sys.path.insert(0, p)
    return root, src
