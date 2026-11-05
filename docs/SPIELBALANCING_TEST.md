# Spielbalancing-Test — der Maßstab für das ganze Spiel

**Was das ist.** Ein **wiederholbarer** Prüfaufbau, der nachrechnet, ob unsere Zahlen in einem
**langen** Spiel zu erreichbaren, ausgeglichenen und überhaupt spielbaren Situationen führen — nicht
nur, ob eine Regel grün geprüft ist. Er wird **bei jeder Datenänderung neu gefahren** und die Zahlen
hier werden ersetzt, nicht ergänzt: dieses Dokument zeigt immer den letzten gemessenen Stand.

**Woher es kommt.** Daniel, 31.10.2026, wörtlich:

> „versuch bitte mal abzuprüfen wie die relationen zu einander aussehen würden in einem langzeit
> spiel ob dann unsere zahlen noch halbwegs sinn machen. Folgendes szenario. Wie viele gesamt truppen
> müsste ich ansammeln und wie müssten sie verteilt sein und angriffe getimed werden damit ich
> einmalig einen anderen spieler mit der hälfte an gesamt truppen wie ich, damit ich einmal alle seine
> vorhandenen ressourcen stehlen würde und wie viele ressourcen wären zu so einem spielzeitpunkt
> überhaupt wahrscheinlich und sinnvoll und sind zu solchen zeitpunkten dann auch die kosten von
> forschung oder truppen ausbildungskosten oder die item produktionskosten im zusammenhang mit
> benötigter menge für die truppenstärken … ob ein spieler dafür zeitgleich soviele angriffe gar
> nicht koordinieren könnte aus seiner benutzeroberfläche und zudem ob all das sinn gibt mit orginal
> spielnachweisen.“

Daraus sind sechs Prüffragen geworden (Abschnitt 1), ein Messwerkzeug (Abschnitt 2) und ein Verdikt
mit Zahlen (Abschnitte 3–5). **Balancing ist damit ein eigener Testtyp neben den Regelprüfungen** —
er prüft nicht „stimmt die Formel“, sondern „führt die Formel zu einem spielbaren Spiel“.

---

## 1. Die sechs Prüffragen

| # | Frage | Plausibel heißt |
|---|---|---|
| **B-1** | Wie groß können Armeen überhaupt werden — und was begrenzt sie? | Eine Armee, die eine Stadt einnehmen kann, muss in **einer** Spielzeit von wenigen Wochen erreichbar sein, nicht in 100 Spieltagen |
| **B-2** | Reichen die Kosten von Forschung, Ausbildung und Ausrüstung im Verhältnis zur Truppenstärke? | Kein einzelner Posten (Gold, Forschung, Werkstatt) darf allein die ganze Wirtschaft über Jahre blockieren |
| **B-3** | Kann ich einem Gegner mit **halber** Truppenstärke **alle** Ressourcen stehlen? | Es muss **einen** Weg geben (Truppen + Karren + Wellen), und er darf nicht 20 Angriffe brauchen |
| **B-4** | Wie viele Ressourcen liegen zu einem Zeitpunkt überhaupt da? | Vorrat und Tragekapazität müssen in derselben Größenordnung liegen, sonst ist Beute sinnlos oder unmöglich |
| **B-5** | Kann ein Spieler die nötigen Angriffe aus der Oberfläche koordinieren? | Die Zahl der Aufträge muss aus **einer** Ansicht heraus machbar sein, und die Wartezeit darf nicht jede Welle einzeln erzwingen |
| **B-6** | Sind die Zahlen mit dem Original nachweisbar? | Jeder dominante Wert ist entweder BELEGT (Handbuch/Fassung 2006 mit Stelle) oder bewusst als VORSCHLAG geführt und benannt |

**Kein Teil dieser Prüfung entscheidet Daniel ab** — sie liefert Zahlen. Wo eine Zahl nicht stimmt,
steht die Frage in `docs/FRAGEN_AN_DANIEL_<TTMM>.md`.

---

## 2. Messverfahren

**Werkzeug:** `python -X utf8 tools/balancing_messung.py` (Optional: `--tage 7,30,90,180`).
Es rechnet **nur** aus Projektdaten und den echten Kernfunktionen; nichts ist geschätzt:

