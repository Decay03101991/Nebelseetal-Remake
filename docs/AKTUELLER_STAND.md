# STAND 02.11.2026, 08:59 - Gebaeude-Optik haengt in der Oberflaeche (Register 124)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `0bf5d31`; dieser Commit bringt Einbau, Pruefdatei und Register 124 | `git log --oneline -1` |
| Eingebaut | Icons in der Menueleiste (20 px, `compound=tk.LEFT`), Icons an JEDEM Bauknopf der Kartenauswahl (28 px), Hintergrund 538 x 222 in Dorfzentrum, Forschung, Kaserne, Stellmacher, Diebesgilde | `tests/test_gebaeude_icons.py` |
| Zuordnung Menue -> Gebaeude | `main.MENU_GEBAEUDE` ABGELEITET: `gelaende.finde_gebaeude` (Dorfzentrum -> `lager`) + `MENUE_BEDINGUNG` (Kaserne -> `kriegerakademie`, Forschung -> `bibliothek`); Weltpunkte ohne Bild | `grep -n "MENU_GEBAEUDE" src/main.py` |
| Neue Pruefdatei | **54 von 54 gruen, 0 Fehler, 0 Befunde** | eigener Lauf |
| Gegenprobe | mit abgeschaltetem Menue-Icon **4 Fehler** (Datei wird rot), Datei-Hash danach wieder gleich | eigener Lauf, Protokoll 08:51 |
| Sammellauf | **120 von 122 gruen, 0 rot, 2 ausgesetzt, 4.759 Pruefungen, 424 s** (08:52-08:59) | `docs/audits/sammellauf_20261102_0852.log` |
| Register / Pruefdateien | **124 Punkte**, **122 Pruefdateien** | `grep -cE`, `ls tests/test_*.py \| wc -l` |
| Guthaben | letzte Ablesung **8,50 USD** Kontostand, **41,49 USD** Gesamtverbrauch (Daniel, 08:09) - seither nur dieser eine Schritt | Register 117, Uebergabe 08:09 |
| EXE im Projektordner | **01.11.2026, 19:01** - enthaelt keinen der Commits ab `6585cd2` | `ls -la`, `git log -1` |
| Abnahme offen | das Aussehen im Fenster hat Daniel noch NICHT gesehen (Icons, Bauknoepfe, Hintergrund) | eigene Messung |

## Der EINE naechste Schritt

**Die Kaserne-Ansicht darf ohne Gebaeude am aktiven Ort nicht abstuerzen** - der Fehler ist aelter als
dieser Schritt und beim Bau der Pruefdatei aufgefallen: `_siedler_warnung_zeichnen`
(`src/main.py`, Aufruf in `_render_ausbildung`) liest `reserve["guenstigste"]`, und
`spieloekonomie.siedler_reserve` liefert diesen Schluessel NICHT, wenn am aktiven Ort kein Gebaeude
steht (Fruehfall: `if not bedarf: return {...}` ohne `guenstigste`). Nachgestellt: Siedlung mit
Kriegerakademie anlegen, aktive Siedlung ohne Gebaeude, Menuepunkt "Kaserne" oeffnen -> `KeyError`.
Zu tun: EINE Stelle lesen (`reserve.get("guenstigste", ("", 0))` im Anzeigecode ODER den Fruehfall in
`siedler_reserve` vollstaendig zurueckgeben - die Rueckgabe ist im Docstring beschrieben, also gehoert
der Schluessel in die Funktion), Wache in `tests/test_gebaeude_icons.py` oder eigener Datei
(Siedlung ohne Gebaeude -> Ansicht rendert), voller Sammellauf, ein Commit.
Arbeitsweise: Pruefdatei ergaenzen, voller Sammellauf, Protokollzeile, ein Commit.

## Reihenfolge danach

1. Icons und Hintergrund im Fenster abnehmen (Daniel) - rechnerisch und in der Pruefdatei belegt,
   im laufenden Spiel noch nicht gesehen.
2. Auswahlrahmen der C2-Lieferung zeichnen (der goldene Rahmen aus `karten_optik_fein` liegt derzeit
   oben); die acht Einzelsymbole aus `assets/icons/leiste/symbole/` sind weiter ungenutzt.
3. Bei sehr breiten Fenstern wiederholt sich die Landschaft in den gedehnten Leistenluecken sichtbar.
4. Wappen den fuenf Bots zuordnen; Burgen zu Weltkarten nur als gekennzeichneter Vorschlag.
5. S-8 Bilanz (500 Mana + 100 Gold, Register 93), danach `weltkarten_seed` fest (Register 94).
6. Demo-Gates G-01 bis G-07 vor jedem Upload; die Demo wird LEER ausgeliefert (Skill-Abschnitt
   "Die oeffentliche Demo wird LEER ausgeliefert", geprueft: `tools/build_public_exe.py`,
   `tests/test_demo_leer.py`).
7. **EXE ist vom 01.11. 19:01** - vor einer Demo neu bauen und startgeprueft starten.

## Fallstricke, in diesem Schritt belegt

- **`grep` auf einen Namen, den man im Kopf hat, findet nichts, was es nicht gibt.** Ich suchte
  `MENUE_ANZEIGE`, im Code steht `MENU_ANZEIGE` (mit E im Wort "Menue" haette es nicht existiert).
  Zwei Messungen (grep und `str.count`) meldeten 0 Treffer, obwohl die Zeile sichtbar war - erst der
  Zeichencode-Vergleich zeigte, dass ich den falschen Namen gesucht hatte. Bei "0 Treffer" also
  zuerst pruefen, ob der GESUCHTE Name stimmt, nicht ob der Code fehlt.
- **Ein Menuenpunkt kann ein Gebaeude sein, ohne so zu heissen.** "Dorfzentrum" ist die Anzeige von
  `lager`, "Kaserne" ist `kriegerakademie`, "Forschung" ist `bibliothek`. Die Zuordnung deshalb
  ABLEITEN (`gelaende.finde_gebaeude` + `MENUE_BEDINGUNG`), nicht als dritte Handliste tippen.
- **`tk.Button` mit `compound=tk.LEFT` braucht eine Bildreferenz im Objekt.** Der Cache in
  `_optik_bild` ist Pflicht, sonst gibt Tk das Bild frei und das Menue zeigt leere Felder.
- **Eine Ansicht, die im Menue nicht steht, ist trotzdem renderbar** (`_switch_view` kennt jede
  Route der Tabelle). Genau so kam der Kaserne-Absturz heraus: eine frische Siedlung ohne Gebaeude
  plus `_switch_view("Kaserne")`.

# STAND 02.11.2026, 01:36 - B4 gelaufen: Gebaeude-Optik als Modul (Register 123)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf | `5f4763b` beim Schreiben; dieser Commit bringt Modul, Pruefdatei und Bilder | `git log --oneline -1` |
| B4-Lauf | `deepseek-v4-pro`, 252 s, **1.878 Prompt- / 33.858 Antwort-Token (28.365 Denken)**; Kosten noch nicht abgerechnet | `docs/audits/usage_b4_20261102.json` |
| Geliefert | `src/gebaeude_optik.py` (ICONS, HINTERGRUENDE, `kachel()`, `hintergrund()`, `fehlende_gebaeude()`, `vorschau_blatt()`) und `tests/test_gebaeude_optik.py` | `docs/audits/BERICHT_B4_20261102.md` |
| Bilder im Projekt | **20 Menue-Icons** (256x256 RGBA) in `assets/icons/gebaeude/menue/`, **20 Hintergruende** (538x222 **RGBA**) in `.../hintergrund/`; NICHT in `archiv/` (gitignored) | eigene Kopie + Pillow-Messung |
| Pruefdatei | **179 von 179 gruen**, echte Namen und echte Bedingungen; **23 von 24 Aufrufen waren vertauscht** (namens `True`, Bedingung der Text) und meldeten 179 gruene Pruefungen ohne Wirkung | eigener Lauf |
| Modulkarte | **51 Dateien** (neu: `gebaeude_optik`) | `tools/modulkarte_bauen.py` |
| Register | **123 Punkte**, **121 Pruefdateien** | `grep -cE`, `ls tests/test_*.py \| wc -l` |
| Kosten und Guthaben | letzte Ablesung **8,97 USD** (00:05); Tagesdeckel 4 EUR heute bereits ueberschritten | Register 117, Protokoll 00:10 |

## Der EINE naechste Schritt

**Die Gebaeude-Optik in die Oberflaeche einhaengen** - das Modul ist nur die Zugriffsschicht. Drei Stellen,
je mit eigener Pruefung: (1) **Baudialog und Gebaeude-Menue** zeigen je Gebaeude das gerahmte Icon
(`gebaeude_optik.kachel(id, px)`); (2) die **Gebaeudeansicht** bekommt den Hintergrund
(`gebaeude_optik.hintergrund(id, breite)`); (3) ein **Kontaktblatt** (`vorschau_blatt`) fuer Daniels
Sichtpruefung vor dem Einbau. Vorher `motiv_1..10.png` sichern (die Handbuchmotive bleiben Rueckfallsatz).
Arbeitsweise: Pruefdatei ergaenzen, voller Sammellauf, ein Commit.

## Reihenfolge danach

1. Icons in Menue und Baudialog, Hintergrund in der Gebaeudeansicht, Kontaktblatt fuer Daniel.
2. Auswahlrahmen der C2-Lieferung zeichnen (der goldene Rahmen aus `karten_optik_fein` liegt derzeit oben);
   die acht Einzelsymbole aus `assets/icons/leiste/symbole/` sind weiter ungenutzt.
3. Wappen den fuenf Bots zuordnen; Burgen zu Weltkarten nur als gekennzeichneter Vorschlag.
4. S-8 Bilanz (500 Mana + 100 Gold, Register 93), danach `weltkarten_seed` fest (Register 94).
5. Demo-Gates G-01 bis G-07 vor jedem Upload; die Demo wird LEER ausgeliefert (Skill-Abschnitt
   „Die oeffentliche Demo wird LEER ausgeliefert“, geprueft: `tools/build_public_exe.py`, `tests/test_demo_leer.py`).

## Fallstricke, in dieser Sitzung belegt

- **Ein starkes Modell liefert Code, der laeuft - aber nicht Code, der prueft.** 23 von 24 `check()`-Aufrufen
  hatten Name und Bedingung vertauscht: `check(name, cond)` mit `check(cond, name)` aufgerufen meldet
  **179 gruene Pruefungen, die nichts pruefen**, weil der Text immer wahr ist. Nach jedem Modelllauf die
  Reihenfolge der Aufrufe pruefen, nicht nur das Ergebnis.
- **Nie auf gitignorte Pfade bauen.** `archiv/` ist gitignored - Bilder muessen unter `assets/` liegen, sonst
  fehlt der Demo die Grafik. Die Projektwurzel kommt aus `spieldaten.projektwurzel()`, nicht aus `__file__`.
