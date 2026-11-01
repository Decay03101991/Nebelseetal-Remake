# Assets und Weltbild – Entwurf für Hermes, 01.11.2026

## 1. Schneideplan

**BELEGT (Auftrag):** Nebelseetal Remake läuft lokal mit Python 3.14 und tkinter; es gibt zwei eigenständig erzeugte RGBA-Kontaktbögen zu 1448 × 1086 px.
**BELEGT (Bildprüfung):** Beide Dateien besitzen tatsächlich Alphakanäle mit teiltransparenten Kanten. Die Motive liegen dicht beieinander; ein bloßer gleichmäßiger Gitterschnitt wäre nicht überall verlustfrei.
**VORSCHLAG:** Zuerst Einzelmotive freistellen, dann einen nummerierten Kontrollbogen abnehmen, erst danach die Zielgrößen exportieren.

### 1.1 Ausgangsmaterial und Zählrichtung

| Nr.-Bereich | Quelldatei | Raster | Zählung | Ergebnis |
|---|---|---|---|---|
| `burg_01`–`burg_06` | `Nebelseetal_Burgen_Iconset_6er.png` | 3 Spalten × 2 Zeilen | links nach rechts, dann unten | Sechs einzelne PNG-Motive |
| `wappen_01`–`wappen_10` | `Nebelseetal_Wappen_Iconset_10er.png` | 5 Spalten × 2 Zeilen | links nach rechts, dann unten | Zehn einzelne PNG-Motive |

**BELEGT (Bildprüfung):** Bei der Burgen-Grafik liegen die Hauptmotive ungefähr in den Spaltenbändern x=12–483, 485–956 und 965–1441; obere und untere Motive kommen sich an der horizontalen Trennzone entgegen.
**BELEGT (Bildprüfung):** Bei den Wappen liegt die obere Inhaltsreihe etwa bei y=83–512, die untere bei y=542–996; einige seitliche Verzierungen reichen über die rechnerischen Spaltengrenzen.
**VORSCHLAG:** Diese Koordinaten dienen nur der Erkennung der sechs beziehungsweise zehn Zielmotive, niemals als ungeprüfte finale Schnittkonturen.

### 1.2 Schneideverfahren je Blatt

| Schritt | Burgen: 3 × 2 | Wappen: 5 × 2 | Prüfung |
|---|---|---|---|
| Raster | Nominale Spalten bei x≈0/484/960/1448; Zeilentrennung um y≈543 | Nominale Spalten bei x≈0/290/580/870/1160/1448; Zeilentrennung zwischen den Motivzeilen | Nur Orientierung, kein harter endgültiger Schnitt |
| Alphatest | Alpha > 16/255 als vorläufiger Inhalt | Alpha > 16/255 als vorläufiger Inhalt | Schwellenwert ist **VORSCHLAG**, schwache Partikel visuell beurteilen |
| Kontur | Pro Burg eine eigene Maske einschließlich Fahnen, Wasser und sichtbarer Basis | Pro Wappen eigene Maske einschließlich Spitzen, Bänder und Zierrand | Keine Motivteile an Nachbarikon verlieren |
| Berührung | Überlappende oder aneinandergrenzende Motive manuell trennen | Seitliche Schildelemente und Zierbänder manuell zuordnen | Bei Unklarheit nicht automatisch abschneiden |
| Splitter | Isolierte 1-px-Punkte nur nach Sichtvergleich entfernen | Ebenso; kleine Glanzpunkte können beabsichtigt sein | Nie alle kleinen Komponenten pauschal löschen |
| Begrenzung | Nach Maske auf sichtbaren Alpha-Begrenzungsrahmen beschneiden | Nach Maske auf sichtbaren Alpha-Begrenzungsrahmen beschneiden | Vollständige Silhouette bei 100 % und 400 % prüfen |
| Padding | Ringsum mindestens 6 % der längeren Motivkante als transparenter Sicherheitsrand | Derselbe Ansatz | **VORSCHLAG**; nichts darf an Canvas-Kanten kleben |
| Zentrierung | Motiv proportional mittig in quadratische Fläche einpassen | Motiv proportional mittig in quadratische Fläche einpassen | Nie verzerren oder vertikale Spitzen abschneiden |
| Freigabe | Nummerierter Kontrollbogen, Soll-/Ist-Abgleich 6/6 | Nummerierter Kontrollbogen, Soll-/Ist-Abgleich 10/10 | Fehlstellen und Duplikate führen zu Nacharbeit |

**BELEGT (Bildprüfung):** Bei Alpha > 16 finden sich in der Burgengrafik noch sichtbare Pixel unmittelbar an y=542 und y=543; ein gerader Schnitt zwischen diesen Zeilen kann Motive zerteilen.
**BELEGT (Bildprüfung):** Auch die Wappen haben an mehreren nominellen Spaltengrenzen sichtbare Alpha-Pixel; streng rechteckige Fünfer-Schnitte können Zierränder abschneiden.
**VORSCHLAG:** Für solche Grenzfälle eine manuell kontrollierte Vordergrundmaske je Symbol erstellen; bei unklarer Objektzugehörigkeit den Originalkontaktbogen direkt daneben anzeigen.
**VORSCHLAG:** Pixel unter der vorläufigen Alpha-Schwelle nicht blind löschen: Feine Nebel-, Eis- oder Lichteffekte können absichtlich schwach sein.

