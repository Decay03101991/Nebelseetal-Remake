# WEB-QUELLEN — Nebelseetal (Karten, Screenshots, Gelände)

Recherche im offenen Web und in Web-Archiven am 04.10.2026.
Alle hier genannten Bilder liegen in diesem Ordner (`docs/original/karten/`) bzw. `docs/original/karten/gamestar/`.
Nichts wurde überschrieben; vorhandene Dateien blieben unangetastet.
Hinweis: Im Ordner liegen zusätzlich Dateien eines parallel laufenden Vorgangs
(Schema `JAHR_host__pfad.ext`, `gamestar_nebelseetal_*_full.jpg`, `QUELLEN.md`) — diese stammen NICHT aus dieser Recherche.

---

## A. Original-Game-Screenshots der Spielseite (nebelseetal.de/bilder/screens/*)

**Seite:** `http://nebelseetal.de/screens.php` (Titel: "Nebelseetal, das Fantasy-Browsergame — Screenshots")
**Archiv-Belege (Wayback):**
- https://web.archive.org/web/20061206090541/http://nebelseetal.de/screens.php  (06.12.2006)
- https://web.archive.org/web/20090228182034/http://nebelseetal.de/screens.php  (28.02.2009)
- https://web.archive.org/web/20100606042128/http://nebelseetal.de/screens.php  (06.06.2010)

Die Seite nennt vier In-Game-Ansichten (Wortlaut aus screens.php):

| Bilddatei (Original) | Titel | Wörtlicher Beschreibungstext |
|---|---|---|
| `bilder/screens/lager.jpg` | Das Lager | "Im Lager seht ihr alle Waren und Einheiten die in einer Siedlung stationiert sind." |
| `bilder/screens/portal.jpg` | Das Portal | "Die Welten des Nebelseetals sind durch magische Portale verbunden. In der Portalübersicht seht Ihr alle Welten der anderen Spieler." |
| `bilder/screens/siedlung.jpg` | Die Siedlungsübersicht | "In der Siedlungsübersicht seht Ihr alle Gebäude die in der Sedlung errichtet wurden." [Schreibfehler "Sedlung" im Original] |
| `bilder/screens/profil.jpg` | Die Spielerprofile | "Jeder Spieler hat die Möglichkeit, ein Profil über sich oder den Charakter den er spielt anzulegen." |

Thumbnails der Seite: `bilder/screens/thumb_lager.jpg`, `thumb_portal.jpg`, `thumb_siedlung.jpg`, `thumb_profil.jpg`.

**ERGEBNIS (negativ, bitte nicht noch einmal suchen):**
Die vier Vollbilder (`lager.jpg`, `portal.jpg`, `siedlung.jpg`, `profil.jpg`) und ihre Thumbnails sind im Web-Archiv **NICHT als Datei vorhanden**. Geprüft per CDX-Index des gesamten Hosts
(`/cdx/search/cdx?url=nebelseetal.de&matchType=domain&...&limit=10000&filter=statuscode:200`)
— der gesamte Bestand enthält **kein** `bilder/screens/*`-Bild. Einzelabfragen
(`.../bilder/screens/siedlung.jpg`) liefern in CDX und in der Wayback-Availability-API **keinen Snapshot**.
Die Screenshot-Bilder sind also nicht mehr rekonstruierbar; erhalten sind nur die obigen Bild-URLs und Texte.

### Wallpaper-Seite

**Seite:** `http://www.nebelseetal.de/wallpaper.php` (Titel: "Nebelseetal, das Fantasy-Browsergame — Wallpaper")
**Archiv-Beleg:** https://web.archive.org/web/20090831062059/http://www.nebelseetal.de/wallpaper.php (31.08.2009)

Wörtlich genannt:
> "**Warlord Wallpaper**  Format: 1024X768"  → Originaldatei `bilder/wallpaper/wallpaper.jpg`
> "**Warlord Wallpaper**  Format: 1440\*900 (Widescreen)"  → Originaldatei `bilder/wallpaper/wallpaper_wide.jpg`

