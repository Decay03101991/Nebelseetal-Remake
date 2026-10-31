

==============================================================================
A  RAHMEN: Worum es geht und welche Regeln gelten
==============================================================================

Es geht um PYTHON-NEBELSEETAL-REMAKE: eine Einzelspieler-Neuauflage des
Browserspiels "Nebelseetal Online" (deutsches Browsergame, Spielanleitung 2009, Vorversion 2006).
Technik: Python + tkinter, kein Server, kein Multiplayer. Gespielt wird gegen Bots, Spieluhr
mit Faktor 180.0
(1 echte Sekunde = 180 Spielsekunden; 1 Spielstunde = 20 echte Sekunden).

DANIELS REGELN (gelten ueber allem):
1. Originaltreue: jede Mechanik wird gegen die Originalquellen gehalten. Handbuch 2009 ist die
   Richtschnur fuer Balance; die Vorversion 2006 zeigt die Entwicklung und fuellt Luecken.
   Abweichungen zwischen beiden werden dokumentiert, NICHTS wird stillschweigend angeglichen.
2. Was die Quellen nicht hergeben, ist VORSCHLAG und wird im Code und im Spiel als VORSCHLAG
   gekennzeichnet - es wird nichts erfunden und nichts "geschaetzt, bis es passt".
3. "Einmal pruefen, festschreiben, nicht tausendmal pruefen": was im Pruefregister als FERTIG
   steht, wird nicht erneut angefasst.
4. Der Spieler soll alles SEHEN und PLANEN koennen (Wegzeiten, Ankunft, Punkte, Kosten).
5. Ein Spiel gegen Bots muss in ueberschaubarer Zeit spielbar sein, ohne dass Regeln erfunden
   werden, nur damit es schneller geht.

PROJEKTSTAND: 105 Commits, Pruefstand 60 von 60 Pruefdateien gruen (568 s). Genau EIN
Entwicklungsprotokoll. Sprache im Code: deutsch, teils ASCII-only in Logikmodulen.


