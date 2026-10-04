"""
Berater — die Auskunft im Spiel (Reiter "Chat").

Arbeitet OHNE Netz und OHNE Schluessel: alle Antworten kommen aus den Spiel- und
Originaldaten (data/*.json) sowie aus fest hinterlegten Handbuchregeln. Damit ist die
Auskunft kostenlos, offline und nachpruefbar.

Wo das Original schweigt (Baupreise, Ausbildungsdauern), sagt der Berater das ausdruecklich
und nennt die Zahl als Vorschlag.

Ein echtes Sprachmodell ist NICHT angebunden. Die Stelle dafuer ist `ANTWORT_QUELLE_LLM` unten
beschrieben — bewusst leer gelassen, damit keine Schluessel in der ausgelieferten Datei landen.
"""
from __future__ import annotations

import json
import os

import gelaende
import spieldaten

WURZEL = spieldaten.projektwurzel()      # auch in der fertigen EXE richtig (eine Stelle: spieldaten)

# Ein echtes Modell koennte hier angebunden werden (Schluessel NICHT in der Datei ablegen,
# sondern in einer Konfiguration ausserhalb). Bleibt vorerst leer: die Auskunft unten
# beantwortet alles aus den Spieldaten.
ANTWORT_QUELLE_LLM = None


def _norm(text: str) -> str:
    import unicodedata
    text = unicodedata.normalize("NFC", str(text)).lower()
    return (text.replace("ä", "ae").replace("ö", "oe")
            .replace("ü", "ue").replace("ß", "ss"))


def _datei(name: str) -> dict:
    with open(os.path.join(WURZEL, "data", name), encoding="utf-8") as f:
        return json.load(f)


def _baupreise() -> dict:
    try:
        return _datei("baupreise.json")["preise"]
    except (OSError, KeyError, ValueError):
        return {}


# --------------------------------------------------------------------------
# Nachschlagen in den Daten
# --------------------------------------------------------------------------
# Die Suche laeuft in `antwort()` ueber ALLE Quellen gleichzeitig (Gebaeude, Einheiten, Waren),
# damit der laengste Name gewinnt. Eine Suche je Bereich nacheinander waere falsch:
# 'Lager' (Gebaeude) steckt in 'Belagerungsturm' (Einheit), 'Farm' in 'Rinderfarm',
# 'Bogen' in 'Langbogen'.


# --------------------------------------------------------------------------
# Bausteine fuer Antworten
# --------------------------------------------------------------------------

def _gebaeude_text(kennung: str, geb: dict) -> list:
    zeilen = [f"{geb['name']} ({geb.get('kategorie', 'ohne Kategorie')})"]
    if geb.get("wirkung"):
        zeilen.append(f"  Wirkung: {geb['wirkung']}")
    if geb.get("voraussetzung"):
        zeilen.append(f"  Voraussetzung: {geb['voraussetzung']}")
    ertraege = geb.get("ertrag_pro_stunde")
    if ertraege:
        teile = []
        for art, wert in ertraege.items():
            if isinstance(wert, dict):
                teile.append(f"{art}: " + ", ".join(f"{w} {z}/h" for w, z in wert.items()))
            else:
                teile.append(f"{art}: {wert}/h")
        zeilen.append("  Ertrag je Gelände (Handbuch S. 10): " + " | ".join(teile))
    elif geb.get("ertrag_pro_stunde") is None and not ertraege:
        zeilen.append("  Kein Geländebezug — steht auf jedem bebaubaren Gelände.")
    if geb.get("abweichung"):
        zeilen.append(f"  Achtung, zwei Fassungen: {geb['abweichung']}")
    preis = _baupreise().get(kennung)
    if preis:
        zahlen = {r: v for r, v in preis.items() if isinstance(v, (int, float))}
        if zahlen:
            kosten = ", ".join(
                f"{int(v) if float(v).is_integer() else v} {r.capitalize()}"
                for r, v in zahlen.items())
            herkunft = ("belegt — aus dem Original-Baumenü" if preis.get("_belegt")
                        else "VORSCHLAG — für dieses Gebäude nennt keine Quelle einen Preis")
            zeilen.append(f"  Baupreis: {kosten}  ({herkunft})")
    return zeilen


