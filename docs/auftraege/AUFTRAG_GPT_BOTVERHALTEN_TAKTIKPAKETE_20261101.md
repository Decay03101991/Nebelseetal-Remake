# AUFTRAG 6 an das starke Chat-Modell — Verhaltens- und Taktikpakete für die Bots

**Stand:** 01.11.2026, 12:45. **Auftraggeber:** Daniel Kössl, über Hermes (Weltenfresser).
**Arbeitsstand des Spiels:** Commit **`8d100a2`** (Register 88). Das öffentliche Repo steht auf
**`954097aa`** und ist **nicht** der Arbeitsstand — verlasse dich auf die hier gemessenen Angaben.

**Gegenstand:** ein vollständig ausgearbeitetes System aus **Verhaltenspaketen (Taktiken)**, **festen
Volksattributen** und einer **Auswahllogik je Dorf**, mit der die Bots wie Mitspieler wirken: nachvollziehbar,
unterscheidbar, überraschend, aber **nicht** zufällig im Sinne von beliebig.

---

## 0. Rolle und Grenze

Du bist **Entwurfs-Autor**. Du lieferst Regeln, Zahlen, Tabellen und wörtliche Spielertexte, aber du änderst
**keinen** Code, startest **keine** Builds und machst **keine** Commits. Was du als **BELEGT** kennzeichnest,
muss eine Quelle im Projekt haben (Datei und Zeile oder ein Zitat aus dem Handbuch 2009); alles andere ist
**VORSCHLAG** oder **UNBEKANNT**. Keine Zahl ohne Quelle, keine Regel ohne Prüfmöglichkeit.

## 0a. Wer dein Papier umsetzt — und was das für dein Papier bedeutet

**Umsetzendes Modell: `deepseek-v4-flash`** (schnell, klein, arbeitet in einem Zug). Vorgabe Daniel
01.11.2026. Daraus folgt:

* **Prüfbare Regeln ohne Auslegung.** Eine Regel ist ein Satz, den ein Prüfskript nachrechnen kann:
  Bedingung, Wirkung, Grenzfall, Grenze.
* **Nur Standardbibliothek.** Kein neues Paket, keine Datenbank, keine Migration alter Spielstände.
  Zufall ausschließlich aus `random.Random(seed)` mit ausdrücklich genanntem Seed.
* **Jeder Teil in EINEM Arbeitsgang.** Ist ein Teil zu groß, teile ihn selbst und sage die Reihenfolge.
* **Spielertexte wörtlich, deutsch, mit Platzhaltern** in `{geschweiften Klammern}`. Keine Emoji.
* **Jede Regel ohne Fenster prüfbar.** Zu jeder Regel gehört die Wache: was wird gesetzt, was gelesen,
  was darf **nicht** passieren.
* Knapp. Tabellen statt Fließtext, keine Wiederholung dieses Auftrags.

---

## 1. Was du über das Spiel wissen musst (gemessen, nicht behauptet)

