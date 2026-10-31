# Dimensionen: Ableitung der sechs aktiven Dimensionen

**Projekt:** `D:\Arbeiten\Nebelseetal_Remake` · **Stand:** 31.10.2026 · **Art:** reine Lese-Ableitung
(keine Datei im Projekt geändert, kein Test gestartet)

**Auftrag:** Daniel hat entschieden: **20 Dimensionen als Kulisse, 6 davon aktiv**
(`docs/ENTSCHEIDUNGEN_CODEAUDIT_20261031.md` Z. 12: „(d) Dimensionen: 20 Kulisse, 6 aktiv"), und die
Auswahl übertragen — ebd. Z. 40: „Leite die 6 aus dem Handbuch ab, lege mir keine Liste vor, bau es
sinnvoll". Die Regel dazu steht ebd. Z. 44–46: „erst Quelle, dann Indiz, dann eigene Lösung — und
jede eigene Festlegung wird im Prüfregister als VORSCHLAG geführt, nie als Beleg."

**Urteilsmaßstab** (`docs/PRUEFREGEL_ORIGINAL.md` Z. 12–17): **BELEGT** = Quelle sagt es wörtlich,
Zitat steht dabei · **INDIZ** = die Quellen deuten darauf, sagen es aber nicht · **VORSCHLAG** =
bewusste Remake-Entscheidung, klar gekennzeichnet.

---

## 1. Quellenlage

### 1.1 Handbuch — `docs/original/Nebelseetal_Spielanleitung_2009.pdf` (Textfassung: `Spielanleitung_2009_Textfassung.txt`, 24 Seiten)

- Z. 80 wörtlich: „Alle Welten in Nebelseetal, liegen im magischen Limbus, der sich in **20 Dimensionen** aufteilt."
- Z. 81–84: Portale verbinden die Dimensionen; „Je weiter eine andere Spielwelt von Deiner Welt entfernt liegt, desto mehr Mana kostet es, das Portal zu öffnen".
- Das Wort „Dimension" kommt im ganzen Handbuch **nur an dieser einen Stelle** vor (Volltextsuche über 1.366 Zeilen).
- **Kein Dimensionsname steht im Handbuch.** Auch kein Start-, kein Reihenfolge-, kein Gefährlichkeitshinweis.
- Z. 5 datiert das Dokument selbst: „(01.09.2006)" — der Dateiname „2009" ist eine Projektbezeichnung, keine Selbstauskunft des Originals.
- Götterschutz Z. 214–236 ist eine **reine Punkteregel**; der einzige Portalbezug ist Z. 234–236: „ihre Namen in der Ruhmeshalle und im Portal grün dargestellt werden" (siehe 5.4).

### 1.2 Vorversion 2006 — `docs/original/Spielanleitung_2005/portal.php.txt`

- Z. 21–22 wörtlich: „Es gibt **20 Dimensionen**, in jeder Dimension sind **20 mal 20 Felder** frei für Spielerwelten."
- Z. 16–19: „Die ersten beiden (X und Y), zeigen die Position Eurer Welt, auf einem zweidimensionalem Raster, in Eurer Dimension an. Die dritte Zahl (Z) zeigt die Dimension an".
- Z. 11–14: „Liegt Sie weit von Eurer Welt entfernt, oder gar in einer anderen Dimension, kostet es Euch viel Mana."
- Z. 23–25: Koordinatenwechsel „einmal binnen 24 Stunden", „5.000 Mana" aus einer Siedlung.
- Z. 40–43: „Eure Welt wird durch ein grünes Banner markiert, fremde Welten durch rote."
- Z. 44–46: „Mit dem Auswahlmenü über dem Raster könnt Ihr Euch die Karten der anderen Dimensionen ansehen." — das Menü listet die Dimensionen also **als Zahl, nicht als Name**.
- **Fazit dieser Quelle: Z ist ein Index, kein Name.**

### 1.3 Alte Website, Screenshot-Seite — `docs/original/recherche/screens.html` (Wayback 06.12.2006)

- Z. 101–106 wörtlich sechs Login-Ziele: **Armageddon, Ragnarök, Utgard, Midgard, Valhalla, Limbus**.
- Jedes Ziel ist eine eigene Subdomain mit eigenem `login.php` (z. B. `armageddon.nebelseetal.de/login.php`).
- Dies ist die **einzige Stelle mit einer vollständigen Sechserliste in einem Menü** — und die einzige, auf der die Zahl 6 überhaupt vorkommt.
- Die Namen stehen dort unter „Login", nicht unter „Portal" und nicht unter „Dimension".

### 1.4 Vorversion 2006, Anleitungsseite — `docs/original/Spielanleitung_2005/anleitung.php.txt`

- Z. 17–22: dieselben sechs Namen in der Navigation, in derselben Reihenfolge, ohne jede Erläuterung.
- Zweiter, unabhängiger Beleg für die Sechserliste (andere Seite, andere Aufnahme als 1.3).
- Die Seite beschreibt im Text nur „hier könnt Ihr Euch die aktuelle Version der Spielanleitung herunterladen" — die Namen sind reine Menüeinträge.

### 1.5 Website-Erzählung — `docs/original/website/` (Dateien ISO-8859-1; Umlaute hier korrekt wiedergegeben)

- `beschreibung.php` Z. 70–73: „Auf jeder Welt in Nebelseetal-Online gibt es ein Magisches Portal, welches eure Welt mit vielen weiteren Welten verbindet. **Dies sind die Welten von anderen Spielern**, die dort ihrerseits Siedlungen errichtet haben."
- `hintergrundgeschichte.php` Z. 127–132: „Vor langer Zeit war die Welt eine Einheit..." — erschaffen von drei göttlichen Drachen: „Epheus der Weiße", „Tardas der Grüne", „Salmur der Rote".
- `hintergrundgeschichte2.php` Z. 126 wörtlich: „die Realitäten verschwammen und splitteten sich zu vielen Welten auf, welche nun, nur noch durch magische Korridore miteinander verbunden waren."
- `hintergrundgeschichte3.php` Z. 122 wörtlich: „Auf jedem einzelnen **Bruchstück** der alten Welt, die nun im magischen Raum, dem Limbus, verstreut liegen, entstand ein magisches Portal."
- Der Bruch in viele Welten ist damit **belegt** — die Zahl 20 und die sechs Namen stehen aber **nicht** in der Erzählung.

### 1.6 Spieleverzeichnis — `docs/original/karten/QUELLEN_WEB.md` (Galaxy-News-Eintrag, Stand Oktober 2006)

- Z. 94 wörtlich: „**Spielwelten: 4-9**".
- Z. 104 nennt die News-Titel „Neuer Server bei Nebelseetal" (06.09.06) und „**Neuer Server Utgard**" (29.05.06).
- Damit sind die sechs Namen **Server- bzw. Spielweltstarts** eines Spiels mit 4–9 laufenden Welten — nicht Dimensionen. **INDIZ.**

### 1.7 Archivdaten — `docs/original/recherche/cdx_nocollapse.txt` (erste Aufnahme je Subdomain)

- midgard 2005-10-01 · valhalla 2005-10-01 · midagrad (Schreibvariante) 2005-10-13 · limbus 2005-10-23 · utgard 2006-07-07 · armageddon 2007-09-11 · ragnaroek 2007-09-20.
- Die sechs Namen erscheinen **gestaffelt über zwei Jahre**. Ein Kosmos aus 20 Dimensionen wird nicht im Halbjahrestakt „eröffnet"; Spielwelten werden es. **INDIZ** für Serverdeutung.
- Gegenprobe 2009: `website/hintergrundgeschichte3.php` Z. 100–102 führt nur noch **drei** Login-Ziele (Armageddon, Valhalla, Limbus) — Welten wurden also wieder geschlossen.

### 1.8 Projektinterne Vorlage (keine Originalquelle, nur Stand der Prüfung)

- `docs/PRUEFREGEL_ORIGINAL.md` Register 3 und 24 (Portal, 20 Dimensionen, X-Y-Z, grün/rot) = BELEGT; Register 44 („die 20 Dimensionen ... werden im Einzelspieler zu **Ländereien**") = VORGABE DANIEL / VORSCHLAG.
- `docs/audits/BEFUND_A2_WEGZEIT_20261031.md` Z. 44: empfiehlt „20 Dimensionen als Hintergrund behalten, aber nur **5–7** für den Spieler aktiv freischalten".
- `docs/HANDOFF_20261031_1400.md` Z. 49: „Dimensionen als Ländereien (Frage 6, Entscheidung gefallen: 20 als Kulisse, 6 aktiv — Umsetzung in `data/welten.json` **offen**)."

---

## 2. Was im Code heute steht

| Gegenstand | Stand | Datei:Zeile |
|---|---|---|
| 20 Dimensionen, Kennungen `d01`–`d20` | vorhanden | `data/welten.json` Z. 52–98 |
| Sechs Dimensionen mit Weltnamen (`d01` Armageddon, `d02` Ragnaroek, `d03` Utgard, `d04` Midgard, `d05` Valhalla, `d06` Limbus) | vorhanden, je Feld `"welt"` | `data/welten.json` Z. 53–70 |
| Vierzehn Dimensionen ohne Welt, Namen „Dimension 07" … „Dimension 20", `"welt": null` | vorhanden | `data/welten.json` Z. 71–98 |
| Liste der sechs Namen als `welten_belegt` | vorhanden | `data/welten.json` Z. 18 |
| **Feld „aktiv"/„versiegelt"** | **fehlt vollständig** (Suche ohne Treffer in `data/welten.json`) | — |
| Belegte Regeln (20×20 Felder, 5.000 Mana, 24 h, grün/rot) | vorhanden | `data/welten.json` Z. 19–34 |
| Anordnung als 10×10-Ebene, `"anzahl": 20` | VORSCHLAG, so gekennzeichnet | `data/welten.json` Z. 35–42 |
| Portalkosten `100 + 25 × Schritte` (Manhattan) | VORSCHLAG, so gekennzeichnet | `data/welten.json` Z. 43–51 |
| Zugriff im Code | `DIMENSIONEN`, `WELTNAMEN`, `dimensionen()`, `welten()`, `entfernung()`, `portalkosten()`, `nachbarn()` | `src/welt.py` Z. 34–36, 60–67, 70–120 |
| Raster einer Dimension (20×20 = 400 Felder), `z` als **Listenindex 0..19** | umgesetzt | `src/portalraum.py` Z. 46–47, 79–80, 92–98 |
| Startdimension des Spielers = **1**, ausdrücklich VORSCHLAG | `self.eigene_dimension = 1` | `src/main.py` Z. 876–878 |
| Startdimension im zweiten Zustandsmodell = **0** | `"eigene_dimension": 0` | `src/spielschicht.py` Z. 187 |
| Jede Siedlung liegt per Vorgabe in Dimension **1** | `dimension: int = 1` | `src/main.py` Z. 244 |
| Dimensionswechsel im Transport **gesperrt** | `raise ValueError("Dimensionswechsel braucht eigene Portalregeln.")` | `src/spieloekonomie.py` Z. 328–329 |
| Dimensionswechsel im Handel **gesperrt** | `raise ValueError("Fremde Dimension benötigt noch unbelegte Missionstarife.")` | `src/spieloekonomie.py` Z. 1016–1017 |
| Bots haben **keine** Dimension | `bot_als_ort(..., dimension)` nur im Handelspfad | `src/main.py` Z. 1620, 1744, 1803 |
| Dimensionsname wird **1-basiert** gesucht (`eintraege[nummer - 1]`) | Anzeige | `src/main.py` Z. 4902–4907 |
| Portalansicht übergibt dieselbe Zahl als Index an `anzeige_raster` | Anzeige | `src/main.py` Z. 4954–4957 |
| UI-Zeile: „die sechs belegten Welten" | Anzeige | `src/main.py` Z. 4984 |
| Götterschutz 299 Punkte / ±20 % — **ohne jeden Dimensionsbezug** | umgesetzt | `src/punkte.py` Z. 225–226, 229–240 |
| Prüfungen: „genau 20 Dimensionen", „welten() liefert genau sechs" | grün | `tests/test_welt.py` Z. 21, 47 |
| Prüfung: `koordinate(0, 0, 0)["welt"] == "Armageddon"` (0-basierte Deutung) | grün | `tests/test_portalraum.py` Z. 82 |

**Kurz:** Es gibt heute 20 Dimensionen **als Anzeige**, sechs davon mit Namen, aber **keine** als
„aktiv" markierte Menge. Spielbar ist faktisch **eine** Dimension (alle Siedlungen `dimension=1`),
und dimensionsübergreifender Handel/Transport wird aktiv abgelehnt.

---

## 3. Ableitung der sechs aktiven Dimensionen

### 3.1 Warum genau sechs

1. **BELEGT:** Es gibt 20 Dimensionen, jede ein 20×20-Raster für Spielerwelten (1.2, Z. 21–22; 1.1, Z. 80). Von „aktiv" oder „versiegelt" sagt keine Quelle etwas.
2. **BELEGT:** Es gibt genau **sechs** namentlich belegte Welten/Weltenstarts (1.3, Z. 101–106; 1.4, Z. 17–22).
3. **INDIZ:** Diese sechs sind Spielwelten/Server, keine Dimensionen (1.6, Z. 94/104; 1.7).
4. **VORGABE DANIEL:** 20 Kulisse, 6 aktiv (1.8).
5. **Folge:** Die Sechs ist **nicht gewählt, sondern abgezählt**. A2 schlug 5–7 vor (1.8, Z. 44) — innerhalb dieser Spanne ist 6 die einzige Zahl, die die Quellen mit Inhalt füllen können. Eine fünfte oder siebte aktive Dimension hätte keinen belegten Namen; sie müsste erfunden werden.

### 3.2 Die sechs Dimensionen

| Name | Bedeutung laut Quelle | Warum aktiv (Begründung) | Urteil |
|---|---|---|---|
| **Midgard** | Nur der **Name** ist belegt (1.3 Z. 104; 1.4 Z. 20). Die Quelle gibt keine Bedeutung an. | Steht in der einzigen vollständigen Sechserliste (1.3) und in der zweiten Liste (1.4) — ohne sie wären es nur fünf der sechs dokumentierten Namen. Zusätzlich die einzige Welt mit drei Schreibvarianten im Archiv (`midgard`, `midagrad`, `midgrad`, 1.7), also die meistgenutzte — taugt damit als **Startdimension** (Mitte des 10×10-Rasters: x=5, y=5). | **INDIZ** (Name BELEGT; Rolle Start = VORSCHLAG) |
| **Armageddon** | Nur der **Name** ist belegt (1.3 Z. 101; 1.4 Z. 17). | Steht in beiden Sechserlisten. Im Archiv eine der beiden **spätesten** Aufnahmen (ab 2007-09, 1.7) und im Raster am weitesten von der Mitte entfernt (x=0, y=0; 10 Schritte) — natürlicher Platz für die **letzte** Stufe. | **INDIZ** (Name BELEGT; Rolle Endstufe = VORSCHLAG) |
| **Ragnaroek** | Nur der **Name** ist belegt (1.3 Z. 102; 1.4 Z. 18). Umlautschreibweise „Ragnarök" in der Quelle, kennungsfähig als `Ragnaroek`. | Steht in beiden Sechserlisten; Aufnahme ab 2007-09, also zusammen mit Armageddon die jüngste Welt — zweite **Endstufe** neben Armageddon (9 Schritte von der Mitte). | **INDIZ** (Name BELEGT; Rolle = VORSCHLAG) |
| **Utgard** | Nur der **Name** ist belegt (1.3 Z. 103; 1.4 Z. 19). | Steht in beiden Sechserlisten; eigene News-Meldung „Neuer Server Utgard" 29.05.06 (1.6) = eigenständige Welt, nicht Unterwelt einer anderen. Im Raster in der Ecke (x=0, y=9; 9 Schritte) — **Grenzland**. | **INDIZ** (Name BELEGT; Rolle = VORSCHLAG) |
| **Valhalla** | Nur der **Name** ist belegt (1.3 Z. 105; 1.4 Z. 21). | Steht in beiden Sechserlisten; Aufnahme schon 2005-10 (1.7), also eine der ältesten Welten. Liegt im Raster **direkt neben der Mitte** (x=4, y=4; 2 Schritte) — damit die billigste und früheste Fremddimension (Portalpreis 100 + 25×2 = 150 Mana). | **INDIZ** (Name BELEGT; Rolle = VORSCHLAG) |
| **Limbus** | Nur der **Name** ist belegt (1.3 Z. 106; 1.4 Z. 22). **Aber:** „Limbus" ist in denselben Quellen der **Name des Ganzen** (1.1 Z. 80 „liegen im magischen Limbus"; 1.5 `hintergrundgeschichte3.php` Z. 122). | Steht in beiden Sechserlisten und wurde 2009 noch als Login-Ziel geführt (1.7), ist also nicht stillgelegt worden. Im Raster in der äußersten Ecke (x=9, y=9) — **Rand des Limbus**. Die Doppeldeutigkeit ist **kein Remake-Fehler**, sondern im Original angelegt (eine Welt dieses Namens existierte nachweislich). | **INDIZ** (Name BELEGT; Rolle = VORSCHLAG; Doppeldeutigkeit = offene Frage 5.1) |

### 3.3 Was aus den Quellen NICHT folgt

| Behauptung | Status |
|---|---|
| „Diese sechs sind Dimensionen" | **nicht belegt.** Keine Quelle nennt eine Dimension beim Namen; Z ist überall nur eine Zahl (1.2, Z. 16–19 und 44–46). |
| Reihenfolge/Schwierigkeitsleiter der sechs | **nicht belegt.** Keine Quelle nennt Gefährlichkeit, Stufe oder Freischaltfolge einer Welt. Jede Leiter ist Balance (VORSCHLAG). |
| Startdimension | **nicht belegt**, sagt der Code selbst (`src/main.py` Z. 876: „das Handbuch nennt keine Startdimension"). Vorschlag: Midgard (Mitte). |
| Namensbedeutungen (Midgard = Mittelerde, Utgard = Außenwelt, Valhalla = Kriegerhalle, Ragnarök = Weltende, Armageddon = Endschlacht) | **außerhalb der Quellen.** Das ist nordische Mythologie und Allgemeinwissen, nicht Nebelseetal-Text: die Spielmythologie kennt drei Drachen (Epheus, Tardas, Salmur, 1.5) und keine nordischen Götter. Die Deutung taugt als **INDIZ für die Rollenverteilung**, nie als Beleg. |
| „Die sechs Namen stammen aus dem Portal" | **falsch.** Sie stammen aus dem **Login-Menü** (1.3 Z. 99–106; 1.4 Z. 17–22). |

---

## 4. Die 14 Kulisse-Dimensionen (VORSCHLAG)

**Grundsatz:** Die Kulisse braucht keine 14 erfundenen Eigennamen. Sie braucht eine ehrliche
Bezeichnung, die aus der Quelle stammt.

**Namensvorschlag: „Bruchstück 07" … „Bruchstück 20".**
Das Wort ist **belegt**: `hintergrundgeschichte3.php` Z. 122 — „Auf jedem einzelnen **Bruchstück** der
alten Welt, die nun im magischen Raum, dem Limbus, verstreut liegen". Die Zahl ist VORSCHLAG.
Damit bleibt sichtbar: das sind Welt-Trümmer im Limbus, keine bespielbaren Länder.

| Feld | Vorschlag | Begründung |
|---|---|---|
| `aktiv` | `true` bei `d01`–`d06`, sonst `false` | die fehlende Angabe aus Abschnitt 2; kleinster möglicher Eingriff in `data/welten.json` |
| `name` (inaktiv) | „Bruchstück 07" … „Bruchstück 20" | belegtes Wort (s. o.), keine Erfindung von Landschaftsnamen |
| Anzeige inaktiv | grau, Klick ohne Wirkung, Text „versiegelt" | keine Reise, keine Siedlung, kein Bot dort |
| Auswahlmenü Portal | alle 20 bleiben gelistet (1.2 Z. 44–46: das Original listet alle) | Originalstruktur bleibt sichtbar; die 14 sind nur nicht betretbar |
| Portalpreis | bestehende Formel unverändert (`100 + 25 × Schritte`) | Formel ist ohnehin VORSCHLAG (`data/welten.json` Z. 43–51) |

**Verworfene Alternativen:**

| Alternative | Warum verworfen |
|---|---|
| 14 Landschaftsnamen („Waldland", „Bergland", „Nebelsee-Ebene") | verspricht Gelände, das das 20×20-Raster nicht liefert; kollidiert mit den 7 Geländearten der Siedlungskarten (Wald, Steppe, Berg, Hügel, Nebelsee, Sumpf, Grasland), die bereits je Siedlung gelten |
| 7 Völker + 7 Geländearten als Namen | beide Listen sind belegt (`hintergrundgeschichte2.php` Z. 130: „Menschen, Feen, Echsenwesen, Zwerge, Gnome, Elben, Orks"), aber als Dimensionsnamen wecken sie falsche Erwartungen („Zwergen-Dimension") und sind inhaltlich nicht gedeckt |
| 14 nummerierte „Dimension NN" (heutiger Stand) | zulässig und ehrlich, aber blasser; kostet nichts, wenn Daniel es so lässt — die Umbenennung ist Geschmack, nicht Beleg |

---

## 5. Risiken und offene Fragen

### 5.1 „Limbus" ist zugleich Container und Teil — UNGEKLÄRT
`portal.php.txt` Z. 6/11 und das Handbuch Z. 80 nennen den **ganzen Raum** Limbus; gleichzeitig
existierte eine Spielwelt `limbus.nebelseetal.de` (1.3 Z. 106). Solange `d06` „Limbus" heißt, kann ein
Spieler nicht unterscheiden, ob er „im Limbus" (überall) oder „in Limbus" (Dimension 6) ist.
**Entscheidung nötig:** Bezeichnung „Limbus (Grenzdimension)" in der Anzeige, oder die Dimension
umbenennen (dann fällt aber ein belegter Name weg).

### 5.2 „Welt" bedeutet in den Quellen etwas anderes als im Code — Bezeichnungsfehler
Quellen: „Jede **Spielerwelt** liegt im magischen Limbus" (1.2 Z. 16) und „Dies sind die **Welten von
anderen Spielern**" (1.5). Die sechs Namen sind dagegen **Weltenstarts/Server**. Im Code heißt es aber
„die sechs belegten Welten" (`src/main.py` Z. 4984; `src/welt.py` Z. 8; `data/welten.json` Z. 5).
Die Zahlen sind richtig, die Bezeichnung ist es nicht — nach der eigenen Regel (Register 64,
Zitatkorrekturen) gehört das berichtigt.

### 5.3 Zählweise 1-basiert gegen 0-basiert — echter Stolperstein
`src/portalraum.py` behandelt `z` als **Listenindex 0..19** (Z. 79–80, 92–98), die Prüfung hält das
fest (`tests/test_portalraum.py` Z. 82: `koordinate(0,0,0)["welt"] == "Armageddon"`). `src/main.py`
führt den Zustand dagegen **1-basiert** (Z. 876–878) und benennt 1-basiert (Z. 4902–4907), übergibt
dieselbe Zahl aber als Index an `anzeige_raster` (Z. 4954–4957). Folge: Die Portalansicht beschriftet
„Dimension 01 — Armageddon", während `welt.koordinate(0, 0, 1)` bereits **Ragnarök** liefert.
Heute fällt es nicht auf, weil das Raster unabhängig von `z` gezeichnet wird — sobald Felder je
Dimension belegt werden, ist es ein Fehler. **UNGEKLAERT**, welche Zählweise gilt.

### 5.4 Grün bedeutet zweierlei — WIDERSPRUCH zwischen zwei Quellen
`portal.php.txt` Z. 40: grünes Banner = **eigene Welt**, rot = fremde. Handbuch Z. 234–236: grün im
Portal = **Spieler im Götterschutz**. Der Code hat nur eine Bedeutung: `portalraum.portalfarbe`
(Z. 164–172) färbt „eigene Dimension" grün, „fremde" rot. Wer die Handbuchstelle kennt, liest die
Farbe falsch. **Entscheidung nötig:** zwei Farben (z. B. Rahmen = Besitz, Punkt = Schutz) oder
Fußnote in der Ansicht.

### 5.5 „6 aktiv" ist heute nicht spielbar — die Sperren sitzen im Code
`src/spieloekonomie.py` Z. 328–329 (Transport) und Z. 1016–1017 (Handel) werfen bei unterschiedlicher
Dimension `ValueError`. Solange das so bleibt, ist jede Dimension außer der Startdimension
unerreichbar — auch wenn sie in `data/welten.json` als aktiv markiert wird. Die Portalregel für
Fremddimensionen ist ausdrücklich „noch unbelegt" (Z. 1017) und muss als VORSCHLAG gebaut werden.

### 5.6 Bots und Siedlungen kennen keine Dimension
`Settlement.dimension` steht auf 1 (`src/main.py` Z. 244); Bots bekommen eine Dimension nur
geliehen, und nur im Handelspfad (`src/main.py` Z. 1620, 1744, 1803). Eine Verteilung der sechs
aktiven Dimensionen auf Bots ist damit noch nicht möglich — jeder Bot landet sonst in Dimension 1.

### 5.7 Falsche Seitenangaben in den Docstrings — verstößt gegen die eigene Prüfregel
`src/welt.py` Z. 4 und `src/portalraum.py` Z. 4 zitieren „Handbuch 2009, S. 80–83 'Portal'";
`src/berater.py` Z. 200 zitiert „Handbuch S. 1/4/12". Das Portal steht auf **Seite 3**
(`Spielanleitung_2009_Textfassung.txt` Z. 79–84, Fußzeile „Seite 3" in Z. 85; PDF-Extraktion Z. 61–65),
und das Handbuch hat **24 Seiten**. Eine Seite 80–83 existiert nicht. Nach Register 64 sind
Belegangaben nachzuweisen — hier sind sie falsch.

### 5.8 Das „Handbuch 2009" datiert sich selbst auf 2006
Z. 5: „(01.09.2006)". Für die Dimensionen ändert das nichts, wohl aber für die in Register 30
behauptete Zeitfolge „2006er Seiten gegen Handbuch 2009": die Webseiten sind 2005/2006, das Handbuch
ist vom 01.09.2006. Die Trennung „alt/neu" ist damit eine Projektkonvention, keine Datierung.

### 5.9 Was Daniel entscheiden müsste

| # | Frage | Empfehlung |
|---|---|---|
| 1 | Startdimension Midgard (Mitte des Rasters, x=5, y=5)? | ja — einzige Welt mit drei Schreibvarianten, also die meistgenutzte; kostet keine Datenänderung, nur ein `rolle`-Feld |
| 2 | „Limbus" als Dimension behalten oder umbenennen? | behalten, aber in der Anzeige „Limbus (Grenzdimension)" nennen |
| 3 | 14 Kulisse-Dimensionen „Bruchstück 07–20" oder weiter „Dimension 07–20"? | „Bruchstück" (belegtes Wort), sonst unverändert lassen |
| 4 | Dimensionsübergreifender Handel/Transport: erlauben (dann Portalpreis-Regel nötig) oder gesperrt lassen? | erlauben, sonst ist „6 aktiv" reine Anzeige |
| 5 | Sollen die 14 versiegelten je eine Andeutung bekommen (ein Satz Text) oder gar nichts? | nichts — jede Andeutung wäre erfunden (Register: nichts erfinden) |
| 6 | Falls Daniel doch 5 oder 7 aktiv will: welcher Name für die zusätzliche Dimension? | dann muss ein Name erfunden und als VORSCHLAG geführt werden; die Quellen geben keinen her |

---

## 6. Ergebnis in einem Satz

Die sechs aktiven Dimensionen sind **Armageddon, Ragnarök, Utgard, Midgard, Valhalla und Limbus** —
weil diese sechs die einzigen namentlich belegten Welten des Originals sind (BELEGT als Namen,
INDIZ als Kandidaten, VORSCHLAG als Dimensionsbesetzung), und weil die Zahl 6 damit die einzige ist,
die sich abzählen statt erfinden lässt.

**Nicht abgeleitet, sondern gesetzt:** welche Dimension Start ist (Vorschlag Midgard), welche Rolle
die fünf anderen spielen, und wie die 14 Kulisse-Dimensionen heißen. Für all das schweigen die
Quellen.