### 1.3 Exportgrößen und Namensschema

| Export | Dateiname (Muster) | Pixel | Verwendung | Urteil |
|---|---|---:|---|---|
| Burg Weltkarte normal | `burg_01_64.png` bis `burg_06_64.png` | 64 × 64 | Kartenanzeige, gegebenenfalls im Raster herunterskaliert | VORSCHLAG |
| Burg Weltkarte vergrößert | `burg_01_96.png` bis `burg_06_96.png` | 96 × 96 | Hover, Auswahl, Kartenzoom | VORSCHLAG |
| Burg Dialog | `burg_01_128.png` bis `burg_06_128.png` | 128 × 128 | Dorfinfos und Planungsdialog | VORSCHLAG |
| Wappen kompakt | `wappen_01_48.png` bis `wappen_10_48.png` | 48 × 48 | Nachrichten-/Kopfzeile | VORSCHLAG |
| Wappen Karte | `wappen_01_64.png` bis `wappen_10_64.png` | 64 × 64 | Kartenmarker, kleinere UI-Bereiche | VORSCHLAG |
| Wappen Dialog | `wappen_01_128.png` bis `wappen_10_128.png` | 128 × 128 | Botprofil, Handel, Planung | VORSCHLAG |

**VORSCHLAG:** Die maximale Detailversion (128 px) vom freigestellten Original ableiten, die kleinen Varianten jeweils neu aus der hochwertigen Masterdatei skalieren.
**VORSCHLAG:** Interne Master ohne Qualitätsverlust als RGBA-PNG erhalten; keine JPG-Zwischenstufe und keine schwarzen Pixel an halbtransparenten Kanten hineinrechnen.
**VORSCHLAG:** Bildgrößen unterscheiden von tatsächlicher Anzeigegröße: Eine 64-px-Datei darf innerhalb einer 46-px-Kartenzelle kleiner gerendert werden.
**VORSCHLAG:** Auf dunkler und heller Prüffläche, auf Schachbrett und bei Originalgröße kontrollieren; Transparenz allein auf Schwarz zu beurteilen ist nicht ausreichend.

### 1.4 Kontrollbogen und Abnahme

| Kontrollbogen | Darstellung | Ausschlusskriterium |
|---|---|---|
| Burgen | Sechs Einzel-Assets mit Nummer, sichtbarem Schnitt-/Canvasrahmen und nebenstehender Originalposition | Abgeschnittene Fahne, Turmspitze, Mauer, Wasserfall oder Basis |
| Wappen | Zehn Einzel-Assets mit Nummer, sichtbarem Schnitt-/Canvasrahmen und nebenstehender Originalposition | Fehlende Schwertspitze, Geweih, Schildecke oder Schmuckband |
| Vergleich | Originalkontaktbogen neben finalem Export, Zoomansicht und Größenvergleich | Vertauschte Nummerierung, Doppelbelegung oder sichtbarer Rest des Nachbarobjekts |

**VORSCHLAG:** Kontrolle für jedes Motiv dokumentieren: `vollständig`, `sauber transparent`, `lesbar bei 48/64 px`, `Zellrahmen nicht berührt`.
**UNBEKANNT — von Hermes zu liefern:** Tatsächliche Bildlade-/Caching-Technik und der bereits vorhandene Asset-Ordner des aktuellen lokalen Projektstands.

## 2. Zuordnung

**BELEGT (Bild):** `burg_01` zeigt Steinmauern mit blauen Bannern; `burg_02` eine Burg mit roten Dächern; `burg_03` eine weiße goldverzierte Zitadelle.
**BELEGT (Bild):** `burg_04` ist eine dunkle violette Festung, `burg_05` eine grüne Baumfestung, `burg_06` eine eisblaue Kristallburg.
**BELEGT (Bild):** Die zehn Wappen zeigen der Reihenfolge nach Wolf, Rabe, Hirsch, Krone, Turm, Schwerter, Baum, Drache, Mond und Hammer.
**BELEGT (Auftrag):** Sechs Burgenbilder stehen sieben Adressaten (Spieler und sechs Bots) gegenüber; sieben vollständig unterschiedliche Burgmotive sind mit diesem Paket nicht möglich.
**VORSCHLAG:** Ein Burgmotiv vorübergehend doppelt nutzen und den Spieler zusätzlich durch eigenen Rahmen und die eindeutige Kennung „Eigen“ hervorheben; alternativ später ein siebtes Originalmotiv beauftragen.

