# Prüfung: Claudes Antwort auf Auftrag Nr. 19 (13.11.2026, Sitzung 44)

**Gegenstand:** `docs/eingaenge/CLAUDE_20261113_ANTWORT_AUFTRAG19_BILDAUFTRAG.md` (28.673 Byte,
sha256 `aa2f25b0…`). **Geprüft von:** Weltenfresser, mit eigenen Messungen — nicht durch Zustimmung.
**Ergebnis in einem Satz:** Inhaltlich tragfähig, alle Größen stimmen; **drei Fundstellen sind um 8 bis 10
Zeilen verschoben**, eine zusätzliche Messung verschärft seinen Verdacht aus Z1 erheblich.

---

## 1. Der Werteblock — nachgerechnet, Zeile für Zeile

| Größe | Seine Formel | Sein Wert | Nachgerechnet | Urteil |
|---|---|---|---|---|
| Ruine | 4 × 44 | 176 | **176** | stimmt |
| Drache | 4 × 44 | 176 | **176** | stimmt |
| Startbild | 4 × 1024 × 4 × 720 | 4096 × 2880 | **4096 × 2880** | stimmt |
| Kopfband Breite | 4 × 1127 | 4508 | **4508** | stimmt |
| Kopfband Höhe | 4508 × 150 / 780 | 867 (er empfiehlt 868) | **866,92 → 867** | stimmt; 868 ist 1 px daneben (Verhältnis 5,194 statt 5,2) und im Beschnitt ohne Wirkung |
| Goldrahmen | 4 × 920 | 3680 | **3680** | stimmt |
| Goldrahmen-Band | 3680 × 3,35 % | 123 | **123** | stimmt |
| Goldrahmen-Ecken | 3680 × 7,5 % | 276 | **276** | stimmt |
| Kachelrahmen | 4 × 64 | 256 | **256** | stimmt |
| Leiste Mitte | 4 × 64 × 4 × 34 | 256 × 136 | **256 × 136** | stimmt |
| Leiste Enden | 4 × 16 × 4 × 34 | 64 × 136 | **64 × 136** | stimmt |
| Marktplatz | 4 × 96 | 384 | **384** | stimmt |
| Beschnitt Kopfbänder | 217 − 200 | 17 px | **17 px** (1127 × 150/780 = 216,7) | stimmt |

**13 von 13 Zeilen stimmen.** Die 3,35 % und 7,5 % des Goldrahmens stehen wörtlich in
`data/gebaeude_motive.json` (`_warum_weltkarte`: „Band 14 px und Eckenradius 30 px am 400er-Kästchen“) —
14/400 = 3,5 %, 30/400 = 7,5 %; er hat die 3,35 % aus dem Kommentar übernommen, nicht aus 14/400
gerechnet. Bei 3680 px ergibt 14/400 **128,8 px** statt 123. **Das ist der einzige Zahlenstreit im
ganzen Dokument**, und er ist 6 px breit.

---

## 2. Die Fundstellen — drei sind verschoben

| Seine Angabe | Tatsächlich | Abweichung |
|---|---|---|
| `main.py:9189` für `_kennzeichen_bild` | **`main.py:9199`** (`_kennzeichen_bild`); 9189 ist eine Zeile IN `_lade_kachelrahmen` | 10 Zeilen |
| `main.py:9853` für `_leiste_kachel_bild` | **`main.py:9863`** | 10 Zeilen |
| `main.py:19103` für `startbild_photo("laden", …)` | **`main.py:19111`**; 19103 ist die Fenstergeometrie | 8 Zeilen |
| `main.py:3760` / `3764` Kopfband-Datei und Maße | **3760 und 3764** ✓ | — |
| `main.py:9177` für `_lade_kachelrahmen` | **9187** | 10 Zeilen |
| `main.py:16480` Drachen-Zeichenweg | **16476** (`_drachen_zeichnen`) | 4 Zeilen |
| `data/drachen.json:93` (Tardas → blau), `:138` (Salmur → lila) | **93** und **138** ✓ | — |
| `main.py:8851` Startbild „anmelden“ | **8851** ✓ | — |

Die Abweichungen sind **kein Denkfehler, sondern eine andere Zählweise** (er hat auf den Zeilenstand
seines ZIPs gezählt). Für die Arbeit heißt es: **jede Fundstelle vor dem Eingriff nachlesen**, nie
danach springen.

---

## 3. Inhaltliche Stichproben am Code — was stimmt

- **F3 Punkt 1 stimmt:** `PORTAL_KOPFBAND` ist **eine** Datei (Ghule), `PORTAL_KOPFBAND_MASSE = (780, 150)`
  — sechs Bänder je Volk brauchen eine Auswahl nach Volk.
  *(Stand 13.11.2026, 22:4x — inzwischen überholt: F3 ist gebaut, Register 639/640. `PORTAL_KOPFBAND`
  ist gelöscht, die Auswahl steht in `data/portal_kopfbaender.json`; die Masse `(780, 150)` gelten
  weiter. Der Befund oben beschreibt den Stand VOR dem Umbau und bleibt als Beleg stehen.)*
