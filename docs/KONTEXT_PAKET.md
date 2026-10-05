# KONTEXT-PAKET — Nebelseetal Remake (Stand 05.10.2026, 20:40 · Zeiten mit `date` geholt)

**Diese Datei ist die Übergabe. Lies SIE zuerst (≈ 9 KB) und sonst nur, was hier als Zeiger steht —
`docs/PROJEKT_STAND.md` (68 KB) und `docs/ENTWICKLUNGSPROTOKOLL.md` (77 KB) sind Nachschlagewerke,
keine Einstiegslektüre.** Projekt: `D:\Arbeiten\Nebelseetal_Remake` (bash/MSYS, `python -X utf8`).
Ziel: fertige, fehlerfrei spielbare, passwortgeschützte Einzelspieler-`.exe` (Handbuch 2009 = Wahrheit).

---

## 1. Belegter Ist-Stand

| Was | Beleg |
|---|---|
| **Sammellauf** | **3654 bestanden · 0 Fehler · 21 Befunde · 51 Dateien** (20:27; `…/cache/scratch/sammellauf.py`, 108 s) |
| **Arbeitsbaum** | **sauber** (`git status --short` leer), letzter Commit **`25466f5`** — 20:33 |
| **`.exe`** | **14.611.526 Byte**, SHA256 `11e7042f6c50fadf…`, gebaut **20:35**; genau **eine** `.exe`, `build/`+`dist/` aufgeräumt |
| **Startprüfung** | aus `…\hermes\cache\scratch\exestart` (anderer Ordner): Fenstertitel **„Nebelseetal Remake"**, antwortet bei **+10/+20/+40 s**, **0** Fehlerberichte (WerFault), danach **0 offene Spielprozesse**, Startordner leer |
| **Sicherung** | `docs/SICHERUNGEN.md` — 16 führende Papiere mit Prüfsummen (20:33, `protokoll_sichern.py --protokoll`) |
| **Zielregister** | nur **diese** Sitzung `20261005_201518_d2b523` aktiv (**1/20 Takte**), **kein fremdes aktives Ziel** (`--pruefen` rc=0) |
| **Kosten** | Tagesmessung **6,52 EUR / 4,00 EUR = „UEBER_LIMIT"** (7,32 USD, 52 Sitzungen, 5 Modelle). **Daniel hat für diesen Auftrag freigegeben** (deepseek-flash, kein teures Modell, kein Kind, **1,00 USD DeepSeek bleiben als Reserve**) → Arbeitsraum ≈ 1 USD. Gemessener Anteil dieser Sitzung bisher: **+0,07 EUR** (20:15: 6,45 → 20:40: 6,52). Maßgeblich ist DeepSeeks Kontostand (Daniel liest ab: **2,01 USD** um 20:20) |

`git log --oneline -3` · `git status --short` · `python tools/zieluebergabe.py --pruefen` → alles in Sekunden.

## 2. Der EINE nächste Schritt

**Schritt 9 — `main`-Anbindung, Anzeige und Migration** (Entwurf
`docs/audits/entwurf_spieloekonomie_sol_2026-10-05.txt` Z. 755-789, Vorgabe in 0c). Inhalt in
Kurzform, jede Zeile mit der Entwurfsstelle:

* **`src/main.py`, `Settlement`-Dataclass** (Z. 757-772): die neuen Ortsfelder `id`, `besitzer`,
  `dimension`, `vorraete`, `waren`, `einheiten`, `bevoelkerung`, `importiert`, `reserve`,
  `werkstaetten`, `ausbildung`, `forschungsauftrag`, `produktions-, verbrauchs-, fertigjournal` —
  **`units`/`garrison` nicht gleichzeitig als führende Bestände weiterführen** (Altmodus liest die
  alten Felder, Neumodus nur `einheiten`).
* **Rückruf-Diffs** (Z. 776-786): `_found_settlement` (Auswahlliste freier Karten + `absicht`
  statt sofortigem `append`) · `_transport_to_settlement` (**vollständig ersetzen** durch
  `transport_start`) · `_karten_bauen`/`_karten_ausbauen` (Kosten aus `BP` gegen den **gewählten
  Ort**, Bibliotheksausbau während einer Forschung ablehnen) · `_ware_herstellen` (`ware_start`) ·
  `_train_unit` (`ausbildung_start`) · `_start_research` (`forschung_start`) · `_trade`
  (bestätigtes Angebot oder deutliche Meldung, **nie** Alt-Gratisgewinn) · `_unlock_next_map`
  (die erfundene „Vermessung" entfällt) · `punktestand` (unterwegs befindliche Einheiten **nicht**
  doppelt zählen).
* **Speicherung und Migration** (Z. 787-788): `asdict(Settlement)`; Altspielstand ohne Versionsfeld →
  `mode="legacy"` mit Warnhinweis, neue Partien `mode="oekonomie-1"`; **keine automatische
  Konvertierung** ohne Daniels Wort, vorher vollständige Kopie.
