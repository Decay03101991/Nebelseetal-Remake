# KONTEXT-PAKET — Nebelseetal Remake (Stand 06.10.2026, 00:36 · Zeiten mit `date` geholt)

**Diese Datei ist die Übergabe. Lies SIE zuerst (≈ 12 KB) und sonst nur, was hier als Zeiger steht —
`docs/PROJEKT_STAND.md` (69 KB) und `docs/ENTWICKLUNGSPROTOKOLL.md` (93 KB) sind Nachschlagewerke,
keine Einstiegslektüre.** Projekt: `D:\Arbeiten\Nebelseetal_Remake` (bash/MSYS, `python -X utf8`).
Ziel: fertige, fehlerfrei spielbare, passwortgeschützte Einzelspieler-`.exe` (Handbuch 2009 = Wahrheit).

---

## 1. Belegter Ist-Stand

| Was | Beleg |
|---|---|
| **Sammellauf** | **3986 bestanden · 0 Fehler · 22 Befunde · 52 Dateien** (00:2x; `…/cache/scratch/sammellauf.py`, 134 s) |
| **Arbeitsbaum** | **sauber** (`git status --short` leer), letzter Commit **`01fe939`** (Teil 7a: Gratisgewinn gesperrt) |
| **`.exe`** | **14.641.733 Byte**, SHA256 `524d6260e28daf74…`, Dateizeitstempel **00:27:57** — **GEBAUT, ABER NICHT STARTPGEPRÜFT** (die Prüfung hing in der Freigabe); Vorgängerfassung gesichert (`…\cache\scratch\exe_alt_0027_vor_teil7.exe`, 14.640.433 Byte). Prüfskript: `…\cache\scratch\exestart\startpruefung_1006_0029.ps1` |
| **Startprüfung** | aus `…\hermes\cache\scratch\exestart` (anderer Ordner, Skript `startpruefung_1006_0029.ps1` — **noch nicht gelaufen**): Fenstertitel **„Nebelseetal Remake"**, antwortet bei **+10/+20/+40 s**, **0** Fehlerberichte (WerFault), danach **0 offene Spielprozesse**, Startordner leer |
| **Sicherung** | `docs/SICHERUNGEN.md` — 16 führende Papiere mit Prüfsummen (00:35, projektunabhängige Kopie unter `D:\Arbeiten\Hermes\Nebelseetal_Protokoll\`) |
| **Zielregister** | nur **diese** Sitzung `20261005_212201_8bd3fb` aktiv (**0/20 Takte**), **kein fremdes aktives Ziel** (`--pruefen` rc=0); die Vorgängersitzung `20261005_201518_d2b523` ist auf `cleared` gesetzt |
| **Kosten** | **Der Tag ist umgesprungen:** am 05.10. endete die Messung bei **7,25 EUR = ÜBER_LIMIT**; der **06.10.** steht bei **0,65 EUR / 4,00 EUR** (0,73 USD), Rest **+3,35 EUR**. **Daniel hat den Auftrag um 20:20 freigegeben** (nur `deepseek-flash`, kein teures Modell, keine Kinder, **1,00 USD DeepSeek bleiben als Reserve**). Anteil der Sitzung am 05.10.: **+0,57 EUR** (6,68 → 7,25); am 06.10. bisher **+0,65 EUR**. Maßgeblich ist DeepSeeks Kontostand (Daniel liest ab) |

`git log --oneline -3` · `git status --short` · `python tools/zieluebergabe.py --pruefen` → alles in Sekunden.

## 2. Der EINE nächste Schritt

**Schritt 9 läuft — Teil 6 ist vollständig fertig, in Teil 7 ist der Gratisgewinn beim Handel gesperrt; offen sind der bestätigte Kaufvertrag (Teil 7b), die Startprüfung der aktuellen `.exe` und danach Teil 8 (Migration).** Der
Auftraggeber hat „Stück für Stück" entschieden: nach JEDEM Teil Einzeltest + einmal Sammellauf +
Protokollzeile + kleiner Commit.

**Teil 6 ist FERTIG (05.10.2026): Ortslager, Anzeige, Transport, Gründung, aktiver Ort, eine
Spieluhr je Ort samt Ware, Ausbildung UND Forschung vor Ort.** Belege: `test_oekonomie_einhaengung`
**312/0/1**, Sammellauf **3979/0/22** über 52 Dateien, `.exe` startgeprüft — Commits `ad12376`
(6a), `0e4a08a` (6b/c), `35e1bd1` (Forschung), `7e83d42` (exe).

**Der NÄCHSTE Schritt: Teil 7b — der bestätigte Kaufvertrag** (Entwurf Z. 779/781, Abschnitt 8b).
Teil 7a ist erledigt: der **Gratisgewinn ist gesperrt** — `_trade` schenkte Rohstoffe ohne
Gegenleistung und wird jetzt **ehrlich abgelehnt** (Grund, Schwellenpreis und Zeiger auf diesen
Schritt stehen in der Meldung; gebucht wird nichts, `01fe939`). Jetzt fehlt der **Weg dahinter**:
`spieloekonomie.handel_start` (Gegenstand, Menge, Preis, Karawane, Dimension, **beidseitige Deckung**
aus Lager UND Gold), `handel_entscheiden` (die Gegenpartei sagt ja/nein) und `handel_abschluss` (die
Ankunft buchen). Die Maske muss **Ware, Menge und Preis** wählen lassen; der Bot braucht seine Form
als **Ortsdict** (`bot_als_dict` in `main.py` — vorher prüfen, ob `besitzer`, `dimension`,
`vorraete`, `einheiten`, `x`, `y` darin stehen), und Karawane plus Gold liegen im **Ortslager**
(Muster aus Teil 6c). **Lies dazu `docs/audits/entwurf_spieloekonomie_sol_2026-10-05.txt`,
Abschnitt 8b** — dort steht der Vertragsweg, den dieser Schritt anschließt.

**DANACH Teil 8 — `_unlock_next_map` + Migration:** die „Vermessung" entfällt, ein Altspielstand
ohne Versionsfeld lädt als `mode="legacy"` mit Warnhinweis, neue Partien als `mode="oeokonomie-1"`.
**Erst danach** Schritt 10 (`tick_bis` und die **Aktivierung**, Entwurf Z. 791-1018) — **vorher darf
der Ökonomiemodus NICHT aktiviert werden** (Entwurf Z. 1092).

> **⚠ OFFEN aus Teil 7a — die `.exe` ist GEBAUT, aber NICHT startgeprüft:** **14.641.733 Byte**,
> SHA256 `524d6260e28daf74…`, 00:27:57; Vorgängerfassung gesichert
> (`…\cache\scratch\exe_alt_0027_vor_teil7.exe`, 14.640.433 Byte). Die Prüfung **lief nicht an** (der
> Befehl hing in der Freigabe, keine Zustimmung) — sie ist **nicht** als bestanden gemeldet und die
> Protokollzeile dafür fehlt absichtlich. **Erst prüfen, dann protokollieren:** Skript
> `…\cache\scratch\exestart\startpruefung_1006_0029.ps1` (Titel, +10/+20/+40 s, WerFault,
> offene Prozesse, Startordner leer) — oder die `.exe` aus einem anderen Ordner selbst starten und
> das Ergebnis als Beleg eintragen.

**Die alten Beschreibungen des Teils (jetzt erfüllt) stehen darunter weiter:**

**Danach die Teile 7-8:** `_trade` über das bestätigte Angebot aus 8b oder eine deutliche
„noch nicht verfügbar"-Meldung (nie der Alt-Gratisgewinn), `_unlock_next_map` (die „Vermessung"
entfällt) + Migration (Altspielstand ohne Versionsfeld → `mode="legacy"` mit Warnhinweis, neue
Partien `mode="oeokonomie-1"`); **erst danach** Schritt 10 (`tick_bis` und die Aktivierung, Entwurf
Z. 791-1018) — **vorher darf der Ökonomiemodus NICHT aktiviert werden** (Entwurf Z. 1092).

**Die Ordnungs-Einsicht, die den Rest bestimmt (beim Bau von Teil 1 gemessen):** die fünfzehn
Ortsfelder sind angelegt, aber **leer**. Solange sie leer sind, kann KEIN Rückruf auf sie umgestellt
werden — `transport_start`, `verbrauchen`, `ware_start` & Co. prüfen ihre Deckung im **lokalen** Lager
und würden jede Zahlung ablehnen. **Deshalb gilt: erst die lokalen Lager füllen und führen, dann die
Rückrufe umstellen.** Vorgeschlagene Reihenfolge (meine Lesart des Entwurfs Z. 775-789; Daniel kann sie
ändern):

* **Teil 3 — lokale Lager führen und die Siedlungskarte darauf umstellen.** **FERTIG.** 3a (`a0d432d`):
  die Ortslager **führen** (Produktion je Ort in `Settlement.vorraete`, Bezahlung Ortslager-zuerst mit
  dem Reichsbestand als Übergangskasse, erste Siedlung übernimmt 10 Siedler · 100 Holz · 100 Stein,
  Kolonie zahlt ihr Paket aus dem Lager der Mutter). 3b (`65c41bf`): die **Anzeige** trennt „lokal" und
  „Reich" — Kopfleiste, Siedlungsliste und Siedlungskarte. Damit ist Punkt 4 der ursprünglichen Liste
  (die Anzeige getrennt zeigen) erledigt.
* **Teil 4 — `_transport_to_settlement` vollständig ersetzen** (Entwurf Z. 779): Herkunft, Rohstoff,
  Menge und Karren abfragen, `transport_start`/`transport_fortschritt` benutzen, Ergebnis mit
  `Settlement(**neu)` zurückschreiben, Mission anhängen — die Mission **muss** in der
  Auftragsschleife über `transport_fortschritt` gebucht werden (`eigentransport` = True; der
  Altpfad `spieldaten_anwenden` lässt sie absichtlich unberührt).
* **Teil 5 — `_found_settlement`** (Entwurf Z. 777): Auswahlliste freier Karten aus dem Kartenvorrat
  samt Nutzen/Kapazitäten/Preis/Mindestbestand, `absicht` statt sofortigem `append`, Sperrgut,
  Vergabe, keine zufällige Erstwahl.
* **Teil 6 — Produktion und Aufträge je Ort:** `_ware_herstellen` (`ware_start`), `_train_unit`
  (`ausbildung_start`), `_start_research` (`forschung_start`), `tick` über `ort_tick`.
* **Teil 7 — `_trade`:** bestätigtes Angebot über das Paar aus Schritt 8b oder eine deutliche
  „noch nicht verfügbar"-Meldung; **nie** der alte Gratisgewinn.
* **Teil 8 — `_unlock_next_map`** (die erfundene „Vermessung" entfällt) und **Speicherung/Migration**
  (Entwurf Z. 788): Altspielstand ohne Versionsfeld → `mode="legacy"` mit Warnhinweis, neue Partien
  `mode="oeokonomie-1"`, keine automatische Konvertierung ohne Daniels Wort.
* **Danach Schritt 10:** `tick_bis` + Ereignisschleife (Entwurf Z. 791-1018), **erst dann** die
  Aktivierung. Einzelheiten je Zeile: Entwurf Z. 755-789 in
  `docs/audits/entwurf_spieloekonomie_sol_2026-10-05.txt`.

**Was in Teil 3a bewusst noch NICHT gemacht ist (entschieden, nicht vergessen):** die globalen Werte
werden weiterhin **fortgeschrieben** (der Reichsbestand ist die Übergangskasse); die endgültige Form
(„Globale `resources` … im Neumodus aus Anzeigen ableiten", Entwurf Z. 787) kommt, wenn die Rückrufe in
Teil 4-7 umgestellt sind und der Zuschuss aus `verbrauche_am_ort` entfallen kann.

## 3. Roadmap Ökonomie-Paket (Reihenfolge des Papiers, „kein Halbumbau")

| Schritt | Inhalt | Beleg |
|---|---|---|
| 0 | 4 Handbuch-Korrekturen (Götterschutz 7 Tage, Steinmetz ohne Forschung, Forschung sperrt Siedlung, Rinderfarm Nahrung+Leder) | `203e2fa` |
| 1 | Kartenvorrat + `data/spieloekonomie.json` | `c68a60f` |
| 2 | Kern `src/spieloekonomie.py` (Achsen, Preise, Vergabe) | `a50edd6` |
| 3 | lokale Lager + Transportbuchung (Karrenpflicht) | `40` |
| 4 | Warenrezepte + lokale Ausbildung | `e6fd766`, `3bdbc6a` |
| 5 | Spieluhr `ort_tick`, `fensterproduktion` | `319c16b`, `a83ec25` |
| 6 | Forschung je Siedlung (`forschung_start`, `forschung_abschluss`) | `1d64cd6`, `c590951` |
| 7 | `zielstatus` (Zielprüfung + Haltefenster 24 h) | `a2b6531`, `eee604e` |
| 8a | `botkern.oekonomie_kartenwahl`, `oekonomie_angebot` | `3785b5d` |
| 8b | Handels-Paar `handel_start`/`handel_abschluss` + Prüfdatei | `25466f5` · `test_handel_transaktion` **101/0/0** |
| **9** | **`main`-Anbindung + Migration — Teil 6 fertig, in Teil 7a ist der Gratisgewinn gesperrt; das NÄCHSTE ist der bestätigte Kaufvertrag (7b)** | 9.1 `c099c4e` · 9.2 `1ce4ae3` · 9.3a `a0d432d` · 9.3b `65c41bf` · 9.4 `5a46ad7` · 9.5 `fab8611` · **9.6a `ad12376` · 9.6b/c `0e4a08a`** · `test_oekonomie_einhaengung` **301/0/1**, Sammellauf **3965/0/22** |
| 10 | `tick_bis` + **Aktivierung** | offen |

**Was die Teile 1, 2, 3a, 3b, 4 und 5 in `src/main.py` wirklich geändert haben:**
1. **Teil 1 (Ökonomie-Felder + Ort-Kennung):** die fünfzehn Felder aus Entwurf Z. 757-772 liegen in
   der `Settlement`-Dataclass (Vorgabewerte → **Altspielstände laden unverändert weiter**); sie bleiben
   bis zur Aktivierung leer, das Spiel rechnet weiter mit den globalen Beständen (**keine zweite
   führende Wahrheit** — die Prüfdatei wacht darüber). `siedlung_kennung(besitzer, map_id, x, y)` =
   `spieler:kontinent:3:7`: hängt an Besitzer und Weltfeld, **nie am Namen**, wird beim Gründen
   vergeben und beim Laden für Altbestände nachgesetzt.
2. **Teil 2 (Punkte + echter Fehler):** `GameState.alle_einheiten()` zählt **anwesende und unterwegs
   befindliche** Einheiten, jede genau einmal (Entwurf Z. 786) — vorher fielen Truppen während einer
   Reise aus den Kriegspunkten. **Dabei ein echter Fehler gefunden und behoben:** ein
   **stationierender** Auftrag verlor seine Truppe **zweimal** (`auftrag_starten` zieht sie beim
   Start ab, `spieldaten_anwenden` für die Art „stationieren" bei der Ankunft noch einmal) —
   gemessen: 5 Krieger minus 2 stationierte = **1** statt 3. **Ehrlich benannter Befund:** die
   stationierte Truppe steht danach in **keinem** Lager (das orts eigene `einheiten`-Feld ist noch
   leer) — kein stiller Verlust, sondern ein Befund in der Prüfdatei.
3. **Teil 3a (die Ortslager FÜHREN):** die Produktion wächst **je Ort** (`ertrag_je_ort`) in
   `Settlement.vorraete`; jede Zahlung der Siedlungskarte läuft über `verbrauche_am_ort` (Ortslager
   zuerst, dann der **Reichsbestand** als Übergangskasse, gezogen nur der fehlende Rest). Die
   **erste** Siedlung übernimmt die belegten Startwerte (Handbuch S. 7: 10 Siedler · 100 Holz ·
   100 Stein), eine Kolonie zahlt ihr Paket aus dem Lager der Mutter gegen das Mindestguthaben.
   **Der Sammellauf fand dabei 10 echte Fehler** — die Vorprüfungen in `_karten_bauen`,
   `_karten_ausbauen` und im Knopf-Text lasen weiter nur den Reichsbestand.
4. **Teil 3b (die Anzeige trennen):** zwei Helfer in `src/main.py` sind die **EINE** Quelle —
   `ortsbestand_text(siedlung)` liest NUR `Settlement.vorraete`/`.bevoelkerung`,
   `reichsbestand_text(state)` NUR `GameState.resources`/`.population` (dazu `mengen_text`/`zahl_text`:
   nur Posten > 0, feste Reihenfolge, unbekannte Posten bleiben). Angezeigt wird: Kopfleiste „Reich:",
   Siedlungsliste mit „Reich: …" über der Liste und je Ort „lokal: …" darunter, Siedlungskarte mit
   hervorgehobenem Panel „Ortsbestand dieser Siedlung (lokal)" samt Reichs-Vergleich,
   Bevölkerungszeile „Siedler (Reich):". **Rundlauf geprüft:** Speichern/Laden trug beide Felder schon
   (`asdict`/`Settlement(**s)`) — vor und nach dem Laden sind Lokal- und Reichstext gleich und
   weiterhin verschieden. Am lebenden Fenster gemessen (Ortslager 137,5 Holz gegen Reich 777 Holz).
5. **Teil 4 (der Transport funktioniert wirklich):** die alte Methode buchte **fest 10 Holz** vom
   Reichsbestand ab und schrieb **nichts** gut — es gab keine Mechanik. Neu:
   `GameState.transport_an_ort(quelle, ziel, rohstoff, menge, karren)` prüft alles und bucht im KERN
   (`spieloekonomie.transport_start`), `_eigentransport_buchen` führt die Mission bei **jedem Takt**
   über `transport_fortschritt` (Ankunft: Fracht + Importherkunft ins **Ortslager** des Ziels;
   Rückkehr: Karren ins Ortslager der Herkunft — je genau einmal). `spieldaten_anwenden` bleibt für
   Eigentransporte unberührt (Entwurf Z. 505), die Heimkehr läuft **nicht** über den Reichsbestand.
   `_ort_uebernehmen` bringt den **bestehenden** Ort auf den neuen Stand (die Oberfläche hält
   Verweise), und `alle_einheiten()` zählt jetzt auch die **Ortslager** (Entwurf Z. 786) — sonst
   fielen die Karren nach der Heimkehr aus den Kriegspunkten. Die Oberfläche hat eine echte
   **Transportmaske** (Herkunft/Rohstoff/Menge/Karren, Ausgangs- und Zielbestand, Ladeplätze).
6. **Teil 5 (die Gründung):** `GameState.kartenvorrat` ist **Spielzustand** (neun Koloniekarten,
   Saat gemerkt, mitgespeichert; ein Altspielstand bekommt ihn nach). Der **erste Start** holt die
   **Startkarte** aus dem Kern und übernimmt 10 Siedler · 100 Holz · 100 Stein genau einmal — keine
   zufällige Erstwahl. Jede **Kolonie** läuft über den Kern: `gruendung_pruefen` ruft
   `spieloekonomie.absicht` (freie Karte, Siedlungsgrenze, **Wagenbau**, **Siedlerkarren**,
   **Mindestbestand im Ortslager**) und `vergabe`; `gruendung_ausfuehren` bucht das **Sperrgut
   (Mindestbestand = Gebühr + Startpaket)** aus dem Ortslager der Ausgangssiedlung, verbraucht den
   Siedlerkarren, vergibt die Karte und setzt **Startpaket + 5 Kolonisten** aufs **vorher gewählte**
   Weltfeld. Die Auswahlmaske zeigt Nutzen (beste zuerst), Kapazitäten, Gebühr (320/200/150) und
   Mindestbestand (480/300/250).

## 4. Arbeitsweise (Vorgabe Daniel — gilt unverändert)

Nach **jedem** Schritt: betroffener **Einzeltest** + **einmal Sammellauf** (keine Spielprozesse offen
lassen), **eine Protokollzeile** in `docs/ENTWICKLUNGSPROTOKOLL.md` (Zeit mit `date`), dann
`python tools/protokoll_sichern.py --protokoll`, **kleiner Commit**. **Prüfende Unteragenten erst
NACH dem Commit.** Handbuch gewinnt bei Widerspruch (Zitat + Zeilennummer belegen). Berührt ein
Schritt eine **belegte** Handbuchregel: erst lesen, dann ändern. Ändert sich `src/` oder `data/*.json`,
am Ende die `.exe` neu bauen und aus einem **anderen** Ordner startprüfen.

## 5. Teuer gelernte Fallen (nicht wiederholen)

| Falle | Regel |
|---|---|
| **`patch`-Werkzeug mit falschem Anker** | Wird eine neue Zeile **an** einer bestehenden eingefügt, muss die Ankerzeile im Ersatztext **wieder vorkommen** — sonst löscht man sie still. Am 05.10. **zweimal passiert** (Protokollzeilen 56 und 57 verdrängt). Wiederherstellung: zeichengleich aus `git show <commit>:<datei>`; neue Zeilen **anhängen** statt einfügen. |
| **Belegte Regel = toter Zweig** | Eine belegte Handbuchregel kann im Entwurfscode **unerreichbar** sein (Handel: Annahme automatisch, Ablehnung nie möglich). Wer eine belegte Regel als „gebaut" meldet, muss den Zweig **auslösen** — sonst ist die Regel nur Text. Gefunden hat es die Prüfdatei, nicht das Nachdenken. |
| **Eine Prüfdatei findet, was das Nachdenken nicht findet** | Der Doppelabzug beim Stationieren (Teil 9.2) fiel **beim Schreiben der Prüfung** auf, nicht beim Lesen des Codes — und `test_auftraege` prüfte nur den Modulvertrag, nie das Zusammenspiel mit `main`. Bei jedem neuen Rückruf: eine Prüfung schreiben, die den **ganzen Weg** geht. |
| **Geschätzte Zeitangaben** | Ein Bauzeitstempel wurde mit „20:35" **geschätzt** (echt: 20:30:30) und musste korrigiert werden. Zeiten immer mit `date` bzw. `stat -c %y` holen, auch in Doku und Protokoll. |
| **Protokollzeile vergessen** | Commit `356b48a` (Kontext-Paket angelegt) hatte **keine** Protokollzeile; sie wurde nachgetragen. Auch ein reiner Doku-Commit ist ein grober Schritt. |
| `git add -A` | **Nie** vor der Kinderprüfung — sonst wandern ungeprüfte Dateien in den Commit. `git status --short` muss genau die erwarteten neuen Dateien zeigen. |
| Kindberichte | sind **Selbstauskunft**: ERGEBNIS-Zahl selbst nachfahren, Wachen-Namen überfliegen, erst dann committen. |
| Kinder parallel zum Sammellauf | stören ihn — nicht gleichzeitig laufen lassen. |
| `.exe`-Bau | währenddessen **kein** Spiel starten. Nach dem Bau: Startprüfung aus einem **anderen** Ordner (Prozesse, Fenstertitel, Antwortbereitschaft, WerFault). |
| `run_tests.bat` hat CRLF | `sed -i` findet dort **nichts** (still, exit 1) → `patch`-Werkzeug benutzen, danach mit `grep -o` prüfen. |
| Prüfmodule | führen sich beim `import` **aus** (`sys.exit(bericht())`) — Helfer nur über `try: import … / except SystemExit: sys.modules[…]` holen. |
| `src/botkern.py` | muss **reines ASCII** bleiben; eine Prüfdatei mit `# -*- coding: ascii -*-` ebenfalls (ein `—` bricht schon den Lint). |
| `docs/PROJEKT_STAND.md`, Abschnitt „Der EINE nächste Schritt" | darf **kein `###`** enthalten (`test_zieluebergabe`) → Zwischentitel als **Fett**. |
| Prüf-Fehler ≠ Ausreißer | erst nachsehen, dann abtun (belegte Fälle: zu lockere Prüfung, Haus auf unerlaubtem Feld). |
| Kinderarbeit | nur `deepseek-flash`; Kindberichte sind kein Beweis. |
| **Nach einer Lager-Umstellung zählt jede Vorprüfung** | Als die Ortslager führend wurden, lasen die Vorprüfungen in `_karten_bauen`, `_karten_ausbauen` und im Knopf-Text weiter nur den Reichsbestand — der Sammellauf fand **10 echte Fehler** (mit echten Startwerten ließ sich nichts mehr bauen). Regel: nach so einer Umstellung zuerst den Sammellauf, dann **jede** Vorprüfung auf dieselbe Deckungsfrage umstellen. |
| **Prüfungen mit ECHTEN Startwerten sind die besten Wächter** | `test_startspiel`, `test_durchspiel` und `test_gui_fehler` fanden die Umstellung sofort; Prüfungen, die sich selbst `resources = 100000` setzen, hätten sie nie bemerkt. |
| **Escape-Ebenen in der Leseausgabe** | Wer Text aus einer Werkzeug-Ausgabe in eine Datei kopiert, kopiert deren Escapes mit: am 05.10. standen ein `\"` und ein `\cache`, wo ein `"` und ein `\` gehörten (Protokollzeile 65 und der erste Anlauf der Übergabe) — beide nachgebessert. Regel: **nach dem Schreiben zurücklesen** und die kritischen Zeichen zählen. |
| **`.exe`-Neubau überschreibt die Vorgängerfassung** | `tools/build_exe.py` legt **keine** Kopie an. Vor dem Bau `cp Nebelseetal_Remake.exe …/cache/scratch/exe_alt_HHMM.exe`, sonst ist die alte Fassung weg (05.10. beim Bau von Teil 3b passiert; die Quelle bleibt in git reproduzierbar). |
| **Zwei Ansichten brauchen EINE Quelle** | Wird dieselbe Zahl an drei Stellen getippt (Siedlungsliste, Karte, Kopfleiste), laufen die Texte auseinander. Deshalb `ortsbestand_text`/`reichsbestand_text` als **einzige** Quelle — und die Prüfung wacht per Quelltext darüber, dass die Aufrufer sie benutzen. |
| **Wachen auf die GANZEN Zeilen ankern** | `"amount = 10" not in quelle` schlug an, weil es `amount = 100` (der belegte Startwert) mitfindet — gefunden hat es der Prüflauf, nicht das Nachdenken. Muster immer mit Zeilenumbruch bilden (`'amount = 10\n        resource'`). |
| **Ein neuer Rückruf braucht oft eine ZWEITE Änderung, damit er nicht tot ist** | Der Transport hängt an Karren im **lokalen** `Settlement.einheiten` — die sind bis Teil 6 leer. Lösung wie die Übergangskasse aus 3a: den fehlenden Karren aus dem Reichsheer holen und **ins Ortslager legen**. |
| **`Settlement(**neu)` und die Verweise der Oberfläche** | Der Ort wird in `self.settlements` ersetzt — `self.karten_siedlung` zeigt dann still auf einen alten Stand. Richtig: den **bestehenden** Gegenstand übernehmen (`_ort_uebernehmen`), nur bei echter Änderung. |
| **Rundlauf-Tests brauchen eine ECHTE Karten-Kennung** | `current_map = "test"` lässt `load` abstürzen (`generate_map` → `StopIteration`). Für Speichern/Laden `map_id=current_map` benutzen. |
| **Startprüfung als eigenen, einfachen Befehl fahren** | Ein Sammelbefehl (stat + find + cp + Prüfskript) blieb in der Freigabe hängen und wurde **nicht** ausgeführt — danach nie eine Prüfung als „gelaufen" melden; die Protokollzeile kommt erst mit dem Prüfergebnis. |
| **`get_tile` braucht die aufgebaute Weltkarte** | Ein frischer Zustand (oder eine Prüfung) hat sie nicht: `self.map_tiles` ist leer → `IndexError`. Vor JEDEM Zugriff auf Weltfelder `_weltkarte_sicherstellen()` (baut die Karte genau dann auf, wenn sie fehlt). Beim Bau von Teil 5 **dreimal** passiert (Auswahl, Kolonie, Startsiedlung). |
| **Wachen auf ersetzten Code umstellen** | Zwei P14-Wachen aus Teil 3a hingen an Zeilen der **alten** `_found_settlement` und wurden rot, als Teil 5 die Methode ersetzte. Nicht die Prüfung löschen: den **echten neuen Anker** suchen, der dieselbe Zusage belegt, und die Zusage stehen lassen. |
| **`absicht` erwartet eine FLACHE Stufenkarte** | `{Gebiet: Stufe}` — nicht `forschung_stand()` (das liefert je Gebiet ein Verzeichnis) → sonst `TypeError` beim Vergleich. |
| **`ort_tick` erntet SELBST** | Er bucht `wirtschaft.ertrag_gesamt` auf die Ortsvorräte, den Siedlerzuwachs und das `produktionsjournal`. Wer ihn NEBEN die Buchungen aus Teil 3a hängt, **verdoppelt jede Ernte**. Teil 6b hat deshalb die eigene Produktionsformel aus `tick` **entfernt** — eine Uhr, eine Formel. Die alte Wache „4 Holz, nicht 8" ist der Beweis. |
| **Ware und Einheit kommen erst mit dem Takt an** | `ware_start`/`ausbildung_start` legen nur den Auftrag an (`ort["werkstaetten"]`/`ort["ausbildung"]`); fertig gebucht wird in `ort_tick`. Ohne Takt kommt nichts an — und ohne **Neuzeichnen** (`tick` gibt die Fertigmeldungen zurück, die App zeichnet dann) sieht der Spieler es nie. |
| **Prüfungen kodieren die alte Wahrheit** | Nach dem Umbau auf „vor Ort" mussten `test_gebaeude_wirkung`, `test_gui_fehler`, `test_durchspiel`, `test_startspiel` ihre DATENLAGE umstellen (Rohstoffe, Siedler, Ausrüstung ins Ortslager; die Einheit nach der Ausbildungszeit im Ortslager prüfen). Zwei meiner NEUEN Erwartungen waren zusätzlich falsch (die Gesamtsicht führt **Zuwächse**, nicht Absolutwerte) — die Prüfung wurde korrigiert, nicht der Code. |

## 6. Nicht erneut zu prüfen (Beleg + Datum)

* Schritte **0–8b** — Commits und Prüfzahlen in Abschnitt 3.
* **Schritt 9, Teil 1** — `c099c4e`, `test_oekonomie_einhaengung` 74/0/0, Sammellauf 3728/0/21 (20:44).
* **Schritt 9, Teil 2** — `1ce4ae3`, dieselbe Prüfdatei **88/0/1**, Sammellauf **3742/0/22** über
  52 Dateien (20:48); der Befund ist der ehrlich benannte Lager-Befund der stationierten Truppe.
* **Schritt 9, Teil 3a** — `a0d432d`, `test_oekonomie_einhaengung` **121/0/1**, Sammellauf **3775/0/22**
  über 52 Dateien (21:1x).
* **Schritt 9, Teil 3b** — `65c41bf`, dieselbe Prüfdatei **143/0/1** (neu: P15 Trennung, P16 Rundlauf
  beider Ansichten, P17 Quelltextwachen), Sammellauf **3797/0/22** über 52 Dateien (21:2x, 124 s).
* **Schritt 9, Teil 4** — `5a46ad7`, dieselbe Prüfdatei **196/0/1** (neu: P18 ganzer Weg Start→Ankunft
  →Heimkehr, P19 neun Ablehnungen ohne jede Änderung, P20 laufender Transport über Speichern/Laden,
  P21 Quelltextwachen), Sammellauf **3850/0/22** über 52 Dateien (21:5x, 133 s).
* **Schritt 9, Teil 5** — `fab8611`, dieselbe Prüfdatei **249/0/1** (neu: P22 Vorrat/Auswahlliste/
  Sortierung/Weltfelder · P23 vier Ablehnungen ohne jede Änderung, ganzer Weg, Gebühr vernichtet,
  Karte vergeben, Rundlauf, sechste Siedlung abgelehnt · P24 Startgründung mit Startkarte,
  Quelltextwachen), Sammellauf **3903/0/22** über 52 Dateien (22:1x, 116 s); am lebenden Fenster
  gemessen (Maske mit Nutzen/Preis/Minimum, Gründung über die Oberfläche, ehrliche Ablehnung ohne
  Karren).
* **Schritt 9, Teil 6a** — `ad12376`, dieselbe Prüfdatei **264/0/1** (neu: P25 der Zeiger auf den
  aktiven Ort, Speichern/Laden, Stand ohne das Feld lädt weiter), Sammellauf **3917/0/23** über
  52 Dateien.
* **Schritt 9, Teil 6 (REST: die Forschung je Ort)** — `35e1bd1`, dieselbe Prüfdatei **312/0/1**
  (neu: P28 Auftrag im Ort im Stand sichtbar, Abschluss genau einmal, Journalzeile, **alter
  Spielstand wird in den Ort umgezogen**, Altpfad im Quelltext verschwunden), `test_gebaeude_wirkung`
  **120/0/1** (Start im aktiven Ort, 50 Holz IM ORT abgezogen, Reich unberührt), `test_gui_fehler`
  **24/0/1**, `test_durchspiel` **52/0/2**, `test_startspiel` **54/0/0**, Sammellauf **3979/0/22** über
  52 Dateien (00:1x, 149 s); am lebenden Fenster gemessen (Forschung läuft in „Denkort", Ortsholz
  5000 → 4950, Reichsholz 100 unverändert, Ansicht „läuft auf Stufe 1 · noch 1.0 h", danach 1/10).
* **Schritt 9, Teil 6b+6c** — `0e4a08a`, dieselbe Prüfdatei **301/0/1** (neu: P26 die Spieluhr je
  Ort, **kein Doppelertrag** — die Wache aus Teil 3a „4 Holz, nicht 8" hält weiter, Journal genau
  eine Zeile je Takt · P27 Ware VOR ORT bis zur Ankunft im Ortslager, Reichslager unberührt,
  Quelltextwachen), **`test_gebaeude_wirkung` 118/0/1**, **`test_startspiel` 54/0/0** (Knopfdruck →
  Auftrag vor Ort → Einheit nach der Zeit, im FENSTER sichtbar), **`test_baseline` 40/0/0**,
  **`test_durchspiel` 51/0/2**, Sammellauf **3965/0/22** über 52 Dateien (23:5x, 100 s); am lebenden
  Fenster gemessen (Lager „Schmiede (1 Stück vor Ort)" und nach dem Einreihen „in Arbeit: 1 |
  fertig: 0 | Restzeit 20.0 Minuten", Kaserne „Anzahl: 2 vor Ort · Reich: 0").
  Messwerte am lebenden Fenster: Dorfzentrum „Reich: 777 Holz, 300 Stein · 21 Siedler" **und**
  „lokal: 137.5 Holz, 42 Stein · 8 Siedler"; Siedlungskarte „Ortsbestand dieser Siedlung (lokal)".
* Die neue `.exe` **startet** (00:18, Fenstertitel, antwortet 10/20/40 s, 0 Fehlerberichte, 0 offene
  Prozesse); sie enthält die **Ortslager (3a)**, die **getrennte Anzeige (3b)**, den **echten
  Transport (4)**, die **Gründung mit Kartenvorrat (5)**, den **aktiven Ort (6a)**, die **eine
  Spieluhr je Ort samt Ware und Ausbildung vor Ort (6b/c)** und die **Forschung je Ort (Teil 6
  Rest)**.
* Der Sammellauf wird **nur nach einer echten Änderung an `src/`** wiederholt.
* Fehlend von Schritt 8a: `tests/test_bot_oekonomie.py` und `docs/audits/pruefung_schritt8.md` (zwei
  gestoppte Kinder; Auftragstext in Protokollzeile 53).

## 7. Offene Entscheidungen für Daniel (nichts eigenmächtig geändert)

0. **Aus 8b:** `handel_entscheiden` + Feld `entscheidung` (macht die belegte Ablehnungsregel S. 20
   erreichbar) und die Wache in `auftraege.spieldaten_anwenden` für Fremdverträge — streichbar, dann
   gilt der Entwurf wörtlich (mit totem Zweig).
1. **Aus 9.1:** die Ort-Kennung `besitzer:map_id:x:y` — sie hängt am Weltfeld; **wenn eine Siedlung
   jemals das Feld wechselt**, braucht sie eine andere Form (Entwurf nennt keine).
2. **Aus 9.2:** die stationierte Truppe hat **noch kein Lager** (Befund): bis die Ortslager führen,
   ist sie nirgends gezählt. Entscheidung fällt mit Teil 3.
3. **Kampfverluste verdrahten** — Handbuchregel wörtlich (S. 23), `src/kampf.py` hat sie gebaut, es
   fehlt die Anbindung; offene Frage: Prozent-Untergrenze oder nur Simulation? →
   `docs/ENTWURF_KAMPFVERLUSTE.md`.
4. **Forschungsstufe global oder je Siedlung?** Handbuch **schweigt** →
   `docs/audits/belege_forschung_je_siedlung.md` (V1/V2/V3).
5. **Reserve-Anzeige** in `zielstatus` (`bool(orte)`) ist gekennzeichneter **VORSCHLAG**.
6. **Skill-Kopie im Profil `coding` veraltet** — nur auf Daniels Wort nachziehen.
7. **Kostendeckel:** heute überschritten, für diesen Auftrag **freigegeben** (Reserve 1,00 USD).

## 8. Wo die Details liegen (nur bei Bedarf lesen)

* Handbuch (Wahrheit): `docs/original/Spielanleitung_2009_Textfassung.txt`
* Ökonomie-Entwurf (die Vorgabe in 10 Schritten): `docs/audits/entwurf_spieloekonomie_sol_2026-10-05.txt`
* Handbuch-Abgleich: `docs/audits/handbuch_abgleich_2026-10-05.txt`
* Audits je Schritt: `docs/audits/pruefung_schritt3_4.md`, `…_schritt5.md`, `…_schritt6.md`, `…_schritt7.md`
* Stand/Historie: `docs/PROJEKT_STAND.md` (0c Tabelle, 0e Übergabe) · `docs/ENTWICKLUNGSPROTOKOLL.md`
* Werkzeuge: `tools/zieluebergabe.py` · `tools/protokoll_sichern.py` · `tools/build_exe.py`
* Sammellauf: `C:\Users\saras\AppData\Local\hermes\cache\scratch\sammellauf.py` (liest `run_tests.bat`)
* Startprüfung: `…\cache\scratch\exestart\startpruefung_1006_0018.ps1` (Prozesse, Titel, WerFault)
* Bau-Umgebung für die `.exe` (Zwischenspeicher, 24 h): `…\cache\scratch\nebel_bauvenv`
  (`uv venv --python 3.14.7` · `uv pip install pyinstaller`), Aufruf mit `--python …/Scripts/python.exe`
