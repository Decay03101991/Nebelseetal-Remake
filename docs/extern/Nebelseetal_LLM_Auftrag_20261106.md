# NEBELSEETAL REMAKE - Wissens- und Auftragsdokument fuer ein externes LLM

**Stand:** 06.11.2026, Pre-Release `Nebelseetal_Pre_Release_V_0.0.3` (Schnitt nach S3).
**Kopf-Commit beim Schreiben:** `1c5cb73` auf `main`, Arbeitsbaum leer.
**Dieses Dokument ist selbsterklaerend.** Wer es liest, braucht keinen Zugriff auf den Code, kein
Netz und keinen Login. Jede Zahl steht hier im Text oder in einer der genannten Datendateien.

---

## 0 Lesehinweis und Zweck (60 Sekunden)

Du bist ein externes Modell und sollst unser Spiel **verstehen**, unseren **Stand annehmen** und
alles **fehlende konstruieren**, so dass unser Agent es nur noch ablaufen lassen muss.

1. Lies die Abschnitte 1 bis 9 vollstaendig. Sie beschreiben Spiel, Mechaniken, Code, gebauten und
   **geplanten** Stand, Abschlussbedingungen und Balancing-Werkzeuge.
2. Nimm den Stand als **gesetzt** an. Du darfst ihn kritisieren, aber du baust auf ihm auf; ersetzt
   wird nichts stillschweigend (Abschnitt 13).
3. Konstruiere, was fehlt: Code-Schnitte, Daten, Wachen (Tests), Ablaeufe, Balancing-Werkzeuge - so
   vollstaendig, dass das Spiel **fertig** ist und sich danach durch **Balancing-Daten und
   Tester-Feedback selbst verbessert**.
4. Liefere in der Form aus Abschnitt 11 und beachte die Ablagehinweise in Abschnitt 12.

Dein Ergebnis wird **nicht direkt eingebaut.** Wir lassen zwei bis drei Modelle dieselbe Datei
bearbeiten, gleichen die Antworten gegeneinander ab und integrieren dann die nach unseren
Prinzipien beste Methode. Plane deine Antwort so, dass sie diesen Abgleich ueberlebt: begruende
jede Zahl, nenne jede Annahme, markiere jede Unsicherheit.

---

## 1 Was das Spiel ist

`Nebelseetal Remake` ist ein **lokales Einzelspieler-Aufbauspiel** als Neuauflage des Browserspiels
Nebelseetal. Python 3.14 und tkinter, JSON-Spielstand, offline, kostenlos, portabel. Aufbau steht
vor Kampf: es gibt keinen Siegscreen, sondern Auszeichnungen und Ruhm. Ein Spieler gegen fuenf Bots
mit eigener Wirtschaft, einen Drachen und Ruinen, verteilt auf sechs Welten mit sechs Voelkern.

Gemessener Umfang am 06.11.2026 (alles aus dem Projekt gezaehlt, nicht geschaetzt):

| Groesse | Wert |
|---|---|
| Python-Dateien in `src/` | 62 (zusammen 35.105 Zeilen, davon `main.py` 15.351) |
| Datendateien in `data/` | 46 JSON-Dateien |
| Pruefdateien in `tests/` | 183 (letzter voller Sammellauf: 7.495 Einzelpruefungen) |
| Werkzeuge in `tools/` | 58 |
| Dokumente in `docs/` | 124 Markdown-Dateien |
| Original-Siedlungskarten | 127 (10x10, drei Gueteklassen 35/43/49) |
| Einheiten | 28, Forschungsgebiete 21, Rohstoffe 9, Waren 17 |
| Commits | ueber 640 |

Spielsprache ist Deutsch; Anzeigetexte tragen echte Umlaute, Code und Kommentare bleiben ASCII.

---

## 2 Spielschleife, Kernkreis und Zeitbasis

**Zeitbasis.** Spieluhr mit Faktor **x180**: 1 Spielstunde = 20 echte Sekunden, 1 Spieltag =
24 Spielstunden = 28.800 Spielsekunden = 8 echte Minuten. Alle Fristen, Dauern und Auftraege rechnen
in **Spielsekunden**, nie in Rechnerzeit. Eine Ausnahme sind reine Anzeige-Uhren; neue Mechaniken
muessen die Spielzeit benutzen.

**Kernkreis** in dieser Reihenfolge: gruenden, produzieren, forschen, ausruesten, ausbilden, bewegen,
kaempfen, punkten. Alles Langsame laeuft ueber Auftraege und Reisezeit; der Rueckweg kostet doppelt so
viel wie der Hinweg. Der Tick bucht Produktion, Versorgung, Warteschlangen, Nachrichtenablauf und
Bot-Zuege.

**Ein Arbeitstakt** ist ein Tick ueber eine Spanne Spielzeit. Jede Buchung ist atomar: entweder
alles oder nichts, mit Rueckbuchung bei Ablehnung.

---

## 3 Oberflaeche, Ansichten, Freischaltungen, Anzeigen

Navigation mit zwei Ebenen (Uebersicht und Siedlung), Leiste immer sichtbar. Siedlungsreiter:
Siedlungsuebersicht, Produktion, Verteidigung.

Anzeigen: Punkte- und Ressourcenleiste (Rohstoffe, Kriegs-, Forschungs-, Handels-, Gesamtpunkte);
Ruhm-Balken als `tk.Canvas` mit Stufen aus `data/ruhm.json`; Postfach mit Filter, Archiv und Blaettern
(20 Nachrichten je Seite); Ansichten fuer Forschung, Portal, Kaserne, Ruhmeshalle, Diplomatie
(geplant); Ingame-Overlays fuer Menuegeschichten und Ereignisse.

Freischaltungen: Forschung schaltet Gebaeude, Waren und Einheiten frei. Menuegeschichten erscheinen
beim ersten Oeffnen ihrer Ansicht (Forschung mit erster Bibliothek, Portal mit erstem Weltwechsel,
Kaserne mit fertiger Kriegerakademie, Ruhmeshalle beim ersten Oeffnen). Postfach-Fristen:
Berichte 1 Spieltag, `kampf` und `gesamtsieg` laufen nie ab, ungelesene Verlustberichte verschieben
sich automatisch ins Archiv.

**Anzeige und Kern lesen immer dieselbe Funktion.** Das ist eine harte Regel (Muster F-04): eine
zweite Rechenstelle fuer denselben Wert hat uns schon zweimal gruen geprueft und trotzdem falsch gerechnet.

