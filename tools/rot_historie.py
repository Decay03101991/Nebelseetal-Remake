"""Rot-Historie (M12) - was darf seltener laufen, was wackelt, was wurde nie aufgezeichnet.

Quelle ist AUSSCHLIESSLICH `docs/audits/laeufe.jsonl` (M12.0): eine Zeile je Datei und Lauf,
geschrieben vom Sammellauf selbst. Keine Messwertdateien, keine Auswertung des harness - damit
haben auch die Dateien eine Historie, die (wie `test_textqualitaet`) nichts in den Index schreiben.

Vier Listen (Claude, Antwort Nr. 16, Teil B, M12):

  1. KANDIDAT HOEHERE STUFE: mindestens 30 Laeufe, 0 rot, **allein gemessene** Mediandauer
     mindestens 10 s, und keine der Dateien aus `PRUEF_BETRIFFT` in den letzten 14 Tagen geaendert.
  2. WACKELKANDIDAT: im SELBEN Commit einmal rot und einmal gruen. Das ist kein Codefehler,
     sondern ein Messumstand (Beleg: `test_weltkarte_malerei`, 4,5 s unter Last / 0,56 s allein).
  3. NIE AUFGEZEICHNET: in `tests/` vorhanden, aber mit 0 Zeilen in der Ablage.
  4. TEUER JE FUND: Gesamtdauer / (Rotfunde + 1) - die obersten zehn.

Aufruf:
  python -X utf8 tools/rot_historie.py                     # liest laeufe.jsonl, schreibt den Bericht
  python -X utf8 tools/rot_historie.py --datei X.jsonl     # andere Ablage (Pruefung)
Ergebnis: docs/audits/ROT_HISTORIE.md und docs/audits/ROT_HISTORIE.csv
"""
from __future__ import annotations

import argparse
import csv
import datetime
import json
import os
import statistics
import subprocess
import sys

HIER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LAEUFE = os.path.join(HIER, "docs", "audits", "laeufe.jsonl")
BERICHT_MD = os.path.join(HIER, "docs", "audits", "ROT_HISTORIE.md")
BERICHT_CSV = os.path.join(HIER, "docs", "audits", "ROT_HISTORIE.csv")
TESTS = os.path.join(HIER, "tests")
MIN_LAEUFE = 30
MIN_MEDIAN_S = 10.0
FENSTER_TAGE = 14
OBERSTE = 10


def dateien_im_testordner() -> list:
    """Alle Pruefdateien, die es gibt (Grundlage fuer "nie aufgezeichnet")."""
    try:
        return sorted(n for n in os.listdir(TESTS) if n.startswith("test_") and n.endswith(".py"))
    except OSError:
        return []


def zeilen_lesen(pfad: str = LAEUFE) -> list:
    """Die Laufzeilen lesen; fehlende Datei ergibt eine leere Liste (kein Fehler)."""
    zeilen = []
    try:
        with open(pfad, encoding="utf-8") as fh:
            for nummer, roh in enumerate(fh, 1):
                roh = roh.strip()
                if not roh:
                    continue
                try:
                    zeilen.append(json.loads(roh))
                except ValueError:
                    continue                      # kaputte Zeile ueberspringen, nicht abbrechen
    except OSError:
        return []
    return zeilen


def _median_allein(laeufe: list):
    """Mediandauer der ALLEIN gemessenen Laeufe (None, wenn keiner allein lief)."""
    dauern = [float(z.get("dauer") or 0.0) for z in laeufe
              if z.get("allein") == "ja" and z.get("bestanden") is not None]
    return statistics.median(dauern) if dauern else None


def _kuerzlich_geaendert(datei: str, aenderungsdaten: dict) -> bool:
    """Wurde eine der BETRIFFT-Dateien in den letzten FENSTER_TAGE Tagen geaendert?

    `aenderungsdaten` ist {pfad: tage_seit_letzter_aenderung}. Fehlt der Eintrag, gilt die
    Bedingung als NICHT erfuellt (unbekannt ist nicht "geaendert") - so wird nichts still
    ausgeschlossen und nichts still aufgenommen; der Bericht nennt die Zahl der Unbekannten.
    """
    if not aenderungsdaten:
        return False
    for pfad, tage in aenderungsdaten.items():
        if datei in str(pfad):
            try:
                if float(tage) < FENSTER_TAGE:
                    return True
            except (TypeError, ValueError):
                continue
    return False


