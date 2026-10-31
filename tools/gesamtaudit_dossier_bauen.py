"""Baut das begrenzte Dossier fuer den Gesamtaudit (ein starker Modellaufruf).

Daniel (31.10.2026): "mindestens einmal ein grosses Model unser Gesamtprojekt anschauen
lassen ... und das Model alles mit den Spiel bekannten Infos abgleichen lassen aber in
einem begrenzten Format das es keine unendlichen Kosten verursacht."

Deshalb KEIN Agentenlauf ueber das ganze Repository (20.772 Zeilen Quellcode), sondern
EIN Dossier mit festem Zeichenbudget:

  A  Rahmen und Spielbild                (kurz, aus dem Projekt)
  B  Quellenlage des Originals           (Register + belegte Auswertungen)
  C  Mechanik-Inventar des CODES         (erzeugt: Module, Konstanten, Daten, Funktionen)
  D  Offene Luecken und bekannte Fehler  (aus den Modulen selbst + Fehlerregister)
  E  Auftrag und Ausgabeformat           (nicht hier, im Lauf-Skript)

Aufruf:  python -X utf8 tools/gesamtaudit_dossier_bauen.py
Ergebnis: docs/audits/GESAMTAUDIT_DOSSIER_20261031.md  + Groessen-/Kostenschaetzung
"""
from __future__ import annotations

import json
import os
import re
import sys

HIER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUELLE = os.path.join(HIER, "src")
ZIEL = os.path.join(HIER, "docs", "audits", "GESAMTAUDIT_DOSSIER_20261031.md")

# Zeichenbudget (1 Token ~ 3,5 Zeichen deutsch/Code)
BUDGET_GESAMT = 165_000


def lies(pfad: str, max_zeichen: int = 0) -> str:
    with open(os.path.join(HIER, pfad), encoding="utf-8", errors="replace") as f:
        text = f.read()
    if max_zeichen and len(text) > max_zeichen:
        return text[:max_zeichen] + f"\n... [gekuerzt, Original {len(text)} Zeichen]"
    return text


def abschnitt(titel: str, inhalt: str) -> str:
    return f"\n\n{'=' * 78}\n{titel}\n{'=' * 78}\n\n{inhalt.strip()}\n"


# ---------------------------------------------------------------- A  Rahmen

def rahmen() -> str:
    return f"""Es geht um PYTHON-NEBELSEETAL-REMAKE: eine Einzelspieler-Neuauflage des
Browserspiels "Nebelseetal Online" (deutsches Browsergame, Spielanleitung 2009, Vorversion 2006).
Technik: Python + tkinter, kein Server, kein Multiplayer. Gespielt wird gegen Bots, Spieluhr
mit Faktor {json.load(open(os.path.join(HIER, 'data', 'spielzeit.json'), encoding='utf-8'))['faktor']}
(1 echte Sekunde = 180 Spielsekunden; 1 Spielstunde = 20 echte Sekunden).

DANIELS REGELN (gelten ueber allem):
1. Originaltreue: jede Mechanik wird gegen die Originalquellen gehalten. Handbuch 2009 ist die
   Richtschnur fuer Balance; die Vorversion 2006 zeigt die Entwicklung und fuellt Luecken.
   Abweichungen zwischen beiden werden dokumentiert, NICHTS wird stillschweigend angeglichen.
2. Was die Quellen nicht hergeben, ist VORSCHLAG und wird im Code und im Spiel als VORSCHLAG
   gekennzeichnet - es wird nichts erfunden und nichts "geschaetzt, bis es passt".
3. "Einmal pruefen, festschreiben, nicht tausendmal pruefen": was im Pruefregister als FERTIG
   steht, wird nicht erneut angefasst.
4. Der Spieler soll alles SEHEN und PLANEN koennen (Wegzeiten, Ankunft, Punkte, Kosten).
5. Ein Spiel gegen Bots muss in ueberschaubarer Zeit spielbar sein, ohne dass Regeln erfunden
   werden, nur damit es schneller geht.

PROJEKTSTAND: 105 Commits, Pruefstand 60 von 60 Pruefdateien gruen (568 s). Genau EIN
Entwicklungsprotokoll. Sprache im Code: deutsch, teils ASCII-only in Logikmodulen."""


# ---------------------------------------------------------- B  Quellenlage

def quellen() -> str:
    teile = []
    teile.append(abschnitt("B1  PRUEFREGISTER DES ORIGINALS (40 Punkte, je mit Seite/Zeile)",
                           lies("docs/PRUEFREGEL_ORIGINAL.md")))
    teile.append(abschnitt("B2  BELEGTE AUSWERTUNG: Kampf, Auftraege, Punkte, Schutz, Spieldaten",
                           lies("docs/original/ORIGINAL_Kampf_und_Punkte.md")))
    teile.append(abschnitt("B3  BELEGTE AUSWERTUNG: Gebaeude, Freischaltung, Erträge (Handbuch S. 9-14)",
                           lies("docs/quellen/ORIGINAL_GEBAEUDE_UND_FREISCHALTUNG.md")))
    teile.append(abschnitt("B4  ABWEICHUNGEN 2006 GEGEN 2009 (Balance 2009, Struktur beide)",
                           lies("docs/quellen/ABWEICHUNGEN_2006_zu_2009.md")))
    return "".join(teile)


