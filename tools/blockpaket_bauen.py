# -*- coding: utf-8 -*-
"""Baut die Paketdateien fuer das starke Modell (Blockplan B1..B8).

Aufruf:  python -X utf8 tools/blockpaket_bauen.py b1
Druckt je Paket Zeichen, Prompt-Token (Schaetzung) und USD (Schaetzung) - das ist
die Freigabegrundlage. Schreibt das Paket nach docs/auftraege/<BLOCK>_paket_<datum>.md.

Grundsaetze (Skill starke-modell-auftraege):
- Pakete werden programmatisch gebaut, nie von Hand kopiert.
- Nur Quellen dieses Themas, Ist-Zustand gemessen, festes Ausgabeformat.
- Schnitte an Eintragsgrenzen (Funktionen/Zeilenbereiche), nie mit text[:n].
"""
import json
import os
import sys
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ZIELORDNER = os.path.join(ROOT, "docs", "auftraege")
ZEICHEN_JE_TOKEN = 3.5
USD_JE_1K_PROMPT = 0.0035   # gemessen: 10 k Prompt ~ 0,035 USD auf deepseek-v4-pro


def lese(pfad, von=None, bis=None):
    voll = os.path.join(ROOT, pfad)
    with open(voll, "r", encoding="utf-8") as f:
        zeilen = f.read().splitlines()
    if von is not None:
        zeilen = zeilen[von - 1:(bis or len(zeilen))]
    return "\n".join(zeilen)


def block(pfad, von=None, bis=None, titel=None):
    """Quellenblock mit Herkunftszeile - damit das Modell zitieren kann."""
    kopf = "### Quelle: `%s`" % pfad
    if von is not None:
        kopf += " (Zeilen %d-%d)" % (von, bis)
    if titel:
        kopf += " - " + titel
    return kopf + "\n```\n" + lese(pfad, von, bis).rstrip() + "\n```\n"


def funktion(pfad, name):
    """Eine Funktion im Wortlaut (von 'def name(' bis zur naechsten Top-Level-Definition)."""
    voll = os.path.join(ROOT, pfad)
    with open(voll, "r", encoding="utf-8") as f:
        zeilen = f.read().splitlines()
    start = None
    for i, z in enumerate(zeilen):
        if z.startswith("def %s(" % name):
            start = i
            break
    if start is None:
        return "### FEHLT: `%s` in `%s`\n" % (name, pfad)
    ende = len(zeilen)
    for j in range(start + 1, len(zeilen)):
        if zeilen[j].startswith("def ") or zeilen[j].startswith("class "):
            ende = j
            break
    while ende > start and not zeilen[ende - 1].strip():
        ende -= 1
    koerper = "\n".join(zeilen[start:ende])
    return ("### Funktion `%s` aus `%s` (Zeilen %d-%d)\n```python\n%s\n```\n"
            % (name, pfad, start + 1, ende, koerper))


def jsonblock(pfad, titel=None):
    return block(pfad, titel=titel)


# Fuer grosse Datendateien: nur die Felder, die dieser Block braucht.
# Die vollstaendige Datei bleibt unter dem genannten Pfad lesbar - nichts ist verloren.
def kompakt_json(pfad, felder, eintrag="gebaeude", zusatz=()):
    voll = os.path.join(ROOT, pfad)
    with open(voll, "r", encoding="utf-8") as f:
        daten = json.load(f)
    liste = daten[eintrag] if isinstance(daten, dict) and eintrag in daten else daten
    schmal = []
    for e in liste:
        neu = {}
        for feld in felder:
            if feld in e:
                neu[feld] = e[feld]
        if "stufen" in e and "stufen" not in felder:
            neu["stufen_anzahl"] = len(e.get("stufen") or [])
        schmal.append(neu)
    kopf = ("### Quelle: `%s` (gekürzt auf die Felder %s; die vollständige Datei liegt unter "
            "diesem Pfad und darf gelesen werden)\n"
            % (pfad, ", ".join(list(felder) + ["stufen_anzahl"])))
    for k in zusatz:
        if isinstance(daten, dict) and k in daten:
            kopf += "```\n%s\n```\n" % json.dumps({k: daten[k]}, ensure_ascii=False, indent=1)
    return kopf + "```json\n" + json.dumps(schmal, ensure_ascii=False, indent=1) + "\n```\n"


def auswahl_json(pfad, felder, titel=None):
    voll = os.path.join(ROOT, pfad)
    with open(voll, "r", encoding="utf-8") as f:
        daten = json.load(f)
    schmal = {k: daten[k] for k in felder if k in daten}
    kopf = "### Quelle: `%s`" % pfad
    if titel:
        kopf += " - " + titel
    return kopf + chr(10) + "```json" + chr(10) + json.dumps(schmal, ensure_ascii=False, indent=1) + chr(10) + "```" + chr(10)


def zeichenzahl(text):
    return len(text)


# ---------------------------------------------------------------- B1

