# Entwurf: Wegzeit, Kampfablauf und Weltlage im Nebelseetal-Remake

> ## ⚠ GEPRÜFT AM 31.10.2026 — VOR DEM BAUEN LESEN
>
> Dieses Papier ist ein **VORSCHLAG** des starken Modells. Es wurde am 31.10.2026 gegen Handbuch
> 2009, Vorversion 2006 und den Code geprüft. Ergebnis: **§1 (Wegzeit) und §3 (Weltlage) sind
> brauchbar, §2 (Kampfablauf) ist in Teilen falsch** und darf so nicht umgesetzt werden.
>
> **Prüfbericht:** `docs/PRUEFUNG_ENTWURF_WEGZEIT_KAMPF_20261031.md` (jede Aussage mit Quelle)
>
> Die sechs falschen Stellen in §2 im Kurzüberblick:
> 1. „Wallstufenwerte fehlen“ — sie stehen im Handbuch selbst (Z. 1216–1252) **und** in `data/buildings.json`.
> 2. „sonst halbierter Schaden“ — die Truppen **ziehen sich zurück, der Kampf ist unentschieden** (Z. 1213–1215).
> 3. „Zweikampfformel ist Vorschlag“ — wörtlich belegt (Z. 1296–1309), gilt aber für das **Handbuch-Modell**.
> 4. Erschöpfung und „10 Sequenzen“ — beides **belegt** (Z. 1324–1328, Z. 1274–1278), nicht offen.
> 5. „Punkteformel Vorschlag“ — **belegt** (Handbuch S. 5; `src/punkte.py` rechnet so).
> 6. „`src/kampf.py` mit `_zweikampf`, `_geraeteverluste`“ — diese Funktionen stehen in
>    `src/kampf_alt_handbuch_2009.py`; `kampf.py` folgt dem **neueren Forum-Original**.
>
> Und in §3: „`movements` ist heute immer leer“ ist falsch — `main.py` legt Bewegungen an
> (Z. 5707) und wertet die Ankunft aus (Z. 6937); daneben läuft der vollständige Auftragspfad
> `self.auftraege` (`src/auftraege.py`). **Zwei Bewegungssysteme**, siehe Entscheidung E3.
>
> Die wirklich offenen Entscheidungen stehen in §6 des Prüfberichts (**E1–E5**), nicht in der
> Tabelle §5 dieses Papiers.


## 1. Wegzeit (c)

### 1.1 Formel

Belegt: Der Geschwindigkeitswert GS gibt die Reisegeschwindigkeit einer Einheit an (Z. 1103-1104). Zeitangaben gelten für eine Strecke, Rückkehr dauert doppelt so lange (Z. 1136-1141). Eine Zahlenformel nennt das Handbuch nicht.

Vorschlag:

- Distanz d = |dx| + |dy| + 20 * |dz|
  - dx, dy: Differenz der X-/Y-Koordinate innerhalb derselben Dimension.
  - dz: Differenz der Dimensionsnummer. Jede Dimension zählt als 20 Felder, weil eine Dimension ein 20x20-Gitter ist (Portal-Screenshot GameStar web_1838856).
- Dauer in Spielstunden = (2 * d) / GS
- Tempo je GS-Punkt: 0,5 Felder pro Spielstunde.
- Einheit mit GS 5 schafft 2,5 Felder/h, Einheit mit GS 35 schafft 17,5 Felder/h.

Begründung: Der Faktor 2 ist nötig, damit eine mittlere Reise mit GS 5 etwa 6 Stunden dauert und damit bei Spieluhrfaktor 180 rund 2 Minuten Echtzeit sichtbar ist. Ohne Faktor wären langsame Einheiten für strategische Angriffe zu schnell.

### 1.2 Beispiele

Alle Echtzeiten bei Spieluhrfaktor 180: 1 Spielstunde = 20 Sekunden Echtzeit.