| Nummer | Datei | Vorschlag für | Begründung am Bild | Sicher? |
|---|---|---|---|---|
| Spieler | `burg_01_64.png` | Eigene Startburg; vorläufig auch Bot 6 | Klassische neutrale Steinburg mit blauen Bannern | VORSCHLAG; Doppelnutzung offen |
| Bot 1 | `burg_03_64.png` | Gorim Goldhand (gierig) | Goldverzierungen, repräsentative weiße Zitadelle | VORSCHLAG |
| Bot 2 | `burg_04_64.png` | Mora Schattenfeder (misstrauisch) | Dunkle Türme, violettes Leuchten | VORSCHLAG |
| Bot 3 | `burg_02_64.png` | Alaric Kronenmund (großspurig) | Hohe Türme und rote Banner, herrschaftlicher Eindruck | VORSCHLAG |
| Bot 4 | `burg_05_64.png` | Silva Wurzelruh (still) | Bäume, grüne Dächer, natürliche Formen | VORSCHLAG |
| Bot 5 | `burg_06_64.png` | Varek Frostschwur (rachsüchtig) | Kalte kristalline Wehrburg; distanzierte Wirkung | VORSCHLAG |
| Bot 6 | `burg_01_64.png` | Nordrik Grauwolf (freundlich) | Solide, offene klassische Steinburg | VORSCHLAG; mit Spieler geteilt |

| Nummer | Datei | Vorschlag für | Begründung am Bild | Sicher? |
|---|---|---|---|---|
| 1 | `wappen_01_48.png` | Bot 6: Nordrik | Weißer Wolf auf blauem Feld, passend zu Blau der Burg | VORSCHLAG |
| 2 | `wappen_02_48.png` | Bot 2: Mora | Schwarzer Rabe vor violettem Grund | VORSCHLAG |
| 3 | `wappen_03_48.png` | Unvergebene freie Fraktion | Hirschmotiv, wirkt naturverbunden | VORSCHLAG |
| 4 | `wappen_04_48.png` | Bot 3: Alaric | Krone auf rotem Feld | VORSCHLAG |
| 5 | `wappen_05_48.png` | Neutrale Orte | Wehrturm, keine eindeutig benannte Person | VORSCHLAG |
| 6 | `wappen_06_48.png` | Bot 5: Varek | Gekreuzte Schwerter, kämpferischer Ausdruck | VORSCHLAG |
| 7 | `wappen_07_48.png` | Bot 4: Silva | Baum und Wurzeln in Grün | VORSCHLAG |
| 8 | `wappen_08_48.png` | Spätere Sonderfestung | Roter Drache auf dunklem Grund | VORSCHLAG |
| 9 | `wappen_09_48.png` | Reserve für spätere Welt | Mond und Sterne | VORSCHLAG |
| 10 | `wappen_10_48.png` | Bot 1: Gorim | Hammer und Berge verweisen auf Handwerk/Erz | VORSCHLAG |

**VORSCHLAG:** Die vier ungenutzten Wappen bleiben exakt `03`, `05`, `08`, `09`; dem Spieler vorerst **kein zusätzliches Bot-Wappen** zuordnen.
**VORSCHLAG:** Bot-ID, Bot-Name, Rahmenfarbe, Burgdatei und Wappendatei aus einer gemeinsamen Zuordnung beziehen, damit niemals mehrere Wahrheiten entstehen.
**UNBEKANNT — von Hermes zu liefern:** Heutige Botnamen und Botfarben aus dem lokalen Arbeitsstand; diese Vorschläge dürfen sie nicht stillschweigend überschreiben.

## 3. Anzeigeorte

**BELEGT (Auftrag):** Das Portal zeigt oben eine Weltkartenliste und darunter die Geländeübersicht der aktuellen Welt; die Oberfläche hat eine dunkle Skin.
**BELEGT (Auftrag):** Bot-Dörfer sind bisher durch Rahmenfarbe plus Bot-Nummer erkennbar; Bot-Wappen/-Festungen sind neu zu planen.
**VORSCHLAG:** Skalierungen und Fallbacks zentral festlegen und an allen Anzeigeorten einheitlich nutzen.

