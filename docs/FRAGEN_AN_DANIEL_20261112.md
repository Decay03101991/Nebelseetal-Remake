# Fragen an Daniel — gesammelt in der Nacht 12./13.11.2026 (Sitzung 41)

**Regel:** Fragen werden **gesammelt** und bei Daniels Rückkehr **in EINER Runde** vorgelegt —
nicht einzeln, nicht mit Zeitablauf (Arbeitsregel 7; Daniels Wort seit Sitzung 39).
Je Frage: **Messlage · Auswirkung · Vorschlag zuerst**. Freie Antwort ist immer möglich.

---

## 1. Sichtprüfung des DPI-Umbaus (offen aus Sitzung 40, F-51)

**Messlage:** `docs/audits/dpi_vorher_weich_20261112.png` gegen `dpi_nachher_scharf_20261112.png`.
Bewusst: Schirm 1920 × 1080, k = 1,2512, Fenster 1560 × 940, Fläche 1127 × 764, Feld 64.
Unbewusst: 1536 × 864, Fläche 1037 × 589, Feld 57.

**Auswirkung:** Bleibt der Umbau, ist alles scharf und physisch kleiner. Wird er zurückgenommen,
ist alles weich und größer. Bis zu deinem Urteil wurde **nichts** geändert.

**Vorschlag:** so lassen (scharf), weil Schrift und Kanten bei 125 % Skalierung sonst unscharf
skaliert werden — **deine** Entscheidung nach den zwei Bildern.

**Deine Frage dazu:** scharf und gut · scharf, aber hässlich · zu klein/groß?

## 2. Löschen von Prüfdateien (F-67 erlaubt Umstellen, nicht Löschen)

**Messlage:** 230 Prüfdateien, 9.905 Prüfungen, 1.380 s seriell. 46 Dateien haben keine
Messwert-Historie (34 davon alte `gpt_`-Dateien). Seit heute Nacht schreibt der Sammellauf eine
Zeile je Datei (`docs/audits/laeufe.jsonl`), damit ist die Lücke im Aufzeichnen zu.
Kandidaten für „nur bei Änderung“ oder Zusammenlegen stehen in der Antwort Nr. 16, Punkt 7.

**Auswirkung:** Löschen spart Laufzeit, kann aber eine alte Prüfung mitnehmen, die noch etwas
Gültiges absichert.

**Vorschlag:** **nichts löschen**. Erst eine volle Runde mit der neuen Laufzeilen-Ablage, dann
Antrag je Datei mit Prüfnamen-Abgleich (mindestens 90 % der Eigenschaften muss die neue Datei
abdecken). Ich lege den Antrag vor, du entscheidest.

## 3. Die 46 alten Dateien einmal einzeln sichten (Claudes C10)

**Messlage:** 34 der 46 sind `gpt_`-Dateien aus den Fixrunden vom 31.10. Ob sie noch etwas Gültiges
prüfen, weiß niemand — sie laufen im Sammellauf mit, schreiben aber nichts in den Index.

**Auswirkung:** Sichtung kostet einmalig die Summe ihrer Einzeldauern (unbekannt, geschätzt
5–10 Minuten), bringt danach Klarheit und möglicherweise Streichkandidaten.

**Vorschlag:** Sichtung nach der ersten vollen Runde automatisch mitlaufen lassen
(`tools/einzeln_sichten.py`) und dir eine Tabelle vorlegen — keine Entscheidung ohne dich.

## 4. `main:*` in den Prüfstand-Köpfen (neu durch M1)

**Messlage:** 184 von 230 Dateien nennen `main`. Damit die Auswahl (M2) nicht 184 Dateien zieht,
steht in ihren Köpfen `main:*` = „irgendeine Funktion in `main.py`“. Sobald eine Datei angefasst
wird, wird der Eintrag auf die **echte** Funktion verengt (z. B. `main:_render_settlement_map`).

**Auswirkung:** Solange `main:*` steht, zieht eine Änderung an `main.py` diese Dateien weiterhin
mit — die Auswahl ist also heute schon ehrlich, aber noch nicht fein.

