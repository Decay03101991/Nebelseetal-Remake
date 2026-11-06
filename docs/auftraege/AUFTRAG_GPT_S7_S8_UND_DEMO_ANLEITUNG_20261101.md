# AUFTRAG 7 an das starke Chat-Modell — S-7 Bots sichtbar, S-8 Bilanz, Demo-Anleitung

**Stand:** 01.11.2026, 16:55. **Auftraggeber:** Daniel Kössl, über Hermes (Weltenfresser).
**Arbeitsstand des Spiels:** Commit **`8d100a2`** (Register 88) plus die an diesem Tag laufenden
Schnitte S-2c und S-5. Das öffentliche Repo steht auf **`954097aa`** und ist **nicht** der
Arbeitsstand — verlasse dich auf die hier gemessenen Angaben, nicht auf GitHub.

**Gegenstand:** die letzten beiden groben Schnitte vor der Demo — **S-7** (die fünf Bots werden im
laufenden Spiel erlebbar, ohne jeden Angriff und ohne jede Markierung auf der Weltkarte) und
**S-8** (die Bilanz aus Mana, Reisekosten und Zeit, damit die Demo nicht an einer falsch
geeichten Wirtschaft scheitert) — **plus** der geführte Start für die ersten zehn Minuten.

**Warum diese drei zusammen:** Sie sind der Rest zwischen dem heutigen Stand und Daniels Ziel
(„sobald die die aktuell groben offenen punkte im spiel bearbeitet sind möchte ich eine offiziele
spielbare demo exe meines spiels auf github hochladen“, 01.11.2026). S-2c, S-3, S-4, S-5 und S-6
haben entweder ein Papier oder sind in Arbeit; **für S-7 und S-8 liegt bisher kein Entwurf vor**,
und die Demo braucht einen Einstieg, den ein fremder Spieler ohne Erklärung versteht.

---

## 0. Rolle und Grenze

Du bist **Entwurfs-Autor**. Du lieferst Regeln, Zahlen, Tabellen und wörtliche Spielertexte, aber du
änderst **keinen** Code, startest **keine** Builds und machst **keine** Commits. Was du als
**BELEGT** kennzeichnest, muss eine Quelle im Projekt haben (Datei und Zeile oder Zitat aus dem
Handbuch 2009); alles andere ist **VORSCHLAG** oder **UNBEKANNT**. Keine Zahl ohne Quelle, keine
Regel ohne Prüfmöglichkeit.

## 0a. Wer dein Papier umsetzt — und was das für dein Papier bedeutet

**Umsetzendes Modell: `deepseek-v4-flash`** (klein, schnell, arbeitet in einem Zug).

* **Prüfbare Regeln ohne Auslegung.** Eine Regel ist ein Satz, den ein Prüfskript nachrechnen kann:
  Bedingung, Wirkung, Grenzfall, Grenze.
* **Nur Standardbibliothek.** Kein neues Paket, keine Datenbank, keine Migration alter Spielstände.
  Zufall ausschließlich aus `random.Random(seed)` mit ausdrücklich genanntem Seed.
* **Jeder Teil in EINEM Arbeitsgang.** Ist ein Teil zu groß, teile ihn selbst und sage die Reihenfolge.
* **Spielertexte wörtlich, deutsch, mit Platzhaltern** in `{geschweiften Klammern}`. Keine Emoji.
* **Jede Regel ohne Fenster prüfbar.** Zu jeder Regel gehört die Wache: was wird gesetzt, was wird
  gelesen, was darf **nicht** passieren.
* Knapp. Tabellen statt Fließtext, keine Wiederholung dieses Auftrags.

---

## 1. Was du über das Spiel wissen musst (gemessen, nicht behauptet)

