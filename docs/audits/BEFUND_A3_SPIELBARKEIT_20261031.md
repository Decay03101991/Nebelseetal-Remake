## Tabelle
| Groesse | belegter Wert | Wirkung bei x180 (gerechnet) | Urteil |
|---|---|---|---|
| Produktion je Gebaeude und Gelaende | Holzfäller Wald 4/Std, Steppe 2/Std; Steinmetz Berg 4, Hügel 2; Erzmine Berg 3, Hügel 1,5; Tempel Nebelsee 5, alle außer Sumpf 1; Farm Grasland 4, Steppe 2; Goldmine Berg 3, Hügel 1,5; Schafszucht Grasland 3, Steppe 1,5; Rinderfarm Grasland 3/3, Steppe 1,5/1,5; Pferdezucht Grasland 3, Steppe 1,5; Jäger Wald 2/2, Steppe 1/1 (Handbuch 2009 S.10) | 4/Std = 1 Einheit alle 15 Spielmin = 5 Echtsek.; 2/Std = 10 s; 3/Std = 6,7 s; 1,5/Std = 13,3 s; 5/Std = 4 s; 1/Std = 20 s | spielbar, aber sehr schnell; braucht Lager-/Abholmechanik (VORSCHLAG) |
| Siedlerzuwachs | 1 Siedler/Spielstunde, Grenze 10 je neuer Siedlung, +5 je Haus (Handbuch 2009 S.11) | 1 Siedler alle 20 Echtsek.; Grenze 10 in 200 s (3 m 20 s); mit 1 Haus Grenze 15 in 300 s (5 min) | spielbar (schnell, Grenze bremst) |
| Forschungsdauer | neue Stufe² in Stunden (Handbuch 2009 S.12) | Stufe 2: 4 h = 80 s; Stufe 3: 9 h = 180 s (3 min); Stufe 5: 25 h = 8 m 20 s; Stufe 10: 100 h = 33 m 20 s | spielbar bis mittlere Stufen; hohe Stufen zäh |
| Ausbildungszeiten | nicht belegbar (im mitgelieferten Material keine Einheitendauer) | nicht rechenbar | nicht beurteilbar |
| Kriegspunkte je Einheit | feste Liste: Bürgerwehr 1, Kämpfer 2, Krieger 4, Ritter 8, Paladin 16, Kurzbogenschütze 2, Bogenschütze 4, Langbogenschütze 8, Armbrustschütze 10, Belagerungsturm 2, Ramme 3, Großer Belagerungsturm 4, Große Ramme 5, Balliste 6, Katapult 7, Großes Katapult 8, Streuner 1, Gauner 2, Dieb 4, Meisterdieb 8, Kundschafter 10, Waldläufer 16; Karren 0 (Handbuch 2009 S.5) | kein x180-Effekt; Punktwert fällt bei Ausbildung an und entfällt bei Verlust | spielbar |
| Verteidigungsanlagen | Ausbaustufe³; Beispiel Palisade Stufe 4 = 64 Kriegspunkte (Handbuch 2009 S.5) | kein x180-Effekt; Punkte fallen sofort bei Ausbau an | spielbar |
| Verhältnis Kriegs- zu Forschungspunkten | KP = Summe Einheitenwerte + Wall³; FP = Summe Forschungsstufen³; Gesamt = (KP + FP) / 2 (Handbuch 2009 S.4–5/6) | Formelverhältnis durch x180 unverändert; beide Punktquellen werden beschleunigt, aber ein fairer Vergleich hängt an den nicht belegten Ausbildungszeiten | spielbar; Balance nicht abschließend prüfbar |

## Bewertung statt Sieg
| Auszeichnung | Kennzahl | Rechenweg | Passung zum Original |
|---|---|---|---|
| Feldherr | Kriegspunkte | Summe aller Militär-/Spionageeinheiten nach belegter Liste + Verteidigungsanlage Stufe³ (Handbuch 2009 S.5) | Bildet das genannte Ziel „großer Feldherr“ ab (Handbuch 2009 S.3); die Kennzahl ist die belegte militärische Stärke |
| Forscher | Forschungspunkte | Summe aller Forschungsstufen³ (Handbuch 2009 S.4) | Bildet das genannte Ziel „friedlicher Forscher“ ab (Handbuch 2009 S.3); exakt die belegte Forschungspunktformel |
| Haendler | Handelspunkte — Kennzahl fehlt im Handbuch 2009; nur in der VORVERSION 2006 belegt | ZUSAMMENFUEHRUNG: 1 Handelspunkt je 100 Gold Handelserloes, kleine Betraege werden mitgerechnet; Verfall 1 Punkt je 24 Stunden ohne Handelseinkommen (Spielanleitung_2005/punktesystem.php.txt, VORVERSION 2006). Ziel „einflussreicher Händler“ ist im Handbuch 2009 S.3 belegt | Passt zum Haendler-Ziel, aber für das 2009er Remake fehlt die Kennzahl; Vergleich mit Bots nur möglich, wenn Bot-Handel existiert |
| Gesamtherrscher | Gesamtpunkte | (Kriegspunkte + Forschungspunkte) / 2; Abrundung bei ungerader Summe VORSCHLAG (Handbuch 2009 S.5/6; src/punkte.py) | Entspricht der belegten Ruhmeshallen-Rangfolge (Handbuch 2009 S.4) |