| Quelle | Was daraus kommt |
|---|---|
| `data/originalkarten/katalog.json` | Geländeverteilung aller 127 Originalkarten (10×10) — was physisch auf eine Karte passt |
| `data/buildings.json` | Erträge je Gebäude und Gelände, Standortregeln, Wallstufen mit SK-Schwellen |
| `data/units.json` | Kosten, Werte (LE/AT/PA/SK …), Ausrüstungswaren je Einheit |
| `data/warenrezepte.json` | Material und Dauer je Ware (Werkstatt) |
| `data/research.json` | Forschungsregeln: Dauer = Stufe² Stunden, Kosten verdoppeln sich |
| Kern | `einheiten.ladung_der_gruppe`, `einheiten.schlagkraft`, `kampf.fuehre_schlacht` (echte Schlachten, 40 Läufe je Wandstufe mit festen Startwerten), `kampfbericht.beute_staffel`, `auftraege.reisezeit_sekunden`, `auftraege.kosten_der_mission`, `forschung.kosten` |

**Zeitbasis:** Spieltage = 24 Spielstunden. Die Spieluhr (Faktor 180 = eine Spielstunde in 20
Sekunden) ändert nur das Anzeigetempo, nicht die Verhältnisse.

**Annahmen (klar benannt, jede änderbar):** Ausbau je Siedlung = 10 Häuser, 1 Bibliothek, 1
Kriegerakademie, 1 Stellmacher, 2 Schmieden, 1 Nähstube, 1 Bogenbauer, 1 Wall; die übrigen Felder
produzieren auf dem **besten** Gelände (Berg dreigeteilt Stein/Metall/Gold, Grasland für
Nahrung/Wolle/Pferde/Rinder, Wald für Holz und Jagd, Nebelsee für Mana). Hochgerechnet auf das
belegte Maximum von **6 Siedlungen**.

---

## 3. Gemessene Basis — Stand 31.10.2026 (Lauf mit `tools/balancing_messung.py`)

### 3.1 Was passt auf eine Karte?

| Gelände | Felder je Karte (Mittel über 127 Karten) |
|---|---|
| Steppe | 23,5 |
| Wald | 20,9 |
| **Sumpf** (unbebaubar) | **19,0** |
| Grasland | 13,6 |
| Hügel | 11,7 |
| Berg | 9,4 |
| Nebelsee | 1,7 |

**Befund:** Fast ein Fünftel jeder Karte ist Sumpf und fällt weg. Berg (9,4) und Nebelsee (1,7) sind
knapp — Metall, Gold und Mana sind also von der Karte her gedeckelt, nicht von der Forschung.

### 3.2 Erträge des Reiches (6 Siedlungen, Plan aus Abschnitt 2)

| Rohstoff | je Stunde | je Spieltag |
|---|---|---|
| Holz | 301 | 7.228 |
| Nahrung | 231 | 5.542 |
| Leder | 149 | 3.584 |
| Metall | 68 | 1.631 |
| Stein | 68 | 1.631 |
| Wolle | 61 | 1.469 |
| **Gold** | **51** | **1.224** |
| Pferde | 49 | 1.175 |
| Mana | 22 | 539 |

### 3.3 Bestand, wenn nichts ausgegeben wird

| Spieltage | Holz | Nahrung | Leder | Metall | Stein | Wolle | Gold | Pferde | Mana | Summe |
|---|---|---|---|---|---|---|---|---|---|---|
| 7 | 50.594 | 38.796 | 25.089 | 11.420 | 11.420 | 10.280 | 8.565 | 8.224 | 3.770 | **168.158** |
| 30 | 216.830 | 166.269 | 107.524 | 48.942 | 48.942 | 44.059 | 36.706 | 35.247 | 16.157 | **720.676** |
| 90 | 650.490 | 498.807 | 322.571 | 146.826 | 146.826 | 132.177 | 110.119 | 105.741 | 48.472 | **2.162.029** |
| 180 | 1.300.980 | 997.614 | 645.143 | 293.651 | 293.651 | 264.353 | 220.238 | 211.483 | 96.945 | **4.324.058** |

### 3.4 Die harte Grenze: Siedler, nicht Rohstoffe

* Siedlergrenze: **10 + 5 je Haus** → bei 10 Häusern **60 je Siedlung**, im Reich **360**.
* **Jede** Einheit und **jeder** Karren kostet Siedler. Armee und Transport teilen sich denselben Topf.
* Folge: **360 Soldaten ist das theoretische Maximum** — und dann wächst die Bevölkerung nicht mehr,
  weil alle Siedler in der Armee stehen.

### 3.5 Was kostet eine Armee?

| Einheit | Siedler | Gold | Pferde | Ausrüstung | Material | Werkstatt-Stunden |
|---|---|---|---|---|---|---|
| Krieger | 1 | 500 | 1 | Schwert, Kettenhemd | Metall 5 | 1,7 |
| Ritter | 1 | 1.000 | 1 | Schwert, Plattenrüstung | Metall 7 | 2,3 |
| Kurzbogenschütze | 1 | 250 | 0 | Kurzbogen | Holz 4 | 1,0 |
| Handkarren | 1 | 0 | 0 | — | — | — |
| Zweispänner | 2 | 0 | 2 | — | — | — |
| Handelskarawane | 10 | 200 | 15 | — | — | — |