---

## 4 Mechaniken mit belegten Werten

Alle Zahlen stammen aus `docs/original/Nebelseetal_Spielanleitung_2009.pdf` (Richtschnur), aus den
Original-Seiten 2006 (`docs/original/Spielanleitung_2005/`, Struktur und Entwicklung) oder aus
gerechneten Tabellen (`docs/S0_TABELLEN_20261107.md`). Wo 2006 und 2009 abweichen, gilt **Balance aus
2009, Struktur aus beiden**; Abweichungen stehen in `docs/quellen/ABWEICHUNGEN_2006_zu_2009.md`.

### 4.1 Gelaende, Rohstoffe, Bauen

Ertrag je Spielstunde nach Gelaende (aus `data/resources.json`):

| Rohstoff | Ertrag je Stunde | Gebaeude |
|---|---|---|
| Holz | Wald 4, Steppe 2 | Holzfäller |
| Stein | Berg 4, Huegel 2 | Steinmetz |
| Metall | Berg 3, Huegel 1.5 | Erzmine |
| Mana | Nebelsee 5, alles ausser Sumpf 1 | Tempel |
| Nahrung | Grasland 4, Steppe 2 | Farm, Jaeger, Rinderfarm |
| Gold | Berg 3, Huegel 1.5 | Goldmine |
| Wolle | Grasland 3, Steppe 1.5 | Schafszucht |
| Leder | Grasland 3, Steppe 1.5 | Rinderfarm, Jaeger |
| Pferde | Grasland 3, Steppe 1.5 | Pferdezucht |

Baupreise (belegt): Holzfäller 10 Holz / 5 Stein / 1 Siedler, Steinmetz 5/10/1, Jaeger 25/25/1,
Haus 80 Holz / 50 Stein, Bibliothek 12/8, Verteidigungswall 16/16. Weitere Preise in
`data/baupreise.json` mit Kennzeichnung BELEGT oder VORSCHLAG je Posten. Es gibt **keine** zentralen
Kapazitaetslager: Lagerung ist ortsgebunden.

### 4.2 Siedler, Haeuser, Nahrung

Siedlergrenze **10 je Siedlung plus 5 je Haus**, Deckel **360** bei maximal 6 Siedlungen. Siedler
wachsen um 1 je Spielstunde bis zur Grenze. Siedler, die in einem Gebaeude arbeiten, belegen keinen
Hausplatz. Forschung Heilkunde erhoeht die Siedlerproduktion um 10 Prozent je Stufe. Seit Daniels
Entscheidung binden **Bauten keine Siedler** - Siedler gehen nur bei der Ausbildung weg.

Nahrung ist der zweite Engpass: **8 Nahrung je Einheit und Spieltag** (`data/nahrungsverbrauch.json`,
Herleitung: Reichsertrag 5.542 je Tag, 100 Einheiten = 14,4 Prozent, Siedlerdeckel 360 = 52 Prozent).
Unterdeckung hat **keine Strafe** (keine Quelle nennt eine), der Bestand faellt auf 0 und der Rest
steht als Unterdeckung im Journal.

### 4.3 Forschung

21 Forschungsgebiete, Zugang ueber die Bibliothek, Pfade in `forschungspfad`/`research.json`.
Forschung kostet Spieltage und schaltet Gebaeude, Waren und Einheiten frei. Bots forschen nach
eigenem Plan, Baukunst zuerst.

Belegte Kette (nicht abkuerzbar): Holzfäller, dann Bibliothek (ohne Forschung baubar), dann Forschung
Baukunst, dann Goldmine, Farm, Kriegerakademie. Ohne Bibliothek keine Forschung, ohne Baukunst keine
Goldmine; Einheiten brauchen zusaetzlich die Ausruestung aus der Werkstatt.

### 4.4 Waren, Ausruestung, Einheiten, Ausbildung

28 Einheiten in `data/units.json`:

| Gruppe | Einheiten |
|---|---|
| Nahkampf | Buergerwehr, Kaempfer, Krieger, Ritter, Paladin |
| Fernkampf | Kurzbogenschuetze, Bogenschuetze, Langbogenschuetze, Armbrustschuetze |
| Kundschafter | Streuner, Gauner, Dieb, Meisterdieb, Kundschafter, Waldlaeufer |
| Karren | Handkarren, Einspaenner, Zweispanner, Handelskarawane, Grosse Handelskarawane, Siedlerkarren |
| Belagerung | Belagerungsturm, Ramme, Grosser Belagerungsturm, Grosse Ramme, Balliste, Katapult, Grosses Katapult |

Beispielkosten: Buergerwehr 1 Siedler / 100 Nahrung / 50 Leder / 50 Wolle; Kaempfer 1 Siedler /
175 Gold; Krieger 1 Siedler / 350 Gold / 1 Pferd; Ritter 1 Siedler / 700 Gold / 1 Pferd; Paladin
1 Siedler / 1.400 Gold / 10 Mana / 1 Pferd. 17 Waren mit Rezepten in `data/warenrezepte.json`
(14 Einheiten brauchen Waren als Ausruestung). Ausbildungsstaetten: Kriegerakademie, Diebesgilde,
Stellmacher; Ausbildung laeuft als Warteschlange je Ort (`einheit`, `gebaeude`, `start`, `ende`,
`dauer_sekunden`, `stufe`, `gebucht`, optional `heilung`).

**Karrenladung** ist die Grenze der Beute: Handkarren 40, Einspaenner 100, Zweispanner 250,
Handelskarawane 1.000, Grosse Handelskarawane 2.500. Forschung Wagenbau erhoeht die Ladung um
10 Prozent je Stufe bis Stufe 10 (Faktor 2,0, Schalter in `data/karrenkapazitaet.json`); der Bonus
wird an **jeder** Stelle mitgegeben, an der aus Ladung eine Kapazitaet wird.

### 4.5 Bewegen und Zeit

Auftraege haben Marschzeit und Wegzeit, der Rueckweg kostet doppelt. Transport und Handel laufen ueber
Warteschlangen. Ein Weltensprung ist gesperrt, solange Auftraege unterwegs sind (Sperre im Kern,
nicht in der Anzeige). Bestand kommt immer aus dem **Ort**, nicht aus dem Reich.

### 4.6 Kampf, Wall, Goetterschutz