- **Auftragsangaben selbst nachmessen.** „Hintergruende RGB“ im Auftrag war falsch (sie sind RGBA); der
  Modellcode folgte meiner Vorgabe und die Pruefdatei schlug mit 20 Fehlern zu Recht an.
- **Ein einzelner starker Aufruf kostet wenig, wenn der Auftrag eng ist:** 252 s, 35.736 Token gesamt.

# STAND 02.11.2026, 00:49 - C2-Ressourcenleiste steht im Kopf (Register 121)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf | `1085861` beim Schreiben; dieser Commit bringt die Leiste | `git log --oneline -1` |
| Ressourcenleiste | **im Kopf eingebaut und auf Kachelbau umgestellt**: feste Ecken und acht Symbolfelder wachsen gleichmaessig (Skala bis 1,5), nur die Luecken dehnen sich - der Balken wird breiter, die Symbole bleiben in Form; Zahlen als eigene Textebene, Positionen aus der Zusammensetzung | Register 121, 122 |
| Keine Zahl doppelt | Leiste zeigt MENGEN, Detailzeile zeigt fuer sechs Rohstoffe nur die RATE; Wolle/Leder/Pferde behalten Menge und Rate | `main.kopfzeile_fuer` |
| Messung am Fenster | **41 Canvas-Teile** (1 Bild + 8 x 5 Texte); fuenf Fensterbreiten gemessen (1000/1440/1920/2560/3440): Symbolfeld bei 2560 und 3440 **pixelgleich**, keine Verzerrung | eigener Tk-Lauf, `test_ressourcenleiste` 39/0/1 |
| Pruefdateien | neu `test_ressourcenleiste` **28/0/1**; `test_nahrungsverbrauch` mit Begruendung auf den neuen Hilfsnamen umgestellt (**53/0/0**) | eigener Lauf |
| Sammellauf | **118 von 120 gruen, 0 rot, 2 ausgesetzt**, 4.515 Pruefungen, 276 s (00:42) | `docs/audits/sammellauf_20261102_0042.log` |
| Register | **121 Punkte**, **120 Pruefdateien** | `grep -cE`, `ls tests/test_*.py \| wc -l` |
| Vorschau | `docs/audits/ressourcenleiste_vorschau_20261102.png` (Zahlen sitzen mittig in den Plaketten) | Sichtpruefung |
| Kosten und Guthaben | Blockplan **1,8715 von 4,00 USD**; Guthaben **8,97 USD** (Ablesung 00:05, Protokoll 00:10) | Register 117 |

## Der EINE naechste Schritt

**Die Leiste im laufenden Fenster abnehmen und danach die GPT-Icons in Menue und Baudialog einhaengen.**
Die Leiste ist rechnerisch und im Bild geprueft, aber **noch nicht von Daniel im Spiel gesehen** - vor dem
naechsten Umbau kurz das Spiel starten, in die Uebersicht gehen und hinsehen (Zahlen mittig, Schriftgroesse
bei kleiner Fensterbreite, Warnfarbe bei fehlender Ernte). Danach der naechste Einbau: die **20 gerahmten
GPT-Icons** in Menue und Baudialog und die **20 Hintergruende (538x222)** in die Gebaeudeansicht, Quelle
`archiv/eingaben/20261101_gebaeude_designs/Nebelseetal_Gebaeude_Designs_Update/`; vorher `motiv_1..10.png`
sichern. Arbeitsweise wie hier: Pruefdatei ergaenzen, voller Sammellauf, ein Commit.

## Reihenfolge danach

1. Leiste im Fenster abnehmen; Schriftgroesse und Warnfarben nach Daniels Urteil nachziehen.
2. GPT-Icons in Menue und Baudialog, Hintergruende in die Gebaeudeansicht (vorher `motiv_1..10.png` sichern).
3. Auswahlrahmen der C2-Lieferung zeichnen (der goldene Rahmen aus `karten_optik_fein` liegt derzeit oben);
   die acht Einzelsymbole aus `assets/icons/leiste/symbole/` sind noch ungenutzt.
4. Wappen den fuenf Bots zuordnen; Burgen zu Weltkarten nur als gekennzeichneter Vorschlag.
5. S-8 Bilanz (500 Mana + 100 Gold, Register 93), danach `weltkarten_seed` fest (Register 94).
6. Demo-Gates G-01 bis G-07 vor jedem Upload; die Demo wird LEER ausgeliefert (Skill-Abschnitt).

## Fallstricke, in dieser Sitzung belegt

- **Mengen und Raten nicht doppelt anzeigen.** Als die Leiste die Mengen uebernahm, zeigte die alte Textzeile
  dieselbe Zahl noch einmal; jetzt entscheidet `kopfzeile_fuer` je Rohstoff, welche Form gilt.
- **Bildmasse aus der Datendatei, nie tippen.** Alle acht Mittelpunkte und die Hoehe kommen aus
  `data/ressourcenleiste.json`; das Spiel rechnet mit einer Skala um, damit die Felder bei jeder Fensterbreite
  unter ihren Symbolen sitzen.
- **Tk-Bilder brauchen eine Referenz** (`self._leisten_bild_ref`), sonst raeumt der Garbage Collector die
  Leiste weg und es bleibt ein leerer Streifen.
- **Eine Wache, die einen alten Funktionsnamen woertlich prueft, wird mit Begruendung umgestellt** - sie sichert
  eine Zusage (eine Quelle fuer Aufbau und Anzeige), nicht den Namen.

# STAND 02.11.2026, 00:30 - C2-Kartenmotive und Kachelrahmen stehen auf der Siedlungskarte (Register 120)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf | `d888d8f` beim Schreiben; dieser Commit bringt den Einbau | `git log --oneline -1` |
| Kartenmotive | **20 freigestellte C2-Motive** auf der Karte, 256 px auf **44 px** verkleinert (Pillow, LANCZOS); Schalter `quelle_der_karte` in `data/gebaeude_motive.json` | Register 120, `assets/icons/gebaeude/c2/` |
| Kachelrahmen | C2-Rahmen (64 px) auf **jedem** Feld, **Deckkraft 35 Prozent** - die Zahl steht in der Datendatei, ohne Code aenderbar; voll aufgelegt war er zu dominant | `docs/audits/kartenvergleich_c2_20261102.png` (drei Fassungen) |
| Rueckfall | Gebaeude ohne Motiv zeichnet weiter den Baukoerper; die acht Handbuchmotive bleiben als Beleg in der Datendatei, nichts geloescht | `main._lade_gebaeude_motiv` liefert `None` |
| Pruefdatei | `tests/test_gebaeude_motive.py` **104/0/1** - mit Begruendung neu geschrieben (die alten Wachen nagelten drei Motive fest) | eigener Lauf |
| Sammellauf | **117 von 119 gruen, 0 rot, 2 ausgesetzt**, 4.485 Pruefungen, 274 s (00:15) | `docs/audits/sammellauf_20261102_0015.log` |
| Register | **120 Punkte**, **119 Pruefdateien** | `grep -cE`, `ls tests/test_*.py \| wc -l` |
| C2-Lieferung | 15 Mini-ZIPs, 31 Nutzbilder, Manifest 20/20 deckungsgleich, Desktop geraeumt | Register 119 |
| Kosten und Guthaben | Blockplan **1,8715 von 4,00 USD**; Guthaben **8,97 USD** / 41,02 USD Gesamtverbrauch (Ablesung Daniel 00:05) | Register 117, Protokoll 00:10 |

## Der EINE naechste Schritt

**Die Ressourcenleiste aus der C2-Lieferung oben einhaengen** - Leiste 1440x140 als Hintergrund, acht
Zahlenfelder mit den Werten als eigene, zentrierte Textebene (helle Zahl, dunkle Kontur). Reihenfolge und
Zahlenfeld-Mittelpunkte stehen woertlich in `archiv/eingaben/20261102_c2_designs/LIEFERUNG.md` (Siedler,
Nahrung, Holz, Stein, Erz, Gold, Mana, Kelch; (184,105) (342,105) (494,105) (646,105) (799,105) (957,105)
(1110,105) (1264,105) bei 1440x140, proportional skalieren). Die Werte kommen aus `kopf_zeilen_text`
bzw. der bestehenden Kopfzeilen-Rechenstelle, damit Anzeige und Kern dieselbe Quelle lesen (F-04).
Danach: GPT-Icons in Menue und Baudialog, danach die acht Ressourcensymbole der Leiste. Arbeitsweise wie
hier: Pruefdatei ergaenzen, voller Sammellauf, ein Commit.

## Reihenfolge danach

1. Ressourcenleiste oben (Teil B der C2-Lieferung) samt acht Symbolen.
2. GPT-Icons (20, gerahmt) in Menue und Baudialog, Hintergruende (538x222) in die Gebaeudeansicht;
   vorher `motiv_1..10.png` sichern.
3. Auswahlrahmen der C2-Lieferung zeichnen (der goldene Rahmen aus `karten_optik_fein` liegt derzeit oben).
4. Wappen den fuenf Bots zuordnen; Burgen zu Weltkarten nur als gekennzeichneter Vorschlag.
5. S-8 Bilanz (500 Mana + 100 Gold, Register 93), danach `weltkarten_seed` fest (Register 94).
6. Demo-Gates G-01 bis G-07 vor jedem Upload.

## Fallstricke, in dieser Sitzung belegt

- **Ein kraeftiger Kachelrahmen auf 100 Feldern zerstoert das Kartenbild.** Erst messen, dann einstellen:
  drei Fassungen rendern und vergleichen (`docs/audits/kartenvergleich_c2_20261102.png`), Deckkraft als Zahl
  in die Datendatei legen.
- **Tk gibt Bilder frei, die niemand referenziert.** Jedes skalierte Motiv und der Rahmen MUESSEN im Cache
  bleiben, sonst verschwinden sie still vom Canvas.
- **Pillow nur im Ladepfad importieren, nicht oben im Modul**: ohne Pillow (nach einem Hermes-Update) faellt
  der Code auf `tk.PhotoImage`+`subsample` zurueck, statt das Spiel unstartbar zu machen.
- **Wachen, die eine alte Zahlenlage festnageln, werden mit Begruendung umgeschrieben**, nicht der Code
  zurueckgebogen (`test_gebaeude_motive` hielt drei Motive fest).

