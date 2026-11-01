# Messbericht Wirtschaft (B1) - 01.11.2026

## A. Kopf

- Datum: 01.11.2026
- Kopf-Commit: 52604ea (Branch main, Arbeitsbaum leer)
- Angelegte Dateien: tools/mess_wirtschaft.py, docs/audits/MESS_WIRTSCHAFT_20261101.md
- Aufruf: python -X utf8 tools/mess_wirtschaft.py (Arbeitsverzeichnis = Projektwurzel, Rueckgabewert 0)
- Unteragenten: 0 (allein gerechnet; Delegation war erlaubt, war aber nicht noetig und haette den Blockrahmen nur belastet)
- Geaenderte Projektdateien: keine. Nur die zwei neuen Dateien wurden angelegt, nichts geloescht, nichts committet.

## B. Die gedruckten Zeilen

```
# Messwirtschaft Nebelseetal Remake (B1, 01.11.2026)

## 1. Ertraege je Gebaeude und Gelaende
Ertrag_bibliothek | kein Ertrag | data/buildings.json
Ertrag_bogenbauer | kein Ertrag | data/buildings.json
Ertrag_diebesgilde | kein Ertrag | data/buildings.json
Ertrag_erzmine_berg | Metall 3 | data/buildings.json:ertrag_pro_stunde
Ertrag_erzmine_huegel | Metall 1.5 | data/buildings.json:ertrag_pro_stunde
Ertrag_farm_grasland | Nahrung 4 | data/buildings.json:ertrag_pro_stunde
Ertrag_farm_steppe | Nahrung 2 | data/buildings.json:ertrag_pro_stunde
Ertrag_goldmine_berg | Gold 3 | data/buildings.json:ertrag_pro_stunde
Ertrag_goldmine_huegel | Gold 1.5 | data/buildings.json:ertrag_pro_stunde
Ertrag_haus | kein Ertrag | data/buildings.json
Ertrag_holzfaeller_wald | Holz 4 | data/buildings.json:ertrag_pro_stunde
Ertrag_holzfaeller_steppe | Holz 2 | data/buildings.json:ertrag_pro_stunde
Ertrag_jaeger_wald | Nahrung 2, Leder 2 | data/buildings.json:ertrag_pro_stunde
Ertrag_jaeger_steppe | Nahrung 1, Leder 1 | data/buildings.json:ertrag_pro_stunde
Ertrag_kriegerakademie | kein Ertrag | data/buildings.json
Ertrag_lager | kein Ertrag | data/buildings.json
Ertrag_naehstube | kein Ertrag | data/buildings.json
Ertrag_pferdezucht_grasland | Pferde 3 | data/buildings.json:ertrag_pro_stunde
Ertrag_pferdezucht_steppe | Pferde 1.5 | data/buildings.json:ertrag_pro_stunde
Ertrag_rinderfarm_grasland | Nahrung 1, Leder 3 | data/buildings.json:ertrag_pro_stunde
Ertrag_rinderfarm_steppe | Nahrung 0.5, Leder 1.5 | data/buildings.json:ertrag_pro_stunde
Ertrag_schafszucht_grasland | Wolle 3 | data/buildings.json:ertrag_pro_stunde
Ertrag_schafszucht_steppe | Wolle 1.5 | data/buildings.json:ertrag_pro_stunde
Ertrag_schmiede | kein Ertrag | data/buildings.json
Ertrag_steinmetz_berg | Stein 4 | data/buildings.json:ertrag_pro_stunde
Ertrag_steinmetz_huegel | Stein 2 | data/buildings.json:ertrag_pro_stunde
Ertrag_stellmacher | kein Ertrag | data/buildings.json
Ertrag_tempel_nebelsee | Mana 5 | data/buildings.json:ertrag_pro_stunde
Ertrag_tempel_sonst | Mana 1 | data/buildings.json:ertrag_pro_stunde
Ertrag_verteidigungswall | kein Ertrag | data/buildings.json

## 1b. Handbuchabgleich (2009, Seite 10/11)
Handbuch_erzmine | BELEGT | Handbuch2009:S.10/11
Handbuch_farm | BELEGT | Handbuch2009:S.10/11
Handbuch_goldmine | BELEGT | Handbuch2009:S.10/11
Handbuch_holzfaeller | BELEGT | Handbuch2009:S.10/11
Handbuch_jaeger | BELEGT | Handbuch2009:S.10/11
Handbuch_pferdezucht | BELEGT | Handbuch2009:S.10/11
Handbuch_rinderfarm | WIDERSPRUCH | Handbuch2009:S.10/11
Handbuch_schafszucht | BELEGT | Handbuch2009:S.10/11
Handbuch_steinmetz | BELEGT | Handbuch2009:S.10/11
Handbuch_tempel | BELEGT | Handbuch2009:S.10/11
Handbuch_rinderfarm_Detail | Handbuch Grasland Nahrung 3 Leder 3, Steppe 1.5/1.5; Daten Grasland Nahrung 1 Leder 3, Steppe 0.5/1.5 | Handbuch2009:S.10/11 vs data/buildings.json

## 2. Reichsertrag je Spielstunde und Spieltag
Programm_erzmine | 8 | ANNAHME: 10x10-Dorf, 90 Felder belegt
Programm_farm | 10 | ANNAHME: 10x10-Dorf, 90 Felder belegt
Programm_goldmine | 8 | ANNAHME: 10x10-Dorf, 90 Felder belegt
Programm_holzfaeller | 9 | ANNAHME: 10x10-Dorf, 90 Felder belegt
Programm_jaeger | 9 | ANNAHME: 10x10-Dorf, 90 Felder belegt
Programm_pferdezucht | 10 | ANNAHME: 10x10-Dorf, 90 Felder belegt
Programm_rinderfarm | 10 | ANNAHME: 10x10-Dorf, 90 Felder belegt
Programm_schafszucht | 10 | ANNAHME: 10x10-Dorf, 90 Felder belegt
Programm_steinmetz | 9 | ANNAHME: 10x10-Dorf, 90 Felder belegt
Programm_tempel | 6 | ANNAHME: 10x10-Dorf, 90 Felder belegt
Dorf_Beispiel_je_Stunde | Gold 18, Holz 36, Leder 40.5, Mana 30, Metall 18, Nahrung 55.5, Pferde 22.5, Stein 26, Wolle 22.5 | Rechnung aus data/buildings.json + data/gelaende.json
Reich_Beispiel_je_Stunde | Gold 108, Holz 216, Leder 243, Mana 180, Metall 108, Nahrung 333, Pferde 135, Stein 156, Wolle 135 | 6 Doerfer (sechs Doerfer)
Reich_Beispiel_je_Tag | Gold 2592, Holz 5184, Leder 5832, Mana 4320, Metall 2592, Nahrung 7992, Pferde 3240, Stein 3744, Wolle 3240 | 24 Spielstunden je Spieltag
Dorf_Bester_Fall_je_Stunde | Gold 24, Holz 36, Leder 48, Mana 30, Metall 24, Nahrung 68, Pferde 30, Stein 36, Wolle 30 | Rechnung aus data/buildings.json + data/gelaende.json
Reich_Bester_Fall_je_Stunde | Gold 144, Holz 216, Leder 288, Mana 180, Metall 144, Nahrung 408, Pferde 180, Stein 216, Wolle 180 | 6 Doerfer (sechs Doerfer)
Reich_Bester_Fall_je_Tag | Gold 3456, Holz 5184, Leder 6912, Mana 4320, Metall 3456, Nahrung 9792, Pferde 4320, Stein 5184, Wolle 4320 | 24 Spielstunden je Spieltag
Dorf_Schlechtester_Fall_je_Stunde | Gold 12, Holz 18, Leder 24, Mana 6, Metall 12, Nahrung 34, Pferde 15, Stein 18, Wolle 15 | Rechnung aus data/buildings.json + data/gelaende.json
Reich_Schlechtester_Fall_je_Stunde | Gold 72, Holz 108, Leder 144, Mana 36, Metall 72, Nahrung 204, Pferde 90, Stein 108, Wolle 90 | 6 Doerfer (sechs Doerfer)
Reich_Schlechtester_Fall_je_Tag | Gold 1728, Holz 2592, Leder 3456, Mana 864, Metall 1728, Nahrung 4896, Pferde 2160, Stein 2592, Wolle 2160 | 24 Spielstunden je Spieltag

## 3. Siedlerzuwachs und Siedlerdecke
Zuwachs_je_Stunde_Reich | 6 | src/gebaeude_wirkung.py:siedler_zuwachs_pro_stunde
Zuwachs_je_Stunde_Reich_Heilkunde10 | 12 | heilkunde (Kleinbuchstabe, so liest gebaeude_wirkung.py:180)
Befund_Heilkunde_Schluessel | gebaeude_wirkung.py liest 'heilkunde', die Forschung heisst 'Heilkunde' - Bonus greift im Spiel nicht | src/gebaeude_wirkung.py:180 vs data/research.json
Grenze_je_Dorf_ohne_Haus | 10 | src/gebaeude_wirkung.py:siedlergrenze_je_siedlung
Grenze_je_Dorf_10_Haeuser | 60 | 10 + 5 je Haus
Reichsdeckel_ohne_Haus | 60 | src/gebaeude_wirkung.py:bevoelkerungsgrenze
Reichsdeckel_10_Haeuser_je_Dorf | 360 | 6 Doerfer x (10 + 5x10)
Zeit_bis_volle_Siedlung_Stunden | 50 | Start 10 -> Grenze 60, 1 Siedler/h

## 4. Goldfluss je Spieltag
Goldmine_Berg_je_Stunde | 3 | data/buildings.json:goldmine.ertrag_pro_stunde
Goldmine_Huegel_je_Stunde | 1.5 | data/buildings.json:goldmine.ertrag_pro_stunde
Gold_Einnahme_Reich_je_Tag | 2592 | Beispielprogramm, 8 Goldminen je Dorf, 6 Doerfer
Gold_Abfluss_Einheit_Krieger | 500 | data/units.json:Krieger.kosten.gold
Gold_Abfluss_Baukosten | nicht vorhanden | data/baupreise.json: kein Goldposten
Gold_Abfluss_Reisekosten | nicht belegt | src/auftraege.py:GOLD_JE_FELD_JE_GS=0.1 (VORSCHLAG)

## 5. Mana je Spielstunde
Tempel_Nebelsee_je_Stunde | 5 | data/buildings.json:tempel.ertrag_pro_stunde
Tempel_sonst_je_Stunde | 1 | data/buildings.json:tempel (alle ausser Sumpf)
Tempel_Sumpf_je_Stunde | 0 | Sumpf unbebaubar (Handbuch S. 11)
Tempel_Nebelsee_Goetterkunde1 | 5.25 | Goetterkunde +5 % je Stufe
Tempel_Nebelsee_Goetterkunde5 | 6.25 | Goetterkunde +5 % je Stufe
Tempel_Nebelsee_Goetterkunde10 | 7.5 | Goetterkunde +5 % je Stufe

## 6. Nahrungsverbrauch
Verbrauch_je_Einheit_je_Tag | 8 | data/nahrungsverbrauch.json:je_einheit_pro_tag
Bedarf_100_Einheiten_je_Tag | 800 | src/spieloekonomie.py:tagesbedarf_nahrung
Bedarf_360_Einheiten_je_Tag | 2880 | src/spieloekonomie.py:tagesbedarf_nahrung
Bedarf_100_Einheiten_je_Stunde | 33.33 | src/spieloekonomie.py:verbrauch_pro_stunde (geteilt durch 24)
Reisekosten_Nahrung_je_Feld | 0.1 je Einheit je Feld geteilt durch GS | src/auftraege.py:NAHRUNG_JE_FELD_DURCH_GS (VORSCHLAG)
Reisekosten_Beispiel_40Krieger_10Felder | Gold 1000, Nahrung 1.6, Mana 10 | src/auftraege.py:kosten_der_mission

## 7. Waren- und Ausbildungsdauern
Warendauer_Armbrust | 10800 s = 180 min | data/warenrezepte.json:dauer (VORSCHLAG)
Warendauer_Bogen | 6000 s = 100 min | data/warenrezepte.json:dauer (VORSCHLAG)
Warendauer_Diebesumhang | 3600 s = 60 min | data/warenrezepte.json:dauer (VORSCHLAG)
Warendauer_Dolch | 2400 s = 40 min | data/warenrezepte.json:dauer (VORSCHLAG)
Warendauer_Fellruestung | 8400 s = 140 min | data/warenrezepte.json:dauer (VORSCHLAG)
Warendauer_Fellumhang | 6000 s = 100 min | data/warenrezepte.json:dauer (VORSCHLAG)
Warendauer_Kettenhemd | 4800 s = 80 min | data/warenrezepte.json:dauer (VORSCHLAG)
Warendauer_Kurzbogen | 3600 s = 60 min | data/warenrezepte.json:dauer (VORSCHLAG)
Warendauer_Kurzschwert | 4800 s = 80 min | data/warenrezepte.json:dauer (VORSCHLAG)
Warendauer_Langbogen | 8400 s = 140 min | data/warenrezepte.json:dauer (VORSCHLAG)
Warendauer_Lederruestung | 4800 s = 80 min | data/warenrezepte.json:dauer (VORSCHLAG)
Warendauer_Magischer Paladinharnisch | 12000 s = 200 min | data/warenrezepte.json:dauer (VORSCHLAG)
Warendauer_Messer | 1200 s = 20 min | data/warenrezepte.json:dauer (VORSCHLAG)
Warendauer_Plattenruestung | 7200 s = 120 min | data/warenrezepte.json:dauer (VORSCHLAG)
Warendauer_Schwert | 1200 s = 20 min | data/warenrezepte.json:dauer (belegt)
Warendauer_Wollumhang | 1200 s = 20 min | data/warenrezepte.json:dauer (VORSCHLAG)
Warendauer_Zweihaender | 10800 s = 180 min | data/warenrezepte.json:dauer (VORSCHLAG)
Ausbildungsdauer_Stufe_1 | 1200 s = 20 min | src/spieloekonomie.py:ausbildung_start (Grunddauer / Stufe)
Ausbildungsdauer_Stufe_2 | 600 s = 10 min | src/spieloekonomie.py:ausbildung_start (Grunddauer / Stufe)
Ausbildungsdauer_Stufe_3 | 400 s = 6.67 min | src/spieloekonomie.py:ausbildung_start (Grunddauer / Stufe)
Ausbildungsdauer_Stufe_4 | 300 s = 5 min | src/spieloekonomie.py:ausbildung_start (Grunddauer / Stufe)
Ausbildungsdauer_Stufe_5 | 240 s = 4 min | src/spieloekonomie.py:ausbildung_start (Grunddauer / Stufe)
Warteschlange_10Schwerter_1Schmiede_min | 200 | Handbuch S. 13 Beispiel; src/werkstatt.py
Warteschlange_10Schwerter_2Schmiede_min | 100 | Handbuch S. 13 Beispiel; src/werkstatt.py

## 8. Verhaeltniskennzahlen
Ertrag_je_Siedler_360 | 4.48 | Reichsertrag (Summe) / Siedlerdeckel 360
Ertrag_je_Siedler_60 | 26.9 | Reichsertrag (Summe) / Grunddeckel 60
Siedler_je_Gebaeude | 0.67 | 360 Siedler / (90 Gebaeude x 6 Doerfer)
Zeit_bis_erste_Siedlung_Tage | 0.84 | Gruendungsbedarf / Dorf-Tagesertrag (Vollertrag, Anlaufzeit nicht enthalten)
Gruendungsbedarf | holz 730, leder 150, metall 80, nahrung 550, pferde 4, stein 300, wolle 100 | spieloekonomie.gruendungskosten + Siedlerkarren + Wagenbau 1
Zeit_bis_100_Einheiten_Gold_Tage | 19.29 | 100 Krieger x 500 Gold / Reichs-Goldertrag je Tag
Zeit_bis_100_Einheiten_Siedler_Tage | 0.69 | 100 Siedler / 6 Siedler je Stunde
Zeit_bis_100_Einheiten_Ausbildung_Tage | 1.39 | 100 x 20 min, eine Akademie
Nahrung_Anteil_100_Einheiten_Prozent | 10.01 | 800 je Tag / Reichs-Nahrungsertrag
Nahrung_Anteil_360_Einheiten_Prozent | 36.04 | 2880 je Tag / Reichs-Nahrungsertrag
```

