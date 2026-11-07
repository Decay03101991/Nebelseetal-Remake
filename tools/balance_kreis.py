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
import shutil
import subprocess
import sys
import tempfile

HIER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Projektordner
STUNDEN_JE_TAG = 24  # ein Spieltag = 24 Spielstunden (Produktionsangaben sind je Stunde)
BAND_UNTEN = 0.7  # VORSCHLAG: unterer Rand des Korridors
BAND_OBEN = 1.1  # VORSCHLAG: oberer Rand des Korridors
PUNKTE_ZIEL = 3.3  # V-3 (docs/S0_TABELLEN_20261107.md): Punkte je Spieltag
REGELKREIS = ("data", "regelkreis.json")  # B-2: Schwellen und Messumfang (F-17)
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


# ============================================================================
# B-2 REGELKREIS (Ablauf Schritt 9, 07.11.2026, Sitzung 14)
#
# Vier Schritte, in dieser Reihenfolge, jeder einzeln aufrufbar:
#   messung    zehn Laeufe mit den Startwerten 1..10 (derselbe Startwert = dieselbe Partie)
#   vorschlag  HOECHSTENS EIN Datenwert je Runde, Schrittweite aus data/regelkreis.json,
#              BELEGT-Werte werden nie vorgeschlagen
#   ab         dieselben Startwerte mit und OHNE Aenderung; die Aenderung lebt nur in einer
#              tempoeraeren Kopie von src/ + data/ - data/ des Projekts wird nie geschrieben
#   urteil     Zielabweichung mindestens 20 Prozent besser, keine andere Groesse schlechter,
#              erstes Gefecht nicht spaeter (Schwellen aus data/regelkreis.json, F-17)
#
# Dazu der Feedback-Eingang: docs/feedback/VORLAGE.md (was Daniel meldet) fuehrt ueber
# docs/feedback/MELDUNGEN.json in docs/feedback/BUENDEL.md; ab drei gleichen Schluesseln wird
# daraus ein Messauftrag - ein Tester-Buendel sticht eine reine Kennzahl (Risiko in Schritt 9).
# ============================================================================
MESSMARKE = "@@MESSUNG@@"  # so beginnt die eine Zeile, die der Messlauf zurueckgibt
LAUFER = '''# -*- coding: utf-8 -*-
"""Messlauf in einem EIGENEN Prozess: Startwerte, Tage und Stil kommen als Argumente.

Warum ein eigener Prozess: `spieldaten` bindet die Projektwurzel beim Import, und `gelaende`,
`gebaeude_wirkung` und `berater` halten sie als Modulkonstante. Ein Umbiegen im laufenden
Prozess waere eine halbe Sache; ein eigener Prozess mit eigener Wurzel ist die ehrliche Kopie.
Das Skript schreibt NICHTS - es druckt eine Zeile JSON.
"""
import json
import sys

wurzel = sys.argv[1].rstrip("/\\\\")              # Projektwurzel, aus der gespielt wird
saaten = [int(x) for x in sys.argv[2].split(",") if x.strip()]   # Startwerte in Reihenfolge
tage = float(sys.argv[3])                        # Laenge einer Partie in Spieltagen
stil = sys.argv[4]                               # Spielerpolitik des Spieltests

sys.path.insert(0, wurzel + "/tools")            # das Spieltest-Werkzeug der Wurzel
sys.path.insert(0, wurzel + "/src")              # und ihre Fachschicht
import spieltest_simulation as SIM               # noqa: E402 - Pfad steht erst jetzt

laeufe = []                                      # eine Zeile je Partie
for saat in saaten:                              # jede Saat ist eine eigene Partie
    log = SIM.spielen(tage, saat, stil)          # ohne Fenster, ohne Dateizugriff
    schritte = log.get("schritte") or []         # Tagesstaende des Laufs
    laeufe.append({
        "saat": saat,                            # der Startwert, unter dem der Lauf steht
        "tage": [{"tag": s.get("tag"),          # Spieltag des Stands
                  "ressourcen": s.get("ressourcen") or {},   # Rohstoffe an diesem Tag
                  "punkte": s.get("punkte")}    # Gesamtpunkte an diesem Tag
                 for s in schritte],
        "tag_erstes_gefecht": (log.get("meilensteine") or {}).get("tag_erstes_gefecht"),
        "punkte_ende": ((log.get("ende") or {}).get("punkte") or {}).get("gesamtpunkte"),
        "uebersprungen": len(log.get("uebersprungen") or []),
    })
print("@@MESSUNG@@" + json.dumps({"laeufe": laeufe, "tage": tage, "stil": stil},
                                 ensure_ascii=False))
'''


def lade_regelkreis(wurzel=HIER):
    """Schwellen und Messumfang aus `data/regelkreis.json`.

    Die drei Zahlen (20 Prozent Verbesserung, 10 Prozent Schrittweite, 3 Meldungen) sind
    Daniels Antwort F-17 und stehen deshalb in der Datendatei, nicht im Code. Fehlt eine
    Schwelle, bricht das Werkzeug ab - ein stiller Standard waere eine zweite Wahrheit.
    """
    pfad = os.path.join(wurzel, *REGELKREIS)                       # data/regelkreis.json
    if not os.path.isfile(pfad):                                   # ohne Datei keine Schwellen
        raise SystemExit("data/regelkreis.json fehlt - der Regelkreis rechnet nicht ohne Schwellen")
    with io.open(pfad, encoding="utf-8") as f:                      # Datei lesen
        daten = json.load(f)                                       # Schwellen + Messumfang
    schwellen = daten.get("schwellen") or {}                       # die drei vereinbarten Zahlen
    for name in ("verbesserung_prozent", "schrittweite_prozent", "meldungen_je_buendel"):
        if schwellen.get(name) is None:                            # jede Zahl muss dastehen
            raise SystemExit("data/regelkreis.json: Schwelle %s fehlt" % name)
    return daten                                                   # fertig gelesen


