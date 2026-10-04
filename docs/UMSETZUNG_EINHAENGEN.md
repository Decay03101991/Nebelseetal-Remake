# Nebelseetal Remake — Umsetzung: die fertigen Module in die Oberfläche einhängen

Stand: 05.10.2026. Dieses Dokument ist der **präzise Umsetzungsplan, keine Umsetzung**.

- Keine der zwölf gelesenen Dateien wurde verändert; es wird genau diese eine Datei neu angelegt.
- Gelesen (je einmal, unverändert): `main.py`, `spielschicht.py`, `kampf.py`, `kampfbericht.py`,
  `gebaeude_wirkung.py`, `auftraege.py`, `speichern.py`, `punkte.py`, `werkstatt.py`,
  `portalraum.py`, `botkern.py`, `docs/PROJEKT_STAND.md`.
- Kennzeichnung: `[BELEGT: Datei:Zeile]` = im Code nachgewiesen · `[VORSCHLAG]` = eigener
  Gestaltungsvorschlag · `unklar: …` = Lücke, die Daniel entscheiden muss.
- Es werden keine Tests ausgeführt; Prüfzahlen sind die belegten Zahlen aus `PROJEKT_STAND.md`.

---

## 1. EINHAENGEN

### 1.0 Gemeinsame Voraussetzung — Datenmodell-Abweichung (zentraler Befund)

`[BELEGT: main.py:32-137]` `main.py` führt den Spielstand als **Datenklassen** (`Resource`,
`Building`, `Unit`, `Research`, `Settlement` mit `.amount`/`.count`/`.level`).
`[BELEGT: spielschicht.py:6-8]` Die Fachschicht arbeitet dagegen mit einem **einfachen dict**
(`ressourcen {name:menge}`, `einheiten {name:anzahl}`, `siedlungen [dict]`, `waren`,
`werkstaetten`, `ereignisse`). Alle zehn Kindmodule erwarten diese dict-Form.

Daraus folgt: die Module rechnen mit dict-Ständen, die Oberfläche mit Datenklassen.
`[VORSCHLAG]` Brücke: zwei Adaptermethoden an `GameState` (neu, nach `[BELEGT: main.py:673]` `_log`):

- `_als_dict()` → `{ressourcen, einheiten, siedlungen (asdict), forschungsstaende {name:stufe},
  bevoelkerung, ruf, seit, eigene_dimension, letzter_wechsel, waren, werkstaetten, ereignisse}`.
- `_aus_dict(d)` → zurück nach `self.resources[r].amount`, `self.units[u].count`,
  `self.research[k].level`, `self.population`, `self.ruf`.

`unklar` / von Daniel zu entscheiden: `GameState` besitzt diese Felder derzeit **nicht**:
`seit` (Götterschutz-Start), `eigene_dimension`, `letzter_wechsel` (Portalraum), `waren` und
`werkstaetten` (Werkstatt). Statt Waren gibt es `goods` `[BELEGT: main.py:463]`, statt
Warteschlangen gibt es nichts. `[VORSCHLAG]` diese Felder im `GameState.__init__`
`[BELEGT: main.py:436-463]` ergänzen.

`[VORSCHLAG]` Vorgehen: die Module werden **einzeln direkt aus main.py** aufgerufen (Adapter je
Aufruf), **nicht** über die Fachschicht. Grund: ein vollständiger Umstieg auf
`spielschicht.neuer_zustand()` `[BELEGT: spielschicht.py:153-189]` würde jeden Renderer
(`self.state.resources[r].amount` usw.) neu schreiben und ließe sich nicht „Teilschritt für
Teilschritt grün" halten. Die Fachschicht dient als Referenz für korrekte dict-Formen und bleibt
unverändert (siehe 1.9). Die Module selbst werden **nicht** angefasst — ihre Prüfdateien bleiben
dadurch in jedem Teilschritt grün.

### 1.1 speichern (W8) — atomares Speichern/Laden