**Vorschlag:** so lassen und beim Anfassen verengen (Claudes C6: „beim Berühren herausziehen“).
Keine Aktion nötig, nur zur Kenntnis — **Widerspruch willkommen**.

## 5. Werkstatt-Zuordnung: zwei Quellen (Befund B4 der Nachrechnung Nr. 16)

**Messlage:** `data/items.json` führt je Ware ein Feld `werkstatt` (Schmiede 8, Nähstube 5,
Bogner 4), und `src/werkstatt.py` liest **nur** diese eine Stelle. `data/warenrezepte.json` hat
das Feld noch nicht. F-64 sagt: Feld je Rezept. Ein Handeintrag dort macht aber
`test_warenrezepte` rot (die Datei muss stückweise der Ableitung entsprechen).

**Auswirkung:** Wird das Feld nur von Hand eingetragen, gibt es zwei Listen, die auseinanderlaufen
können — genau die Fehlerart, die „verbund-konsistenz“ verhindern will.

**Vorschlag:** das Feld **aus der Ableitung** schreiben (`tools/warenrezepte_ableiten.py` kennt die
Werkstatt bereits) **plus** eine Wache, die beide Seiten vergleicht. Damit gibt es eine Quelle und
zwei Ansichten. Sagst du ja, baue ich es so.

## 6. Völkerfarben: Burgbilder oder `FRAKTIONEN_WELTEN.md`?

**Messlage:** Zwei Quellen widersprechen sich. `FRAKTIONEN_WELTEN.md` (unser Projekt) sagt Trolle
dunkelrot/schwarz und Ghule grün/knochenweiß. Claudes Angaben „Trolle weiß-gold, Ghule violett“
stammen nach seiner Auskunft aus **deiner** Beschreibung der Burgbilder.

**Auswirkung:** F-71 sagt bereits „die Burgbilder geben die Farbe vor“ — dann wird
`FRAKTIONEN_WELTEN.md` angepasst, nicht die Bilder. Bestätige bitte, dass das so gemeint war.

**Vorschlag:** Burgbilder führen, Datei anpassen (F-71). Ich baue es erst, wenn du es bestätigst.

---

## Antworten, die ich in der Nacht **nicht** brauche (nur zur Kenntnis)

- **Nachrechnung Nr. 16:** Werteblock vollständig bestätigt, Block 5 = 370 (meine 380 war falsch),
  vier Befunde (B1–B4) — alle vier ändern den Bauweg, keine deiner Entscheidungen.
- **F-57 gebaut:** Abstand = gemessener Rollbalken (21 px), S = 448, Wachen grün.
- **F-60 gebaut:** `dorfzentrum_kennzahlen` in der Ökonomie, Wache 23/0/0.
- **M12.0 gebaut:** der Sammellauf schreibt eine Zeile je Datei — die 46 blinden Flecken sind zu.
- **M11 gebaut:** `docs/FAKTENBLATT.md` aus `data/` (17 Waren, 17 Rezepte mit je 1 Zutat,
  28 Einheiten, 21 Forschungen, 20 Gebäude, Werkstätten 8/5/4) plus Auftragsprüfung.

## 7. Soll `test_e2e_wege` als neunte Datei in die Stufe T4? (neu aus dem vollen Lauf)

**Messlage:** Der volle Lauf 13.11.2026 (seriell, jede Datei allein) zeigt: `test_e2e_wege` braucht **186,2 s** und ist damit die teuerste Prüfdatei überhaupt — teurer als jede der acht T4-Dateien. In Paket 15b stand sie mit 361,7 s unter Last, wurde dort aber nicht zu den T4-Kandidaten gezählt. Die übrigen acht sind allein deutlich schneller als gedacht: `test_produktionskette_ohne_cheats` 81,8 s statt 301,2 s, `test_handelspunkte` 25,7 s statt 109,7 s.

**Auswirkung:** T4 dauert heute rund 20 Minuten (1.216 s für alle 238 Dateien). Mit `test_e2e_wege` als neunter Datei wird der Lauf vor einer EXE kaum länger (die Datei läuft dort ohnehin mit), aber sie wird **bewusst** Teil der verbindlichen Stufe statt „irgendwo in T3“.