Die Auszeichnungsnamen sind VORSCHLAG; die genannten Kennzahlen und Rechenwege sind belegt.

## Wann endet ein Lauf
- Zeitlimit (VORSCHLAG): Vorteil: klares, planbares Ende; Auszeichnungen werden zu einem festen Zeitpunkt vergeben; fair gegen Bots. Nachteil: kann mitten in Forschung/Ausbau abbrechen. Empfohlene Zahl: 120 Echtminuten = 360 Spielstunden = 15 Spieltage bei x180.
- Erreichte Auszeichnung (VORSCHLAG): Vorteil: zielorientiertes Ende, passt zu „eigene Ziele“ (Handbuch 2009 S.3). Nachteil: bei mehreren Zielen uneindeutig; die Haendler-Kennzahl fehlt im 2009er Handbuch und kann daher als Endbedingung ausfallen.
- Freies Weiterspielen bis alle Siedlungen verloren (VORSCHLAG): Vorteil: volle Freiheit, kein künstliches Ende. Nachteil: kein Abschluss und damit keine Bewertung; kann sehr lange dauern; einziges Ende ist der Totalverlust.
- Empfehlung: Zeitlimit mit anschließender Auszeichnungsbewertung; danach optional freies Weiterspielen. Begründung: Das Handbuch nennt keine Siegbedingung (Handbuch 2009 S.3), also ist ein neutrales Zeitende besser als ein künstliches Punktziel.

## Drei Stellschrauben
- Zeitfaktor (VORSCHLAG): zentraler Faktor 180 belassen; für langsamere Läufe x60 (1 Spielstunde = 60 Echtsekunden), für schnelle Tests x300 (1 Spielstunde = 12 Echtsekunden). Keine Handbuchrate wird geändert, nur der Multiplikator.
- Startbedingungen (VORSCHLAG): belegte Startwerte 10 Siedler, 100 Holz, 100 Steine unangetastet lassen (Handbuch 2009 S.7); stattdessen Startkarte garantieren: 5x5 Kacheln mit mindestens 1 Bibliotheksplatz (Grasland/Steppe/Nebelsee, Handbuch 2009 S.12) und 4 bebaubaren Nicht-Sumpf-Feldern (Sumpf unbebaubar, Handbuch 2009 S.11).
- Kartengroesse (VORSCHLAG): statt 20 Dimensionen (Handbuch 2009 S.3) für den Einzelspieler 1 Dimension mit 6 Welten (1 eigene + 5 Bot-Siedlungen, passend zu maximal 6 Siedlungen, Handbuch 2009 S.3). Verkleinert nur den Limbus, keine Originalzahl.

## Fehlende Zahlen
- Ausbildungszeiten: nicht belegbar; das mitgelieferte Material enthält keine Dauer je Einheit. Deshalb ist die Balance zwischen Kriegspunkten und Forschungsdauer nicht abschließend beurteilbar.
- Bot-Punkte: `bot.punkte` ist Zufall (`src/botkern.py` Z. 150) und nicht belegbar. Ersatz: Bot-Forschungspunkte = Summe der Bot-Forschungsstufen³; Bot-Kriegspunkte = Summe(Bot-Einheiten × belegter Einheitenwert) + Bot-Wallstufe³; Bot-Gesamtpunkte = (Bot-FP + Bot-KP) // 2 (Handbuch 2009 S.4–5/6; src/punkte.py). Erst danach kann das Schutzband ±20 % bis 299 fair verdrahtet werden.
- Handelspunkte: fehlen im Handbuch 2009; belegt nur in der VORVERSION 2006 (Spielanleitung_2005/punktesystem.php.txt).
- Zielzahl 300: Die Zielzahl 300 als Sieg ist verworfen; sie ist nur die belegte Schutzgrenze (Handbuch 2009 S.5/6). Der entsprechende VORSCHLAG im Code muss ersetzt oder entfernt werden.

## Was das für den Code bedeutet
Der Bot braucht einen persistenten Datenstand aus Einheiten, Wallstufe und Forschungsstufen und muss seine Punkte aus den belegten Formeln statt aus einem Zufallswert ableiten. Die Zielzahl 300 wird nicht als Sieg verwendet, sondern durch ein Zeitlimit mit Abschlussbewertung ersetzt. Die drei Stellschrauben sollten als zentrale Konfiguration vor die Handbuchwerte gelegt werden, damit keine Originalrate im Datenmodell verändert wird.