def messumfang(wurzel=HIER, regelkreis=None, saaten=None, tage=None, stil=None):
    """Die vier Messangaben: Startwerte, Tage, Stil - Argument schlaegt Datendatei."""
    regelkreis = regelkreis if regelkreis is not None else lade_regelkreis(wurzel)
    angaben = regelkreis.get("messung") or {}                       # Messumfang aus der Datei
    saaten = [int(s) for s in (saaten if saaten is not None else angaben.get("saaten") or [])]
    tage = float(tage if tage is not None else angaben.get("tage") or 12)
    stil = str(stil if stil is not None else angaben.get("stil") or "breit")
    if not saaten:                                                  # ohne Startwerte kein Lauf
        raise SystemExit("data/regelkreis.json: messung.saaten ist leer")
    return saaten, tage, stil                                       # Reihenfolge bleibt erhalten


def messung(wurzel=HIER, regelkreis=None, saaten=None, tage=None, stil=None):
    """Zehn Laeufe mit den Startwerten 1..10 - und dieselbe Zahl Laeufe ergibt dieselbe Liste.

    Der Lauf startet in einem eigenen Prozess in der angegebenen Wurzel; das Werkzeug schreibt
    nichts in das Projekt (kein Log, kein Spielstand). Rueckgabe: Laeufe mit Tagesstaenden,
    Punkten und dem Tag des ersten Gefechts.
    """
    saaten, tage, stil = messumfang(wurzel, regelkreis, saaten, tage, stil)
    ordner = tempfile.mkdtemp(prefix="regelkreis_messung_")         # Laufscript in den Scratch
    try:
        script = os.path.join(ordner, "messlauf.py")                # das Script des Messlaufs
        with io.open(script, "w", encoding="utf-8", newline="\n") as f:
            f.write(LAUFER)                                         # Inhalt von oben
        befehl = [sys.executable, "-X", "utf8", script, wurzel.replace(os.sep, "/"),
                  ",".join(str(s) for s in saaten), str(tage), stil]
        lauf = subprocess.run(befehl, cwd=wurzel, capture_output=True, text=True,
                              encoding="utf-8", errors="replace", timeout=1800)  # grosszuegig
    finally:
        shutil.rmtree(ordner, ignore_errors=True)                   # Scratch immer aufraeumen
    zeile = ""                                                      # die Zeile mit der Antwort
    for kandidat in (lauf.stdout or "").splitlines():
        if kandidat.startswith(MESSMARKE):                          # nur die markierte Zeile zaehlt
            zeile = kandidat[len(MESSMARKE):]                       # ohne Marke weiterreichen
    if not zeile:                                                   # kein Ergebnis = Fehler, kein 0-Wert
        raise SystemExit("Messlauf ohne Ergebnis (RC %s):\n%s" % (lauf.returncode,
                                                                  (lauf.stderr or "")[-600:]))
    ergebnis = json.loads(zeile)                                    # gepruefte Antwort
    ergebnis.update({"saaten": saaten, "tage": tage, "stil": stil, "wurzel": wurzel})
    return ergebnis                                                 # fertig gemessen


def mittel_je_tag(mess, groesse):
    """Mittelwert einer Groesse je Spieltag ueber alle Laeufe: {Tag: Mittelwert}."""
    summen, zaehler = {}, {}                                        # Summe und Anzahl je Tag
    for lauf in mess.get("laeufe") or []:                           # jede Partie zaehlt gleich
        for tag in lauf.get("tage") or []:                          # jeder Tagesstand der Partie
            wert = (tag.get("ressourcen") or {}).get(groesse)       # Rohstoff an diesem Tag
            if not isinstance(wert, (int, float)) or isinstance(wert, bool):
                continue                                            # nicht gemessen = nicht mitzaehlen
            summen[tag["tag"]] = summen.get(tag["tag"], 0.0) + float(wert)  # aufsummieren
            zaehler[tag["tag"]] = zaehler.get(tag["tag"], 0) + 1    # und mitzaehlen
    return {tag: summen[tag] / zaehler[tag] for tag in sorted(summen)}  # Mittel je Tag


def punkte_je_tag(mess):
    """Punkte je Spieltag: Mittel des Endpunkte-Stands geteilt durch die Laenge der Partie."""
    werte = [float(l["punkte_ende"]) for l in mess.get("laeufe") or []
             if isinstance(l.get("punkte_ende"), (int, float))
             and not isinstance(l.get("punkte_ende"), bool)]
    if not werte:                                                   # keine Punkte gemessen
        return None                                                 # None heisst "nicht gemessen"
    return round(sum(werte) / len(werte) / float(mess.get("tage") or 1), 3)  # Punkte je Tag


def zielabweichung(mess, kurve):
    """Abweichung der Zielgroesse (Punkte je Spieltag) vom Zielwert der Sollkurve, in Prozent."""
    ist = punkte_je_tag(mess)                                       # gemessene Punkte je Tag
    ziel = float((kurve.get("punkte_ziel_je_spieltag") or {}).get("wert") or 0)  # V-3: 3,3
    if ist is None or ziel <= 0:                                    # ohne Ist oder Ziel kein Urteil
        return {"ist": ist, "ziel": ziel, "abweichung_prozent": None}
    return {"ist": ist, "ziel": ziel,                               # das Ist, das Ziel
            "abweichung_prozent": round(abs(ist - ziel) / ziel * 100.0, 2)}  # und der Abstand


