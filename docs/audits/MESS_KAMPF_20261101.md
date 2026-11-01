# Messbericht Kampf — Wall, Schlagkraft, Beute, Ladung, Reisekosten

## A. Kopf

| Punkt | Wert |
|---|---|
| Datum | 01.11.2026 (Systemzeit 21:05 MEZ) |
| Kopf-Commit | a3fd069 („B1 des starken Modells …“) — der Auftrag nennt als Ist-Zustand 52604ea; gemessen wurde am aktuellen Stand, in dem B1 bereits abgeschlossen ist |
| Angelegte Dateien | tools/mess_kampf.py (Werkzeug), docs/audits/MESS_KAMPF_20261101.md (dieser Bericht) |
| Aufruf | python -X utf8 tools/mess_kampf.py → Rückgabewert 0 |
| Sammellauf | python -X utf8 -u tools/sammellauf.py (Pflicht, Ergebnis in Abschnitt B) |
| Unteragenten | 0 — alle Messungen direkt ausgeführt, keine Delegation (Maschine schwach, keine parallelen Schwerläufe) |

Geändert wurde keine weitere Datei. Es wurde nichts gelöscht, nichts committet, nichts gepusht.
Gelesen wurde nur. Das Werkzeug nutzt ausschließlich die vorhandenen Funktionen
`kampf.fuehre_schlacht`, `kampfbericht.vorrunde` / `beute_staffel` / `beute_am_ziel`,
`einheiten.schlagkraft` / `angriff` / `ladung_der_gruppe` und `auftraege.kosten_der_mission`
sowie die Daten `data/units.json`, `data/karrenkapazitaet.json`, `data/buildings.json`.

Messaufstellung (fest, im Werkzeug hart codiert, Seed 20261101, 40 Läufe je Wallstufe):

- Angreifer: Krieger 200 (Fuss-SK 600) + Bogenschütze 30 + Katapult 16 (Belagerungs-SK 720)
- Verteidiger: Krieger 100 + Bogenschütze 20
- Zufall: `random.Random(20261101 + i)` je Lauf i = 0 … 39

## B. Die gedruckten Zeilen (vollständige Werkzeugausgabe)