* **Prüfaussagen (Z. 789):** sichtbare Ausgangs- und Zielbestände, echtes Wartelabel, defizitäre
  Karte mit Fehlrohstoff statt nutzloser Nullzahl, Gründungsklick zeichnet neu; mitziehen:
  `test_gui_fehler`, `test_baseline`, `test_startspiel`, `test_kartenansicht`,
  `test_siedlungskarte`, `test_w8_einhaengung`, `test_speichern_robust`, `test_durchspiel`,
  `test_punkte_einhaengung`.
* **Erwartet:** Sammellauf weiter **ohne Fehler** (die aufgezählten Prüfdateien bauen auf dem
  Altmodus auf und müssen ihre Annahme ggf. anpassen), plus betroffener Einzeltest je Rückruf.

Danach **Schritt 10** (`tick_bis` + Ereignisschleife, Entwurf Z. 791-1018, **erst dann** die
Aktivierung des Ökonomiemodus). **Bis dahin ruft nichts im Spiel `src/spieloekonomie.py` auf** — das
ist Zusage, nicht Zufall, und wird von Prüfdateien mitgeprüft.

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
| **8b** | **Handels-Paar + Prüfdatei — FERTIG** | `25466f5` · `test_handel_transaktion` **101/0/0** |
| **9** | **`main`-Anbindung + Migration ← nächster Schritt** | offen |
| 10 | `tick_bis` + **Aktivierung** | offen |

**Zustand im Spiel:** der **Altmodus läuft unverändert** — nichts im Spiel ruft `src/spieloekonomie.py`
auf. Prüfzahlen je Schritt: `test_oekonomie_uhr` 42 · `test_lokale_forschung` 47 · `test_versorgungsziel` 69 ·
`test_oekonomie_kern_unabhaengig` 158 · `test_lokale_lager` 70 · `test_warentransport` 45 ·
`test_warenrezepte` 26 · `test_ausbildungsauftraege` 49 · `test_spieloekonomie` 370 · `test_botkern` 90 ·
**`test_handel_transaktion` 101**.

