# Entwurf Ausbildung und Hersteller (Nebelseetal Remake)

Status: Entwurf (nur Lesen gemessen, kein Code geaendert, kein git, keine Tests, keine Fenster).
Datum: 30.10.2026. Richtschnur: Original-Handbuch 2009 (docs/original/Spielanleitung_2009_Textfassung.txt)
und die 2005er Fassung (docs/original/Spielanleitung_2005/). Urteile: BELEGT / WIDERSPRUCH /
NICHT BELEGT / VORSCHLAG. Wo eine Zahl fehlt: null und begruendet, nichts geschaetzt.

---

## 1. Ist-Zustand (gemessen, nur lesen)

### 1.1 Einheit -> Gebaeude (data/units.json, Feld "gebaeude", 28 Einheiten)

Auszaehlung ueber data/units.json: anzahl 28. Drei Ausbildungsstaetten, alle 28 Einheiten haben
genau eine `gebaeude`-Angabe. Keine Einheit hat ein leeres oder doppeltes `gebaeude`.

Zaehlung je Gebaeude:

| Gebaeude | Anzahl Einheiten | Beleg |
|---|---|---|
| Kriegerakademie | 9 (5 Nahkampf, 4 Fernkampf) | data/units.json |
| Diebesgilde | 6 (Kundschafter) | data/units.json |
| Stellmacher | 13 (6 Karren, 7 Belagerungswaffen) | data/units.json |
| Summe | 28 | data/units.json "anzahl": 28 |

Tabelle Kriegerakademie (9):

| Einheit | Gebaeude | Kosten | Voraussetzung | Beleg |
|---|---|---|---|---|
| Bürgerwehr | Kriegerakademie | 1 Siedler, 100 Nahrung, 50 Leder, 50 Wolle | keine | units.json Z. 6-34 |
| Kämpfer | Kriegerakademie | 1 Siedler, 250 Gold | Kriegskunst 1 | units.json Z. 35-67 |
| Krieger | Kriegerakademie | 1 Siedler, 500 Gold, 1 Pferd | Kriegskunst 3 | units.json Z. 68-101 |
| Ritter | Kriegerakademie | 1 Siedler, 1000 Gold, 1 Pferd | Kriegskunst 7 | units.json Z. 102-135 |
| Paladin | Kriegerakademie | 1 Siedler, 2000 Gold, 10 Mana, 1 Pferd | Kriegskunst 10 | units.json Z. 136-171 |
| Kurzbogenschütze | Kriegerakademie | 1 Siedler, 250 Gold | Kriegskunst 2 | units.json Z. 172-203 |
| Bogenschütze | Kriegerakademie | 1 Siedler, 500 Gold | Kriegskunst 4 | units.json Z. 204-235 |
| Langbogenschütze | Kriegerakademie | 1 Siedler, 1000 Gold | Kriegskunst 6 | units.json Z. 236-267 |
| Armbrustschütze | Kriegerakademie | 1 Siedler, 2000 Gold | Kriegskunst 8 | units.json Z. 268-300 |

Tabelle Diebesgilde (6):

| Einheit | Gebaeude | Kosten | Voraussetzung | Beleg |
|---|---|---|---|---|
| Streuner | Diebesgilde | 1 Siedler, 100 Nahrung, 50 Gold | keine | units.json Z. 301-330 |
| Gauner | Diebesgilde | 1 Siedler, 250 Gold | Heimlichkeit 1 | units.json Z. 331-363 |
| Dieb | Diebesgilde | 1 Siedler, 500 Gold | Heimlichkeit 3 | units.json Z. 364-396 |
| Meisterdieb | Diebesgilde | 1 Siedler, 750 Gold | Heimlichkeit 5 | units.json Z. 397-429 |
| Kundschafter | Diebesgilde | 1 Siedler, 1000 Gold | Heimlichkeit 8 | units.json Z. 430-462 |
| Waldläufer | Diebesgilde | 1 Siedler, 2000 Gold | Heimlichkeit 10 | units.json Z. 463-495 |

Tabelle Stellmacher (13):