Sammellauf (Pflichtlauf): 117 Dateien, 115 gruen, 0 rot, 2 ausgesetzt, 4355 bestandene Pruefungen, 696 Sekunden (0 Fehler, 38 Befunde; ausgesetzt: test_oekonomie_kern_unabhaengig.py, test_weltkarte.py - beide dokumentiert zurueckgezogen).

## C. Erträge je Gebäude und Gelände

Handbuchwerte aus der Tafel 2009 (Seite 10/11), Datenwerte aus data/buildings.json. Urteil je Gelände.

| Gebäude | Gelände | Handbuchwert | Datenwert | Urteil |
|---|---|---|---|---|
| Holzfäller | Wald | 4 Holz | 4 Holz | BELEGT |
| Holzfäller | Steppe | 2 Holz | 2 Holz | BELEGT |
| Steinmetz | Berg | 4 Stein | 4 Stein | BELEGT |
| Steinmetz | Hügel | 2 Stein | 2 Stein | BELEGT |
| Erzmine | Berg | 3 Metall | 3 Metall | BELEGT |
| Erzmine | Hügel | 1,5 Metall | 1,5 Metall | BELEGT |
| Tempel | Nebelsee | 5 Mana | 5 Mana | BELEGT (Register 56) |
| Tempel | alle außer Sumpf | 1 Mana | 1 Mana | BELEGT (Register 56) |
| Farm | Grasland | 4 Nahrung | 4 Nahrung | BELEGT |
| Farm | Steppe | 2 Nahrung | 2 Nahrung | BELEGT |
| Goldmine | Berg | 3 Gold | 3 Gold | BELEGT |
| Goldmine | Hügel | 1,5 Gold | 1,5 Gold | BELEGT |
| Schafszucht | Grasland | 3 Wolle | 3 Wolle | BELEGT |
| Schafszucht | Steppe | 1,5 Wolle | 1,5 Wolle | BELEGT |
| Rinderfarm | Grasland | 3 Nahrung, 3 Leder | 1 Nahrung, 3 Leder | WIDERSPRUCH |
| Rinderfarm | Steppe | 1,5 Nahrung, 1,5 Leder | 0,5 Nahrung, 1,5 Leder | WIDERSPRUCH |
| Pferdezucht | Grasland | 3 Pferde | 3 Pferde | BELEGT |
| Pferdezucht | Steppe | 1,5 Pferde | 1,5 Pferde | BELEGT |
| Jäger | Wald | 2 Nahrung, 2 Leder | 2 Nahrung, 2 Leder | BELEGT |
| Jäger | Steppe | 1 Nahrung, 1 Leder | 1 Nahrung, 1 Leder | BELEGT |

