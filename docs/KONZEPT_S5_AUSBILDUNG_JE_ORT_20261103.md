# S-5 Ausbildung je Ort — Konzept (03.11.2026, Entwurf vor dem Bau)

**Vorgabe:** Daniel, Entscheidung 4 der Runde 12:20, woertlich: „S-5 Ausbildung je Ort
(Warteschlange statt Kauf; Armee zieht in die Doerfer und isst dort)“.

**Stand:** Entwurf. Gebaut ist noch nichts; dieser Text ist die Messlage, auf der der Schnitt steht.

## 1. Ist-Stand, am Code gemessen

| Gegenstand | Befund | Beleg |
|---|---|---|
| Kern-Warteschlange | `spieloekonomie.ausbildung_start`, `ausbildung_uebersicht`, `ausbildung_grenzen`, `ausbildung_abbrechen` gibt es bereits | `src/spieloekonomie.py` |
| Ort traegt die Auftraege | `Settlement.ausbildung` ist eine Liste je Ort; `bot_dorf_als_ort` reicht sie schon durch | `src/main.py` Zeile 249 und 757 |
| Spielerweg | `spielschicht.ausbilden(zustand, einheit)` nimmt die Staette aus `gebaeude_wirkung.ausbildungsstaette(...)` — also aus dem GEBAEUDE des Ortes | `src/spielschicht.py` Zeile 444 |
| Bot-Weg heute | Der Bot KAUFT: `GameState.bot_armee_aufstellen` bucht Kosten und stellt die Einheit direkt in `bot.army`; die Warteschlange des Ortes bleibt leer | `src/main.py` |
| Armee je Dorf | `BotDorf.einheiten` existiert, ist aber **leer**; die Armee haengt an `BotPlayer.army` | `src/main.py` Zeile 245 |
| Essen | `bot_futter_buchen` bucht NUR im Hauptdorf; `bot_dorf_tick` bucht Garnison-Nahrung je Dorf nur fuer `dorf.einheiten` | `src/main.py` |

**Der Code sagt selbst, was zu tun ist** (`bot_dorf_tick`-Docstring): „sobald S-5 Einheiten je Ort
ausbildet, muss die Armee dort hineinwandern (sonst isst sie zweimal)“.

## 2. Der Schnitt in dieser Reihenfolge

**S-5b zuerst — die Armee gehoert ins Dorf.** `BotDorf.einheiten` wird der fuehrende Speicher (wie
B-3 es fuer `vorraete` gemacht hat); `BotPlayer.army` wird die **Summe** der Doerfer, gelesen ueber
eine Eigenschaft, geschrieben ueber EINE Funktion (`bot_armee_buchen`). Grund fuer die Reihenfolge:
steht die Armee im Dorf, bevor die Ausbildung ueber den Kern laeuft, isst sie genau einmal.

**S-5a — Warteschlange statt Kauf.** Der Bot startet die Ausbildung ueber `spieloekonomie.
ausbildung_start` aus dem Lager des Dorfes mit dem Einheiten-Gebaeude; `ort_tick` bucht das Ende
(derselbe Weg wie beim Spieler, keine zweite Dauer, keine zweite Kostentabelle). Der Kaufpfad in
`botkern` faellt weg.

**S-5c — Essen je Dorf.** `bot_futter_buchen` isst dort, wo die Einheiten stehen; der Reichsbedarf
ist die Summe der Doerfer.

## 3. Wachen (zuerst schreiben)

1. **Kette ohne Cheats:** Dorf mit Kaserne, Gold/Nahrung/Ausruestung vorhanden -> Ausbildung starten
   -> Takt bis zum Ende -> Einheit steht in `dorf.einheiten` UND in `bot.armee`, Kosten genau einmal,
   zweiter Start legt nicht nach (zweiter Aufruf == 0).
2. **Eine Wahrheit:** die Dauer kommt aus dem Kern, nicht aus einer zweiten Zahl im Bot-Code; die
   Wache rechnet gegen die Spielerdauer.
3. **Ort statt Reich:** ein Dorf ohne Einheiten-Gebaeude bildet nichts aus, auch wenn das Reich Gold hat.
4. **Essen:** Dorf mit Einheiten isst, Dorf ohne nicht; die Summe ist der Reichsbedarf. Wache: keine
   Doppelzaehlung, nachdem die Armee umgezogen ist.

## 4. Fallstricke aus dem Skill, die hier greifen

- Ein Dataclass-Feld zur Eigenschaft umzubauen macht jeden Schreibzugriff auf die Kopie still
  wirkungslos (B-3-Lehre: `bot.vorraete[...] = x` buchte ins Nichts). Zwei `ast`-Wachen wie bei B-3.
- Neue Felder additiv mit Vorgabe, alte Spielstaende laden ohne Migration.
- Quellwachen ueber Docstrings abschneiden (`ast.unparse`), sonst faerbt der eigene Kommentar rot.
- Was der Kern liest, muss der Ort tragen (`importiert`, `verbrauchsjournal`, `ausbildung`).
- `.py` in `src/`/`tests/` ASCII; Anzeigenamen aus `data/` lesen, nie tippen.