def _einheit_text(name: str, e: dict) -> list:
    werte_daten = e.get("werte") or {}
    werte = []
    for feld, beschriftung in [("LE", "Lebensenergie"), ("AT", "Attacke"), ("PA", "Parade"),
                               ("RS", "Rüstungsschutz"), ("TP_min", "Treffer min"),
                               ("TP_max", "Treffer max"), ("MU", "Mut"), ("GS", "Geschwindigkeit"),
                               ("SK", "Stärkeklasse")]:
        wert = werte_daten.get(feld)
        if wert is not None:
            werte.append(f"{beschriftung} {wert}")
    zeilen = [f"{name} ({e.get('kategorie', '')})"]
    if werte:
        zeilen.append("  Werte: " + ", ".join(werte))
    if e.get("kosten"):
        zeilen.append("  Kosten: " + ", ".join(f"{v} {k.capitalize()}" for k, v in e["kosten"].items()))
    if e.get("waren"):
        zeilen.append("  Benötigte Waren: " + ", ".join(str(w) for w in e["waren"]))
    if e.get("voraussetzung"):
        zeilen.append(f"  Voraussetzung: {e['voraussetzung']}")
    if e.get("kriegspunkte") is not None:
        zeilen.append(f"  Kriegspunkte: {e['kriegspunkte']}")
    if e.get("gebaeude"):
        zeilen.append(f"  Ausgebildet in: {e['gebaeude']}")
    fehlend = e.get("nicht_original") or []
    if fehlend:
        zeilen.append("  Im Handbuch nicht angegeben: " + ", ".join(str(x) for x in fehlend))
    return zeilen


def _ware_text(name: str, w: dict) -> list:
    zeilen = [f"{name}"]
    if w.get("werkstatt"):
        zeilen.append(f"  Hergestellt in: {w['werkstatt']}")
    if w.get("voraussetzung"):
        zeilen.append(f"  Voraussetzung: {w['voraussetzung']}")
    if w.get("benoetigt_von"):
        zeilen.append("  Verlangt von: " + ", ".join(str(x) for x in w["benoetigt_von"]))
    if w.get("anmerkung"):
        zeilen.append(f"  Anmerkung: {w['anmerkung']}")
    return zeilen


# --------------------------------------------------------------------------
# Themen ohne Sachbegriff
# --------------------------------------------------------------------------

def _antwort_gelaende() -> list:
    zeilen = ["Es gibt sieben Geländearten (Handbuch S. 9-11):"]
    for art in gelaende.GELAENDEARTEN:
        zeilen.append(f"  {gelaende.name(art)} — {'bebaubar' if gelaende.ist_bebaubar(art) else 'NICHT bebaubar'}")
    zeilen.append("Sümpfe können nicht bebaut werden (Handbuch S. 11).")
    zeilen.append("Bestes je Gelände: Holzfäller auf Wald 4 Holz/h, Steinmetz auf Berg 4 Stein/h, "
                  "Farm auf Grasland 4 Nahrung/h, Mine auf Berg 3 Erz/h, "
                  "Tempel am Nebelsee 5 Mana/h (sonst nur 1).")
    zeilen.append("Fünf Kartentypen: waldreich, steinreich, Weideland, Nebelseeufer, ausgeglichen — "
                  "jede Siedlung bekommt eine zufällige, niemals zweimal dieselbe eigene.")
    return zeilen