* **50 Krieger** = 25.000 Gold = **20 Spieltage** des vollen Goldertrags, 50 Siedler, 250 Metall,
  83 Werkstatt-Stunden (= 2 Spieltage in 2 Schmieden).
* **100 Krieger** = 50.000 Gold = **41 Spieltage**, 100 Siedler, 500 Metall, 3 Spieltage Werkstatt.
* **200 Krieger** = 100.000 Gold = **82 Spieltage**, 200 Siedler, 1.000 Metall, 7 Spieltage Werkstatt.

### 3.6 Forschung

| Stufe | Kosten der Stufe | Gesamt (Holz) | Gesamtdauer |
|---|---|---|---|
| 1 | 50 | 50 | 1 h = 0,04 Spieltage |
| 3 | 200 | 350 | 14 h = 0,6 Spieltage |
| 5 | 800 | 1.550 | 55 h = 2,3 Spieltage |
| 7 | 3.200 | 6.350 | 140 h = 5,8 Spieltage |
| 8 | 6.400 | 12.750 | 204 h = 8,5 Spieltage |
| 10 | 25.600 | 51.150 | 385 h = 16,0 Spieltage |

**Alle 21 Gebiete auf Stufe 10:** 1.074.150 Holz = **149 Spieltage**, wenn der gesamte Holzertrag
(7.228/Tag) nur in Forschung ginge.

### 3.7 Wall: wie viele Truppen öffnen ihn? (SK-Schwellen aus den Daten)

| Wallstufe | Name | Schwelle Fußtruppen | nötige Krieger (SK 3) | Schwelle Belagerung |
|---|---|---|---|---|
| 1 | Erdwall | 10 | 3 | — |
| 2 | Steinwall | 40 | 13 | — |
| 3 | Kleine Palisade | 90 | 30 | — |
| 4 | Palisade | 160 | 53 | — |
| 5 | Verstärkte Palisade | 250 | 83 | 500 |
| 6 | Mauer | 360 | **120** | 600 |
| 7 | Verstärkte Mauer | 490 | 163 | 700 |
| 8 | Festungsmauer | 640 | 213 | 800 |
| 9 | Verstärkte Festungsmauer | 810 | 270 | 900 |
| 10 | Bollwerk | 1.000 | **333** | 1.000 |

### 3.8 Kampf: Angreifer mit DOPPELTER Stärke gegen die Hälfte (echte Simulation, 40 Läufe)

Angreifer 40 Krieger + 10 Handkarren, Verteidiger 20 Krieger, Beutevorrat 5.000/5.000/2.000:

| Wall | Vorrunde bestanden | Siege | eigene Verluste Ø | Beute Ø |
|---|---|---|---|---|
| 0 | 40/40 | 40/40 | 10,9 von 50 | Holz 168 · Metall 66 · Stein 166 |
| 2 | 40/40 | 40/40 | 10,9 von 50 | wie oben |
| 3 | 40/40 | 40/40 | 10,9 von 50 | wie oben |
| 4 | **0/40** | 0/40 | 0 | **keine** — Vorrunde scheitert, kein Kampf |
| 6 | 0/40 | 0/40 | 0 | keine |

**Befund:** Nicht die Schlacht entscheidet, sondern **die Wandstufe**: 40 Krieger schlagen 20 Krieger
bei Wall 0–3 verlustarm (22 %) und kommen an Wall 4 nicht einmal heran.

### 3.9 Beute: Karren, Siedler und Wellen

| Karren | Ladung je Stück | Siedler je Stück | Ladung je Siedler |
|---|---|---|---|
| Handkarren | 40 | 1 | 40 |
| Zweispänner | 250 | 2 | **125** |
| Handelskarawane | 1.000 | 10 | 100 |

Beuteanteile (VORSCHLAG, Register 45): Wall heil **10 %**, Wall beschädigt **30 %**, Wall gebrochen
**60 %**, keine Verteidiger mehr **100 %** — gedeckelt durch die Ladung der Karren.

**Feldzug mit 60 Zweispännern (120 Siedler, Ladung 15.000), je Welle 3,2 h hin und zurück, das Reich
produziert in der Zeit weiter:**

| Spieltage | Bestand | Wellen bis < 5 % | geholt | Rest |
|---|---|---|---|---|
| 7 | 168.158 | **14** | 210.000 | 3.000 (2 %) |
| 30 | 720.676 | 20 (Abbruch) | 300.000 | 484.736 (**67 %**) |
| 90 | 2.162.029 | 20 | 300.000 | 1.926.089 (89 %) |
| 180 | 4.324.058 | 20 | 300.000 | 4.088.118 (95 %) |

