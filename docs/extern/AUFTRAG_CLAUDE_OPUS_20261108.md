# AUFTRAG an Claude Opus (Claude Pro, Chat) - Nebelseetal Remake, Stand 08.11.2026

> Dieses Dokument ist zum Kopieren in claude.ai gedacht. Es beschreibt Auftrag, Randbedingungen und
> das verbindliche Ausgabeformat. Stand des Projekts: Commit `fa5834b` (gepusht).

## 0. Wer du bist und was wir von dir wollen

Du bist der starke Partner eines Ein-Mann-Projekts. Wir wollen von dir nicht "viel Text", sondern
**kluge Arbeit und eine eigene Meinung**:

1. **Entscheidungen mitdenken.** Wenn zwei Wege gehen, sage, welchen du nimmst und warum - mit dem
   Preis des anderen Weges. Keine Aufzaehlung ohne Empfehlung.
2. **Fehler finden.** Widersprueche, doppelte Rechenwege, stille Ausfaelle, Testluegen. Mit Datei und
   Zeile, nicht "irgendwo".
3. **Umsetzbare Anweisungen liefern.** Deine Antwort wird von einem KLEINEREN Modell
   (`deepseek-flash`) in Code umgesetzt. Es braucht Anker, keine Andeutungen.
4. **Tipps geben**, die wir noch nicht kennen - auch ungefragt, aber getrennt von der Aufgabe.

## 1. Die Lage in sieben Saetzen

Das Projekt ist ein lokales Einzelspieler-Remake des Browserspiels "Nebelseetal" (Python 3.14 +
tkinter, JSON-Spielstand, portabel, offline). Daniel spielt es selbst und meldet Fehler als
Spieltester. Es gibt ein Fehlerregister mit ueber 300 Eintraegen, ein Entwicklungsprotokoll und einen
Ablaufplan mit nummerierten Schritten. Heute wurden drei Spieltests ausgewertet und die groessten
Punkte behoben (Nahrungsnot-Sperre mit Ausweg, Anzeige rechnet nicht mehr selbst, Quellwachen).
Zwei Quellwachen sind neu: `tests/test_quelle_ast.py` (Ansichten rechnen nicht) und
`tests/test_daten_und_quellen.py` (jede Zahl hat eine Herkunft). Ein Sammellauf ueber 203 Pruefdateien
laeuft mit `-j 2` in rund 11 Minuten und muss 0 rot ergeben. Der naechste Schritt ist die Umsetzung
von vier Punkten aus dem letzten Spieltest (Abschnitt 4).

## 2. Harte Randbedingungen (bitte ernst nehmen)

**Daniels Rechner ist schwach: 2 CPU-Kerne, keine GPU.** Waehrend eines Spieltests darf nichts
Ressourcenhungriges laufen, sonst wird das Spiel traege und der Test ist wertlos.

**Das WLAN ist nicht zuverlaessig.** Lange Antworten brechen ab. Deshalb:

* Antworte in **Abschnitten von hoechstens etwa 150 Zeilen**, mit einer Kopfzeile
  ("TEIL 1/4 - Punkt A: ..."), damit ein Abbruch nichts zerstoert.
* **Keine grossen Codebloecke.** Zeige hoechstens 15 Zeilen am Stueck; den vollstaendigen Umbau
  beschreibst du als Patch-Plan (siehe Abschnitt 7).
* Wiederhole am Anfang jedes Teils in EINER Zeile, was schon geliefert ist.

**Deine Antwort muss ein kleineres Modell umsetzen koennen.** Das heisst konkret:

* **Anker statt Beschreibung:** Datei, Funktionsname, eine eindeutige Zeile aus dem Jetzt-Zustand,
  dann "alt -> neu".
* **Keine Wahlmoeglichkeiten** wie "man koennte auch". Entscheide dich; wenn es zwei Wege gibt, nenne
  den verworfenen in EINEM Satz mit Grund.
* **Keine Zahlen aus dem Bauch.** Jede Zahl, die ins Spiel geht, ist entweder belegt (mit Quelle) oder
  ausdruecklich als VORSCHLAG markiert. Unbelegte Zahlen sind im Projekt ein Stilbruch.
* **ASCII in Pruefdateien.** Neue `tests/*.py` sind ASCII-only, weil ein Umlaut beim Import einen
  SyntaxError ausloest; Docstrings und Kommentare in Tests also ohne Umlaute.