| Einheit | Gebaeude | Kosten | Voraussetzung | Beleg |
|---|---|---|---|---|
| Handkarren | Stellmacher | 100 Holz, 15 Metall, 15 Leder, 15 Wolle, 1 Siedler, KEINE Waren | keine | units.json Z. 496-535; Handbuch Z. 838-855 |
| Einspänner | Stellmacher | 250 Holz, 100 Metall, 200 Leder, 200 Wolle, 1 Pferd, 2 Siedler | Wagenbau 3 | units.json Z. 536-579 |
| Zweispänner | Stellmacher | 500 Holz, 150 Metall, 250 Leder, 250 Wolle, 2 Pferde, 2 Siedler | Wagenbau 7 | units.json Z. 580-623 |
| Handelskarawane | Stellmacher | 500 Holz, 250 Metall, 200 Gold, 500 Wolle, 500 Leder, 10 Siedler, 15 Pferde | Wagenbau 2 | units.json Z. 624-668 |
| Große Handelskarawane | Stellmacher | 1000 Holz, 500 Metall, 400 Gold, 1000 Wolle, 1000 Leder, 20 Siedler, 30 Pferde | Wagenbau 6 | units.json Z. 669-713 |
| Siedlerkarren | Stellmacher | 200 Holz, 80 Metall, 150 Leder, 100 Wolle, 4 Pferde, 5 Siedler, 300 Nahrung | Wagenbau 1 | units.json Z. 714-758; Handbuch Z. 935-953 |
| Belagerungsturm | Stellmacher | 800 Holz, 50 Metall, 500 Leder, 10 Pferde, 5 Siedler | Wagenbau 4 | units.json Z. 759-799 |
| Ramme | Stellmacher | 500 Holz, 150 Metall, 100 Leder, 10 Pferde, 5 Siedler | Wagenbau 5 | units.json Z. 800-840 |
| Großer Belagerungsturm | Stellmacher | 1200 Holz, 80 Metall, 800 Leder, 15 Pferde, 7 Siedler | Wagenbau 6 | units.json Z. 841-881 |
| Große Ramme | Stellmacher | 1100 Holz, 300 Metall, 250 Leder, 20 Pferde, 10 Siedler | Wagenbau 7 | units.json Z. 882-922 |
| Balliste | Stellmacher | 600 Holz, 200 Metall, 300 Leder, 10 Pferde, 10 Siedler | Wagenbau 8 | units.json Z. 923-963 |
| Katapult | Stellmacher | 1500 Holz, 200 Metall, 1000 Leder, 20 Pferde, 10 Siedler | Wagenbau 9 | units.json Z. 964-1004 |
| Großes Katapult | Stellmacher | 1900 Holz, 300 Metall, 1400 Leder, 25 Pferde, 15 Siedler | Wagenbau 10 | units.json Z. 1005-1045 |

Bestaetigung der Koordinator-Angaben (nachgelesen, nicht neu gemessen): Handkarren steht auf
"Stellmacher" (units.json Z. 498), Siedlerkarren ebenfalls (Z. 716). Handkarren kostet 100 Holz /
15 Metall / 15 Leder / 15 Wolle / 1 Siedler und hat `waren: []` (Z. 506). Siedlerkarren verlangt
Forschung "Wagenbau" Stufe 1 (Z. 727-730). Beides deckt sich mit dem Handbuch (Z. 838-855 bzw.
Z. 935-953). KEIN WIDERSPRUCH.

### 1.2 Mehrfachbau (data/buildings.json, Feld "max_je_siedlung")