- **Import:** `import speichern` ergänzen nach `[BELEGT: main.py:27]`.
- **Funktion `GameState.save`** `[BELEGT: main.py:608-628]`: den direkten Schreibblock
  `with open(path,"w") … json.dump` `[BELEGT: main.py:627-628]` **ersetzen** durch
  `speichern.sichere_kopie(path)` (Sicherung) und `ok, meldung = speichern.speichere(data, path)`
  `[BELEGT: speichern.py:91-140]`; bei `ok=False` Meldung loggen, die alte Datei bleibt stehen.
  Das dict `data` ist bereits vorhanden `[BELEGT: main.py:609-626]`, es ändert sich nur der Schreibweg.
- **Funktion `GameState.load`** `[BELEGT: main.py:630-668]`: `json.load(f)`
  `[BELEGT: main.py:633-634]` **ersetzen** durch `daten, fehler = speichern.lade(path)`
  `[BELEGT: speichern.py:145-159]`; bei `daten is None` `speichern.wiederherstellen(path)` aus
  `.bak` `[BELEGT: speichern.py:191-220]`.
- **Aufrufer** `_save`/`_load` `[BELEGT: main.py:1938-1940 / 1942-1947]` bleiben unverändert
  (sie rufen weiterhin `self.state.save/load`).
- **Anzeige:** Meldung aus `speichere`/`lade` über `self._log` `[BELEGT: main.py:1949-1956]`.
- Vollständige Kette in Abschnitt 4.

### 1.2 punkte (W6) — Punktanzeige auf die Originalformeln

- **Import:** `import punkte` nach `[BELEGT: main.py:27]`.
- **Funktion `_render`** `[BELEGT: main.py:2009-2020]`: die Zeilen
  `lbl_forschung = score`, `lbl_krieg = ruf`, `lbl_gesamt = score+ruf+total_units`
  `[BELEGT: main.py:2018-2020]` **ersetzen** durch `punkte.forschungspunkte(staende)`
  `[BELEGT: punkte.py:78]`, `punkte.kriegspunkte(einheiten, wall)` `[BELEGT: punkte.py:94]`,
  `punkte.gesamtpunkte(staende, einheiten, wall)` `[BELEGT: punkte.py:111]`, mit
  `wall = gebaeude_wirkung.wall_stufe(settlements)` `[BELEGT: gebaeude_wirkung.py:237]`.
- **Funktion `_render_hall_of_fame`** `[BELEGT: main.py:1688-1697]`: dieselben Formeln statt
  `score`/`ruf`/`combat` (dort steht heute eine falsche Gesamtsumme).
- **Anzeige Götterschutz:** `punkte.goetterschutz_aktiv(seit, jetzt)` `[BELEGT: punkte.py:191]`
  benötigt das noch fehlende Feld `seit` (siehe 1.0, `unklar`).
- **Sieg/Niederlage:** `punkte.sieg_oder_niederlage(...)` `[BELEGT: punkte.py:213]` als
  `[VORSCHLAG]`-Anzeige (das Handbuch nennt keine Bedingung `[BELEGT: punkte.py:216-218]`).

### 1.3 kampfbericht + kampf (W2b + W2) — Kampf aus dem Spiel

- **Import:** `import kampf`, `import kampfbericht` nach `[BELEGT: main.py:27]`.
- **Ersetzen** der beiden bisherigen Angriffe `_attack_map` `[BELEGT: main.py:1501-1519]` und
  `_attack` `[BELEGT: main.py:1642-1664]` durch **eine** gemeinsame Funktion
  `_angriff_durchfuehren(ziel)`; sie ruft `kampf.fuehre_schlacht(...)` `[BELEGT: kampf.py:207]`
  und `kampfbericht.spieldaten_anwenden` `[BELEGT: kampfbericht.py:298]` bzw.
  `kampfbericht.bericht` `[BELEGT: kampfbericht.py:252]`.
- Vollständiger Ablauf mit allen Fehlerfällen in Abschnitt 2.

### 1.4 gebaeude_wirkung (W4b) — bereits eingehängt