def korridor(mess, kurve, groessen=None):
    """Je Groesse: Lage im Korridor der Sollkurve, Fehlbetrag und Richtung.

    `fehlbetrag` ist der mittlere relative Abstand ausserhalb des Bandes (0 = im Korridor).
    `richtung` ist "zu wenig", "zu viel", "gemischt" oder "im Korridor" - der Vorschlag braucht
    eine eindeutige Richtung, sonst kann EIN Schritt sie nicht verbessern.
    """
    groessen = groessen or kurve.get("korridorgroessen") or ["holz", "stein", "nahrung", "gold"]
    ziel = {int(z["tag"]): z for z in kurve.get("tage") or []}      # Korridor je Spieltag
    aus = {}                                                        # Ergebnis je Groesse
    for groesse in groessen:
        mittel = mittel_je_tag(mess, groesse)                       # Mittelwert je Tag
        fehl, draussen, zu_wenig, zu_viel = 0.0, [], 0, 0           # Sammler
        fehl_unten, fehl_oben = 0.0, 0.0                            # Abstand je Richtung
        for tag in sorted(mittel):
            band = ziel.get(int(tag))                               # Korridor dieses Tages
            if not band or groesse not in band:                     # Tag ohne Band: ueberspringen
                continue
            unten = float(band[groesse]["unten"])                   # unterer Rand
            oben = float(band[groesse]["oben"])                     # oberer Rand
            wert = float(mittel[tag])                               # gemessener Mittelwert
            if unten <= wert <= oben:                               # im Band: nichts zu tun
                continue
            if wert < unten:                                        # zu wenig
                anteil = (unten - wert) / unten if unten > 0 else 0.0
                fehl_unten += anteil                                # Abstand nach unten
                zu_wenig += 1
                draussen.append([tag, "zu wenig", round(wert, 2), unten])
            else:                                                   # zu viel
                anteil = (wert - oben) / oben if oben > 0 else 0.0
                fehl_oben += anteil                                 # Abstand nach oben
                zu_viel += 1
                draussen.append([tag, "zu viel", round(wert, 2), oben])
            fehl += anteil                                          # Abstand aufsummieren
        tage_im_band = len([t for t in mittel if int(t) in ziel]) or 1
        # Die Richtung entscheidet der ABSTAND, nicht die Zahl der Tage: ein einzelner
        # Ausreisser in die Gegenrichtung (Tag 1: 22 statt 8 Holz) darf die Lage nicht kippen.
        if not zu_wenig and not zu_viel:                             # ueberall im Band
            richtung = "im Korridor"
        elif fehl_unten > fehl_oben * 1.05:                          # eindeutig zu wenig
            richtung = "zu wenig"
        elif fehl_oben > fehl_unten * 1.05:                          # eindeutig zu viel
            richtung = "zu viel"
        else:                                                       # beide Seiten gleich stark
            richtung = "gemischt"
        aus[groesse] = {
            "fehlbetrag": round(fehl / tage_im_band, 4),            # mittlerer Abstand je Tag
            "richtung": richtung,                                   # was zu tun waere
            "anzahl_draussen": len(draussen),                       # Zahl der Tage ausserhalb
            "tage_draussen": draussen[:10],                         # die ersten zehn als Beleg
            "mittel_ende": round(mittel[max(mittel)], 2) if mittel else None,
        }
    return aus


def _preis_kandidaten(wurzel):
    """Alle aenderbaren Preisfelder: Gebaeude OHNE `_belegt` (BELEGT wird nie vorgeschlagen)."""
    preise = lade(wurzel, "data", "baupreise.json").get("preise") or {}
    kandidaten = []                                                 # ein Eintrag je Preisfeld
    for gebaeude, eintrag in preise.items():
        if not isinstance(eintrag, dict):                            # kein Block: ueberspringen
            continue
        if "_belegt" in eintrag:                                     # BELEGT: nie vorschlagen
            continue
        felder, gewicht = [], 0.0                                    # Preisfelder und ihr Gewicht
        for feld, wert in eintrag.items():
            if str(feld).startswith("_") or feld == "budget":         # Erklaertexte zaehlen nicht
                continue
            if not isinstance(wert, (int, float)) or isinstance(wert, bool):
                continue                                             # nur echte Zahlen
            felder.append(feld)                                      # Preisfeld merken
            gewicht += float(wert)                                    # Gewicht = Baukosten gesamt
        for feld in felder:                                          # je Preisfeld ein Kandidat
            kandidaten.append({"datei": "baupreise.json", "gebaeude": gebaeude,
                               "feld": str(feld), "alt": eintrag[feld], "gewicht": gewicht})
    return kandidaten