| Gebaeude | max_je_siedlung | Kategorie | Mehrfach je Siedlung? | Beleg |
|---|---|---|---|---|
| kriegerakademie | 1 | Ausbildung | nein | buildings.json Z. 236 |
| diebesgilde | 1 | Ausbildung | nein | buildings.json Z. 252 |
| stellmacher | 1 | Ausbildung | nein | buildings.json Z. 268 |
| bibliothek | 1 | Sonstiges | nein | buildings.json Z. 372 |
| haus | null | Sonstiges | ja | buildings.json Z. 381 |
| schmiede | (mehrfach_moeglich true) | Werkstatt | ja, fertigt parallel | buildings.json Z. 185-186 |
| bogenbauer | (mehrfach_moeglich true) | Werkstatt | ja, fertigt parallel | buildings.json Z. 202-203 |
| naehstube | (mehrfach_moeglich true) | Werkstatt | ja, fertigt parallel | buildings.json Z. 220-221 |
| holzfaeller, steinmetz, erzmine, tempel, farm, goldmine, schafszucht, rinderfarm, pferdezucht, jaeger | (kein Feld) | Produktion | keine Obergrenze gesetzt | buildings.json (Feld fehlt) |
| verteidigungswall | (kein Feld) | Verteidigung | keine Obergrenze gesetzt | buildings.json (Feld fehlt) |
| lager | (kein Feld) | Sonstiges | keine Obergrenze gesetzt | buildings.json Z. 393-407 |