### 3.10 Weg, Kosten je Welle

| Entfernung | eine Strecke | hin und zurück | Gold | Nahrung | Mana |
|---|---|---|---|---|---|
| 5 Felder | 0,4 h | 0,8 h | 500 | 0,8 | 7,5 |
| 10 Felder | 0,8 h | 1,6 h | 1.000 | 1,6 | 10,0 |
| 20 Felder | 1,6 h | 3,2 h | 2.000 | 3,2 | 15,0 |

(Gold skaliert mit der **Armeegröße** — 40 Einheiten auf 10 Feldern kosten 1.000 Gold = 2 Krieger.)

### 3.11 Nahrungsverbrauch der Garnison (Daniels Entscheidung 7, seit 31.10.2026 im Kern)

Einheiten verbrauchen **laufend** Nahrung, nicht nur bei der Anschaffung. Den Betrag nennt **keine**
Originalstelle — er ist ein VORSCHLAG und aus dem Reichsertrag hergeleitet
(`data/nahrungsverbrauch.json`): **8 Nahrung je Einheit und Spieltag** = 1/3 je Spielstunde.

| Garnison | Verbrauch je Spieltag | Anteil am Nahrungsertrag (5.542/Tag) | bleibt übrig |
|---|---|---|---|
| 50 Einheiten | 400 | 7,2 % | 5.142 |
| 100 Einheiten | 800 | 14,4 % | 4.742 |
| 200 Einheiten | 1.600 | 28,9 % | 3.942 |
| **360 (Siedlerdeckel)** | **2.880** | **52,0 %** | **2.662** |

**Befund.** Der Ertrag trägt **692** Einheiten, der Siedlerdeckel liegt bei **360** — eine Armee kann
das Reich also nicht aushungern, eine große bindet aber die Hälfte der Nahrung. Zusammen mit den
Waren, die ebenfalls Nahrung kosten (Brot 20, Bier 30, Trank 10) und den Einheitenpreisen
(Streuner/Bürgerwehr 100, Siedlerkarren 300) bleibt Nahrung ein **zweiter Engpass neben Gold**,
aber ein tragbarer.

**Nicht gebaut (bewusst):** keine Strafe bei Unterdeckung (keine Toten, kein Aufstand). Der Bestand
fällt auf 0, der Rest steht als `unterdeckung` im `produktionsjournal`. Eine Strafe wäre eine eigene
Entscheidung Daniels.

---

### 3.11b Wagenbau auf der Karrenladung (Daniels Entscheidung 2, seit 31.10.2026 im Kern)

Die belegten Ladungswerte (Handkarren 40, Einspänner 100, Zweispänner 250, Handelskarawane 1.000,
Große Handelskarawane 2.500) bleiben die **Basis**; **Wagenbau** gibt **+10 % je Stufe** obendrauf,
gedeckelt auf **Stufe 10 = Faktor 2,0** (`data/karrenkapazitaet.json`, VORSCHLAG, abschaltbar).

| Wagenbau | Faktor | Zweispänner | 60 Zweispänner | Handelskarawane |
|---|---|---|---|---|
| 0 (Basis) | 1,00 | 250 | 15.000 | 1.000 |
| 5 | 1,50 | 375 | 22.500 | 1.500 |
| 10 | 2,00 | 500 | 30.000 | 2.000 |

**Folge für die Beute (Abschnitt 3.9):** mit voller Forschung trägt dieselbe Flotte die doppelte
Menge — der Feldzug braucht rechnerisch **etwa die Hälfte der Wellen**. **Offen:** diese Zahlen sind
hier gerechnet, noch **nicht** durch `tools/balancing_messung.py` gefahren (das Werkzeug übergibt
noch keine Forschungsstufen). Gates G-2 und G-6 sind deshalb mit Wagenbau **neu zu messen**, bevor
sie als erfüllt oder verfehlt gelten.

### 3.12 Karten, Dörfer und Pech (Teil 2 des Balancing-Tests, Daniel 31.10.2026)

Daniel wörtlich: „Integriere in das balancing testing auch verschiedene karten dörfer die spieler
besitzen können bis zu welchen zeitpunkten und beachte dabei das man auch richtig pech haben kann nur
schlechte karten bekommt und deswegen sehr viele ressourcen verbraucht bevor man eine richtige neue
karte besiedelt sowas kann enormen einfluss auf das spielverhalten haben.“

**Werkzeug:** `python -X utf8 tools/balancing_karten.py [--spiele N] [--seed S]` — rechnet jede der
127 Originalkarten einzeln durch (bester Ausbauplan, Stundenertrag), den Gründungs- und Ausbaubedarf
aus `data/baupreise.json`/`data/units.json` und zwei Ziehungsarten.