Die beiden `bilder/wallpaper/*.jpg` sind **nicht** archiviert. Erhalten ist dagegen eine ältere Wallpaper-Datei der Seite:

- **Original-URL:** `http://www.nebelseetal.de/downloads/wallpaper/nebelseetal_1024X768.jpg`
- **Archiv-Beleg:** https://web.archive.org/web/20060112174944/http://www.nebelseetal.de/downloads/wallpaper/nebelseetal_1024X768.jpg (12.01.2006)
- **Heruntergeladen nach:** `web_nebelseetal_wallpaper_1024x768.jpg` (JPEG, 1024×768, 110.921 Byte)

---

## B. GameStar-Artikel über Nebelseetal

**Live-URL:** https://www.gamestar.de/artikel/nebelseetal-browserspiel-des-tages-seichte-strategie-unterhaltung,1948911.html
**Archiv-Beleg:** https://web.archive.org/web/20191021134218/https://www.gamestar.de/artikel/nebelseetal-browserspiel-des-tages-seichte-strategie-unterhaltung,1948911.html (21.10.2019)
**Titel:** "Nebelseetal - Browserspiel des Tages - Seichte Strategie-Unterhaltung"
**Autor/Datum:** Gerald Meyer, **09.09.2008 17:00 Uhr** (10. Teil der Serie "Browserspiel des Tages")

Der Artikel enthält **drei** eigene Nebelseetal-Bilder unter `images.cgames.de`
(Alt-Hosts 5–9images.cgames.de; Größenpfade u. a. 4, 204, 226, 256, 290, 692, 1024, 1280):
`https://images.cgames.de/images/gamestar/<groesse>/nebelseetal-browserspiel-des-tages_<ID>.jpg`

| ID | Rolle im Artikel |
|---|---|
| **1838855** | Aufmacher-/Teaserbild (og:image); Bild-ID der Projektdatei `docs/nebelseetal_gamestar.jpg` (Größe 290, 94.692 Byte) |
| **1838856** | Artikelbild 1 — Bildunterschrift: "Die Portale, durch die gehandelt werden darf oder durch die Sie Ihre Truppen zur Eroberung schicken." |
| **1838857** | Artikelbild 2; Bild-ID der Projektdatei `docs/nebelseetal_gamestar2.jpg` (Größe 226, 124.399 Byte) |

Alle drei IDs wurden in den Größen 4, 204, 226, 256, 290, 692, 1024, 1280 heruntergeladen
(sofern > 20 kB und gültiges JPEG) nach **`docs/original/karten/gamestar/web_<ID>_<groesse>.jpg`** (21 Dateien).
Größe "4" ist jeweils die Originalfassung (1838855 = 202.370 B, 1838856 = 196.948 B, 1838857 = 201.222 B).

**Karten-/Siedlungs-relevante Textstellen (wörtlich):**
> "Ein kleiner grafischer Einspieler verdeutlicht Ihnen: gähnende Leere überall. Das muss geändert werden!"
> "Im rechten Menü finden Sie unter der Siedlungsübersicht auch die Punkte Aufträge und Bauen."
> "Da Ihre kleine Siedlung ohne Holz, Stein und Nahrung nicht funktioniert, erbauen Sie **auf einer schematischen Darstellung** Holzfällerhütten, Steinbrüche und Jadghütten."
> "**Unter der 3D-Ansicht Ihres Fleckchens Erde** finden Sie die verbleibende Zeit aufgeführt."
> "Das Spiel läuft – wie ähnliche Ableger – in Echtzeit ab, also nicht rundenbasiert. Der Noob-Schutz dauert sieben Tage."

---

## C. Browsergame-Portale

