"""Zieluebergabe zwischen Sitzungen — nachpruefbar statt Handarbeit (Vorgabe Daniel 05.10.2026).

Warum es dieses Werkzeug gibt
----------------------------
Ein `/goal` lebt **in der Sitzung**, nicht im Chatfenster: eine Sitzung mit `status: active`
arbeitet weiter, auch wenn ihr Chat archiviert ist. Am 05.10.2026 hat genau das passiert — eine
alte Koordinator-Sitzung schrieb bis 01:31 weiter in `src/main.py`, waehrend eine neue Sitzung
denselben Auftrag begann (Beleg: `docs/ENTWICKLUNGSPROTOKOLL.md`, Abschnitt „Tag 2").

Das Werkzeug macht die Uebergabe pruefbar und **vorsichtig**:

    python tools/zieluebergabe.py --pruefen              nur lesen; Rueckgabe 1, wenn eine FREMDE
                                                         Sitzung ein aktives Ziel hat
    python tools/zieluebergabe.py --stand                Tabelle aller Ziele
    python tools/zieluebergabe.py --beenden SITZUNG      GENAU diese Sitzung sauber beenden
                                                         (status=cleared mit Grund im Datensatz)
    python tools/zieluebergabe.py --naechster-schritt    den EINEN naechsten Schritt aus
                                                         docs/PROJEKT_STAND.md (Abschnitt 0c)
    python tools/zieluebergabe.py --startzeile           die Startzeile fuer die neue Sitzung

Absichtlich **nicht** enthalten: eine neue Sitzung selbst starten. Ein zweiter Schreiber, der von
allein anlaeuft, ist genau der Fehler, den dieses Werkzeug verhindern soll. Die Startzeile wird
ausgegeben und von Daniel (oder von der neuen Sitzung selbst) benutzt.

Nur Standardbibliothek. `--db` erlaubt eine Kopie des Registers (fuer Pruefungen).
"""
from __future__ import annotations

import argparse
import json
import os
import sqlite3
import sys
from pathlib import Path

SCHLUESSEL = "goal:%s"

# Das Projekt, dessen Uebergabe gelesen wird (nur fuer --naechster-schritt/--startzeile).
PROJEKT = Path(__file__).resolve().parent.parent
STAND_DATEI = PROJEKT / "docs" / "AKTUELLER_STAND.md"


def register_pfad() -> Path:
    """Das Zielregister: `state.db` im Hermes-Zuhause (auch mit HERMES_HOME)."""
    home = os.environ.get("HERMES_HOME") or str(Path(os.environ.get("LOCALAPPDATA", Path.home()))
                                                / "hermes")
    return Path(home) / "state.db"


def ziele(db_pfad) -> list:
    """Alle Ziele aus dem Register lesen: [{sitzung, status, takte, max_takte, text}].

    Schreibt nichts. Fehlt die Datei, ist die Liste leer (kein Absturz).
    """
    pfad = Path(db_pfad)
    if not pfad.exists():
        return []
    try:
        con = sqlite3.connect(f"file:{pfad.as_posix()}?mode=ro", uri=True, timeout=5)
    except sqlite3.Error:
        return []
    try:
        zeilen = con.execute(
            "select key, value from state_meta where key like 'goal:%'").fetchall()
    except sqlite3.Error:
        return []
    finally:
        con.close()

    out = []
    for key, wert in zeilen:
        try:
            daten = json.loads(wert)
        except (TypeError, ValueError):
            daten = {}
        out.append({
            "sitzung": str(key).split(":", 1)[1] if ":" in str(key) else str(key),
            "status": str(daten.get("status") or "?"),
            "takte": int(daten.get("turns_used") or 0),
            "max_takte": int(daten.get("max_turns") or 0),
            "text": str(daten.get("goal") or "").replace("\n", " "),
        })
    out.sort(key=lambda z: (z["status"] != "active", z["sitzung"]))
    return out


def fremde_aktive(ziel_liste, eigene_sitzung: str) -> list:
    """Aktive Ziele in FREMDE Sitzungen — die Geisterlaeufer."""
    return [z for z in ziel_liste
            if z["status"] == "active" and z["sitzung"] != str(eigene_sitzung or "")]


def eigene_ziele(ziel_liste, eigene_sitzung: str) -> list:
    """Aktive Ziele der EIGENEN Sitzung (leer, wenn das eigene Ziel pausiert/beendet ist).

    Wichtig fuer die Ehrlichkeit: „kein fremdes aktives Ziel" heisst NICHT, dass die eigene
    Zielverfolgung laeuft — ein pausiertes Ziel laeuft nicht von selbst weiter.
    """
    if not eigene_sitzung:
        return []
    return [z for z in ziel_liste if z["status"] == "active" and z["sitzung"] == str(eigene_sitzung)]


