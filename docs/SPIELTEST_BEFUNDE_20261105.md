# Spieltest-Befunde 05.11.2026 — zwei Läufe, zwei Bewertungen, Zahlen statt Erzählung

**Zweck:** die erste bezahlte Spieltest-Runde auswerten. Zwei Läufe mit verschiedenem Verhalten,
zwei Urteile eines starken Modells (`deepseek-v4-pro`), daraus die belegten Engstellen und ein
Vorschlag je Befund. Die Verläufe selbst stehen in `docs/audits/SPIELTEST_LOG_20261105_1855.md`
(Lauf 1) und `docs/audits/SPIELTEST_LOG_20261105_1902.md` (Lauf 2), die Urteile in
`docs/audits/SPIELTEST_BEWERTUNG_20261105_L1.md` und `..._L2.md`.

**Kosten:** 0,0305 USD + 0,0333 USD = **0,0638 USD** von den 3,16 USD, die Daniel für Spieltests
freigegeben hat. Rest frei: 3,10 USD.

## 1. Die zwei Läufe

| Lauf | Stil | Spieltage | Saat | Einheiten am Ende | Erstes Gefecht | Gefechte | Punkte (Krieg/Forschung/Gesamt) | Bewertung | Kosten |
|---|---|---|---|---|---|---|---|---|---|
| 1 | breit | 8 | 7 | 5 (2 Kämpfer, 2 Bürgerwehr, 1 Handkarren) | T5,28 | 2 | 7 / 32 / 19 | `SPIELTEST_BEWERTUNG_20261105_L1.md` (3.382 Zeichen) | 0,0305 USD |
| 2 | krieg | 10 | 23 | 7 (4 Kämpfer, 2 Bürgerwehr, 1 Handkarren) | T5,28 | 5 | 11 / 70 / 40 | `SPIELTEST_BEWERTUNG_20261105_L2.md` (3.473 Zeichen) | 0,0333 USD |

Beide Läufe enden **ohne Tick-Fehler** (`uebersprungen` leer), also ist die Skip-Mechanik im
Normalfall nicht nötig — sie bleibt die Absicherung für den Fehlerfall.

## 2. Rohstoffbild (Endstand und Engstelle)

| Lauf | Holz min. | Holz Ende | Stein | Metall | Wolle | Leder | Gold | Mana | Pferde |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 4 (Tag 4) | 147 | 603 | 1.077 | 438 | 590 | 779 | 0 | 0 |
| 2 | 3 (Tag 8) | 58 | 951 | 1.113 | 447 | 610 | 719 | 0 | 0 |

**Ein Befund steht in beiden Läufen gleich:** Holz ist die einzige echte Engstelle, alles andere
liegt am Ende im Überschuss (Metall über 1.000, Wolle und Leder über 400, Gold über 700). Mana und
Pferde werden in 18 Spieltagen **nie** berührt.

## 3. Befunde mit Umsetzungsvorschlag

| Nr | Befund | Beleg (Zahl, Stelle) | Wirkung für den Spieler | Vorschlag | Aufwand |
|---|---|---|---|---|---|
| B1 | Holz ist ab Spieltag 1 die Bremse | Lauf 1: Holz 6 an Tag 1, 4 an Tag 4; Lauf 2: 3 an Tag 8; dritter Holzfäller erst T0,18 (Engpass-Regel) | Bau, Ausbildung und Karren warten auf Holz; der Spieler erlebt Stillstand | Entweder Start-Holz anheben (Originalzahl, nur mit Daniel) oder den dritten Holzfäller fest in die Startkette nehmen | S |
| B2 | Der **Handkarren** blockiert jeden Angriff | 236 Angriffs-Fehlversuche in beiden Läufen (Lauf 1: 193+43, Lauf 2: 88+87+42+19); erster Handkarren T5,28 | Ohne Karren keine Beute, also kein Angriff — der Spieler wartet 5 Spieltage | Karren-Kosten prüfen (Handkarren 100 Holz, 15 Metall, 15 Leder, 15 Wolle) **oder** Angriff ohne Karren erlauben (Beute 0, Kriegspunkte zählen) | M |
| B3 | Ausbildung scheitert ohne sichtbare Voraussetzung | 238 Ausbildungs-Fehlversuche (Lauf 1: 84 Handkarren, 77 Kämpfer, 77 Bürgerwehr) | Der Spieler klickt, es passiert nichts, kein Grund am Knopf | Voraussetzung am Knopf anzeigen (Stellmacher, Kriegerakademie) und Knopf bis dahin sperren | S |
| B4 | Warenfertigung ohne sichtbaren Weg | 55 Fehlversuche (36 Kurzschwert ohne Schmiede, 19 Lederrüstung ohne Nähstube) | Kämpfer wirkt unmöglich, obwohl nur eine Werkstatt fehlt | Werkstatt-Bedarf an der Ware anzeigen, Weg Werkstatt → Ware → Akademie nennen | S |
| B5 | **Kampf ist so nicht beurteilbar** | 5 Gefechte in Lauf 2, jedes mit derselben Beute 16 Holz/10 Nahrung/12 Stein, 0 Verluste, immer Ausgang Angreifer | Kein Spielerurteil über Kampf, Wall oder Verluste möglich | Angriffsziel aus einem ECHTEN Bot-Dorf speisen (Wallstufe, Verteidiger, Vorräte aus dem Bot-Zustand) | M |
| B6 | Mana- und Pferde-Kette kommt nie vor | Mana 0 und Pferde 0 in beiden Läufen über 18 Spieltage | Paladin, Ritter, Tempel, Pferdezucht bleiben ungemessen | Einen dritten Stil (breit mit Tempel und Pferdezucht) laufen lassen | S |
| B7 | Wirkungslose Bau- und Ausbauversuche | 874 in Lauf 1 (414 Bibliothek Max-Stufe, 356 alle Gebäude stehen, 104 Stellmacher Max-Stufe) | Im Verlauf ein Artefakt der Politik (jeder Schritt versucht es erneut); im Spiel wäre es ein UI-Punkt | Als UI-Aufgabe führen: Knopf bei Max-Stufe und bei vollem Bauplatz sperren | S |