```
KOPF.WERKZEUG | tools/mess_kampf.py (Auftrag B2) | docs/auftraege/B2_paket_20261101.md
KOPF.DATUM | 2026-11-01 21:05 | Systemzeit
KOPF.SEED | 20261101 | random.Random(seed + i), i = 0..39
AUFSTELLUNG.ANGREIFER | Krieger 200 (Fuss-SK 600) + Bogenschuetze 30 + Katapult 16 (Belagerungs-SK 720) | einheiten.schlagkraft
AUFSTELLUNG.VERTEIDIGER | Krieger 100 + Bogenschuetze 20 | einheiten.schlagkraft
WALL.LEGENDE | vorrunde siege verluste_angreifer(min/med/max) verluste_verteidiger(min/med/max) treffer_med | fuehre_schlacht, seed 20261101
WALL.0 | vorrunde=40/40 siege=40/40 va=42/59/72 vv=84/90/102 treffer=15 | fuehre_schlacht, seed 20261101
WALL.1 | vorrunde=40/40 siege=40/40 va=42/60/77 vv=82/90/99 treffer=27 | fuehre_schlacht, seed 20261101
WALL.2 | vorrunde=40/40 siege=40/40 va=39/60/74 vv=80/91/101 treffer=35 | fuehre_schlacht, seed 20261101
WALL.3 | vorrunde=40/40 siege=40/40 va=42/61/82 vv=80/89/100 treffer=42 | fuehre_schlacht, seed 20261101
WALL.4 | vorrunde=40/40 siege=40/40 va=41/61/78 vv=77/91/104 treffer=44 | fuehre_schlacht, seed 20261101
WALL.5 | vorrunde=40/40 siege=40/40 va=46/60/81 vv=80/89/99 treffer=46 | fuehre_schlacht, seed 20261101
WALL.6 | vorrunde=40/40 siege=40/40 va=52/66/81 vv=78/92/100 treffer=42 | fuehre_schlacht, seed 20261101
WALL.7 | vorrunde=40/40 siege=40/40 va=44/64/82 vv=80/91/98 treffer=48 | fuehre_schlacht, seed 20261101
WALL.8 | vorrunde=0/40 siege=0/40 va=0/0/0 vv=0/0/0 treffer=0 | fuehre_schlacht, seed 20261101
WALL.9 | vorrunde=0/40 siege=0/40 va=0/0/0 vv=0/0/0 treffer=0 | fuehre_schlacht, seed 20261101
WALL.10 | vorrunde=0/40 siege=0/40 va=0/0/0 vv=0/0/0 treffer=0 | fuehre_schlacht, seed 20261101
TREFFERCHANCE.LEGENDE | chance_bogenschuetze_angreifer_in_prozent | fern/100 - 0.05*stufe*zustand/100 (VORSCHLAG mauerabzug)
TREFFERCHANCE.0 | 30 | fern/100 - 0.05*stufe*zustand/100 (VORSCHLAG mauerabzug)
TREFFERCHANCE.1 | 25 | fern/100 - 0.05*stufe*zustand/100 (VORSCHLAG mauerabzug)
TREFFERCHANCE.2 | 20 | fern/100 - 0.05*stufe*zustand/100 (VORSCHLAG mauerabzug)
TREFFERCHANCE.3 | 15 | fern/100 - 0.05*stufe*zustand/100 (VORSCHLAG mauerabzug)
TREFFERCHANCE.4 | 10 | fern/100 - 0.05*stufe*zustand/100 (VORSCHLAG mauerabzug)
TREFFERCHANCE.5 | 5 | fern/100 - 0.05*stufe*zustand/100 (VORSCHLAG mauerabzug)
TREFFERCHANCE.6 | 0 | fern/100 - 0.05*stufe*zustand/100 (VORSCHLAG mauerabzug)
TREFFERCHANCE.7 | 0 | fern/100 - 0.05*stufe*zustand/100 (VORSCHLAG mauerabzug)
TREFFERCHANCE.8 | 0 | fern/100 - 0.05*stufe*zustand/100 (VORSCHLAG mauerabzug)
TREFFERCHANCE.9 | 0 | fern/100 - 0.05*stufe*zustand/100 (VORSCHLAG mauerabzug)
TREFFERCHANCE.10 | 0 | fern/100 - 0.05*stufe*zustand/100 (VORSCHLAG mauerabzug)
SCHWELLE.LEGENDE | fuss belagerung pass_ab fail_bis abgleich_spieldaten | kampfbericht.vorrunde vs gebaeude_wirkung.wall_schwelle
SCHWELLE.1 | fuss=10 bel=- pass_ab=ja fail_bis=nein abgleich_spieldaten=ja | kampfbericht.vorrunde vs gebaeude_wirkung.wall_schwelle
SCHWELLE.2 | fuss=40 bel=- pass_ab=ja fail_bis=nein abgleich_spieldaten=ja | kampfbericht.vorrunde vs gebaeude_wirkung.wall_schwelle
SCHWELLE.3 | fuss=90 bel=- pass_ab=ja fail_bis=nein abgleich_spieldaten=ja | kampfbericht.vorrunde vs gebaeude_wirkung.wall_schwelle
SCHWELLE.4 | fuss=160 bel=- pass_ab=ja fail_bis=nein abgleich_spieldaten=ja | kampfbericht.vorrunde vs gebaeude_wirkung.wall_schwelle
SCHWELLE.5 | fuss=250 bel=500 pass_ab=ja fail_bis=nein abgleich_spieldaten=ja | kampfbericht.vorrunde vs gebaeude_wirkung.wall_schwelle
SCHWELLE.6 | fuss=360 bel=600 pass_ab=ja fail_bis=nein abgleich_spieldaten=ja | kampfbericht.vorrunde vs gebaeude_wirkung.wall_schwelle
SCHWELLE.7 | fuss=490 bel=700 pass_ab=ja fail_bis=nein abgleich_spieldaten=ja | kampfbericht.vorrunde vs gebaeude_wirkung.wall_schwelle
SCHWELLE.8 | fuss=640 bel=800 pass_ab=ja fail_bis=nein abgleich_spieldaten=ja | kampfbericht.vorrunde vs gebaeude_wirkung.wall_schwelle
SCHWELLE.9 | fuss=810 bel=900 pass_ab=ja fail_bis=nein abgleich_spieldaten=ja | kampfbericht.vorrunde vs gebaeude_wirkung.wall_schwelle
SCHWELLE.10 | fuss=1000 bel=1000 pass_ab=ja fail_bis=nein abgleich_spieldaten=ja | kampfbericht.vorrunde vs gebaeude_wirkung.wall_schwelle
BEUTE.LEGENDE | staffel anteil% handkarren40_klein handkarren40_gross zweispaenner250_klein zweispaenner250_gross | kampfbericht.beute_staffel
BEUTE.keine_verteidiger | anteil=100% hand40_klein=40 hand40_gross=40 zweisp250_klein=250 zweisp250_gross=250 | kampfbericht.beute_staffel
BEUTE.mauer_gebrochen | anteil=60% hand40_klein=40 hand40_gross=40 zweisp250_klein=180 zweisp250_gross=250 | kampfbericht.beute_staffel
BEUTE.mauer_beschaedigt | anteil=30% hand40_klein=40 hand40_gross=40 zweisp250_klein=90 zweisp250_gross=250 | kampfbericht.beute_staffel
BEUTE.mauer_heil | anteil=10% hand40_klein=30 hand40_gross=40 zweisp250_klein=30 zweisp250_gross=250 | kampfbericht.beute_staffel
BEUTE.ABBUCHUNG | genommen=30 rest_summe=270 negativ=False | kampfbericht.beute_am_ziel (Wall heil, 1 Verteidiger, Handkarren)
LADUNG.BASIS | handkarren=40 einspaenner=100 zweispaenner=250 handelskarawane=1000 grossehandelskarawane=2500 | einheiten.ladung (data/units.json)
LADUNG.WAGENBAU0 | handkarren=40 einspaenner=100 zweispaenner=250 handelskarawane=1000 grossehandelskarawane=2500 | einheiten.ladung_der_gruppe (Faktor 1.0)
LADUNG.WAGENBAU1 | handkarren=44 einspaenner=110 zweispaenner=275 handelskarawane=1100 grossehandelskarawane=2750 | einheiten.ladung_der_gruppe (Faktor 1.1)
LADUNG.WAGENBAU5 | handkarren=60 einspaenner=150 zweispaenner=375 handelskarawane=1500 grossehandelskarawane=3750 | einheiten.ladung_der_gruppe (Faktor 1.5)
LADUNG.WAGENBAU10 | handkarren=80 einspaenner=200 zweispaenner=500 handelskarawane=2000 grossehandelskarawane=5000 | einheiten.ladung_der_gruppe (Faktor 2.0)
LADUNG.WAGENBAU11 | handkarren=80 einspaenner=200 zweispaenner=500 handelskarawane=2000 grossehandelskarawane=5000 | einheiten.ladung_der_gruppe (Faktor 2.0)
LADUNG.WAGENBAU15 | handkarren=80 einspaenner=200 zweispaenner=500 handelskarawane=2000 grossehandelskarawane=5000 | einheiten.ladung_der_gruppe (Faktor 2.0)
REISEKOSTEN.LEGENDE | einheiten entfernung gold nahrung mana reisezeit_h | auftraege.kosten_der_mission (Saetze VORSCHLAG)
REISE.10.1 | einheiten=10 gold=25.00 nahrung=0.04 mana=5.50 reisezeit=0.08 | auftraege.kosten_der_mission (VORSCHLAG)
REISE.10.5 | einheiten=10 gold=125.00 nahrung=0.20 mana=7.50 reisezeit=0.40 | auftraege.kosten_der_mission (VORSCHLAG)
REISE.10.20 | einheiten=10 gold=500.00 nahrung=0.80 mana=15.00 reisezeit=1.60 | auftraege.kosten_der_mission (VORSCHLAG)
REISE.40.1 | einheiten=40 gold=100.00 nahrung=0.16 mana=5.50 reisezeit=0.08 | auftraege.kosten_der_mission (VORSCHLAG)
REISE.40.5 | einheiten=40 gold=500.00 nahrung=0.80 mana=7.50 reisezeit=0.40 | auftraege.kosten_der_mission (VORSCHLAG)
REISE.40.20 | einheiten=40 gold=2000.00 nahrung=3.20 mana=15.00 reisezeit=1.60 | auftraege.kosten_der_mission (VORSCHLAG)
REISE.100.1 | einheiten=100 gold=250.00 nahrung=0.40 mana=5.50 reisezeit=0.08 | auftraege.kosten_der_mission (VORSCHLAG)
REISE.100.5 | einheiten=100 gold=1250.00 nahrung=2.00 mana=7.50 reisezeit=0.40 | auftraege.kosten_der_mission (VORSCHLAG)
REISE.100.20 | einheiten=100 gold=5000.00 nahrung=8.00 mana=15.00 reisezeit=1.60 | auftraege.kosten_der_mission (VORSCHLAG)
GEGENPROBE.LEGENDE | stufe fuss_schwelle AT_Krieger_noetig SK_Krieger_noetig | E.angriff=50 vs E.schlagkraft=3 (Register 54)
GEGENPROBE.1 | fuss=10 AT_Krieger=1 SK_Krieger=4 | E.angriff=50 vs E.schlagkraft=3
GEGENPROBE.2 | fuss=40 AT_Krieger=1 SK_Krieger=14 | E.angriff=50 vs E.schlagkraft=3
GEGENPROBE.3 | fuss=90 AT_Krieger=2 SK_Krieger=30 | E.angriff=50 vs E.schlagkraft=3
GEGENPROBE.4 | fuss=160 AT_Krieger=4 SK_Krieger=54 | E.angriff=50 vs E.schlagkraft=3
GEGENPROBE.5 | fuss=250 AT_Krieger=5 SK_Krieger=84 | E.angriff=50 vs E.schlagkraft=3
GEGENPROBE.6 | fuss=360 AT_Krieger=8 SK_Krieger=120 | E.angriff=50 vs E.schlagkraft=3
GEGENPROBE.7 | fuss=490 AT_Krieger=10 SK_Krieger=164 | E.angriff=50 vs E.schlagkraft=3
GEGENPROBE.8 | fuss=640 AT_Krieger=13 SK_Krieger=214 | E.angriff=50 vs E.schlagkraft=3
GEGENPROBE.9 | fuss=810 AT_Krieger=17 SK_Krieger=270 | E.angriff=50 vs E.schlagkraft=3
GEGENPROBE.10 | fuss=1000 AT_Krieger=20 SK_Krieger=334 | E.angriff=50 vs E.schlagkraft=3
GEGENPROBE.BEISPIEL | 1_Krieger_wall1 AT_besteht=ja SK_besteht=nein | AT wuerde faelschlich bestehen, SK lehnt ab (Register 54 behoben)
```

