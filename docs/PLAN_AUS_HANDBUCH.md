# Plan nach dem Original-Handbuch — als Einzelspieler-Spiel

**Grundlage:** `docs/original/Nebelseetal_Spielanleitung_2009.pdf` (24 Seiten).
Seitenangaben sind **Handbuch-Druckseiten**. Jedes Kapitel wird nach drei Fragen abgearbeitet:

1. **Original** — was steht dort?
2. **Einzelspieler** — was wird daraus ohne andere Spieler?
3. **Paket/Stand** — wer baut es, was ist schon da?

Alles, was im Original einen **anderen Spieler** voraussetzt, wird auf **Bots** abgebildet — nicht
gestrichen. Nur reine Netzfunktionen (Chat, Forum, Anmeldung) entfallen.

---

## Übersicht: 24 Seiten → Pakete

| Seite | Thema | Einzelspieler-Kern | Paket | Stand |
|---|---|---|---|---|
| 1 | Das Spiel | Echtzeit-Aufbauspiel, ein Herrscher, eine Start­siedlung | W1d | Code fehlt |
| 2 | Grundlegendes: Ziel, Bildschirmaufbau, Hauptmenü | Überblick + Portal (→ Weltenkarte) | W7 | teils |
| 3 | Nebenbereiche, Punktesystem (Forschung) | Gilde/Ruhmeshalle gegen Bots | W6 | offen |
| 4 | Kriegspunkte, Gesamtpunktzahl | Rechnung 1:1 übernehmen | W6 | offen |
| 5 | Rufpunkte, Götterschutz | Schutz gegen Bots statt Spieler | W5 | offen |
| 6 | Spielübersichtsseite | Siedlungsliste + laufende Aufträge | W7 | teils |
| 7 | Siedlungsübersicht, Baumenü | Karte, Zuwachs, Gebäude setzen/abreißen | W4/W7 | teils |
| 8 | Lager, Siedeln, aufgeben | bis 6 Siedlungen, Karte zufällig | W4 | teils |
| 9–10 | Rohstoffe und Gebäude | 9 Rohstoffe, Geländeertrag, Siedler | W1d/W4 | Daten da |
| 11–12 | Forschung | Dauer Stufe², Kosten verdoppeln | W1d/W4 | Daten da |
| 13 | Waren | 3 Werkstätten, Warteschlangen | W3 | Daten da |
| 14 | Einheiten | 4 Typen, 3 Ausbildungsgebäude | W1d | Daten da |
| 15–17 | Einheitentabelle und Werte | 28 Einheiten, LE…SK | W1d | Daten da |
| 18–19 | Aufträge | Stationieren, Spionage, Transport, Handel, Angriff | W4/W5 | offen |
| 20–22 | Kampf | Vorrunde, Sequenzen, Zweikampf | W2 | **als Nächstes** |
| 23 | Spionage | Bericht gegen Bots | W5 | offen |
| 24 | Ende | — | — | — |

---

## Teil A — Grundlagen (Seite 1–5)

