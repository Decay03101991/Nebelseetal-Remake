# Original-Werte der 28 Einheiten

Spaltensicher ausgelesen aus `docs/original/Nebelseetal_Spielanleitung_2009.pdf`
(Tabelle 'Einheitentabelle', Handbuch S. 16, und 'Karren und Belagerungswaffen',
Handbuch S. 17/18) mit `tools/pdf_stats.py` ueber Wort-Koordinaten.

Werte woertlich aus der Vorlage. `-` in der Druckvorlage (nicht relevant) und die
in der Karren-/Belagerungstabelle **fehlende Spalte MU** werden als `null` gefuehrt;
es wurde **nichts geschaetzt oder aufgefuellt**.

## Wertetabelle

| # | Einheit | Typ | LE | AT | PA | SI | HE | RS | TP | GS | MU | SK |
|---:|---|---|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|
| 1 | Bürgerwehr | Kampfeinheit Nahkampf (Kriegerakademie) | 15 | 20 | 20 | 10 | 10 | 0 | 1-6 | 5 | 40 | 1 |
| 2 | Kämpfer | Kampfeinheit Nahkampf (Kriegerakademie) | 20 | 40 | 25 | 10 | 15 | 1 | 2-8 | 10 | 75 | 2 |
| 3 | Krieger | Kampfeinheit Nahkampf (Kriegerakademie) | 30 | 50 | 40 | 15 | 15 | 2 | 3-10 | 25 | 85 | 3 |
| 4 | Ritter | Kampfeinheit Nahkampf (Kriegerakademie) | 35 | 70 | 50 | 15 | 5 | 4 | 4-15 | 20 | 95 | 4 |
| 5 | Paladin | Kampfeinheit Nahkampf (Kriegerakademie) | 50 | 85 | 60 | 20 | 0 | 6 | 6-20 | 20 | 100 | 5 |
| 6 | Kurzbogenschütze | Kampfeinheit Fernkampf (Kriegerakademie) | 15 | 40 | 0 | 10 | 10 | 0 | 1-6 | 5 | 60 | 1 |
| 7 | Bogenschütze | Kampfeinheit Fernkampf (Kriegerakademie) | 15 | 50 | 0 | 10 | 10 | 0 | 1-8 | 5 | 60 | 2 |
| 8 | Langbogenschütze | Kampfeinheit Fernkampf (Kriegerakademie) | 20 | 60 | 0 | 10 | 10 | 0 | 1-10 | 5 | 60 | 4 |
| 9 | Armbrustschütze | Kampfeinheit Fernkampf (Kriegerakademie) | 20 | 60 | 0 | 10 | 10 | 1 | 2-12 | 5 | 60 | 5 |
| 10 | Streuner | Kundschafter (Diebesgilde) | 10 | 10 | 15 | 30 | 30 | 0 | 1-4 | 10 | 60 | 2 |
| 11 | Gauner | Kundschafter (Diebesgilde) | 15 | 30 | 20 | 50 | 45 | 0 | 1-6 | 15 | 65 | 3 |
| 12 | Dieb | Kundschafter (Diebesgilde) | 15 | 40 | 40 | 65 | 70 | 0 | 2-7 | 20 | 70 | 5 |
| 13 | Meisterdieb | Kundschafter (Diebesgilde) | 20 | 40 | 45 | 70 | 80 | 0 | 3-8 | 25 | 80 | 7 |
| 14 | Kundschafter | Kundschafter (Diebesgilde) | 25 | 50 | 60 | 85 | 90 | 1 | 2-9 | 30 | 90 | 9 |
| 15 | Waldläufer | Kundschafter (Diebesgilde) | 30 | 60 | 65 | 90 | 95 | 2 | 3-10 | 35 | 100 | 11 |
| 16 | Handkarren | Karren (Stellmacher) | null | null | null | null | null | null | - | 10 | null | 0 |
| 17 | Einspänner | Karren (Stellmacher) | null | null | null | null | null | null | - | 25 | null | 0 |
| 18 | Zweispänner | Karren (Stellmacher) | null | null | null | null | null | null | - | 30 | null | 0 |
| 19 | Handelskarawane | Karren (Stellmacher) | null | null | null | null | null | null | - | 25 | null | 0 |
| 20 | Große Handelskarawane | Karren (Stellmacher) | null | null | null | null | null | null | - | 30 | null | 0 |
| 21 | Siedlerkarren | Karren (Stellmacher) | null | null | null | null | null | null | - | 20 | null | 0 |
| 22 | Belagerungsturm | Belagerungswaffe (Stellmacher) | null | null | null | null | null | null | 0 | 15 | null | 35 |
| 23 | Ramme | Belagerungswaffe (Stellmacher) | null | null | null | null | null | null | 0-4 | 15 | null | 25 |
| 24 | Großer Belagerungsturm | Belagerungswaffe (Stellmacher) | null | null | null | null | null | null | 0 | 15 | null | 45 |
| 25 | Große Ramme | Belagerungswaffe (Stellmacher) | null | null | null | null | null | null | 0-8 | 15 | null | 35 |
| 26 | Balliste | Belagerungswaffe (Stellmacher) | null | null | null | null | null | null | 1-10 | 15 | null | 25 |
| 27 | Katapult | Belagerungswaffe (Stellmacher) | null | null | null | null | null | null | 2-13 | 15 | null | 45 |
| 28 | Großes Katapult | Belagerungswaffe (Stellmacher) | null | null | null | null | null | null | 5-18 | 15 | null | 55 |

**28 Einheiten** (erwartet 28). Davon mit **allen 11 Werten vollstaendig: 15** (die 15 Armee-/Kundschaftereinheiten). Die 6 Karren und 7 Belagerungswaffen haben in der Vorlage keine Angaben zu LE/AT/PA/SI/HE/RS/TP bzw. MU (siehe unten).