Ohne Ertrag (kein ertrag_pro_stunde in data/buildings.json): Schmiede, Bogenbauer, Nähstube, Kriegerakademie, Diebesgilde, Stellmacher, Verteidigungswall, Bibliothek, Haus, Dorfzentrum (Kennung lager). Alle zehn sind genannt, kein Ertrag.

## D. Reichsertrag je Stunde und Tag

Beispielbelegung (ANNAHME): ein 10x10-Dorf, Geländeverteilung aus data/gelaende.json (Gewichte 20 Grasland, 20 Steppe, 18 Wald, 13 Hügel, 12 Berg, 7 Nebelsee, 10 Sumpf), jedes bebaubare Feld (90) trägt ein Gebäude. Das Programm steht in Abschnitt B (Programm_...). Reich = 6 Dörfer.

| Fall | Rechenweg (je Dorf und Stunde) | Reich je Stunde | Reich je Tag |
|---|---|---|---|
| Bester Fall | jedes Produktionsgebäude auf seinem besten Gelände (Summe: 36 Holz, 36 Stein, 24 Metall, 24 Gold, 68 Nahrung, 48 Leder, 30 Wolle, 30 Pferde, 30 Mana) | Gold 144, Holz 216, Stein 216, Metall 144, Nahrung 408, Leder 288, Wolle 180, Pferde 180, Mana 180 | Gold 3456, Holz 5184, Stein 5184, Metall 3456, Nahrung 9792, Leder 6912, Wolle 4320, Pferde 4320, Mana 4320 |
| Beispiel | Mischbelegung nach Gelände (Summe: 36 Holz, 26 Stein, 18 Metall, 18 Gold, 55,5 Nahrung, 40,5 Leder, 22,5 Wolle, 22,5 Pferde, 30 Mana) | Gold 108, Holz 216, Stein 156, Metall 108, Nahrung 333, Leder 243, Wolle 135, Pferde 135, Mana 180 | Gold 2592, Holz 5184, Stein 3744, Metall 2592, Nahrung 7992, Leder 5832, Wolle 3240, Pferde 3240, Mana 4320 |
| Schlechtester Fall | jedes Produktionsgebäude nur auf seinem zweitbesten Gelände (Summe: 18 Holz, 18 Stein, 12 Metall, 12 Gold, 34 Nahrung, 24 Leder, 15 Wolle, 15 Pferde, 6 Mana) | Gold 72, Holz 108, Stein 108, Metall 72, Nahrung 204, Leder 144, Wolle 90, Pferde 90, Mana 36 | Gold 1728, Holz 2592, Stein 2592, Metall 1728, Nahrung 4896, Leder 3456, Wolle 2160, Pferde 2160, Mana 864 |

