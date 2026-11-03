"""Setzt in ANZEIGETEXTEN echte Umlaute (Schnitt T-1, Vorgabe Daniel 03.11.2026).

Die Messstelle ist `tools/anzeigetexte_inventur.py`: es zaehlt die Literale, die wirklich
in eine Anzeige gehen (Klassen A belegt und B Fliesstext). Dieses Werkzeug liest DIESELBE
Messung und ersetzt darin nur die Ersatzschreibweisen, die in `WORT_KARTE` stehen.

Was NICHT angefasst wird:
    * Kennungen, JSON-Schluessel, Dateinamen, Bezeichner (die Inventur zaehlt sie nicht)
    * Docstrings und Kommentare (stehen nicht in der Messung; ein Kommentar ausserhalb
      eines Literals wird nie beruehrt, weil nur Literal-Spannen ersetzt werden)
    * die Pruefdateien unter tests/ (ASCII-only bleibt Pflicht)

Ersetzt wird auf der EXAKTEN Quelle-Spanne des Literals. `ast` nennt Spalten in UTF-8-BYTES
(nachgemessen 03.11.2026 an einer Zeile mit Umlaut vor dem Literal), deshalb wird auf Bytes
geschnitten und die Spanne zeichenweise zurueckgeschrieben.

Aufruf:
    python -X utf8 tools/anzeigetexte_umlaute_setzen.py --tabelle     # Wortkarte zeigen
    python -X utf8 tools/anzeigetexte_umlaute_setzen.py --probe       # nur anzeigen
    python -X utf8 tools/anzeigetexte_umlaute_setzen.py --schreiben   # ersetzen
    python -X utf8 tools/anzeigetexte_umlaute_setzen.py --schreiben --eine main.py
"""
from __future__ import annotations

import ast
import io
import os
import re
import sys

import anzeigetexte_inventur as inventur  # die EINE Messstelle (Klassen A und B)

SRC = inventur.SRC  # Ordner mit dem Spielcode

