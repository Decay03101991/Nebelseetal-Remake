# Messung S-8 Stufe 1: Ertrag aus den gebauten Anlagen (03.11.2026, 21:1x)

**Anlass.** Bis heute rechnete ein Bot-Dorf seinen Ertrag aus dem Kartenprofil - also aus den FELDERN
der Karte, ohne dass dort etwas stehen musste. Gemessen war: ein Dorf mit 48 Holzfällern erntete genau
so viel wie eines mit 5. Diese Messung zeigt, was der Umbau auf den Ertrag aus den Anlagen aendert -
alle Zahlen NEU gemessen, keine aus einer Vorsitzung uebernommen.

**Werkzeug.** `tools/bot_wirtschaft_messung.py` (neu): faehrt eine echte Partie (frische App,
`GameState.bots_fortschreiben` im 6-Stunden-Takt, 24 Spieltage), misst je Bot Dorfzahl, Kasse, je Dorf
Karte, Anlagen, Stundenertrag, Vorraete, Siedlerkarren und Siedler. `--weg karte|anlagen|felder`
ueberschreibt den Ertragsweg, ohne die Datendatei anzufassen - so laufen beide Fassungen unter SONST
gleichen Bedingungen (gleiche Saat, gleicher Start).

Aufruf: `python -X utf8 tools/bot_wirtschaft_messung.py --tage 24 --aus <datei>`

## 1. Dorfzahl nach 24 Spieltagen (Daniels Ziel: vier Doerfer je Bot)

| Bot | vorher (Kartenprofil) | nachher (Anlagen) | Gruendungstag nachher |
|---|---|---|---|
| Haug | 4 | **4** | Tag 3 |
| Brynhild | 4 | **4** | Tag 9 |
| Grom | 4 | **4** | Tag 6 |
| Silra | **2** | **4** | Tage 3 / 6 / 9 |
| Krank | 4 | **4** | Tag 7 |
| Summe | 18 | **20** | - |

Der Vorlauf `--weg karte` nach dem Umbau liefert EXAKT die Zahlen des Laufs vor dem Umbau (Kassen
29.544 / 14.136 / 15.847 / 471 / 23.097 Holz) - der Schalter trennt also wirklich nur den Ertragsweg.

## 2. Stundenertrag des ersten Dorfes (aus dem Spiel, nicht gerechnet)

| Bot | vorher: Holz / Stein / Nahrung / Gold | nachher: Holz / Stein / Nahrung / Gold |
|---|---|---|
| Haug | 22,26 / 1,90 / 11,90 / 1,50 | 22,05 / **12,35** / **21,60** / **6,00** |
| Brynhild | 18,48 / 3,80 / 28,00 / 3,00 | 22,05 / **12,35** / 24,60 / **6,00** |
| Grom | 13,30 / 3,78 / 20,30 / 2,70 | 19,95 / **13,65** / 24,60 / **9,00** |
| Silra | 13,60 / 8,80 / 21,00 / 6,60 | 21,00 / 13,00 / 22,20 / **9,00** |
| Krank | 14,60 / 9,20 / 17,85 / 6,90 | 21,00 / 13,00 / 24,60 / **9,00** |

**Der Gesamtertrag steigt nicht einfach, er wird AUSGEGLICHEN.** Das Kartenprofil gab je nach Karte
fast nur einen Rohstoff (Haug: 22,26 Holz, aber 1,90 Stein und 1,50 Gold); die Anlagen liefern, was
wirklich gebaut ist. Genau das braucht die Wirtschaft: ohne Stein und Metall gibt es keine Mauer und
keinen Siedlerkarren (der Karren kostet 80 Metall).

## 3. Holzvorrat Silra (der Fall aus der Uebergabe: kam nie ueber 190 Holz)

| Spieltag | vorher (Hauptdorf) | nachher (Hauptdorf) |
|---|---|---|
| 22 | 98,49 | 6.602,00 |
| 23 | 24,89 | 7.106,00 |
| 24 | 151,29 | 7.610,00 |

Kasse aller Doerfer am Ende: **471 Holz** vorher gegen **34.136 Holz** nachher.

## 4. Was den Umbau erst wirksam gemacht hat (jedes Stueck gemessen)

| Befund | Wirkung |
|---|---|
| Der Erzmine fehlte im Bauplan | Mit dem Ertrag aus den Anlagen erntete KEIN Bot-Dorf Metall mehr (14 bis 36 im Lager, vorher kam es aus dem Kartenprofil). Ein Siedlerkarren kostet 80 Metall - also wurde kein Karren gebaut und **kein Bot gruendete** (Dorfzahl fiel von 4/4/4/2/4 auf 3/3/3/2/3). Behoben: eine Erzmine in `data/bot_wirtschaft.json` (VORSCHLAG fuer die Zahl 1, 3 Metall/h auf Berg) |
| `bot_karren_bauen` buchte VOR der Pruefung | Ein Dorf, das schon einen Karren hatte, verlor bei jedem Aufruf 200 Holz (Buchung, dann Ablehnung). Reihenfolge korrigiert; Wache: ein zweiter Karren kostet nichts mehr |
| Die Gruendung nahm das REICHSTE Dorf als Quelle | Stand dort kein Karren, wurde abgelehnt - auch wenn zwei andere Doerfer einen hatten (Grom blieb bei drei Doerfern). Jetzt kommen nur Doerfer MIT Karren als Quelle in Frage |

Nach diesen drei Korrekturen erreicht **jeder Bot vier Doerfer**.

## 5. Grenzen dieser Messung

- Eine Saat (`random.seed(7)`) und ein Startzustand: die Zahlen sind reproduzierbar, aber nicht der
  Durchschnitt vieler Partien.
- Gemessen wurde der Bot-Takt, nicht der Spieler. Der Spieler rechnet dieselbe Kernfunktion
  (`wirtschaft.ertrag_gesamt`) - Gleichheit ist durch die Wache `test_s8_ertrag_aus_anlagen`
  Abschnitt 1 belegt (Handrechnung ueber die Felder), nicht durch diese Messung.
- Der alte Weg bleibt als Schalter `ertrag_weg: karte` erhalten; ein Vergleich ist also jederzeit
  ohne Codeaenderung wiederholbar.
