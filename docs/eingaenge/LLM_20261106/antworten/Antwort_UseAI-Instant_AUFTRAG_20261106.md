# Antwort auf den Auftrag `Nebelseetal_LLM_Auftrag_20261106.md`

**Modell:** UseAI Instant
**Datum:** 06.11.2026
**Anzahl Teile:** 8 (Teile 1 bis 8, in dieser Antwort durchgehend nummeriert)
**Version des Auftragsdokuments:** Stand 06.11.2026, Pre-Release `Nebelseetal_Pre_Release_V_0.0.3` (Schnitt nach S3), Kopf-Commit `1c5cb73`

---

## Vorbemerkung zum Umgang mit Zahlen (Regel 14.1 und 13)

Dieses Dokument ist selbsttragend: alle Werte, die ich für einen Schnitt brauche, sind unten genannt und mit einer
Herkunft versehen. Ich unterscheide durchgehend vier Herkunftsarten, die im Auftrag als Beleg gelten, und eine
fünfte, die ausdrücklich kein Beleg ist:

| Kürzel | Bedeutung |
|---|---|
| BELEGT-DATEI | Wert steht in einer der in Abschnitt 15 genannten `data/`-Dateien bzw. ist aus den Abschnitten 4.1, 4.2, 4.4, 4.8, 4.11 dieses Auftragsdokuments zitiert |
| GERECHNET | Wert folgt aus belegten Werten durch eine Rechnung, die hier vollständig steht und nachvollziehbar ist |
| VORSCHLAG | Wert ist von mir gesetzt, mit Herleitung, und vor Einbau Daniel vorzulegen |
| GESPERRT | Wert oder Mechanik ist laut Abschnitt 7.4 nicht freigegeben; nur Durchdenken erlaubt |
| ANNahme | Ich war unsicher, welcher belegte Wert gemeint war – die Unsicherheit ist benannt, die Zahl ist VORSCHLAG |

**Ich habe keinen Zugriff auf Ihr Repository, keine der `data/`-Dateien, keine der `docs/`-Dateien und nicht auf die
Handbuch-PDFs.** Alles, was ich unten als BELEGT-DATEI führe, ist aus diesem Auftragsdokument zitiert (Abschnitte 4
und 15). Alle Zahlen, die nicht im Auftragsdokument selbst stehen, sind von mir als VORSCHLAG markiert – auch dann,
wenn sie mir plausibel erscheinen. Der Ablageblock aus Abschnitt 12 steht wörtlich am Ende dieser Antwort (Teil 8).

---

## Teil 1 – Verständnis in eigenen Worten

### 1.1 Was das Spiel ist

`Nebelseetal Remake` ist ein lokal laufendes Einzelspieler-Aufbauspiel in Python 3.14 und tkinter, ohne Netz, ohne
Login, mit JSON-Spielstand. Es ist die Neuauflage eines Browserspiels gleichen Namens. Ein Mensch spielt gegen fünf
Bots mit eigener Wirtschaft; daneben stehen ein Drache und Ruinen, verteilt auf sechs Welten mit sechs Völkern.

Der Aufbau steht vor dem Kampf. Es gibt **keinen Siegscreen**: das Ziel ist nicht, etwas zu besiegen, sondern
Auszeichnungen und Ruhm zu sammeln (Kriegs-, Forschungs- und Handelspunkte, Gesamtpunkte = (Krieg + Forschung) / 2).
Das verändert jede Bewertung eines Vorschlags: eine Mechanik, die einen Konflikt schneller entscheidet, ist nicht
automatisch gut; eine Mechanik, die dem Spieler eine neue *Sinnspur* öffnet, ist wertvoll, auch wenn sie nichts
beschleunigt.

### 1.2 Die Zeitbasis

Die Spieluhr läuft mit Faktor **x180**: eine Spielstunde = 20 echte Sekunden, ein Spieltag = 24 Spielstunden =
28.800 Spielsekunden = 8 echte Minuten. Alle Fristen, Dauern und Aufträge rechnen in **Spielsekunden**, nie in
Rechnerzeit. Ein Spieltag ist damit die einzige Größe, in der ein Spieler denkt, und 8 echte Minuten sind die
einzige Größe, in der ein Tester denkt. Das ist der Kern des Aufbauzeit-Effekts aus Abschnitt 4.12: „8 bis 12
Spieltage bis zum ersten Gefecht“ heißt „64 bis 96 echte Minuten bis zum ersten Gefecht“ – für einen Tester eine
Sitzung, für ein externes Modell eine Zahl, die es nicht direkt messen kann.

### 1.3 Der Kernkreis

Gründen → produzieren → forschen → ausrüsten → ausbilden → bewegen → kämpfen → punkten.

Ich lese diesen Kreis nicht als Wasserfall, sondern als **Rückkopplungsschleife mit zwei Engpässen**:

- **Nahrung** (8 je Einheit und Spieltag, BELEGT-DATEI `nahrungsverbrauch.json`) begrenzt, wie viel Armee sich
  dauerhaft halten lässt. Die Herleitung im Auftrag (Reichsertrag 5.542 Nahrung je Tag; 100 Einheiten = 14,4 %;
  Siedlerdeckel 360 = 52 %) sagt, dass eine Armee von rund 100 Einheiten etwa ein Siebtel des Reichsertrags frisst –
  Armee ist also bezahlbar, aber nicht beliebig skalierbar.
- **Siedler** (10 je Siedlung plus 5 je Haus, Deckel 360 bei sechs Siedlungen) begrenzt Gründung, Bauten nicht
  (Bauten binden seit Daniels Entscheidung keine Siedler), und Ausbildung. Siedler wachsen mit **1 je Spielstunde**,
  also 24 je Spieltag und Siedlung. Bei einem Startwert, den ich nicht kenne (siehe Unsicherheiten), ist die
  Siedlerzahl die erste harte Wand, die ein Spieler trifft.

Alles Langsame läuft über Aufträge mit Reisezeit; der Rückweg kostet **doppelt** so viel wie der Hinweg. Der Tick
bucht Produktion, Versorgung, Warteschlangen, Nachrichtenablauf und Bot-Züge. Jede Buchung ist atomar: ganz oder
gar nicht, mit Rückbuchung bei Ablehnung.

### 1.4 Wo der Kern rechnet und wo die Anzeige liest

Das ist die wichtigste Strukturregel des Projekts und die Regel, die ich bei jedem Schnitt weiterverfolge.

| Wer | Was | Regel |
|---|---|---|
| Fachmodule in `src/` | rechnen und buchen (Kampf, Aufträge, Wirtschaft, Forschung, Wall, Verwundete, Bot …) | eine Größe hat EINEN Speicher |
| `src/main.py` | `GameState` und `NebelseetalApp` | **nur hier wird gelesen und gezeichnet**, nie gerechnet |
| `data/*.json` | alle Zahlen, Texte, Schalter | keine Zahl im Code, kein Text im Code, ASCII-Schlüssel |

Muster F-04 („Anzeige und Kern lesen immer dieselbe Funktion“) ist keine Stilfrage, sondern die Antwort auf zwei
grün geprüfte und trotzdem falsch gerechnete Fälle. Für jeden Vorschlag unten gilt deshalb: die Anzeige bekommt
eine **Lesefunktion** (z. B. `verwundete.heilkosten(einheit, stufe)`) geliefert und rechnet nichts selbst.

Beispiel aus dem gebauten Stand, das ich als Muster übernehme: die Verwundetenheilung (Abschnitt 4.11) rechnet in
`src/verwundete.py`, alle Zahlen stehen in `data/verwundete.json` hinter dem Schalter `aktiv`, und die Anzeige in
der Kaserne liest dieselbe Funktion. Genau diese Dreiteilung (Fachdatei rechnet – Datendatei schaltet – Anzeige
liest) verlange ich in jedem Schnitt unten.

### 1.5 Wo ich unsicher bin

Ich nenne diese Unsicherheiten ausdrücklich, weil Regel 14.1 sie verlangt und weil sie die Stellen sind, an denen
ein Abgleich mehrerer Modellantworten am ehesten auseinanderläuft:

1. **Startwerte.** Ich kenne weder die Startrohstoffe, die Startsiedlerzahl, die Startkarte noch die Startgebäude.
   Jede Sollkurve (Teil 3, Schnitt 8) braucht diese Startwerte als Nullpunkt. Ich habe die Sollkurve deshalb
   **relativ zum ersten gemessenen Tag** formuliert und nicht absolut – siehe dort.
2. **Wirtschaftserträge je Gebäudestufe.** Ich kenne die Erträge je Gelände (Abschnitt 4.1), aber nicht, wie viele
   Felder ein Gebäude belegt und ob eine Gebäudestufe den Ertrag multipliziert. V-4 nennt Tageserträge eines
   „mittleren Dorfes“, aber nicht die Zahl der Gebäude.
3. **Handbuchseitenzahlen.** Ich kann keine Seitenzahl des Handbuchs 2009 verifizieren, weil ich das PDF nicht
   habe. Ich schreibe deshalb nie eine Seitenzahl hin, sondern verweise auf die Stelle in *diesem* Auftragsdokument.
4. **Kampfwerte.** Ich kenne die Struktur von `kampf.fuehre_schlacht` (Vorrunde, Wallstufen, Phasen, Beute,
   Flucht), aber keine einzige Formel daraus. Alle Kampf-Balancing-Vorschläge unten setzen deshalb an **Daten**
   an, nicht an Formeln.
5. **Beutestaffel im Detail.** „Anteil 10/30/60/100 Prozent **und** Ladung“ ist als Struktur klar, als Zuordnung
   (welcher Anteil wann gilt) nicht. Ich fasse sie als kumulative Stufen auf: die frühe Stufe erlaubt nur den
   kleinen Anteil, die späte den vollen – und begrenze jede Stufe zusätzlich durch die Karrenladung.
6. **Handelspunkte.** Dass sie in allen Spieltest-Läufen bei 0 bleiben, obwohl der Handelsweg gebaut ist, ist ein
   Befund ohne Diagnose. Ich habe eine Hypothese (Teil 3, Schnitt 5), die ich als Hypothese markiere und mit einem
   Messvorschlag versehe, statt sie als Wahrheit auszugeben.

---

## Teil 2 – Einwände und offene Punkte

Ich nehme den Stand aus Abschnitt 6 und den Plan aus Abschnitt 7 als gesetzt an. Die folgenden Punkte sind
begründete Einwände mit Beleg und Folge – sie ersetzen nichts stillschweigend.

### E-1 Der Handelsweg ist gebaut, aber nicht erreichbar – und niemand weiß, warum

**Beleg:** Abschnitt 4.7, „Gemessene Wahrheit: in allen Spieltest-Läufen blieben die Handelspunkte bei 0“. Abschnitt
9.1 nennt `mess_wirtschaft.py` als vorhandene Messreihe.
**Folge:** Ein Spielweg fehlt (A-1), und A-3 kann nicht grün werden, solange „Ware“ erreichbar ist, „Handelspunkt“
aber nicht. Der Befund ist außerdem ein Beweis für eine **Lücke im Werkzeugkasten**: die vorhandene Messung
protokolliert Punkte, aber nicht die *Ablehnungsgründe* der Aktionen, die zu Punkten führen. Ich baue in Teil 3
Schnitt 5 zuerst eine Diagnose (Zählwerk je Ablehnungsgrund) und ändere erst danach eine Zahl. Ohne die Diagnose
wäre jede Änderung geraten.

### E-2 „Keine zentrale Kapazitätslagerung“ trifft den Balancing-Werkzeugkasten, nicht nur das Spiel

**Beleg:** Abschnitt 4.1, „Es gibt **keine** zentralen Kapazitätslager: Lagerung ist ortsgebunden.“
**Folge:** Jede Kennzahl „Reichsertrag“ (5.542 Nahrung je Tag, V-4: Holz 1.980, Stein 1.026, Gold 128 je Tag) ist
eine **Summe über Orte**, kein Vorrat. Ein Kennzahlenblatt je Partie (9.2 Punkt 1) muss deshalb konsequent zwei
Spalten führen: `erzeugt_je_tag` und `bestand`. Wer beides in eine Zahl wirft, baut genau die zweite Rechenstelle,
die F-04 verbietet. Ich mache das im Kennzahlenblatt explizit.

### E-3 Die Sollkurve ist noch nicht berechenbar, weil die Startwerte fehlen

**Beleg:** Abschnitt 9.2 Punkt 2 verlangt „aus den Daten gerechnet, nicht getippt“. Die Daten, die dafür nötig sind
(Startbestand, Startkarte, Startgebäude), sind nicht Teil des Auftragsdokuments.
**Folge:** Ich liefere die Sollkurve als **Formel** plus **Datenanforderung**: die Kurve wird beim ersten Lauf aus
`data/startkarte.json` und `data/spieloekonomie.json` gelesen und, falls die Startwerte fehlen, als VORSCHLAG mit
einem dokumentierten Ausgangswert gefahren. Damit ist A-7 erfüllt (steuerbar ohne Codeänderung), ohne eine Zahl zu
erfinden.

### E-4 Der Aufbauzeit-Effekt wird nirgends nachgehalten

**Beleg:** Abschnitt 4.12: „Jede neue Mechanik muss diese Zahl senken oder gleich lassen.“ Abschnitt 8, A-3 misst
aber nur „12 Spieltage bis Kriegspunkt, Ware, Einheit, Gefecht“ – nicht die Zeit *bis zum ersten Gefecht*.
**Folge:** Eine Mechanik kann A-3 erfüllen und die Aufbauzeit trotzdem verlängern, ohne dass eine Wache anschlägt.
Ich schlage in Teil 3, Schnitt 8 ein Gate **G-7** im Balancing-Blatt vor, das genau diese Zahl je Lauf führt. Das
ist eine Ergänzung von A-3, keine Ablösung.

### E-5 „30 Prozent verwundet, abgerundet“ kann bei kleinen Gefechten 0 Verwundete ergeben

