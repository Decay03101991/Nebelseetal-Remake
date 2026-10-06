# AUFTRAG — Dorfzentrum als Dashboard und Lager mit Funktion

**Stand:** 06.10.2026, 08:32 · **angelegt von:** Hermes (Sitzung `20261006_011522_6f090e`)
**Art:** Auftrags-Entwurf. **Das ist noch nichts Gebautes** — hier steht, was Daniel will, was heute
da ist und was offen ist. Die Reihenfolge und die drei offenen Fragen entscheidet Daniel.

---

## 1. Daniels Wunsch, wörtlich (06.10.2026, 08:3x)

> „bestände zu sehen. Aber auch die bestände in den einzelnen Siedlungen usw"

> „ich möchte auch das dass Dorfzentrum die Übersicht der von mir gewählten und ausgebauten Maps
> bietet nicht im unter menü wenn ich die einzelnen karten öffne. Das bebauen der maps und die
> rohstoffgewinnung ist zentral. Der gebäude bau usw gehört sauber als Dashboard neben die maps,
> schön übersichtlich und eine passende logische und sinnvolle Benutzeroberfläche. Der Stil mit den
> umbenennen, Transport und siedlunggründen buttons gefällt mir aber wie gesagt die gesamt ansicht
> vom Dorfzentrum muss angepasst werden. Da es der dreh und angelpunkt ist im spiel. In der Lager
> Ansicht gefällt mir nicht das alle kacheln so über groß und nicht gleichmäßig angepasst sind auf
> ihre icons. Aber vorallem sollte im Lager einiges an funktion vorzufinden sein als spieler.
> Es sollte hier möglich sein, Gesamt lagerbest… " ← **hier bricht die Nachricht ab (offene Frage 1)**

## 2. Ist-Zustand, gemessen (nicht behauptet)

