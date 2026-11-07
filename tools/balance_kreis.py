# -*- coding: utf-8 -*-
"""B-1 Sollkurve aus den Daten (Ablauf Schritt 8, 07.11.2026, Sitzung 13).

Der Idealplan spielt die BELEGTE Aufbaukette Tag fuer Tag nach und schreibt daraus einen
Zielkorridor je Spieltag: unten = Ideal x 0,7, oben = Ideal x 1,1 (VORSCHLAG, siehe Datei).

Eingaben (alle mit Hash im Kopf der Ausgabe):
  data/resources.json             Startwerte und Ertraege je Gelaende (Handbuch 2009)
  data/baupreise.json             Baupreise (vier belegt, die uebrigen VORSCHLAG)
  data/research.json              Forschungen (Voraussetzungen; KOSTEN stehen nicht darin)
  data/units.json                 Einheiten (nur fuer den Hash - der Plan baut keine Armee)
  data/originalkarten/katalog.json + data/startkarte.json   Gelaende der belegten Startkarte

Der Plan baut in DIESER Reihenfolge, sobald er es bezahlen kann, auf dem besten freien Gelaende:
  Holzfäller, Steinmetz, Bibliothek, danach Goldmine und Farm (Baukunst-Gate), Haus bei Siedlernot.
Ein Spieltag sind 24 Spielstunden; ein Gebaeude erntet seine Stunden je Gelaende.

Aufruf:  python -X utf8 tools/balance_kreis.py --sollkurve [--wurzel <projektordner>] [--schreiben]
Ohne --schreiben wird nur gerechnet und gedruckt (die Pruefdatei nutzt das).
"""
import argparse
import hashlib
import io
import json
import os

HIER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Projektordner
STUNDEN_JE_TAG = 24  # ein Spieltag = 24 Spielstunden (Produktionsangaben sind je Stunde)
BAND_UNTEN = 0.7  # VORSCHLAG: unterer Rand des Korridors
BAND_OBEN = 1.1  # VORSCHLAG: oberer Rand des Korridors
PUNKTE_ZIEL = 3.3  # V-3 (docs/S0_TABELLEN_20261107.md): Punkte je Spieltag
GELAENDE_MAP = {"wald": "Wald", "berg": "Berg", "huegel": "Hügel", "grasland": "Grasland",
                "steppe": "Steppe", "nebelsee": "Nebelsee", "sumpf": "Sumpf"}  # Katalog -> Ertragsschluessel
# Wo ein Gebaeude stehen soll: erstes Gelaende mit Ertrag, das noch frei ist (Reihenfolge = Vorliebe).
BAU_GELAENDE = {"holzfaeller": ("Wald", "Steppe"), "steinmetz": ("Berg", "Hügel"),
                "goldmine": ("Berg", "Hügel"), "farm": ("Grasland", "Steppe"),
                "bibliothek": ("Grasland", "Steppe", "Wald"), "haus": ("Grasland", "Steppe", "Wald")}
# Reihenfolge des Idealplans (belegte Kette: Holzfäller -> Bibliothek -> Baukunst -> Goldmine/Farm).
REIHENFOLGE = ("holzfaeller", "holzfaeller", "steinmetz", "steinmetz", "bibliothek",
               "goldmine", "farm")
# Ist die Reihe abgearbeitet, baut der Plan im Kreis weiter, solange Felder und Siedler reichen.
WEITER = ("holzfaeller", "steinmetz", "farm", "goldmine")


def lade(wurzel, *teile):
    """Liest eine Datendatei als dict; fehlt sie, bricht das Werkzeug ab (keine stillen Nullen)."""
    pfad = os.path.join(wurzel, *teile)
    with io.open(pfad, encoding="utf-8") as f:
        return json.load(f)


