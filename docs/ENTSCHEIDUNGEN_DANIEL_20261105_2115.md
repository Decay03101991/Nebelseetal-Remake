# Daniels Entscheidungen zur Uebergabe — 05.11.2026, 21:15 (woertlich, mit Folge)

Sechs Fragen aus der Uebergaberunde, alle in EINER Runde beantwortet. Wortlaut unveraendert
uebernommen; die Folge-Spalte sagt, was daraus gebaut oder gemessen wird.

| Nr | Frage | Daniels Antwort (woertlich) | Folge |
|---|---|---|---|
| 1 | Wofuer arbeitet das grosse Modell zuerst? | "Voraussetzungen im Spiel sichtbar machen (Waffentechnik 3, Schmiede, fehlende Ware) — der Punkt, den alle vier Urteile nennen" | Erster Schnitt der naechsten Sitzung: Anzeige der offenen Bedingung je Ware und je Einheit, wirkungslose Knoepfe sperren (`src/main.py:11653`, `:14213`) |
| 2 | Wie arbeitet das grosse Modell? | "Fertige Umsetzungspakete: Modell liefert Code/Patches, ich prüfe und baue ein" | Jeder Auftrag verlangt **fertige Dateien oder Patches** samt eigener Wache, nicht nur einen Entwurf; die Sitzung prueft jede Kernzahl nach und baut ein |
| 3 | Budget fuer das grosse Modell? | "noch übrig für das große deepseek model neuer stand: 4 USD stehen ab sofort als neues guthaben für das große model zur verfügung und darf gerne auch genutzt werden nur nicht verschwenden" | **4,00 USD** fuer Modellaeufe der naechsten Sitzung; je Lauf Kosten und Antwortlaenge protokollieren, leere Laeufe nicht als Ergebnis zaehlen |
| 4 | Mana bleibt in jedem Lauf bei 0 — wie weiter? | "Moment mal also Tempel liefern auch im Original bereits das mana aber natürlich müssen wir den Manabedarf erst möglichst vorausschauend mit spielentwicklung beurteilen können und daher messen. Mit diesen Werten können wir besser beurteilen wie viel Mana produktion pro std der tempel produzieren muss vorallem, da man nicht so viele von Ihnen pro karte baut, aber sehr viel mit mana springen wird, müssen einerseits kosten gesenkt andererseits Produktion erhöht werden genau wie bei allen anderen ressourcen muss man mit allen damit zusammenhängenden faktoren eine kluge mechanik bauen (die wir hoffentlich schon haben) und dann viel detailarbeit und balancing ausbauen und verfeinern" | **Erst messen, dann senken/erhoehen** — Messlage unten. Kein Wert ohne Rechnung in eine Datendatei |
| 5 | Forschungsdauer Waffentechnik 3 (~6 Spieltage)? | "Forschungsdauern/Kosten senken (Quellenlage prüfen)" | Dauern und Kosten in `data/research.json` gegen Handbuch 2009 und die 2006er Seiten pruefen, Abweichung dokumentieren, dann senken — mit Wache und erneutem Spieltest-Lauf |
| 6 | Start-Holz anheben? (frueher entschieden) | bleibt: **Originalzahl** | unveraendert |

## Messlage zum Mana (vorhandenes Zahlenmaterial, 05.11.2026, 21:15)

| Groesse | Wert | Beleg |
|---|---|---|
| Tempel-Ertrag | **5 Mana/Stunde** auf Nebelsee, **1/Stunde** auf allen anderen Gelaenden ausser Sumpf | `data/buildings.json` Eintrag `tempel` (Handbuch 2009, Daniels Entscheidung 31.10.2026: 5/1) |
| Tempel-Voraussetzung | Baukunst | ebd. |
| Ein Tempel auf Nebelsee | **120 Mana je Spieltag** (5 x 24 Spielstunden) | Rechnung aus dem Ertrag; 1 Spieltag = 24 Spielstunden, Spieluhr x180 |
| Portal-Weltwechsel | **5.000 Mana je Wechsel** | `src/portalraum.py:56` (`kosten_mana` aus den belegten Regeln) |
| Ein Weltwechsel mit EINEM Tempel | **~41,7 Spieltage** (5.000 / 120) | Rechnung |
| Drachenjagd | "drei Anlaeufe, zwei Weltensprünge je Anlauf" = **6 Wechsel = 30.000 Mana** | `data/drachen.json` (Text der Trophaeen-Beschreibung) |
| Sechs Wechsel mit EINEM Tempel | **250 Spieltage** | Rechnung |
| Paladin | **10 Mana je Einheit** | `data/units.json:142` |
| Siedlungsgruendung | **5 Mana** in den Gruendungskosten | `data/spieloekonomie.json:32` |

