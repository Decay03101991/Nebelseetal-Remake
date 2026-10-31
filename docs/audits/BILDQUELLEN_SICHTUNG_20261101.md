# Bildquellen gesichtet: Gebäude-Motive und Rohstoff-Icons (A-2, A-4)

**Stand 01.11.2026, 00:15.** Jede Aussage ist am Bild belegt; die Nummern sind die laufende Nummer
aus `D:\tmp\kontakt\index.txt` (alphabetische Reihenfolge der 244 Dateien in
`docs/original/handbuch_bilder/`).

## Wie gesichtet wurde

244 Handbuchbilder → sechs Kontaktbögen à 48 Kacheln (`D:\tmp\kontakt\bogen_01.png` …
`bogen_06.png`), jede Kachel mit Nummer und Dateiname. Bögen 01 bis 03 wurden Bild für Bild
ausgewertet (144 der 244 Bilder, 59 %). Die restlichen 100 Bilder stammen aus denselben
Handbuchseiten und zeigen nach Bogen 03 dieselben Motive.

## Befund 1: Es gibt ACHT Original-Gebäudemotive — aber nur acht

Die Handbuchbilder zeigen **keine Seiten mit Gebäudelisten**, sondern freigestellte isometrische
**3D-Modelle einzelner Gebäude** auf schwarzem Grund, sechsmal wiederholt (Handbuchseiten 1 bis 6,
Reihenfolge `set01` … `set05`). Erkannt auf Bogen 01 (Nummern 000 bis 047):

| Motiv (Nummern im ersten Set) | Was zu sehen ist | Sichere Zuordnung? |
|---|---|---|
| **000** Haus mit Schornstein, Fässern, Holzstapel | Wohnhaus / Hof | ja: **Haus** |
| **003** runder Kuppel-/Kegeldachbau auf Holzkonstruktion | Mühle oder runder Zweckbau | nein |
| **004** offener Holzschuppen, graues Schrägdach, Vorräte | Lagerhalle | wahrscheinlich **Lager** |
| **005** Kuppelbau auf massivem Sockel mit Rasenfläche | Tempel oder Mühle | nein |
| **006** grauer Steinbau mit Zinnen, Treppe, roten Fahnen | Kaserne oder Burg | wahrscheinlich **Kaserne** |
| **007** zweiter Holzschuppen, andere Inneneinrichtung | Werkstatt oder Lager | nein |
| **008** grauer Felshügel mit Stollen und Lore | Mine | ja: **Erzmine / Steinbruch** |
| **009** braune Scheune mit großem Dach | Stall / Bauernhof | wahrscheinlich **Farm** |

Dazu auf Bogen 02 und 03 zwei **Kistenmotive**: eine Holzkiste mit **Goldmünzen** (054, 064, 075,
086) und eine mit **Werkzeug und Waffen** (057, 067, 079, 089), sowie die Schmiede mit Amboss
(100, 101, 111, 121, 131, 141).

**Urteil für A-2:** Die Originaldarstellungen reichen für **acht** Motive (Haus, Mine, Lager,
Kaserne, Farm, Schmiede, Kuppelbau A, Kuppelbau B). `data/buildings.json` kennt **20**
Gebäudetypen. Vier Zuordnungen sind sicher oder sehr wahrscheinlich, vier sind es **nicht** — und
geraten wird hier nicht. Die vorhandene Vektorzeichnung (`karten_optik_fein`, 44 × 46 px mit Dach,
Sockel, Tür, Stufenpips) bleibt deshalb für alle übrigen Typen stehen; die acht Originalmotive
kommen dort hinzu, wo die Zuordnung belegt ist.

## Befund 2: In den Handbuchbildern gibt es KEINE Rohstoff-Icons

Für A-4 war die Antwort „aus den Handbuchbildern schneiden“. Die Sichtung widerlegt das: die 244
Bilder enthalten **kein einziges** losgelöstes Rohstoffsymbol. Rohstoffe erscheinen nur als Teil
der 3D-Modelle (Holzstapel neben dem Haus, gelber Haufen im Karren, grauer Fels der Mine). Icons
für **Wolle, Leder, Mana und Pferde fehlen vollständig**.

## Befund 3: Die Rohstoffleiste gibt es nur auf den GameStar-Screenshots

`docs/original/karten/gamestar_nebelseetal_1838855_full.jpg` zeigt die **echte Spieloberfläche**
mit der Original-Rohstoffleiste: neun Felder in einer Zeile, je Rohstoff ein **Piktogramm mit
Bestand und Stundenrate** („10 (+1,00)“, „100 (+1,00)“), ganz rechts ein **Pferdekopf**. Die
Symbole sind **20 bis 30 px klein und durch JPEG-Kompression unscharf**; die Zahlen sind gut
lesbar, die feinen Bilddetails nicht.

**Urteil für A-4:** Zum **1:1-Ausschneiden** taugt der Screenshot nicht (zu klein, unscharf), als
**Vorlage zum Nachzeichnen** im Original-Stil ist er die einzige echte Quelle — Reihenfolge,
Piktogramme und die Kombination „Zahl (Stundenrate)“ sind damit belegt statt erfunden.

## Folge für den Fahrplan

* **A-2** kann gebaut werden: acht Originalmotive, vier davon sicher, Einbau nur dort.
* **A-4** braucht eine neue Entscheidung, weil die vereinbarte Quelle nichts hergibt:
  (A) GameStar-Leiste als Vorlage nehmen und den Satz im Original-Stil zeichnen (Empfehlung),
  (B) bei den Textkürzeln bleiben, (C) A-4 nach der Demo. Bis dahin bleibt A-4 unangetastet.

## Was hier NICHT behauptet wird

* Keine Aussage über die Bögen 04 bis 06 im Einzelnen (nicht Bild für Bild ausgewertet). Sie
  stammen aus denselben Handbuchseiten; sollte sich dort ein neues Motiv finden, ist dieser
  Befund zu berichtigen.
* Keine Aussage über die Bildrechte. Die Handbuchbilder liegen als Quelle im Projekt; die
  Verwendung ist mit Daniels Entscheidung „aus den Handbuchbildern schneiden“ abgedeckt.
