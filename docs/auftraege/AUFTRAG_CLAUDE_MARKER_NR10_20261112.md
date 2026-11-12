# AUFTRAG NR. 10 AN CLAUDE (Klasse Opus 5.5): DAS MARKERSYSTEM AUF DER WELTKARTE — BAUFERTIG

| | |
|---|---|
| **Auftrag von** | Hermes Agent „Weltenfresser“, Projekt Nebelseetal Remake, Stand 12.11.2026, 20:2x |
| **Fuer** | Daniel Koessl |
| **Ort im Spiel** | Portalansicht, Gelaendekaestchen (die Weltkarte mit den Doerfern der fuenf Bots) |
| **Vorgaenger** | Deine Antwort auf Auftrag Nr. 4, Teile B1 bis B6 (Markersystem) — **das ist der Auftrag, sie zu bauen** |
| **Umsetzendes Modell** | `deepseek-v4-flash` (schnelles, kleines Modell) |
| **Sprache der Antwort** | Deutsch, mit Zahlen und Koordinaten |
| **Umfang** | Dieser Auftrag ist absichtlich groesser: er soll das Markersystem EINMAL vollstaendig festlegen, damit danach kein zweiter Auftrag noetig ist |

## 1. Warum dieser Auftrag — und was heute dasteht

Du hast in Auftrag Nr. 4 ein Markersystem entworfen (B1 drei Stufen, B2 sechs Umrisse, B3 eigener
Marker, B4 Zustaende, B5 Marsch und Drache, B6 zwei Objekte auf einem Feld). **Gebaut ist davon nur
ein Bruchstueck.** Was heute wirklich im Code steht, gemessen am 12.11.2026:

| Was | Heute | Wo |
|---|---|---|
| Feldgroesse der Weltkarte | **20 bis 46 px**, gerechnet als `max(20, min(46, Breite_der_Spalte // 20))`; ohne gemessene Breite fest **20 px** (400 px Karte) | `_portal_zelle` |
| Raster | 20 x 20 Felder | Code |
| Dorf-Marke | **Burgbild** deiner Fraktion, **92 Prozent** der Feldgroesse (bei 20 px also **18 px**), plus **Wappenabzeichen** unten rechts mit **40 Prozent** (**8 px**) | `data/bot_wappen.json`, `_dorf_marke` |
| Kontrastrahmen | **zwei Rechtecke**: aussen `#120707`, innen `#FFFFFF` (fremde) bzw. Skin-Gold (eigene). Gold allein lag auf Steppe bei 2,15 : 1 und war unsichtbar | `_dorf_ring`, Register 475 |
| Rueckfall ohne Bild | farbiger Kasten mit X in Fraktionsfarbe | `_dorf_kasten` |
| Marschlinie | eigene Optik-Datei `data/marsch_optik.json` (Fassung A), KEINE Strichelung, keine Pfeilspitze in deinem Sinn | `src/marsch_optik.py` |
| Drache / Ruine | als Figur gezeichnet, **nicht** als Raute | `src/drachen.py`, `src/ruinendeckung.py` |
| Auswahl, Bedrohung | Auswahlrahmen als Bild (`kachelrahmen_auswahl.png`); **kein** Bedroht-Abzeichen | Code |
| Doerfer je Karte | bis zu **20** (fuenf Bots mit je bis zu vier Doerfern plus Spieler) | Spielstand |

**Der Kern des Problems:** die Erkennung haengt heute an einem **Bild** (Burg), nicht an einer
**Form**. Bei 20 px ist die Burg 18 px gross und zeigt keine Fraktion — Daniel hat das am 11.11.2026
bestaetigt: „ich erkenne kaum die doerfer oder bots". Deine B2-Idee (sechs unterscheidbare Umrisse)
loest genau das, ist aber nie gebaut worden.

## 2. Was ich von dir brauche (Teil A bis G)