## 3. Zugang zum Stand (sparsam lesen, WLAN)

Repository: **https://github.com/Decay03101991/Nebelseetal-Remake** (Branch `main`, oeffentlich).
Kopf: `fa5834b`. Diese Dateien zuerst, in dieser Reihenfolge:

| Datei | Warum |
|---|---|
| `docs/AKTUELLER_STAND.md` (nur der oberste Block) | was heute gebaut wurde, in Klartext |
| `docs/ENTWICKLUNGSPROTOKOLL.md` (letzte ~20 Zeilen) | die Belege mit Zeiten, Zahlen, Commit-Hashes |
| `docs/FRAGEN_AN_DANIEL_20261107.md` (Nachtraege 16:10 und 16:35) | die offenen Entscheidungen |
| `src/main.py` - nur die genannten Funktionen | dort liegt die Oberflaeche (16.000 Zeilen, nicht am Stueck lesen!) |

Nicht noetig fuer den ersten Auftrag: die `tests/`-Masse (203 Dateien) und `data/*.json` (51 Dateien).

## 4. Dein erster Auftrag: vier Punkte aus dem letzten Spieltest

Daniel hat die Punkte selbst formuliert. Fuer jeden Punkt willst du liefern: **Befund** (was heute im
Code steht), **Vorschlag** mit deiner Empfehlung, **Risiken**, **Patch-Plan**, **Testidee**.

**Punkt A - Der Wall gehoert in die Siedlungskarte, nicht ins Dorfzentrum.**
Daniels Wortlaut: "Der Dorfwall sollte in die geoeffnete Karte in das dortige Menue eingebaut werden,
wo man auch Gebaeude baut, bei Verteidigung." Heute steht der Wall-Kasten im Dorfzentrum
(`_render_overview`) und zusaetzlich eine duenne Zeile auf der Karte (`_render_settlement_map`,
Rubrik "Verteidigung"); das Dorfzentrum soll nach Daniels Willen nur Siedlungsgruendung und
Dorfauswahl zeigen. Gesucht: die saubere Aufteilung - was bleibt im Dorfzentrum (hoechstens eine
Zeile mit Verweis?), was zieht in die Rubrik "Verteidigung", und wie bleibt es EINE Anzeige
(`_mauer_reparatur_block` ist heute schon die gemeinsame Stelle).

**Punkt B - Der Handel ist nicht auffindbar.**
Daniel: "Davon sehe ich als Spieler nichts im ersten Eindruck ... nichts darueber auffindbar."
Die Handelsmaske liegt im Menuepunkt "Marktplatz" (`_render_market`): je Bot eine Zeile mit Knopf
"Handeln", Bots mit Handelsneigung <= 0,3 fehlen ganz; die **Handelskarawane** als Voraussetzung wird
nirgends genannt, und der Zustand (vorhanden? unterwegs?) fehlt. Gesucht: eine Marktplatz-Ansicht,
die in zwei Sekunden sagt, WO man handelt, WAS man braucht und was gerade fehlt - ohne neue Regel,
alle Zahlen aus dem Kern.

**Punkt C - Portal: Ziel per Klick auf die Weltkarte statt Auswahlliste.**
Daniel: "die Auswahl wohin ich springen will sollte nicht per Dropdown-Feld sein, sondern indem ich
ein freies Feld auf der entsprechenden Weltkarte auswaehle, gecheckt wird ob das Feld frei ist und
ich die Voraussetzungen habe, und mich dann dort hin springen lassen." Heute: `_render_portal` mit
Auswahllisten, 20 Pixelrechnungen, 5000 Mana Preis, 24 Stunden Sperre. Gesucht: der Umbauplan -
welche Klicklogik, welche Pruefung im Kern (nicht in der Ansicht), wie bleibt die Sperre sichtbar.

**Punkt D - Eine Bibliothek laesst sich nicht versetzen.**
Nachgemessen: `_karten_abreissen` verweigert den Abriss der LETZTEN Bibliothek (Daniels Regel vom
30.10.2026), und `max_je_siedlung: 1` verbietet eine zweite je Siedlung. Bis eine zweite SIEDLUNG
steht, ist die Bibliothek unversetzbar. Daniel hat die Frage offen (Frage 17): Abriss mit Rueckfrage,
ein Knopf "versetzen" (abriss + neu setzen in einem Zug), oder so lassen. **Deine Meinung ist gefragt**,
und dann der Patch-Plan fuer deinen Favoriten.

