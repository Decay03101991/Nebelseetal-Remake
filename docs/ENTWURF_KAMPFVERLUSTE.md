# Entwurf: Kampfverluste (Vorgabe Daniel, 05.10.2026, 18:1x)

**Zweck:** Daniels Vorgabe festhalten, gegen das Handbuch stellen und den Ist-Zustand messen.
**Jede Zahl, die das Handbuch nicht nennt, ist VORSCHLAG.**

---

## 1. Daniels Vorgabe (wörtlich)

> „Bei der kampfsimulation musst du dich aufs offizielle regelbuch beziehen aber auch beachten,
> dass wir auf ein einzelspieler spiel setzen. Wichtig ist aber wenn z.b. ein Kampf verloren wird,
> dass ein prozentualer anteil an truppen vernichtet wird. Dabei vorallem Karren und
> Transporteinheiten wenn verloren wurde. Wenn man gewinnt, überleben natürlich auch die
> Transporteinheiten. Bei fast gleichen kämpfen wo nur knapp gewonnen wird müssen allerdings
> trotzdem große teile der Gesamtarmee schaden nehmen bzw sterben. Damit truppen produktion nicht
> zu deprimierend ist, dürfen aber nicht immer alle truppen vernichtet sein. Dafür muss ein
> logisches schlüssiges angepasstes system her."

---

## 2. Was das Handbuch dazu WÖRTLICH sagt (belegt)

| Regel | Stelle | Zitat |
|---|---|---|
| Der **Verlierer** verliert einen Teil seiner Karren und Belagerungswaffen | Handbuch S. 23, Z. 1334-1337 | „Der Verlierer verliert einen Teil seiner stationierten bzw. mitgeschickten Karren und Belagerungswaffen. Wie viele, hängt von der Dauer der Schlacht ab. Jede Einheit hat eine Fluchtchance von 40%. Jede Kampfsequenz, die die Schlacht dauert erhöht sich diese Chance um 5%." |
| **Unentschieden** kostet keine Karren | Handbuch S. 23, Z. 1338 | „Geht die Schlacht unentschieden aus, bleiben alle Karren und Belagerungswaffen erhalten." |
| Der **Sieger** behält seine Karren (nur der Verlierer verliert) | Handbuch S. 23, Z. 1331-1333 | „… gewinnt der Angreifer die Schlacht. Falls er Transportkarren in seiner Angriffstruppe mitführt, beginnen diese die Siedlung zu plündern." — die Verlustregel nennt **nur den Verlierer** |
| Einzelverluste: **Tod** unter 1 Lebensenergie, **Flucht** unter 5 | Handbuch S. 23, Z. 1319-1323 | „Sinkt die Lebensenergie einer Einheit unter 1, stirbt sie. Sinkt die Lebensenergie unter 5, wird anhand ihres Mut-Wertes entschieden, ob sie weiterhin im Kampf geschehen bleibt, oder Flieht. Geflohene Einheiten stehen … nach der Schlacht wieder zur Verfügung, Tote Einheiten werden nach der Schlacht gelöscht." |
| Schlachtende | Handbuch S. 23, Z. 1293-1295 + Z. 1276-1278 | Ende, sobald eine Armee keine Nahkampfeinheiten mehr hat, **oder 10 Sequenzen vorüber** sind; danach „unentschieden …, der Angreifer zieht sich in dem Fall ohne Beute zurück" |