def beende(db_pfad, sitzung: str, grund: str) -> tuple:
    """Setzt das Ziel GENAU dieser Sitzung auf `cleared` (Grund im Datensatz). (ok, Meldung).

    Nichts anderes wird angefasst; fehlt die Sitzung, wird ehrlich abgelehnt.
    """
    pfad = Path(db_pfad)
    if not pfad.exists():
        return False, f"Zielregister nicht gefunden: {pfad}"
    schluessel = SCHLUESSEL % sitzung
    con = sqlite3.connect(str(pfad), timeout=15)
    try:
        con.execute("PRAGMA busy_timeout=15000")
        zeile = con.execute("select value from state_meta where key=?", (schluessel,)).fetchone()
        if not zeile:
            return False, f"Kein Ziel fuer die Sitzung {sitzung} im Register."
        daten = json.loads(zeile[0])
        vorher = str(daten.get("status") or "?")
        daten["status"] = "cleared"
        daten["paused_reason"] = (str(daten.get("paused_reason") or "") + " | " + grund).strip(" |")
        con.execute("update state_meta set value=? where key=?",
                    (json.dumps(daten, ensure_ascii=False), schluessel))
        con.commit()
    finally:
        con.close()
    return True, f"{sitzung}: {vorher} -> cleared ({grund})"


def setze_aktiv(db_pfad, sitzung: str, grund: str) -> tuple:
    """Setzt das Ziel GENAU dieser Sitzung wieder auf `active` (Gegenstueck zu `beende`).

    Gedacht fuer die eigene Sitzung, wenn der Zielrichter die Verfolgung pausiert hat: danach
    laeuft sie wieder von selbst weiter. Nichts anderes wird angefasst.
    """
    pfad = Path(db_pfad)
    if not pfad.exists():
        return False, f"Zielregister nicht gefunden: {pfad}"
    schluessel = SCHLUESSEL % sitzung
    con = sqlite3.connect(str(pfad), timeout=15)
    try:
        con.execute("PRAGMA busy_timeout=15000")
        zeile = con.execute("select value from state_meta where key=?", (schluessel,)).fetchone()
        if not zeile:
            return False, f"Kein Ziel fuer die Sitzung {sitzung} im Register."
        daten = json.loads(zeile[0])
        vorher = str(daten.get("status") or "?")
        if vorher == "active":
            return True, f"{sitzung}: war schon aktiv — nichts geaendert."
        daten["status"] = "active"
        daten["paused_reason"] = (str(daten.get("paused_reason") or "") + " | " + grund).strip(" |")
        con.execute("update state_meta set value=? where key=?",
                    (json.dumps(daten, ensure_ascii=False), schluessel))
        con.commit()
    finally:
        con.close()
    return True, f"{sitzung}: {vorher} -> active ({grund})"


def naechster_schritt(pfad=None) -> str:
    """Den EINEN naechsten Schritt aus dem Uebergabedokument holen (Abschnitt 0c).

    Gesucht wird die Ueberschrift „### Der EINE nächste Schritt"; geliefert wird der Text bis zur
    naechsten Ueberschrift. Fehlt sie, kommt ein ehrlicher Hinweis zurueck (kein Absturz).
    """
    datei = Path(pfad or STAND_DATEI)
    if not datei.exists():
        return f"Uebergabedokument nicht gefunden: {datei}"
    text = datei.read_text(encoding="utf-8", errors="replace")
    marke = "## Next actions für den temporären Coding-Agenten"
    stelle = text.find(marke)
    if stelle < 0:
        return f"'{marke}' steht nicht in {datei.name}."
    rest = text[stelle + len(marke):]
    ende = rest.find("\n## ")
    return (rest[:ende if ende > 0 else len(rest)].strip()
            + "\n\nVerpflichtend: Einzeltest, Sammellauf und Eintrag ins zentrale "
              "Entwicklungsprotokoll.md nach jedem bestaetigten Fix.")


def startzeile(eigene_sitzung: str = "") -> str:
    """Ausgabe einer rein informativen Wiedereinstiegsanweisung – keine Agentenaktion."""
    return "\n".join([
        f"Lies ZUERST {PROJEKT / 'docs' / 'HERMES_UEBERGABE_AKTUELL.md'} als einzige aktive Hermes-Uebergabe.",
        f"Lies {PROJEKT / 'docs' / 'AKTUELLER_STAND.md'} fuer die offenen Schritte und Spielbereiche.",
        f"Lies {PROJEKT / 'docs' / 'HERMES_KONTROLLE_UND_SKILLS.md'} fuer geltende Sicherheits- und Lernregeln.",
        "Nach jedem Schritt: gezielter Einzeltest + Sammellauf (run_tests.bat unter Windows),",
        "eine Zeile ins zentrale docs/ENTWICKLUNGSPROTOKOLL.md mit Testbeleg;",
        "anschliessend Freigabe durch Hermes, sauberer Commit und nach Sicherheitspruefung Push.",
        "Vor der ersten Aenderung: python tools/zieluebergabe.py --pruefen",
        "Ein fremdes aktives Ziel nie parallel weiterbearbeiten (gegebenenfalls --beenden SITZUNG).",
        "Ziel in DIESER Sitzung setzen: /goal <naechster offener Schritt aus docs/AKTUELLER_STAND.md>",
    ])