# Wortkarte: ASCII-Schreibweise -> echte Umlaute. Gesucht wird als TEILWORT (Stamm),
# damit auch Zusammensetzungen treffen (Gelaendearten, Gruendungspaket, Uebersichtskarte).
# Reihenfolge zaehlt nicht: laengere Staemme werden zuerst geprueft (siehe WORT_KARTE_SORTIERT).
WORT_KARTE = [
    # waehlen und Auswahl
    ("waehl", "wähl"),            # waehlen, auswaehlen, gewaehlt, Waehle
    # Gebaeude, Gelaende, Menue, Flaechen
    ("gebaeu", "gebäu"),          # Gebaeude, Funktionsgebaeude, Rohstoffgebaeude
    ("gelaend", "geländ"),        # Gelaende, Gelaendearten, Gelaendefarben
    ("menue", "menü"),            # Menue, Menuepunkt, Baumenue
    ("flaech", "fläch"),          # Flaeche, Flaechchen
    # fuehren (fuehrt, gefuehrt, mitgefuehrt)
    ("fuehr", "führ"),            # fuehrt, fuehrend, mitgefuehrte
    # fuer, ueber, zurueck, naechst, uebrig
    ("fuer", "für"),              # fuer, Fuer
    ("ueber", "über"),            # ueber, uebernommen, Uebersicht, ueberschreiben
    ("zurueck", "zurück"),        # zurueck, Zuruecksetzen, zurueckkehren
    ("naechst", "nächst"),        # naechste, naechsten, naechster
    ("uebrig", "übrig"),          # uebrig, uebrige
    # koennen, muessen, duerfen, moechten, haetten
    ("koenn", "könn"),            # koennen, koennte
    ("muess", "müss"),            # muessen, muesste
    ("duerf", "dürf"),            # duerfen, duerfte
    ("moecht", "möcht"),          # moechte, moechten
    ("braeucht", "bräucht"),      # braeuchte
    ("haett", "hätt"),            # haette, haetten
    ("wuerde", "würde"),          # wuerde, wuerden
    # Groesse, moeglich, hoechst, gueltig, zulaessig
    ("groess", "größ"),           # groesser, Groesse, Kartengroesse
    ("gross", "groß"),            # gross, Grossreich
    ("moegl", "mögl"),            # moeglich, Moeglichkeit, Moeglichst
    ("hoechst", "höchst"),        # hoechstens, Hoechstertrag
    ("gueltig", "gültig"),        # gueltig, ungueltig
    ("zulaessig", "zulässig"),    # zulaessig, unzulaessig
    # aendern, ergaenzen, erfuellen, entfallen, enthalten, halten
    ("aender", "änder"),          # aendert, aendern, Aenderungen, unveraendert
    ("veraender", "veränder"),    # veraendert
    ("ergaenz", "ergänz"),        # ergaenzt, Ergaenzung
    ("erfuell", "erfüll"),        # erfuellt, erfuellbar
    ("entfaell", "entfäll"),      # entfaellt
    ("haelt", "hält"),            # haelt, enthaelt, behaelt
    # gehoeren, erhoehen, Hoehe
    ("gehoer", "gehör"),          # gehoert, gehoeren, zugehoerig
    ("erhoe", "erhö"),            # erhoeht, erhoehen
    ("hoehe", "höhe"),            # Hoehe, Hoehen
    # laufen, fallen, schlagen, tragen, wachsen, haengen
    ("laeuf", "läuf"),            # laeuft, Waldlaeufer
    ("faell", "fäll"),            # faellt, Holzfaeller, Faelle
    ("schlaeg", "schläg"),        # schlaegt, Schlaeger
    ("traeg", "träg"),            # traegt, traege
    ("waechst", "wächst"),        # waechst
    ("haeng", "häng"),            # haengt, abhaengig
    # rueck (Rueckzug, Rueckweg, Rueckkehr, rueckwirkend)
    ("rueck", "rück"),            # Rueckzug, Rueckweg, rueckwirkend
    ("vorrueck", "vorrück"),      # vorruecken
    # pruefen, loeschen, erloesen
    ("pruef", "prüf"),            # pruefen, Pruefung, Pruefsumme
    ("geloesch", "gelösch"),      # Geloeschte, geloescht
    ("loesch", "lösch"),          # loeschen, Loeschung
    ("loes", "lös"),              # Loesung, geloest
    ("erloes", "erlös"),          # Handelserloes, erloest
    # zaehlen, Zahlen, Stueck
    ("zaehl", "zähl"),            # zaehlen, zaehlt
    ("fuenf", "fünf"),            # fuenf, Fuenfkampf
    ("saetz", "sätz"),            # Saetze, Vorschlaege (nicht: Saetze aus saetz)
    ("stueck", "stück"),          # Stueckzahl, Bruchstueck
    # Kaempfer, Militaer, Schuetze, Staerke, Schwaeche
    ("kaempf", "kämpf"),          # Kaempfer, Nahkaempfer
    ("militaer", "militär"),      # Militaer
    ("schuetz", "schütz"),        # Schuetzen
    ("staerk", "stärk"),          # Staerke, staerker
    ("schwaech", "schwäch"),      # Schwaeche
    ("spaeh", "späh"),            # Spaeher
    ("spaenn", "spänn"),          # Einspaenner, Zweispaenner
    ("raech", "räch"),            # Raecher
    # Vorraete, Gebuehr, Kapazitaet, Bestaende, Staende, Staette
    ("vorraet", "vorrät"),        # Vorraete, vorraete
    ("gebuehr", "gebühr"),        # Gebuehr
    ("kapazitaet", "kapazität"),  # Kapazitaet
    ("bestaend", "beständ"),      # Bestaende
    ("staend", "ständ"),          # Staende, Spielstaende, bestaendig
    ("staett", "stätt"),          # Ausbildungsstaette
    # Voelker, Doerfer, Goetter, Werkstaetten, Tuerme, Waelle
    ("voelk", "völk"),            # Voelker, Voelkern
    ("doerf", "dörf"),            # Doerfer, Doerfern, Testdoerfer
    ("goett", "gött"),            # Goetterschutz, Goetter
    ("werkstaett", "werkstätt"),  # Werkstaetten
    ("tuerm", "türm"),            # Tuerme
    ("waell", "wäll"),            # Ortswaelle
    ("plaetz", "plätz"),          # Ladeplaetze
    ("bauplaetze", "bauplätze"),  # Bauplaetze
    # Nahe, frueh, spaet, laenger, aelter, endgueltig, noetig
    ("naehe", "nähe"),            # Naehe, naeher
    ("frueh", "früh"),            # fruehestens
    ("spaet", "spät"),            # spaeter, spaetestens
    ("laenger", "länger"),        # laenger
    ("aelter", "älter"),          # aelter, aeltere
    ("endguelt", "endgült"),      # endgueltig
    ("noetig", "nötig"),          # noetig, benoetigt
    # Woerterbuch, Buecher, Luecken, Schluessel, fluessig
    ("woerterbuch", "wörterbuch"),  # Woerterbuch
    ("buech", "büch"),            # Buecher
    ("lueck", "lück"),            # Luecken
    ("schluess", "schlüss"),      # Schluessel
    ("fluessig", "flüssig"),      # fluessig
    # ausdruecklich, Ankuendigung, tatsaechlich, eigenstaendig, abhaengig
    ("ausdrueck", "ausdrück"),    # ausdruecklich
    ("ankuendig", "ankündig"),    # Ankuendigung
    ("tatsaechlich", "tatsächlich"),  # tatsaechliche
    ("eigenstaendig", "eigenständig"),  # eigenstaendige
    ("abhaengig", "abhängig"),    # abhaengig, unabhaengig
    ("vollstaendig", "vollständig"),  # unvollstaendig
    ("beschaedig", "beschädig"),  # beschaedigt
    ("klaer", "klär"),            # Aufklaerung, aufgeklaert
    ("schraenk", "schränk"),      # Eingeschraenkter
    # verfuegen, genuegen, gruen, gruenden, zusaetzlich, regulaer
    ("verfueg", "verfüg"),        # Verfuegung, verfuegbar
    ("genueg", "genüg"),          # genuegt, genuegend
    ("gruen", "grün"),            # gruen, Gruenflaeche
    ("gruend", "gründ"),          # gruenden, Gruendung, Gruende
    ("zusaetzl", "zusätzl"),      # zusaetzlich
    ("regulaer", "regulär"),      # regulaerer, regulaeren
    # woertlich, pluendern, sued, waehrend, waere, schliessen, oeffnen
    ("woertlich", "wörtlich"),    # woertlich
    ("pluender", "plünder"),      # pluendern
    ("sued", "süd"),              # sued
    ("waehr", "währ"),            # waehrend
    ("waer", "wär"),              # waere, waeren, gewaehrt
    ("schliess", "schließ"),      # Schliessen, schliessen
    ("oeffn", "öffn"),            # oeffnen, geoeffnet
    ("kaestchen", "kästchen"),    # Kaestchen, Gelaendekaestchen
    ("oekonomie", "ökonomie"),    # Oekonomie (Ausnahme: spieloekonomie bleibt Kennung)
    # ausser, draussen, eintragen, Auftraege, Vorschlaege, Haendler, erzuernt
    ("ausser", "außer"),          # ausser, ausserhalb
    ("fusstt", "fußt"),           # Schreibfehler in der Quelle: ss + tt, richtig ist ss + t
    ("fuss", "fuß"),              # Fusstruppen, Fusstruppe, fuss
    ("drauss", "drauß"),          # draussen
    ("eintraeg", "einträg"),      # Eintraege
    ("auftraeg", "aufträg"),      # Auftraege
    ("vorschlaeg", "vorschläg"),  # Vorschlaege
    ("haendl", "händl"),          # Haendler
    ("erzuernt", "erzürnt"),      # erzuernt
    # weitere deutsche Staemme, damit spaetere Texte nicht durchfallen
    ("kraeft", "kräft"),          # Kraefte
    ("maecht", "mächt"),          # maechtig
    ("naecht", "nächt"),          # naechtlich
    ("taet", "tät"),              # Taetigkeit
    ("faeh", "fäh"),              # Faehigkeit
    ("gaeng", "gäng"),            # gaengig
    ("raeum", "räum"),            # Raeume
    ("schaetz", "schätz"),        # schaetzen
    ("aeuss", "äuß"),             # aeusserst
    ("aehnl", "ähnl"),            # aehnlich
    ("erwaehn", "erwähn"),        # erwaehnt
    ("bevoelker", "bevölker"),    # Bevoelkerung
    ("hoer", "hör"),              # hoeren, gehoert (nicht: gehoert -> gehoer)
    ("aussen", "außen"),          # aussen
    ("wuensch", "wünsch"),        # wuenschen
    ("taeusch", "täusch"),        # taeuschen
    ("foerder", "förder"),        # foerdern
    ("koerper", "körper"),        # Koerper
    ("ernaehr", "ernähr"),        # ernaehren
    ("anfaeng", "anfäng"),        # anfaenglich
    ("unterstuetz", "unterstütz"),  # unterstuetzen
    ("haeuf", "häuf"),            # haeufig
    ("taeglich", "täglich"),      # taeglich
]