# STAND 01.11.2026, 23:55 - Heilkunde-Bonus und Rinderfarm behoben (Register 118)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf | `c565e59` beim Schreiben; dieser Commit bringt Fix und Doku | `git log --oneline -1` |
| Heilkunde-Bonus | **greift jetzt**: `siedler_zuwachs_pro_stunde` rechnet ueber `forschung_wirkung.siedlerfaktor`; gemessen **1,5 Siedler je Stunde bei Stufe 5** (vorher 1,0) | Register 118, eigener Lauf |
| Rinderfarm | **3 Nahrung + 3 Leder** auf Grasland, **1,5 + 1,5** auf Steppe (Handbuch 2009, Seite 10, woertlich) | `data/buildings.json`, Register 118 |
| Anzeige | die Gebaeudewirkungen zeigen den Zuwachs inklusive Heilkunde - Kern und Anzeige lesen dieselbe Stufenkarte (`self.state.forschungs_stufen()`) | `src/main.py`, Wachen A11/A12 |
| C2-Lieferung | **15 Mini-ZIPs, 31 Nutzbilder aufgenommen und geprueft**: 20 Kartenmotive 256x256 RGBA **freigestellt** (41-54 % Deckung), 8 Symbole 96x96, Leiste 1440x140, 2 Kachelrahmen 64x64; Manifest **20 von 20 IDs deckungsgleich** mit `data/buildings.json`; Desktop geraeumt | Register 119, `archiv/eingaben/20261102_c2_designs/` |
| Neue Pruefdatei | `tests/test_heilkunde_rinderfarm.py` **23/0/0**; `test_gpt_ne01_origwerte` **63/0/0**, `test_oekonomie_kern_10x10_nachfolger` **98/0/4** (die vier Befunde sind alt) | eigener Lauf 23:52 |
| Register | **118 Punkte**, **119 Pruefdateien** | `grep -cE`, `ls tests/test_*.py \| wc -l` |
| Sammellauf | **117 von 119 gruen, 0 rot, 2 ausgesetzt**, 4.424 Pruefungen, 456 s (23:55-00:04) - die zwei ausgesetzten sind `test_oekonomie_kern_unabhaengig` und `test_weltkarte` (dokumentiert zurueckgezogen) | `docs/audits/sammellauf_20261101_2355.log` |
| Kosten und Guthaben | unveraendert: Blockplan **1,8715 von 4,00 USD**, Guthaben **9,18 USD** (Ablesung 22:48) - heute kein starker Modelllauf mehr | Register 114, 117 |

## Der EINE naechste Schritt

**Die C2-Kartenmotive auf die Siedlungskarte bringen** - vorher entscheidet Daniel, WELCHE Fassung
gilt: die **20 freigestellten C2-Motive** (Register 119, decken alle 20 Gebaeude ab, 256x256 RGBA) oder die
**zehn handgeschnittenen Handbuchmotive** (Register 113, Daniels Zuordnung 1-10). Danach die Karte:
Motiv rund 44 px plus Gelaenderahmen (`kachelrahmen_ruhe.png`/`_auswahl.png`, 64x64) je Kachel, und die
Ressourcenleiste 1440x140 oben mit acht Zahlenfeldern (Einbauhinweise in
`archiv/eingaben/20261102_c2_designs/LIEFERUNG.md`). Arbeitsweise wie hier: Pruefdatei ergaenzen, voller
Sammellauf, ein Commit. Der Einbau aendert das sichtbare Kartenbild sichtbar - deshalb zuerst die Entscheidung.

## Reihenfolge danach

1. Kartenoptik Variante 2 in `src/main.py` (Motiv rund 44 px + Gelaenderahmen je Kachel).
2. GPT-Icons in Menue und Baudialog, Hintergruende (538x222) in die Gebaeudeansicht
   (`archiv/eingaben/20261101_gebaeude_designs/`); vorher `motiv_1..10.png` sichern.
3. C2 pruefen, sobald Daniels ZIPs kommen (Kartenmotive, Ressourcenleiste, Kachelrahmen).
4. Wappen den fuenf Bots zuordnen; Burgen zu Weltkarten nur als gekennzeichneter Vorschlag.
5. S-8 Bilanz (500 Mana + 100 Gold, Register 93), danach `weltkarten_seed` fest (Register 94).
6. Demo-Gates G-01 bis G-07 vor jedem Upload.

## Fallstricke, in dieser Sitzung belegt

- **Der alte Kleinbuchstaben-Schluessel `heilkunde` wirkt bewusst NICHT mehr.** Wer ihn wieder einbaut,
  holt den Befund aus Register 105 zurueck; Wache 7e2 in `test_oekonomie_kern_10x10_nachfolger` haelt das fest.
- **Leder haengt an Tierhaltung, nicht an Felderwirtschaft.** Eine Pruefung des Rinderfarm-Bonus mit
  Felderwirtschaft allein misst nichts - eigener Fehlversuch in dieser Sitzung, B7 fiel zuerst rot aus.
- **Datenaenderung heisst: Tests nach dem alten Literal greppen.** `grep -rn "rinderfarm" tests/` fand zwei
  Stellen; beide sind mit Begruendung umgestellt, nicht der Code zurueckgebogen.

# STAND 01.11.2026, 22:50 - B3 abgeschlossen und unabhaengig geprueft, vier GPT-Pakete entpackt und abgeglichen

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf | **`85c0c3b`** (B3), Doku-Commit folgt | `git log --oneline -1` |
| B3 (S-7 Bots erlebbar) | **ABGESCHLOSSEN**, nicht abgebrochen: die Sitzung `local-94abacfd` (deepseek-v4-pro) lief bis 22:45 | Register 114 |
| B3 Abnahme | `test_s7_botverhalten` **45/0/0**, die vier zuvor roten Pruefdateien wieder gruen, Sammellauf 22:35: **116/118 gruen, 0 rot, 2 ausgesetzt, 4.400 Pruefungen, 500 s** | eigener Lauf des Koordinators, `docs/audits/sammellauf_20261101_2235.log` |
| Kosten Blockplan | B1 0,5980 + B2 0,2553 + B3 **1,0182** = **1,8715 USD** von 4,00 USD | Register 114; Preis aus B1 kalibriert, Probe 0,6010 gegen 0,5980 |
| Guthaben 22:48 | **9,18 USD**, Gesamtverbrauch **40,81 USD**; Differenz zur Ablesung 21:0x = 1,21 USD, gedeckt durch B3 1,0182 + Koordination 0,19 | Register 117 |
| Tagesdeckel | rund **4,2 USD** heute – der 4-EUR-Rahmen ist praktisch erreicht | Register 117 |
| Sammellauf dieses Stands | **116/118 gruen, 0 rot, 2 ausgesetzt, 4.400 Pruefungen, 283 s** (22:56) | `docs/audits/sammellauf_20261101_2251.log` |
| Register | **117 Punkte**, **118 Pruefdateien** | `grep -cE`, `ls tests/test_*.py \| wc -l` |
| GPT-Gebaeudepakete | **vier ZIPs eingegangen**, hashgeprueft, entpackt nach `archiv/eingaben/20261101_gebaeude_designs/`; **20 Icons, 20 Hintergruende, 4 Tafeln**, Manifest-IDs **20 von 20 deckungsgleich** mit `data/buildings.json` | Register 115 |
| **Wichtigster Befund zum Einbau** | die 20 Icons sind **nicht freigestellt** (256x256, 0 % Transparenz, gemalte Szene im Goldrahmen) – sie taugen fuer **Menue und Baudialog**, **nicht** als Kartenmotive | Pillow-Messung, Sichtpruefung der Vorschau |
| Offen aus B3 | WIRKUNG der Volksattribute und Verhaltensboni nicht verdrahtet (Hook-Stellen in `kampf.py`, `spieloekonomie.py`, `auftraege.py`), Sperrzeit 1 h statt 48 h | Bericht S-7, Abschnitt 5 |

## Der EINE naechste Schritt

**Die Icons in Menue und Baudialog einhaengen, die Hintergruende in die Gebaeudeansicht** – nach den
zwei offenen Fixes (Heilkunde, Rinderfarm), die Daniel am 01.11. freigegeben hat. Kartenmotive bleiben
die zehn Handbuchmotive aus Register 113; die GPT-Icons ersetzen sie nicht.

## Reihenfolge

1. Heilkunde-Bonus auf `forschung_wirkung.siedlerfaktor` legen, Rinderfarm auf 3/1,5 (Freigabe liegt vor).
2. Zehn Handbuchmotive in `data/gebaeude_motive.json` eintragen (Daniels Zuordnung, Register 113), dann Karte.
3. Kartenoptik Variante 2 (Motiv rund 44 px + Gelaenderahmen je Kachel).
4. GPT-Icons in Menue und Baudialog, Hintergruende (538x222) in die Gebaeudeansicht.
5. Wappen den fuenf Bots zuordnen; Burgen zu Welten nur als gekennzeichneter Vorschlag.
6. S-8 Bilanz (500 Mana + 100 Gold, Register 93), `weltkarten_seed` fest (Register 94).
7. Demo-Gates G-01 bis G-07 vor jedem Upload.

## Fallstricke, in dieser Sitzung belegt

- **Ein laufender Block ist nicht am Arbeitsbaum zu erkennen.** Die Uebergabe 21:55 meldete B3 als
  abgebrochen, waehrend die Sitzung weiterlief und den Baum rot hielt. Richtig ist ein Blick auf die
  **letzte Zeile des Aufrufprotokolls** (`AppData/Local/hermes/logs/agent.log`, Sitzungskennung).
- **`data/gebaeude.json` gibt es nicht** – die Gebaeudeliste steht in `data/buildings.json`.
- **`archiv/` und `*.log` sind gitignored**: Eingabepakete und Sammellauf-Protokolle liegen auf der
  Platte, nicht in der Versionsgeschichte. Wer sie braucht, muss die Platte sichern, nicht das Repo.
- **GPT-Icons sind Buttons, keine Kulisse**: 0 % Transparenz. Fuer die Karte braucht es die
  Handbuchmotive oder eine neue Freistellung.

# STAND 01.11.2026, 21:55 - B3 abgebrochen und gesichert, Sitzungsende vorbereitet

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf | **`f5351f6`**, Arbeitsbaum **leer** | `git status --porcelain` (0 Zeilen) |
| B3 (S-7 Bot-Taktik) | **abgebrochen**, kein Bericht, kein Test, keine `usage_b3_*.json` | `ls docs/audits/BERICHT_S7_20261101.md` = nicht vorhanden |
| B3-Reste | 112 Zeilen in `src/bottaktik.py` + `src/main.py`, syntaktisch gueltig, ungeprueft; gesichert als Patch **280 Zeilen** (`eaf258ee`) und als `stash@{0}` | `archiv/unfertig/B3_unfertig_20261101.patch` |
| Kosten starkes Modell | B1 0,5980 + B2 0,2553 = **0,8533 USD**; von 4 USD bleiben rund **3,15 USD** | `usage_b1_*.json`, `usage_b2_*.json` |
| Guthaben | **10,39 USD**, Gesamtverbrauch 39,60 USD (Daniel 01.11. abgelesen) | Register 111 |
| Register | **113 Punkte**, 117 Pruefdateien | `grep -cE`, `ls tests/test_*.py` |
| Letzter belastbarer Sammellauf | 117 Dateien, 115 gruen, 0 rot, 2 ausgesetzt, 4.350 Pruefungen, 628 s (19:14) | `docs/audits/sammellauf_20261101_1914.log` |
| GPT-Gebaeudepaket | **nicht herunterladbar**: gespeicherte HTML enthaelt keine Dateien, Sandbox-Link tot; Daniel hat GPT angewiesen, **vier kleinere ZIPs** daraus zu machen | `C:/Users/saras/Desktop/Nebelseetal_Gebaeude_Design_Gesamtpaket_herunterladen.html` |