| Gegenstand | Stand | Belegstelle |
|---|---|---|
| Bauart | Python 3.14 + tkinter, JSON-Spielstand, offline, Einzelspieler gegen Bots | `src/main.py` |
| Ziel | **kein Sieg mehr** — `punkte.spielausgang` liefert nur `niederlage`/`weiter`; Bewertung über Auszeichnungen (Feldherr, Forscher, Händler, Gesamtherrscher) | `src/punkte.py`, Register E5 |
| Kernkreis | gründen → produzieren → forschen → ausrüsten → ausbilden → bewegen → kämpfen → punkten | `docs/PLAN_Einzelspieler.md` |
| Dörfer | **höchstens 6 je Spieler** (global über alle Weltkarten) | `SIEDLUNGEN_MAXIMUM = 6`, `src/main.py` |
| Wirtschaft | **jedes Dorf führt sein eigenes Lager** (`Settlement.vorraete`, `.waren`, `.einheiten`); die Reichsanzeige ist nur eine Summe, keine zweite Kasse | `src/main.py`, `ortsbestand_text` |
| Gebäude | 20 Gebäude mit Wirkung, Voraussetzung und `max_je_siedlung` in `data/buildings.json` | `data/buildings.json` |
| Forschung | 21 Forschungen, je Dorf eigene Bibliothek, Verbundstand ist Schnitt S-3 | `data/research.json`, `src/forschungspfad.py` |
| Waren und Ausrüstung | 17 Waren in drei Werkstätten (Schmiede, Bogenbauer, Nähstube); Einheiten brauchen Ausrüstung, nicht nur Gold | `data/items.json`, `src/ausruestung.py`, `src/werkstatt.py` |
| Einheiten | 28 Einheiten mit belegten Werten (LE/AT/PA/SK, Kriegspunkte, Kosten in Siedlern und Rohstoffen) | `data/units.json` |
| Kampf | Vorrunde über **SK** gegen Wallschwellen, dann Schlacht; Beute gestaffelt und ladungsgedeckelt; die Wallprüfung warnt, sie lehnt nicht mehr ab | `src/kampf.py`, `src/kampfbericht.py`, `src/auftraege.py` |
| Bewegung | jede Einheit reist als **Auftrag** (Hinweg und Rückweg), Reisezeit aus Entfernung und langsamster Einheit | `src/auftraege.py` |
| Portal | **20 Weltkarten, je 400 Felder**; sechs belegte Namen: Armageddon, Ragnaroeck, Utgard, Midgard, Valhalla, Limbus. Startwelt ist **Midgard** (`d04` = Nummer 4). Bespielbar sind zuerst Midgard und Valhalla. Der Weltensprung kostet Mana und ist gesperrt, solange irgendetwas unterwegs ist (auch Handel) | `src/portalraum.py`, `data/welten.json`, `src/main.py`, Schnitt S-2b |
| Uhr | **Spieluhr** (`state.spielsekunden`), nicht Rechnerzeit; Bot-Zug stundenweise (`BOT_TAKT_SEKUNDEN = 3600`) | `src/main.py:774` |
| Bots heute | **5 Gegner**: Haug und Brynhild (menschlich), Grom (zwergisch), Silra (elfisch), Krank (monster) | `src/botkern.py`, `src/bottaktik.py` |
| Teststand | voller Sammellauf **114 Prüfdateien, 112 grün, 0 rot, 2 ausgesetzt, 4.132 Prüfungen, 776 s** (01.11.2026, 12:17) | `docs/audits/sammellauf_20261101_1205.log` |
| Register | 88 Punkte geprüfte Originalregeln | `docs/PRUEFREGEL_ORIGINAL.md` |

### 1.1 Der Ist-Stand der Bots (wichtig für dich)

* **`src/botkern.py` ist angeschlossen** (`main.py`, Bot-Zug): Startvorräte, Wagenpark,
  Handelsneigung, Temperament (`TEMPERAMENT_SPANNE = 0.10`), `handelspreis(referenzpreis,
  temperament)`, `bot_punkte`, `bots_tick`.
* **`src/bottaktik.py` ist NICHT angeschlossen.** Es ist ein Zustandsautomat mit **acht Zuständen**
  (SAMMELN, WACHSEN, SICHERN, SUCHEN, MARSCHIEREN, RAUBERN, FLEHEN, RÄCHEN) und fünf Taktiken plus
  einer neutralen, mit Schwellenwerten, Gedächtnis und einer Ankündigung vor einem Angriff.
  Schnittstellen: `taktik_von(bot)`, `tick(bot, welt, jetzt, rng)` → Entscheidung,
  `wirkung_anwenden(bot, entscheidung, jetzt)` → **neuer** Bot (Eingabe unverändert),
  `anzeige(bot)`, `pruefe_taktik()`, `offene_luecken()`. **Der Anschluss ist der Schnitt S-7.**
* **Was es heute nicht gibt:** Bot-Koordinaten im Spielstand, mehrere Dörfer je Bot (geplant: bis zu
  fünf weitere), irgendeine Spur des Bots im Spieler-Postfach, Rückmeldung an den Spieler, wenn ein
  Bot etwas tut.

### 1.2 Was S-7 und S-8 sind (und was sie NICHT sind)