Die drei Fälle sind eine Spannweite, keine einzelne Zahl: Nahrung je Tag liegt zwischen 4896 und 9792, Gold je Tag zwischen 1728 und 3456.

Hinweis: data/nahrungsverbrauch.json nennt als Reichsertrag an Nahrung 230,93 je Stunde (aus tools/balancing_messung.py, Ausbauplan je Siedlung, 6 Siedlungen). Mein Beispielprogramm ergibt 333 je Stunde. Das ist kein Widerspruch, sondern zwei verschiedene Belegungsannahmen: balancing_messung rechnet einen Teil-Ausbauplan, dieses Werkzeug rechnet 90 voll belegte Felder je Dorf (Vorgabe dieses Blocks, "je Feld ein Gebäude").

## E. Siedler

- Zuwachs: 1 Siedler je Stunde und Siedlung (Handbuch S. 11), also 6 je Stunde im Reich bei sechs Dörfern (Rechenstelle src/gebaeude_wirkung.py:siedler_zuwachs_pro_stunde).
- Heilkunde +10 % je Stufe ist belegt (Handbuch Abschnitt 5). Befund: die Rechenstelle liest den Schlüssel "heilkunde" (klein), die Forschung heißt aber "Heilkunde" (groß, data/research.json). Mit dem großen Schlüssel greift der Bonus im Spiel nicht (gemessen: 6 statt 12 bei Stufe 10). Das ist ein Code-Befund, keine Zahl im Spiel zu ändern, aber zu melden.
- Grenze je Dorf: 10 Siedler, plus 5 je Haus. Ohne Haus 10, mit 10 Häusern 60.
- Reichsdeckel: 6 Dörfer mal 10 = 60 (ohne Haus); 6 mal 60 = 360 (mit je 10 Häusern).
- Zeit bis zur vollen Siedlung: von 10 auf 60 bei 1 je Stunde = 50 Stunden (rund 2,1 Spieltage); reichsweit von 60 auf 360 bei 6 je Stunde ebenfalls 50 Stunden.