| Distanztyp | d in Feldern | Einheit | Dauer Spielstunden | Dauer Echtzeit |
|---|---|---|---|---|
| nah | 6 | Buergerwehr GS 5 | 2,4 h | 48 s |
| nah | 6 | Waldlaeufer GS 35 | 0,343 h | 6,9 s |
| mittel | 16 | Buergerwehr GS 5 | 6,4 h | 2:08 min |
| mittel | 16 | Waldlaeufer GS 35 | 0,914 h | 18,3 s |
| weit | 32 | Buergerwehr GS 5 | 12,8 h | 4:16 min |
| weit | 32 | Waldlaeufer GS 35 | 1,83 h | 36,6 s |

Bewertung: Langsame Einheiten lohnen sich nur fuer kurze Transporte. Schnelle Einheiten sind fuer Angriffe und weit entfernte Ziele klar im Vorteil. Keine Reisedauer ist unspielbar kurz oder unertraeglich lang.

### 1.3 Rueckkehr

Belegt: Rueckkehr dauert doppelt so lange (Z. 1136-1141). Die obige Dauer gilt fuer eine Strecke. Ein Hin- und Ruecktransport dauert also 4 * d / GS.

## 2. Kampfablauf (d)

### 2.1 Ablaufplan

| Schritt | Regel | Quelle/Status | Anzeige fuer Spieler |
|---|---|---|---|
| 1. Auftrag starten | Einheiten auswaehlen, Ziel waehlen, Anzahl eingeben, Kosten werden angezeigt | Z. 1114-1119 | Auftragsmaske mit Einheiten, Ziel, Kosten, Wegzeit |
| 2. Ankunft | Einheiten erreichen Ziel; Kampf beginnt, wenn Ziel feindlich | Vorschlag | Meldung "Einheiten erreichen Ziel"; Kampf startet automatisch |
| 3. Vorrunde Wall | Verteidiger mit Wall: SK der angreifenden Einheiten gegen Wallstufe. Vorschlag: hoechster SK muss Wallstufe erreichen, sonst halbierter Schaden in Sequenz 1 | SK belegt als Schlagkraft zum Durchbrechen der Verteidigung (Z. 1080-1107); Wallstufenwerte fehlen | Status "Wall wird angegriffen", SK-Vergleich, Wallbalken |
| 4. Kampfsequenzen | Zweikampf-Ketten: AT gegen PA, Schaden = TP minus RS, Minimum 1 Schaden. Tod unter LE 1, Flucht unter LE 5 (Mut entscheidet) | Einzelwerte belegt (Z. 1080-1107); genaue Zweikampfformel ist Vorschlag, Code _zweikampf vorhanden | Sequenzzaehler, Lebensbalken, Trefferprotokoll, Verluste |
| 5. Fluchtpruefung | Fluchtchance 40 % + 5 % je Kampfsequenz; Einheit flieht bei LE < 5, Mut entscheidet | Z. 1330-1338 | Meldung "Einheit X flieht", aktuelle Fluchtchance |
| 6. Erschoepfung | Vorschlag: nach 10 Sequenzen endet der Kampf unentschieden, wenn keine Seite geflohen oder besiegt ist | Nicht belegt, Vorschlag gegen Endlosschlacht | Meldung "Erschoepfung: Kampf endet unentschieden" |
| 7. Beute | Nur mit Karren (Z. 1332). Karrenladung: Handkarren 40, weitere Karren 100 / 250 (botkern). Vorschlag: Beute = Rohstoffe des Ortslagers, soweit Karrenkapazitaet reicht, maximal 50 % des Ortslagers | Beutetransport belegt, Beuteanteil Vorschlag | Beuteliste: Rohstoffart, Menge, beladene Karren |
| 8. Verluste | Verlierer verliert Karren und Belagerungswaffen; unentschieden kostet nichts (Z. 1330-1338). Getoetete Einheiten sind weg | Belegt | Verlustliste, Geraeteverlust |
| 9. Punkte | Kriegspunkte -> Gesamtpunktzahl; Projektsieg bei 300 Gesamtpunkten. Punkteformel Vorschlag | Projektregel; Formel nicht belegt | Kampfbericht mit Punktegewinn |

### 2.2 Code-Abdeckung

Im Projekt vorhanden (Prompt): `src/kampf.py` mit `_geraeteverluste`, `_verluste_zaehlen`, `_zweikampf`. Damit sind Kernlogik fuer Zweikampf und Verluste bereits gebaut.

Es fehlt:

- Verdrahtung in die Oberflaeche (Prompt).
- Ablaufsteuerung fuer Sequenzen und Flucht.
- Wallschwellen und Erschoepfung.
- Beuteberechnung und Beladung.
- Punktevergabe.
- Anzeige aller Schritte als Kampfprotokoll.

## 3. Weltlage (e)

### 3.1 Aufbau der Partiewelt

Belegt: Welt ist ein Gitter (X, Y) je Dimension; 20 Dimensionen; Koordinaten der Form (15-18--9) = X-Y-Z (Portal-Screenshot). Eigene Welt gruen, fremde Reiche rot (Spielanleitung 2005, portal.php.txt). Hoechstens 6 Siedlungen je Spieler (Z. 311-312). Neue Siedlung bekommt eine Karte per Zufall, nie zweimal dieselbe (Z. 313-315).

Vorschlag:

- Eine Einzelspieler-Partie spielt in einer aktiven Dimension mit 20x20 Koordinaten.
- Der Mensch startet mit einer Siedlung auf einem zufaelligen freien Feld.
- Die zwei Bots starten mit je einer Siedlung auf freien Feldern derselben Dimension, Mindestabstand 5 zum Menschen und zueinander.
- Jeder Spieler kann bis zu 6 Siedlungen gruenden. Neue Siedlung: freie Koordinate, Mindestabstand 3 zu fremden Reichen, Mindestabstand 1 zu eigenen Siedlungen. Die 10x10-Baukarte wird per Zufall aus 127 Originalkarten gewaehlt, keine doppelt (belegt fuer Kartenvergabe).
- Die aktive Dimension zeigt alle Siedlungen: eigene gruen, Bots rot.

Abweichung zum Ist-Zustand: `movements` ist heute immer leer (Prompt). Der Entwurf setzt voraus, dass Bewegungen erzeugt und angezeigt werden. `bots` existiert mit zwei Namen; der Entwurf macht sie zu aktiven Siedlungsbesitzern.

### 3.2 Bot-Integration und Gegnerfindung

- Bots starten auf derselben Karte (Wunsch Daniel) und sind sofort als rote Markierung sichtbar.
- Gegner finden:
  - Weltkarte: rote Siedlungen direkt anklicken, Koordinaten ablesen.
  - Ruhmeshalle (Vorschlag): Liste der Bots mit Koordinaten und Punktzahl; Klick springt zur Karte.
  - Nachbarschaft: Auf der 20x20-Karte sind nahe Ziele ohne Portal erreichbar.
- Portal: Portalwechsel kostet 5.000 Mana aus einer Siedlung, hoechstens einmal je 24 h (portal.php.txt). Vorschlag: Der Wechsel verschiebt die ausgewaehlte eigene Siedlung in eine andere Dimension. Dadurch veraendern sich ihre Koordinaten und alle Laufwege zu ihr. Dies erfuellt Daniels Wunsch nach verlegbarem Standort.

### 3.3 Planungsansicht

Ziel: Daniel kann Angriffe planen und waehrend Truppen unterwegs alles sehen.

Anzeige bei Planung:

- Zielkoordinate und Siedlungsname, Entfernung in Feldern.
- Ausgewaehlte Einheiten mit GS.
- Wegzeit in Spielstunden und Echtzeit bei aktuellem Zeitfaktor (Standard 180).
- Ankunftszeit in Spieluhr und realer Uhrzeit.
- Rueckkehrzeit (doppelte Wegzeit) fuer Transportauftraege.
- Kosten des Auftrags.
- Route als Linie auf der Weltkarte.

Anzeige waehrend Bewegung:

- Liste "Laufende Auftraege" (belegt durch Portal-Screenshot) erweitert um: Ziel, Restzeit, Fortschrittsbalken, Ankunftszeit.
- Bei Angriffen: Status "unterwegs", "kaempft", "kehrt zurueck".
- Keine starre Wartezeit ohne Rueckmeldung: Die Restzeit tickt sichtbar.

## 4. Umsetzungsschritte