**Vorschlag:** `test_e2e_wege` als **neunte** Datei nach T4 (F-67 nennt acht — deshalb frage ich). Die Stufe selbst bleibt HART vor jeder EXE.

---

## ANTWORTEN (Daniel, 13.11.2026, einzeln gestellt und angeklickt)

| # | Frage | Antwort | Folge |
|---|---|---|---|
| 1 | DPI-Umbau | **„Scharf und gut — so lassen“** | F-73: F-51 bleibt endgültig. Bilder im Chat gezeigt, danach entschieden. |
| 2 | Prüfdateien löschen | **„Nichts löschen — erst Prüfnamen-Abgleich je Datei“** | F-74: F-67 bleibt; Streichen nur mit Antrag und ≥ 90 % Abdeckung. |
| 3 | 46 alte Dateien sichten | **„ja und prüfe dabei ob sie so wie sie prüfen noch brauchbar sind oder geändert werden müssen oder irgendwo sinnvoll integriert werden können“** | F-75: Sichtung mit DREI Urteilen je Datei (brauchbar / ändern / integrieren), Tabelle vorlegen. |
| 4 | `main:*` in den Köpfen | **„So lassen — beim Anfassen verengen“** | F-76: Übergangsform bleibt. |
| 5 | Werkstatt je Rezept | **„Es gibt ja keine werkstatt an sich … Ingame gibt es Menüpunkte für diese Werkstätten als Bogenmacher oder Schmiede … kein menüpunkt werkstatt oder werkstätten nötig“** | F-77: **kein Menüpunkt „Werkstätten“**; nur die Gebäude (Schmiede, Bogenbauer, Nähstube). Das Rezeptfeld bleibt auf die Gebäude-Kennung bezogen. |
| 6 | Völkerfarben | **„Die burgbilder kann ich vorerst nicht ersetzen aber das ist der einzige grund warum ich sie festlege. Heißt es muss geschichte und stil den burgen angepasst werden. Auch Wappen usw“** | F-78: **Burgbilder sind fest**; Geschichte, Stil **und Wappen** werden ihnen angepasst. `FRAKTIONEN_WELTEN.md` in dieser Sitzung angepasst (Trolle weiß-gold, Ghule violett). |
| 7 | `test_e2e_wege` nach T4 | **„Ja — als neunte Datei nach T4“** | F-79: gebaut — T4 hat jetzt neun Dateien, `PRUEF_STUFE = 4`. |

---

# SITZUNG 42 (13.11.2026, nachts) — Fragen aus dem Dorfzentrum-Umbau und der Prüfstands-Sichtung

**Regel unverändert:** gesammelt, in EINER Runde, je Frage Messlage · Auswirkung · Vorschlag zuerst.

## A. Das Dorfzentrum — Sichtprüfung (die wichtigste)

### F-86 Sichtprüfung des neuen Dorfzentrums

**Messlage:** drei Belegbilder, alle am 13.11.2026 aus dem laufenden Fenster aufgenommen:
`docs/audits/dorfzentrum_20261113_01xx.png` (Reiter Lager), `dorfzentrum_werkstaetten_20261113.png`,
`dorfzentrum_einheiten_20261113.png`. Gebaut ist Nr. 16 Teil A: links die Spalte (Kopf mit
Kennzahlen, nächster Schritt, Ort, Aktionen, Auswahl, Hinweis), rechts die Arbeitsfläche mit den
drei Reitern Lager / Werkstätten / Einheiten, 18 Kacheln zu 185 × 72 px (DPI-bewusst 206 × 83).

**Auswirkung:** Bis zu deinem Urteil bleibt es so. Dein Befund entscheidet, ob die Größen
(Kacheln, Schriften, Blockhöhen) stimmen oder nachgezogen werden.

**Vorschlag:** so lassen — aber sich die drei Bilder ansehen, vor allem die Kacheln (V_0.0.4 war
„besser, aber immer noch nicht übersichtlich und schön genug“).

**Deine Frage dazu:** gut · zu klein · zu eng · anders?

