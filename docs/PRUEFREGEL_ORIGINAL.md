# Prüfregel gegen das Original — und was bereits geprüft ist

**Daniel, 30.10.2026:** „Prüfe bitte alles was wir ins Spiel integrieren immer mit den Originalen
Spielregeln und Abläufen und Zahlen und Werten ab." … „aber nicht alles tausendmal prüfen."

**Also:** jedes NEUE Ding wird gegen eine Quelle gehalten, das Urteil wird hier eingetragen, und
was hier steht, wird **nicht erneut** nachgesehen. Nur ein echter Widerspruch öffnet einen Punkt
wieder.

## Urteile

| Kürzel | Bedeutung |
|---|---|
| BELEGT | Quelle nennt es wörtlich; Zitat steht dabei |
| WIDERSPRUCH | Quelle sagt etwas anderes als unser Code/unsere Daten → wird geändert |
| NICHT BELEGT | Quelle schweigt → Wert bleibt `null`, nichts wird erfunden |
| VORSCHLAG | bewusste Remake-Entscheidung, klar gekennzeichnet |

## Register des Geprüften (nicht erneut prüfen)

| # | Gegenstand | Quelle | Urteil | Stand |
|---|---|---|---|---|
| 1 | Baupreise Holzfäller 10 Holz/5 Stein/1 Siedler, Steinmetz 5/10/1, Jäger 25/25/1, Haus 80/50 | GameStar-Screenshot `web_1838857` + `data/baupreise.json` (`_hinweis`, `preise`) | **BELEGT** — unsere Daten stimmen | 30.10.2026 |
| 2 | Haus hebt die Siedlergrenze um 5; Siedler, die in einem Gebäude arbeiten, belegen **keinen** Hausplatz | Screenshot `web_1838857` (Haustext wörtlich) + `gebaeude_wirkung.siedlergrenze_je_siedlung` (10 + 5 je Haus) | **BELEGT** — Rechnung stimmt | 30.10.2026 |
| 3 | Portal: Koordinaten **X-Y-Z**, Gitter **20 × 20**, eigene Dimension/Reich = grüner Punkt, fremde = rote Punkte | Screenshot `web_1838856` (Koordinaten „15-18--9") + `docs/original/Spielanleitung_2005/portal.php.txt` | **BELEGT** | 30.10.2026 |
| 4 | Navigation: **zwei Ebenen** („Übersicht" / „Siedlung"), Leiste immer gleich, Siedlungsreiter Siedlungsübersicht / Produktion / Verteidigung | Screenshot `web_1838856` + `web_1838857`, festgehalten in `docs/quellen/ORIGINAL_UI_BEFUNDE.md` | **BELEGT** | 30.10.2026 |
| 5 | Ein Hersteller je Siedlung (Kriegerakademie, Diebesgilde, Stellmacher, Bibliothek je 1) | `data/buildings.json`, Feld `max_je_siedlung` = 1 | **BELEGT** — wird in `bauen_auf_karte` durchgesetzt | 30.10.2026 |
| 6 | Handkarren/Siedlerkarren gehören zum Stellmacher; Siedlerkarren braucht Wagenbau 1 | `data/units.json` Felder `gebaeude` und `voraussetzung` | **BELEGT** | 30.10.2026 |
| 7 | Höchstens zwei Bibliotheken je Spieler, eine je Siedlung, die letzte bleibt stehen | **Daniels Ansage 30.10.2026** (nicht aus den Originaldokumenten!) | **VORGABE DANIEL** | 30.10.2026 |
| 8 | **Einheiten- und Item-Bilder passen** — keine Neuzuordnung, kein Neuschneiden, keine Umbenennung | **Ansage Daniel 30.10.2026** („die einheiten bilder und item bilder so passen") | **ABGESCHLOSSEN** | 30.10.2026 |
| 9 | **Bibliothek erscheint als Menüpunkt erst mit der Bibliothek**; nur auf Grasland/Steppe/Nebelsee; eine je Siedlung (keine Gesamtgrenze im Original) | Spielanleitung 2009, Seite 12 (Z. 400–408) | **BELEGT** — Menüpunkt am 30.10. gebaut; Gelände und „eine je Siedlung" stimmten schon | 30.10.2026 |
| 10 | **Forschungsdauer = neue Stufe² in Stunden**, Stufe steigt erst nach Ablauf, Kosten verdoppeln sich je Stufe, Siedlung während der Studien blockiert | Spielanleitung 2009, Seite 12/13 (Z. 421–452) | **BELEGT** — `src/forschung.py` rechnet schon so | 30.10.2026 |
| 11 | **Siedlergrenze 10 je neuer Siedlung, +5 je Haus, 1 Siedler/Stunde** | Spielanleitung 2009, Seite 11 (Z. 382–386) | **BELEGT** — `gebaeude_wirkung` stimmt | 30.10.2026 |
| 12 | **Erträge je Gebäude und Gelände** (Holzfäller Wald 4/Steppe 2, Steinmetz Berg 4/Hügel 2, Erzmine 3/1,5, Tempel Nebelsee 5/sonst 1, Farm Grasland 4/Steppe 2, Goldmine 3/1,5, Schafszucht 3/1,5, Rinderfarm 3/3 bzw. 1,5/1,5, Pferdezucht 3/1,5, Jäger 2/2 bzw. 1/1) | Spielanleitung 2009, Seite 10 (Z. 338–373) | **BELEGT** — Tabelle steht in `docs/quellen/ORIGINAL_GEBAEUDE_UND_FREISCHALTUNG.md` | 30.10.2026 |
| 13 | **Freischaltung neuer Gebäude/Einheiten läuft über Forschungsstufen**, nicht über eine Gebäudekette; „Voraussetzungen" im Hauptmenü zeigt die Bedingungen | Spielanleitung 2009, Seite 12 (Z. 396–412) | **BELEGT** | 30.10.2026 |
| 14 | **Sumpf ist unbebaubar**; jedes Produktionsgebäude hat zwei bevorzugte Geländearten | Spielanleitung 2009, Seite 10/11 (Z. 378–381) | **BELEGT** — Geländeregeln stimmen | 30.10.2026 |
| 15 | **Bauvoraussetzungen je Gebäude** (sechs ohne Forschung: Holzfäller, Steinmetz, Jäger, Bibliothek, Haus, Lager; alle anderen `Baukunst`) | `data/buildings.json`, Feld `voraussetzung` je Eintrag | **FERTIG — NICHT NEU EINTRAGEN.** Am 30.10. versehentlich doppelt bearbeitet und zurückgenommen. Wer die Kette braucht: `python tools/freischaltung.py` liest sie, statt sie zu schreiben | 30.10.2026 |
| 16 | **Gebäude-Baumenü** (Screenshot, Reiter, Kosten, offene GUI-Aufgaben) | `docs/BAUMENUE_ABGLEICH.md` | **FERTIG** — dort steht der Abgleich samt Aufgabenliste | 28.10.2026 |
| 17 | **Es gibt KEINE Lagerkapazität.** „Lager" ist ein **Menüpunkt zur Übersicht** über Waren und Einheiten der Siedlung, keine Grenze | Spielanleitung 2009, Seite 9 (Z. 302–304) | **BELEGT** — Frage (a) damit erledigt; nichts einzubauen | 31.10.2026 |
| 18 | **Der rote Balken** unter jedem Rohstoff zeigt, **wann die nächste Einheit dazukommt** (kein Lagerbalken!) | Spielanleitung 2009, Seite 7 (Z. 261–263) | **BELEGT** — die Deutung „Kapazität" war falsch; ggf. als Fortschrittsbalken nachbauen | 31.10.2026 |
| 19 | **Mehrere Gebäude wirken additiv**: jedes bebaute Feld produziert für sich (Ertrag je Gelände), Siedlergrenze +5 je Haus | Spielanleitung 2009, Seiten 10–11 (Z. 338–386) | **BELEGT** — Frage (b) erledigt; keine Sonderregel für „zweites Gebäude" | 31.10.2026 |
| 20 | **GS = Reisegeschwindigkeit** (höher = schneller zwischen zwei Siedlungen); Auftragsdauer wird **je Strecke** angezeigt, Rückkehr = doppelte Dauer. **Eine Zahlformel nennt das Handbuch nicht** | Spielanleitung 2009, Seite 18 (Z. 1103–1104) und Seite 19 (Z. 1136–1141) | **BELEGT (qualitativ)** — die Formel bleibt VORSCHLAG: Wegzeit = Felder ÷ GS der langsamsten Einheit | 31.10.2026 |
| 21 | **Ziele eines Auftrags:** eigene Siedlung, **Portalkoordinaten** eines Spielers, Verbündeter, Gildenmitglied; Auftragsart hängt von den gewählten Einheiten ab | Spielanleitung 2009, Seite 19 (Z. 1114–1148) | **BELEGT** — Grundlage für Daniels Planungsplattform (C6) | 31.10.2026 |

## Offen — hier fehlt die Quelle (nicht raten!)

| # | Frage | Status | Nächster Schritt |
|---|---|---|---|
| A | ~~**Lagerkapazität**~~ | **erledigt 31.10.**: es gibt keine (Register 17/18) — „Lager" ist eine Übersicht, der Balken zeigt die Zeit bis zur nächsten Einheit | — |
| B | ~~Wirkung eines **zweiten** Gebäudes~~ | **erledigt 31.10.**: additiv, jedes Feld produziert für sich (Register 19) | — |
| C | **Wegzeiten**: GS = Reisegeschwindigkeit, Dauer je Strecke, Rückkehr doppelt (Register 20) — **die Zahlenformel fehlt** | offen (Vorschlag nötig) | mit dem starken Modell entwerfen: Wegzeit = Felder ÷ GS, gegen gespielte Runden prüfen |
| D | Wie wird entschieden, **wo** die 6 Siedlungen einer Partie liegen (Zufall belegt) und wie hängen Laufwege davon ab | teilweise belegt (Zufall) | Portal-/Weltseiten |
| E | Kampfablauf im Bild: Reihenfolge, Anzeige, Beute | offen | Handbuchbilder `docs/original/handbuch_bilder/` (244 Dateien, nicht ausgewertet) |
| F | ~~„Voraussetzungen" als eigener Menüpunkt — was zeigt er?~~ | **erledigt 30.10.**: er zeigt die Voraussetzungen der Forschungen (Handbuch Seite 12) | — |