### Die Karten selbst (gemessen über alle 127)

| Kategorie | Karten | freie Felder (min/median/max) | Nahrung/h | Holz/h | Gold/h |
|---|---|---|---|---|---|
| beste | 35 | 51 / 88 / 100 | 8,0 / 32,0 / 64,0 | 0 / 43,2 / 120,0 | 0 / 12,6 / 18,9 |
| mittlere | 43 | 24 / 84 / 95 | 9,6 / 35,2 / 79,2 | 0 / 48,0 / 103,2 | 1,8 / 9,0 / 14,4 |
| schlechte | 49 | 32 / 80 / 100 | 9,6 / 41,6 / 89,6 | 0 / 45,6 / 120,0 | 0 / 4,5 / 11,7 |

**Befund 1: Die historische Kategorie-Ist-Zahl sagt wenig.** Fast jede Karte hat 80–100 freie Felder;
die Kategorie beschreibt die **Mischung**, nicht die Größe. Gold reicht von 0 bis 18,9/h, Nahrung von
8,0 bis 89,6/h. Die gemessen **stärkste** Karte trägt den Namen „Der ultimative Mist“ — und ist eine
Karte der Gruppe *schlechte*. Wer nach dem Kategorienamen wählt, wählt falsch.

### Was eine neue Siedlung wirklich kostet

| Posten | Holz | Stein | Nahrung | Metall | Leder | Wolle | Pferde |
|---|---|---|---|---|---|---|---|
| Mindestbestand im Ortslager (Gründungsgebühr + Startpaket) | 480 | 300 | 250 | — | — | — | — |
| Siedlerkarren (Pflicht, Handbuch) | 200 | — | 300 | 80 | 150 | 100 | 4 |
| Forschung Wagenbau 1 | 50 | — | — | — | — | — | — |
| **Summe vor dem ersten Bau** | **730** | **300** | **550** | **80** | **150** | **100** | **4** |
| Ausbau der neuen Karte (10 Häuser + alle Produktionsgebäude) | 1.099–2.293 | 692–1.539 | — | — | — | — | — |
| **Gesamt bis die Siedlung trägt** | **1.829–3.023** | **992–1.839** | 550 | 80 | 150 | 100 | 4 |

**Befund 2 (Daniels Punkt):** die Gründungsgebühr ist **nicht** der Preis einer Siedlung — der Ausbau
kostet das Zwei- bis Dreifache, bei einem großen Plan zusätzlich **50 Siedler**. Eine schlechte Karte
ist deshalb teurer als eine gute: man zahlt dieselben Gebäude auf schlechteren Feldern.

### Bis zu welchem Zeitpunkt hat man wie viele Dörfer (Vollertrag, Untergrenze)

| Siedlungen | Reichsertrag/Tag | Tage bis zur nächsten Gründung |
|---|---|---|
| 1 → 2 | Holz 1.152 · Stein 288 · Nahrung 998 | 1,0 |
| 2 → 3 | Holz 2.304 · Stein 576 · Nahrung 1.997 | 0,5 |
| 3 → 4 | Holz 3.456 · Stein 864 · Nahrung 2.995 | 0,3 |
| 4 → 5 | Holz 4.608 · Stein 1.152 · Nahrung 3.994 | 0,3 |
| 5 → 6 | Holz 5.760 · Stein 1.440 · Nahrung 4.992 | 0,2 |

**Lesart:** das ist eine **Untergrenze** (jede Siedlung hat ab Tag 1 den ganzen Ausbauplan). In
Wahrheit kosten Bau und Forschung Zeit — die Anlauf-Simulation (Baureihenfolge, Stunden für Stunden)
ist **noch nicht gebaut** und steht als offener Punkt (Frage 11).

### Pech und Glück: zwei Ziehungsarten

| Szenario | Holz/Tag | Stein/Tag | Nahrung/Tag | Gold/Tag |
|---|---|---|---|---|
| **PECH** — nur die 5 schlechtesten Karten | 2.650 | 864 | 2.726 | **648** |
| **GLÜCK** — die 5 besten Karten | 12.730 | 2.045 | 9.926 | **1.534** |

Zufall über 2.000 Partien (gleichverteilt aus den 126 freien Originalkarten):

| Kennzahl | 5 % schlechteste | Median | 5 % beste |
|---|---|---|---|
| Reichsertrag/Tag (6 Siedlungen, Summe) | 20.525 | 24.964 | 29.740 |
| **Gold/Tag** (der Engpass des Spiels) | **886** | **1.318** | **1.685** |

