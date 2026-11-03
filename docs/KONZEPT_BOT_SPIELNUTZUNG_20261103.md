# Konzept: Bots nutzen das Spiel wie der Spieler (Daniel 03.11.2026, 22:2x)

**Daniels Vorgabe (22:2x), woertlich-nah:** Die Bots muessen beim Kartenwaehlen VERSTEHEN, was die Felder
ihnen bringen, und danach entscheiden; sie duerfen dann alle Felder dementsprechend nutzen - genau wie
der Spieler. Sie duerfen Gebaeude ABREISSEN und ihr Dorf UMBauen, wenn sie es brauchen. Sie muessen das
Spiel moeglichst voll nutzen wie der Spieler, weil sie nur drei weitere Doerfer gruenden duerfen: wenn
der Spieler fuenf Gruendungen schafft, hat ein Bot mit vier Doerfern kaum noch eine Chance - er muss
wirklich effektiv spielen, um ein echter Gegner zu sein. "Arbeite das zum passenden Zeitpunkt ein, das
ist mir wichtig, auch wenn es sehr umfassend sein wird."

**Rang:** ENTWURF. Wird in Stufen gebaut, nicht in einem Schnitt. Der Zeitpunkt ist festgelegt (Abschnitt 5).

## 1. Was heute im Code steht (gemessen)

| Gegenstand | Ist-Stand | Beleg |
|---|---|---|
| Kartenwahl des Bots | `botkern.oekonomie_kartenwahl` mit drei Stufen (leicht/mittel/schwer); **mittel** nimmt die am schlechtesten gedeckte Rohstoffachse (Rate/Bedarf), **schwer** den Portfolio-Nutzen. Vorgabe ist **mittel** (`data/bot_wirtschaft.json: kartenwahl_stufe`) | `src/botkern.py`, `src/main.py` |
| Was die Wahl NICHT liest | das **Feldprofil** der Karte als Entscheidungsgroesse (welche Anlage auf welchem Gelaende wie viel gaebe) und die **Taktik** des Bots | `oekonomie_kartenwahl` liest nur `raten` und `bedarf` |
| Feldnutzung | Bauplan mit festen Zahlen je Gebaeude (`anlagen_je_gebaeude`); seit S-8 Stufe 2 mit Feld-Prioritaeten; Obergrenze = die Zahl in der Datei, **nicht** die Karte | `bot_doerfer_bebauen` |
| Abriss | **nur der Spieler** kann abreissen (`_karten_abreissen`, mit Sperren: keine Erstattung, die letzte Werkstatt bleibt stehen, Versorgungsschutz-Risiko). Ein Bot kann **nicht** umbauen | `src/main.py` |
| Gruendungen | Bot: hoechstens **4 Doerfer** (`hoechstens_doerfer`). Spieler: bis **6 Siedlungen** (Handbuch 2009) | `data/bot_gruendung.json`, Handbuch |

## 2. Die vier Schnitte

### S-11 Kartenwahl mit Feldverstandnis (der Kern von Daniels Punkt 1)

Der Bot bewertet jede der drei Kandidatenkarten mit dem, was sie IHM bringt:
1. **Feldprofil je Karte** (`bot_kartenprofil`: je Rohstoff Felder x Ertrag, nur auf Gelaende, auf dem
   die Anlage stehen darf) - das ist die vorhandene, belegte Rechnung.
2. **Was seine Taktik braucht** (S-8 Stufe 3: Mindestzahlen je Taktik, Engpass-Rohstoffe).
3. **Was ihm heute fehlt** (Bedarf: Rate/Bedarf je Rohstoff - die vorhandene Regel).
Die Wahl nimmt die Karte, die den groessten Nutzen fuer den ENGSTEN Rohstoff seiner Taktik bringt - nicht
mehr Gold pauschal. Pruefzusage: zwei Bots mit derselben Kandidatenliste und verschiedenen Taktiken
waehlen nachweislich verschiedene Karten; die gewaehlte Karte traegt den Engpass-Rohstoff der Taktik am
besten von den dreien.

### S-12 Alle Felder nutzen (Daniels Punkt 2)

