"""data/units.json aus den Originalquellen bauen — und auflisten, was im Code erfunden ist.

Quellen (alle im Projekt):
  docs/original/ORIGINAL_Einheiten_Waren_Rohstoffe.md   Kosten, Kriegspunkte, Voraussetzung
  data/unit_stats.json                                  LE/AT/PA/SI/HE/RS/TP/GS/MU/SK
  data/icons_index.json                                 Icon-Datei je Originalname
"""
import json
import os
import re
import sys

ROOT = r"D:\Arbeiten\Nebelseetal_Remake"
DOC = os.path.join(ROOT, "docs", "original", "ORIGINAL_Einheiten_Waren_Rohstoffe.md")

ROHSTOFFE = {"siedler", "gold", "nahrung", "leder", "wolle", "metall", "mana", "holz",
             "stein", "pferde", "eisen", "metall"}
# Einzahl/Mehrzahl und Schreibvarianten aus der Originaldoku
ALIASE = {"pferd": "pferde", "pferde": "pferde", "siedler": "siedler", "steine": "stein",
          "steins": "stein", "nahrungs": "nahrung", "metalle": "metall"}
# Kurzformen der Einheiten-Tabelle auf die Namen der Warentabelle ziehen
WAREN_ALIASE = {"Paladinharnisch": "Magischer Paladinharnisch"}

# ------------------------------------------------------------------ Doku auswerten
tabelle = {}          # Name -> dict
kategorie = None
gebaeude_je_kategorie = {
    "Kampfeinheiten — Nahkampf (Kriegerakademie) — 5": ("Nahkampf", "Kriegerakademie"),
    "Kampfeinheiten — Fernkampf (Kriegerakademie) — 4": ("Fernkampf", "Kriegerakademie"),
    "Kundschafter (Diebesgilde) — 6": ("Kundschafter", "Diebesgilde"),
    "Karren (Stellmacher) — 6": ("Karren", "Stellmacher"),
    "Belagerungswaffen (Stellmacher) — 7": ("Belagerung", "Stellmacher"),
}

for zeile in open(DOC, encoding="utf-8"):
    z = zeile.strip()
    if z.startswith("### 1."):
        titel = re.sub(r"^###\s+\d+(\.\d+)*\s*", "", z).strip()
        kategorie = gebaeude_je_kategorie.get(titel)
        if kategorie is None:
            print(f"  (Abschnitt nicht zugeordnet: {titel!r})")
        continue
    if not kategorie or not z.startswith("|"):
        continue
    if set(z) <= set("|- "):          # Trennzeile
        continue
    spalten = [s.strip() for s in z.strip("|").split("|")]
    if len(spalten) < 5 or not spalten[0].isdigit():
        continue
    # Spalten NICHT nach Position raten — die Tabellen haben 5 bis 7 Spalten.
    # Stattdessen inhaltlich erkennen: Voraussetzung ist das Feld, das auf eine
    # Forschungsart mit Stufe passt; Kosten ist das erste Feld mit "Zahl Wort";
    # Ladung ist ein reines Zahlenfeld dazwischen.
    felder = spalten[1:]
    name = felder[0]
    punkte = felder[1]
    rest = felder[2:]
    vor_pat = re.compile(r"^(Kriegskunst|Heimlichkeit|Wagenbau)\s+\d+$")
    kosten_pat = re.compile(r"\d+\s+\S")
    kosten_text, vor_text, ladung = None, None, None
    for f in rest:
        if vor_text is None and vor_pat.match(f):
            vor_text = f
            continue
        if kosten_text is None and kosten_pat.search(f) and not vor_pat.match(f):
            kosten_text = f
            continue
        if (ladung is None and kosten_text is None and f.isdigit()):
            ladung = int(f)
    tabelle[name] = {
        "kategorie": kategorie[0],
        "gebaeude": kategorie[1],
        "kriegspunkte": int(punkte) if punkte.isdigit() else None,
        "ladung": ladung,
        "kosten_text": kosten_text or "",
        "voraussetzung_text": vor_text or "—",
    }
print(f"Einheiten aus der Originaldoku gelesen: {len(tabelle)}")


def zerlege_kosten(text):
    """'1 Siedler, 250 Gold, 1 Kurzschwert' -> ({'siedler':1,'gold':250}, ['Kurzschwert'])"""
    roh, waren = {}, []
    for teil in re.split(r",\s*", text):
        m = re.match(r"^(\d+)\s+(.+)$", teil.strip())
        if not m:
            continue
        anzahl, was = int(m.group(1)), m.group(2).strip()
        schluessel = ALIASE.get(was.lower(), was.lower())
        if schluessel in ROHSTOFFE:
            roh[schluessel] = roh.get(schluessel, 0) + anzahl
        else:
            waren += [was] * anzahl
    return roh, waren


def zerlege_voraussetzung(text):
    m = re.match(r"^(Kriegskunst|Heimlichkeit|Wagenbau)\s+(\d+)$", text.strip())
    if m:
        return {"forschung": m.group(1), "stufe": int(m.group(2))}
    return None


werte = json.load(open(os.path.join(ROOT, "data", "unit_stats.json"), encoding="utf-8"))
werte_liste = werte["einheiten"] if isinstance(werte["einheiten"], list) else \
    list(werte["einheiten"].values())
