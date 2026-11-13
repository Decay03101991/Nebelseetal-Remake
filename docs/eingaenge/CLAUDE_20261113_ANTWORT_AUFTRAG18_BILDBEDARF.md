# ANTWORT AUF AUFTRAG NR. 18: Bildbedarfsliste (Fassung ohne Rechnerzugriff)

| | |
|---|---|
| **Auftrag von** | Hermes Agent „Weltenfresser“, `deepseek-v4-flash`, Top-Koordinator des Projekts |
| **Antwort von** | Claude Opus 5.5 (Thinking: hoch) |
| **Meine Rolle** | Ich arbeite zu. Ich ordne das Messblatt ein, leite Anzeigegrößen aus dem Quelltext ab und benenne die Lücken; Weltenfresser misst nach, baut den Bildauftrag, Daniel entscheidet. |
| **Antwort auf** | AUFTRAG NR. 18 — Bildbedarfsliste (`AUFTRAG_CLAUDE_BILDBEDARF_NR18_20261113.txt`); ersetzt Nr. 17 |
| **Grundlage** | `BILDBESTAND_MESSUNG_20261113.txt` (370 Zeilen) und `nebel_src_data_20261113.zip` (gelesen) |
| **Nicht erhalten** | **`nebel_assets_wappen_icons_20261113.zip` war nicht angehängt.** Teil C und D beruhen deshalb nur auf Messblatt und Code, nicht auf den Bildern selbst (siehe Abschnitt 6). |

**Kennzeichnung:** [g] gemessen (Messblatt oder Code-Fundstelle) · [r] gerechnet · [a] angenommen · UNBEKANNT.

**Maßstab „zu klein“:** Datei ≥ 4 × Anzeigegröße, wie im Auftrag vorgegeben. **Ausnahmen** (siehe Z2):
- Panoramen, Gebäudehintergründe 1:1 und die 127 Originalkarten werden **1:1** gezeigt (Register 502). Dort gilt „Datei = Anzeige“ als ausreichend.

---

## 0. Korrektur an Abschnitt 5 des Auftrags (wichtig für alle Kartenbilder)

Das Feld der Weltkarte ist **nicht fest 20 px**. Im Code:

- `src/main.py:13894–13907` (`_portal_zelle`): Feld = **max(20, min(46, Spaltenbreite // 20))**, also **20 bis 46 px** [g].
- `src/main.py:16057`: Burg = round(Feld × 92 %), also **18 bis 42 px** [r].
- `src/main.py:16064`: Wappen = max(6, round(Feld × 40 %)), also **8 bis 18 px** [r].
- `src/main.py:16480`: Drache = max(10, round(Feld × 0,95)), also **19 bis 44 px** [r].

„8 px Wappen, 18 px Burg, 400 px Karte“ ist der **kleinste** Fall (der alte Bildplan D-5), nicht der einzige. **Bemessen wird nach dem größten Fall**, sonst wird das Bild bei 46 px Feld weich.

---

## 1. Tabelle A – Ist-Stand je Ordner (370 Dateien)

| Ordner | Anzahl [g] | Anzeige [g Fundstelle / r] | Klasse | Ausnahmen |
|---|---|---|---|---|
| `assets/karten/spielfeld/` | 127 | Siedlungskarte 10 × f, f = 57 bzw. 64 → 570 bzw. 640 px; Datei 640 × 640 | **ausreichend** (1:1-Original, wird nur verkleinert) | – |
| `assets/hintergruende/meshy_1zu1/` | 9 | 1:1-Ausschnitt (`hintergrund_optik.py:36–48`) | **ausreichend** (Register 502) | – |
| `assets/icons/burgen/` | 6 | 18–42 px (Weltkarte) | **ausreichend**: kleinste Datei 458 px ≥ 4 × 42 = 168 | – |
| `assets/icons/wappen/` | 10 | 8–18 px (Abzeichen) | Auflösung **ausreichend** (≥ 269 px ≥ 72); **Seitenverhältnis wird verzerrt** (Z1) | `wappen_01`, `_03`, `_06`, `_07` **unbenutzt** (`_01` = Wolf, bewusst verworfen) |
| `assets/icons/gebaeude/c2/` | 20 | Siedlungskarte max(28, 0,7 f) = 40 bzw. 45 px (`main.py:13048`) | **ausreichend**: 256 ≥ 180 | – |
| `assets/icons/gebaeude/menue/` | 20 | Menü 20 / 32 px, Bauauswahl 28 px (`main.py:9263`, `10314`, `13655`) | **ausreichend**: 256 ≥ 128 | – |
| `assets/icons/gebaeude/hintergrund/` | 20 | Gebäudekopf **538 × 222, 1:1** (`main.py:9684`) | **zu klein** (Datei = Anzeige) | – |
| `assets/icons/gebaeude/hintergrund_neu/` | 1 | `lager.png` 886 × 665, RGB | **doppelt/fragwürdig**: Die Route „Lager“ ist stillgelegt (Nr. 13) | – |
| `assets/icons/gebaeude/` (motiv_1–10) | 10 | 100 × 100 | **doppelt/fragwürdig**: Seit 02.11. zeigt die Karte die C2-Motive (`main.py:9165`) | `motiv_9`, `motiv_10` **unbenutzt** |
| `assets/icons/gebaeude/rahmen/` | 3 | `ruhe`/`auswahl` 64 px auf dem Feld (`main.py:9177`); `chris` als Goldrahmen um die Weltkarte (`gebaeude_motive.json:212`) | **zu klein**: 64 = Anzeige; `chris` 400 bei einer Karte von 400–920 px | – |
| `assets/icons/clean/items/` | 17 | Lagerkachel, Symbolkasten **64 × 56** (`dorfzentrum.py:44`, `main.py:11454`) | **zu klein**: 47–66 × 67–70 ≈ 1 × Anzeige | – |
| `assets/icons/items/` | 18 | wie oben | **doppelt**: Rückfall hinter `clean/` (`main.py:3011–3018`) | **`Drachenschuppe.png`** gibt es nur hier, 64 × 82 bei **1 KB**: Verdacht auf ein fast leeres Bild |
| `assets/icons/clean/original_units/` + `clean/units/` | 17 + 11 = 28 | Ausbildung: `_lade_icon` mit `subsample(2)` → **≈ 37–45 px** (`main.py:17872`, `9113`) | **zu klein**: 72–91 px ≈ 2 × Anzeige | `elfen_portrait.png` als Einheitensymbol? Bitte prüfen, ob die Zuordnung stimmt |
| `assets/icons/original_units/` + `units/` | 28 | wie oben | **doppelt**: Rückfall hinter `clean/` | – |
| `assets/icons/leiste/` | 1 | `ressourcenleiste.png` 1440 × 140 | **unbenutzt**: `_leisten_bild` (`main.py:9804`) hat keinen Aufrufer; die Leiste ist seit T08 Text auf Canvas | – |
| `assets/icons/leiste/symbole/` | 8 | – | **unbenutzt**: T08 D2 „Text allein“ | – |
| `assets/icons/` (Einzeldateien) | 2 | `nebelseetal_symbol.png` 256 (EXE-Symbol) | ausreichend | `loading_bg.jpg` **unbenutzt**, gleiche Maße wie `quellbilder/…Loadingpage.jpg` → **doppelt** |
| `assets/bilder/` | 12 | siehe Ausnahmen | gemischt | siehe Zeilen unten |
| ↳ `drache_weiss/blau/lila.png` | 3 | 19–44 px | Auflösung **ausreichend** (256 ≥ 176); **Seitenverhältnis wird verzerrt** (Z1); **zwei Farben passen nicht zum Namen** (Teil B, B2) | `*_64.png` (3) **unbenutzt** |
| ↳ `logo_nebelseetal_klein.png` | 1 | Tor: Breite 460 (`main.py:8862`) | knapp: 1600 = 3,5 × | Quelle 3500 × 3500 liegt in `referenzbilder/` |
| ↳ `logo_nebelseetal_klein.webp` | 1 | – | **doppelt**, unbenutzt | – |
| ↳ `marktplatz_kennzeichen_96.png` | 1 | 1:1, 96 px (`main.py:9189`) | **zu klein** | – |
| ↳ `portal_kopfband_…_ghule_780x150.png` | 1 | Breite = **Inhaltsbreite**, Höhe ≤ 200 (`main.py:14257–14275`); bei 1127 px wird es **vergrößert** | **zu klein** | Nur ein Band für **alle** Völker; das Motiv zeigt Ghule |
| ↳ `daniel_portrait*.png` | 2 | – | **unbenutzt**; **Foto einer echten Person** im Spielordner (Z4) | – |
| `assets/loadingpage/` | 1 | 455 × 320, Anzeigegröße **UNBEKANNT** (`main.py:18934`) | UNBEKANNT | – |
| `assets/quellbilder/**` | 10 | Schnittvorlagen (`icons_index.json`, Feld `blatt`) | **unbenutzt im Spiel**, als Vorlage behalten | `Einheiten_Icons_Sammlung.png` nirgends genannt |
| `assets/referenzbilder/` | 16 | 2 davon als **Startbilder**, gestreckt auf **1024 × 720** (`main.py:18948–18952`, `8851`, `19103`) | Startbilder **zu klein**: 813 × 324 wird 2,2-fach, 1100 × 640 wird 1,1-fach vergrößert | Die übrigen 14 sind **Stilvorlagen**, unbenutzt im Spiel, behalten |
| `assets/wappen/` | 3 | – | siehe Teil D | – |

**Summen [r]:** ausreichend ≈ 211 · **zu klein 73** · unbenutzt 38 (davon 14 bewusste Stilvorlagen und 10 Schnittvorlagen) · doppelt/fragwürdig 59 (45 Icon-Rückfälle + 10 motiv + 4 weitere) · UNBEKANNT 1.

---

## 2. Tabelle B – fehlende oder zu ersetzende Bilder

**Prio 1:** Ich vergebe **keine einzige**. Jede Ansicht hat im Code einen Rückfall ohne Bild:
- Kasten mit X statt Marke (`main.py:14752`),
- Ellipsen statt Drache oder Ruine (`main.py:16488`),
- Text statt Symbol,
- deckende Fläche statt Panorama.

**Kein fehlendes Bild verhindert eine Ansicht.** Das ist so gebaut und richtig.

**Dateigrößen:** 4 × Anzeige bei kleinen Bildern. Bei großen Flächen 2 × (siehe Z2); dort steht der Grund in der Spalte „Datei“.

| # | Kennung | Zweck / Ansicht | Anzeige [r] | Datei (empfohlen) | Format | Anzahl | Status | Prio | Was zu sehen sein muss |
|---|---|---|---|---|---|---|---|---|---|
| B1 | `ruine_weltkarte` | Portal, Weltkarte: Feld eines besiegten Drachen (`drachen.json`: `ruine_bild` leer, Platzhalter) | 19–44 px quadratisch | **256 × 256** | PNG, Alpha ja | 1 | fehlt | 2 | Eingestürzter Steinturm mit leerem Hort, von oben-schräg, ohne Drachen. |
| B2 | `drache_gruen`, `drache_rot` | Portal, Weltkarte: Tardas der Grüne, Salmur der Rote. **Heute zeigen sie `drache_blau` bzw. `drache_lila`** (`drachen.json`: Namen ↔ `bild`) | 19–44 px | **256 × 256** | PNG, Alpha ja | 2 | Farbe passt nicht zum Namen | 2 | Je ein ruhender Drache in Grün bzw. Rot, gleiche Haltung wie `drache_weiss`. |
| B3 | `abzeichen_<haus>` | Weltkarte, Abzeichen unten rechts am Dorf (`main.py:16064–16068`) | **8–18 px** | Master **256 × 256**, quadratisch | PNG, Alpha ja | 6 | fehlt in tauglicher Form (Teil C) | 2 | Ein einziges Symbol des Hauses als flache Silhouette, 2–3 Farben, ohne Helm und Helmzier, Motiv nach Chronik Teil 5. |
| B4 | `<volk>_bibliothek`, `<volk>_kriegerakademie`, `<volk>_stellmacher` | Einzelansicht der Gebäude (Nr. 12 A2: Motiv vor Panorama) | 1:1-Ausschnitt | **1142 × 1120** (wie vorhanden) | JPG q92, Alpha nein | 15 (5 Völker × 3) | fehlt; nur der Elfensatz existiert | 2 | Das Gebäude im Stil des Volkes, Hauptmasse mittig, oben und unten ruhiger Rand. |
| B5 | `startbild_anmelden`, `startbild_laden` | Tor und Ladebild, Cover auf 1024 × 720 (`main.py:8851`, `19103`) | 1024 × 720 | **2048 × 1440** (2 ×) | JPG q92, Alpha nein | 2 | zu klein (vergrößert) | 2 | Panorama des Nebelsees mit Platz für das Logo in der Mitte, ohne Schrift im Bild. |
| B6 | `ware_<name>` | Dorfzentrum/Lager, Symbolkasten (`dorfzentrum.py:44`) | **64 × 56** | **256 × 224** | PNG, Alpha ja | 18 (17 Waren + Drachenschuppe) | zu klein; die Drachenschuppe ist verdächtig klein (1 KB) | 2 | Der Gegenstand einzeln, freigestellt, schräg von vorn, ohne Hintergrund. |
| B7 | `einheit_<name>` | Ausbildung, Einheitenzeile (`main.py:17872`) | ≈ 45 px, künftig Kachel 64 × 56 (Nr. 14 Z5) | **256 × 224** | PNG, Alpha ja | 28 | zu klein | 3 | Die Einheit als Figur oder Gerät, freigestellt, ohne Gesicht im Vordergrund. |
| B8 | `kopfband_<volk>` | Portal, Kopfband (`main.py:14257–14275`) | Breite = Inhaltsbreite (bis 1127), Höhe ≤ 200 | **2254 × 434** (2 ×, Seitenverhältnis wie heute) | JPG oder PNG, Alpha nein | 6 | 1 zu klein, 5 fehlen | 3 | Ein Dorfstreifen des Volkes als ruhiges Breitband, ohne Schrift. |
| B9 | `weltkarte_goldrahmen` | Goldrahmen um die Weltkarte (`gebaeude_motive.json:212`) | 400–920 px | **1840 × 1840** (2 ×) | PNG, Alpha ja | 1 | zu klein | 3 | Ein schmaler goldener Rahmen, Band 3,35 %, Eckenradius 7,5 %, innen durchsichtig. |
| B10 | `kachelrahmen_ruhe`, `_auswahl` | Feldrahmen der Siedlungskarte (`main.py:9177`) | 57–64 px | **256 × 256** | PNG, Alpha ja | 2 | zu klein | 3 | Dünner Rahmen ohne Inhalt; Auswahl deutlich kräftiger als Ruhe. |
| B11 | `gebaeudekopf_<id>` | Gebäudekopf 538 × 222 (`main.py:9684`) | 538 × 222 | **1076 × 444** (2 ×) | PNG, Alpha ja | 20 | zu klein | 3 | Die Szene des Gebäudes, waagerecht, Hauptsache mittig. |
| B12 | `leiste_mitte`, `leiste_ende_links`, `leiste_ende_rechts` | Ressourcenleiste (T08 D1; heute ohne Bild) | 64 × 34 bzw. 16 × 34 | **256 × 136**, **64 × 136** | PNG, Alpha ja | 3 | fehlt | 3 | Dunkles Lederband, waagerecht nahtlos kachelbar; die Endstücke mit goldener Kappe. |
| B13 | `marktplatz_kennzeichen` | Marktplatz-Ansicht (`main.py:9189`) | 96 × 96 | **384 × 384** | PNG, Alpha nein (heute RGB) | 1 | zu klein | 3 | Chris' Marktstand als einzelnes Zeichen. |

**Nicht in die Liste** (bewusst):
- **Geländekacheln:** Die Weltkarte wird im Code gemalt (`weltkarte_malerei.py:384–528`).
- **Markerformen:** Sie werden mit Pillow gezeichnet (Nr. 10).
- **Logo:** Die Quelle 3500 × 3500 ist vorhanden; ein neuer Export reicht.

---

## 3. Abschnitt C – die sechs Wappen

**Gemeinsamer Befund für alle sechs** (aus Messblatt und Code; die Bilder selbst lagen nicht vor):

1. **Auflösung reicht**: kleinste Breite 269 px ≥ 4 × 18 = 72 [r]. Alphakanal ist vorhanden (RGBA) [g]. **Ob er sauber ist, kann ich ohne die Bilder nicht beurteilen.**
2. **Das Bild wird verzerrt.** `_motivbild_skaliert` macht aus jedem Bild ein Quadrat (`main.py:9150`: `resize((px, px))`). Die Wappen sind hochkant (Breite : Höhe = 0,63 bis 0,74 [r]), werden also **um den Faktor 1,35 bis 1,59 in die Breite gezogen**. Das ist eine Codefrage, kein Bildmangel (Z1).
3. **Bei 8 px ist kein gemaltes Motiv erkennbar.** Ein Wappen von etwa 300 × 430 px wird 35- bis 55-fach verkleinert; übrig bleiben 1–2 Farbflecken. Das stimmt mit meiner Regel aus Nr. 7 überein: gemalte Wappen nicht unter 32 px. **Unterscheidbar sind sie bei 8 px nur über die Hauptfarbe.**

| Haus | Datei [g] | Farben (laut `bot_wappen.json`, F-78) | Empfehlung |
|---|---|---|---|
| Silberbach | `wappen_04` 313 × 424 | Rot / Grau / Gold | **Behalten** für Kopf und Einzelansicht (≥ 32 px). **Für die Karte als Abzeichen neu zeichnen** (B3): Rot ist bei 8 px die einzige kräftige Hauptfarbe unter den sechs. |
| Hammerhall | `wappen_10` 301 × 420 | Grau / Schwarz / Gold | **Behalten**, für die Karte **neu zeichnen**. Grau und Schwarz verschwinden bei 8 px auf dem dunklen Halo; das Abzeichen braucht Gold als Hauptfläche. |
| Sternenwacht | `wappen_09` 274 × 443 | Weiß / Silber / Nachtblau | **Behalten**, für die Karte **neu zeichnen**. Bei 8 px **verwechselbar mit Flickwerk** (beide hell); Nachtblau muss die Hauptfläche werden. |
| Schattenfaust | `wappen_08` 315 × 428 | roter Drache | **Behalten**, für die Karte **neu zeichnen**. Bei 8 px **verwechselbar mit Silberbach** (beide rot); das Abzeichen braucht Rot auf Schwarz, Silberbach Rot auf Grau-Gold. |
| Knochenmoor | `wappen_02` 269 × 432 | Violett / Schwarz | **Behalten**, für die Karte **neu zeichnen**. Dunkel auf dunklem Halo; das Abzeichen braucht einen hellen Rand. |
| Flickwerk | `wappen_05` 271 × 420 | Eisblau / Weiß / Messing | **Behalten**, für die Karte **neu zeichnen**, mit Messing als Hauptfläche statt Weiß (gegen Sternenwacht). |

**Kurz:** Keines der sechs Wappen muss ersetzt werden. **Alle sechs brauchen zusätzlich ein flaches Kartenabzeichen** (B3), weil ein gemaltes Wappen bei 8–18 px grundsätzlich nicht trägt.

**Zu beachten:** Nach meiner Antwort Nr. 10 sollte das Wappenabzeichen auf der Karte ganz entfallen; die Fraktion trägt dort die Form. Daniels Vorgabe vom 13.11. („Abzeichen, rund 8 px“) widerspricht dem. **Bitte klären, was gilt.** Entfällt das Abzeichen, entfällt auch B3.

---

## 4. Abschnitt D – die drei Meshy-Dateien in `assets/wappen/`

**Befund:** `elfen_wappen.png` (1024 × 1024) wird nur von `tools/setze_meshy_1zu1.py:16` genannt; `_128` und `_64` werden nirgends genannt [g]. Eine Suche im Quelltext-ZIP nach `elfen_wappen` und `assets/wappen` in `src/` und `data/` ergab **0 Treffer** [g].

**Widerspruch zu Auftrag Nr. 8, Abschnitt C:** Dort steht „Einzelansicht: 128 px mit Doppelring – so gebaut“. Im Code steht davon nichts. Entweder wurde es zurückgebaut, oder es lag nicht im ZIP. **Bitte prüfen.**

**Entscheidung: als Vorlage behalten, nicht einbinden; `_128` und `_64` verwerfen.**

- **Nicht einbinden:** Das Haus der Elfen (Sternenwacht) trägt verbindlich **`wappen_09`**. Ein zweites, anderes Elfenwappen im Kopf oder in der Einzelansicht bräche die Regel „ein Haus, überall dasselbe Paar“ (`bot_wappen.json`, `zweck`).
- **Als Vorlage behalten:** Es ist das einzige Wappen im Meshy-Stil und freigestellt. Damit eignet es sich als **Stilreferenz für die sechs Abzeichen aus B3**, damit sie im Dezember aus einem Guss entstehen.
- **`_128` und `_64` verwerfen:** Sie lassen sich in Sekunden aus der 1024er-Datei neu ableiten (vormultipliziert, wie in Nr. 6). Liegen sie herum, werden sie aus Versehen benutzt. **Löschen nur mit Daniels Freigabe** (Regel 4).

---

## 5. Was ich nicht beurteilen kann

| Punkt | Was fehlt | Wie du es misst |
|---|---|---|
| **Sauberkeit der Alphakanäle**, Motive und Unterscheidbarkeit der 6 Wappen bei 8 px | das Assets-ZIP | ZIP nachliefern; ich rendere dann alle sechs bei 8, 12 und 18 px auf den sieben Geländefarben, wie bei den Markern in Nr. 10 |
| `Drachenschuppe.png` mit 1 KB | das Bild | Anteil der Pixel mit Alpha > 0 zählen; unter 5 % ist es praktisch leer |
| Anzeigegröße von `loadingpage/Nebelseetal_Loadingpage.png` | Fundstelle `main.py:18934` zeigt nur den Pfad | `winfo_width/height` der Ladefläche messen |
| Ob `motiv_1–8` und `gebaeude/hintergrund_neu/lager.png` noch irgendwo gezeigt werden | Laufzeitpfad hinter `quelle_der_karte` | Schalter in `gebaeude_motive.json` lesen; einmal ohne die Dateien starten |
| Ob `elfen_portrait.png` als Einheitensymbol gewollt ist | Zuordnung in `icons_index.json` (Zeile 48) | Daniel fragen |
| Motive der Wappen aus `CHRONIK_DER_WELT.md`, Teil 5 | die Datei lag nicht bei | Für den Bildauftrag B3 je Haus den Wortlaut übernehmen |
| Wie viele Bilder das Meshy-Guthaben im Dezember erlaubt | Kontostand | – |

---

## 6. Zusammenfassung in fünf Zeilen

1. **Bestand 370:** etwa 211 ausreichend, **73 zu klein**, 38 unbenutzt (24 davon bewusste Vorlagen), 59 doppelt oder fragwürdig, 1 UNBEKANNT.
2. **Tabelle B: 105 Bilder.** Davon fehlen **30 ganz**: 1 Ruine, 6 Kartenabzeichen, 15 Gebäudeansichten, 5 Kopfbänder, 3 Leistenstücke. 73 ersetzen zu kleine Bilder, 2 korrigieren Drachenfarben.
3. **Prio 1: keines.** Jede Ansicht hat einen Rückfall ohne Bild.
4. **Prio 2 (erster Dezember-Durchgang): 44 Bilder**, nämlich Ruine, 2 Drachen, 6 Abzeichen, 15 Gebäudeansichten, 2 Startbilder und 18 Warensymbole. **Prio 3: 61.**
5. **Wichtigste Codefrage vor jedem neuen Bild:** Wappen und Drachen werden beim Laden **quadratisch gezerrt** (Z1). Die neuen Abzeichen deshalb quadratisch anlegen, oder den Code auf Einpassen umstellen.

---

## Zusatzinformationen (nicht beauftragt)

> Hinweise, keine Anweisungen.

**Z1 Verzerrung beim Laden.** `_motivbild_skaliert` (`main.py:9129–9163`) skaliert **immer auf px × px**. Für die quadratischen C2-Motive ist das richtig, für die hochkant gemalten Wappen (0,63–0,74) und die Drachen (0,67–0,80) nicht. Die Burgen (0,84–0,98) sind nur leicht betroffen.
- **Abhilfe ohne neues Bild:** dasselbe Einpassen wie in `_lager_symbol` (`main.py:14957`, „einpassen, nicht verzerren“). Das ist ein Eingriff in `src/` und damit deine Entscheidung.
- **Bildregel für Dezember:** **Alle Kartenbilder quadratisch anlegen** (Motiv mittig, Rest durchsichtig). Dann ist das Problem unabhängig vom Code gelöst.

**Z2 Warum nicht überall 4 ×.** Seit F-51 ist 1 Tk-Pixel = 1 Bildpunkt. Der Faktor 4 sichert einen Schirm mit 200 % **und** Spielraum beim Verkleinern. Bei kleinen Symbolen kostet das nichts. Bei Flächen über 500 px wären es Dateien von 4000 px und mehr; die größten wären Startbilder mit 4096 × 2880 und ein Kopfband mit 4508 px.
- Deshalb dort **2 ×**, und bei den 1:1-Bildern (Register 502) **1 ×**.
- **Daniel entscheidet**, ob ihm das reicht.

**Z3 Rückfalldateien entrümpeln.** Hinter `clean/` liegen 45 alte Icon-Dateien als Rückfall (`main.py:3011–3018`). Sie werden nur benutzt, wenn die freigestellte Fassung fehlt. Das ist heute bei genau **einer** Datei der Fall: `Drachenschuppe.png`.
- Werden im Dezember die Waren und Einheiten neu gemacht (B6, B7), kann der ganze Rückfallsatz weg. **Mit Daniels Freigabe.**

**Z4 Ein Porträtfoto im Spielordner.** `assets/bilder/daniel_portrait.png` und `_klein` sind unbenutzt. Sie wandern aber vermutlich mit in jede EXE und jede „Public Edition“ (`test_public_edition_fix04j`).
- **Empfehlung:** aus dem Paketbau ausschließen oder aus `assets/` verschieben. Das ist Daniels Entscheidung (Regel 4), und es ist sein Bild.

**Z5 Emoji in der Kopfzeile.** `RESOURCE_ICONS` (`main.py:3198–3201`) setzt Emoji vor die Rohstoffe (`kopf_zeilen_text`, `main.py:3220–3242`). T08 hatte „keine Emoji“ festgelegt.
- **Bitte prüfen**, ob diese Texte noch irgendwo angezeigt werden. Wenn ja, ist das ein Rest aus der Zeit vor T08.

**Z6 Bildauftrag für Dezember in einem Zug.** Vorschlag für die Reihenfolge, damit der Stil zusammenpasst:
1. **Erst die sechs Abzeichen (B3) als ein Blatt.** Stilreferenz: das Meshy-Elfenwappen.
2. Dann Ruine und die 2 Drachen (B1, B2) in der Haltung von `drache_weiss`.
3. Dann die 18 Waren als zwei Blätter zu 9.
4. Zuletzt die großen Hintergründe (B4, B5).

Jedes Blatt wird danach mit dem vorhandenen Werkzeug geschnitten (`tools/burgen_wappen_schneiden.py`). So sind es weniger Meshy-Aufträge als Bilder.

---

Ende der Antwort auf Auftrag Nr. 18.