Der Bauplan hoert auf, eine feste Obergrenze zu sein: Mindestzahlen je Taktik (S-8 Stufe 3), danach
werden freie Felder nach Ertrag gefuellt - bis kein passendes Feld mehr frei ist. Genau das hat Daniel
am 22:0x entschieden (alle Felder, die die Taktik sinnvoll fuellt; Restfelder mit dem besten Ertrag).
Pruefzusage: ein Bot-Dorf belegt am Ende jedes Feld, auf dem eine Anlage stehen darf und das seine
Taktik braucht; die Zahl der Anlagen ist von Karte zu Karte VERSCHIEDEN.

### S-13 Abriss und Umbau (Daniels Punkt 3)

Der Bot bekommt dieselbe Aktion wie der Spieler, mit denselben Sperren des Kerns (keine Erstattung, die
letzte Werkstatt bleibt, Versorgungsschutz). Dazu eine Regel, WANN er umbaut:
- ein Gebaeude steht auf einem Feld, das eine Anlage seiner Taktik besser braucht (Feld-Prioritaet),
- oder sein Lager laeuft ueber (Rohstoff dauerhaft am Deckel, waehrend ein Engpass offen ist),
- oder die Taktik hat gewechselt (das Dorf wurde kriegerisch, es braucht Kaserne statt Markt).
Sperren: hoechstens EIN Abriss je Dorf und Spieltag, nie das letzte Gebaeude einer Art, die eine
Gruendung oder die Verteidigung traegt. Jeder Abriss wird als Nachricht ins Postfach geschrieben
(der Spieler soll sehen, dass der Bot umbaut).
Pruefzusage: ein Bot reisst nachweislich ab und baut am selben Feld etwas anderes; die Zahl der
Gebaeude bleibt gleich oder steigt; keine Sperre des Kerns wird verletzt.

### S-14 Schieflage 4 gegen 6 - ENTSCHIEDEN (Daniel 22:3x): kein Gleichstand

**Bots behalten hoechstens DREI Neugruendungen, also vier Doerfer** (`hoechstens_doerfer: 4` bleibt
stehen). Der Abstand zum Spieler wird NICHT ueber die Dorfzahl ausgeglichen. Stattdessen gilt Daniels
Satz: die Bots duerfen weiter Truppen produzieren und **sich selbst optimieren** - der Ausgleich kommt
aus besserem Spiel, nicht aus mehr Doerfern. Damit werden S-13 (Umbau) und S-15 (Dorf aufgeben)
wichtiger als jede Mengenregel: ein Bot mit vier optimal gespielten Doerfern muss gegen sechs
mittelmaessig gespielte bestehen koennen.

### S-15 Dorf aufgeben und neu gruenden - fuer Bots UND Spieler (Daniel 22:3x)

**Daniels Vorgabe:** ein Bot darf ein gegruendetes Dorf "nochmal vernichten, um es neu zu gruenden, weil
eine andere Karte besser waere fuer ein Botdorf". **Der Spieler soll das auch tun koennen.**

Das ist eine neue Mechanik fuer BEIDE Seiten und beruehrt die Grundregeln nicht: Doerfer werden weiter
NIE eingenommen (das waere Eroberung von aussen), hier gibt der Besitzer sein EIGENES Dorf auf.

Sechs Gestaltungsfragen, gesammelt fuer die eine Runde (mit Vorschlag):

| Frage | Warum sie wichtig ist | Vorschlag |
|---|---|---|
| Was passiert mit Vorraeten und Gebaeuden? | sonst waere Aufgeben ein kostenloser Neustart mit vollem Lager | **Gebaeude und Vorraete verfallen** - das Dorf verschwindet ganz |
| Was passiert mit den Siedlern? | Siedler sind die harte Grenze (10 + 5 je Haus) | **sie kehren ins Hauptdorf zurueck**, hoechstens bis zu dessen Grenze; der Rest ist verloren |
| Was passiert mit stationierten Truppen? | sie duerfen nicht im Nichts stehen | sie marschieren ins Hauptdorf zurueck, mit Wegzeit (wie ein eigener Marsch) |
| Zaehlt das aufgegebene Dorf gegen die Hoechstzahl? | sonst waere Aufgeben ein Schluessel zu mehr Doerfern | **ja, bis zur Neugruendung** - gezaehlt wird, was lebt |
| Sperre zwischen Aufgeben und Neugruendung? | sonst wuerfelt ein Bot im Minutentakt | **72 Spielstunden**, wie zwischen zwei Gruendungen |
| Darf die aufgegebene Karte wieder gewaehlt werden? | sonst verliert der Bot eine gute Karte dauerhaft | nein - **eine aufgegebene Karte ist fuer diesen Bot gesperrt** |

