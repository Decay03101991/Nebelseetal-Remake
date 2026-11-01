# AUFTRAG an ein starkes Chat-Modell — Papier: Burgen, Wappen, Weltbild

**Für:** Daniels großes GPT-Chat-Modell (Lesezugriff auf das öffentliche GitHub-Repo, kein Schreibzugriff
auf den Arbeitsstand; siehe Abschnitt 1a).
**Von:** Hermes (Weltenfresser), Sitzung 01.11.2026.
**Ergebnis:** EIN Markdown-Dokument, das Daniel zurückgibt. Kein Code, keine Dateiänderung.

---

## 0. Rolle und Grenze

Du bist **Entwerfer**, nicht Programmierer. Du lieferst ein Papier, das ein anderer umsetzt.
Du erfindest **keine** Spielwerte. Was nicht in diesem Auftrag steht, ist für dich **UNBEKANNT**
und wird als `UNBEKANNT — von Hermes zu liefern` notiert, nicht geschätzt.

## 1. Das Projekt (alles hier ist belegt, nichts davon raten)

Lokales Einzelspieler-Remake eines Browserspiels: **Nebelseetal Remake**, Python 3.14 + tkinter,
JSON-Spielstand, offline, kostenlos. Kein Netz, keine Server, kein Mehrspieler.

| Gegenstand | Stand |
|---|---|
| Siedlung | 10 × 10 Felder, Originalkarten, Gebäude stehen auf Feldern |
| Weltbild | demnächst **20 × 20 Felder** (Entscheidung Daniel 01.11.2026) |
| Bots | **6 Bots, je genau ein Dorf**, feste Position, in dieser Stufe **kein Angriff, keine Taktik**; sie wirtschaften und handeln |
| Weltkarten | sechs belegte Namen: **Armageddon, Ragnarök, Utgard, Midgard, Valhalla, Limbus**; bespielbar zuerst **Midgard** und **Valhalla**, Start in **Midgard** |
| Bot-Erkennbarkeit heute | farbiger **Rahmen mit Bot-Nummer**; Wappen und Festungen wurden ausdrücklich auf später verschoben — **dieses Papier holt sie nach** |
| Transferwährung | Mana; Dorftransfer **500 Mana** (VORSCHLAG), Tempel **20/h auf Nebelsee, 5/h sonst** (VORSCHLAG) |
| Portal-Menü | oben die Liste der Weltkarten, darunter das Geländekästchen der aktuellen Welt |
| Fensterbreiten, die tragen müssen | 1420 px und 1600 px (darunter rutscht der Berater unter die Karte) |
| Stil | dunkle Skin, Originalvorlagen statt Emoji, jedes Menü und jeder Knopf mit genug Platz |

## 1a. Dein Zugriff auf das Repository — und seine Falle

Du kannst das öffentliche Repository lesen:
`https://github.com/Decay03101991/Nebelseetal-Remake`, Branch **main**.

**Gemessen am 01.11.2026, 09:50 (git ls-remote):** `refs/heads/main` steht auf **`954097aa`** — das ist
der **veröffentlichte Release-Stand vom 31.10.2026**. Der Arbeitsstand von Hermes ist **deutlich
weiter** (lokaler Kopf `52f5dab`, danach unversionierte Arbeit). Was du auf GitHub siehst, ist also
**nicht** der heutige Code.

Konsequenz für dich, verbindlich:
- **Für dieses Papier brauchst du den Code nicht.** Deine Grundlage ist dieser Auftrag. Wenn du im
  Repo nachschlägst, dann nur, um Begriffe zu verstehen.
- Jede Aussage über den Code trägt **Datei + Zeile** aus dem, was du wirklich gelesen hast — und du
  schreibst dazu: „Stand 954097aa, kann veraltet sein“. Alles andere ist **UNBEKANNT**.
