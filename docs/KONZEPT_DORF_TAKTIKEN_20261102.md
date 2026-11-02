# KONZEPT K-1 — Dorf-Taktiken als Regler für den Volksbonus (02.11.2026)

Vorschlag von Daniel, hier zu Ende gedacht und auf Machbarkeit geprüft. Stand: Entwurf, nichts
davon ist gebaut.

## 1. Der Sinn hinter dem Vorschlag (so, wie ich ihn verstehe)

Ein Volk ist **dauerhaft geprägt**: es hat eine Stärke (+5 % auf etwas) und eine Schwäche (−5 % auf
etwas anderes). Diese Prägung ist nicht verhandelbar — sie gehört zum Volk.

**Wie stark diese Prägung im Spiel spürbar wird, entscheidet aber die Taktik der Dörfer.**
Jedes Dorf gibt genau **einen Punkt Wirkung** (1 %). Diesen Punkt kann das Dorf entweder

- in die **Stärke** des Volkes legen (Offensive: der Bonus wächst, bis **+10 %**), oder
- in den **Ausgleich der Schwäche** (Solide: der Malus schrumpft, bis **0 %**).

Damit gilt: mehr Dörfer = mehr Wirkung, aber **nie mehr als das Doppelte**. Und jede Taktikwahl ist
eine echte Entscheidung statt einer Geschmacksfrage. Der Bot wirkt dadurch mit jedem neuen Dorf
vielseitiger und schwerer vorherzusagen — ohne stärker zu werden, als das Volk es erlaubt.

## 2. Die Buchführung (knapp, prüfbar)

| Größe | Regel |
|---|---|
| Volksbonus | `plus_prozent` (z. B. +5) und `minus_prozent` (z. B. −5) je Fraktion, fest in Daten |
| Punkte | **1 Punkt je Dorf**, das eine **passende** Taktik aktiv hat; Deckel **5** Punkte |
| Kanal | jeder Punkt geht entweder nach `staerken` oder `ausgleichen` — **nie beides** |
| Wirkung | `plus_effektiv = plus_prozent + staerken` (höchstens +10) <br> `minus_effektiv = minus_prozent + ausgleich` (höchstens 0) |
| Untergrenze | `minus_effektiv` bleibt negativ oder 0, wird **nie positiv** (kein Gratis-Bonus) |

Rechenbeispiel (menschlich: Holz +5 %, Stein −5 %, 6 Dörfer, 3 passend):

- 2 Dörfer auf `staerken`, 1 Dorf auf `ausgleichen` → Holz **+7 %**, Stein **−4 %**.
- alle 5 Punkte auf `staerken` → Holz **+10 %**, Stein **−5 %**.
- alle 5 Punkte auf `ausgleichen` → Holz **+5 %**, Stein **0 %**.

## 3. Warum das balanced ist (Invarianten, die eine Wache prüfen kann)

1. **Deckel:** `plus_effektiv` liegt immer zwischen `plus_prozent` und `plus_prozent + 5`;
   `minus_effektiv` immer zwischen `minus_prozent` und 0. Kein Wert kann entgleisen.
2. **Kein Doppelzählen:** die Summe der verteilten Punkte ist genau die Zahl der Dörfer mit
   passender Taktik, gedeckelt auf 5 — ein Dorf gibt einen Punkt, nicht zwei.
3. **Rückwärtskompatibel:** 0 passende Dörfer ergeben exakt den heutigen Zustand.
4. **Determinismus:** gleiche Dörfer und gleiche Taktiken ergeben immer denselben Bonus (kein Zufall).
5. **Symmetrie der Wahl:** ein Punkt in `ausgleichen` ist genauso viel wert wie einer in `staerken`
   (1 Prozentpunkt) — es gibt keine mathematisch bessere Wahl, nur eine passendere zum Spielplan.

## 4. Die Taktik-Pakete (Datentabelle, noch nicht beschlossen)

Welche Taktik welchen Kanal bedient, hängt am Volk — deshalb eine Tabelle je Fraktion. Vorschlag;
jede Zeile ist eine Zeile in `data/bot_boni.json`, Daniel kann sie ohne Code ändern:

| Fraktion | Volk plus / minus | `staerken` (passende Taktik) | `ausgleichen` | neutral |
|---|---|---|---|---|
| menschlich | Holz +5 / Stein −5 | SAMMELN, WACHSEN, RAUBERN | SICHERN, FLIEHEN | MARSCHIEREN, SUCHEN, RÄCHEN |
| zwergisch | Stein +5 / Holz −5 | SAMMELN, SICHERN, WACHSEN | MARSCHIEREN, FLIEHEN | RAUBERN, SUCHEN, RÄCHEN |
| elfisch | Reise +5 / PA −5 | MARSCHIEREN, SUCHEN | SICHERN, FLIEHEN | SAMMELN, WACHSEN, RAUBERN |
| monster | AT +5 / Handel −5 | RAUBERN, RÄCHEN | SAMMELN, SICHERN | WACHSEN, MARSCHIEREN, SUCHEN |