Sammellauf (Pflicht): 117 Dateien, 114 gruen, 1 rot, 2 ausgesetzt, 636 s; zusammen 4355 bestandene Pruefungen, 1 Fehler, 38 Befunde (ROT: test_textqualitaet.py, ohne ERGEBNIS-Zeile, RC 1).

## C. Wallstufen 0–10 (40 Läufe je Stufe, Streuung)

Messaufstellung: Angreifer Krieger 200 + Bogenschütze 30 + Katapult 16, Verteidiger Krieger 100 + Bogenschütze 20.

| Stufe | Vorrunde (x/40) | Siege (x/40) | Verluste Angreifer Min/Med/Max | Verluste Verteidiger Min/Med/Max | Treffer (Median) |
|---|---|---|---|---|---|
| 0 | 40/40 | 40/40 | 42/59/72 | 84/90/102 | 15 |
| 1 | 40/40 | 40/40 | 42/60/77 | 82/90/99 | 27 |
| 2 | 40/40 | 40/40 | 39/60/74 | 80/91/101 | 35 |
| 3 | 40/40 | 40/40 | 42/61/82 | 80/89/100 | 42 |
| 4 | 40/40 | 40/40 | 41/61/78 | 77/91/104 | 44 |
| 5 | 40/40 | 40/40 | 46/60/81 | 80/89/99 | 46 |
| 6 | 40/40 | 40/40 | 52/66/81 | 78/92/100 | 42 |
| 7 | 40/40 | 40/40 | 44/64/82 | 80/91/98 | 48 |
| 8 | 0/40 | 0/40 | 0/0/0 | 0/0/0 | 0 |
| 9 | 0/40 | 0/40 | 0/0/0 | 0/0/0 | 0 |
| 10 | 0/40 | 0/40 | 0/0/0 | 0/0/0 | 0 |