`[BELEGT: main.py:24]` `import gebaeude_wirkung` ist vorhanden und wird genutzt
(Bevölkerungsgrenze `[BELEGT: main.py:595]`, Wall-Beschreibung `[BELEGT: main.py:1020]`,
Forschungs-/Ausbildungsvoraussetzung `[BELEGT: main.py:1845, 1894]`). **Neues Einbinden ist nur
für die Kampf-Vorrunde** (`wall_stufe`/`wall_schwelle` `[BELEGT: gebaeude_wirkung.py:237/264]`)
**und für die Punkte** (Wallstufe) nötig — kein neuer Import.

### 1.5 werkstatt (W3) — Warenfertigung

- **Import:** `import werkstatt` nach `[BELEGT: main.py:27]`.
- **Zustand:** `GameState` hat `goods` `[BELEGT: main.py:463]`, aber kein Warenlager der
  17 Originalwaren und keine Warteschlangen. `[VORSCHLAG]` Felder `waren` und `werkstaetten`
  ergänzen (siehe 1.0, `unklar`).
- **Anzeige:** in `_render_storage` `[BELEGT: main.py:1348-1384]` die erfundene `GOODS`-Liste
  `[BELEGT: main.py:88-106]` durch `werkstatt.waren_der_werkstatt(typ)` `[BELEGT: werkstatt.py:103]`
  ersetzen und eine Fertigungs-Schaltfläche anbinden (`werkstatt.einreihen`
  `[BELEGT: werkstatt.py:194]`).
- **Ablauf:** `werkstatt.fortschritt` / `werkstatt.fertige_waren`
  `[BELEGT: werkstatt.py:268/337]` im Zeitlauf `_tick_loop` `[BELEGT: main.py:1958]` bzw.
  `GameState.tick` `[BELEGT: main.py:576]` aufrufen; fertige Waren nach `waren` buchen
  (Muster: `[BELEGT: spielschicht.py:258-264]`).

### 1.6 portalraum (W5-2) — Portalansicht

- **Import:** `import portalraum` nach `[BELEGT: main.py:27]`.
- **Funktion `_render_portal`** `[BELEGT: main.py:1333-1343]`: die alte Anzeige
  (freigeschaltete `MAPS` + Bots) **ersetzen** durch `portalraum.anzeige_raster(z, radius,
  eigene_dimensionen)` `[BELEGT: portalraum.py:175]` (20×20-Raster, eigene grün / fremde rot
  `[BELEGT: portalraum.py:164-172]`) und einen Knopf „Koordinatenwechsel" über
  `portalraum.wechsel_erlaubt` / `nach_wechsel` `[BELEGT: portalraum.py:119/147]`.
- **Zustand:** braucht `eigene_dimension` und `letzter_wechsel` (siehe 1.0, `unklar`).
  Das alte `MAPS`-Modell `[BELEGT: main.py:347-353]` bleibt für die Weltkarte (`_render_maps`
  `[BELEGT: main.py:1397]`) bestehen; nur der Portalreiter wird ersetzt — `[VORSCHLAG]`, da die
  Weltkarte laut `[BELEGT: PROJEKT_STAND.md:203]` ebenfalls noch das alte Modell ist.

### 1.7 auftraege (WA) — Aufträge/Missionen

- **Import:** `import auftraege` nach `[BELEGT: main.py:27]`.
- **Zustand:** eine Auftragsliste ergänzen (`auftraege.neue_liste()` `[BELEGT: auftraege.py:193]`).
- **Aufruf:** `auftraege.starten(liste, art, einheiten, von, nach, entfernung, jetzt, fracht)`
  `[BELEGT: auftraege.py:220]`; **Anzeige** über den vorhandenen Knopf „Transport"
  `[BELEGT: main.py:1003]` und eine neue Auftragsliste im Fenster.
- **Ablauf** im `_tick_loop` `[BELEGT: main.py:1958]`: `auftraege.fortschritt`
  `[BELEGT: auftraege.py:360]`, `auftraege.angekommen` `[BELEGT: auftraege.py:391]`,
  `auftraege.spieldaten_anwenden` `[BELEGT: auftraege.py:450]`; Berichte über
  `auftraege.bericht` `[BELEGT: auftraege.py:420]` in den Reiter „Nachrichten".