| Anzeigeort | Geplantes Bild und Größe | Fallback bei fehlendem Asset | Darf nicht passieren | Urteil |
|---|---|---|---|---|
| Weltkarte: eigenes Dorf | Burg-Quellexport 64 px, im Feld ca. 32–44 px; eigener Doppelrahmen und „Eigen“ statt Botnummer | Klarer quadratischer Marker mit „Eigen“ | Spieler mit einer Botnummer verwechseln | VORSCHLAG |
| Weltkarte: Bot-Dorf | Burg-Quellexport 64 px, sichtbar ca. 32–44 px; Wappen als Eckabzeichen 12–14 px, Rahmenfarbe und Botnummer | Farbiger Rahmen + Botnummer wie bisher; optional Initialen | Wappen darf Botnummer und Rahmen nicht vollständig verdecken | VORSCHLAG |
| Weltkarte: Auswahl/Zoom | Burg 96 px im separaten Infofeld/Hover, nicht über Nachbarzellen | Name, Nummer, Koordinate in Text | Vergrößerte Burg drückt Kartenraster auseinander | VORSCHLAG |
| Portal: Weltkartenliste oben | Kleines Kartenkennzeichen oder 48-px-Wappen nur wo sinnvoll | Weltkartenname als Text | Botwappen mit Weltkartennamen gleichsetzen | VORSCHLAG |
| Portal: Geländekästchen unten | In belegter Zelle dieselbe Burg-Zuordnung, proportional unter Zellgrenze | Rahmenfarbe und Nummer | Abweichende Bot-ID/Farbe gegenüber Weltkarte | VORSCHLAG |
| Bot-Nachrichten: Absender | Wappen 48 px, daneben Name und Botnummer | Monogramm + Botnummer | Nachricht erscheint unter falscher Identität | VORSCHLAG |
| Handelsdialog | Wappen 48 px, Burg optional 64 px bei Profildetails | Botname, Nummer, Farbmarkierung | Handelsergebnis hängt vom dekorativen Asset ab | VORSCHLAG |
| Kampfseite | Wappen 48 px, Burg optional 96 px im Zielprofil | Textkennung mit Botnummer | Bilder suggerieren aktive Bot-Angriffsfähigkeit dieser Entwicklungsstufe | VORSCHLAG, für später |
| Planungsseite | Wappen 48 px, Burg 128 px im großen Dorfprofil | Name/Koordinate/Nummer als Text | Fehlendes Bild blockiert Missionsplanung | VORSCHLAG, für später |
| Dorfdetaildialog | Burg 128 px, Wappen 48 px nur bei Bots | Standardrahmen, ausgeschriebene Eigentümerkennung | Uneinheitliche Farben zwischen Karte und Detailseite | VORSCHLAG |

**VORSCHLAG:** Botnummer bleibt selbst bei vollständig geladenen Bildern sichtbar; Bilder ergänzen die Orientierung, ersetzen sie nicht.
**VORSCHLAG:** Alle Orte verwenden denselben einmal zugeordneten Bot-Datensatz und zeigen bei Bildfehler weiterhin einen bedienbaren Zustand.
**UNBEKANNT — von Hermes zu liefern:** Ob die gegenwärtigen Kampf-/Planungsseiten die genannten Bildflächen bereits besitzen; keine UI-Montage ohne Abgleich.

## 4. Weltbild 20 × 20

**BELEGT (Auftrag):** Die Weltkarte wird auf 20 × 20 Felder ausgelegt; wichtige Fensterbreiten sind 1420 und 1600 px.
**BELEGT (Auftrag):** Die Siedlungskarte innerhalb eines Dorfes bleibt 10 × 10 Felder; beide Raster dürfen nicht verwechselt werden.
**UNBEKANNT — von Hermes zu liefern:** Tatsächliche Kartenbreite nach Berater, Scrollleisten, Abständen und Fensterhöhe des lokalen UI-Arbeitsstands.
**VORSCHLAG:** Für eine überprüfbare Beispielrechnung zunächst pauschal 500 px für Seitenleiste und Breitenreserve ansetzen; dies ist ein **Planungsbudget, kein gemessener Ist-Wert**.

| Fensterbreite | Beispielrechnung für Kartenraum | Rechnerische Maximal-Zelle | Resultierende Kartenhöhe | Einordnung |
|---|---|---|---|---|
| 1420 px | (1420 − 500) / 20 = 46 px | 46 × 46 px | 20 × 46 = 920 px | Nur wenn auch mindestens 920 px Kartenhöhe verfügbar |
| 1600 px | (1600 − 500) / 20 = 55 px | 55 × 55 px | 20 × 55 = 1100 px | Nur wenn auch mindestens 1100 px Kartenhöhe verfügbar |
| Beide | Zellkante = min(verfügbare Kartenbreite / 20; verfügbare Kartenhöhe / 20) | Abzurunden auf ganze Pixel | 20 × tatsächliche Zellkante | Verbindliche Berechnung nach realer UI-Messung |

**VORSCHLAG:** Wenn die Höhe nicht reicht, die 20×20-Weltkarte verkleinern oder im festen Kartenviewport scrollen/zoomen, niemals den Berater überdecken oder in eine zweite Zeile verschieben.
**VORSCHLAG:** Die 64-/96-px-Burgdateien bleiben Quellexporte; im 46-px-Feld bekommt die Burg etwa 34 px, im 55-px-Feld etwa 42 px.