## F. Gold und Mana

Gold:
- Goldmine je Stunde: Berg 3, Hügel 1,5 (belegt).
- Gold je Tag im Beispielprogramm: 2592 (8 Goldminen je Dorf, 6 Dörfer).
- Abfluss Gold: Einheitenkosten sind belegt (Krieger 500 Gold, data/units.json). Baukosten in Gold gibt es nicht (data/baupreise.json hat keinen Goldposten). Reisekosten in Gold sind nur der Richtung nach belegt, die Höhe ist VORSCHLAG (GOLD_JE_FELD_JE_GS = 0,1) und damit "nicht belegt".

Mana:
- Tempel je Stunde: Nebelsee 5, alle anderen bebaubaren Gelände 1, Sumpf 0 (unbebaubar).
- Götterkunde +5 % je Stufe (belegt, Handbuch Abschnitt 5): Faktor 1,05 bei Stufe 1, 1,25 bei Stufe 5, 1,5 bei Stufe 10. Tempel auf Nebelsee: 5,25 / 6,25 / 7,5 je Stunde.

## G. Nahrung

- Laufender Verbrauch: 8 je Einheit und Spieltag (data/nahrungsverbrauch.json, VORSCHLAG; Rechenstelle spieloekonomie.tagesbedarf_nahrung). Je Stunde 1/3 je Einheit.
- 100 Einheiten binden 800 je Tag, 360 Einheiten 2880 je Tag.
- Verbrauchsanteil am Tagesertrag (Beispielprogramm, 7992 Nahrung je Tag im Reich): 100 Einheiten 10,01 %, 360 Einheiten 36,04 %.
- Reisekosten je Feld getrennt: 0,1 Nahrung je Einheit und Feld geteilt durch GS (VORSCHLAG, NAHRUNG_JE_FELD_DURCH_GS). Beispiel 40 Krieger, 10 Felder, GS 25: Nahrung 1,6 (und Gold 1000, Mana 10, beide VORSCHLAG).