- Hinweis: `[BELEGT: spielschicht.py:645-646]` die Fachschicht lässt `auftrag_starten` absichtlich
  weg, weil `auftraege.py` beim Bau der Fassade noch fehlte.

### 1.8 botkern (W5) — Bot-Verhalten

- **Import:** `import botkern` nach `[BELEGT: main.py:27]`.
- **Ersetzen** der ad-hoc-Botlogik: `generate_map` erzeugt Bots `[BELEGT: main.py:542-555]`,
  `_trade`/`_attack` `[BELEGT: main.py:1629-1664]` rechnen mit alter Kampfstärke.
- `[VORSCHLAG]` Bots auf dict-Form bringen (`botkern.neue_bots` `[BELEGT: botkern.py:114]`) und
  im Zeitlauf `botkern.bots_tick` / `wirkung_anwenden` `[BELEGT: botkern.py:418/390]` rufen.
  `botkern.handelspreis` `[BELEGT: botkern.py:212]` erwartet den **Referenzpreis**; der Faktor
  ×1,2 steckt in `botkern.referenzpreis_aus_beschaffung` `[BELEGT: botkern.py:207]`
  (Hinweis auch `[BELEGT: PROJEKT_STAND.md:242-243]`).
- `unklar:` die `BotPlayer`-Felder (`army`, `settlements`, `noob_protection`)
  `[BELEGT: main.py:108-118]` haben kein Gegenstück im botkern-dict — Migrations-/Adapter-
  Entscheidung offen.

### 1.9 spielschicht (Fachschicht)

`[BELEGT: PROJEKT_STAND.md:232-233]` `spielschicht.py` ist als tkinter-freie Fassade für genau
diesen Schritt gedacht (133 Prüfungen). `[VORSCHLAG]` in dieser Runde **nicht** als alleinige
Zustandsebene einführen (Datenmodell weicht ab, siehe 1.0); stattdessen als Referenz für korrekte
dict-Formen nutzen und die direkten Modul-Aufrufe (1.1–1.8) daran angleichen. Ein vollständiger
Fassaden-Umstieg ist ein eigener späterer Schritt; die dabei zu schließenden Lücken nennt
`[BELEGT: PROJEKT_STAND.md:240-241]` (Kampfverluste, Ausbildungsdauer, Portal-Mana je Siedlung).

---

## 2. KAMPFABLAUF — vom Klick bis zum Bericht im Reiter „Nachrichten"

### 2.1 Ablauf Schritt für Schritt

1. **Zielauswahl.** Der Spieler klickt „Angreifen" (bisher `_attack` `[BELEGT: main.py:1642]`
   bzw. `_attack_map` `[BELEGT: main.py:1501]`). `[VORSCHLAG]` Das Ziel wird als dict beschrieben:
   `wall_stufe` (aus `gebaeude_wirkung.wall_stufe` des Verteidigers `[BELEGT: gebaeude_wirkung.py:237]`),
   `wall_zustand_prozent`, `vorraete` (Lager des Verteidigers), `verteidiger` (Einheiten-dict).
   `unklar:` woher die Verteidiger-Einheiten einer fremden Siedlung stammen — botkern führt keine
   Verteidiger-Armee je Siedlung.

2. **Truppenprüfung (zu wenig Truppen).** Vor dem Kampf wird geprüft, ob der Angreifer Kampf-/
   Kundschafter- oder Belagerungseinheiten besitzt. Ohne Schlagkraft wird abgelehnt (Meldung unten).

3. **Vorrunde (Wallschwellen aus gebaeude_wirkung).** `wall_stufe` kommt aus
   `gebaeude_wirkung.wall_stufe(...)`; die Schwellen liefert `gebaeude_wirkung.wall_schwelle(stufe)`
   `[BELEGT: gebaeude_wirkung.py:264-272]`. Geprüft wird sie von `kampfbericht.vorrunde`
   `[BELEGT: kampfbericht.py:74]` und — intern — erneut von `kampf.fuehre_schlacht` (dort über
   `spieldaten.wallstufen()` `[BELEGT: kampf.py:227]`). Schlagkraft der Fusstruppen
   (Nahkampf **und** Fernkampf `[BELEGT: kampf.py:40]`) und der Belagerungswaffen gegen die durch
   den Mauerzustand prozentual verringerte Schwelle `[BELEGT: kampf.py:245-268]`. Nicht bestanden
   → Rückzug, unentschieden `[BELEGT: kampf.py:253-265]`.