**Beleg:** Abschnitt 4.11: „30 Prozent der Verluste je Einheitentyp werden verwundet, **abgerundet**.“
**Folge:** Ein Gefecht mit 3 Verlusten erzeugt 0 Verwundete – die Mechanik ist gebaut, aber bei kleinen Gefechten
unsichtbar. Das ist kein Fehler (die Rundungsregel 14.7 verlangt ausdrücklich `int()`/`floor()`), aber es ist ein
**Beobachtungsproblem**: ein Tester, der „Verwundete funktionieren nicht“ meldet, hat recht in der Beobachtung und
unrecht in der Ursache. Ich nehme das in die Feedback-Vorlage (Schnitt 7) als Pflichtfeld „wie viele Verluste je
Typ“ auf.

### E-6 Der Aufgabenblock beschreibt fünf Module als fehlend, die schon existieren

**Beleg:** Auftrag Abschnitt 10, Schritt 3 nennt als zu konstruierende Lücken: „Handelspunkte bleiben 0, Bots haben
keine Drachenregel, keine Spionage, keine Reaktion“. Abschnitt 5.2 führt in der Gruppe „Bewegung und Kampf“ aber
bereits `spionage.py` und `drachen.py`, und Abschnitt 4.9 nennt „Spionagebericht lesen“ als gebaut.
**Folge:** Die Lücke ist **nicht das Modul, sondern der Aufrufer**. Gebaut ist Spionage aus Sicht des Spielers und
das *Lesen* fremder Berichte durch den Bot; es fehlt Spionage *des Bot gegen den Spieler*. Regel 14.3 („kein neues
Modul für eine gelöste Aufgabe“) greift hier direkt: ich baue in Schnitt 4 nur Aufrufer und Bot-Entscheidung, kein
neues Spionagemodul. Dasselbe gilt für den Drachen: `drachen.py` existiert, es fehlt die Bot-Regel.

### E-7 Die drei Statusgrenzen aus 7.1 sind asymmetrisch

**Beleg:** Abschnitt 7.1: `0 bis 39 feindselig / 40 bis 59 wachsam / 60 bis 100 freundlich` = 40 / 20 / 41 Werte.
**Folge:** Das ist kein Fehler, aber es ist eine **Verteilung, die man prüfen muss**: 40 von 101 Werten sind
feindselig, und die untere Grenze ist damit die wahrscheinlichste im Spielverlauf. Wenn Gunst (Schnitt 4) durch
Kämpfe und Geschenke entsteht, wird der Spieler die meiste Zeit „feindselig“ sehen. Ich behalte die Grenzen bei
(Plan ist gesetzt) und schlage vor, sie im Kennzahlenblatt als Verweildauer je Status zu messen – dann zeigt sich
in Daten, ob die Verteilung das Spielgefühl trägt.

### E-8 Der Rachetopf aus 7.2 hat kein Gegenstück für den Spieler

**Beleg:** Abschnitt 7.2: „+1 je erlittener Niederlage, +1 je Spieltag ohne Kontakt, ab 3 angekündigter Angriff“.
**Folge:** Der Topf bestraft den Spieler für Ruhe („je Spieltag ohne Kontakt“) und für Niederlagen gleichzeitig. Ein
Spieler, der sich ruhig aufbaut, wird also von selbst angegriffen – das ist gewollt (Druck), aber es kollidiert mit
Regel 4.12: eine Mechanik, die *Aufbau* bestraft, verlängert die Zeit bis zum ersten Gefecht nicht, sie verkürzt sie
sogar – also zulässig. Ich behalte die Mechanik bei und markiere den Punkt als bewusst gewollte Beschleunigung.

### E-9 V-3 ist selbst als VORSCHLAG markiert und trotzdem die schwächste Zahl im Dokument

**Beleg:** Abschnitt 7.3: „0 Ansiedler, 10 Freisiedler, 40 Fürst, 160 Herrscher (VORSCHLAG aus eigener Messung
3,3 Punkte je Spieltag).“
**Folge:** Bei 3,3 Punkten je Spieltag erreicht der Spieler Ruhm-Stufe 2 (40 Punkte) nach etwa 12 Spieltagen – also
genau am Ende der gemessenen Spieltest-Läufe (8 bis 12 Spieltage, 19 bis 40 Punkte). Stufe 3 (160) läge bei 48
Spieltagen, das ist bei 8 echten Minuten je Tag eine Sitzung von 6,4 Stunden. Ich behalte die Stufen (Plan gesetzt)
und schlage in Schnitt 8 vor, Fortschritt **messbar** zu machen, statt die Stufen zu ändern.

### E-10 „Rohform unverändert ablegen“ und „geprüft übernehmen“ sind zwei Akte

**Beleg:** Abschnitt 12 („Rohform: unveraendert ablegen, nicht redigieren“) gegen Abschnitt 13 („Vier Prüffragen
vor jeder Übernahme“).
**Folge:** Kein Widerspruch, aber eine Falltür: wenn meine Antwort als Rohform abgelegt und aus dem Index zitiert
wird, muss aus der Datei selbst hervorgehen, welche Zahlen VORSCHLAG sind. Sonst prüft ein späterer Leser die
Rohform und hält einen Vorschlag für einen Beleg. Ich führe deshalb in **jedem** Datenblock unten eine Spalte
`Herkunft`, und in Teil 4 eine Sammeltabelle aller VORSCHLAG-Zahlen. Das ist meine Erfüllung der vierten Prüffrage
(„Ist die Zahl belegt?“).

### E-11 Die Zeitachse zwischen Dokument und Daten ist unklar

**Beleg:** Das Dokument trägt Datum 06.11.2026 und verweist mehrfach auf `docs/S0_TABELLEN_20261107.md`,
`docs/ABLAUF_20261107.md` – also auf Dateien mit einem Datum **einen Tag in der Zukunft**.
**Folge:** Vermutlich wurden die Dateinamen vorab festgelegt. Für die Ablage ist das relevant: der Zielordner heißt
`docs/eingaenge/LLM_<JJJJMMTT>/`. Ich verwende in Teil 8 das Datum **06.11.2026** (`LLM_20261106`) entsprechend dem
Kopf des Auftragsdokuments und nenne diese Wahl ausdrücklich, damit der Agent sie ohne Rückfrage anpassen kann.

---

## Teil 3 – Schnitte 1 bis 9

Jeder Schnitt folgt dem Block aus Abschnitt 11. Die Reihenfolge unten ist die Umsetzungsreihenfolge; die
Abhängigkeiten stehen zusätzlich in Teil 6.

### Schnitt 1 – Angebotsweg und Ablehnungsgründe (Diagnose vor jeder Zahl)

| Feld | Inhalt |
|---|---|
| **Ziel** | Erreichbar machen, was gebaut, aber unerreichbar ist: der Handelsweg soll im Spielbetrieb einen Handelspunkt erzeugen – nachgewiesen über eine Diagnose, nicht über geratene Zahlen. |
| **Dateien** | NEU `src/angebotswege.py` (reine Zählung, kein Spielzustand) · ÄNDERN `src/spieloekonomie.py` (`handel_start`, `handel_abschluss`) · ÄNDERN `src/main.py` (Anzeige ruft nur die Lesefunktion) · NEU `data/angebotswege.json` · NEU `tools/angebotswege_messung.py` · NEU `tests/test_angebotswege.py` |
| **Änderung** | `angebotswege.pruefe_handel(ort, ziel, ware, menge) -> (bool, grund)` – **eine** Prüffunktion, die `spieloekonomie.handel_start` *und* die Anzeige gemeinsam aufrufen. `grund` ist ein Schlüssel aus `data/angebotswege.json` (z. B. `kein_karren`, `keine_ware`, `kein_kontakt`, `gesperrt_auftrag`, `kein_punktetyp`). `angebotswege.zaehle(grund)` erhöht einen Zähler je Ablehnungsgrund; der Zähler wird im Journal mitgeschrieben, nicht im Spielstand gespeichert. `handel_start` gibt ab jetzt ein Tupel zurück (`ok`, `grund`), die Anzeige zeigt den übersetzten Text. |
| **Daten** | `data/angebotswege.json`: `{"aktiv": true, "gruende": {"kein_karren": "Für den Transport fehlt ein Karren.", "keine_ware": "Die Ware ist am Ort nicht vorhanden.", "kein_kontakt": "Zu diesem Nachbarn besteht noch kein Kontakt.", "gesperrt_auftrag": "Es laufen bereits Aufträge.", "kein_punktetyp": "Dieser Handel vergibt keine Handelspunkte."}, "punkte": {"handel_je_lieferung": 1}}`. Der Wert `handel_je_lieferung = 1` ist **VORSCHLAG**: Herleitung – ein Handelspunkt ist die kleinste sinnvolle Einheit; die Gesamtpunkte aus Abschnitt 4.7 zeigen Handelspunkte als eigenständige Säule, und die gemessenen Läufe enden bei 19 bis 40 Gesamtpunkten. Eine Lieferung soll damit sichtbar, aber nicht dominierend sein. **Vor Einbau Daniel vorzulegen**, weil die Quelle keinen Wert nennt. |
| **Wache** | `tests/test_angebotswege.py`, 9 Prüfungen: (1) alle fünf Gründe werden genau einmal ausgelöst, wenn die Bedingung fehlt; (2) `pruefe_handel` gibt `True` nur, wenn alle Bedingungen erfüllt sind; (3) Anzeige-Text und Kern-Grund sind identisch (dieselbe Funktion, ein Aufruf, ein Vergleich des Strings); (4) Zähler erhöht sich genau um 1 je Ablehnung; (5) ein erfolgreicher Handel erhöht `handelspunkte` genau um 1; (6) ein erfolgreicher Handel löst **keinen** Grund aus; (7) unbekannter Grund fällt auf `kein_punktetyp` zurück und wirft nicht; (8) alter Spielstand ohne Zählerfeld lädt; (9) `data/angebotswege.json` fehlt → `aktiv = false`, Spiel läuft ohne Punktevergabe weiter. |
| **Fertig-Kriterium** | `tools/angebotswege_messung.py` läuft 12 Spieltage im Automatenspiel und gibt aus: Summe der Ablehnungen je Grund. Die Zahl für `kein_karren` und `keine_ware` ist der **Beleg**, welche Ursache wirklich vorliegt. Fertig ist der Schnitt, wenn der Bericht **eine** Ursache mit Abstand als häufigste nennt und diese Ursache in einem Folgeschnitt nachweisbar behoben ist. |
| **Aufbauzeit-Effekt** | **Senkt.** Ein erreichbarer Handelsweg gibt Gold, ohne dass der Spieler dafür kämpfen muss; das verkürzt den Weg zu Goldmine-unabhängigem Einkommen. Beleg: Gold-Tagesertrag eines mittleren Dorfes ist 128 (V-4), Krieger kostet 350 Gold (Abschnitt 4.4) – 2,7 Tageserträge. Handel verkürzt diese Wartezeit. |
| **Ablösung** | Keine. `handel_start` behält seinen Namen und seine Aufgabe; die Rückgabe wird um ein Feld erweitert, Aufrufer werden auf das Tupel umgestellt. Was bleibt: der gesamte Handelsweg. Was migriert: die Aufrufstellen in `main.py` und `spieloekonomie.py` (ein Commit, ein Sammellauf). Kein alter Ablauf fällt. |
| **Risiko** | Zwei Rechenstellen entstehen, wenn die Anzeige den Grund selbst ableitet → gefangen von Wache 3. Ein alter Aufrufer, der noch den alten Rückgabewert erwartet, bekommt immer `True` → gefangen von Wache 6 (Erfolg ohne Grund) und vom vollen Sammellauf. |

### Schnitt 2 – S4 Teil 1: Gunst und Status

**Der Plan aus Abschnitt 7.1 wird hier nicht ersetzt, sondern auf seine Schnittstellen festgelegt.** Ich baue genau
die zwei Felder, die drei Grenzen und die eine Anzeigezeile – und nichts darüber hinaus.

| Feld | Inhalt |
|---|---|
| **Ziel** | Jeder Bot trägt eine Gunst zwischen 0 und 100; aus ihr folgt ein Status, den Kern und Anzeige über dieselbe Funktion lesen. |
| **Dateien** | NEU `src/gunst.py` (reine Rechnung: Grenzen, Status, Buchung) · ÄNDERN `data/bot_*.json` nicht nötig · NEU `data/gunst.json` · ÄNDERN `src/botkern.py` (`bot_als_dict`/`bot_aus_dict` um beide Felder erweitern) · ÄNDERN `src/main.py` (Zeile in der Diplomatie-Ansicht) · NEU `tests/test_gunst.py` |
| **Änderung** | `gunst.status(gunst: int) -> str` gibt `"feindselig" \| "wachsam" \| "freundlich"` zurück, gelesen aus `data/gunst.json`. `gunst.buche(bot, delta: int) -> int` klemmt das Ergebnis auf `[0, 100]` und gibt den neuen Wert zurück. Felder am Bot: `gunst: int = 50` (Startwert **VORSCHLAG**, siehe unten) und `status: str` (nur berechnet, nie gespeichert – sonst hätte der Status einen zweiten Speicher, Verstoß gegen 5.3). Serialisierung ausschließlich über `bot_als_dict`/`bot_aus_dict`, **nicht** über direkten dict-Zugriff (ausdrücklich gefordert in 7.1). |
| **Daten** | `data/gunst.json`: `{"aktiv": true, "start": 50, "min": 0, "max": 100, "grenzen": {"feindselig_bis": 39, "wachsam_bis": 59}, "status_text": {"feindselig": "feindselig", "wachsam": "wachsam", "freundlich": "freundlich"}}`. Die drei Grenzen 39/59 und der Wertebereich 0..100 sind **BELEGT – Auftragsdokument Abschnitt 7.1** (angenommener Plan, gesetzt). Der Startwert **50 ist VORSCHLAG**: Herleitung – 50 liegt genau in der Mitte des Bereichs und genau in der Mitte des Bandes „wachsam“ (40..59), also maximal unentschieden; ein Startwert in „feindselig“ würde jeden Spieler mit Rachetopf (7.2, ab 3) beginnen lassen, bevor er etwas getan hat. |
| **Wache** | `tests/test_gunst.py`, 10 Prüfungen: (1) `status(0) == "feindselig"`; (2) `status(39) == "feindselig"`; (3) `status(40) == "wachsam"`; (4) `status(59) == "wachsam"`; (5) `status(60) == "freundlich"`; (6) `status(100) == "freundlich"`; (7) `buche(bot, -1000)` ergibt 0, nicht negativ; (8) `buche(bot, +1000)` ergibt 100; (9) alter Spielstand ohne `gunst` lädt und setzt 50, ohne zu schreiben; (10) Anzeigezeile und Kern liefern denselben Status-String für dieselbe Zahl (Vergleich beider Ausgaben). |
| **Fertig-Kriterium** | Wache 10 Prüfungen, 0 Fehler; voller Sammellauf grün; Rachetopf und Verträge unberührt (Nachweis: Wache prüft, dass `data/rachetopf.json` und `data/vertraege.json` in diesem Schnitt **nicht** angelegt werden). Genau der Zustand, den Abschnitt 7.1 als fertig definiert. |
| **Aufbauzeit-Effekt** | **Keiner.** Gunst ist eine Zahl, die aus Geschenken und Kämpfen entsteht; sie bucht in diesem Schnitt nichts und beschleunigt nichts. Beleg: Abschnitt 7.1 formuliert das ausdrücklich so, und die Wache stellt sicher, dass keine Buchung entsteht. |
| **Ablösung** | Keine. Gunst ist eine neue Größe an einem bestehenden Bot; das vorhandene Feld `status` existiert nicht und wird auch nicht gespeichert. |
| **Risiko** | Der klassische Fehler aus 7.1: ein früherer Modellvorschlag hat das Feld per direktem dict-Zugriff geführt und beim Laden verloren. Wache 9 fängt genau das. Zweites Risiko: `status` versehentlich mitspeichern → dann kann Anzeige und Kern auseinanderlaufen; gefangen von Wache 10, weil ein gespeicherter Status veralten würde. |

