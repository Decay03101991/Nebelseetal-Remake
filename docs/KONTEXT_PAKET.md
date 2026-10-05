# KONTEXT-PAKET — Nebelseetal Remake (Stand 05.10.2026, 21:12 · Zeiten mit `date` geholt)

**Diese Datei ist die Übergabe. Lies SIE zuerst (≈ 10 KB) und sonst nur, was hier als Zeiger steht —
`docs/PROJEKT_STAND.md` (69 KB) und `docs/ENTWICKLUNGSPROTOKOLL.md` (80 KB) sind Nachschlagewerke,
keine Einstiegslektüre.** Projekt: `D:\Arbeiten\Nebelseetal_Remake` (bash/MSYS, `python -X utf8`).
Ziel: fertige, fehlerfrei spielbare, passwortgeschützte Einzelspieler-`.exe` (Handbuch 2009 = Wahrheit).

---

## 1. Belegter Ist-Stand

| Was | Beleg |
|---|---|
| **Sammellauf** | **3775 bestanden · 0 Fehler · 22 Befunde · 52 Dateien** (21:1x; `…/cache/scratch/sammellauf.py`, 105 s) |
| **Arbeitsbaum** | **sauber** (`git status --short` leer), letzter Commit **`a0d432d`** (Schritt 9, Teil 3a) |
| **`.exe`** | **14.618.766 Byte**, SHA256 `799c8a68bdca7fe3…`, Dateizeitstempel **21:09:43**; genau **eine** `.exe`, `build/`+`dist/` aufgeräumt; Vorgängerfassung liegt als `…\cache\scratch\exe_alt_2030.exe` |
| **Startprüfung** | aus `…\hermes\cache\scratch\exestart` (anderer Ordner, Skript `startpruefung_1005_2055.ps1`): Fenstertitel **„Nebelseetal Remake"**, antwortet bei **+10/+20/+40 s**, **0** Fehlerberichte (WerFault), danach **0 offene Spielprozesse**, Startordner leer |
| **Sicherung** | `docs/SICHERUNGEN.md` — 16 führende Papiere mit Prüfsummen (20:50, projektunabhängige Kopie unter `D:\Arbeiten\Hermes\Nebelseetal_Protokoll\`) |
| **Zielregister** | nur **diese** Sitzung `20261005_201518_d2b523` aktiv (**0/20 Takte** laut Werkzeug), **kein fremdes aktives Ziel** (`--pruefen` rc=0) |
| **Kosten** | Tagesmessung **6,68 EUR / 4,00 EUR = „UEBER_LIMIT"** (7,40 USD). **Daniel hat den Auftrag um 20:20 freigegeben** (nur `deepseek-flash`, kein teures Modell, keine Kinder, **1,00 USD DeepSeek bleiben als Reserve**). Gemessener Anteil dieser Sitzung: **+0,23 EUR** (20:15: 6,45 → 21:12: 6,68). Maßgeblich ist DeepSeeks Kontostand (Daniel liest ab: 2,01 USD um 20:20) |

`git log --oneline -3` · `git status --short` · `python tools/zieluebergabe.py --pruefen` → alles in Sekunden.

## 2. Der EINE nächste Schritt

**Schritt 9 läuft — Teile 1, 2 und 3a sind fertig; als Nächstes Teil 3b.** Der Auftraggeber hat
„Stück für Stück" entschieden: nach JEDEM Teil Einzeltest + einmal Sammellauf + Protokollzeile +
kleiner Commit.

**Teil 3b (der nächste Schritt): die ANZEIGE trennen — „lokal" und „gesamtes Reich".** Seit Teil 3a
liegt der Bestand in den Ortslagern (`Settlement.vorraete`/`bevoelkerung`); die Seitenleiste und die
Siedlungsliste zeigen aber weiter nur die Gesamtsicht (`GameState.resources`/`population`). Der
Spieler liest damit eine Zahl, die nicht mehr „Lager dieser Siedlung" bedeutet. Zu tun: in der
Siedlungsliste je Ort „lokal: …" neben „Reich: …" zeigen, in der Siedlungskarte den Ortsbestand
hervorheben, und im Spielstand beide Ansichten speichern/laden (Rundlauf prüfen). Danach die
Teile 4-7 (`_transport_to_settlement` vollständig ersetzen, `_found_settlement` mit Kartenauswahl/
`absicht`/Preis, `_ware_herstellen`/`_train_unit`/`_start_research` je Ort, `_trade`) und zuletzt
`_unlock_next_map` + Migration; **erst danach** Schritt 10 (`tick_bis` und die Aktivierung).

**Die Ordnungs-Einsicht, die den Rest bestimmt (beim Bau von Teil 1 gemessen):** die fünfzehn
Ortsfelder sind angelegt, aber **leer**. Solange sie leer sind, kann KEIN Rückruf auf sie umgestellt
werden — `transport_start`, `verbrauchen`, `ware_start` & Co. prüfen ihre Deckung im **lokalen** Lager
und würden jede Zahlung ablehnen. **Deshalb gilt: erst die lokalen Lager füllen und führen, dann die
Rückrufe umstellen.** Vorgeschlagene Reihenfolge (meine Lesart des Entwurfs Z. 775-789; Daniel kann sie
ändern):

* **Teil 3 — lokale Lager führen und die Siedlungskarte darauf umstellen.**
  1. Beim Gründen: die **erste** Siedlung übernimmt die belegten Startwerte (10 Siedler · 100 Holz ·
     100 Stein, Handbuch S. 7) in `bevoelkerung`/`vorraete`; Kolonien übernehmen das bezahlte Paket
     (Entwurf Z. 775 „erste Siedlung übernimmt 10 aus vorhandenen Startdaten; Kolonie übernimmt 5 aus
     dem bezahlten Siedlerkarren").
  2. **EINE Quelle:** die lokalen Lager sind führend, die globalen Werte werden nach jeder Änderung
     **abgeleitet** (`_global_aus_orten()`), nie mehr eigenständig bezahlt (Entwurf Z. 787).
  3. `aktive_siedlung_id` als UI-Zustand (Entwurf Z. 775) — jede Zahlung der Siedlungskarte
     (`_karten_bauen`, `_karten_ausbauen`, `_karten_abreissen`, Siedler) läuft über `verbrauchen`
     gegen **diesen** Ort.
  4. Anzeige: „lokal (diese Siedlung) + Gesamtreich" getrennt zeigen, sonst liest der Spieler eine
     Zahl, die nicht mehr stimmt.
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
| **9** | **`main`-Anbindung + Migration — TEILE 1-3a fertig, Teil 3b als Nächstes** | 9.1 `c099c4e` · 9.2 `1ce4ae3` · **9.3a `a0d432d`** · `test_oekonomie_einhaengung` **121/0/1** |
| 10 | `tick_bis` + **Aktivierung** | offen |

**Was Teil 1 und 2 in `src/main.py` wirklich geändert haben:**
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

## 6. Nicht erneut zu prüfen (Beleg + Datum)

* Schritte **0–8b** — Commits und Prüfzahlen in Abschnitt 3.
* **Schritt 9, Teil 1** — `c099c4e`, `test_oekonomie_einhaengung` 74/0/0, Sammellauf 3728/0/21 (20:44).
* **Schritt 9, Teil 2** — `1ce4ae3`, dieselbe Prüfdatei **88/0/1**, Sammellauf **3742/0/22** über
  52 Dateien (20:48); der Befund ist der ehrlich benannte Lager-Befund der stationierten Truppe.
* Die neue `.exe` **startet** (20:49:57, Fenstertitel, antwortet 10/20/40 s, 0 Fehlerberichte, 0
  offene Prozesse) — sie enthält die Feld-/Kennungs-Änderung **und** die Punkt- und
  Stationier-Korrektur.
* **Schritt 9, Teil 3a** — `a0d432d`, `test_oekonomie_einhaengung` **121/0/1**, Sammellauf **3775/0/22**
  über 52 Dateien (21:1x). Die neue `.exe` (**21:09:43**) enthält sie **im Spiel wirksam**.
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
* Startprüfung: `…\cache\scratch\exestart\startpruefung_1005_2055.ps1` (Prozesse, Titel, WerFault)
* Bau-Umgebung für die `.exe` (Zwischenspeicher, 24 h): `…\cache\scratch\nebel_bauvenv`
  (`uv venv --python 3.14.7` · `uv pip install pyinstaller`), Aufruf mit `--python …/Scripts/python.exe`