4. **Eigentlicher Kampf (src/kampf.py).**
   `kampf.fuehre_schlacht(angreifer, verteidiger, wall_stufe, wall_zustand, angreifer_karren,
   verteidiger_karren, vorraete, rng)` `[BELEGT: kampf.py:207-214]`. Ablauf: Mauerschaden je
   Belagerungswaffe `[BELEGT: kampf.py:270-284]`, dann bis zu 10 Kampfsequenzen (Fernkampf
   gleichzeitig, Nahkampf nur der Angreifer) `[BELEGT: kampf.py:286-333]`; die Schlacht endet,
   sobald eine Armee keine Nahkämpfer mehr hat `[BELEGT: kampf.py:291-293]`.

5. **Beute (Karrenladung).** Nur bei Angreifersieg und nur mit Transportkarren; Kapazität =
   Summe der Karrenladungen `[BELEGT: kampf.py:357-373]`. Die Beute ist hart auf die Karrenladung
   gedeckelt (anteilig nach Vorratsmenge) `[BELEGT: kampfbericht.py:202-242]`.

6. **Bericht (kampfbericht.bericht).** `kampfbericht.bericht(ergebnis)` liefert
   `{'titel', 'zeilen', 'typ': 'kampf'}` `[BELEGT: kampfbericht.py:252-293]`. `[VORSCHLAG]`
   `titel` + `zeilen` in `state.messages` anhängen; `_render_messages` `[BELEGT: main.py:1740-1744]`
   zeigt heute nur `msg['text']` — für mehrzeilige Berichte je `zeilen`-Eintrag eine eigene
   `text`-Zeile anhängen (oder `msg['text'] = "\n".join(zeilen)`).

7. **Punkte/Verluste.** `kampfbericht.spieldaten_anwenden(zustand, ergebnis)` bucht Beute zu
   `ressourcen`, zieht `verluste_angreifer` + `geraete_verloren` von `einheiten` ab und setzt
   `wall_zustand_prozent` `[BELEGT: kampfbericht.py:298-334]`. Danach wird
   `punkte.kriegspunkte(einheiten, wall)` neu berechnet `[BELEGT: punkte.py:94]`.

### 2.2 Fehlerfälle und die jeweils richtige Meldung

- **Zu wenig Truppen:**
  `„Keine Kaempfer und keine Belagerungswaffen vorhanden."` `[BELEGT: spielschicht.py:525-526]`;
  beim Auftragsstart: `„Ohne Schlagkraft kann die Vorrunde gegen den Wall nicht bestanden werden -
  der Angriff wird abgelehnt."` `[BELEGT: auftraege.py:277-279]`.

- **Wall zu hoch (Fusstruppen-Schwelle nicht erreicht):**
  `„Die Schlagkraft der Fusstruppen … erreicht die Schwelle … nicht - Rueckzug, keine Beute."`
  `[BELEGT: kampfbericht.py:136-137]`; kampf-intern:
  `„Schwelle nicht erreicht — die Truppen ziehen sich zurueck, die Schlacht gilt als unentschieden."`
  `[BELEGT: kampf.py:254-255]`.

- **Wall zu hoch (Belagerungswaffen reichen ab Stufe 5 nicht):**
  `„Fusstruppen erreichen die Schwelle …, aber die Schlagkraft der Belagerungswaffen … erreicht
  … nicht - Rueckzug, keine Beute."` `[BELEGT: kampfbericht.py:140-142]`; kampf-intern:
  `„Belagerungswaffen reichen nicht — Rueckzug, unentschieden."` `[BELEGT: kampf.py:263]`.