def _antwort_forschung() -> list:
    regeln = spieldaten.forschungsregeln()
    zeilen = ["Forschung (Handbuch S. 12/13):",
              f"  Kosten: {regeln.get('kosten', '50 Holz, je Stufe verdoppelt')}",
              "  Dauer: Stufe × Stufe Stunden (Stufe 3 = 9 Stunden, Stufe 5 = 25 Stunden).",
              "  Voraussetzung: eine Bibliothek.",
              "  Punkte: Stufe hoch drei (Stufe 2 = 8 Punkte).",
              "Reihenfolge: Baukunst öffnet die meisten Gebäude; Verteidigungsanlagen den Ausbau des Walls."]
    zeilen.append("Hinweis: die Originalzeiten sind als Einzelspieler sehr lang (Stufe 10 = 100 Stunden) — "
                  "ein Zeitfaktor ist in Planung, aber noch nicht entschieden.")
    return zeilen


def _antwort_kampf() -> list:
    return ["Kampf (Handbuch S. 20-22):",
            "  Zuerst die Fernkämpfer beider Seiten gleichzeitig, dann der Nahkampf.",
            "  Der Verteidigungswall muss vorher überwunden werden — jede Stufe hat einen "
            "Schwellenwert für Fußtruppen und einen für Belagerungswaffen.",
            "  Mauerschaden = Waffenwert − Ausbaustufe.",
            "  Höchstens zehn Kampfsequenzen.",
            "  Nahkämpfer schlagen einen zufälligen Gegner; dabei zählen Attacke/Parade/Rüstungsschutz/Treffer.",
            "  Im Nahkampf sinken Attacke und Parade beider Seiten mit jeder Sequenz.",
            "  Wer unter 5 Lebensenergie fällt, muss einen Mut-Wurf machen — gelingt er, flieht er "
            "(Geflohene gelten nicht als Verlust).",
            "  Beute gibt es nur, wenn Transportkarren mitgezogen wurden."]


def _antwort_punkte() -> list:
    return ["Punkte (Handbuch S. 23):",
            "  Forschungspunkte: für jede Stufe wird die Stufe dreimal multipliziert — also Stufe hoch drei.",
            "  Kriegspunkte: für Verteidigungsanlagen die Ausbaustufe hoch drei, dazu Punkte für Einheitenverluste.",
            "  Gesamtpunkte: die halbe Summe aus Forschungs- und Kriegspunkten.",
            "  Der Ruf steigt durch Kämpfe und Handel."]


def _antwort_portal() -> list:
    return ["Limbus und Portale (Handbuch S. 1/4/12):",
            "  Alle Welten liegen im Limbus, der sich in 20 Dimensionen teilt.",
            "  Verbunden sind sie über magische Portale.",
            "  Im Portalbereich siehst du die Position deiner Welt und die der anderen.",
            "  Je weiter eine Welt entfernt liegt, desto mehr Mana kostet das Öffnen des Portals.",
            "  Die sechs alten Welten hießen: Armageddon, Ragnarök, Utgard, Midgard, Valhalla, Limbus."]


def _antwort_start() -> list:
    return ["Der Start (Handbuch S. 7):",
            "  Du beginnst mit 100 Holz, 100 Stein und 10 Siedlern.",
            "  1. Im Dorfzentrum eine Siedlung gründen — sie bekommt eine eigene Geländekarte.",
            "  2. Karte öffnen und auf Wald einen Holzfäller bauen, auf Berg einen Steinmetz, "
            "auf Grasland eine Farm.",
            "  3. Ein Haus erhöht die Siedlerzahl, eine Bibliothek schaltet die Forschung frei.",
            "  Sümpfe sind nicht bebaubar — dort geht nichts."]


def _antwort_steuerung() -> list:
    return ["Bedienung:",
            "  Links das Menü, oben die Rohstoffleiste.",
            "  Im Dorfzentrum stehen deine Siedlungen und der Weg zu ihrer Karte.",
            "  Auf der Siedlungskarte ein Feld anklicken: du siehst die Eignung und die Gebäude, "
            "die dort gebaut werden können — mit Preis.",
            "  Ein belegtes Feld kann abgerissen werden; die Baustoffe kommen nicht zurück.",
            "  Speichern über die Einstellungen."]