### C1. Galaxy-News (Spieleverzeichnis) — game_id=994
**Live (heute nur 403/Bot-Sperre):** http://www.galaxy-news.de/games/994_nebelseetal.html
**Archiv-Belege:**
- https://web.archive.org/web/20090704125327/http://www.galaxy-news.de/games/994_nebelseetal.html (04.07.2009)
- https://web.archive.org/web/20070429143425/http://www.galaxy-news.de/games/994_nebelseetal.html (29.04.2007)

Stammdaten (wörtlich):
> Betreiber: **Andreas Bock** · Entwicklungsstand: Öffentlicher Test · Stand: Oktober 2006
> Genre: Strategie · Schauplatz: Mittelalter · **Registrierte Spieler: 500-1000** · **Spielwelten: 4-9** · Zeiteinteilung: Echtzeit · Rundenlänge: unendlich
> **Veröffentlichung: August 2003** · Kosten: Kostenlos spielbar

Beschreibung (wörtlich):
> "Schlüpfe in die Rolle eines Herrschers und baue deine Siedlungen auf. Erforsche neue Wissensgebiete und bilde Einheiten aus um dich gegen die anderen Spieler zu behaupten."
> Features: 10 Ressourcen, 17 Warentypen, 28 Einheitentypen, 18 Forschungen, Spielerprofil, Gilden mit Gildenwertung/-profil/Spielerrängen, verschiedene Skins.
> "Das Spiel läuft in Echtzeit … Du beginnst das Spiel mit einer Siedlung, die es zunächst gilt auszubauen. … Je höher der Wissensstand deines Volkes ist, desto mehr Möglichkeiten hast du, deine Siedlung zu erweitern, Einheiten auszubilden und neue Siedlungen zu gründen."

Die Seite verlinkt eine eigene **Bildergalerie** (content_id=4035, Bilder 9948–9957) und Artikel
("Neue Spielversion und frohe Weihnachten" 23.12.06; "Highspeed auf dem Schlachtfeld" 28.10.06;
"Neuer Server bei Nebelseetal" 06.09.06; "Neuer Server Utgard" 29.05.06).
**Galerie-Bilder (10 Stück) NICHT archiviert:** Original-URLs `http://www.galaxy-news.de/upload/galleries/9948.jpg` … `/9957.jpg`
(+ Thumbnails `/upload/galleries/thumbnails/9948.jpg` …). CDX liefert für 9948/9950/9957 **keinen Snapshot**
(nur 404 bzw. 429); der CDX-Index des `upload/galleries/`-Pfads enthält diese IDs nicht. Rekonstruktion daher nicht möglich.
Galerie-Seite selbst archiviert: https://web.archive.org/web/20080511114405/http://www.galaxy-news.de/?page=content&op=showgallery&content_id=4035&showpicture=9949

### C2. browsergame-index.de
**Live-URL:** https://www.browsergame-index.de/browsergames/nebelseetal
Wörtlich:
> "Nebelseetal ist ein kostenloses Fantasie Rollenspiel. Der Spieler beginnt als Herrscher über eine Siedlung, baut Gebäude, forscht, erforscht das Land und tritt in Kontakt mit seinen Nachbarn."
(Keine Screenshots auf der Seite; "Für dieses Browserspiel wurde noch keine Beschreibung eingetragen.")

### C3. Weitere Portale — negativ
Für bgame.de (game=1), browsergames24.de (lid=1253), browserwelten.net (gameid=1007),
browsergames.de, mmorpg.de, gamona.de, 4players.de, buffed.de, gametwist.de liefert der
Wayback-CDX **keine** archivierte Nebelseetal-Spielseite (Suche über `filter=original:.*nebelseetal.*`
und über die bekannten numerischen IDs). Die Verweis-Buttons der Spielseite existierten, die Zielseiten sind aber nicht archiviert.

---

## D. TEXTFUNDE zum Kartenaufbau / Geländearten (wörtlich)

### D1. Rohstoffproduktion und Geländearten
**Seite:** `http://www.nebelseetal.de/spielanleitung/rohstoffe.php`
**Archiv-Beleg:** https://web.archive.org/web/20050301230212/http://www.nebelseetal.de/spielanleitung/rohstoffe.php (01.03.2005)