def paket_b1():
    t = []
    a = t.append

    a("""# AUFTRAG B1 - Wirtschaft messen: Erträge, Siedler, Gold, Mana, Nahrung, Dauern

Du bist **Messingenieur** für ein laufendes Python-Spiel (Remake eines Browserspiels von 2009).
Du baust **ein Messwerkzeug** und **einen Messbericht**. Du änderst **keinen** Spielcode.

## 1. Deine Rolle und deine Grenzen

| Punkt | Regel |
|---|---|
| Rolle | Messingenieur. Du rechnest mit dem vorhandenen Code und den vorhandenen Daten, du baust keine Funktionen um. |
| Erlaubt | genau zwei neue Dateien anlegen: `tools/mess_wirtschaft.py` und `docs/audits/MESS_WIRTSCHAFT_20261101.md`. Lesen darfst du alles. |
| Verboten | `src/` anfassen, `data/*.json` ändern, `docs/PRUEFREGEL_ORIGINAL.md` / `docs/ENTWICKLUNGSPROTOKOLL.md` / `docs/AKTUELLER_STAND.md` schreiben, `git add/commit/push`, Dateien außerhalb des Projekts, Kennungen umbenennen, Zahlen schätzen oder erfinden. |
| Sprache | Deutsch, Tabellen, keine Emojis. |
| Kodierung | `tools/mess_wirtschaft.py` ist **reines ASCII** (`# -*- coding: utf-8 -*-` ist erlaubt, aber kein Umlaut im Code/String). Der Bericht `.md` darf Umlaute haben, aber **deutsche Anführungszeichen paarig** „…“ - ein einzelnes gerades `"` als Schluss macht die Textprüfung rot. |
| Rechenart | `python -X utf8` (Windows, Arbeitsverzeichnis = Projektwurzel). Kein GUI-Import, kein Tk, kein Fenster. |

## 2. Delegieren ist erlaubt (Vorgabe Daniel, 01.11.2026)

Wörtlich: „und das große model soll ruhig auch delegieren dürfen und eigene kleine agenten nutzen von sich selbst solange der laptop dadurch nicht abstürzt“.

| Punkt | Regel |
|---|---|
| Erlaubt | eigene kleine Unteragenten starten (`hermes -z "…" -m <kleines Modell> --yolo`, ohne `--usage-file`-Pflicht) für klar abgegrenzte Teilarbeiten: Quellen auszählen, Tabellen ziehen, eine Zahl gegenprüfen, Textstellen suchen |
| Grenze | **höchstens zwei** Unteragenten gleichzeitig, **kein** Unteragent schreibt in `src/` oder `data/`; schreibende Arbeit (die zwei Ausgabedateien) machst **du** |
| Maschine | der Laptop ist schwach: **nie** zwei schwere Läufe gleichzeitig, **nie** ein Sammellauf parallel zu einem Unteragenten, kein EXE-Bau, kein Fensterstart. Vor einem Sammellauf alle Kinder beendet |
| Kosten | jeder Unteragent kostet echte Anfragen. Der Blockrahmen ist **0,35-0,45 USD** - Delegation darf ihn nicht überschreiten. Im Bericht (Abschnitt A) steht, wie viele Unteragenten du gestartet hast und wofür |
| Ergebnis | was ein Unteragent liefert, ist ein Entwurf: jede Zahl, die in deinen Bericht wandert, prüfst du selbst nach |

Wenn du allein schneller bist als mit Kindern: allein arbeiten. Delegation ist eine Erlaubnis, keine Pflicht.

## 3. Code-Kommentare (Vorgabe Daniel, 01.11.2026 - gilt für allen neuen Code)

Wörtlich: „code im spiel vorallem wenn er ins github online repo hochgeladen wird mal unbedingt hinter der codezeile jeweils ausgeklammert kurz erklärt sein damit man zu jeder zeile grob weiß was sie tut und die aufgabe von bestimmten code blöcken rein informativ mit im code stehen. das bringt maximale Nachvollziehbarkeit.“

| Punkt | Regel |
|---|---|
| Je Zeile | **hinter jeder Codezeile** ein kurzer Kommentar (Python: zwei Leerzeichen, dann `#`), der sagt, was die Zeile tut - in einfachem Deutsch, ohne Fachjargon |
| Je Block | über jeder Funktion und jedem logischen Absatz ein Kommentar, der die **Aufgabe des Blocks** erklärt (was hinein, was heraus, warum) |
| Kurz halten | je Zeile höchstens eine knappe Halbzeile; der Kommentar erklärt die Absicht, nicht die Syntax („zaehlt die Siedler je Dorf“, nicht „Schleife ueber die Liste“) |
| Nicht schwindeln | ein Kommentar beschreibt, was die Zeile WIRKLICH tut - kein Kommentar, der etwas anderes behauptet als der Code (das ist schlimmer als kein Kommentar) |
| ASCII | in `.py`-Dateien bleibt der Kommentar ASCII (`ae/oe/ue/ss`), Anzeigetexte ausgenommen |

## 4. Die Vorgabe (wörtlich, von Daniel, 01.11.2026)

> „ich will das du ein rießen arbeitspaket für das schwere starke model von deepseek vorbereitest das für uns sehr sehr viel Balancen Abgleichen und Spieltesten und bewerten soll und lass es große teile der offenen aufgaben übernehmen und am besten auch umsetzen.“

Blockziel B1 aus dem Blockplan: **ein wiederverwendbares Messwerkzeug `tools/mess_wirtschaft.py`, das die Wirtschaft des Spiels aus Daten und Kernfunktionen rechnet und einen Bericht schreibt.** Kein Umbau am Spiel.

## 5 Was das Werkzeug messen MUSS

Jede Kennzahl mit **einer gedruckten Zeile**: Kennzahl, Wert, Quelle (Datei:Zeile oder Datenfeld).

1. **Erträge je Gebäude und Gelände** - gelesen aus `data/buildings.json` (`ertrag_pro_stunde`), gegengehalten gegen die Handbuchtafel (Abschnitt 6 unten). Auch die Gebäude **ohne** Ertrag (Werkstätten, Ausbildungsstätten, Wall, Bibliothek, Haus, Dorfzentrum) sind zu nennen, mit dem Vermerk „kein Ertrag“.
2. **Reichsertrag je Spielstunde und je Spieltag** aus einer **nachvollziehbaren Beispielbelegung**: ein Dorf mit 10x10 Feldern, je Feld ein Gebäude, Geländeverteilung aus `data/gelaende.json` (Gewichte) - und zusätzlich der Fall „bester Fall“ (jedes Gebäude auf seinem besten Gelände) und „schlechtester Fall“ (nur zweitbestes Gelände). Rechne die drei Fälle als Spannweite, nicht als eine Zahl.
3. **Siedlerzuwachs und Siedlerdecke**: 1 Siedler/Stunde je Siedlung, Grenze 10 + 5 je Haus, sechs Dörfer. Nutze die vorhandene Rechenstelle (`gebaeude_wirkung.siedlergrenze_je_siedlung`, `bevoelkerungsgrenze`, `siedler_zuwachs_pro_stunde`), nicht eine eigene Formel.
4. **Goldfluss je Spieltag**: aus Goldmine (Berg/Hügel) - und was dagegen an Gold abfließt, soweit es aus Daten belegbar ist (Reisekosten, Baukosten in Gold). Wenn nichts belegbar ist: „nicht belegbar“ schreiben, nicht raten.
5. **Mana je Spielstunde**: Tempel auf Nebelsee 5, sonst 1, auf Sumpf 0, Götterkunde +5 % je Stufe (so steht es im Register, siehe Abschnitt 6). Rechne die Varianten einzeln.
6. **Nahrungsverbrauch**: 8 je Einheit und Spieltag (laufend), Reisekosten je Feld getrennt; nutze `spieloekonomie.tagesbedarf_nahrung` und `verbrauch_pro_stunde`.
7. **Waren- und Ausbildungsdauern**: Dauer je Ware aus den Rezeptdaten, Dauer je Einheit aus `spieloekonomie.ausbildung_start` (Grunddauer geteilt durch Stufenfaktor), Warteschlangen-Effekt bei mehreren Werkstätten.
8. **Verhältniskennzahlen** (daraus entsteht der Balance-Wert): Ertrag je Siedler, Siedler je Gebäude, Zeit bis zur ersten Siedlung, Zeit bis 100 Einheiten, Verbrauchsanteil der Nahrung am Tagesertrag bei 100 und bei 360 Einheiten.

## 6 Ist-Zustand (gemessen am 01.11.2026, Kopf `52604ea`)

| Gegenstand | Wert |
|---|---|
| Projekt | `D:\\Arbeiten\\Nebelseetal_Remake`, Branch `main`, Arbeitsbaum leer |
| Python | `python -X utf8`, Arbeitsverzeichnis = Projektwurzel; zusätzliche Pakete sind vorhanden, aber nicht nötig |
| Datenordner | `data/` mit 22 Dateien (u. a. `buildings.json`, `units.json`, `gelaende.json`, `gebaeude_wirkung.json`, `nahrungsverbrauch.json`, `spielzeit.json`, `bausiedler.json`, `baupreise.json`, `warenrezepte.json`) |
| Spieluhr | `data/spielzeit.json`: Faktor 180 Spielsekunden je Echtzeitsekunde, umschaltbar 1/20/60/180/600 |
| Vorhandene Messwerkzeuge | `tools/balancing_messung.py` (Erträge, Einheitenkosten, Schlachten, Beute) und `tools/balancing_karten.py` (127 Originalkarten, Gründungs- und Ausbaubedarf) - **lies sie zuerst**, damit du nichts doppelt baust |
| Prüflauf | `python -X utf8 -u tools/sammellauf.py` fährt 117 Prüfdateien (rund 300-650 s). Läuft am Ende Pflicht. |

**Wichtig:** In `tools/balancing_messung.py` stehen schon Funktionen für Erträge (`ertrag_je_stunde`, `feld_statistik`, `ausbau_je_siedlung`, `siedlergrenze`). Dein Werkzeug darf diese importieren oder nachbauen - aber die Zahlen müssen übereinstimmen; eine Abweichung ist ein Befund und gehört in den Bericht.

## 7 Quellen im Wortlaut
""")

    a(block("docs/original/Spielanleitung_2009_Textfassung.txt", 336, 391,
            "Handbuch 2009, Seite 10 und 11: Rohstoffproduktion, Gebäude, Siedlerzuwachs, Sumpf unbebaubar"))
    a("""
**Achtung, genau hier liegt der Prüfwert:** Das Handbuch nennt die **Rinderfarm** auf Grasland mit
„3 Nahrung, 3 Leder“ und auf Steppe mit „1,5 Nahrung, 1,5 Leder“. In `data/buildings.json` steht für die
Rinderfarm etwas anderes (siehe Abschnitt 8). Das ist **kein** Schreibfehler im Paket, sondern genau die
Abweichung, die du finden und benennen sollst - mit Urteil, nicht geglättet.
""")

    a(block("docs/original/Spielanleitung_2009_Textfassung.txt", 1185, 1196,
            "Handbuch 2009, Seite 20: Auftragskosten - Gold, Nahrung, Mana und Geschwindigkeit"))

    a("""
## 8 Was das Register bereits entschieden hat (nicht neu verhandeln, aber prüfen)

| Regel | Inhalt | Stand |
|---|---|---|
| Register 56 | **Mana: 5/1 gilt** (Tempel Nebelsee 5, sonst 1). Die Produktion liest ausschließlich `data/buildings.json`; die älteren 8/2 sind verworfen. | behoben 31.10.2026 |
| Register 69 | **Nahrungsverbrauch 8 je Einheit und Spieltag** (= 1/3 je Spielstunde), EINE Rechenstelle `spieloekonomie.tagesbedarf_nahrung`; keine Strafe bei Unterdeckung | gebaut 31.10.2026 |
| Register 70 | **Nahrungsnot sperrt die Produktion im Ort** (kein Bauen, keine Waren, keine Ausbildung, solange die Garnison mehr verbraucht als der Ort erntet) | gebaut |
| Register 71 | Kartengröße: 127 Originalkarten, Ausbaubedarf 1.099-2.293 Holz / 692-1.539 Stein; „Gold 886 / 1.318 / 1.685 je Tag“ als Spannweite | gemessen 31.10.2026 |
| Register 73 | **Wagenbau hebt die Karrenladung** um 10 % je Stufe (Höchststufe 10 = Faktor 2,0); Basiswerte 40/100/250/1.000/2.500 bleiben | gebaut |
| Register 86 | Jede Gründung bringt **drei Startgebäude** (Tempel, Holzfäller, Steinmetz) kostenlos mit; Startressourcen 10 Siedler / 100 Holz / 100 Stein | gebaut 01.11.2026 |
| Register 90 | Das **Dorfzentrum** kommt kostenlos mit der Gründung, den Platz setzt der Spieler | gebaut 01.11.2026 |

## 9 Daten im Wortlaut (das ist die Rechengrundlage)
""")

    a(kompakt_json("data/buildings.json",
                   ["id", "name", "kategorie", "rohstoff", "ertrag_pro_stunde", "nur_auf",
                    "max_je_siedlung", "abweichung", "anmerkung", "voraussetzung"],
                   zusatz=("regeln", "_gelaenderegeln_vorschlag")))
    a(jsonblock("data/gebaeude_wirkung.json", "Wirkungen: Siedlergrenze, Siedlerzuwachs, Bibliothek, Ausbildungsstätten, Wall"))
    a(jsonblock("data/nahrungsverbrauch.json", "Nahrungsverbrauch und Schalter"))
    a(auswahl_json("data/spieloekonomie.json",
                   ["version", "baukunst_mindeststufe", "gruendung", "vergabe_stunden",
                    "versorgung_stunden", "mindestsiedlungen", "plan",
                    "pilot_ausbildung_minuten", "pilot_waren_minuten", "_hinweis"],
                   titel="Regeln der Wirtschaft (Auszug: die Felder, die dieser Block braucht; "
                         "die vollständige Datei liegt unter diesem Pfad und darf gelesen werden)"))
    a(jsonblock("data/bausiedler.json", "Siedlerbedarf je Gebäude"))
    a(jsonblock("data/spielzeit.json", "Spieluhr"))

    a("""
## 10 Die Rechenstellen im Wortlaut (lies sie, statt eigene Formeln zu erfinden)
""")
    a(funktion("src/spieloekonomie.py", "tagesbedarf_nahrung"))
    a(funktion("src/spieloekonomie.py", "verbrauch_pro_stunde"))
    a(funktion("src/spieloekonomie.py", "ort_tick"))
    a(funktion("src/spieloekonomie.py", "ausbildung_start"))
    a(funktion("src/gebaeude_wirkung.py", "siedlergrenze_je_siedlung"))
    a(funktion("src/gebaeude_wirkung.py", "siedler_zuwachs_pro_stunde"))

    a("""
Konstanten in `src/spieloekonomie.py`, die du brauchst (Zeilen 47-70, im Wortlaut):

```python
""")
    a(lese("src/spieloekonomie.py", 40, 72))
    a("""
```

## 11 Rechenpflicht (das ist der Wert dieses Blockes)

1. **Jede Kernzahl selbst rechnen**, nicht abschreiben: was du im Bericht behauptest, muss eine Zeile im Werkzeug erzeugen, und du führst das Werkzeug aus.
2. **Jede Abweichung zwischen `data/` und Handbuch benennen** - mit Quelle (Handbuchzeile) und Urteil: `BELEGT` / `WIDERSPRUCH` / `NICHT BELEGT` / `VORSCHLAG`.
3. **Nichts glätten.** Ein Ausreißer bleibt stehen und wird erklärt. Wenn zwei Quellen sich widersprechen, nenne beide Zahlen und sage, welche gilt und warum.
4. **Keine Zahl erfinden.** Was nicht messbar ist, wird als „nicht messbar“ mit Grund geführt - niemals geschätzt.
5. **Das Werkzeug muss laufen**: `python -X utf8 tools/mess_wirtschaft.py` endet mit Rückgabewert 0 und druckt je Kennzahl eine Zeile. Es schreibt seine Ausgabe zusätzlich als Text in den Bericht? Nein - du führst es aus und **kopierst die gedruckten Zeilen** in den Bericht (Abschnitt B).

## 12 Ausgabeformat (verbindlich)

**Datei 1: `tools/mess_wirtschaft.py`** - ASCII, höchstens 500 Zeilen, eine `main()`, Ausgabe über `print`, Rückgabewert 0. Jede gedruckte Zeile in der Form:
`<Kennzahl> | <Wert> | <Quelle>`.

**Datei 2: `docs/audits/MESS_WIRTSCHAFT_20261101.md`** - höchstens 400 Zeilen, genau diese Gliederung:

| Abschnitt | Inhalt |
|---|---|
| A. Kopf | Datum, Kopf-Commit `52604ea`, welche Dateien du angelegt hast, wie das Werkzeug aufgerufen wird |
| B. Die gedruckten Zeilen | die vollständige Ausgabe des Werkzeugs im Codeblock (ungekürzt) |
| C. Erträge je Gebäude und Gelände | Tabelle: Gebäude, Gelände, Handbuchwert, Datenwert, Urteil |
| D. Reichsertrag je Stunde und Tag | drei Fälle (beste / Beispiel / schlechteste Belegung) mit Rechenweg in einer Zeile je Fall |
| E. Siedler | Zuwachs, Grenze je Dorf, Reichsdeckel, Zeit bis zur vollen Siedlung |
| F. Gold und Mana | Goldfluss je Tag, Mana je Stunde je Gelände, Götterkunde-Wirkung |
| G. Nahrung | Verbrauch je Einheit/Tag, Anteil am Tagesertrag bei 100 und 360 Einheiten, Reisekosten je Feld |
| H. Dauern | Warendauern, Ausbildungsdauern je Stufe, Warteschlangen-Effekt |
| I. Die drei wichtigsten Kernaussagen | drei Sätze, je mit Zahl und Quelle |
| J. Jede Abweichung | Liste aller Widersprüche `data/` gegen Handbuch, je mit Handbuchzeile, Datenwert, Urteil und Vorschlag |
| K. Was nicht messbar ist | was du nicht messen konntest und warum (kein Raten) |
| L. Vorschläge | höchstens fünf, je mit Zahl, Wirkung und Aufwand S/M/L - ausdrücklich als VORSCHLAG gekennzeichnet |

## 13 Abschluss (Pflicht)

1. `python -X utf8 tools/mess_wirtschaft.py` ausführen, Ausgabe kopieren.
2. `python -X utf8 -u tools/sammellauf.py` ausführen (dauert mehrere Minuten) und das Ergebnis in Abschnitt B als eine Zeile anhängen: Dateien, grün, rot, ausgesetzt, Prüfungen, Sekunden. Wird der Sammellauf rot, ist das ein Befund über die Umgebung, kein Grund zu basteln: Ergebnis ehrlich hinschreiben.
3. Letzte Zeile deiner Antwort (nicht des Berichts): `FERTIG <Pfad des Berichts> <Zeilenzahl>`.
""")

    return "".join(t)