| Schritt | Inhalt | Pruefzusage |
|---|---|---|
| 1 | Weltkoordinatenmodell: jede Siedlung erhaelt X, Y, Z; Standard 20x20 | Jede Siedlung zeigt Koordinaten; Weltkarte zeigt 20x20-Felder |
| 2 | Wegzeitfunktion nach Formel 2 * d / GS | Fuer Testkoordinaten werden korrekte Spielstunden und Echtzeitminuten angezeigt |
| 3 | Bewegungsauftrag anlegen: Einheiten, Ziel, Karren, Kosten | `movements` erhaelt Eintrag; Einheiten werden aus Ortslager entfernt; Kosten abgezogen |
| 4 | Laufende Auftraege anzeigen | In der Auftragsansicht erscheinen Ziel, Ankunftszeit, Restzeit, Fortschritt |
| 5 | Ankunft verarbeiten | Nach Ablauf der Wegzeit landen Einheiten im Ziellager; Rueckkehr startet automatisch |
| 6 | Kampfprotokoll UI | Kampf startet bei feindlichem Ziel; Sequenzen, Lebensbalken, Flucht, Verluste sind sichtbar |
| 7 | Beute und Geraeteverlust | Sieger erhaelt Rohstoffe nur bei Karren; Verlierer verliert Karren und Belagerungswaffen |
| 8 | Bot-Aktivitaet | Bots bewegen Einheiten mit derselben Wegzeit und kaempfen nach demselben Ablauf |
| 9 | Planungsansicht | Beim Klick auf Ziel werden Route, Wegzeit, Ankunftszeit und Kosten live angezeigt |
| 10 | Portalwechsel | 5000 Mana Kosten, 24 h Sperre, Siedlung wechselt Dimension, Laufwege aendern sich |
| 11 | Kriegspunkte | Kampfbericht zeigt Punktegewinn; Siegbedingung 300 Gesamtpunkte ist erreichbar |

Kein Schritt loescht bestehende Pruefdateien. Alle Schritte sind einzeln pruefbar, ohne Code zu aendern.

## 5. Was die Quellen nicht hergeben

| Luecke | Betroffene Mechanik | Entscheidung Daniel |
|---|---|---|
| Zahlenformel fuer Reisedauer | Wegzeit | Faktor 2, Dimensionsdistanz 20, Manhattan-Distanz |
| Startpositionen und Mindestabstaende | Weltlage | Abstand 5 beim Start, 3 zu Fremden, 1 zu Eigenen |
| Portal verschiebt Siedlung? | Weltlage | Ganze Siedlung umziehen, nicht nur Ansicht |
| Genaue Zweikampfformel | Kampf | Trefferwurf AT/PA, Schaden TP-RS, Minimum 1 |
| Wallschwellenwerte | Kampf | Wallstufe und SK-Schwelle |
| Erschoepfungsgrenze | Kampf | 10 Sequenzen unentschieden |
| Beuteanteil | Kampf | Maximal 50 % des Ortslagers |
| Kriegspunkteformel | Kampf/Punkte | Besiegte Einheit zaehlt mit welchem Wert |
| Ruhmeshalle | Weltlage | Existenz und Inhalt |
| Bot-Verhalten | Weltlage/Bots | Wann Bots angreifen, gruenden, Portal nutzen |

## 6. Querwirkungen