## H. Dauern

Waren (data/warenrezepte.json, Dauer in Sekunden): nur das Schwert ist belegt (20 min = 1200 s, Handbuchbeispiel S. 13). Alle anderen Warendauern sind VORSCHLAG: Messer 20 min, Dolch 40, Kurzschwert 80, Schwert 20 (belegt), Zweihänder 180, Kettenhemd 80, Plattenrüstung 120, Magischer Paladinharnisch 200, Kurzbogen 60, Bogen 100, Langbogen 140, Armbrust 180, Wollumhang 20, Lederrüstung 80, Diebesumhang 60, Fellumhang 100, Fellrüstung 140.

Ausbildung (src/spieloekonomie.py:ausbildung_start): Grunddauer 20 min geteilt durch Stufenfaktor. Stufe 1 = 20 min, Stufe 2 = 10 min, Stufe 3 = 6,67 min, Stufe 4 = 5 min, Stufe 5 = 4 min. Die Grunddauer 20 min ist selbst VORSCHLAG (kein Originalwert belegt).

Warteschlange (Handbuchbeispiel S. 13, nachgerechnet mit src/werkstatt.py): 10 Schwerter à 20 min brauchen mit einer Schmiede 200 min, mit zwei Schmieden 100 min.

## I. Die drei wichtigsten Kernaussagen