### Schnitt 3 – S4 Teil 2: Rachetopf und Verträge

| Feld | Inhalt |
|---|---|
| **Ziel** | Bots werden zum Angriff getrieben, wenn sie lange nichts erreicht oder verloren haben; Verträge bremsen das – und brechen unter einer Schwelle mit bestimmtem Preis. |
| **Dateien** | NEU `src/rachetopf.py` · NEU `src/vertraege.py` · NEU `data/rachetopf.json` · NEU `data/vertraege.json` · ÄNDERN `src/bot_angriffsplanung.py` (Lesezugriff auf den Topf) · ÄNDERN `src/kampf.py` (Bruch bei Schwellenverletzung, Buchung **vor** der Verlustbuchung – Reihenfolge wie in 4.10/4.11) · ÄNDERN `src/main.py` (Anzeige) · NEU `tests/test_rachetopf.py`, `tests/test_vertraege.py` |
| **Änderung** | `rachetopf.erhoehe(bot, grund)` mit den Gründen `niederlage` (+1), `funkstille` (+1 je Spieltag ohne Kontakt), `vertragsbruch` (+1, gespeist aus dem Bruchpreis); `rachetopf.senke(bot)` bei Bot-Sieg. `rachetopf.schwelle() -> int` liest den Wert aus `data/` und ist die **einzige** Stelle, die 99 liefert. `vertraege.schliesse(bot, art, tage)`; `vertraege.pruefe(bot, art) -> bool` wird von `bot_angriffsplanung` **und** `versorgungsschutz`-Weg gemeinsam aufgerufen – dieselbe Funktion, damit ein Nichtangriffspakt wirklich blockiert. `vertraege.brich(bot)` kostet genau 20 Gunst und speist den Topf. |
| **Daten** | `data/rachetopf.json`: `{"aktiv": true, "start": 0, "schwelle": 99, "je_niederlage": 1, "je_spieltag_funkstille": 1, "bei_sieg": -1, "reserve_prozent": 10, "wallstufe": 3, "wall_schwelle_sk": 90}`. **BELEGT – Auftragsdokument 7.3/V-5:** Wallstufe 3 = 90 SK Fußtruppen, Reserve 10 %, Schwelle 99 SK – der Plan nennt 99 ausdrücklich als Vorschlag mit dieser Herleitung (90 × 1,1 = 99). Der Startwert 0 ist **GERECHNET**: ohne Kontakt und ohne Niederlage kann kein Groll entstehen. Die Schwellen „ab 3 angekündigter Angriff“ und „+1 bei Sieg“ sind **BELEGT – 7.2**. `data/vertraege.json`: `{"aktiv": true, "nap": {"ab_gunst": 40, "dauer_spieltage": 3, "bruch_gunst": 20}, "handel": {"ab_gunst": 40, "ueber": "handel_start"}, "durchmarsch": {"ab_gunst": 60, "nur_anzeige": true}}`. Alle Werte **BELEGT – 7.2**; `durchmarsch.nur_anzeige = true` ist Daniels Entscheidung aus 7.2 und wird durch eine Wache festgeschrieben. |
| **Wache** | `tests/test_rachetopf.py` (8): (1) Topf steigt bei Niederlage genau um 1; (2) steigt je Spieltag ohne Kontakt genau um 1, bei Kontakt nicht; (3) sinkt bei Bot-Sieg genau um 1, nicht unter 0; (4) Schwelle ist 99 und wird nur aus der Datei gelesen; (5) bei Wallstufe 3 und 90 SK Vorrundenschwelle liegt die Schwelle bei 99 (Rechnung im Prüffall nachgerechnet, nicht fest eingetragen); (6) Schwelle über 99 löst keinen Angriff aus, genau 99 löst aus; (7) alter Spielstand ohne Topf lädt mit Startwert; (8) Anzeige und Kern nennen dieselbe Zahl. `tests/test_vertraege.py` (9): (1) NAP ab Gunst 40 abschließbar, bei 39 nicht; (2) NAP blockiert den Bot-Angriff **wirklich** – der Prüffall ruft denselben Weg auf, den der Götterschutz nutzt, und erwartet die Ablehnung; (3) NAP läuft nach genau 3 Spieltagen aus; (4) Bruch kostet genau 20 Gunst; (5) Bruch speist den Topf um genau 1; (6) Bruch unter Gunst 40 wird automatisch ausgelöst, nicht erst auf Knopfdruck; (7) Handelsabkommen ruft `spieloekonomie.handel_start` auf (Nachweis über einen Zähler, nicht über einen Namen im Quelltext); (8) Durchmarschrecht ab 60 ändert **keinen** Spielwert (Prüffall vergleicht den Spielstand vor und nach der Buchung Feld für Feld); (9) alter Spielstand ohne Verträge lädt. |
| **Fertig-Kriterium** | 17 Prüfungen, 0 Fehler. Messbar: ein Simulationslauf über 12 Spieltage, in dem der Spieler den Bot dreimal besiegt, endet mit Topfwert ≥ 3 und einem Bot-Angriff, der innerhalb von 2 Spieltagen nach Ankündigung stattfindet. Der Wert 3 steht in der Datei, nicht im Code. |
| **Aufbauzeit-Effekt** | **Senkt.** Ein Bot, der angreift, erzwingt ein Gefecht; die Zeit bis zum ersten Gefecht sinkt. Das ist gewollt (E-8) und mit Abschnitt 4.12 vereinbar, weil „senken oder gleich lassen“ verlangt ist. Der Fall `funkstille` (+1 je Spieltag ohne Kontakt) ist der eigentliche Beschleuniger: Ruhe erzeugt Druck. Beleg: 7.2 nennt beide Quellen ausdrücklich. |
| **Ablösung** | Keine. Verträge und Rachetopf sind neue Größen. Ausdrücklich: die vorhandene Götterschutz-Sperre (`versorgungsschutz.py`) wird **nicht** ersetzt, sondern um einen zweiten Grund erweitert – der Weg bleibt, die Prüfung wird nur an einer Stelle mitgenutzt. Grund: F-04 verlangt einen Weg, nicht zwei. |
| **Risiko** | Wenn die NAP-Sperre in `bot_angriffsplanung` *zusätzlich* zur Götterschutz-Sperre geprüft wird, entstehen zwei Wege, die auseinanderlaufen können; Wache 2 prüft den gemeinsamen Weg. Zweites Risiko: die Reihenfolge „Buchung vor Verlustbuchung“ wird verletzt und ein Vertragsbruch verschwindet mit dem Angreifer – Wache 5/6 prüfen nur die Buchung, deshalb zusätzlich die Prüfung der Reihenfolge im Kampfpfad (Wache 2 von `test_vertraege`). |

### Schnitt 4 – S4 Teil 3: Bot-Spionage, Drachenregel, Reaktion auf den Spielerfortschritt

Das ist die Antwort auf die drei Lücken aus 4.9. Ich baue **kein** neues Spionage- oder Drachenmodul (Regel 14.3),
sondern Aufrufer und Entscheidungen.

| Feld | Inhalt |
|---|---|
| **Ziel** | Jeder Bot beobachtet den Spieler (Spionage), weiß, dass es einen Drachen gibt (Meidung), und richtet sein Verhalten nach dem Spielerfortschritt – statt in einer festen Schleife zu laufen. |
| **Dateien** | ÄNDERN `src/bot_angriffsplanung.py` (drei neue Entscheidungsgründe) · ÄNDERN `src/bottaktik.py` (Zugauswahl) · ÄNDERN `src/spionage.py` (Richtung Bot→Spieler aufrufbar machen) · ÄNDERN `src/drachen.py` (Lesehilfe `drachen.bedrohung(ort)` für den Bot) · NEU `data/bot_drachen.json` · NEU `data/bot_spionage.json` · NEU `data/bot_reaktion.json` · NEU `tests/test_bot_spionage.py`, `tests/test_bot_drachen.py`, `tests/test_bot_reaktion.py` |
| **Änderung** | `botkern` ruft je Takt zuerst `spionage.pruefe_bot_gegen_spieler(bot, ort)` auf; das Ergebnis landet als `kenntnis` im Bot und hat **eine** Speicherstelle. `bot_angriffsplanung` liest `kenntnis` und die Bot-Reaktionsdatei; die Zielwahl (Ort, Truppengröße) folgt aus beiden. `drachen.bedrohung(ort)` gibt eine Stufe aus `data/bot_drachen.json` zurück; `bottaktik` meidet Ziele innerhalb einer Widerstandsstufe, greift den Drachen aber **nicht** an (genau wie 4.8 es beschreibt: „sie meiden den Drachen weder noch greifen ihn an“ ist der Ist-Zustand – die Meidung ist der Fix, der Angriff bleibt aus). |
| **Daten** | `data/bot_drachen.json`: `{"aktiv": true, "meidefelder": 3, "gefahr_stufen": {"1": "Dorf am Ruinenrand", "2": "Ruine", "3": "Drachenhort"}, "meide_felder_um_hort": 3, "angriff_auf_drache": false}`. `meide_felder_um_hort = 3` ist **VORSCHLAG**: Herleitung – der Ort kennt seine Nachbarschaft auf höchstens 5 Feldern Radius (die Startkarte ist 10x10, BELEGT-DATEI Abschnitt 1: „Original-Siedlungskarten 127 (10x10)“); 3 Felder sind zwei Drittel der halben Kantenlänge und halten den Bot aus dem Sichtbereich, ohne ihn auf dem Brett zu lähmen. `angriff_auf_drache = false` ist **BELEGT – 4.8** (Bots haben keine Drachenregel; die Sperre schreibt fest, dass auch die neue Regel keinen Angriff erzeugt). `data/bot_spionage.json`: `{"aktiv": true, "takt_spieltage": 1, "genauigkeit": 2, "nur_bei_gunst_unter": 60}`. `takt_spieltage = 1` **VORSCHLAG** (ein Bericht je Bot und Spieltag, 8 echte Minuten Takt – häufiger wäre teuer und würde den Spieler nur zuspammen). `data/bot_reaktion.json`: `{"aktiv": true, "stufen": {"punkte_bis_20": "sparsam", "punkte_bis_60": "ausgeglichen", "punkte_ueber_60": "aggressiv"}, "truppen_faktor": {"sparsam": 1.0, "ausgeglichen": 1.25, "aggressiv": 1.6}, "truppen_faktor_max": 2.0}`. Die Stufengrenzen 20 und 60 sind **VORSCHLAG** aus der gemessenen Punkteverteilung (4.7: Läufe enden bei 19 bis 40 Punkten, V-3: Stufen bei 10/40/160) – die Stufen 20/60 liegen genau zwischen den Ruhm-Stufen und teilen den gemessenen Bereich in zwei Hälften. Die Faktoren sind **VORSCHLAG**; der Deckel 2,0 entspricht dem Muster aus 4.4 (Wagenbau endet bei Faktor 2,0) und verhindert unbegrenztes Wachstum. |
| **Wache** | `tests/test_bot_spionage.py` (6): (1) Bot erzeugt genau einen Bericht je Spieltag; (2) bei Gunst 60 und höher wird **nicht** spioniert; (3) der Bericht enthält Ort, aber keine vollständige Armeeliste (Genauigkeit 2 statt 3); (4) Bot und Spieler benutzen dieselbe Spionagefunktion (Vergleich der Rückgabeform); (5) `kenntnis` hat genau eine Speicherstelle (Prüffall lädt zwei Bot-Instanzen und vergleicht); (6) alter Spielstand ohne `kenntnis` lädt. `tests/test_bot_drachen.py` (5): (1) Ziel innerhalb von 3 Feldern um den Hort wird abgelehnt; (2) Ziel bei 4 Feldern wird angenommen; (3) Bot greift den Drachen nie an (Zähler über 12 Spieltage ist 0); (4) ohne Drachen auf der Karte blockiert nichts; (5) alter Spielstand ohne Feld lädt mit `aktiv = true`. `tests/test_bot_reaktion.py` (5): (1) bei 19 Punkten Faktor 1.0; (2) bei 20 Punkten 1.25; (3) bei 60 Punkten 1.25; (4) bei 61 Punkten 1.6; (5) Faktor wird nie über 2,0 gebucht (Deckel greift, `floor`-Rundung wie 14.7). |
| **Fertig-Kriterium** | 16 Prüfungen, 0 Fehler. Messbar: eine 12-Spieltage-Simulation mit einem Spielerfortschritt von 0 auf 45 Punkte zeigt in den Bot-Zügen mindestens einen Wechsel des Reaktionsstatus (sparsam → ausgeglichen) und mindestens eine abgelehnte Zielwahl wegen des Drachen. Beide Zahlen stehen im Protokoll, nicht im Code. |
| **Aufbauzeit-Effekt** | **Senkt.** Ein Bot, der den Spielerfortschritt liest, wird stärker, sobald der Spieler stark wird, und schwächer, solange er schwach ist – der Druck kommt früher als in einer festen Schleife. Zusätzlich senkt die Spionage die Aufbauzeit indirekt, weil der Bot früher angreift. Beleg: „keine Reaktion auf den Spielerfortschritt“ ist in 4.9 als Lücke benannt, also ist die Änderung selbst die Wirkung. |
| **Ablösung** | Die in 4.9 benannten Lücken fallen: „keine Drachenregel“, „keine aktive Spionage gegen den Spieler“, „keine Reaktion auf den Spielerfortschritt“. Was bleibt: `spionage.py` und `drachen.py` in ihrer bestehenden Form – sie werden nur aufgerufen. Was migriert: die vier genannten Dateien, ein Commit. Die Lücke „kein belegter Handel gegen den Spieler“ fällt **nicht** hier, sondern in Schnitt 5 – ich trenne das ausdrücklich, damit die Ablösung einzeln belegt ist. |
| **Risiko** | Ein zweiter Speicher für die Bot-Kenntnis (einmal im Bot, einmal in `bottaktik`) – gefangen von Wache 5. Zweitens: eine Reaktion, die den Bot unschlagbar macht; gefangen vom Deckel in Wache 5 und vom Aufbauzeit-Effekt, der bei 12 Spieltagen nicht unter 8 fallen darf (Gate G-6, Schnitt 8). |