Kampf laeuft in Vorrunde, Wallstufen, weiteren Phasen, Beute und Flucht (eine einzige Funktion:
`kampf.fuehre_schlacht`). Beute haengt an der Karrenladung und ist strukturell gedeckelt:
Anteil 10/30/60/100 Prozent **und** Ladung - alles stehlen geht nur frueh.

Wall: Stufen 1 bis 10 mit Zustand in Prozent (`data/buildings.json` nennt je Stufe die Vorrunden-
Schwelle in Schlagkraft, Stufe 3 = 90 SK Fusstruppen). Mauerreparatur ist **gebaut** (S2): Preis je
Prozentpunkt **16 mal Stufe / 100** Holz und Stein, Dauer 360 Spielsekunden je Prozentpunkt,
Rohstoffe beim Start atomar gebucht, Zustand steigt im Tick, Kampf bricht eine laufende Reparatur ab,
Reparatur und Ausbau sperren sich gegenseitig.

Goetterschutz ist ein Punkteband und schuetzt vor Rueckstand (`versorgungsschutz.py`, `punkte.py`);
er endet mit dem ersten Kriegspunkt. Der Diebstahlpfad hat dieselben Gates wie der Angriff.

### 4.7 Punkte, Auszeichnungen, Ruhm

Kriegs-, Forschungs-, Handels- und Gesamtpunkte (Gesamtpunkte = (Krieg + Forschung) / 2). Kein Sieg,
sondern vier Auszeichnungen. Ruhm-Stufen aus `data/ruhm.json`: 0 / 10 / 40 / 160 (VORSCHLAG aus
unserer eigenen Messung: Spieltest-Laeufe endeten nach 8 bis 12 Spieltagen bei 19 bis 40 Punkten).
Der Balken zeigt den Abstand zur naechsten Stufe.

Gemessene Wahrheit: in allen Spieltest-Laeufen blieben die **Handelspunkte bei 0** - der Handelsweg
ist gebaut, aber im Spielbetrieb nicht erreichbar. Das ist ein offener Befund, kein Schoenheitsfehler.

### 4.8 Portale, Weltwechsel, Drachen, Ruinen

Weltwechsel kostet 5.000 Mana; ein Tempel erzeugt 120 Mana je Spieltag, ein Wechsel dauert rechnerisch
etwa 41,7 Spieltage. Portal-Koordinaten X-Y-Z im 20x20-Gitter; eigene Dimension gruen, fremde rot.
Drachen geben Weltpunkte und Trophaeen, Ruinen Deckung. Bots haben **keine** Drachenregel - sie
meiden den Drachen weder noch greifen sie ihn an.

### 4.9 Bots (fuenf Nachbarn)

Gebaut: eigene Wirtschaft je Dorf, Gebaeude nach Kartenprofil, Forschung (Baukunst zuerst), Nahrungs-
und Vorratsplanung mit Reserve, Ausbildung je Ort, Karren, Warenkette aus Werkstatt und Rezepten,
Gruenden und Karte kaufen, Dorf aufgeben, Wall bauen, Raubzug, Diebstahl, Spionagebericht lesen,
Ruinen raeumen, Takte (feste Spielzeit-Punkte), Punkte, Stimmen, Welten, Wappen.

Bot-Daten: `bot_wirtschaft.json`, `bot_bauplan.json`, `bot_bedarf.json`, `bot_forschung.json`,
`bot_gruendung.json`, `bot_raubzug.json`, `bot_diebstahl.json`, `bot_stimmen.json`, `bot_wappen.json`.
Struktur: 69 von 74 `bot_*`-Funktionen stehen in `main.py`; die Bot-Wirtschaft ist eine eigene
Schicht (`botkern.py`, `bot_angriffsplanung.py`, `bottaktik.py`).

Bekannte Luecken (Stand 06.11.2026): keine Drachenregel, kein belegter Handel gegen den Spieler,
keine aktive Spionage gegen den Spieler, keine Reaktion auf den Spielerfortschritt, keine
durchgehenden Persoenlichkeitsprofile. Diese Luecken sind Teil deines Auftrags.

### 4.10 Postfach und Nachrichten

`data/nachrichten.json` fuehrt Kategorien und Fristen (Frist 1 Spieltag = 28.800 Spielsekunden).
Gebaut sind unter anderem die Typen `kampf`, `gesamtsieg` und - seit dem 06.11.2026 - **`verlust`**:
jede Verlustbuchung erzeugt genau eine Nachricht mit Ort und Mengenaufzaehlung, geschrieben **vor**
der Verlustbuchung und unabhaengig vom Schalter der Verwundeten (ein Verlustbericht darf nicht an
einer zweiten Mechanik haengen).

### 4.11 Verwundete und Heilung (S3, gebaut 06.11.2026)

- **30 Prozent** der Verluste je Einheitentyp werden verwundet, **abgerundet**.
- Heilung kostet **75 Prozent** aller Kostenposten der Einheit aus `data/units.json` - **ohne**
  Siedler und **ohne** Waren (Ausruestung bleibt am Soldaten).
- Heildauer **50 Prozent** der Ausbildungsdauer der Stufe (Stufe 1: 600 Sekunden).
- Heilung laeuft in der **vorhandenen** Warteschlange `ausbildung` mit Kennzeichen `heilung`; das
  Fertigjournal nennt die Art `heilung`, nicht `einheit`.
- Feld `Settlement.verwundete`; Buchung an drei Stellen (Bot greift Spielerort an, eigener Auftrag,
  Drachenkampf) **vor** der Verlustbuchung.
- Alle Zahlen in `data/verwundete.json` (Schalter `aktiv`), Rechnung in `src/verwundete.py`; die
  Anzeige in der Kaserne liest dieselbe Funktion.
- **Anzeige schreibt deutsche Zahlen**: hoechstens zwei Nachkommastellen mit Komma
  (`hilfen.zahl_de`), der Kern bleibt ungerundet. Beispiel: ein Krieger kostet 262,5 Gold und
  0,75 Pferde.
- Wache `tests/test_verwundete.py`, 52 Pruefungen, 0 Fehler.

### 4.12 Was ein Spieltag an Aufbauzeit bedeutet