Auffällige Ausreisser (nicht geglättet): Stufe 6 hat den höchsten Median der Angreifer-Verluste (66) und
zugleich einen Treffer-Rückgang von 46 (Stufe 5) auf 42 — das ist kein Zufallsausreisser, sondern die Folge
des Mauerabzugs (Abschnitt J, Punkt 1). Stufe 8 bis 10: Vorrunde 0/40, weil die Fuss-Schwelle 640/810/1000
die vorhandene Fuss-SK 600 übersteigt — Rückzug ohne Kampf, daher keine Verluste und keine Treffer.

## D. Schwellenverhalten (gemessen gegen dokumentiert)

Für jede Stufe wurde `kampfbericht.vorrunde` genau an der dokumentierten Schwelle und knapp darunter geprüft.

| Stufe | Fuss-Schwelle (dok.) | Belagerung (dok.) | besteht an Schwelle | fällt bei Schwelle−1 | Abgleich spieldaten |
|---|---|---|---|---|---|
| 1 | 10 | – | ja | nein | ja |
| 2 | 40 | – | ja | nein | ja |
| 3 | 90 | – | ja | nein | ja |
| 4 | 160 | – | ja | nein | ja |
| 5 | 250 | 500 | ja | nein | ja |
| 6 | 360 | 600 | ja | nein | ja |
| 7 | 490 | 700 | ja | nein | ja |
| 8 | 640 | 800 | ja | nein | ja |
| 9 | 810 | 900 | ja | nein | ja |
| 10 | 1000 | 1000 | ja | nein | ja |

