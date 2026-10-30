# Gebäude, Aufbau und Freischaltung im Original (ausgelesen 30.10.2026)

**Quelle:** `docs/original/Spielanleitung_2009_Textfassung.txt` — Seiten 9–14 (Zeilen 330–460 im
Textsatz; die Datei markiert jede Seite mit `===== Seite N =====`). Wörtliche Zitate sind in
Anführungszeichen, Seitenzahl in Klammern.
**Zweck:** Daniel: „kannst du mal schauen, wie das mit dem Gebäudeaufbau und dem Freischalten
nacheinander im Originalspiel aufgebaut war" … „es gibt Abschnitte die einzelne Gebäude und deren
Funktion erklären … daraus können wir viel schließen."

---

## 1. Die Reihenfolge ist im Original NICHT eine Gebäudekette, sondern eine Freischaltung über die Bibliothek

Der Aufbau in der Anleitung, Seite für Seite:

| Seite | Inhalt |
|---|---|
| 9 | Die Siedlungsseite hat **Buttons, die in Bereiche führen** — „beispielsweise in die Kriegerakademie in der Einheiten ausgebildet werden können, oder in die Bibliothek in der Du neue Wissensgebiete erforschen kannst" |
| 10 | Tabelle **Rohstoffproduktion**: jedes Gebäude, welches Gelände, wie viel Ertrag pro Stunde |
| 11 | Regel: jedes Gebäude produziert auf **zwei** Geländearten unterschiedlich viel; **Sümpfe sind unbebaubar**; **1 neuer Siedler pro Stunde**, Grenze **10 je neuer Siedlung, +5 je Haus** |
| 12 | **Forschung**: Bibliothek bauen → Button „Forschung" erscheint; Ausbau in Stufen; Dauer und Kosten |
| 13 | Beispiel Baukunst 2→3 = 9 Stunden; Kosten verdoppeln sich je Stufe; während der Studien ist der Forschungsbereich **der Siedlung** blockiert |
| 14 | **Waren**: erst Waffen/Rüstungen produzieren (Schmiede, Bogenbauer, Näherei), dann Militäreinheiten |

**Kern der Freischaltung (Seite 12, wörtlich):**
1. „Um Forschung zu betreiben musst Du in Deiner Siedlung zunächst eine **Bibliothek** bauen. Dies
   kannst Du über den Button **„Bauen"** im **Siedlungsmenü** tun."
2. „Sie kann nur auf **Grasland, Steppe oder Nebelseen** errichtet werden. **In jeder Siedlung kann
   nur eine einzige Bibliothek gebaut werden.**"
3. „Verfügt Deine Siedlung über eine Bibliothek, **erscheint im Siedlungsmenü der Button
   „Forschung"**."
4. „Mit jeder Stufe, die Deine Bibliothek ausgebaut wird, stehen Dir **weitere
   Forschungsmöglichkeiten** in ihr offen."
5. „Welche Voraussetzungen Du für die Forschungen benötigst, kannst Du unter **„Voraussetzungen"**
   im Hauptmenü erfahren."