Wichtig zum Lager: buildings.json Z. 396-398 fuehrt "Lager" als reine Uebersicht ("gibt einen
Ueberblick ueber alle in der Siedlung befindlichen Waren und Einheiten") und vermerkt ausdruecklich:
"ob es ein eigenstaendiges Bauwerk ist, ist nicht ausdruecklich belegt." Ein Lager hat KEINE
Kapazitaetszahl. Mehrere Lager bewirken nichts.

### 1.3 Was rechnet eine Ausbaustufe (src/gebaeude_wirkung.py + data/gebaeude_wirkung.json)

- `gebaeude_stufe(siedlung, gebaeude)` (gebaeude_wirkung.py Z. 109-118) liefert die HOECHSTE
  Ausbaustufe eines Gebaeudes in EINER Siedlung; 0 = nicht gebaut. Ein Feld ohne gespeicherte
  Stufe gilt als Stufe 1 (Z. 40-42, 100-106).
- `ausbildungsstaette(siedlungen, einheit)` (Z. 218-228) nimmt die hoechste Stufe ueber ALLE
  uebergebenen Siedlungen.
- `max_stufe(gebaeude)` (Z. 121-128) liest die Obergrenze aus data/gebaeude_wirkung.json:
  Verteidigungswall 10, Kriegerakademie/Diebesgilde/Stellmacher/Bibliothek je 5, Haus 4
  (gebaeude_wirkung.json Z. 34-42). Die Zahlen 5 und 4 sind als VORSCHLAG gekennzeichnet; belegt
  ist nur, dass die Staetten Stufen haben.
- WICHTIG (Ist-Luecke): Die Ausbaustufe rechnet heute auf KEINE Zeitwirkung. Die Ausbildungsdauer
  in `spieloekonomie.ausbildung_start` (spieloekonomie.py Z. 495) ist fest
  `REGELN["pilot_ausbildung_minuten"] * 60` = 20 Minuten * 60 = 1200 s (data/spieloekonomie.json
  Z. 34, als VORSCHLAG). Die Handbuchregel "je hoeher die Stufe, desto schneller" ist damit im
  Code NOCH NICHT umgesetzt. Der alte `bonus_system.get_training_time` (mit building_level-Faktor,
  bonus_system.py Z. 83-89, 146-150) wird von `ausbildung_start` NICHT aufgerufen.

---

## 2. Handbuch-Abgleich (Regel "ein Hersteller je Karte genuegt")

| Aussage (Auftrag 30.10.2026) | Quelle + Zitat | Urteil |
|---|---|---|
| "Je EIN Stellmacher pro Karte genuegt" | Handbuch S. 15, Textfassung Z. 504-506: "In jeder Deiner Siedlungen kann jeweils nur eine Kriegerakademie, eine Diebesgilde und ein Stellmacher gebaut werden. Die Gebäude werden stufenweise ausgebaut. Je höher die Stufe, desto schneller werden dort Einheiten ausgebildet." | BELEGT, mit einer Praezisierung: die Obergrenze ist "eine JE SIEDLUNG", nicht "eine je Reich/Karte". Ein zweiter Stellmacher in einer ANDEREN Siedlung ist laut Handbuch erlaubt (bis zu 6 Siedlungen, Handbuch Z. 311-312). "Pro Karte" ist im Remake = "je Siedlungskarte", also deckungsgleich. |
| "Je EIN Bogenmacher pro Karte genuegt" | Handbuch S. 14, Z. 460-462 (Bogenbauer = Werkstatt fuer Fernwaffen) und Z. 469-470: "Je mehr Fertigungsgebäude Du errichtest, desto mehr Waren werden gleichzeitig angefertigt." | WIDERSPRUCH: "Bogenmacher" = "Bogenbauer", eine WERKSTATT (kein Ausbildungsgebaeude). Das Handbuch erlaubt und belohnt mehrere Werkstaetten explizit durch Parallelfertigung. |
| "Je EIN Item-Hersteller pro Karte genuegt" | Handbuch S. 14, Z. 471-475: "Du gibst 10 Schwerter in Auftrag. Für ein Schwert benötigt Dein Schmied 20 Minuten. Wenn Du in Deiner Siedlung zwei Schmieden gebaut hast, werden immer zwei Schwerter gleichzeitig in dieser Zeit gefertigt. Um den gesamten Auftrag abzuschließen benötigst Du also statt 200 nur 100 Minuten." | WIDERSPRUCH: Item-Hersteller = Schmiede / Bogenbauer / Naehstube. Mehrere davon fertigen laut Handbuch parallel. |
| "Mehrere machen nur bei Farm und Pferdezucht Sinn, weil sie die Produktion erhoehen" | Handbuch S. 10, Z. 353-368: Farm (Nahrung, Grasland 4 / Steppe 2), Pferdezucht (Pferde, Grasland 3 / Steppe 1,5). Kein Satz im Handbuch nennt eine Obergrenze oder eine Sonderstellung von Farm/Pferdezucht. 2005er Fassung (rohstoffe.php.txt) nennt nur die Ertraege, keine Mehrfachregel. | NICHT BELEGT als Handbuchregel. Es ist die Design-Absicht von Daniel (VORSCHLAG-Status). Konsequenz im Handbuch ist, dass JEDES Produktionsgebaeude seinen Ertrag je Stunde liefert; eine ausdrueckliche Obergrenze gibt es fuer Produktionsgebaeude nicht. |
| "Handkarren ausschliesslich beim Stellmacher; vorher gar nicht produzierbar" | Handbuch S. 15, Z. 501: "Zum Bau von Karren und Belagerungswaffen benötigst Du einen Stellmacher". data/units.json Z. 498: Handkarren `gebaeude` = "Stellmacher". | BELEGT. |
| "Lagerkapazitaet reicht nicht" (die Meldung, die der Spieler las) | Handbuch S. 9, Z. 302-304: "Im Lager kannst Du dir einen Überblick über alle in der Siedlung befindlichen Waren und Einheiten verschaffen." Es gibt im Handbuch KEINE Lagerkapazitaet als Sperre. | WIDERSPRUCH zur Deutung als "Kapazitaet": das Lager ist eine Uebersicht, keine Kapazitaet. Die Sperre war ein fehlender Rohstoff, nicht das Lager. Die Meldung im Code hiess bis 30.10.2026 "Lokales Lager reicht nicht." und nannte den Rohstoff nicht (siehe Abschnitt 3). |

Zusatzbefund (kein Glaetten): Daniels Regel fasst "Stellmacher / Bogenmacher / Item-Hersteller"
zu EINER Gruppe zusammen. Im Handbuch sind das ZWEI verschiedene Kategorien:
- Stellmacher = Ausbildungsgebaeude, 1 je Siedlung (BELEGT, deckt Daniels Regel ab).
- Bogenbauer / Schmiede / Naehstube = Werkstaetten, mehrfach + parallel (BELEGT, widerspricht
  Daniels Regel fuer diesen Teil).

---

## 3. Was passiert heute bei zwei Stellmachern (Code gelesen, nicht ausgefuehrt)

Gleiche Siedlung: ein zweiter Stellmacher wird ABGELEHNT. Zwei getrennte Pfade sperren das:
- `spielschicht.bauen` (spielschicht.py Z. 304-307): wenn `max_je_siedlung` eine positive Zahl ist
  und `gebaeude_stufe >= grenze`, kommt "gibt es hoechstens 1x je Siedlung (belegte Originalregel)."
- `main.bauen_auf_karte` (main.py Z. 312-318): dieselbe Sperre, Wortlaut "hoechstens 1x je Siedlung
  (belegte Originalregel) — hier steht schon eines. Stattdessen ausbauen."

Verschiedene Siedlungen: je ein Stellmacher in Siedlung A und B ist erlaubt (die Obergrenze ist
"je Siedlung"). Was er bewirkt bzw. nicht bewirkt:

- Ausbildungstempo: `ausbildung_start` rechnet die Dauer FEST mit `pilot_ausbildung_minuten` (20
  Min), unabhaengig von der Stufe UND unabhaengig davon, wie viele Stellmacher es gibt
  (spieloekonomie.py Z. 495). Ein zweiter Stellmacher macht die Ausbildung NICHT schneller.
- Parallelitaet: die Warteschlange liegt JE ORT unter `ort["ausbildung"]`; ein neuer Auftrag
  beginnt erst, wenn der letzte Auftrag DERSELBEN Staette in DEMSELBEN Ort fertig ist
  (spieloekonomie.py Z. 492: `freie_zeit = max(... for a in neu["ausbildung"] if a["gebaeude"] == geb)`).
  Zwei Siedlungen mit je einem Stellmacher bilden also unabhaengig parallel aus — aber jede
  Siedlung braucht ihre eigenen Rohstoffe, Siedler und Ausruestung VOR ORT (ausbildung_start
  prueft `gebaeude_stufe(ort, geb)`, spieloekonomie.py Z. 479).
- Ansichts-Inkonsistenz (echter Befund): die Ausbildungsansicht prueft GLOBAL
  (`gebaeude_wirkung.ausbildungsstaette(self.state.settlements, key)`, main.py Z. 6373), der
  Kern prueft VOR ORT (`_train_unit` -> `ausbildungsstaette([ort], key)`, main.py Z. 6466, und
  `ausbildung_start` -> `gebaeude_stufe(ort, geb)`, spieloekonomie.py Z. 479). Steht der
  Stellmacher nur in Siedlung B und ist Siedlung A aktiv, zeigt die Ansicht den Ausbilden-Knopf,
  aber der Kern lehnt mit "braucht Stellmacher ... noch nicht gebaut" ab. Die Ansicht ist damit
  ortsblind.

Die eigentliche Sperre aus dem Spielbericht (kein Handkarren baubar, Meldung klang nach
"Lagerkapazitaet"): Das war `verbrauchen` (spieloekonomie.py Z. 282-307). Bis 30.10.2026 warf es
nur "Lokales Lager reicht nicht." und nannte den Rohstoff nicht. Seit 30.10.2026 ruft es
`fehlbestand.text` auf (Z. 291-297) und meldet z. B. "Lokales Lager reicht nicht: holz fehlt 62.80
(37.20 von 100)" (Format aus fehlbestand.py Z. 123-139). Die Berechnung des Koordinators (Holz >= 100
im Ort noetig; bei 37,2 Holz abgelehnt) ist damit im Code abgebildet. Die Ansicht zeigt die
ROHSTOFF-Kosten (Holz/Metall/Leder/Wolle) bislang jedoch NICHT an — nur Waren (Ausruestung) und
Forschung (main.py Z. 6383-6394). Deshalb kann der Spieler vor dem Klick nicht sehen, dass Holz
fehlt.