==============================================================================
B1  PRUEFREGISTER DES ORIGINALS (40 Punkte, je mit Seite/Zeile)
==============================================================================

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
| 22 | **Hauptmenü = die Welt-Ebene** (Übersicht, Portal, Diplomatie, Einstellungen, Ruhmeshalle, Gildenhalle, Voraussetzungen, Nachrichten, Forum, IRC-Chat, Logout); Umschalten über ein **Dropdownfeld über dem Menü** zwischen Siedlungsübersicht und Spielübersicht. Im Menü stehen die **neuesten fünf Nachrichten** und die Punkte | Fanpage-Anleitung 2007, `Grundlegenes.html` (web.archive.org, Capture 13.11.2007), Abschnitt Bildschirmaufbau/Hauptmenü | **BELEGT** — bestätigt unabhängig die am 30.10. gebauten zwei Navigationsebenen samt Punkteleiste | 31.10.2026 |
| 23 | **Ressourcenleiste**: in einer Siedlung die Ressourcen DIESER Siedlung, in der Hauptübersicht und allen siedlungsfernen Bereichen die **Summe aller Siedlungen** | ebd., Bildschirmaufbau | **BELEGT** — deckt sich mit Ortslager + Reichssumme im Code | 31.10.2026 |
| 24 | **Portal kostet nach Entfernung:** „Je weiter eine andere Spielwelt von Deiner Welt entfernt liegt, desto mehr Mana kostet es, das Portal zu öffnen, um Einheiten zu diesem Spieler zu entsenden." 20 Dimensionen im Limbus | ebd., Hauptmenü/Portal | **BELEGT — NEU.** Die 5.000 Mana sind der Dimensionswechsel; das Entsenden selbst kostet **entfernungsabhängig**. Im Entwurf vom 31.10. fehlte das | 31.10.2026 |
| 25 | **„Voraussetzungen" zeigt ALLE Bedingungen**: für Einheiten, Gebäude, Waren UND Forschungen, samt „ob Dein Volk sie schon erfüllt hat" | ebd., Hauptmenü/Voraussetzungen | **BELEGT** — unsere Ansicht zeigt bisher nur Forschungen; Erweiterung nötig | 31.10.2026 |
| 26 | **Der Balken zeigt die Zeit bis zur nächsten Einheit** (unabhängige zweite Quelle) | Fanpage 2007, `Siedlung.html` | **BELEGT** — bestätigt Register 18 | 31.10.2026 |
| 27 | **Wallschwellen (Vorrunde), vollständige Tabelle:** Fußtruppen-Schlagkraft / Belagerungs-Schlagkraft je Stufe — Erdwall 10/–, Steinwall 40/–, Kleine Palisade 90/–, Palisade 160/–, Verstärkte Palisade 250/500, Mauer 360/600, Verstärkte Mauer 490/700, Festungsmauer 640/800, Verstärkte Festungsmauer 810/900, Bollwerk 1000/1000. Beschädigter Wall senkt die Schwelle anteilig (Zustand 50 % = halbe Schlagkraft) | Fanpage 2007, `Kampf.html` | **BELEGT — NEU.** Gilt für das Remake, weil unser Verteidigungswall dieselben 10 Stufen führt. Stand im Entwurf als „Entscheidung Daniel" — ist es NICHT | 31.10.2026 |
| 28 | **Reicht die Schlagkraft nicht, ziehen sich die Truppen zurück — der Kampf gilt als unentschieden** | ebd. | **BELEGT** | 31.10.2026 |
| 29 | **Auftragsarten:** Stationieren (alle Einheitentypen, nur eigene Siedlungen), Spionage (Bericht mit Karte, Ressourcen, stationierten Einheiten; Pferde machen Spione schneller), Transportieren (nur mit Handkarre/Einspänner/Zweispänner; Kriegseinheiten dürfen mit, nützen nichts), Handeln (Karawanen, Kaufpreis, Bestätigung durch den Partner) | Fanpage 2007, `Auftraege.html` | **BELEGT** — Grundlage der Auftrags-/Planungsansicht | 31.10.2026 |
| 30 | **Jede Mechanik in BEIDEN Fassungen lesen.** Die Original-Seiten 2006 und das Handbuch 2009 weichen messbar ab (Siedlergrenze **5 vs. 10**, max. **10 vs. 6** Siedlungen, Tempel **8/2 vs. 5/1**, Jäger **nur Wald vs. Wald+Steppe**, Erträge allgemein). 2009 ist Richtschnur, 2006 zeigt die Entwicklung und füllt Lücken | `docs/original/Spielanleitung_2005/` (Seiten von 2006) gegen `Spielanleitung_2009_Textfassung.txt` | **BELEGT** — alle Abweichungen in `docs/quellen/ABWEICHUNGEN_2006_zu_2009.md`, nichts stillschweigend angeglichen | 31.10.2026 |
| 31 | **Kriegspunkte je Einheit** (Bürgerwehr 1 … Paladin 16 … Waldläufer 16) stimmen in **allen 15 Werten** mit `data/units.json` überein | 2006er `punktesystem.php` gegen `data/units.json` | **BELEGT** — nichts zu ändern | 31.10.2026 |
| 32 | **Gesamtpunktzahl:** 2009 = **(Krieg + Forschung) / 2**; 2006 = **je ein Drittel** aus Forschung, Krieg **und Handel**. Handelspunkte (1 je 100 Gold, Verfall 24 h) gibt es nur in der älteren Fassung | Handbuch S. 5/6 gegen 2006er `punktesystem.php` | **BELEGT beide** — Code folgt 2009 (richtig). Handelspunkte: **Entscheidung Daniel** | 31.10.2026 |
| 33 | **Ausbildungsgeschwindigkeit steigt mit der Gebäudestufe** („Je höher die Stufe, desto schneller") und **ein Hersteller je Siedlung**; Menübutton erscheint mit dem Gebäude | 2006er `einheiten.php` | **BELEGT** — bestätigt den Bau vom 30.10.; offen bleibt die Stufenabhängigkeit der Ausbildungszeit | 31.10.2026 |
| 34 | **Warenvoraussetzungen** vollständig nur in der älteren Fassung: Messer (keine), Dolch (Waffentechnik 1), Kurzschwert (3), Schwert (5), Zweihänder (8), Kettenhemd (Rüstungsbau 3), Plattenrüstung (5), Paladinharnisch (Rüstungsbau 7 + Magiekunde 2), Kurzbogen (Waffentechnik 2), Bogen (4), Langbogen (6), Armbrust (8), Wollumhang (keine), Lederrüstung (Nähkunst 1 + Rüstungsbau 2), Diebesumhang (Nähkunst 2), Fellumhang (Nähkunst 4), Fellrüstung (Nähkunst 6) | 2006er `warentabelle.php` | **BELEGT** — gegen `data/warenrezepte.json` prüfen | 31.10.2026 |
| 35 | **Wallschwellen stehen im Handbuch SELBST** (nicht nur auf der Fanpage 2007): Fußtruppen 10/40/90/160/250/360/490/640/810/1000, Belagerung ab Stufe 5: 500/600/700/800/900/1000. Beschädigte Mauer → prozentual weniger Schlagkraft (Beispiel: Verst. Mauer 50 % → 245/350) | Spielanleitung 2009, Seite 21 (Z. 1216–1258) — zweite, unabhängige Quelle zu Punkt 27 | **BELEGT** — Tabelle zusätzlich in `data/buildings.json` (Gebäude 16, Stufen 1–10); umgesetzt in `kampf.py` Z. 190–204 | 31.10.2026 |
| 36 | **Reicht die Schlagkraft nicht, ziehen sich die Truppen zurück — der Kampf gilt als unentschieden.** Kein „halbierter Schaden" | Spielanleitung 2009, Seite 21 (Z. 1213–1215) | **BELEGT** — bestätigt Punkt 28 aus dem Handbuch selbst | 31.10.2026 |
| 37 | **Kampfsequenzen:** je Sequenz schießen **zuerst beide** Fernkampfseiten gleichzeitig (erst feuern, dann Verluste beider Seiten), danach stürmen die angreifenden Nahkämpfer **nacheinander** je eine **zufällige** verteidigende Nahkampfeinheit; **nach 10 Sequenzen** ohne Sieger endet die Schlacht **unentschieden**, der Angreifer zieht sich **ohne Beute** zurück | Spielanleitung 2009, Seiten 21/22 (Z. 1274–1295) | **BELEGT** — umgesetzt in `kampf.py` Z. 217–312; zusammen mit `docs/original/ORIGINAL_Kampf_und_Punkte.md` §2.2 | 31.10.2026 |
| 38 | **Erschöpfung:** der Sieger eines Zweikampfs verliert **1 Punkt AT und PA** bis zum Schlachtende, summiert sich; deshalb kann Übermacht schwacher Einheiten starke besiegen | Spielanleitung 2009, Seite 23 (Z. 1324–1328) | **BELEGT** — im aktiven Forum-Modell als Erschöpfungsschaden/Schwelle umgesetzt (`kampf.py` `_ausgeschieden`), Bedeutung gleich, Zahlen aus dem neueren Original | 31.10.2026 |
| 39 | **Auftragskosten:** eigene Siedlungen kosten **Gold und Nahrung** (je Einheit); fremde **zusätzlich Mana nach Entfernung**; Geschwindigkeit in **10-%-Schritten drosselbar**, langsamer = **weniger Gold, mehr Nahrung**, Anzeige im Feld „Reisedauer" | Spielanleitung 2009, Seite 20 (Z. 1185–1194) | **BELEGT** — Konstante vorhanden (`auftraege.py` Z. 57–59), aber **nicht angeschlossen** (Z. 514) und Reisekosten leer (Z. 536) | 31.10.2026 |
| 40 | **Zwei Kampfsysteme, dokumentiert:** (a) Handbuch 2009 = LE/AT/PA/MU, Rückfallmodul `kampf_alt_handbuch_2009.py`; (b) **neueres Original-Forumssystem** (Konstitution %, Kampfwert-Spanne, Rüstung, Fernkampfchance, Erschöpfung durch Treffer) in `src/kampf.py`, aktiv über `main.py`. Die neuere Fassung ist **später** als das Handbuch und ersetzt es im Code (Projektentscheidung 29.10., „GPT-KA01…KA06, 14 Testdateien grün"). Punkte, Beute, Geräteverlust und Wall bleiben aus dem Handbuch, weil das Forum-Dokument sie nicht nennt | `docs/quellen/Das_Kampfsystem_Neu_Original.odt` gegen Spielanleitung 2009; `docs/ENTWICKLUNGSPROTOKOLL.md` Z. 133 | **BELEGT (beide Quellen)** — Konflikt offen für Daniel: Entscheidung E1 in `docs/PRUEFUNG_ENTWURF_WEGZEIT_KAMPF_20261031.md` §6 | 31.10.2026 |

## Offen — hier fehlt die Quelle (nicht raten!)

| # | Frage | Status | Nächster Schritt |
|---|---|---|---|
| A | ~~**Lagerkapazität**~~ | **erledigt 31.10.**: es gibt keine (Register 17/18) — „Lager" ist eine Übersicht, der Balken zeigt die Zeit bis zur nächsten Einheit | — |
| B | ~~Wirkung eines **zweiten** Gebäudes~~ | **erledigt 31.10.**: additiv, jedes Feld produziert für sich (Register 19) | — |
| C | **Wegzeiten**: GS = Reisegeschwindigkeit, Dauer je Strecke, Rückkehr doppelt (Register 20) — **die Zahlenformel fehlt** | offen (Vorschlag nötig) | mit dem starken Modell entwerfen: Wegzeit = Felder ÷ GS, gegen gespielte Runden prüfen |
| D | Wie wird entschieden, **wo** die 6 Siedlungen einer Partie liegen (Zufall belegt) und wie hängen Laufwege davon ab | teilweise belegt (Zufall) | Portal-/Weltseiten |
| E | Kampfablauf im Bild: Reihenfolge, Anzeige, Beute | offen | Handbuchbilder `docs/original/handbuch_bilder/` (244 Dateien, nicht ausgewertet) |
| F | ~~„Voraussetzungen" als eigener Menüpunkt — was zeigt er?~~ | **erledigt 30.10.**: er zeigt die Voraussetzungen der Forschungen (Handbuch Seite 12) | — |


==============================================================================
B2  BELEGTE AUSWERTUNG: Kampf, Auftraege, Punkte, Schutz, Spieldaten
==============================================================================

# Originaldaten: Kampf, Aufträge, Punkte, Schutz

**Richtschnur für das Remake.** Quelle: Original-Handbuch `Nebelseetal_Spielanleitung_2009.pdf`
(Seiten 4/5, 18–23). Textfassung: `Spielanleitung_2009_Textfassung.txt`.
Ergänzend: `Spielanleitung_2005/punktesystem.php.txt`, `handel.php.txt`, `portal.php.txt`.

---

## 1. Auftragsarten (Handbuch Seite 18/19)

Einheiten werden über den Menüpunkt **Aufträge** befehligt. Ziele: eigene Siedlung,
**Portalkoordinaten**, Verbündeter, Gildenmitglied.

| Auftragsart | Ablauf |
|---|---|
| **Stationieren** | Einheiten reisen zu einer Siedlung und bleiben dort; mit Karren können Waren mitgenommen werden. In **fremden** Siedlungen nicht möglich. |
| **Spionage** | Spionagebericht mit Siedlungskarte, gelagerten Ressourcen, stationierten Einheiten, Verteidigungsanlagen und deren Zustand. Pferde können mitgegeben werden (frisches Pferd = schneller). |
| **Transportieren** | Nur mit Transporteinheiten (Handkarre, Einspänner, Zweispänner). Liefert ab und **kehrt zurück**. Kriegseinheiten können begleiten, nützen aber nichts. |
| **Handeln** | Handelskarawanen zu einem anderen Spieler, mit Kaufpreis. Der Partner bestätigt (Gold fließt automatisch) oder lehnt ab (Karawane kehrt mit Ware zurück). |
| **Angriff** | Truppen greifen eine feindliche Siedlung an. Siehe Abschnitt 2. |

**Zeitangaben gelten für eine Strecke.** Bei Rückkehr (z. B. Transport) dauert der Auftrag doppelt so lang.

**Auftragskosten:** eigene Siedlungen kosten Gold und Nahrung (je nach Einheiten); fremde Siedlungen
zusätzlich **Mana für das Portal**, abhängig von der Entfernung der Zielwelt. Geschwindigkeit ist in
**10-%-Schritten drosselbar**: langsamer = **weniger Gold, mehr Nahrung**, angezeigt als „Reisedauer".

---

## 2. Kampfablauf (Handbuch Seite 20–22)

### 2.1 Vorrunde — Verteidigungswall überwinden

Zuerst wird geprüft, ob der Angreifer den Wall überwinden kann. Dazu wird die **Schlagkraft (SK)
aller angreifenden Fußtruppen** summiert. Sie muss den **Schwellenwert** des Walls erreichen.
Ab der **verstärkten Palisade** ist zusätzlich Schlagkraft von **Belagerungswaffen** nötig.
Reicht sie nicht, ziehen sich die Truppen zurück — der Kampf gilt als **unentschieden**.

| Verteidigungswall (Ausbaustufe) | Schwellenwert Fußtruppen | Schwellenwert Belagerungswaffen |
|---|---|---|
| Erdwall (1) | 10 | — |
| Steinwall (2) | 40 | — |
| Kleine Palisade (3) | 90 | — |
| Palisade (4) | 160 | — |
| Verstärkte Palisade (5) | 250 | 500 |
| Mauer (6) | 360 | 600 |
| Verstärkte Mauer (7) | 490 | 700 |
| Festungsmauer (8) | 640 | 800 |
| Verstärkte Festungsmauer (9) | 810 | 900 |
| Bollwerk (10) | 1000 | 1000 |

**Mauerschaden:** Belagerungswaffen beschädigen die Mauer; eine beschädigte Mauer verlangt
**prozentual weniger Schlagkraft**. Beispiel aus dem Handbuch: eine verstärkte Mauer (Stufe 7) mit
nur noch 50 % Zustand ist mit 245 Schlagkraft Fußtruppen + 350 Schlagkraft Belagerungswaffen zu
stürmen (jeweils die Hälfte).

Schadensermittlung: **Schaden der Waffe (Zufallswert, siehe Einheitentabelle) minus Ausbaustufe der
Mauer**; bleibt ein positiver Rest, wird er vom Zustand der Mauer abgezogen.
Beispiel: Katapult (Schaden **2-13**) gegen Mauer Stufe 6, gewürfelt 8 → 8 − 6 = 2 → Zustand 100 % → **98 %**.
Der Schaden wird **für jede mitgeführte Belagerungswaffe einzeln** ermittelt.

### 2.2 Kampfsequenzen

- Eine Schlacht läuft in **Kampfsequenzen**. Nach **10 Sequenzen** ohne Sieger endet sie
  **unentschieden** — der Angreifer zieht sich **ohne Beute** zurück.
- Ablauf je Sequenz:
  1. **Fernkampf gleichzeitig**: angreifende Fernkämpfer schießen auf die **Fußtruppen** des
     Verteidigers (sind keine vorhanden, auf dessen Fernkämpfer) — gleichzeitig schießen die
     verteidigenden Fernkämpfer auf die Fußtruppen des Angreifers (analog). **Erst beide feuern,
     dann werden die Verluste beider Seiten berechnet.**
  2. **Nahkampf**: die angreifenden Nahkämpfer stürmen **nacheinander** je eine **zufällige**
     verteidigende Nahkampfeinheit (sind keine mehr da, die Fernkämpfer).
  3. Nach allen angreifenden Einheiten beginnt die nächste Sequenz.
- Ende: eine Armee hat **keine Nahkampfeinheiten** mehr, **oder** 10 Sequenzen sind vorbei.

### 2.3 Zweikampf (Einheit gegen Einheit)

- Läuft in **Kampfrunden**. Die Einheit mit dem **höheren Mutwert (MU)** beginnt; bei Gleichstand
  der Verteidiger.
- Angriff: Zufallszahl 1–100 **≤ AT** = Treffer. Sonst verfehlt, der Gegner ist dran.
- Bei Treffer: Prüfung, ob der Verteidiger mit seinem **PA** pariert. Pariert er, **kein Schaden**,
  und er ist selbst mit Angreifen dran.
- Kein Parieren: Schaden = Zufallswert im **TP-Bereich** der Einheit **minus RS** des Verteidigers.
  Sinkt der Wert dadurch auf 0 oder darunter, wird trotzdem **1 Schadenspunkt** angerichtet.
  Der Schaden geht von der **LE** ab.
- **LE unter 1** → Einheit stirbt (wird nach der Schlacht gelöscht).
  **LE unter 5** → anhand des **MU** entscheidet sich, ob sie weiterkämpft oder **flieht**.
  Geflohene Einheiten stehen dem Spieler nach der Schlacht **wieder zur Verfügung**.
  Je niedriger der MU, desto wahrscheinlicher die Flucht.
- **Erschöpfung:** der Sieger eines Zweikampfs verliert **1 Punkt AT und PA** bis zum Ende der
  Schlacht (summiert sich). Deshalb kann Übermacht schwacher Einheiten starke besiegen.

### 2.4 Ausgang der Schlacht

- Sind **alle verteidigenden Einheiten tot oder geflohen**, gewinnt der **Angreifer**. Führt er
  **Transportkarren** mit, beginnen diese die Siedlung zu **plündern**.
- Sind **alle angreifenden Fußtruppen tot oder geflohen**, gewinnt der **Verteidiger**.
- Der **Verlierer** verliert einen Teil seiner Karren und Belagerungswaffen; wie viele, hängt von der
  Dauer ab. Jede Einheit hat **40 % Fluchtchance**, die pro Kampfsequenz um **5 %** steigt.
- **Unentschieden:** alle Karren und Belagerungswaffen bleiben erhalten.

---

## 3. Punktesystem (Handbuch Seite 3–5)

| Punktart | Berechnung |
|---|---|
| **Forschungspunkte** | Summe aller Forschungsstufen **hoch drei**. Beispiel: Felderwirtschaft 1 = 1, Kriegskunst 4 = 64, Minenarbeit 2 = 8 → **73** |
| **Kriegspunkte** | je Einheit ein fester Punktewert (siehe Liste unten) **plus** Verteidigungsanlagen: **Ausbaustufe³**. Beispiel: Palisade Stufe 4 = **64** |
| **Gesamtpunktzahl** | **(Kriegspunkte + Forschungspunkte) / 2** |
| **Rufpunkte** | für aktive Spielteilnahme; gehen **nicht** in die Gesamtpunktzahl ein, sind gegen Boni (z. B. Extraressourcen) eintauschbar. Bei Punktgleichheit entscheidet der **höhere Ruf**, danach das **frühere Anmeldedatum**. |

**Kriegspunkte je Einheit (wörtlich aus dem Handbuch):**
Bürgerwehr 1 · Kämpfer 2 · Krieger 4 · Ritter 8 · Paladin 16 ·
Kurzbogenschütze 2 · Bogenschütze 4 · Langbogenschütze 8 · Armbrustschütze 10 ·
Belagerungsturm 2 · Ramme 3 · Großer Belagerungsturm 4 · Große Ramme 5 · Balliste 6 · Katapult 7 ·
Großes Katapult 8 · Streuner 1 · Gauner 2 · Dieb 4 · Meisterdieb 8 · Kundschafter 10 ·
Waldläufer 16 · Handkarren 1 · Einspänner 2 · Zweispänner 3.
(Handelskarawanen, Siedlerkarren und Sammlerkarren haben **„Punktewert: -"**, geben also **keine** Kriegspunkte.)

Beispiel aus dem Handbuch: 10 Paladine + 12 Bogenschützen = 10·16 + 12·4 = **208 Kriegspunkte**.

---

## 4. Götterschutz (Handbuch Seite 5)

- Neue Spieler sind die **ersten sieben Tage** geschützt und **nicht angreifbar**.
- Der Schutz endet **früher**, sobald der Spieler seinen **ersten Kriegspunkt** erhält — also bereits
  beim Ausbau von Verteidigungsanlagen oder bei der ersten Militär-/Spionageeinheit.
- **Bis 299 Punkte: eingeschränkter Götterschutz.** Angriff nur auf Spieler im Bereich
  **eigene Punktzahl ± 20 %**. Über die Grenze von 299 Punkten hinweg ist **kein** Angriff möglich
  (in keine Richtung). Ein Spieler mit 299 Punkten kann nur 240–299 angreifen und ist für alle
  oberhalb 299 nicht angreifbar.
- **Ab 300 Punkten: kein Schutz** mehr.
- Geschützte Spieler erscheinen in Ruhmeshalle und Portal **grün** und mit einem **grünen Punkt**.

---

## 5. Weitere belegte Spieldaten

| Regel | Wert |
|---|---|
| Startwerte | 10 Siedler, 100 Holz, 100 Steine |
| Maximale Siedlungen | 6 |
| Siedlungsnamen | Karte wird zufällig zugewiesen; nie zweimal dieselbe gleichzeitig |
| Schriftverkehr | Nachrichten leuchten auf; Bestätigungen über erfüllte Aufträge laufen dort ein |
| Gildenwertung | nur Gilden mit **mehr als zwei** Mitgliedern werden gewertet |
| Rangfolge bei Punktgleichheit | höherer Ruf, danach früheres Anmeldedatum |
| Bauplätze | Gebäude auf der Siedlungskarte platzieren; Mauszeiger zeigt Eignung; Abriss bringt nichts zurück |
| Echtzeit | Produktion, Bewegung, Forschung laufen in Echtzeit ab, nicht in Runden |
| Bibliothek | nur auf Grasland, Steppe oder Nebelsee; **eine je Siedlung** |
| Ausbildungsgebäude | Kriegerakademie, Diebesgilde, Stellmacher — je **eines** je Siedlung |
| Werkstätten | Schmiede, Bogner, Nähstube — **mehrfach** möglich, fertigen parallel |


==============================================================================
B3  BELEGTE AUSWERTUNG: Gebaeude, Freischaltung, Erträge (Handbuch S. 9-14)
==============================================================================

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


==============================================================================
B4  ABWEICHUNGEN 2006 GEGEN 2009 (Balance 2009, Struktur beide)
==============================================================================

# Abweichungen: Original-Seiten 2006 ↔ Handbuch 2009

**Warum diese Datei:** Die Projektregel lautet seit dem 04.10.2026: „Wo 2005er Fassung und 2009er
Handbuch abweichen, ist das vermerkt — **nicht stillschweigend angeglichen**." Daniel hat am 31.10.
die Original-Seiten des Spiels erneut geschickt; sie weichen an vielen Stellen vom Handbuch ab.
Diese Datei hält jede Abweichung fest, damit niemand später glaubt, eine der beiden Zahlen sei
„falsch" — es sind zwei Fassungen desselben Spiels.

**Quellen:** `docs/original/Spielanleitung_2005/` (Original-Seiten, Stand 2006) und
`docs/original/Spielanleitung_2009_Textfassung.txt` (Handbuch 2009, mit Zeilennummern).
**Richtschnur des Remakes ist das Handbuch 2009** (Daniel, 04.10.2026) — die 2006er Zahlen gelten
als ältere Fassung und werden nur dort genutzt, wo das Handbuch schweigt.

## 0. Der Grundsatz (Daniel, 31.10.2026)

Wörtlich: „ich gehe davon aus dass sich das Spiel damals natürlich auch entwickelt hat und das
Balancing der aktuelleren Version deutlich besser war als zuvor."

Daraus folgt die Trennlinie, die für jede Zahl gilt:

| Was | Quelle | Begründung |
|---|---|---|
| **Balance-Zahlen** (Erträge, Siedlergrenze, Höchstzahl Siedlungen, Tempel-Ertrag, Kosten) | **2009** | die weiterentwickelte, besser ausbalancierte Fassung |
| **Struktur und Mechanik** (welche Gebäude, welche Menüpunkte, welche Auftragsarten, Warenvoraussetzungen, Ausbildungsgeschwindigkeit, Punktelogik, Wallschwellen) | **beide** | was 2009 offenlässt, steht in 2006; was 2009 abgeschafft hat, zeigt 2006 als Geschichte |

**Nicht** zurückdrehen: kein 2006er Wert ersetzt einen 2009er Wert, ohne dass Daniel es entscheidet.

---

## 1. Erträge je Gebäude und Gelände

| Gebäude | 2006 (Original-Seite `rohstoffe.php`) | 2009 (Handbuch S. 10) | Urteil |
|---|---|---|---|
| Holzfäller | Wald **4** / Steppe **1** | Wald 4 / Steppe 2 | ABWEICHUNG Steppe |
| Steinmetz | Berg **4** / Hügel **1** | Berg 4 / Hügel 2 | ABWEICHUNG Hügel |
| Erzmine | Berg **3** / Hügel **1** | Berg 3 / Hügel 1,5 | ABWEICHUNG Hügel |
| Tempel | Nebelsee **8** / sonst **2** | Nebelsee 5 / sonst 1 | ABWEICHUNG beide |
| Farm | Grasland **4** / Steppe **2** | Grasland 4 / Steppe 2 | gleich |
| Goldmine | Berg **3** / Hügel **1** | Berg 3 / Hügel 1,5 | ABWEICHUNG Hügel |
| Schafszucht | Grasland **2** / Steppe **1** | Grasland 3 / Steppe 1,5 | ABWEICHUNG beide |
| Rinderfarm | Grasland **2** / Steppe **1** (nur Leder) | Grasland 3+3 / Steppe 1,5+1,5 (Nahrung **und** Leder) | ABWEICHUNG beide, 2009 gibt zusätzlich Nahrung |
| Pferdezucht | Grasland **2** / Steppe **1** | Grasland 3 / Steppe 1,5 | ABWEICHUNG beide |
| Jäger | **nur Wald** (1 Nahrung, 1 Leder) | Wald 2+2 / Steppe 1+1 | ABWEICHUNG Gelände und Menge |

## 2. Siedlergrenze — die folgenreichste Abweichung

| | 2006 | 2009 |
|---|---|---|
| Grundwert je neuer Siedlung | **5 Siedler** | **10 Siedler** |
| je Haus | +5 | +5 |
| Zuwachs | 1 Siedler/Stunde | 1 Siedler/Stunde |

**Unser Code folgt 2009** (`gebaeude_wirkung.siedlergrenze_je_siedlung`: 10 + 5 je Haus). Bleibt so.

## 3. Höchstzahl Siedlungen

| | 2006 | 2009 |
|---|---|---|
| Maximum | **10 Siedlungen** | **6 Siedlungen** (Handbuch Z. 311–312) |

**Unser Code folgt 2009** (6). Bleibt so.

## 4. Punktesystem — die Vorversion zeigt, was sich GEÄNDERT hat

2006er Seite `punktesystem.php`, wörtlich:
- **Forschungspunkte** = Summe über alle Forschungen von **Stufe × Stufe**.
- **Kriegspunkte** je ausgebildeter Militär-/Spionageeinheit: Bürgerwehr 1, Kämpfer 2, Krieger 4,
  Ritter 8, Paladin 16, Kurzbogenschütze 2, Bogenschütze 4, Langbogenschütze 8, Armbrustschütze 10,
  Streuner 1, Gauner 2, Dieb 4, Meisterdieb 8, Kundschafter 10, Waldläufer 16.
  „Solltet Ihr Einheiten verlieren, verringern sich auch Eure Kriegspunkte."
- **Handelspunkte**: je **100 Gold** Handelseinnahme 1 Punkt (20 Gold = 0,2), Verfall 1 Punkt je
  24 Stunden ohne Handelseinnahme.
- **„Alle drei Punktearten fließen zu je einem Drittel in Eure Gesamtpunktezahl ein."**

**Das Handbuch 2009 rechnet anders** (S. 5/6): **Gesamtpunktzahl = (Kriegspunkte + Forschungspunkte)
/ 2** — also nur zwei Punktarten, keine Handelspunkte, halbiert statt gedrittelt.

**Unser Code folgt 2009** (`src/punkte.gesamtpunkte`, `// 2`, mit Begründung an der Stelle). Das ist
**keine Lücke**, sondern die neuere Fassung. Die **Kriegspunkte-Tabelle ist in `data/units.json`
bereits vollständig und stimmt in allen 15 Werten** mit der 2006er Tabelle überein (geprüft 31.10.).

**Was daraus offen bleibt:** ob Handelspunkte im Remake eine Rolle spielen sollen (Daniels
Entscheidung — das Handbuch 2009 kennt sie im Punktestand nicht mehr; das Handelssystem selbst ist
belegt). Erst danach lohnt ein Einbau.

## 5. Ausbildung: die Gebäudestufe macht schneller

2006er Seite `einheiten.php`, wörtlich: „Diese Gebäude werden stufenweise ausgebaut. **Je höher die
Stufe, desto schneller werden die entsprechenden Einheiten ausgebildet.**" Ebenso: „In jeder Eurer
Siedlungen kann jeweils **nur eine** Kriegerakademie, eine Diebesgilde und ein Stellmacher errichtet
werden" und „Sobald Ihr eines dieser Gebäude errichtet habt, **erscheint im Siedlungsmenü der Button**
Stellmacher, Diebesgilde bzw. Kriegerakademie."
**Bedeutung:** Das bestätigt unabhängig, was am 30.10. gebaut wurde (Menüpunkt erst mit dem Gebäude,
ein Hersteller je Siedlung). **Offen:** unsere Ausbildungszeit ist eine feste Pilotregel
(`pilot_ausbildung_minuten`); die Stufenabhängigkeit fehlt.

## 6. Weitere kleine Abweichungen

| Thema | 2006 | 2009 |
|---|---|---|
| Siedeln | über Menüpunkt **„Aufträge" → „Neue Siedlung gründen"** | eigener Menüpunkt **„Siedeln"** |
| Siedlungsmenü | „Siedlungsübersicht, Gebäude bauen, Gebäude abreißen, Lager, Aufträge" | zusätzlich Umbenennen, Siedeln, Siedlung aufgeben |
| Auswahl der Siedlung | „Auge hinter dem Siedlungsnamen", Auswahlfeld **unter** dem Menü | Klick auf den Namen oder Dropdown **über** dem Menü |
| Weltnamen | Armageddon, Ragnarök, Utgard, Midgard, Valhalla, Limbus (als Welten) | Limbus mit **20 Dimensionen** |
| Waren-Voraussetzungen | vollständige Tabelle (Waffentechnik 1/3/5/8, Rüstungsbau 3/5/7, Nähkunst 1/2/4/6, Magiekunde 2) | Handbuch nennt die Stufen nicht in dieser Form |
| Produktionstakt | „4 Holz pro Stunde → alle **15 Minuten** 1 Holz" | keine Aussage zum Takt |

**Die Waren-Tabelle aus 2006 ist die einzige vollständige Quelle für Warenvoraussetzungen** —
Messer (keine), Dolch (Waffentechnik 1), Kurzschwert (3), Schwert (5), Zweihänder (8),
Kettenhemd (Rüstungsbau 3), Plattenrüstung (5), Magischer Paladinharnisch (Rüstungsbau 7 +
Magiekunde 2), Kurzbogen (Waffentechnik 2), Bogen (4), Langbogen (6), Armbrust (8),
Wollumhang (keine), Lederrüstung (Nähkunst 1 + Rüstungsbau 2), Diebesumhang (Nähkunst 2),
Fellumhang (Nähkunst 4), Fellrüstung (Nähkunst 6).

---

## Was daraus folgt (Vorschlag, nicht ausgeführt)

1. **Nichts umstellen, was heute 2009 folgt** (Siedlergrenze 10, 6 Siedlungen) — die Abweichung ist
   jetzt dokumentiert, nicht geglättet.
2. **Handelspunkte und die Drittel-Regel** prüfen und Daniel vorlegen (verändert die Siegbedingung).
3. **Warenvoraussetzungen** aus der 2006er Tabelle gegen `data/warenrezepte.json` halten.
4. **Ausbildungszeit** an die Gebäudestufe koppeln (2006 belegt die Richtung, nicht die Zahl).


==============================================================================
C1  MODULE des Quellcodes (src/)
==============================================================================

- admin_oberflaeche.py (191 Zeilen): Nur die Bedienoberflaeche fuer Admin-Testwerkzeuge. Sicherheitsgrenze: Diese Datei authentifiziert NICHT. Der Hauptdialog muss vor dem Aufruf das separate Admin-Passwort geprueft haben. Jede Mutation im Kernmodul ``admin
- admin_teststand.py (125 Zeilen): Reproduzierbarer Admin-Teststand: keine Aenderung von Originalertraegen. * Sechs unterschiedliche Karten (Start, Ausgleich, Holz, Minen, Farmen, Mischkarte) * Gebietsspezifische Produktion, mit expliziter Stein- und Holz
- admin_werkzeuge.py (246 Zeilen): Isolierte Admin-Testwerkzeuge (keine Aenderung der normalen Spielregeln). Alle Mutationen brauchen eine explizite Admin-Freigabe UND den Teststand-Marker. Authentifizierung erfolgt in der GUI ueber das separate Passwortt
- auftraege.py (545 Zeilen): Nebelseetal Remake - Auftraege und Missionen (Paket WA, 04.10.2026). Ein Auftrag ist eine Reise einer Einheitengruppe von der eigenen Siedlung zu einem Ziel und (in der Regel) wieder zurueck. Dieses Modul fuehrt die Auft
- ausgabemodus.py (11 Zeilen): Laufzeitmodus der getrennten Windows-Testfassung. Die Projektquellen einschliesslich Admin-Logik bleiben vollstaendig auf GitHub. Der separate EXE-Einstieg setzt den oeffentlichen Modus vor Import der GUI. Dies ist Bedie
- ausruestung.py (273 Zeilen): Nebelseetal Remake — Ausruestung: welche Waren eine Einheit zur Ausbildung braucht. Beobachtung: manche Einheiten sind erst ausbildbar, wenn die noetigen Waren (Waffen, Ruestungen, Umhaenge) im Lager liegen — auch wenn d
- baumenue_info.py (133 Zeilen): FIX04 – Datenmodell fuer das historische Baumenue der Siedlungskarte. Keine zweite Bau-/Zahlungslogik: alle Entscheidungen kommen aus main.bauen_auf_karte, main.baukosten und GameState.ortsdeckung. Alle Bezeichnungen aus
- berater.py (359 Zeilen): Berater — die Auskunft im Spiel (Reiter "Chat"). Arbeitet OHNE Netz und OHNE Schluessel: alle Antworten kommen aus den Spiel- und Originaldaten (data/*.json) sowie aus fest hinterlegten Handbuchregeln. Damit ist die Ausk
- bonus_system.py (155 Zeilen): Nebelseetal Remake — Central Bonus System All research/building bonuses flow through these helpers so values stay consistent.
- bot_angriffsplanung.py (108 Zeilen): GPT-B01: konservative Bot-Zielwahl nach den Wallregeln der Originalanleitung. Keine eigenen Kampfwerte, keine Magieressourcen, keine Mutation. Der Bot greift nur Orte an, deren belegte Wall-SK-Schwelle er aktuell erreich
- botkern.py (574 Zeilen): Nebelseetal Remake - Bot-Kern (Paket W5, 05.10.2026). Was ein Computergegner ueber die Zeit tut: bauen, forschen, handeln, angreifen, warten. Reine Logik - kein Fenster, keine Uhr, keine Datei. Die Zeit (`jetzt`, in Seku
- dorfwall.py (122 Zeilen): Isolierter Wallkern fuer Nebelseetal (GPT-Zuarbeit, 28.10.2026). Das Remake-Modell (keine Behauptung ueber Originalbaukosten): - Verteidigungsanlagen: einmal erforschter, reichsweiter Technologiestand (1..10). - Jede Sie
- einheiten.py (193 Zeilen): Nebelseetal Remake — Einheiten-Bruecke. Verbindet die Originaldaten (`data/units.json`) mit dem Spiel. Vorher gab es **zwei** widersprechende Tabellen: `main.UNITS` (36 Einheiten, nur Anzeige) und `bonus_system.UNIT_BASE
- fehlbestand.py (140 Zeilen): Fehlbestand: welche Rohstoffe fehlen und um wieviel. Reine Standardbibliothek, keine Importe aus dem uebrigen Projekt - der Baustein laeuft damit auch in Werkzeugen, Bots und Einzelpruefungen ohne Spielkontext. Oeffentli
- forschung.py (232 Zeilen): Nebelseetal Remake — zeitlicher Ablauf der Forschung (reine Rechenlogik). Diese Schicht haelt *nur* den Ablauf: welche Stufe ein Gebiet hat, welcher Auftrag laeuft, wie viel Zeit noch bleibt und wann eine Stufe steigt. S
- forschung_wirkung.py (177 Zeilen): Nebelseetal Remake -- Wirkung der 21 Originalforschungen auf die Produktion. Dieses Modul beantwortet genau EINE Frage: Wie veraendert eine Forschung die Ausbeute der neun Rohstoffe, die Siedlerproduktion und den Verteid
- forschungspfad.py (350 Zeilen): Forschungspfad -- die fachliche Frageschicht rund um die 21 Originalforschungen. Dieses Modul ist die reine Datenschicht fuer die Frage, die Daniel am Forschungspanel vermisst hat: **Was schaltet eine Forschung sichtbar 
- gebaeude_wirkung.py (344 Zeilen): Nebelseetal Remake — Wirkungen der 20 Originalgebaeude (Paket W4b-5, 04.10.2026). Bis hierher lagen die Wirkungen in fuenf **erfundenen** Gebaeuden (`main.BUILDINGS`: Haus, Bibliothek, Kaserne, Wachturm, Portal) und wirk
- gelaende.py (233 Zeilen): Gelaende und Siedlungskarte fuer das Nebelseetal-Remake. Belegt (Handbuch 2009, S. 9-11): * sieben Gelaendearten: Grasland, Steppe, Wald, Huegel, Berg, Nebelsee, Sumpf * Sumpf ist nicht bebaubar * Erträge haengen vom Gel
- gildenrangliste_original.py (48 Zeilen): Historische Gildenwertung als reine, inaktive Datenfunktion. Quelle: TutorialundBeschreibung_einesSpielers(1).odt S. 10, Ranglisten-Screenshot vom 31.08.2011. Kein Mehrspieler-/Gildensystem im Remake wird hierdurch aktiv
- gpt_versorgungsdiagnose.py (126 Zeilen): Nur-lesende Versorgungsdiagnose fuer Nebelseetal. GPT-Zuarbeit 002: keine Aenderung an Spielregeln, Spielstand oder Hermes-Dateien. Quellen: src/gelaende.py, src/wirtschaft.py, data/baupreise.json und Handbuch. Die Diagn
- kampf.py (327 Zeilen): Nebelseetal – Kampfsystem des späteren Original-Forumstexts. Quelle: docs/quellen/Das_Kampfsystem_Neu_Original.odt (Spielerfund 28.10.2026). NICHT mit dem früheren Handbuchmodell LE/AT/PA verwechseln! Frühere Implementie
- kampf_alt_handbuch_2009.py (401 Zeilen): Nebelseetal Remake — Kampfablauf nach dem Originalhandbuch (Seiten 20-23). Zweite Fassung nach einem Regelgutachten (gpt-6-astra, 04.10.2026), dessen Befunde alle am wörtlichen Handbuchtext geprüft wurden. Korrigiert geg
- kampfbericht.py (367 Zeilen): Nebelseetal Remake - Kampfbericht (Paket W2b, 04.10.2026). Ergaenzt den fertigen Kampfablauf (`src/kampf.py`) um die vier Teile des Handbuchs (Seiten 20-23), die dort noch keine eigene, einzeln pruefbare Funktion hatten:
- karten_optik.py (599 Zeilen): Zeichenplaene fuer die Siedlungskarte des Nebelseetal-Remakes (Paket: feinere Kartenoptik). Dieses Modul liefert NUR DATEN — eine Liste von Zeichenbefehlen ("Plan") je Feld. Es zeichnet selbst nichts (ausser ``zeichne``,
- karten_optik_fein.py (863 Zeilen): Feinere Zeichenplaene fuer die Siedlungskarte des Nebelseetal-Remakes (``src/karten_optik_fein.py``) — die naechste, FEINERE Generation neben ``src/karten_optik.py``. Dieses Modul gibt den sieben Gelaendearten aus ``gela
- main.py (7140 Zeilen): Nebelseetal Remake — Core Game Engine Single-player, local, portable Windows desktop app. Multi-map system, trade, combat, research, bots, stationing.
- oberflaeche_original.py (185 Zeilen): Nebelseetal Remake - Menue-Vergleich (Paket W7, 04.10.2026). Stellt das WOERTLICH belegte Original-Menue (Datenblatt `data/menue_original.json`, Quelle: archiv/analysen/audits/astra_gamestar_antwort.txt, Screenshot 18388
- originalkarten.py (128 Zeilen): Original-Kartenkatalog Nebelseetal, 127 archivierte Grafiken in 3 Qualitaetsgruppen. Der Katalog enthaelt sowohl geschriebene Quellzahlen als auch das automatisch aus Originalbildern abgeleitete 10x10-Spielraster. Der sp
- originalkarten_grafik.py (36 Zeilen): Authentische Rasterbilder der 127 Originalkarten, keine Legacy-Symbole. UI-frei: prueft die ID gegen den Katalog und verwaltet nur Pfade. Die PNGs wurden direkt aus den originalen ODT-Kartenbildern (NEAREST, 640x640) erz
- portalraum.py (216 Zeilen): Portal- und Limbus-Raum fuer das Nebelseetal-Remake (Paket W5-2). Belegt (Portal-Anleitung 2005, portal.php; Handbuch 2009, S. 80-83): * Jede Spielerwelt liegt im magischen Limbus auf Koordinaten (X, Y, Z): X und Y sind 
- public_start.py (20 Zeilen): Windows-Testbuild: normaler Spielerweg, getrennte Laufzeitdaten. Dieser Einstieg blockiert die Admin-Oberflaeche; der volle Admin-Quellcode bleibt fuer Hermes im Repository. Keine Security-/Anti-Tamper-Garantie fuer Open
- punkte.py (313 Zeilen): Nebelseetal Remake — Punkte, Rangliste, Goetterschutz und Sieg/Niederlage (Paket W6, 04.10.2026). Belegte Originalregeln (Handbuch 2009, Seiten 3-6, nachgeprueft in ``docs/original/ORIGINAL_Kampf_und_Punkte.md``): * Fors
- speichern.py (338 Zeilen): Robustes Speichern (Paket W8) - atomar, geprueft, mit Sicherung und Wiederherstellung. Warum ein eigenes Modul: Der Spielstand wird derzeit direkt in die Zieldatei geschrieben (``json.dump`` auf den Endpfad). Bricht der 
- spieldaten.py (211 Zeilen): Nebelseetal Remake — Datenschicht. EINE Stelle, an der die Originaldaten aus `data/*.json` geladen werden. Alles, was vorher eigene Tabellen im Code hatte (Einheiten, Waren, Forschungen, Rohstoffe, Gebaeude), kommt ab hi
- spielerhilfe.py (176 Zeilen): FIX04c – Spielerhilfe während des Götterschutzes, jederzeit aufrufbar. Nur Präsentation/Orientierung, KEINE Spielmechanik. Der einzige maßgebliche Schutzstatus ist GameState.noob_protection. Daten zu Baueignung/-ertrag k
- spieloekonomie.py (973 Zeilen): Nebelseetal Remake — deterministischer Kern der Spielökonomie (Ökonomie-Paket, Schritt 2). Quelle: `archiv/analysen/audits/entwurf_spieloekonomie_sol_2026-10-05.txt` (Abschnitt F, Schritt 2, Codeblock Z. 237-414). Reine 
- spielschicht.py (664 Zeilen): Nebelseetal Remake - FACH-SCHICHT (Spielebene) fuer die Oberflaeche. Diese Schicht ist die EINZIGE Stelle, an der die Oberflaeche den Spielstand anfasst. Statt ein gutes Dutzend Module einzeln zu rufen, ruft die GUI hier
- spielstaende.py (48 Zeilen): Drei stabile, unabhaengige Speicherslots und ein gesonderter Admin-Teststand. Die bestehende savegame.json bleibt als Altstand erhalten und wird NICHT migriert. Dieses Modul hat bewusst keine GUI und keine Spielregeln.
- spielstand_archiv.py (162 Zeilen): Private Spielstandarchive: eindeutig, zeitgestempelt, ohne unbemerktes Loeschen. Zielordner: <aktueller Spielstandordner>/archiv/spielstaende/, nicht im GitHub-Code. Ueberschreiben ist eine AUSNAHME: bestehender Slot wir
- spielzeit.py (169 Zeilen): Spielzeit — der Zeitfaktor (Vorgabe Daniel 05.10.2026, Spielbericht). **Der Befund:** `tick(dt_seconds)` rechnete Echtzeitsekunden 1:1 als Spielsekunden (`dt_h = dt_seconds / 3600`). Damit war ein Spieltag = 24 Echtzeits
- tor.py (231 Zeilen): Passworttor fuer das Nebelseetal-Remake (Schritt 8 in `docs/WEG_ZUR_EXE.md`). Zweck: Das Spiel soll nur mit dem von **Daniel selbst gesetzten** Passwort starten. Das Passwort kommt **niemals** in einen Chat und wird **ni
- versorgungsschutz.py (160 Zeilen): Reine Vorabpruefung auf selbst verschuldete Rohstoff-Sackgassen. GPT-Zuarbeit 28.10.2026. Aendert weder Preise, Ertrag, Spielstand noch Originalregeln. Die genau eine Preisquelle wird als Funktion uebergeben. Nur fuer di
- welt.py (135 Zeilen): Weltkarte des Limbus fuer das Nebelseetal-Remake. Belegt (Handbuch 2009, S. 80-83 "Portal"; Portal-Anleitung 2005, portal.php; alte Website screens.php): * Alle Welten in Nebelseetal liegen im magischen Limbus, der sich 
- welt_optik.py (600 Zeilen): Zeichenplaene fuer die WELTkarte des Nebelseetal-Remakes (Paket: feinere Weltkartenoptik). Dieses Modul liefert NUR DATEN — eine Liste von Zeichenbefehlen ("Plan") je Element. Es zeichnet selbst nichts (ausser ``zeichne`
- welt_optik_fein.py (898 Zeilen): FEINERE Zeichenplaene fuer die WELTkarte des Nebelseetal-Remakes (naechste Ausbaustufe). Dieses Modul ist die feinere Nachfolgegeneration von ``src/welt_optik.py`` und aendert dieses NICHT. Es liefert NUR DATEN — eine Li
- werkstatt.py (422 Zeilen): Nebelseetal Remake - Waren und Werkstaetten (Paket W3, 04.10.2026). Die 17 Waren des Originals werden in drei Werkstaetten gefertigt: Schmiede -> Waffen und Ruestungen (Messer ... Magischer Paladinharnisch), 8 Waren Boge
- wirtschaft.py (252 Zeilen): Wirtschaft — stuendlicher Rohstoffertrag der Siedlungen (Remake Nebelseetal). Rechnet aus den Siedlungskarten (Gelaende + Gebaeude je Feld) aus, was der Spieler je Stunde erwirtschaftet: * siedlung_ertrag(siedlung) — Ert
- zeitbasis.py (102 Zeilen): Eine einzige Trennung von Rechnerzeit, Laufzeit und Spielzeit. Die monotone Uhr liefert NUR verstrichene Echtzeit waehrend eines laufenden Spiels. UTC- und lokale ISO-Zeiten dienen NUR als Beleg und Anzeige, nie als Rech


==============================================================================
C2  SPIELZAHLEN IM CODE (Modul-Konstanten, unverändert uebernommen)
==============================================================================

- admin_teststand.py: TEST_SEED = "ADMIN_TEST_2026_ORIGINALKARTEN_10x10"
- admin_teststand.py: KARTEN_IDS = ("start", "original-015", "original-037", "original-005", "original-019", "original-051")
- admin_teststand.py: NAMEN = ("Test-Hauptstadt", "Test-Ausgleich", "Test-Holzdorf", "Test-Bergdorf", "Test-Farmdorf", "Test-Mischdorf")
- admin_teststand.py: TEST_VORRAT = {"holz": 2500, "stein": 2500, "nahrung": 2500, "metall": 1500,
- admin_teststand.py: PRODUKTIONSGEB = ("holzfaeller", "steinmetz", "jaeger", "farm", "erzmine", "goldmine",
- admin_teststand.py: KETTENGEB = ("bibliothek", "haus", "stellmacher", "schmiede", "bogenbauer", "naehstube",
- admin_werkzeuge.py: ROHSTOFFE = ("holz", "stein", "metall", "mana", "nahrung", "gold", "wolle", "leder", "pferde")
- admin_werkzeuge.py: MAX_ZUGABE = 1_000_000
- auftraege.py: STAND = "2026-10-04.1"
- auftraege.py: AUFTRAGSARTEN = ("stationieren", "transportieren", "handeln", "angreifen")
- auftraege.py: SEKUNDEN_JE_FELD = 3600.0
- auftraege.py: HIN_UND_RUECK_FAKTOR = 2.0
- auftraege.py: DROSSELUNG_SCHRITTE_PROZENT = 10
- auftraege.py: DROSSELUNG_ZITAT = "Drosselung in 10-%-Schritten (Handbuch 2009, Seite 20)"
- auftraege.py: AKTION_DAUER_SEKUNDEN = 0.0
- auftraege.py: BEUTE_ANTEIL_PROZENT = 50
- ausruestung.py: ARTEN = ("forschung", "werkstatt", "ware", "einheit")
- baumenue_info.py: KATEGORIEN = ("Produktion", "Werkstatt", "Ausbildung", "Verteidigung", "Sonstiges")
- baumenue_info.py: SPIELERHILFE = (
- berater.py: WURZEL = spieldaten.projektwurzel()      # auch in der fertigen EXE richtig (eine Stelle: spieldaten)
- berater.py: ANTWORT_QUELLE_LLM = None
- berater.py: THEMEN = [
- bonus_system.py: UNIT_BASE = {
- bonus_system.py: TIER_SCALE = {name: 1.0 for name in _E.namen()}
- bonus_system.py: UNIT_TRAIN_BASE = {name: 0.0 for name in _E.namen()}
- bonus_system.py: BUILDING_BASE_COST = {
- botkern.py: STAND = "2026-10-05.1"
- botkern.py: SEKUNDEN_JE_STUNDE = 3600
- botkern.py: SEKUNDEN_JE_TAG = 86400
- botkern.py: ANGRIFF_MIN_STUNDEN = 6.0
- botkern.py: ANGRIFF_MAX_STUNDEN = 24.0
- botkern.py: BEUTE_ANTEIL = 0.5
- botkern.py: HANDEL_AUFSCHLAG = 1.2
- botkern.py: TEMPERAMENT_SPANNE = 0.10
- botkern.py: BOT_NAMEN = ["Haug", "Brynhild", "Grom", "Silra", "Krank"]
- botkern.py: BOT_FRAKTIONEN = {
- botkern.py: VORSCHLAG_START_VORRAETE = {
- botkern.py: VORSCHLAG_START_KARREN = (0, 3)   # Anzahl des kleinsten Karrens
- einheiten.py: ROLLEN = {
- einheiten.py: ROLLEN_TEXT = {
- fehlbestand.py: STELLEN = 2
- forschung.py: STUNDEN_IN_SEKUNDEN = 3600
- forschung_wirkung.py: ROHSTOFFE = ("holz", "stein", "metall", "mana", "nahrung", "gold", "wolle", "leder", "pferde")
- forschung_wirkung.py: SIEDLER = "siedler"
- forschung_wirkung.py: RESSOURCEN_FORSCHUNGEN = ("Felderwirtschaft", "Steinbruch", "Forstwirtschaft",
- gebaeude_wirkung.py: WURZEL = Path(spieldaten.projektwurzel())
- gebaeude_wirkung.py: WIRKUNGSDATEI = WURZEL / "data" / "gebaeude_wirkung.json"
- gebaeude_wirkung.py: STANDARD_STUFE = 1
- gelaende.py: WURZEL = Path(spieldaten.projektwurzel())
- gelaende.py: DATEN = WURZEL / "data"
- gelaende.py: ARTEN = {a["id"]: a for a in _GELAENDE["gelaendearten"]}
- gelaende.py: NACH_NAME = {a["name"]: a["id"] for a in _GELAENDE["gelaendearten"]}
- gelaende.py: GELAENDEARTEN = [a["id"] for a in _GELAENDE["gelaendearten"]]
- gelaende.py: SUMPF = "sumpf"
- gpt_versorgungsdiagnose.py: PREISE = json.loads((Path(spieldaten.projektwurzel()) / 'data' / 'baupreise.json').read_text(encoding='utf-8'))['preise']
- gpt_versorgungsdiagnose.py: GRUNDVERSORGUNG = {
- kampf.py: STAND = "2026-10-28.GPT-NE01.wissenswertes"
- kampf.py: PROFILE = {
- kampf_alt_handbuch_2009.py: STAND = "2026-10-04.2"
- kampf_alt_handbuch_2009.py: FUSSTRUPPEN = ("Nahkampf", "Fernkampf")
- kampfbericht.py: STAND = "2026-10-04.1"
- kampfbericht.py: AUSGANG_TEXT = {
- karten_optik.py: KARTEN_HINTERGRUND = "#0F1418"
- karten_optik.py: FORMEN = ("polygon", "rectangle", "oval", "line", "text", "arc")
- karten_optik_fein.py: FORMEN = ("polygon", "rectangle", "oval", "line", "text", "arc")
- karten_optik_fein.py: BAU_BREITE = 44.0        # "Baubereich 44 × 46 px"
- karten_optik_fein.py: BAU_HOEHE = 46.0
- karten_optik_fein.py: KOERPER_BREITE = 30.0    # "Hauptkörper etwa 30 × 22 px"
- karten_optik_fein.py: KOERPER_HOEHE = 22.0
- karten_optik_fein.py: DACH_BREITE = 38.0       # "Dach 38 × 16 px"
- karten_optik_fein.py: DACH_HOEHE = 16.0
- karten_optik_fein.py: SOCKEL_BREITE = 36.0     # "Sockel 36 × 5 px"
- karten_optik_fein.py: SOCKEL_HOEHE = 5.0
- karten_optik_fein.py: TUER_BREITE = 6.0        # "Tür 6 × 10 px"
- karten_optik_fein.py: TUER_HOEHE = 10.0
- karten_optik_fein.py: FENSTER_BREITE = 4.0     # "Fenster 4 × 5 px"
- karten_optik_fein.py: FENSTER_HOEHE = 5.0
- karten_optik_fein.py: ANBAU_BREITE = 10.0      # "Lager mit seitlichem 10 × 14-px-Anbau"
- karten_optik_fein.py: ANBAU_HOEHE = 14.0
- karten_optik_fein.py: DACH_HELL = "#875241"        # "Dach in zwei Flächen #875241 und #59382F"
- karten_optik_fein.py: DACH_DUNKEL = "#59382F"
- karten_optik_fein.py: WAND_HELL = "#C0AD86"        # "Wände #C0AD86 und #8F795C"
- karten_optik_fein.py: WAND_DUNKEL = "#8F795C"
- karten_optik_fein.py: KONTUR = "#302924"           # "Kontur #302924"
- karten_optik_fein.py: BODENSCHATTEN = "#343B30"    # "versetzter Bodenschatten #343B30"
- karten_optik_fein.py: EBENE_FARBE = "#74805A"
- karten_optik_fein.py: WALD_FARBE = "#455E43"
- karten_optik_fein.py: GEBIRGE_FARBE = "#77776C"
- karten_optik_fein.py: WASSER_FARBE = "#416875"
- karten_optik_fein.py: HALM_MINDEST = 3              # "drei bis fünf ... Halmlinien"
- karten_optik_fein.py: HALM_HOECHST = 5
- karten_optik_fein.py: HALM_LAENGE_MIN = 3.0         # "3–6 px lange Halmlinien"
- karten_optik_fein.py: HALM_LAENGE_MAX = 6.0
- karten_optik_fein.py: WALD_GRUPPEN = 3              # "drei versetzte Baumgruppen"
- karten_optik_fein.py: WALD_GRUPPE_BREITE = 14.0     # "etwa 14 × 20 px"
- karten_optik_fein.py: WALD_GRUPPE_HOEHE = 20.0
- karten_optik_fein.py: WALD_KRONE_DUNKEL = "#344C38"  # "Kronen #344C38 und #60734B"
- karten_optik_fein.py: WALD_KRONE_HELL = "#60734B"
- karten_optik_fein.py: FELS_FORMEN = 2               # "zwei ... Felsformen"
- karten_optik_fein.py: FELS_BREITE_MIN = 18.0        # "18–28 px breite Felsformen"
- karten_optik_fein.py: FELS_BREITE_MAX = 28.0
- karten_optik_fein.py: GEBIRGE_LICHT = "#969385"     # "Lichtfläche #969385"
- karten_optik_fein.py: WASSER_LINIEN_MIN = 2         # "zwei bis drei 12–22 px lange Linien in #6D9296"
- karten_optik_fein.py: WASSER_LINIEN_MAX = 3
- karten_optik_fein.py: WASSER_LINIE_MIN = 12.0
- karten_optik_fein.py: WASSER_LINIE_MAX = 22.0
- karten_optik_fein.py: WASSER_LINIE = "#6D9296"
- karten_optik_fein.py: UFER_BREITE_MIN = 3.0         # "3–5 px breites Polygonband #999071"
- karten_optik_fein.py: UFER_BREITE_MAX = 5.0
- karten_optik_fein.py: UFER_FARBE = "#999071"
- karten_optik_fein.py: UFER_BREITE = 4.0             # gewaehlt innerhalb 3–5 px
- karten_optik_fein.py: WEG_FARBE = "#75674F"        # "8 px breite Linie #75674F"
- karten_optik_fein.py: WEG_BREITE = 8.0
- karten_optik_fein.py: WEG_INNEN_FARBE = "#A28E69"  # "4 px breite Innenlinie #A28E69"
- karten_optik_fein.py: WEG_INNEN_BREITE = 4.0
- karten_optik_fein.py: AUSWAHL_EINZUG = 3.0          # "Auswahlrechteck 3 px nach innen setzen"
- karten_optik_fein.py: AUSWAHL_UNTER_FARBE = "#172128"  # "dunkle Unterkontur #172128"
- karten_optik_fein.py: AUSWAHL_UNTER_BREITE = 5.0       # "mit 5 px Strichbreite"
- karten_optik_fein.py: AUSWAHL_GOLD = "#E4C77D"         # "darüber #E4C77D mit 2 px"
- karten_optik_fein.py: AUSWAHL_GOLD_BREITE = 2.0
- karten_optik_fein.py: AUSWAHL_ECKEN_LAENGE = 8.0       # "Vier 8 px lange Eckwinkel"
- karten_optik_fein.py: PIP_KANTE = 4.0               # "Stufenpips als 4 × 4-px-Quadrate"
- karten_optik_fein.py: PIP_ABSTAND = 2.0             # "mit 2 px Abstand"
- karten_optik_fein.py: PIP_FARBE = AUSWAHL_GOLD      # erreichte Stufe in Astra-Gold
- karten_optik_fein.py: PIP_LEER = BODENSCHATTEN      # noch nicht erreichte Stufe gedaempft
- karten_optik_fein.py: KOORDINATEN_BREITE = 18.0     # "18 px breite beziehungsweise hohe äußere Rasterleiste"
- karten_optik_fein.py: KOORDINATEN_TEXT = "#EEE2CA"  # Panel-Textfarbe aus "Siedlung 3" (Detailpanel #EEE2CA)
- karten_optik_fein.py: RICHTUNGEN = ("norden", "osten", "sueden", "westen")
- karten_optik_fein.py: FAMILIEN = ("lager", "kaserne", "produktion", "ausbildungsstaette", "wall", "haus", "bibliothek")
- main.py: GOODS = {
- main.py: SIEDLUNGEN_MAXIMUM = 6
- main.py: KARTENVERSUCHE = 400
- main.py: STAND_VERSION_ALT = 1
- main.py: STAND_VERSION = 2
- main.py: MODUS_NEU = "oeokonomie-1"
- main.py: MODUS_LEGACY = "legacy"
- main.py: ICON_WURZEL = spieldaten.projektwurzel()
- main.py: BAUPREISE_DATEI = os.path.join(ICON_WURZEL, "data", "baupreise.json")
- main.py: RESOURCES = ["holz", "stein", "metall", "mana", "nahrung", "gold", "wolle", "leder", "pferde"]
- main.py: RESOURCE_ICONS = {
- main.py: BUILDINGS = {}
- main.py: UNIT_ICONS = {}
- main.py: UNITS = {}
- main.py: FORSCHUNG_HOECHSTSTUFE = 10
- main.py: RESEARCHES = {}
- main.py: WARE_EINTRAEGE = spieldaten.waren()
- main.py: WARE_ICONS = {name: str(eintrag.get("icon") or "")
- main.py: MAPS = [
- main.py: WELT_ZOOM_STUFEN = (16, 24, 32, 48, 64, 96)
- main.py: WELT_ZOOM_STANDARD = 48
- main.py: WELT_GELAENDEFARBEN = {
- main.py: WELT_GELAENDENAMEN = {
- main.py: WELT_GELAENDEREIHENFOLGE = ("forest", "plains", "mountain", "water", "village", "ruins")
- main.py: WELT_REGIONEN = ("Nordwesten", "Norden", "Nordosten",
- main.py: BOTS = [
- main.py: BOT_TAKT_SEKUNDEN = 3600.0
- main.py: BOT_BESCHAFFUNGSKOSTEN = 250.0
- main.py: MENU_ITEMS = [
- main.py: MENUE_BEDINGUNG = {
- main.py: BIBLIOTHEK_OBERGRENZE = 2
- main.py: EBENEN = ("Uebersicht", "Siedlung")
- main.py: EBENE_JE_PUNKT = {
- main.py: MENU_ANZEIGE = {
- main.py: MENU_ZUSATZ = {"Uebersicht": ["Voraussetzungen", "Neuigkeiten"], "Siedlung": []}
- main.py: SKINS = {
- main.py: LADEBILD_PNG = ("assets", "loadingpage", "Nebelseetal_Loadingpage.png")
- originalkarten.py: KATALOG_DATEI = "data/originalkarten/katalog.json"
- originalkarten.py: START_ID = "original-036"  # Singleplayer-Auswahl, keine Handbuchvorgabe.
- punkte.py: GOETTERSCHUTZ_TAGE = 7
- punkte.py: SEKUNDEN_JE_TAG = 86400
- punkte.py: VORSCHLAG_ZIEL_PUNKTE = 300
- speichern.py: ENDUNG_TMP = ".tmp"
- speichern.py: ENDUNG_BAK = ".bak"
- spieldaten.py: STAND = "2026-10-04"
- spieldaten.py: FORSCHUNG_GRUNDKOSTEN_HOLZ = 50
- spielerhilfe.py: FRAGEN = (
- spielerhilfe.py: ADMIN_HILFE_MODI = ("auto", "anzeigen", "ausblenden")
- spieloekonomie.py: DATEN = Path(spieldaten.projektwurzel()) / "data"
- spieloekonomie.py: REGELN = lade("spieloekonomie.json")
- spieloekonomie.py: WARENREZEPTE = lade("warenrezepte.json")
- spielschicht.py: STAND = "2026-10-04.1"
- spielschicht.py: STUNDEN_SEKUNDEN = 3600
- spielschicht.py: START_SAAT = 12345
- spielschicht.py: START_SIEDLER = 10
- spielstaende.py: SLOTS = (1, 2, 3)
- spielstand_archiv.py: BEREICHE = {"spieler", "admin", "testbereinigung", "abgebrochen"}
- spielzeit.py: PFAD = os.path.join(spieldaten.projektwurzel(), "data", "spielzeit.json")
- spielzeit.py: STANDARD_FAKTOR = 180.0
- spielzeit.py: STUFEN = (1.0, 20.0, 60.0, 180.0, 600.0)
- tor.py: ORDNER = os.path.join(os.path.expanduser("~"), ".nebelseetal")
- tor.py: STANDARD_PFAD = os.path.join(ORDNER, "tor.json")
- tor.py: RUNDEN = 200_000
- tor.py: SALZ_BYTES = 16
- tor.py: MIN_LAENGE = 4            # VORSCHLAG: das Handbuch kennt kein Passwort, es ist unsere eigene Wahl
- tor.py: WARTEZEITEN = (0, 5, 15, 60)   # Stufe 0..3: keine / 5 s / 15 s / 60 s (Wartezeit nach je 3 Fehlversuchen)
- tor.py: VERSION = 1
- versorgungsschutz.py: PRODUZENT = {'holz': 'holzfaeller', 'stein': 'steinmetz'}
- welt.py: WURZEL = Path(spieldaten.projektwurzel())
- welt.py: DATEN = WURZEL / "data"
- welt.py: DIMENSIONEN = _DATEI["dimensionen"]
- welt.py: REGEL = _DATEI["portalregel"]
- welt.py: WELTNAMEN = _DATEI["welten_belegt"]
- welt_optik.py: KARTEN_HINTERGRUND = "#0F1418"
- welt_optik.py: FORMEN = ("polygon", "rectangle", "oval", "line", "text", "arc")
- welt_optik.py: GELAENDEARTEN = ("forest", "plains", "mountain", "water", "village", "ruins")
- welt_optik_fein.py: MASS_PX = 48.0
- welt_optik_fein.py: FORMEN = ("polygon", "rectangle", "oval", "line", "text", "arc")
- welt_optik_fein.py: GELAENDEARTEN = ("forest", "plains", "mountain", "water", "village", "ruins")
- welt_optik_fein.py: WELT1_EBENE = "#707B58"            # astra: "Ebene #707B58"
- welt_optik_fein.py: WELT1_WALD = "#405A43"             # astra: "Wald #405A43"
- welt_optik_fein.py: WELT1_GEBIRGE = "#75766F"          # astra: "Gebirge #75766F"
- welt_optik_fein.py: WELT1_WASSER = "#405F70"           # astra: "Wasser #405F70"
- welt_optik_fein.py: WELT1_RASTER = "#38433C"           # astra: "Rasterlinien nur 1 px in #38433C"
- welt_optik_fein.py: WELT1_RASTER_BREITE = 1            # astra: "1 px"
- welt_optik_fein.py: WELT1_LICHT_GRUEN = "#637451"      # astra Lichtfarbe — gilt fuer die EBENE
- welt_optik_fein.py: WELT1_LICHT_GEBIRGE = "#96958A"    # astra Lichtfarbe (Gebirge)
- welt_optik_fein.py: WELT1_LICHT_WASSER = "#658594"     # astra Lichtfarbe (Wasser)
- welt_optik_fein.py: LICHT_ABLEITUNG_FAKTOR = 0.22
- welt_optik_fein.py: WELT1_LICHT_WALD = _aufhellen(WELT1_WALD, LICHT_ABLEITUNG_FAKTOR)
- welt_optik_fein.py: WELT1_UFER = "#938A70"             # astra: "an Ufern ein 2–3 px breites Band #938A70"
- welt_optik_fein.py: WELT1_UFER_MIN = 2                 # astra: "2–3 px breit"
- welt_optik_fein.py: WELT1_UFER_MAX = 3
- welt_optik_fein.py: WELT1_WALD_GRUPPEN_MIN = 2         # astra: "Wald mit zwei bis drei ... Baumgruppen"
- welt_optik_fein.py: WELT1_WALD_GRUPPEN_MAX = 3
- welt_optik_fein.py: WELT1_WALD_BREITE_MIN = 10         # astra: "10–16 px breit"
- welt_optik_fein.py: WELT1_WALD_BREITE_MAX = 16
- welt_optik_fein.py: WELT1_GRAT_ANZAHL = 2              # astra: "Gebirge mit zwei ... Gratpolygonen"
- welt_optik_fein.py: WELT1_GRAT_BREITE_MIN = 16         # astra: "16–22 px"
- welt_optik_fein.py: WELT1_GRAT_BREITE_MAX = 22
- welt_optik_fein.py: WELT1_WELLE_MIN = 2                # astra: "Wasser mit zwei ... Wellenlinien"
- welt_optik_fein.py: WELT1_WELLE_MAX = 3
- welt_optik_fein.py: WELT1_WELLE_LAENGE_MIN = 12        # astra: "12–18 px lang"
- welt_optik_fein.py: WELT1_WELLE_LAENGE_MAX = 18
- welt_optik_fein.py: WELT1_BEFEHLE_MIN = 4              # astra: "Etwa 4–11 Befehle je Feld, bei Wald bis etwa 14."
- welt_optik_fein.py: WELT1_BEFEHLE_MAX = 11
- welt_optik_fein.py: WELT1_BEFEHLE_WALD_MAX = 14
- welt_optik_fein.py: WELT2_ORTSZEICHEN_BREITE = 24      # astra: "Ortszeichen auf etwa 24 x 28 px begrenzen"
- welt_optik_fein.py: WELT2_ORTSZEICHEN_HOEHE = 28
- welt_optik_fein.py: WELT2_WAND = "#B9A582"             # astra: "Wände #B9A582"
- welt_optik_fein.py: WELT2_DACH = "#81503F"             # astra: "Dächer #81503F"
- welt_optik_fein.py: WELT2_RUINE = "#969083"            # astra: "Ruinen #969083"
- welt_optik_fein.py: WELT2_KONTUR = "#292B27"           # astra: "dunkle Konturen #292B27"
- welt_optik_fein.py: WELT2_SOCKEL = "#356D98"           # astra: "blauer Sockel ... in #356D98"
- welt_optik_fein.py: WELT2_SOCKEL_BREITE = 20           # astra: "20 x 6 px"
- welt_optik_fein.py: WELT2_SOCKEL_HOEHE = 6
- welt_optik_fein.py: WELT2_MAST = "#D8D3BD"             # astra: "Mast 2 x 21 px in #D8D3BD"
- welt_optik_fein.py: WELT2_MAST_BREITE = 2
- welt_optik_fein.py: WELT2_MAST_HOEHE = 21
- welt_optik_fein.py: WELT2_FAHNE = "#F2EEDB"            # astra: "weiße Fahne 12 x 8 px in #F2EEDB"
- welt_optik_fein.py: WELT2_FAHNE_BREITE = 12
- welt_optik_fein.py: WELT2_FAHNE_HOEHE = 8
- welt_optik_fein.py: WELT2_REGION_FARBE = "#D7CEB4"     # astra: "Regionsnamen ... #D7CEB4"
- welt_optik_fein.py: WELT2_REGION_SCHATTEN = "#26312B"  # astra: "um 1 px versetztem dunklem Textschatten #26312B"
- welt_optik_fein.py: WELT2_REGION_SCHRIFT = 18          # astra: "etwa 18 px Schriftgröße"
- welt_optik_fein.py: WELT2_REGION_VERSATZ = 1           # astra: "um 1 px versetzt"
- welt_optik_fein.py: WELT2_ORT_BEFEHLE_MIN = 7          # astra: "etwa 7–13 Befehle je Ort"
- welt_optik_fein.py: WELT2_ORT_BEFEHLE_MAX = 13
- welt_optik_fein.py: WELT2_FAHNE_BEFEHLE_MIN = 4        # astra: "etwa 4–5 für die eigene Fahne"
- welt_optik_fein.py: WELT2_FAHNE_BEFEHLE_MAX = 5
- welt_optik_fein.py: WELT3_AUSWAHL_GOLD = "#E4C77D"     # astra: "goldene Markierung #E4C77D"


==============================================================================
C3  FUNKTIONEN JE MODUL (die Mechanik selbst, ohne UI)
==============================================================================

- admin_oberflaeche.py: oeffnen(…)
- admin_teststand.py: _setzen(…), teststand_aufbauen(…)
- admin_werkzeuge.py: _pruefe_admin(…), spielerhilfe_modus_setzen(…), _ort(…), verfuegbare_posten(…), geben(…), _karte_id(…), freie_karten(…), _bauten_uebertragen(…), karte_waehlen(…), _weltgroesse(…), gebiet_wechseln(…), _ziel_vorpruefen(…), positionieren(…)
- auftraege.py: _als_zahl(…), _als_int(…), _ziel_name(…), _ziel_daten(…), _bestand(…), _unbekannte(…), _geschwindigkeit(…), _schlagkraft_fussttruppen(…), _schlagkraft_belagerung(…), reisezeit_sekunden(…), ladung_der_mission(…), auftragsarten(), neue_liste(), _pruefe_fracht(…), starten(…), _status_zeiten(…), _status(…), fortschritt(…)
- ausgabemodus.py: ist_oeffentliche_testversion()
- ausruestung.py: _einheiten(), _waren(), _einheit_oder_fehler(…), _zahl(…), _anzahl(…), _werkstatt_von(…), _voraussetzungen_von(…), bedarf(…), fehlende(…), ausbildbar(…), verbrauchen(…), _schritt(…), kette(…), bestand_text(…), offene_luecken()
- baumenue_info.py: _gesamt_ertrag(…), _rate_text(…), standort_hinweis(…), angebote(…)
- berater.py: _norm(…), _datei(…), _baupreise(), _gebaeude_text(…), _einheit_text(…), _ware_text(…), _antwort_gelaende(), _antwort_forschung(), _antwort_kampf(), _antwort_punkte(), _antwort_portal(), _antwort_start(), _antwort_steuerung(), _antwort_sieg(), antwort(…), tipps(…), begruessung()
- bonus_system.py: get_military_multiplier(…), get_production_multiplier(…), get_building_cost_multiplier(…), get_training_time_multiplier(…), get_trade_bonus(…), get_defense_bonus(…), get_medic_redution(…), get_unit_stats(…), get_combat_power(…), get_building_cost(…), get_training_time(…), get_map_switch_cost(…)
- bot_angriffsplanung.py: _anzahl(…), _stufe(…), _zustand(…), schlagkraft(…), pruefe_vorrunde(…), waehle_ziel(…)
- botkern.py: _zahl(…), _ganzzahl(…), _klemme(…), _karren_nach_ladung(), _kurz(…), neue_bots(…), bot_uebersicht(…), referenzpreis_aus_beschaffung(…), handelspreis(…), _lagerkapazitaet(…), beute_begrenzen(…), naechster_angriff_moeglich(…), _naechste_wartezeit(…), _wirtschaftliche_aktion(…), tick(…), wirkung_anwenden(…), bots_tick(…), offene_luecken()
- dorfwall.py: _feld(…), _setzen(…), forschungsstand(…), stufe(…), zustand(…), kennwerte(…), wache_besetzen(…), rahmen_plan(…)
- einheiten.py: alle(), namen(), nach_rolle(…), rolle(…), ist_kaempfer(…), ist_transport(…), ist_belagerung(…), _w(…), angriff(…), verteidigung(…), leben(…), schlagkraft(…), mut(…), geschwindigkeit(…), mauer_schaden(…), ladung(…), kriegspunkte(…), fehlende_werte(…)
- fehlbestand.py: _zahl(…), _bestand(…), _bedarf(…), _zwei(…), _menge(…), _betrag(…), fehlbestand(…), text(…)
- forschung.py: dauer_stunden(…), dauer_sekunden(…), kosten(…), gebiete(), neuer_stand(…), restzeit_stunden(…), restzeit_sekunden(…), naechste_stufe(…), naechste_kosten(…), _fehlende_rohstoffe(…), starten(…), fortschritt(…), abschliessen(…), abbrechen(…), punkte(…), punkte_je_gebiet(…)
- forschung_wirkung.py: _stufe(…), _faktor(…), faktor(…), faktor_alle(…), siedlerfaktor(…), verteidigungsfaktor(…), belegte_faktoren(), fehlende_forschungsnamen(…), befund_kontrolle(), offene_luecken()
- forschungspfad.py: _wurzel(), _lade(…), _forschungen(), _waren(), _einheiten(), _gebaeude(), _pruefe_name(…), _stufe(…), _parse_voraussetzung(…), _nennt(…), _bib_bedarf(…), voraussetzung(…), erfuellt(…), jetzt_moeglich(…), blockiert(…), wirkung_text(…), schaltet_frei(…), empfohlene_reihenfolge(…)
- gebaeude_wirkung.py: regeln(), luecken(), _feld(…), _kennung(…), _bauten(…), bestand(…), anzahl(…), stufe_von_feld(…), gebaeude_stufe(…), max_stufe(…), stufen_name(…), siedlergrenze_je_siedlung(…), bevoelkerungsgrenze(…), siedler_zuwachs_pro_stunde(…), bibliothek_stufe(…), hat_bibliothek(…), forschung_erlaubt(…), ausbildungsgebaeude(…)
- gelaende.py: _lade(…), name(…), _norm(…), finde_gebaeude(…), ist_bebaubar(…), farbe(…), alle_gebaeude(), gebaeude_name(…), ertrag_pro_stunde(…), bau_moeglich(…), siedlungskarte_erzeugen(…), karte_profil(…), karte_beschreiben(…), karte_als_text(…)
- gildenrangliste_original.py: _zahl(…), gildenwertung(…), gildenrangliste(…)
- gpt_versorgungsdiagnose.py: _feld(…), _kostensatz(…), _arten_freier_felder(…), _pruefe_kauf(…), untersuche(…), drucktext(…)
- kampf.py: _einheiten(…), _aktiv(…), _nah(…), _fern(…), _alle(…), _forschungsstufe(…), _ausgeschieden(…), _sieggeraete(…), _beute(…), fuehre_schlacht(…)
- kampf_alt_handbuch_2009.py: _eigenschaften(…), _aufstellen(…), _lebt(…), _aktive(…), _fusstruppen(…), _fernkaempfer(…), _nahkaempfer(…), _schlagkraft(…), mu_wert(…), _fluchtprobe(…), _pruefe_tot_oder_flucht(…), _ein_schlag(…), _zweikampf(…), _verluste_zaehlen(…), _geraeteverluste(…), fuehre_schlacht(…)
- kampfbericht.py: _als_zahl(…), _als_int(…), _schwelle_wall(…), vorrunde(…), mauer_schaden(…), beute(…), _aufzaehlung(…), bericht(…), spieldaten_anwenden(…), offene_luecken()
- karten_optik.py: _punkte(…), _box(…), emblem_plan(…), _wald(…), _berg(…), _huegel(…), _nebelsee(…), _sumpf(…), _steppe(…), _grasland(…), gebaeude_plan(…), wege_plan(…), raster_plan(…), zeichne(…), _fuell(…), offene_luecken()
- karten_optik_fein.py: _randlinien(…), _normal(…), _rgb(…), _hex(…), _abdunkeln(…), _aufhellen(…), _flaeche_farbe(…), _bau_koordinaten(…), _basis_bau(…), _familie_detail(…), _wall_bau(…), gebaeude_baukasten_plan(…), _ebene(…), _steppe(…), _wald(…), _huegel(…), _berg(…), _wasser(…)
- oberflaeche_original.py: _daten(), netz_eintraege(), original_menue(), offline_menue(), _menue_aus_text(…), aktuelles_menue(), fehlend(), zusaetzlich(), reihenfolge_abweichungen(), punktezeile(), abweichungsbericht()
- originalkarten.py: _katalog(), _index(), alle(…), kennungen(), daten(…), karte(…), startkarte(…), vorrat(…), ziehchancen(…), zufalls_originalkarte(…)
- originalkarten_grafik.py: manifest(), grafikpfad(…)
- portalraum.py: dimensionen(), dim_zahl(), feld_zahl(), _achsen(), _ist_ganz(…), _ist_dimension(…), koordinate(…), ist_gueltig(…), wechselkosten(), wechsel_erlaubt(…), nach_wechsel(…), portalfarbe(…), anzeige_raster(…), beschreibung()
- punkte.py: _stufe(…), _anzahl(…), _ke_einheit(…), forschungspunkte(…), kriegspunkte(…), gesamtpunkte(…), rufpunkte(…), _hole(…), rangliste(…), goetterschutz_tage(), goetterschutz_aktiv(…), sieg_oder_niederlage(…), belegte_formeln(), vorschlaege()
- speichern.py: _lies_text(…), _lies_json(…), _serialisiere(…), _entferne_quiet(…), speichere(…), lade(…), sichere_kopie(…), wiederherstellen(…), pruefe_datei(…), aufraeumen(…), offene_luecken()
- spieldaten.py: projektwurzel(), _lade(…), einheiten(), einheit(…), einheiten_nach_kategorie(), wert(…), wert_fehlt(…), luecken(), kosten(…), benoetigte_waren(…), kriegspunkte(…), voraussetzung(…), ladung(…), icon_pfad(…), waren(), waren_icons(), forschungen(), forschungsregeln()
- spielerhilfe.py: schutz_aktiv(…), hilfe_sichtbar(…), grundproduktion_erste_siedlung(…), startaufgabe_pflicht(…), admin_hilfe_modus_text(…), naechster_schritt(…), kurzinfo(…), antwort(…)
- spieloekonomie.py: lade(…), mengen(…), gruendungskosten(), feste_karte(…), vorrat(…), startkarte(…), kapazitaeten(…), achsen(…), relativ(…), _ist_originalkarten_verbund(…), kartenqualitaet(…), kartennutzen(…), _begrenzen(…), einzelmaximum(), schattenpreis(…), bezahlbar(…), buchen(…), absicht(…)
- spielschicht.py: _rohstoff_ids(), _preise(), _baukosten(…), _kosten_text(…), _siedlung(…), _fehlbetrag(…), _bezahlen(…), _melde(…), _forschungsstaende(…), neuer_zustand(…), tick(…), bauen(…), ausbauen(…), abreissen(…), forschung_starten(…), forschung_stand(…), ausbilden(…), ware_fertigen(…)
- spielstaende.py: ordner_vorbereiten(…), slot_pfad(…), altstand_pfad(…), admin_pfad(…), slot_status(…)
- spielstand_archiv.py: archivwurzel(…), ordner_anlegen(…), _zielgruppe(…), archiviere(…), archivierte_staende(…), wiederherstellen(…), archiv_groesse(…)
- spielzeit.py: einstellungspfad(), _lade_json(…), _laden(), daten(), faktor(), setzen(…), vergessen(), stufen(), spielstunden_je_echtsekunde(), echtzeit_fuer_spielstunden(…), text(…)
- tor.py: _pruefwert(…), _lade(…), _schreibe(…), hat_passwort(…), tor_pfad(…), fehlversuche(…), wartezeit_sekunden(…), gesperrt_bis(…), restwartezeit(…), passwort_pruefen_regeln(…), setze_passwort(…), pruefe_passwort(…), aendere_passwort(…), zuruecksetzen(…), uebersicht(…)
- versorgungsschutz.py: _wert(…), _normalisiere(…), _quellen(…), _felder(…), _anlauf_moeglich(…), risiko_nach_ausgabe(…), offene_luecken(), risiko_nach_abriss(…)
- welt.py: _lade(…), _norm(…), finde(…), dimensionen(), welten(), entfernung(…), portalkosten(…), nachbarn(…), beschreibung(…)
- welt_optik.py: _punkte(…), _box(…), gelaende_plan(…), _wald(…), _gebirge(…), _wasser(…), _ebene(…), _dorf(…), _ruine(…), fahne_plan(…), auswahl_plan(…), regionen_plan(…), _feld(…), uebersicht_plan(…), ortszeichen_plan(…), zeichne(…), _fuell(…), offene_luecken()
- welt_optik_fein.py: _aufhellen(…), _skala(…), _p(…), _flaech(…), _norm_art(…), _ist_wasser(…), _variante(…), _uv(…), zoom_detail(…), detail_masse(), gelaende_plan_fein(…), _kanten(…), _rasterlinie(…), _ufersaum(…), _schmuck(…), _ebene_fein(…), _wald_fein(…), _gebirge_fein(…)
- werkstatt.py: _werkstatt_eintraege(), werkstaetten(), _namen_nach_kennung(), _vergleich(…), _werkstatt_kennung(…), _waren(), waren_der_werkstatt(…), werkstatt_fuer(…), _stufe_wert(…), _stufe_faktor(…), dauer_sekunden(…), dauer_belegt(…), kapazitaet(…), neue_warteschlange(…), einreihen(…), _fortschreiben(…), fortschritt(…), _fortschritt_text(…)
- wirtschaft.py: _feld(…), _rohstoff_von(…), _zahl_text(…), siedlung_ertrag(…), uebersprungen_von(…), _ist_neue_originalsiedlung(…), ertrag_gesamt(…), ertrag_text(…), _beste_je_gelaende(…), kapazitaet(…)
- zeitbasis.py: zeitmarke(…), zeitstempel_text(…), offene_luecken()


==============================================================================
C4  DATENDATEIEN (data/) - die im Spiel wirksamen Tabellen
==============================================================================

## Gebaeude (data/buildings.json) — Name | Kategorie | Voraussetzung | max je Siedlung | Baupreise Stufe 1 | Wirkung
- Holzfäller | Produktion | keine (ohne Forschung baubar) | None | null | produziert Holz
- Steinmetz | Produktion | keine (ohne Forschung baubar) | None | null | produziert Stein
- Erzmine | Produktion | Baukunst | None | null | produziert Metall
- Tempel | Produktion | Baukunst | None | null | produziert Mana
- Farm | Produktion | Baukunst | None | null | produziert Nahrung
- Goldmine | Produktion | Baukunst | None | null | produziert Gold
- Schafszucht | Produktion | Baukunst | None | null | produziert Wolle
- Rinderfarm | Produktion | Baukunst | None | null | produziert Nahrung und Leder
- Pferdezucht | Produktion | Baukunst | None | null | produziert Pferde
- Jäger | Produktion | keine (ohne Forschung baubar) | None | null | produziert Nahrung und Leder aus der Jagd
- Schmiede | Werkstatt | Baukunst | None | null | stellt Waffen und Rüstungen her (Waren der Schmiede, u. a. Messer, Dolch, Kurzschwert, Schwert, Zweihänder, Kettenhemd, Plattenrüstung, Magischer Pala
- Bogenbauer | Werkstatt | Baukunst | None | null | stellt Fernwaffen her (Kurzbogen, Bogen, Langbogen, Armbrust; Voraussetzungen über Waffentechnik)
- Nähstube | Werkstatt | Baukunst | None | null | stellt Stoff- und Fellkleidung her (Wollumhang, Lederrüstung, Diebesumhang, Fellumhang, Fellrüstung; Voraussetzungen über Nähkunst/Rüstungsbau)
- Kriegerakademie | Ausbildung | Baukunst | 1 | null | bildet Armee-Einheiten (Kampfeinheiten) aus: Nahkampf (Bürgerwehr, Kämpfer, Krieger, Ritter, Paladin) und Fernkampf (Kurzbogenschütze, Bogenschütze, L
- Diebesgilde | Ausbildung | Baukunst | 1 | null | bildet Kundschafter aus (Streuner, Gauner, Dieb, Meisterdieb, Kundschafter, Waldläufer)
- Stellmacher | Ausbildung | Baukunst | 1 | null | baut Karren (Handkarren, Einspänner, Zweispänner, Handelskarawane, Große Handelskarawane, Siedlerkarren) und Belagerungswaffen (Belagerungsturm, Ramme
- Verteidigungswall | Verteidigung | Baukunst (schaltet Verteidigungsforschung frei); neue Schutzmöglichkeiten über die Forschung 'Verteidigungsanlagen' | None | null | Schutz vor Angriffen. In der Vorrunde einer Schlacht wird geprüft, ob die Schlagkraft (SK) der angreifenden Fußtruppen den Schwellenwert des Walls err
- Bibliothek | Sonstiges | keine (ohne Forschung baubar) | 1 | null | ermöglicht Forschung; Ausbau in Stufen erweitert die Forschungsmöglichkeiten; mit jeder Stufe teurer. Nur auf Grasland, Steppe oder Nebelsee errichtba
- Haus | Sonstiges | keine (ohne Forschung baubar) | None | null | erhöht die Siedlergrenze um 5 Siedler je Haus
- Lager | Sonstiges | keine belegt | None | null | gibt einen Überblick über alle in der Siedlung befindlichen Waren und Einheiten; der Warenbestand wird hier geprüft

## Rohstoffe (data/resources.json)
- versionsvermerk: "Zwei Fassungen belegt: archivierte Spielanleitung 2005 (HTML) und Handbuch 2009 (Textfassung). Sie weichen bei mehreren Ertraegen und bei der Siedlergrenze ab. Primaerwerte = 2009; Abweichungen sind 
- gebaeude_ohne_forschung: ["Holzfäller", "Steinmetz", "Jäger", "Bibliothek", "Haus"]
- regeln: {"gelände": "Jedes produzierende Gebäude erzeugt auf 2 verschiedenen Geländearten unterschiedliche Mengen. Ausnahme: der Jäger (in der 2005er Fassung nur Wald, 2009 auch Steppe).", "sumpf": "Sümpfe si
- siedler: {"produktion_pro_stunde": 1, "grenze_neue_siedlung": {"handbuch_2009": 10, "fassung_2005": 5}, "erhoehung_pro_haus": 5, "abweichung": "Siedlergrenze einer neuen Siedlung: Handbuch 2009 = 10 Siedler, 2
- startwerte: {"siedler": 10, "holz": 100, "steine": 100, "_anmerkung": "Startwerte laut Handbuch 2009 Seite 7 (10 Siedler, 100 Holz, 100 Steine) und ORIGINAL_Kampf_und_Punkte.md Abschnitt 5."}
- max_siedlungen: 6
- rohstoffe: [{"id": "holz", "name": "Holz", "erzeugendes_gebaeude": ["Holzfäller"], "ertrag_pro_stunde": {"Wald": 4, "Steppe": 2}, "ertrag_2005": {"Wald": 4, "Steppe": 1}, "abweichung": "Steppe: 2005 = 1, Handbuc

## Forschungen (data/research.json)
- Kriegskunst | "Die Kunst des bewaffneten Kampfes und des taktischen Vorgehens auf dem Schlachtfeld ermöglicht es Euch, Eure Armee duch stärkere Einheiten aufzuwerten." | kosten null
- Heimlichkeit | "Die hohe Kunst des Schleichens, ist die Grundlage um gute Spione auszubilden." | kosten null
- Schmiedekunst | "Mit Schmiedekunst erhöht Ihr die Effektivität Eurer Waffen und Rüstungen um je 5%." | kosten null
- Bogenbau | "Neue Techniken beim Bogenbau steigern die Geschwindigkeit, mit der Euer Bogenbauer produziert." | kosten null
- Nähen | "Neue Nähtechniken beschleunigen die Arbeit Eurer Schneider in der Näherei." | kosten null
- Waffentechnik | "Waffentechnik ermöglicht es Euch, neue Arten von Waffen herzustellen." | kosten null
- Rüstungsbau | "Rüstungsbau ermöglicht Euren Schmieden, neue Arten von Rüstungen herzustellen." | kosten null
- Nähkunst | "Die Verfeinerung der Nähkünste ermöglicht Euch, neue Umhänge und Lederrüstungen herzustellen." | kosten null
- Magiekunde | "Die Erforschung der arkanen Künste, ist Voraussetzung für die verschiedenen Pfade der Magie." | kosten null
- Kampfmagie | "Durch den Pfad der Kampfmagie, erlangt Ihr neue magische Formeln, um vernichtende Zauber über Eure Feinde zu sprechen." | kosten null
- Baukunst | "Baukunst ist eine wichtige Voraussetzung für einige Forschungen, die es Euch ermöglichen, Eure Siedlungen besser zu verteidigen." | kosten null
- Mauerbau | "Mit neuen Erkenntnissen im Mauerbau könnt Ihr die Effizienz Eurer Verteidigungsanlagen erhöhen. Pro Stufe erhöht sich der Verteidigungswert um 10%." | kosten null
- Verteidigungsanlagen | "Mit der Weiterentwicklung von Verteidigungsanlagen, stehen euch neue Möglichkeiten offen, Eure Siedlungen vor Angriffen zu schützen." | kosten null
- Wagenbau | "Neue Erkenntnisse bei der Konstruktion von Fahrzeugen, ermöglicht Euren Stellmachern, neue Arten von Karren zu bauen." | kosten null
- Felderwirtschaft | "Felderwirtschaft erhöht die Nahrungsproduktion Eurer Siedlungen um 10% pro Stufe." | kosten null
- Steinbruch | "Neue Techniken beim Abbau von Steinen, erhöhen die Steinproduktion Eurer Steinmetze um 10% pro Stufe." | kosten null
- Forstwirtschaft | "Forstwirtschaft erhöht die Effektivität Eurer Holzfäller um 10% pro Stufe." | kosten null
- Tierhaltung | "Durch neue Erkenntnisse in der Tierhaltung, könnt Ihr Eure Pferde-, Woll- und Lederproduktion um je 5% pro Stufe erhöhen." | kosten null
- Minenarbeit | "Durch neue Techniken bei der Arbeit in Euren Minen, erhöht Ihr die Metall- und Goldproduktion um je 5% pro Stufe." | kosten null
- Götterkunde | "Neue Erkenntnisse über die Götter, verschaffen Euch pro Stufe 5% mehr Mana." | kosten null
- Heilkunde | "Je besser Eure Heiler über Hygiene, Krankheiten und die Versorgung von Wunden Bescheid wissen, desto schneller steigt Eure Siedleranzahl. Die Siedlerproduktion | kosten null

## Einheiten (data/units.json) — Name | Gebaeude | Punkte | Werte | Ladung | Voraussetzung
- Bürgerwehr | Kriegerakademie | 1 | {"LE": 15, "AT": 20, "PA": 20, "SI": 10, "HE": 10, "RS": 0, "TP_min": 1, "TP_max": 6, "GS": 5, "MU": 40, "SK": 1} | None | null
- Kämpfer | Kriegerakademie | 2 | {"LE": 20, "AT": 40, "PA": 25, "SI": 10, "HE": 15, "RS": 1, "TP_min": 2, "TP_max": 8, "GS": 10, "MU": 75, "SK": 2} | None | {"forschung": "Kriegskunst", "stufe": 1}
- Krieger | Kriegerakademie | 4 | {"LE": 30, "AT": 50, "PA": 40, "SI": 15, "HE": 15, "RS": 2, "TP_min": 3, "TP_max": 10, "GS": 25, "MU": 85, "SK": 3} | None | {"forschung": "Kriegskunst", "stufe": 3}
- Ritter | Kriegerakademie | 8 | {"LE": 35, "AT": 70, "PA": 50, "SI": 15, "HE": 5, "RS": 4, "TP_min": 4, "TP_max": 15, "GS": 20, "MU": 95, "SK": 4} | None | {"forschung": "Kriegskunst", "stufe": 7}
- Paladin | Kriegerakademie | 16 | {"LE": 50, "AT": 85, "PA": 60, "SI": 20, "HE": 0, "RS": 6, "TP_min": 6, "TP_max": 20, "GS": 20, "MU": 100, "SK": 5} | None | {"forschung": "Kriegskunst", "stufe": 10}
- Kurzbogenschütze | Kriegerakademie | 2 | {"LE": 15, "AT": 40, "PA": 0, "SI": 10, "HE": 10, "RS": 0, "TP_min": 1, "TP_max": 6, "GS": 5, "MU": 60, "SK": 1} | None | {"forschung": "Kriegskunst", "stufe": 2}
- Bogenschütze | Kriegerakademie | 4 | {"LE": 15, "AT": 50, "PA": 0, "SI": 10, "HE": 10, "RS": 0, "TP_min": 1, "TP_max": 8, "GS": 5, "MU": 60, "SK": 2} | None | {"forschung": "Kriegskunst", "stufe": 4}
- Langbogenschütze | Kriegerakademie | 8 | {"LE": 20, "AT": 60, "PA": 0, "SI": 10, "HE": 10, "RS": 0, "TP_min": 1, "TP_max": 10, "GS": 5, "MU": 60, "SK": 4} | None | {"forschung": "Kriegskunst", "stufe": 6}
- Armbrustschütze | Kriegerakademie | 10 | {"LE": 20, "AT": 60, "PA": 0, "SI": 10, "HE": 10, "RS": 1, "TP_min": 2, "TP_max": 12, "GS": 5, "MU": 60, "SK": 5} | None | {"forschung": "Kriegskunst", "stufe": 8}
- Streuner | Diebesgilde | 1 | {"LE": 10, "AT": 10, "PA": 15, "SI": 30, "HE": 30, "RS": 0, "TP_min": 1, "TP_max": 4, "GS": 10, "MU": 60, "SK": 2} | None | null
- Gauner | Diebesgilde | 2 | {"LE": 15, "AT": 30, "PA": 20, "SI": 50, "HE": 45, "RS": 0, "TP_min": 1, "TP_max": 6, "GS": 15, "MU": 65, "SK": 3} | None | {"forschung": "Heimlichkeit", "stufe": 1}
- Dieb | Diebesgilde | 4 | {"LE": 15, "AT": 40, "PA": 40, "SI": 65, "HE": 70, "RS": 0, "TP_min": 2, "TP_max": 7, "GS": 20, "MU": 70, "SK": 5} | None | {"forschung": "Heimlichkeit", "stufe": 3}
- Meisterdieb | Diebesgilde | 8 | {"LE": 20, "AT": 40, "PA": 45, "SI": 70, "HE": 80, "RS": 0, "TP_min": 3, "TP_max": 8, "GS": 25, "MU": 80, "SK": 7} | None | {"forschung": "Heimlichkeit", "stufe": 5}
- Kundschafter | Diebesgilde | 10 | {"LE": 25, "AT": 50, "PA": 60, "SI": 85, "HE": 90, "RS": 1, "TP_min": 2, "TP_max": 9, "GS": 30, "MU": 90, "SK": 9} | None | {"forschung": "Heimlichkeit", "stufe": 8}
- Waldläufer | Diebesgilde | 16 | {"LE": 30, "AT": 60, "PA": 65, "SI": 90, "HE": 95, "RS": 2, "TP_min": 3, "TP_max": 10, "GS": 35, "MU": 100, "SK": 11} | None | {"forschung": "Heimlichkeit", "stufe": 10}
- Handkarren | Stellmacher | 1 | {"LE": null, "AT": null, "PA": null, "SI": null, "HE": null, "RS": null, "TP_min": null, "TP_max": null, "GS": 10, "MU": null, "SK": 0} | 40 | null
- Einspänner | Stellmacher | 2 | {"LE": null, "AT": null, "PA": null, "SI": null, "HE": null, "RS": null, "TP_min": null, "TP_max": null, "GS": 25, "MU": null, "SK": 0} | 100 | {"forschung": "Wagenbau", "stufe": 3}
- Zweispänner | Stellmacher | 3 | {"LE": null, "AT": null, "PA": null, "SI": null, "HE": null, "RS": null, "TP_min": null, "TP_max": null, "GS": 30, "MU": null, "SK": 0} | 250 | {"forschung": "Wagenbau", "stufe": 7}
- Handelskarawane | Stellmacher | None | {"LE": null, "AT": null, "PA": null, "SI": null, "HE": null, "RS": null, "TP_min": null, "TP_max": null, "GS": 25, "MU": null, "SK": 0} | 1000 | {"forschung": "Wagenbau", "stufe": 2}
- Große Handelskarawane | Stellmacher | None | {"LE": null, "AT": null, "PA": null, "SI": null, "HE": null, "RS": null, "TP_min": null, "TP_max": null, "GS": 30, "MU": null, "SK": 0} | 2500 | {"forschung": "Wagenbau", "stufe": 6}
- Siedlerkarren | Stellmacher | None | {"LE": null, "AT": null, "PA": null, "SI": null, "HE": null, "RS": null, "TP_min": null, "TP_max": null, "GS": 20, "MU": null, "SK": 0} | None | {"forschung": "Wagenbau", "stufe": 1}
- Belagerungsturm | Stellmacher | 2 | {"LE": null, "AT": null, "PA": null, "SI": null, "HE": null, "RS": null, "TP_min": 0, "TP_max": 0, "GS": 15, "MU": null, "SK": 35} | None | {"forschung": "Wagenbau", "stufe": 4}
- Ramme | Stellmacher | 3 | {"LE": null, "AT": null, "PA": null, "SI": null, "HE": null, "RS": null, "TP_min": 0, "TP_max": 4, "GS": 15, "MU": null, "SK": 25} | None | {"forschung": "Wagenbau", "stufe": 5}
- Großer Belagerungsturm | Stellmacher | 4 | {"LE": null, "AT": null, "PA": null, "SI": null, "HE": null, "RS": null, "TP_min": 0, "TP_max": 0, "GS": 15, "MU": null, "SK": 45} | None | {"forschung": "Wagenbau", "stufe": 6}
- Große Ramme | Stellmacher | 5 | {"LE": null, "AT": null, "PA": null, "SI": null, "HE": null, "RS": null, "TP_min": 0, "TP_max": 8, "GS": 15, "MU": null, "SK": 35} | None | {"forschung": "Wagenbau", "stufe": 7}
- Balliste | Stellmacher | 6 | {"LE": null, "AT": null, "PA": null, "SI": null, "HE": null, "RS": null, "TP_min": 1, "TP_max": 10, "GS": 15, "MU": null, "SK": 25} | None | {"forschung": "Wagenbau", "stufe": 8}
- Katapult | Stellmacher | 7 | {"LE": null, "AT": null, "PA": null, "SI": null, "HE": null, "RS": null, "TP_min": 2, "TP_max": 13, "GS": 15, "MU": null, "SK": 45} | None | {"forschung": "Wagenbau", "stufe": 9}
- Großes Katapult | Stellmacher | 8 | {"LE": null, "AT": null, "PA": null, "SI": null, "HE": null, "RS": null, "TP_min": 5, "TP_max": 18, "GS": 15, "MU": null, "SK": 55} | None | {"forschung": "Wagenbau", "stufe": 10}

## Waren (data/warenrezepte.json) — Kosten | Dauer | Voraussetzungen
- Messer | {"metall": 1} | 1200 | {}
- Dolch | {"metall": 2} | 2400 | {"Waffentechnik": 1}
- Kurzschwert | {"metall": 4} | 4800 | {"Waffentechnik": 3}
- Schwert | {"metall": 1} | 1200 | {"Waffentechnik": 5}
- Zweihänder | {"metall": 9} | 10800 | {"Waffentechnik": 8}
- Kettenhemd | {"metall": 4} | 4800 | {"Rüstungsbau": 3}
- Plattenrüstung | {"metall": 6} | 7200 | {"Rüstungsbau": 5}
- Magischer Paladinharnisch | {"metall": 10} | 12000 | {"Rüstungsbau": 7, "Magiekunde": 2}
- Kurzbogen | {"holz": 4} | 3600 | {"Waffentechnik": 2}
- Bogen | {"holz": 7} | 6000 | {"Waffentechnik": 4}
- Langbogen | {"holz": 10} | 8400 | {"Waffentechnik": 6}
- Armbrust | {"holz": 12} | 10800 | {"Waffentechnik": 8}
- Wollumhang | {"wolle": 1} | 1200 | {}
- Lederrüstung | {"leder": 4} | 4800 | {"Nähkunst": 1, "Rüstungsbau": 2}
- Diebesumhang | {"wolle": 3} | 3600 | {"Nähkunst": 2}
- Fellumhang | {"leder": 5} | 6000 | {"Nähkunst": 4}
- Fellrüstung | {"leder": 7} | 8400 | {"Nähkunst": 6}

## Gelaende (data/gelaende.json)
- {"id": "grasland", "name": "Grasland", "bebaubar": true, "haeufigkeit": 20, "farbe": "#5C7A3C", "farbe_rand": "#48602F", "_belegt": "Name und Ertraege belegt (Handbuch S. 10). Haeufigkeit VORSCHLAG."}
- {"id": "steppe", "name": "Steppe", "bebaubar": true, "haeufigkeit": 20, "farbe": "#8C7A4A", "farbe_rand": "#6E5F38", "_belegt": "Name und Ertraege belegt. Haeufigkeit VORSCHLAG."}
- {"id": "wald", "name": "Wald", "bebaubar": true, "haeufigkeit": 18, "farbe": "#3F6B24", "farbe_rand": "#2E4E1A", "_belegt": "Name und Ertraege belegt (Holzfäller Wald 4). Farbe im Rahmen der Original-Farbwelt (Forumslogo
- {"id": "huegel", "name": "Hügel", "bebaubar": true, "haeufigkeit": 13, "farbe": "#6E5A3C", "farbe_rand": "#54452E", "_belegt": "Name und Ertraege belegt (Steinmetz Hügel 2). Haeufigkeit VORSCHLAG."}
- {"id": "berg", "name": "Berg", "bebaubar": true, "haeufigkeit": 12, "farbe": "#5A5A62", "farbe_rand": "#44444A", "_belegt": "Name und Ertraege belegt (Steinmetz Berg 4, Erzmine 3). Haeufigkeit VORSCHLAG."}
- {"id": "nebelsee", "name": "Nebelsee", "bebaubar": true, "haeufigkeit": 7, "farbe": "#2F4A5A", "farbe_rand": "#243946", "_belegt": "Tempel auf Nebelsee: 8 Mana/h laut neuer Quelle WeitereWerteKampfsystem.odt S. 4; Handbu
- {"id": "sumpf", "name": "Sumpf", "bebaubar": false, "haeufigkeit": 10, "farbe": "#3A3A2A", "farbe_rand": "#2C2C20", "_belegt": "BEWIESEN: 'Sümpfe können nicht bebaut werden' (Handbuch S. 11). Haeufigkeit VORSCHLAG."}

## Gebaeude-Wirkungen (data/gebaeude_wirkung.json)
{
 "bevoelkerung": {
  "grund_je_siedlung": 10,
  "je_haus": 5,
  "siedler_je_stunde": 1,
  "heilkunde_prozent_je_stufe": 10,
  "startwert_ohne_siedlung": 10,
  "_belegt": "Handbuch Seite 11, wortwoertlich: 'Deine Siedlung bekommt, ausser den Rohstoffen, noch einen neuen Siedler pro Stunde, bis ihre Siedlergrenze erreicht ist. Diese Grenze liegt in jeder neuen Siedlung bei 10 Siedlern. Wenn Du in Deiner Siedlung Haeuser errichtest, erhoeht sich der Grenzwert um 5 Siedler pro Haus.' Heilkunde: 'Siedlerproduktion +10 % je Stufe' (ORIGINAL_Einheiten_Waren_Rohstoffe.md, Abschnitt 5).",
  "_startwert": "Vor der ersten Siedlung bekommt der Spieler den belegten Startwert von 10 Siedlern (Handbuch Seite 7) - sonst waere der Start unbewohnbar."
 },
 "forschung": {
  "bibliothek_noetig": true,
  "_belegt": "Handbuch Seite 12: 'Um Forschung zu betreiben musst Du in Deiner Siedlung zunaechst eine Bibliothek bauen.' Die Bibliothek selbst kostet keinen Forschungsaufwand (buildings.json: 'keine (ohne Forschung baubar)')."
 },
 "ausbildung": {
  "_belegt": "Handbuch Seite 14-17. Je Einheit steht das Gebaeude in data/units.json (Feld 'gebaeude'): Kriegerakademie 9 Kampfeinheiten, Diebesgilde 6 Kundschafter, Stellmacher 6 Karren + 7 Belagerungswaffen. buildings.json: 'Kriegerakademie, Diebesgilde und Stellmacher je hoechstens eines je Siedlung; hoehere Stufe = schnellere Ausbildung.'",
  "stufen_hoechstens": 5,
  "_stufen_vorschlag": "VORSCHLAG: Das Handbuch belegt, DASS die drei Ausbildungsstaetten Stufen haben, nennt aber keine Anzahl. Hier stehen 5 wie bei den Forschungsstufen (Handbuch Seite 13). Daniel kann die Zahl in dieser Datei aendern."
 },
 "verteidigung": {
  "wall_stufen_hoechstens": 10,
  "kriegspunkte": "ausbaustufe hoch drei",
  "_belegt": "data/buildings.json (Verteidigungswall, 10 Stufen von Erdwall bis Bollwerk mit Schwellenwerten) und ORIGINAL_Kampf_und_Punkte.md (Schwellen der Vorrunde, Kriegspunkte = Ausbaustufe hoch drei).",
  "_verteidigungsbonus_offen": "Die HOEHE des Verteidigungsboni ist NICHT belegt. Sie kommt weiterhin aus bonus_system.get_defense_bonus (+50 % je Stufe) - der Wall hat den erfundenen Wachturm dort ersetzt. Steht in docs/PROJEKT_STAND.md unter den offenen Entscheidungen."
 },
 "ausbaustufen_hoechstens": {
  "verteidigungswall": 10,
  "kriegerakademie": 5,
  "diebesgilde": 5,
  "stellmacher": 5,
  "bibliothek": 5,
  "haus": 4,
  "_vorschlag": "Wall 10 ist BELEGT (buildings.json). Haus bis Stufe 4, Bibliothek und die drei Ausbildungsstaetten: das Handbuch belegt nur, dass es Stufen gibt; die ZAHLEN sind VORSCHLAG (Haus: Vorgabe Daniel 05.10.2026 - 'der Haeuserausbau ist noch nicht klug entworfen'). Stufe 1 = das belegte Haus (+5 Siedler); jede weitere Stufe hebt die Siedlergrenze um weitere 5. Fuer alle anderen der 20 Gebaeude gibt es keinen Ausbau (null)."
 },
 "ausbau_linear": "Ausbau auf Stufe n kostet das n-fache des Grundpreises - dieselbe Regel wie in data/baupreise.json (dort als VORSCHLAG gekennzeichnet).",
 "haus_stufen": {
  "_hinweis": "VORSCHLAG (Entwurf deepseek-v4-pro, 05.10.2026, docs/audits/entwurf_ausruestung_forschung_haus_2026-10-05.txt, Abschnitt C). Stufe 1 ist das BELEGTE Haus (Handbuch Seite 11: +5 Siedler je Haus). Die Stufen 2-4 heben NUR die Siedlergrenze (+5 je Stufe), NICHT den Zuwachs (1 Siedler je Stunde) - der Zuwachs ist belegt und hat mit der Heilkunde (+10 % je Stufe) bereits seinen belegten Hebel.",
  "stufen": {
   "1": {
    "kosten": {
     "holz": 80,
     "stein": 50
    },
    "siedler": 5,
    "belegt": true
   },
   "2": {
    "kosten": {
     "holz": 160,
     "stein": 100
    },
    "siedler": 10,
    "belegt": false
   },
   "3": {
    "kosten": {
     "holz": 240,
     "stein": 150
    },
    "siedler": 15,
    "belegt": false
   },
   "4": {
    "kosten": {
     "holz": 320,
     "stein": 200
    },
    "siedler": 20,
    "belegt": false
   }
  }
 },
 "offene_luecken": {
  "werkstaetten": "Schmiede, Bogenbauer und Naehstube stellen im Original Waren her. Das Waren-Handwerk fehlt noch - Paket W3 (PROJEKT_STAND.md, Abschnitt 5).",
  "baukunst": "Das Original verlangt fuer die meisten Gebaeude die Forschung 'Baukunst' (Holzfaeller, Steinmetz, Jaeger, Bibliothek und Haeuser sind ohne Forschung baubar). Im Spiel stehen noch die 18 erfundenen Forschungsgebiete; 'Baukunst' gibt es dort nicht. Die Bauregel greift daher erst mit dem Paket, das die 21 Originalforschungen ins Spiel holt.",
  "lager": "Der Lager-Eintrag (buildings.json) beschreibt eine Uebersicht ueber Waren und Einheiten - das ist die Ansicht 'Lager' im Menue, keine Zahl."
 }
}

## Welten/Portal (data/welten.json)
{
 "welten_belegt": [
  "Armageddon",
  "Ragnaroek",
  "Utgard",
  "Midgard",
  "Valhalla",
  "Limbus"
 ],
 "belegte_regeln": {
  "felder_je_dimension": 20,
  "felder_je_dimension_gesamt": 400,
  "_belegt_felder": "Woertlich (portal.php 2005, Z. 22): 'in jeder Dimension sind 20 mal 20 Felder frei fuer Spielerwelten.' Also 20 x 20 = 400 Felder je Dimension.",
  "portalkoordinaten": "X und Y sind die Position im Feld der Dimension, Z ist die Dimension selbst (portal.php 2005).",
  "koordinatenwechsel": {
   "kosten_mana": 5000,
   "hoechstens_je_stunden": 24,
   "_belegt": "Woertlich (portal.php 2005, Z. 25): 'Welt an ihren neuen Platz verschiebt. Sie benoetigen hierfuer 5.000 Mana.' sowie 'Ihr habt die Moeglichkeit, einmal binnen 24 Stunden, eure Koordinaten zu wechseln.'"
  },
  "bannerfarben": {
   "eigene_welt": "gruen",
   "fremde_welten": "rot",
   "_belegt": "Woertlich (portal.php 2005): 'Eure Welt wird durch ein gruenes Banner markiert, fremde Welten durch rote.'"
  }
 },
 "ebene": {
  "_hinweis": "VORSCHLAG: Die 20 Dimensionen werden hier als je ein Punkt in einer 10x10-Ebene (x/y von 0 bis 9) dargestellt. Im Original ist JEDE Dimension ein eigenes 20x20-Raster (belegt, portal.php); diese Uebersicht fasst jede Dimension zu einem Punkt zusammen. Die konkreten x/y-Werte sind NICHT belegt.",
  "x_von": 0,
  "x_bis": 9,
  "y_von": 0,
  "y_bis": 9,
  "anzahl": 20
 },
 "portalregel": {
  "art": "manhattan",
  "grundbetrag": 100,
  "kosten_je_schritt": 25,
  "standart_umkreis": 3,
  "formel": "mana = grundbetrag + kosten_je_schritt * entfernung_in_schritten",
  "_belegt": "Belegt: die Portalkosten haengen von der Entfernung ab; in eine andere Dimension zu reisen kostet deutlich mehr Mana (Handbuch 2009, S. 82; portal.php 2005).",
  "_vorschlag": "VORSCHLAG: als einfache Regel Grundbetrag 100 Mana plus 25 Mana je Schritt. Die genauen Zahlen sind NICHT belegt und duerfen geaendert werden."
 },
 "dimensionen": [
  {
   "kennung": "d01",
   "name": "Armageddon",
   "x": 0,
   "y": 0,
   "welt": "Armageddon",
   "_belegt": "Weltname Armageddon belegt (alte Website, screens.php).",
   "_vorschlag": "Lage x=0, y=0 im Limbus-Raster - VORSCHLAG."
  },
  {
   "kennung": "d02",
   "name": "Ragnaroek",
   "x": 9,
   "y": 0,
   "welt": "Ragnaroek",
   "_belegt": "Weltname Ragnaroek belegt (alte Website, screens.php).",
   "_vorschlag": "Lage x=9, y=0 im Limbus-Raster - VORSCHLAG."
  },
  {
   "kennung": "d03",
   "name": "Utgard",
   "x": 0,
   "y": 9,
   "welt": "Utgard",
   "_belegt": "Weltname Utgard belegt (alte Website, screens.php).",
   "_vorschlag": "Lage x=0, y=9 im Limbus-Raster - VORSCHLAG."
  },
  {
   "kennung": "d04",
   "name": "Midgard",
   "x": 5,
   "y": 5,
   "welt": "Midgard",
   "_belegt": "Weltname Midgard belegt (alte Website, screens.php).",
   "_vorschlag": "Lage x=5, y=5 im Limbus-Raster - VORSCHLAG."
  },
  {
   "kennung": "d05",
   "name": "Valhalla",
   "x": 4,
   "y": 4,
   "welt": "Valhalla",
   "_belegt": "Weltname Valhalla bel


==============================================================================
D1  OFFENE LUECKEN, wie die Module sie selbst ausweisen
==============================================================================

### auftraege.offene_luecken()
```json
{
 "reisezeit_formel": "Die Formel aus Entfernung und Geschwindigkeit ist VORSCHLAG (SEKUNDEN_JE_FELD = 3600 s je Feld bei Geschwindigkeit 1). Das Handbuch (S. 19) nennt nur Beispielstunden, keine Formel.",
 "drosselung": "BELEGT ist die Drosselung in 10-%-Schritten (Handbuch S. 20); wie sie die Reisezeit aendert, sagt das Handbuch nicht. Sie ist hier als Konstante DROSSELUNG_SCHRITTE_PROZENT abgelegt, aber nicht auf die Formel angewandt.",
 "aktion_dauer": "Die Dauer der Handlung am Ziel ist VORSCHLAG (AKTION_DAUER_SEKUNDEN = 0). Fuer stationieren/transportieren/angreifen nennt das Handbuch keine Aufenthaltsdauer; handeln wartet laut Entwurf auf eine Bestaetigung ohne bezifferte Dauer.",
 "beute_anteil": "Der Beute-Anteil ist VORSCHLAG (BEUTE_ANTEIL_PROZENT = 50). Der Entwurf selbst nennt ihn ausdruecklich offen ('Was Daniel entscheiden muss', Punkt 3); das Handbuch beziffert die Beutemenge nicht.",
 "geschwindigkeit_wahl": "VORSCHLAG: das Tempo des Auftrags ist die langsamste mitgefuehrte Einheit (min GS). Das Handbuch nennt keine Regel fuer gemischte Gruppen.",
 "fusstruppen_begriff": "VORSCHLAG: als Angreifer-Fussttruppen zaehlen Kampf- UND Kundschaftereinheiten (einheiten.ist_kaempfer). Der Begriff ist im Handbuch nicht definiert.",
 "stationieren_fremd": "BELEGT ist das Verbot in fremden Siedlungen (S. 19). WIE ein Ziel als fremd erkannt wird, sagt das Handbuch nicht; hier entscheidet das Feld 'fremd' am Ziel. Ein reiner Zielname gilt als eigene Siedlung.",
 "kosten": "Reisekosten (Gold/Nahrung/Mana) sind hier leer gelassen: das Handbuch nennt sie, beziffert sie aber nicht je Auftrag. Es wird kein Wert erfunden.",
 "handel_gold": "Beim Handeln ist kein Goldpreis erfunden. Ohne Feld 'gold_bietet' am Ziel gibt es 0 Gold; eine Ablehnung bringt die Waren zurueck (S. 20).",
 "beute_ohne_karren": "BELEGT (S. 23): Beute gibt es nur mit Transportkarren. Ohne Karren bleibt die Beute leer, auch wenn Vorraete uebergeben werden."
}
```

### kampfbericht.offene_luecken()
```json
{
 "fusstruppen_begriff": "Der Begriff 'Fußtruppen' der Vorrunde ist im Handbuch nicht definiert. kampf.py zaehlt Nahkampf- UND Fernkampfeinheiten dazu; die engere Lesart (nur Nahkampf) ist nicht ausgeschlossen.",
 "flucht_formel": "Zum Fliehen unter LE 5 nennt das Handbuch nur 'je niedriger der MU, desto wahrscheinlicher', aber keine Formel.",
 "beute_verteilung": "Die Beute ist auf die Karrenladung begrenzt, eine Aufteilung auf die Rohstoffe ist nicht geregelt. Hier gilt: anteilig nach Vorratsmenge.",
 "beute_reihenfolge": "In welcher Reihenfolge Rohstoffe verladen werden, ist nicht geregelt (hier alphabetisch).",
 "belagerungsturm_mauerschaden": "Belagerungsturm und Grosser Belagerungsturm haben Mauerschaden 0-0: sie brechen keine Mauer, tragen aber Schlagkraft zur Vorrunde bei.",
 "mauer_reparatur": "Ob und wie sich eine beschaedigte oder eroberte Mauer erholt, sagt das Handbuch nicht.",
 "vorrunde_wiederholung": "Wie viele Versuche ein Angreifer gegen den Wall hat, ist offen.",
 "geraetebeute": "Ob erbeutete Karren und Belagerungswaffen mitgenommen werden koennen, ist nicht geregelt."
}
```



==============================================================================
D2  Bekannte Fehler und Designpruefungen (docs/Fehlerregister_Nebelseetal.md)
==============================================================================

# Vollständiges Fehlerregister und Reparaturwege (GPT, 28.10.2026)

**Quellenhierarchie:** Originalspielanleitung (`docs/original/Nebelseetal_Spielanleitung_2009.pdf`, Deckblatt 01.09.2006) > Daniels ausdrücklich entschiedene Remake-Werte/Schritte > als **Vorschlag** markierte Preise/Zeiten. Die beigefügten `docs/`-Pläne und neuester Code-Stand sind entscheidend. Nur Hermes ändert gemeinsame Dateien. **„Befund“ bedeutet reproduziert, nicht behoben.** Alle Zeilen sind auf den übergebenen ZIP-Code-Stand bezogen, nicht auf zukünftige Commits.

## Bestätigte Fehler

### F01 — Reichs-/Ortsbestand wird doppelt als Geldquelle behandelt [KRITISCH, neue Reproduktion]
- **Quelle:** `src/main.py`: `GameState.tick` schreibt lokale Ertragsdifferenz auch nach `resources[res].amount` (um Z. 2069–2072). `ortsdeckung`, `reichsdeckung`, `verbrauche_am_ort`, `verbrauche_reichsweit` verwenden diese `resources` später als **zusätzliche** eigenständige Geldquelle (ca. Z. 903–998). Dasselbe Risiko besteht mit `population` + `bevoelkerung`.
- **Echte Probe:** `test_gpt_doppelkasse.py` baut einen Holzfäller auf Wald und tickt 3600 Spielsekunden. Im einzigen Ort entstehen nach Original **4 Holz**. Reichsanzeige wird ebenfalls auf **4** gesetzt. Danach akzeptieren sowohl lokaler als auch reichsweiter Zahlweg **7 Holz** – mehr als physisch vorhanden. Zwei Warenbestände wurden aus einer Ernte erzeugt; eine Buchung kann den Spiegel auseinanderziehen. Auch 5 tatsächliche Siedler + gespiegelte 5 werden zu fälschlichen 10 verfügbaren Siedlern addiert.
- **Fixweg (Hermes):** Zuerst Entscheidung für eine **einzige** führende Bestandsquelle je Spielmodus. Im Neumodus `oeokonomie-1` ausschließlich lokale `Settlement.vorraete` und `bevoelkerung` als physische Lager; Reichsübersicht als **berechnete Anzeige**, nicht eine zweite Kasse. `tick` soll keine zusätzliche freie Ernte schaffen; Tests gegen Produktion im Ort und UI-Summendarstellung nachziehen. Bei global wirklich erlaubten Aktionen klaren Ort/Quellmenge und echte Abbuchungsorte festlegen (z. B. Mana-Kosten nach Original nachprüfen). Für `legacy` getrennte, nicht-destruktive Behandlung und Save-Migration. Vorab Deckung, danach atomare Abbuchung, nie negativ. **Nicht** einfach nur die globale Zuwachsbuchung löschen, solange andere Leser davon abhängen.
- **Abnahme:** `test_gpt_doppelkasse.py --strict` grün (5 bisher fehlschlagende Erwartungen); 4 Holz nach 1 h, Zahlung 7 Holz verweigert, Siedler nicht doppelt; Save/Load, alle Ressourcenzähler, Bau/Transport/Handel/Kampfbeute prüfen.
- **Abhängigkeit:** F02 ist ein **Folgefehler desselben Kassenkonzepts**. Gemeinsamen Fix planen, sonst verbleiben Scheineinkünfte.

### F02 — Ortsfremder Bau ohne Karren durch globale Übergangskasse [HOCH, reproduziert]
- **Quelle:** `src/main.py`: `ortsdeckung()` und `verbrauche_am_ort()` ergänzen fehlendes Ortsholz aus `GameState.resources`, selbst bei `mode='oeokonomie-1'`.
- **Echte Probe:** Dorf A 0 Holz, Dorf B 100 Holz, Reichsressource 100 Holz. `ortsdeckung(A,{'holz':10})` meldet keine Fehlmenge; `verbrauche_am_ort(A,{'holz':10})` liefert `True`; B behält 100 Holz, der Reichszähler sinkt nur 100→90. Es existiert **kein** Karren-/Transportauftrag.
- **Fixweg:** Derselbe F01-Hauptpatch macht Ortsbau im Neumodus strikt ortsgebunden; nur eine abgeschlossene Transportmission erhöht das Ziellager. Übergangskasse `legacy` **nicht** ohne Migration entfernen. Bei globalen Aktionen Quelle/Empfänger und Recht auf Teilzahlungen explizit festlegen, damit keine „Fernkasse“ entsteht.
- **Abnahme:** `test_gpt_integrationsrisiken.py --strict` grün für die beiden Ortskassenproben; zusätzlich echter Versand mit Handkarren → Ankunft → Rückkehr; Fehlbuchung vor Ankunft weiterhin unmöglich.

### F03 — Farm ohne Baukunst auf Grasland gebaut [HOCH, reproduziert]
- **Original:** Handbuch Siedlungs-Baumenü: frei ab Start sind **Holzfäller, Steinmetz, Jäger, Bibliothek, Haus**. Weitere Gebäude benötigen Kenntnisse in **Baukunst**.
- **Quelle:** `src/main.py`: `bauen_auf_karte(siedlung,'farm',feld)` prüft Feld, Gelände, Limit, nicht den Forschungsstand; UI `_karten_bauen()` ruft den Weg ohne Baukunst-Check auf. Test mit Grasland und 0 Baukunst ergibt `True`.
- **Fixweg:** Zentrale `bau_zulassen`-Prüfung **vor Feldmutation und Abbuchung**, die die erforderliche Forschungsstufe über die vorhandene Forschungsquelle ermittelt. Engine+GUI dieselbe Funktion verwenden, Baupreise/Feld/Limit weiter prüfen. Keine späteren Altbauten automatisch abreißen. Optional Bauaktion **atomar** gestalten (Bezahlung und Platzierung als eine Transaktion), damit ein abgelehnter Bau nichts verändert.
- **Abnahme:** `test_gpt_integrationsrisiken.py --strict` (Farm nicht baubar ohne Baukunst, Holzfäller frei, Sumpf gesperrt), zusätzlich Baukunst vorhanden → Farm möglich, ungenügende Ortspreise → keine Feldänderung.

### F04 — Mehrere ganze Tage in einem Tick nur als EIN Tag gezählt [HOCH, GPT-001]
- **Quelle:** `GameState.tick()`, um Z. 2091: `_day_accum += dt_seconds; if _day_accum >= 86400: ...; day += 1`.
- **Echte Probe:** 7 Tage (=604800 s) als ein einziger Tick: `day == 2` statt `8`, `_day_accum == 518400` statt `0`; Götterschutz bleibt aktiv, obwohl nach Handbuch nach 7 Tagen enden muss (wenn nicht bereits der erste Kriegspunkt ihn beendet). Dieselben 7 Tage als sieben Einzel-Ticks liefern `day == 8` und beendeten Schutz.
- **Fixweg:** `divmod(_day_accum + dt_seconds, 86400)` oder gleichwertige ganzzahlige Tagesanzahl statt `if`. Historische übergroße `_day_accum` in Altständen nicht ohne Migrationsprüfung uminterpretieren. Götterschutz für Null-Kriegspunkte und ersten Kriegspunkt separat prüfen.
- **Abnahme:** `test_gpt_tageswechsel.py --strict`, gemischte kleine/große Ticks, Speicherstand und Schutz; die 8 Befunde sind Varianten *einer* Ursache.

## Nachgewiesene Integrations-/Abnahme-Lücken (nicht als eigene Logikfehler ausgeben)

### A01 — EXE entspricht nicht letztem Quellcode [RELEASE-FREIGABE OFFEN]
- Die mitgelieferte EXE `c1523670...` entspricht der am 06.10. um 08:22 dokumentierten Version, während der neue Quellcode danach `tick_bis()` in `GameState.tick()` verdrahtet (ZIP-Commit `1c4dffa...`). Die Screenshots vom 23.10. zeigen nach Daniels Auskunft den damaligen Stand; keine jüngere Entwicklung.
- **Aktion:** Erst Hermes' laufenden Schritt fertigstellen, dann kontrolliert neu bauen, echte EXE aus fremdem Arbeitsverzeichnis starten und Hash/Commit/Testprotokoll festhalten. **Keine** Behauptung, neuere Quelle sei schon in aktueller EXE.

### A02 — Durchspiel/Balance nicht hinreichend belegt [RISIKO, kein bewiesener Einzeldefekt]
- Originalraten im Code stimmen in Stichproben (77 Kontrollen), aber das beweist **nicht**, dass ein Spieler Holz, Stein, Nahrung, Metall, Leder, Wolle, Pferde und Mana in jeder erlaubten Baufolge in sinnvoller Menge erreichen kann. Daniels beobachtete Sackgassen sind ernst zu nehmen; einzelne davon können aus F01/F02 folgen.
- **Aktion:** Für neue Startspiele alle Kartentypen, einige deterministische Seeds, 0/1/6/24/72 Spielstunden und typische Bau-/Forschungsfolgen simulieren. Vergleiche Ort vs. Reich, offene Felder, fehlende Waren, Warteschlangen und Karrenverfügbarkeit. Testziel ist **Planbarkeit**, nicht Unbesiegbarkeit jeder ungünstigen Entscheidung. Warnhinweise statt kostenlose Rettungsrohstoffe. Nur **Vorschlagspreise/Dauern** anhand gemessener Pacing-Ziele kalibrieren; nie Originalstundenraten still ändern.

### A03 — Sieggrenze 300 Punkte gegen Originalwallpunkte [DESIGNPRÜFUNG]
- Originalregel ist `Kriegspunkte += Wallstufe³`, Gesamtpunkte `(Krieg+Forschung)/2`. Stufe 10 bringt also **korrekt 1000 Kriegspunkte**, kein Wertefehler. Ein Sieg bei 300 Gesamtpunkten ist dagegen eine Remake-Zielzahl und kann die Mehrsiedlungs-Wirtschaft zu früh beenden.
- **Aktion:** Hermes soll die Erreichbarkeit über einen echten Spieldurchlauf messen; höchstens eine Entscheidungsvorlage für Daniel, kein selbstständiges Regelüberschreiben.

### A04 — Kartenvorrat-Projektwiderspruch [ENTSCHEIDUNG OFFEN]
- Dokumentation nennt „Startkarte + 10 Karten“, die geprüften Vorlagen ergeben „Startkarte + 9“ = 10 Kartentypen (8×7, 40 Baufelder). **Nicht** still eine Karte erfinden oder die Historie umschreiben. Im neuen laufenden Projekt prüfen, ob explizit bereits behoben.

### A05 — Nicht vollständige plattformgerechte Endabnahme [TESTLÜCKE]
- 21 ältere Basistests wurden einzeln versucht: 18 Exit 0, zwei GUI-Tests brauchten Display, einer Windows `TEMP`; ein angefangener Xvfb-Sammellauf wurde nicht abgeschlossen. Das sind **keine bestätigten Spielefehler**, aber keine Grundlage für ein freigegebenes Build.
- **Aktion:** `run_tests.bat` auf Windows; echte 15-Minuten-Partie, Neustart, Laden, Sieg/Niederlage, Transport+Kampf, Langzeit-/Mehrtick-Test, Leerlauf/Freeze-/Prozesszahl prüfen.

## Ausdrücklich KEINE Fehler
- 8×5 auf alten `legacy`-Screenshots, obwohl die neue Vorgabe 8×7 lautet: Legacy-Karte kann bewusst unverändert sein. **8×7 nur für neue Partien verifizieren.**
- 1000 Kriegspunkte durch einen Verteidigungswall Stufe 10: **korrekte Originalrechnung**.
- 28 Originaleinheiten, 17 Waren, 21 Forschungen und die getesteten Produktionserträge: nach den unabhängigen Kontrollen aktuell konsistent. Die vollständigen Laufzeitwirkungen jeder Einheit sind **nicht** damit bewiesen.

## Wichtigste Dateien / Prüfungen
- `01_TESTS/tests/test_gpt_doppelkasse.py` → F01 (Normalmodus 4 OK / 5 Befunde, strict 5 erwartete Fehler)
- `01_TESTS/tests/test_gpt_integrationsrisiken.py` → F02/F03 (Normalmodus 4 OK / 3 Befunde, strict 3 erwartete Fehler)
- `01_TESTS/tests/test_gpt_tageswechsel.py` → F04 (Normalmodus 13 OK / 8 Befunde, strict erwartete Fehler)
- `01_TESTS/tests/test_gpt_originaltreue.py` → Originaldaten (77 OK)
- `01_TESTS/tests/test_gpt_produktion_truppen_kette.py` → Daten-/Kettenplausibilität (171 OK)
- `01_TESTS/tests/test_gpt_versorgungsdiagnose.py` → Diagnose (15 OK)
- `03_BELEGE/` alle echt erfassten Ausgaben.




==============================================================================
D3  Aktueller Stand (docs/AKTUELLER_STAND.md)
==============================================================================

> **KORREKTUR / neuester Stand (FIX05, Stand 30.10.2026):** Die oeffentliche FIX04j-Test-EXE wurde laut bestaetigtem Nutzertest gestartet, gespeichert und geladen; aeltere Aussagen "noch keine gebaute EXE" unterhalb sind historisch ueberholt. **FIX05 ist am 30.10.2026 kontrolliert in dieses Projekt uebernommen** (11 von 12 Delta-Dateien, jede gegen ihren Manifest-Hash geprueft; `tools/originalkarten_grafiken_bauen.py` bewusst NICHT uebernommen, weil die Delta-Fassung nur ein doppeltes Backslash im Moduldocstring einfuehrt). Neu: Tempo-Einstellung liegt im privaten Laufzeitordner (`~/.nebelseetal/spielzeit_einstellung.json`) statt im PyInstaller-Buendel; Fehlerdialog bei Schreibfehlern; sechs neue Tempo-Regressionen. Neue 10x10-Originalkartenpruefung und alle offenen 25 Sichtpruefungen im `docs/quellen/CODE_UND_KARTENPRUEFUNG_FIX05.md` dokumentiert. **Windows-Neubau der EXE, vollstaendige Regression und Nutzerabnahme (Start/Speichern/Neustart/Laden) stehen noch aus** — die Uebernahme ist Code, nicht Freigabe.

> **WICHTIGER NEUERER STAND (FIX04j, 28.10.2026):** Oeffentliche Test-EXE wird getrennt vom Admin-Entwicklerbuild vorbereitet. Das Repository enthaelt **saemtliche** Admin-Module und Dokumente; nur der oeffentliche EXE-Einstieg bietet keine Admin-UI. Es liegt hier **noch kein gebauter und unter Windows abgenommener FIX04j-Release** vor. Details: `docs/RELEASE_PUBLIC_FIX04j.md`, neuester Protokollabschnitt. Aeltere Statusangaben weiter unten sind historisch und nicht automatisch gueltig.

> **Neuester isolierter GUI-Stand FIX04i (28.10.2026):** Im Adminbereich sind Ressourcen und Aktionen auf getrennten Zeilen; das Schildmotiv der vorhandenen Ladebild-PNG wird in Spieler- und Admin-Speicherfenstern als Hintergrund angezeigt, mit lesbarem Bedienfeld. Fachlogik von FIX04h bleibt erhalten. Neue und benachbarte Tests erfolgreich; **Windows- und EXE-Abnahme ausstehend.**

> **Neuester isolierter Entwicklungsstand FIX04h (28.10.2026):** Spielstandverwaltung aufgeraeumt: normale Spieler sehen nur aktive Slots und keine archivierten Fassungen; explizite Wiederherstellung nur im autorisierten Admin-Entwicklerarchiv mit klarer Slotzuordnung. Archivgroesse wird lesend angezeigt, keine automatische Loeschung. Kuenftige Beibehaltung/Begrenzung/Abschaltung des Entwicklungsarchivs **offen**. FIX04g unter Windows vom Nutzer bis Save→Archiv→Restore→Load bestaetigt; FIX04h erst unter Linux/Xvfb getestet, Windows-Neubau noch ausstehend.

> **Neuester isolierter Entwicklungsstand FIX04g (28.10.2026):** Pflicht-Starthilfe bis echte Grundproduktion, Admin-Hilfeausnahmen, private datierte Spielstandarchive, Spieler-/Admin-Slotverwaltung, manuelles Wiederherstellen. Details: `docs/ENTWICKLUNGSPROTOKOLL.md` / `docs/HERMES_UEBERGABE_AKTUELL.md`. **Nicht** als Windows-Release getestet; lokaler Windows-/GitHub-Stand kann abweichen.

# Nebelseetal Remake – EINZIGER aktueller Entwicklungsstand

**Stand:** 28.10.2026 | **Arbeitskopie:** konsolidierter GPT-Entwicklungsstand nach FIX01 und Originalkarten-Umstellung. **Nicht:** Hermes-HEAD / freigegebene Windows-Version.

## Projektstruktur

- `src/`: ein aktiver Spielcode; Einstieg `src/main.py`, Originalgrafik-Zuordnung `src/originalkarten_grafik.py`, Karten-Daten `src/originalkarten.py`.
- `assets/`: aktuell benötigte Spielgrafiken; `assets/karten/original/` die 127 unveränderten Quellbilder, `assets/karten/spielfeld/` die 127 daraus für den Spielbetrieb hergeleiteten 640×640-PNGs (nearest neighbor, keine erfundenen Landschaftssymbole).
- `data/`: Regeln und aktueller Originalkarten-Katalog (`originalkarten/katalog.json`, Grafikmanifest).
- `tests/`: aktive Tests; ältere 8×7-Tests liegen separat im Archiv und gelten **nicht** als bestanden.
- `tools/`: Bau-/Test-/Quellenwerkzeuge, z.B. `originalkarten_grafiken_bauen.py`, `build_exe.py`.
- `docs/`: ein aktuelles `ENTWICKLUNGSPROTOKOLL.md`, eine aktuelle Hermes-Übergabe, Quellen und aktueller Status.
- `archiv/`: alte Zwischenstände, Tests, Protokollfassungen, alte Übergaben, Bildstudien; **nicht veröffentlichen**.

## Aktueller Spielstand nach Systemen

| Teil | Implementiert / Bedeutung | Noch offen |
|---|---|---|
| Siedlungskarten | 127 historisch belegte Originalbilder, im Spiel als Bilder statt Zeichenvorschlag; 10×10-Daten/Index; freier Kartenvorrat | 25 automatisch klassifizierte Kartenraster visuell noch nicht abgenommen; Raster-Bild-Kongruenz manuell prüfen |
| Gelände | Originalbild zeigt Wald-Baumgruppen, Fels-/Berg- und Grasfelder, Gebäude/Wege/Koordinaten als separate Überlagerung | Unterschiede zwischen Pixelbild und automatisch erkanntem Feldtyp für die 25 ungeprüften Karten korrigieren |
| Frühere 8×7-Karten | Generator und Kartentypen im aktiven Spiel **abgeschaltet**; Quellen/Tests archiviert | Ältere Savegames nur als historische Dateien; keine automatische Migration / kein stilles Zurückkehren der alten Welt |
| Produktion / Wirtschaft | lokales Ortslager, Holz/Stein, Waren, Ausbildung, Forschung, Karren | Altprüfungen auf Originalkarten umstellen, echte Regressionen reparieren, keine kostenlosen Bot-Ressourcen |
| Bau-Menü | Bau-/Auswahlfunktionen; Screenshots `docs/nebelseetal_gamestar2.jpg` als Referenz | historische Bauoberfläche (Navigation, Kosten, Siedlerbedarf, Baufelder) noch nicht vollständig nachgebaut |
| Kampf / Mauern / Bots | Grundfunktionen, lokaler Wall/Kampf/Beute | KI-Ökonomie, Belagerung, gesamter End-to-End-Durchlauf |
| Speichern / Laden | 3 Spielerslots und Adminbereich, Schutz vor nicht-originalen Kartenständen im Ladepfad | Reale Windows-Spielstände prüfen; kein verdecktes 8×7-Upgrade; nötigenfalls getrennte manuelle Import-Routine mit Freigabe entwerfen |
| Windows EXE | Python-Spiel plus `.bat`-Buildablauf | **Keine** aktuelle auf Windows neu kompilierte/verifizierte EXE in dieser Lieferung |
| GitHub | Öffentliche Seite `Decay03101991/Nebelseetal-Remake` | Hermes nach Rückübernahme zuständig für geprüfte Commits, Protokoll- und README-Pflege; keine Zugangsdaten/Archive veröffentlichen |

## Getestet und nicht getestet

- Vor der Originalgrafik-Umstellung: 35 ausgewählte Tests, 34 erfolgreich, 1 alter Kartenansichtstest mit 11 Fehlkontrollen. Nicht als komplette Suite zählen.
- Nach der Umstellung: neuer Originalkarten-Test besteht mit **7/7**; darin Nachweis aller 127 Bilddateien, Bilddatei-Prüfsummen, GUI-PhotoImage-Smoketest und Sperren gegen Legacy-Karten.
- Separate Nachbartests wurden selektiv geprüft; nicht alle älteren Testfälle gelten für die aktuelle Datenstruktur (siehe `archiv/tests_legacy_8x7/`).
- **GPT-FIX02 (28.10.2026):** `test_startspiel.py` nun **61/0/1** (Nahrung vs. Holz-Grundrate korrekt, 100 Originalkarten-Feldtags, Baukunst->Akademie->Ausbildung). `test_durchspiel.py` **64/0/2** (Bauen/Forschung/Ausbildung/Handel/Save/Load/Portal/Werkstatt inklusive Fertigstellung). `test_gpt_wall_gui.py` **4/4**, neuer `test_gpt_originalkarten_feldklick.py` **2/2**. 24 gezielt ausgewählte Testdateien nach Korrekturen gruen; `test_gui_fehler.py` anfangs blockiert, nach Ersetzung veralteter Dialog-/Wall-/Slot-Annahmen **23/0/1**. Dies ersetzt die alten historischen Befunde NUR fuer diese geprueften Dateien, nicht fuer die Gesamtsuite.
- Keine reale Windows-EXE, keine vollständige Windows- oder Gesamtspielabnahme. Release-Status: **NEIN**.

## Next actions für den temporären Coding-Agenten

1. Original-Raster und sichtbares Originalbild für die 25 Karten manuell Feld für Feld abnehmen; automatische Klassifikation nicht ungeprüft korrigieren.
2. Historische Wirtschafts-/Baumenü-Tests mit 10×10-Originalkarten neu aufbauen (Archiv bewahren), fehlende UI-Funktionen implementieren.
3. Bot-Ökonomie, Handel, Produktion, Kampf, Save/Load als echte Spielrunde nachweisen.
4. Unter Windows aus `EXE_NEUESTEN_STAND_BAUEN.bat` kompilieren, startetest und Releaseprüfung.
5. Hermes nach Rückkehr gegen sein reales Git-HEAD vergleichen lassen; nur nach Tests offizielles Repo aktualisieren.

**Führende Detaildokumente:** `docs/HERMES_UEBERGABE_AKTUELL.md`, `docs/HERMES_KONTROLLE_UND_SKILLS.md`, `docs/KARTEN_NUR_ORIGINALE.md`, `docs/ENTWICKLUNGSPROTOKOLL.md`.

**Zusaetzlicher Speichertest (28.10.2026):** `tests/test_originalkarten_savegames.py` ist mit 2/2 gruen: eine neue echte Originalkarte uebersteht Save/Load und eine alte 8x7-Karte wird vor Zustandsschaeden abgewiesen.


## Letzte Entwicklungsrunde – GPT-FIX02, 28.10.2026

Die einzige aktive Spiellogik-Aenderung ist in `src/main.py`: 100 unsichtbare Felderkennungen ueber dem unveraenderten Originalkartenbild. Dazu wurden die Durchspiel-/Wall-/Starttests auf reale Spielregeln und Originalkarten angepasst und eine neue GUI-Regression ergaenzt. **24 selektierte Testdateien bestehen, darunter der reparierte GUI-Aktionstest mit 18 Ansichten/13 Aktionen.** Kein neuer Windows-Build. Keine GitHub-Aktualisierung – die erfolgt auf ausdruecklichen Wunsch Daniels erst am Ende. Alle Einzelheiten und Befunde siehe `docs/ENTWICKLUNGSPROTOKOLL.md` Abschnitt GPT-FIX02.


### Ergänzende Originalkarten-Bauprüfung – GPT-FIX02b

`tests/test_gpt_originalkarten_baukasse.py`: unter Tkinter/Xvfb **4/4 erfolgreich**: Ortslager-Zahlung ohne Doppelbuchung, belegte Felder bleiben unverändert, Rohstoffmangel ohne Seiteneffekte, echtes Originalkartenbild nach Bau. Damit sind **25 ausgewählte Testdateien** grün. Die 11 alten Kartenansicht-Fehlkontrollen sind noch **nicht** vollständig ersetzt (siehe einziges Entwicklungsprotokoll). Kein neuer Windows-Build oder GitHub-Push.


## Zusatzprüfung GPT-FIX02c (28.10.2026)

Der von Daniel wieder zusammengesetzte Stand ist bytegenau identisch mit dem FIX02-Paket (1.229 Projektdateien). Zusätzlich lokales `.git` aus altem Hermes-Head, aber **kein** aktueller Windows-EXE-Build. Historische Protokoll-/Zielübergabe-Pfade in isolierter Kopie korrigiert (belegt im einzigen Entwicklungsprotokoll). Zehn zentrale Spieltestdateien nach Entpackung bestanden; die vollständige Testsuite und ein Windows-Praxistest fehlen. Neue GitHub-Fassung darf erst nach Sichtung des GitHub-Clone-Diffs, Geheimnis-/Rechtekontrolle und echter Windows-Prüfung zum Release werden.

**FIX02c Buildgate-Nachtrag:** Vorprüfskript auf vorhandenen Originalkarten-Katalogtest korrigiert; 6/6 unter Linux/Xvfb erfolgreich. Keine Windows-EXE vorhanden oder freigegeben. Drei fehlende Tests im historischen GPT-Abschluss-Teststarter bleiben offen.


### FIX04 – aktueller isolierter Entwicklungsstand vom 28.10.2026

- Kartenbild: weiterhin ausschliesslich die authentischen 127 Siedlungskarten 10x10; Originalbilder nicht veraendert.
- Siedlungs-Baumenue: Bereiche Produktion/Werkstatt/Ausbildung/Verteidigung/Sonstiges im Auswahlfeld, je Bauangebot Zweck, Ertrag, Preis, Siedler- und Forschungsbedarf sowie konkrete Sperr-/Fehlmengen. Eine einzige Baukasse und ein einziger Bauaktionsweg bleiben erhalten; Dorfwall bleibt separate Siedlungsfunktion.
- GUI-Kontrolle: neuer FIX04-Test **5/5**, Spielstarttest **61/0/1** nach korrigierter Beschriftungserwartung; weitere ausgewählte Spieltests bestanden. Vollsuite und Windows-FIX04-EXE noch offen.
- Letzter praktischer Windows-Build: FIX03 unter Python 3.11.16 (Astral), von Daniel mit funktionierendem Start, Admin und Speichern/Laden bestaetigt. Jede Codeaenderung FIX04 erfordert danach einen *neuen* Windows-Build; noch kein GitHub-Push.
- Offene Risiken: GUI bei kleiner Bildschirmaufloesung; alte Weltregionen in `main.MAPS` (nicht mit 127 Original-Siedlungskarten verwechseln), Bot-Oekonomie/Belagerungen, 25 visuelle Kartenraster und alle Tests vor Release.


### 28.10.2026 – Vorlaeufige Entwicklung FIX04d (noch nicht Windows-veroeffentlicht)

FIX04 ergaenzt das Baumenue der 127 Originalkarten um Rubriken und regelbasierte Statusanzeige. FIX04b/c enthalten Standorttipps und eine begleitende Spielerhilfe mit zehn Fragen. FIX04d ergaenzt einen nur im Admin-Teststand zulaessigen Anzeige-Override (`auto`, `anzeigen`, `ausblenden`) ohne Eingriff in den Goetterschutz. 7/7 neue Admin-Tests erfolgreich; benachbarte GUI-, Start-, Save- und Durchspieltests erfolgreich. Vollsuite, Windows-FIX04d-EXE, Botwirtschaft und 25 visuell offene Kartenraster bleiben offen. Auf GitHub ist dieser Stand noch **nicht** veroeffentlicht; bisherige FIX03-EXE ist nicht FIX04d.