def vorschlag(mess, kurve, regelkreis=None, wurzel=HIER):
    """HOECHSTENS ein Datenwert, der die schlechteste Groesse in den Korridor zurueckholt.

    Regel: die Groesse mit dem groessten Fehlbetrag, die einen aenderbaren Preis hat; dort das
    Gebaeude mit dem groessten Gewicht (groesste Wirkung); Schrittweite hoechstens der Wert aus
    `data/regelkreis.json` (10 Prozent). "zu wenig" senkt den Preis, "zu viel" hebt ihn.
    Kein Kandidat, gemischte Richtung oder Schrittweite unter einer Einheit: KEIN Vorschlag.
    """
    regelkreis = regelkreis if regelkreis is not None else lade_regelkreis(wurzel)
    schwellen = regelkreis.get("schwellen") or {}                    # die drei Zahlen
    grenze = float(schwellen["schrittweite_prozent"])                 # hoechste Schrittweite (Datei)
    lage = korridor(mess, kurve)                                      # Lage je Groesse
    kandidaten = _preis_kandidaten(wurzel)                            # was aenderbar ist
    notizen = []                                                      # was uebersprungen wurde
    for groesse, eintrag in sorted(lage.items(), key=lambda kv: -float(kv[1]["fehlbetrag"])):
        if float(eintrag["fehlbetrag"]) <= 0:                         # im Korridor: nichts zu tun
            continue
        if eintrag["richtung"] == "gemischt":                         # beide Richtungen
            notizen.append("%s liegt an manchen Tagen zu tief, an anderen zu hoch - ein Schritt "
                           "kann das nicht verbessern" % groesse)
            continue
        passend = [k for k in kandidaten if k["feld"] == groesse]     # Preisfelder dieser Groesse
        if not passend:                                               # nur belegte Preise
            notizen.append("%s hat keinen aenderbaren Preis (alle BELEGT)" % groesse)
            continue
        passend.sort(key=lambda k: -float(k["gewicht"]))              # groesste Wirkung zuerst
        for kandidat in passend:
            alt = float(kandidat["alt"])                              # heutiger Wert
            schritt = max(1.0, round(alt * grenze / 100.0))           # mindestens eine Einheit
            if alt > 0 and schritt / alt > grenze / 100.0 + 1e-9:      # mehr als 10 Prozent
                notizen.append("%s/%s: 10 Prozent waeren weniger als eine Einheit - waere mehr "
                               "als die erlaubte Schrittweite" % (kandidat["gebaeude"], groesse))
                continue
            if eintrag["richtung"] == "zu wenig":                      # zu wenig Rohstoff
                neu = alt - schritt                                   # Preis senken
                richtung = "senken"
            else:                                                      # zu viel Rohstoff
                neu = alt + schritt                                   # Preis heben
                richtung = "heben"
            if neu == alt:                                            # keine Veraenderung
                continue
            if isinstance(kandidat["alt"], int):                      # ganze Preise bleiben ganz
                neu = int(round(neu))
            return {"status": "vorschlag", "datei": kandidat["datei"],
                    "gebaeude": kandidat["gebaeude"], "feld": kandidat["feld"],
                    "alt": kandidat["alt"], "neu": neu, "groesse": groesse,
                    "richtung": richtung,
                    "schrittweite_prozent": round(abs(neu - alt) / alt * 100.0, 2) if alt else None,
                    "fehlbetrag": eintrag["fehlbetrag"], "notizen": notizen}
    return {"status": "keiner", "notizen": notizen,                  # kein Vorschlag in dieser Runde
            "grund": "keine Groesse mit aenderbarem Preis ausserhalb des Korridors"}


def _wurzelkopie(wurzel):
    """Kopie von src/, data/ und dem Spieltest-Werkzeug in einen temporaeren Ordner."""
    ziel = tempfile.mkdtemp(prefix="regelkreis_ab_")                 # eigener Ordner
    shutil.copytree(os.path.join(wurzel, "src"), os.path.join(ziel, "src"))   # Code kopieren
    shutil.copytree(os.path.join(wurzel, "data"), os.path.join(ziel, "data"))  # Daten kopieren
    os.makedirs(os.path.join(ziel, "tools"))                          # Werkzeugordner
    shutil.copy2(os.path.join(wurzel, "tools", "spieltest_simulation.py"),
                 os.path.join(ziel, "tools", "spieltest_simulation.py"))  # nur der Messlauf
    return ziel


def _wert_setzen(projekt, vorschlagswert):
    """Setzt den vorgeschlagenen Wert in einer KOPIE. `data/` des Projekts wird nie geoeffnet."""
    pfad = os.path.join(projekt, "data", vorschlagswert["datei"])     # Datei der Kopie
    with io.open(pfad, encoding="utf-8") as f:                        # Kopie lesen
        daten = json.load(f)
    block = (daten.get("preise") or {}).get(vorschlagswert["gebaeude"])  # Gebaeudeblock
    if not isinstance(block, dict):                                   # Block muss es geben
        raise SystemExit("Gebaeude %s fehlt in %s" % (vorschlagswert["gebaeude"], pfad))
    block[vorschlagswert["feld"]] = vorschlagswert["neu"]             # den einen Wert setzen
    with io.open(pfad, "w", encoding="utf-8", newline="\n") as f:    # neue Einrueckung wie vorher
        json.dump(daten, f, ensure_ascii=False, indent=2)
        f.write("\n")
    return pfad


def ab(wurzel=HIER, vorschlagswert=None, regelkreis=None, saaten=None, tage=None, stil=None):
    """Dieselben Startwerte mit und ohne Aenderung - die Aenderung wirkt nur in einer Kopie."""
    regelkreis = regelkreis if regelkreis is not None else lade_regelkreis(wurzel)
    if vorschlagswert is None:                                       # ohne Vorschlag kein A/B
        mess = messung(wurzel, regelkreis, saaten, tage, stil)       # dann nur messen
        vorschlagswert = vorschlag(mess, sollkurve(wurzel), regelkreis, wurzel)
        vorher = mess                                                # dieselbe Messung ist "vorher"
    else:                                                            # mit Vorschlag: erst messen
        vorher = messung(wurzel, regelkreis, saaten, tage, stil)
    kopie = _wurzelkopie(wurzel) if vorschlagswert.get("status") == "vorschlag" else None
    try:
        if kopie:                                                    # Aenderung nur in der Kopie
            _wert_setzen(kopie, vorschlagswert)
        nachher = messung(kopie or wurzel, regelkreis, saaten, tage, stil)
    finally:
        if kopie:                                                    # Kopie immer entfernen
            shutil.rmtree(kopie, ignore_errors=True)
    return {"vorher": vorher, "nachher": nachher, "vorschlag": vorschlagswert}


