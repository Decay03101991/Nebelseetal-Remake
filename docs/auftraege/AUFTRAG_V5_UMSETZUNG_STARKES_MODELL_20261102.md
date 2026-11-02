# AUFTRAG V-5 — UMSETZUNG (starkes Modell, 02.11.2026)

Du bist der Umsetzer für einen konkreten Schritt in einem lokalen Einzelspieler-Remake
(Python 3, tkinter, JSON-Spielstand, offline). Auftraggeber ist Daniel. Du lieferst **Code und
Prüfungen als Text** — du kannst nichts ausführen, also behaupte auch keine Testergebnisse.

## GEGENSTAND

Im Spiel gibt es fünf Bots. Jeder Bot hat eine **Fraktion** und eine **Taktik**. Für beide existieren
bereits Boni, aber sie stehen **nur als Text** in der Oberfläche und **wirken nicht**:

**Volksattribute je Fraktion** (`src/bottaktik.py`, `VOLKSATTRIBUTE`, dauerhaft):

| Fraktion | Plus | Minus | Bots |
|---|---|---|---|
| menschlich | Holzertrag +5 % | Steinertrag −5 % | Haug, Brynhild |
| zwergisch | Steinertrag +5 % | Holzertrag −5 % | Grom |
| elfisch | Reisegeschwindigkeit +5 % | PA der Einheiten −5 % | Silra |
| monster | AT der Einheiten +5 % | Handelserlös −5 % | Krank |

**Taktikbonus je Bot** (`src/bottaktik.py`, `TAKTIKEN[bot]["bonus"]`, an den aktuellen Zustand
gebunden, mit Ablaufzeit 48 h in `verhaltensbonus`):

| Bot | Taktikbonus |
|---|---|
| Haug | Beute +5 % |
| Brynhild | Verteidigung +5 % |
| Grom | Ausbau +5 % |
| Silra | Reisegeschwindigkeit +5 % |
| Krank | Angriff AT +5 % |

Zusammen **13 Wirkungen**: 8 aus den Volksattributen (je plus und minus) und 5 Taktikboni.
Überschneidung: Silra hat Reise +5 % (Volk) **und** +5 % (Taktik), Krank hat AT +5 % **und** +5 %.

## WAS DU LIEFERST

Ein Dokument, deutsch, mit genau diesen Abschnitten:

1. **Kurzfassung** — höchstens 10 Zeilen: welcher Weg, welche Überschneidungsregel, was du NICHT
   entschieden hast.
2. **Entscheidungen** — Tabelle `Frage | Messlage | Möglichkeit A (Folge) | Möglichkeit B (Folge) |
   Empfehlung`. Diese Entscheidungen gehören Daniel; du empfiehlst, du entscheidest nicht.
3. **Umsetzung** — je Schritt ein Block:
   `SCHRITT <n> — <Datei>`, darunter `ANKER:` mit einer **wortgleichen** Zeile aus dem unten
   gelieferten Code (so, dass sie in der Datei genau einmal vorkommt) und `ERSATZ:` mit dem
   vollständigen neuen Code (Einrückung wie im Original). Neue Dateien als `NEUE DATEI: <pfad>` mit
   vollem Inhalt.
4. **Neue Prüfdatei** — vollständiger Inhalt, ASCII, Muster: `tests/harness.py` (`check(name, cond,
   detail)`, `abschnitt`, `bericht`). Je Wirkung mindestens eine Bedingung plus Grenzfälle
   (‑1 / 0 / exakt Soll / +1) und eine Gegenprobe, die bei der alten, nicht verdrahteten Fassung rot
   wird.
5. **Datenwerte** — jede Zahl, die nicht aus einer Quelle stammt, gehört als Wert in eine
   JSON-Datei unter `data/` (nicht fest in den Code), mit einem Feld, das die Begründung trägt.
6. **Dokumentzeilen** — je eine Zeile für `docs/PRUEFREGEL_ORIGINAL.md` (Register) und
   `docs/ENTWICKLUNGSPROTOKOLL.md`.
7. **Nicht beantwortet** — was du nicht belegen konntest, mit `UNBEKANNT`.

## HARTE REGELN

- **Keine Zahl ohne Quelle.** Belegt ist nur, was in den gelieferten Dateien oder im Handbuch steht.
  Alles andere ist `VORSCHLAG` mit Rechnung, z. B. „5 % von X ergibt Y, weil …".
- **Eine Wahrheit je Größe.** Kern und Anzeige lesen DIESELBE Funktion (im Projekt `F-04`-Muster).
  Kein zweiter Rechenweg, keine zweite Tabelle.
- **Nichts löschen.** Abgelöste Fassungen und Belegzahlen bleiben stehen und werden als abgelöst
  gekennzeichnet.
- **`src/main.py` hat ZWEI große Klassen** (`GameState` und `NebelseetalApp`). `self.state` gibt es
  nur in der App-Klasse.
- **`.py` ist ASCII** (`ae/oe/ue/ss`); nur Anzeigetexte dürfen Umlaute tragen.
- **Der Spieler bleibt unberührt**, solange du es nicht ausdrücklich als Entscheidung vorlegst: die
  Boni gelten für BOTS. Ob der Spieler eigene Volksattribute bekommt, ist eine Frage an Daniel.
- **Kein Umbau der Ordnerstruktur**, keine neuen Abhängigkeiten, kein Netzwerk, keine Datei-Zeit.
- **Bestehende Prüfungen dürfen rot werden** — dann sag welche, warum, und wie die Zusicherung
  stattdessen lauten muss (mit Begründung), statt den Code zurückzubiegen.
- Zahlen, die Daniel später ohne Code ändern können soll, gehören in `data/` (Schalter `aktiv`
  und Prozentwerte), nicht als Literal in den Code.

## WAS DU VOR ALLEM PRÜFEN SOLLST

- Wo wird der Ertrag je Siedlung und Stunde gerechnet, und wo liest die Anzeige ihn? Beide Stellen
  müssen dieselbe Funktion benutzen.
- Wo entsteht die Reisedauer eines Auftrags (`auftraege`), und wie kommt die Geschwindigkeit hinein?
- Wo werden AT/PA/SK einer Einheit gelesen (`einheiten`), und wo fließen sie in den Kampf
  (`kampf`, `kampfbericht`)?
- Wo wird Beute gebucht (`kampfbericht.beute_am_ziel`, `beute_staffel`) und wie kommt ein Bonus hinein,
  ohne die Deckelung durch die Karrenladung zu umgehen?
- Wo wird der Handelserlös gerechnet (`spieloekonomie`)?
- Wie kommt der Taktikbonus eines Bots an die Stelle, an der er wirken soll, ohne dass eine zweite
  Wahrheit über den Zustand entsteht (`bottaktik.verhaltensbonus_aktiv` existiert bereits und hat
  heute KEINEN Aufrufer im Produktivcode)?

## CODE-DATEIEN (so, wie sie im Projekt stehen)