| Inhalt pro belegter Zelle | Beispiel 46 px | Beispiel 55 px | Konfliktlösung |
|---|---|---|---|
| Außenrahmen | 2 px umlaufend | 2 px umlaufend | Gleiche Rahmenfarbe an allen Orten |
| Burg | 34 × 34 px zentral | 42 × 42 px zentral | Silhouette darf Rand nicht überdecken |
| Bot-Wappen | 12 × 12 px oben links | 14 × 14 px oben links | Kleine opake Unterlage für Lesbarkeit |
| Botnummer | Schrift-/Badgefläche ca. 12 × 12 px unten rechts | ca. 14 × 14 px unten rechts | Nicht mit Wappen überlagern |
| Eigene Siedlung | Doppelrahmen + Kurzmarker „Eigen“ im Hover | Entsprechend | Keine Botnummer für den Spieler |
| Freies Feld | Gelände sichtbar, bei Auswahl nur Kontur und Koordinaten | Entsprechend | Keine scheinbar besetzte Zelle erzeugen |

**VORSCHLAG:** In der normalen Zellansicht Burg als Hauptmotiv, Wappen und Nummer als bewusst überlagerte Eckabzeichen anzeigen; volle Symbolgröße erst im Infofenster.
**VORSCHLAG:** Zellinhalt vor dem Zeichnen begrenzen und Clipping testen; die freigestellte Grafik darf keine hit-test-Fläche außerhalb ihrer Zelle beanspruchen.
**VORSCHLAG:** Der ausgewählte freie Zielplatz erhält eine helle Kontur und eine Zeile „Freies Feld (x,y)“; die Zielkoordinate ist vor Bestätigung nochmals sichtbar.
**VORSCHLAG:** Beim Hover nach **0,6 Sekunden** ein Infofeld einblenden (Zeitwert ist Vorschlag, nicht Ist-Stand) mit Eigentümer, Welt, Koordinate, Transferstatus und Kosten.
**VORSCHLAG:** Im Hover bei einem zulässigen Transfer „Dorftransfer: 500 Mana“ anzeigen, aber **500 Mana ist derzeit nur ein Vorschlag**, bis Daniel/Hermes den Wert festlegen.
**VORSCHLAG:** Solange Transferregeln nicht geklärt sind, nur „Transferkosten: UNBEKANNT“ oder eine aus dem echten Spielzustand gelesene Zahl verwenden.
**VORSCHLAG:** Legende außerhalb des Kartenrasters: „Eigenes Dorf“, „Bot-Dorf“, „Freies Feld“, „Ausgewähltes Feld“, „Gesperrt“ und sechs Botfarben mit Nummern.
**VORSCHLAG:** Gleiche Nummer und Farbe im Hover, in der Legende, im Dorfdetail und in Nachrichten verwenden; nicht die Farben einer Karte automatisch anderen Welten gleichsetzen.
**BELEGT (Auftrag):** Bespielbar sind zunächst Midgard und Valhalla, Startwelt ist Midgard; Armageddon, Ragnarök, Utgard und Limbus bleiben als Namen sichtbar, ihre Freischaltlogik ist unbekannt.
**VORSCHLAG:** Nicht bespielbare Karten sichtbar als nicht verfügbar markieren, ohne frei erfundene Eintrittsbedingungen anzuzeigen.
**UNBEKANNT — von Hermes zu liefern:** Echte Transferbeschränkungen, Kollisionsregeln, Weltgrenzen, Koordinatenursprung und Maus-/Hoververhalten im lokalen Arbeitsstand.

## 5. Risiken und Top 10

**VORSCHLAG:** Spielgefühl entsteht vor allem durch Wiedererkennbarkeit, räumliche Zuordnung und durchgängige Rückmeldung; reine Verzierung ohne verlässliche Informationen hat geringeren Nutzen.
**VORSCHLAG:** Die Burg am richtigen Ort, ein sichtbares Wappen in der Nachricht und ein nachvollziehbarer Transfer tragen zur Orientierung bei; aufwendige Lichtanimationen sind zunächst Dekoration.
**BELEGT (Auftrag):** Bots wirtschaften und handeln in dieser Stufe; sie führen noch keine Angriffe und keine Taktik aus.
**VORSCHLAG:** Militärtexte und Bilder lediglich vorbereiten; neue Kampfhandlungen werden nicht durch dieses Papier beauftragt.

| Rang | Maßnahme | Wirkung | Aufwand | Urteil |
|---:|---|---|---|---|
| 1 | Zuverlässige Zuordnung Bot-ID ↔ Farbe ↔ Burg ↔ Wappen | Verhindert falsche Gegner-/Handelspartneranzeige | mittel | VORSCHLAG |
| 2 | Jede Burg und jedes Wappen vollständig freistellen, visuell abnehmen | Verhindert sichtbar beschädigte Assets | mittel | VORSCHLAG |
| 3 | 20×20-Raster bei 1420 und 1600 px ohne Überlauf | Macht Weltkarte überhaupt gut bedienbar | groß | VORSCHLAG |
| 4 | Eigene Siedlung eindeutig von sechs Bots abgrenzen | Verhindert Verwechslung bei Doppelverwendung | klein | VORSCHLAG |
| 5 | Gleicher Botmarker auf Karte, Handel und Nachrichten | Stärkt Wiedererkennung und Vertrauen | mittel | VORSCHLAG |
| 6 | Koordinaten und Transferkosten vor Bestätigung anzeigen | Verhindert versehentliche Ortswechsel | mittel | VORSCHLAG |
| 7 | Vorhandenen Botnummer-Rahmen als robusten Fallback beibehalten | UI funktioniert ohne PNG weiter | klein | VORSCHLAG |
| 8 | Hover mit Dorfname, Nummer und Weltkoordinate | Ermöglicht schnelle Orientierung | mittel | VORSCHLAG |
| 9 | Wappen für Handelsbots passend zu Symbol und Auftreten wählen | Verleiht Botbegegnungen Charakter | klein | VORSCHLAG |
| 10 | 96-/128-px-Grafiken nur in Detailansichten anzeigen | Mehr Atmosphäre ohne Kartenüberfrachtung | klein | VORSCHLAG |