| Schnitt | Bedeutung |
|---|---|
| **S-7** | Die Bots werden **erlebbar**: sie gründen, wirtschaften und bewegen sich nach `bottaktik`, und der Spieler **merkt** es — aber **kein Angriff**, keine Eroberung, kein Kampf gegen Bots in dieser Stufe. |
| **S-8** | Die **Bilanz**: Weltensprung-Preis, Mana-Haushalt, Reisekosten und Zeit im Verhältnis zu dem, was ein Dorf erwirtschaftet — gerechnet, nicht geschätzt. Danach ist die Demo freigabefähig. |

---

## 2. Daniels bindende Vorgaben — du darfst sie nicht ändern

| Nr | Vorgabe | Folge für dein Papier |
|---|---|---|
| D-1 | **Die Weltkarten zeigen ausschließlich Gelände.** Keine Orte, Dörfer, Gegnerrahmen, Bot-Nummern, Symbole, Flaggen oder dauerhaften Markierungen. (Daniel, 01.11.2026; hebt alle älteren Vorgaben zur Bot-Anzeige auf der Karte auf.) | S-7 darf **keine** Kartenfunktion erfinden. Ein Bot wird über **Berichte und Meldungen** erlebbar, nicht über einen Punkt auf der Karte. |
| D-2 | **Kein Angriff in S-7.** | Jedes Bot-Verhalten, das einen Marsch gegen einen Spieler oder einen anderen Bot auslöst, ist bis zur Freigabe gesperrt — und muss im Papier ausdrücklich als gesperrt benannt sein. |
| D-3 | **Bots gründen „ganz normal wie der Spieler“** bis zu fünf weitere Dörfer, also höchstens sechs. | Kein Bot-Sonderrecht, keine kostenlose Gründung, keine Ausnahme von der Dorfgrenze. |
| D-4 | **Meldungen nur in vorhandenen Kanälen** (Postfach/Nachrichten, Diplomatie, Ruhmeshalle). | Kein neues Fenster, keine neue Kartenfunktion, kein Popup. |
| D-5 | **Keine Zahl ohne Quelle.** Wo eine Messung fehlt, steht `UNBEKANNT` und Hermes misst. | Rechne nichts schön; nenne die fehlende Messung beim Namen. |
| D-6 | **Die Demo ist eine eigene öffentliche Spielerfassung** mit frischem Spielstart, nicht ein Teststand. | Deine Anleitung muss ab dem **ersten** Spielmoment funktionieren, nicht ab einem vorbereiteten Savegame. |

---

## 3. Was dein Papier liefern soll — sieben Teile

### Teil 1 — S-7: Wie ein Bot erlebbar wird, ohne auf der Karte zu stehen

Liefere **8 bis 12 erkennbare Ereignisse** (`E-01`…`E-12`), je mit:

| Feld | Inhalt |
|---|---|
| Auslöser | welche echte Bot-Handlung das Ereignis erzeugt (Gründung, Ausbildung, Handel, Bewegung, Forschung) |
| Bedingung | wann der Spieler es **erfahren darf** (Kenntnis, Entfernung, Aufklärung) und wann ausdrücklich **nicht** |
| Kanal | Postfach / Nachrichtenliste / Diplomatie-Ansicht / Ruhmeshalle / Dorfzentrum — nur vorhandene Kanäle |
| Text | wörtlicher deutscher Spielertext mit Platzhaltern |
| Häufigkeit | höchstens wie oft je Spieltag, damit das Postfach nicht zumüllt |
| Gegenprobe | was der Text **nicht** verrät (Position, Truppenstärke, Vorräte) |

**Zusätzlich zwingend:**

* **Ein Kenntnis-Modell in Worten:** Was weiß der Spieler über einen Bot, bevor er ihm begegnet?
  Reicht ein Name? Ein Name und eine Fraktion? Ein Dorfname? Achte darauf, dass das Spiel **nichts
  Allwissendes** verrät — die Bots kennen den Spieler ebenfalls nicht vollständig.
* **Ein Tagesrhythmus:** Wie oft darf der Spieler in den ersten drei Spieltagen etwas von den Bots
  hören, damit es lebendig wirkt und nicht nervt? Als Tabelle „Spieltag × erwartete Meldungen“.
* **Was ausdrücklich NICHT passiert:** Angriff, Eroberung, Spionage, Kartenmarker, Bot-Besuch mit
  fremder Ansicht, Bestechung.

### Teil 2 — S-7: Der Bot in der Diplomatie und in der Ruhmeshalle

Der Spieler muss die fünf Bots **unterscheiden** können, ohne dass sie auf der Karte stehen:

* Welche **feste** Angabe steht zu jedem Bot (Name, Fraktion, ein bis zwei Sätze Charakter)?
  Es gibt bereits Temperament und Taktik in `botkern`/`bottaktik` — welche davon werden sichtbar,
  welche bleiben verborgen? Begründe die Grenze.
* Welche **veränderliche** Angabe steht dort (Punkte, Dörfer, Stimmung), und woraus wird sie
  berechnet? Keine zweite Punkteformel: `botkern.bot_punkte` und `punkte.punktestand` sind die
  vorhandenen Rechenstellen.
* Wörtliche Texte für die Diplomatie-Ansicht (`T-xx`), höchstens zehn Zeilen.

### Teil 3 — S-8: Die Bilanz aus Mana, Reisekosten und Zeit

Das ist der Teil, an dem die Demo scheitern kann. Liefere **eine Rechentafel**, keine Gefühlswerte:

1. **Mana-Haushalt:** Woher kommt Mana, wohin geht es? Nenne je Quelle und je Senke die vorhandene
   Funktion und Datei. Der Weltensprung steht im Code heute mit einem **belegten Festpreis von
   5.000 Mana**; Daniels Vorschlag ist **500 Mana plus „ein wenig Gold“**. Rechne beide Varianten
   gegen den tatsächlichen Mana-Zufluss und sage, welche tragbar ist — und was passiert, wenn der
   Zufluss in der Demo kleiner ist als im Altzustand.
2. **Reisekosten:** Was kostet ein Marsch, ein Transport, eine Handelskarawane heute? Nenne die
   Rechenstelle und die Größen, die eingehen (Entfernung, langsamste Einheit, Traglast, Karren).
   Rechne **ein** durchgerechnetes Beispiel je Fall mit erfundenen, klar gekennzeichneten
   Testzahlen — und nenne getrennt die Zahl, die Hermes dafür messen muss.
3. **Die Waage:** Ertrag eines Dorfes je Spieltag gegen die Kosten einer Reise und eines
   Weltensprungs. Als Tabelle für 1, 2 und 6 Dörfer. Ziel: der Spieler soll **nicht** in eine Lage
   kommen, in der er sich bewegen kann oder wirtschaften, aber nicht beides.
4. **Grenzfall:** Was passiert bei 0 Mana, bei genau dem Preis, bei einem Preis über dem Bestand?
   Je Grenzfall ein Satz mit erwarteter Ablehnung und wörtlichem Text.
5. **Kein Doppelpreis:** Wenn ein Weltensprung Mana **und** Gold kostet, welche der beiden Stellen
   bucht, und wo steht die andere Zahl nur zur Anzeige? Eine Buchungsstelle, sonst zählt das Spiel
   doppelt.

### Teil 4 — Der geführte Start: die ersten zehn Minuten der Demo

Es gibt bereits eine Karte „Dein nächster Schritt“ im Dorfzentrum (`main.naechster_schritt`,
`src/spielerhilfe.py` mit `startaufgabe_pflicht`). Entwirf daraus eine **geschlossene Kette** von
der ersten Sekunde bis zur ersten echten Eigenversorgung:

* **8 bis 12 Schritte** (`A-01`…`A-12`), je: Ziel in einem Satz, Bedingung „wann gilt der Schritt als
  erledigt“ (aus dem Spielstand ablesbar, nicht geschätzt), wörtlicher Text der Karte, wörtlicher
  Knopftext, und was passiert, wenn der Spieler den Schritt überspringt.
* **Belegte Kette nicht abkürzen:** Holzfäller → Bibliothek (ohne Forschung baubar) → Forschung
  „Baukunst“ → Goldmine/Farm/Kriegerakademie; Einheiten brauchen zusätzlich Ausrüstung aus der
  Werkstatt, nicht nur Gold. Wer diese Reihenfolge umstellt, sperrt den Spieler aus.
* **Der erste Tag muss ehrlich sein:** sage, wie lange ein echter Spieler bis zur ersten Einheit
  braucht, wenn er nichts falsch macht — und was in dieser Zeit passiert (Bots, Meldungen, Sperren).
* **Abbruchfreundlich:** der Spieler darf jederzeit etwas anderes tun; die Karte darf ihn nicht
  gängeln und nicht mit „Pflicht“ drohen.

### Teil 5 — Integration in die bestehenden Module (keine zweite Wahrheit)