# ---------------------------------------------------------------- C1 (Chat-Abo, kein Guthaben)

def paket_c1():
    t = []
    a = t.append
    a("""# AUFTRAG C1 - Demo-Begleittexte fuer "Nebelseetal Remake"

Du bist **Autor und Redakteur** fuer die Texte, die eine Spiel-Demo begleiten: Spielerhandbuch, FAQ,
README, Projektseite, bekannte Grenzen. Du hast **keinen** Zugriff auf den Code und kein Terminal -
deshalb steht in diesem Auftrag jeder Fakt, den du verwenden darfst, als Tabelle. Was hier nicht steht,
ist fuer dich **UNBEKANNT** und wird als solches gekennzeichnet, nicht erfunden.

## 1. Deine Rolle und die harten Regeln

| Punkt | Regel |
|---|---|
| Rolle | Autor. Du schreibst Spielertexte, keine Spielregeln. **Du erfindest keine Zahl, keine Mechanik, keinen Spielinhalt.** |
| Belegpflicht | Hinter jeder inhaltlichen Aussage steht eine Kennzeichnung: `[BELEGT: Register 91]`, `[NICHT GEBAUT]` oder `[UNBEKANNT - von Hermes zu liefern]`. Eine Aussage ohne Kennzeichnung gilt als Fehler. |
| Verboten | Neue Funktionen versprechen, Zahlen schaetzen, "bald verfuegbar" ohne Beschluss, Werbesprache, Emojis, den Vorgaenger nicht abwerten |
| Sprache | Deutsch, klare kurze Saetze, Tabellen wo sie helfen, du-Form wie im Original-Handbuch. Keine Emojis. |
| Ton | Freundlich und sachlich. Der Leser ist ein erwachsener Spieler. Ein Testspiel wird als Testspiel benannt, ohne Untertreibung und ohne Uebertreibung. |
| Umfang | 350-600 Zeilen im Ergebnis. Lieber vollstaendig als knapp. |

## 2. Was gebaut werden soll (Vorgabe Daniel, 01.11.2026)

Vier Textstuecke, die zusammen vor einer Demo-Veroeffentlichung fertig sein muessen:

| Teil | Was es ist | Zielgruppe |
|---|---|---|
| **A. Spielerhandbuch** | das Handbuch fuer einen neuen Spieler: was das Spiel ist, wie eine Partie ablaeuft, welche Gebaeude/Einheiten/Forschungen es gibt, wie Kampf und Handel funktionieren, was die Demo nicht kann | neuer Spieler |
| **B. FAQ** | 15-25 echte Fragen mit kurzen Antworten, darunter die unangenehmen: "Ist das eine Kopie?", "Warum sieht es alt aus?", "Was ist noch nicht fertig?", "Wo sind meine Spielstaende?" | neugieriger Interessent |
| **C. README / Projektseite** | technische Kurzfassung: was das Programm ist, wie man es startet, Systemvoraussetzungen, wo die Spielstaende liegen, wie man Fehler meldet, Stand und Grenzen | GitHub-Besucher |
| **D. Bekannte Grenzen** | ehrliche Liste dessen, was fehlt oder unfertig ist - nach Schwere, mit "was Sie stattdessen tun koennen" | beide |

## 3. Der Stand, den du beschreiben darfst (gemessen am 01.11.2026, Kopf `52604ea`)

Das Spiel ist ein **Remake eines Browserspiels von 2009**, Einzelspieler gegen Computergegner (Bots),
Python mit Fensteroberflaeche, laeuft offline auf Windows, portabel ohne Installation.

### 3a. Was gebaut und geprueft ist - das darfst du beschreiben

| Funktion | Stand | Beleg |
|---|---|---|
| Gruendung einer Siedlung auf einer 10x10-Karte | gebaut, geprueft | Register 86 |
| Drei Startgebaeude bei der Gruendung: Tempel, Holzfäller, Steinmetz, kostenlos | gebaut, geprueft | Register 86 |
| Startressourcen 10 Siedler, 100 Holz, 100 Stein | gebaut, geprueft | Register 86 |
| Dorfzentrum: kommt kostenlos mit der Gruendung, den Platz setzt der Spieler selbst | gebaut, geprueft | Register 89, 90 |
| Sechs Doerfer je Partie, Siedlergrenze 10 je Dorf, +5 je Haus | gebaut | Register 86, Handbuch S. 11 |
| 20 Gebaeude mit Ertraegen je Gelaendeart, Sumpf unbebaubar | gebaut | `data/buildings.json`, Handbuch S. 10-11 |
| Warenproduktion in Werkstaetten (Schmiede, Bogenbauer, Naehstube) mit Warteschlange | gebaut, geprueft | Register 60, 68 |
| 21 Forschungen, Bibliothek noetig, Verbund: bezahlt im Dorf, gilt reichsweit | gebaut | `data/research.json`, `forschungspfad.py` |
| Ausbildung von Einheiten, Dauer abhaengig von der Gebaeudestufe (20 Minuten Grunddauer je Stufe) | gebaut, geprueft | Register 53 |
| Kampf mit Wallstufen, Schlagkraft-Schwellen, Beute nach Karrenladung | gebaut, geprueft | Register 54, 62 |
| Auftraege: Transport, Handel, Angriff, Spionage; Reisezeit, Rueckweg gleich lang | gebaut, geprueft | Register 63, 84 |
| Sechs Weltkarten mit Gelaende (sieben Gelaendearten in 2x2-Bloecken, fester Seed) | gebaut, geprueft | Register 91 |
| Weltensprung zwischen Weltkarten (Portal) | gebaut; **Preis wird auf 500 Mana + 100 Gold umgestellt** | Register 93 |
| Bots mit eigener Wirtschaft, Punkten und Wall | gebaut, aber **Verhalten noch grob** | Register 72 |
| Speichern/Laden in drei Slots | gebaut, geprueft | `src/spielstaende.py` |
| Kein Sieg mehr: Niederlage oder Weiter, Bewertung ueber Auszeichnungen (Feldherr, Forscher, Haendler, Gesamtherrscher) | gebaut, geprueft | Register 50, 59 |
| Demo liefert **leer** aus: kein Spielstand im Paket, eigener Speicherordner | gebaut, geprueft | Register 101 |

### 3b. Was ausdruecklich NICHT gebaut ist - das darfst du NICHT als vorhanden beschreiben

| Fehlt | Was das fuer den Text heisst |
|---|---|
| Einheiten zwischen eigenen Doerfern verlegen (S-4) | nicht erwaehnen oder als "in Arbeit" fuehren |
| Ein ganzes Dorf auf eine andere Weltkarte transferieren (S-6) | dito |
| Bots mit erkennbarem Verhalten/Taktiken (S-7) | Bots nur als "Gegner mit eigener Wirtschaft" beschreiben, keine Taktikversprechen |
| Forschungsverbund-Sperren (S-3: Abriss der Bibliothek bei laufender Forschung) | nicht erwaehnen |
| Bilanz/Preisumstellung des Weltensprungs (S-8) | Preis **nicht** nennen - er ist noch nicht im Spiel |
| Handbuch als eigene Datei | **das ist dein Auftrag** |

## 4. Daniels Entscheidungen, die die Texte binden

| Nr. | Entscheidung |
|---|---|
| 93 | Weltensprung kostet kuenftig **500 Mana + 100 Gold** (Originalwert 5.000 bleibt als Beleg im Code) - **im Text noch nicht nennen** |
| 95 | Das Wort **"Demo"** steht im Titel und in der Versionsbezeichnung, damit der Umfang sofort erkennbar ist |
| 96 | Das Handbuch erscheint **erst nach dem fertigen Weltbild** - das ist erledigt, du kannst schreiben |
| 97 | Das Handbuch ist eine **eigene Datei** neben dem Release, nicht nur innerhalb einer Webseite und nicht als Ansicht im Spiel |
| 98 | **"Limbus"** bleibt Weltname; die magische Ebene heisst im Text **"der magische Limbus"** |
| 99 | Die Demo ist ein **moeglichst weit umgesetztes Testspiel**, kein minimaler Auszug. Funktionen gehen vor Release-Texten. |
| 101 | Die Demo wird **leer** ausgeliefert: kein vorhandener Spielstand im Paket |

## 5. Die sieben Fehler des Vorgaenger-Textpakets - korrigiere sie, wiederhole sie nicht

Diese Liste ist ein Pruefvermerk ueber einen frueheren Textentwurf. Jeder Punkt ist am Code nachgemessen.
**Deine Texte duerfen keinen dieser Fehler wiederholen.**

""")
    a(block("docs/audits/PRUEFVERMERK_GPT_TEXTPAKET_20261101.md", 47, 135,
            "Pruefvermerk: die sieben Widersprueche und was der alte Text ausliess"))
    a("""
## 6. Die Freigabe-Gates - G-06 betrifft genau deine Texte

Vor einem Upload prueft der Verantwortliche sieben Gates. Gate G-06 lautet: **"README, Release-Notizen,
bekannte Grenzen, Startanleitung und Build widersprechen sich nicht."** Deine vier Texte muessen also
untereinander und mit den Zahlen aus Abschnitt 3 uebereinstimmen: gleiche Zahl, gleiche Schreibweise,
gleicher Name, ueberall.

""")
    a(block("docs/EXTERNES_FEEDBACK_GITHUB_20261101.md", 33, 52,
            "die sieben Freigabe-Gates im Wortlaut"))
    a("""
## 7. Originalzitate (damit deine Texte keine erfundenen Regeln behaupten)

""")
    a(block("docs/original/Spielanleitung_2009_Textfassung.txt", 336, 391,
            "Handbuch 2009, Seite 10-11: Ertraege je Gebaeude und Gelaende, Siedlergrenze, Sumpf unbebaubar"))
    a(block("docs/original/Spielanleitung_2009_Textfassung.txt", 393, 405,
            "Handbuch 2009, Seite 12: Bibliothek und Forschung"))
    a(block("docs/original/Spielanleitung_2009_Textfassung.txt", 1203, 1220,
            "Handbuch 2009, Seite 21: Wall, Schlagkraft, Rueckzug"))
    a("""
## 8. Ausgabeformat (verbindlich)

**Genau eine Datei**: `DEMO_TEXTE_20261101.md`, mit diesen Teilen in dieser Reihenfolge:

| Teil | Inhalt | Zeilen (Richtwert) |
|---|---|---|
| Kopf | was dieses Dokument ist, fuer welchen Stand es gilt, wie es zu pflegen ist | 15 |
| **A. Spielerhandbuch** | gegliedert H-01 bis H-17: Das Spiel - Start und Ziel - Die Siedlung - Gebaeude - Rohstoffe - Siedler - Forschung - Werkstaetten und Waren - Einheiten - Ausbildung - Auftraege und Reisen - Kampf - Weltkarten und Weltensprung - Punkte und Auszeichnungen - Bots - Speichern und Laden - Tastatur und Maus | 200-280 |
| **B. FAQ** | 15-25 Fragen, je Frage 2-5 Saetze Antwort, die unangenehmen Fragen zuerst | 60-90 |
| **C. README / Projektseite** | Kurzbeschreibung, Voraussetzungen, Start, Spielstaende, Fehler melden, Stand, Grenzen, Herkunft und Rechtshinweis | 60-100 |
| **D. Bekannte Grenzen** | Tabelle: Grenze - Wirkung fuer den Spieler - Ausweg heute - geplant (mit Register, falls belegt) | 30-50 |
| **E. Was ich nicht wissen kann** | jede Angabe, die du gebraucht haettest und die im Auftrag fehlt - als Liste, damit nichts geraten wird | 10-20 |

## 9. Abschluss

Letzte Zeile deiner Antwort: `FERTIG DEMO_TEXTE_20261101.md <Zeilenzahl>`.
Wenn du eine Angabe brauchst, die in diesem Auftrag nicht steht: **nicht raten**, sondern in Teil E
als `[UNBEKANNT - von Hermes zu liefern]` fuehren und den Satz nennen, in dem sie fehlt.
""")
    return "".join(t)