## Offene Entscheidungen, von Daniel am 01.11. beantwortet

| Thema | Entscheidung |
|---|---|
| Kartenoptik | **Variante 2**: Motiv rund 44 px plus Geländerahmen je Kachel, damit das Feld sichtbar bleibt |
| Gebaeudemotive | **alle zehn** korrigierten Motive in die Spieldaten und auf die Siedlungskarte |
| Wappen | Zuordnung zu den Bots nach Wahl von Hermes, keine Vorgabe von Daniel |
| Burgen | Zuordnung zu den Weltkarten bleibt offen (Vorschlag erlaubt, im Katalog als Vorschlag markiert) |
| B1-Befunde | **beide sofort beheben**: Heilkunde-Bonus auf `forschung_wirkung.siedlerfaktor` legen, Rinderfarm auf 3/1,5 |

# STAND 01.11.2026, 21:35 - B2 gelaufen, Katalog vollstaendig (zehn Motive, sechs Burgen, zehn Wappen)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

| Gegenstand | Wert | Beleg |
|---|---|---|
| B1 | Wirtschaft gemessen, Werkzeug + Bericht (263 Zeilen) | Commit `a3fd069` |
| B2 | Kampf gemessen, `tools/mess_kampf.py` + Bericht (272 Zeilen), 40 Laeufe je Wallstufe 0-10 | `docs/audits/MESS_KAMPF_20261101.md` |
| B2 Kernzahlen | Schwelle gemessen == dokumentiert auf allen zehn Stufen; Beute ladungsgedeckelt; Wall 1 braucht 4 Krieger nach SK statt 1 nach AT | Bericht Abschnitte D, E, H |
| Kosten starkes Modell | B1 0,5980 + B2 0,2553 = **0,8533 USD**, von 4 USD bleiben rund 3,15 USD | `usage_b1_*.json`, `usage_b2_*.json` |
| Guthaben | **10,39 USD**, Gesamtverbrauch 39,60 USD (Differenz 1,21 USD, gedeckt) | Register 111 |
| Register | **113 Punkte** | `grep -cE` |
| Symbolkatalog | 11 Seiten: zehn Motive zugeordnet, sechs Burgen, zehn Wappen, Zuordnungsblatt | `docs/SYMBOLKATALOG_Nebelseetal_20261101.pdf` |
| B3 Paket | `docs/auftraege/B3_paket_20261101.md`, 41.579 Zeichen, S-7 Bots erlebbar | Datei |

**Offen aus B2 (Register 110):** die Auftrags-Vorpruefung zaehlt Fernkaempfer und Kundschafter mit, die
Schlacht fuer die Wallschwelle nur Nahkampf. **Offen aus B1 (Register 105):** Heilkunde-Bonus greift nie,
Rinderfarm liefert 1 statt 3 Nahrung.

## Der EINE naechste Schritt

Block **B3** starten (S-7 Bots erlebbar): Paket liegt fertig, Lauf einzeln mit `--usage-file`, fertig erst
an der `usage_*.json`, danach Kernzahlen nachrechnen, voller Sammellauf, Commit oder Ruecknahme,
Kostenzeile im Protokoll. Danach der Optik-Schnitt nach Register 112: Gebaeude kleiner auf dem Feld,
Ressourcenleiste, Motivauswahl, Burgen- und Wappenzuordnung.

---

# STAND 01.11.2026, 21:05 - B1 des starken Modells gelaufen, zwei echte Fehler gefunden

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Blockplan:** `docs/AUFTRAG_STARKES_MODELL_BLOCKPLAN_20261101.md` (B1 bis B8, rund 4,00 USD).
**B1 ist abgeschlossen**, B2 ist vorbereitet und startet als naechstes.

| Gegenstand | Wert | Beleg |
|---|---|---|
| B1 Werkzeug | `tools/mess_wirtschaft.py`, 315 Zeilen, reines ASCII, Rueckgabewert 0 | eigener Lauf |
| B1 Bericht | `docs/audits/MESS_WIRTSCHAFT_20261101.md`, 263 Zeilen, drei Kernaussagen, jede Abweichung | Datei |
| B1 Kosten | **0,5980 USD gemessen** (52 Aufrufe, 11,9 Mio Input / 11,7 Mio Cache, 103 k Output) | `docs/audits/usage_b1_20261101.json` + Preise aus dem Export |
| Sammellauf | 117 Dateien, **115 gruen, 0 rot**, 2 ausgesetzt, 4.350 Pruefungen, 695 s | `docs/audits/sammellauf_20261101_2045_b1.log` |
| Register | **108 Punkte** | `grep -cE '^\| [0-9]+ \|'` |
| Symbolkatalog | `docs/SYMBOLKATALOG_Nebelseetal_20261101.pdf`, 8 Seiten, ueber `tools/icons_katalog_pdf.py` reproduzierbar | Datei |
| Chat-Paket C1 | `docs/auftraege/C1_paket_20261101.md`, 18.810 Zeichen, noch nicht gelaufen | Datei |
| B2 Paket | `docs/auftraege/B2_paket_20261101.md`, 41.868 Zeichen | Datei |

**Zwei Befunde aus B1 (Register 105), nicht behoben:** der Heilkunde-Bonus greift im Spiel nie
(`gebaeude_wirkung` liest `heilkunde` klein), und die Rinderfarm liefert 1 statt 3 Nahrung gegen
Handbuch Seite 10. Beide brauchen Daniels Entscheidung, weil sie Spielwerte beruehren.

## Der EINE naechste Schritt

Block **B2** starten (Kampf messen): Paket liegt fertig, Lauf einzeln mit `--usage-file`, fertig erst
an der `usage_*.json`. Danach Kernzahlen selbst nachrechnen, voller Sammellauf, Commit oder
Ruecknahme, Kostenzeile im Protokoll. Parallel offen: Daniels Motivzuordnung in den Symbolkatalog
einarbeiten (Scheune, Schafzucht, Goldmine, Farm, Kriegerakademie, Erzmine, Steinbruch, Holzfaehler),
die zwei fehlenden Motive seite01_bild02 und bild03 schneiden und die automatische
Hintergrund-Entfernung aus dem Katalogwerkzeug nehmen.

---

# STAND 01.11.2026, 20:15 - Uebergabe geschrieben, Blockplan fuer das starke Modell liegt bereit

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Diese Sitzung ist abgeschlossen.** Uebergabe: `docs/UEBERGABE_20261101_2010.md` (Kopie auf dem
Desktop, hashgleich), Startzeile dort Abschnitt 8.

**Blockplan fuer `deepseek-v4-pro`:** `docs/AUFTRAG_STARKES_MODELL_BLOCKPLAN_20261101.md` - acht Bloecke,
zusammen 3,55-4,50 USD, Kontostand 11,60 USD.

| Block | Inhalt | Art | Kosten |
|---|---|---|---|
| B1 | Wirtschaft messen (Ertraege, Siedler, Gold, Mana, Nahrung) | Messwerkzeug | 0,35-0,45 USD |
| B2 | Kampf messen (Wall, SK, Beute, 40 Laeufe je Stufe) | Messwerkzeug | 0,35-0,45 USD |
| B3 | S-7 Bots erlebbar (`bottaktik` anbinden) | Umbau | 0,60-0,75 USD |
| B4 | S-3 Forschungsverbund absichern | Umbau klein | 0,35-0,45 USD |
| B5 | S-4 Einheitenverlegung | Umbau | 0,50-0,65 USD |
| B6 | S-6 Dorftransfer (500 Mana + 100 Gold) | Umbau | 0,55-0,70 USD |
| B7 | Balance-Abgleich und Kette ohne Cheats | Messung + Doku | 0,45-0,55 USD |
| B8 | Demo-Reifepruefung (Gates G-01 bis G-07) | Pruefung | 0,40-0,50 USD |

**Kein Block ist gestartet** - Daniel entscheidet ueber den Start. Budget-Wache: bei 3,00 USD gemessenem
Verbrauch wird vor B7/B8 angehalten und gefragt.

## Der EINE naechste Schritt

Block **B1** starten: Paketdatei bauen (20.000-45.000 Zeichen), Zeichen/Token/USD **drucken** und Daniel
vorlegen, dann `tools/mess_wirtschaft.py` und `docs/audits/MESS_WIRTSCHAFT_<datum>.md` vom starken Modell
bauen lassen; danach Kernzahlen selbst nachrechnen, voller Sammellauf, Commit oder Ruecknahme, Kostenzeile
im Protokoll. Arbeitsweise: ein Schritt = ein Commit = ein gruener voller Sammellauf.

---

# STAND 01.11.2026, 19:25 - Demo wird LEER ausgeliefert, externes GitHub-Feedback aufgenommen

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

## Was seit 19:00 dazukam