**Risiko R1 – VORSCHLAG:** Ein automatischer Raster-Schnitt schneidet Berührungen falsch; Gegenmaßnahme: Motive einzeln maskieren und kontrollieren.
**Risiko R2 – VORSCHLAG:** Sieben Eigentümer bei nur sechs Burgmotiven erzeugen Dopplungen; Gegenmaßnahme: Eigen-Rahmen oder zusätzliches siebtes Motiv.
**Risiko R3 – VORSCHLAG:** Rahmenfarben können auf der dunklen Skin zu ähnlich wirken; Gegenmaßnahme: unterscheidbare Farbtöne, Symbol und Zahl zusätzlich verwenden.
**Risiko R4 – VORSCHLAG:** Auf dem 20×20-Raster werden Wappen sehr klein; Gegenmaßnahme: Wappen nur als Eckabzeichen und größer im Hover.
**Risiko R5 – VORSCHLAG:** Ein 920- oder 1100-px-Quadrat kann die verfügbare Fensterhöhe überschreiten; Gegenmaßnahme: dynamische Zellgröße/Scrollviewport.
**Risiko R6 – VORSCHLAG:** Unklare Transfer- oder Marschregeln werden durch die Oberfläche scheinbar als bestehend ausgegeben; Gegenmaßnahme: nur aus dem realen Zustand stammende Werte anzeigen.
**Risiko R7 – VORSCHLAG:** Visuelle Aufrüstung wird fälschlich als Bot-Kampf-KI verstanden; Gegenmaßnahme: aktuelle friedliche Botstufe ausdrücklich erhalten.

## 6. Bot-Steckbriefe

**VORSCHLAG:** Alle sechs Namen und Charaktere sind neue Gestaltungsoptionen, keine Behauptung über bestehende Botidentitäten.
**VORSCHLAG:** Für Farben ist eine gut erkennbare Helligkeit auf dunklem Untergrund gewählt. Der tatsächliche Kontrast muss gegen die gemessene UI-Hintergrundfarbe geprüft werden, die hier **UNBEKANNT — von Hermes zu liefern** ist.
**VORSCHLAG:** Nicht allein nach Farbe unterscheiden: Wappenmotiv, Botnummer und Name sind weitere unabhängige Merkmale.

| Bot | Name | Typ | Rahmenfarbe | Burg | Wappen | Charakter in Handel/Kampf | Anrede | Urteil |
|---:|---|---|---|---|---|---|---|---|
| 1 | Gorim Goldhand | gierig | `#E8C66B` Gold | `burg_03` | `wappen_10` | Handelt hart um Preise; im hypothetischen Kampf kalkuliert er Beute. | „Was bietet Ihr?“ | VORSCHLAG |
| 2 | Mora Schattenfeder | misstrauisch | `#C5A6FF` Lavendel | `burg_04` | `wappen_02` | Fragt nach Sicherheiten; im hypothetischen Kampf vermutet sie Fallen. | „Nennt zuerst Euer Anliegen.“ | VORSCHLAG |
| 3 | Alaric Kronenmund | großspurig | `#FF8C99` Rosa-Rot | `burg_02` | `wappen_04` | Prahlt mit seinem Einfluss; im hypothetischen Kampf kündigt er Ruhm an. | „Ihr sprecht mit Alaric.“ | VORSCHLAG |
| 4 | Silva Wurzelruh | still | `#79E2AB` Mintgrün | `burg_05` | `wappen_07` | Antwortet knapp; im hypothetischen Kampf bleibt sie sachlich. | „Ich höre.“ | VORSCHLAG |
| 5 | Varek Frostschwur | rachsüchtig | `#FFAD70` Orange | `burg_06` | `wappen_06` | Vergisst gebrochene Absprachen nicht; im hypothetischen Kampf fordert er Ausgleich. | „Ich erinnere mich an Euch.“ | VORSCHLAG |
| 6 | Nordrik Grauwolf | freundlich | `#71CFFF` Himmelblau | `burg_01` | `wappen_01` | Bietet faire Geschäfte an; im hypothetischen Kampf fordert er einen geordneten Rückzug. | „Willkommen in meinem Dorf.“ | VORSCHLAG |