def hash_von(wurzel, *teile):
    """SHA256 einer Eingabedatei - so steht im Kopf, WORAUS die Kurve gerechnet wurde."""
    with open(os.path.join(wurzel, *teile), "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def gelande_der_startkarte(wurzel):
    """Die Gelaendefelder der belegten Startkarte (Register 228) als {Ertragsschluessel: Anzahl}."""
    katalog = lade(wurzel, "data", "originalkarten", "katalog.json")
    start = lade(wurzel, "data", "startkarte.json").get("standard_karte")
    eintrag = None
    for k in katalog.get("karten") or []:
        if str(k.get("id")) == str(start):
            eintrag = k
            break
    if eintrag is None:
        raise SystemExit("Startkarte %s steht nicht im Katalog" % start)
    roh = (eintrag.get("original_attribute") or {}).get("felder") or {}
    felder = {}
    for name, anzahl in roh.items():
        schluessel = GELAENDE_MAP.get(str(name).lower())
        if schluessel:
            felder[schluessel] = int(anzahl)
    return str(start), felder


def ertrag(rohstoffe, rohstoff, gelaende):
    """Ertrag je Stunde eines Rohstoffs auf einem Gelaende (0, wenn er dort nichts bringt)."""
    for eintrag in rohstoffe:
        if str(eintrag.get("id")) == rohstoff:
            return float((eintrag.get("ertrag_pro_stunde") or {}).get(gelaende, 0) or 0)
    return 0.0


def _normal(name):
    """Ein Gebaeudename ohne Umlaute und in Kleinschreibung - fuer Vergleiche ueber Datengrenzen.

    Die Datendateien schreiben "Holzfäller" und "Jäger", der Plan arbeitet mit "holzfaeller".
    Ohne diese Umschrift findet der Plan den Ertrag nicht und rechnet still mit 0 (gemessen
    07.11.2026: Holz wuchs einen ganzen Spieltag nicht).
    """
    text = str(name or "").lower()
    for alt, ersatz in (("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("ß", "ss")):
        text = text.replace(alt, ersatz)
    return text


def rohstoff_je_gebaeude(rohstoffe, gebaeude):
    """Welcher Rohstoff gehoert zu einem Gebaeude (leer, wenn es keinen erzeugt, z. B. Haus)."""
    gesucht = _normal(gebaeude)
    for eintrag in rohstoffe:
        namen = [_normal(n) for n in (eintrag.get("erzeugendes_gebaeude") or [])]
        if any(gesucht in n for n in namen):
            return str(eintrag.get("id"))
    return ""


def preis(preise, gebaeude):
    """Die Kosten eines Gebaeudes als dict; fehlt der Eintrag, ist es nicht baubar."""
    eintrag = preise.get(gebaeude)
    if not isinstance(eintrag, dict):
        return None
    return {k: v for k, v in eintrag.items() if not str(k).startswith("_") and k != "budget"}


def sollkurve(wurzel=HIER, tage=20):
    """Rechnet den Idealplan und den Korridor. Reine Rechnung - schreibt nichts."""
    res = lade(wurzel, "data", "resources.json")
    rohstoffe = res.get("rohstoffe") or []
    preise = lade(wurzel, "data", "baupreise.json").get("preise") or {}
    startwerte = res.get("startwerte") or {}
    karte, felder = gelande_der_startkarte(wurzel)
    frei = dict(felder)  # noch freie Felder je Gelaende
    bestand = {"holz": float(startwerte.get("holz", 0)), "stein": float(startwerte.get("steine", 0)),
               "nahrung": 0.0, "gold": 0.0}
    siedler = int(startwerte.get("siedler", 0))
    haeuser = 0
    gebaut = []
    forschung = {}
    reihe = list(REIHENFOLGE)
    zeilen = []
    luecken = []
    for tag in range(0, tage + 1):
        if tag > 0:  # an einem Tag ernten ALLE stehenden Gebaeude 24 Stunden
            for eintrag in gebaut:
                name = eintrag["gebaeude"]
                stoff = rohstoff_je_gebaeude(rohstoffe, name)
                if stoff and stoff in bestand:
                    bestand[stoff] += ertrag(rohstoffe, stoff, eintrag["gelaende"]) * STUNDEN_JE_TAG
            # Bauen: das naechste Stueck der Reihe, wenn bezahlbar und ein Feld frei ist
            while reihe:
                name = reihe[0]
                kosten = preis(preise, name)
                if kosten is None:
                    luecken.append("Preis fuer %s fehlt in data/baupreise.json" % name)
                    reihe.pop(0)
                    continue
                if name in ("goldmine", "farm") and "Baukunst" not in forschung:
                    # Baukunst braucht Bibliothek 1; die FORSCHUNGSKOSTEN stehen nicht in den Daten.
                    if any(g["gebaeude"] == "bibliothek" for g in gebaut):
                        forschung["Baukunst"] = 1
                        luecken.append("Forschungskosten fehlen in data/research.json - Baukunst gilt "
                                       "ab dem Tag nach der Bibliothek als erforscht (Annahme)")
                    else:
                        break
                braucht = int(kosten.get("siedler", 0) or 0)
                if name != "haus" and siedler - braucht < 0:  # keine Siedler mehr frei
                    kosten_haus = preis(preise, "haus")  # dann erst ein Haus (es BEHERBERGT Siedler)
                    if kosten_haus is None:  # ohne Preis kein Haus
                        break  # dann steht der Plan
                    name, kosten = "haus", kosten_haus  # dieses Stueck wird ein Haus
                bezahlbar = (bestand["holz"] >= float(kosten.get("holz", 0) or 0)
                             and bestand["stein"] >= float(kosten.get("stein", 0) or 0))
                if not bezahlbar:  # nicht bezahlbar
                    break  # dann wartet der Plan auf den naechsten Tag
                feld = None
                for gelaende in BAU_GELAENDE.get(name, ()):
                    if frei.get(gelaende, 0) > 0:
                        feld = gelaende
                        break
                if feld is None:
                    luecken.append("kein freies Gelaende fuer %s am Tag %d" % (name, tag))
                    reihe.pop(0)
                    continue
                frei[feld] -= 1
                bestand["holz"] -= float(kosten.get("holz", 0) or 0)
                bestand["stein"] -= float(kosten.get("stein", 0) or 0)
                if name == "haus":
                    haeuser += 1
                    siedler += 5
                else:
                    siedler -= braucht
                gebaut.append({"gebaeude": name, "gelaende": feld, "tag": tag})
                reihe.pop(0)
                if not reihe and sum(frei.values()) > 0:  # Reihe abgearbeitet, Felder frei
                    reihe.extend(WEITER)  # dann im Kreis weiterbauen
        zeile = {"tag": tag, "siedler": siedler, "gebaeude": len(gebaut)}
        for stoff in ("holz", "stein", "nahrung", "gold"):
            wert = round(bestand[stoff], 2)
            zeile[stoff] = {"ideal": wert, "unten": round(wert * BAND_UNTEN, 2),
                            "oben": round(wert * BAND_OBEN, 2)}
        zeilen.append(zeile)
    return {
        "stand": "2026-11-07",
        "zweck": ("B-1 Sollkurve: Zielkorridor je Spieltag aus dem Idealplan der belegten Kette "
                  "(Ablauf Schritt 8). Erzeugt von tools/balance_kreis.py --sollkurve - nicht von Hand "
                  "aendern, neu rechnen."),
        "erzeugt_aus": {
            "data/resources.json": hash_von(wurzel, "data", "resources.json"),
            "data/baupreise.json": hash_von(wurzel, "data", "baupreise.json"),
            "data/research.json": hash_von(wurzel, "data", "research.json"),
            "data/units.json": hash_von(wurzel, "data", "units.json"),
            "data/startkarte.json": hash_von(wurzel, "data", "startkarte.json"),
            "data/originalkarten/katalog.json": hash_von(wurzel, "data", "originalkarten", "katalog.json"),
        },
        "startkarte": karte,
        "baender": {"unten": BAND_UNTEN, "oben": BAND_OBEN,
                    "quelle": "VORSCHLAG (Ablauf Schritt 8): untere Grenze Ideal x 0,7, obere x 1,1."},
        "punkte_ziel_je_spieltag": {"wert": PUNKTE_ZIEL,
                                    "quelle": "V-3 (docs/S0_TABELLEN_20261107.md): Punkte-Ziel je Spieltag."},
        "annahmen": [
            "Ein Spieltag sind 24 Spielstunden; die Ertraege aus data/resources.json gelten je Stunde.",
            "Der Plan baut zuerst %s, danach im Kreis %s - jeweils auf dem besten freien Gelaende "
            "der Startkarte; ein Haus entsteht nur, wenn die Siedler ausgehen."
            % (", ".join(REIHENFOLGE), ", ".join(WEITER)),
            "Kein Kampf, keine Beute, keine Karren, keine Einheiten: der Plan misst den AUFBAU.",
            "Forschungskosten stehen NICHT in data/research.json - Baukunst gilt als erforscht, sobald "
            "die Bibliothek steht (Luecke, keine erfundene Zahl).",
        ],
        "luecken": sorted(set(luecken)),
        "tage": zeilen,
    }


def main():
    """Aufruf von der Kommandozeile: rechnen, drucken und mit --schreiben ablegen."""
    zerleger = argparse.ArgumentParser(description="B-1 Sollkurve aus den Daten")
    zerleger.add_argument("--sollkurve", action="store_true", help="die Sollkurve rechnen")
    zerleger.add_argument("--wurzel", default=HIER, help="Projektordner (fuer Pruefungen)")
    zerleger.add_argument("--tage", type=int, default=20, help="Anzahl der Spieltage")
    zerleger.add_argument("--schreiben", action="store_true", help="data/sollkurve.json schreiben")
    args = zerleger.parse_args()
    if not args.sollkurve:
        print("Aufruf: --sollkurve [--tage N] [--schreiben] [--wurzel PFAD]")
        return 0
    kurve = sollkurve(args.wurzel, args.tage)
    if args.schreiben:
        ziel = os.path.join(args.wurzel, "data", "sollkurve.json")
        with io.open(ziel, "w", encoding="utf-8", newline="\n") as f:
            json.dump(kurve, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print("geschrieben:", ziel)
    print("Startkarte:", kurve["startkarte"], "| Tage:", len(kurve["tage"]))
    for zeile in kurve["tage"][:6]:
        print("Tag %2d  Holz %8.1f  Stein %8.1f  Nahrung %8.1f  Gold %7.1f  Siedler %3d  Gebaeude %2d"
              % (zeile["tag"], zeile["holz"]["ideal"], zeile["stein"]["ideal"],
                 zeile["nahrung"]["ideal"], zeile["gold"]["ideal"], zeile["siedler"],
                 zeile["gebaeude"]))
    if kurve["luecken"]:
        print("Luecken:", len(kurve["luecken"]))
        for luecke in kurve["luecken"][:5]:
            print("   -", luecke)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