Ein Spieltag ist 8 echte Minuten. Eine Partie bis zum ersten Gefecht dauert in unseren Messungen
8 bis 12 Spieltage. Jede neue Mechanik muss diese Zahl **senken oder gleich lassen**; sie steht als
eigene Spalte im Ablaufplan (`docs/ABLAUF_20261107.md`, Spalte Aufbauzeit-Effekt). Eine Mechanik ohne
diese Angabe wird nicht eingebaut.

---

## 5 Wie unser Code gebaut ist

### 5.1 Schichten

| Schicht | Inhalt | Regel |
|---|---|---|
| `src/main.py` | Oberflaeche und Spielzustand: `GameState` (ab etwa Zeile 824) und `NebelseetalApp` (ab etwa Zeile 2.997) | nur hier darf gelesen/gezeichnet werden; keine Rechnung in der Anzeige |
| Fachmodule in `src/` | je ein Thema (Kampf, Auftraege, Wirtschaft, Forschung, Wall, Verwundete, Bot ...) | rechnen und buchen; Anzeige ruft sie auf |
| `data/*.json` | alle Zahlen, Texte und Schalter | **keine Zahl im Code**, kein Text im Code; ASCII-Schluessel |
| `tests/test_*.py` | Wachen je Thema, ueber `tests/harness.py` (`check`, `befund`, `bericht`) | eine Wache je Bedingung, Kern und Anzeige getrennt |
| `tools/*.py` | Messen, Bauen, Pruefen (Sammellauf, Balancing, Spieltest, EXE) | duerfen schreiben, nie im laufenden Spiel mitmischen |

### 5.2 Die 62 Module nach Aufgabe

| Gruppe | Module |
|---|---|
| Einstieg und Oberflaeche | `main`, `oberflaeche_original`, `karten_optik`, `karten_optik_fein`, `welt_optik`, `welt_optik_fein`, `marsch_optik`, `gebaeude_optik`, `berater`, `baumenue_info`, `ausgabemodus`, `admin_oberflaeche` |
| Wirtschaft und Bauen | `spieloekonomie`, `wirtschaft`, `gelaende`, `haeuser`, `gebaeude_wirkung`, `baupreise` (Daten), `werkstatt`, `ausruestung`, `einheiten`, `fehlbestand`, `dorfwall` |
| Forschung und Boni | `forschung`, `forschungspfad`, `forschung_wirkung`, `boni`, `bonus_system`, `punkte`, `versorgungsschutz` |
| Bewegung und Kampf | `auftraege`, `kampf`, `kampfbericht`, `verwundete`, `spionage`, `drachen`, `ruinendeckung`, `portalraum`, `welt`, `originalkarten`, `originalkarten_grafik` |
| Bots | `botkern`, `bot_angriffsplanung`, `bottaktik`, `voelker` |
| Text und Story | `story`, `stimmen`, `postfach`, `hilfen` |
| Spielstand und Zeit | `speichern`, `spielstaende`, `spielstand_archiv`, `spielzeit`, `zeitbasis`, `spieldaten`, `spielschicht`, `tor`, `public_start` |
| Sonstiges | `gildenrangliste_original`, `spielerhilfe`, `admin_teststand`, `admin_werkzeuge`, `gpt_versorgungsdiagnose`, `menue_original` |

### 5.3 Regeln, die jede Aenderung binden (aus Fehlern gelernt)

- **Eine Groesse hat EINEN Speicher.** Armee je Dorf, Vorraete je Ort, Ausbildung in der Warteschlange
  des Ortes. Wer den Kern rechnen laesst und daneben selbst bucht, bucht doppelt.
- **Feld gegen Eigenschaft:** `asdict()` laesst Eigenschaften weg (nichts wird gespeichert),
  `BotPlayer(**daten)` kennt alte Schluessel nicht mehr. Alten Schluessel beim Laden entfernen, neuen
  ueber den Setter setzen.
- **Alte Spielstaende laden ohne Migration.** Fehlende Schluessel mit Standardwert lesen, nie still
  schreiben.
- **Rundung:** Ressourcen und Einheiten mit `int()` oder `math.floor()` deckeln, nie negativ;
  Bruchteile nur dort, wo eine Anzeige sie ausdruecklich will.
- **Zaehlweisen nicht mischen** (Index 0..n gegen Nummer 1..n) - Umrechnung an EINER Stelle, Grenzen
  als Wache.
- **Quellwachen schneiden Docstring und Kommentar ab**, sonst trifft die Wache den eigenen Kommentar.
- **Pruefdateien sind ASCII** (ein Umlaut im Kommentar reisst den Import); Anzeigetexte in `main.py`
  tragen echte Umlaute.
- Ein Schnitt = ein Commit = ein voller Sammellauf (`tools/sammellauf.py`, 21 bis 22 Minuten,
  183 Dateien, 7.495 Pruefungen).

---

## 6 Der gebaute Stand (06.11.2026)

| Schritt | Inhalt | Zustand |
|---|---|---|
| S0 | `tools/s0_tabellen.py` rechnet fuenf Tabellen aus den Projektdaten (V-1 bis V-5, Abschnitt 7.3) | gebaut, Register 253 |
| S1 | Postfach mit `read`, `archived`, `ablauf_am`, Fristen, Filter, Archiv, Blaettern, Ruhm-Balken | gebaut, Register 250 |
| S1b | Vier Menuegeschichten in `data/story.json`, Einmal-Kennzeichen im Spielstand, Overlay mit einem Knopf | gebaut, Register 251 |
| S2 | Mauerreparatur je Prozentpunkt (Preis V-1, Sperre gegen Ausbau, Kampf bricht ab) | gebaut, Register 252 |
| S3 | Verwundetenheilung (Abschnitt 4.11) | gebaut, Register 257 |
| Block 5 | Verlustbericht als eigener Typ `verlust`; flatternde Kartenwahl-Wache mit festem Startwert geheilt | gebaut, Register 259 |
| Pruefstand | Voller Sammellauf 181 von 183 Dateien gruen, 0 rot, 7.495 Pruefungen, 1.346 Sekunden | belegt, Register 258 |

Zwei Dateien ohne Ergebniszeile laufen mit Rueckgabewert 0 - dieselbe Eigenart wie
`test_rueckmarsch`, kein Fehler.

---

## 7 Der geplante Stand (noch nicht gebaut)

**Diese Abschnitte sind ANGENOMMENER PLAN.** Du sollst sie als gesetzt behandeln und darauf aufbauen.

### 7.1 S4 Teil 1 - Gunst und Status (60 bis 75 Minuten)