# --------------------------------------------------- C  Mechanik-Inventar

def inventar() -> str:
    sys.path.insert(0, QUELLE)

    module = []
    for name in sorted(os.listdir(QUELLE)):
        if not name.endswith(".py"):
            continue
        p = os.path.join(QUELLE, name)
        with open(p, encoding="utf-8", errors="replace") as f:
            text = f.read()
        zeilen = text.count("\n") + 1
        zweck = ""
        m = re.search(r'^"""(.*?)(?:"""|$)', text, re.S)
        if m:
            zweck = " ".join(m.group(1).split())[:220]
        module.append((name, zeilen, zweck))
    modul_text = "\n".join(f"- {n} ({z} Zeilen): {z2 or '(kein Kopfkommentar)'}"
                           for n, z, z2 in module)

    # Modul-Konstanten (GROSS = ...) - die eigentlichen Spielzahlen
    konst = []
    for name, _z, _z2 in module:
        with open(os.path.join(QUELLE, name), encoding="utf-8", errors="replace") as f:
            text = f.read()
        treffer = re.findall(r"^([A-ZÄÖÜ][A-ZÄÖÜ0-9_]{2,})\s*(?::[^=\n]+)?=\s*(.+)$",
                             text, re.M)
        for k, wert in treffer:
            wert = wert.strip()
            if len(wert) > 120:
                wert = wert[:120] + " ..."
            konst.append(f"- {name}: {k} = {wert}")
    # nur Konstanten mit Zahl oder kurzer Liste, Dubletten raus
    gesehen, konst_kurz = set(), []
    for zeile in konst:
        if zeile in gesehen:
            continue
        gesehen.add(zeile)
        konst_kurz.append(zeile)
    konst_text = "\n".join(konst_kurz[:260])

    # Funktionsnamen je Modul (die Mechanik selbst)
    funk = []
    for name, _z, _z2 in module:
        if name in ("main.py",):
            continue
        with open(os.path.join(QUELLE, name), encoding="utf-8", errors="replace") as f:
            text = f.read()
        namen = re.findall(r"^def ([a-zA-Z_][\w]*)\(([^)]*)\)", text, re.M)
        if namen:
            kurz = ", ".join(f"{n}({'…' if a else ''})" for n, a in namen[:18])
            funk.append(f"- {name}: {kurz}")
    funk_text = "\n".join(funk)

    # Datendateien
    daten = []
    B = json.load(open(os.path.join(HIER, "data", "buildings.json"), encoding="utf-8"))
    daten.append("## Gebaeude (data/buildings.json) — Name | Kategorie | Voraussetzung | max je Siedlung | "
                 "Baupreise Stufe 1 | Wirkung")
    for g in B.get("gebaeude", []):
        preis = g.get("stufen") or []
        p1 = preis[0].get("kosten") if preis and isinstance(preis[0], dict) else g.get("kosten")
        daten.append(f"- {g.get('name')} | {g.get('kategorie')} | {g.get('voraussetzung')} | "
                     f"{g.get('max_je_siedlung')} | {json.dumps(p1, ensure_ascii=False)} | "
                     f"{str(g.get('wirkung'))[:150]}")
    R = json.load(open(os.path.join(HIER, "data", "resources.json"), encoding="utf-8"))
    daten.append("\n## Rohstoffe (data/resources.json)")
    for k, v in (R if isinstance(R, dict) else {}).items():
        if k.startswith("_"):
            continue
        daten.append(f"- {k}: {json.dumps(v, ensure_ascii=False)[:200]}")
    F = json.load(open(os.path.join(HIER, "data", "research.json"), encoding="utf-8"))
    daten.append("\n## Forschungen (data/research.json)")
    forschungen = F.get("forschungen")
    if isinstance(forschungen, dict):
        for name_f, eintrag in forschungen.items():
            if not isinstance(eintrag, dict):
                daten.append(f"- {name_f} | {str(eintrag)[:160]}")
                continue
            daten.append(f"- {name_f} | {json.dumps(eintrag.get('wirkung'), ensure_ascii=False)[:160]} "
                         f"| kosten {json.dumps(eintrag.get('kosten'), ensure_ascii=False)[:100]}")
    else:
        for f_ in (forschungen or []):
            daten.append(f"- {f_.get('name')} | {json.dumps(f_.get('wirkung'), ensure_ascii=False)[:160]} "
                         f"| kosten {json.dumps(f_.get('kosten'), ensure_ascii=False)[:100]}")
    U = json.load(open(os.path.join(HIER, "data", "units.json"), encoding="utf-8"))
    daten.append("\n## Einheiten (data/units.json) — Name | Gebaeude | Punkte | Werte | Ladung | Voraussetzung")
    for n, e in U.get("einheiten", {}).items():
        daten.append(f"- {n} | {e.get('gebaeude')} | {e.get('kriegspunkte')} | "
                     f"{json.dumps(e.get('werte'), ensure_ascii=False)} | {e.get('ladung')} | "
                     f"{json.dumps(e.get('voraussetzung'), ensure_ascii=False)}")
    W = json.load(open(os.path.join(HIER, "data", "warenrezepte.json"), encoding="utf-8"))
    daten.append("\n## Waren (data/warenrezepte.json) — Kosten | Dauer | Voraussetzungen")
    for k, v in (W.items() if isinstance(W, dict) else []):
        if k.startswith("_"):
            continue
        daten.append(f"- {k} | {json.dumps(v.get('kosten'), ensure_ascii=False)} | {v.get('dauer')} | "
                     f"{json.dumps(v.get('voraussetzungen'), ensure_ascii=False)}")
    G = json.load(open(os.path.join(HIER, "data", "gelaende.json"), encoding="utf-8"))
    daten.append("\n## Gelaende (data/gelaende.json)")
    gelaende = G.get("gelaendearten") if isinstance(G, dict) else G
    if isinstance(gelaende, dict):
        for k, v in gelaende.items():
            if not str(k).startswith("_"):
                daten.append(f"- {k}: {json.dumps(v, ensure_ascii=False)[:220]}")
    else:
        for eintrag in (gelaende or []):
            daten.append(f"- {json.dumps(eintrag, ensure_ascii=False)[:220]}")
    Gw = json.load(open(os.path.join(HIER, "data", "gebaeude_wirkung.json"), encoding="utf-8"))
    daten.append("\n## Gebaeude-Wirkungen (data/gebaeude_wirkung.json)")
    daten.append(json.dumps({k: v for k, v in Gw.items() if not k.startswith("_")},
                            ensure_ascii=False, indent=1)[:6000])
    Wl = json.load(open(os.path.join(HIER, "data", "welten.json"), encoding="utf-8"))
    daten.append("\n## Welten/Portal (data/welten.json)")
    daten.append(json.dumps({k: v for k, v in Wl.items() if not k.startswith("_")},
                            ensure_ascii=False, indent=1)[:3000])
    daten_text = "\n".join(daten)

    return (abschnitt("C1  MODULE des Quellcodes (src/)", modul_text)
            + abschnitt("C2  SPIELZAHLEN IM CODE (Modul-Konstanten, unverändert uebernommen)", konst_text)
            + abschnitt("C3  FUNKTIONEN JE MODUL (die Mechanik selbst, ohne UI)", funk_text)
            + abschnitt("C4  DATENDATEIEN (data/) - die im Spiel wirksamen Tabellen", daten_text))