Bitte so, dass `deepseek-v4-flash` es **abschreiben** kann: Zahlen, Koordinaten, Reihenfolgen — keine
Auslegung, keine Gestaltungsdiskussion.

### A) Die sechs Umrisse als ZAHLEN (das Wichtigste in diesem Auftrag)

Zu B2 hast du die Formen benannt (Lilie/Schild, Sechseck, Kreis, Quadrat mit 2 px Ecken, Dreieck
mit Spitze oben, fuenfzackiger Stern). **Jetzt brauche ich je Form die Punktliste**, und zwar in
**Einheitskoordinaten 0..1** (x nach rechts, y nach unten, Ursprung links oben), damit ich sie mit
jeder Feldgroesse multiplizieren kann. Bitte als Tabelle:

| Fraktion | Form | Punkte (x; y) in 0..1 | Anzahl |
|---|---|---|---|
| Menschen | Schild | z. B. (0,50; 0,00) (0,85; 0,10) … | 8 bis 16 |
| Zwerge | Sechseck | | 6 |
| Elfen | Kreis | **Sonderfall: Mittelpunkt + Radius** | – |
| Gnome | Quadrat, Ecken 2 px | Ecken + Eckenradius | 4 |
| Ghule | Dreieck, Spitze oben | | 3 |
| Trolle | Stern, 5 Zacken | **innen/aussen im Wechsel** | 10 |

**Fuer den Kreis und die abgerundeten Ecken:** sag mir, ob ich `create_oval` bzw. `create_polygon`
mit `smooth` nehmen soll oder eine Punktliste mit 16 Punkten. Ich will **eine** Zeichenart je Form,
damit spaeter niemand zwei Wege pflegt.

**Wichtig:** die Form traegt die Fraktion bei **mittlem und kleinem** Marker. Beim grossen Marker
darf die Burg bleiben — sag mir, ob die Burg **dann** noch Fraktionsinfo traegt oder nur Schmuck ist.

### B) Die drei Stufen als Pixelrezept

Zu B1 hast du drei Stufen mit Hoehen 26 / 34 / 50 px genannt. Heute ist das Feld **20 bis 46 px**
gross, also nicht 22 px wie in deiner Annahme. Bitte gib die Stufen **relativ zum Feld** an, damit
sie bei jeder Feldgroesse stimmen:

| Stufe | Feld von … bis | Markerhoehe | Halo | Rand | Innenflaeche | was ist DARIN (bei welcher Groesse) |
|---|---|---|---|---|---|---|
| klein | 20–25 px | ? | 2 / 2 px | | | |
| mittel | 26–37 px | ? | 2 / 2 px | | | |
| gross | 38–46 px | ? | 2 / 2 px | | | |

