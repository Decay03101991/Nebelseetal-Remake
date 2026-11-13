# SICHTUNG DER 46 ALTEN PRUEFDATEIEN (F-75)

**Auftrag:** Daniel, 12.11.2026 (F-75, Register 568), woertlich: „ja und pruefe dabei ob sie so wie sie
pruefen noch brauchbar sind oder geaendert werden muessen oder irgendwo sinnvoll integriert werden koennen“.

**Grundlage:** `docs/auftraege/PAKET_15B_PRUEFDATEIEN_20261112.csv` (230 Dateien, 230 Zeilen). Die
**46 Dateien ohne einen einzigen aufgezeichneten Lauf** sind die Liste — das sind genau die blinden
Flecken, die M12.0 und M12 in Sitzung 41 geschlossen haben. Seither schreibt der Sammellauf eine Zeile
je Datei und Lauf; die Sichtung hier ist die inhaltliche Seite dazu.

**Verfahren (nachvollziehbar, ohne Menschenurteil wo es Zahlen gibt):**
- **Pruefungen** = gezaehlte `check(...)`, `self.assert...` und `ok(...)` im Quelltext der Datei.
- **Meldeweg** = benutzt die Datei `harness` (`bericht()`, Messwerte, Befundkanal) oder eine eigene
  Zaehlung mit eigener ERGEBNIS-Zeile.
- **Partner** = eine andere Datei mit **mindestens 80 Prozent gleicher Modulmenge** (`src_module` aus
  Paket 15b, Jaccard) und **mehr** Pruefungen.

**Die drei Urteile und ihre Regel:**

| Urteil | Regel |
|---|---|
| **brauchbar wie sie ist** | eigener Gegenstand, **mindestens 7 Pruefungen**, kein Partner mit mehr Pruefungen. Die Datei darf bleiben, wie sie ist. |
| **muss geaendert werden** | **unter 7 Pruefungen** oder **eigene Pruefzaehlung statt `harness`** — dann fehlen Messwerte und der Befundkanal, und der Lauf weiss weniger als bei den anderen. Inhalt bleibt, Form wird nachgezogen. |
| **sinnvoll integrierbar** | ein Partner deckt den Gegenstand mit **mehr Pruefungen** ab. Vorschlag: Namen fuer Namen uebernehmen, danach streichen — **nur mit Daniels Wort** (F-74). |

**Ergebnis in Zahlen:** 30 brauchbar, 8 sinnvoll integrierbar, 8 muss geaendert werden.
**Es wurde nichts geloescht, nichts umgeschrieben und nichts zusammengelegt.** Diese Datei ist eine
Messung mit Vorschlag, keine Aenderung.

---

## 1. Muss geaendert werden (8)

Diese acht Dateien pruefen mit **eigener Zaehlung** (`check`/`PRUEFUNGEN`/`ERGEBNIS` selbst gebaut)
statt mit `harness`. Sie laufen und sie zaehlen — aber sie schreiben **keine Messwerte**, lesen den
Pruefstand-Kopf nicht und kennen keinen Befundkanal. Genau darum standen sie in der Liste der
46 blinden Flecken.

| Datei | Pruefungen | Module | Was fehlt | Empfehlung |
|---|---|---|---|---|
| `test_gebaeude_menue_und_meldungen` | 47 | einheiten fehlbestand main spieloekonomie | kein `bericht()` — meldet nur eine eigene Zeile | auf `harness` umstellen (Kopf bleibt, `check`/`bericht`/`messwert` uebernehmen) |
| `test_gpt_originalkarten_historische_info` | 0 | originalkarten spieldaten | kein `bericht()` — meldet nur eine eigene Zeile | auf `harness` umstellen (Kopf bleibt, `check`/`bericht`/`messwert` uebernehmen) |
| `test_gpt_originalkarten_katalog` | 27 | originalkarten spieloekonomie | kein `bericht()` — meldet nur eine eigene Zeile | auf `harness` umstellen (Kopf bleibt, `check`/`bericht`/`messwert` uebernehmen) |
| `test_navigation_ebenen` | 6 | main punkte spieloekonomie tor | kein `bericht()` — meldet nur eine eigene Zeile | auf `harness` umstellen (Kopf bleibt, `check`/`bericht`/`messwert` uebernehmen) |
| `test_opus_lauf_arbeitsordner` | 14 | main | kein `bericht()` — meldet nur eine eigene Zeile | auf `harness` umstellen (Kopf bleibt, `check`/`bericht`/`messwert` uebernehmen) |
| `test_projektpfade` | 7 | admin_teststand main stimmen tor | kein `bericht()` — meldet nur eine eigene Zeile | auf `harness` umstellen (Kopf bleibt, `check`/`bericht`/`messwert` uebernehmen) |
| `test_rueckmarsch` | 17 | main | kein `bericht()` — meldet nur eine eigene Zeile | auf `harness` umstellen (Kopf bleibt, `check`/`bericht`/`messwert` uebernehmen) |
| `test_textqualitaet` | 6 | main | kein `bericht()` — meldet nur eine eigene Zeile | auf `harness` umstellen (Kopf bleibt, `check`/`bericht`/`messwert` uebernehmen) |