# ---------------------------------------------------------------- B2

def paket_b2():
    t = []
    a = t.append
    a("""# AUFTRAG B2 - Kampf messen: Wall, Schlagkraft, Beute, Ladung, Reisekosten

Du bist **Messingenieur** fuer den Kampf eines laufenden Python-Spiels. Du baust **ein Messwerkzeug**
und **einen Messbericht**. Du aenderst **keinen** Spielcode.

## 1. Rolle und Grenzen

| Punkt | Regel |
|---|---|
| Rolle | Messingenieur. Du rechnest mit den vorhandenen Kampffunktionen, du baust keine neue Kampfregel. |
| Erlaubt | genau zwei neue Dateien: `tools/mess_kampf.py` und `docs/audits/MESS_KAMPF_20261101.md`. Lesen darfst du alles. |
| Verboten | `src/` anfassen, `data/*.json` aendern, `docs/PRUEFREGEL_ORIGINAL.md` / `docs/ENTWICKLUNGSPROTOKOLL.md` / `docs/AKTUELLER_STAND.md` schreiben, `git add/commit/push`, Zahlen schaetzen oder erfinden |
| Delegation | erlaubt (hoechstens zwei Unteragenten gleichzeitig, keiner schreibt in `src/` oder `data/`); im Bericht nennen, wie viele und wofuer |
| Maschine | der Laptop ist schwach: nie zwei schwere Laeufe gleichzeitig, kein EXE-Bau, kein Fensterstart, kein Sammellauf parallel zu einem Unteragenten |
| Code-Kommentare | hinter jeder Codezeile ein kurzer Kommentar (zwei Leerzeichen, `#`), je Funktion eine Zeile zur Aufgabe; `.py` bleibt ASCII (`ae/oe/ue/ss`) |
| Sprache | Deutsch, Tabellen, keine Emojis; Bericht mit paarigen deutschen Anfuehrungszeichen |

## 2. Blockziel (aus dem Blockplan, woertlich)

> **B2 - Kampf messen (kein Umbau am Spiel):** `tools/mess_kampf.py` - echte Schlachten ueber
> `kampf.fuehre_schlacht`, 40 Laeufe je Wallstufe, Beute ueber `kampfbericht.beute_am_ziel`,
> Reisekosten ueber die vorhandene Wegzeitfunktion.
> **Muss messen:** Trefferquote/Verluste je Wallstufe 0...10, Schwellenverhalten (die Wallpruefung
> rechnet mit **SK**, nicht mit AT - Register 54), Beute-Staffel 10/30/60/100 % **gegen die
> mitnehmbare Menge**, Ladungsdeckel je Karrenart (40/100/250/1.000/2.500, Wagenbau-Bonus +10 %/Stufe,
> Deckel Faktor 2,0).
> **Abnahme:** 40 Laeufe je Stufe sind im Bericht als Tabelle sichtbar; auffaellige Ausreisser werden
> benannt, nicht geglaettet.

## 3. Ist-Zustand (gemessen 01.11.2026, Kopf `52604ea`)

| Gegenstand | Wert |
|---|---|
| `src/kampf.py` | 18.234 Byte, `fuehre_schlacht(angreifer, verteidiger, ...)` ab Zeile 162, Selbstauskunft `vorschlaege()` ab Zeile 357 |
| `src/kampfbericht.py` | 20.935 Byte: `vorrunde` (Z. 65), `mauer_schaden` (Z. 147), `beute_lage` (Z. 205), `beute_staffel` (Z. 227), `beute_am_ziel` (Z. 280), `beute` (Z. 315), `bericht` (Z. 359) |
| `src/einheiten.py` | 11.038 Byte: `angriff` (AT), `verteidigung`, `leben`, `schlagkraft` (SK), `ladung`, `kapazitaet`, `ladung_der_gruppe(bestand, forschung)` |
| Vorhandenes Messwerkzeug | `tools/balancing_messung.py` enthaelt `kampf_probe(angreifer, verteidiger, wall, zustand, vorraete, laeufe=40)` - **lies es zuerst**; dein Werkzeug darf es nutzen oder nachbauen, die Zahlen muessen aber zueinander passen (Abweichung = Befund) |
| Pruefstand | `python -X utf8 -u tools/sammellauf.py`, 117 Dateien, kalt rund 700 s. Laeuft am Ende Pflicht. |

**Wichtig fuer die Messung:** Kaempfe sind **zufaellig** (Wuerfel). Eine einzelne Schlacht sagt nichts.
Deshalb 40 Laeufe je Stufe mit festem, im Bericht genanntem Startwert des Zufallsgenerators
(`random.Random(seed)`), damit die Messung wiederholbar ist. Streuung berichten (Minimum, Median,
Maximum, Anteil Siege), nicht nur einen Mittelwert.

## 4. Registerpunkte, die den Kampf binden (nicht neu verhandeln, aber pruefen)

| Nr. | Inhalt |
|---|---|
| 54 | **Die Wallvorrunde rechnet mit SK (Schlagkraft), nicht mit AT** - der alte Fehler liess fast jeden Trupp bestehen. Behoben 31.10.2026 |
| 58 | **Die Wallpruefung beim Auftrag WARNT, sie lehnt nicht mehr ab**; entschieden wird bei Ankunft |
| 62 | **Beute am Kartenfeld wird nicht gewuerfelt**: `kampfbericht.beute_am_ziel` rechnet mit Karrenladung, Vorrat und bucht am Feld ab. Kampf und Verluste auf einem Marsch entfallen ganz |
| 67 | **EIN Einsatzweg**: Ortsheer ist die Quelle, der Auftrag traegt seine `quelle_id`, ein Kampf (`kampf.fuehre_schlacht`), Beute ins Ortslager |
| 73 | **Wagenbau hebt die Karrenladung** +10 % je Stufe, Hoechststufe 10 = Faktor 2,0; Basiswerte 40/100/250/1.000/2.500 bleiben |
| 84 | **Jeder Angriff reist** - der Sofortpfad ist stillgelegt; gekaempft wird bei Ankunft, gebucht wird die Heimkehr |
| 52 | Erfundene Kampfwerte sind als **VORSCHLAG** gefuehrt: Mauermalus 5 %/Stufe, Turmschutz als Stueckzahl (10/30), Rueckzug mit `ceil`, Kampfwert-Spannen, Beutestaffel |

## 5. Quellen im Wortlaut

""")
    a(block("docs/original/Spielanleitung_2009_Textfassung.txt", 1200, 1235,
            "Handbuch 2009, Seite 21: Wall, Schlagkraft-Schwellen, Rueckzug"))
    a(block("docs/original/Spielanleitung_2009_Textfassung.txt", 1235, 1272,
            "Handbuch 2009, Seite 21/22: Mauerzustand in Prozent, Belagerungswaffen, Kampfsequenzen"))
    a("""
## 6. Die Kampffunktionen im Wortlaut (das ist der Messgegenstand)

""")
    a(funktion("src/kampf.py", "fuehre_schlacht"))
    a(funktion("src/kampf.py", "vorschlaege"))
    a(funktion("src/kampfbericht.py", "vorrunde"))
    a(funktion("src/kampfbericht.py", "beute_staffel"))
    a(funktion("src/kampfbericht.py", "beute_am_ziel"))
    a(funktion("src/kampfbericht.py", "mauer_schaden"))
    a(funktion("src/einheiten.py", "schlagkraft"))
    a(funktion("src/einheiten.py", "angriff"))
    a(funktion("src/einheiten.py", "ladung_der_gruppe"))
    a("""
## 7. Daten im Wortlaut

""")
    a(kompakt_json("data/units.json", ["kategorie", "kosten", "kriegspunkte", "werte", "ladung"],
                   eintrag="einheiten"))
    a(jsonblock("data/karrenkapazitaet.json", "Wagenbau-Bonus, Schalter und Deckel"))
    a(kompakt_json("data/buildings.json", ["id", "name", "kategorie", "stufen"],
                   zusatz=("regeln",)))
    a("""
## 8. Was das Werkzeug messen MUSS

1. **Wallstufen 0 bis 10, je 40 Laeufe** mit derselben Angreiferaufstellung und derselben
   Verteidigeraufstellung: Tabelle mit Stufe, Anteil bestandener Vorrunden, Anteil Siege,
   Verluste Angreifer (Min/Median/Max), Verluste Verteidiger, ob der Wall ueberwunden wurde.
2. **Schwellenverhalten:** ab welcher Summe Schlagkraft die Vorrunde besteht, je Stufe. Vergleiche
   die gemessene Schwelle mit der Schwelle, die `kampfbericht._schwelle_wall` bzw. die
   Wallstufen-Tabelle in `data/buildings.json` nennt. Nenne jede Abweichung.
3. **Beute:** die Staffel 10 / 30 / 60 / 100 Prozent gegen die **mitnehmbare Menge** (Karrenladung)
   bei kleinem und grossem Vorrat (z. B. 100 und 10.000 je Rohstoff). Belegt werden muss, dass
   zuerst die Ladung deckelt und der Anteil danach - nicht umgekehrt.
4. **Ladung:** je Karrenart der Deckel (40/100/250/1.000/2.500), mit Wagenbau 1, 5, 10 und ueber
   der Hoechststufe; Deckel Faktor 2,0.
5. **Reisekosten:** Gold, Nahrung und Mana je Feld ueber die vorhandene Wegzeit-/Kostenfunktion,
   fuer 10, 40 und 100 Einheiten und fuer Entfernungen 1, 5, 20 Felder; Kennzeichnung, was belegt
   und was VORSCHLAG ist.
6. **Gegenprobe zum AT/SK-Fehler:** dieselbe Aufstellung einmal mit `E.angriff` (AT) und einmal mit
   `E.schlagkraft` (SK) durch die Vorrunde schicken und beide Ergebnisse nebeneinander zeigen.
   Das ist der Beweis, dass Register 54 wirklich behoben ist.
""")
    a("""
## 9. Ausgabeformat (verbindlich)

**Datei 1: `tools/mess_kampf.py`** - ASCII, hoechstens 600 Zeilen, `main()`, jede gedruckte Zeile in
der Form `<Kennzahl> | <Wert> | <Quelle>`, Rueckgabewert 0.

**Datei 2: `docs/audits/MESS_KAMPF_20261101.md`** - hoechstens 400 Zeilen, Gliederung:

| Abschnitt | Inhalt |
|---|---|
| A. Kopf | Datum, Kopf-Commit, angelegte Dateien, Aufruf, Zahl der Unteragenten |
| B. Die gedruckten Zeilen | vollstaendige Werkzeugausgabe im Codeblock, dazu eine Zeile mit dem Ergebnis des Sammellaufs |
| C. Wallstufen 0-10 | die Tabelle mit 40 Laeufen je Stufe und die Streuung |
| D. Schwellenverhalten | gemessene gegen dokumentierte Schwelle, je Stufe, mit Urteil |
| E. Beute | Staffel gegen mitnehmbare Menge, klein und gross, mit Urteil |
| F. Ladung und Wagenbau | Deckel je Karrenart und Stufe |
| G. Reisekosten | je Einheit, Entfernung und Rohstoff, mit Kennzeichnung BELEGT/VORSCHLAG |
| H. AT-gegen-SK-Gegenprobe | die zwei Zahlenreihen nebeneinander |
| I. Die drei wichtigsten Kernaussagen | je mit Zahl und Quelle |
| J. Auffaelligkeiten, nicht geglaettet | Ausreisser, Ausnahmen, offene Fragen |
| K. Was nicht messbar ist | und warum |

## 10. Abschluss (Pflicht)

1. `python -X utf8 tools/mess_kampf.py` ausfuehren, Ausgabe kopieren, Rueckgabewert pruefen.
2. `python -X utf8 -u tools/sammellauf.py` ausfuehren und das Ergebnis als eine Zeile in Abschnitt B
   anhaengen (Dateien, gruen, rot, ausgesetzt, Pruefungen, Sekunden).
3. Letzte Zeile deiner Antwort: `FERTIG <Pfad des Berichts> <Zeilenzahl>`.
""")
    return "".join(t)


