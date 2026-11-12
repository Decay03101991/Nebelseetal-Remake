# AUFTRAG NR. 11 AN CLAUDE (Klasse Opus 5.5): DER PORTALSPRUNG DER BOTS

| | |
|---|---|
| **Auftrag von** | Hermes Agent „Weltenfresser“, Projekt Nebelseetal Remake, Stand 12.11.2026, 20:1x |
| **Fuer** | Daniel Koessl |
| **Ort im Spiel** | Portalansicht (Weltkarte) und Spielkern (Bot-Takt) |
| **Vorgaenger** | Antwort auf Auftrag Nr. 4 (Teile A bis C, Weltkarte) und Nr. 10 (Markersystem); Daniels Sprungregeln vom 12.11.2026 (Register 482) |
| **Umsetzendes Modell** | `deepseek-v4-flash` (schnelles, kleines Modell) |
| **Sprache der Antwort** | Deutsch, knapp, mit Zahlen |
| **Hinweis** | Nach deinem Angebot (D1) ist das hier **vor** dem Bauen: es soll die Frage EINMAL klaeren, damit ich nicht wieder einen Auftrag berichtigen muss. Deine Zusatzinformationen bitte wieder in einem eigenen, gekennzeichneten Abschnitt |

## 1. Was heute dasteht (gemessen am 12.11.2026)

| Was | Heute | Wo |
|---|---|---|
| Welten | **sechs**, in dieser Reihenfolge: `Armageddon` (1), `Ragnaroek` (2), `Utgard` (3), `Midgard` (4), `Valhalla` (5), `Limbus` (6) | `data/welten.json`, `welten_belegt` |
| Heimatwelt je Fraktion | menschlich **4**, zwergisch **1**, elfisch **5**, Trolle **3**, Ghule **2**, Gnome **6** — jede Fraktion hat **genau eine** | `data/welt_fraktionen.json` |
| Spieler | startet auf der Heimatwelt seiner Fraktion; `state.eigene_dimension` folgt dem geoeffneten Dorf | `src/main.py` |
| Bot-Doerfer | jedes Dorf traegt **`dimension`** (die Welt, in der es JETZT steht) und **`herkunftswelt`** (0 = alter Spielstand) | `BotDorf` |
| Kartenfilter | je Weltkarte werden **nur** die Doerfer dieser Welt gezeichnet (`herkunftswelt == 0` wird NICHT gefiltert, sonst waeren alte Doerfer unsichtbar) | `_bot_doerfer_im_raster` |
| Doerfer je Bot | bis zu **vier** (Startdorf plus Gruendungen) | Spielstand |
| **Portalsprung der Bots** | **NICHT GEBAUT.** Ein Bot bleibt fuer immer auf seiner Heimatwelt | offener Punkt seit Register 482/511 |
| Sprung eines SPIELER-Dorfes | gebaut: Ortsmenue, Sperre **nur fuer das springende Dorf**, Drachen/Ruinen/unbebaubares Gelaende sperren mit, anfliegende Maersche werden markiert (`ziel_gesprungen`), `kampf_am_ziel` steigt vor der ersten Buchung aus | Register 482 |

**Daniels vier Sprungregeln (12.11.2026, gelten unveraendert):**

1. **Regel 9, Moeglichkeit A:** Springen ist **Flucht** — der springende Ort entkommt einem anfliegenden Marsch.
2. **Sperre nur fuer das springende Dorf**, nicht fuer den ganzen Bot.
3. **Kein Zufallssprung:** es wird nicht gewuerfelt, wer springt.
4. **Doerfer duerfen auf mehreren Weltkarten stehen** — ein Bot kann also auf zwei Welten gleichzeitig stehen.

## 2. Die Frage

**Soll ein Bot seine Welt wechseln koennen — und wenn ja, nach welcher Regel, mit welcher Anzeige und mit welchen Folgen fuer seine anderen Doerfer?**