| Frage | Antwort erwarten wir |
|---|---|
| Was gehört nach `src/bottaktik.py`? | Anschluss des vorhandenen Automaten, keine zweite Entscheidungsstelle |
| Was gehört nach `src/botkern.py`? | nur Wirtschaftswerte, keine Verhaltenslogik |
| Wo entstehen die Meldungen? | die vorhandene Nachrichtenliste (`state.messages`, `nachrichten_farbe`) — nicht ein zweiter Postfachspeicher |
| Was braucht der Spielstand (neue Felder)? | Name, Typ, Vorgabewert, Verhalten bei alten Ständen (Lesedefault, keine Migration) |
| Was braucht die Anzeige (Portal, Dorfzentrum, Diplomatie, Ruhmeshalle)? | je Ort ein Satz, was dort steht — und was dort ausdrücklich **nicht** steht |
| Was darf nicht entstehen? | eine zweite Punkteformel, eine zweite Kampfformel, ein zweiter Mana-Zähler, eine zweite Kartenanzeige |

### Teil 6 — Prüfplan

Eine Wache je Regel, ohne Fenster, auf reinen Spielstands- und Datenkopien. Mindestens:

* Die Weltkarte enthält nach S-7 **kein** einziges Bot-Element (Gelände und Auswahl, sonst nichts).
* Ein Bot-Ereignis erzeugt **genau eine** Meldung, auch wenn der Bot-Zug zweimal im selben Tick läuft.
* Ein gesperrtes Verhalten (Angriff) kann **nicht** ausgelöst werden, auch nicht über eine
  Sonderregel oder einen Taktikwechsel.
* Der Weltensprung bucht **einmal** und nur bei erfüllten Voraussetzungen; bei zu wenig Mana bleibt
  jeder Bestand bytegleich.
* Alte Spielstände ohne die neuen Felder laden und speichern ohne Migration.
* Der geführte Start erreicht die erste Eigenversorgung **ohne** gesetzte Werte (kein Fixture-Cheat).

### Teil 7 — Recherche: gibt es das schon?

**Eigener Auftragsteil, ausdrücklich erwünscht.** Prüfe, wie andere Spiele das lösen, und was davon
zu unseren Grenzen passt (nur Standardbibliothek, deterministisch, prüfbar, kein Fenster):

* **Gegner erlebbar ohne Sichtkontakt** — Nachrichtensysteme, „Ereigniskarten“, Bot-Botschaften in
  Aufbauspielen und 4X-Runden (nur als Muster, keine Kopie).
* **Mana-/Ressourcen-Senken und -Quellen ausbalancieren** — bekannte Faustregeln für „Senke
  höchstens X % des Zuflusses je Spieltag“.
* **Onboarding/Tutorial-Muster** — geführte erste Minuten ohne Zwang („goal-driven onboarding“,
  Schrittketten, Hinweiskarten).
* **Schwarzes Brett / Bekanntmachungen** als billige Form von „Welt lebt“ ohne Simulation.

Je Modell: Idee, Kosten, Passung zu unseren Grenzen, was wir übernehmen, was nicht — und warum.
Am Ende **eine** Empfehlung mit Begründung.

---

## 4. Formregeln für dein Papier

* Deutsch. Tabellen. Keine Emoji. Abschnitte in der Reihenfolge Teil 1 bis 7.
* Jede Regel mit Kennung: `E-xx` (Ereignis), `T-xx` (Spielertext), `A-xx` (Anleitungsschritt),
  `B-xx` (Bilanzregel), `W-xx` (Wache).
* Jede Zahl mit Urteil **BELEGT** (Quelle im Projekt) / **VORSCHLAG** (deine Zahl, mit Begründung) /
  **UNBEKANNT** (muss Hermes messen oder Daniel entscheiden).
* **Höchstens acht offene Entscheidungen** am Ende, jede mit zwei Möglichkeiten und Empfehlung
  zuerst. Keine Frage, die du selbst beantworten kannst.
* Sage ausdrücklich, was du **nicht** wissen kannst (lokaler Code, Messwerte, Daniels Geschmack).

## 5. Was Hermes mit dem Papier tut

Hermes prüft jede Zahl gegen den echten Code und den nächsten Sammellauf, baut S-7 als Anschluss des
vorhandenen `bottaktik`-Automaten (ohne Angriff), rechnet die S-8-Bilanz am gemessenen Ertrag nach
und legt die offenen Entscheidungen Daniel **gesammelt** vor. Was nicht belegbar ist, wird nicht
gebaut, sondern als offener Punkt geführt. Danach folgt die Demo-Freigabeprüfung (frischer
Spielstart, Speichern und Laden, voller Sammellauf grün, EXE-Start belegt, Release-Notizen).
