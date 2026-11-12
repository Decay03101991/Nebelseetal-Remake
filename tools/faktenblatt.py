"""Faktenblatt: die Zahlen des Spiels EINMAL aus `data/` gezaehlt (M11).

Warum es dieses Werkzeug gibt (Claude, Antwort Nr. 16, Teil B): in den Auftraegen Nr. 12 bis 15
standen drei falsche Zahlen ("vier Zutaten", "18 Waren", "2148 px Dorfzentrum"). Sie kamen nicht
aus den Daten, sondern aus dem Gedaechtnis. Ab jetzt kommt jede Zahl im Auftrag aus diesem Blatt,
und `tools/auftrag_pruefen.py` warnt, wenn ein Auftrag eine andere Zahl nennt.

Grundsaetze
  * Die Zahlen werden GEZAEHLT, nicht gepflegt: `zaehlen(daten_ordner)` liest `data/` und liefert
    ein Woerterbuch. Keine 17, keine 3 und keine 230 stehen im Code.
  * Feste Sortierung, kein Zufall - zwei Laeufe ergeben dieselbe Datei.
  * Kein Tk noetig: Textbreiten in px sind freiwillig. Ist Tk nicht verfuegbar, wird der Abschnitt
    weggelassen und im Blatt ausdruecklich als fehlend vermerkt.

Aufruf:
  python -X utf8 tools/faktenblatt.py                 # schreibt docs/FAKTENBLATT.md und .json
  python -X utf8 tools/faktenblatt.py --ohne-tk       # ohne Textbreiten (schnell, kopflos)
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys

HIER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATEN = os.path.join(HIER, "data")
MD_PFAD = os.path.join(HIER, "docs", "FAKTENBLATT.md")
JSON_PFAD = os.path.join(HIER, "docs", "faktenblatt.json")
ROHSTOFFE = ("holz", "metall", "wolle", "leder")


def _lade(daten_ordner: str, name: str) -> dict:
    """Eine JSON-Datei aus dem Datenordner lesen; fehlt sie, kommt ein leeres dict."""
    pfad = os.path.join(daten_ordner, name)
    try:
        with open(pfad, encoding="utf-8") as fh:
            inhalt = json.load(fh)
    except (OSError, ValueError):
        return {}
    return inhalt if isinstance(inhalt, dict) else {}


def zaehlen(daten_ordner: str = DATEN) -> dict:
    """Alle Zahlen des Spiels aus `data/` - reine Funktion, ohne Tk, ohne Git.

    Rueckgabe (fest sortiert)::

        {"waren": {...}, "rezepte": {...}, "einheiten": {...}, "forschungen": {...},
         "gebaeude": {...}, "voelker": {...}, "welten": {...}, "gelaendearten": {...},
         "werkstaetten": {...}, "quellen": {...}}
    """
    items = _lade(daten_ordner, "items.json")
    waren = items.get("waren") or {}
    rezepte = _lade(daten_ordner, "warenrezepte.json")
    units = _lade(daten_ordner, "units.json")
    research = _lade(daten_ordner, "research.json")
    buildings = _lade(daten_ordner, "buildings.json")
    voelker = _lade(daten_ordner, "voelker.json")
    welten = _lade(daten_ordner, "welten.json")
    gelaende = _lade(daten_ordner, "gelaende.json")

    # ---- Waren und Rezepte -------------------------------------------------
    waren_namen = sorted(waren)
    zutaten_je_rezept = {}
    zutaten_rohstoffe = {r: {"rezepte": 0, "summe": 0} for r in ROHSTOFFE}
    rezepte_ohne_kosten = []
    unbekannte_rohstoffe = {}
    for name in sorted(rezepte):
        kosten = (rezepte[name] or {}).get("kosten") or {}
        zutaten_je_rezept[name] = len(kosten)
        if not kosten:
            rezepte_ohne_kosten.append(name)
        for rohstoff, menge in kosten.items():
            if rohstoff not in zutaten_rohstoffe:
                unbekannte_rohstoffe[rohstoff] = unbekannte_rohstoffe.get(rohstoff, 0) + 1
                continue
            zutaten_rohstoffe[rohstoff]["rezepte"] += 1
            try:
                zutaten_rohstoffe[rohstoff]["summe"] += int(menge)
            except (TypeError, ValueError):
                pass
    hoechste = max(zutaten_je_rezept.values()) if zutaten_je_rezept else 0

    # ---- Werkstaetten: die Zuordnung steht in items.json -------------------
    werkstatt_waren = {}
    for name in waren_namen:
        fach = (waren[name] or {}).get("werkstatt")
        if fach:
            werkstatt_waren.setdefault(str(fach), []).append(name)
    rezept_hat_werkstatt = any("werkstatt" in (r or {}) for r in rezepte.values())

    # ---- Einheiten, Forschungen, Gebaeude ---------------------------------
    einheiten = units.get("einheiten") or {}
    forschungen = research.get("forschungen") or {}
    gebaeude_liste = buildings.get("gebaeude") or []
    je_kategorie = {}
    for gebaeude in gebaeude_liste:
        kategorie = str((gebaeude or {}).get("kategorie") or "ohne")
        je_kategorie[kategorie] = je_kategorie.get(kategorie, 0) + 1

    # ---- Voelker, Welten, Gelaende ----------------------------------------
    fraktionen = voelker.get("fraktionen") or {}
    if isinstance(fraktionen, list):
        fraktionen = {str(f.get("kennung") or f.get("name") or i): f
                      for i, f in enumerate(fraktionen) if isinstance(f, dict)}
    welten_liste = welten.get("welten_belegt") or welten.get("welten") or []
    if isinstance(welten_liste, dict):
        welten_liste = list(welten_liste.values())
    # Heimatwelt: nur zaehlen, wenn die Datei das Feld fuehrt - sonst bleibt es None (unbekannt,
    # nicht 0). "0" waere hier eine Behauptung ueber die Daten, die die Daten nicht hergeben.
    mit_heimat = 0
    heimat_feld = False
    for welt in welten_liste:
        if isinstance(welt, dict):
            for schluessel in ("heimatwelt", "ist_heimatwelt", "heimat"):
                if schluessel in welt:
                    heimat_feld = True
                    if welt.get(schluessel):
                        mit_heimat += 1
                    break
    gelaendearten = gelaende.get("gelaendearten") or {}

    return {
        "waren": {"anzahl": len(waren_namen), "namen": waren_namen},
        "rezepte": {"anzahl": len(rezepte),
                    "hoechste_zutaten_je_rezept": hoechste,
                    "je_rezept": dict(sorted(zutaten_je_rezept.items())),
                    "zutaten_rohstoffe": zutaten_rohstoffe,
                    "ohne_kosten": sorted(rezepte_ohne_kosten),
                    "unbekannte_rohstoffe": dict(sorted(unbekannte_rohstoffe.items())),
                    "ohne_ware": sorted(set(rezepte) - set(waren_namen)),
                    "waren_ohne_rezept": sorted(set(waren_namen) - set(rezepte))},
        "einheiten": {"anzahl": len(einheiten), "namen": sorted(einheiten)},
        "forschungen": {"anzahl": len(forschungen), "namen": sorted(forschungen)},
        "gebaeude": {"anzahl": len(gebaeude_liste), "je_kategorie": dict(sorted(je_kategorie.items()))},
        "voelker": {"anzahl": len(fraktionen), "namen": sorted(fraktionen)},
        "welten": {"anzahl": len(welten_liste),
                   "namen": sorted(str(w.get("name") if isinstance(w, dict) else w)
                                   for w in welten_liste),
                   "mit_heimatwelt": mit_heimat if heimat_feld else None},
        "gelaendearten": {"anzahl": len(gelaendearten),
                          "namen": sorted(gelaendearten) if isinstance(gelaendearten, dict) else []},
        "werkstaetten": {"quelle": "data/items.json, Feld werkstatt",
                         "je_werkstatt": {k: sorted(v) for k, v in sorted(werkstatt_waren.items())},
                         "je_werkstatt_anzahl": {k: len(v) for k, v in sorted(werkstatt_waren.items())},
                         "rezepte_mit_werkstattfeld": rezept_hat_werkstatt},
        "quellen": {"daten_ordner": os.path.basename(os.path.normpath(daten_ordner)),
                    "dateien": ["items.json", "warenrezepte.json", "units.json", "research.json",
                                "buildings.json", "voelker.json", "welten.json", "gelaende.json"]},
    }


def textbreiten(zaehlung: dict) -> dict:
    """Die laengsten Namen in px - nur wenn Tk verfuegbar ist, sonst ein leerer Vermerk.

    Gemessen wird mit `font.measure` an der gerenderten Schrift (16 px, wie der Kleintext im
    Lager), nicht gerechnet: Tk rundet Pixelgroessen auf ganze Punkte (Register 548).
    """
    try:
        import tkinter as tk
        from tkinter import font as tkfont
    except Exception:                                        # noqa: BLE001
        return {"verfuegbar": False, "grund": "tkinter fehlt"}
    try:
        root = tk.Tk()
        root.withdraw()
        schrift = tkfont.Font(family="Arial", size=-16)
        messen = schrift.measure
    except Exception as fehler:                              # noqa: BLE001
        return {"verfuegbar": False, "grund": "kein Fenster: %s" % type(fehler).__name__}
    try:
        lang_waren = max(zaehlung["waren"]["namen"] or [""], key=messen)
        lang_einheiten = max(zaehlung["einheiten"]["namen"] or [""], key=messen)
        return {"verfuegbar": True, "schrift_px": 16,
                "laengste_ware": [lang_waren, messen(lang_waren)],
                "laengste_einheit": [lang_einheiten, messen(lang_einheiten)]}
    finally:
        try:
            root.destroy()
        except Exception:                                    # noqa: BLE001
            pass


def data_stand(pfad: str = DATEN) -> dict:
    """Letzter Commit, der `data/` geaendert hat - Hash und Datum (nicht der ganze Stand)."""
    befehl = ["git", "log", "-1", "--format=%h|%cd", "--date=format:%d.%m.%Y %H:%M", "--", "data"]
    try:
        p = subprocess.run(befehl, capture_output=True, text=True, cwd=HIER, timeout=60)
    except (OSError, subprocess.SubprocessError):
        return {"hash": "", "datum": ""}
    if p.returncode != 0 or not (p.stdout or "").strip():
        return {"hash": "", "datum": ""}
    hash_wert, _, datum = (p.stdout.strip().partition("|"))
    return {"hash": hash_wert, "datum": datum}


def als_markdown(zaehlung: dict, breiten: dict = None, stand: dict = None,
                 erzeugt: str = "") -> str:
    """Das Blatt als Markdown - feste Reihenfolge, jede Zahl mit ihrer Quelldatei."""
    z = zaehlung
    zeilen = ["# FAKTENBLATT - automatisch gezaehlt aus `data/` (M11)", ""]
    zeilen.append("**Erzeugt:** %s · **Stand von `data/`:** %s (`%s`)"
                  % (erzeugt or "-",
                     (stand or {}).get("datum") or "unbekannt",
                     (stand or {}).get("hash") or "-"))
    zeilen.append("")
    zeilen.append("> **Nicht von Hand aendern.** Diese Datei entsteht mit "
                  "`python -X utf8 tools/faktenblatt.py`; die Wache `test_faktenblatt` meldet jede "
                  "Abweichung zwischen Blatt und Daten. Wer eine Zahl im Auftrag nennt, nimmt sie "
                  "von hier - dann wandern keine abgetippten Zahlen mehr in Rezepte.")
    zeilen.append("")
    zeilen.append("## Waren, Rezepte, Zutaten")
    zeilen.append("")
    zeilen.append("| Groesse | Zahl | Quelle |")
    zeilen.append("|---|---|---|")
    zeilen.append("| Waren | **%d** | `data/items.json` (`waren`) |" % z["waren"]["anzahl"])
    zeilen.append("| Rezepte | **%d** | `data/warenrezepte.json` |" % z["rezepte"]["anzahl"])
    zeilen.append("| hoechste Zutatenzahl je Rezept | **%d** | `data/warenrezepte.json` (`kosten`) |"
                  % z["rezepte"]["hoechste_zutaten_je_rezept"])
    for rohstoff in ROHSTOFFE:
        eintrag = z["rezepte"]["zutaten_rohstoffe"].get(rohstoff) or {}
        zeilen.append("| Rezepte mit %s | %d (Summe %d) | `warenrezepte.json` |"
                      % (rohstoff, eintrag.get("rezepte", 0), eintrag.get("summe", 0)))
    zeilen.append("| Rezepte ohne Zutaten | %d | `warenrezepte.json` |"
                  % len(z["rezepte"]["ohne_kosten"]))
    zeilen.append("| Waren ohne Rezept | %d | Abgleich `items.json` gegen `warenrezepte.json` |"
                  % len(z["rezepte"]["waren_ohne_rezept"]))
    zeilen.append("")
    zeilen.append("## Werkstaetten")
    zeilen.append("")
    zeilen.append("Quelle: %s. " % z["werkstaetten"]["quelle"]
                  + ("Die Rezepte tragen das Feld bereits." if z["werkstaetten"]["rezepte_mit_werkstattfeld"]
                     else "**Die Rezepte tragen noch KEIN Feld `werkstatt`** (F-61/F-64 offen) - "
                          "die Zuordnung steht heute nur an der Ware."))
    zeilen.append("")
    zeilen.append("| Werkstatt | Waren | Anzahl |")
    zeilen.append("|---|---|---|")
    for fach, anzahl in z["werkstaetten"]["je_werkstatt_anzahl"].items():
        zeilen.append("| %s | %s | **%d** |" % (fach, ", ".join(z["werkstaetten"]["je_werkstatt"][fach]),
                                                anzahl))
    zeilen.append("")
    zeilen.append("## Einheiten, Forschungen, Gebaeude")
    zeilen.append("")
    zeilen.append("| Groesse | Zahl | Quelle |")
    zeilen.append("|---|---|---|")
    zeilen.append("| Einheiten | **%d** | `data/units.json` |" % z["einheiten"]["anzahl"])
    zeilen.append("| Forschungen | **%d** | `data/research.json` |" % z["forschungen"]["anzahl"])
    zeilen.append("| Gebaeude | **%d** | `data/buildings.json` |" % z["gebaeude"]["anzahl"])
    for kategorie, anzahl in z["gebaeude"]["je_kategorie"].items():
        zeilen.append("| davon %s | %d | `buildings.json` (`kategorie`) |" % (kategorie, anzahl))
    zeilen.append("")
    zeilen.append("## Voelker, Welten, Gelaende")
    zeilen.append("")
    zeilen.append("| Groesse | Zahl | Quelle |")
    zeilen.append("|---|---|---|")
    zeilen.append("| Voelker | **%d** | `data/voelker.json` |" % z["voelker"]["anzahl"])
    zeilen.append("| Welten | **%d** | `data/welten.json` |" % z["welten"]["anzahl"])
    if z["welten"]["mit_heimatwelt"] is None:
        zeilen.append("| Welten mit Heimatwelt | _nicht gefuehrt_ | `data/welten.json` hat kein Feld "
                      "`heimatwelt` je Welt (Stand 12.11.2026) |")
    else:
        zeilen.append("| Welten mit Heimatwelt | **%d** | `data/welten.json` |"
                      % z["welten"]["mit_heimatwelt"])
    zeilen.append("| Gelaendearten | **%d** | `data/gelaende.json` |" % z["gelaendearten"]["anzahl"])
    zeilen.append("")
    zeilen.append("## Textbreiten (Tk, 16 px)")
    zeilen.append("")
    if breiten and breiten.get("verfuegbar"):
        zeilen.append("| Name | Breite |")
        zeilen.append("|---|---|")
        for schluessel, titel in (("laengste_ware", "laengster Warenname"),
                                  ("laengste_einheit", "laengster Einheitenname")):
            name, px = breiten[schluessel]
            zeilen.append("| %s: %s | **%d px** |" % (titel, name, px))
    else:
        zeilen.append("_Fehlt: %s. Die Breiten werden erst gemessen, wenn ein Fenster zur "
                      "Verfuegung steht._" % ((breiten or {}).get("grund") or "Tk nicht befragt"))
    zeilen.append("")
    return "\n".join(zeilen) + "\n"


def schreiben(zaehlung: dict, md_pfad: str = MD_PFAD, json_pfad: str = JSON_PFAD,
              breiten: dict = None, stand: dict = None, erzeugt: str = "") -> tuple:
    """Markdown und JSON schreiben und beide Pfade zurueckgeben."""
    for pfad in (md_pfad, json_pfad):
        ordner = os.path.dirname(pfad)
        if ordner:
            os.makedirs(ordner, exist_ok=True)
    with open(md_pfad, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(als_markdown(zaehlung, breiten, stand, erzeugt))
    inhalt = {"stand": erzeugt, "data_stand": stand or {}, "textbreiten": breiten or {},
              "zaehlung": zaehlung}
    with open(json_pfad, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(inhalt, fh, ensure_ascii=False, indent=2, sort_keys=True)
        fh.write("\n")
    return md_pfad, json_pfad


def main(argv=None) -> int:
    import datetime
    leser = argparse.ArgumentParser(description="Faktenblatt aus data/ erzeugen (M11)")
    leser.add_argument("--ohne-tk", action="store_true", help="ohne Textbreiten")
    leser.add_argument("--daten", default=DATEN, help="anderer Datenordner (Pruefung)")
    args = leser.parse_args(argv)
    zaehlung = zaehlen(args.daten)
    breiten = {"verfuegbar": False, "grund": "--ohne-tk"} if args.ohne_tk else textbreiten(zaehlung)
    stand = data_stand()
    erzeugt = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
    md, js = schreiben(zaehlung, breiten=breiten, stand=stand, erzeugt=erzeugt)
    print("Faktenblatt: %d Waren, %d Rezepte, %d Einheiten, %d Forschungen, %d Gebaeude"
          % (zaehlung["waren"]["anzahl"], zaehlung["rezepte"]["anzahl"],
             zaehlung["einheiten"]["anzahl"], zaehlung["forschungen"]["anzahl"],
             zaehlung["gebaeude"]["anzahl"]))
    print("Markdown: %s" % md)
    print("JSON:     %s" % js)
    return 0


if __name__ == "__main__":
    sys.exit(main())
