# Messung S-8 Stufe 3: Bauplaene je Taktik (04.11.2026)

**Wozu dieses Dokument:** S-8 Stufe 3 gibt jeder Bot-Taktik MINDESTZAHLEN und eine Regel fuer die
RESTFELDER. Die Zahlen des Entwurfs (`D:/Arbeiten/Hermes/Notizen/S8_STUFE3_BAUPLAENE_20261103.md`)
waren an drei Stellen falsch gerechnet; hier stehen die ECHTEN Werte, die Rechnung und die Messung
ueber 24 Spieltage. Grundlage fuer S-12 (alle Felder nutzen) und S-11 (Kartenwahl mit
Feldverstaendnis).

## 1. Die belegten Ertraege (gemessen an `data/buildings.json` und `gelaende.ertrag_pro_stunde`)

| Anlage | Wald | Grasland | Steppe | Berg | Huegel |
|---|---|---|---|---|---|
| Holzfäller | **4 Holz** | - | 2 Holz | - | - |
| Jäger | **2 Nahrung + 2 Leder** | - | 1 + 1 | - | - |
| Farm | - | **4 Nahrung** | **2 Nahrung** | - | - |
| Rinderfarm | - | **3 Nahrung + 3 Leder** | 1,5 + 1,5 | - | - |
| Schafszucht | - | **3 Wolle** | 1,5 Wolle | - | - |
| Pferdezucht | - | **3 Pferde** | 1,5 Pferde | - | - |
| Steinmetz | - | - | - | **4 Stein** | 2 Stein |
| Goldmine | - | - | - | **3 Gold** | 1,5 Gold |
| Erzmine | - | - | - | **3 Metall** | 1,5 Metall |
| Stellmacher | keine Ernte (Werkstatt) | - | - | - | - |

**Drei Annahmen des Entwurfs waren falsch und sind hier berichtigt:**

1. **Jäger liefern sehr wohl Ertrag:** 2 Nahrung und 2 Leder auf Wald (auf Steppe 1 + 1). Der
   Entwurf rechnete mit 0 und damit jede Taktik zu niedrig.
2. **Schafszucht und Pferdezucht geben 3** auf Grasland (1,5 auf Steppe) - der Entwurf rechnete
   mit 1,5 und damit mit der Hälfte des echten Werts.
3. **Die Farm gibt 4 auf Grasland und 2 auf Steppe** - der Entwurf kannte nur Grasland.

Die PLAENE selbst (welche Anlage, welche Mindestzahl, welches Gelaende) sind unveraendert
uebernommen; nur die Rechnung ist neu.

## 2. Die Plaene (in `data/bot_bauplan.json`, Block `anlagen_bauplaene`)

Die fünf Taktiken des SPIELS stehen in `bottaktik.TAKTIKEN` (Pluenderer, Waechterin, Bastionier,
Spaeherin, Raecher); der Entwurf nannte fuenf ABSTRACTE Taktiken (kriegerisch, haendlerisch,
defensiv, ausgleichend, geheim). Die Zuordnung ist ein **VORSCHLAG** und leitet sich aus dem
Bonus jeder Taktik ab, wie er im Code steht:

| Taktik im Spiel | Bonus im Code | Entwurf-Plan | Warum |
|---|---|---|---|
| Raecher | Angriff AT +5 % | kriegerisch (Erzmine 4) | Waffen und Ausruestung kosten Metall |
| Pluenderer | Beute +5 % | haendlerisch (Goldmine 4) | Beute wird nach Daniels Entscheid zuerst in GOLD ausgezahlt |
| Waechterin | Verteidigung +5 % | defensiv (Steinmetz 4) | Wall und Mauer kosten Stein |
| Bastionier | Ausbau +5 % | ausgleichend (ueberall 3) | baut dauerhaft, ohne Schwerpunkt |
| Spaeherin | Reisegeschwindigkeit +5 % | geheim (Pferdezucht 3) | Reisen laufen ueber Pferde |

**Mindestzahlen je Taktik** (Rueckfall fuer den Spieler-Bauplan: Stellmacher 1 in jeder Taktik):