| Gegenstand | Stand | Belegstelle |
|---|---|---|
| Bauart | Python 3.14 + tkinter, JSON-Spielstand, offline, Einzelspieler gegen Bots | `src/main.py` |
| Ziel | **kein Sieg mehr** — `punkte.spielausgang` liefert nur `niederlage`/`weiter`; Bewertung über Auszeichnungen (Feldherr, Forscher, Händler, Gesamtherrscher) | `src/punkte.py`, Register E5 |
| Kernkreis | gründen → produzieren → forschen → ausrüsten → ausbilden → bewegen → kämpfen → punkten | `docs/PLAN_Einzelspieler.md` |
| Dörfer | **höchstens 6 je Spieler**, Grenze global über alle Weltkarten (`SIEDLUNGEN_MAXIMUM = 6`) | `src/main.py:263` |
| Wirtschaft | **jedes Dorf hat sein eigenes Lager** (`Settlement.vorraete`, `.waren`, `.einheiten`); die Reichsanzeige ist nur eine Summe, keine zweite Kasse | `src/main.py`, `ortsbestand_text` |
| Gebäude | 20 Gebäude mit Wirkung, Voraussetzung und `max_je_siedlung` in `data/buildings.json`; Erträge je Gelände | `data/buildings.json`, `src/gelaende.py` |
| Forschung | 21 Forschungen, je Dorf eigene Bibliothek, Verbundstand geplant (S-3) | `data/research.json`, `src/forschungspfad.py` |
| Waren und Ausrüstung | 17 Waren in drei Werkstätten (Schmiede, Bogenbauer, Nähstube); Einheiten brauchen Ausrüstung, nicht nur Gold | `data/items.json`, `src/ausruestung.py`, `src/werkstatt.py` |
| Einheiten | 28 Einheiten mit belegten Werten (LE/AT/PA/SK, Kriegspunkte, Kosten in Siedlern und Rohstoffen) | `data/units.json` |
| Kampf | Vorrunde über **SK** gegen Wallschwellen, dann Schlacht; Beute gestaffelt und ladungsgedeckelt | `src/kampf.py`, `src/kampfbericht.py` |
| Bewegung | jede Einheit reist als **Auftrag** (Hinweg und Rückweg), Reisezeit aus Entfernung und langsamster Einheit | `src/auftraege.py` |
| Portal | 20 Weltkarten, 400 Felder je Welt, Weltensprung kostet Mana und ist gesperrt, solange etwas unterwegs ist | `src/portalraum.py`, `src/main.py` |
| Uhr | Spieluhr (`state.spielsekunden`), nicht Rechnerzeit; Bot-Zug stundenweise (`BOT_TAKT_SEKUNDEN = 3600`) | `src/main.py:772` |
| Bots heute | **5 Gegner** (Haug, Brynhild, Grom, Silra, Krank — Fraktionen menschlich, menschlich, zwergisch, elfisch, monster) mit Temperament und Wirtschaft in `botkern`; Koordinaten, Dörfer und Taktik in `bottaktik` | `src/botkern.py`, `src/bottaktik.py` |

### 1.1 Der Ist-Stand der Bot-Logik (wichtig für dich)

**`src/botkern.py`** (Stand `2026-10-05.1`) rechnet die **Wirtschaft** des Bots: Startvorräte
(`VORSCHLAG_START_VORRAETE`), Wagenpark, Handelsneigung, Temperament (`TEMPERAMENT_SPANNE = 0.10`),
Handelspreis (`handelspreis(referenzpreis, temperament)`), Punkte (`bot_punkte`), Zug je Stunde
(`bots_tick`). **Dieses Modul ist im Spiel angeschlossen** (`main.py` ~2687).

**`src/bottaktik.py`** (Stand `2026-11-01.1`) ist der **Verhaltens-Zustandsautomat**: acht Zustände
(SAMMELN, WACHSEN, SICHERN, SUCHEN, MARSCHIEREN, RAUBERN, FLIEHEN, RAECHEN), fünf Taktiken
(Haug „Plünderer“, Brynhild, Grom, Silra, Krank) plus eine neutrale, Schwellenwerte, Gedächtnis,
Ankündigung vor einem Angriff. Schnittstellen: `taktik_von(bot)`, `tick(bot, welt, jetzt, rng)` →
Entscheidung, `wirkung_anwenden(bot, entscheidung, jetzt)` → **neuer** Bot (Eingabe unverändert),
`anzeige(bot)`, `pruefe_taktik()`, `offene_luecken()`. **Dieses Modul ist noch NICHT angeschlossen** —
der Anschluss ist der geplante Schnitt **S-7** (Bots nur mit Koordinaten, **kein Angriff** in jener Stufe).

**Was es heute nicht gibt:** Attribute je Volk, Boni je Verhalten, Auswahl eines Verhaltens **je Dorf**,
Umschalten im Spielverlauf, mehrere Dörfer je Bot (geplant: bis zu fünf weitere), irgendeine Bewertung,
welches Verhalten in welcher Lage gut ist.

**Daniels Entscheidungen, die du nicht ändern darfst** (01.11.2026): Bots gründen „ganz normal wie der
Spieler“ bis zu fünf weitere Dörfer; jeder Bot darf eine von mehreren Taktiken nutzen, „um durch
koordinaten näherung oder entfernung sich zu schützen oder eben anzugreifen“; Angriffe erst, wenn die
Taktik-Pakete existieren; Wappen und Festungen später.

---

## 2. Daniels Anforderung, wörtlich zerlegt