**Befund 3:** die Kartenlage verschiebt den **Goldertrag um ±30 %** — bei 41 Spieltagen für 100
Krieger sind das gut 12 Spieltage Unterschied. Das ist spürbar, aber nicht ruinös; ein echter
Pechstrudel entsteht erst durch die **Ausbaukosten** (Befund 2), nicht durch den Ertrag allein.

### Der wichtigste Befund: es gibt heute GAR KEINEN Zufall

`originalkarten.vorrat()` gibt **alle** 126 Karten frei, die Gründungsmaske lässt die **freie Wahl**,
und `ziehchancen()` sagt das selbst („nur_optionale_zufallsziehung_nicht_freie_auswahl“). Das Original
vergibt Karten dagegen **per Zufall** (Handbuch 2009, Z. 313). Wer Pech haben soll, braucht also erst
eine Entscheidung: freie Wahl (heute, kein Pech) oder Zufallsziehung (original, mit Pech). Das steht
als **Frage 10** in `docs/FRAGEN_AN_DANIEL_20261031_1845.md` — ohne Entscheidung wird nichts gebaut.

---

## 4. Verdikt je Prüffrage

| # | Antwort aus den Messwerten | Urteil |
|---|---|---|
| **B-1** | Armee-Deckel **360** Köpfe im ganzen Reich (Siedler). 100 Krieger kosten 41 Spieltage **Gold**. Eine Armee „mittlerer“ Größe (60–100) ist in 20–40 Spieltagen erreichbar | **spielbar, aber golddominant** — Gold ist der Engpass, nicht Metall, nicht Forschung |
| **B-2** | Forschung Stufe 10 je Gebiet 51.150 Holz = **7 Spieltage** des gesamten Holzertrags (nicht 149 — die gelten für alle 21 Gebiete). Werkstatt und Material sind **kein** Engpass (Metall 500 für 100 Krieger = 0,3 Spieltage) | **Forschung und Ausbildung sind im Rahmen**; nur „alles auf 10“ ist ein Langzeitprojekt |
| **B-3** | Mit 60 Zweispännern (120 der 360 Siedler) holt man an Spieltag 7 in **14 Wellen** 98 % — an Spieltag 30 nur noch 33 %, danach praktisch nichts. „Einmal alle Ressourcen stehlen“ ist **nur früh** möglich | **nicht erfüllt** für das Langzeitspiel — die Beute ist strukturell gedeckelt (Siedler → Karren → Ladung) |
| **B-4** | Vorrat wächst linear mit der Zeit (168k → 4,3 Mio), Tragekapazität wächst nur mit Siedlern (gedeckelt bei 360) | **Verhältnis kippt** — ab etwa Spieltag 30 ist der Vorrat größer als jede mögliche Transportflotte |
| **B-5** | 14 Wellen à 3,2 h sind **ein** Spielabend, nicht mehr: pro Welle ein Auftrag (Ziel, Truppen, Bestätigung). Ab 20+ Wellen wird es Klickarbeit ohne Entscheidung | **koordinierbar, aber ab ~10 Wellen monoton** — Rückmeldung: Wellen müssen weniger, nicht mehr werden |
| **B-6** | Alle dominanten Werte sind belegt: Einheitenkosten (Handbuch), Wallschwellen (Handbuch S. 21), Erträge (Handbuch), Siedler +5 je Haus (S. 11), Karrenladung (S. 23). **Nicht belegt** und damit Stellschrauben: Beuteanteile 10/30/60/100 %, Reisekosten-Sätze, Ausbildungsdauer (Grunddauer), Aufteilung der Beute auf Rohstoffe | **Originaltreue ist gegeben**, die Balance hängt an vier VORSCHLAG-Werten |

**Die drei Zahlen, die das Spielgefühl am stärksten bestimmen (VORSCHLAG, nicht belegt):**

1. **Gold je Einheit** (500 für den Krieger) gegen **Goldertrag** (3/h je Goldmine, 9,4 Bergfelder je
   Karte): Armeen wachsen im Wochen-, nicht im Tagesmaßstab.
2. **Beuteanteile** 10/30/60/100 %: Sie entscheiden, ob ein Angriff etwas bringt.
3. **Ladung je Karren** (40/250/1.000) und **Karren kosten Siedler**: Sie entscheiden, ob Beute
   überhaupt nach Hause kommt.

---

## 5. Was daraus als Nächstes folgt (keine Entscheidung ohne Daniel)

* **Frage 1 — Beute-Deckel:** Soll die Tragekapazität mit der Zeit wachsen (größere Karren, Forschung
  „Wagenbau“ als Kapazitätshebel), oder soll die Beute bewusst eine **Quote** bleiben (nur ein Teil
  des Vorrats, dafür nie „alles“)?