## 5. Entscheidungen, bei denen wir deine Meinung wollen

Antworte je Frage in drei Zeilen: **Empfehlung - Grund - Preis des anderen Weges.**

1. **Frage 17 (Bibliothek versetzen)** - siehe Punkt D.
2. **Frage 18 (Pakt annehmen/ablehnen)** - Daniel will, dass ein Bot einen Pakt nach seiner
   Einstellung zu ihm annehmen oder ablehnen kann. Heute bucht der Knopf immer. Wie wuerdest du die
   Regel bauen (Schwelle, Wahrscheinlichkeit, Begruendung im Postfach), ohne das Original zu verbiegen?
3. **Frage 15 (neun Balance-Werte ohne Quelle im Code)** - z. B. Beuteanteil 50 %, Beschaffungskosten
   250, Zeitraffer 180. Sollen sie in `data/` wandern oder mit dem Satz "VORSCHLAG bleibt" im Code
   stehen bleiben?
4. **Frage 16 (sechs Datendateien ohne Quellenangabe)** - Bot-Bedarf, Bot-Diebstahl, Bot-Forschung,
   Bot-Stimmen, Spionage, Marsch-Optik. Was ist der billigste ehrliche Weg?
5. **Design** - Daniel hat das gesamte Design als "dringend" markiert, die Vorlagen kommen aber von
   einem Menschen (Herr Duebner). Bis dahin: welche drei Eingriffe wuerden den groessten Eindruck
   machen, ohne dass wir eine Palette erfinden?

## 6. Was du NICHT tust

* Keine erfundenen Zahlen, Namen, Preise oder Fristen. Wenn etwas fehlt: "fehlt, Vorschlag: ...".
* Keine Regel aendern, die Daniel entschieden hat (Nahrungsnot-Sperre 70/74, hoechstens zwei
  Bibliotheken, keine Niederlage-Strafe, ein Spieltag = 86.400 Sekunden). Vorschlagen ja, einbauen nein.
* Keine Massen-Umbauten "zur Sicherheit". Jede Aenderung muss eine Wache haben oder eine bestehende
  gruen lassen.
* Keine Behauptung ohne Datei und Zeile. "Ich vermute" ist erlaubt, wenn es als Vermutung dasteht.
* Keine Zugangsdaten, keine Passwoerter, keine persoenlichen Daten von Daniel in Beispielen.
* Kein Code-Dump ueber 15 Zeilen. Wir setzen Patch-Plaene um, keine Bloecke.

## 7. Verbindliches Ausgabeformat

Kopf jeder Antwort:

```
TEIL <n>/<gesamt> - <Punkt> - Stand fa5834b
Bisher geliefert: <eine Zeile>
```

Dann je Punkt:

```
BEFUND:    <was heute im Code steht, mit Datei und Funktion>
VORSCHLAG: <deine Empfehlung, in einem Satz>
RISIKO:    <was kaputtgehen kann, in einem Satz>
PATCH-PLAN:
  1. <datei> :: <funktion> :: <Ankerzeile aus dem Jetzt-Zustand>
     alt: <...>
     neu: <...>
  2. ...
TEST:      <welche Pruefdatei das abdeckt, oder welche neue Wache noetig ist>
FRAGE:     <nur wenn wirklich etwas offen bleibt>
```

Am Ende jedes Teils eine Zeile: `NAECHSTER TEIL: <was kommt>`.

## 8. Wie wir deine Antwort verwerten

Ich (Hermes, `deepseek-flash`) pruefe jede Zahl und jeden Anker gegen den Code, setze den Patch um,
fahre die Pruefungen und den vollen Sammellauf. Was nicht belegbar ist, kommt zurueck an dich mit dem
Messwert. Deine Antworten liegen im Projekt unter `docs/extern/` mit Datum und Hash. Erwarte also
keine ungepruefte Uebernahme - erwarte, dass deine Vorschlaege GEMESSEN werden.

## 9. Rahmen

Claude Pro, 21,42 EUR/Monat (18,00 EUR + MwSt.), Verlaengerung 08.12.2026. Kein API-Verbrauch, keine
versteckten Kosten. Dafuer erwarten wir konkrete, pruefbare Arbeit - nicht Prosa.