> „logische taktik entwürfe für bots die alle spielabläufe berücksichtigen und klug aufgebaut sind sodass
> bots eine art verhalten zu haben scheinen. aber das muss zufällig sein und vllt nur gewisse attribute an
> gewisse völker oder bots gebunden sind wie zum beispiel der bot hat grunsätzlich 5% mehr holzproduktion
> am anfang aber sobald er ein verhalten wählt kann er durch vorteile oder werte die ihm ein verhalten
> bringt z.b. noch einen angriffs boost für seine truppen haben wenn er sehr agressiv spielt aber für jedes
> gegründete dorf können bots ein anderes verhalten wählen somit kann man aus ein paar verschiedenen
> vorbereiteten taktiken oder verhaltensweisen durch insgesamt 5 andere bots und deren jeweils 6 dörfern
> später im spielverlauf schon viele verschiedene botverhalten aufeinander treffen und bots sollten das
> verhalten oder die taktik ihrer dörfer auch umwählen dürfen sodass es immer spannend bleibt wie der
> verlauf kommen wird aber die taktik oder verhaltenspakete müssen wirklich detailiert und gut integriert
> sein und gut funktionieren damit wir schauen können wie das spielverhalten sich dann anfühlt wenn die
> bots so agieren.“

Daraus sind **sieben** bindende Anforderungen geworden:

| Nr | Anforderung | Prüfbar heißt |
|---:|---|---|
| A-1 | **Alle Spielabläufe berücksichtigen** — nicht nur Kämpfen, sondern sammeln, bauen, forschen, ausrüsten, ausbilden, handeln, siedeln, reisen | jedes Verhalten nennt für jeden Ablauf, was es tut oder ausdrücklich nicht tut |
| A-2 | **Klug, aber zufällig** — der Bot soll nicht ausrechenbar sein, aber auch nicht dumm | Zufall nur aus Seed, mit Verteilung und Grenzen; dieselbe Lage + derselbe Seed = dieselbe Entscheidung |
| A-3 | **Feste Attribute an Volk/Bot** — z. B. 5 % mehr Holzproduktion ab Beginn | Attribut ist **dauerhaft** und vom Verhalten unabhängig |
| A-4 | **Boni aus dem Verhalten** — z. B. Angriffsboost bei sehr aggressivem Spiel | Bonus ist **verhaltensgebunden** und endet mit dem Verhalten |
| A-5 | **Ein Verhalten je Dorf** — jedes Dorf darf ein anderes wählen (bis 5 Bots × 6 Dörfer) | Datenmodell trägt das Verhalten **am Dorf**, nicht am Bot |
| A-6 | **Umschalten erlaubt**, damit es spannend bleibt | Regel für Auslöser, Sperrzeit, Ankündigung und Kosten des Wechsels |
| A-7 | **Detailtiefe und Integration** — man muss das Spielgefühl testen können | jedes Verhalten ist im Spiel sichtbar (Anzeige, Nachricht, Vorzeichen) und im Prüfstand nachweisbar |

---

## 3. Was dein Papier liefern soll — sieben Teile

### Teil 1 — Verhaltenskatalog (das Herzstück)

Liefere **8 bis 12 Verhaltenspakete**, jedes mit stabiler Kennung (`V-01`…`V-12`), deutsche Name, Kurzbeschreibung
in einem Satz. Je Verhalten **zwingend**:

| Feld | Inhalt |
|---|---|
| Zweck | was das Verhalten erreichen will (Wachstum, Sicherheit, Nähe, Beute, Rache …) |
| Bedingungen | wann es gewählt werden darf (Lage, Punkte, Truppenstärke, Nachbarschaft, Vorräte) |
| Aktionen je Spielablauf | was es in sammeln / bauen / forschen / ausrüsten / ausbilden / handeln / siedeln / reisen tut — **für jeden der acht Abläufe eine Zeile**, notfalls „ausdrücklich nichts“ |
| Werte | konkrete Zahlen (Schwellen, Anteile, Dauern) oder „aus vorhandener Quelle: <Datei>“ |
| Boni | was das Verhalten dem Dorf oder seinen Truppen gibt (A-4), mit Obergrenze |
| Nachteile | was es kostet — **jedes Verhalten muss einen erkennbaren Preis haben** |
| Sichtbarkeit | was der Spieler davon sieht (Anzeige, Nachricht, Vorzeichen im Weltbild) |
| Grenzen | was das Verhalten ausdrücklich **nicht** tut (z. B. keine Angriffe auf Welten, solange …) |