def _gefecht_mittel(mess):
    """Mittlerer Tag des ersten Gefechts ueber die Laeufe, die eines hatten (None = nicht gemessen)."""
    tage = [float(l["tag_erstes_gefecht"]) for l in mess.get("laeufe") or []
            if isinstance(l.get("tag_erstes_gefecht"), (int, float))
            and not isinstance(l.get("tag_erstes_gefecht"), bool)]
    if not tage:                                                     # kein Lauf hatte ein Gefecht
        return None                                                 # None, NICHT 0
    return round(sum(tage) / len(tage), 3)                           # Mittel der gemessenen Tage


def urteil(ablauf, kurve, regelkreis=None):
    """Das Urteil ueber einen A/B-Lauf nach den drei Schwellen aus `data/regelkreis.json`.

    Angenommen wird nur, wenn (1) die Zielabweichung mindestens `verbesserung_prozent` besser
    ist, (2) keine andere Groesse schlechter liegt als vorher (wer den Korridor verlaesst oder
    sich verschlechtert, wird MIT NAMEN abgelehnt) und (3) das erste Gefecht nicht spaeter
    kommt. Ein `null` beim ersten Gefecht wird uebergangen und nicht als Tag 0 gezaehlt.
    """
    vorher, nachher = ablauf["vorher"], ablauf["nachher"]            # die zwei Messungen
    if list(vorher.get("saaten") or []) != list(nachher.get("saaten") or []):
        raise ValueError("ungleiche Startwerte (Reihenfolge zaehlt): vorher %s, nachher %s"
                         % (vorher.get("saaten"), nachher.get("saaten")))
    if str(vorher.get("stil")) != str(nachher.get("stil")) or \
            float(vorher.get("tage") or 0) != float(nachher.get("tage") or 0):
        raise ValueError("Stil oder Laenge unterscheiden sich - das ist kein A/B")
    regelkreis = regelkreis if regelkreis is not None else lade_regelkreis()
    schwellen = regelkreis.get("schwellen") or {}
    schwelle = float(schwellen["verbesserung_prozent"])              # geforderte Verbesserung (Datei)
    gruende, befunde, korridore = [], [], {}                         # Sammler des Urteils
    ziel_vor = zielabweichung(vorher, kurve)                         # Abweichung vorher
    ziel_nach = zielabweichung(nachher, kurve)                       # Abweichung nachher
    if ziel_vor["abweichung_prozent"] is None or ziel_nach["abweichung_prozent"] is None:
        ziel_ok = False                                             # ohne Zahl kein Urteil
        gruende.append("Zielabweichung nicht messbar (keine Punkte im Lauf)")
    elif float(ziel_vor["abweichung_prozent"]) <= 1e-9:
        ziel_ok = False                                             # Ziel war schon erreicht
        gruende.append("das Ziel war vorher schon erreicht (0 Prozent Abweichung) - "
                       "es gibt nichts zu verbessern")
    elif float(ziel_nach["abweichung_prozent"]) < float(ziel_vor["abweichung_prozent"]) - 1e-9 \
            and float(ziel_nach["abweichung_prozent"]) <= \
            float(ziel_vor["abweichung_prozent"]) * (1.0 - schwelle / 100.0) + 1e-9:
        ziel_ok = True                                              # mindestens 20 Prozent besser
    else:
        ziel_ok = False                                             # zu wenig Verbesserung
        gruende.append("Zielabweichung verbessert sich nur um %s Prozentpunkte (%s -> %s Prozent), "
                       "gefordert sind mindestens %s Prozent"
                       % (round(float(ziel_vor["abweichung_prozent"])
                                - float(ziel_nach["abweichung_prozent"]), 2),
                          ziel_vor["abweichung_prozent"], ziel_nach["abweichung_prozent"], schwelle))
    groessen = regelkreis.get("korridorgroessen") or None            # beurteilte Groessen
    lage_vor, lage_nach = korridor(vorher, kurve, groessen), korridor(nachher, kurve, groessen)
    for groesse in lage_vor:                                        # jede Groesse einzeln
        alt, neu = lage_vor[groesse], lage_nach[groesse]
        war_drin = float(alt["fehlbetrag"]) <= 0                     # lag im Korridor
        ist_drin = float(neu["fehlbetrag"]) <= 0                     # liegt im Korridor
        schlechter = float(neu["fehlbetrag"]) > float(alt["fehlbetrag"]) + 1e-9
        korridore[groesse] = {"vorher": alt["fehlbetrag"], "nachher": neu["fehlbetrag"],
                              "war_im_korridor": war_drin, "ist_im_korridor": ist_drin,
                              "anzahl_draussen_vorher": alt["anzahl_draussen"],
                              "anzahl_draussen_nachher": neu["anzahl_draussen"]}
        if war_drin and not ist_drin:                               # hat den Korridor verlassen
            gruende.append("%s verlaesst den Korridor (%s Tage draussen statt 0)"
                           % (groesse, neu["anzahl_draussen"]))
        elif schlechter:                                            # schlechter geworden
            gruende.append("%s wird schlechter (%s statt %s Fehlbetrag)"
                           % (groesse, neu["fehlbetrag"], alt["fehlbetrag"]))
        elif not war_drin and not ist_drin:                         # blieb ausserhalb
            befunde.append("%s bleibt ausserhalb des Korridors (%s -> %s)"
                           % (groesse, alt["fehlbetrag"], neu["fehlbetrag"]))
    gefecht_vor, gefecht_nach = _gefecht_mittel(vorher), _gefecht_mittel(nachher)
    gefecht_ok = True                                               # ohne Messung kein Verstoss
    if gefecht_vor is None or gefecht_nach is None:
        befunde.append("erstes Gefecht nicht in allen Laeufen gemessen - Vergleich uebergangen")
    elif gefecht_nach > gefecht_vor + 1e-9:                         # spaeter als vorher
        gefecht_ok = False
        gruende.append("erstes Gefecht kommt spaeter (Tag %s statt %s)" % (gefecht_nach, gefecht_vor))
    if float(nachher.get("tage") or 0) and any(
            (l.get("uebersprungen") or 0) > 0 for l in nachher.get("laeufe") or []):
        befunde.append("mindestens ein Lauf hatte uebersprungene Schritte - Zahlen mit Vorsicht lesen")
    angenommen = bool(ziel_ok and gefecht_ok and not gruende)       # alles drei muss stimmen
    return {"angenommen": angenommen, "ziel_vorher": ziel_vor, "ziel_nachher": ziel_nach,
            "ziel_ok": ziel_ok, "gefecht_vorher": gefecht_vor, "gefecht_nachher": gefecht_nach,
            "gefecht_ok": gefecht_ok, "korridore": korridore, "schwelle_prozent": schwelle,
            "gruende": gruende, "befunde": befunde}