**Die Demo wird leer ausgeliefert** (Register 101, Daniels Vorgabe "in der demo exe darf es keine
vorhandenen spielstaende geben sie muss leer sein"):

| Gegenstand | Wert | Beleg |
|---|---|---|
| Bau prueft das Paket | bricht ab, wenn in `data/` oder `assets/` ein Spielstand, Admin-Teststand, Passworttor oder eine Sperrdatei liegt | `tools/build_public_exe.py` `spielstaende_im_paket` |
| Demo-Speicherordner | `%LOCALAPPDATA%\Nebelseetal_Remake\Demo` - eigener, nie benutzter Ordner; der alte Testordner wird nicht mehr gelesen | `src/public_start.py` |
| Testspielstaende | **16 Dateien geloescht** (nur Teststaende, Daniels Ansage), vorher hashgeprueft in `archiv/testspielstaende_20261101.zip` (1.116.438 Byte, testzip sauber) | ZIP + `MANIFEST_SHA256.txt` |
| Zurueck im Profil | nur `tor.json` (Passworttor, kein Spielstand); veraltete `game.lock` entfernt | `ls ~/.nebelseetal/` |
| Pruefdatei | `tests/test_demo_leer.py` **28/0/0** | Lauf 19:12 |
| Nachbar | `test_public_edition_fix04j` 6 Tests OK (Wache auf den neuen Ordnernamen umgestellt) | Lauf 19:13 |
| Voller Sammellauf | **117 Dateien, 115 gruen, 0 rot, 2 ausgesetzt, 4.350 Pruefungen, 628 s** | `docs/audits/sammellauf_20261101_1914.log` |
| Auftrag 9 (Chat-Modell) | `docs/AUFTRAG_GPT_TRANSFER_S3_S4_S6_20261101.md`, 10.651 Byte, Kopie auf dem Desktop | `59002d91...` |

**Externes GitHub-Feedback vom 01.11.2026 aufgenommen** (Register 102): der Bericht prueft ausschliesslich
den OEFFENTLICHEN Stand (`main` = FIX04j, `v0.4.0-test.1`, PR #1 mit eigener Wurzel), nicht den lokalen HEAD.
Einordnung, Zuordnung zu vorhandenen Stellen und die sieben Demo-Freigabe-Gates G-01 bis G-07 stehen in
`docs/EXTERNES_FEEDBACK_GITHUB_20261101.md`; das Original liegt hashgeprueft unter
`archiv/eingaben/20261101_github_feedback/` (31.499 Byte, `dff01476...`). Es betrifft nur das Online-Repo und
ist reines Feedback: **nichts davon ist umgesetzt, kein Push, kein Release.** Zwei Punkte bleiben bei Daniel:
Lizenz fuer den eigenen Code und rechtliche Einordnung der historischen Grafiken.

## Der EINE naechste Schritt

**Das Bot-Taktikpaket gegen den Code pruefen**
(`archiv/eingaben/20261101_gpt_antworten/GPT_Taktikpaket_HERMES_ENTWURF_BOTVERHALTEN_TAKTIKPAKETE_20261101.md`,
47.159 Byte) und danach S-7 vorbereiten (Bots erlebbar, `bottaktik` anschliessen). Fuer das starke Chat-Modell
liegt das naechste Paket als `docs/AUFTRAG_GPT_TRANSFER_UND_DEMO_REST_20261101.md`. Danach S-3, S-4, S-6, S-7,
S-8 (Bilanz und Weltensprung 500 Mana plus 100 Gold), dann Demo-Bau mit den Gates G-01 bis G-07.
Arbeitsweise: ein Schritt = ein Commit = ein gruener voller Sammellauf.

---


# STAND 01.11.2026, 19:00 - S-5 gebaut: die Weltkarten zeigen Gelaende

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**S-5 ist gebaut und gruen** (Register 91, Freigabe 92). Das Gelaende der Weltkarten kommt aus
`portalraum.weltbild`:

| Gegenstand | Wert | Beleg |
|---|---|---|
| Quellen | sieben Gelaendearten und ihre `haeufigkeit` NUR aus `data/gelaende.json` (Summe 100) | `portalraum.gelaendeverteilung` |
| Raster | 10x10 Gruppen zu je 2x2 gleichartigem Gelaende = 100 Gruppen, 400 Felder | `portalraum.weltbild` |
| Verteilung | exakt 4 x haeufigkeit Felder je Art (Grasland 80, Nebelsee 28 ...) | Pruefdatei Abschnitt 3 |
| Seed | SHA-256 aus `kennung|seed`, Konfigurationswert `weltkarten_seed` in `data/welten.json` | `portalraum._seed_zahl` |
| Stabilitaet | gleicher Name und Seed = bytegleiches Raster, auch in einem frischen Interpreter | Pruefdatei Abschnitt 5 |
| Anzeige | Gelaendefarbe je Feld, Legende mit Haeufigkeiten, angewaehltes Feld mit Gelaendenamen | `main._render_portal` |
| Wirkung | KEINE Bauplatz-, Rohstoff- oder Ertragswirkung; Ernte vor/nach Weltwechsel identisch | Pruefdatei Abschnitt 9 |
| Pruefdatei | `tests/test_weltbild_gelaende.py` **135/0/0** | Lauf 18:53 |
| Voller Sammellauf | **116 Dateien, 114 gruen, 0 rot, 2 ausgesetzt, 4.349 Pruefungen, 305 s** | `docs/audits/sammellauf_20261101_1853.log` |
| Register | 91 (Status GEBAUT) und 100 (Nebenbefund) | `docs/PRUEFREGEL_ORIGINAL.md` |
| EXE | **47.981.465 Byte**, SHA256 `e361a2b3b8f1ddf062ab82041fc14a84232b79519af98e4ee2662aeab9585683`, gebaut 19:01 zu Code-Stand `b256f3b` | `stat -c %s`, `sha256sum` |
| EXE-Startbeleg | Kind-PID **15392**, Fenster `Nebelseetal Remake`, `MainWindowHandle` 86509210, nach **149 s** Responding True, danach beendet | `Get-Process`, Bildschirmaufnahme (Tor mit Passwortfeld) |

**Nebenbefund, im selben Commit behoben:** die Portalansicht gab die Nummern des Spielstands (d04 = 4)
ungefiltert als Index an das Raster - die eigene Weltkarte erschien als fremde (Bannerfarbe rot). Die neue
Pruefdatei hat es gefunden, keine bestehende Wache (Register 100).

## Der EINE naechste Schritt

**Das Bot-Taktikpaket gegen den Code pruefen**
(`archiv/eingaben/20261101_gpt_antworten/GPT_Taktikpaket_HERMES_ENTWURF_BOTVERHALTEN_TAKTIKPAKETE_20261101.md`,
47.159 Byte) - wie beim Textpaket jede Aussage am heutigen Stand messen, Widersprueche einzeln benennen, dann
S-7 (Bots erlebbar, `bottaktik` anschliessen) vorbereiten. Danach S-3 (Forschungsuebernahme, acht
Entscheidungen), S-4, S-6 (Dorftransfer), S-7, S-8 (Bilanz und der neue Weltensprung-Preis 500 Mana plus
100 Gold aus Register 93), dann Demo-Bau und Freigabepruefung. Arbeitsweise: ein Schritt = ein Commit =
ein gruener voller Sammellauf; offene Punkte sammeln statt einzeln fragen.

---

---

# STAND 01.11.2026, 18:40 - Fragenrunde beantwortet, S-5 FREIGEGEBEN

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

## Was seit 17:26 dazukam

**Der GPT-Antworttext zum Demo-Paket ist geprueft, nicht uebernommen.** Pruefvermerk
`docs/audits/PRUEFVERMERK_GPT_TEXTPAKET_20261101.md` (Commit `b91186f`): 26 Angaben stimmen mit dem Code,
**sieben muessen raus**, vier fehlen. Der schwerste Befund **W-01**: das Textpaket behauptet an fuenf
Stellen, die Weltkarten zeigten Gelaende - das ist heute falsch (`portalanzeige` kennt kein Gelaende,
Register 91 steht auf NOCH NICHT GEBAUT) und wird erst mit S-5 wahr. Weitere: Spionage ist nicht
"gar nicht da" (Diebesgilde und sechs Kundschafter-Einheiten existieren), `Ragnaroeck` statt `Ragnaroek`,
Tempel auf Sumpf erzeugt 0 statt 1 Mana, Siedlerobergrenze ist belegt statt unbekannt, Limbus doppelt,
Ausbildungsdauer im Code geregelt statt unbekannt.

**Alle dreizehn offenen Fragen sind beantwortet** (`docs/FRAGEN_AN_DANIEL_20261101_1820.md`, Abschnitt
Antworten). Die Entscheidungen stehen als Register 92 bis 99.

| # | Entscheidung | Wirkung |
|---|---|---|
| 92 | **S-5 freigegeben** | Weltbild als Gelaende wird jetzt gebaut |
| 93 | **Weltensprung 500 Mana plus 100 Gold** (5.000 bleibt Originalwert) | Einbau in S-8; heute bucht der Code noch 5.000 |
| 94 | `weltkarten_seed` bekommt einen festen Wert | beim Demo-Bau nachtragen |
| 95 | "Demo" im Titel | Release-Texte |
| 96 | Handbuch erst nach S-5 | keine Veroeffentlichung vorher |
| 97 | Handbuch als eigene Datei neben dem Release | Ablage |
| 98 | Limbus bleibt Weltname, Ebene heisst "der magische Limbus" | Spielertexte |
| 99 | **Die Demo ist ein moeglichst weit umgesetztes Testspiel** | Funktionen vor Release-Texten |

## Der EINE naechste Schritt

**S-5 - das Weltbild als Gelaende** (Register 91 Vorgabe, 92 Freigabe): sieben Gelaendearten aus
`data/gelaende.json` (Feld `haeufigkeit`, Summe 100) als 2x2-Bloecke auf 20x20 = 400 Feldern, stabiler
Seed je Welt aus einem neuen Konfigurationswert `weltkarten_seed` in `data/welten.json`. Andockstellen:
`portalraum.anzeige_raster` (Feld bekommt Gelaende dazu), `main._render_portal`/`_portal_feld_waehlen`,
Farben und Namen aus `gelaende.farbe`/`gelaende.name`. Keine Orte, Doerfer, Gegner oder dauerhaften
Markierungen. Neue Pruefdatei, voller Sammellauf, Registereintrag an Punkt 91, Protokollzeile, ein Commit.

**Danach in dieser Reihenfolge:** das Bot-Taktikpaket gegen den Code pruefen
(`archiv/eingaben/20261101_gpt_antworten/GPT_Taktikpaket_HERMES_ENTWURF_BOTVERHALTEN_TAKTIKPAKETE_20261101.md`),
dann S-3 (Forschungsuebernahme, acht Entscheidungen), S-4, S-6 (Dorftransfer), **S-7 (Bots erlebbar,
`bottaktik` anschliessen)**, S-8 (Bilanz und der neue Weltensprung-Preis), dann Demo-Bau und
Freigabepruefung.

---

# STAND 01.11.2026, 17:26 - S-2c abgeschlossen: das Dorfzentrum ist das Lager, und den Platz bestimmt der Spieler

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

## Was in dieser Sitzung gebaut wurde

**S-2c und S-2c-D sind fertig und gruen** - das Dorfzentrum ist Menuepunkt UND Gebaeude, die
Lagerverwaltung steht darin, und es kommt kostenlos mit jeder Gruendung, ohne dass das Spiel den Platz
vorgibt:

| Gegenstand | Wert | Beleg |
|---|---|---|
| Gebaeude | Kennung bleibt `lager`, Anzeigename **Dorfzentrum**, `alias: ["Lager"]`, `max_je_siedlung: 1` | `data/buildings.json` |
| Alias-Erkennung | `finde_gebaeude` liest zusaetzlich den `alias` - ein Altstand mit "Lager" in `bauten` zaehlt als Dorfzentrum, ohne Migration | `src/gelaende.py` |
| Menue | `MENUE_ENTFALLEN = {"Lager"}` blendet den Punkt in der ANZEIGE aus; `MENU_ITEMS` bleibt die belegte Original-Liste (16 Eintraege); Anker fuer Stellmacher/Diebesgilde ist `MENUE_ANKER = "Dorfzentrum"` | `src/main.py` |
| EINE Lageransicht | `_render_storage(eigener_titel=False)` wird von `_render_overview` gerufen; die alte Route traegt `STILLGELEGT` | `src/main.py` |
| Platzwahl | `Settlement.dorfzentrum_offen` (Vorgabe False) wird bei jeder Gruendung gesetzt; `_dorfzentrum_setzen(feld)` setzt das Gebaeude kostenlos auf das vom Spieler gewaehlte Feld | `src/main.py` |
| Abriss | Das einzige Dorfzentrum ist gesperrt - auch unter dem alten Namen "Lager" | `_karten_abreissen` |
| Pruefdatei | `tests/test_dorfzentrum_ist_lager.py` **82/0/0** | Lauf 17:23 |
| Voller Sammellauf | **115 Dateien, 113 gruen, 0 rot, 2 ausgesetzt, 4.214 Pruefungen, 272 s** | `docs/audits/sammellauf_20261101_1723_s2cd.log` |
| Register | 90 | `docs/PRUEFREGEL_ORIGINAL.md` |

**Daniels Entscheidung, woertlich (01.11.2026):** "kostenlos bei jeder gruendung mitgesetzt aber das setzen
lassen ist wichtig damit der spieler bestimmt welches feld seiner karte besetzt wird". Gelesen als
MITGELIEFERT, nicht automatisch gesetzt: die Gruendung setzt nur das Kennzeichen, die Siedlungskarte zeigt
den Kasten "Dorfzentrum einplanen" mit dem Knopf "Dorfzentrum hier setzen (kostenlos)". Die S-1-Regel bleibt
unberuehrt - es bleiben **drei** automatische Startgebaeude, alle 35 Wachen unveraendert gruen.

**Was das im Spiel bedeutet:** Im Menue steht kein eigener Punkt "Lager" mehr. Das Dorfzentrum zeigt oben die
Uebersicht (naechster Schritt, Siedler, Siedlungen, Auftraege, Gebaeudewirkungen) und darunter die
Lagerverwaltung des aktiven Ortes: Bestand, Waren, Einheiten und die Werkstaetten mit ihren Warteschlangen.
Nach der Gruendung wahlt der Spieler das Feld des Dorfzentrums selbst; ein zweites ist nicht baubar, das
einzige nicht abreissbar.

## Werkzeug wiederhergestellt: PyInstaller

Das Hermes-Update am 01.11. (13:59-14:52) hat die Python-Runtime getauscht; `PyInstaller` fehlte danach. Die
Pruefung `tools/build_exe.py --pruefen` lief noch, der Bau brach mit "No module named PyInstaller" ab und
liess die alte EXE unangetastet. Auf Daniels Freigabe mit `uv pip install pyinstaller` (6.22.3)
nachinstalliert. Nach dem Commit `4ed7fbb` neu gebaut: **EXE 47.974.724 Byte, SHA256 `595c48bf...`**
(17:29), **Start belegt** - Kind-PID 13892, Fenster "Nebelseetal Remake", MainWindowHandle 163907294, nach
116 s und 129 s Responding True, danach beendet. Zwischenbau 17:14 (47.972.104 Byte, `4df48ffa...`) war nur
der Werkzeugbeweis und ist ueberholt.

## Der naechste Schritt

**S-5: das Weltbild als Gelaende** (Daniel hat die Ableitung entschieden: die sieben vorhandenen
Gelaendearten mit ihren Gewichten aus `data/gelaende.json`, als 2x2-Bloecke mit stabilem Seed je Welt - siehe
Register 91). Danach S-3 (Forschungsuebernahme, Papier liegt), S-4, S-6, S-7, S-8.

**Papier eingetroffen und geprüft:** die Antwort des Chat-Modells auf Auftrag 7 (S-7/S-8/Demo-Anleitung)
liegt in `archiv/eingaben/20261101_gpt_antworten/HERMES_ENTWURF_S7_S8_DEMO_ANLEITUNG_20261101.md`; der
Gegenbefund am echten Code steht in `docs/audits/PRUEFVERMERK_S7_S8_ENTWURF_20261101.md`. **Wichtigster
Befund:** die vom Papier befürchtete "blockierende Mana-Lücke" gibt es nicht — der **Tempel** ist ein
Mana-Produzent (5/h auf Nebelsee, sonst 1/h) und kommt seit S-1 bei jeder Gründung mit. Der Weltensprung
kostet belegt 5.000 Mana (`data/welten.json`, aus portal.php 2005); 500 Mana wären für ein einzelnes Dorf
auf Normalgelände in rund 21 Spieltagen erspart, 5.000 in über 200. Mana wird außerdem bei **jeder**
Portalreise verbraucht (5 + 0,5 je Feld + 20 je Zonenstufe, `src/auftraege.py`). Der achte Bot-Zustand heißt
`FLIEHEN`, nicht `FLEHEN`. Offen bleiben: Goldpreis `G`, echte 24-Spielstunden-Messung, Bot-Ereignisquellen.

**Auftrag 7 beantwortet und abgelegt:** `AUFTRAG_GPT_S7_S8_UND_DEMO_ANLEITUNG_20261101.md` - S-7 (Bots
sichtbar ohne Kartenmarker, kein Angriff), S-8 (Bilanz Mana und Reisekosten) und der gefuehrte Start der
Demo. Die Antwort ist geprueft (siehe oben), **gebaut ist davon noch nichts**. Auf dem Desktop liegt genau diese eine Datei.

# STAND 01.11.2026, 12:20 - S-2b abgeschlossen: die Portal-Uebersicht zeigt Weltkartenliste und Gelaendekaestchen

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

## Was in dieser Sitzung gebaut wurde

**S-2b ist fertig und gruen** - die Portalansicht traegt oben die sechs belegten Weltkarten mit Namen und
Kennzeichen, darunter das Gelaendekaestchen der aktuellen Welt mit anklickbaren Feldern:

| Gegenstand | Wert | Beleg |
|---|---|---|
| Weltkartenliste | `portalraum.weltkarten(eigene_nummern, unterwegs)`: sechs Zeilen mit Nummer, Kennung, Name, Status (eigene Welt / fremde Welt / noch nicht bespielbar), Bannerfarbe als Wort, `waehlbar` samt Grund | `src/portalraum.py` |
| Gelaendekaestchen | 20 x 20 = 400 Felder (`portalraum.anzeige_raster`), ein Klick waehlt ein Feld (`_portal_feld_waehlen`), Auswahl steht als `portal_auswahl` in der Ansicht | `src/main.py` |
| Startwelt | **Midgard (d04 = Nummer 4)** statt des alten Vorschlags Armageddon, im Aufbau und beim Laden; Daten in `data/welten.json` (`startwelt`, `weltkarten_spielbar`) | `src/welt.py` (`startwelt_nummer()`), `GameState` |
| Sperre | Weltensprung gesperrt, solange Auftraege unterwegs sind (Hin- oder Rueckreise, auch Handel) - `auftraege.laufende()` mit der SPIELUHR, `_unterwegs_anzahl()` | Daniel, Anhang 2 („ein weltenwechsel ist fuer das dorf gar nicht moeglich solange auftraege einheiten truppen oder sonst was unterwegs ist auch handel z. b.“) |
| Pruefdatei | `tests/test_portal_uebersicht.py` **60/0/0** | Lauf 12:05 |
| Voller Sammellauf | **114 Dateien, 112 gruen, 0 rot, 2 ausgesetzt, 4.132 Pruefungen, 776 s** | `docs/audits/sammellauf_20261101_1205.log` |
| Register | 88 | `docs/PRUEFREGEL_ORIGINAL.md` |

**Was das im Spiel bedeutet:** Das Portal oeffnet mit der Liste Armageddon, Ragnaroek, Utgard, Midgard,
Valhalla, Limbus. Eigene Weltkarten stehen gruen, fremde rot (belegte Bannerfarben aus portal.php 2005),
die vier noch nicht bespielbaren sind als solche benannt und nicht anklickbar. Bespielbar sind zuerst
Midgard (Start) und Valhalla. Unter der Liste liegt das 20 x 20-Kaestchen der aktuellen Welt; ein Klick
waehlt ein Feld an, und die Ansicht sagt ausdruecklich, dass der Dorftransfer erst mit S-6 kommt.

## Nebenbefund, behoben: Nummer und Index waren vermischt

`portalraum` rechnet mit dem Index 0..19, der Spielstand fuehrt die 1-basierte Nummer aus der Kennung
(d04 = 4). Bis S-2a standen beide unvermittelt nebeneinander: `wechsel_erlaubt(20, ...)` lehnte die
zwanzigste Weltkarte ab („Unbekannte Ausgangswelt: 20“), waehrend `_dimensionsname(20)` sie benannte und
der Knopf „20“ sie anbot; „01“ buchte auf Ragnaroek statt auf Armageddon. Die Umrechnung steht jetzt an
EINER Stelle (`nummer_von`, `kennung_von`, `index_von`, `nummer_von_index`) und ist im neuen Prueftest,
Abschnitt 4, belegt. `src/spielschicht.py` fuehrt seinen eigenen Zustand weiter absichtlich 0-basiert -
der Hinweis steht als Docstring dort, damit es niemand „vereinheitlicht“.

## Ziel nach den groben offenen Punkten: eine offizielle spielbare Demo-EXE auf GitHub

**Daniel, 01.11.2026, woertlich:** „sobald die die aktuell groben offenen punkte im spiel bearbeitet
sind möchte ich eine offiziele spielbare demo exe meines spiels auf github hochladen“.

Damit ist der Meilenstein klar und gehoert ab jetzt in jede Uebergabe:

* **Kein Zwischen-Release.** Erst wenn die groben offenen Punkte abgearbeitet sind, wird die Demo
  veroeffentlicht - gemeint sind mindestens **S-2c** (Dorfzentrum ist das Lager), **S-3** (Forschung
  ueber die Bibliothek), **S-4** (Einheitenregel), **S-5** (Weltbild 20 x 20), **S-6** (Dorftransfer),
  **S-7** (Bots sichtbar, kein Angriff) und **S-8** (Bilanz Mana und Reisekosten).
* **Offiziell heisst geprueft:** eine EXE, die startet, eine Partie ohne Absturz erlaubt und deren
  Spielstand sich speichern und laden laesst - belegt mit Sammellauf, EXE-Start und einem
  Spieltest-Verlauf, nicht behauptet.
* **Bekannte Grenze, die in die Release-Notizen gehoert:** der Remote-Stand auf GitHub ist **nicht**
  der Arbeitsstand (zuletzt `954097aa` vom 31.10.). Vor dem Hochladen wird die Reihenfolge
  festgelegt: Arbeitsstand committen, `main` aktualisieren, Version setzen, Release-Notizen
  schreiben, Demo-EXE anhaengen.
* **Teststaende sind keine Spielstaende** (Daniel, Anhang 2: „Aktuelle spielstände sind nur teststände
  zur entwicklung“). Fuer die Demo wird ein frischer Spielstart geprueft, kein alter Teststand.

## Was bewusst NICHT gebaut wurde

* **Gelaende je Feld.** Das Handbuch nennt kein Gelaende je Weltkartenfeld; das Kaestchen zeigt deshalb
  die belegten Bannerfarben und die Auswahl, keine erfundenen Gelaendearten. Gehoert zu S-5, offener Punkt.
* **Der Dorftransfer selbst.** Ein Klick merkt nur ein Feld; uebertragen, Kosten und Postfach kommen mit S-6.
* **Die Limbus-Doppelbedeutung ist weiter offen** (Weltname *und* Raum). Die Anzeige vermeidet die
  Entscheidung: die Liste heisst „Weltkarten“, der umgebende Raum wird nicht benannt.

## Der naechste Schritt

**S-2c: das Dorfzentrum ist das Lager.** Andockstellen: `_render_overview` (heute Dorfzentrum),
`_render_storage` (heute Menuepunkt „Lager“), `wirtschaft.dorf_uebersicht`, `ortsbestand_text(siedlung)`,
`data/buildings.json` -> Eintrag `lager` (`max_je_siedlung` ist heute nicht gesetzt, „ein Lager je Dorf“
muss dort durchgesetzt werden).

**Vor dem Bau zu entscheiden (steht gesammelt in der Uebergabe):** ob das Dorfzentrum als Gebaeude bei
jeder Gruendung mitgesetzt wird (dann vier Startgebaeude statt drei - S-1 und seine 35 Pruefungen ziehen
mit) oder ob es gebaut werden muss.

**Papier bereit, nicht gebaut:** `docs/design/VERBUND_FORSCHUNG_EINHEITEN_TRANSFER_20261101.md`
(46.061 Byte, SHA256 `9815fb27…`, 327 Zeilen) - Entscheidungsentwurf zu S-3 (Forschungsuebernahme),
S-4 (Einheitenpruefung, stationierte Truppen) und S-6 (Dorftransfer), mit Kennzeichnung BELEGT /
VORSCHLAG / UNBEKANNT, einem Pruefplan und acht offenen Entscheidungen in Abschnitt 7. **Selbstauskunft
eines externen Modells:** jede Zahl vor dem Einbau selbst nachpruefen.

**Desktop:** keine Kopien mehr. Die Uebergabe liegt in `docs/UEBERGABE_20261101_1105.md` und
`D:\Arbeiten\Hermes\Uebergaben\20261101_1105\`.

# STAND 01.11.2026, 09:47 - S-1 abgeschlossen: die Gruendung bringt drei Startgebaeude mit

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

## Was in dieser Sitzung gebaut wurde

**S-1 ist fertig und gruen** - der Patch aus `docs/audits/S1_ENTWURF_20261101/` ist angewendet, die
sieben roten Pruefdateien sind einzeln nachgezogen, der volle Sammellauf ist sauber:

| Gegenstand | Wert | Beleg |
|---|---|---|
| Code | `STARTGEBAEUDE_VORLIEBEN`, `_startgebaeude_setzen`, `_startgebaeude_meldung` in `src/main.py`, benutzt an beiden Gruendungswegen (`_erste_siedlung_gruenden`, `GruendungGameState.gruendung_ausfuehren`) | `git diff`, Register 86 |
| Pruefdatei | `tests/test_gruendung_startgebaeude.py` **35/0/0** | Lauf 09:24 |
| Nachgezogene Wachen | 7 Dateien, jede mit Satz und Quelle im Kommentar, keine Wache geloescht | Abschnitt unten |
| Voller Sammellauf | **112 Dateien, 111 gruen, 0 rot, 1 ausgesetzt, 4.125 Pruefungen, 598 s** | `docs/audits/sammellauf_20261101_0931.log` |
| EXE | **46.144.237 Byte**, SHA256 `b2194fc5…`, Start belegt (Kind-PID 11692, Fenster `Nebelseetal Remake`, 95 s stabil) | `sha256sum`, `Get-Process` 09:48 |
| Register | 86 | `docs/PRUEFREGEL_ORIGINAL.md` |

**Was das im Spiel bedeutet:** jede Gruendung - erstes Dorf UND jede Kolonie - setzt Holzfäller
(moeglichst Wald), Steinmetz (moeglichst Huegel oder Berg) und Tempel (moeglichst Nebelsee, sonst
Steppe) auf freie Felder, kostenlos, ohne Siedlerabzug, der Tempel ohne Baukunst. Die Meldung nennt je
Gebaeude Gelaende und Feld und sagt ausdruecklich, wenn das Wunschgelaende fehlt und ein Ersatz
genommen wurde. Startressourcen bleiben 10 Siedler / 100 Holz / 100 Stein.

## Die sieben nachgezogenen Wachen (Beleg fuer die Ruecknahme am 04:02)

Sechs der sieben haengen an EINER gemeinsamen Wache in `tools/gpt_erzeuge_startstaende.py` (sie erzeugt
den Startzustand fuer die GPT-Pruefdateien): `assert s.bevoelkerung == 10.0 and not s.bauten` ist auf
die neue Wahrheit gestellt - zehn Siedler, genau Holzfaeller, Steinmetz und Tempel, je Stufe 1.
`test_produktionskette_ohne_cheats` hatte ihre eigene Zeile und ist ebenso umgestellt. Die uebrigen
Erwartungen waren Zahlen, die auf dem leeren Aufbauzustand beruhten und offen angehoben wurden:
Holz 101 -> 105 und Stein 101 -> 103 je Stunde (Grundertrag 1/h plus Startgebaeude 4/h bzw. 2/h),
25 Stunden 125 -> 225 bzw. 175, Frischstart nach zwei Bauten 90/90 -> 94/92.

## Der naechste Schritt

**S-2b: die Portal-Uebersicht** - oben die Liste der Weltkarten mit Namen, darunter das
Gelaendekaestchen der aktuellen Welt (Daniel, Anhang 3 Frage 30). Danach **S-2c: Dorfzentrum ist das
Lager** (Lagerverwaltung im Dorfzentrum, ein Lager je Dorf - Anhang 1 Abschnitt 2, M-11).

**Erledigt in dieser Sitzung (S-2a, Register 87, Commit folgt):** der Menuepunkt Karten ist weg (die
alte Weltkarte ist stillgelegt und traegt einen Vermerk), und die Anzeige sagt Weltkarte und
Weltensprung statt Dimension - `MENU_ITEMS` hat 16 Punkte, das alte `test_weltkarte` ist als
Zeitzeugnis ausgesetzt, die neue Wache ist `tests/test_weltkarten_anzeige.py` (27/0/0).

**Vorbereitet, noch nicht gebaut:** das Papier des starken Chat-Modells zu Burgen, Wappen und
Weltbild liegt in `docs/design/ASSETS_UND_WELTBILD_20261101.md`; es gehoert zu S-5 und S-7 und ist
dort gegengeprueft einzubauen. Das Assetpaket selbst liegt in
`archiv/eingaben/20261101_burgen_wappen/` (ZIP plus zwei entpackte Kontaktboegen).

**Nebenher offen, von Daniel geliefert:** das Assetpaket `Hermes_Nebelseetal_Assets_Icons.zip`
(2 Kontaktboegen, je 1448 x 1086 px, RGBA: 6 Burgen, 10 Wappen) liegt auf dem Desktop und ist noch
nicht im Projekt. Es gehoert zu S-5 (Weltbild) und S-7 (Bots) - der Auftrag an das starke Chat-Modell
steht in `docs/AUFTRAG_GPT_WELTBILD_UND_ASSETS_20261101.md`.

# STAND 01.11.2026, 09:17 - 35 Fragen beantwortet, Fahrplan neu

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

## Was sich seit 03:32 geaendert hat

**Daniel hat alle offenen Fragen beantwortet** (35 Fragen in sieben Formularen). Die Antworten stehen woertlich in `docs/KONZEPT_WELTKARTEN_UND_BOTS_20261101.md` (Anhang 3) und sind bindend. Die wichtigsten Aenderungen am Modell:

| Punkt | neu |
|---|---|
| Transfer | **Mana**, 500 statt 5.000; Tempel 20/h Nebelsee, 5/h sonst (VORSCHLAG) |
| Bots | **nur Koordinaten**: sechs Bots, je ein Dorf, feste Position, **kein Angriff**, keine Taktik |
| Weltkarten | **sechs belegte Namen** (Armageddon, Ragnarok, Utgard, Midgard, Valhalla, Limbus), bespielbar zuerst Midgard und Valhalla, Start in Midgard |
| Dorftransfer | **ein Dorf je Vorgang**, Einstieg per Klick aufs freie Feld |
| Spionage | Kundschafter-Auftrag, Bericht exakt, gehoert zur Kampfplanungsseite |
| Begriffe | Dimensionen heissen **Weltkarten und Weltensprung** (ab S-2 in der Anzeige) |

**Gebaut wurde in dieser Runde nichts** - Daniel wollte erst alle Antworten und dann die Uebergabe.

## Der naechste Schritt

**S-1 abschliessen.** Der Patch liegt in `docs/audits/S1_ENTWURF_20261101/`; **sieben** Pruefdateien muessen dabei einzeln nachgezogen werden (Liste in der Uebergabe 09:17, Abschnitt 4). Danach S-2 bis S-8 nach dem Fahrplan in Anhang 3.

Guthaben: **3,03 USD** (diese Sitzung hat 1,27 USD gekostet).

# STAND 01.11.2026, 03:32 - Entscheidung 1 gebaut, Bot-Taktik-Modul liegt bereit

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

## Neu seit 02:48

| Paket | Register | Pruefdatei | Sammellauf |
|---|---|---|---|
| **Bot-Taktik-Modul `src/bottaktik.py`** - acht Zustaende, fuenf Taktiken, Gedaechtnis, Koordinaten, Manhattan-Abstand, sichtbare Signale. **Noch nicht von main.py benutzt** (Anschluss = S-7) | 85 | `test_bottaktik` 48/0/0 | 03:22: 111 Dateien, 110 gruen, 0 rot, 1 ausgesetzt, 4.089 Pruefungen, 357 s |
| Modulkarte neu gebaut (50 Dateien) | - | `test_projektpfade` 103/0/0 | - |

## Der naechste Schritt (unveraendert S-1)

Gruendung setzt Tempel, Holzfaeller und Steinmetz samt Startressourcen und nennt die Felder. Einzelheiten in der Uebergabe, Abschnitt 4.


> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen (nichts wird geloescht).

## Was gerade gebaut wurde (Commit folgt in dieser Sitzung, Register 84)

| Paket | Register | Pruefdatei | Sammellauf |
|---|---|---|---|
| **Entscheidung 1: jeder Angriff reist** - ein Kern `_angriff_auftrag_starten`, `_angriff_durchfuehren` entfernt, `_attack`/`_attack_map`/`_auftrag_angriff` starten Auftraege, Kampf erst bei Ankunft | 84 | `test_kampf_einhaengung` 58/0/0, `test_produktionskette_ohne_cheats` 48/0/0, `test_gpt_kampf_botbeute_echte_kasse` 7/0/0, `test_durchspiel` 65/0/2 | 02:39: 110 Dateien, 109 gruen, 0 rot, 1 ausgesetzt, 4.041 Pruefungen, 363 s |
| **Spielspannung und Bot-Taktik als Entwurf** (starkes Modell, 189 Zeilen): Spielschleifen, sieben Spannungsquellen, Zustandsautomat mit fuenf Taktiken, Gedaechtnis, sichtbare Vorzeichen, acht Widersprueche, Top 10 nach Wirkung | - | `docs/design/SPIELSPANNUNG_UND_BOTTAKTIK_20261101.md` | - |

## Der naechste Schritt

**S-1 aus dem Modell sechs Doerfer**: Gruendung setzt Tempel, Holzfischer (Wald) und Steinmetz (Huegel/Berg) und die Startressourcen 10 Siedler / 100 Holz / 100 Stein; die Meldung nennt die Felder. Andockstellen: `_erste_siedlung_gruenden`, `_kolonie_gruenden` (src/main.py), `gelaende.bau_moeglich`, `data/buildings.json` (Tempel-Ausnahme bei der Gruendungssetzung). Neue Pruefdatei; betroffen: `test_startspiel`, `test_durchspiel`, `test_originalkarten_baukasse`.

**Vor S-1 zu entscheiden (Fragen an Daniel, gesammelt):** Transferwaehrung (Mana empfohlen), Bot-Umfang (2-3 Taktiken, 1-3 Doerfer empfohlen), Goetterschutz-Dauer (so lassen und nur anzeigen empfohlen), Kartenziehung (nach dem Dorf-Umbau empfohlen). Bis zur Antwort gilt die Empfehlung, im Code als VORSCHLAG gekennzeichnet.

# STAND 01.11.2026, 01:00 — verbindlich für den Wiedereinstieg

> Dieser Block steht ÜBER den älteren Ständen. Die Angaben darunter (FIX05, FIX04j…) sind
> historisch und nicht mehr die Wahrheit. Alles hier ist gemessen, der Beleg steht daneben.

## Was in der Sitzung 31.10./01.11.2026 gebaut und committet wurde

| Paket | Commit | Register | Prüfdatei | Sammellauf |
|---|---|---|---|---|
| A-1 Mengeneingabe für Ausbildung **und** Ware (Daniels Antwort 1 = B) | `7720e99` | 79 | `test_mengeneingabe` 69/0/0 | 22:57: 107 Dateien, 106 grün, 0 rot |
| A-3 Dorfübersicht rechts der Karte + Siedler-Schalter (Antwort 2 = A, Antwort 5 = B) | `fe97182` | 80 | `test_dorfuebersicht` 24/0/1 | 23:22: 108 Dateien, 107 grün, 0 rot |
| A-6 Siedler-Reserve sichtbar und gewarnt | `df6da4d` | 81 | `test_siedler_warnung` 29/0/1 | 23:52: 109 Dateien, 108 grün, 0 rot |
| A-2 Original-Gebäudemotive auf der Karte | `97c1301` | 82 | `test_gebaeude_motive` 43/0/1 | 00:16: 110 Dateien, 109 grün, 0 rot, 4.022 Prüfungen |
| Bildquellen gesichtet (A-2/A-4) | `8835f0a` | — | — | — |
| Weltkarten-Konzept (Lords Mobile) aufgenommen und abgeglichen | `a037d5b` | — | — | — |
| A-5 Designkonzept als **Papier** vorgelegt | `b6a886f` | 83 | — | — |

Letzte EXE: `46.144.440 Byte`, SHA256 `6030147d…`, Startbeleg: Prozess 53 s stabil, Fenster mit
Titel. **Offen:** die Sichtprüfung des Passworttors (Tk liefert keinen UIA-Baum).

## Daniels Entscheidungen aus dem Formular (31.10.2026) — bindend

1. A-1 Umfang = **B**: Ausbildung **und** Ware-Herstellung. *gebaut*
2. A-3 Ort = **A**: rechte Spalte der Siedlungskarte. *gebaut*
3. A-4 = **A**: aus den Handbuchbildern schneiden. **Erledigt durch Befund:** die 244
   Handbuchbilder enthalten **keine** Rohstoff-Icons (nur Gebäudemodelle). Die einzige echte
   Quelle ist die Rohstoffleiste auf `docs/original/karten/gamestar_nebelseetal_1838855_full.jpg`
   (20–30 px, unscharf). **Neue Entscheidung nötig:** als Vorlage nachzeichnen (Empfehlung)
   oder A-4 nach der Demo schieben.
4. A-5 = am Original orientiert, benutzerfreundlich, jedes Menü und jeder Button mit genug Platz.
   **Papier liegt vor** (`docs/design/SIEDLUNG_KONZEPT_20261101.html`, Bild daneben), Abnahme offen.
5. Siedler-Mechanik = **B**: Bauten binden keine Siedler mehr. *gebaut als Schalter*
   `data/bausiedler.json` (`aktiv: false`). **Achtung, bewusste Abweichung vom Original:**
   Holzfäller, Steinmetz und Jäger kosten laut `data/baupreise.json` je 1 Siedler (Screenshot
   1838857). `aktiv: true` stellt das Original wieder her.

## Der EINE nächste Schritt: Entscheidung 1 — der Sofortangriff reist

Daniels Entscheidung (31.10.2026): „Sofortangriff **reist** wie der Auftrag; der Knopf
‚Angreifen' entfällt.“ Heute gibt es **zwei** Wege:

* `NebelseetalApp._angriff_durchfuehren` (~Z. 6215) — **ohne** Reisezeit, direkt am Ziel.
  Wird aufgerufen von `_attack(bot)` (~Z. 6472) und `_attack_map(map_id)` (~Z. 6274).
* `NebelseetalApp._auftrag_angriff(bot)` (~Z. 6502) — **mit** Reisezeit, Rückkehr und Bericht
  über `state.auftrag_starten("angreifen", …)`.

**Ziel:** nur noch der Auftragsweg. Andockstellen: `_attack`, `_attack_map` (beide auf den
Auftragsweg umstellen), ein neuer Auftragsweg für **Kartenangriffe** (`_attack_map` hat heute
kein Gegenstück in `_auftrag_*`), und `_angriff_durchfuehren` stilllegen.

**Wichtig vor dem Bauen:** drei Prüfdateien hängen heute am Sofortpfad und müssen mitwandern —
`tests/test_kampf_einhaengung.py` (prüft `_angriff_durchfuehren` als EINEN Kampfweg),
`tests/test_gpt_kampf_botbeute_echte_kasse.py` und
`tests/test_produktionskette_ohne_cheats.py`. Neue Wachen nötig: Angriff kostet Reisezeit,
Truppen sind während des Marsches nicht doppelt verfügbar, kein Pfad ohne Marsch mehr.

## Was außerdem offen ist

* **Vier unklare Gebäudemotive** (Nummern 2, 3, 4, 6 aus `D:	mp\motivbogen.png`): Daniel ordnet
  zu, dann nur `data/gebaeude_motive.json` ändern (`eingebaut: true`, `gebaeude: <id>`).
* **A-5 bauen** erst nach Abnahme des Papiers.
* Weltkarten-Konzept: Abgleich liegt in `docs/KONZEPT_ABGLEICH_20261101.md`; Reihenfolge
  vorgeschlagen (Spionage → Start-/Ziel-Schnappschuss → Portalversetzung → Frühwarnung),
  **nichts freigegeben**.

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

> **GELTENDER STAND 31.10.2026, 20:45 (Hermes).** Diese Ueberschrift ist der Wiedereinstiegspunkt, den
> `tools/zieluebergabe.py` liest; die Liste darunter ist **HISTORIE der GPT-Runde vom 28.10.2026** und
> **nicht mehr** der Fahrplan. Geltend: Hermes fuehrt das Projekt seit 30.10.2026 zurueck.
> **Fertig und committet (31.10.):** F-04 (`52b5a51`), Spielbalancing-Test (`1cd799b`), Befund Siedler/Bots
> (`4e68de8`), **Nahrungsverbrauch je Einheit** (`8db75a6`, Register 69, 52 Pruefungen, Sammellauf 20:13 mit
> 103 Dateien/102 gruen/3.756 Pruefungen), **Balancing-Test Teil 2 - Karten, Doerfer und Pech** (`bca75e1`,
> Register 71, Werkzeug `tools/balancing_karten.py`, Gates G-8/G-9).
> **Fertig seit dem letzten Stand:** **Wagenbau-Kapazitaet** (Register 73) - `data/karrenkapazitaet.json`,
> Bonus +10 % je Stufe (Deckel Stufe 10 = Faktor 2,0), EINE Rechnung `einheiten.ladung_der_gruppe`,
> Stufen aus `GameState.forschungs_stufen()`, Pruefdatei 44/0/1, Sammellauf 20:58 (104 Dateien,
> 103 gruen, 3.801 Pruefungen), EXE `aa2c48c6...`.
> **Fertig seit dem letzten Stand:** **Nahrungsnot-Sperre** (Register 70/74, Commit `e20b4c6`) und die
> **Schenkungs-Botschaft** im Nachrichtenmenue samt Aufstockung von Slot 1 (Register 77, Commit `11746b5`).
> **Daniels Spielbericht vom 31.10.2026 liegt vor** und ist der neue Fahrplan:
> `docs/ANFORDERUNGEN_DANIEL_20261031_SPIELBERICHT.md` mit sechs Paketen **A-1 bis A-6** (Register 78).
> **Reihenfolge: A-1 Mengeneingabe fuer Einheiten -> A-3 Dorfuebersicht -> A-6 Siedler-Vorwarnung beim
> Bauen -> A-2 Original-Gebaeude-Icons -> A-4 Ressourcen-Icons -> A-5 Designkonzept Siedlung.**
> **Danach (bestehend):** Sofortangriff reist -> Kampfplanungsseite -> F-03 -> F-05/F-06 -> F-07/F-13 ->
> F-11 -> P3.4/P3.6 -> P4 -> Aufraeumen -> P5 -> P1 -> F-12. **Bots spaeter** (Register 72);
> **Kartenziehung = C** entschieden, nicht gebaut (Register 75). Offen fuer die Messung:
> `tools/balancing_messung.py` uebergibt keine Forschungsstufen, G-2/G-6 mit Wagenbau neu messen.
> **Ziel:** erste spielbare DEMO als Windows-EXE auf GitHub (Kriterien in Abschnitt 4 des Spielberichts).
> Nach JEDEM Schritt verpflichtend: Registereintrag in `docs/PRUEFREGEL_ORIGINAL.md`, Protokollzeile in
> `docs/ENTWICKLUNGSPROTOKOLL.md`, Einzeltest **und** voller Sammellauf
> (`python -X utf8 tools/sammellauf.py`), neue EXE mit Startpruefung, dann EIN Commit.
> **Offene Fragen (Auswahlformular):** 7-9 beantwortet (Register 70), **Frage 10** offen (Kartenziehung:
> freie Wahl / Zufall / Wahl aus drei gezogenen Karten).

**Historisch (28.10.2026, GPT-Runde - nur noch Nachweis, kein Auftrag):**

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