# ------------------------------------------------- D  Luecken und Fehler

def luecken() -> str:
    sys.path.insert(0, QUELLE)
    teile = []
    for modul in ("auftraege", "kampfbericht", "punkte", "werkstatt", "spieloekonomie"):
        try:
            m = __import__(modul)
            f = getattr(m, "offene_luecken", None)
            if callable(f):
                teile.append(f"### {modul}.offene_luecken()\n```json\n"
                             + json.dumps(f(), ensure_ascii=False, indent=1)[:4500] + "\n```")
        except Exception as fehler:  # noqa: BLE001 - Dossier darf nie scheitern
            teile.append(f"### {modul}: nicht lesbar ({type(fehler).__name__}: {fehler})")
    teile.append(abschnitt("D2  Bekannte Fehler und Designpruefungen (docs/Fehlerregister_Nebelseetal.md)",
                           lies("docs/Fehlerregister_Nebelseetal.md", 14000)))
    teile.append(abschnitt("D3  Aktueller Stand (docs/AKTUELLER_STAND.md)",
                           lies("docs/AKTUELLER_STAND.md", 13000)))
    return abschnitt("D1  OFFENE LUECKEN, wie die Module sie selbst ausweisen", "\n\n".join(teile))


def main():
    text = (abschnitt("A  RAHMEN: Worum es geht und welche Regeln gelten", rahmen())
            + quellen() + inventar() + luecken())
    os.makedirs(os.path.dirname(ZIEL), exist_ok=True)
    with open(ZIEL, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    zeichen = len(text)
    token = zeichen / 3.5
    print(f"Dossier: {ZIEL}")
    print(f"Zeichen: {zeichen}  (Budget {BUDGET_GESAMT})")
    print(f"Tokens prompt ≈ {token:.0f}")
    print(f"Kostenschaetzung bei 0,66 USD/M prompt und 1,98 USD/M completion:")
    for aus in (15000, 25000, 40000):
        print(f"   completion {aus:>6} Token -> "
              f"{(token / 1e6 * 0.66 + aus / 1e6 * 1.98):.4f} USD")
    return 0


if __name__ == "__main__":
    sys.exit(main())