### Seite 1 — Das Spiel
**Original:** Browserspiel, kostenlos, Echtzeit („nicht in Runden"), der Spieler ist Herrscher über
ein mittelalterliches Reich, jedes Reich auf eigener Welt, verbunden durch **Portale**. Start mit
einer Siedlung. Rohstoffe → Gebäude → Forschung → Waffen/Rüstungen → Armee.
**Einzelspieler:** Der Zeitablauf bleibt Echtzeit, wird aber **skalierbar** (Faktor einstellbar:
Original-Tempo bis stark beschleunigt). Das Portal führt nicht zu Spielerwelten, sondern zur
**Weltenkarte mit den fünf Karten** (Kontinent, Nebelwald, Hochfels, Glimmersümpfe, Portalreich).
**Paket:** W1d (Zeitablauf), W5 (Weltenkarte).
**Offen:** Zeitfaktor als Standard (Daniel).

### Seite 2 — Grundlegendes: Spielziel, Bildschirmaufbau, Hauptmenü
**Original:** Ziel ist frei wählbar (Feldherr, Forscher, Händler) — alles läuft über Rohstoffe.
**Maximal 6 Siedlungen.** Bildschirm: links Hauptmenü, oben Ressourcenleiste (in einer Siedlung:
deren Bestände, sonst Gesamtsumme), Mitte Hauptanzeige, rechts Zusatzmenü in manchen Bereichen.
Hauptmenü: Übersicht, Portal. Im Portal: Position der eigenen Welt im **Limbus, 20 Dimensionen**;
Entfernung bestimmt die Manakosten des Portals.
**Einzelspieler:** Layout 1:1 übernehmen (haben wir schon: Leiste oben, Menü links, Inhalt Mitte,
Zusatzspalte rechts). Der Limbus wird zur **Entfernungsmatrix zwischen den fünf Karten** — Mana
kostet der Sprung zwischen Karten, abhängig von einer festen Entfernungstabelle.
**Paket:** W7 (Layout, ist da), W5 (Entfernung/ Mana).

### Seite 3 — Nebenbereiche und Punktesystem
**Original:** Diplomatie (Gilde gründen/beitreten, Buddyliste, Herrscherprofil), Einstellungen
(Passwort, Newsletter, Skin, Urlaubsmodus, Account löschen), Ruhmeshalle (Vergleich mit anderen),
Gildenhalle (Gilden ab drei Mitgliedern gewertet), Voraussetzungen-Übersicht, Nachrichten (mit
Bestätigungen erfüllter Aufträge), Forum, IRC-Chat, Logout.
**Punktesystem:** Forschungspunkte = Summe **Stufe hoch drei** je Forschung
(Beispiel Handbuch: Felderwirtschaft 1 = 1, Kriegskunst 4 = 64, Minenarbeit 2 = 8 → **73**).
**Einzelspieler:**
- **Ruhmeshalle:** Rangliste gegen die **Bots** — gleiche Rechnung, dadurch fair vergleichbar.
- **Gildenhalle:** entfällt als Netzfunktion; optional als „Bündnis" mit zwei Bots (KANN).
- **Diplomatie:** bleibt als **Beziehungsseite** zu den Bots (Handel, Angriff, Ruf).
- **Skin:** bleibt (haben wir: drei Skins). **Urlaubsmodus:** wird zur **Pause** (Spielzeit anhalten).
- **Entfällt:** Passwort, Newsletter, Account löschen, Forum, IRC-Chat, Logout, Buddyliste.
- **Nachrichten:** bleiben und werden wichtiger — hier landen Auftragsbestätigungen und Kampfberichte.
**Paket:** W6 (Punkte, Rangliste), W7 (Nachrichten/Skins/Pause).

### Seite 4 — Kriegspunkte und Gesamtpunktzahl
**Original:** Kriegspunkte je Einheit (Bürgerwehr 1 … Paladin 16, Armbrustschütze 10, Katapult 7,
Großes Katapult 8 …), **Verteidigungsanlagen = Ausbaustufe hoch drei** (Palisade 4 = 64).
**Gesamtpunktzahl = (Kriegspunkte + Forschungspunkte) / 2.** Beispiel: (150 + 200) / 2 = 175.
**Einzelspieler:** Rechnung unverändert übernehmen. Die Punktewerte stehen schon in
`data/units.json` (25 von 28 belegt; Handelskarawanen und Siedlerkarren haben laut Handbuch keinen
Punktewert — genau so übernommen).
**Paket:** W6.

### Seite 5 — Rufpunkte und Götterschutz
**Original:** Rufpunkte für aktive Teilnahme, **nicht** in der Gesamtpunktzahl, eintauschbar gegen
Boni; entscheiden bei Punktgleichheit, danach das frühere Anmeldedatum.
**Götterschutz:** erste **7 Tage** unangreifbar; endet früher mit dem **ersten Kriegspunkt**.
Bis **299 Punkte** eingeschränkter Schutz: Angriff nur im Bereich **±20 %**. Ab 300 kein Schutz.
Geschützte Spieler erscheinen grün.
**Einzelspieler:** Götterschutz wird zum **Anfängerschutz gegen Bots**: Die Bots greifen erst an,
wenn der Spieler seinen ersten Kriegspunkt hat oder Tag 7 erreicht ist; danach greifen nur Bots im
Punktebereich ±20 % an. Anmeldungsdatum entfällt → bei Punktgleichheit entscheidet der **Ruf**.
Rufpunkte bleiben und werden gegen Boni (Rohstoffe, Mana) eintauschbar.
**Paket:** W5 (Schutz, Bot-Angriffe), W6 (Ruf).

---

## Teil B — Siedlungen und Wirtschaft (Seite 6–13)

### Seite 6 — Spielübersichtsseite
**Original:** Nach dem Einloggen: Liste der Siedlungen mit gelagerten Rohstoffen und Einheiten,
laufende Forschungen, darüber eine Liste **aller laufenden Aufträge**.
Start: **10 Siedler, 100 Holz, 100 Steine**.
**Einzelspieler:** Startwerte exakt so (`data/resources.json`). Auftragsliste zeigt Bewegungen,
Transporte und Angriffe mit Restzeit.
**Paket:** W4 (Startwerte, Auftragsliste), W7 (Anzeige).

### Seite 7 — Siedlungsübersicht und Baumenü
**Original:** Karte der Siedlung, gelagerte Rohstoffe, Zuwachstabelle; Ressourcenanzeige mit
**Balken bis zur nächsten Einheit**; rechtes Siedlungsmenü. Menüpunkte: Siedlungsübersicht,
**Aufträge**, **Bauen** (Bereiche Produktion und Verteidigung), **Gebäude abreißen**
(Sicherheitsabfrage, keine Rohstoffe zurück, Feld wird frei).
**Einzelspieler:** Vollständig baubar. Wichtig: Gebäude werden **auf der Siedlungskarte platziert**,
der Mauszeiger zeigt die Eignung (hohe/niedrige/keine Produktion). Das ist der größte
Oberflächen-Umbau — die heutige Liste „Stufe 0 / Ausbauen" ersetzt das nicht.
**Paket:** W4 (Bau, Eignung, Abbruch), W7 (Karte + Menü).

### Seite 8 — Lager, Umbenennen, Siedeln, aufgeben
**Original:** **Lager** zeigt Waren und Einheiten. **Umbenennen** frei. **Siedeln:** kostet
Ressourcen und **Siedlerkarren**; höchstens **6 Siedlungen**; neue Siedlung bekommt eine **zufällige
Karte**, nie zweimal dieselbe gleichzeitig. **Siedlung aufgeben** löscht alles endgültig.
**Einzelspieler:** Übernehmen. Die „Karten" der Siedlungen werden aus einem Vorrat von
Siedlungskarten gezogen (Terrainverteilung je Geländeart) — damit sind Sümpfe, Wald, Berge usw. echt
und die Ertragstabelle stimmt.
**Paket:** W4.

### Seite 9–10 — Rohstoffproduktion und Gebäude
**Original:** 10 produzierende Gebäude mit Ertrag **pro Stunde je Geländeart** (z. B. Holzfäller:
Wald 4, Steppe 2; Tempel/Mana: Nebelsee 5, sonst 1; Jäger: Wald 2+2). Sümpfe **unbebaubar**.
**Ein Siedler pro Stunde** bis zur Grenze; Grenze **10**, **+5 pro Haus**.
**Einzelspieler:** Alles 1:1 aus `data/resources.json` und `data/buildings.json`. Der Siedlerzuwachs
ist der Taktgeber der Wirtschaft.
**Paket:** W4. **Stand:** Daten fertig und geprüft.

### Seite 11–12 — Forschung
**Original:** Bibliothek bauen (nur Grasland/Steppe/Nebelsee, **eine** je Siedlung), in Stufen
ausbauen, Forschung beauftragen. **Dauer = neue Stufe² Stunden.** **Kosten verdoppeln sich je
Stufe.** Während der Studien ist der Bereich **blockiert**; die Stufe steigt **erst nach Ablauf**;
**Abbruch** kostet Zeit und Ressourcen.
**Einzelspieler:** Übernehmen. Bei beschleunigtem Tempo wird nur der Zeitfaktor geteilt, die Formel
bleibt.
**Paket:** W4. **Stand:** 21 Forschungen in `data/research.json`.

### Seite 13 — Waren
**Original:** Schmiede (Waffen/Rüstungen), Bogenbauer (Fernwaffen), Nähstube (Stoff/Fell). Waren
laufen über **Warteschlangen**; **mehrere gleiche Werkstätten fertigen parallel** (Beispiel: 10
Schwerter à 20 Min. mit zwei Schmieden = 100 statt 200 Min.). Warenbestand im Lager.
**Einzelspieler:** Übernehmen. Die Waren sind im Original **Voraussetzung für Einheiten** — diese
Verknüpfung steht schon in `data/units.json` (`waren` je Einheit) und in `data/items.json`
(`benoetigt_von`).
**Paket:** W3.

---

## Teil C — Einheiten und Krieg (Seite 14–22)

### Seite 14 — Einheiten
**Original:** **Vier Typen**: Karren, Belagerungswaffen, Kundschafter, Kampfeinheiten. Ausbildungs-
gebäude: **Stellmacher** (Karren + Belagerung), **Diebesgilde** (Kundschafter), **Kriegerakademie**
(Kampf), je eines je Siedlung, höhere Stufe = schneller.
**Einzelspieler:** Übernehmen. Heute bildet der Code alle Einheiten in einer Kaserne aus → wird auf
die drei Gebäude aufgeteilt.
**Paket:** W1d. **Stand:** 28 Einheiten mit Gebäudezuordnung in `data/units.json`.

### Seite 15–17 — Einheitentabelle, Werte, Abkürzungen
**Original:** Alle 28 Einheiten mit Kosten (Gold, Rohstoffe, Siedler, Pferde, Waren) und einer
Wertetabelle: **LE, AT, PA, SI, HE, RS, TP, GS, MU, SK**. Karren haben **Ladung**.
**Einzelspieler:** 1:1. Zwei belegte Eigenheiten: Für die Gruppe *Karren und Belagerungswaffen*
druckt das Handbuch **kein MU** — die 13 Einheiten haben dort `null`; für Belagerungsturm und
Großen Belagerungsturm steht TP als **0** („kein Schaden", nicht „kein Wert").
**Paket:** W1d. **Stand:** `data/units.json`, `data/unit_stats.json` (15 vollständig, 13 mit Lücken,
jede Lücke begründet). **Offene Entscheidung:** Ersatzregel für MU bei diesen 13 (Vorschlag: MU 0,
damit Karren nicht fliehen — sie sollen laut Seite 22 Ausrüstung bergen).

### Seite 18–19 — Aufträge
**Original:** Auftragsarten: **Stationieren**, **Spionage**, **Transportieren** (nur mit
Transportkarren, kehrt zurück), **Handeln** (Handelskarawanen, Partner bestätigt oder lehnt ab),
**Angriff**. Ziele im Original: eigene Siedlung, **Portalkoordinaten**, Verbündeter, Gildenmitglied.
**Zeitangaben gelten für eine Strecke** (Rückkehr = doppelt). **Kosten:** Gold + Nahrung, bei fremden
Siedlungen zusätzlich **Mana je Entfernung**. Geschwindigkeit in **10-%-Schritten drosselbar**:
langsamer = weniger Gold, mehr Nahrung.
**Einzelspieler:** Ziele sind eigene Siedlungen oder **Bot-Siedlungen** (statt Koordinaten: Auswahl
aus der Weltenkarte). Handeln läuft als **Angebot mit Annehmen/Ablehnen** durch den Bot.
Geschwindigkeitswahl bleibt (10-%-Schritte) und wirkt auf Gold/Nahrung.
**Paket:** W4 (Transport/Stationieren), W5 (Handel, Spionage, Angriff).

### Seite 20–22 — Kampf — **das Herzstück**
**Original:**
1. **Vorrunde:** Schlagkraft **aller angreifenden Fußtruppen** muss den **Schwellenwert des Walls**
   erreichen; ab verstärkter Palisade zusätzlich Schlagkraft von **Belagerungswaffen**. Schafft er es
   nicht, zieht er sich zurück — **unentschieden**. Wallstufen 1–10 (Erdwall 10 … Bollwerk 1000/1000).
2. **Mauerschaden:** Schaden der Belagerungswaffe (Zufallswert, z. B. Katapult 2-13) **minus
   Ausbaustufe der Mauer**; Rest geht vom Zustand ab (Beispiel: 8 − 6 = 2 → Mauer von 100 % auf 98 %).
   Beschädigte Mauer verlangt **prozentual weniger** Schlagkraft.
3. **Kampfsequenzen:** höchstens **10**. Je Sequenz: **Fernkampf zuerst und gleichzeitig** (auf die
   Fußtruppen des Gegners, sonst auf dessen Fernkämpfer) → **dann Verluste auf beiden Seiten
   berechnen** → dann stürmen die **Nahkämpfer nacheinander** je eine **zufällige** gegnerische
   Nahkampfeinheit.
4. **Zweikampf:** höherer **MU** beginnt (Gleichstand: Verteidiger). **Zufallszahl 1–100 ≤ AT** =
   Treffer; sonst Fehlschlag. Bei Treffer prüft der Verteidiger mit **PA**; pariert er, kein Schaden.
   Sonst Schaden = Zufallswert im **TP-Bereich minus RS**, mindestens 1. Abzug von **LE**.
   **LE < 1** = tot, **LE < 5** = Fluchtprobe über **MU**; Geflohene kehren nach der Schlacht zurück.
5. **Erschöpfung:** Der Sieger eines Zweikampfs verliert **1 AT und 1 PA** bis Schlachtende
   (summiert sich) — deshalb kann Übermacht schwacher Einheiten starke besiegen.
6. **Ausgang:** alle Verteidiger tot/geflohen → **Angreifer siegt** und **plündert** (wenn er
   **Transportkarren** mitführt). Alle angreifenden Fußtruppen tot/geflohen → **Verteidiger siegt**.
   Der **Verlierer** verliert einen Teil der Karren und Belagerungswaffen: **40 % Fluchtchance je
   Einheit, +5 % je Kampfsequenz**. Unentschieden → alle Karren und Belagerungswaffen bleiben.
**Einzelspieler:** Der Ablauf wird **wörtlich** umgesetzt — genau das fehlt heute (der Code macht
einen einzigen Zufallsvergleich). Alles, was dafür nötig ist, liegt vor: Werte (`data/units.json`),
Wallschwellen (`data/buildings.json`), Ablaufregeln (`docs/original/ORIGINAL_Kampf_und_Punkte.md`).
Der Kampf läuft **schrittweise sichtbar** ab (Sequenz für Sequenz) und endet mit einem **Bericht**,
der im Nachrichtenbereich archiviert wird.
**Paket:** W2. **Offene Entscheidung:** Sollen die 10 Sequenzen im Echtzeit-Takt laufen (zuschauen)
oder in einem Zug berechnet und als Bericht gezeigt werden? Vorschlag: **als Bericht**, mit Option
„Schritt für Schritt".

---

## Teil D — Spionage und Ende (Seite 23–24)

### Seite 23 — Spionage
**Original:** Spionageeinheiten aus der Diebesgilde; Unterschied ist neben den Kampfwerten die
**Reisegeschwindigkeit**. Bericht enthält Siedlungskarte, gelagerte Ressourcen, stationierte
Einheiten, Verteidigungsanlagen samt Zustand. **Pferde** können mitgegeben werden (frisches Pferd =
schneller).
**Einzelspieler:** Gegen **Bot-Siedlungen**. Der Bericht ist der Schlüssel zum Angriff: erst
ausspähen, dann entscheiden. Bots spionieren auch den Spieler aus (Hinweis im Nachrichtenbereich).
**Paket:** W5.

### Seite 24 — Ende der Anleitung
**Original:** Weitere Abschnitte (z. B. Diplomatie) waren angekündigt, aber nicht erschienen.
**Einzelspieler:** Der Diplomatiebereich wird aus dem, was belegt ist, gebaut (Bots, Ruf, Handel,
Angriff) — **nichts erfinden**, was nicht im Handbuch steht.

---

## Einzelspieler-Abbildung auf einen Blick

| Original setzt voraus | Ersatz im Einzelspieler | Paket |
|---|---|---|
| Andere Spieler | **Bots** mit Profil, Siedlungen, Armee, Verhalten | W1d/W5 |
| Portalkoordinaten | Auswahl aus der **Weltenkarte** (5 Karten) | W5 |
| Limbus/Entfernung | feste **Entfernungstabelle** zwischen den Karten → Manakosten | W5 |
| Handel mit Bestätigung | Bot-**Angebot** mit Annehmen/Ablehnen | W5 |
| Deine Siedlung / fremde Siedlung | eigene Siedlung / **Bot-Siedlung** | W4/W5 |
| Gildenhalle, Buddyliste | entfällt bzw. „Bündnis" (KANN) | — |
| Chat, Forum, IRC, Login, Passwort, Newsletter | entfällt | — |
| Urlaubsmodus | **Pause** (Spielzeit anhalten) | W7 |
| Ruhmeshalle | **Rangliste gegen Bots** (gleiche Rechnung) | W6 |
| Anmeldedatum bei Punktgleichheit | entfällt → **Ruf** entscheidet | W6 |
| Speedserver (200×) | **Zeitfaktor** in den Einstellungen | W1d |

## Reihenfolge (nach Blockade, nicht nach Kapitelnummer)

1. **W1d — Code auf die Originaldaten umstellen** (S. 9–17): 28 Einheiten, 9 Rohstoffe, 17 Waren,
   21 Forschungen, 20 Gebäude. Danach: 28/28 Einheiten mit Kampfkraft > 0. *Blockiert alles andere.*
2. **W2 — Kampf** (S. 20–22): Vorrunde, 10 Sequenzen, Zweikampf, Erschöpfung, Flucht, Beute, Bericht.
3. **W3 — Waren und Handwerk** (S. 13): Werkstätten, Warteschlangen, Waren als Einheitenvoraussetzung.
4. **W4 — Wirtschaft und Siedlungen** (S. 6–12): Baukosten/zeiten, Geländeertrag, Siedler, Siedeln.
5. **W5 — Welt, Bots, Aufträge** (S. 18–19, 23): Weltenkarte, Bot-Verhalten, Handel, Spionage, Schutz.
6. **W6 — Punkte und Ziel** (S. 3–5): Punkteformeln, Rangliste, Ruf, Sieg/Niederlage.
7. **W7 — Oberfläche** (S. 2, 6–8): Siedlungskarte mit Platzierung, Original-Icons, Nachrichten, Pause.
8. **W8 — Speichern** robust + Versionskennung.
9. **W9 — Portable Windows-Version** + README.

## Offene Entscheidungen (Daniel)

1. **Zeitfaktor** als Standard: Original-Tempo oder beschleunigt? (Forschung Stufe² Stunden wäre im
   Original 25 Stunden für Stufe 5.)
2. **Kampfdarstellung:** Bericht in einem Zug, oder Sequenzen Schritt für Schritt?
3. **MU fehlt** für die 13 Karren/Belagerungswaffen: MU 0 setzen (fliehen nie), oder eine eigene
   Regel?
4. **Ziel:** Sieg über alle vier Nebenwelten + Punktzahl, oder reine Punktwertung?
5. **Gildenhalle/Bündnis:** weglassen oder als Bündnis mit zwei Bots?