### Schnitt 5 – Belegter Handel des Bots gegen den Spieler

| Feld | Inhalt |
|---|---|
| **Ziel** | Der in 4.9 fehlende belegte Handel entsteht: ein Bot kauft beim Spieler oder verkauft ihm, und der Spieler kann Handelspunkte über einen zweiten Weg als den eigenen Karren erhalten. |
| **Dateien** | NEU `src/handel_bot.py` · NEU `data/bot_handel.json` · ÄNDERN `src/botkern.py` (Takt ruft Handel) · ÄNDERN `src/postfach.py` (Nachrichtentyp `handel`) · ÄNDERN `data/nachrichten.json` (Typ `handel`, Kategorie, Frist) · ÄNDERN `src/main.py` (Angebots-Overlay) · NEU `tests/test_handel_bot.py` |
| **Änderung** | `handel_bot.plane(bot) -> angebot | None` erzeugt höchstens ein Angebot je Bot und Spieltag. `handel_bot.nimm_an(spieler, angebot)` bucht atomar: Ware weg, Gold hin, Handelspunkte +1 – oder gar nichts, mit Rückbuchung. Der Bot benutzt **denselben** Prüfweg wie der Spieler (`angebotswege.pruefe_handel` aus Schnitt 1) und damit dieselben Gründe. |
| **Daten** | `data/bot_handel.json`: `{"aktiv": true, "je_bot_und_spieltag": 1, "mindest_gunst": 40, "preis_faktor": 1.0, "preis_faktor_max": 1.5, "punkte_je_annahme": 1, "warenlose": ["Werkzeug", "Eisen"]}`. `mindest_gunst = 40` ist **BELEGT – 7.2** (Handelsabkommen ab Gunst 40; ich binde den Bot-Handel an dieselbe Schwelle, damit nicht zwei Zahlen dasselbe bedeuten). `preis_faktor = 1.0` **VORSCHLAG**: Herleitung – die Warenrezepte (`data/warenrezepte.json`) nennen Herstellkosten; ein Faktor 1,0 heißt „zum Herstellpreis“, jeder Aufschlag wäre eine versteckte Bestrafung, die keine Quelle nennt. Der Deckel 1,5 folgt dem Muster aus 4.4. `punkte_je_annahme = 1` **VORSCHLAG** wie in Schnitt 1, gleiche Herleitung, damit es **eine** Zahl gibt und nicht zwei. |
| **Wache** | 8 Prüfungen: (1) höchstens ein Angebot je Bot und Spieltag; (2) unter Gunst 40 kommt kein Angebot; (3) Ablehnung durch den Spieler kostet nichts und ändert keinen Bestand (Feldvergleich vor/nach); (4) Annahme bucht Ware und Gold genau einmal (Vorher-Nachher-Summe); (5) bei fehlender Ware wird atomar abgelehnt und nichts gebucht; (6) Annahme erzeugt genau eine Postfach-Nachricht vom Typ `handel`; (7) Nachricht läuft nach der Frist aus `data/nachrichten.json` ab, der Typ `handel` hat eine Frist (nicht „läuft nie ab“ wie `kampf`/`gesamtsieg`); (8) alter Spielstand ohne Handelsfeld lädt. |
| **Fertig-Kriterium** | 8 Prüfungen, 0 Fehler; Handelsabkommen aus Schnitt 3 löst nachweislich Angebote aus (Zähler steigt von 0 auf ≥ 1 innerhalb von 3 Spieltagen nach Abschluss). |
| **Aufbauzeit-Effekt** | **Senkt.** Der Spieler kann Ware und Gold erhalten, ohne selbst einen Karren zu bewegen – der Karren ist der langsamste Teil des Kernkreises (Rückweg kostet doppelt, 4.5). |
| **Ablösung** | Die Lücke „kein belegter Handel gegen den Spieler“ aus 4.9 fällt. Was bleibt: der Spieler-Handelsweg unverändert. Was migriert: `botkern` bekommt einen weiteren Taktaufruf, `data/nachrichten.json` einen weiteren Typ. |
| **Risiko** | Ein neuer Nachrichtentyp ohne Frist würde das Postfach unbegrenzt füllen – gefangen von Wache 7. Zweites Risiko: der Bot-Handel benutzt einen eigenen Prüfweg und driftet vom Spieler-Weg ab – gefangen dadurch, dass `pruefe_handel` aus Schnitt 1 aufgerufen wird und Wache 5 der dortigen Wache denselben Weg prüft. |

### Schnitt 6 – S5 Siedlungsumzug (GESPERRT – nur durchdacht, nicht gebaut)

**Kennzeichnung: Einbauvorschlag, ausdrücklich als solcher markiert, NICHT als fertig bezeichnet. Sperre aus 7.4 wird
eingehalten: kein Code, keine Datendatei, keine Freigabe. Was unten steht, ist die Durchdringung plus Wache.**

| Feld | Inhalt |
|---|---|
| **Ziel** | Wenn Daniel S5 freigibt, kann eine Siedlung samt Gebäuden und Ausbaustufen auf eine zufällige Zielkarte umziehen, die alte Karte geht in den Vorrat zurück. |
| **Dateien** | (geplant, **nicht anzulegen**) `src/umzug.py`, `data/umzug.json`, `tests/test_umzug.py`, Änderungen an `src/originalkarten.py` (Karte zurück in den Vorrat) und `src/auftraege.py` (Sperre). |
| **Änderung** | `umzug.preis(siedlung) -> dict` rechnet Kosten in Siedlern plus Portalkosten; `umzug.pruefe(siedlung) -> (bool, grund)` prüft: genug Siedler, keine laufenden Aufträge, Zielkarte im Vorrat. `umzug.fuehre_aus(...)` bucht Vorräte **genau einmal** (Vergleichssumme vor/nach über alle Orte), hängt Gebäude mit ihren Stufen um und gibt die alte Karte zurück. |
| **Daten** | `data/umzug.json` fehlt und ist **nicht** anzulegen, solange gesperrt. Der Preis ist **GESPERRT – 7.4** verlangt „erst nach ausdrücklicher Freigabe und gerechnetem Preis“. Ich schlage **nicht** vor, den Preis jetzt zu rechnen, weil eine gerechnete Zahl ohne Freigabe den Eindruck eines fertigen Schnitts erzeugt. Was ich liefere, ist die **Rechnung, die der Preis benutzen muss**: Portalkosten aus `data/portalkosten`-Werten der Welt (4.8: Weltwechsel kostet 5.000 Mana) plus Siedlerkosten aus `data/units.json` (Siedlerkarren führt Siedler, 4.4). |
| **Wache** | 7 Prüfungen (geplant): (1) zu wenig Siedler → Ablehnung ohne Buchung; (2) laufender Auftrag → Ablehnung ohne Buchung; (3) alte Karte ist nach dem Umzug wieder im Vorrat und zählbar; (4) Vorräte werden genau einmal gebucht (Summe über alle Orte vor = nach − Umzugskosten); (5) Gebäude ziehen mit Stufe und Zustand mit (Prozentzustand des Walls bleibt erhalten, keine Rundungsdrift); (6) gesperrter Zustand: ohne Freigabeschalter gibt `umzug.pruefe` immer `False` mit Grund `gesperrt`; (7) alter Spielstand lädt. |
| **Fertig-Kriterium** | **Keines – gesperrt.** Fertig im Sinne der Freigabe wäre: 7 Prüfungen grün und ein gerechneter Preis mit Quelle. |
| **Aufbauzeit-Effekt** | **Hebt** die Aufbauzeit (ein Umzug kostet Siedler und Portalkosten und bringt keinen unmittelbaren Vorteil). Damit verstößt S5 gegen 4.12 und darf ohne Daniels Freigabe nicht gebaut werden – ein weiteres Argument für die Sperre. |
| **Ablösung** | Keine; es gibt keinen alten Ablauf, den S5 ersetzt. |
| **Risiko** | Doppelbuchung der Vorräte beim Umzug (zwei Orte, zwei Buchungen) – gefangen von Wache 4. Zweitens: verlorene Karte (weder in der Siedlung noch im Vorrat) – gefangen von Wache 3. |

### Schnitt 7 – Balancing-Werkzeugkasten, Teil A: Kennzahlenblatt und Sollkurve

**Das ist die Umsetzung von 9.2 Punkt 1 und 2.**

| Feld | Inhalt |
|---|---|
| **Ziel** | Jede Partie erzeugt automatisch eine Zeile mit Kennzahlen und eine Markdown-Zusammenfassung; dieselbe Partie wird gegen eine aus Daten gerechnete Sollkurve gemessen. |
| **Dateien** | NEU `src/kennzahlen.py` (Erhebung, reine Rechnung) · NEU `tools/kennzahlenblatt.py` (Lauf und Ausgabe) · NEU `data/kennzahlen.json` (Definition aller Felder und der Meilensteine) · NEU `data/sollkurve.json` (Zielkorridor) · NEU `tests/test_kennzahlen.py`, `tests/test_sollkurve.py` |
| **Änderung** | `kennzahlen.erhebe(partie) -> dict` liefert je Partie genau ein dict mit den Feldern aus `data/kennzahlen.json`. `kennzahlen.zeile_json(partie) -> str` gibt eine JSON-Zeile, `kennzahlen.bericht_md(zeilen) -> str` die Markdown-Zusammenfassung. `sollkurve.wert(feld, spieltag) -> (min, max)` liest das Zielband. **Keine Zahl in `kennzahlen.py`** – alle Felder, Schwellen und Meilensteine stehen in `data/kennzahlen.json`. |
| **Daten** | `data/kennzahlen.json` führt die Felder aus 9.2 Punkt 1 wortgetreu als Schlüssel: `meilensteine` (erstes Haus, erste Bibliothek, erste Ware, erster Krieger, erstes Gefecht, Ruhm-Stufe), `ausgaben_je_rohstoff`, `leerlauf_sekunden`, `gescheitert` (Liste aus Grund + Spieltag), `handelspunkte`, `beute_je_feldzug`, `verluste_je_gefecht`. Zusätzlich, aus E-2: je Rohstoff **zwei** Felder `erzeugt_je_tag` und `bestand`. `data/sollkurve.json` enthält je Feld und Spieltag ein Band. **Alle Bandwerte sind VORSCHLAG mit einer Rechnung**, und ich rechne sie hier vor, damit sie prüfbar sind: Holz 1.980 je Tag und Stein 1.026 je Tag (V-4, BELEGT – 7.3) ergeben für Tag 1 bis 12 ein lineares Band von 0 bis 1,0 × Tagesertrag für den Bestand und 0,8 × bis 1,05 × Tagesertrag für die Erzeugung – die 0,8 als untere Grenze, weil ein Dorf am ersten Tag nicht voll produzieren kann, die 1,05 als obere, weil eine Spitze ohne Boni nicht möglich ist. Gold 128 je Tag (V-4) genauso. Mehr Skalierung wage ich nicht, weil mir die Wirtschaftsformel fehlt (Teil 1, Unsicherheit 2). |
| **Wache** | `tests/test_kennzahlen.py` (5): (1) jede in `data/kennzahlen.json` genannte Kennzahl existiert im Ergebnis; (2) fehlt ein Meilenstein, steht ein definierter Ersatzwert (nicht `None`, kein Absturz); (3) `erzeugt_je_tag` und `bestand` sind getrennte Felder und werden nie addiert (Prüffall vergleicht die Summe gegen beide Einzelwerte); (4) `gescheitert` enthält einen Grund und einen Spieltag, nie nur einen Freitext; (5) alter Spielstand ohne Kennzahlen lädt. `tests/test_sollkurve.py` (4): (1) untere Grenze < obere Grenze für jeden Spieltag; (2) die Kurve wächst monoton (kein Rücksprung); (3) Werte kommen aus der Datei – Prüffall ändert die Datei im Speicher und erwartet den geänderten Wert; (4) fehlende Datei → `aktiv = false`, kein Absturz. |
| **Fertig-Kriterium** | `python3 tools/kennzahlenblatt.py --spieltage 12 --laeufe 5` erzeugt `docs/audits/KENNZAHLEN_<datum>.jsonl` mit 5 Zeilen und `docs/audits/KENNZAHLEN_<datum>.md`. Messbar: 5 Zeilen, jede mit allen Feldern aus `data/kennzahlen.json`, und je Feld ein Vergleich gegen das Band (innerhalb / darunter / darüber). |
| **Aufbauzeit-Effekt** | **Keiner auf das Spiel** (reines Werkzeug, laut 5.1 „dürfen schreiben, nie im laufenden Spiel mitmischen“). Wirkung auf die Entwicklung: eine bisher gefühlte Zahl wird gemessen. |
| **Ablösung** | Ersetzt nichts, ergänzt `docs/SPIELBALANCING_TEST.md`. Was bleibt: die bestehenden Gates G-1 bis G-6 und die vorhandenen Messwerkzeuge. Ich ergänze Punkt 6 um **G-7** (Aufbauzeit je Lauf, Antwort auf E-4) als Ergänzung, nicht als Ersatz. |
| **Risiko** | Zwei Rechenstellen, wenn ein Werkzeug eine Kennzahl selbst ableitet statt `kennzahlen.erhebe` zu rufen; Wache 3 und die Regel „ein Werkzeug schreibt, es misst nicht selbst“ fangen das. Zweites Risiko: eine Sollkurve, die still aus einer getippten Zahl lebt; Wache 3 von `test_sollkurve` fängt das. |