| Anlage | Pluenderer | Waechterin | Bastionier | Spaeherin | Raecher |
|---|---|---|---|---|---|
| Holzfäller | 3 | 4 | 3 | 3 | 3 |
| Jäger | 1 | 1 | 1 | 1 | 1 |
| Farm | 2 | 3 | 2 | 2 | 2 |
| Rinderfarm | 3 | 2 | 2 | 3 | 2 |
| Schafszucht | 2 | 1 | 2 | 1 | 1 |
| Pferdezucht | 2 | 1 | 2 | 3 | 2 |
| Erzmine | 2 | 2 | 3 | 3 | 4 |
| Steinmetz | 2 | 4 | 3 | 2 | 2 |
| Goldmine | 4 | 2 | 3 | 3 | 2 |
| Stellmacher | 1 | 1 | 1 | 1 | 1 |

**Restfelder** (nach den Mindestzahlen, je Gelaende in dieser Reihenfolge, Holzfäller gedeckelt):

| Gelaende | Pluenderer | Waechterin | Bastionier | Spaeherin | Raecher |
|---|---|---|---|---|---|
| Wald | Holzfäller (max 6), dann Jäger | gleich | gleich | gleich | gleich |
| Grasland | Schafszucht, Rinderfarm | Farm, Rinderfarm | Rinderfarm, Schafszucht | Pferdezucht, Rinderfarm | Rinderfarm, Pferdezucht |
| Berg | Goldmine, Erzmine | Steinmetz, Goldmine | Goldmine, Erzmine | Goldmine, Erzmine | Erzmine, Goldmine |
| Steppe | Rinderfarm | Rinderfarm | Rinderfarm | Rinderfarm | Rinderfarm |
| Huegel | bleibt frei (Haus, Bibliothek, Lager, Schmiede, Akademie, Wall) | gleich | gleich | gleich | gleich |

## 3. Zwei Befunde, die den Plan sonst kaputt machen (gemessen, nicht vermutet)

1. **Die Feldreserve.** Haus, Bibliothek, Lager, Schmiede, Akademie, Diebesgilde, Bogenbauer und
   Wall baut der Bot ueber `bot_dorf_bauen` in DIESELBEN `dorf.bauten`. Waeren alle Felder mit
   Anlagen voll, faende er keinen Bauplatz mehr - keine Bibliothek, keine Forschung, keine Kaserne,
   keine Truppen. Darum bleibt genau so vielen Feldern frei, wie der Gebaeude-Bauplan noch braucht
   (`main.bot_bauplan_offene_bauten`, Summe aus `hoechstens` = 9). Dieselbe Lehre wie am 03.11.,
   als 99 Holzfäller die Steppe belegten und die Zuchtanlagen verschwanden.
2. **Das Bibliotheksfeld.** Eine Bibliothek darf NUR auf Grasland, Steppe oder Nebelsee stehen
   (`gelaende.bau_moeglich`). Das LETZTE solche freie Feld bleibt unangetastet, solange keine
   Bibliothek steht - sonst waere die Forschung fuer immer versperrt.

## 4. Drei Irrwege dieser Sitzung (offen benannt)

1. **Die Reihenfolge des Entwurfs macht die Erzmine zum Verlierer.** In der ersten Fassung standen
   die Mindestzahlen in der Reihenfolge der Entwurfs-Tabelle (Steinmetz, Goldmine, Erzmine). Auf
   Berg-armen Karten nahmen die beiden ersten jeden Berg, die Erzmine bekam keinen - die Wache
   `test_bot_warenkette` meldete Goldmine 1 statt 4 auf `original-118b` (5 Bergfelder fuer 8
   Anlagen). Seit S-8 Stufe 1 ist belegt, dass ohne Erzmine kein Karren (80 Metall) und keine
   Gruendung zustande kommt; die Erzmine steht deshalb in der Datendatei VOR Steinmetz und
   Goldmine.
2. **Phase A in Runden statt in Bloecken.** Vorher setzte ein Gebaeude seine ganze Zahl auf einmal
   und nahm damit alle Felder seiner Gelaendeart. Jetzt setzt jedes Gebaeude je Runde eine Anlage -
   so bekommen alle, die Berg brauchen, ihren Anteil.