- Nützliche Orte im Repo (Orientierung, keine Beweise): `docs/` (Konzepte, Register `PRUEFREGEL_ORIGINAL.md`,
  Protokoll `ENTWICKLUNGSPROTOKOLL.md`), `src/main.py` (Einstieg + Oberfläche), `src/gelaende.py`
  (Gelände und Bauerlaubnis), `src/wirtschaft.py` (Erträge), `data/buildings.json` (Erträge je Gebäude
  und Gelände), `data/units.json`, `tests/` (Prüfdateien).

## 2. Das Material (von Daniel geliefert, am Bild gemessen)

Paket `Hermes_Nebelseetal_Assets_Icons.zip`, zwei Kontaktbögen, **beide 1448 × 1086 px, RGBA mit
echter Transparenz**:

| Datei | Inhalt | Aufbau (gemessen) |
|---|---|---|
| `Nebelseetal_Burgen_Iconset_6er.png` | 6 Burgen-/Dorf-Icons für die Weltkarte | **3 Spalten × 2 Zeilen**; Inhaltsbänder der Spalten 12–483, 485–956, 965–1441; Zeilen 3–1051 (zwei Reihen) |
| `Nebelseetal_Wappen_Iconset_10er.png` | 10 Wappen-/Fraktions-Icons | **5 Spalten × 2 Zeilen**; Inhaltsbänder der Zeilen 83–512 und 542–996; Spalten durchgehend 6–1447 |

Zum Charakter der Bilder (README des Pakets, wörtlich sinngemäß): eigens erzeugte Fantasy-Icons für
dieses Projekt, „inspiriert von der allgemeinen Wirkung mobiler Fantasy-Strategiespiele“ — also
**keine Ausschnitte aus einem fremden Spiel**. Behandle sie als eigenes Material.

## 3. Aufgabe — sieben Teile, je mit Tabellenzwang

### Teil 1 — Schneideplan je Blatt
- Zellraster, Rand, Padding, **Alpha-Schwelle** (ab welchem Alphawert ein Pixel als Inhalt gilt),
  Vorgehen bei **berührenden** Icons und bei 1-px-Splittern.
- Zielgrößen und wofür: Weltkarte 64 und 96 px, Nachrichten-/Kopfzeile 48 px, Dialog 128 px.
- **Dateinamen** (ASCII, ohne Umlaute): z. B. `burg_01` … `burg_06`, `wappen_01` … `wappen_10`.
- Ausgabe als PNG mit Transparenz; dazu ein **Kontrollbogen mit Nummern und sichtbarem Schnittrahmen**,
  an dem ein Mensch erkennt, ob eine Figur angeschnitten ist.
- Nenne die Fallstricke, die du kennst (Skalieren erst nach dem Zuschnitt auf den Begrenzungsrahmen,
  kein JPEG als Zwischenschritt, Transparenz nicht gegen Schwarz prüfen, …).

### Teil 2 — Zuordnung
Welche Burg zu **wem**: Spieler und sechs Bots; welches Wappen zu welchem Bot. Berge die Begründung
aus dem, was du am Bildaufbau wirklich siehst (Krone, Burgtyp, Wappenfarbe, Symbole). Was du nicht
siehst, bleibt `UNBEKANNT`. Tabelle: `Nummer | Datei | Vorschlag für | Begründung am Bild | sicher?`

### Teil 3 — Wo die Bilder erscheinen
Je Ort eine Zeile: **Weltkarte** (eigenes Dorf vs. Bot: Burg, Wappen, Rahmfarbe, Nummer),
**Portal-Übersicht** (Weltkartenliste oben, Geländekästchen darunter), **Bot-Nachrichten**
(Absenderzeile mit Wappen), **Handelsdialog**, **Kampf- und Planungsseite**.
Immer mit: Größe in px, was bei fehlendem Bild passiert (**Fallback**), und was **nicht** passieren darf
(z. B. zwei Wahrheiten für dieselbe Bot-Farbe).