* **Frage 2 — Gold als Engpass:** Ist es gewollt, dass 100 Krieger 41 Spieltage des gesamten
  Goldertrags kosten? Alternative: Goldertrag je Goldmine (belegt 3/h) unverändert lassen und den
  **Einheitenpreis** senken — oder den Armeedeckel über Häuser/Ausbaustufen heben.
* **Frage 3 — Wall-Wettlauf:** Wall 10 verlangt 333 Krieger = 92 % des Soldaten-Deckels. Soll eine
  maximale Wand damit praktisch uneinnehmbar sein (Belagerungswaffen sind der einzige Weg), oder
  sollen die Schwellen relativ zur Armeegröße gedeckelt werden?
* **Frage 4 — Wellen-Zahl:** Soll ein Feldzug aus 3–4 Wellen bestehen (dann muss die Ladung je Karren
  steigen oder die Beutequote), oder ist die lange Serie gewollt?

Diese vier Fragen stehen im Auswahlformular; bis zur Antwort bleibt der **gemessene** Stand gültig und
wird nicht stillschweigend geändert.

---

## 6. Balancing-Gates (was später automatisch geprüft werden soll)

Diese Schwellen sind der Kern des „Balancing-Tests“ — sie sind noch **nicht** als Prüfdatei gebaut,
sondern hier festgelegt. Ein Gate ist eine Zahl, die sich aus den Daten rechnen lässt:

| Gate | Bedingung | Heute |
|---|---|---|
| G-1 Armee erreichbar | 100 Krieger in ≤ 30 Spieltagen bezahlbar | **41 Tage — verfehlt** |
| G-2 Beute wirkt | Ein Feldzug (≤ 5 Wellen) holt ≥ 25 % des Vorrats | **verfehlt** (14 Wellen für 98 %, ab Tag 30 gar nicht) |
| G-3 Wall fair | Wall 6 in ≤ 40 % des Soldaten-Deckels angreifbar | **erfüllt** (120 von 360 = 33 %) |
| G-4 Forschung | Ein Forschungszweig auf 10 in ≤ 10 Spieltagen | **erfüllt** (7 Tage) |
| G-5 Ausbildung | 100 Einheiten in ≤ 5 Spieltagen ausgerüstet | **erfüllt** (3 Tage) |
| G-6 Wellen | Ein Feldzug ≤ 5 Aufträge | **verfehlt** (14) |
| G-7 Nahrung trägt die Armee | Garnison beim vollen Siedlerdeckel (360) bindet ≤ 60 % des Nahrungsertrags | **erfüllt** (52,0 %) |
| G-8 Erste Gründung | die STARTKARTE allein trägt den Gründungsbedarf in ≤ 10 Spieltagen (Vollertrag) | **erfüllt** (0,8 Tage) |
| G-9 Pech nicht ruinös | auch die schlechteste Kartenlage trägt die 6. Siedlung in ≤ 120 Spieltagen | **erfüllt** (Vollertrag; die Anlaufzeit fehlt noch) |

**Regel:** Ein Gate, das verfehlt wird, ist **kein Fehler im Code**, sondern eine offene
Balancing-Frage (siehe Abschnitt 5). Erst wenn Daniel entschieden hat, wird die Zahl geändert — dann
muss dieses Dokument neu gemessen werden.

---

## 7. Wartung

1. **Nach jeder Änderung** an `data/units.json`, `data/buildings.json`, `data/warenrezepte.json`,
   `data/research.json`, `data/nahrungsverbrauch.json` oder an `beute_staffel` /
   `kosten_der_mission` / `reisezeit_sekunden` / `tagesbedarf_nahrung`:
   `python -X utf8 tools/balancing_messung.py` laufen lassen.
2. Die Tabellen in Abschnitt 3 **ersetzen** (nicht anhängen) und das Datum im Kopf ändern.
3. Verdikt (Abschnitt 4) und Gates (Abschnitt 6) neu beurteilen; ein geändertes Urteil mit einem Satz
   begründen.
4. Wenn alle Gates stehen und Daniel die offenen Fragen beantwortet hat: die Gates als echte
   Prüfdatei bauen (`tests/test_balancing_gates.py`) und in den Sammellauf aufnehmen.
5. Das Werkzeug ist **kein** Ersatz für den Spieltest: Es rechnet Verhältnisse, es spielt nicht.

---

## 8. Grenzen dieser Messung (ehrlich)

* Der Ausbauplan ist eine **Annahme** — eine andere Verteilung verschiebt die Erträge um ±20 %.
* Bots handeln mit; ihre Vorräte und Truppen sind hier **nicht** modelliert.
* Die Kampfsimulation läuft mit **festen** Startwerten und ohne Forschungsboni (also ohne
  Waffentechnik/Rüstungsbau-Vorteile) — sie zeigt die Richtung, nicht den Grenzfall.