**VORSCHLAG:** Die Kontrastprüfung soll mindestens normale UI-Lesbarkeit anstreben; bei geringer Differenz zur dunklen Skin einen neutralen hellen Innenstrich ergänzen.
**VORSCHLAG:** Die sechs Farben unterscheiden sich zusätzlich durch Farbton und Symbol; bei Farbsehschwächen müssen Botnummer und Name die Unterscheidung allein ermöglichen.
**VORSCHLAG:** Das blaue `burg_01` wird derzeit auch für die eigene Startburg empfohlen; eigener Doppelrahmen und „Eigen“-Markierung sind deshalb verpflichtender Teil **dieses Vorschlags**.

| Freies Wappen | Bildmotiv | Geplanter Zweck | Urteil |
|---|---|---|---|
| `wappen_03` | Hirsch | Freie spätere Fraktion | VORSCHLAG |
| `wappen_05` | Wehrturm | Neutrale Orte | VORSCHLAG |
| `wappen_08` | Drache | Spätere besondere Festung | VORSCHLAG |
| `wappen_09` | Mond und Sterne | Reserve für spätere Welt oder Fraktion | VORSCHLAG |

**UNBEKANNT — von Hermes zu liefern:** Ob sechs Bots bereits individuelle Namen und Persönlichkeitstexte besitzen; bestehende Festlegungen haben Vorrang.

## 7. Textpaket

**VORSCHLAG:** Jede der folgenden Zeilen ist ein einzelner UI-Satz; Werte in `{geschweiften_klammern}` müssen vor Anzeige durch **tatsächliche** Zahlen beziehungsweise Kennungen aus dem Spiel ersetzt werden.
**VORSCHLAG:** Ist ein Zahlenwert unbekannt oder eine Aktion noch nicht implementiert, darf weder ein Fantasiewert noch eine als „0“ getarnte Unbekannte erscheinen.
**BELEGT (Auftrag):** Die Gründung nennt die Wunschpositionen Holzfäller/Wald (9,9), Steinmetz/Hügel (6,6) und Tempel/Nebelsee (1,2).

| Fall | Fertige Anzeigezeile | Urteil |
|---|---|---|
| Gründung – Wunschgelände vorhanden | „Holzfäller auf Wald (9,9), Steinmetz auf Hügel (6,6) und Tempel auf Nebelsee (1,2) vorgesehen.“ | VORSCHLAG |
| Gründung – Ersatzgelände | „Wunschfeld ({wunsch_x},{wunsch_y}) ist nicht verfügbar; {gebaeude} wird stattdessen auf {gelaende} ({ersatz_x},{ersatz_y}) gesetzt.“ | VORSCHLAG |
| Gründung – kein zulässiger Ersatz | „Für {gebaeude} wurde kein zulässiges Feld gefunden; das Gebäude wurde nicht gesetzt.“ | VORSCHLAG |
| Bot erkannt | „Bot {bot_nummer}: {bot_name}, Dorf ({x},{y}) in {welt}; Handel ist verfügbar.“ | VORSCHLAG |
| Handelsangebot angenommen | „Bot {bot_nummer} hat das Angebot angenommen: {menge_angebot} {ware_angebot} gegen {menge_gegenleistung} {ware_gegenleistung}.“ | VORSCHLAG |
| Handelsangebot abgelehnt | „Bot {bot_nummer} hat das Angebot abgelehnt: {konkreter_ablehnungsgrund}.“ | VORSCHLAG |
| Angriff entsandt – später | „Angriff mit {truppen_anzahl} Truppen auf ({x},{y}) entsandt; Marschdauer: {marschdauer}.“ | VORSCHLAG, derzeit nicht aktiv |
| Angriff angekommen – später | „Angriff mit {truppen_anzahl} Truppen auf ({x},{y}) angekommen; Kampfbericht {bericht_nummer} liegt vor.“ | VORSCHLAG, derzeit nicht aktiv |
| Heimkehr mit Beute – später | „{truppen_heimkehr} Truppen sind nach ({x},{y}) zurückgekehrt und brachten {beute_menge} {beute_ware} mit.“ | VORSCHLAG, derzeit nicht aktiv |
| Kundschafter erfolgreich – später | „Kundschafterbericht zu ({x},{y}): {feind_truppen} Truppen erkannt, Wallstufe {wall_stufe} bestätigt.“ | VORSCHLAG, derzeit nicht aktiv |
| Kundschafter teilweise abgewehrt – später | „Kundschafter bei ({x},{y}) abgewehrt; {erkannte_truppen} Truppen erkannt, Wallstufe {wall_stufe_oder_unbekannt}.“ | VORSCHLAG, derzeit nicht aktiv |
| Kundschafter vollständig abgewehrt – später | „Kundschafter bei ({x},{y}) abgewehrt; Truppenzahl und Wallstufe sind unbekannt.“ | VORSCHLAG, derzeit nicht aktiv |
| Dorftransfer – Bestätigung | „Dorf nach ({ziel_x},{ziel_y}) versetzen? Kosten: {transferkosten_mana} Mana.“ | VORSCHLAG |
| Dorftransfer – Postfach | „Dorftransfer nach ({ziel_x},{ziel_y}) abgeschlossen; {transferkosten_mana} Mana wurden abgezogen.“ | VORSCHLAG |
| Dorftransfer – gesperrt | „Dorftransfer nicht möglich: {aktive_missionen} Missionen sind noch unterwegs.“ | VORSCHLAG |