## Nicht sicher zuzuordnen

**Ergebnis der Pruefung: spaltenweise ist kein Wert mehrdeutig.** Der urspruengliche
Fehler kam allein daher, dass die Tabelle *Karren und Belagerungswaffen* nur
**9 Wertspalten** besitzt (LE AT PA SI HE RS TP GS SK) -- die Spalte **MU fehlt**
dort. Dadurch haben diese Zeilen 9 statt 10 Werte und verrutschen bei reiner
Textreihenfolge. Ueber die x-Koordinaten ist die Zuordnung eindeutig, wie die
Rohzeilen (Wert + x-Ursprung) zeigen:

- PDF-S.16 **Bürgerwehr**: 15@303  20@327  20@351  10@376  10@400  0@426  1-6@446  5@474  40@496  1@523
- PDF-S.16 **Kämpfer**: 20@303  40@327  25@351  10@376  15@400  1@426  2-8@446  10@472  75@496  2@523
- PDF-S.16 **Krieger**: 30@303  50@327  40@351  15@376  15@400  2@426  3-10@444  25@472  85@496  3@523
- PDF-S.16 **Ritter**: 35@303  70@327  50@351  15@376  5@402  4@426  4-15@444  20@472  95@496  4@523
- PDF-S.16 **Paladin**: 50@303  85@327  60@351  20@376  0@402  6@426  6-20@444  20@472  100@494  5@523
- PDF-S.16 **Kurzbogenschütze**: 15@303  40@327  0@354  10@376  10@400  0@426  1-6@446  5@474  60@496  1@523
- PDF-S.16 **Bogenschütze**: 15@303  50@327  0@354  10@376  10@400  0@426  1-8@446  5@474  60@496  2@523
- PDF-S.16 **Langbogenschütze**: 20@303  60@327  0@354  10@376  10@400  0@426  1-10@444  5@474  60@496  4@523
- PDF-S.16 **Armbrustschütze**: 20@303  60@327  0@354  10@376  10@400  1@426  2-12@444  5@474  60@496  5@523
- PDF-S.16 **Streuner**: 10@303  10@327  15@351  30@376  30@400  0@426  1-4@446  10@472  60@496  2@523
- PDF-S.16 **Gauner**: 15@303  30@327  20@351  50@376  45@400  0@426  1-6@446  15@472  65@496  3@523
- PDF-S.16 **Dieb**: 15@303  40@327  40@351  65@376  70@400  0@426  2-7@446  20@472  70@496  5@523
- PDF-S.16 **Meisterdieb**: 20@303  40@327  45@351  70@376  80@400  0@426  3-8@446  25@472  80@496  7@523
- PDF-S.17 **Kundschafter**: 25@303  50@327  60@351  85@376  90@400  1@426  2-9@446  30@472  90@496  9@523
- PDF-S.17 **Waldläufer**: 30@303  60@327  65@351  90@376  95@400  2@426  3-10@444  35@472  100@494  11@521
- PDF-S.17 **Handkarren**: -@316  -@342  -@368  -@394  -@419  -@445  -@471  10@494  0@523
- PDF-S.17 **Einspänner**: -@316  -@342  -@368  -@394  -@419  -@445  -@471  25@494  0@523
- PDF-S.17 **Zweispänner**: -@316  -@342  -@368  -@394  -@419  -@445  -@471  30@494  0@523
- PDF-S.17 **Handelskarawane**: -@316  -@342  -@368  -@394  -@419  -@445  -@471  25@494  0@523
- PDF-S.17 **Große Handelskarawane**: -@316  -@342  -@368  -@394  -@419  -@445  -@471  30@494  0@523
- PDF-S.17 **Siedlerkarren**: -@316  -@342  -@368  -@394  -@419  -@445  -@471  20@494  0@523
- PDF-S.17 **Belagerungsturm**: -@316  -@342  -@368  -@394  -@419  -@445  0@471  15@494  35@520
- PDF-S.17 **Ramme**: -@316  -@342  -@368  -@394  -@419  -@445  0-4@467  15@494  25@520
- PDF-S.17 **Großer Belagerungsturm**: -@316  -@342  -@368  -@394  -@419  -@445  0@471  15@494  45@520
- PDF-S.18 **Große Ramme**: -@316  -@342  -@368  -@394  -@419  -@445  0-8@467  15@494  35@520
- PDF-S.18 **Balliste**: -@316  -@342  -@368  -@394  -@419  -@445  1-10@465  15@494  25@520
- PDF-S.18 **Katapult**: -@316  -@342  -@368  -@394  -@419  -@445  2-13@465  15@494  45@520
- PDF-S.18 **Großes Katapult**: -@316  -@342  -@368  -@394  -@419  -@445  5-18@465  15@494  55@520

Ungeklaerte Einzelpunkte (bewusst so belassen, nicht geraten):

- **TP = `0`** bei *Belagerungsturm* und *Großer Belagerungsturm*: die Vorlage druckt
  eine `0`, nicht `-`. Als Bereich **0-0** uebernommen. Ob damit 'kein Schaden' oder
  'kein Wert' gemeint ist, laesst sich aus der Tabelle nicht entscheiden.
- **MU** fehlt in der gesamten Karren-/Belagerungstabelle -> fuer alle 13 Einheiten
  `null`. Es ist nicht auszuschliessen, dass MU dort nur nicht abgedruckt wurde.
- Die Spalten **LE AT PA SI HE RS** sind bei Karren und Belagerungswaffen in jeder Zeile
  mit `-` belegt (Handbuch: 'nicht relevant, da fuer diese Auftraege ohne Bedeutung').