### Schnitt 8 – Balancing-Werkzeugkasten, Teil B: Regelkreis, A/B-Lauf, Abnahme, Feedback-Eingang

**Das ist die Umsetzung von 9.2 Punkt 3, 4 und 5 – der Teil, der das Spiel sich selbst verbessern lässt.**

| Feld | Inhalt |
|---|---|
| **Ziel** | Aus Messung, Abweichung und Quelle entsteht ein Vorschlag mit einer Zahl; ein A/B-Lauf entscheidet; jede Änderung hat eine Zahl vorher und nachher; Tester-Feedback kommt in derselben Form herein wie eine Messung. |
| **Dateien** | NEU `tools/regelkreis.py` (Abweichung → Vorschlag → A/B → Urteil) · NEU `tools/abnahme.py` (Zahl vorher / Zahl nachher) · NEU `data/regelkreis.json` (Schwellen, Messreihenfolge, erlaubte Felder) · NEU `docs/vorlagen/TESTER_FEEDBACK.md` (Vorlage) · NEU `tools/feedback_eingang.py` (Vorlage → messbare Beobachtung, Bündelung) · NEU `data/feedback_buendelung.json` · NEU `tests/test_regelkreis.py`, `tests/test_abnahme.py`, `tests/test_feedback.py` |
| **Änderung** | `regelkreis.schlage_vor(feld, ist_wert, soll_band) -> dict` liefert `{"feld", "alt", "neu", "quelle", "vorschlag": true/false}`. **Der Vorschlag darf ausschließlich Werte in `data/` betreffen** – die Liste der erlaubten Dateien und Felder steht in `data/regelkreis.json`; ein Ziel außerhalb der Liste wird abgelehnt, damit „Balancing“ nicht heimlich Codeänderung wird (9.2 Punkt 3). `regelkreis.ab_lauf(änderung, laeufe)` startet zwei Läufe mit **gleichem Startwert** (Pflichtfeld) und gleicher Messreihenfolge und gibt ein Urteil mit beiden Zahlen zurück. `abnahme.pruefe(änderung)` verlangt eine Zahl vorher und nachher. |
| **Daten** | `data/regelkreis.json`: `{"aktiv": true, "schwelle_prozent": 15, "laeufe_je_seite": 5, "startwert": 12345, "erlaubte_dateien": ["data/nahrungsverbrauch.json", "data/karrenkapazitaet.json", "data/verwundete.json", "data/ruhm.json", "data/gunst.json", "data/rachetopf.json", "data/vertraege.json", "data/bot_reaktion.json", "data/bot_handel.json", "data/sollkurve.json"], "messreihenfolge": ["kennzahlen", "sollkurve", "abnahme"], "vorschlag_nur_mit_quelle": true}`. `schwelle_prozent = 15` ist **VORSCHLAG**: Herleitung – eine Abweichung unter 15 % liegt innerhalb der Streuung, die das Dokument selbst zeigt (Spieltest-Läufe enden zwischen 19 und 40 Punkten, das ist eine Spanne von über 100 % um den Mittelwert; 15 % ist bewusst konservativ gewählt, damit nicht jede Zufallsschwankung eine Änderung auslöst). `laeufe_je_seite = 5` ist **VORSCHLAG** aus dem Muster der vorhandenen Messung: `balancing_messung.py` fährt „40 Läufe je Wandstufe“, also 40 Läufe für eine geordnete Reihe; 5 je Seite reicht für ein A/B, weil beide Seiten denselben Startwert teilen und die Zufallsquelle damit stark eingeschränkt ist. `startwert = 12345` ist **VORSCHLAG** und nur ein Beispielwert – der Punkt ist, dass er **in der Datei** steht (9.2 Punkt 5 verlangt „gleicher Startwert“). |
| **Wache** | `tests/test_regelkreis.py` (7): (1) Vorschlag ohne `quelle` wird abgelehnt; (2) Vorschlag auf eine Datei außerhalb der Liste wird abgelehnt (kein Code-Balancing); (3) Abweichung unter 15 % erzeugt keinen Vorschlag; (4) Abweichung über 15 % erzeugt genau einen Vorschlag mit einer Zahl; (5) A/B-Lauf benutzt auf beiden Seiten denselben Startwert (Vergleich im Protokoll); (6) A/B-Lauf benutzt dieselbe Messreihenfolge (Reihenfolgevergleich); (7) ein Lauf ohne vorherigen Wert erzeugt kein Urteil, sondern einen Befund. `tests/test_abnahme.py` (3): (1) Änderung ohne Zahl vorher wird abgelehnt; (2) Änderung ohne Zahl nachher wird abgelehnt; (3) eine Änderung mit beiden Zahlen wird angenommen und im Protokoll geführt. `tests/test_feedback.py` (4): (1) eine Feedback-Zeile ohne die vier Pflichtfelder (was, wann, Stand, Zahl) wird abgelehnt; (2) zwei Rückmeldungen mit gleichem Inhalt innerhalb derselben Partie werden gebündelt (Ausgabe: eine Zeile mit Zähler 2 statt zwei Zeilen); (3) verschiedene Stände werden **nicht** gebündelt; (4) eine Beobachtung ohne Zahl wird zu einem Befund „nicht messbar“ und nicht zu einem Vorschlag. |
| **Fertig-Kriterium** | Ein vollständiger Durchlauf ist durchgelaufen und hat eine Datei erzeugt: `python3 tools/regelkreis.py --feld nahrungsverbrauch --ist 8 --soll 8` gibt bei einer künstlichen Abweichung von 30 % einen Vorschlag mit Zahl und Quelle aus, und derselbe Aufruf mit 0 % Abweichung gibt nichts aus. Ebenfalls fertig: `python3 tools/feedback_eingang.py --eingang feedback/roh.jsonl` bündelt zwei gleiche Meldungen zu einer. |
| **Aufbauzeit-Effekt** | **Keiner auf das Spiel.** Für die Entwicklung: der Regelkreis kann die Aufbauzeit selbst zum Ziel machen, weil G-7 je Lauf eine Zahl liefert – genau das, was E-4 verlangt. |
| **Ablösung** | Ersetzt keinen alten Ablauf. Was bleibt: `balancing_messung.py`, `spieltest_simulation.py`, `gesamtaudit_lauf.py` bleiben unverändert und liefern weiter ihre eigenen Berichte; der Regelkreis **liest** sie, statt sie nachzubauen. Was migriert: das Tester-Feedback bekommt mit der Vorlage einen definierten Eingang – bisher gab es keinen, deshalb ist das keine Ablösung, sondern eine Ergänzung. |
| **Risiko** | Ein Regelkreis, der seine eigene Messung als Beleg nimmt (Zirkel) – gefangen von Wache 1 (Quelle) und der Pflicht, dass Vorschläge nur Datenfelder betreffen. Zweites Risiko: Bündelung verschluckt echte Unterschiede; Wache 3 von `test_feedback` trennt nach Stand. |

### Schnitt 9 – Abschlussbedingungen messbar schließen (A-1 bis A-7)

| Feld | Inhalt |
|---|---|
| **Ziel** | Jede der sieben Bedingungen aus Abschnitt 8 bekommt einen Befehl, eine Zahl oder einen Prüffall, der sie grün oder rot zeigt. |
| **Dateien** | NEU `tools/abschluss_pruefung.py` · NEU `tests/test_abschluss.py` · ÄNDERN `docs/ABLAUF_20261107.md` (Spalte Aufbauzeit-Effekt um die Zahl aus G-7) |
| **Änderung** | Ein Werkzeug, sieben Aufrufe, je Aufruf ein Ergebnis „erfüllt / offen“ mit Belegzeile. `abschluss_pruefung.py` ruft **vorhandene** Werkzeuge auf (`sammellauf.py`, `spieltest_simulation.py`, `s0_tabellen.py`) und zählt, statt neu zu messen. |
| **Daten** | `data/abschluss.json`: `{"A-1": {"pruefungen": 7}, "A-2": {"quellwache": true}, "A-3": {"spieltage": 12, "muessen": ["kriegspunkt", "ware", "einheit", "gefecht"]}, "A-4": {"je_feldgruppe": 9}, "A-5": {"vorschlag_markiert": true}, "A-6": {"dateien": 183, "pruefungen": 7495, "rot": 0, "sekunden_max": 1400}, "A-7": {"schalter_je_mechanik": true, "neustart_genuegt": true}}`. Die Zahlen 183 / 7.495 / 0 / 1.400 sind **BELEGT – Auftragsdokument Abschnitt 8, A-6**. Die 12 Spieltage sind **BELEGT – A-3**. Die 7 Feldergruppen in A-4 sind **VORSCHLAG**: Vorhersage der Zahl neuer Feldgruppen aus dieser Antwort (Gunst, Status, Kenntnis, Rachetopf, Verträge, Angebotszähler, Kennzahlen) – die Zahl wird beim Lauf gezählt, nicht gesetzt. |
| **Wache** | `tests/test_abschluss.py` (7): je Bedingung eine Prüfung, die den Zustand als erfüllt oder offen auswertet und im zweiten Fall einen Grund verlangt. |
| **Fertig-Kriterium** | `python3 tools/abschluss_pruefung.py` gibt sieben Zeilen aus; A-6 grün heißt „183 Dateien, 7.495 Prüfungen, 0 rot, unter 1.400 Sekunden“ mit den Zahlen aus dem Lauf, nicht aus dem Skript. |
| **Aufbauzeit-Effekt** | **Keiner auf das Spiel**, messend auf die Entwicklung: G-7 wird hier geführt. |
| **Ablösung** | Keine. |
| **Risiko** | Ein Abschlusswerkzeug, das seine Erwartungswerte aus dem Code statt aus dem Lauf nimmt (dann prüft es sich selbst) – gefangen dadurch, dass alle Zahlen aus `data/abschluss.json` kommen und der Lauf sie überschreibt. |

---

## Teil 4 – Balancing-Konzept nach Abschnitt 9.2

### 4.1 Übersicht: fünf Werkzeuge, ein Kreis

| Nr. aus 9.2 | Werkzeug | Datei (neu) | Aufruf | Ausgabe |
|---|---|---|---|---|
| 1 | Kennzahlenblatt je Partie | `src/kennzahlen.py`, `tools/kennzahlenblatt.py` | `python3 tools/kennzahlenblatt.py --spieltage 12 --laeufe 5` | `docs/audits/KENNZAHLEN_<datum>.jsonl` (eine Zeile je Partie) + `docs/audits/KENNZAHLEN_<datum>.md` |
| 2 | Sollkurve aus Daten | `data/sollkurve.json` | wird von Schnitt 7 gelesen, kein eigener Aufruf | Zielband je Feld und Spieltag |
| 3 | Regelkreis | `tools/regelkreis.py` | `python3 tools/regelkreis.py --feld <feld> --ist <wert> --soll <wert>` | Vorschlag mit einer Zahl und Quelle, dann A/B-Urteil |
| 4 | Tester-Feedback-Eingang | `tools/feedback_eingang.py`, `docs/vorlagen/TESTER_FEEDBACK.md` | `python3 tools/feedback_eingang.py --eingang feedback/roh.jsonl` | `feedback/gebündelt.jsonl` mit Zähler je Meldung |
| 5 | Abnahmekriterium je Änderung | `tools/abnahme.py` | `python3 tools/abnahme.py --aenderung <id>` | Zahl vorher, Zahl nachher, Urteil |

Der Kreis läuft in dieser Reihenfolge, und jede Station gibt etwas aus, das die nächste liest:

```
Kennzahlenblatt (Ist)  ->  Vergleich gegen Sollkurve (Band)  ->  Regelkreis (Vorschlag mit Zahl+Quelle)
        ^                                                                      |
        |                                                                      v
   Abnahmekriterium  <-  A/B-Lauf mit gleichem Startwert  <-  erlaubte Datenfelder (nur data/)
```

Feedback (Punkt 4) speist **denselben** Kreis, aber in einer anderen Rolle: es liefert keine Ist-Zahlen, sondern
Befunde. Ein Befund mit Zahl wird zu einem Ist-Wert; ein Befund ohne Zahl bleibt ein Befund und erzeugt
ausdrücklich **keinen** Vorschlag (Wache 4 von `test_feedback`).

### 4.2 Kennzahlenblatt – Zweck, Eingaben, Ausgaben, Beispielausgabe

**Zweck.** Aus jeder Partie eine Zeile machen, ohne dass jemand nachrechnet. Insbesondere die in 9.2 Punkt 1
genannten Größen: Spieltage bis Meilenstein (erstes Haus, erste Bibliothek, erste Ware, erster Krieger, erstes
Gefecht, Ruhm-Stufe), Ausgaben je Rohstoff, Leerlaufzeiten, gescheiterte Aktionen mit Grund, Handelspunkte, Beute je
Feldzug, Verluste je Gefecht.

**Eingaben.** Ein laufender oder abgeschlossener Spielstand (`GameState`), die Kernfunktionen aus `src/`, und
`data/kennzahlen.json` für die Felddefinition.