Der Gedanke dahinter: wer in einem Dorf auf Angriff setzt, verstärkt die Stärke seines Volkes; wer
auf Verteidigung oder Rückzug setzt, glättet die Schwäche. Ein Dorf, das weder noch betreibt, gibt
keinen Punkt — Ruhe ist keine Taktik.

## 5. Was zuerst gebaut werden muss (Befund am Code, gemessen 02.11.2026)

**Die Bots haben heute keine Dörfer.** `BotPlayer` (main.py) führt `settlements: List[str]`, aber die
fünf Bots werden ohne Siedlungen angelegt (`BotPlayer("Haug", "menschlich", …)`); im Code steht
ausdrücklich: „ein Bot hat derzeit eine abstrakte Hauptsiedlung. Nur als Zwischenstufe; später je
Bot-Siedlung in eine eigene Ortsstruktur“. Wirtschaftlich ist ein Bot ein Vorrats-Dict
(`bot.vorraete`), keine Siedlung mit Feldern und Erträgen. `bottaktik.offene_luecken()` nennt selbst
den VORSCHLAG "1–3 Dörfer je Bot, deterministisch per Seed".

Reihenfolge, die daraus folgt:

| Stufe | Inhalt | Aufwand (geschätzt) |
|---|---|---|
| A | **Volksboni verdrahten** (die 13 Wirkungen, ohne Dorf-Ebene) — heute wirken sie nicht | 1 Takt |
| B | **Echte Bot-Dörfer**: je Dorf eigene Vorräte, Wall, Erträge, Taktik-Slot; alte Spielstände laden mit Vorgabewerten | 2 Takte |
| C | **Dorf-Taktiken und Kopplung** nach diesem Konzept (Punkte, Kanäle, Wechsel mit Sperrzeit) | 1–2 Takte |
| D | **Balance-Messung**: Simulation mehrerer Verteilungen, Gate gegen Übermacht | 1 Takt |

Stufe A ist unabhängig und kann sofort laufen; B ist die Voraussetzung für alles Weitere.

## 6. Wie geprüft wird

- **Regelwachen:** Deckel, kein Doppelzählen, Rückwärtskompatibilität, Determinismus (Abschnitt 3),
  je eine Bedingung, dazu die Grenzfälle −1 / 0 / Soll / +1.
- **Anzeige = Kern:** eine Funktion `volksbonus_effektiv(bot, doerfer)` liefert die Zahlen; die
  Anzeige und jede Wirkstelle lesen sie (F-04-Muster).
- **Messung, kein Gefühl:** `tools/balancing_messung.py` fährt N Partien je Verteilung
  (0 / 2 / 5 passende Dörfer, `staerken` gegen `ausgleichen`) und berichtet Bot-Stärke und
  Spieler-Siegquote. Gate: die 10-Prozent-Grenze ist hart, und keine Verteilung darf die Bots
  stärker machen als der Deckel erlaubt.

## 7. Offene Entscheidungen (gehören Daniel)

| Frage | Möglichkeit A | Möglichkeit B | Empfehlung |
|---|---|---|---|
| Ab wann zählt ein Dorf? | ab dem 1. Dorf (Gründung zählt mit) | ab dem 2. Dorf (Gründung ist geschenkt) | **B** — sonst hat jeder sofort +6 % ohne Entscheidung |
| Deckel bei 6 Siedlungen | 5 Punkte | 6 Punkte | **5**, wie von Daniel genannt; die Gründung bleibt ohne Punkt |
| Wer wechselt Taktiken? | nur der Spieler entscheidet seine Dörfer, Bots nach fester Regel | auch Bots dürfen wechseln (mit Sperrzeit) | **B**, aber mit 48-Stunden-Sperre je Dorf — sonst ist nichts ablesbar |
| Dritter Kanal | nur Stärke und Ausgleich | zusätzlich "Beute" o. Ä. als dritter Kanal | **A** zum Start; ein dritter Kanal bricht die einfache Summenregel |
| Darf ein Punkt verfallen? | nein, immer zuweisen | ja, wenn keine passende Taktik läuft | **A** — Ruhe heißt neutral, nicht "Punkt weg" |

## 8. Erweiterung (Daniel, 02.11.2026, 16:20): Völkerwahl am Start und fremde Boni

### 8.1 Das Hauptdorf traegt das Volk, nicht die Punkte

- Der **Spieler waehlt zu Spielbeginn sein Volk**. Das ist der Start des Spiels, nicht eine
  Nebeneinstellung: die Wahl legt +5 % / -5 % fuer die ganze Partie fest.