def auswerten(zeilen, aenderungsdaten=None, bekannte_dateien=None) -> dict:
    """Die vier Listen - reine Funktion, ohne Git und ohne Dateizugriff.

    Rueckgabe::

        {"kandidaten": [...], "wackler": [...], "nie": [...], "teuer": [...],
         "dateien": n, "laeufe": n, "unbekanntes_alter": n}
    """
    nach_datei = {}
    for z in zeilen or []:
        datei = z.get("datei")
        if not datei:
            continue
        nach_datei.setdefault(str(datei), []).append(z)

    kandidaten, wackler, teuer = [], [], []
    unbekannt = 0
    for datei in sorted(nach_datei):
        laeufe = nach_datei[datei]
        rot = [z for z in laeufe if z.get("bestanden") is False]
        median = _median_allein(laeufe)
        if not aenderungsdaten or datei not in aenderungsdaten:
            unbekannt += 1
        if (len(laeufe) >= MIN_LAEUFE and not rot and median is not None
                and median >= MIN_MEDIAN_S and not _kuerzlich_geaendert(datei, aenderungsdaten)):
            kandidaten.append({"datei": datei, "laeufe": len(laeufe),
                               "median_allein_s": round(median, 2)})
        # Wackelkandidat: je Commit einmal rot und einmal gruen (in beliebiger Reihenfolge).
        nach_commit = {}
        for z in laeufe:
            commit = z.get("commit")
            if commit is None:
                continue
            nach_commit.setdefault(str(commit), set()).add(z.get("bestanden"))
        for commit in sorted(nach_commit):
            ergebnisse = nach_commit[commit]
            if True in ergebnisse and False in ergebnisse:
                wackler.append({"datei": datei, "commit": commit,
                                "laeufe": len(nach_commit)})
        gesamt = sum(float(z.get("dauer") or 0.0) for z in laeufe)
        teuer.append({"datei": datei, "laeufe": len(laeufe), "rot": len(rot),
                      "gesamt_s": round(gesamt, 1),
                      "je_fund_s": round(gesamt / (len(rot) + 1), 1)})
    kandidaten.sort(key=lambda e: (-e["median_allein_s"], e["datei"]))
    wackler.sort(key=lambda e: (e["datei"], e["commit"]))
    teuer.sort(key=lambda e: (-e["je_fund_s"], e["datei"]))
    nie = []
    if bekannte_dateien is not None:
        nie = sorted(set(bekannte_dateien) - set(nach_datei))
    return {"kandidaten": kandidaten, "wackler": wackler, "nie": nie,
            "teuer": teuer[:OBERSTE], "dateien": len(nach_datei), "laeufe": len(zeilen or []),
            "unbekanntes_alter": unbekannt}


def aenderungsdaten(tage: int = FENSTER_TAGE, jetzt: datetime.datetime = None) -> dict:
    """{datei: tage seit der letzten Aenderung} aus `git log` - ohne Netz, ohne Zweigwechsel."""
    jetzt = jetzt or datetime.datetime.now()
    ab = (jetzt - datetime.timedelta(days=3650)).strftime("%Y-%m-%dT%H:%M:%S")
    befehl = ["git", "log", "--since=" + ab, "--name-only", "--pretty=format:%cd",
              "--date=format:%Y-%m-%dT%H:%M:%S", "--", "tests", "src", "data", "tools"]
    try:
        p = subprocess.run(befehl, capture_output=True, text=True, cwd=HIER, timeout=120)
    except (OSError, subprocess.SubprocessError):
        return {}
    if p.returncode != 0:
        return {}
    ergebnis, datum = {}, None
    for linie in (p.stdout or "").splitlines():
        linie = linie.strip()
        if not linie:
            continue
        if linie[:4].isdigit() and "-" in linie:
            try:
                datum = datetime.datetime.fromisoformat(linie.replace("Z", ""))
            except ValueError:
                datum = None
            continue
        if datum is None:
            continue
        name = os.path.basename(linie)
        tage_seit = (jetzt - datum).total_seconds() / 86400.0
        if name not in ergebnis or tage_seit < ergebnis[name]:
            ergebnis[name] = round(tage_seit, 2)
    return ergebnis


