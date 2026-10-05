# Nebelseetal Remake — Projektstand und Übergabe

Stand: **05.10.2026, 17:00** (mit `date`, `git log`, Sammellauf und Startprüfung geprüft; Schritt 31 ist
gebaut, 32–34 sind Dokumente). Diese Fassung ersetzt die
vorherige (archiviert unter `docs/archiv/PROJEKT_STAND_alt_2026-10-04_2345.md`; die Fassungen davor
unter `docs/archiv/PROJEKT_STAND_alt_2026-10-04_2200.md` und `..._alt_2026-10-04.md`).
**Diese Datei ist der Einstiegspunkt.** Jede neue Sitzung liest zuerst hier — nicht die Chat-Historie.
Abschnitte 1–11 sind der ältere, weiterhin gültige Rahmen; **Abschnitt 0c ist der aktuelle Stand.**

---

## 0. DAS LAUFENDE GESAMTZIEL — BITTE ÜBERNEHMEN

**Regel (Vorgabe Daniel, 05.10.2026):** Das **Gesamtziel** unten wird **nie** verändert oder ersetzt.
Jede neue Sitzung **passt nur ihre eigene Zielsetzung an den aktuellen Schritt an** (Zieltext im
Register = Wortlaut unten; der jeweilige Schritt steht in der Startzeile und in Abschnitt 0c,
Unterabschnitt „Der EINE nächste Schritt").

Daniels Ziel, wörtlich **und unverändert seit dem ersten Auftrag**:

> „Eine fertige schlüssige fehlerfrei Spielbare .exe, die stabil das Spiel Nebelseetal (damals
> Browsergame) als remake und Einzelspielerspiel startet. Überprüft und vllt so gesichert das man es
> nur spielen kann mit meinem vorgegebenen Passwort."

**Startzeile für die neue Sitzung (zum Kopieren — Stand 05.10.2026, 17:00, Schritt 31 ist erledigt):**

```
Lies D:\Arbeiten\Nebelseetal_Remake\docs\PROJEKT_STAND.md, Abschnitt 0c (Stand, Kontext-Paket, der
EINE nächste Schritt) — die Chat-Historie brauchst du nicht. Dann: python tools/zieluebergabe.py
--pruefen und setze dein eigenes Ziel: als Wortlaut das UNVERÄNDERTE Gesamtziel aus Abschnitt 0
(Schritt 31 ist erledigt — nichts davon wiederholen). Arbeite danach den EINEN nächsten Schritt aus
Abschnitt 0c: das Ökonomie-Paket in der Reihenfolge des Entwurfs
docs/audits/entwurf_spieloekonomie_sol_2026-10-05.txt (9 Schritte), und zwar ZUERST die vier
Handbuch-Korrekturen aus docs/audits/handbuch_abgleich_2026-10-05.txt. Nach jedem Schritt:
betroffener Einzeltest + einmal Sammellauf (keine Spielprozesse offen lassen), eine Protokollzeile
(Zeit mit `date` holen, nie schätzen), python tools/protokoll_sichern.py --protokoll, kleiner Commit;
prüfende Unteragenten erst NACH dem Commit. Am Ende des Pakets die .exe neu bauen (tools/build_exe.py)
und aus einem anderen Ordner startprüfen. Kommt von Daniel ein Spielbericht zur aktuellen .exe, hat der
VORRANG.
```

**Erste Handlung der neuen Sitzung:** `python tools/zieluebergabe.py --pruefen` (0 = kein fremdes Ziel).
**Vor dem Sammellauf keine Spielprozesse offen lassen** — sonst schlägt die erste Prüfdatei ohne
Ausgabe fehl (belegt 05.10., siehe Lehre (e) unten).
**Achtung, zwei Startzeilen:** `tools/zieluebergabe.py --startzeile` liefert eine **allgemeine
Vorlage**; verbindlich ist die **Startzeile direkt hier oben** (sie kennt den echten nächsten Schritt
und den Stand von heute).

**Zum eigenen Ziel:** das Ziel der Sitzung `20261005_150058_c9027c` ist am 05.10.2026 um 17:01 sauber
auf `cleared` gesetzt (Grund im Datensatz, kein fremdes aktives Ziel). Die neue Sitzung braucht ein
**neues** Ziel mit dem Wortlaut aus Abschnitt 0 — geprüft, dass kein Geisterläufer arbeitet.

---

## 0c. Stand (05.10.2026, 17:00, fortgeschrieben 18:30 — mit `date`, `git log`, Sammellauf und Startprüfung geprüft)

> ### NEU: Schritt 31 fertig · Daniels Richtungsentscheidung · zwei starke Modellläufe ausgewertet
>
> **1. Raster 8 × 7 = 56 Felder, davon 40 bebaubar (Schritt 30, Commit `ec89dc6`).** Gesperrt ist **nur
> der Sumpf** (Variante B; das Handbuch belegt sieben Geländearten). `bauplaetze` heißt jetzt „bebaubare
> Felder", neu dazu `felder` = 56. Unabhängig nachgeprüft (1600 Karten, 0 Verstöße).
>
> **2. Sieg/Niederlage eingehängt (Schritt 31, Commit `2cb8ce6`).** `GameState.punktestand()` +
> `spielausgang()` über `src/punkte.py`; `_pruefe_spielende()` hält den Ausgang **einmal** fest;
> Seitenleiste zeigt „Ziel: x / 300 Punkte" bzw. **SIEG**/**NIEDERLAGE**; die Spieluhr steht danach;
> der Ausgang wird mitgespeichert. **Vor der ersten Siedlung gilt die Partie nicht als verloren.**
> Prüfbeleg: `test_punkte_einhaengung` **60/0/0**.
>
> **3. Daniels neue Richtungsvorgabe (05.10.2026, 16:1x–16:2x), wörtlich in
> `docs/ENTWURF_SPIELZIEL_HANDEL_KARTEN.md`:** kein „wer schneller ist, gewinnt" — **Handel zwischen
> den eigenen Siedlungen** und die **Wahl der richtigen Karten** tragen das Spiel; eine Neugründung muss
> **teuer** sein und ein **Mindestguthaben** verlangen; nur die **Startkarte** ist ausgeglichen, die
> Neugründungen kommen aus einem Vorrat mit **2–3 ausgeglichenen** und sonst spezialisierten Karten;
> **entschieden:** der **Punktestand** (Forschung **und** Krieg) entscheidet, verdient über eine echte
> Ökonomie · Gründungspreis **320/200/150 + Startpaket 160/100/100 + Mindestbestand 480/300/250 + ein
> Siedlerkarren** („so übernehmen, später nach und nach anpassen") · **Startkarte + 10 Karten** bei
> höchstens 6 Siedlungen · Bots **leicht/mittel/schwer** kennen die Ökonomie.
>
> **4. Zwei starke Modellläufe (Kosten gemessen, nicht geschätzt):** der Ökonomie-Entwurf auf
> `gpt-6.1-sol` kostete **1,2332 USD** (`docs/audits/entwurf_spieloekonomie_sol_2026-10-05.txt`, 1140
> Zeilen, Gliederung A–H mit Code); der **Handbuch-Abgleich** auf `deepseek-v4-pro` **0,2459 USD**
> (`docs/audits/handbuch_abgleich_2026-10-05.txt`, 145 Zeilen, jede Stelle mit Zitat).
>
> **5. Der Handbuch-Abgleich hat vier echte Widersprüche in unserem Code gefunden** (alle vom
> Koordinator selbst nachgelesen — **das Handbuch gewinnt**):
> **Götterschutz** 7 Tage und Ende mit dem ersten Kriegspunkt (HB Z. 215-217) gegen fest **Tag 3**
> (`main.py` Z. 1093) · **Steinmetz ohne Forschung** baubar (HB Z. 279-281) gegen **Baukunst**
> (`buildings.json` Z. 44) · ein Forschungsauftrag sperrt die **ganze Siedlung** (HB Z. 423-424) gegen
> nur dasselbe Gebiet (`forschung.py` Z. 123-124) · **Rinderfarm Nahrung UND Leder** (HB Z. 362-365)
> gegen nur Leder. Dazu vier Funktionsfehler: **„Vermessung" existiert nicht** (Karten werden nie
> freigeschaltet) · **`_transport_to_settlement` bucht 10 Holz ab, ohne Gutschrift** — es gibt also
> **keine** Handelsmechanik · die **Uhr ist gemischt** (×180 nur für die Produktion) · der **Bot-Handel
> verschenkt** Zufallsrohstoffe.
>
> **6. `.exe`:** **14.577.217 Byte**, SHA256 `9f5c1deb…`, Dateizeitstempel `16:59:37`, genau **eine**
> EXE, aus `C:\Users\saras` startgeprüft (ein Fenster, antwortet 10/20/40 s, sauber über `WM_CLOSE`,
> danach 0 Prozesse). Enthält Raster **und** Sieg-/Niederlagebedingung.
>
> **7. Prüfstand:** Sammellauf **2665 bestanden, 0 Fehler, 21 Befunde über 41 Dateien**. **Guthaben
> (Daniel abgelesen 16:5x): DeepSeek 3,24 USD · OpenAI 0,97 USD.**
>
> **Bau-Umgebung für die `.exe` (liegt im Zwischenspeicher und wird nach 24 h geleert — dann neu
> anlegen):** `uv venv --python 3.14.7 <ordner>` · `uv pip install --python <ordner>/Scripts/python.exe
> pyinstaller` · `python tools/build_exe.py --python <ordner>/Scripts/python.exe`.

**Darunter der Stand vom Vormittag** (Sitzung `20261005_104846_864c4b`, sauber beendet um 13:44) —
gültig, wo oben nichts Neues steht:

**Diese Sitzung (`20261005_104846_864c4b`) ist am 05.10.2026 um 13:44 sauber beendet** (`cleared`,
kein fremdes aktives Ziel — `--pruefen` = 0). Sie hat Daniels Erweiterung vom 05.10. umgesetzt:
**feinere Karten**, **Ausrüstung/Forschung/Hausausbau**, **Geländeregeln für alle Gebäude** und —
nach Daniels Spielbericht — den **Zeitfaktor** samt sichtbarem Rohstoffeingang.

### Nicht erneut zu prüfen (Stand 05.10.2026, alles mit Beleg)

| Was | Beleg | Wann |
|---|---|---|
| **Sammellauf 2599 bestanden, 0 Fehler, 21 Befunde über 41 Dateien** | Protokoll 28 + BOARD + `docs/ENTWICKLUNGSPROTOKOLL.md` | 13:3x |
| **`.exe` 14.531.774 Byte, SHA256 `bffd3c44…`** (Zeitfaktor + Warnung + Geländeregeln) | `stat -c %y` = `13:41:04`, Startprüfung aus `C:\Users\saras` | 13:41 |
| **Geländeregeln unabhängig gegengeprüft: 6 Prüfsteine, 0 Abweichungen**, Alt-Spielstände ladbar | BOARD-Zeile „kind-pruefer (Geländeregeln)" | 13:33 |
| Zeitfaktor: Handbuchformeln unangetastet, ×180 = 1 Spielstunde in 20 s | `tests/test_spielzeit.py` **24/0/0** | 13:2x |
| Aufgabenkarte nennt den fehlenden Erzeuger, Kopfzeile warnt statt „(0)" | `tests/test_startspiel.py` **46/0/0** | 13:3x |
| Alle 20 Gebäude haben eine Geländeregel, Nebelsee nur Bibliothek+Tempel | `tests/test_gelaende.py` **86/0/0** | 13:2x |
| Papiere außerhalb des Projekts gesichert (16 Dateien, Prüfsummen) | `D:\Arbeiten\Hermes\Nebelseetal_Protokoll\zuletzt.txt` | 13:43 |

| Was | Stand (gemessen) |
|---|---|
| Prüfstand | **2599 bestanden, 0 Fehler, 21 Befunde über 41 Dateien** (Sammellauf 13:3x, sauberer Lauf ohne offene Spielprozesse) |
| **Zeitfaktor (erledigt, Schritt 28)** | `src/spielzeit.py` + `data/spielzeit.json`: **Standard ×180** (VORSCHLAG: 1 Spielstunde = 20 echte Sekunden; ×1 = Originaltempo weiter wählbar). **Die Handbuchformeln bleiben unangetastet** — nur die Spieluhr läuft schneller; angewandt an einer Stelle (`_tick_loop`), Wegezeiten rechnen mit, in den **Einstellungen** umstellbar, Kopfzeile zeigt „Tempo ×180 · 1 Std = 20 s". **Belegter Befund (Daniels Spielbericht):** vorher rechnete `tick` Echtzeitsekunden 1:1 — 4 Holz je **echter** Stunde, nach einer Sekunde auf 0,00 gerundet, also kein sichtbarer Eingang |
| **Aufgabenkarte gegen das Festbauen (erledigt, Schritt 28)** | Die Karte nennt **vor** dem Forschen den fehlenden Erzeuger samt Feld und Preis (Holz → Holzfäller · Stein → Steinmetz · Nahrung → Farm); die Kopfzeile zeigt für Kernrohstoffe ohne Erzeuger **⚠** statt „(0)". Geprüft in `tests/test_startspiel.py` (46/0/0) |
| **Ausrüstungskette (erledigt, Schritt 26)** | `_train_unit` verlangt jetzt **beides** aus `data/units.json`: die **Forschungsstufe** (Kämpfer 1 · Krieger 3 · Ritter 7 · Paladin 10 · Gauner Heimlichkeit 1 · Karren/Belagerung Wagenbau 1–10) **und die Ausrüstung** (14 der 28 Einheiten brauchen Waren — Krieger: Schwert + Kettenhemd · Paladin: Zweihänder + Schwert + Harnisch). Die Waren werden beim Auftrag verbraucht; der Knopf ist gesperrt und nennt das Fehlende mit Soll/Ist. Früher war **keine** dieser Bedingungen wirksam |
| **Forschung (erledigt, Schritt 26)** | `_start_research` erzwingt die Voraussetzungen aus `data/research.json`; die Ansicht zeigt je Forschung „schaltet frei — Waren/Einheiten" bzw. „gesperrt: Grund". Quelle: `src/forschungspfad.py` (123 Prüfungen) |
| **Hausausbau (erledigt, Schritt 25)** | Haus bis **Stufe 4**, je Stufe **+5 Siedler** (Stufe 1 = belegtes Haus, VORSCHLAG für 2–4). `data/gebaeude_wirkung.json` → „haus_stufen" |
| **Geländeregeln (erledigt, Schritt 27)** | Jedes der 20 Gebäude hat jetzt eine Eignungsregel in `data/buildings.json` (`nur_auf`). Belegt: Sumpf für alle gesperrt · Bibliothek Grasland/Steppe/Nebelsee · Tempel überall außer Sumpf · Produktionsgebäude aus der Handbuch-Ertragstabelle (Holzfäller Steppe/Wald · Steinmetz, Erz- und Goldmine Hügel/Berg · vier Zuchten Grasland/Steppe · Jäger Steppe/Wald). **VORSCHLAG für die neun übrigen** (Haus, Lager, Schmiede, Bogenbauer, Nähstube, Kriegerakademie, Diebesgilde, Stellmacher, Wall) — in der Datei als Vorschlag gekennzeichnet, von Daniel änderbar. **Folge: im Nebelsee stehen nur noch Bibliothek und Tempel.** Geprüft in `tests/test_gelaende.py` (86/0/0) |
| **Feinere Karten (Schritt 24/25)** | eingehängt: `src/karten_optik.py` (Siedlungskarte) und `src/welt_optik.py` (Weltkarte). **Gebaut, NOCH NICHT eingehängt:** `src/karten_optik_fein.py` (80 Prüfungen) und `src/welt_optik_fein.py` (128) — die Umsetzung des zweiten astra-Gutachtens |
| Gutachten dieser Sitzung | `docs/audits/ux_astra_karten_feinheit_2026-10-05.txt` (astra über zwei echte Aufnahmen in `docs/audits/aufnahmen_2026-10-05/`) · `docs/audits/entwurf_ausruestung_forschung_haus_2026-10-05.txt` (deepseek-v4-pro: Kette, Forschungstabelle, Hausstufen, 30-Minuten-Einstieg, Zeitfaktor 1:20 als VORSCHLAG) |
| `.exe` | **05.10. 13:41 gebaut** (Dateizeitstempel `13:41:04`): **14.531.774 Byte**, SHA256 `bffd3c444d6eb1433b14c1b7a768946cc45bdc1d8511332bca0de33bc7a85ed3`, aus `C:\Users\saras` startgeprüft (ein Fenster, genau eine Instanz) — **enthält Zeitfaktor, Rohstoff-Warnung und Geländeregeln** (Schritte 27 und 28). Ältere Fassungen: 13:29 (14.524.603 Byte, `1fad511d…`, Geländeregeln) · 12:38 (14.524.225 Byte, `63b09fbf…`). `build/`, `dist/`, `.spec`, `__pycache__` sind aufgeräumt, genau eine EXE im Projektordner. **Wichtig:** nur diese Fassung zeigt Tempo und Warnung — wer mit einer älteren spielt, sieht den Zeitfaktor nicht |
| Guthaben | **von Daniel abgelesen am 05.10. um 13:48: OpenAI 2,17 USD · DeepSeek 4,06 USD** (11:00: 2,66 / 4,97 → im Nachmittag 0,49 bzw. 0,91 USD verbraucht). **Gemessener Tagesverbrauch laut `scripts/tageskosten_check.py`: 4,13 USD ≈ 3,68 EUR über 23 Sitzungen und 4 Modelle = 80 % des harten Tageslimits (4 EUR) — Lage „WARNUNG".** Für die nächste Sitzung heißt das: **keine teuren Aufrufe ohne Begründung**, Kinder und Prüfer nur auf `deepseek-flash`, Bilddeutungen (astra) nur, wenn es wirklich nicht anders geht. **Beobachtung zum Messskript:** es meldete zwischen 13:45 und 13:48 nur +0,005 USD, während Daniels Guthabenanzeige um **0,19 USD** fiel — die Schätzung läuft der Anbieterwahrheit nach. **Maßgeblich ist die Guthabenanzeige des Anbieters, nicht die Schätzung** |

### Der EINE nächste Schritt (Stand 05.10.2026, 17:00 — Schritt 31 ist ERLEDIGT)

**Der neue nächste Schritt: das Ökonomie-Paket bauen — zuerst die vier Handbuch-Korrekturen, dann die
neun Schritte des Entwurfs.** Der Auftraggeber hat das Paket ausdrücklich so entschieden („das ganze
Paket in der Reihenfolge des Papiers — kein Halbumbau").

1. **Die vier Handbuch-Korrekturen** (`docs/audits/handbuch_abgleich_2026-10-05.txt`, Abschnitt „Die
   zehn wichtigsten Abweichungen", Punkt 1–4): Götterschutz **7 Tage** bzw. Ende mit dem ersten
   Kriegspunkt statt Tag 3 · **Steinmetz ohne Forschung** · Forschung sperrt die **ganze Siedlung** ·
   **Rinderfarm Nahrung UND Leder**. Jede ist belegt, **das Handbuch gewinnt** — keine Rückfrage nötig.
2. **Schritt 1 des Entwurfs** (`docs/audits/entwurf_spieloekonomie_sol_2026-10-05.txt`, Z. 209-233):
   `data/gelaende.json` um `kartenvorrat` (Startkarte + zehn Koloniekarten mit den Feldkontingenten aus
   Tabelle B) erweitern · neue `data/spieloekonomie.json` (Gründung, Fenster, Schwellen, Planbedarf,
   Bot-Stufen) · neue `tests/test_spieloekonomie.py`. **Die alten `kartentypen.listen` und ihr Generator
   bleiben unverändert**, bis der letzte Integrationsschritt kommt.
3. **Danach die Schritte 2–9 des Entwurfs** in ihrer Reihenfolge (deterministischer Kern · lokale Lager
   und Transportbuchung · Warenrezepte und lokale Ausbildung · gemeinsame Spieluhr · Forschung je
   Siedlung · Zielprüfung und Haltefenster · Bot-Planung · `main`-Anbindung und Migration).
   **Erst nach dem letzten Schritt** wird auf den Ökonomiemodus umgestellt; Altpartien bleiben Altmodus.

#### Ist-Stand des Pakets (05.10.2026, 18:30 — mit Werkzeugen geprüft, nicht behauptet)

**Schritte 0 bis 5 sind ERLEDIGT und geprüft. Der nächste Schritt ist Schritt 6 (Forschung je
Siedlung), danach 7, 8, 9 und zuletzt die Aktivierung (10).**

| Schritt | Inhalt | Stand | Beleg (Commit / Prüfzahl) |
|---|---|---|---|
| 0 | die vier Handbuch-Korrekturen | **fertig** | `203e2fa` · Kinderprüfung 18 Zeilen, **0 Widersprüche** (`6f8ef2f`) |
| 1 | Kartenvorrat · `data/spieloekonomie.json` · `test_spieloekonomie.py` | **fertig** | `c68a60f` |
| 2 | deterministischer Kern `src/spieloekonomie.py` | **fertig** | `a50edd6` · `test_oekonomie_kern_unabhaengig` **158/0/0** |
| 3 | lokale Lager und Transportbuchung (Karrenpflicht) | **fertig** | `40` · `test_lokale_lager` **70/0/0**, `test_warentransport` **45/0/0** |
| 4 | Warenrezepte (`data/warenrezepte.json`) und lokale Ausbildung | **fertig** | `e6fd766`, `3bdbc6a` · `test_warenrezepte` **26/0/0**, `test_ausbildungsauftraege` **49/0/0** |
| 5 | gemeinsame Spieluhr: `ort_tick`, `fensterproduktion` | **Kern fertig** | `319c16b`, `a83ec25` · `test_oekonomie_uhr` **42/0/0** |
| 6 | Forschung je Siedlung | **offen — der nächste Schritt** | — |
| 7 | Zielprüfung und Haltefenster | offen | — |
| 8 | Bot-Planung | offen | — |
| 9 | `main`-Anbindung und Migration | offen | — |
| 10 | Ereignisschleife `tick_bis` und Aktivierung | offen | — |

**Aus Schritt 5 ist bewusst noch NICHT gebaut:** die Umstellung der `main`-Uhr auf `spielsekunden`
(genau **eine** Stelle mit `spielzeit.faktor()`). Das gehört zur Anbindung (9/10), und **vorher darf
der Ökonomiemodus NICHT aktiviert werden** (Entwurf Z. 1092). Bis dahin läuft der **Altmodus
unverändert**, und **nichts** im Spiel ruft `src/spieloekonomie.py` auf — das ist Zusage, nicht Zufall,
und wird von den Prüfdateien mitgeprüft.

**Vorgemerkt für NACH diesem Paket (Vorgabe Daniel, 05.10.2026, 18:1x): die Kampfverluste
verdrahten.** Wörtlich: bei verlorenem Kampf soll „ein prozentualer anteil an truppen vernichtet"
werden, „vorallem Karren und Transporteinheiten"; bei Sieg überleben die Transporteinheiten; bei
knapp gewonnenen, fast gleichen Kämpfen muss „trotzdem" ein großer Teil der Armee Schaden nehmen
oder sterben, aber „nicht immer alle truppen vernichtet" sein. **Befund:** das Handbuch nennt die
Regel wörtlich (S. 23, Z. 1330-1338: der **Verlierer** verliert einen Teil seiner Karren und
Belagerungswaffen, Fluchtchance **40 % + 5 % je Kampfsequenz**; unentschieden kostet nichts), und
`src/kampf.py` **hat sie gebaut** (`_geraeteverluste`, Z. 192-202; Einzelverluste Z. 181-189).
**Es fehlt allein die Verdrahtung in die Oberfläche** — das nennt `spielschicht.offene_luecken()`
selbst. Festgehalten in `docs/ENTWURF_KAMPFVERLUSTE.md` (mit der einen offenen Entscheidung: keine
erfundene Prozentzahl, erst bauen und messen).

**Arbeitsweise für diesen Schritt (Vorgabe Daniel, unverändert):** nach jedem Schritt den betroffenen
Einzeltest **und einmal den Sammellauf** — dabei **keine Spielprozesse offen lassen** (sonst schlägt die
erste Prüfdatei ohne Ausgabe fehl). Danach **eine Protokollzeile** mit der Zeit aus `date` (nie
schätzen), dann `python tools/protokoll_sichern.py --protokoll` und ein **kleiner Commit**. Prüfende
Unteragenten erst **NACH** dem Commit loslassen. Ändert sich etwas in `src/` oder `data/*.json`, am
Ende die `.exe` neu bauen (`tools/build_exe.py`) und aus einem **anderen** Ordner startprüfen. Bei
jedem Schritt, der eine **belegte** Handbuchregel berührt: **erst das Handbuch lesen**, dann ändern.

### (Liste vom Vormittag — die Punkte 1 und 3 sind inzwischen erledigt)

**Erledigt und nicht zu wiederholen:** der `.exe`-Neubau nach den Geländeregeln — **gebaut am
05.10. um 13:41:04** (14.531.774 Byte, SHA256 `bffd3c44…`), aus `C:\Users\saras` startgeprüft.

1. **Erledigt in Schritt 29** — die zwei Feinkarten-Module (`karten_optik_fein`, `welt_optik_fein`)
   sind eingehängt; die Notizen unten bleiben als Nachvollziehbarkeit stehen. astra hat die
   Zahlen geliefert: Baukörper 44×46 px, Dach 38×16, Sockel 36×5, Tür 6×10, Fenster 4×5 (#875241/
   #59382F/#C0AD86/#8F795C) · Uferband 3–5 px #999071 nur an echten Land-Wasser-Grenzen · Weg 8 px
   #75674F mit 4 px Innenlinie #A28E69 · Auswahl 5 px #172128 + 2 px #E4C77D + vier 8-px-Eckwinkel ·
   Stufenpips 4×4 px · Koordinatenleiste 18 px · Weltkarte: 1-px-Raster #38433C, Varianten
   **deterministisch aus den Feldkoordinaten** (sonst springt das Bild beim Neuzeichnen).
   **Drei Dinge beim Einhängen beachten** (Befunde der Kinder, 05.10.2026): (a) Geländefarben für
   Steppe/Hügel/Sumpf stehen **nicht** im astra-Bericht — sie gehören aus `gelaende.farbe()` bezogen,
   sonst entstehen zwei Farbwahrheiten; (b) `#637451` wird im Modul für Ebene **und** Wald verwendet
   (astra nennt drei Lichtfarben für vier Geländearten) — beim Einhängen prüfen und ggf. trennen;
   (c) astra spricht vom **8×7-Raster**, im Projekt gilt `spalten 8 × zeilen 5 = 40 Felder`
   (Frage 12 an Daniel) — die Module nehmen `spalten`/`zeilen` als Parameter, die Zahlen also vom
   Aufrufer übergeben, nie im Modul festlegen.
2. **Aufgabenkarte für den Einstieg** (Entwurf Abschnitt D): Holzfäller/Steinmetz → Bibliothek →
   Baukunst → Farm/Haus → Schmiedekunst → Schmiede/Nähstube → erste Ware → erste Einheit.
3. **Erledigt am 05.10.2026 (14:24) — alles beantwortet:** **Zeitfaktor bestätigt** (×180) · die
   neun Geländeregeln bestätigt · Raster **8×7 = 56/40 gebaut (Schritt 30)** · Lichtfarbe getrennt ·
   **Sieg-/Niederlage: Vorschläge am 15:16 vorgelegt, Wahl offen.** Der ursprüngliche Wortlaut dieser
   Zeile: **Zeitfaktor bestätigen** — er ist jetzt gebaut und in den
   Einstellungen umstellbar (Vorschlag ×180 = 1 Spielstunde in 20 Sekunden; ×1 = Originaltempo) ·
   **die neun Geländeregeln bestätigen oder ändern** (eine
   Zeile je Gebäude in `data/buildings.json`) · **Sieg-/Niederlagebedingung** (heute
   unerreichbar!) · Kampfmagie als einziger größerer Vorschlag · Ausbaustufen des Hauses
   bestätigen (Stufe 4, je +5 Siedler) · Raster 8×7 oder 8×5 — **entschieden und gebaut: 8×7, 40 von 56 bebaubar.**

**Lehren dieser Reihe:** (a) ein grüner Prüfstand beweist keine Spielbarkeit — die alte Prüfung fuhr
Methoden statt Schaltflächen; (b) **Zeiten nie schätzen**, immer `date`; (c) eine Zeichenfläche, die
im Fenster mitwächst, macht ihre Scrollbalken wirkungslos (feste Größe!); (d) **kein Kind und kein
Sammellauf laufen lassen, während `main.py` umgebaut wird** — der Lauf misst sonst einen
Zwischenstand; (e) beim Sammellauf **keine Spielprozesse** offen lassen (`test_tor` meldet sonst
einen zweiten Start als Fehler; am 05.10. schlug `test_baseline` als erste Datei zweimal mit leerer
Ausgabe fehl, während das Spiel offen war — allein und im sauberen Lauf 40/0/0); (f) ändert man eine
**Datendatei** (`data/*.json`), muss die `.exe` neu gebaut werden, sonst spielt Daniel den alten
Stand.

**Auftrag vom 05.10.2026 (wörtlich, zur Nachvollziehbarkeit):** „Arbeite danach den EINEN nächsten
Schritt aus Abschnitt 0c: die Weltkarte nach der astra-Vorgabe nachziehen (Zeichenfläche, Zoomstufen,
Scrollbalken, Detailpanel, Übersichtskarte)." — **erledigt in Schritt 24–26** (Weltkarte) und
**Schritt 27** (Geländeregeln). Der aktuelle nächste Schritt steht oben in dieser Liste.
## 0d. Abschluss und Selbstreflexion dieser Sitzung (05.10.2026, 17:00 — mit `date` geprüft)

**Zustand:** nichts läuft. Kein Prozess offen, Arbeitsverzeichnis **sauber** (alle Commits bis
`d03861a` + die Dokumente dieses Abschlusses), **genau eine** EXE im Projektordner, keine Bau-Reste
(`build/`, `dist/`, `.spec`, `__pycache__` entfernt), die 16 führenden Papiere projektunabhängig
gesichert (`D:\Arbeiten\Hermes\Nebelseetal_Protokoll\`). Letzter Sammellauf: **2665 bestanden,
0 Fehler, 21 Befunde über 41 Dateien**. Das Gesamtziel in Abschnitt 0 bleibt **unverändert**.

**Was diese Sitzung geleistet hat (Schritt 30–34):** das Siedlungskarten-Raster auf **8 × 7 = 56
Felder, 40 bebaubar** umgestellt · die **Sieg-/Niederlagebedingung** eingehängt · Daniels **neue
Richtungsvorgabe** (Handel und Kartenwahl statt Wettlauf) aufgenommen und in vier Entscheidungen
festgehalten · einen **Ökonomie-Entwurf** von `gpt-6.1-sol` eingeholt, **nachgerechnet** und gesichert
· einen **Handbuch-Abgleich** von `deepseek-v4-pro` eingeholt, ausgewertet und die vier gefundenen
Widersprüche selbst im Handbuch bestätigt · `.exe` zweimal neu gebaut und startgeprüft.

**Was gut lief:** erst 0c gelesen statt Historie · Zielregister vor der ersten Änderung geprüft · jede
Zahl mit Werkzeugausgabe belegt · den Kindbericht **selbst nachgemessen** (1200 Karten, 0 Verstöße)
statt geglaubt · den Entwurf des starken Modells **nachgerechnet** (alle Kernzahlen reproduziert, die
Kernbehauptung bestätigt) · beide Quellenfehler **wörtlich im Handbuch** nachgeschlagen, statt sie zu
übernehmen · Kosten ehrlich korrigiert, sobald die Messung sie widerlegte.

**Meine fünf Fehler — damit die nächste Sitzung sie nicht wiederholt:**

1. **Kostenschätzung um Faktor 3 daneben.** Ich sagte 0,15–0,40 USD für den Entwurf, gemessen wurden
   **1,2332 USD**; beim Abgleich wiederholt (0,05–0,15 gesagt, **0,2459** gemessen). *Ursache, die ich
   nicht bedacht hatte:* das Modell liest den **ganzen** Kontext bei **jedem** Aufruf neu.
   *Regel: Aufrufe × Kontextgröße rechnen, `--usage-file` mitgeben, Kontostand vorher nennen.*
2. **Ich habe dem starken Modell einen falschen Ist-Zustand vorgegeben** („Transport vorhanden",
   „Vermessung schaltet Karten frei"). Es hat mich korrigiert. *Regel: eigene Ist-Angaben vorher prüfen —
   derselbe Fehler wie am 05.10. vormittags bei „Sumpf und Nebelsee".*
3. **Die erste Startprüfung war falsch gebaut.** Ich suchte die Fenster nach Prozess-Kennung; eine
   PyInstaller-Einzeldatei startet aber **zwei** Prozesse, das Fenster gehört dem Kind. *Regel: Fenster
   nach **Titel** suchen, nicht nach PID.*
4. **Fast zu früh gebaut.** Nach dem Handbuch-Abgleich wollte ich direkt loslegen; Auftraggeber musste
   erst anordnen, **alles** gegen das Handbuch abzugleichen. *Regel: erst die Quelle prüfen, dann bauen —
   der Entwurf hätte sonst vier belegte Regeln mit falschen Werten eingebaut.*
5. **Zwei Protokollzeilen mit Platzhalterzeit** (`16:5x`, `17:0x`) geschrieben und erst danach durch die
   echte `date`-Zeit ersetzt. *Regel: die Zeit **vor** dem Schreiben holen.*

**Dauerhaft aufgenommen:** das Gesamt-Verfahren steht jetzt im Skill `nebelseetal-remake` (Abschnitt
„Neue Lehren 05.10.2026, Abend"): Auftragsdatei → **ein** starker Lauf → Tabelle mit Zitat-Urteil →
**jeden Kernbefund selbst nachlesen**; dazu die belegten Handbuch-Regeln als Nachschlagewerk
(Götterschutz 7 Tage · Steinmetz ohne Forschung · Forschung sperrt die Siedlung · Rinderfarm mit
Nahrung **und** Leder · 6 Siedlungen · Karten per Zufall · Beute nur mit Karren · „Vermessung" gibt es
nicht · die Uhr ist gemischt). Die reine Kostenregel steht im Sitzungsgedächtnis.

**Nebenbefund, der bleibt:** die Sammlung der Prüfungen wächst mit jedem neuen Test — der Sammellauf
liegt jetzt bei **2665**. Wer eine feste Sollzahl aufschreibt, erzeugt Falschalarm; verbindlich ist
**0 Fehler**, nicht die Summe.

## 0b. Stand beim Sitzungswechsel (04.10.2026, 23:45 — mit `date` geprüft)

**Nichts ist in Arbeit. Kein Prozess läuft, kein Kind arbeitet. Arbeitsverzeichnis sauber**
(Commit `9bbb3c2`), alles committet, Papiere projektunabhängig gesichert
(`D:\Arbeiten\Hermes\Nebelseetal_Protokoll\`, 14 Dateien, Prüfsummen geprüft).

| Was | Stand (gemessen) |
|---|---|
| Prüfstand | **1651 bestanden, 0 Fehler, 9 Befunde** über **23 Dateien** (`run_tests.bat`, Rückgabewert 0) |
| Fertige Module (alle vom Koordinator nachgerechnet) | `forschung_wirkung` 94 · `werkstatt` 118 · `portalraum` 69 · `punkte` 76 · `kampfbericht` 108 · `spielschicht` 133 · `botkern` 90 · `auftraege` 111 · `speichern` 95 · `oberflaeche_original` 64 |
| Eingehängt | W4b-5 (Gebäudewirkungen), W4b-6 (21 Forschungen + alle neun Rohstoffe), Passworttor |
| **Nicht** eingehängt | die zehn Module in der Oberfläche — **das ist der nächste Schritt**, nach `docs/UMSETZUNG_EINHAENGEN.md` |
| `.exe` | liegt im Projektordner (14.024.744 Byte), mit Tor startgeprüft; **Neubau erst nach dem Einhängen** |
| Kosten der Nacht | teure Aufrufe zusammen **+0,79 USD** (astra für die Bilder, v4-pro für den Plan); Guthaben: OpenAI **4,08** · DeepSeek **2,08** USD (1,00-USD-Reserve unberührt) |
| Offene Fragen an Daniel | **13** — `docs/FRAGEN_FUER_MORGEN.md` |
| Brett der Kinder | **abgeschafft** (Daniel, 04.10.) — Kinder melden im Abschlussbericht, der Koordinator prüft nach und trägt in `docs/BOARD.md` ein |

### So startet die neue Sitzung (kurz — nichts doppelt prüfen!)

**Regel: nur das prüfen, was sich seit dieser Übergabe geändert hat.** Der Sammellauf ist teuer
(rund 7 Minuten) und war beim Schreiben dieser Zeilen grün. Wenn `git log` zeigt, dass seither
**nur Dokumente** dazukamen, ist ein neuer Sammellauf **nicht** nötig — erst nach der ersten
Änderung an `src/`.

```bash
cd /d/Arbeiten/Nebelseetal_Remake
git log --oneline -3     # was kam seit 9bbb3c2 dazu? nur docs/* => nichts nachzuprüfen
git status --short       # leer = sauber (wenn nicht: erst fragen, nicht überschreiben)
```

**Nicht erneut zu prüfen (Beleg steht hier, nicht im Kopf):**

| Sache | Beleg | Stand |
|---|---|---|
| Prüfstand | `run_tests.bat`, Rückgabewert **0** | 04.10.2026, 23:40 — **1651 / 0 Fehler / 9 Befunde**, 23 Dateien |
| Die zehn Kind-Module | je eigener Lauf des Koordinators | 23:16–23:20, Zahlen in der Tabelle oben |
| `.exe` + Passworttor | Startlauf mit Fenster, sauberes Schließen | 22:42; Datei 14.024.744 Byte im Projektordner |
| Papiere gesichert | `MANIFEST.txt` mit SHA256 je Datei | 04.10.2026 nach jeder Änderung, 14 Dateien |

**Erst wenn `src/` angefasst wird:** den betroffenen Einzeltest laufen lassen (nicht den Sammellauf!),
und den Sammellauf einmal am Ende des Schritts.

### Schritt 1 (der einzige nächste Schritt)

`src/speichern.py` einhängen — **`main.py:608-634`**: in `save()` das direkte Schreiben
(Zeile **627-628**: `open(path,"w")` + `json.dump`) durch `speichern.sichere_kopie(path)` +
`speichern.speichere(data, path)` ersetzen (Rückgabe `(ok, grund)` auswerten und bei `ok == False`
über `self._log(...)` melden), in `load()` über `speichern.lade(path)` lesen und bei Fehlschlag
`speichern.wiederherstellen(path)` versuchen. Einzelprüfung danach:
`python -X utf8 tests/test_speichern_robust.py` → **95 grün** · `tests/test_baseline.py` → **40 grün**.
Alles Weitere steht in `docs/UMSETZUNG_EINHAENGEN.md`, Abschnitt 4 und 5.

---

## 1. In zwei Befehlen prüfen

```bash
cd /d/Arbeiten/Nebelseetal_Remake
run_tests.bat
git log --oneline | head -12
```

Erwartet: **1651 bestanden, 0 Fehler, 9 Befunde** über **23** Prüfdateien (gemessen im Sammellauf
`run_tests.bat` am 04.10.2026, 23:40 — Rückgabewert 0). Die neun Befunde sind ehrliche Hinweise, keine
Fehler; sie stehen bei den jeweiligen Modulen (u. a. fehlende Ausbildungsdauer, keine Dateisperre beim
Speichern, Rundung der Gesamtpunkte).
Einzelaufstellung (gemessen): baseline 40 · spieldaten 53 · kampf 42 · gelaende 81 ·
siedlungskarte 33 · kartenansicht 40 · berater 66 · wirtschaft 42 · forschung 68 · welt 42 ·
ertrag_anbindung 21 · gebaeude_wirkung 103 · tor 61 · forschung_wirkung 94 · werkstatt 118 ·
portalraum 69 · punkte 76 · kampfbericht 108 · spielschicht 133 · botkern 90 · auftraege 111 ·
speichern 95 · oberflaeche_original 64.
Die neun **Befunde** sind ehrlich und bekannt, keine Fehler: (1) das Handbuch nennt keine
Ausbildungsdauer, deshalb kann die Stufe einer Ausbildungsstätte die Dauer noch nicht messbar senken
(`bonus_system.UNIT_TRAIN_BASE = 0`); (2) `werkstatt` meldet eine Lücke in den Waren-Regeln, die
das Handbuch offen lässt; (3) weitere ehrliche Hinweise in `punkte` (Rundung, Götterschutz),
`speichern` (keine Dateisperre, Klartext), `auftraege` und `spielschicht` (Kampfverluste,
Ausbildungsdauer, Portal-Mana je Siedlung) — alle dort als Vorschlag gekennzeichnet.

Grün heißt „nichts ist kaputt und die umgestellten Teile halten sich ans Handbuch" — **nicht**
„Spiel ist fertig". Was fehlt, steht in Abschnitt 5.

**Achtung:** `test_kartenansicht.py` braucht einen angemeldeten Windows-Desktop (es baut ein echtes
Fenster und bedient es). Ohne Bildschirm bricht es mit klarer Meldung ab.

## 2. Richtschnur

**Das Original-Handbuch 2009 ist verbindlich.** Alles stammt daraus oder aus belegten Quellen der
alten Website (`docs/original/`). Fehlt eine Angabe, wird sie **null** gesetzt und begründet — es
wird **nichts geschätzt**. Eigene Zahlen stehen immer als `VORSCHLAG` mit Ableitung.

**Erhaltene Original-Spielbilder:** drei echte Screenshots aus dem GameStar-Review vom 09.09.2008,
1261×833 Pixel, in `docs/original/karten/`. Sie sind die **einzige verbliebene Quelle** echter
Spielansichten. Auswertung: `docs/audits/astra_gamestar_antwort.txt` (0,47 USD).

**Die Suche nach den Originalbildern ist ABGESCHLOSSEN — nicht wiederholen.** Vier Wege geprüft,
alle negativ für die Spielansichten:

| Weg | Ergebnis |
|---|---|
| Web-Archiv, CDX über `nebelseetal.de` **und alle sechs Unterdomänen** | kennt nur `screens.php`, **keine** der vier Bilddateien; Wildcard-Zeitstempel 2005–2015 → 404, die Unterdomänen haben 0 Bilddateien |
| Web-Archiv, direkte Bildabrufe über vier Zeitstempel × fünf Server × vier Größen | kein Treffer |
| Browserspiel-Portale, archive.today, YouTube, osnanet, Reddit (blockiert) | keine Spielbilder; der Reddit-Thread ließ sich nicht abrufen |
| **Common Crawl** (66 Abfragen, 1 h) | 2009er Index hat die **Seiten** (`screens.php`, `wallpaper.php` — gesichert), aber **keine Bilder**; 2018 nur die geparkte Startseite |

**Was es gibt und wo es liegt:** die GameStar-Screenshots (3), der Wallpaper, die Website-Schaltflächen
und Logos (32 Bilddateien in `docs/original/karten/`), die Common-Crawl-Seitenruinen
(`docs/original/karten/commoncrawl/`), die vier Website-Bilder in `docs/original/assets_website/`.

## 3. Was fertig ist

| Paket | Inhalt | Beleg / Prüfung |
|---|---|---|
| **W0** Sicherheitsnetz | Git, `.gitignore`, Prüfrahmen, `run_tests.bat` | 526 Prüfungen grün |
| **W1a–c** Originaldaten + Icons | Handbuch 2009, 16 Website-Seiten, 15 Seiten von 2005, 45 Icons | `docs/original/`, `data/*.json` |
| **W1d** Einheiten | 28 Originaleinheiten mit Rollen statt 36 erfundene | Paladin ×10 = 1450 |
| **W2** Kampfablauf | `src/kampf.py`: Vorrunde, Mauerschaden, 10 Sequenzen, Flucht, Beute | 42 Prüfungen, Handbuch S. 20–22 |
| **W4a** Rohstoffe | 9 Originalrohstoffe, Start 100/100/10, Siedler = Bevölkerung | 40 Prüfungen |
| **W4b-1** Gelände | 7 Geländearten, Erträge je Geländeart, Sümpfe gesperrt | `src/gelaende.py`, 81 Prüfungen |
| **W4b-2** Siedlungskarte | eigene Karte je Siedlung, **niemals zwei gleiche**; Bauen mit Eignungsanzeige; Abreißen | 33 + 37 Prüfungen, S. 259/283/292/313 |
| **W4b-3** Wirtschaft | Ertrag aus den bebauten Feldern, Summe über Siedlungen, Forschungsfaktor | `src/wirtschaft.py`, 42 Prüfungen |
| **W4b-5** Die 20 Originalgebäude | **jede** Wirkung kommt aus den bebauten Feldern: Haus +5 Siedler, Bibliothek schaltet Forschung frei, Kriegerakademie/Diebesgilde/Stellmacher bilden aus, Verteidigungswall mit 10 Stufen; die fünf erfundenen globalen Gebäude sind entfallen | `src/gebaeude_wirkung.py` + `data/gebaeude_wirkung.json`, 103 Prüfungen |
| **W4c** Forschung | Stufe steigt erst nach Ablauf · Dauer Stufe² Stunden · Kosten verdoppeln · Bibliothek nötig · Abbruch kostet Rohstoffe | `src/forschung.py`, 68 Prüfungen |
| **W5-1** Weltkarte (Modell) | Limbus mit 20 Dimensionen | `src/welt.py` + `data/welten.json`, 42 Prüfungen |
| **WA** Aufträge/Bots (Entwurf) | Auftragsarten, Ablauf, Bot-Regeln, Beute, drei Scheiterfälle | `docs/ENTWURF_AUFTRAEGE.md`, Seite für Seite nachgeprüft |
| **Auskunft** | Reiter „Chat" antwortet aus den Spieldaten — ohne Netz, ohne Schlüssel | `src/berater.py`, 65 Prüfungen |
| **Karten** | 5 Kartentypen mit eigenen Vorteilen; 2 Mustervorlagen | `docs/MUSTERVORLAGEN.md` |
| **Siedlungskarte ist EIGENER ENTWURF, kein Originalbeleg** (astra-Gutachten 04.10.2026, zweimal unabhängig) | Auf **keinem** der drei GameStar-Fotos ist eine Siedlungskarte zu sehen: Foto 1 ist die Nachrichtenansicht, Foto 2 die **Portal**ansicht (das 20×20-Raster gehört dorthin), Foto 3 das Baumenü. Der Entwurf steht deshalb vollständig als VORSCHLAG in `docs/KARTEN_ENTWURF.md`. **Wer die Karte später als „originalgetreu" ausgibt, erfindet etwas.** | `docs/KARTEN_ENTWURF.md` |
| **Zahlenwiderspruch im Kartenmaß** (von astra gefunden, vom Koordinator nachgerechnet) | `data/gelaende.json` nennt spalten 8 × zeilen 5 = **40** Felder, zugleich **56** Felder („40 Bauplätze, Rest Wege/Wasser"). Beides zusammen ist unmöglich. Auflösung als Frage 12 an Daniel: **8 × 7 = 56**, davon 40 bebaubar. | Frage 12 |
| **Tor & Auslieferung** (Schritt 8+9) | **Passworttor** (PBKDF2, Erststart setzt selbst, Wartezeit nach Fehlversuchen) und die **`.exe`** — gebaut mit PyInstaller, Einzeldatei ohne Konsole, Symbol mit 6 Größen; Start aus einem Pfad mit Leerzeichen belegt | `src/tor.py` + 61 Prüfungen, `tools/build_exe.py`, Startlauf 04.10. 22:42 |
| **Sechs neue Module** (Kinder-Arbeit, je eigene Prüfdatei) | W4b-6 `forschung_wirkung` (94) · W3 `werkstatt` (118) · W5-2 `portalraum` (69) · W6 `punkte` (76) · W2b `kampfbericht` (108) | 465 Prüfungen grün |

### Neu gefundene Originalwerte (wichtig!)

**Die Baupreise sind NICHT unbekannt** — sie standen die ganze Zeit in unserem eigenen Code:

| Gebäude | Original (Screenshot 1838857) | Stand im Code |
|---|---|---|
| Holzfäller | 10 Holz, 5 Stein, **1 Siedler** | 10/5/1 Nahrung ✗ |
| Steinmetz | 5 Holz, 10 Stein, 1 Siedler | 5/10/1 Nahrung ✗ |
| Jäger | 25 Holz, 25 Stein, 1 Siedler | 25/25/1 Nahrung ✗ |
| Haus | 80 Holz, 50 Stein | 80/50 ✓ |

Zwei unabhängige Quellen stimmen überein. Der Fehler ist überall derselbe: dritter Posten =
**1 Siedler**, nicht 1 Nahrung. Der daraus abgeleitete Preisentwurf des Modells (8 Holz + 4 Stein)
ist **widerlegt** und in `data/baupreise.json` zu korrigieren.

Weitere belegte Originalregeln (Seiten von 2005):
- **1 Siedler je Stunde**; Siedlergrenze **10 je Siedlung + 5 je Haus** (Handbuch 2009 S. 11 wörtlich;
  die 2005er Fassung nannte 5 — Versionsunterschied). **Seit W4b-5 rechnet das Spiel damit** —
  vorher wuchs die Bevölkerung mit einem erfundenen Wert von 30 Siedlern je Stunde.
- **Bibliothek** nur auf Grasland, Steppe oder Nebelsee, eine je Siedlung — seit W4b-5 als
  Standortregel im Spiel (`data/buildings.json`, Feld `nur_auf`).
- **Ausbildung:** Kriegerakademie → 9 Kampfeinheiten, Diebesgilde → 6 Kundschafter, Stellmacher →
  6 Karren + 7 Belagerungswaffen. Das steht je Einheit in `data/units.json` (Feld `gebaeude`);
  seit W4b-5 bildet das Spiel nur dort aus, wo die Stätte wirklich steht.
- **Verteidigungswall:** 10 Stufen von Erdwall bis Bollwerk; Schwellenwerte der Vorrunde (Stufe 4
  Palisade = 160 Schlagkraft, ab Stufe 5 zusätzlich Belagerungswaffen); Kriegspunkte = Stufe hoch drei.
- Heilkunde: **+10 % Siedlerproduktion je Stufe**
- Weltkoordinaten **(X, Y, Z)**: X/Y im 20×20-Raster der eigenen Dimension, Z = Dimension.
  Andere Dimensionen kosten viel Mana — erst in der eigenen Dimension suchen.
- Koordinatenwechsel: **5.000 Mana aus EINER Siedlung**, höchstens einmal je 24 Stunden
- Portalansicht: **20×20-Raster** über einer Spiralnebelstruktur, eigene Welt **grün**, fremde **rot**
- „Sümpfe sind unbebaubar und somit für Eure Siedlungen völlig wertlos."

### Original-Menü (wörtlich aus dem Screenshot 1838855)

Übersicht · Portal · Diplomatie · Einstellungen · Ruhmeshalle · Gildenhalle · Voraussetzungen ·
Nachrichten · Neuigkeiten · Anleitung · Schlachtsimulator · Forum · Chat · Spieler werben · Logout
Dazu oben die Rohstoffleiste, links „Eure Punkte: Forschung / Krieg / Gesamt", unten „Laufende Aufträge:".

## 4. Die teuer erarbeiteten Modelldaten — WO SIE LIEGEN

**Nichts davon darf verloren gehen.** Alles liegt im Projekt und in Git:

| Ordner | Inhalt | Umfang |
|---|---|---|
| `docs/audits/` | **12 Antworten** der teuren Modelle, unverändert gesichert | 532 KB |
| `docs/audits/eingaben/` | **11 Eingaben** — was den Modellen vorgelegt wurde | 376 KB |

Die wichtigsten Antworten:

| Datei | Was darin steht | Kosten |
|---|---|---|
| `astra_gamestar_antwort.txt` | Analyse der drei Original-Screenshots: Portalansicht (20×20 mit grün/rot), Original-Menü, **Original-Baupreise** | 0,47 USD |
| `astra_audit2_antwort.txt` + `2b` | Konformitätsaudit über alle 24 Handbuchseiten (fand meinen Fehler „10 statt 7 Tage Götterschutz") | ~0,78 USD |
| `astra_wirtschaft_antwort.txt` | Wirtschaftsentwurf (Baupreise, Ausbildungsdauern, Pacing) — Preise **widerlegt**, Rest brauchbar | ~0,8 USD |
| `astra_kampf_antwort.txt` | Kampf-Audit | 0,43 USD |
| `astra_karten_antwort.txt` | Analyse der vier Website-Bilder: **keines zeigt eine Karte** | ~0,3 USD |
| `astra_wallpaper_antwort.txt` | Farbwelt des Originals aus vier Bildern | ~0,2 USD |
| `design_auftraege.txt` | Auftrags- und Bot-System (deepseek-v4-pro) | 0,12 USD |
| `muster_siedlung.txt`, `muster_welt.txt` | die Mustervorlagen | 0,04–0,12 USD |

**Ausgewertet und nutzbar** in: `docs/AUDIT_KONFORMITAET_astra.md`, `docs/ENTWURF_WIRTSCHAFT.md`,
`docs/ENTWURF_AUFTRAEGE.md`, `docs/MUSTERVORLAGEN.md`, `data/gelaende.json` (Farbwelt).

**Regel:** neue Modell-Antworten **immer sofort** aus dem Zwischenspeicher
(`%LOCALAPPDATA%\hermes\cache\scratch`) nach `docs/audits/` kopieren und einchecken — der
Zwischenspeicher wird nach 24 Stunden geleert. Genau so waren am 04.10.2026 zwei Ergebnisse fast
verloren gegangen (die Kartenanalyse und die Siedlungsvorlage).

## 5. Was der Code noch NICHT kann

| fehlt | Folge | Paket |
|---|---|---|
| ~~Kartenerträge an die Rohstoffproduktion angebunden~~ | **erledigt am 04.10.2026 (W4b-4)** — bebaute Felder liefern jetzt wirklich | — |
| ~~Die 20 Originalgebäude wirken nur als Anzeige~~ | **erledigt am 04.10.2026 (W4b-5)** — Haus, Bibliothek, die drei Ausbildungsstätten und der Wall wirken jetzt aus den bebauten Feldern | — |
| ~~Haus und Bibliothek gibt es doppelt (global *und* auf der Karte)~~ | **erledigt mit W4b-5** — die fünf erfundenen globalen Gebäude (Haus, Bibliothek, Kaserne, Wachturm, Portal) sind ersatzlos entfallen; `main.BUILDINGS` ist leer | — |
| ~~Forschung wirkt nur auf Holz, Stein, Nahrung~~ | **erledigt am 04.10.2026 (W4b-6)** — `bonus_system.get_production_multiplier` liefert die belegten Faktoren für **alle neun** Rohstoffe; im Spiel stehen jetzt die **21 Originalforschungen** statt 18 erfundener Gebiete | — |
| **Fertig gebaut, aber noch nicht in der Oberfläche** (Stand 23:20) | die Module sind geprüft grün, aber `main.py` ruft sie noch nicht auf: W3 Waren/Werkstätten, W2b Kampfbericht, W6 Punkte, W5-2 Portalraum, W5 Bot-Kern, **W8 robustes Speichern (95)**, **W7 Menü-Vergleich (64)**. **Das Einhängen ist der nächste Schritt** (Fachschicht + Oberfläche). **Noch nicht gebaut:** WA Aufträge (Kind arbeitet) | Einhängen |
| **Forschung im Spiel steigt SOFORT** (neu entdeckt mit W4b-5) | `src/forschung.py` (Dauer = Stufe² Stunden, Stufe steigt erst nach Ablauf) ist fertig, aber **nicht eingehängt**: `_start_research` zieht die Kosten und erhöht die Stufe im selben Klick. Die Bibliothekspflicht greift jetzt — die Wartezeit fehlt | Einhängen (mit der Fachschicht) |
| **Wallstufen wirken noch nicht im Kampf** | die Schwellenwerte sind abrufbar (`gebaeude_wirkung.wall_schwelle`, `kampfbericht.vorrunde`), aber es gibt noch keinen Angriff aus der Oberfläche | Einhängen |
| 17 Waren als Emoji statt Handwerk | das Werkstatt-Modul rechnet Warteschlangen richtig — es erscheint nur noch nicht im Fenster | Einhängen |
| Auftragssystem nur als Entwurf/Modul | keine Missionen auslösbar | Einhängen |
| Kampf nur als Modul | nicht aus dem Spiel auslösbar | Einhängen |
| Weltkarte nur als Rechenmodell | `src/welt.py` + `src/portalraum.py` (20 Dimensionen) sind fertig, im Fenster steckt aber noch das alte `MAPS`-Modell; keine Portalansicht | Einhängen |
| Oberfläche weicht vom Original ab | das Original-Menü ist belegt und wird gerade gegen unsere Liste gestellt | Einhängen |
| **Götterschutz endet laut Handbuch mit dem ersten Kriegspunkt** (neu entdeckt mit W6) | `src/punkte.py` setzt die **7 Tage** richtig um, lässt den Schutz aber nicht vorzeitig enden, wenn der Spieler Kriegspunkte sammelt. Steht in `punkte.vorschlaege()` — Frage 11 an Daniel | Einhängen |
| **Rundung der Gesamtpunkte offen** (W6) | „Gesamt = halbe Summe" ist belegt, die Rundung bei ungerader Summe nicht: das Modul rundet **ab** (VORSCHLAG) — Frage 10 an Daniel | Einhängen |
| kein Passworttor, keine `.exe` | ~~fehlt~~ **beides da** (04.10.2026): `.exe` mit Tor, Start belegt. Es fehlt nur noch der letzte Neubau nach dem Einhängen der Module | Einhängen + Neubau |

## 6. Nächste Schritte (in dieser Reihenfolge)

1. ~~**W4b-4 — Kartenerträge anbinden**~~ **erledigt am 04.10.2026.** `GameState.stundenertrag()`
   speist Zeitlauf und Anzeige aus `wirtschaft.ertrag_gesamt()`; 21 Prüfungen in
   `tests/test_ertrag_anbindung.py` (Holzfäller auf Wald 4/h, Steppe 2/h, zwei Felder 8/h,
   Bergbau Stufe 2 → 4,8/h). **Zwei Befunde dabei, beide behoben:** (a) das Wirtschaftsmodul liefert
   die Kennungen in Lesefassung („Holz") — der Zeitlauf fand sie nicht und schrieb stillschweigend
   nichts gut; jetzt wird an der Grenze umgeschrieben. (b) die fünf rohstofferzeugenden Gebäude
   (Holzfäller, Steinmetz, Jäger, Schmiede, Markt) sind aus der globalen Liste entfernt — sonst
   hätten beide Systeme denselben Rohstoff erzeugt.
2. ~~**Baupreise korrigieren**~~ **erledigt am 04.10.2026 (Commit `4b84544`).**
3. ~~**W4b-5 — die 20 Originalgebäude samt Wirkungen**~~ **erledigt am 04.10.2026 (Commit `a158175`).**
   Jede Wirkung kommt jetzt aus den bebauten Feldern der Siedlungskarten: Haus +5 Siedler je
   Siedlung, 1 neuer Siedler je Stunde (Heilkunde +10 % je Stufe), Bibliothek schaltet die Forschung
   frei und steht nur auf Grasland/Steppe/Nebelsee, Kriegerakademie/Diebesgilde/Stellmacher bilden
   die passenden Einheiten aus (Stufe = Tempo), der Verteidigungswall trägt 10 Stufen samt
   Schwellenwerten und Kriegspunkten. Ausbauen geht auf der Karte (Wall bis 10, Bibliothek und
   Ausbildungsstätten bis 5 — **Vorschlag**, das Handbuch nennt keine Zahl). Die fünf erfundenen
   globalen Gebäude sind entfallen. **103 Prüfungen** in `tests/test_gebaeude_wirkung.py`,
   Gesamtlauf 630 bei 0 Fehlern und 1 bekanntem Befund. **Drei ehrliche Nebenfund:** der
   erfundene Portal-Bau ist weg (weitere Karten schaltet jetzt die Forschung „Vermessung" frei);
   die `max_je_siedlung`-Regel aus dem Original wird nun durchgesetzt; und beim Nachprüfen fiel auf,
   dass `src/forschung.py` und `src/welt.py` zwar fertig, aber im Spiel **nicht eingehängt** sind.
4. **Einhängen — die Reihenfolge** (Hauptagent, in einer neuen Sitzung): `src/spielschicht.py` ist die
   tkinter-freie Fassade für genau diesen Schritt (133 Prüfungen). Ihre ehrlichen Lücken stehen in
   `spielschicht.offene_luecken()` und sind beim Einhängen zu schließen:
   (a) **Kampfverluste**: `kampf.py` ist in der Fassade nicht eingebunden — `angriff()` nutzt
   `kampfbericht`, aber Einzelverluste je Einheit fehlen;
   (b) **Ausbildungsdauer**: das Handbuch nennt keine, deshalb bildet die Fassade sofort aus;
   (c) **Portal-Mana**: der Zustand führt EINEN Mana-Vorrat, das Original verlangt die 5.000 Mana
   **aus einer Siedlung** — je Siedlung nachziehen;
   (d) **`auftrag_starten` fehlt absichtlich**, weil `src/auftraege.py` beim Bau der Fassade noch
   nicht existierte (Kind WA liefert es nach) — nach dem Einbau dort anschließen.
   Achtung bei den Bots: `botkern.handelspreis()` erwartet den **Referenzpreis** und rechnet nur das
   Temperament (±10 %); der Faktor ×1,2 sitzt in `botkern.referenzpreis_aus_beschaffung()`.
5. ~~**W4b-6 — Produktionsfaktor für alle neun Rohstoffe**~~ **erledigt am 04.10.2026 (Commit `c0f4a5d`).**
   `bonus_system.get_production_multiplier` holt die Faktoren aus `forschung_wirkung`; im Spiel stehen
   jetzt die **21 Originalforschungen**. Offen bleibt nur die belegte Bauregel „Baukunst nötig"
   (dafür müsste die Bibliotheksstufe die Baurechte steuern — eigener kleiner Schritt) und die
   Forschungsvoraussetzungen der Einheiten (z. B. Kriegskunst für den Kämpfer).
6. **W4c-Nachtrag — Forschung mit Wartezeit**: `src/forschung.py` (Dauer = Stufe² Stunden, Stufe
   steigt erst nach Ablauf) in die Oberfläche einhängen; die Fassade `spielschicht` rechnet es schon
   richtig, `main._start_research` steigt aber noch sofort.
7. **W5-2 — Portalansicht einhängen**: `src/portalraum.py` (20 Dimensionen, 5.000 Mana, 24-h-Sperre)
   ersetzt das alte `MAPS`-Modell im Portalreiter.
8. **WA — Auftragssystem**: `src/auftraege.py` ist **noch nicht gebaut** (Kind neu gestartet, nachdem
   der erste Lauf abgebrochen wurde). Nach dem Eintreffen einhängen: Reisezeit, Rückkehr, Beute.
9. **W2b — Kampf ins Spiel**: `src/kampfbericht.py` (Vorrunden-Schwellen, Mauerschaden, Beute,
   Bericht) mit einer Angriffs-Schaltfläche verbinden und den Bericht in die Nachrichten legen.
10. **W3 — Waren im Fenster**: `src/werkstatt.py` in einer Ansicht (Warteschlangen, parallele
    Werkstätten) sichtbar machen.
11. **W8 — robustes Speichern**: `src/speichern.py` + `tests/test_speichern_robust.py` sind **fertig und
    von mir nachgerechnet** (95 grün, 5 ehrliche Befunde: keine Dateisperre gegen zwei Schreiber,
    Klartext, kein Verzeichnis-Sync). Jetzt **in `main.py` einhängen** (statt des direkten Schreibens).
12. **W7 — Oberfläche**: `src/oberflaeche_original.py` + `data/menue_original.json` + Prüfdatei sind
    **fertig und nachgerechnet** (64 grün; einen echten Fehler im Kind-Test selbst gefunden und
    behoben — es suchte das Wort „tkinter" auch in der Beschreibung). Danach die Menüordnung nach der
    belegten Liste nachbauen (Netz-Einträge bleiben draußen).
13. **W9 — Auslieferung**: `.exe` **neu bauen** (`tools/build_exe.py`) und erneut startprüfen.
14. **Karten und Weltdaten sichern**: an jedem Paketende `python tools/protokoll_sichern.py --protokoll`.

## 7. Offene Entscheidungen (Daniel)

**Entschärft:** Baupreise — vier Gebäude sind jetzt belegt (Abschnitt 3). Offen bleibt nur die
Bepreisung der übrigen, deren Menüeintrag wir nicht im Bild haben.

**Neu aus W4b-5 (jeweils mit Vorschlag umgesetzt, damit das Spiel läuft — bitte bestätigen oder ändern):**

- **Ausbaustufen von Bibliothek und Ausbildungsstätten**: das Handbuch belegt, *dass* es Stufen
  gibt, nennt aber keine Zahl. Umgesetzt sind **5 Stufen** (wie die Forschungsstufen) — in
  `data/gebaeude_wirkung.json` änderbar. Der Wall hat die belegten **10**.
- **Höhe des Verteidigungsboni**: der Wall trägt jetzt den Bonus, aber die Zahl (+50 % je Stufe)
  stammt aus `bonus_system` und ist **nicht belegt** (vorher hing sie am erfundenen Wachturm).
- **Ausbildungsdauer**: das Handbuch nennt keine. Sie steht deshalb bei 0,5 Minuten, und die Stufe
  der Stätte verändert bisher nichts Messbares. Ohne Daniels Zahl bleibt das so.
- **Weitere Karten**: schaltet jetzt die Forschung **„Vermessung"** frei (der erfundene
  Portal-Bau ist entfallen). Alternative wäre eine eigene Portalmechanik nach `docs/welt.py`.
- **Siedlergrenze**: 10 je Siedlung + 5 je Haus (belegt); **vor** der ersten Siedlung 10
  (Startwert). So ist der Spielstart bewohnbar — bitte bestätigen.

Weiter offen:

- **Zeitfaktor**: Spieltag = 2 Echtzeitstunden (Vorschlag) — oder näher am Original?
- **Forschungstempo**: Handbuchformeln (Stufe² Stunden; Stufe 10 = 100 Stunden) **mit** Zeitfaktor,
  oder gestauchte Zahlen?
- **Baupreise der übrigen 16 Gebäude**: aus dem Ertrag ableiten oder eigene Regel?
- **Bauzeit**: 3 Minuten je Gebäude mit Warteschlange (Vorschlag)?
- **Bots**: Handelsregel (Referenzpreis ×1,2, Temperament ±10 %) · Angriffstakt (alle 6–24 h) ·
  Beutemenge (50 % der Lager, gedeckelt durch Karrenladung)?
- **Kartenmaß**: 8×5 = 40 Felder ist **Vorschlag** — das Handbuch nennt keine Größe.
- **Sieg-/Niederlagebedingung**: nennt das Handbuch nicht — Vorschlag nötig.
- **Kampfdarstellung**: Bericht in einem Zug oder Schritt für Schritt?

## 8. Arbeitsweise in diesem Projekt (bewährt — beibehalten)

- **Erst prüfen, WAS läuft**, nicht was im Ordner liegt. Genau **eine** ausführbare Fassung im
  Projekt, alte Builds in die Quarantäne.
- **Nie schätzen.** Fehlt ein Wert: `null` + Begründung.
- **Nachprüfen statt glauben.** Jedes Modell- oder Agentenergebnis wird gegen die Quelle gehalten.
  In dieser Sitzung deckte das einen Rechenfehler, einen widerlegten Preisvorschlag und einen
  falschen Weltbezug auf.
- **Schreibvorgänge nachprüfen.** Eine Änderung an `run_tests.bat` meldete Erfolg und kam nie an —
  nur durch `grep` aufgefallen. Immer zurücklesen.
- **Modell-Antworten sofort sichern** (Abschnitt 4) — der Zwischenspeicher räumt nach 24 Stunden auf.
- **Originaldateien unantastbar**: `docs/original/`, die 7 Icon-Blätter, Daniels 17 Dateien.
- **Parallel arbeiten, aber nach Dateien trennen**: jedes Kind bekommt eigene neue Dateien + eigene
  Prüfdatei, bestehende Dateien anzufassen ist verboten. Das Einhängen in `main.py` macht der
  Hauptagent selbst, nacheinander.
- **Agent-zu-Agent Englisch/ASCII**, alles für Daniel **Deutsch**.
- **Erst `deepseek-v4-pro`** für Entwürfe und Analysen (0,04–0,12 USD), `gpt-6-astra` nur für
  **Bilddeutung** (0,47 USD für drei Bilder). Merksatz: ein teures Modell ist ein Rechenschritt,
  kein Arbeiter.
- **Kleine Commits** nach jedem Paket.

## 9. Guthaben (Stand 22:15)

| Konto | Stand | Regel |
|---|---|---|
| OpenAI (astra) | **5,56 USD verfügbar** — 3,33 USD am 04.10. verbraucht (gemessen über `/v1/organization/costs?group_by=line_item`), von Daniel von der Billing-Seite abgelesen; Auto-Recharge aus, keine Schulden möglich | nur noch für Bilddeutung |
| DeepSeek | 3,32 USD (**nicht nachgeprüft** — der Schlüssel liegt nur in Hermes, nicht in der Shell des Agenten) | ein kleiner Rest **muss** bleiben |
| Kosten je Auftrag | v4-pro 0,04–0,12 USD · astra 0,47 USD (3 Bilder). **Größter Posten sind die Cache-Schreibkosten** (3,56 gegen 0,94 USD Ausgabe) → Aufträge kurz halten | `docs/ENTWICKLUNGSPROTOKOLL.md` (Abschnitt Kosten), Skill `kosten-schutzregel` |

**Kosten des Schritts W4b-5 (gemessen, nicht geschätzt):** Tagessumme vor dem Schritt
**8,81 EUR** (9,89 USD), danach **8,87 EUR** (9,96 USD) → **rund 0,06 EUR**
(`tageskosten_check.py --json`, summiert über **alle** Profile; die Differenz enthält jede Nutzung
im selben Zeitfenster). Es wurde **kein** teures Modell eingesetzt: kein `gpt-6-astra` (Bilddeutung
war nicht nötig — alle Angaben stehen in Handbuch und Datendateien) und kein `deepseek-v4-pro`.

**Zur 4-EUR-Regel:** die Tagessumme liegt mit 8,87 EUR über dem normalen Limit von 4 EUR. Für
diesen Auftrag („Nebelseetal Remake so gut wie möglich") hat Daniel die Tagesregel ausgesetzt —
nachzulesen im Skill `kosten-schutzregel` („laufende Ausnahme"). Außerhalb dieses Auftrags gilt die
4-EUR-Regel unverändert.

## 10. Dauerhaftes Arbeitssystem

| Baustein | Wo |
|---|---|
| `docs/PROJEKT_STAND.md` | dieses Dokument — Wiederaufnahme ohne Chatverlauf |
| `docs/AGENTEN_PLAN.md` | **wie die Sitzung ihre Agenten aufteilt und welches Modell wann** — inklusive Auftragsvorlage zum Kopieren |
| `docs/BOARD.md` | **Tagebuch des Koordinators für Daniel** — was die Kinder gemeldet haben. Kein Brett der Kinder (Vorgabe Daniel 04.10.2026) |
| `docs/LEHREN.md` | **ehrliche Nachlese** der Sitzung: 13 Fehler, was gut lief, was dauerhaft gilt |
| `docs/ENTWICKLUNGSPROTOKOLL.md` | **laufendes Protokoll** der groben Arbeitsschritte **mit Kosten** (Daniel schreibt die Entstehung mit) — nach jedem Schritt fortschreiben |
| `docs/ORDNUNG.md` | was wohin gehört |
| `docs/audits/` + `eingaben/` | alle Modelldaten (Abschnitt 4) |
| `tests/` (dreizehn Dateien) + `run_tests.bat` | Wahrheitsquelle „läuft es noch?" — Stand 04.10.2026: **691 Prüfungen, 0 Fehler, 1 Befund** |
| Skills `multi-agent-coding`, `kosten-schutzregel`, `nebelseetal-remake` | Betriebs- und Projektwissen |
| Kanban-Board `nebelseetal` | Paketliste (Verteiler braucht laufendes Gateway) |
| `D:/Arbeiten/_Quarantaene/` | alte Builds (dort: `Nebelsee Memory.exe` mit README) |

## 11. Letzte Commits

| Commit | Inhalt |
|---|---|
| *(neu)* | Kampfsimulator auf das echte Schlachtmodell, EXE neu gebaut (14.108.969 Byte) und startgeprüft |
| `697ab1b` | **W2-Nachtrag: Kampfsimulator** als Trockenkurs über `kampf.fuehre_schlacht`; unbenutzte `bonus_system`-Importe entfernt (Verdrahtungsprüfer ohne Funde) |
| `a1f224a` | **W3 Werkstatt + 17 Originalwaren** eingehängt; Verdrahtungsprüfer und GUI-Fehler-Test aufgenommen (1798/0/15 über 27 Dateien), EXE-Neubau |
| `ff87d75` | **W5-2 Portalraum** eingehängt; astra-Rat gesichert und mit gemessenen Kosten belegt (0,3444 USD) |
| `b14f7f5` | **W6 Punkte + W2/W2b Kampf** eingehängt; zwei Verdrahtungs-Prüfdateien (1734/0/14 über 25 Dateien) |
| `9ec34fb` | **W8 robustes Speichern** eingehängt (Schritt 1 des Umsetzungsplans) |
| `ca6970e` | W4b-5 dokumentiert: Übergabe, Brett und Entwicklungsprotokoll mit Kosten |
| `a158175` | **W4b-5**: die 20 Originalgebäude wirken aus den Siedlungskarten (630 Prüfungen grün) |
| `fb2ec06` | Kosten ins Entwicklungsprotokoll, falsche Kontostände richtiggestellt |
| `26c0149` | Entwicklungsprotokoll eingeführt (Daniel schreibt die Entstehung mit) |
| `472704f` | W4b-4: Kartenerträge liefern wirklich Rohstoffe (526 Prüfungen grün) |
| `4b84544` | Baupreise auf die BELEGTEN Originalwerte korrigiert + Siedler als Baukosten |
| *(neu)* | alle Modelldaten ins Projekt gesichert (23 Dateien, 908 KB) |
| `295301a` | drei neue Module, Mustervorlagen, Original-Screenshots — 488 Prüfungen grün |
| `b75400a` | Auftrags- und Bot-Entwurf, Seite für Seite nachgeprüft |
| `67bec37` | Gesamtlauf um die Prüfdatei der Auskunft erweitert |
| `e1b8d95` | Auskunft im Spiel (Reiter Chat) |
| `9bf3175` | Siedlungsansicht im Fenster: Karte sehen, Feld wählen, bauen, abreißen |
| `bca0392` | Siedlungskarte im Spiel + Ordnung im Projekt |
| `9ee2fac` | Gelände und Siedlungskarten mit fünf Kartentypen |
| `b5f76b2` | Wirtschafts-Entwurf + Weg zur .exe festgelegt |
| `f3e4c4f` | Konformitäts-Audit (astra) über alle 24 Handbuchseiten |