Urteil: Die gemessene Schwelle stimmt auf allen zehn Stufen exakt mit der dokumentierten überein
(`kampfbericht.vorrunde` und `gebaeude_wirkung.wall_schwelle`). Die Quelle von `fuehre_schlacht`
(`spieldaten.wallstufen()`) liefert dieselben Werte (`abgleich_spieldaten=ja`). Keine Abweichung.

## E. Beute: Staffel gegen mitnehmbare Menge

Kleiner Vorrat 300 (3×100), grosser Vorrat 30.000 (3×10.000). Zwei Karrenarten: Handkarren (Ladung 40),
Zweispänner (Ladung 250).

| Staffel | Anteil | Handkarren 40 klein | Handkarren 40 gross | Zweispänner 250 klein | Zweispänner 250 gross |
|---|---|---|---|---|---|
| keine_verteidiger | 100 % | 40 | 40 | 250 | 250 |
| mauer_gebrochen | 60 % | 40 | 40 | 180 | 250 |
| mauer_beschaedigt | 30 % | 40 | 40 | 90 | 250 |
| mauer_heil | 10 % | 30 | 40 | 30 | 250 |

Nachweis „zuerst Ladung, dann Anteil“: Der Code rechnet `ziel = min(kapazitaet, int(gesamt * anteil))`.
Beim grossen Vorrat liefert jede Staffel exakt die Ladung (40 bzw. 250), nie mehr — die Ladung ist die
bindende Grenze. Beim kleinen Vorrat greift der Anteil nur dort, wo er unter der Ladung liegt:
Zweispänner klein zeigt die volle Staffel 250/180/90/30 (100/60/30/10 % von 300), nur die 100 %-Stufe wird
auf 250 gedeckelt (300 wäre mehr, als der Karren trägt). Abbuchung (`beute_am_ziel`, Wall heil, 1 Verteidiger,
Handkarren): genommen 30, Rest 270, kein negativer Bestand.

## F. Ladung und Wagenbau (Deckel je Karrenart, Faktor 2,0)

| Wagenbau-Stufe | Faktor | Handkarren | Einspänner | Zweispänner | Handelskarawane | Grosse Handelskarawane |
|---|---|---|---|---|---|---|
| 0 (ohne) | 1,0 | 40 | 100 | 250 | 1000 | 2500 |
| 1 | 1,1 | 44 | 110 | 275 | 1100 | 2750 |
| 5 | 1,5 | 60 | 150 | 375 | 1500 | 3750 |
| 10 | 2,0 | 80 | 200 | 500 | 2000 | 5000 |
| 11 (über Höchststufe) | 2,0 | 80 | 200 | 500 | 2000 | 5000 |
| 15 (über Höchststufe) | 2,0 | 80 | 200 | 500 | 2000 | 5000 |