# Laengste Staemme zuerst, damit "loesch" nicht von "loes" halb ersetzt wird.
WORT_KARTE_SORTIERT = sorted(WORT_KARTE, key=lambda paar: len(paar[0]), reverse=True)


def _fall_anpassen(treffer, ersatz):
    """Uebernimmt die Schreibweise des Treffers auf den Ersatz (gross/klein/gemischt)."""
    if treffer.isupper():  # GELAENDE -> GELÄNDE
        return ersatz.upper()
    if treffer[:1].isupper():  # Gelaende -> Gelände
        return ersatz[:1].upper() + ersatz[1:]
    return ersatz  # gelaende -> gelände


def umlaute(text):
    """Ersetzt alle Ersatzschreibweisen der Wortkarte in einem Text.

    Code-Bezuege (inventur.schuetzen: Kennungen aus AUSNAHMEN, `einheiten.ist_kaempfer`,
    `data/bot_gruendung.json`, Funktionsnamen vor Klammern) werden vorher ausgeblendet und
    danach zurueckgesetzt - eine Anzeige, die auf Code verweist, muss den Code-Namen nennen.
    """
    ergebnis, geschuetzt = inventur.schuetzen(text)  # Code-Bezuege ausblenden
    for ascii_form, umlaut_form in WORT_KARTE_SORTIERT:
        muster = re.compile(re.escape(ascii_form), re.IGNORECASE)  # Teilwort, Schreibung egal
        ergebnis = muster.sub(lambda t: _fall_anpassen(t.group(0), umlaut_form), ergebnis)
    return inventur.entschuetzen(ergebnis, geschuetzt)  # Code-Bezuege zurueckholen