| Was | Heute | Beleg |
|---|---|---|
| **Dorfzentrum** | `NebelseetalApp._render_overview` (Rückruf „Dorfzentrum“, `src/main.py` Z. 2614 ff.): Titel · Karte „Dein nächster Schritt“ · **eine flache Liste** „Siedlungen:“ mit „Reich: …“, je Siedlung eine Zeile `{Name} ({map_id})` + „aktiv“/**Als aktiv setzen** + „Gebäude auf der Karte: N“ bzw. „{Kartentyp} · Felder belegt: N“ + Knöpfe **Karte öffnen · Transport · Umbenennen** · darunter die `lokal: …`-Zeile · Knopf „Neue Siedlung gründen“ · Liste „Laufende Aufträge:“ | `_render_overview`, Z. 2614-2730 |
| **Karten/Bauen** | Das Bauen passiert **in der geöffneten Siedlungskarte** (`_oeffne_siedlungskarte` → Siedlungskarte mit Auswahlspalte rechts). Im Dorfzentrum sieht man davon nur die Zahl der bebauten Felder | `_render_overview` Z. 2707 ff.; Siedlungskarte |
| **Rohstoffgewinnung** | Wird nur als Bestand/`lokal:`-Zeile gezeigt; **kein Ertrags-/Erzeuger-Bild** im Dorfzentrum | `ortsbestand_text` (Z. 393), `stundenertrag()` |
| **Lager** | `_render_storage` (Z. 3832 ff.): Panel „Ortslager der aktiven Siedlung“ (Textzeilen) · „Waren (Reich/Übergang)“ mit `werkstatt.lager_text` · **Kachel-Raster, 6 Spalten**, `padx=10, pady=10, sticky="nsew"` + `grid_rowconfigure/columnconfigure(..., weight=1)` → **jede Kachel dehnt sich auf die Zellgröße**, die Kacheln sind dadurch groß und untereinander ungleich · dann „Einheiten (Reich/Übergang)“ ebenso · darunter die Werkstätten mit Warteschlange | `_render_storage`, Z. 3832 ff. |
| **Kachelgröße/Icons** | Icons werden **halbiert** geladen (`_lade_icon(..., faktor=2)`, ~90 px → ~45 px), aber **nichts** passt die Kachel an das Icon an | `_lade_icon`, Z. 3902 ff. |
| **Umfang** | **45 Kacheln** im Lager (17 Waren aus `data/items.json` + 28 Einheiten aus `UNITS`) — alle in EINEM Raster, ohne Filter, ohne Gruppierung | `len(WARE_EINTRAEGE)=17`, `len(M.UNITS)=28` |

**Kurz:** Das Dorfzentrum ist heute eine Liste mit Knöpfen, das Lager ein Textblock plus ein
dehnendes 6-Spalten-Raster ohne Funktionen.

## 3. Was ich als Auftrag verstehe (VORSCHLAG — Daniels Korrektur in einer Zeile genügt)

**A · Dorfzentrum = Dashboard (Dreh- und Angelpunkt)**
1. **Map-Übersicht oben**: je eigene Siedlung eine **Karte/Kachel** mit Name, Kartenbild (Miniatur
   der `raster`-Felder), Ausbaustand (bebaute Felder, Kartentyp, Siedler, Grenze), **Ortslager** und
   **Ertrag je Stunde** (die wichtigsten Rohstoffe) — auf einen Blick, ohne die Karte zu öffnen.
2. **Bauen und Rohstoffgewinnung zentral, direkt daneben**: eine rechte Spalte („Dashboard“) mit
   Gebiet/aktive Siedlung, der **Bauauswahl** für diese Siedlung und der **Ertragsübersicht**
   (was kommt je Stunde herein, was fehlt). **Der Bau soll nicht mehr nur im Untermenü der Karte
   stattfinden** — die Karte bleibt zum Anschauen/Auswählen, gebaut wird auf dem Dashboard.
3. **Stil beibehalten**: dieselben Knöpfe („Als aktiv setzen“, „Umbenennen“, „Transport“,
   „Neue Siedlung gründen“) in derselben Optik, nur sauber in Spalten ausgerichtet.
4. **Logik**: oben der Zustand (Maps/Bestände), rechts das Handeln (Bauen/Transport/Gründen), unten
   die Aufträge/Posten — eine Richtung von „sehen“ nach „tun“.

**B · Lager mit echten Funktionen**
1. **Gleichmäßige Kacheln**: feste Kachelgröße (z. B. 88×88 px), Icon auf die Kachel **zugeschnitten
   bzw. skaliert** (`zoom`/`subsample` je Icon, zentriert), Name + Menge in festen Zeilen; **kein**
   `sticky="nsew"`-Dehnen mehr.
2. **Gruppierung/Filter**: Rohstoffe (Ortslager) · Waren (17) · Einheiten (28) · Werkstätten — je
   Gruppe eigenes Raster, damit 45 Kacheln nicht in einem Brei verschwinden.
3. **Funktionen (Daniels Punkt 2, hier ist die offene Frage 1)** — Vorschlag: Gesamtbestände ALLER
   Siedlungen nebeneinander sehen · **Umlagern/Transport direkt aus dem Lager heraus** (mit Karren-
   Pflicht, über den vorhandenen `transport_an_ort`) · Werkstatt-Warteschlangen starten/sehen ·
   Einheiten-Ausbildung anstoßen · (nur falls Daniel will) Handel aus dem Lager heraus.
4. **Nichts erfinden**: jede Umlagerung läuft über die belegten Wege (`transport_start`,
   `verbrauchen`, Ortslager-zuerst) — kein zweiter Zahlweg.

## 4. Fragen an Daniel — **BEANTWORTET** (06.10.2026, 08:4x)

1. **Der abgebrochene Satz** war nicht abgebrochen, sondern **umgestellt geliefert**: „Es sollte hier
   möglich sein, **Gesamtlagerbestände** zu sehen. **Aber auch die Bestände in den einzelnen
   Siedlungen** usw.“ → Das Lager braucht **beides**: die **Gesamtsicht** (über alle Siedlungen) und
   **je Siedlung** deren eigene Bestände.
2. **Reihenfolge: erst Schritt 10 (Aktivierung), dann dieses UI-Paket** (Daniel bestätigt die
   Empfehlung). Grund: danach ist die Datenlage endgültig — das Dashboard wird **einmal** richtig
   gebaut, nicht zweimal.
3. **Der Gebäudebau lebt im Dorfzentrum als Dashboard; die Siedlungskarte zeigt nur noch und wählt
   aus.**
4. `.exe`-Neubau + Startprüfung nach dem UI-Paket (Projektregel) bleibt.

*(Die Fragen standen so zur Entscheidung:)*

1. **Der abgebrochene Satz:** „Es sollte hier möglich sein, Gesamt lagerbest…“ — **wie geht er
   weiter?** (Gesamtlagerbestände **aller** Siedlungen sehen? Waren **umlagern**? Beides?)
2. **Reihenfolge:** zuerst dieses UI-Paket — oder zuerst **Schritt 10** (die Aktivierung des
   Ökonomiemodus, das letzte Stück des Ökonomie-Pakets)?
   **Meine Empfehlung:** **erst Schritt 10.** Grund: die Aktivierung stellt die Ortslager von
   „Übergang“ auf „führend“ um (Entwurf Z. 1092) — danach ist die Datenlage endgültig, und das
   Dashboard wird **einmal** richtig gebaut statt zweimal. Nach Daniels Prinzip „kein Halbumbau“.
3. **Dashboard-Ort:** soll die Bauauswahl (Gebäude) **im Dorfzentrum** liegen und die Siedlungskarte
   nur noch zeigen/wählen — oder soll das Dashboard **neben** der geöffneten Karte stehen
   (geteilter Bildschirm: Karte links, Bau+Daten rechts)?
4. **Passworttor/EXE:** Nach dem UI-Paket ist ein `.exe`-Neubau + Startprüfung fällig (Projektregel),
   damit Daniel das Neue auch spielt.

## 5. Arbeitsweise für dieses Paket (unverändert)

Nach jedem Schritt: betroffener **Einzeltest** (`test_gui_fehler`, `test_startspiel`,
`test_kartenansicht`, `test_siedlungskarte` sind hier die Wächter) + **einmal Sammellauf** (keine
offenen Spielprozesse), **eine Protokollzeile** (Zeit aus `date`),
`protokoll_sichern.py --protokoll`, **kleiner Commit**; am Ende `.exe` neu bauen und aus einem
**anderen** Ordner startprüfen. Keine Regel des Handbuchs wird dabei angefasst; reine Oberfläche.