**Balancing-Regel:** kein Verhalten darf in allen Lagen das beste sein. Zeige das mit einer Matrix
„Verhalten × Lage“ (mindestens 4 Lagen), in der jedes Verhalten mindestens einmal vorne und mindestens
einmal hinten liegt. Ohne diese Matrix ist der Katalog nicht abgenommen.

### Teil 2 — Attribute und Völker

Zwei getrennte Schichten, klar getrennt (das ist A-3 gegen A-4):

1. **Volksattribute** (dauerhaft, ab Spielstart): für die vier belegten Fraktionen **menschlich,
   zwergisch, elfisch, monster**. Je Fraktion genau **zwei** Eigenschaften mit Zahl — z. B. Holzproduktion,
   Steinproduktion, Ausbildungsdauer, Handelspreis, Reisegeschwindigkeit, Wallwiderstand. Daniel hat
   ausdrücklich „5 % mehr Holzproduktion“ als Beispiel genannt. Begründe jede Zahl gegen den gemessenen
   Reichsertrag, nicht aus dem Bauch.
2. **Verhaltensboni** (nur solange das Verhalten gilt): je Verhalten höchstens **zwei** Boni, jeder mit
   Obergrenze und ausdrücklicher Dauer.

**Harte Grenzen, die du einhalten musst:** keine Boni, die eine Kernregel aushebeln (kein „Angriff ohne
Marsch“, kein „Wall wird ignoriert“, keine freie Forschung). Jeder Bonus wird **an einer Stelle** gerechnet
und ist im Prüfplan nachweisbar; keine zweite Rechenwahrheit.

### Teil 3 — Auswahl und Umschalten je Dorf

* **Wo steht das Verhalten?** Vorschlag für ein Feld am Dorf (Name, Typ, Vorgabewert, Verhalten bei alten
  Spielständen ohne das Feld). Keine Migration.
* **Wer wählt?** je Dorf eine Bewertungsfunktion über die Lage; sei **eine** Funktion mit klaren Summanden
  und Gewichten, kein Regelwald. Nenne die Gewichte als Tabelle.
* **Zufall:** wie viel Streuung, aus welchem Seed (`random.Random(seed)` mit zusammen­gesetztem Seed aus
  Spielstart-Seed, Bot, Dorf und Spieltag), damit derselbe Spielverlauf reproduzierbar bleibt.
* **Umschalten (A-6):** Auslöser (z. B. Niederlage, Nachbar wird stark, Vorräte knapp, Punkteabstand),
  Sperrzeit, Ankündigung im Spiel, Kosten. Der Spieler muss **sehen**, dass ein Dorf sein Verhalten
  wechselt — sonst wirkt es zufällig statt lebendig.
* **Verhalten der Bots zueinander:** dürfen Bots auf das Verhalten anderer Bots reagieren? Wenn ja: nur
  über das, was der Spieler auch sehen kann (keine Hellseherei).

### Teil 4 — Integration in den bestehenden Code

Nenne für jede neue Regel die Stelle, an der sie hingehört, und unterscheide sauber:

| Frage | Antwort erwarten wir |
|---|---|
| Was gehört nach `src/bottaktik.py` (Verhalten, Entscheidung, Zustände)? | Erweiterung des Zustandsautomaten, keine zweite Entscheidungsstelle |
| Was gehört nach `src/botkern.py` (Wirtschaft, Punkte, Handel)? | nur Wirtschaftswerte, keine Verhaltenslogik |
| Welche Wirkungen müssen im **Kern** gerechnet werden (Ertrag, Ausbildung, Kampfkraft, Reisezeit)? | eine Rechenstelle je Wirkung, mit Datei und Funktion |
| Was braucht der Spielstand (neue Felder)? | Name, Typ, Vorgabewert, Verhalten bei alten Ständen |
| Was braucht die Anzeige (Portal, Weltbild, Dorfzentrum, Nachrichten)? | je Ort ein Satz, was dort steht |
| Was **darf nicht** entstehen? | eine zweite Bot-Wahrheit neben `botkern`, eine zweite Kampfformel, eine zweite Punkteformel |

**Wichtig:** Bots dürfen nur tun, was der Spieler auch kann (dieselben Gebäude, dieselben Einheiten,
dieselben Reisezeiten). Ein Bot-Vorteil ist ein **Attribut oder Bonus**, niemals eine Ausnahme von der Regel.

