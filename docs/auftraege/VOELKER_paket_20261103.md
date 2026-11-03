# AUFTRAG VOELKER — Voelkerwahl am Spielstart, sechs Fraktionen (starkes Modell, 03.11.2026)

Du bist der Planer UND Umsetzer eines konkreten Schritts in einem lokalen Einzelspieler-Remake
(Python 3, tkinter, JSON-Spielstand, offline, keine Netzverbindung). Auftraggeber ist Daniel.
Du kannst nichts ausfuehren - behaupte also keine Testergebnisse, sondern liefere Text, den der
Koordinator einbaut und prueft.

## GEGENSTAND (gemessen am Code vom 03.11.2026, Kopf fd734ae)

**Beschlossen, noch nicht gebaut** (Gesamtkonzept Abschnitt 6, woertlich): "Voelkerwahl am Start
(sechs Voelker, der Spieler waehlt, die Bots bekommen die uebrigen) und die Verdrahtung der 13
Volksboni." Aus der Uebergabe vom 02.11.2026, Punkt 4: "A2 Voelkerwahl am Spielstart: sechs Voelker,
keine Doppelung, Spieler waehlt; die Bots bekommen die uebrigen. `botkern.BOT_FRAKTIONEN` ist heute
fest (4 Fraktionen fuer 5 Bots) und muss in den Spielstand wandern."

**Heute im Code:**

```python
# src/bottaktik.py
VOLKSATTRIBUTE: Dict[str, Dict[str, str]] = {
    "menschlich": {"plus": "Holzertrag +5 %", "minus": "Steinertrag -5 %"},
    "zwergisch": {"plus": "Steinertrag +5 %", "minus": "Holzertrag -5 %"},
    "elfisch": {"plus": "Reisegeschwindigkeit +5 %", "minus": "PA der Einheiten -5 %"},
    "monster": {"plus": "AT der Einheiten +5 %", "minus": "Handelserloes -5 %"},
}

# src/botkern.py
BOT_FRAKTIONEN = {
    "Haug": "menschlich",
    "Brynhild": "menschlich",
    "Grom": "zwergisch",
    "Silra": "elfisch",
    "Krank": "monster",
}
```

- Es gibt **vier** Fraktionen und **fuenf** Bots; `menschlich` ist doppelt belegt. Der Spieler hat
  heute **keine** Fraktion: kein Feld im Spielstand, keine Wahl, keine Anzeige.
- Die Fraktion steht bereits am Bot (`bot.faction`) und wird an mehreren Stellen gelesen
  (`bottaktik.volksattribute({"fraktion": bot.faction})`, Anzeigen in `main.py`).
- Die 13 Wirkungen der Volks- und Taktikboni sind ein EIGENER Schritt (Auftrag V-5) - hier wird die
  Wahl gebaut, nicht die Wirkung verdrahtet.

## ENTSCHEIDUNG DANIEL (03.11.2026, woertlich)

"Mit Voelker sind die Fraktionen gemeint, Menschlich, Zwergisch, Elfisch, Trolle, Ghule, Gnome dann
haben wir 6 Fraktionen."

Damit gilt:

- Die sechs Fraktionen heissen **menschlich, zwergisch, elfisch, Trolle, Ghule, Gnome**.
- **"monster" kommt in dieser Liste nicht vor.** Sein Plus/Minus (AT +5 % / Handelserloes -5 %) muss
  also einer der drei neuen Fraktionen zugeordnet werden - oder begruendet entfallen. Das ist eine
  Entscheidung fuer Daniel; du machst einen **VORSCHLAG** und kennzeichnest ihn als solchen.
- Fuer die drei neuen Fraktionen (Trolle, Ghule, Gnome) gibt es **keine Quelle** fuer Plus/Minus. Jeder
  Wert ist ein VORSCHLAG und gehoert mit `"quelle": "VORSCHLAG"` in die Datendatei, nie still in den
  Code.

## WAS DU LIEFERST

Ein Dokument, deutsch, mit genau diesen Abschnitten:

1. **Kurzfassung** - hoechstens 10 Zeilen: welcher Weg, welche Verteilungsregel, was du NICHT
   entschieden hast.
2. **Entscheidungen** - Tabelle `Frage | Messlage | Moeglichkeit A (Folge) | Moeglichkeit B (Folge) |
   Empfehlung`. Mindestens: Wer bekommt welche Fraktion (Spieler waehlt, Bots bekommen die uebrigen -
   aber in welcher Reihenfolge und nach welcher Regel)? Was passiert mit `monster`? Welche Plus/Minus
   bekommen Trolle, Ghule, Gnome? Bekommt auch der Spieler eine Wirkung oder zunaechst nur eine Anzeige
   (die Wirkung ist V-5)? Wie wird die Wahl im Spielstand gespeichert (Feldname, alte Spielstaende ohne
   das Feld)? Ist die Wahl beim ersten Start endgueltig oder wiederholbar bis zur ersten Siedlung?
   Reihenfolge der Startmaske: erst Volk, dann Karte, oder umgekehrt?