Zwei Felder am Bot, gefuehrt ueber `bot_als_dict`/`bot_aus_dict` (nicht als direkter dict-Zugriff -
das war ein Fehler eines frueheren Modellvorschlags). Gunst 0 bis 100, Statusgrenzen
**0 bis 39 feindselig / 40 bis 59 wachsam / 60 bis 100 freundlich**. Eine Anzeigezeile in der
Diplomatie-Ansicht, die dieselbe Funktion liest wie der Kern. Wache: Gunst bleibt in 0..100,
Statusgrenzen an den drei Raendern (39/40, 59/60), alter Spielstand ohne Feld laedt, Anzeige und Kern
gleich. Fertig, wenn Wache und voller Sammellauf gruen sind und Rachetopf und Vertraege unberuehrt
bleiben. Aufbauzeit-Effekt: keiner (Gunst ist eine Zahl, die aus Geschenken und Kaempfen entsteht).

### 7.2 S4 Teil 2 und 3 - Rachetopf, Vertraege, Ereignisse

- **Rachetopf:** +1 je erlittener Niederlage, +1 je Spieltag ohne Kontakt, ab **3** angekuendigter
  Angriff; ein Bot-Sieg senkt die Rache. Schwelle aus V-5 (**90 SK** Wallstufe 3, Reserve 99 SK als
  Vorschlag).
- **Vertraege:** Nichtangriffspakt ab Gunst 40 fuer 3 Spieltage, bricht unter 40 (Bruch kostet genau
  20 Gunst und speist den Rachetopf); Handelsabkommen ueber den vorhandenen Handelsweg
  (`spieloekonomie.handel_start`); Durchmarschrecht ab Gunst 60 ist **reine Anzeige ohne Mechanik**
  (Daniels Entscheidung).
- **Ereignisse** mit Zwei-Spieltage-Frist ueber die vorhandene Overlay-Technik: Haugs Tribut
  (990 Holz **oder** 64 Gold = halber Tagesertrag eines mittleren Dorfes), Groms Handelsangebot
  (5 Werkzeuge gegen 20 Eisen - Warenwert 1:4 ist ein VORSCHLAG), Silras Informationsverkauf
  (12 Gold = ein Zehntel des Gold-Tagesertrags, mindestens 1).
- Wachen: NAP blockiert den Bot-Angriff wirklich (derselbe Weg wie Goetterschutz), Bruch kostet
  genau 20, Ereignis laeuft nach der Frist ab, alter Spielstand laedt.

### 7.3 Die fuenf gerechneten Tabellen (V-1 bis V-5)

**V-1 Mauerreparatur** (gebaut): Preis je Prozentpunkt 16 mal Stufe / 100 fuer Holz und Stein, Dauer
360 Spielsekunden je Punkt. 0 auf 100 Prozent kostet also den Wallpreis mal Stufe und dauert
10 Spielstunden (200 echte Sekunden).

**V-2 Heilungspreis** (gebaut): 75 Prozent der Kostenposten ohne Siedler und ohne Waren, Dauer
50 Prozent. Beispiele: Armbrustschuetze 1.050 Gold, Balliste 450 Holz / 150 Metall / 225 Leder /
7,5 Pferde, Buergerwehr 75 Nahrung / 37,5 Leder / 37,5 Wolle, Krieger 262,5 Gold / 0,75 Pferde,
Handkarren je Posten 11,25.

**V-3 Ruhm-Raenge** (gebaut): 0 Ansiedler, 10 Freisiedler, 40 Fuerst, 160 Herrscher (VORSCHLAG aus
eigener Messung 3,3 Punkte je Spieltag).

**V-4 Ereigniszahlen** (geplant): mittleres Dorf mit 22,3 Steppe, 20,6 Wald, 20,3 Sumpf,
13,6 Grasland, 10,9 Huegel, 10,7 Berg, 1,6 Nebelsee Feldern; Tagesproduktion Holz 1.980, Stein 1.026,
Nahrung 1.720, Gold 128.

**V-5 Rache-Schwelle** (geplant): Wallstufe 3 = 90 SK Fusstruppen (belegte Vorrundentabelle), Rache
greift ab 99 SK (Wallschwelle plus 10 Prozent Reserve).

### 7.4 S5 - Siedlungsumzug (GESPERRT, nicht freigegeben)

Gebaeude und Ausbaustufen ziehen mit um, Kosten in Siedlern und Portalkosten, Zielkarte zufaellig,
die alte Karte geht zurueck in den Vorrat. Wache (geplant): zu wenig Siedler, laufende Auftraege
sperren, alte Karte wieder verfuegbar, Vorraete genau einmal gebucht, Gebaeude unveraendert mitgezogen.

**Sperre:** Daniel hat am 06.11.2026 entschieden, S5 **gesperrt** zu lassen - Bau erst nach
ausdruecklicher Freigabe und gerechnetem Preis. Du darfst die Mechanik durchdenken und die Wache
beschreiben; ein Einbauvorschlag muss als solcher markiert und **nicht** als fertig bezeichnet werden.

---

## 8 Abschlussbedingungen - was "fertig, nur noch Balancing" messbar heisst

Deine Antwort muss diese sieben Bedingungen als **messbare** Zustaende liefern. Eine Bedingung ohne
Zahl, Befehl oder Prueffall gilt als nicht geliefert.

| Nr. | Bedingung | Messung |
|---|---|---|
| A-1 | Alle Spielwege sind ohne Cheats erreichbar | eine E2E-Kette je Weg (Rohstoff, Forschung, Ware, Ausbildung, Einsatz, Rueckkehr, Speichern/Laden) gruen, ohne gesetzte Zustaende |
| A-2 | Jede Ansicht zeigt nur, was der Kern erlaubt | Quellwache: keine zweite Rechenstelle fuer Kosten, Sperren, Gunst, Mengen |
| A-3 | Kein Spielweg endet in einer Sackgasse | Automatenspiel `tools/spieltest_simulation.py` erreicht in 12 Spieltagen Kriegspunkt, Ware, Einheit und ein Gefecht; Abbruchgruende mit Grund im Bericht |
| A-4 | Alte Spielstaende laden | je neuer Feldgruppe ein alter Spielstand ohne Migration, Ladeprobe gruen |
| A-5 | Alle Zahlen sind belegt oder als VORSCHLAG markiert | jede neue Zahl mit Quelle (Handbuch 2009, Seite; 2006er Seite; Datendatei; gerechnete Tabelle) |
| A-6 | Der volle Sammellauf ist gruen | 200 Dateien, 8.874 Pruefungen, 0 rot, Dauer unter 1.200 Sekunden seriell (gemessen 08.11.2026: 1.132 s) - **VORSCHLAG**, Daniel bestaetigt die Grenze (F-2). Mit `tools/sammellauf.py -j 2` gemessen 820 s; das ist der empfohlene Alltagsaufruf, die Vorgabe bleibt 1. |
| A-7 | Balancing ist ohne Codeaenderung steuerbar | jede Balance-Zahl steht in `data/`, ein Schalter je Mechanik, Neustart genuegt |