Dazu drei Fragen, die heute keiner beantworten kann:
1. **Was ist bei 20 px drin?** Bei 20 px Feld und 26 px Marker ragt er 3 px je Seite ueber das Feld
   (deine Regel „Marker = Feld + 4 px" ergibt 24 px, nicht 26). Welche Zahl gilt?
2. **Bleibt das Burgbild im Spiel** (nur grosse Stufe) oder faellt es ganz weg?
3. **Was passiert bei 46 px Feld** — waechst der Marker mit oder bleibt er bei 50 px?

### C) Eigener Marker, Auswahl, Bedrohung

- **Eigener Marker (B3):** Doppelrand Gold `#E0B040` 2 px, innen 1 px Halo und 1 px Gold, **+4 px**
  groesser als ein Bot-Marker derselben Stufe, immer obenauf. **Bitte als Pixelrezept mit
  Reihenfolge** (was wird zuerst gezeichnet?), damit ich es in EINER Schleife abarbeiten kann.
- **Auswahl (B4):** zusaetzlicher Creme-Ring 2 px ausserhalb des Halos, darum 1 px Halo
  („Zielscheibe"), bei 22 px Feld waechst der Marker auf 32 px — **bei 20 und bei 46 px welche
  Zahl?** Und: der 2-px-Creme-Innenrahmen um das Feld — liegt er **auf** der Geländekachel?
- **Bedroht (B4):** Dreieck-Abzeichen oben rechts, 8 / 10 / 12 px je Stufe, Fuellung Orange
  `#E8582A`, 1 px Halo-Umriss. **Ankerpunkt** bitte genau (verschoben um wie viel gegen die Ecke?),
  und ob es den Marker vergroessert.

### D) Marschlinie, Drache, Ruine

Heute zeichnet `src/marsch_optik.py` eine Linie ohne Strichelung. Deine B5-Regel:

- **Marschlinie:** 3 px Creme mit je 1 px Halo-Ummantelung (zusammen 5 px), Spitze als gefuelltes
  Dreieck 10 bis 14 px, Start als Quadrat 6 px.
- **Feindlicher Marsch:** Orange und **gestrichelt** (6 px an, 4 px aus).

**Bitte als Zahlenrezept:** Bei Tk ist eine „Ummantelung" entweder eine zweite, dickere Linie
darunter oder drei Linien. Sag mir, welchen Weg ich nehmen soll, **und ob die Strichelung bei einer
3-px-Linie mit 1-px-Halo noch lesbar ist** (6 an / 4 aus bei 5 px Gesamtbreite ist optisch eng).
Wenn nicht: welche Zahlen?

- **Drache / Ruine (B5):** Raute, auf die Spitze gestellt, Flaeche Halo-dunkel, darin Creme-
  Fluegelsilhouette ab mittel; Ruine dieselbe Raute mit `#8A8178` und eingestuerzter Turmsilhouette.
  **Bitte Kantenlaenge je Stufe** und die Punkte der Raute (4 Punkte, 0..1).
- **Zwei Objekte auf einem Feld (B6):** Reihenfolge ausgewaehlt > eigenes Dorf > fremdes Dorf >
  Drache/Ruine > Marschziel; Dorf + Drache: Drache als Mini-Raute 10 px unten links; Dorf +
  Marschziel: Pfeilspitze endet am Halo-Rand, Dorf traegt das Bedroht-Dreieck.
  **Frage:** verschiebt die Mini-Raute den Dorfmarker, oder liegt sie ueber ihm?

### E) Trefferflaechen und Klick

- Wie gross ist die **Trefferflaeche** eines Markers relativ zum Feld (Feld? Marker? Feld + 4 px)?
- Klick waehlt „immer das oberste Objekt" (B6). **Was ist „oben"** — die Zeichenreihenfolge oder
  eine eigene Prioritaetsliste? Bei zwei Objekten auf einem Feld brauche ich eine **Zahl**, nach der
  ich sortiere.
- Das Seitenpanel zeigt „Auf diesem Feld: Dorf X · Drache" als umschaltbare Reiter. **Wie viele
  Reiter sind hoechstens noetig** (gibt es Felder mit drei Objekten)?

### F) Leistung (bitte beachten, sonst baut flash es langsam)

Eine Weltkarte hat **20 x 20 = 400 Felder** und bis zu **20 Doerfer**. Gezeichnet werden heute
**232 Objekte** je Karte (gemessen: Gelaende, Wege, Rahmen, Burgen, Wappen). Bei jedem Klick und
jedem Ansichtswechsel wird die Karte **neu gezeichnet** (kein Cache).

- **Wie viele Canvas-Objekte** darf ein Marker hoechstens kosten (Halo, Rand, Flaeche, Abzeichen,
  Auswahl)? Nenne die Obergrenze je Stufe.
- Ist es vertretbar, die Formen **einmal als Bild** (Pillow) zu bauen und je Fraktion/Stufe/Groesse
  im Cache zu halten, oder sollen sie **immer** als Canvas-Polygon gezeichnet werden? Beides hat
  Folgen: Bilder skalieren (verboten laut Register 502 fuer Hintergruende, fuer Marker nicht
  entschieden) gegen viele Canvas-Objekte bei jedem Neuzeichnen.

### G) Abnahme (messbar)

| # | Kriterium | Pruefweg |
|---|---|---|
| 1 | Jede der sechs Formen ist bei 26 px Hoehe von jeder anderen zu unterscheiden (nicht nur die Farbe) | Sicht + Vergleich der Punktlisten |
| 2 | Halo gegen Kachel haelt mindestens 3,12 : 1 auf allen sieben Geländearten | WCAG-Rechnung je Geländefarbe |
| 3 | Rand gegen Halo, Flaeche gegen Rand: nenne die Paare und ihre Kontraste | Rechnung |
| 4 | Marker ragt hoechstens so weit ueber das Feld, wie du angibst (Zahl), und verdeckt kein Nachbarfeld | Messung |
| 5 | Der eigene Marker ist ohne Farbe erkennbar (Doppelring) | Sicht bei Graustufen |
| 6 | Marschlinie ist in beiden Faellen (eigen/fremd) ohne Farbe unterscheidbar (Strichelung) | Sicht bei Graustufen |
| 7 | Ein Klick trifft genau ein Objekt, bei zwei Objekten das nach E genannte | Messung |
| 8 | Hoechstens die Zahl aus F an Canvas-Objekten je Marker | Zaehlung `find_all` |

## 3. Regeln fuer deine Antwort

1. **Kein Code, keine Dateien, kein Patch** — aber **Zahlen, Punkte, Koordinaten und Reihenfolgen**
   sind ausdruecklich erwuenscht (das ist der Zweck dieses Auftrags).
2. **`data/` bleibt unberuehrt** — keine neuen Datenschluessel, die es nicht gibt. (Die Optik-Datei
   `data/marsch_optik.json` gibt es; sag, ob die neuen Zahlen dort hineingehoeren.)
3. **Keine Mechanik-Zahlen** (Kosten, Ertraege, Kampfwerte).
4. **Keine fremden Bilder** — benutzt wird, was in `assets/icons/burgen/` und `assets/icons/wappen/`
   liegt.
5. **Keine geratenen Masse.** Unbekanntes als **UNBEKANNT** hinschreiben; ich messe nach.
6. **Umsetzbar fuer `deepseek-v4-flash`:** nur Pillow und Tkinter.
7. Am Ende: **„Was ich nicht geprueft habe"**.

## 4. Was du nicht noch einmal fragen musst

| Groesse | Wert | Quelle |
|---|---|---|
| Feldgroesse Weltkarte | 20 bis 46 px (`max(20, min(46, Spaltenbreite // 20))`) | `_portal_zelle`, gemessen |
| Raster | 20 x 20 Felder | Code |
| Geländearten | sieben (Grasland, Steppe, Wald, Hügel, Berg, Nebelsee, Sumpf) | `data/gelaende.json` |
| Fraktionen | sechs: menschlich, zwergisch, elfisch, Trolle, Ghule, Gnome | `data/voelker.json` |
| Burgbild | 92 Prozent der Feldgroesse (18 px bei 20 px Feld) | `data/bot_wappen.json` |
| Wappenabzeichen | 40 Prozent der Feldgroesse (8 px bei 20 px Feld) | `data/bot_wappen.json` |
| Kontrastrahmen heute | aussen `#120707`, innen `#FFFFFF` bzw. Skin-Gold | `_dorf_ring` |
| Gold auf Steppe | 2,15 : 1 (deshalb der zweite Ring) | Register 475 |
| Objekte je Karte | 232 (gemessen 12.11.2026) | Messung |
| Siedlungskarte | **anderer** Ort: 10 x 10 Felder zu 57 px — hier NICHT gemeint | Register 507/514 |
| Spielstand | `main` = `f01fe68` | `git ls-remote` |