* Handel zwischen eigenen Siedlungen, Götter schutz und Portalwechsel sind nicht eingerechnet.
* „Spieltage“ sind Spielzeit, nicht Echtzeit: bei Faktor 180 ist ein Spieltag 8 Echtzeitminuten.

## 9. Drachenkampf - Messung 05.11.2026 (W-17)

**Werkzeug:** `tools/drachen_balancing.py`, roher Lauf in
`docs/audits/drachen_balancing_20261105.log`. Gerechnet mit den echten Kernfunktionen
(`kampf.fuehre_schlacht` mit den Drachenschwellen, `drachen.feueratem_verluste`), 100 Laeufe je
Zelle, fester Zufallskeim - dieselbe Zeile liefert immer dieselbe Zahl.

**Der Befund, der zaehlt:** die Schwellen 700/950 gelten fuer **Schlagkraft**, nicht fuer Kopfzahl.
Ein Krieger hat Schlagkraft 3, ein Katapult 45. Also sind 700 SK = **234 Krieger** und 950 SK =
**22 Katapulte**. Und genau dort passiert das Interessante: **234 Krieger + 22 Katapulte gewinnen
0 von 100 Laeufen.** Der Feueratem schlaegt VOR der Vorrunde zu (8 % = 19 Krieger), danach stehen
nur noch 215 Krieger = 645 SK gegen die Schwelle 700 - die Truppen ziehen sich zurueck, es kommt
gar nicht zum Kampf. **Wer die Schwelle nur knapp erfuellt, verliert durch den Atem.**

| Krieger | SK Fuss | Katapult | SK Belagerung | Siege | eigene Verluste (Ø) | beim Drachen (Ø) |
|---|---|---|---|---|---|---|
| 200 | 600 | 22 | 990 | 0/100 | - | - |
| 234 (Schwelle) | 702 | 22 (Schwelle) | 990 | **0/100** | - | - |
| 300 | 900 | 22 | 990 | **100/100** | 162 | 142 |
| 400 | 1200 | 22 | 990 | 100/100 | 154 | 141 |
| 700 | 2100 | 22 | 990 | 100/100 | 154 | 143 |
| 1000 | 3000 | 22 | 990 | 100/100 | 154 | 142 |

**Was die Tabelle sagt:**
- **Belagerung ist die harte Bedingung:** mit 11 Katapulten (495 SK) gewinnt KEINE Zelle, egal wie
  viele Krieger mitkommen. Ab 22 Katapulten (990 SK) gewinnt jede Zelle ab 300 Kriegern.
- **Der sichere Sieg beginnt bei 300 Kriegern und 22 Katapulten** - das ist die kleinste
  Zusammensetzung mit 100 % Siegquote.
- **Verluste sind fast unabhaengig von der Groesse der Truppe:** rund 152-162 eigene Einheiten,
  gleich ob 300 oder 1000 Krieger antreten. Mehr Truppen bringen keine geringeren Verluste, nur
  eine groessere Reserve. Bei 300 Kriegern + 22 Katapulten ist das **50 % der Truppe**.
- **Unter der Schwelle wird nicht gekaempft:** 12 von 36 Zellen liegen unter einer der beiden
  Schwellen, und keine davon hat einen Sieg. Die Vorrunde haelt also zuverlaessig.

**Gegenprobe fuer den Recherche-Vorschlag 2 (haerterer Feueratem):** mit 12 % statt 8 % kostet der
Atem 28 statt 19 Krieger (bei 234) bzw. 84 statt 56 (bei 700).

| Krieger | Katapult | Siege bei 12 % | eigene Verluste (Ø) |
|---|---|---|---|
| 234 | 22 | 0/100 | - |
| 400 | 22 | 100/100 | 155 |
| 700 | 22 | 100/100 | 154 |

**Ehrliche Deutung:** ein Atem, der durchgehend mit 12 % brennt, aendert bei den tragfaehigen
Zusammensetzungen **etwa eine Einheit** (154 -> 155). Die zweite Phase waere also vor allem
**Erzaehlung und Gefuehl**, keine Balance-Aenderung - es sei denn, sie wird deutlich haerter
angesetzt (z. B. 20 % unter halber Wache) oder sie verhindert die Vorrunde, wenn die Truppe knapp
ist. Diese Entscheidung gehoert Daniel (Frage 2), nicht der Messung.

**Grenzen dieser Messung:** nur Krieger und Katapulte (keine Paladine, keine Bogenschuetzen, keine
Forschungsboni), ein Drache (Epheus, 204 Verteidiger - die drei Drachen sind gleich stark), keine
Karren, kein Weltensprung. Die Zahlen zeigen die Richtung des Gefechts, nicht jeden Spielweg.