Basiswerte 40/100/250/1000/2500 bleiben unverändert (Quelle `data/units.json`, Feld „ladung“).
Deckel Faktor 2,0 bei Wagenbau 10 wird eingehalten; über der Höchststufe (11, 15) bleibt der Faktor auf 2,0
gedeckelt (`einheiten.stufe_von` kappt bei 10). Bonus +10 % je Stufe, Quelle `data/karrenkapazitaet.json`.

## G. Reisekosten (BELEGT/VORSCHLAG)

Alle Sätze sind VORSCHLAG (auftraege.offene_luecken["kosten"]): Gold, Nahrung und Mana sind nirgends mit
Zahlen belegt, nur die Richtung („Gold und Nahrung je nach Einheiten“, fremdes Ziel: Mana nach Entfernung).
BELEGT ist nur die Reisezeit-Richtung (Rückkehr = doppelt so lang, Handbuch S. 19) und die Drosselung
in 10-%-Schritten; die Formel SEKUNDEN_JE_FELD = 7200 s ist VORSCHLAG (Registerpunkt 43).

| Einheiten | Entfernung | Gold (V) | Nahrung (V) | Mana (V) | Reisezeit h (V) |
|---|---|---|---|---|---|
| 10 | 1 | 25,00 | 0,04 | 5,50 | 0,08 |
| 10 | 5 | 125,00 | 0,20 | 7,50 | 0,40 |
| 10 | 20 | 500,00 | 0,80 | 15,00 | 1,60 |
| 40 | 1 | 100,00 | 0,16 | 5,50 | 0,08 |
| 40 | 5 | 500,00 | 0,80 | 7,50 | 0,40 |
| 40 | 20 | 2000,00 | 3,20 | 15,00 | 1,60 |
| 100 | 1 | 250,00 | 0,40 | 5,50 | 0,08 |
| 100 | 5 | 1250,00 | 2,00 | 7,50 | 0,40 |
| 100 | 20 | 5000,00 | 8,00 | 15,00 | 1,60 |

Gold und Nahrung skalieren linear mit der Truppenzahl; Mana hängt nur von der Entfernung ab
(5 + 0,5 je Feld), nicht von der Truppenzahl — 10 und 100 Einheiten zahlen identisch Mana.

## H. AT-gegen-SK-Gegenprobe (Register 54)

Dieselbe Aufstellung einmal mit `E.angriff` (AT = 50 beim Krieger) und einmal mit `E.schlagkraft`
(SK = 3 beim Krieger) durch die Vorrunde geschickt. Angabe: wie viele Krieger die Fuss-Schwelle erreichen.

| Stufe | Fuss-Schwelle | Krieger nötig nach AT | Krieger nötig nach SK |
|---|---|---|---|
| 1 | 10 | 1 | 4 |
| 2 | 40 | 1 | 14 |
| 3 | 90 | 2 | 30 |
| 4 | 160 | 4 | 54 |
| 5 | 250 | 5 | 84 |
| 6 | 360 | 8 | 120 |
| 7 | 490 | 10 | 164 |
| 8 | 640 | 13 | 214 |
| 9 | 810 | 17 | 270 |
| 10 | 1000 | 20 | 334 |

Beispiel: 1 Krieger gegen Wall 1 — nach AT würde die Vorrunde bestehen (50 ≥ 10), nach SK nicht (3 < 10).
`AT_besteht=ja`, `SK_besteht=nein`. Das ist der Beweis, dass Register 54 (SK statt AT) behoben ist:
die alte AT-Lesart hätte fast jeden Trupp bestehen lassen.

## I. Die drei wichtigsten Kernaussagen

1. Register 54 ist behoben: Die Wallvorrunde rechnet mit Schlagkraft (SK), nicht mit Angriff (AT). Für Wall 1
   braucht es 4 Krieger (SK) statt 1 (AT); 1 Krieger wird nach SK abgelehnt, nach AT fälschlich zugelassen.
   Quelle: kampfbericht.vorrunde + einheiten.angriff/schlagkraft (Abschnitt H).