---

## 4. Entwurf

### 4a Zuordnung Einheit -> Gebaeude

Keine Datenanpassung noetig. data/units.json ist korrekt und belegt (Abschnitt 1.1):
Kriegerakademie 9, Diebesgilde 6, Stellmacher 13. Die Menue-Trennung in drei Ansichten
("Kaserne" -> Kriegerakademie, "Stellmacher", "Diebesgilde") existiert seit 30.10.2026 bereits
(main.py Z. 6318-6334). Der Handkarren steht damit NICHT mehr in der Truppenausbildung.

### 4b Regel fuer Mehrfachbau je Gebaeudetyp

| Gebaeudetyp | Regel | Begruendung | Kennzeichnung |
|---|---|---|---|
| Ausbildungsstaetten (Kriegerakademie, Diebesgilde, Stellmacher) | hoechstens 1 je Siedlung | Handbuch S. 15, Z. 504-505 | BELEGT (bereits im Code gesperrt) |
| Bibliothek | hoechstens 1 je Siedlung | Handbuch S. 12, Z. 404 | BELEGT (bereits im Code gesperrt) |
| Werkstaetten (Schmiede, Bogenbauer, Naehstube) | mehrere erlaubt, fertigen parallel | Handbuch S. 14, Z. 469-475 | BELEGT |
| Produktionsgebaeude (Holzfaeller, Steinmetz, Erzmine, Tempel, Farm, Goldmine, Schafszucht, Rinderfarm, Pferdezucht, Jaeger) | mehrere erlaubt, jeder liefert seinen Ertrag | kein Handbuchsatz nennt eine Obergrenze; der Ertrag ist je Gebaeude belegt (S. 10) | VORSCHLAG (Mehrfachbau selbst NICHT BELEGT, aber folgerichtig) |
| Haus | mehrere erlaubt, +5 Siedler je Haus | Handbuch S. 11, Z. 383-384 | BELEGT |
| Verteidigungswall | hoechstens 1 je Siedlung | nur ein Wall hat Sinn (Stufe); kein Handbuchsatz nennt eine Obergrenze | VORSCHLAG |
| Lager | keine Wirkung, reine Uebersicht | Handbuch S. 9, Z. 302-304; buildings.json Z. 396-398 | BELEGT (als Ansicht), Kapazitaet NICHT BELEGT |