**Wichtig für Daniels Punkt 3 („knapp gewonnen"):** Das Handbuch erzeugt große Verluste nicht über
einen Prozentsatz, sondern über die **Zweikampf-Simulation** — jede Nahkampfeinheit kämpft
nacheinander, jeder Treffer zehrt Lebensenergie, und der Sieger wird durch **Erschöpfung**
(Angriffs-/Abwehrfähigkeit −1 je Zweikampf) zunehmend schwächer (Z. 1324-1329). Ein knapper Sieg ist
damit strukturell ein **langer** Kampf mit vielen Zweikämpfen — also vielen Verlusten auf beiden
Seiten. Das ist genau die Größe, die Daniel verlangt, nur aus der Simulation statt aus einer Zahl.

---

## 3. Ist-Zustand im Code (gemessen, nicht geschätzt)

**Vorhanden und belegt umgesetzt — `src/kampf.py`:**

| Was | Stelle |
|---|---|
| Kampfsequenzen (max. 10), Fernkampf zuerst, dann Zweikämpfe | `fuehre_schlacht`, Z. 207 ff. |
| Zweikampf mit Mut, Trefferchance, Abwehr, Schadensspanne, Rüstung | `_zweikampf` / `_ein_schlag`, Z. 132-178 |
| **Tod unter LE 1, Flucht unter LE 5** (Mut entscheidet) | `_pruefe_tot_oder_flucht`, Z. 118 |
| **Gefallene je Einheitenname** (Geflohene zählen nicht) | `_verluste_zaehlen`, Z. 181-189 |
| **Karren-/Belagerungsverluste des Verlierers: 40 % + 5 % je Sequenz** | `_geraeteverluste`, Z. 192-202 |
| Beute nur mit **überlebenden** Karren | Z. 358-369 |
| Ergebnis enthält `verluste_angreifer`, `verluste_verteidiger`, `geflohen`, `sequenzen`, `ausgang` | Z. 335-351 |
| Auf den Spielstand anwenden (Verluste, Rückgut, Beute) | `src/kampfbericht.py`, `spieldaten_anwenden`, Z. 298 |

**Die Lücke ist die VERDRAHTUNG, nicht die Regel.** `src/spielschicht.py` nennt sie selbst:
`offene_luecken()["kampfverluste"]` = „Verluste einzelner Einheiten rechnet der (nicht eingebundene)
…". In der Oberfläche gibt es einen Angriffsknopf, aber die Einzelverluste werden nicht auf die
Armee des Spielers gebucht.

**Damit ist der Ist-Zustand ehrlich:** Regelwerk und Rechenkern sind da und geprüft
(`tests/test_kampf.py` 42 · `tests/test_kampfbericht.py` 108 · `tests/test_kampf_einhaengung.py` 42),
aber im spielbaren Spiel sterben bis heute **keine** Einzelnen.

---

## 4. Was auf Daniels Vorgabe noch fehlt (und was eine Entscheidung braucht)

| Daniels Punkt | Stand | Nötig |
|---|---|---|
| **Verlorener Kampf → prozentualer Anteil vernichtet, vor allem Karren** | **belegt vorhanden** (`_geraeteverluste`, 40 % + 5 %/Sequenz) — aber nicht verdrahtet | Verdrahtung |
| **Sieg → Transporteinheiten überleben** | **belegt vorhanden** (Verlustregel trifft nur den Verlierer) | Verdrahtung |
| **Unentschieden → Karren bleiben** | **belegt vorhanden** | Verdrahtung |
| **Knapper Sieg → trotzdem große Verluste** | entsteht aus der **Zweikampf-Simulation + Erschöpfung**; **nicht** als Prozentzahl belegt | prüfen, ob die Simulation das messbar liefert; **keine** Prozentzahl erfinden |
| **Nie ALLE Truppen vernichtet** | Simulation lässt Einheiten **fliehen** (LE < 5) statt sterben; Karren haben 40 %+ Fluchtchance | Verdrahtung + Nachweis |

**Der einzige echte VORSCHLAG-Kandidat** ist eine **Untergrenze an Überlebenden** für den Fall, dass
die Simulation nach zehn Sequenzen fast alles auslöscht. Das Handbuch nennt dafür keine Zahl. Zwei
Wege, **beide Vorschlag**:

* (a) **Keine zusätzliche Zahl** — es gilt allein die Simulation (Flucht + 10-Sequenzen-Grenze). Das
  ist am nächsten am Handbuch, kann aber im Einzelfall „alles tot" ergeben.
* (b) **Mindest-Überlebende je Einheitenart** (z. B. 1 Stück, wenn mehr als 1 vorhanden war) — gegen
  den Absturz in die Entmutigung, ausdrücklich als Remake-Vorschlag gekennzeichnet.

**Empfehlung des Koordinators:** **(a) bauen und messen**, erst wenn die Messung zeigt, dass Partien
dadurch entmutigend werden, (b) als gekennzeichneten Vorschlag nachziehen. Daniel entscheidet.

---

## 5. Reihenfolge

1. **Zuerst das laufende Ökonomie-Paket** (Entwurf `entwurf_spieloekonomie_sol_2026-10-05.txt`,
   Schritte 5-9) — der Angriff hängt an denselben Orts- und Uhrstrukturen.
2. Danach die **Kampfverluste verdrahten**: `kampf.fuehre_schlacht` aus der Oberfläche aufrufen,
   `kampfbericht.spieldaten_anwenden` auf die **lokalen** Bestände buchen (nicht global), Ergebnis in
   die Nachrichten legen, und **messen**: Verlustanteil je Ausgang (Sieg knapp / Sieg klar /
   Niederlage / unentschieden) über viele Kämpfe.
3. Erst auf Grund dieser Messung über (a)/(b) entscheiden.

**Einzelspieler-Besonderheit (Daniels Hinweis):** es gibt keine Netzspieler, also darf die
Kampflogik ihre Erwartungen an „faire" Gegner fallen lassen — der Bot ist der einzige Gegner, und
Verluste dürfen für den Spieler spürbar, aber nicht ruinös sein.