**Wann ein Bot aufgibt (VORSCHLAG):** wenn sein Dorf auf seiner Karte den Engpass-Rohstoff seiner Taktik
nicht traegt (Feldprofil, S-11) UND eine freie Karte diesen Rohstoff deutlich besser traegt (Vergleich
ueber `bot_kartenprofil`) UND die Neugruendung bezahlbar ist (480/300/250 plus Karren). Sonst bleibt das
Dorf stehen - Umbau (S-13) ist immer die erste Wahl, Aufgeben die zweite.

**Pruefzusage:** ein Bot gibt nachweislich ein Dorf auf, gruendet auf einer besseren Karte neu, hat
danach weiterhin hoechstens vier Doerfer, und seine Kasse ist nicht gewachsen (kein Neustart-Bonus).
Der Spieler findet die Aktion im Dorf-Menue mit Rueckfrage und einer Warnung, was verloren geht.

## 3. Was das fuer den Spieler bedeutet

- Der Bot wird ein echter Gegner: er waehlt seine Karte nach dem, was sie ihm bringt, nutzt jedes Feld,
  baut um, wenn es nicht mehr passt - und kann (Weg 1) genauso viele Doerfer halten wie der Spieler.
- Der Spieler sieht es: Abriss und Umbau stehen als Nachricht im Postfach, die Spionage zeigt die
  Anlagen auf der Karte.
- Kein Doerfer wird eingenommen, Truppen werden nie am Zielort stationiert (die zwei Regeln bleiben).

## 4. Was NICHT passiert

- Keine erfundenen Erträge: alles aus `gelaende.ertrag_pro_stunde` und `data/*.json`.
- Kein stiller Regelbruch: jede neue Bot-Faehigkeit nutzt die Kernfunktion des Spielers
  (`spieloekonomie`, `dorfwall`, `versorgungsschutz`), keine zweite Wahrheit.
- Keine Zahl im Code, die Daniel nicht genannt oder aus den Daten hergeleitet ist.

## 5. Zeitpunkt im Ablauf (festgelegt)

| # | Schritt | Warum hier |
|---|---|---|
| 4 | **S-8 Stufe 3 Bauplan je Taktik** | entworfen (starkes Modell), Bau offen - liefert die Mindestzahlen, auf denen S-11 und S-12 aufsetzen |
| 4b | **S-12 Alle Felder nutzen** | direkt nach Stufe 3: der Bauplan fuellt die Karte, statt eine Zahl abzuarbeiten |
| 4c | **S-11 Kartenwahl mit Feldverstandnis** | braucht Stufe 3 (Taktik-Engpass) und S-12 (was die Felder hergeben) |
| 4d | **S-13 Abriss und Umbau** | braucht S-11 und S-12: erst wenn der Bot weiss, was er will, lohnt Umbau |
| 4e | **S-14 entschieden: kein Gleichstand** | Bots behalten drei Neugruendungen (vier Doerfer); der Ausgleich kommt aus besserem Spiel, nicht aus mehr Doerfern |
| 4f | **S-15 Dorf aufgeben und neu gruenden** (Bot UND Spieler) | Daniels Vorgabe; sechs Gestaltungsfragen mit Vorschlag stehen im Konzept |
| 5 | Die acht Kampfregeln 1 bis 8 | abgesegnet (Register 175) - bleiben danach |
| 6 | Oberflaeche: Overlay-Basis, Weltkarte, C | laeuft parallel in der Reihenfolge des Stand-Blocks |

**Regel fuer den Bau:** Jeder Schnitt bekommt seine Wache, den vollen Sammellauf und die Registerzeile;
gemessen wird mit `tools/bot_wirtschaft_messung.py` ueber 24 Spieltage, damit "effektiver" eine Zahl hat
(Dorfzahl, Kasse, Engpass) und kein Gefuehl.