PAKETE = {"b1": paket_b1, "b2": paket_b2, "c1": paket_c1}


def main():
    name = (sys.argv[1] if len(sys.argv) > 1 else "b1").lower()
    if name not in PAKETE:
        print("Unbekanntes Paket: %s (bekannt: %s)" % (name, ", ".join(PAKETE)))
        return 2
    text = PAKETE[name]()
    os.makedirs(ZIELORDNER, exist_ok=True)
    ziel = os.path.join(ZIELORDNER, "%s_paket_%s.md" % (name.upper(), date.today().strftime("%Y%m%d")))
    with open(ziel, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    zeichen = zeichenzahl(text)
    token = zeichen / ZEICHEN_JE_TOKEN
    usd_prompt = token / 1000.0 * USD_JE_1K_PROMPT
    print("Paket      : %s" % ziel)
    print("Zeichen    : %d" % zeichen)
    print("Zeilen     : %d" % len(text.splitlines()))
    print("Prompt-Tok.: %.0f (Schaetzung %.1f Zeichen/Token)" % (token, ZEICHEN_JE_TOKEN))
    print("USD Prompt : %.4f (nur Prompt; Denken ist der groessere Posten, real 0,15-0,45 USD)" % usd_prompt)
    if zeichen < 20000:
        print("WARNUNG: Paket ist kleiner als die Vorgabe 20.000 Zeichen.")
    if zeichen > 45000:
        print("WARNUNG: Paket ist groesser als die Vorgabe 45.000 Zeichen.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