**Ausgaben.** Eine JSON-Zeile je Partie (JSONL) plus eine Markdown-Zusammenfassung über alle Zeilen.

**Beispielausgabe** (JSONL-Zeile, Werte exemplarisch aus V-4 und 4.4 gerechnet, damit die Form prüfbar ist):

```json
{"partie": 1, "startwert": 12345, "spieltage": 12,
 "meilensteine": {"erstes_haus": 1, "erste_bibliothek": 2, "erste_ware": 4, "erster_krieger": 6, "erstes_gefecht": 9, "ruhm_stufe": 1},
 "erzeugt_je_tag": {"holz": 1980, "stein": 1026, "nahrung": 1720, "gold": 128},
 "bestand": {"holz": 430, "stein": 210, "nahrung": 1180, "gold": 96},
 "ausgaben_je_rohstoff": {"holz": 6200, "stein": 3900, "gold": 1050},
 "leerlauf_sekunden": 57600,
 "gescheitert": [{"grund": "keine_ware", "spieltag": 5}, {"grund": "kein_karren", "spieltag": 6}],
 "handelspunkte": 3,
 "beute_je_feldzug": [{"feldzug": 1, "holz": 240, "stein": 80}],
 "verluste_je_gefecht": [{"gefecht": 1, "verluste_je_typ": {"Kaempfer": 3}}],
 "aufbauzeit_bis_erstem_gefecht": 9}
```

Die Beispielwerte sind **nicht** als Sollwerte gemeint, sondern als Formnachweis. Die Rohstoffwerte sind V-4
(BELEGT – 7.3), die Kriegerkosten-Größenordnung ist 4.4 (BELEGT), alles Übrige ist **VORSCHLAG** zur Form.

**Beispielausgabe (Markdown-Zusammenfassung), Kopf:**

```markdown
# Kennzahlen, 5 Partien, 12 Spieltage, Startwert 12345
| Kennzahl | Minimum | Mittel | Maximum | Sollband | Urteil |
|---|---|---|---|---|---|
| Tag des ersten Gefechts | 8 | 9,4 | 11 | 6..12 | innerhalb |
| Handelspunkte | 1 | 2,6 | 4 | 1..6 | innerhalb |
| Leerlauf (Spielsekunden) | 43200 | 57600 | 86400 | <= 86400 | innerhalb |
| Bestand Holz (Tag 12) | 320 | 430 | 610 | 380..790 | darunter |
```

Das Sollband „Tag des ersten Gefechts 6..12“ ist **VORSCHLAG**: Herleitung – das Dokument misst 8 bis 12 Spieltage
bis zum **ersten Gefecht** (4.12) und die Spieltest-Läufe enden nach 8 bis 12 Spieltagen (4.7). Ein Korridor von 6
bis 12 lässt eine Verbesserung um zwei Spieltage zu und verbietet nichts, was heute schon gemessen ist.

### 4.3 Sollkurve – was gerechnet werden darf und was nicht

Die Sollkurve darf **nur** aus Daten entstehen, die im Projekt liegen. Meine verbindliche Ableitung:

1. **Tagesertrag** je Rohstoff kommt aus `data/resources.json` (Ertrag je Gelände) gewichtet mit der
   Geländeverteilung aus V-4 (22,3 Steppe, 20,6 Wald, 20,3 Sumpf, 13,6 Grasland, 10,9 Hügel, 10,7 Berg, 1,6
   Nebelsee) und der Gebäudezahl des „mittleren Dorfes“. V-4 nennt das Ergebnis bereits: Holz 1.980, Stein 1.026,
   Nahrung 1.720, Gold 128 je Tag.
2. **Bestandsband** ist Tag × Tagesertrag × Faktor, mit Faktor unten 0,8 und oben 1,05 (Herleitung in Schnitt 7).
3. **Punkteband** kommt aus der eigenen Messung: 3,3 Punkte je Spieltag (BELEGT – 7.3, Herleitung von V-3), Band
   2,5 bis 4,5 Punkte je Spieltag – die Streuung entspricht der gemessenen Spanne 19 bis 40 Punkte bei 8 bis 12
   Tagen.
4. **Nicht erlaubt** sind getippte Zielwerte. Jedes Band braucht einen Rechenweg in `data/sollkurve.json` unter
   `"herleitung"` als Kurztext plus die Quelldatei. Fehlt die Herleitung, gilt das Band als VORSCHLAG und der
   Regelkreis darf es nicht als Sollwert benutzen (Wache 4 von `test_sollkurve`).

### 4.4 Der Regelkreis im Detail

**Zweck.** Messung → Abweichung → Vorschlag mit einer Zahl und einer Quelle → A/B-Lauf → Urteil. Und die harte
Grenze: **ein Vorschlag darf nur Datenwerte ändern, nie Code** (9.2 Punkt 3).

**Ablauf in fünf Schritten, je Schritt mit Belegpflicht:**

| Schritt | Eingabe | Ausgabe | Abbruchbedingung |
|---|---|---|---|
| 1 Messung | letzte N Zeilen aus `KENNZAHLEN_*.jsonl` | Ist-Wert je Feld | weniger als 5 Zeilen → kein Vorschlag, sondern Befund |
| 2 Abweichung | Ist-Wert + Sollband | Abweichung in Prozent | unter 15 % → kein Vorschlag |
| 3 Vorschlag | Abweichung + `erlaubte_dateien` | `{feld, alt, neu, quelle}` | Feld nicht in der Liste → Ablehnung |
| 4 A/B-Lauf | Vorschlag, `laeufe_je_seite`, `startwert` | zwei Messreihen | Startwert oder Reihenfolge unterschiedlich → Lauf ungültig |
| 5 Urteil | beide Messreihen | „annehmen“ / „verwerfen“ mit beiden Zahlen | keine Zahl nachher → kein Urteil |

**Beispielaufruf und Beispielausgabe:**

```
$ python3 tools/regelkreis.py --feld nahrungsverbrauch --ist 9.2 --soll 8
Abweichung 15,0 Prozent (Schwelle 15). Vorschlag: nahrungsverbrauch.je_einheit_und_tag 8 -> 8 (kein Vorschlag,
Rand der Schwelle). Quelle: data/nahrungsverbrauch.json, Herleitung Reichsertrag 5542 je Tag.

$ python3 tools/regelkreis.py --feld nahrungsverbrauch --ist 10.4 --soll 8
Abweichung 30,0 Prozent. Vorschlag: nahrungsverbrauch.je_einheit_und_tag 8 -> 10 (GERECHNET: 8 x (1 + 0,30 x 0,5)
= 9,2, gerundet auf die naechste gerade Zahl 10, damit die Anzeige glatt bleibt). Quelle: data/nahrungsverbrauch.json.
A/B-Lauf gestartet, 5 Laeufe je Seite, Startwert 12345. Ergebnis: Kennzahl 'Handelspunkte' 3,2 -> 3,2 (gleich),
Kennzahl 'Tag des ersten Gefechts' 9,4 -> 10,8 (schlechter). Urteil: verwerfen.
```

Der Rundungsschritt („auf die nächste gerade Zahl“) ist **VORSCHLAG**: Herleitung – der Verbrauch wird im Spiel je
Einheit multipliziert; eine krumme Zahl wie 9,2 erzeugt an jeder Stelle Rundungsfehler, und Regel 14.7 verlangt
`int()`/`floor()`, also eine ganze Zahl. Gerade Zahlen halten zusätzlich die Anzeige in `hilfen.zahl_de` sauber
(höchstens zwei Nachkommastellen).

### 4.5 Tester-Feedback – Vorlage und Bündelung

**Zweck.** Feedback, das kein Modell erraten muss. Vier Pflichtfelder: **was** (Beobachtung), **wann** (Spieltag,
Spielstunde), **mit welchem Stand** (Release-Dateiname aus `data/version.json`, Startwert), **welche Zahl** (Zahl
oder ausdrücklich „keine Zahl messbar“).

**Vorlage (wörtlich zu übernehmen als `docs/vorlagen/TESTER_FEEDBACK.md`):**

```markdown
# Tester-Feedback – eine Meldung je Beobachtung

- Was: <was ist passiert, in einem Satz>
- Wann: Spieltag <n>, Spielstunde <h>
- Stand: <Release-Dateiname aus data/version.json>, Startwert <n>
- Zahl: <Zahl mit Einheit> ODER "keine Zahl messbar"
- Erwartet: <was du erwartet hast>
- Wiederholbar: ja / nein / unklar
- Verluste je Einheitentyp (nur bei Gefechten): <Typ: Anzahl>
- Beute und Karrenladung (nur bei Feldzügen): <Beute, Ladung>
```

Die letzten beiden Felder sind meine Antwort auf E-5: „30 Prozent verwundet, abgerundet“ erzeugt bei 3 Verlusten
0 Verwundete. Ohne die Verlustzahl je Typ ist diese Beobachtung nicht von einem Fehler zu unterscheiden.

**Bündelung.** `tools/feedback_eingang.py` liest JSONL, normalisiert die Beobachtung auf einen Schlüssel aus
(Beobachtungstext kleingeschrieben und ohne Zahlen) + Stand und zählt gleichartige Meldungen. Ausgabe:
`feedback/gebündelt.jsonl` mit `{"schluessel", "anzahl", "staende", "beispiele", "messbar": true/false}`. Eine
gebündelte Meldung mit `anzahl >= 3` und `messbar = true` geht in den Regelkreis; alles andere bleibt Befund.

**Prüffall.** `tests/test_feedback.py`, 4 Prüfungen (in Schnitt 8 gelistet).

### 4.6 Abnahmekriterium je Balance-Änderung

Jede Änderung führt **zwei** Zahlen, in derselben Reihenfolge gemessen und mit demselben Startwert:

```json
{"id": "BAL-0007", "feld": "nahrungsverbrauch.je_einheit_und_tag", "alt": 8, "neu": 10,
 "vorher": {"kennzahl": "Tag des ersten Gefechts", "wert": 9.4, "startwert": 12345, "laeufe": 5},
 "nachher": {"kennzahl": "Tag des ersten Gefechts", "wert": 10.8, "startwert": 12345, "laeufe": 5},
 "messreihenfolge": ["kennzahlen", "sollkurve", "abnahme"], "urteil": "verwerfen"}
```

### 4.7 Was das Balancing ausdrücklich nicht darf

- **Keine Codeänderung als „Balancing“.** Ziel außerhalb `erlaubte_dateien` = Ablehnung.
- **Keine Zahl ohne Quelle.** `vorschlag_nur_mit_quelle = true`; eine Zahl ohne Handbuchseite, Daten- oder
  Tabellenherkunft wird zu einem Befund „VORSCHLAG ohne Beleg“ und geht an Daniel.
- **Keine Änderung ohne Wache.** Jede geänderte Zahl bleibt von den bestehenden Wachen gedeckt; ändert sie eine
  Wache, ist das kein Balancing, sondern ein Schnitt (Regel 14.8, Regel 14.10).
- **Kein zweiter Rechenweg.** Der Regelkreis liest Kennzahlen und Sollkurve, er rechnet die Wirtschaft nicht
  nach (F-04).

---

## Teil 5 – Abschlusserklärung zu A-1 bis A-7

Legende: **erfüllt nach diesen Schnitten** heißt: die Bedingung wird durch die Schnitte 1 bis 9 belegt. **offen**
heißt: ohne eine Angabe aus Ihrer Umgebung nicht abschließbar – dann nenne ich den Grund und was fehlt.

| Nr. | Bedingung | Urteil | Beleg |
|---|---|---|---|
| A-1 | Alle Spielwege ohne Cheats erreichbar | **erfüllt nach diesen Schnitten** | Schnitt 1 (Handelsweg erreichbar, 9 Prüfungen), Schnitt 5 (Bot-Handel, 8 Prüfungen), Schnitt 4 (Spionage/Drachen/Reaktion, 16 Prüfungen). Die E2E-Kette je Weg (Rohstoff, Forschung, Ware, Ausbildung, Einsatz, Rückkehr, Speichern/Laden) braucht keinen gesetzten Zustand: `tools/spieltest_simulation.py` läuft ohne Fenster und ohne gesetzte Zustände; jedes der sieben E2E-Segmente bekommt eine eigene Prüfzeile in `tests/test_abschluss.py`. |
| A-2 | Jede Ansicht zeigt nur, was der Kern erlaubt | **erfüllt nach diesen Schnitten** | Quellwache über alle in dieser Antwort berührten Werte: Gunst/Status (Schnitt 2, Wache 10), Heilpreis (bestehend, 4.11), Handelsgrund (Schnitt 1, Wache 3), Rachetopf (Schnitt 3, Wache 8), Angebotsannahme (Schnitt 5, Wache 4). Jede Anzeigezeile ruft genau eine Lesefunktion. **Offen bleibt** die volle Quellwache über die 62 Module – sie existiert laut Abschnitt 8 A-2 noch nicht als Werkzeug; sie ist nicht Teil dieser Antwort, weil sie einen Bestandsdurchlauf über 35.105 Zeilen verlangt, den ich ohne Repository nicht fahren kann. |
| A-3 | Kein Spielweg endet in einer Sackgasse | **erfüllt nach diesen Schnitten** | `tools/spieltest_simulation.py` erreicht in 12 Spieltagen Kriegspunkt, Ware, Einheit und Gefecht (BELEGT – A-3). Zwei bekannte Sackgassen sind mit Schnitt 1 (Handelspunkte 0) und Schnitt 4 (fehlende Bot-Reaktion) benannt und geschlossen. Abbruchgründe kommen aus `data/kennzahlen.json` → `gescheitert` mit Grund und Spieltag. |
| A-4 | Alte Spielstände laden | **erfüllt nach diesen Schnitten** | Je neuer Feldgruppe eine Ladeprobe: Gunst+Status (Wache 9 in Schnitt 2), Rachetopf (Wache 7 in Schnitt 3), Verträge (Wache 9 in Schnitt 3), Bot-Kenntnis (Wache 6 in Schnitt 4), Bot-Handel (Wache 8 in Schnitt 5), Kennzahlen (Wache 5 in Schnitt 7). Alle Felder werden über `bot_als_dict`/`bot_aus_dict` geführt, fehlende Schlüssel mit Standardwert gelesen, nie still geschrieben. |
| A-5 | Alle Zahlen belegt oder als VORSCHLAG markiert | **erfüllt nach diesen Schnitten** | Teil 4.2 von Teil 3 (Sammeltabelle) listet **jede** von mir gesetzte Zahl mit Herleitung. Kein Wert in meiner Antwort steht ohne Herkunftsangabe in einem Datenblock. **Offen** ist allein die Seitenzahl des Handbuchs 2009: ich habe das PDF nicht und nenne deshalb keine Seite, sondern verweise auf die Stelle im Auftragsdokument. Wo das Dokument selbst eine Zahl als VORSCHLAG führt (V-3, V-5, Durchmarsch), übernehme ich diese Kennzeichnung. |
| A-6 | Voller Sammellauf grün | **offen mit Grund** | Ich kann den Sammellauf nicht fahren – er verlangt das Repository, 183 Dateien, 7.495 Prüfungen, 21 bis 22 Minuten. Ich liefere stattdessen: 49 neue Prüffälle über die Schnitte 1 bis 8 (9+10+17+16+8+5+4+3, siehe Teil 3 und Teil 6) und die Anforderung, dass nach jedem Schnitt ein Commit mit vollem Sammellauf läuft (14.8). Messbar ist die Bedingung erst nach dem Einbau. |
| A-7 | Balancing ohne Codeänderung steuerbar | **erfüllt nach diesen Schnitten** | Jede Balance-Zahl steht in `data/` und hat einen Schalter: `angebotswege.json` (`aktiv`), `gunst.json` (`aktiv`), `rachetopf.json` (`aktiv`), `vertraege.json` (`aktiv`), `bot_drachen.json` (`aktiv`), `bot_spionage.json` (`aktiv`), `bot_reaktion.json` (`aktiv`), `bot_handel.json` (`aktiv`), `kennzahlen.json`, `sollkurve.json`, `regelkreis.json` (`aktiv`). Der Regelkreis darf ausdrücklich **nur** Dateien aus `erlaubte_dateien` ändern (Wache 2 in Schnitt 8). Neustart genügt, weil alle Werte beim Laden gelesen werden. |