| Mechanik | Betroffen | Was sich dort aendert | Muss angepasst werden? |
|---|---|---|---|
| Wegzeit | Forschung | Forschung laeuft parallel, kein Blockieren. Planung muss Wartezeit mit Forschungsende abstimmen | Nur UI: Restzeit Forschung neben Laufzeit anzeigen |
| Wegzeit | Wirtschaft/Ernte | Einheiten ernten waehrend Reise nicht; Transporte binden Arbeitskraefte | Bot-Planung und UI-Hinweis "Einheit unterwegs" |
| Wegzeit | Siedlergrenze | Siedlerkarren transportiert Siedler zu neuer Siedlung; Gruendung erst nach Ankunft | Gruendungsbutton erst nach Ankunft aktiv |
| Wegzeit | Bots | Bots brauchen identische Wegzeit, sonst unrealistisch | Bot-KI muss Distanz und GS nutzen |
| Wegzeit | Punkte | Keine direkte Aenderung | Nein |
| Wegzeit | Wall/Verteidigung | Verteidiger hat Vorwarnzeit; lange Wege erlauben Reaktion | Verteidigungsplanung der Bots |
| Wegzeit | Beute | Langsame Karren bestimmen Angriffstempo; Eskorte noetig | Planung zeigt Karren-GS und Beuteaussicht |
| Wegzeit | Siedlungsgruendung | Expansionstempo haengt an Siedlerkarren-GS 20 | Gruendungsplanung mit Wegzeit |
| Wegzeit | Auftragsansicht | Muss Restzeit, Ankunft, Fortschritt zeigen | Bestehende Ansicht erweitern |
| Kampfablauf | Forschung | Kampfpunkte koennen Sieg beschleunigen, Forschung nicht blockieren | Punkteanzeige |
| Kampfablauf | Wirtschaft/Ernte | Verluste reduzieren Arbeitskraefte; Beute erhoeht Ortslager | Lagerbestand aktualisieren |
| Kampfablauf | Siedlergrenze | Getoetete Einheiten setzen Hausplaetze frei, Siedlerzahl sinkt | Siedleranzeige aktualisieren |
| Kampfablauf | Bots | Bots muessen Flucht und Verluste korrekt verarbeiten | Bot-Logik |
| Kampfablauf | Punkte | Kriegspunkte aus Kampf entscheiden mit ueber Sieg | Punkteformel festlegen |
| Kampfablauf | Wall/Verteidigung | SK entscheidet ueber Wallwirkung | Wallstufen modellieren |
| Kampfablauf | Beute | Nur Karren erlauben Beute; Karren koennen verloren gehen | Karrenverlust und Beladung |
| Kampfablauf | Siedlungsgruendung | Verlorener Siedlerkarren blockiert Gruendung | Verlustanzeige |
| Kampfablauf | Auftragsansicht | Nach Kampf Auftrag abschliessen, Ergebnis zeigen | Abschlussmeldung |
| Weltlage | Forschung | Portalwechsel unterbricht laufende Forschung nicht; Siedlung bleibt bestehen | Forschung an Siedlung binden |
| Weltlage | Wirtschaft/Ernte | Neue Weltkoordinate veraendert Laufwege, nicht Baukarte | Ortslager bleibt erhalten |
| Weltlage | Bots | Bots sind auf Karte sichtbar, nutzen Portal | Sichtbarkeit und KI |
| Weltlage | Punkte | Entfernung beeinflusst Angriffsfrequenz, nicht Punktewert | Nein |
| Weltlage | Wall/Verteidigung | Lage bestimmt, welche Verteidigung erreichbar ist | Planung |
| Weltlage | Beute | Nahe rote Siedlungen sind lohnende Ziele | Planungsansicht |
| Weltlage | Siedlungsgruendung | Freie Koordinaten begrenzen Expansion | Kartenansicht freie Felder |
| Weltlage | Auftragsansicht | Routen auf Weltkarte anzeigen | Kartenintegration |

## 7. Spielgefuehl

### Wegzeit

- Sieht: Bewegungsauftrag mit Wegzeit, Ankunftszeit, Fortschrittsbalken waehrend der Reise.
- Fuehlt: Vorbereitung und Vorfreude; schnelle Einheiten geben das Gefuehl von Tempo, langsame Karren machen Logistik spuerbar.
- Zieht sich: Lange Rueckwege doppelter Dauer ohne Abkuerzung; deshalb Planung mit Rueckkehrzeit sichtbar.

### Kampfablauf

- Sieht: Sequenz fuer Sequenz Lebensbalken, Treffer, Fluchtmeldungen, Beute und Verluste.
- Fuehlt: Jede Entscheidung hat sichtbare Folgen; Fluchtchance erzeugt Spannung.
- Zieht sich: Zu viele Sequenzen ohne Erschoepfung wuerden langweilen; deshalb Erschoepfung nach Vorschlag.

### Weltlage

- Sieht: 20x20-Karte mit eigenen gruenen und feindlichen roten Siedlungen, Routen und Portalkosten.
- Fuehlt: Uebersicht und Kontrolle; Entfernungen werden verstaendlich, Portalumzug ist ein teurer strategischer Hebel.
- Zieht sich: Wenn Bots zu weit weg sind, wirkt die Karte leer; deshalb Mindestabstaende und rote Sichtbarkeit.