### Teil 4 — Weltbild 20 × 20
Zellgröße bei 1420 px und bei 1600 px Fensterbreite, gerechnet; wie **Burg + Wappen + Nummer +
Rahmfarbe** in einer Zelle Platz finden, ohne Überlauf; Hover nach Sekunden mit den Transferkosten;
Anwahlzustand eines freien Feldes; Legende. Nenne die Rechnung, nicht nur das Ergebnis.

### Teil 5 — Risiken und Wirkung
- Was bringt Spielgefühl, was ist Deko?
- **Top 10 nach Wirkung** (Tabelle: Rang | Maßnahme | Wirkung | Aufwand klein/mittel/groß).
- Welche Fragen muss Daniel entscheiden — höchstens 8, jede mit **Empfehlung zuerst**.

### Teil 6 — Sechs Bot-Steckbriefe (Vorschlag, klar als VORSCHLAG markiert)
Je Bot: **Name**, **Rahmenfarbe** (Farbwert als Hex, auf dunkler Haut lesbar), **Burg** (`burg_0?`),
**Wappen** (`wappen_0?`), **eine Zeile Charakter** (wie er im Handel und im Kampf klingt),
**Anrede** an den Spieler. Sechs Stück, sie müssen sich als Gruppe lesen lassen: einer gierig, einer
misstrauisch, einer großspurig, einer still, einer rachsüchtig, einer freundlich — die Zuordnung
darfst du vorschlagen, die Farben müssen auf der dunklen Haut unterscheidbar bleiben (nenne den
Kontrast-Gedanken, nicht nur den Hexwert). Dazu: welche der **10 Wappen** übrig bleiben (4) und wofür
sie taugen (freie Fraktion, Neutral, später Festung, Reserve).

### Teil 7 — Textpaket Deutsch (knapp, kein Emoji, kein Pathos)
Fertige Sätze, die ein Spieler liest, jeweils in **einer** Zeile:
1. Gründung mit Startgebäuden: „Holzfäller auf Wald (9,9) · Steinmetz auf Hügel (6,6) · Tempel auf
   Nebelsee (1,2)“ — Formulierung für **Wunschgelände** und für **Ersatz**, wenn das Wunschgelände fehlt.
2. Bot erkannt: Zeile auf der Weltkarte, wenn die Maus über einem Bot-Dorf steht.
3. Handelsangebot angenommen / abgelehnt (Ablehnung muss den Grund nennen).
4. Angriff entsandt (mit Marschdauer) / Ankunft / Heimkehr mit Beute.
5. Kundschafter-Bericht: exakte Truppenzahl und Wallstufe, ein Satz, der auch bei Abwehr Sinn ergibt.
6. Dorftransfer: Kosten, Bestätigung im Postfach, Sperre solange etwas unterwegs ist.
Regel für alle Texte: **die Zahl steht im Satz**, keine vagen Wörter („einige“, „reichlich“).

## 4. Formregeln für dein Papier

- **Deutsch**, Tabellen, **keine Emojis**, 200–320 Zeilen, kein Vorwort, kein Schlussgeplänkel.
- Urteil je Aussage: **BELEGT** (steht in diesem Auftrag) / **VORSCHLAG** (deine Empfehlung) /
  **UNBEKANNT** (fehlt).
- Keine erfundenen Dateipfade, keine erfundenen Zahlen, kein Pseudocode, der wie Projektcode aussieht.
- Abschnitte in genau dieser Reihenfolge: 1 Schneideplan, 2 Zuordnung, 3 Anzeigeorte, 4 Weltbild,
  5 Risiken und Top 10, 6 Bot-Steckbriefe, 7 Textpaket, dann **Offene Fragen an Daniel** (höchstens 8,
  jede mit Empfehlung) und **Was ich nicht wissen kann**.

## 5. Was Hermes damit tut

Hermes übernimmt dein Papier als `docs/design/ASSETS_UND_WELTBILD_<datum>.md`, prüft jede Zahl gegen
die echten Bilddateien und den Code nach und setzt es in den Schnitten S-5 (Weltbild) und S-7 (Bots) um.
Was du als `UNBEKANNT` markierst, wird **nicht** gebaut — es geht an Daniel.