### F-87 Zieht die Ansicht bei Fenstergröße nicht nach — reicht das?

**Messlage:** Die Arbeitsfläche R hängt an der Fensterbreite; die Kacheln werden beim Neuaufbau
gesetzt, nicht bei jedem Fensterzug (der frühere Nachlauf `_lager_nachziehen` ist mit der alten
Kachelform entfallen). Im Spiel ist das Fenster fest (1560 × 940 bewusst / 1446 × 744 unbewusst),
darum fällt es dort nicht auf. Belegt als Befund in `tests/test_lager_kacheln_b4.py`.

**Auswirkung:** Wer das Fenster zieht, sieht die Kacheln in der alten Größe, bis die Ansicht neu
gebaut wird. Kein Datenfehler, nur Darstellung.

**Vorschlag:** so lassen (das Fenster ist fest) — oder einen Nachlauf wie in der Siedlungsansicht
nachrüsten, wenn du das Fensterziehen im Betrieb nutzt.

### F-88 Das Lage-Band steht jetzt IM Block Auswahl

**Messlage:** Deine Entscheidung T7 (11.11.2026: Forschung, Götterschutz, Wallbau als eigene Zeile)
ist unverändert gültig; Nr. 16 Teil A kennt diese Zeile nicht. Ich habe sie oben in den Block
„Auswahl je Reiter“ gelegt, damit die sieben Blöcke und Block 5 als Rest erhalten bleiben. Wache
`test_lage_band` 12/0/0.

**Auswirkung:** Kein Block kommt hinzu, keine Zahl aus Teil A verschiebt sich. Optisch sitzt das
Band jetzt über den Angaben zur gewählten Ware.

**Vorschlag:** so lassen, bis du es siehst — sagst du „eigener Block“, bekommt es Block 8 und
Block 5 wird um 60 px kleiner.

## B. Prüfstand: Sichtung und Streichkandidaten (F-75 / F-74 sind gemessen)

### F-80 Acht Dateien mit eigener Prüfzählung auf `harness` umstellen?

**Messlage:** `test_gebaeude_menue_und_meldungen`, `test_gpt_originalkarten_historische_info`
(**0 Prüfungen**), `..._katalog`, `test_navigation_ebenen`, `test_opus_lauf_arbeitsordner`,
`test_projektpfade`, `test_rueckmarsch`, `test_textqualitaet` zählen selbst und schreiben keine
Messwerte. Beleg: `docs/SICHTUNG_ALTER_PRUEFDATEIEN_20261113.md`, Abschnitt 1.

**Auswirkung:** Umstellen kostet einmalig Arbeit, bringt Messwerte und den Befundkanal. Keine
Prüfung wird dabei entfernt.

**Vorschlag:** ja, in einem Paket, jede Datei einzeln grün gefahren.

### F-81 Acht Paare zusammenlegen (Name für Name übernehmen, dann streichen)?

**Messlage:** fix04e → fix04f, fix04b → fix04, baukasse / prueflauf_ehrlich / waren_icons →
fixrunde_ortslager, schild_fix04i → profile_login, spielstand_gui_fix04h → spielstandarchiv_fix04g,
wall_gui → wallsystem. Beleg: Sichtung, Abschnitt 2.

**Auswirkung:** 8 Dateien weniger, rund 100 s weniger Laufzeit je voller Runde (Schätzung aus
Paket 15b). Risiko: eine Prüfung geht verloren, wenn beim Übertragen geschludert wird.

**Vorschlag:** ja — aber erst nach F-74 und erst nach der nächsten vollen Runde mit Laufzeilen.

### F-82 `test_gpt_originalkarten_historische_info` hat 0 Prüfungen

**Messlage:** 76 Zeilen, läuft ohne eine einzige Zusicherung durch — ein grüner Lauf, der nichts
behauptet. Gegenstand laut Kopf: historische Karteninfos werden nie als Gratisrohstoffe genutzt.

**Auswirkung:** Die Datei täuscht Sicherheit vor. Füllen kostet eine Stunde, Aussetzen kostet
nichts, lässt die Lücke aber offen.