def _zeilen_versatz(quelle):
    """Byte- und Zeichen-Versatz jeder Zeile (ast zaehlt Spalten in UTF-8-Bytes)."""
    byte_versatz = [0]  # Byte-Anfang je Zeile
    zeichen_versatz = [0]  # Zeichen-Anfang je Zeile
    for zeile in quelle.splitlines(keepends=True):
        byte_versatz.append(byte_versatz[-1] + len(zeile.encode("utf-8")))
        zeichen_versatz.append(zeichen_versatz[-1] + len(zeile))
    return byte_versatz, zeichen_versatz


def _zeichen_index(quelle, versatz, zeile, spalte):
    """Rechnet eine ast-Position (Zeile, Byte-Spalte) in einen Zeichenindex um."""
    byte_versatz, zeichen_versatz = versatz  # beide Tabellen
    anfang = byte_versatz[zeile - 1]  # Byte-Anfang der Zeile
    kopf = quelle.encode("utf-8")[anfang:anfang + spalte]  # Zeilenkopf bis zur Spalte
    return zeichen_versatz[zeile - 1] + len(kopf.decode("utf-8", "replace"))


def _anzeige_knoten(baum):
    """Liefert {(id): (klasse, art)} aller Anzeige-Literale - dieselbe Messung wie die Inventur."""
    ausschluss = inventur._docstring_knoten(baum) | inventur._schluessel_knoten(baum)
    sinken = {}  # id(Knoten) -> Sink-Art
    for knoten in ast.walk(baum):
        if isinstance(knoten, ast.Call):
            for art, teile in inventur._sinken(knoten):
                for k, _text in teile:
                    sinken.setdefault(id(k), art)
    anzeige = {}  # id(Knoten) -> (Klasse, Art)
    for knoten in ast.walk(baum):
        if not isinstance(knoten, ast.Constant) or not isinstance(knoten.value, str):
            continue
        if id(knoten) in ausschluss:  # Docstring oder Schluessel
            continue
        if not re.search(r"[A-Za-z]", knoten.value):  # keine Buchstaben
            continue
        art = sinken.get(id(knoten), "ohne Sinke")  # Sink-Art oder Kennzeichen
        klasse = inventur._klasse(knoten.value, art != "ohne Sinke")  # A, B oder C
        if klasse != "C":
            anzeige[id(knoten)] = (klasse, art)
    return anzeige