def _tabelle(ziel_liste, eigene_sitzung: str) -> str:
    if not ziel_liste:
        return "Kein Ziel im Register."
    zeilen = [f"{'Sitzung':<26} {'Status':<9} {'Takte':>6}  Ziel (Auszug)"]
    for z in ziel_liste:
        marke = "  <-- diese Sitzung" if z["sitzung"] == str(eigene_sitzung or "") else ""
        if z["status"] == "active" and z["sitzung"] != str(eigene_sitzung or ""):
            marke = "  <-- GEISTERLAEUFER (arbeitet weiter!)"
        zeilen.append(f"{z['sitzung']:<26} {z['status']:<9} "
                      f"{z['takte']:>3}/{z['max_takte']:<2}  {z['text'][:60]}{marke}")
    return "\n".join(zeilen)


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Zieluebergabe zwischen Sitzungen (nur lesen "
                                             "oder EINE Sitzung beenden).")
    p.add_argument("--db", default=None, help="Pfad zum Zielregister (Vorgabe: state.db im "
                                              "Hermes-Zuhause; fuer Pruefungen eine Kopie)")
    p.add_argument("--pruefen", action="store_true", help="nur lesen; 1 bei fremdem aktivem Ziel")
    p.add_argument("--stand", action="store_true", help="Tabelle aller Ziele")
    p.add_argument("--beenden", default=None, metavar="SITZUNG",
                   help="GENAU diese Sitzung sauber beenden (status=cleared)")
    p.add_argument("--fortsetzen", default=None, metavar="SITZUNG",
                   help="GENAU diese Sitzung wieder auf active setzen (Zielverfolgung laeuft "
                        "danach von selbst weiter)")
    p.add_argument("--grund", default="von der neuen Sitzung sauber beendet (Zieluebergabe)",
                   help="Grund, der im Datensatz vermerkt wird")
    p.add_argument("--sitzung", default=os.environ.get("HERMES_SESSION_ID", ""),
                   help="die EIGENE Sitzung (Vorgabe: HERMES_SESSION_ID)")
    p.add_argument("--naechster-schritt", action="store_true",
                   help="den EINEN naechsten Schritt aus dem Uebergabedokument zeigen")
    p.add_argument("--startzeile", action="store_true", help="Startzeile fuer die neue Sitzung")
    args = p.parse_args(argv)

    db = args.db or register_pfad()

    if args.naechster_schritt:
        print(naechster_schritt())
        return 0
    if args.startzeile:
        print(startzeile(args.sitzung))
        return 0
    if args.beenden:
        ok, meldung = beende(db, args.beenden, args.grund)
        print(("OK   " if ok else "ROT  ") + meldung)
        if not ok:
            return 1
        print()
        print(_tabelle(ziele(db), args.sitzung))
        return 0
    if args.fortsetzen:
        ok, meldung = setze_aktiv(db, args.fortsetzen, args.grund)
        print(("OK   " if ok else "ROT  ") + meldung)
        if not ok:
            return 1
        print()
        print(_tabelle(ziele(db), args.sitzung))
        return 0

    liste = ziele(db)
    print(f"Zielregister: {db}")
    print()
    print(_tabelle(liste, args.sitzung))
    geister = fremde_aktive(liste, args.sitzung)
    eigene = eigene_ziele(liste, args.sitzung)
    print()
    if not liste:
        print("Kein Ziel im Register - es kann keines weiterlaufen.")
        return 0
    if geister:
        print(f"ACHTUNG: {len(geister)} fremde(s) Ziel aktiv — es arbeitet weiter, auch wenn der "
              f"Chat archiviert ist:")
        for z in geister:
            print(f"  {z['sitzung']}  (Takte {z['takte']}/{z['max_takte']})")
        print("Sauber beenden:  python tools/zieluebergabe.py --beenden "
              f"{geister[0]['sitzung']}")
        if args.pruefen:
            return 1
        return 0
    print("Kein fremdes aktives Ziel — es arbeitet keine andere Sitzung.")
    if not eigene:
        print("Aber: AUCH DIESE SITZUNG verfolgt gerade kein AKTIVES Ziel (pausiert oder beendet).")
        print("Ohne aktives Ziel laeuft die Zielverfolgung NICHT von selbst weiter.")
        if args.sitzung:
            print(f"Fortsetzen:      python tools/zieluebergabe.py --fortsetzen {args.sitzung}")
        else:
            print("Fortsetzen:      /goal resume in der Sitzung (oder --sitzung <eigene> angeben)")
    elif args.pruefen:
        print(f"OK: diese Sitzung verfolgt ein aktives Ziel ({eigene[0]['takte']}/"
              f"{eigene[0]['max_takte']} Takte).")
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