3. **Ein Textskript hat die Erzmine in den NÄCHSTEN Block geschoben** (der Anker traf die erste
   Fundstelle der ganzen Datei, nicht die des Blocks). Das JSON blieb syntaktisch gueltig, weil ein
   doppelter Schluessel still den letzten Wert nimmt - die Messung zeigte dann Haug mit 0 Erzmine
   und nur 3 Doerfern. Aufgefallen ist es nur, weil die Zahl unmoeglich war; Datei aus der
   Sicherung zurueckgeholt und das Skript blockweise neu gebaut.

## 5. Die Messung: 24 Spieltage, echte Bot-Takte

Werkzeug: `python -X utf8 tools/bot_wirtschaft_messung.py --tage 24 --aus <datei>` (144 Bot-Takte,
je 6 Spielstunden). Rohe Zahlen: `s8s3_final.json` im Scratch-Ordner der Sitzung.

| Bot (Taktik) | Doerfer | Anlagen je Dorf | Erzminen | Goldminen | Steinmetze | Metall/h | Kasse Metall | Kasse Gold |
|---|---|---|---|---|---|---|---|---|
| Haug (Pluenderer) | 4 | 76 / 76 / 76 / 52 | 8 | 17 | 8 | 24,0 | 13.210 | 26.493 |
| Brynhild (Waechterin) | 4 | 97 / 81 / 85 / 55 | 8 | 8 | 21 | 24,0 | 12.172 | 10.892 |
| Grom (Bastionier) | 4 | 77 / 76 / 91 / 83 | 11 | 31 | 11 | 31,5 | 16.780 | 42.703 |
| Silra (Spaeherin) | 4 | 84 / 84 / 78 / 56 | 12 | 38 | 8 | 36,0 | 16.392 | 54.951 |
| Krank (Raecher) | 4 | 85 / 64 / 91 / 76 | **39** | 8 | 8 | **111,0** | **55.832** | 11.350 |

**Gegen den Stand vor dem Schnitt (S-8 Stufe 2, 03.11.2026):**

| Groesse | vorher | jetzt | Beleg |
|---|---|---|---|
| Doerfer je Bot nach 24 Tagen | 4/4/4/4/4 | **4/4/4/4/4** | `dorfspur` in beiden Messdateien |
| Anlagen je Dorf | 26 bis 30 | **52 bis 97** | Anlagenzahl je Dorf |
| Stundenertrag je Dorf | ausgeglichen (gleiche Anlagen) | **nach Taktik verschieden** | Spalte Erzminen/Goldminen/Steinmetze |
| Metall in der Kasse | 11.435 bis 16.584 | **12.172 bis 55.832** | Kasse je Bot |
| Kasse Leder/Nahrung | am Deckel | weiter am Deckel (20.000 / je Dorf) | `hoechstvorrat_je_stoff` |

**Was die Messung zeigt:** jede Taktik baut nachweislich anders (Raecher 39 Erzminen gegen 8
Goldminen, Spaeherin 31 Pferdezuchten, Waechterin 21 Steinmetze), die Karten sind deutlich voller,
und KEIN Bot verliert eine Gruendung - die Zahl der Doerfer bleibt bei 4 je Bot, wie vor dem
Schnitt. Der Raecher haeufte 55.832 Metall an, weil Metall nach dem Bau der Karren keinen Abnehmer
mehr hat: das ist der naechste Engpass nach dem Bauplan (S-11/S-12 und die Ausruestung).

## 6. Was noch NICHT gebaut ist

- **S-12 (alle Felder nutzen):** Huegel bleibt nach dem Entwurf fuer die ertraglosen Gebaeude frei,
  und Sumpf/Nebelsee tragen keine Anlage. Die Pruefzusage von S-12 (jedes Feld, das die Taktik
  sinnvoll fuellt) ist damit noch offen.
- **S-11 (Kartenwahl mit Feldverstaendnis):** die Kartenwahl nutzt die Mindestzahlen noch nicht als
  Engpass-Information.
- **Die Zuordnung Taktik zu Entwurf-Plan** ist ein VORSCHLAG und wartet auf Daniels Wort.