werte_je_name = {(e.get("name") or e.get("einheit")): e for e in werte_liste}

icons = json.load(open(os.path.join(ROOT, "data", "icons_index.json"), encoding="utf-8"))["icons"]

# ------------------------------------------------------------------ zusammenfuehren
einheiten = {}
nicht_original = []
for name, e in tabelle.items():
    roh, waren = zerlege_kosten(e["kosten_text"])
    waren = [WAREN_ALIASE.get(w, w) for w in waren]
    w = werte_je_name.get(name, {})
    felder = {}
    for k in ("LE", "AT", "PA", "SI", "HE", "RS", "TP_min", "TP_max", "GS", "MU", "SK"):
        felder[k] = w.get(k)
    fehlend = [k for k, v in felder.items() if v is None]
    icon = icons.get(name, {}).get("pfad")
    einheiten[name] = {
        "kategorie": e["kategorie"],
        "gebaeude": e["gebaeude"],
        "kosten": roh,
        "waren": waren,
        "voraussetzung": zerlege_voraussetzung(e["voraussetzung_text"]),
        "kriegspunkte": e["kriegspunkte"],
        "werte": felder,
        "icon": icon,
        "ladung": e["ladung"],
        "nicht_original": ([] if not fehlend else
                           [f"werte.{k} (in der Vorlage nicht abgedruckt)" for k in fehlend]),
    }
    if fehlend:
        nicht_original.append((name, fehlend))

out = {
    "_hinweis": ("Nur Originalangaben aus dem Handbuch 2009 und der Spielanleitung 2005. "
                 "Felder, die die Vorlage nicht hergibt, sind null und stehen in 'nicht_original'. "
                 "Es ist KEIN Wert geraten."),
    "_quelle": "docs/original/Nebelseetal_Spielanleitung_2009.pdf, docs/original/Spielanleitung_2005/",
    "anzahl": len(einheiten),
    "einheiten": einheiten,
}
p = os.path.join(ROOT, "data", "units.json")
json.dump(out, open(p, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print(f"geschrieben: {p}  ({os.path.getsize(p)} Byte, {len(einheiten)} Einheiten)")

# ------------------------------------------------------------------ Pruefung
print("\n=== Pruefung ===")
mit_icon = sum(1 for e in einheiten.values() if e["icon"])
mit_werten = sum(1 for e in einheiten.values() if sum(1 for v in e["werte"].values() if v is not None) >= 8)
mit_kosten = sum(1 for e in einheiten.values() if e["kosten"] or e["waren"])
mit_punkten = sum(1 for e in einheiten.values() if e["kriegspunkte"] is not None)
print(f"  Icon gesetzt:        {mit_icon}/{len(einheiten)}")
print(f"  Werte >=8 belegt:    {mit_werten}/{len(einheiten)}")
print(f"  Kosten belegt:       {mit_kosten}/{len(einheiten)}")
print(f"  Kriegspunkte belegt: {mit_punkten}/{len(einheiten)}")
print(f"  Einheiten mit Luecken: {len(nicht_original)}")
for n, f in nicht_original[:6]:
    print(f"    {n}: {', '.join(f)}")

# ------------------------------------------------------------------ Code-Abgleich
print("\n=== Was im Code erfunden ist (nicht im Original) ===")
sys.path.insert(0, os.path.join(ROOT, "src"))
os.chdir(os.path.join(ROOT, "src"))
import main as M


def normal(s: str) -> str:
    """Namen vergleichbar machen: klein, ohne Umlaute, ohne Trenner."""
    s = s.lower().replace("ß", "ss")
    for a, b in (("ä", "a"), ("ö", "o"), ("ü", "u")):
        s = s.replace(a, b)
    return re.sub(r"[^a-z0-9]", "", s)


original_norm = {normal(n): n for n in einheiten}
code_norm = {normal(u.name): k for k, u in M.UNITS.items()}

erfunden = [M.UNITS[k].name for k in M.UNITS if normal(M.UNITS[k].name) not in original_norm]
treffer = [M.UNITS[k].name for k in M.UNITS if normal(M.UNITS[k].name) in original_norm]
fehlend_code = [n for nn, n in original_norm.items() if nn not in code_norm]

print(f"  Einheiten im Code: {len(M.UNITS)}")
print(f"    davon aus dem Original: {len(treffer)} -> {', '.join(sorted(treffer))}")
print(f"    erfunden ({len(erfunden)}): {', '.join(sorted(erfunden))}")
print(f"  Originaleinheiten, die im Code fehlen ({len(fehlend_code)}): {', '.join(fehlend_code)}")
print(f"\n  Rohstoffe im Code ({len(M.RESOURCES)}): {M.RESOURCES}")
print(f"    Original: Holz, Stein, Metall, Mana, Nahrung, Gold, Wolle, Leder, Pferde")
print(f"  Waren im Code: {len(M.GOODS)}")
print(f"  Forschungen im Code: {len(M.RESEARCHES)} (Original: 21)")
print(f"  Gebaeude im Code: {len(M.BUILDINGS)} (Original: 20)")