Wörtlich:
> "Rohstoffe werden benötigt um neue Gebäude zu errichten, Wahren herzustellen und Einheiten auszubilden."
> "Jedes Gebäude produziert auf 2 verschiedenen Geländearten unterschiedliche Mengen an Rohstoffen."
> "Sümpfe sind unbebaubar und somit für Eure Siedlungen völlig wertlos."

Produktionstabelle (= **Geländearten und ihre Erträge**), wörtlich:

| Gebäude | Rohstoff | Produktion |
|---|---|---|
| Holzfäller | Holz | Wald(4) / Steppe(1) |
| Steinmetz | Steine | Berg(4) / Hügel(1) |
| Erzmine | Metall | Berg(3) / Hügel(1) |
| Tempel | Mana | Nebelsee(8) / Alle außer Sumpf(2) |
| Farm | Nahrung | Grasland(4) / Steppe(2) |
| Goldmiene | Gold | Berg(3) / Hügel(1) |
| Schafzucht | Wolle | Grasland(2) / Steppe(1) |
| Rinderfarm | Leder | Grasland(2) / Steppe(1) |
| Pferdezucht | Pferde | Grasland(2) / Steppe(1) |
| Jäger | Nahrung, Leder | Wald(1 Nahrung, 1 Leder) |

=> **Geländearten: Wald, Steppe, Berg, Hügel, Nebelsee, Sumpf, Grasland.**
Weiter wörtlich: "Eure Siedlung bekommt außer den Rohstoffen einen neuen Siedler pro Stunde … Diese Grenze liegt in jeder neuen Siedlung bei 5 Siedlern … erhöht sich der Grenzwert um 5 Siedler pro Haus."

### D2. Siedlungskarten
**Seite:** `http://www.nebelseetal.de/spielanleitung/siedeln.php`
**Archiv-Beleg:** https://web.archive.org/web/20050302040743/http://www.nebelseetal.de/spielanleitung/siedeln.php (02.03.2005)
Wörtlich:
> "Einer neuen Siedlung wird per Zufall eine Karte zugewiesen. Es werden niemals zwei Eurer Siedlungen die gleiche Karte bekommen."
> "Das Löschen einer Siedlung ist in erster Linie sinnvoll, wenn Ihr eine besonders schlechte Siedlungskarte erwischt habt."
> "Es ist nicht möglich mehr als 10 Siedlungen zu errichten."

**Seite:** `http://www.nebelseetal.de/spielanleitung/siedlungen.php`
**Archiv-Beleg:** https://web.archive.org/web/20050302090011/http://www.nebelseetal.de/spielanleitung/siedlungen.php (02.03.2005)
Wörtlich:
> "Hier seht Ihr die Karte der Siedlung, die Rohstoffe, die sich in der Siedlung befinden und die Rohstoffproduktions-Auflistung."
> "Klickt auf das Gebäude, welches Ihr errichten möchtet und platziert es anschließend auf der Siedlungskarte."
> "Es wird eine Kartenansicht angezeigt, auf der Ihr das entsprechende Gebäude anklicken müsst."

### D3. Weltkarte / Rastergröße (Limbus, Portalkoordinaten)
**Seite:** `http://www.nebelseetal.de/spielanleitung/portal.php`
**Archiv-Beleg:** https://web.archive.org/web/20050228222200/http://www.nebelseetal.de/spielanleitung/portal.php (28.02.2005)
Wörtlich:
> "Diese bestehen aus drei Zahlen. Die ersten beiden (X und Y), zeigen die Position Eurer Welt, auf einem zweidimensionalem Raster, in Eurer Dimension an. Die dritte Zahl (Z) zeigt die Dimension an, in der sich Eure Welt befindet."
> **"Es gibt 20 Dimensionen, in jeder Dimension sind 20 mal 20 Felder frei für Spielerwelten."**
> "Ihr habt die Möglichkeit, einmal binnen 24 Stunden, eure Koordinaten zu wechseln. … Sie benötigen hierfür 5.000 Mana."
> "Eure Welt wird durch ein grünes Banner markiert, fremde Welten durch rote."

