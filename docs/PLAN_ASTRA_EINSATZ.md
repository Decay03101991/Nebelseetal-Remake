# Wann wir `gpt-6-astra` einsetzen — Einsatzplan

Stand: 04.10.2026. Guthaben OpenAI: **8,89 USD** (aufgeladen, Nachladen aus → keine Schulden möglich).
Freigabe von Daniel: „für diesen Auftrag die vollen 8,89 USD verwenden" — Ziel: das Spiel so gut
wie möglich machen.

---

## Der Grundsatz

**astra ist kein Arbeiter, sondern ein Gutachter.** Es schreibt keine Codeteile und läuft nie in
einer Werkzeugschleife. Belegter Fall vom 04.10.2026: ein agentischer Lauf mit 45.000-Token-Kontext
hat **1,50 EUR für nichts** verbrannt, weil jeder Umlauf den ganzen Kontext erneut bezahlt
(31 + 69 + 19 Shell-Befehle). Regel seitdem: ein Umlauf, kleiner Kontext, keine Werkzeuge,
`--reasoning medium`, nach 2 Minuten abbrechen, wenn nichts kommt.

astra kommt dorthin, wo **Urteilskraft** fehlt — nicht dorthin, wo Fleiß reicht:

| Nicht für astra | Warum |
|---|---|
| Code schreiben | Der eigene Weg ist belegt und geprüft: `src/einheiten.py`, `src/kampf.py`, 111 Prüfungen, alles nachvollziehbar. Ein starkes Modell macht das nicht besser, nur teurer. |
| Icon-Arbeit | Visuell. Entscheidet Daniel am Kontrollblatt — kein Modell sieht das besser. |
| Große Kontexte „lies das ganze Projekt" | Genau die Falle, die 1,50 EUR gekostet hat. |

## Die vier Einsatzstellen

### 1. Kampf-Regel-Audit (zuerst)
**Warum:** Der Kampf ist das Herz, und ein falsch gelesenes Detail verdirbt alles — z. B. welche
Einheiten als **Fußtruppen** zählen (meine Annahme: Nahkampf + Fernkampf), worauf Fernkämpfer
schießen, wie die 10 Sequenzen enden.
**Kontext (klein):** der Kampfabschnitt des Handbuchs **wörtlich** (`docs/original/ORIGINAL_Kampf_und_Punkte.md`)
+ eine knappe Beschreibung meines Ablaufs. Kein weiteres Projektwissen.
**Auftrag:** Abweichungen nennen, jede mit Zitat; Unsicheres als „Handbuch schweigt" kennzeichnen.
**Ergebnis:** Liste von Abweichungen. Ich prüfe jede gegen das Zitat und ändere nur, was hält.
**Kosten:** ~0,30–0,50 USD.

### 2. Konformitäts-Audit der 24 Seiten
**Warum:** Nicht jede Originalregel ist umgesetzt, und ich kenne meine eigenen Lücken nicht
vollständig. Beispiel: das Handbuch erlaubt **6 Siedlungen**, der Code lässt **3** zu.
**Kontext:** Handbuchtext + eine Liste, was der Code heute kann und nicht kann.
**Auftrag:** Prüfliste „Regel des Handbuchs → im Code vorhanden / fehlt / abweichend", je mit Seitenzahl.
**Ergebnis:** Arbeitsliste für W4b, W5, W6. Das ist der größte Hebel, weil es Vollständigkeit schafft.
**Kosten:** ~0,40–0,60 USD.

### 3. Wirtschafts-Entwurf für die fehlenden Zahlen
**Warum:** Das Handbuch nennt **Erträge, aber keine Preise** — Baupreise und Ausbildungsdauern fehlen
vollständig. Irgendwer muss ein stimmiges System entwerfen; raten ist verboten, entscheiden muss es Daniel.
**Kontext:** Ertragstabelle je Geländeart, Einheitenkosten, Forschungsregel, Taktgeber.
**Auftrag:** Ein nachvollziehbares Preissystem (z. B. aus Ertrag × Bauzeit) plus Pacing-Ziel für die
ersten drei Spieltage. **Jede Zahl als Vorschlag kennzeichnen**, nicht als Originalwert.
**Ergebnis:** ein Vorschlag, den ich Daniel zur Entscheidung vorlege (Eintrag in `PROJEKT_STAND.md`).
**Kosten:** ~0,30–0,50 USD.

### 4. Einzelspieler-Entwurf
**Warum:** Bots, Sieg/Niederlage, Götterschutz als Anfängerschutz, Zeitfaktor, Fortschrittsgefühl —
genau die Punkte, wo der Umbau von „Mehrspieler-Browser" zu „Einzelspieler" über Erfolg entscheidet.
**Kontext:** der Plan gegen die Handbuchseiten + die Einzelspieler-Abbildung + der Zielzustand.
**Auftrag:** konkreter Entwurf mit Zahlen; Widersprüche zum Original benennen.
**Ergebnis:** Grundlage für W5/W6/W7.
**Kosten:** ~0,50–0,70 USD.

## Reserve und Reihenfolge

Summe der vier Einsätze: **~1,5–2,3 USD**. Die restlichen **~6 USD bleiben Reserve** für Nachläufe,
wenn ein Audit etwas Wichtiges aufdeckt. Kein Einsatz ohne benannten Grund.

Reihenfolge nach Wirkung: **1 → 2 → 3 → 4.** Nach jedem Einsatz: prüfen, einarbeiten, einchecken —
erst dann der nächste.

## Prüfpflicht (meine Arbeit, kostenlos)

Keine Aussage von astra wird übernommen, nur weil sie plausibel klingt:
- Jede genannte Abweichung wird **am Zitat im Handbuch** nachgeschlagen.
- Zahlen werden **gegen die Datendateien** geprüft, nicht gegen das Modellgedächtnis.
- Was sich nicht belegen lässt, wird als „Entwurf, nicht Original" gekennzeichnet.
- Die Prüfläufe müssen grün bleiben (`run_tests.bat`, derzeit 111 Prüfungen).

## Zeitpunkt

Die 8,89 USD sind ein **Vorrat**, kein Tageskontingent — die Credits verfallen nicht um Mitternacht.
Die Tagesgrenze von 4 EUR gilt weiter über alle Modelle. Heute sind davon ~3,7 EUR verbraucht.
Deshalb: Einsätze auf die kommenden Tage verteilen, statt heute die Tagesregel zu reißen — außer
Daniel will einen Einsatz heute ausdrücklich.
