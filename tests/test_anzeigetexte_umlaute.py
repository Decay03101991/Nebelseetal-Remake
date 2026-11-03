# -*- coding: ascii -*-
"""Wache T-1: Ingame-Texte tragen echte Umlaute (Vorgabe Daniel 03.11.2026).

Daniels Wortlaut: "Ich will Ingame NICHT das du zum Beispiel statt waehlen einfach plump
waehlen schreibst. Solche kleinigkeiten machen viel aus im Gesamteindruck."

Was diese Datei prueft:
  1. Die Inventur laeuft und findet Anzeigetexte (sonst prueft alles danach nichts).
  2. In KEINEM Anzeigetext steht eine Ersatzschreibweise aus WORDLISTE.
  3. Die Wortliste deckt Daniels Vorgabe woertlich ab (die Woerter stehen unten).
  4. Technische Ausnahmen sind begruendet - hier UND in der Messstelle.
  5. Code-Bezuege in Anzeigetexten bleiben ASCII (ein Hinweis darf `einheiten.ist_kaempfer`
     nennen; ein Umlaut dort wuerde einen Namen zeigen, den es im Code nicht gibt).
  6. GEGENPROBE: ein erfundener Text mit "waehlen" MUSS als Fundstelle erkannt werden -
     sonst ist die Wache blind und ihr Gruen bedeutet nichts.

Die Messung selbst steht in `tools/anzeigetexte_inventur.py` (EINE Quelle fuer Messung und
Ersetzung, Muster F-04). Diese Datei haelt die WORTLISTE und die Ausnahmen - sie ist die
Zusage an Daniel, nicht die Messung.

Warum die Datei ASCII-only ist: sie ist eine Pruefdatei, und Pruefdateien sind ASCII-only.
Die Zielwoerter stehen deshalb als Ersatzschreibweise in der Liste, die Umlautform wird aus
Zeichencodes gebaut (siehe UMLAUT unten) - so bleibt die Datei selbst ASCII.
"""
from __future__ import annotations

import os
import sys

HIER = os.path.dirname(os.path.abspath(__file__))  # Ordner tests/
ROOT = os.path.dirname(HIER)  # Projektwurzel
sys.path[:0] = [os.path.join(ROOT, "src"), os.path.join(ROOT, "tools")]

import harness  # noqa: E402  (Pruefrahmen: check, befund, bericht)
from harness import check, befund, abschnitt, bericht  # noqa: E402

import anzeigetexte_inventur as inventur  # noqa: E402  (die Messstelle)

# Umlaute ueber Zeichencodes: haelt diese Datei ASCII-only.
AE, OE, UE, SS = chr(0xE4), chr(0xF6), chr(0xFC), chr(0xDF)
UMLAUT = {"ae": AE, "oe": OE, "ue": UE, "ss": SS}

# Daniels Wortliste (Vorgabe 03.11.2026, docs/VORGABE_INGAME_TEXTE_20261103.md) - diese
# Woerter duerfen in Anzeigetexten NICHT als Ersatzschreibweise stehen.
WORDLISTE = [
    "waehlen", "auswaehlen", "Gebaeude", "fuer", "koennen", "muessen", "groesse", "moeglich",
    "zurueck", "naechste", "aendern", "zusaetzlich", "hoechstens", "schliessen", "oeffnen",
    "pruefen", "uebersicht", "verfuegbar", "bevoelkerung", "gruenden", "waere", "ueber",
    "koennte", "muesste",
]