- Das **Hauptdorf** (die erste Siedlung) traegt genau diese Basiswerte und gibt **keinen Punkt**.
- **Jedes weitere Dorf gibt einen Punkt** (also ab dem 2. Dorf). Damit ist die in Abschnitt 7
  gestellte Frage beantwortet: die Gruendung ist geschenkt.
- Die **Bots bekommen die uebrigen Voelker** zugewiesen - nicht mehr fest im Code.

### 8.2 Dritter Kanal: fremde Boni bis 5 %

Ein Dorf kann seinen Punkt in **drei** Richtungen legen:

| Kanal | Wirkung | Deckel |
|---|---|---|
| eigene Staerke | der Plus-Wert des eigenen Volkes waechst | +5 Punkte (also hoechstens +10 %) |
| eigener Ausgleich | der Minus-Wert des eigenen Volkes schrumpft Richtung 0 | +5 Punkte (hoechstens 0 %) |
| **fremd** | das Dorf holt sich einen Bonus eines ANDEREN Volkes | **hoechstens +5 %**, nur EIN fremdes Volk |

**Wichtig fuer die Balance:** die Punkte sind EIN Budget ueber alle drei Kanaele. Ein Volk kommt
damit hoechstens auf **+10 Prozentpunkte Wirkung** (5 eigene plus 5 dazu, gleich in welcher
Mischung) - nie auf 15. Fremde Boni stapeln sich nicht: zwei Doerfer beim selben fremden Volk
ergeben zusammen hoechstens dessen 5 %.

### 8.3 Was das am Code aendert (gemessen 02.11.2026)

- `botkern.BOT_FRAKTIONEN` ist heute eine **feste** Tabelle mit **vier** Fraktionen fuer **fuenf**
  Bots (menschlich doppelt: Haug und Brynhild). "Spieler waehlt, Bots bekommen den Rest" braucht
  deshalb: eine Voelkerliste, eine Zuordnung **im Spielstand** statt als Konstante, und eine
  Volkswahl im Startablauf (Fenster + Spielstand-Feld, alte Spielstaende laden mit Vorgabewert).
- Die Boni gelten heute **nur fuer Bots**. Mit der Voelkerwahl bekommt auch der **Spieler** seine
  +5 / -5 - das braucht Kern UND Anzeige aus derselben Funktion (F-04-Muster).
- Folge fuer den Plan: zwischen Stufe A (Boni verdrahten) und Stufe B (Bot-Doerfer) schiebt sich
  eine eigene Stufe **A2 Voelkerwahl** (Voelkerliste, Zuordnung im Spielstand, Startfenster).

### 8.4 Neue offene Fragen

| Frage | Moeglichkeit A | Moeglichkeit B | Empfehlung |
|---|---|---|---|
| Wie viele Voelker? | **6** - Spieler und fuenf Bots, jeder ein eigenes Volk, keine Doppelung | **5** - ein Volk kommt bei den Bots doppelt vor (wie heute menschlich) | **A**: sechs Voelker, damit die Wahl exklusiv ist |
| Gilt die Dorf-Punkt-Mechanik auch fuer den Spieler? | ja, gleiche Regel fuer alle | nur Bots | **A** - sonst hat der Spieler eine Sonderregel, die niemand versteht |
| Fremder Bonus: frei oder gebunden? | frei waehlbar (der Spieler sucht sich, was er braucht) | gebunden an ein Nachbarvolk (mehr Rollenspiel, weniger Kontrolle) | **A** zum Start; gebunden waere ein eigener Schritt |

### 8.5 Antworten Daniels (02.11.2026, rund 17:00) - diese Punkte sind entschieden

1. **Sechs Voelker.** Spieler und fuenf Bots, jeder ein eigenes Volk, keine Doppelung.
2. **Gleiche Regel fuer alle, aber Verhalten wirkt beim Spieler nur ueber die WERTE.** Beim Spieler
   veraendert die Taktik ausschliesslich die Boni; er handelt selbst. Beim Bot bedeutet eine Taktik
   auch, dass sich das Dorf entsprechend VERHAELT (aggressiv greift frueher an, Forschung/Verteidigung
   spaeter oder gar nicht).
3. **Fremder Bonus frei waehlbar** - das Dorf holt sich, was es braucht. Bei Bots werden Verhalten und
   Taktik aus ihrer Lage und ihren Werten gewaehlt.
4. **Reihenfolge:** erst Stufe B (echte Bot-Doerfer), dann alles zusammen.

Damit bleiben offen: die konkreten Zahlen der Taktik-Pakete (Abschnitt 4) und die Frage, wie stark
ein aggressives Verhalten den Angriffsrhythmus verschiebt - beides wird gemessen, nicht geschaetzt.