- **Kein Wall:**
  `„Kein Wall vorhanden - die Vorrunde entfaellt, der Angreifer kann vorruecken."`
  `[BELEGT: kampfbericht.py:113-115]`; kampf-intern:
  `„Kein Wall vorhanden — keine Vorrunde noetig."` `[BELEGT: kampf.py:243]`.

- **Beute größer als Ladung:** das ist **kein Fehler** — die Beute wird still auf die
  Karrenladung gedeckelt (anteilig) `[BELEGT: kampfbericht.py:202-242, kampf.py:357-373]`. Ein
  echter „Überladen"-Fehler existiert nur beim **Transport**:
  `„Ueberladen: X Einheiten Fracht passen nicht auf Y Ladeplaetze."` `[BELEGT: auftraege.py:214-216]`.

- **Rückkehr der Truppen:** Gefallene zählen als Verlust, **Geflohene kehren zurück und zählen
  nicht** `[BELEGT: kampf.py:77, 181-189]`; nur `verluste_angreifer` wird abgezogen
  `[BELEGT: kampfbericht.py:323-329]`. Im Auftragsmodell dauert die Rückkehr so lange wie die
  Hinreise (Faktor 2) `[BELEGT: auftraege.py:54-55, 296-297]`; überlebende Truppen kehren damit
  automatisch heim.

---

## 3. KARTENANSICHT — bebaute Felder, Ausbaustufen, Auswahl

Die Siedlungskarte ist bereits eingebaut und nutzt die vorhandenen Funktionen; hier ist **nichts
Neues einzuhängen**, nur zu verifizieren.

- **Öffnen:** `_oeffne_siedlungskarte(siedlung)` `[BELEGT: main.py:1108-1111]` setzt
  `self.karten_siedlung` und wechselt zur Ansicht „Siedlungskarte" (Eintrag in `mapping`
  `[BELEGT: main.py:955]`); erreichbar über den Knopf „Karte öffnen" `[BELEGT: main.py:996]`.
- **Bebaute Felder:** `_render_settlement_map` `[BELEGT: main.py:1216-1331]` baut je Feld einen
  `tk.Button`; die Beschriftung ist der Gebäudename (gekürzt), wenn das Feld bebaut ist, sonst der
  Feldindex `[BELEGT: main.py:1253-1259]`; „bebaut" = `siedlung.bauten.get(str(i))`.
- **Ausbaustufen:** `gebaeude_wirkung.stufe_von_feld(siedlung, feld)` `[BELEGT: gebaeude_wirkung.py:100-106]`;
  Anzeigename über `stufen_name` `[BELEGT: gebaeude_wirkung.py:131-135]`, Obergrenze über
  `max_stufe` `[BELEGT: gebaeude_wirkung.py:121-128]`. Das Infofeld zeigt bei bebautem Feld
  `„Hier steht: … — {stufen_name} ({warum})"` `[BELEGT: main.py:1291-1294]` und einen Knopf
  „Ausbauen auf Stufe n" `[BELEGT: main.py:1306-1309]`.
- **Auswahl:** `_karten_feld_waehlen(feld)` `[BELEGT: main.py:1113-1115]` setzt `self.karten_feld`;
  das gewählte Feld wird gelb umrandet `[BELEGT: main.py:1261-1262]`.
- **Ausbau speichern:** `_karten_ausbauen` `[BELEGT: main.py:1163-1204]` schreibt
  `siedlung.stufen[str(feld)] = stufe+1` `[BELEGT: main.py:1201]`.
- **Abreißen:** `_karten_abreissen` `[BELEGT: main.py:1150-1161]` entfernt `bauten` und `stufen`
  des Felds (keine Erstattung, belegte Originalregel).
- Hinweis zur Schlüsselform: Ausbaustufen liegen keyed nach `str(feld)` in `bauten` **und**
  `stufen` `[BELEGT: main.py:204-205]`; `stufe_von_feld` liest `str(feld)`
  `[BELEGT: gebaeude_wirkung.py:104]`.

---

## 4. SPEICHERN/LADEN — Umstellung auf src/speichern.py