def _antwort_sieg() -> list:
    return ["Ziel:",
            "  Die Rangliste führt nach Gesamtpunkten; der Götterschutz gilt sieben Tage.",
            "  Ein eindeutiges Sieg- oder Niederlage-Ereignis nennt das Handbuch nicht — "
            "das ist ein offener Punkt für unser Remake."]


THEMEN = [
    (("sumpf",), lambda: ["Sumpf: nicht bebaubar (Handbuch S. 11). "
                          "Kein Gebäude liefert dort etwas — das Feld bleibt leer.",
                          "Auf allen anderen sechs Geländearten kannst du bauen."]),
    (("gelände", "gelaende", "terrain", "untergrund", "karte", "karten"), _antwort_gelaende),
    (("forschung", "forschen", "technologie"), _antwort_forschung),
    (("kampf", "angriff", "schlacht", "wall", "belagerung"), _antwort_kampf),
    (("punkte", "rangliste", "score"), _antwort_punkte),
    (("portal", "limbus", "welt", "welten", "dimension", "mana"), _antwort_portal),
    (("anfang", "start", "beginn", "erste schritte", "einstieg", "anfangen", "fange",
      "loslegen", "wie geht es los", "neu anfangen"), _antwort_start),
    (("steuerung", "bedienung", "wie geht", "hilfe", "anleitung"), _antwort_steuerung),
    (("sieg", "gewinn", "ziel", "niederlage"), _antwort_sieg),
    (("rohstoff", "ressource", "rohstoffe"), lambda: [
        "Die neun Rohstoffe (Handbuch S. 9-10): " + ", ".join(
            r["name"] for r in spieldaten.rohstoffe()),
        "Holz und Stein sind der Einstieg, Nahrung hält die Siedler, Mana braucht die Forschung, "
        "Gold die Ausbildung, Wolle/Leder/Pferde die Ausrüstung."]),
    (("ware", "waren", "handwerk", "produkt"), lambda: [
        "Es gibt 17 Waren; hergestellt werden sie in Schmiede, Bogenbauer und Nähstube.",
        "Beispiele: " + ", ".join(list(spieldaten.waren())[:8]) + " …"]),
    (("haus", "siedler", "bevölkerung", "bevoelkerung"), lambda: [
        "Haus: erhöht die Siedlerkapazität (Handbuch S. 10).",
        "Start 10 Siedler; das Handbuch nennt 1 neuen Siedler je Stunde."]),
]


# --------------------------------------------------------------------------
# Oeffentliche Schnittstelle
# --------------------------------------------------------------------------

def antwort(frage: str, zustand=None) -> str:
    """
    Beantwortet eine Frage aus den Spieldaten.

    `zustand` ist optional der Spielzustand (GameState) — dann kommen die Tipps von unten dazu.
    """
    frage = (frage or "").strip()
    if not frage:
        return begruessung()

    if ANTWORT_QUELLE_LLM is not None:                 # vorbereitet, aber nicht eingerichtet
        try:
            return ANTWORT_QUELLE_LLM(frage, zustand)
        except Exception:
            pass                                            # faellt auf die Auskunft zurueck

    # Nachschlagen: der LAENGSTE Treffer aus ALLEN Quellen gewinnt.
    # Grund: Namen stecken ineinander und ueber die Bereiche hinweg — 'Lager' (Gebaeude)
    # steckt in 'Belagerungsturm' (Einheit), 'Farm' in 'Rinderfarm', 'Bogen' in 'Langbogen'.
    # Wer Bereich fuer Bereich prueft, erklaert die falsche Sache.
    n = _norm(frage)
    kandidaten = []
    for kennung, geb in gelaende.alle_gebaeude().items():
        kandidaten.append(("gebaeude", geb["name"], (kennung, geb)))
        kandidaten.append(("gebaeude", kennung, (kennung, geb)))
    for name, eintrag in spieldaten.einheiten().items():
        kandidaten.append(("einheit", name, (name, eintrag)))
    for name, eintrag in spieldaten.waren().items():
        kandidaten.append(("ware", name, (name, eintrag)))

    treffer = [k for k in kandidaten if _norm(k[1]) in n]
    if treffer:
        art, _, daten = max(treffer, key=lambda k: len(_norm(k[1])))
        if art == "gebaeude":
            return "\n".join(_gebaeude_text(daten[0], daten[1]))
        if art == "einheit":
            return "\n".join(_einheit_text(daten[0], daten[1]))
        return "\n".join(_ware_text(daten[0], daten[1]))

    # Thema?
    for schluesselwoerter, bauer in THEMEN:
        if any(w in n for w in schluesselwoerter):
            return "\n".join(bauer())

    # 5. Tipps zum Spielstand
    if any(w in n for w in ("tipp", "was soll", "rat", "weiter", "hilfe mir", "stecke")):
        return tipps(zustand)

    return ("Das weiß ich nicht — ich antworte aus dem Handbuch und den Spieldaten.\n"
            "Frag mich zum Beispiel:\n"
            "  • Was macht der Holzfäller?\n"
            "  • Welches Gelände braucht der Steinmetz?\n"
            "  • Was kostet die Forschung?\n"
            "  • Wie läuft ein Kampf ab?\n"
            "  • Wie fange ich an?\n"
            "  • Gib mir einen Tipp")