# Technische Ausnahmen: Woerter, die wie eine Ersatzschreibweise aussehen, aber Kennungen
# sind. Begruendung hier UND in `tools/anzeigetexte_inventur.py` (AUSNAHMEN).
AUSNAHMEN_DOKU = {
    "spieloekonomie": "Modulname des Kerns - eine Anzeige, die darauf verweist, nennt den Code",
    "oeokonomie-1": "Kennzeichen eines Admin-Teststandes, kein Anzeigetext",
    "PRIORITAET": "Name der Konstanten _PRIORITAET - ein Hinweistext nennt sie woertlich",
    "GELAENDEFARBEN": "Name der Konstanten WELT_GELAENDEFARBEN in einem Hinweistext",
    "GELAENDEREIHENFOLGE": "Name der Konstanten WELT_GELAENDEREIHENFOLGE in einem Hinweistext",
}

PROBEN_QUELLE = '''\
"""Erfundene Quelle fuer die Gegenprobe (kein Spielcode)."""


def baue(label):
    """Baut einen Text - dieselbe Form wie im Spiel."""
    return label


def anzeigen(wurzel):
    """Setzt zwei Anzeigetexte, einer mit Ersatzschreibweise."""
    wurzel.tk.Label(wurzel, text="Bitte eine Zahl ab 1 waehlen.")
    wurzel.tk.Label(wurzel, text="Bitte eine Zahl ab 1 w" + chr(0xE4) + "hlen.")
'''


def _melden(funde, grenze=12):
    """Druckt die ersten Fundstellen, damit ein roter Lauf lesbar bleibt."""
    for klasse, datei, zeile, art, wort, text in funde[:grenze]:
        print("        %s:%s (%s) %s \"%s\"" % (datei, zeile, art, wort, text[:70]))


def abschnitt_1_inventur():
    """1. Die Messung laeuft und findet ueberhaupt Anzeigetexte."""
    abschnitt("1. die Inventur der Anzeigetexte laeuft")
    ergebnis = inventur.sammle()
    anzeige = sum(z["A"] + z["B"] for z in ergebnis["je_datei"].values())
    check("die Inventur liest Anzeigetexte", anzeige > 1000, "%d Texte" % anzeige)
    check("die Inventur nennt Dateien", len(ergebnis["je_datei"]) > 40,
          "%d Dateien" % len(ergebnis["je_datei"]))


def abschnitt_2_keine_ersatzform():
    """2. Keine Ersatzschreibweise in einem Anzeigetext."""
    abschnitt("2. keine Ersatzschreibweise in Anzeigetexten")
    ergebnis = inventur.sammle()
    funde = ergebnis["funde"]
    check("kein Anzeigetext traegt eine Ersatzschreibweise", not funde,
          "%d Fundstellen" % len(funde))
    if funde:
        _melden(funde)
    check("die Datendateien (Gebaeude, Einheiten, Forschung, Waren) sind sauber",
          not ergebnis["json"], "%d Namen" % len(ergebnis["json"]))
    for dateiname, kennung, feld, wert in ergebnis["json"][:10]:
        print("        %s %s %s \"%s\"" % (dateiname, kennung, feld, wert))


def abschnitt_3_wortliste():
    """3. Die Wortliste deckt Daniels Vorgabe ab und die Wache greift bei jedem Wort."""
    abschnitt("3. Daniels Wortliste wird von der Wache erkannt")
    fehlend = [wort for wort in WORDLISTE if not inventur.ERSATZ_MUSTER.fullmatch(wort)]
    check("jedes Wort aus Daniels Vorgabe steht in der Wache", not fehlend, str(fehlend))
    for wort in WORDLISTE:  # Gegenprobe je Wort: das Muster MUSS treffen
        if not inventur.ERSATZ_MUSTER.fullmatch(wort):
            print("        trifft nicht: %s" % wort)