**Deine Abschlusserklaerung** muss zu jeder Bedingung sagen: erfuellt, mit welchem Beleg (Datei,
Funktion, Prueffall), oder **offen mit Grund**.

---

## 9 Balancing-Werkzeuge: Bestand und was fehlt

### 9.1 Was es gibt (gemessen, `tools/`)

| Werkzeug | Aufgabe | Ergebnis |
|---|---|---|
| `balancing_messung.py` | rechnet aus Daten und Kernfunktionen: Karten-Gelaende, Erträge, Einheitenkosten, Forschung, echte Schlachten (40 Laeufe je Wandstufe), Beute-Staffel, Reisekosten | `docs/SPIELBALANCING_TEST.md` (lebendes Dokument, Gates G-1 bis G-6) |
| `balancing_karten.py` | Karten, Doerfer und Pech getrennt messen | Kartenbefunde je Kategorie |
| `drachen_balancing.py` | Drachenkampf messen | Drachenwerte gegen Ertrag |
| `bot_wirtschaft_messung.py` | Wirtschaft der Bots ueber echte Spieltage | Bot-Wachstum je Spieltag |
| `mess_wirtschaft.py`, `mess_kampf.py` | Einzelmessungen Wirtschaft und Kampf | Messreihen |
| `spieltest_simulation.py` | laesst das Remake **ohne Fenster** spielen und protokolliert | `docs/audits/SPIELTEST_LOG_*.md` |
| `spieltest_paket_bauen.py` | packt einen Verlauf als Paket fuer ein starkes Modell | ZIP unter 8 MB |
| `gesamtaudit_lauf.py` | ein bezahlter Aufruf an ein starkes Modell ueber Dossier und festen Auftrag | Urteil mit Befunden |
| `balancing_gutachten.py` | Balancing-Gutachten mit dem grossen Modell | Textgutachten |
| `s0_tabellen.py` | rechnet die fuenf Tabellen aus den Daten | `docs/S0_TABELLEN_20261107.md` |
| `sammellauf.py` | alle 183 Pruefdateien hintereinander, mit Log | Fortschritt und Ergebnis je Datei |

### 9.2 Was fehlt (dein Auftrag, Teil 2)

Das Spiel soll sich **durch Balancing-Daten und Tester-Feedback selbst verbessern**. Dafuer fehlen
mindestens:

1. **Ein Kennzahlenblatt je Partie** (automatisch): Spieltage bis Meilenstein (erstes Haus, erste
   Bibliothek, erste Ware, erster Krieger, erstes Gefecht, Ruhm-Stufe), Ausgaben je Rohstoff,
   Leerlaufzeiten, gescheiterte Aktionen mit Grund, Handelspunkte, Beute je Feldzug, Verluste je
   Gefecht. Format: eine JSON-Zeile je Partie plus eine Markdown-Zusammenfassung.
2. **Eine Sollkurve** (Zielkorridor je Spieltag fuer Gold, Holz, Nahrung, Einheiten, Punkte) aus den
   Daten gerechnet, nicht getippt - damit ein Lauf gegen ein Ziel gemessen wird und nicht gegen ein
   Gefuehl.
3. **Ein Regelkreis**: Messung, Abweichung von der Sollkurve, Vorschlag mit einer Zahl und einer
   Quelle, A/B-Lauf mit und ohne Aenderung, Urteil. Der Vorschlag darf nur Datenwerte aendern, nie
   Code - sonst ist es kein Balancing.
4. **Tester-Feedback Eingang**: eine Vorlage, die Feedback in messbare Beobachtungen uebersetzt
   (was, wann, mit welchem Stand, welche Zahl), und ein Verfahren, das gleiche Rueckmeldungen
   buendelt, statt sie zu wiederholen.
5. **Ein Abnahmekriterium je Balance-Aenderung**: eine Zahl vorher, eine Zahl nachher, gleiche
   Messreihenfolge, gleicher Startwert.

Liefere zu jedem Punkt: Zweck, Eingaben, Ausgaben, Dateinamen, Aufruf, Beispielausgabe,
Prueffall - so konkret, dass ein Agent es ohne Rueckfrage bauen kann.

---

## 10 DEIN AUFTRAG

**Schritt 1 - Verstehen.** Fasse in eigenen Worten zusammen, was das Spiel ist, wie der Kernkreis
laeuft, welche Mechanik welche Zahl liest und wo die Anzeige den Kern liest. Nenne dabei
ausdruecklich die Stellen, an denen du unsicher bist.

**Schritt 2 - Annehmen.** Uebernimm den Stand aus Abschnitt 6 und den Plan aus Abschnitt 7
**als gesetzt**. Widerspruch ist erlaubt, aber nur als begruendeter Einwand mit Beleg; er ersetzt
nichts stillschweigend.

**Schritt 3 - Konstruieren.** Konstruiere alles, was fehlt, damit das Spiel fertig ist:

- die Restmechaniken (S4 vollstaendig; S5 nur als durchdachter, gesperrter Vorschlag),
- jeden fehlenden Ablauf, den ein Spieler wirklich geht (einschliesslich der Luecken aus 4.7 und 4.9:
  Handelspunkte bleiben 0, Bots haben keine Drachenregel, keine Spionage, keine Reaktion),
- die Balancing-Werkzeuge aus 9.2,
- die Wachen (Prueffaelle) zu allem, was du baust, je Bedingung eine Pruefung, Kern und Anzeige
  getrennt,
- die Datendateien mit **allen** Zahlen und Schaltern.