def ersetzen_in_datei(dateiname, schreiben=False):
    """Ersetzt die Ersatzschreibweisen in den Anzeigetexten EINER Datei.

    Rueckgabe: Liste von (zeile, alt, neu) - je geaendertem Literal eine Zeile.
    """
    pfad = os.path.join(SRC, dateiname)  # voller Pfad
    # newline="" liest und schreibt OHNE Umwandlung: die Dateien haben teils LF, teils CRLF
    # (gemessen 03.11.2026: main.py 12.521 x LF, auftraege.py 753 x CRLF). Ohne das wuerde
    # jedes geschriebene File komplett auf LF umgestellt - ein Riesen-Diff ohne Inhalt.
    quelle = io.open(pfad, encoding="utf-8", newline="").read()
    baum = ast.parse(quelle, filename=dateiname)
    anzeige = _anzeige_knoten(baum)  # welche Literale sind Anzeige
    versatz = _zeilen_versatz(quelle)  # Byte-Versatz je Zeile
    aenderungen = []  # [(start, ende, neu, zeile, alt, neu_text)]
    for knoten in ast.walk(baum):
        if id(knoten) not in anzeige:  # kein Anzeige-Literal
            continue
        if not inventur.ERSATZ_MUSTER.search(knoten.value):  # nichts zu ersetzen
            continue
        if not hasattr(knoten, "end_lineno") or knoten.end_lineno is None:
            continue
        start = _zeichen_index(quelle, versatz, knoten.lineno, knoten.col_offset)
        ende = _zeichen_index(quelle, versatz, knoten.end_lineno, knoten.end_col_offset)
        stelle = quelle[start:ende]  # Quelltext des Literals (mit Anfuehrungszeichen)
        neu = umlaute(stelle)  # Umlaute setzen
        if neu != stelle:  # nur echte Aenderungen buchen
            aenderungen.append((start, ende, neu, knoten.lineno, stelle, neu))
    if not aenderungen:
        return []
    text = quelle
    for start, ende, neu, *_rest in sorted(aenderungen, reverse=True):  # von hinten nach vorn
        text = text[:start] + neu + text[ende:]
    text = _kopfzeile_anpassen(text)  # ASCII-Kopfzeile vertraegt keine Umlaute
    if schreiben:  # erst nach vollstaendigem Zusammenbau schreiben
        io.open(pfad, "w", encoding="utf-8", newline="").write(text)
    return [(zeile, alt, neu) for _s, _e, _n, zeile, alt, neu in sorted(aenderungen)]