def urteil_text(ablauf, bewertung, kurve, regelkreis=None):
    """Die lesbare Fassung des Urteils - genau das, was in `docs/balancing/URTEIL_<n>.md` steht."""
    vorschlagswert = ablauf.get("vorschlag") or {}                   # der geprüfte Vorschlag
    z = ["# Urteil B-2 - A/B-Lauf des Regelkreises", ""]
    z.append("Erzeugt von `tools/balance_kreis.py --urteil` (Ablauf Schritt 9). "
             "Das Urteil ist eine Rechnung ueber zwei Messungen, keine Meinung: "
             "dieselben Startwerte, dieselbe Laenge, einmal mit und einmal ohne Aenderung.")
    z.append("")
    z.append("## Messumfang")
    z.append("")
    laeufe = ablauf["vorher"].get("saaten") or []                    # die Startwerte der Runde
    z.append("| Feld | Wert |")
    z.append("|---|---|")
    z.append("| Startwerte | %s |" % ", ".join(str(s) for s in laeufe))
    z.append("| Laenge | %g Spieltage |" % float(ablauf["vorher"].get("tage") or 0))
    z.append("| Stil | %s |" % ablauf["vorher"].get("stil"))
    z.append("| Laeufe je Seite | %d |" % len(ablauf["vorher"].get("laeufe") or []))
    z.append("| Wurzel der Aenderung | tempoeraere Kopie von `src/` und `data/` |")
    z.append("")
    z.append("## Der gepruefte Vorschlag")
    z.append("")
    if vorschlagswert.get("status") == "vorschlag":
        z.append("| Feld | Wert |")
        z.append("|---|---|")
        z.append("| Datendatei | `data/%s` |" % vorschlagswert.get("datei"))
        z.append("| Gebaeude | %s |" % vorschlagswert.get("gebaeude"))
        z.append("| Groesse | %s (%s) |" % (vorschlagswert.get("groesse"),
                                            vorschlagswert.get("richtung")))
        z.append("| Wert | %s -> **%s** |" % (vorschlagswert.get("alt"), vorschlagswert.get("neu")))
        z.append("| Schrittweite | %s Prozent |" % vorschlagswert.get("schrittweite_prozent"))
        z.append("| Fehlbetrag vorher | %s |" % vorschlagswert.get("fehlbetrag"))
    else:
        z.append("**Kein Vorschlag in dieser Runde.** %s" % (vorschlagswert.get("grund") or ""))
    for notiz in vorschlagswert.get("notizen") or []:                 # was uebersprungen wurde
        z.append("")
        z.append("- uebersprungen: %s" % notiz)
    z.append("")
    z.append("## Zielgroesse (Punkte je Spieltag, Zielwert %s)"
             % bewertung["ziel_vorher"].get("ziel"))
    z.append("")
    z.append("| | vorher | nachher |")
    z.append("|---|---|---|")
    z.append("| Punkte je Spieltag | %s | %s |"
             % (bewertung["ziel_vorher"].get("ist"), bewertung["ziel_nachher"].get("ist")))
    z.append("| Abweichung vom Ziel | %s Prozent | %s Prozent |"
             % (bewertung["ziel_vorher"].get("abweichung_prozent"),
                bewertung["ziel_nachher"].get("abweichung_prozent")))
    z.append("| gefordert | mindestens %g Prozent besser | |" % bewertung["schwelle_prozent"])
    z.append("")
    z.append("## Korridore (Sollkurve, `data/sollkurve.json`)")
    z.append("")
    z.append("| Groesse | Fehlbetrag vorher | Fehlbetrag nachher | Tage draussen vorher | nachher |")
    z.append("|---|---|---|---|---|")
    for groesse, eintrag in bewertung["korridore"].items():
        z.append("| %s | %s | %s | %s | %s |"
                 % (groesse, eintrag["vorher"], eintrag["nachher"],
                    eintrag["anzahl_draussen_vorher"], eintrag["anzahl_draussen_nachher"]))
    z.append("")
    z.append("## Erstes Gefecht")
    z.append("")
    z.append("Tag %s vorher, Tag %s nachher (`null` = in keinem Lauf gemessen, nicht Tag 0)."
             % (bewertung["gefecht_vorher"], bewertung["gefecht_nachher"]))
    z.append("")
    z.append("## Urteil")
    z.append("")
    z.append("**%s**" % ("ANGENOMMEN" if bewertung["angenommen"] else "ABGELEHNT"))
    z.append("")
    for grund in bewertung["gruende"]:                                # die tragenden Gruende
        z.append("- %s" % grund)
    for befund in bewertung["befunde"]:                               # Beobachtungen ohne Gewicht
        z.append("- Beobachtung: %s" % befund)
    z.append("")
    z.append("**Nichts wurde uebernommen.** Ein angenommenes Urteil ist eine Freigabe fuer Daniel, "
             "kein Schreibvorgang: `data/` bleibt unveraendert, bis er den Wert setzt.")
    z.append("")
    return "\n".join(z)