**Schritt 4 - Liefern.** Liefere in der Form aus Abschnitt 11, mit Ablagehinweisen aus Abschnitt 12.
Das Ergebnis muss so beschaffen sein, dass unser Agent es **fertig zum Ablaufimplementieren**
einsetzen kann: kein Platzhalter, kein "spaeter genauer", keine Rueckfrage an uns.

**Was dein Ergebnis leisten muss:**

- das Spiel ist **komplett** (kein Spielweg fehlt, keiner endet in einer Sackgasse),
- nach deinem Schnitt ist **nur noch Balancing** notwendig (Abschnitt 8 messbar erfuellt),
- das Spiel verbessert sich danach durch **Balancing-Daten und Tester-Feedback** selbst,
- jede Abloesung eines alten Ablaufs ist **ausdruecklich benannt**: was faellt, was bleibt, was
  migriert, mit Begruendung und Beleg. Daniel hat am 06.11.2026 entschieden: Abloesen nur als eigener
  Schnitt mit Beleg und erst nach dem Abgleich mehrerer Modellantworten.

---

## 11 Lieferformat der Antwort

Deine Antwort hat diese acht Teile, in dieser Reihenfolge. Fehlt ein Teil, gilt die Antwort als
unvollstaendig.

1. **Verstaendnis in eigenen Worten** (hoechstens eine Seite): Spiel, Kernkreis, Zeitbasis, wo der
   Kern rechnet und wo die Anzeige liest.
2. **Einwaende und offene Punkte** gegen unseren Stand, je Einwand mit Beleg und Folge.
3. **Schnitte 1 bis n** - je Schnitt ein Block:

   | Feld | Inhalt |
   |---|---|
   | Ziel | was der Schnitt erreicht, in einem Satz |
   | Dateien | anzulegende und zu aendernde Dateien mit Pfad |
   | Aenderung | was genau hineinkommt (Funktion, Signatur, Buchtung, Schalter) |
   | Daten | jede Zahl mit Herkunft: Handbuch 2009 mit Seite, 2006er Seite, Datendatei, gerechnete Tabelle - oder ausdruecklich VORSCHLAG |
   | Wache | die Prueffaelle, je Bedingung einer, mit erwartetem Ergebnis |
   | Fertig-Kriterium | eine Zahl oder ein Zustand, an dem man fertig erkennt |
   | Aufbauzeit-Effekt | senkt, hebt oder laesst die Zeit bis zum ersten Gefecht unveraendert - mit Begruendung |
   | Abloesung | was dieser Schnitt ersetzt, was bleibt, was migriert (oder: keine) |
   | Risiko | was kaputtgehen kann und welche Wache es faengt |

4. **Balancing-Konzept** nach Abschnitt 9.2, mit Dateinamen und Aufrufen.
5. **Abschlusserklaerung** zu A-1 bis A-7: erfuellt oder offen, je mit Beleg.
6. **Reihenfolge der Umsetzung** als nummerierte Liste mit Abhaengigkeiten (was haengt woran).
7. **Was du absichtlich nicht lieferst** und warum.
8. **Ablagehinweise an unseren Agenten** (Abschnitt 12), wortgleich uebernehmbar.

Antworte in **einer** zusammenhaengenden Markdown-Antwort. Wenn du sie in Teile splittest, nummeriere
sie fortlaufend und sage im ersten Teil, wie viele Teile folgen.

---

## 12 Ablage in unserem Ordnersystem (Hinweise, die in deiner Antwort stehen muessen)

Unsere Antwortverwaltung legt jede Modellantwort hashgeprueft ab und indexiert sie. Damit deine
Antwort richtig landet, schreibe am Ende deiner Antwort diesen Block ausdruecklich hin (er darf
angepasst, aber nicht weggelassen werden):

```
Ablage (fuer den Agenten):
- Zieldatei: docs/eingaenge/LLM_<JJJJMMTT>/antworten/Antwort_<MODELL>_AUFTRAG_20261106.md
- Index:     docs/eingaenge/LLM_<JJJJMMTT>/README.md  (Spalten: Datei, Modell, Datum, Teile, Urteil, Quelle)
- Rohform:   unveraendert ablegen, nicht redigieren; SHA256 beim Ablegen bilden und im Index nennen
- Nichts loeschen, nichts ueberschreiben: vorhandene Datei mit gleichem Namen bekommt _2, _3 ...
- Desktop:   die Antwortdatei gehoert NICHT auf den Desktop; nach der Ablage dort nichts liegen lassen
```

Zusaetzlich gilt fuer jede Antwort:

- Sie nennt am Kopf **Modell, Datum, Anzahl Teile** und die **Version dieses Dokuments**
  (`Stand 06.11.2026, V_0.0.3`).
- Sie ist als **eine** Datei abzulegen; Anhaenge nur, wenn sie ohne sie nicht lesbar ist.
- Sie enthaelt **keinen** Verweis auf fluechtige Links (`blob:`, `/mnt/data/`) als Beleg.

---

## 13 Vorsicht: nichts ungeprueft uebernehmen

Das ist die wichtigste Regel unseres Entwicklers, und sie steht ausdruecklich in deiner Antwort:

- **Deine Antwort wird nicht direkt eingebaut.** Zwei bis drei Modelle bearbeiten dieselbe Datei;
  danach gleichen wir die Antworten gegeneinander ab und integrieren die nach unseren Prinzipien
  beste Methode.
- **Jede Zahl aus einer Modellantwort ist bis zum Beleg ein VORSCHLAG.** Beleg heisst: Handbuch 2009
  mit Seite, 2006er Seite, Datendatei oder eine gerechnete Tabelle. Ohne Beleg wird die Zahl nicht
  eingebaut, sondern Daniel vorgelegt.
- **Vier Prueffragen vor jeder Uebernahme:** Passt es zur Mechanik? Ist die Zahl belegt? Hilft es dem
  Spielgefuehl? Braucht es ein neues Bauteil (und wenn ja, warum kein vorhandenes)?
- **Alte Ablaeufe werden nicht stillschweigend ersetzt** (Daniel 06.11.2026): nur als eigener Schnitt
  mit Beleg - was faellt, was bleibt, was migriert.

Formuliere deine Antwort so, dass ein Mensch diese vier Prueffragen je Punkt beantworten kann, ohne
deinen Text umzudeuten.

---

## 14 Harte Regeln fuer deine Vorschlaege