### Teil 5 — Sichtbarkeit und Spielgefühl

Beschreibe, was der Spieler erlebt, wenn die Bots nach diesen Paketen spielen: Vorzeichen vor einem Angriff,
Nachrichten im Postfach („{Bot} in {Dorf} rüstet auf“), Anzeige im Weltbild (Rahmen mit Nummer, Verhalten als
kurzes Wort), Verhalten im Handel (Preise), Reaktion auf Niederlagen. Formuliere die Texte **wörtlich**.

### Teil 6 — Prüfplan

Eine Wache je Regel, ohne Fenster. Mindestens: Determinismus (gleicher Seed = gleiche Entscheidung),
Streuung (verschiedene Seeds = verschiedene Entscheidungen, aber innerhalb der Grenzen), kein Verhalten
dominiert (Matrix aus Teil 1), jeder Bonus endet mit dem Verhalten, Umschalten hält die Sperrzeit ein,
alte Spielstände ohne das neue Feld laufen, Bots tun nichts, was der Spieler nicht kann.

### Teil 7 — Recherche: gibt es das schon?

**Das ist ein eigener Auftragsteil und ausdrücklich erwünscht.** Prüfe, welche **fertigen Denkmodelle** es für
solche Gegner gibt und was davon auf unser Spiel passt — nicht als fertige Bibliothek (wir bauen selbst, nur
Standardbibliothek), sondern als **Bauplan**:

* **Utility AI / Nutzenbewertung** (eine Bewertungsfunktion je Aktion, Gewichte, Streuung) —
  passt am besten zu Teil 3.
* **Behavior Trees** (zusammensetzbare Knoten) — prüfe, ob der Aufwand gegenüber einem Zustandsautomaten
  gerechtfertigt ist.
* **GOAP / HTN-Planung** (Ziel → Plan aus Aktionen mit Vorbedingungen) — prüfe, ob unsere acht Zustände dafür
  reichen oder ob Planung zu teuer ist.
* **Blackboard / Gedächtnis** (was ein Bot über die Welt weiß) — wir haben bereits ein Gedächtnis in
  `bottaktik`; prüfe, ob es reicht.
* **Persönlichkeiten und Agenden aus Handelsspielen und 4X-Strategie** (z. B. „Agenda“-Systeme, die Ziele und
  Abneigungen fest an eine Figur binden) — genau das Muster für A-3.
* **Einfache Markov-/Zustands-Modelle mit Zufall** — prüfe, ob ein Zustandsautomat mit Gewichten schon genügt.

Je Modell: **Was ist die Idee, was kostet es, was passt zu unseren Grenzen (stdlib, deterministisch,
prüfbar, kein Fenster), was übernehmen wir, was nicht — und warum.** Am Ende **eine** Empfehlung mit
Begründung, welche Bauform wir bauen, und der Hinweis, welche Teile du aus der Literatur übernimmst
(Nennung des Musters genügt, keine Kopie fremden Codes).

---

## 4. Formregeln für dein Papier

* Deutsch. Tabellen. Keine Emoji. Abschnitte in der Reihenfolge aus Teil 1 bis 7.
* Jede Regel mit Kennung: `V-xx` (Verhalten), `A-xx` (Attribut), `S-xx` (Auswahl/Umschalten), `W-xx` (Wache),
  `T-xx` (Spielertext).
* Jede Zahl mit Urteil **BELEGT** (Quelle im Projekt) / **VORSCHLAG** (deine Zahl, mit Begründung) /
  **UNBEKANNT** (muss Daniel entscheiden).
* **Höchstens acht offene Entscheidungen** am Ende, jede mit zwei Möglichkeiten und Empfehlung zuerst.
  Keine Frage, die du selbst beantworten kannst.
* Sage ausdrücklich, was du **nicht** wissen kannst (Repo-Stand, lokale Messwerte, Daniels Geschmack).

## 5. Was Hermes mit dem Papier tut

Hermes prüft jede Zahl gegen den echten Code, baut die Verhaltenspakete als eigenen Schnitt (geplant nach
S-8, gemeinsam mit Spionage und Kampfplanung), legt die acht Entscheidungen Daniel **gesammelt** vor und
fährt danach einen Spieltest-Verlauf, an dem sich das Spielgefühl messen lässt. Was nicht belegbar ist, wird
nicht gebaut, sondern als offener Punkt geführt.