def abschnitt_4_ausnahmen():
    """4. Technische Ausnahmen sind begruendet und stehen in der Messstelle."""
    abschnitt("4. technische Ausnahmen sind begruendet")
    for wort, grund in AUSNAHMEN_DOKU.items():
        eintrag = inventur.AUSNAHMEN.get(wort)
        check("Ausnahme %s steht in der Messstelle" % wort, eintrag is not None)
        if eintrag:
            check("Ausnahme %s nennt einen Grund" % wort, bool(eintrag[0]))
            check("Ausnahme %s nennt denselben Grund wie hier" % wort, eintrag[0] == grund)
        check("Ausnahme %s hat hier einen Grund" % wort, bool(grund))
    for wort in inventur.AUSNAHMEN:  # keine stille Ausnahme in der Messstelle
        check("Ausnahme %s ist hier dokumentiert" % wort, wort in AUSNAHMEN_DOKU)


def abschnitt_5_code_bezuege():
    """5. Code-Bezuege in Anzeigetexten bleiben ASCII (Schuetzen und Rueckweg)."""
    abschnitt("5. Code-Bezuege in Anzeigetexten bleiben ASCII")
    proben = [
        "erwartet eine der 20 Kennungen aus gelaende.alle_gebaeude()",
        "Die Datei data/bot_gruendung.json wird gelesen",
        "einheiten.ist_kaempfer zaehlt dazu",
        "Die Reihenfolge kommt aus spieloekonomie.REGELN",
        "main.WELT_GELAENDEFARBEN nennt die Farben",
    ]
    for probe in proben:
        geschuetzt, tabelle = inventur.schuetzen(probe)
        check("Schutz laesst sich zuruecknehmen: %s" % probe[:32],
              inventur.entschuetzen(geschuetzt, tabelle) == probe)
        check("Schutz blendet etwas aus: %s" % probe[:32], geschuetzt != probe,
              geschuetzt[:60])
    # Die Wache darf eine Kennung NICHT als Ersatzschreibweise melden.
    for probe in ("spieloekonomie", "PRIORITAET", "GELAENDEFARBEN"):
        check("Kennung %s gilt nicht als Fundstelle" % probe, inventur.ist_ausnahme(probe))
    check("ein normales Wort gilt nicht als Ausnahme", not inventur.ist_ausnahme("waehlen"))


def abschnitt_6_gegenprobe():
    """6. GEGENPROBE: die Wache MUSS bei einer Ersatzschreibweise rot werden."""
    abschnitt("6. Gegenprobe - die Wache greift wirklich")
    funde = inventur.pruefe_quelle(PROBEN_QUELLE, "probe_gegenprobe.py")
    woerter = [fund[4] for fund in funde]
    check("die Gegenprobe erzeugt Fundstellen", bool(funde), "%d Fundstellen" % len(funde))
    check("die Gegenprobe findet 'waehlen'", "waehlen" in woerter, str(woerter))
    check("die Gegenprobe sieht GENAU eine Fundstelle (der Umlaut-Text zaehlt nicht)",
          len(funde) == 1, str([(f[2], f[3], f[4]) for f in funde]))
    if funde:
        _melden(funde)
    # Zweite Gegenprobe: derselbe Text mit echtem Umlaut erzeugt keine Fundstelle.
    sauber = PROBEN_QUELLE.replace("waehlen", "w" + AE + "hlen")
    check("derselbe Text mit echtem Umlaut ist sauber",
          not inventur.pruefe_quelle(sauber, "probe_sauber.py"))
    # Dritte Gegenprobe: ein Docstring mit Ersatzschreibweise zaehlt NICHT.
    docstring = '"""Ein Docstring mit waehlen und Gebaeude - keine Anzeige."""\n'
    check("ein Docstring zaehlt nicht als Anzeige",
          not inventur.pruefe_quelle(docstring, "probe_doc.py"))


def main():
    """Fuehrt alle Abschnitte aus und zieht den Schlussstrich."""
    print("T-1: Anzeigetexte mit echten Umlauten (Daniel 03.11.2026)")
    abschnitt_1_inventur()
    abschnitt_2_keine_ersatzform()
    abschnitt_3_wortliste()
    abschnitt_4_ausnahmen()
    abschnitt_5_code_bezuege()
    abschnitt_6_gegenprobe()
    bericht()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