1. **Keine erfundenen Zahlen.** Nur Werte aus Datendateien, aus dem Handbuch 2009 (mit Seite), aus
   den 2006er Seiten oder aus den gerechneten Tabellen. Fehlt ein Wert, schreibe VORSCHLAG und
   begruende die Herleitung.
2. **Kein Wissen ueber andere Spiele einmischen.** Wir bauen eine Neuauflage, keine Mischung.
3. **Kein neues Modul fuer eine geloeste Aufgabe.** Waechst eine Datei, wird reine Rechnung in die
   vorhandene Fachdatei gezogen. Ein neues Modul braucht einen Satz Begruendung.
4. **Anzeige und Kern lesen dieselbe Funktion** - bei Kosten, Sperren, Gunst, Mengen, Dauer.
5. **Texte und Zahlen stehen in `data/`**, nicht im Code; Code und Kommentare ASCII,
   Anzeigetexte deutsch mit echten Umlauten.
6. **Alte Spielstaende laden ohne Migration**; fehlende Schluessel mit Standardwert lesen.
7. **Rundung und Deckel:** `int()` oder `math.floor()`, nie negativ; Bruchteile nur, wo die Anzeige
   sie will (deutsche Schreibweise mit Komma, zwei Stellen).
8. **Ein Schnitt, ein Commit, ein voller Sammellauf.** Ein Vorschlag, der den Sammellauf rot macht,
   ist kein fertiger Schnitt.
9. **Jede neue Mechanik nennt ihren Aufbauzeit-Effekt** (Abschnitt 4.12).
10. **Kein Vorschlag ohne Wache.** Eine Mechanik ohne Prueffall gilt als nicht gebaut.

---

## 15 Glossar der Datendateien

`data/` (46 Dateien, hier die wichtigen):

| Datei | Inhalt |
|---|---|
| `baupreise.json` | Baupreise und Ausbauregeln, je Posten BELEGT oder VORSCHLAG |
| `buildings.json` | Gebaeude, Stufen, Wirkungen, Vorrunden-Schwellen je Wallstufe |
| `resources.json` | Rohstoffe und Ertrag je Gelaende |
| `units.json` | 28 Einheiten mit Kosten, Kampfwerten, Kriegspunkten |
| `unit_stats.json` | abgeleitete Kampfwerte je Einheit |
| `items.json`, `warenrezepte.json` | 17 Waren, Rezepte, Werkstaetten |
| `research.json` | 21 Forschungsgebiete und Freischaltungen |
| `nahrungsverbrauch.json` | 8 Nahrung je Einheit und Spieltag, Schalter `aktiv` |
| `karrenkapazitaet.json` | Wagenbau-Bonus (10 Prozent je Stufe, Deckel 10) |
| `verwundete.json` | 30 / 75 / 50 Prozent der Verwundetenheilung, Schalter `aktiv` |
| `nachrichten.json` | Nachrichtentypen, Kategorien, Fristen |
| `ruhm.json` | Ruhm-Stufen 0 / 10 / 40 / 160 |
| `drachen.json` | Drachenwerte und Beutehort |
| `startkarte.json`, `originalkarten/katalog.json` | Startkarte und 127 Originalkarten |
| `story.json`, `bot_stimmen.json` | Story- und Stimmentexte (kein Text im Code) |
| `welten.json`, `welt_fraktionen.json`, `voelker.json`, `bot_wappen.json` | Welten, Fraktionen, Voelker, Wappen |
| `bot_*.json` (9 Dateien) | Bot-Verhalten: Wirtschaft, Bauplan, Bedarf, Forschung, Gruendung, Raubzug, Diebstahl, Stimmen, Wappen |
| `spieloekonomie.json` | Kernregeln der Wirtschaft (unter anderem Bot-Stufen) |
| `spielzeit.json`, `version.json` | Zeitmodell, Release-Dateiname |
| `boni.json`, `gebaeude_wirkung.json`, `haeuser.json`, `gelaende.json` | Boni, Gebaeudewirkungen, Siedlergrenzen, Gelaenderegeln |
| `trophaeen.json`, `beute_vorrang.json`, `spionage.json` | Trophaeen, Beutereihenfolge, Spionagewerte |

---

## Anhang A - Wo unsere Quellen liegen (nur fuer Menschen)

1. Handbuch 2009: `docs/original/Nebelseetal_Spielanleitung_2009.pdf`, 24 Seiten - **Richtschnur**.
2. Original-Seiten 2006: `docs/original/Spielanleitung_2005/` (16 Seiten, Tabellen vollstaendig
   pipe-getrennt) - Struktur und Entwicklung, Balance nur nach Daniels Entscheidung.
3. Abweichungen 2006 gegen 2009: `docs/quellen/ABWEICHUNGEN_2006_zu_2009.md`.
4. Geprueft und festgehalten: `docs/PRUEFREGEL_ORIGINAL.md` (Register, 259 Eintraege).
5. Gerechnete Tabellen: `docs/S0_TABELLEN_20261107.md` (V-1 bis V-5, jede Zahl mit Rechenweg).
6. Ablaufplan: `docs/ABLAUF_20261107.md` (Schritte, Wachen, Fertig-Kriterien, Aufbauzeit-Effekt).
7. Balancing-Messung: `docs/SPIELBALANCING_TEST.md`, Spieltest-Befunde:
   `docs/SPIELTEST_BEFUNDE_20261105.md`.
8. Repository (Beiwerk, nicht Voraussetzung): https://github.com/Decay03101991/Nebelseetal-Remake
   - Release-Uebersicht: .../releases - juengste Fassung: .../releases/tag/v_0.0.3
   (Pre-Releases sind auf der Uebersicht ausgeblendet, nur ueber den direkten Tag-Link erreichbar).

## Anhang B - Fragen, die DU in deiner Antwort beantworten sollst

1. Welche Mechanik fehlt dem Spiel, damit es **komplett** ist - und woran erkennt man das messbar?
2. Wo ist unser Balancing-Werkzeugkasten zu schwach fuer Selbstverbesserung, und was genau fehlt?
3. Welche unserer geplanten Zahlen (V-1 bis V-5) wuerden das Spielgefuehl verderben, und welche Zahl
   schlaegst du mit welcher Herleitung vor?
4. Welcher alte Ablauf wird durch deinen Vorschlag ueberfluessig - und was muesste migriert werden?
5. Welche drei Pruefungen wuerden deinen eigenen Vorschlag am schnellsten widerlegen?