1. Die Rinderfarm widerspricht dem Handbuch: Daten stehen auf 1 Nahrung / 3 Leder (Grasland) statt 3 / 3, und 0,5 / 1,5 (Steppe) statt 1,5 / 1,5 (Quelle data/buildings.json:rinderfarm gegen Handbuch 2009 S. 10). Im Beispielprogramm liefert die Rinderfarm damit nur 7,5 statt 22,5 Nahrung je Dorfstunde, der Reichsertrag an Nahrung sinkt von 70,5 auf 55,5 je Dorfstunde.
2. Die harte Grenze ist die Siedlerdecke, nicht der Rohstoff: 360 Siedler im Reich (6 mal 60 bei 10 Häusern je Dorf), Zuwachs 6 je Stunde, die volle Siedlung steht nach 50 Stunden.
3. Gold ist der Engpass für eine Armee: 100 Krieger kosten 50000 Gold, das sind 19,3 Spieltage des vollen Goldertrags (2592 je Tag im Beispielprogramm); Siedler (0,69 Tage) und Ausbildung (1,39 Tage) fallen dagegen kaum ins Gewicht.

## J. Jede Abweichung

1. Rinderfarm, data gegen Handbuch. Handbuchzeile: Seite 10, "Rinderfarm ... Grasland (3 Nahrung, 3 Leder), Steppe (1,5 Nahrung, 1,5 Leder)". Datenwert: Grasland 1 Nahrung / 3 Leder, Steppe 0,5 / 1,5. Urteil: WIDERSPRUCH. Vorschlag: entweder die Daten an das Handbuch 2009 angleichen oder die neuere Quelle WeitereWerteKampfsystem.odt S. 4 (1+3 bzw. 0,5+1,5) als geltend festlegen - Daniel entscheidet, eine Entscheidung gehört ins Register.