3. **Umsetzung** - je Schritt ein Block: `SCHRITT <n> - <Datei>`, darunter `ANKER:` mit einer
   **wortgleichen** Zeile aus dem unten gelieferten Code (so, dass sie in der Datei genau einmal
   vorkommt) und `ERSATZ:` mit dem vollstaendigen neuen Code (Einrueckung wie im Original). Neue
   Dateien als `NEUE DATEI: <pfad>` mit vollem Inhalt.
4. **Neue Pruefdatei** - vollstaendiger Inhalt, **ASCII** (ein Umlaut = SyntaxError beim Import),
   Muster `tests/harness.py` (`check(name, cond, detail)`, `abschnitt`, `bericht`). Je Entscheidung
   mindestens eine Bedingung, dazu die Grenzfaelle: fuenf Bots + Spieler = sechs Fraktionen ohne
   Doppelung; alter Spielstand ohne Feld; Wahl ohne Argument (Rueckfall auf heute, damit die 16
   Pruefdateien mit `_found_settlement()` weiter gruen bleiben).
   **Pflicht:** eine Bedingung, die bei der HEUTIGEN Fassung (vier Fraktionen, `monster` doppelt
   belegt) rot wird.
5. **Datenwerte** - die sechs Fraktionen mit Plus/Minus, Beschreibung und Quelle gehoeren in
   `data/voelker.json` (Vorschlag), nicht in den Code. Jeder Wert traegt `"quelle"`: `"bottaktik.py"`
   fuer die vier bestehenden, `"VORSCHLAG"` fuer die neuen, mit einem Feld `"begruendung"`.
6. **Dokumentzeilen** - je eine Zeile fuer `docs/PRUEFREGEL_ORIGINAL.md` (Register) und
   `docs/ENTWICKLUNGSPROTOKOLL.md`.
7. **Nicht beantwortet** - was du nicht belegen konntest, mit `UNBEKANNT`.

## HARTE REGELN

- **Keine Zahl ohne Quelle.** Nur was in den gelieferten Codeauszuegen oder im Handbuch steht, ist
  belegt. Alles andere ist `VORSCHLAG` und gehoert in die Datendatei, nicht in den Code.
- **Der stehende Aufruf bleibt:** `_found_settlement()` und `_erste_siedlung_gruenden()` ohne Argument
  muessen weiterhin sofort gruenden - 16 Pruefdateien mit 22 Aufrufstellen haengen daran.
- **Die zwei Regeln, die nie gebrochen werden:** Doerfer werden NIE eingenommen; Angriffstruppen werden
  nie am Zielort stationiert. Keine Beschreibung darf etwas anderes sagen.
- **Kein Fenster, kein Netz:** alles muss ohne laufendes Spiel pruefbar sein. Pruefdateien sind ASCII,
  Spieltexte duerfen Umlaute tragen.
- **Keine stillen Aenderungen an bestehenden Entscheidungen:** wird eine alte Wache falsch, wird sie
  UMBENANNT und die neue Entscheidung im Docstring genannt.
- **Keine Doppelung:** jede Fraktion genau einmal (sechs Fraktionen, ein Spieler, fuenf Bots). Wenn dir
  das nicht aufgeht, sag es unter `Nicht beantwortet` statt zu tricksen.

## GELIEFERTER CODE (wortgetreu, Stand fd734ae)

```python
# src/bottaktik.py, Zeilen 210-215
VOLKSATTRIBUTE: Dict[str, Dict[str, str]] = {
    "menschlich": {"plus": "Holzertrag +5 %", "minus": "Steinertrag -5 %"},
    "zwergisch": {"plus": "Steinertrag +5 %", "minus": "Holzertrag -5 %"},
    "elfisch": {"plus": "Reisegeschwindigkeit +5 %", "minus": "PA der Einheiten -5 %"},
    "monster": {"plus": "AT der Einheiten +5 %", "minus": "Handelserloes -5 %"},
}

# src/botkern.py, Zeilen 55-61
BOT_FRAKTIONEN = {
    "Haug": "menschlich",
    "Brynhild": "menschlich",
    "Grom": "zwergisch",
    "Silra": "elfisch",
    "Krank": "monster",
}
```

## RAHMEN

- Ziel: ein Startfenster, in dem der Spieler seine Fraktion waehlt und sieht, was sie bedeutet; die
  fuenf Bots bekommen die uebrigen Fraktionen ohne Doppelung. Die Wirkung der Boni kommt spaeter (V-5),
  die Anzeige gehoert hierher.
- Der Schritt gehoert zum eingefrorenen Demo-Umfang ("Voelker- und Kartenwahl am Start").
- Antworte auf Deutsch, mit klaren Ueberschriften. Wo du etwas nicht weisst: `UNBEKANNT` statt einer
  Vermutung.