Entscheidung fuer Daniel (offen): "pro Karte" im Sinne von "pro Siedlung" ist belegt. Soll ein
Stellmacher tatsaechlich nur EINMAL IM REICH stehen (statt einmal je Siedlung), waere das eine
bewusste Remake-Abweichung gegenueber Handbuch Z. 504-505 und muss als solche gekennzeichnet
werden. Vorschlag: bei "je Siedlung" bleiben (deckt die Handbuchregel und Daniels Absicht, dass
"einer genuegt", ab — mehr als einer bringt laut Handbuch ja nur in einer zweiten Siedlung etwas).

### 4c Ausbildungsansicht (was sichtbar sein muss)

Je Einheit, gruppiert nach Gebaeude (die drei bestehenden Ansichten), in EINER Zeile bzw. einem
Block:

1. Name, Icon, Rolle (Ladung/GS fuer Karren, Schlagkraft/Mauerschaden fuer Belagerung,
   LE/AT/PA/TP/SK fuer Kaempfer/Kundschafter) — vorhanden (main.py Z. 6354-6363).
2. Kosten vollstaendig: Rohstoffe (z. B. Handkarren "100 Holz, 15 Metall, 15 Leder, 15 Wolle"),
   Siedler, Pferde/Nahrung wo vorhanden — FEHLT HEUTE (nur Waren werden gezeigt).
3. Warenbedarf (Ausruestung) mit Soll/Ist — vorhanden (main.py Z. 6383-6389).
4. Fehlbestand LIVE gegen das Ortslager, je Rohstoff, mit Soll/Ist:
   "holz fehlt 62.80 (37.20 von 100)" ueber `fehlbestand.fehlbestand` + `fehlbestand.text`
   (fehlbestand.py Z. 101-139). Der Ausbilden-Knopf ist gesperrt, solange ein Rohstoff fehlt,
   und der Grund steht daneben — FEHLT HEUTE (Fehlbestand kommt erst nach dem Klick als Exception).