**VORSCHLAG:** Für den Transfer kann bei Daniels späterer Freigabe `{transferkosten_mana}` den Wert 500 erhalten; derzeit ist dieser Wert nur vorgeschlagen.
**VORSCHLAG:** Ein abgelehnter Handel nennt einen aus dem echten Prüfergebnis stammenden Grund, beispielsweise fehlenden Lagerbestand, nicht einen pauschalen Standardsatz.
**VORSCHLAG:** Bei abgewehrter Spionage niemals eine unbekannte Truppenzahl oder Wallstufe als exakt bekannt ausgeben; die abgestuften Textvarianten bilden das korrekt ab.
**VORSCHLAG:** Die Angriffs-, Heimkehr- und Kundschaftertexte sind Vorlagen für einen späteren Entwicklungsstand; sie schalten kein Bot-Angriffsverhalten frei.

## Offene Fragen an Daniel

| Nr. | Empfehlung zuerst | Zu entscheiden | Urteil |
|---:|---|---|---|
| 1 | Ein zusätzliches siebtes Burgmotiv später ergänzen; bis dahin `burg_01` doppelt mit klarer Eigen-Markierung | Reicht die temporäre Doppelverwendung? | VORSCHLAG |
| 2 | Vorhandene Botnamen und Identitäten beibehalten, wenn Hermes bereits welche festgelegt hat | Dürfen vorgeschlagene sechs Namen stattdessen verwendet werden? | VORSCHLAG |
| 3 | Sechs vorgeschlagene Farbtöne als Startpunkt, Kontrast am echten dunklen Skin prüfen | Gefällt die sichtbare Fraktionsfarbpalette? | VORSCHLAG |
| 4 | Wappen auf der Weltkarte klein, im Hover und in Nachrichten größer darstellen | Soll zusätzlich jedes Dorf einen eigenen Wappenplatz im Detaildialog erhalten? | VORSCHLAG |
| 5 | Transfers nur auf freie zulässige Felder und mit Sperre bei laufenden Missionen anbieten | Welche konkreten Transferbeschränkungen sollen gelten? | VORSCHLAG |
| 6 | 500 Mana nur als Vorschlag, bis freigegeben | Soll der Dorftransfer tatsächlich 500 Mana kosten? | VORSCHLAG |
| 7 | 20×20-Karte höhenabhängig zoombar/scrollbar machen, nicht den Berater verschieben | Soll die ganze Karte ständig sichtbar sein oder ist Scrollen erlaubt? | VORSCHLAG |
| 8 | Militärtexte jetzt nur als spätere Vorlagen verwalten | Soll die Karte schon jetzt Planungs-/Kampfelemente zeigen, obwohl Bots noch nicht angreifen? | VORSCHLAG |

## Was ich nicht wissen kann

- **UNBEKANNT — von Hermes zu liefern:** Der aktuelle lokale Codezustand nach `52f5dab` und unversionierte Änderungen; das öffentliche GitHub steht laut Auftrag auf `954097aa` und ist kein verlässlicher Beleg für diese Sitzung.
- **UNBEKANNT — von Hermes zu liefern:** Echte widgetinterne Maße, verfügbare Kartenhöhe, Skalierungsverhalten und Aufteilung bei 1420/1600 px.
- **UNBEKANNT — von Hermes zu liefern:** Tatsächliche Namen, Kennzahlen, Botfarben, Handelsbedingungen und eventuelle bereits bestehende Icon-Bindungen.
- **UNBEKANNT — von Hermes zu liefern:** Die wirklichen Transferkosten, Portal-Freischaltungen, Kollisions-/Geländeregeln, Koordinatenkonventionen und Laufzeit laufender Missionen.
- **UNBEKANNT — von Hermes zu liefern:** Ob und in welcher Form Kampf- und Planungsseiten schon existieren; Botangriffe und Taktik sind in dieser Stufe laut Auftrag nicht vorgesehen.
- **UNBEKANNT — von Hermes zu liefern:** Exakte Eignung und Vollständigkeit jeder separat freigestellten PNG-Datei; nur die beiden Kontaktbögen wurden hier betrachtet, noch keine Schnitte erzeugt.
- **VORSCHLAG:** Hermes übernimmt nur freigegebene Angaben, prüft Assets und UI an seinem echten lokalen Stand und entscheidet über Umsetzung in S-5 (Weltbild) und S-7 (Bots).