**Vorschlag:** füllen (der Gegenstand ist wertvoll) — oder ausdrücklich als ausgesetzt kennzeichnen.

### F-83 Prüfnamen-Abgleich auf den geprüften Gegenstand umstellen?

**Messlage:** Alle vier Streichkandidaten erreichen die 90-Prozent-Regel nicht: `test_ressourcenleiste`
9,5 % (4 von 42), die anderen drei **0 %**. Grund: Prüfnamen sind freie deutsche Sätze, zwei Dateien
formulieren denselben Gegenstand fast immer anders. Beleg: `docs/PRUEFNAMEN_ABGLEICH_20261113.md`.

**Auswirkung:** In der jetzigen Form erlaubt die Regel nie eine Löschung — auch dann nicht, wenn
inhaltlich alles doppelt wäre. Sie misst Formulierung statt Doppelung.

**Vorschlag:** ja, zusätzlich auf den Gegenstand stützen (Funktion oder Datenfeld je Prüfname) und
die 90 Prozent darauf rechnen.

### F-84 Die 42 Prüfnamen von `test_ressourcenleiste` einzeln sichten?

**Messlage:** Einziger Fall mit echter Nähe: `test_ressourcenleiste_t08` (70 Prüfungen) deckt
inhaltlich 4 von 42 Namen. Die alte Datei prüft also Dinge, die T08 nicht prüft.

**Auswirkung:** Sichten kostet eine halbe Stunde; danach weiß man, ob die vier bis zehn fehlenden
Namen in T08 gehören.

**Vorschlag:** ja, ohne die alte Datei zu löschen.

### F-85 Drei Kandidaten endgültig von der Streichliste nehmen?

**Messlage:** `test_ansicht_hintergrund` (71 Prüfnamen, Panorama/Schleier/Kastenoptik),
`test_bot_wappen` (22, Wappen der fünf Bots) und `test_dorfzentrum_ist_lager` (79, Entscheidung S-2c)
decken Gegenstände ab, die keine andere Datei prüft — Deckung 0 %.

**Auswirkung:** Von der Liste nehmen beendet die Diskussion; drauf lassen kostet nur ein Wort.

**Vorschlag:** ja, alle drei streichen von der Liste (die Dateien bleiben!).

## C. Offen aus Sitzung 41 (unverändert)

- **F-78 Wappen:** Die Burgbilder sind fest, Geschichte und Stil folgen ihnen — `FRAKTIONEN_WELTEN.md`
  steht (Trolle weiß-gold, Ghule violett), die **Wappen unter `assets/icons/wappen/` sind noch nicht
  geprüft**. Vorschlag: als nächstes Bildpaket, sobald du die Burgbilder bestätigst.
- **F-72 / C3 und C7:** freigegeben, **nicht gebaut** (`SKILL.md` teilen; Regel 2 um gekennzeichnete
  Startwerte ergänzen). Beides sind Regeländerungen — Protokoll, Hash, Rückrollweg nach Arbeitsregel 9.
  Vorschlag: in einer eigenen Sitzung, nicht zwischen zwei Bauaufträgen.
- **M3 bis M10:** bewusst nach F-62 zurückgestellt. `T2` ist mit 202 Dateien zu groß für den
  häufigen Lauf; bis die Dauern aus `laeufe.jsonl` belastbar sind, gilt T1 plus die Auswahl aus M2.
- **Der Portalsprung (F-70)** und die **Dorfzentrum-Sichtprüfung** stehen weiter offen (F-86 oben).

---

# SITZUNG 43 (13.11.2026, morgens) — der Befund vor der Sichtprüfung

**Regel unverändert:** gesammelt, in EINER Runde, je Frage Messlage · Auswirkung · Vorschlag zuerst.
Alles hier ist gemessen, nicht umgebaut (`docs/BEFUND_DORFZENTRUM_20261113_0820.md`).

## D. Das Dorfzentrum

### F-86a Die drei Belegbilder, die du beurteilen solltest, sind veraltet