def naechste_urteil_nummer(wurzel=HIER):
    """Die naechste freie Nummer fuer `docs/balancing/URTEIL_<n>.md`."""
    ordner = os.path.join(wurzel, "docs", "balancing")
    if not os.path.isdir(ordner):                                     # Ordner darf fehlen
        return 1
    hoechste = 0                                                     # bisher hoechste Nummer
    for name in os.listdir(ordner):
        if name.startswith("URTEIL_") and name.endswith(".md"):       # nur Urteilsdateien
            stamm = name[len("URTEIL_"):-len(".md")]
            if stamm.isdigit():                                       # nur reine Nummern
                hoechste = max(hoechste, int(stamm))
    return hoechste + 1                                              # die naechste Nummer


def urteil_schreiben(wurzel, ablauf, bewertung, kurve, regelkreis=None):
    """Schreibt `docs/balancing/URTEIL_<n>.md` - die EINZIGE Datei, die dieser Schritt anlegt."""
    text = urteil_text(ablauf, bewertung, kurve, regelkreis)
    nummer = naechste_urteil_nummer(wurzel)                           # fortlaufend, nie ueberschreiben
    pfad = os.path.join(wurzel, "docs", "balancing", "URTEIL_%d.md" % nummer)
    os.makedirs(os.path.dirname(pfad), exist_ok=True)                 # Ordner sicherstellen
    with io.open(pfad, "w", encoding="utf-8", newline="\n") as f:     # LF wie die Dokumente
        f.write(text)
    return pfad                                                      # damit der Aufrufer es nennt


# ------------------------------------------------------------------ Feedback-Eingang
def buendeln(meldungen, schwelle=3):
    """Meldungen mit demselben Schluessel zu Buendeln; ab `schwelle` wird ein Messauftrag daraus.

    Der Schluessel ist das Feld `was` (klein geschrieben, ohne Leerraum am Rand). Der
    Gefuehlsdurchschnitt ist die zweite, weichere Haelfte: eine Zahl allein soll nie entscheiden.
    """
    gruppen = {}                                                     # Schluessel -> Buendel
    for meldung in meldungen or []:
        schluessel = str(meldung.get("was") or "").strip().lower()    # der Schluessel der Meldung
        if not schluessel:                                            # ohne Schluessel kein Buendel
            gruppen.setdefault("ohne Schluessel", {"schluessel": "ohne Schluessel", "zaehler": 0,
                                                   "gefuehle": [], "meldungen": []})
            gruppe = gruppen["ohne Schluessel"]
        else:
            gruppe = gruppen.setdefault(schluessel, {"schluessel": schluessel, "zaehler": 0,
                                                     "gefuehle": [], "meldungen": []})
        gruppe["zaehler"] = gruppe["zaehler"] + 1                     # zaehlen
        gefuehl = meldung.get("gefuehl")                              # 1 bis 5, freiwillig
        if isinstance(gefuehl, (int, float)) and not isinstance(gefuehl, bool):
            gruppe["gefuehle"].append(float(gefuehl))                 # nur echte Zahlen
        gruppe["meldungen"].append({"wann": meldung.get("wann"), "stand": meldung.get("stand"),
                                    "zahl": meldung.get("zahl")})     # der Beleg je Meldung
    aus = []                                                         # die Buendel als Liste
    for gruppe in gruppen.values():
        gefuehle = gruppe.pop("gefuehle")                             # Schnitt statt Rohwerte
        gruppe["gefuehl_schnitt"] = (round(sum(gefuehle) / len(gefuehle), 2)
                                     if gefuehle else None)
        gruppe["messauftrag"] = gruppe["zaehler"] >= int(schwelle)     # ab drei: messen
        aus.append(gruppe)
    aus.sort(key=lambda g: (-g["zaehler"], g["schluessel"]))          # haeufigste zuerst
    return aus


def feedback_lesen(wurzel=HIER):
    """Die eingegangenen Meldungen aus `docs/feedback/MELDUNGEN.json` (leer, wenn keine da sind)."""
    pfad = os.path.join(wurzel, "docs", "feedback", "MELDUNGEN.json")
    if not os.path.isfile(pfad):                                      # fehlende Datei = keine Meldung
        return []
    with io.open(pfad, encoding="utf-8") as f:                         # Datei lesen
        return (json.load(f).get("meldungen") or [])


def buendel_schreiben(wurzel=HIER, schwelle=None):
    """Schreibt `docs/feedback/BUENDEL.md` aus den Meldungen. Nichts anderes wird angefasst."""
    if schwelle is None:                                              # Schwelle aus der Datendatei
        schwelle = float((lade_regelkreis(wurzel).get("schwellen") or {})["meldungen_je_buendel"])
    buendel = buendeln(feedback_lesen(wurzel), schwelle)
    z = ["# Feedback-Buendel", ""]
    z.append("Erzeugt von `tools/balance_kreis.py --feedback` aus `docs/feedback/MELDUNGEN.json`. "
             "Ab **%s gleichen Meldungen** entsteht ein Messauftrag; ein Tester-Buendel sticht eine "
             "reine Kennzahl, entschieden wird von Daniel." % schwelle)
    z.append("")
    if not buendel:                                                   # leere Lage ehrlich sagen
        z.append("**Keine Meldungen eingegangen.**")
    else:
        z.append("| Schluessel | Meldungen | Gefuehl (1-5) | Messauftrag |")
        z.append("|---|---|---|---|")
        for eintrag in buendel:
            z.append("| %s | %s | %s | %s |"
                     % (eintrag["schluessel"], eintrag["zaehler"],
                        eintrag["gefuehl_schnitt"] if eintrag["gefuehl_schnitt"] is not None else "-",
                        "ja" if eintrag["messauftrag"] else "nein"))
    z.append("")
    pfad = os.path.join(wurzel, "docs", "feedback", "BUENDEL.md")
    os.makedirs(os.path.dirname(pfad), exist_ok=True)                 # Ordner sicherstellen
    with io.open(pfad, "w", encoding="utf-8", newline="\n") as f:     # LF wie die Dokumente
        f.write("\n".join(z))
    return pfad, buendel