---

## E. NICHT gefunden / nicht abrufbar (ehrliche Meldung)

- **On-Site-Game-Screenshots** (`bilder/screens/{lager,portal,siedlung,profil}.jpg`): nicht archiviert (CDX + Availability-API leer). Nur Texte/Bild-URLs erhalten.
- **Wallpaper** `bilder/wallpaper/wallpaper.jpg` und `wallpaper_wide.jpg`: nicht archiviert.
- **archive.today:** `https://archive.ph/https://www.nebelseetal.de` → **"No results"** (kein Snapshot des Spiels).
- **YouTube:** Suchen `Nebelseetal`, `Nebelsee Browserspiel`, `Nebelseetal 2007` liefern **keine** Videos zum Spiel (nur themenfremde Treffer).
- **Reddit** r/zocken Thread `1u8ucdr` ("Bin ich alt geworden…", Kommentar "Hat hier jemand Nebelseetal gespielt?…"): **Abruf blockiert** — sowohl `www.reddit.com`/`old.reddit.com` (JSON sowie Browser → "You've been blocked by network security"). Kommentare/Bildverweise nicht auslesbar.
- **osnanet.de:** kein archivierter Pfad/Subdomain mit "nebelsee…" (Host ist ein Osnabrücker Homepage-Anbieter mit Nutzer-Unterordnern); Fanseite dort nicht auffindbar.
- **Fanportal** `www.nebelseetal-fanportal.ch.vu`: archiviert (Belege 2011/2012/2021), aber rein JS-gestützt ohne statischen Textinhalt ("Nebelseetal-Fanportal"); inhaltlich nichts auslesbar.
- **Alt-Forum** `forum.nebelseetal.de`: über 2600 Captures vorhanden (Boards `board.php?boardid=1..92`), Abruf der Texte scheiterte an Wayback-Rate-Limit (HTTP 429) und Exa-503. **Nicht abschließend ausgewertet** — lohnt einen erneuten, gedrosselten Versuch (Threadbeschreibungen zu Karte/Gelände erwartbar).
- **GameStar-Artikelbilder:** über `images.cgames.de` heute vollständig abrufbar und gesichert (siehe B); archivierte Alt-Hosts `7images/8images.cgames.de` lieferten dagegen keine Snapshots.
- **Weitere Portale** (bgame.de, browsergames24.de, browserwelten.net, browsergames.de, mmorpg.de, gamona.de, 4players.de, buffed.de, gametwist.de): keine archivierten Spielseiten.

## F. Hochgeladene/sichere Bilddateien (Fassung "Speedsim"/Projekt)

| Datei | Quelle |
|---|---|
| `web_nebelseetal_wallpaper_1024x768.jpg` | nebelseetal.de/downloads/wallpaper/nebelseetal_1024X768.jpg (Wayback 2006) |
| `gamestar/web_1838855_{4,204,226,256,290,692,1024,1280}.jpg` | images.cgames.de (GameStar-Artikel, ID 1838855) |
| `gamestar/web_1838856_{...}.jpg` | images.cgames.de (GameStar-Artikel, ID 1838856) |
| `gamestar/web_1838857_{...}.jpg` | images.cgames.de (GameStar-Artikel, ID 1838857) |
| `web_gamestar_1838855_226.jpg`, `web_gamestar_1838855_293.jpg` | images.cgames.de (erste Sicherung, ID 1838855) |
| `web_gamestar_1838856_226.jpg`, `web_gamestar_1838856_293.jpg` | images.cgames.de (ID 1838856) |
| `web_gamestar_1838857_226.jpg`, `web_gamestar_1838857_293.jpg` | images.cgames.de (ID 1838857) |