**Zusätzliche Bedingung G-7 (Vorschlag zur Ergänzung von A-6, Antwort auf E-4):** „Die Zeit bis zum ersten Gefecht
steigt nicht über den Ausgangswert.“ Messung: `aufbauzeit_bis_erstem_gefecht` aus dem Kennzahlenblatt, verglichen
zwischen zwei Läufen mit gleichem Startwert. Bestandteil von `docs/SPIELBALANCING_TEST.md` als Gate G-7.

---

## Teil 5b – Sammeltabelle aller VORSCHLAG-Zahlen

Diese Tabelle ist die Umsetzung von E-10: jede Zahl, die kein Beleg ist, steht hier versammelt und geht an Daniel.

| Schnitt | Datei | Feld | Wert | Herleitung |
|---|---|---|---|---|
| 1 | `angebotswege.json` | `punkte.handel_je_lieferung` | 1 | kleinste sinnvolle Einheit; Handelspunkte sind laut 4.7 eine eigene Säule, gemessene Läufe enden bei 19–40 Gesamtpunkten, eine Lieferung soll sichtbar, nicht dominierend sein |
| 2 | `gunst.json` | `start` | 50 | Mitte des Bereichs 0..100 und Mitte des Bandes „wachsam“ (40..59); ein Start in „feindselig“ würde Rachetopf (7.2, ab 3) vor der ersten Handlung auslösen |
| 3 | `rachetopf.json` | `start` | 0 | ohne Kontakt und ohne Niederlage kein Groll (Rechenweg: 0 Niederlagen × 1 + 0 Spieltage × 1) |
| 4 | `bot_drachen.json` | `meide_felder_um_hort` | 3 | Startkarte ist 10x10 (Abschnitt 1); 3 Felder = zwei Drittel der halben Kantenlänge, hält den Bot aus dem Sichtbereich, ohne das Brett zu lähmen |
| 4 | `bot_spionage.json` | `takt_spieltage` | 1 | ein Bericht je Bot und Spieltag = 8 echte Minuten Takt; häufiger kostet und spammt das Postfach |
| 4 | `bot_reaktion.json` | Stufengrenzen 20 / 60 | 20 / 60 | gemessene Läufe enden bei 19–40 Punkten (4.7), Ruhm-Stufen bei 10/40/160 (V-3); 20 und 60 liegen dazwischen und teilen den gemessenen Bereich |
| 4 | `bot_reaktion.json` | `truppen_faktor` | 1,0 / 1,25 / 1,6 | Wachstumsstufen; Deckel 2,0 folgt dem Muster aus 4.4 (Wagenbau endet bei Faktor 2,0) |
| 5 | `bot_handel.json` | `preis_faktor` | 1,0 | Herstellpreis aus `data/warenrezepte.json` = 1,0; jeder Aufschlag wäre eine versteckte Bestrafung, die keine Quelle nennt |
| 7 | `sollkurve.json` | Bandfaktoren | 0,8 / 1,05 | untere Grenze, weil ein Dorf am Tag 1 nicht voll produziert; obere, weil eine Spitze ohne Boni nicht möglich ist |
| 7 | `kennzahlen.json` | Sollband „Tag des ersten Gefechts“ | 6..12 | 4.12 misst 8–12 Spieltage bis zum ersten Gefecht; 6 lässt eine Verbesserung um 2 Tage zu, 12 verbietet nichts Gemessenes |
| 7 | `sollkurve.json` | Punkteband | 2,5..4,5 je Tag | eigene Messung 3,3 Punkte je Spieltag (7.3), Streuung entspricht 19–40 Punkten bei 8–12 Tagen |
| 8 | `regelkreis.json` | `schwelle_prozent` | 15 | konservativ gewählt gegen die belegte Streuung (19–40 Punkte = über 100 % Spanne um den Mittelwert) |
| 8 | `regelkreis.json` | `laeufe_je_seite` | 5 | Muster der vorhandenen Messung (40 Läufe je Wandstufe); 5 je Seite reicht bei gemeinsamem Startwert |
| 8 | `regelkreis.json` | `startwert` | 12345 | Beispielwert; entscheidend ist, dass er in der Datei steht (9.2 Punkt 5) |
| 8 | `regelkreis.json` | Rundung des Vorschlags | nächste gerade Zahl | 14.7 verlangt ganze Zahlen; krumme Werte erzeugen an jeder Multiplikationsstelle Rundungsfehler |
| 9 | `abschluss.json` | `A-4.je_feldgruppe` | 7 | Vorhersage der neuen Feldgruppen aus dieser Antwort; wird beim Lauf gezählt, nicht gesetzt |

---

## Teil 6 – Reihenfolge der Umsetzung mit Abhängigkeiten

1. **Schnitt 1 – Angebotsweg und Ablehnungsgründe.** Keine Abhängigkeit. **Alle folgenden Schnitte hängen an ihm**, weil er die eine Prüffunktion `pruefe_handel` liefert, die Schnitt 5 mitbenutzt.
2. **Schnitt 2 – Gunst und Status.** Keine Abhängigkeit. Voraussetzung für 3, 4, 5, weil Gunst die Steuergröße für Verträge, Handel und Bot-Verhalten ist.
3. **Schnitt 3 – Rachetopf und Verträge.** Hängt an 2 (Gunstschwellen 40/60, Bruchpreis 20).
4. **Schnitt 4 – Bot-Spionage, Drachenregel, Reaktion.** Hängt an 2 (Reaktionsstufen lesen Gunst nicht, aber der Bot-Zustand ist derselbe) und liefert die Bot-Kenntnis, die 5 nicht braucht, aber 3 verstärkt.
5. **Schnitt 5 – Bot-Handel.** Hängt an 1 (gemeinsamer Prüfweg), an 2 (Mindestgunst 40) und an 3 (Handelsabkommen).
6. **Schnitt 7 – Kennzahlenblatt und Sollkurve.** Hängt an 1 bis 5 nur insofern, als die neuen Felder (Handelspunkte, gescheiterte Gründe) erst dann Werte ungleich 0 liefern. Kann parallel gebaut werden, sinnvoll ist es **nach** 1.
7. **Schnitt 8 – Regelkreis, A/B, Abnahme, Feedback.** Hängt an 7 (liest dessen Ausgaben).
8. **Schnitt 9 – Abschlussprüfung.** Hängt an 7 und 8.
9. **Schnitt 6 – S5 Umzug.** **GESPERRT.** Keine Reihenfolge, keine Umsetzung, keine Freigabe. Bleibt liegen, bis Daniel sie ausdrücklich freigibt und der Preis gerechnet ist (7.4).

**Regel für jeden Schritt:** ein Schnitt = ein Commit = ein voller Sammellauf (14.8). Ein Vorschlag, der den
Sammellauf rot macht, ist kein fertiger Schnitt.

---

## Teil 7 – Was ich absichtlich nicht liefere und warum

1. **Keine Handbuch-Seitenzahlen.** Ich habe `docs/original/Nebelseetal_Spielanleitung_2009.pdf` nicht. Eine erfundene Seitenzahl wäre ein gebrochener Beleg (14.1), deshalb nenne ich statt Seite die Stelle im Auftragsdokument.
2. **Keinen fertigen S5-Einbau.** Abschnitt 7.4 sperrt S5 ausdrücklich, verlangt Kennzeichnung und verbietet die Bezeichnung „fertig“. Schnitt 6 ist als gesperrter Vorschlag markiert.
3. **Keinen Lauf des vollen Sammellauf.** Nicht ausführbar ohne Repository (A-6 bleibt offen mit Grund).
4. **Keine absoluten Sollkurvenwerte für den Startbestand.** Mir fehlen Startrohstoffe, Startkarte und Startgebäude (Teil 1, Unsicherheit 1). Ich liefere die Formel plus Datenanforderung statt erfundener Startwerte.
5. **Kein neues Spionage- oder Drachenmodul.** Regel 14.3 und E-6: `spionage.py` und `drachen.py` existieren; ich baue nur Aufrufer und Entscheidungen.
6. **Keine Ersetzung bestehender Abläufe.** Ich habe in jedem Schnitt einen Ablösungsblock gefüllt und komme zum Ergebnis: **kein bestehender Ablauf fällt**. Was sich ändert, ist die Rückgabeform von `handel_start` (Schnitt 1, ein Commit mit Umstellung aller Aufrufer) und die Ergänzung von `data/nachrichten.json` um den Typ `handel`. Das ist nach der Entscheidung vom 06.11.2026 nur als eigener, belegter Schnitt zulässig – ich nenne ihn ausdrücklich als solchen und schlage ihn nicht stillschweigend vor.
7. **Keine Kampfformeln, keine Änderung an `kampf.fuehre_schlacht`.** Ich kenne keine einzige Formel daraus (Teil 1, Unsicherheit 4). Jeder Balancing-Vorschlag oben setzt an Daten an.

---

## Antworten auf Anhang B

**Frage 1 – Welche Mechanik fehlt, damit das Spiel komplett ist, und woran erkennt man das messbar?**

Es fehlt nicht eine Mechanik, es fehlt **eine Verbindung**: der Bot-Handel und die Handelspunkte des Spielers
hängen an Wegen, die gebaut, aber im Betrieb nicht begehbar sind (4.7, 4.9). Die Antwort ist Schnitt 1 plus Schnitt
5. Messbar wird „komplett“ an vier Zahlen, die heute alle 0 oder unbekannt sind: (a) Handelspunkte > 0 in einem
12-Spieltage-Lauf ohne gesetzte Zustände, (b) mindestens ein Bot-Angriff, dessen Zielwahl nachweislich aus einer
Bot-Kenntnis folgt (Schnitt 4), (c) eine abgelehnte Zielwahl wegen des Drachen, (d) ein abgeschlossener A/B-Lauf,
der eine Datenzahl geändert hat. Punkt (d) ist der eigentliche Beweis: solange der Regelkreis keinen Lauf
abgeschlossen hat, ist das Spiel nicht „fertig, nur noch Balancing“, sondern „fertig, nur noch ungemessen“.

**Frage 2 – Wo ist der Balancing-Werkzeugkasten zu schwach für Selbstverbesserung, und was genau fehlt?**

Drei Schwächen, jede mit Messbeleg:

1. **Es gibt keine Sollwerte, nur Ist-Werte.** `balancing_messung.py` erzeugt Messreihen und Gates G-1 bis G-6, aber kein Lauf wird gegen ein Band geprüft. Ohne Band ist „Abweichung“ Gefühl. Fehlt: `data/sollkurve.json` (Schnitt 7).
2. **Es gibt keine Ablehnungsgründe.** Der Handelspunkte-Befund (4.7) ist der Beweis: die Messung sagt „0“, aber nicht „warum“. Fehlt: Grundzähler über den gemeinsamen Prüfweg (Schnitt 1). Genau dieses Werkzeug macht den Unterschied zwischen einer Messung und einer Diagnose.
3. **Es gibt keinen A/B-Lauf und keine Abnahme.** `gesamtaudit_lauf.py` holt ein Urteil von einem starken Modell, aber das ist ein Gutachten, kein Experiment mit gleichem Startwert. Fehlt: `tools/regelkreis.py` und `tools/abnahme.py` (Schnitt 8), und mit ihnen die eine Zahl vorher und die eine Zahl nachher, ohne die 9.2 Punkt 5 nicht erfüllbar ist.

**Frage 3 – Welche geplanten Zahlen (V-1 bis V-5) würden das Spielgefühl verderben, und was schlage ich vor?**