2. Schwellenverhalten exakt: Mit Fuss-SK 600 und Belagerungs-SK 720 werden die Wälle 0–7 in allen 40 Läufen
   überwunden (100 % Vorrunde, 100 % Siege), ab Wall 8 (Fuss-Schwelle 640) in 0 von 40 Läufen. Gemessene
   Schwelle = dokumentierte Schwelle auf allen zehn Stufen (abgleich_spieldaten=ja).
   Quelle: fuehre_schlacht + gebaeude_wirkung.wall_schwelle (Abschnitte C und D).
3. Beute wird zuerst durch die Ladung gedeckelt: Beim grossen Vorrat (30.000) liefert jede Staffel exakt die
   Karrenladung (40 bzw. 250), nie mehr; der Anteil (10/30/60/100 %) greift nur, wo er unter der Ladung liegt
   (`ziel = min(kapazitaet, int(gesamt * anteil))`). Quelle: kampfbericht.beute_staffel (Abschnitt E).

## J. Auffälligkeiten, nicht geglättet

1. Angreifer-Bogenschützen werden ab Wall 6 wirkungslos: der Mauerabzug (5 Prozentpunkte je Stufe, VORSCHLAG)
   senkt die Trefferchance des Bogenschützen von 30 % (Wall 0) auf 0 % ab Wall 6. Der Verteidiger hat keinen
   Abzug und schiesst weiter. Folge: die Fernkampf-Treffer steigen mit der Wallstufe zwar (mehr Runden),
   aber ausschliesslich zugunsten des Verteidigers. VORSCHLAG-Wert (Register 52, kampf.vorschlaege["mauerabzug"]).
2. Hohe eigene Verluste trotz 2:1-Überlegenheit: Median rund 60 von 200 Angreifern (Spitze 82) gegen
   rund 90 von 100 Verteidigern. Krieger gegen Krieger mit gleichen Werten führt im Nahkampf zu rund 50 %
   Austausch je Angriff — kein Messfehler, sondern die Kampfwert-Gleichheit der Aufstellung.
3. Mana-Reisekosten hängen nur von der Entfernung ab (5 + 0,5 je Feld), nicht von der Truppenzahl:
   10 und 100 Einheiten zahlen identisch Mana. Sätze VORSCHLAG (Abschnitt G).
4. Diskrepanz Auftrag-Vorprüfung gegen Schlacht (benannt, nicht geändert): `auftraege._schlagkraft_fussttruppen`
   zählt über `einheiten.ist_kaempfer` Kampf- UND Kundschafter (nah und fern), `fuehre_schlacht` zählt für die
   Wallschwelle nur NAHKAMPF (`_nah`). Ein reiner Fernkampftrupp könnte im Auftrag „würde bestehen“ angezeigt
   bekommen, in der Schlacht aber zurückgezogen werden. Register 54 (AT/SK) ist davon unberührt; dies ist ein
   eigener, offener Punkt.

## K. Was nicht messbar ist (und warum)

1. Trefferquote als Treffer je Schuss, getrennt je Seite: das Schlachtergebnis protokolliert je Fernrunde nur
   die Zahl der Treffer („N Treffer“), nicht die Schusszahl und nicht die Seite. Gemessen wurde deshalb die
   Treffer-Summe beider Seiten (Median) und die theoretische Trefferchance des Angreifers aus der Formel.
2. Beute in der echten Schlacht (`fuehre_schlacht.ergebnis["beute"]`) rechnet über `kampf._beute` nur mit der
   Ladungsgrenze, ohne Staffel; die Staffel (`beute_staffel` / `beute_am_ziel`) ist der Auftrags-/Bot-Pfad
   (Register 62). Die zwei Formeln wurden nicht gegeneinander verschmolzen, weil der Auftrag sie als getrennte
   Messgegenstände nennt.
3. Mauerreparatur und Turmschutz: nicht gemessen. Die Messaufstellung nutzt nur Katapulte (kein Belagerungsturm),
   und eine Mauerreparatur ist im Handbuch nicht belegt.
4. „Belegte“ Reisekosten: existieren nicht — alle Sätze sind VORSCHLAG; messbar ist nur, was die vorhandene
   Formel liefert (Abschnitt G).