**Schritt 8b im Einzelnen (Was der Handel jetzt kann und was eigenen Zusatz ist):** `handel_start`
sperrt Gold **und** Ware beim Start (mit anteiliger Importherkunft), `handel_abschluss` bucht Ankunft
und Rückkehr **genau einmal**, bei Ablehnung kehren Gold und Ware vollständig zurück, verlorene Orte
erzeugen **keine** Geistergutschrift (Gut bleibt am Vertrag bzw. wird als `verlorenes_sperrgut`
vermerkt). **Eigener Zusatz, den Daniel streichen kann:** `handel_entscheiden(vertrag, angenommen)`
samt Vertragsfeld `entscheidung` — ohne ihn war die **belegte** Ablehnungsregel (Handbuch S. 20:
„Bei Ablehnung kehrt die Karawane MIT den Waren zurück, Gold wird nie übertragen") **nicht
erreichbar**, weil der Entwurfscode automatisch annahm, sobald der Verkäuferort noch lebte (der
Ablehnungszweig war toter Code). Ebenso: `auftraege.spieldaten_anwenden` lässt jetzt **auch** einen
Fremdvertrag unberührt (wie einen Eigentransport).

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
| **Belegte Regel = toter Zweig** | Eine belegte Handbuchregel kann im Entwurfscode **unerreichbar** sein (Handel: Annahme automatisch, Ablehnung nie möglich). Wer eine belegte Regel als „gebaut" meldet, muss den Zweig **auslösen** — sonst ist die Regel nur Text. Gefunden hat es die Prüfdatei, nicht das Nachdenken. |
| **Protokollzeile vergessen** | Commit `356b48a` (20:08, Kontext-Paket angelegt) hatte **keine** Protokollzeile; sie wurde nachgetragen. Auch ein reiner Doku-Commit ist ein grober Schritt. |
| **`patch`-Werkzeug mit falschem Anker** | Wird eine neue Zeile **an** einer bestehenden eingefügt, muss die Ankerzeile im Ersatztext **wieder vorkommen** — sonst löscht man sie still (hier: Protokollzeile 56 verdrängt, aus `git show HEAD:` zeichengleich wiederhergestellt). |
| `git add -A` | **Nie** vor der Kinderprüfung — sonst wandern ungeprüfte Dateien in den Commit. `git status --short` muss genau die erwarteten neuen Dateien zeigen. |
| Kindberichte | sind **Selbstauskunft**: ERGEBNIS-Zahl selbst nachfahren, Wachen-Namen überfliegen, erst dann committen. |
| Kinder parallel zum Sammellauf | stören ihn — nicht gleichzeitig laufen lassen. |
| `.exe`-Bau | währenddessen **kein** Spiel starten. Nach dem Bau: Startprüfung aus einem **anderen** Ordner (Prozesse, Fenstertitel, Antwortbereitschaft, WerFault). |
| `run_tests.bat` hat CRLF | `sed -i` findet dort **nichts** (still, exit 1) → `patch`-Werkzeug benutzen, danach mit `grep -o` prüfen. |
| Prüfmodule | führen sich beim `import` **aus** (`sys.exit(bericht())`) — Helfer nur über `try: import … / except SystemExit: sys.modules[…]` holen. |
| `src/botkern.py` | muss **reines ASCII** bleiben (Prüfung „reines ASCII"); `—` bricht sie. |
| `docs/PROJEKT_STAND.md`, Abschnitt „Der EINE nächste Schritt" | darf **kein `###`** enthalten (`test_zieluebergabe`) → Zwischentitel als **Fett**. |
| Prüf-Fehler ≠ Ausreißer | erst nachsehen, dann abtun (belegte Fälle: zu lockere Prüfung, Haus auf unerlaubtem Feld). |
| Messfehler zuerst bei sich suchen | zwei „Fehler" in Schritt 7 waren **Datensatzfehler**, nicht Code. |
| Kinderarbeit | nur `deepseek-flash`; Kindberichte sind kein Beweis. |

## 6. Nicht erneut zu prüfen (Beleg + Datum)

* Schritte **0–8a** — Commits und Prüfzahlen in Abschnitt 3 + Tabelle in `PROJEKT_STAND.md` 0c.
* **Schritt 8b** — Commit `25466f5`, `tests/test_handel_transaktion.py` **101/0/0**, Sammellauf
  **3654/0/21** über 51 Dateien (20:27). Die neue Prüfdatei steckt in `run_tests.bat`.
* `test_baseline` ist seit **18:17 deterministisch** (Haus auf einem erlaubten Feld, dreimal 40/0/0).
* Die `.exe` **startet** (**20:35** aus anderem Ordner: Titel, antwortet 10/20/40 s, 0 Fehlerberichte,
  0 offene Prozesse).
* Der Sammellauf wird **nur nach einer echten Änderung an `src/`** wiederholt (nicht nach
  Dokument-Commits).
* Fehlend von Schritt 8a: Prüfdatei `tests/test_bot_oekonomie.py` und Audit
  `docs/audits/pruefung_schritt8.md` — die zwei prüfenden Kinder wurden für die saubere Übergabe
  **gestoppt, bevor sie Dateien anlegten** (Auftragstext in Protokollzeile **53**).

## 7. Offene Entscheidungen für Daniel (nichts eigenmächtig geändert)

0. **Neu aus Schritt 8b:** `handel_entscheiden` + Feld `entscheidung` (nötig, damit die belegte
   Ablehnungsregel S. 20 erreichbar wird) und die kleine `spieldaten_anwenden`-Wache für
   Fremdverträge — beides kann er streichen lassen; dann gilt der Entwurf wörtlich (mit totem Zweig).
1. **Kampfverluste verdrahten** — Handbuchregel wörtlich (S. 23: Verlierer verliert einen Teil seiner
   Karren/Belagerungswaffen, Fluchtchance 40 % + 5 % je Sequenz; unentschieden kostet nichts);
   `src/kampf.py` hat sie **gebaut**, es fehlt die Anbindung. Offene Frage: **Prozent-Untergrenze oder
   nur Simulation?** → `docs/ENTWURF_KAMPFVERLUSTE.md`.
2. **Forschungsstufe global oder je Siedlung?** Handbuch **schweigt**; Bibliothek/Auftrag/Sperre
   belegt je Siedlung → `docs/audits/belege_forschung_je_siedlung.md` (V1/V2/V3).
3. **Reserve-Anzeige** in `zielstatus` (`bool(orte)`) ist gekennzeichneter **VORSCHLAG**, ändert den
   Sieg nicht.
4. **Skill-Kopie im Profil `coding` veraltet** (4.589 Byte vom 04.10. gegen 38 KB in `default`) — nur
   auf Daniels Wort nachziehen.
5. **Kostendeckel:** heute überschritten, für diesen Auftrag **freigegeben** mit Reserve 1,00 USD.

## 8. Wo die Details liegen (nur bei Bedarf lesen)

* Handbuch (Wahrheit): `docs/original/Spielanleitung_2009_Textfassung.txt`
* Ökonomie-Entwurf (die Vorgabe in 10 Schritten): `docs/audits/entwurf_spieloekonomie_sol_2026-10-05.txt`
* Handbuch-Abgleich: `docs/audits/handbuch_abgleich_2026-10-05.txt`
* Audits je Schritt: `docs/audits/pruefung_schritt3_4.md`, `…_schritt5.md`, `…_schritt6.md`, `…_schritt7.md`
* Stand/Historie: `docs/PROJEKT_STAND.md` (0c Tabelle, 0e Übergabe) · `docs/ENTWICKLUNGSPROTOKOLL.md`
* Werkzeuge: `tools/zieluebergabe.py` · `tools/protokoll_sichern.py` · `tools/build_exe.py`
* Sammellauf: `C:\Users\saras\AppData\Local\hermes\cache\scratch\sammellauf.py` (liest `run_tests.bat`)
* Startprüfung: `…\cache\scratch\exestart\startpruefung_1005_2035.ps1` (Prozesse, Titel, WerFault)