5. Ausbildungszeit: Dauer je Einheit in Minuten. Da das Handbuch KEINE Ausbildungsdauer nennt
   (Pruefstand-Befund, skill nebelseetal-remake), ist der Pilotwert 20 Minuten je Einheit
   (data/spieloekonomie.json Z. 34) als VORSCHLAG sichtbar zu machen, plus die Stufe der Staette
   (z. B. "20 Min, Stellmacher Stufe 1"). Sobald die Stufenregel umgesetzt ist (4b), zeigt die
   Ansicht die stufenabhaengige Dauer.
6. Bestand "Anzahl X vor Ort · Reich Y" — vorhanden (main.py Z. 6369).

### 4d Fehlt das Gebaeude

Nicht leere Liste, sondern Hinweis:
- Steht die Staette in KEINER Siedlung: Menuepunkt fehlt (bereits so, main.py Z. 611-635,
  `menu_sichtbar`). Zusaetzlich zeigt die Kaserne den Hinweis "Baue eine Kriegerakademie"
  (main.py Z. 3632-3635, Berater).
- Steht die Staette in einer ANDEREN Siedlung als der aktiven: je Einheit den Hinweis
  "braucht Stellmacher — hier nicht gebaut (steht in <Name>)" statt des Ausbilden-Knopfes.
  Das schliesst die Ortsblindheit aus Abschnitt 3. Heute steht dort nur "braucht <Staette>"
  (main.py Z. 6395-6398), aber die globale Pruefung in Z. 6373 zeigt trotzdem den Knopf —
  WIDERSPRUCH, der in Schritt 4 unten behoben wird.
- Steht die Staette und es fehlt nur Forschung/Waren/Rohstoff: Knopf gesperrt, Grund daneben,
  nie eine leere Liste.

---

## 5. Umsetzungsschritte (klein, einzeln pruefbar)

Kein Schritt loescht bestehende Pruefdateien. Alle Angaben in src/main.py und src/spieloekonomie.py
sowie die Daten in data/units.json bleiben unveraendert, soweit nicht ausdruecklich genannt.

1. Kosten je Einheit in der Ausbildungsansicht anzeigen (src/main.py `_render_ausbildung`):
   Rohstoffkosten und Siedler aus data/units.json `kosten` als eigene Zeile.
   Pruefzusage: eine fensterlose Pruefung belegt, dass die Ansicht fuer Handkarren den Text
   "100 Holz · 15 Metall · 15 Leder · 15 Wolle · 1 Siedler" enthaelt; alle bestehenden
   Pruefdateien bleiben gruen.

2. Fehlbestand LIVE vor dem Klick (src/main.py `_render_ausbildung`): gegen das ORTSLAGER
   (`fehlbestand.fehlbestand` + `fehlbestand.text`) rechnen; Knopf gesperrt mit dem Text
   "holz fehlt 62.80 (37.20 von 100)", solange etwas fehlt.
   Pruefzusage: ein Ort mit 37.2 Holz zeigt genau diesen Text und einen gesperrten Knopf; ein Ort
   mit >= 100 Holz zeigt den freien Knopf. (Deckt exakt den gemeldeten Spielbericht ab.)

3. Ausbildungszeit je Einheit anzeigen (src/main.py): Dauer = pilot_ausbildung_minuten (20 Min,
   VORSCHLAG) plus Stufe der Staette.
   Pruefzusage: die Ansicht nennt fuer Handkarren "20 Min" und die Stufe des Stellmachers; der
   VORSCHLAG-Charakter ist im Text markiert.

4. Ortsbezug der Ansicht korrigieren (src/main.py `_render_ausbildung` und `_train_unit`):
   die Ansicht prueft gegen die AKTIVE Siedlung (`ausbildungsstaette([ort], key)`), nicht gegen
   `self.state.settlements`.
   Pruefzusage: Stellmacher nur in Siedlung B, aktive Siedlung A -> Knopf gesperrt mit
   "braucht Stellmacher — hier nicht gebaut"; aktive Siedlung B -> Knopf frei. Der Kern und die
   Ansicht stimmen damit ueberein (heute WIDERSPRUCH, Abschnitt 3).