**KORREKTUR 13.11.2026 (Sitzung 44, Register 594):** Die Spalte *Pruefungen* dieser Tabelle ist ein
**Quelltext-Zaehlung** und lag bei dieser Datei falsch: gezaehlt wurden `check(`, `self.assert...` und
`ok(` — die Zusicherung heisst hier aber **`ck(`**. Der Lauf zeigt **650 Pruefungen, 0 Fehler** (vor und
nach der Umstellung auf `harness` gleich). Die Datei ist also **kein** gruener Lauf ohne Aussage.

**Besonderheit `test_gpt_originalkarten_historische_info`:** gezaehlt **0 Pruefungen** — die Datei ist
76 Zeilen lang, laeuft aber ohne eine einzige Zusicherung durch. Das ist der schlimmste Fall der Liste:
ein gruener Lauf, der nichts behauptet. Sie braucht Pruefungen, nicht nur eine neue Form.

---

## 2. Sinnvoll integrierbar (8)

Jede dieser Dateien hat einen Partner mit **mindestens 80 Prozent gleicher Modulmenge und mehr
Pruefungen**. Der Vorschlag ist immer derselbe: die Pruefnamen der kleinen Datei in die grosse
uebernehmen, danach die kleine streichen — **erst nach Daniels Wort** und erst nach dem
Pruefnamen-Abgleich (`docs/PRUEFNAMEN_ABGLEICH_20261113.md`).

| Datei | Pruefungen | Partner (Pruefungen) | Warum |
|---|---|---|---|
| `test_gpt_admin_hilfe_navigation_fix04e` | 23 | `test_gpt_pflicht_starthilfe_fix04f` (25 P) auf | gleiche Module, kleiner als der Partner |
| `test_gpt_baumenue_standorttipps_fix04b` | 15 | `test_gpt_baumenue_kategorien_fix04` (21 P) auf | gleiche Module, kleiner als der Partner |
| `test_gpt_originalkarten_baukasse` | 20 | `test_gpt_fixrunde_ortslager_zeit_20261028` (24 P) auf | gleiche Module, kleiner als der Partner |
| `test_gpt_prueflauf_ehrlich` | 7 | `test_gpt_fixrunde_ortslager_zeit_20261028` (24 P) auf | gleiche Module, kleiner als der Partner |
| `test_gpt_schild_nebenfenster_fix04i` | 20 | `test_gpt_profile_login` (60 P) auf | gleiche Module, kleiner als der Partner |
| `test_gpt_spielstand_gui_fix04h` | 23 | `test_gpt_spielstandarchiv_fix04g` (48 P) auf | gleiche Module, kleiner als der Partner |
| `test_gpt_wall_gui` | 10 | `test_gpt_wallsystem_eingehaengt` (39 P) auf | gleiche Module, kleiner als der Partner |
| `test_gpt_waren_icons` | 18 | `test_gpt_fixrunde_ortslager_zeit_20261028` (24 P) auf | gleiche Module, kleiner als der Partner |

**Achtung bei `test_gpt_admin_hilfe_navigation_fix04e` und `test_gpt_pflicht_starthilfe_fix04f`:**
beide sind **heute angefasst** worden (Dorfzentrum-Umbau). Sie sind aus dem Dorfzentrum-Umbau
**gruen** hervorgegangen (04e in der Fassung `OK`, 04f `OK`). Ein Zusammenlegen ist damit keine
Aufraeumarbeit mehr, sondern eine Aenderung an zwei frisch geprueften Dateien — das gehoert hinter
F-74, nicht davor.