2. Heilkunde-Schlüssel (Code-Befund, kein data/Handbuch-Widerspruch). src/gebaeude_wirkung.py:180 liest "heilkunde" (klein), data/research.json und forschung_wirkung führen "Heilkunde" (groß). Folge: der belegte Bonus +10 % Siedler je Stufe greift in siedler_zuwachs_pro_stunde nicht. Urteil: BEFUND (Code), nicht hier behoben (Messingenieur ändert keinen Spielcode). Vorschlag: Schlüssel angleichen.

3. Reichsertrag-Differenz (Dokumentationshinweis). data/nahrungsverbrauch.json nennt 230,93 Nahrung je Stunde (balancing_messung-Ausbauplan), dieses Werkzeug misst 333 je Stunde (Vollbelegung). Kein Widerspruch, sondern zwei Belegungsannahmen; siehe Abschnitt D.

## K. Was nicht messbar ist

- Reisekosten in Gold/Nahrung/Mana: nur die Richtung ist belegt, die drei Sätze in src/auftraege.py sind VORSCHLAG, also "nicht belegt" und hier nicht als belegt ausgegeben.
- Baukosten in Gold: nicht vorhanden (data/baupreise.json hat keinen Goldposten), also nichts zu messen.
- Ausbildungs-Grunddauer: 20 min sind VORSCHLAG, keine Originalstelle nennt eine Ausbildungsdauer (geprüft 31.10.2026, docs/audits/AUSBILDUNGSDAUER_BELEGT_20261031.md).
- Warendauern außer Schwert: VORSCHLAG, nicht belegt.
- Anlaufzeit: "Zeit bis zur ersten Siedlung" 0,84 Tage ist eine Untergrenze (Vollertrag ab Tag 1); die echte Anlaufzeit hängt von der Startkarte ab und ist hier nicht simuliert.

## L. Vorschläge

1. Rinderfarm-Wert klären (Wirkung: die Rinderfarm liefert im Beispielprogramm 7,5 statt 22,5 Nahrung je Dorfstunde, der Reichsertrag an Nahrung sinkt um rund 21 %). Aufwand S.
2. Heilkunde-Schlüssel in src/gebaeude_wirkung.py angleichen, damit der belegte Bonus +10 % je Stufe greift. Aufwand S.
3. Reisekosten-Sätze (Gold/Nahrung/Mana je Feld) nach dem Spieltest balancieren; die Richtung ist belegt, die Höhe noch offen. Aufwand M.
4. Ausbildungs-Grunddauer (20 min) im Register als VORSCHLAG festhalten oder einen belegten Wert nachtragen. Aufwand S.
5. Verbrauchsanteil beobachten: 8 je Einheit und Tag bindet bei 360 Einheiten 36 % des Beispielertrags an Nahrung; beim Ausbau des Reichs nachjustieren. Aufwand S.