**Ergebnis der Messlage:** mit dem belegten Tempel-Ertrag ist EIN Weltwechsel rund 42 Spieltage
entfernt, die Drachenjagd rund 250 — die Mana-Kette ist bei x180 praktisch geschlossen. Genau das
meint Daniel mit "Kosten senken, Produktion erhoehen". Die naechste Sitzung rechnet zusaetzlich den
Bedarf je Partie (wie viele Wechsel sind fuer welche Auszeichnung noetig) und legt dann Produktion und
Preise so fest, dass die Kette erreichbar bleibt — Kennzeichnung als BELEGT (Ertrag) bzw. VORSCHLAG
(Preis), beides mit Wache.

## Was daraus NICHT folgt

- Kein neuer Mana-Wert auf Zuruf: erst die Bedarfsrechnung, dann die Zahl, dann die Wache.
- Kein Anheben des Start-Holzes (Frage 6 bleibt bei der Originalzahl).
- Kein Modelllauf ohne Paket: jeder Auftrag nennt Dateien, erwartete Zahlen und Ausgabeformat.

## Leitlinie Spielfluss (Daniel 21:25 und 21:27, woertlich)

> "Das schwierige ist ich will schon das man viel zeit ins spiel investieren muss um wirklich voll
> ausgebaut und mächtig zu sein aber es darf auch nicht zu langatmig sein und durch das springen und
> kämpfen haben wir es schneller gemacht. Jetzt will ich den spielfluss nicht zu schnell werden lassen
> mit der entwicklung"
>
> "Es muss ein Aufbauspiel bleiben"

**Was daraus folgt — vier Regeln, die jede Balancing-Aenderung binden:**

1. **Der Aufbau bleibt der Kern.** Springen (Portalwechsel) und Kaempfen sind Werkzeuge, die den
   Aufbau schneller ERREICHBAR machen duerfen, nicht Ersatz fuer ihn. Keine Aenderung darf eine Stufe
   ueberspringen, die fruehere Definition von "ausgebaut" verlangt.
2. **Zeit bis "voll ausgebaut" bleibt lang** (Groessenordnung: viele Spieltage, nicht Stunden) —
   aber ohne Leerlauf: Wartezeit muss mit einer Entscheidung gefuellt sein (bauen, forschen,
   ausbilden), sonst wird sie langatmig.
3. **Senken heisst verschieben, nicht verkürzen.** Wer Forschungsdauern oder -kosten senkt (Frage 5),
   nennt in derselben Rechnung, wo die gewonnene Zeit wieder gebunden wird (hoehere Gebaeudestufen,
   Materialbedarf, Siedlerdeckel). Sonst wird die Entwicklung insgesamt schneller als gewollt.
4. **Mana ist ein SPRUNG-Mittel, kein Aufbau-Beschleuniger.** Kosten senken und Produktion erhoehen
   (Frage 4) macht Weltwechsel erreichbar; es darf nicht dazu fuehren, dass Aufbauzeit durch Sprünge
   ersetzt wird. Die Messung nennt deshalb beide Zahlen: Mana-Bedarf je Partie UND Aufbauzeit in
   Spieltagen.

**Messpflicht fuer die naechste Sitzung:** vor jeder Balance-Aenderung eine Tabelle "Spieltage bis
Gebaeude n / Forschung n / erste Einheit / erster Weltwechsel / voll ausgebaut" aus
`tools/spieltest_simulation.py` — vorher und nachher, gleiche Saat und gleicher Stil. Eine Aenderung,
die den Aufbau insgesamt verkuerzt, ist gegen diese Leitlinie und wird Daniel vorgelegt, nicht
eingebaut.