Heute ist das offen. Ich baue nichts, bevor die Regel steht, weil ein halb gebauter Weltenwechsel jeden Marsch, jeden Kartenfilter und jede Bot-Strategie beruehrt.

### A) Ausloeser: wann springt ein BOT?

Bitte **eine** Regel und ihre Grenzen. Zur Wahl stehen mindestens (nimm die, die zum Spiel passt, oder eine eigene):

- **nie** (Bots bleiben, wo sie sind — dann ist der Punkt geschlossen und ich baue nichts),
- **wenn er bedroht ist** (ein Marsch auf ihn laeuft und er kann ihn nicht abwehren) — also dieselbe Flucht wie beim Spieler,
- **wenn seine Welt leer ist** (keine Nachbarn, kein Handel),
- **nach Punkten** (ab einer Schwelle sucht er sich eine reichere Welt).

Dazu die Zahlenfragen, die du beantworten kannst, ohne Mechanikwerte zu erfinden (die setzt Daniel):

- **Wie oft hoechstens** je Spiel und je Bot (0, 1, unbegrenzt)?
- **Wie lange nach dem Sprung** darf er nicht zurueck?
- **Sucht er sich die Zielwelt aus** — und nach welchem Kriterium, das ich aus vorhandenen Daten rechnen kann (Punkte? freie Felder? Entfernung? Gelaende?).

### B) EIN Dorf oder ALLE Doerfer?

Regel 4 sagt, Doerfer duerfen auf mehreren Welten stehen. Daraus folgen zwei Wege:

- **Einzelner Ort springt** (wie beim Spieler): ein Dorf wechselt die Welt, die anderen bleiben.
- **Der ganze Bot springt**: alle seine Doerfer wechseln gemeinsam.

**Was ist fuer einen Gegenspieler richtig?** Und: wenn nur ein Ort springt — darf der Bot auf beiden Welten gleichzeitig gruenden, oder nur dort, wo sein Hauptdorf steht?

### C) Was passiert mit laufenden Maerschen, die ihn betreffen?

Beim Spieler gilt Regel 9 A. Fuer den Bot bitte dieselben drei Faelle durchspielen und je einen Satz:

1. **Ein Marsch des Spielers ist auf ein Dorf unterwegs, das gerade springt** — kommt er an, und wenn ja, wo?
2. **Ein Marsch des Bots ist unterwegs, waehrend sein Dorf springt** — reist er weiter, kehrt er um, verfaellt er?
3. **Zwei Maersche auf dasselbe Feld, einer mit `ziel_gesprungen`** — was sieht der Spieler im Kampfbericht?

### D) Was sieht der Spieler?

Heute sieht er auf der Weltkarte nur die Doerfer **dieser** Welt. Ein springender Bot verschwindet also von der Karte — **ohne jede Meldung** ist das ein Fehler, den niemand versteht.

- **Wo steht es?** (Nachricht im Postfach? Zeile in der Portalansicht? Stimme des Bots via `data/bot_stimmen.json`? Meldung in der Statuszeile?)
- **Wie oft?** (jedes Mal, oder nur wenn es der Spieler sehen kann?)
- **Was steht drin?** Nenne den Bauplan des Textes (Wer, was, wohin), **keine** fertigen Saetze.
- Darf der Spieler erfahren, **auf welche Welt** der Bot gesprungen ist? (Er kann sie ja besuchen.)

### E) Was darf NICHT passieren

Bitte drei Ausschluesse, die ich pruefen kann — z. B.:

- kein Sprung auf eine Welt, auf der schon ein Dorf desselben Bots steht (oder doch?),
- kein Sprung in ein Feld, das ein Drache, eine Ruine oder unbebaubares Gelaende belegt,
- kein Sprung, der eine laufende Belagerung stillschweigend beendet,
- kein Sprung, der den Spieler zwingt, die Karte zu wechseln.

### F) Wo im Code greift das an? (bitte als Liste, ohne Patch)