Damit ist Daniels Wunsch („Forschung erst als Menüpunkt, wenn eine Bibliothek steht") **original
belegt** — es ist im Original kein Sonderfall, sondern die normale Siedlungslogik. Das haben wir am
30.10. so gebaut.

## 2. Was die Forschungen freischalten (Seite 12)

„Forschungen sind wichtige Voraussetzungen, **für Einheiten, Waffen, Gebäude und weitere
Forschungsmöglichkeiten**. Manche erhöhen die Produktivität Deiner Siedlungen, andere ermöglichen
**den Bau neuer Gebäude und Einheiten** oder steigern die Effektivität Deiner Kampfeinheiten."

→ Die Freischaltung läuft also **über Forschungsstufen**, nicht über eine feste Gebäudereihenfolge.
Für uns heißt das: `data/units.json` (`voraussetzung`) und `data/buildings.json`
(`voraussetzung`) sind die richtige Stelle — und `research.json` (Feld `voraussetzung`, z. B.
„Bibliothek 1") die Bedingung darüber.

## 3. Harte Zahlen aus dem Abschnitt (alle wörtlich belegt)

| Regel | Wert | Seite |
|---|---|---|
| Forschungsdauer | **neue Stufe² in Stunden** („Ein Forschungsauftrag dauert (Neue Stufe*Neue Stufe) in Stunden") | 12 |
| Forschungsstufe steigt | **erst nach Ablauf** der Zeit („Während der gesamten Studienzeit bleibt die Stufe … auf ihrem alten Wert") | 13 |
| Kosten je Forschungsstufe | **verdoppeln sich** (Stufe 1 = 50 Holz → 100 → 200 → 400 …) | 13 |
| Blockade | während der Studien in **dieser Siedlung** kein Ausbau und kein zweiter Auftrag | 12/13 |
| Abbruch | investierte Zeit **und** Rohstoffe sind verloren | 12 |
| Bibliothek-Ausbau | mit jeder Stufe teurer, jede Stufe schaltet Forschungen frei | 12 |
| Siedlergrenze | 10 je neuer Siedlung, **+5 je Haus**, 1 Siedler/Stunde Zuwachs | 11 |
| Gelände | jedes Produktionsgebäude hat **zwei** bevorzugte Geländearten, **Sumpf unbebaubar** | 10/11 |

## 4. Erträge je Gebäude und Gelände (Seite 10, wörtlich)

| Gebäude | Rohstoff | Wald | Steppe | Berg | Hügel | Grasland | Nebelsee | sonst |
|---|---|---|---|---|---|---|---|---|
| Holzfäller | Holz | 4 | 2 | – | – | – | – | – |
| Steinmetz | Stein | – | – | 4 | 2 | – | – | – |
| Erzmine | Metall | – | – | 3 | 1,5 | – | – | – |
| Tempel | Mana | – | – | – | – | – | 5 | alle außer Sumpf 1 |
| Farm | Nahrung | – | 2 | – | – | 4 | – | – |
| Goldmine | Gold | – | – | 3 | 1,5 | – | – | – |
| Schafszucht | Wolle | – | 1,5 | – | – | 3 | – | – |
| Rinderfarm | Leder (+Nahrung) | – | 1,5 / 1,5 | – | – | 3 / 3 | – | – |
| Pferdezucht | Pferde | – | 1,5 | – | – | 3 | – | – |
| Jäger | Nahrung, Leder | 2 / 2 | 1 / 1 | – | – | – | – | – |

## 5. Gegen den Code gehalten (was schon stimmt — nicht neu prüfen)

| Punkt | Befund |
|---|---|
| Forschungsdauer Stufe² | **stimmt schon**: `src/forschung.dauer_stunden()` = Stufe², über `spieldaten.forschungsdauer_stunden` |
| Kostenverdopplung | **stimmt schon**: `src/forschung.py` Kopf nennt „Stufe 1 = 50 Holz, dann 100, 200, 400, 800 …" |
| Bibliothek nur Grasland/Steppe/Nebelsee | **stimmt schon**: `data/buildings.json`, `nur_auf` = genau diese drei, mit Belegvermerk `_belegt_nur_auf` |
| Eine Bibliothek je Siedlung | **stimmt schon**: `max_je_siedlung` = 1, durchgesetzt in `bauen_auf_karte` |
| Forschung erst ab Bibliothek | **am 30.10. gebaut**: Menüpunkt erscheint nur mit Bibliothek |
| Siedlergrenze 10 + 5 je Haus | **stimmt schon**: `gebaeude_wirkung.siedlergrenze_je_siedlung` |
| Sumpf unbebaubar | **stimmt schon**: Geländeregeln (Projektregel seit 05.10.) |

## 6. Widerspruch, den Daniel entscheiden muss

Daniels Vorgabe „höchstens **zwei** Bibliotheken je Spieler, eine dritte nicht" ist **strenger als
das Original**: das Handbuch begrenzt nur **je Siedlung** auf eine Bibliothek und setzt **keine**
Gesamtgrenze über das Spiel. Im Code steht seine Grenze (`BIBLIOTHEK_OBERGRENZE = 2`) und ist dort
als seine Entscheidung kommentiert. **Zu entscheiden:** Original folgen (Grenze fällt, je Siedlung
eine) oder Daniels Grenze behalten.

## 7. Was daraus für den Aufbau folgt (nah am Original)

1. **Siedlungsmenü führt die Bereiche** als Buttons: Dorfzentrum/Übersicht, Bauen (Produktion und
   Verteidigung), Lager, und — sobald gebaut — Kriegerakademie, Stellmacher, Diebesgilde,
   Bibliothek/Forschung. Genau das ist am 30.10. entstanden.
2. **Der Sprung „neue Einheiten" läuft über Forschung**, nicht über Gebäudeketten: Einheit X wird
   freigeschaltet, wenn ihre Forschung die Stufe erreicht (`data/units.json`, `voraussetzung`).
3. **Waren zuerst, dann Truppen** (Seite 14): Schmiede/Bogenbauer/Näherei liefern Waffen und
   Rüstungen, die Ausbildung verbraucht sie. In unserem Code prüft `ausbildung_start` die
   Ausrüstung vor Ort — stimmt mit dem Original.