**Messlage:** `dorfzentrum_20261113_01xx.png` (01:41) und die zwei Bilder von 01:46 sind **älter als
der Code, den sie zeigen sollen**: die Ansicht wurde 01:47 committet (`1d11e51`), die
Regressionen-Runde lief 02:41 (`5e40828`). Im alten Einheiten-Bild ist die rechte Bestandsspalte am
Fensterrand abgeschnitten — der Fehler, den `5e40828` behoben hat. Neu liegen neun Bilder aus dem
echten Fenster (1560 × 940, DPI-bewusst): `<reiter>_fenster_0815.png`, `<reiter>_spalte_sicht_0815.png`,
`<reiter>_arbeitsflaeche_0815.png` für Lager / Werkstätten / Einheiten.

**Auswirkung:** Ein Urteil über die alten Bilder wäre ein Urteil über einen Stand von vor 01:47.

**Vorschlag:** die neuen Bilder ansehen — und dabei F-89 im Blick halten, denn dort steht ein
gemessener Fehler, der das Aussehen stärker bestimmt als jede Kachelgröße.

**Deine Frage dazu:** die neuen Bilder als Grundlage nehmen? (ja / nein)

### F-89 Die linke Spalte rollt — der Block „Hinweis“ liegt außerhalb des Fensters

**Messlage:** `_dz_leinwand.yview()` = **(0.0, 0.665)**. Die Spalte ist **448 × 1149** hoch, das
Sichtfenster **448 × 764** — also 385 px unsichtbar. Der Block **`hinweis` steht auf y = 1061** und ist
ohne Rollen überhaupt nicht zu sehen; der Block **`auswahl` ist 699 px hoch**, obwohl nur das Lage-Band
darin steht. Gegenprobe im Worktree auf `9a8fbc2` (01:59): yview (0.0, 1.0), Blöcke 64/62/72/64/364/78,
`hinweis` auf y = 676 — **alles sichtbar.** Ursache: `5e40828` hat in `_dz_rest_verteilen` das
`update_idletasks` entfernt (richtig); `winfo_reqheight()` eines **Frames** mit gepackten Kindern liefert
aber 1, solange die Geometrie nicht gerechnet ist (bei **Labels** steht sie sofort). `_dz_block_hoehen`
notiert deshalb 1/1/1/1/699/1, und Block 5 bekommt den Rest von fast der ganzen Spalte.

**Auswirkung:** Die Ansicht sieht voller aus, als sie ist: unten ein großer leerer Kasten (Block
Auswahl), und der erklärende Hinweis fehlt. Das ist unabhängig vom Geschmack Nacharbeit — und es ist
genau die Art Fehler, die dein V_0.0.4-Urteil („nicht übersichtlich und schön genug“) beschreibt.

**Vorschlag:** reparieren, und zwar so, dass die Fehlerklasse verschwindet:
**(a)** die sechs Blöcke in ein `grid` legen und Zeile 5 `weight=1` geben — dann rechnet Tk den Rest
selbst, ohne Handmessung. *(b)* als kleiner Eingriff: `_dz_rest_verteilen` an ein `<Configure>` der
Spalte hängen und beim zweiten Durchlauf rechnen. Ich empfehle **(a)**, halte aber (b) für den
kleineren Schritt, wenn du das Raster nicht anfassen willst.

**Deine Frage dazu:** (a) grid, (b) Nachlauf — oder erst nach deinem Blick auf die Bilder?

## E. Kleinere Maße, die von der Übergabe abweichen (nur zur Kenntnis, nichts geändert)

- **Kachelhöhe 82 statt 83 px** (`dorfzentrum.masse` liefert 82, die Übergabe nennt 83).
- **Arbeitsfläche 638 px breit, verlangt 658** — 20 px fehlen; die dritte Kachelspalte passt gerade
  noch (3 × 206 + 2 × 10 = 638), ihr Text liegt am Rand.
- **Block „Aktionen“ verlangt 1229 px** bei 448 verfügbar — der Text wird beschnitten. In `9a8fbc2`
  genauso, also kein neuer Fehler, aber sichtbar.

**Vorschlag:** mit der Spaltenreparatur zusammen entscheiden, nicht einzeln.