### 4.1 Wo heute direkt geschrieben wird

`[BELEGT: main.py:627-628]` in `GameState.save` steht heute der direkte Schreibvorgang:
`with open(path, "w", encoding="utf-8") as f: json.dump(data, f, indent=2, ensure_ascii=False)`.
Das dict `data` wird zuvor in den Zeilen `[BELEGT: main.py:609-626]` zusammengestellt — dieser
Teil bleibt. Das direkte **Lesen** steht in `GameState.load` `[BELEGT: main.py:633-634]`
(`with open(path, "r") … json.load(f)`). Der Speicherort `save_path` wird in `__init__` gesetzt
`[BELEGT: main.py:687-690]` (in der EXE im Nutzerordner, sonst neben dem Quelltext). Gespeichert
wird nur manuell über den Knopf „Speichern" → `_save` `[BELEGT: main.py:867, 1938-1940]`.

### 4.2 Umstellung (atomar, Sicherung, Wiederherstellung)

- **Speichern:** statt `json.dump` rufen:
  1. `speichern.sichere_kopie(path)` legt `<pfad>.bak` **vor** dem Überschreiben an und prüft sie
     durch Zurücklesen `[BELEGT: speichern.py:164-188]`;
  2. `speichern.speichere(data, path)` schreibt nach `<pfad>.tmp` (flush + `os.fsync`), liest die
     Zwischendatei zurück und vergleicht, setzt dann mit `os.replace` atomar um und liest den
     Endpfad nochmals `[BELEGT: speichern.py:91-140]`. Bei jedem Fehler bleibt die alte Datei
     unangetastet; es gibt entweder den alten oder den neuen Stand, nie einen halben
     `[BELEGT: speichern.py:4-17]`.
- **Laden:** `speichern.lade(path)` `[BELEGT: speichern.py:145-159]`; bei `(None, fehler)`
  `speichern.wiederherstellen(path)` aus `<pfad>.bak` `[BELEGT: speichern.py:191-220]` — die
  Wiederherstellung schreibt selbst wieder atomar über eine geprüfte `.tmp`.
- **Aufräumen:** `speichern.aufraeumen(path)` entfernt liegengebliebene `.tmp`-Dateien
  `[BELEGT: speichern.py:268-290]`. `[VORSCHLAG]` einmal beim Start (`main()`
  `[BELEGT: main.py:2059]`, vor dem Fensteraufbau `[BELEGT: main.py:2072]`) rufen.
- **Ehrliche Grenzen** (im Bericht mitführen): kein fsync auf das Verzeichnis, `os.replace` nur
  innerhalb eines Dateisystems atomar, keine Dateisperre gegen zwei Schreiber, Klartext, keine
  Prüfsumme der Rohbytes `[BELEGT: speichern.py:295-319]`.

---

## 5. ARBEITSREIHENFOLGE

Leitregel: nach **jedem** Teilschritt bleiben die Prüfungen grün, weil (a) die Module selbst nicht
angefasst werden und (b) die `main.py`-Änderungen nur GUI-/Anzeigepfade ersetzen oder ergänzen.
Die neue Gesamtzahl von `run_tests.bat` ist erst bestimmbar, wenn die neuen Prüfdateien dort
aufgenommen sind (siehe Schritt 11).

1. **speichern einhängen** (GameState.save/load → `speichern.speichere/lade/sichere_kopie`,
   Abschnitt 4). Prüfen: `tests/test_speichern_robust.py` → **95 grün** `[BELEGT: PROJEKT_STAND.md:261]`;
   zusätzlich `run_tests.bat` → **1157 grün** (Baseline bleibt) `[BELEGT: PROJEKT_STAND.md:59]`.

2. **punkte einhängen** (Punktanzeige, Abschnitt 1.2). Prüfen: `tests/test_punkte.py` → **76 grün**
   `[BELEGT: PROJEKT_STAND.md:63]`; `run_tests.bat` 1157 grün.