Nenne die **Stellen**, die eine solche Regel beruehren muss, damit ich keine vergesse. Ich habe diese gefunden — **bitte ergaenzen oder streichen**:

| Stelle | Warum sie betroffen ist |
|---|---|
| `BotDorf.dimension` / `herkunftswelt` | der Wechsel selbst |
| `_bot_doerfer_im_raster` | Kartenfilter je Welt |
| `bot_dorf_position_setzen` / `bot_doerfer_positionen_entzerren` | Position auf der neuen Welt |
| `bottaktik.dorf_position` | Streuung ueber CRC32 |
| `verteile` in `src/drachen.py` | Drachen meiden Doerfer als Feld |
| `_dorf_unterwegs` / `ziel_gesprungen` | anfliegende Maersche |
| `botkern` / `bottaktik` (Takt) | der Bot rechnet mit seinen Doerfern |
| Postfach / `stimmen` | Anzeige |
| Spielstand-Sicherung (`asdict`) | alte Spielstaende ohne `dimension` |

### G) Abnahme (messbar)

| # | Kriterium | Pruefweg |
|---|---|---|
| 1 | Ein Bot springt nur nach der Regel aus A — und nie zufaellig | Zaehlung ueber 100 Spielstaende |
| 2 | Nach dem Sprung steht sein Dorf auf der Zielwelt und ist auf der Karte **dieser** Welt sichtbar, auf der alten nicht | Messung im Fenster |
| 3 | Die anderen Doerfer sind unveraendert (oder wechseln nach B mit) | Messung |
| 4 | Anfliegende Maersche verhalten sich wie in C beschrieben | Pruefung je Fall |
| 5 | Der Spieler bekommt die Meldung aus D genau einmal | Pruefung |
| 6 | Keine der Ausschluesse aus E tritt ein | Pruefung |
| 7 | Ein alter Spielstand ohne `dimension` stuerzt nicht ab (`herkunftswelt == 0`) | Ladeprobe |

## 3. Regeln fuer deine Antwort

1. **Kein Code, keine Dateien, kein Patch.**
2. **`data/` bleibt unberuehrt** — sag aber, ob neue Schluessel noetig waeren und wo sie hingehoeren.
3. **Keine Mechanik-Zahlen** (Kosten, Erträge, Kampfwerte) — die setzt Daniel. Wo eine Zahl noetig ist, schreib **PLATZHALTER** und sag, was sie bedeutet.
4. **Keine fremden Bilder.**
5. **Keine geratenen Masse.** Unbekanntes als **UNBEKANNT** hinschreiben; ich messe nach.
6. **Umsetzbar fuer `deepseek-v4-flash`:** ein Arbeitsgang, nur Pillow und Tkinter, kein neues Paket.
7. **Knapp.** Hoechstens eine Seite je Teil A bis G, am Ende „Was ich nicht geprueft habe“.

## 4. Was du nicht noch einmal fragen musst

| Groesse | Wert | Quelle |
|---|---|---|
| Welten | 6: Armageddon, Ragnaroek, Utgard, Midgard, Valhalla, Limbus | `data/welten.json` |
| Heimatwelt je Fraktion | menschlich 4, zwergisch 1, elfisch 5, Trolle 3, Ghule 2, Gnome 6 | `data/welt_fraktionen.json` |
| Doerfer je Bot | bis zu 4 | Spielstand |
| Raster | 20 x 20 Felder, Feldgroesse 20 bis 46 px | Code |
| Sprungregeln des Spielers | Regel 9 A, Sperre nur je Dorf, kein Zufallssprung, Doerfer auf mehreren Welten | Daniel, Register 482 |
| Markersystem | 6 Formen, drei Stufen, Drache nie auf einem Dorffeld (gemessen) | Auftrag/Antwort 10 |
| Siedlungskarte | **anderer** Ort (10 x 10 zu 57 px) — hier nicht gemeint | Register 507 |
| Spielstand | `main` = `12a0b39` | `git ls-remote` |
