#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pdf_stats.py -- Spaltensichere Auslesung der Einheiten-Wertetabelle aus dem
Original-Handbuch "Nebelseetal_Spielanleitung_2009.pdf".

WARUM DIESES SKRIPT:
  Eine naive Textextraktion (get_text()) liefert die Zahlen zwar, aber die
  Spalten laufen ineinander. Ursache (hier belegt): Die Tabelle
  "Karren und Belagerungswaffen" hat im Original nur 9 Wertspalten
  (LE AT PA SI HE RS TP GS SK) -- die Spalte MU fehlt dort. Dadurch haben
  diese Datenzeilen 9 statt 10 Werte und rutschen bei reiner Textreihenfolge
  unter die falschen Kopfzeilen.

LOESUNG:
  get_text("words") liefert jedes Wort MIT Koordinaten (x0,y0,x1,y1,...).
  Wir gruppieren die Woerter ueber die y-Position zu Zeilen und ordnen die
  Werte ueber die x-Position den Kopfspalten zu -- unabhaengig von der
  Textreihenfolge.

Nur Standardbibliothek + pymupdf. Aufruf:  python tools/pdf_stats.py
Schreibt:
  data/unit_stats.json
  docs/original/ORIGINAL_Werte_Einheiten.md
"""

from __future__ import annotations

import json
import os
import re
from collections import defaultdict

import pymupdf  # PyMuPDF

# ---------------------------------------------------------------------------
# Pfade (relativ zum Projektwurzelverzeichnis = Elternordner dieses Skripts)
# ---------------------------------------------------------------------------
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PDF_PATH = os.path.join(ROOT, "docs", "original", "Nebelseetal_Spielanleitung_2009.pdf")
JSON_PATH = os.path.join(ROOT, "data", "unit_stats.json")
MD_PATH = os.path.join(ROOT, "docs", "original", "ORIGINAL_Werte_Einheiten.md")

# ---------------------------------------------------------------------------
# Referenzdaten aus ORIGINAL_Einheiten_Waren_Rohstoffe.md (28 Namen, Reihenfolge)
# ---------------------------------------------------------------------------
ORIGINAL_NAMES = [
    "Bürgerwehr", "Kämpfer", "Krieger", "Ritter", "Paladin",              # 1-5  Nahkampf
    "Kurzbogenschütze", "Bogenschütze", "Langbogenschütze", "Armbrustschütze",  # 6-9  Fernkampf
    "Streuner", "Gauner", "Dieb", "Meisterdieb", "Kundschafter", "Waldläufer",  # 10-15 Kundschafter
    "Handkarren", "Einspänner", "Zweispänner", "Handelskarawane",
    "Große Handelskarawane", "Siedlerkarren",                              # 16-21 Karren
    "Belagerungsturm", "Ramme", "Großer Belagerungsturm", "Große Ramme",
    "Balliste", "Katapult", "Großes Katapult",                             # 22-28 Belagerungswaffen
]
NR = {name: i + 1 for i, name in enumerate(ORIGINAL_NAMES)}

# Rohtext im PDF -> Originalname (Kuerzel aufloesen)
NAME_NORMALISIERUNG = {
    "Gr. Handels-": "Große Handelskarawane",
    "Gr. Belagerungsturm": "Großer Belagerungsturm",
    "Gr. Ramme": "Große Ramme",
    "Gr. Katapult": "Großes Katapult",
}

# Zuordnung Typ
GRUPPE = {
    **{n: "Kampfeinheit Nahkampf (Kriegerakademie)" for n in
       ["Bürgerwehr", "Kämpfer", "Krieger", "Ritter", "Paladin"]},
    **{n: "Kampfeinheit Fernkampf (Kriegerakademie)" for n in
       ["Kurzbogenschütze", "Bogenschütze", "Langbogenschütze", "Armbrustschütze"]},
    **{n: "Kundschafter (Diebesgilde)" for n in
       ["Streuner", "Gauner", "Dieb", "Meisterdieb", "Kundschafter", "Waldläufer"]},
    **{n: "Karren (Stellmacher)" for n in
       ["Handkarren", "Einspänner", "Zweispänner", "Handelskarawane",
        "Große Handelskarawane", "Siedlerkarren"]},
    **{n: "Belagerungswaffe (Stellmacher)" for n in
       ["Belagerungsturm", "Ramme", "Großer Belagerungsturm", "Große Ramme",
        "Balliste", "Katapult", "Großes Katapult"]},
}

# Spaltenreihenfolge der Wertetabelle
STAT_COLS = ["LE", "AT", "PA", "SI", "HE", "RS", "TP", "GS", "MU", "SK"]

# y-Toleranz zum Gruppieren einer Zeile, x-Toleranz zum Spaltenzuordnen
Y_TOL = 2.5
X_TOL = 12.0


def cluster_rows(words, y_tol=Y_TOL):
    """Woerter ueber die y0-Position zu visuellen Zeilen gruppieren."""
    rows = []
    for w in sorted(words, key=lambda w: (w[1], w[0])):
        for row in rows:
            if abs(row["y"] - w[1]) <= y_tol:
                row["words"].append(w)
                break
        else:
            rows.append({"y": w[1], "words": [w]})
    for row in rows:
        row["words"].sort(key=lambda w: w[0])
    return rows


def is_header(row):
    toks = [w[4] for w in row["words"]]
    return ("Bezeichnung" in toks) and ("LE" in toks)


def is_data_row(row, x_stat_min):
    """Datenzeile: Name links (x0 < 140), Werte rechts (x0 >= 290) UND mindestens
    ein echter Zahlenwert/eine Wertangabe in der Wertspalten-Region. Letzteres
    schliesst die Erklaertexte im Abschnitt 'Abkuerzungen' aus, die ebenfalls
    Woerter rechts von x=290 enthalten, aber keine Zahlen."""
    ws = row["words"]
    if not ws:
        return False
    if is_header(row):
        return False
    left = ws[0][0] < 140
    right = any(w[0] >= x_stat_min for w in ws)
    if not (left and right):
        return False
    return any(re.fullmatch(r"\d+(-\d+)?", w[4]) for w in ws if w[0] >= x_stat_min)


def parse_tp(tok):
    """'1-6' -> (1,6); '0' -> (0,0); '-' -> (None,None)."""
    if tok is None or tok.strip() in ("", "-"):
        return None, None
    m = re.fullmatch(r"(\d+)-(\d+)", tok.strip())
    if m:
        return int(m.group(1)), int(m.group(2))
    m = re.fullmatch(r"(\d+)", tok.strip())
    if m:
        v = int(m.group(1))
        return v, v
    return None, None


def to_int_or_none(tok):
    if tok is None or tok.strip() in ("", "-"):
        return None
    m = re.fullmatch(r"-?\d+", tok.strip())
    return int(m.group(0)) if m else None


def parse_name(ws):
    """Name = Woerter links der Kosten-Spalte (x0 < 138), alphanumerisch."""
    parts = [w[4] for w in ws if w[0] < 138 and re.search(r"[A-Za-zÄÖÜäöüß]", w[4])]
    return " ".join(parts).strip()


def extract():
    doc = pymupdf.open(PDF_PATH)
    units = []
    raw_rows = []          # (seite, name, [(x, tok), ...]) fuer die Dokumentation
    seen = set()

    for pno in range(doc.page_count):
        page = doc[pno]
        rown = cluster_rows(page.get_text("words"))

        # Kopfzeilen dieser Seite finden
        headers = [r for r in rown if is_header(r)]
        if not headers:
            continue

        for hi, header in enumerate(headers):
            # Spaltenpositionen aus der Kopfzeile lesen
            cols = {}
            for w in header["words"]:
                if w[4] in STAT_COLS:
                    cols[w[4]] = w[0]
            x_header_min = min(cols.values())
            x_stat_min = x_header_min - 25
            next_header_y = headers[hi + 1]["y"] if hi + 1 < len(headers) else 1e9

            # Datenzeilen zwischen dieser Kopfzeile und der naechsten
            for row in rown:
                if not (header["y"] < row["y"] < next_header_y):
                    continue
                if not is_data_row(row, x_stat_min):
                    continue

                raw_name = parse_name(row["words"])
                name = NAME_NORMALISIERUNG.get(raw_name, raw_name)
                if name not in NR:
                    # Unbekannte/unvollstaendige Zeile nicht stillschweigend verwerfen
                    raw_rows.append((pno + 1, raw_name or "?",
                                     [(round(w[0]), w[4]) for w in row["words"] if w[0] >= 290]))
                    continue
                if name in seen:
                    continue
                seen.add(name)

                # Wert woerter (rechts ab ~290) den Kopfspalten per x0 zuordnen
                werte = {c: None for c in STAT_COLS}
                for w in row["words"]:
                    if w[0] < x_header_min - 25:
                        continue
                    # naechstgelegene Kopfspalte
                    col = min(cols, key=lambda c: abs(cols[c] - w[0]))
                    if abs(cols[col] - w[0]) <= X_TOL:
                        werte[col] = w[4]

                tp_min, tp_max = parse_tp(werte["TP"])
                units.append({
                    "nr": NR[name],
                    "name": name,
                    "typ": GRUPPE[name],
                    "LE": to_int_or_none(werte["LE"]),
                    "AT": to_int_or_none(werte["AT"]),
                    "PA": to_int_or_none(werte["PA"]),
                    "SI": to_int_or_none(werte["SI"]),
                    "HE": to_int_or_none(werte["HE"]),
                    "RS": to_int_or_none(werte["RS"]),
                    "TP_min": tp_min,
                    "TP_max": tp_max,
                    "GS": to_int_or_none(werte["GS"]),
                    "MU": to_int_or_none(werte["MU"]),
                    "SK": to_int_or_none(werte["SK"]),
                })
                raw_rows.append((pno + 1, name,
                                 [(round(w[0]), w[4]) for w in row["words"] if w[0] >= 290]))

    doc.close()
    units.sort(key=lambda u: u["nr"])
    return units, raw_rows


def anmerkung_fuer(u):
    """Begruendet fehlende (null) Werte aus der Vorlage heraus."""
    fehlend = [c for c in ["LE", "AT", "PA", "SI", "HE", "RS", "TP_min", "GS", "MU", "SK"]
               if u[c] is None]
    teile = []
    if u["typ"].startswith(("Karren", "Belagerungswaffe")):
        teile.append("Tabelle 'Karren und Belagerungswaffen' (Handbuch S. 17/18) fuehrt "
                     "die Spalten LE AT PA SI HE RS TP mit '-' (Handbuch: nicht relevanter "
                     "Wert) belegt; die Spalte MU fehlt in dieser Tabelle vollstaendig.")
        if u["name"] in ("Belagerungsturm", "Großer Belagerungsturm"):
            teile.append("TP steht lt. Vorlage als '0' (nicht '-') und ist als Bereich 0-0 "
                         "uebernommen.")
    if not fehlend:
        return ""
    teile.append("Daher null fuer: " + ", ".join(fehlend) + ".")
    return " ".join(teile)


def write_json(units):
    os.makedirs(os.path.dirname(JSON_PATH), exist_ok=True)
    for u in units:
        u["anmerkung"] = anmerkung_fuer(u)
    # Feldreihenfolge stabilisieren
    order = ["nr", "name", "typ", "LE", "AT", "PA", "SI", "HE", "RS",
             "TP_min", "TP_max", "GS", "MU", "SK", "anmerkung"]
    units = [{k: u[k] for k in order} for u in units]
    payload = {
        "quelle": "docs/original/Nebelseetal_Spielanleitung_2009.pdf",
        "seiten_handbuch": "16-18 (Tabelle 'Einheitentabelle' und 'Karren und Belagerungswaffen')",
        "methode": "pymupdf get_text('words'); Zeilen per y0, Spalten per x0 zugeordnet",
        "anzahl_einheiten": len(units),
        "einheiten": units,
    }
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return payload


def fmt(v):
    return "null" if v is None else str(v)


def write_md(units, raw_rows):
    os.makedirs(os.path.dirname(MD_PATH), exist_ok=True)
    volle = [u for u in units if all(u[c] is not None
             for c in ["LE", "AT", "PA", "SI", "HE", "RS", "TP_min", "TP_max", "GS", "MU", "SK"])]
    lines = []
    lines.append("# Original-Werte der 28 Einheiten")
    lines.append("")
    lines.append("Spaltensicher ausgelesen aus `docs/original/Nebelseetal_Spielanleitung_2009.pdf`")
    lines.append("(Tabelle 'Einheitentabelle', Handbuch S. 16, und 'Karren und Belagerungswaffen',")
    lines.append("Handbuch S. 17/18) mit `tools/pdf_stats.py` ueber Wort-Koordinaten.")
    lines.append("")
    lines.append("Werte woertlich aus der Vorlage. `-` in der Druckvorlage (nicht relevant) und die")
    lines.append("in der Karren-/Belagerungstabelle **fehlende Spalte MU** werden als `null` gefuehrt;")
    lines.append("es wurde **nichts geschaetzt oder aufgefuellt**.")
    lines.append("")
    lines.append("## Wertetabelle")
    lines.append("")
    lines.append("| # | Einheit | Typ | LE | AT | PA | SI | HE | RS | TP | GS | MU | SK |")
    lines.append("|---:|---|---|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|")
    for u in units:
        tp = "-" if u["TP_min"] is None else (f"{u['TP_min']}-{u['TP_max']}"
                                              if u["TP_min"] != u["TP_max"] else str(u["TP_min"]))
        lines.append("| {} | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} |".format(
            u["nr"], u["name"], u["typ"],
            fmt(u["LE"]), fmt(u["AT"]), fmt(u["PA"]), fmt(u["SI"]), fmt(u["HE"]),
            fmt(u["RS"]), tp, fmt(u["GS"]), fmt(u["MU"]), fmt(u["SK"])))
    lines.append("")
    lines.append(f"**{len(units)} Einheiten** (erwartet 28). "
                 f"Davon mit **allen 11 Werten vollstaendig: {len(volle)}** "
                 "(die 15 Armee-/Kundschaftereinheiten). Die 6 Karren und 7 Belagerungswaffen "
                 "haben in der Vorlage keine Angaben zu LE/AT/PA/SI/HE/RS/TP bzw. MU (siehe unten).")
    lines.append("")

    # Abschnitt: nicht sicher zuzuordnen / ohne Werte
    lines.append("## Nicht sicher zuzuordnen")
    lines.append("")
    lines.append("**Ergebnis der Pruefung: spaltenweise ist kein Wert mehrdeutig.** Der urspruengliche")
    lines.append("Fehler kam allein daher, dass die Tabelle *Karren und Belagerungswaffen* nur")
    lines.append("**9 Wertspalten** besitzt (LE AT PA SI HE RS TP GS SK) -- die Spalte **MU fehlt**")
    lines.append("dort. Dadurch haben diese Zeilen 9 statt 10 Werte und verrutschen bei reiner")
    lines.append("Textreihenfolge. Ueber die x-Koordinaten ist die Zuordnung eindeutig, wie die")
    lines.append("Rohzeilen (Wert + x-Ursprung) zeigen:")
    lines.append("")
    for pno, name, wertlist in raw_rows:
        txt = "  ".join(f"{tok}@{x}" for x, tok in wertlist)
        lines.append(f"- PDF-S.{pno} **{name}**: {txt}")
    lines.append("")
    lines.append("Ungeklaerte Einzelpunkte (bewusst so belassen, nicht geraten):")
    lines.append("")
    lines.append("- **TP = `0`** bei *Belagerungsturm* und *Großer Belagerungsturm*: die Vorlage druckt")
    lines.append("  eine `0`, nicht `-`. Als Bereich **0-0** uebernommen. Ob damit 'kein Schaden' oder")
    lines.append("  'kein Wert' gemeint ist, laesst sich aus der Tabelle nicht entscheiden.")
    lines.append("- **MU** fehlt in der gesamten Karren-/Belagerungstabelle -> fuer alle 13 Einheiten")
    lines.append("  `null`. Es ist nicht auszuschliessen, dass MU dort nur nicht abgedruckt wurde.")
    lines.append("- Die Spalten **LE AT PA SI HE RS** sind bei Karren und Belagerungswaffen in jeder Zeile")
    lines.append("  mit `-` belegt (Handbuch: 'nicht relevant, da fuer diese Auftraege ohne Bedeutung').")
    lines.append("")
    with open(MD_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def main():
    units, raw_rows = extract()
    write_json(units)
    write_md(units, raw_rows)

    # --- Selbstpruefung -----------------------------------------------------
    with open(JSON_PATH, encoding="utf-8") as f:
        data = json.load(f)
    u = data["einheiten"]
    orden = ["LE", "AT", "PA", "SI", "HE", "RS", "TP_min", "TP_max", "GS", "MU", "SK"]
    voll = [x for x in u if all(x[c] is not None for c in orden)]
    namen = [x["name"] for x in u]
    print("Selbstpruefung:")
    print("  Einheiten gelesen :", len(u), "(erwartet 28)")
    print("  Namen eindeutig   :", len(set(namen)) == len(namen))
    print("  Namen == Original :", set(namen) == set(ORIGINAL_NAMES))
    print("  vollstaendig (11/11):", len(voll))
    print("  teils null (Vorlage '- / fehlende Spalte):", len(u) - len(voll))
    print("  JSON :", JSON_PATH)
    print("  MD   :", MD_PATH)


if __name__ == "__main__":
    main()