- **F3 Punkt 2 stimmt:** `MARKTPLATZ_KENNZEICHEN` ist ausdrücklich „in ANZEIGEGROESSE geschnitten
  (96 × 96), damit Tk die Datei ohne Pillow laden kann“ (`main.py:3762`) — eine 384er-Datei würde
  tatsächlich 4× zu groß erscheinen.
- **F3 Punkt 3 stimmt:** die Kartenbilder laufen über `_motivbild_skaliert` und werden seit F-99
  eingepasst; dort ist nichts zu tun.
- **Die Ruine ist wirklich leer:** `data/drachen.json:6` `"ruine_bild": ""`, `"ruine_platzhalter": true`.

---

## 4. Z1 — sein Verdacht ist bestätigt und schlimmer als gedacht (eigene Messung)

`assets/wappen/elfen_wappen.png` (1024 × 1024, die Meshy-Stilvorlage):

| Meßgröße | Wert |
|---|---|
| voll durchsichtige Pixel (Alpha = 0) | **60,4 %** der Fläche |
| davon mit RGB ≠ Schwarz | **96,2 %** |
| Mittelwert dieser „unsichtbaren“ Farben | **RGB (175, 171, 219)** — helles Lavendel |

Das heißt: **drei Fünftel des Bildes tragen eine helle Farbe, die nur durch den Alphakanal verdeckt
wird.** Jedes Werkzeug, das ohne Vormultiplizieren verkleinert (oder Alpha ignoriert), zieht einen
hellen Saum. **Folge für Dezember:** Freisteller nur mit Werkzeugen bearbeiten, die vormultiplizieren,
und die Bitte „transparent pixels black“ an das Modell tatsächlich mitschicken.

---

## 5. F1 — die Farbfragen, mit gemessenen Dateien beantwortet

Farbanteile der **deckenden** Pixel (Alpha ≥ 55 %), in 32er-Stufen zusammengefasst:

| Datei | häufigste Farben | Was das heißt |
|---|---|---|
| `burgen/burg_05.png` (479 × 550) | `#303010` 7,1 %, `#305010` 5,5 %, `#505030` 5,0 %, `#503010` 4,6 % | **dunkles Oliv bis Braun mit Gold** — „Grün/Schwarz/Gold“ ist wohlwollend; ein kräftiges Grün ist nicht drin |
| `wappen/wappen_08.png` (315 × 428) | `#101010` 19,0 %, `#301010` 11,7 %, `#501010` 7,4 %, `#701010` 6,8 %, `#903030` 4,8 %, `#b03030` 4,6 % | **schwarz mit rotem Drachen** — deckt sich mit der Chronik (Rot/Schwarz/Gold) |
| `wappen/wappen_09.png` (274 × 443) | `#101030` 16,3 %, `#103050` 15,7 %, `#303050` 6,1 %, `#f0f0f0` 3,2 % | **Nachtblau mit Weiß** — deckt sich mit Chronik und F-78 |
| `wappen/wappen_05.png` (271 × 420) | `#103050` 7,8 %, `#101010` 6,6 %, `#101030` 6,4 %, `#505050` 6,0 % | **dunkles Marineblau mit Grau** — „Eisblau“ ist am oberen Rand dessen, was die Datei hergibt |

**Damit ist F1 beantwortbar, ohne dass Daniel raten muss:**
- **Schattenfaust:** Wappen und Chronik sagen **Rot/Schwarz** — die Burg ist die Ausnahme (Oliv). Die
  stehende Regel „Hausfarbe folgt dem Wappen“ (05.11.2026) spricht **für Rot/Schwarz/Gold**.
- **Sternenwacht:** Weiß/Silber/Nachtblau ist durch die Datei gedeckt; die Meshy-Vorlage zeigt andere
  Farben (Waldelfen), ist aber **Stil**- und nicht Farbvorgabe (F-103).
- **Flickwerk:** bleibt offen — Chronik Grau/Schwarz/Gold gegen F-78 Eisblau/Weiß/Messing, und die Datei
  ist dunkelblau. **Hier entscheidet Daniel.**

---

## 6. Was noch offen ist und wer es entscheidet

| Punkt | Wer | Warum es blockiert |
|---|---|---|
| **F1 Flickwerk-Farbe** | Daniel | das sechste Kopfband und die Beschriftung hängen daran |
| **F2 „hochgerechnet = 4×?“** | Daniel | 4096 × 2880 und 4508 × 868 liefern die Modelle vermutlich nicht; ohne Antwort ist F-101 nicht erfüllbar |
| **F3 Codeanpassungen** (Kopfband je Volk, Kennzeichen verkleinern) | **Weltenfresser** | keine Entscheidung nötig, nur Arbeit — erst sinnvoll, wenn die Bilder da sind |
| **F4 B4 (Gebäude-Einzelansichten)** | Daniel | seine Liste, seine Reihenfolge |
| **F5 `drache_weiss.png` als Bildreferenz** | Weltenfresser | liegt vor (`assets/bilder/drache_weiss.png`), wird den Drachen-Prompts beigelegt |