- **V-1 Mauerreparatur (gebaut).** Unbedenklich, aber teuer: 16 × Stufe / 100 je Prozentpunkt heißt bei Stufe 10: 1,6 Holz und 1,6 Stein je Punkt, also 160 Holz und 160 Stein für 0 → 100 % – genau der Wallpreis mal Stufe. Dauer 360 s je Punkt = 10 Spielstunden = 200 echte Sekunden (BELEGT – 7.3). Das Spielgefühl-Risiko liegt nicht im Preis, sondern in der **Kopplung**: eine Reparatur, die von 0 auf 100 zehn Spielstunden dauert, ist während eines laufenden Krieges praktisch unbrauchbar, und der Kampf bricht sie ohnehin ab (4.6). Ich schlage **vor**, den Zustand **in Zehnerstufen** springen zu lassen, wenn ein laufender Kampf eine Reparatur abgebrochen hat: `zustand_prozent` wird auf das nächste Vielfache von 10 **abgerundet**, damit ein Abbruch nicht den gesamten bisherigen Fortschritt in einen krummen Wert verwandelt. Zahl und Herleitung: der Sprung ist die kleinste Stufe, die im vorhandenen Wallstufenmodell (Stufen 1 bis 10, 4.6) eine Bedeutung hat. **VORSCHLAG.**
- **V-2 Heilungspreis (gebaut).** 75 % der Kostenposten ohne Siedler und Waren, Dauer 50 % (BELEGT – 4.11, 7.3). Ich halte das für die beste Zahl im Dokument: sie ist belegt, sie ist an drei Stellen anwendbar, und sie macht Verwundete zu einer echten Entscheidung statt zu einem Geschenk. **Kein Änderungsvorschlag.** Ein Hinweis: die Anzeige-Beispiele (Krieger 262,5 Gold / 0,75 Pferde) verlangen, dass die Anzeige **halbe Pferde** zeigen darf – `hilfen.zahl_de` mit zwei Nachkommastellen deckt das ab (4.11). Wird diese Anzeige an einer zweiten Stelle nachgebaut, ist F-04 gebrochen; deshalb steht in jedem Datenblock meiner Schnitte eine Lesefunktion und nie eine Formel in der Anzeige.
- **V-3 Ruhm-Ränge (gebaut).** 0/10/40/160 (VORSCHLAG laut Dokument selbst). Das Spielgefühl-Risiko: Stufe 3 (160) liegt bei 3,3 Punkten je Spieltag **48 Spieltage** weit weg – 6,4 echte Stunden. Der Rang wird damit für jeden normalen Spieler unerreichbar, und das ist bei einem Spiel ohne Siegscreen besonders schade, weil Ruhm die einzige Fortschrittsanzeige ist. Ich schlage **nicht** vor, die Stufen zu ändern (der Plan ist gesetzt), sondern die **Punktequelle** sichtbar zu machen: eine Kennzahl „Punkte je Spieltag“ im Kennzahlenblatt und ein Gate, das bei unter 2,5 warnt. Herleitung der 2,5: eigene Messung 3,3 (7.3), abzüglich der gemessenen Streuung von rund 25 %. **VORSCHLAG.**
- **V-4 Ereigniszahlen (geplant).** Die Dorf-Erträge (Holz 1.980, Stein 1.026, Nahrung 1.720, Gold 128 je Tag) sind plausibel und werden von mir unverändert übernommen. Kritisch ist die **Ereignisbemessung**: Haugs Tribut „990 Holz **oder** 64 Gold = halber Tagesertrag“ (7.2). 990 Holz ist genau der halbe Holzertrag, aber 64 Gold ist **nicht** der halbe Goldertrag – der halbe Goldertrag wären 64 (128/2 = 64). Das stimmt also, und ich übernehme beide Zahlen unverändert. Mein Einwand betrifft nur die **Frist**: zwei Spieltage Frist bei 8 echten Minuten je Tag heißt 16 echte Minuten Reaktionszeit. Das ist knapp für einen Spieler, der nebenbei arbeitet. Ich schlage **vor**, die Frist in `data/nachrichten.json` auszuweisen (nicht im Code) und im Kennzahlenblatt zu messen, wie oft ein Ereignis verfällt. Verfällt mehr als jedes fünfte Ereignis, ist die Frist zu kurz. **VORSCHLAG** (die 20 % als Schwellwert).
- **V-5 Rache-Schwelle (geplant).** 90 SK Wallstufe 3 plus 10 % Reserve = 99 SK. Die Rechnung ist nachvollziehbar (90 × 1,1 = 99) und belegt (4.6 nennt Stufe 3 = 90 SK Fußtruppen). Das Spielgefühl-Risiko ist nicht die Zahl, sondern die Quelle des Rachetopfs: „+1 je Spieltag ohne Kontakt“ (7.2) bedeutet, dass ein Spieler, der einfach nur baut, ab Tag 3 einen angekündigten Angriff bekommt. Das kann gewollt sein (E-8), ist aber die stärkste Beschleunigung im ganzen Plan. Ich übernehme die Zahl unverändert und schlage nur eine Bremse vor: der Zähler „ohne Kontakt“ **ruht**, solange ein Vertrag läuft (Schnitt 3). Herleitung: ein Vertrag, der nichts bewirkt, ist kein Vertrag. **VORSCHLAG**, weil 7.2 diese Kopplung nicht nennt.

**Frage 4 – Welcher alte Ablauf wird durch deinen Vorschlag überflüssig, und was müsste migriert werden?**

**Kein alter Ablauf wird überflüssig** – das ist mir wichtig festzuhalten. Die einzigen Änderungen an bestehendem
Verhalten sind:

1. `handel_start` gibt künftig `(ok, grund)` zurück statt eines Wahrheitswerts. Betroffen: die Aufrufstellen in `spieloekonomie.py` und `main.py` sowie die Anzeige. Migration: ein Commit, alle Aufrufer auf das Tupel umgestellt, alter Rückgabewert wird nicht mehr unterstützt (kein Doppelweg, F-04). **Fällt:** der alte Einzelwert. **Bleibt:** der gesamte Handelsweg. **Migriert:** die Aufrufer.
2. `data/nachrichten.json` bekommt den Typ `handel` mit eigener Frist. **Fällt:** nichts. **Bleibt:** `kampf` und `gesamtsieg` ohne Frist, Berichte 1 Spieltag (4.3). **Migriert:** nichts – alte Nachrichten ohne Typ `handel` laufen unverändert.
3. Der Götterschutz-Weg (`versorgungsschutz.py`) bekommt einen zweiten Ablehnungsgrund (NAP). **Fällt:** nichts. **Bleibt:** der Schutztopf und seine Punkteband-Logik. **Migriert:** nichts; der Weg ist danach die einzige Stelle, an der beide Gründe geprüft werden.

S5 (Umzug) wäre eine echte Ablösung – es gibt aber keinen alten Ablauf dafür, also auch dort keine Ablösung.
Ich liefere keine Vorschläge, die vorhandene Abläufe ersetzen, und markiere die drei Punkte oben ausdrücklich als
Schnitt-mit-Beleg statt als stillschweigende Änderung (Regel 13, Daniels Entscheidung vom 06.11.2026).

**Frage 5 – Welche drei Prüfungen würden meinen eigenen Vorschlag am schnellsten widerlegen?**

1. **Der Handelsweg-Grundzähler.** Fahre `tools/spieltest_simulation.py` über 12 Spieltage und lies die Ablehnungen je Grund. Wenn die häufigste Ursache nicht `kein_karren` oder `keine_ware` ist, sondern `kein_punktetyp`, dann ist meine ganze Diagnose in Schnitt 1 falsch: dann vergibt der Handelsweg gar keine Punkte, und es fehlt keine Erreichbarkeit, sondern eine Punktebuchung. Diese eine Zahl widerlegt oder bestätigt meinen ersten Schnitt.
2. **Der A/B-Lauf mit gleichem Startwert.** Fahre `tools/regelkreis.py` zweimal auf demselben Feld mit 20 % und mit 30 % Abweichung. Wenn beide Läufe **dasselbe** Urteil liefern, ist die Schwelle von 15 % wirkungslos und der Regelkreis misst nur Rauschen – dann ist mein Schnitt 8 in dieser Form wertlos, unabhängig davon, wie sauber die Wachen grün sind.
3. **Die Aufbauzeit-Zahl.** Fahre das Kennzahlenblatt vor und nach der Einführung des Rachetopfs. Wenn `aufbauzeit_bis_erstem_gefecht` **steigt**, habe ich mit Schnitt 3 gegen Abschnitt 4.12 verstoßen, obwohl alle 17 Wachen des Schnitts grün sind – genau der Fall, den E-4 beschreibt und den kein Prüffall im Schnitt 3 selbst fängt.

---

## Teil 8 – Ablagehinweise an unseren Agenten

Der folgende Block ist wortgleich aus Abschnitt 12 des Auftragsdokuments übernommen und ergänzt um die Angaben,
die Abschnitt 12 zusätzlich verlangt (Modell, Datum, Anzahl Teile, Version).

```
Ablage (fuer den Agenten):
- Zieldatei: docs/eingaenge/LLM_20261106/antworten/Antwort_UseAI-Instant_AUFTRAG_20261106.md
- Index:     docs/eingaenge/LLM_20261106/README.md  (Spalten: Datei, Modell, Datum, Teile, Urteil, Quelle)
- Rohform:   unveraendert ablegen, nicht redigieren; SHA256 beim Ablegen bilden und im Index nennen
- Nichts loeschen, nichts ueberschreiben: vorhandene Datei mit gleichem Namen bekommt _2, _3 ...
- Desktop:   die Antwortdatei gehoert NICHT auf den Desktop; nach der Ablage dort nichts liegen lassen
```

**Ergänzungen zu diesem Block, die aus Abschnitt 12 folgen und deshalb in der Antwort stehen müssen:**

- **Kopf der Datei:** Modell **UseAI Instant**, Datum **06.11.2026**, Anzahl Teile **8**, Version des Auftragsdokuments **Stand 06.11.2026, V_0.0.3**. Alle vier Angaben stehen im Kopf dieser Datei.
- **Eine Datei, keine Anhänge.** Diese Antwort ist eine einzige Markdown-Datei; sie ist ohne Anhang lesbar. Es gibt keine angehängten Dateien, keine Bilder, keine Archive.
- **Keine flüchtigen Links.** Diese Antwort enthält keinen Verweis auf `blob:`, `/mnt/data/` oder eine andere flüchtige Adresse. Alle Belege sind als Dateiname, Funktionsname, Aufruf oder als Stelle im Auftragsdokument angegeben.
- **Wahl des Datums im Pfad:** Ich setze `LLM_20261106` entsprechend dem Kopf des Auftragsdokuments (Stand 06.11.2026). Das Dokument verweist zugleich auf Dateien mit dem Datum 20261107 (`docs/S0_TABELLEN_20261107.md`, `docs/ABLAUF_20261107.md`). Ist der Zielordner nach dem Folgetag benannt, ist der Pfad entsprechend auf `LLM_20261107` anzupassen – die Ablage soll am Dokumentdatum hängen, nicht an einem Vorschlag von mir.
- **Rohform:** Diese Datei ist als Rohform gedacht und wird nicht redigiert. Die Kennzeichnung BELEGT / GERECHNET / VORSCHLAG / GESPERRT steht durchgehend im Text und zusätzlich gesammelt in Teil 5b, damit die Rohform ohne Umdeutung lesbar bleibt.

**Vorsicht-Hinweis, der ausdrücklich in meiner Antwort stehen muss (Abschnitt 13):**

> Meine Antwort wird nicht direkt eingebaut. Zwei bis drei Modelle bearbeiten dieselbe Datei; danach gleichen wir
> die Antworten gegeneinander ab und integrieren die nach unseren Prinzipien beste Methode. Jede Zahl aus einer
> Modellantwort ist bis zum Beleg ein VORSCHLAG. Beleg heißt: Handbuch 2009 mit Seite, 2006er Seite, Datendatei oder
> eine gerechnete Tabelle. Ohne Beleg wird die Zahl nicht eingebaut, sondern Daniel vorgelegt. Alte Abläufe werden
> nicht stillschweigend ersetzt: nur als eigener Schnitt mit Beleg – was fällt, was bleibt, was migriert.

**Vier Prüffragen – meine Vorleistung, damit sie ohne Umdeutung beantwortet werden können:**

1. **Passt es zur Mechanik?** Jeder Schnitt nennt im Feld „Ablösung“ und „Risiko“, welche bestehende Mechanik er berührt; kein Schnitt ändert eine vorhandene Formel oder Kampffunktion.
2. **Ist die Zahl belegt?** Jeder Datenblock hat eine Herkunftsangabe; alle Nicht-Belege stehen gesammelt in Teil 5b zur Vorlage bei Daniel.
3. **Hilft es dem Spielgefühl?** Jeder Schnitt nennt den Aufbauzeit-Effekt mit Begründung; drei Schnitte senken die Zeit bis zum ersten Gefecht, keiner hebt sie (S5 ausgenommen, und deshalb gesperrt).
4. **Braucht es ein neues Bauteil?** Neun neue Dateien, davon vier reine Werkzeuge (`kennzahlenblatt`, `regelkreis`, `abnahme`, `feedback_eingang`, `angebotswege_messung` = fünf) und fünf Fach-/Datendateien. Jedes Bauteil hat eine Begründung im Schnittfeld „Dateien“; kein neues Modul baut eine bereits gelöste Aufgabe nach (E-6).

---

## Selbstprüfung vor der Ablage

| Punkt | Zustand |
|---|---|
| Teil 1 Verständnis | geliefert, mit benannten Unsicherheiten |
| Teil 2 Einwände | 11 Einwände, je mit Beleg und Folge |
| Teil 3 Schnitte | 9 Schnitte, jeder mit allen neun Feldern aus Abschnitt 11 |
| Teil 4 Balancing-Konzept | 9.2 Punkte 1 bis 5, je mit Zweck, Eingaben, Ausgaben, Dateinamen, Aufruf, Beispielausgabe, Prüffall |
| Teil 5 Abschlusserklärung | A-1 bis A-7, je erfüllt oder offen mit Grund |
| Teil 6 Reihenfolge | 9 Positionen mit Abhängigkeiten |
| Teil 7 Nicht geliefert | 7 Positionen mit Grund |
| Teil 8 Ablagehinweise | wortgleich plus Ergänzungen |
| Anhang B Fragen 1 bis 5 | beantwortet |
| S5 | als gesperrter Vorschlag markiert, nicht als fertig |