def _kopfzeile_anpassen(text):
    """Stellt eine `coding: ascii`-Kopfzeile auf utf-8, sobald Anzeigetexte Umlaute tragen.

    Python liest die Kopfzeile als Kodierungserklaerung: mit `ascii` bricht der Import an
    jedem Umlaut (belegt 03.11.2026 an marsch_optik.py und voelker.py: SyntaxError
    "'ascii' codec can't decode byte 0xc3"). Daniel 03.11.2026: die ASCII-Regel gilt fuer
    Code und Kommentare, ANZEIGETEXTE sind davon ausgenommen - also utf-8 im Kopf.
    """
    if all(ord(zeichen) < 128 for zeichen in text):  # reines ASCII: nichts zu tun
        return text
    kopf_ascii = "# -*- coding: ascii -*-"
    if not text.startswith(kopf_ascii):  # andere oder keine Kopfzeile
        return text
    kopf_neu = ("# -*- coding: utf-8 -*-  # ANZEIGETEXTE tragen echte Umlaute (Schnitt T-1, "
                "Daniel 03.11.2026);\n"
                "#                          Code, Kennungen und Kommentare bleiben ASCII.\n")
    return kopf_neu + text.split("\n", 1)[1]


def alle_dateien(schreiben=False):
    """Fuehrt die Ersetzung ueber alle Dateien aus, in denen die Inventur Funde meldet."""
    ergebnis = inventur.sammle()  # Messung vorher
    betroffen = [d for d, z in ergebnis["je_datei"].items() if z["stellen"]]
    gesamt = []
    for dateiname in sorted(betroffen):  # Datei fuer Datei
        aenderungen = ersetzen_in_datei(dateiname, schreiben=schreiben)
        if aenderungen:
            gesamt.append((dateiname, aenderungen))
    return gesamt


def tabelle():
    """Zeigt die Wortkarte mit Beispielwoertern aus dem echten Bestand."""
    ergebnis = inventur.sammle()  # Messung der Fundstellen
    worte = set()  # alle betroffenen Woerter
    for _klasse, _datei, _zeile, _art, _wort, text in ergebnis["funde"]:
        for token in re.findall(r"[A-Za-z]+", text):
            if inventur.ERSATZ_MUSTER.search(token):
                worte.add(token)
    print("Wortkarte: %d Staemme, %d betroffene Woerter" % (len(WORT_KARTE), len(worte)))
    print("-" * 60)
    for wort in sorted(worte):
        neu = umlaute(wort)  # Umwandlung
        print("%-28s -> %s%s" % (wort, neu, "" if neu != wort else "   (UNVERAENDERT)"))


def main(argv):
    """Kommandozeile: --tabelle, --probe (Vorgabe) oder --schreiben."""
    eine = None  # einzelne Datei, falls --eine
    if "--eine" in argv:
        eine = argv[argv.index("--eine") + 1]
    if "--tabelle" in argv:
        tabelle()
        return 0
    schreiben = "--schreiben" in argv  # ohne Flag nur anzeigen
    if eine:
        aenderungen = ersetzen_in_datei(eine, schreiben=schreiben)
        if not aenderungen:
            print("Keine Ersatzschreibweise in Anzeigetexten:", eine)
        for zeile, alt, neu in aenderungen:
            print("%s:%s\n   alt: %s\n   neu: %s" % (eine, zeile, alt, neu))
        print("Datei %s: %d Literale %s" % (eine, len(aenderungen),
                                            "geaendert" if schreiben else "zu aendern"))
        return 0
    gesamt = alle_dateien(schreiben=schreiben)
    summe = 0  # Zahl aller Literale
    for dateiname, aenderungen in gesamt:
        summe += len(aenderungen)
        print("%-28s %3d Literale" % (dateiname, len(aenderungen)))
    print("-" * 44)
    print("%-28s %3d Literale" % ("SUMME", summe))
    print("Modus:", "GESCHRIEBEN" if schreiben else "nur angezeigt (--schreiben fehlt)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