5. Stufe -> Tempo umsetzen (src/spieloekonomie.py `ausbildung_start`, Z. 495): die Dauer mit der
   Stufe skalieren (je hoeher die Stufe, desto schneller). Kein Handbuchwert vorhanden, daher
   VORSCHLAG-Formel und als VORSCHLAG in data/spieloekonomie.json dokumentieren.
   Pruefzusage: Stellmacher Stufe 2 bildet schneller aus als Stufe 1 (Dauer sinkt messbar); die
   Handbuchregel "je hoeher die Stufe, desto schneller" (Z. 505-506) ist damit erstmals im Code
   erfuellt.

6. Zweiten Stellmacher in derselben Siedlung weiter sperren (Verifikation, kein Umbau): die beiden
   Pfade spielschicht.py Z. 304-307 und main.py Z. 312-318 greifen bereits.
   Pruefzusage: ein Test baut einen zweiten Stellmacher in derselben Siedlung und bekommt
   "hoechstens 1x je Siedlung (belegte Originalregel)". Bestehende Pruefdateien bleiben gruen.

7. Werkstaetten-Mehrfachbau beibehalten (kein Umbau, Schutz vor Rueckfall): Schmiede, Bogenbauer,
   Naehstube bleiben mehrfach baubar und fertigen parallel.
   Pruefzusage: das Handbuchbeispiel ist gruen — 10 Schwerter mit zwei Schmieden dauern 100 statt
   200 Minuten (Handbuch S. 14, Z. 471-475).

8. Meldungstext "Lager" entgiften (src/spieloekonomie.py, nur Text): die Meldung "Lokales Lager
   reicht nicht:" bleibt technisch korrekt, aber die Ansicht zeigt den Fehlbestand VOR dem Klick
   (Schritt 2). Kein Text mit "Kapazitaet" einfuehren, weil das Handbuch keine Lagerkapazitaet
   kennt (Abschnitt 1.2).
   Pruefzusage: nirgends erscheint "Lagerkapazitaet" oder "Kapazitaet"; die Ablehnung nennt den
   fehlenden Rohstoff mit Soll/Ist.

---

## 6. Was dieses Papier NICHT belegt

- Ausbildungsdauer je Einheit: Das Handbuch nennt KEINE Ausbildungsdauer (Pruefstand-Befund).
  Der Wert 20 Minuten ist VORSCHLAG (data/spieloekonomie.json, pilot_ausbildung_minuten).
- Anzahl der Ausbaustufen der drei Ausbildungsstaetten und der Bibliothek: Handbuch belegt nur,
  dass es Stufen gibt; die Zahl 5 ist VORSCHLAG (data/gebaeude_wirkung.json Z. 24-27, 34-42).
- Die Tempo-Formel je Stufe ("je hoeher, desto schneller"): belegt ist nur DASS es so ist,
  nicht WIE viel schneller. Jede konkrete Formel ist VORSCHLAG.
- Ob Produktionsgebaeude (Farm, Pferdezucht, Holzfaeller, Steinmetz, Minen, Tempel, Schafszucht,
  Rinderfarm, Jaeger) beliebig oft je Siedlung baubar sind: KEIN Handbuchsatz belegt das. Belegt
  ist nur der Ertrag JE Gebaeude. Daniels Aussage "mehrere nur bei Farm und Pferdezucht sinnvoll"
  ist eine Design-Entscheidung (VORSCHLAG), keine Handbuchregel.
- Ob der Verteidigungswall nur einmal je Siedlung stehen darf: NICHT BELEGT (VORSCHLAG).
- Eine "Lagerkapazitaet" als Spielmechanik: existiert im Handbuch nicht. Lager ist eine Ansicht.
- Der exakte Wortlaut der Original-Fehlermeldung bei fehlenden Rohstoffen: nicht erhalten; der
  heutige Text ist ein Remake-Wortlaut.
- "Bogenmacher" als Begriff: das Handbuch nennt das Gebaeude "Bogenbauer" (S. 14); die Auswertung
  ORIGINAL_Einheiten_Waren_Rohstoffe.md nennt es "Bogner" (buildings.json Z. 204).