## 4. Grenzen dieser Messung — was hier NICHT beurteilt ist

1. **Die Saat wirkt nicht.** Nachgerechnet: `--saat 1` und `--saat 99` ergeben bei 2 Spieltagen
   identische Bauten und identische Rohstoffe (Vergleich im Klartext: `gleich: True`). Grund ist die
   feste Startkarte (Register 229) und die fehlende zweite Siedlung. Verläufe unterscheiden sich
   zurzeit nur über `--stil` und `--tage`. Der Bericht sagt das jetzt selbst.
2. **Die Waren sind im Lauf kostenlos.** `spielschicht.ware_fertigen` reicht die Rezepte durch,
   bucht aber **keine Kosten** und prüft **keine Forschungsvoraussetzung** — der GUI-Weg
   (`spieloekonomie.ware_start_menge`) tut beides. Folge: Kurzschwert und Lederrüstung entstehen im
   Lauf umsonst, und ohne Waffentechnik-Forschung. Die Kette Werkstatt → Ware → Einheit ist also
   **zu günstig** gemessen; T1,38 für den ersten Kämpfer ist eine Untergrenze.
3. **Keine Oberfläche, keine Klickzeit.** Aussagen über Bedienbarkeit und Spielgefühl sind damit
   nicht belegt (beide Urteile sagen das selbst).
4. **Bots kommen nur als fixes Ziel vor.** Bot-Wirtschaft, Bot-Angriffe und Verteidigung sind in
   keinem der beiden Läufe berührt.

## 5. Was die zwei Urteile vorschlagen (unverbindlich, mit meiner Einordnung)

| Vorschlag des Modells | Lauf 1 | Lauf 2 | Aufwand | Meine Einordnung |
|---|---|---|---|---|
| Start-Holz erhöhen (auf 150 bzw. 180) | ja | ja | S | **Nur nach Daniel** — Startvorräte sind eine Originalzahl (10 Siedler, 100 Holz, 100 Stein) |
| Dritter Holzfäller früh | — | ja | S | Deckt sich mit B1; die Engpass-Regel der Simulation tut das schon ab T0,18 |
| Ausbildungs-/Angriffsvoraussetzungen anzeigen und Knöpfe sperren | ja | ja | S | Deckt sich mit B3, B4, B7 — reine UI-Arbeit, kein Balancing |
| Pause von 10 echten Sekunden je Spieltag | — | ja | S | Neue Mechanik, gehört zu Daniels Entscheidung (Spieluhr x180) |
| Tutorial oder geführte Startsequenz | ja | ja | L | Größter Hebel für den Einstieg, aber ein eigener Schnitt mit Konzept |
| Fortschritt der vier Auszeichnungen anzeigen | — | ja | M | Passt zu E5 (kein Sieg, vier Auszeichnungen) |
| Angriff erst ab 2–4 Kämpfern und 1 Karren freischalten | ja | ja | S | Deckt sich mit B2, ändert aber die Spielregel — Daniel fragen |

## 6. Reihenfolge der nächsten Schnitte (Vorschlag, klein nach groß)

1. **W1 — Waren-Kosten im Kern-Weg** (`spielschicht.ware_fertigen` bucht Kosten und prüft die
   Forschungsvoraussetzung wie `spieloekonomie`). Kernänderung, eigener Schnitt, eigene Wache,
   danach die beiden Läufe neu fahren (kostet je ~0,03 USD) — erst dann sind die Zahlen belastbar.
2. **B2 — Karren vor dem Angriff:** entweder Karren früher möglich oder Angriff ohne Karren mit
   Beute 0. Messbar machen, nicht raten.
3. **B3/B4/B7 — Voraussetzungen und Knöpfe** (eine UI-Runde, drei Punkte).
4. **B5 — Kampfziel aus einem echten Bot-Dorf.**
5. **B6 — dritter Stil** (Tempel, Pferdezucht), damit Mana und Pferde im Verlauf vorkommen.

## 7. Offene Fragen an Daniel (eine Runde, Empfehlung zuerst)

1. **Start-Holz:** Originalzahl lassen oder auf 150 anheben? *Empfehlung: lassen* — die Engstelle ist
   gewollt, und die Simulation kann sie mit dem dritten Holzfäller selbst lösen.
2. **W1 jetzt bauen** (Waren kosten im Kern-Weg Geld und Forschung)? *Empfehlung: ja, als nächster
   Schnitt* — ohne das sind alle weiteren Zahlen zu günstig.
3. **Angriff ohne Karren erlauben** (Beute 0)? *Empfehlung: nein, aber Karren früher baubar machen* —
   die Beute-Regel ist belegt, die Karren-Kosten sind es auch; der Engpass gehört ins Balancing.
4. **Neue Spielversion 0.0.2 veröffentlichen**, sobald der volle Sammellauf grün ist (die
   Ware-Wache und der Instrument-Fix sind spielrelevant)? *Empfehlung: ja, mit Ankündigung.*