def _regelkreis_lauf(args):
    """Der Regelkreis von der Kommandozeile: messen, vorschlagen, A/B, Urteil.

    Jeder Schritt ist einzeln aufrufbar; `--urteil` faehrt die ganze Runde und schreibt
    `docs/balancing/URTEIL_<n>.md`. Geschrieben wird in `data/` NICHTS - die Aenderung des
    A/B-Laufs lebt in einer tempoeraeren Kopie.
    """
    regelkreis = lade_regelkreis(args.wurzel)                          # Schwellen und Messumfang
    kurve = sollkurve(args.wurzel, args.tage)                          # Korridor je Spieltag
    mess = messung(args.wurzel, regelkreis)                            # zehn Laeufe, Startwerte 1..10
    ziel = zielabweichung(mess, kurve)                                 # Punkte gegen den Zielwert
    lage = korridor(mess, kurve)                                       # Lage je Groesse
    print("Messung: %d Laeufe, %s Spieltage, Stil %s"
          % (len(mess["laeufe"]), mess["tage"], mess["stil"]))
    print("Ziel: %.3f Punkte je Spieltag (Zielwert %s), Abweichung %s Prozent"
          % (float(ziel["ist"] or 0), ziel["ziel"], ziel["abweichung_prozent"]))
    for groesse in ("holz", "stein", "nahrung", "gold"):
        eintrag = lage.get(groesse) or {}
        print("  %-8s Fehlbetrag %-8s Richtung %-12s Tage draussen %s  Ende %s"
              % (groesse, eintrag.get("fehlbetrag"), eintrag.get("richtung"),
                 eintrag.get("anzahl_draussen"), eintrag.get("mittel_ende")))
    if args.messung and not (args.vorschlag or args.ab or args.urteil):
        return 0                                                       # nur messen war der Auftrag
    vor = vorschlag(mess, kurve, regelkreis, args.wurzel)               # hoechstens EIN Datenwert
    if vor.get("status") == "vorschlag":
        print("Vorschlag: %s/%s %s -> %s (Schrittweite %s Prozent, Groesse %s, %s)"
              % (vor["gebaeude"], vor["feld"], vor["alt"], vor["neu"],
                 vor["schrittweite_prozent"], vor["groesse"], vor["richtung"]))
    else:
        print("Vorschlag: keiner -", vor.get("grund"))
    for notiz in vor.get("notizen") or []:
        print("   uebersprungen:", notiz)
    if args.vorschlag and not (args.ab or args.urteil):
        return 0                                                       # nur vorschlagen war der Auftrag
    if vor.get("status") != "vorschlag":
        return 0                                                       # ohne Vorschlag kein A/B
    lauf = ab(args.wurzel, vor, regelkreis)                            # A/B in einer Kopie
    bewertung = urteil(lauf, kurve, regelkreis)                        # das Urteil
    print("Urteil:", "ANGENOMMEN" if bewertung["angenommen"] else "ABGELEHNT")
    for grund in bewertung["gruende"]:
        print("   -", grund)
    for befund in bewertung["befunde"]:
        print("   Beobachtung:", befund)
    if args.urteil:                                                    # die Urteilsdatei
        pfad = urteil_schreiben(args.wurzel, lauf, bewertung, kurve, regelkreis)
        print("Geschrieben:", pfad)
    return 0


def main():
    """Aufruf von der Kommandozeile: Sollkurve, Regelkreis (messen, vorschlagen, A/B, Urteil)."""
    zerleger = argparse.ArgumentParser(description="B-1 Sollkurve und B-2 Regelkreis aus den Daten")
    zerleger.add_argument("--sollkurve", action="store_true", help="die Sollkurve rechnen")
    zerleger.add_argument("--wurzel", default=HIER, help="Projektordner (fuer Pruefungen)")
    zerleger.add_argument("--tage", type=int, default=20, help="Anzahl der Spieltage")
    zerleger.add_argument("--schreiben", action="store_true", help="data/sollkurve.json schreiben")
    zerleger.add_argument("--messung", action="store_true", help="B-2: die zehn Laeufe messen")
    zerleger.add_argument("--vorschlag", action="store_true", help="B-2: messen und vorschlagen")
    zerleger.add_argument("--ab", action="store_true", help="B-2: A/B fahren und urteilen")
    zerleger.add_argument("--urteil", action="store_true",
                          help="B-2: ganze Runde fahren und docs/balancing/URTEIL_<n>.md schreiben")
    zerleger.add_argument("--feedback", action="store_true",
                          help="Feedback-Buendel aus docs/feedback/MELDUNGEN.json schreiben")
    args = zerleger.parse_args()
    if args.feedback:                                                  # Feedback zuerst
        pfad, buendel = buendel_schreiben(args.wurzel)
        print("Buendel:", pfad, "| Schluessel:", len(buendel),
              "| Messauftraege:", sum(1 for b in buendel if b["messauftrag"]))
        return 0
    if args.messung or args.vorschlag or args.ab or args.urteil:        # der Regelkreis
        return _regelkreis_lauf(args)
    if not args.sollkurve:
        print("Aufruf: --sollkurve [--tage N] [--schreiben] | --messung | --vorschlag | "
              "--ab | --urteil | --feedback  [--wurzel PFAD]")
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