def als_markdown(ergebnis: dict, stand: str = "") -> str:
    """Der Bericht als Markdown - feste Reihenfolge, keine Zufallssortierung."""
    zeilen = ["# Rot-Historie (M12)", ""]
    zeilen.append("**Stand:** %s · **Quelle:** `docs/audits/laeufe.jsonl` (M12.0) · "
                  "**Dateien:** %d · **Laeufe:** %d"
                  % (stand or "-", ergebnis.get("dateien", 0), ergebnis.get("laeufe", 0)))
    zeilen.append("")
    zeilen.append("Grenzen: Kandidat ab **%d Laeufen**, **0 rot**, **Mediandauer >= %.0f s allein "
                  "gemessen**, keine Aenderung an den BETRIFFT-Dateien in den letzten **%d Tagen**."
                  % (MIN_LAEUFE, MIN_MEDIAN_S, FENSTER_TAGE))
    zeilen.append("")
    zeilen.append("## 1. Kandidaten fuer eine hoehere Stufe (%d)" % len(ergebnis.get("kandidaten") or []))
    zeilen.append("")
    if ergebnis.get("kandidaten"):
        zeilen.append("| Datei | Laeufe | Median allein |")
        zeilen.append("|---|---|---|")
        for e in ergebnis["kandidaten"]:
            zeilen.append("| `%s` | %d | %.1f s |" % (e["datei"], e["laeufe"], e["median_allein_s"]))
    else:
        zeilen.append("_keine_")
    zeilen.append("")
    zeilen.append("## 2. Wackelkandidaten: im selben Commit rot und gruen (%d)"
                  % len(ergebnis.get("wackler") or []))
    zeilen.append("")
    if ergebnis.get("wackler"):
        zeilen.append("| Datei | Commit | Laeufe dieses Commits |")
        zeilen.append("|---|---|---|")
        for e in ergebnis["wackler"]:
            zeilen.append("| `%s` | `%s` | %d |" % (e["datei"], e["commit"], e["laeufe"]))
    else:
        zeilen.append("_keine_")
    zeilen.append("")
    zeilen.append("## 3. Nie aufgezeichnet (%d)" % len(ergebnis.get("nie") or []))
    zeilen.append("")
    if ergebnis.get("nie"):
        zeilen.append("Diese Dateien liegen in `tests/`, haben aber **keine** Zeile in der Ablage:")
        zeilen.append("")
        for name in ergebnis["nie"]:
            zeilen.append("- `%s`" % name)
    else:
        zeilen.append("_keine_")
    zeilen.append("")
    zeilen.append("## 4. Teuer je Fund (oberste %d)" % OBERSTE)
    zeilen.append("")
    if ergebnis.get("teuer"):
        zeilen.append("| Datei | Laeufe | rot | Gesamt | je Fund |")
        zeilen.append("|---|---|---|---|---|")
        for e in ergebnis["teuer"]:
            zeilen.append("| `%s` | %d | %d | %.1f s | %.1f s |"
                          % (e["datei"], e["laeufe"], e["rot"], e["gesamt_s"], e["je_fund_s"]))
    else:
        zeilen.append("_keine_")
    zeilen.append("")
    return "\n".join(zeilen) + "\n"


def als_csv(ergebnis: dict) -> str:
    """Alle vier Listen in EINER Tabelle, mit einer Spalte `liste`."""
    import io
    puffer = io.StringIO()
    schreiber = csv.writer(puffer, delimiter=";", lineterminator="\n")
    schreiber.writerow(["liste", "datei", "laeufe", "median_allein_s", "commit", "rot",
                        "gesamt_s", "je_fund_s"])
    for e in ergebnis.get("kandidaten") or []:
        schreiber.writerow(["kandidat", e["datei"], e["laeufe"], e["median_allein_s"], "", "", "", ""])
    for e in ergebnis.get("wackler") or []:
        schreiber.writerow(["wackelt", e["datei"], e["laeufe"], "", e["commit"], "", "", ""])
    for name in ergebnis.get("nie") or []:
        schreiber.writerow(["nie", name, 0, "", "", "", "", ""])
    for e in ergebnis.get("teuer") or []:
        schreiber.writerow(["teuer", e["datei"], e["laeufe"], "", "", e["rot"], e["gesamt_s"],
                            e["je_fund_s"]])
    return puffer.getvalue()


def schreiben(ergebnis: dict, md_pfad: str = BERICHT_MD, csv_pfad: str = BERICHT_CSV,
              stand: str = "") -> tuple:
    """Markdown und CSV schreiben und beide Pfade zurueckgeben."""
    for pfad in (md_pfad, csv_pfad):
        ordner = os.path.dirname(pfad)
        if ordner:
            os.makedirs(ordner, exist_ok=True)
    with open(md_pfad, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(als_markdown(ergebnis, stand))
    with open(csv_pfad, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(als_csv(ergebnis))
    return md_pfad, csv_pfad


def main(argv=None) -> int:
    leser = argparse.ArgumentParser(description="Rot-Historie aus docs/audits/laeufe.jsonl")
    leser.add_argument("--datei", default=LAEUFE, help="andere Laufzeilen-Ablage")
    leser.add_argument("--ohne-git", action="store_true", help="Aenderungsdaten nicht abfragen")
    args = leser.parse_args(argv)
    zeilen = zeilen_lesen(args.datei)
    if not zeilen:
        print("Keine Laufzeilen in %s - zuerst den Sammellauf laufen lassen (M12.0)." % args.datei)
        return 1
    aenderungen = {} if args.ohne_git else aenderungsdaten()
    ergebnis = auswerten(zeilen, aenderungen, dateien_im_testordner())
    stand = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
    md, csv_pfad = schreiben(ergebnis, stand=stand)
    print("Rot-Historie: %d Dateien, %d Laeufe" % (ergebnis["dateien"], ergebnis["laeufe"]))
    print("  Kandidaten hoehere Stufe: %d" % len(ergebnis["kandidaten"]))
    print("  Wackelkandidaten:         %d" % len(ergebnis["wackler"]))
    print("  nie aufgezeichnet:        %d" % len(ergebnis["nie"]))
    print("  teuer je Fund (top %d):    %d" % (OBERSTE, len(ergebnis["teuer"])))
    print("Bericht: %s" % md)
    print("Tabelle: %s" % csv_pfad)
    return 0


if __name__ == "__main__":
    sys.exit(main())