---

## 3. Brauchbar wie sie ist (30)

| Datei | Pruefungen | Art | Module | Gegenstand (Kopfzeile) |
|---|---|---|---|---|
| `test_gpt_abriss_schutz` | 10 | unittest | admin_teststand main spieloekonomie versorgungsschutz | Externer GPT-Koordinator 28.10.: keine Abriss-Softlocks; Originalbauwe |
| `test_gpt_admin_spielerhilfe_fix04d` | 39 | unittest | admin_oberflaeche admin_teststand admin_werkzeuge main speichern spielerhilfe | FIX04d – Admin überschreibt nur die HilfedARSTELLUNG, nicht Spielregel |
| `test_gpt_baumenue_kategorien_fix04` | 21 | unittest | baumenue_info gelaende main | FIX04: Historisches Baumenue mit echten Rubriken und einer Baukasse. T |
| `test_gpt_bot_angriffsplanung` | 32 | unittest | bot_angriffsplanung botkern einheiten main | GPT-B01: Original-SK/Belagerung und echte Botberichte (externer GPT-Ag |
| `test_gpt_botkarten_nullbedarf` | 11 | unittest | botkern main spieloekonomie | GPT-B03: Bot-Kartenwahl darf bei Null-/Fehlbedarf nicht abstuerzen. |
| `test_gpt_dorfwall` | 28 | unittest | dorfwall main | Eigenstaendiger Regressionstest der externen Wall-Zuarbeit. Aufruf (au |
| `test_gpt_fixrunde_ortslager_zeit_20261028` | 24 | unittest | main | — |
| `test_gpt_frischstart` | 33 | unittest | admin_teststand main spielstaende wirtschaft | GPT extern: neue Partie statt Rettung eines nicht benoetigten Legacy-S |
| `test_gpt_koordinator_regression` | 49 | unittest | auftraege einheiten main spieloekonomie | Externe GPT-Koordinator-Zuarbeit (28.10.2026). Gezielte Integrations-  |
| `test_gpt_originalkarten_feldklick` | 9 | unittest | karten_optik_fein main | Regression: Originalbild bleibt echt, 100 Felder sind einzeln erreichb |
| `test_gpt_pflicht_starthilfe_fix04f` | 25 | unittest | admin_teststand admin_werkzeuge main spielerhilfe spieloekonomie | FIX04f: Starthilfe ist bis Gruendung + tatsaechlicher Grundproduktion  |
| `test_gpt_portable_uebergabe` | 14 | unittest | gelaende main spieldaten tor | GPT-ABS01: Portable Windows-Testkopie / Startpfade / Hermes-Protokoll. |
| `test_gpt_profile_login` | 60 | unittest | admin_teststand main speichern spielstaende tor | GPT-PR01: Grundtor -> Profilwahl -> drei Normal-Slots ODER Admin-Testw |
| `test_gpt_projektordnung_20261028` | 7 | unittest | einheiten gelaende main | Prueft Pfade und die einzige aktive Entwicklungschronik der Konsolidie |
| `test_gpt_rechnerzeit_einheitlich` | 30 | unittest | main speichern zeitbasis | GPT-Z01: monotone echte Laufzeit; Datumsstempel nie als Wirtschaftsuhr |
| `test_gpt_spielerhilfe_goetterschutz_fix04c` | 23 | unittest | main spielerhilfe | FIX04c – Hilfe erscheint nur während echten Schutzes, bleibt aufrufbar |
| `test_gpt_spielstandarchiv_fix04g` | 48 | unittest | admin_teststand main speichern spielstaende spielstand_archiv | FIX04g: private Spielstand-Archive und Verwalten; Testdaten nur in tem |
| `test_gpt_spielzeit_einstellungen_fix05` | 19 | unittest | main spielzeit | FIX05: Benutzer-Tempo bleibt dauerhaft, ohne Source-/EXE-Bundle zu mut |
| `test_gpt_wall_bot_kampf` | 12 | unittest | botkern einheiten main | GPT W-03: Bot-Überfälle rechnen gegen echte Ortswälle statt Gratisbeut |
| `test_gpt_wallsystem_eingehaengt` | 39 | unittest | dorfwall main originalkarten | GPT W-02: echte Integration Ortswall in GameState, Karte, Buchung, Pun |
| `test_gpt_windows_portabilitaet` | 10 | unittest | main spieldaten tor | Tests fuer eigenstaendige Projektkopien und Windows-Ablauf (keine EXE- |
| `test_gpt_wirtschaft_kette_e2e` | 32 | unittest | einheiten gelaende main spieloekonomie | GPT-OEK04: wirtschaftliche Kette auf echten 10x10-Karten. Bau mit echt |
| `test_gpt_zeit_auftragsketten` | 14 | unittest | auftraege einheiten main | GPT-Z03: echter GameState-Transport, Zeitstempel bei grossen Zeitsprue |
| `test_gpt_zeitstempel_und_schutz` | 23 | unittest | main spielzeit zeitbasis | GPT-Z02: Nachrichtentimestamp und Spielzeit sind getrennt, finite vali |
| `test_oekonomie_kern_unabhaengig` | 69 | harness | gelaende spieloekonomie | Eigener Kartengenerator: Kontingente aus der Datei, Positionen per Saa |
| `test_originalkarten_only` | 20 | unittest | gelaende main originalkarten originalkarten_grafik spieloekonomie | Verpflichtende Regression: nur 127 echte 10x10-Originalkarten im aktiv |
| `test_originalkarten_savegames` | 8 | unittest | main originalkarten | Originalkarten: echte GameState-Persistenz und bewusst abgewiesene alt |
| `test_public_edition_fix04j` | 18 | unittest | admin_oberflaeche admin_teststand admin_werkzeuge ausgabemodus main public_start spielstaende tor | Release-Edition Regressionen: public GUI ohne Admin, Daten weiterhin i |
| `test_punkte_einhaengung` | 40 | unittest | forschung main punkte | — |
| `test_weltkarte` | 78 | harness | main welt_optik_fein | Alles, was ein blosser Auswahlklick NICHT veraendern darf. |

**Zwei davon sind Sonderfaelle und stehen bewusst hier, nicht unter „aendern“:**
- `test_oekonomie_kern_unabhaengig` (69 Pruefungen, `harness`) ist im Sammellauf **ausgesetzt**
  (dokumentiert zurueckgezogen, „NICHT MEHR IM SAMMELLAUF“). Brauchbar ja — aber es laeuft nicht mit.
- `test_weltkarte` (78 Pruefungen, `harness`) ist ebenfalls ausgesetzt. Beide stehen in der Liste von
  Register 567 als „2 ausgesetzt“.

---

## 4. Was diese Sichtung NICHT entschieden hat

1. **Nichts wird geloescht.** F-74 verlangt vor jedem Streichen den Pruefnamen-Abgleich mit der
   90-Prozent-Regel; der steht in `docs/PRUEFNAMEN_ABGLEICH_20261113.md` und ergibt fuer die vier
   Kandidaten **keine** Freigabe.
2. **Nichts wird umgeschrieben.** Die acht Dateien mit eigener Zaehlung bleiben unveraendert, bis
   Daniel zustimmt — es sind fremde Zuarbeiten (GPT/Opus), und die Regel „Vorgaengerarbeit nie still
   verwerfen“ gilt.
3. **Die Dauern fehlen noch.** Fuer die 46 Dateien steht in Paket 15b keine Dauer (`dauer_s` leer),
   weil sie nie aufgezeichnet wurden. Mit M12.0 schreibt der Sammellauf sie jetzt; nach der naechsten
   vollen Runde ist die Spalte belegbar.

---

## 5. Fragen an Daniel (Sammelrunde, eine Runde)

- **F-80:** Sollen die acht Dateien mit eigener Zaehlung auf `harness` umgestellt werden? Vorschlag:
  ja, in einem Paket, jede einzeln gruen gefahren, keine Pruefung dabei entfernt.
- **F-81:** Sollen die acht integrierbaren Paare zusammengelegt werden (Name fuer Name uebernehmen,
  danach streichen)? Vorschlag: ja — aber erst nach F-74 und erst nach der naechsten vollen Runde,
  damit die 90-Prozent-Regel an echten Zahlen steht.
- **F-82:** `test_gpt_originalkarten_historische_info` hat 0 Pruefungen. Soll ich sie mit echten
  Zusicherungen fuellen (Gegenstand: historische Karteninfos werden nie als Gratisrohstoffe genutzt)
  oder als ausgesetzt kennzeichnen?