def tipps(zustand=None) -> str:
    """Tipps zum aktuellen Spielstand — rechnet aus, was fehlt."""
    if zustand is None:
        return ("Tipp: In einer Siedlung zählt, was auf dem Gelände steht. "
                "Ein Holzfäller gehört auf Wald, ein Steinmetz auf Berg oder Hügel, "
                "eine Farm auf Grasland. Sümpfe bleiben leer.")

    zeilen = []
    for s in getattr(zustand, "settlements", []):
        if not getattr(s, "karte", None):
            zeilen.append(f"{s.name}: hat noch keine Karte — im Kartenfenster zuweisen.")
            continue
        arten = {}
        for feld, gebaut in s.bauten.items():
            art = s.karte["raster"][int(feld)]
            arten.setdefault(art, []).append(gebaut)

        if "wald" in s.karte["raster"] and "wald" not in arten:
            zeilen.append(f"{s.name}: auf den Waldfeldern steht noch kein Holzfäller "
                          f"(4 Holz/Stunde je Feld).")
        if ("berg" in s.karte["raster"] or "huegel" in s.karte["raster"]) and \
                not ({"berg", "huegel"} & set(arten)):
            zeilen.append(f"{s.name}: Berg und Hügel sind frei — dort fehlt ein Steinmetz "
                          f"(4 bzw. 2 Stein/Stunde).")
        if "grasland" in s.karte["raster"] and "grasland" not in arten:
            zeilen.append(f"{s.name}: auf Grasland fehlt eine Farm (4 Nahrung/Stunde).")
        if "nebelsee" in s.karte["raster"] and "nebelsee" not in arten:
            zeilen.append(f"{s.name}: am Nebelsee fehlt ein Tempel (5 Mana/Stunde statt 1).")
        suempfe = s.karte["zaehlung"].get("sumpf", 0)
        if suempfe:
            zeilen.append(f"{s.name}: {suempfe} Sumpffelder bleiben leer — das ist normal.")
    if not zeilen:
        zeilen.append("Alles Wichtige steht: jede Siedlung hat auf ihren besten Feldern ein Gebäude. "
                      "Als Nächstes lohnt eine Bibliothek (Forschung) und ein Haus (mehr Siedler).")
    return "\n".join(zeilen)


def begruessung() -> str:
    return ("Ich bin die Auskunft im Spiel. Ich antworte aus dem Originalhandbuch und den "
            "Spieldaten — ohne Netz und ohne Schlüssel.\n"
            "Frag mich zum Beispiel:\n"
            "  • Was macht der Holzfäller?\n"
            "  • Welche Einheit ist stärker, Paladin oder Ritter?\n"
            "  • Was brauche ich für eine Bibliothek?\n"
            "  • Wie läuft ein Kampf ab?\n"
            "  • Gib mir einen Tipp")
