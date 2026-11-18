# Bildbriefing Dezember 2026 — Daniels Entscheidungen und die eine Berichtigung

**Wozu dieses Blatt:** Claudes Antwort Nr. 21 (`docs/eingaenge/CLAUDE_20261118_BILDBRIEFING_NR21/`) ist die
Zeichner-Fassung. Vier Punkte waren darin offen; Daniel hat sie am 18.11.2026 entschieden. Dieses Blatt
gehört **vor** Claudes Dokument — wer zeichnet, liest zuerst hier.

## 1. Die vier Entscheidungen (Daniel, 18.11.2026, einzeln gestellt)

| Punkt | Frage | **Entscheidung** | Folge fürs Briefing |
|---|---|---|---|
| **D8** | Goldrahmen im Marktplatz-Kennzeichen (B13)? | **Der Rahmen bleibt.** | Prompt behält `thin rounded gold border`; im Negativ bleibt „frame“ **gestrichen** |
| **D11** | Farbe des Gnomen-Kopfbands (B8) | **Marineblau #103050** (Wappen `wappen_05`) | Gnomen-Prompt: `navy blue`, nicht `ice blue` |
| **D-c** | Burg oder Wappen bestimmt die Farbe? | **Die Burg gilt** — Trolle grün/oliv (`burg_05`), Gnome eisblau (`burg_06`) | Farbangaben der Bildaufträge folgen der Burg; Ausnahme ist das Gnomen-**Kopfband** (D11) |
| **Klärung** | (Widerspruch D11 gegen D-c bei den Gnomen) | **Beide gelten, für verschiedene Bilder:** Kopfband Marineblau, die übrigen Farben des Hauses nach der Burg (Eisblau) | im Briefing je Datei die richtige Quelle nennen |

**Was ausdrücklich NICHT geändert wird:** die **Chronik** und `data/haeuser.json` behalten ihre
Farbangaben (Trolle „Rot, Schwarz und Gold“, Gnome „Grau, Schwarz und Gold“). Diese Sätze beschreiben die
**Wappen**, und die Wappen sind geliefert. D-c gilt für die **neuen Bilder**, nicht für die vorhandenen
Texte.

## 2. Die eine Berichtigung an Claudes Antwort

Claudes Abschnitt 0 setzt für Haus Sternenwacht das Wappen `wappen_09`. **Gemessen ist das falsch:** die
verbindliche Datei ist `assets/wappen/elfen_wappen.png` (1024 × 1024, sha256 `8041ec43…`); `wappen_09`
(274 × 443, sha256 `47141319…`) ist eine andere Datei. Überall, wo das Elfenwappen gebraucht wird, gilt
`elfen_wappen.png`.

## 3. Was schon berichtigt ist (18.11.2026, Register 671)

Die Besucherseite `index.html` und `FRAKTIONEN_WELTEN.md` zeigten fünf von sechs Haus-Wappen falsch (Bild
**und** Text). Beide folgen jetzt `data/haeuser.json`, die Chronik war bereits richtig.

## 4. Was der Zeichner noch wissen muss (aus der Nachrechnung)

- **Seitenverhältnisse:** 0 px Toleranz bei B1, B2, B10, B12, B13; ±1 px bei den hochgerechneten B5, B8, B9.
  Die Leisten-**Endstücke** sind **8 : 17** (64 × 136), die Leisten-**Mitte** 32 : 17 (256 × 136).
- **Alpha:** `alpha: true` heißt PNG **Farbtyp 6** (RGBA); `alpha: false` heißt **Farbtyp 2** (RGB) — nicht
  Farbtyp 6 mit lauter deckenden Pixeln. B5 ist JPG.
- **Farben je Haus** (gemessen an den gelieferten Wappen, 32er-Stufen ab 0): Silberbach #200000 / #600000 /
  Gold #a06020 · Hammerhall #202020 / #000000 / #604020 · Sternenwacht #002020 / #004040 / Silber #a0a0a0 ·
  Trolle (Wappen) #000000 / #200000 / #400000 / #600000 — **neu nach der Burg: grün/oliv** ·
  Knochenmoor #000000 / #402060 / #402040 · Gnome (Wappen) #002040 / #404040 — **Kopfband marineblau, sonst
  eisblau nach der Burg**.
- **Eckenradius:** Weltkartenrahmen 7,5 % (30 px von 400, Datenwert `gebaeude_motive.json`), Kachelrahmen
  **UNBEKANNT** — Vorschlag 1,5 × Band (Claude, ausdrücklich als Vorschlag gekennzeichnet).