3. **Kampf einhängen** (kampf + kampfbericht, Abschnitt 1.3 und 2). Prüfen:
   `tests/test_kampf.py` → **42 grün** `[BELEGT: PROJEKT_STAND.md:60]`,
   `tests/test_kampfbericht.py` → **108 grün** `[BELEGT: PROJEKT_STAND.md:63]`; `run_tests.bat` grün.

4. **Kartenansicht verifizieren** (keine Änderung nötig, Abschnitt 3). Prüfen:
   `tests/test_kartenansicht.py` → **40 grün** `[BELEGT: PROJEKT_STAND.md:60]` — braucht einen
   angemeldeten Windows-Desktop `[BELEGT: PROJEKT_STAND.md:72-73]`.

5. **werkstatt einhängen** (Warenfertigung, Abschnitt 1.5). Prüfen: `tests/test_werkstatt.py` →
   **118 grün** `[BELEGT: PROJEKT_STAND.md:63]`.

6. **portalraum einhängen** (Portalansicht, Abschnitt 1.6). Prüfen: `tests/test_portalraum.py` →
   **69 grün** `[BELEGT: PROJEKT_STAND.md:63]`.

7. **auftraege einhängen** (Missionen, Abschnitt 1.7). Prüfen: `unklar` — keine Prüfzahl in
   `PROJEKT_STAND.md` aufgeführt (das Modul ist nach dem Stand der Übergabe vom 04.10. entstanden).

8. **botkern einhängen** (Bot-Verhalten, Abschnitt 1.8). Prüfen: `unklar` — keine Prüfzahl in
   `PROJEKT_STAND.md` aufgeführt (Modulstand 05.10., nach der Übergabe).

9. **spielschicht-Fassade** (optional, später, Abschnitt 1.9). Prüfen: `tests/test_spielschicht.py`
   → **133 grün** `[BELEGT: PROJEKT_STAND.md:233]`.

10. **Neubau der .exe:** `tools/build_exe.py` `[BELEGT: PROJEKT_STAND.md:117]` und erneuter
    Startlauf (Passworttor + Spiel) `[BELEGT: PROJEKT_STAND.md:117]`. `[VORSCHLAG]` unmittelbar
    davor `run_tests.bat` vollständig grün fahren.

11. `[VORSCHLAG]` die neuen Prüfdateien (speichern 95, spielschicht 133, auftraege `unklar`,
    botkern `unklar`) in `run_tests.bat` aufnehmen. Die daraus folgende neue Gesamtzahl ist
    `unklar`, bis die auftraege-/botkern-Prüfzahlen vorliegen; die heute belegten **18 Dateien**
    ergeben zusammen **1157** `[BELEGT: PROJEKT_STAND.md:59-63]`.

---

## 6. NACHTRAG DES KOORDINATORS (05.10.2026, 00:05) — die „unklar"-Stellen sind beantwortet

Der Plan wurde geschrieben, **eine Minute bevor** die Übergabe aktualisiert wurde. Die drei offenen
Punkte sind inzwischen gemessen (nicht geschätzt):

| im Plan „unklar" | Antwort (gemessen) |
|---|---|
| Prüfzahl `auftraege` | **111 bestanden, 0 Fehler, 1 Befund** (`tests/test_auftraege.py`, Lauf des Koordinators) |
| Prüfzahl `botkern` | **90 bestanden, 0 Fehler, 0 Befunde** |
| Gesamtzahl `run_tests.bat` | **1651 bestanden, 0 Fehler, 9 Befunde über 23 Dateien**, Rückgabewert 0 |
| `speichern` / `spielschicht` | **95** / **133** grün — die neuen Prüfdateien sind **schon** in `run_tests.bat` aufgenommen |

**Zusätzlich bestätigt:** `[BELEGT: main.py:627-628]` ist der direkte Schreibort für den Spielstand —
genau dort setzt Schritt 1 (speichern) an. Die Kartenansicht braucht nach dem Plan **keinen** Umbau.

**Ebenfalls bestätigt (Koordinator):** `data/gelaende.json` widerspricht sich (8 × 5 = 40 Felder *und*
56 Felder) — der Plan geht davon aus; die Auflösung ist Frage 12 an Daniel.

