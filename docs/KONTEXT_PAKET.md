# KONTEXT-PAKET — Nebelseetal Remake (Stand 06.10.2026, 08:25 · Zeiten mit `date` geholt)

> **✅ TEIL 8 IST FERTIG (06.10.2026, 08:25) — offen ist nur noch Schritt 10 (die Aktivierung).**
> **8a** Kartenfreischaltung ehrlich (`d937d47`) · **8b** Version/Modus + Migration (`e8edc1e`) ·
> Sammellauf **4061/0/22** über 52 Dateien · `.exe` **14.652.424 Byte**, SHA256 `c1523670aa307077…`,
> Dateizeitstempel **08:22:35**, gebaut **und** startgeprüft (Titel „Nebelseetal Remake“, antwortet
> +10/+20/+40 s, 0 Fehlerberichte, 0 offene Prozesse). Die **Pause** der Vorgängersitzung ist von
> Daniel am 06.10. um **08:08** aufgehoben („ok es geht weiter“). **Maßgeblich für den Stand sind
> `docs/PROJEKT_STAND.md` 0c und 0e** sowie die Abschnitte 1-3 dieses Pakets (unten nachgezogen).

**Diese Datei ist die Übergabe. Lies SIE zuerst (≈ 12 KB) und sonst nur, was hier als Zeiger steht —
`docs/PROJEKT_STAND.md` (69 KB) und `docs/ENTWICKLUNGSPROTOKOLL.md` (93 KB) sind Nachschlagewerke,
keine Einstiegslektüre.** Projekt: `D:\Arbeiten\Nebelseetal_Remake` (bash/MSYS, `python -X utf8`).
Ziel: fertige, fehlerfrei spielbare, passwortgeschützte Einzelspieler-`.exe` (Handbuch 2009 = Wahrheit).

---

## 1. Belegter Ist-Stand

| Was | Beleg |
|---|---|
| **Sammellauf** | **4061 bestanden · 0 Fehler · 22 Befunde · 52 Dateien** (08:1x; Teil 8a +17, Teil 8b +21 — davor 4023 nach Teil 7b) |
| **Arbeitsbaum** | **sauber** (`git status --short` leer), letzte Commits **`e8edc1e`** (Zeile 85, Teil 8b), **`d937d47`** (Zeile 84, Teil 8a), `2fc9431` (Sicherung vor dem Herunterfahren) |
| **`.exe`** | **14.652.424 Byte**, SHA256 `c1523670aa307077fd8be3c0858d52a44a1a20a40c024f1d2275658c4276ac75`, Dateizeitstempel **08:22:35** — **GEBAUT UND STARTPGEPRÜFT** (aus `…\cache\scratch\exestart`, anderem Ordner, `startpruefung_1006_0822.ps1`); enthält **Teil 8** zusätzlich zu 3a-7b; Vorgängerfassung gesichert (`…\cache\scratch\exe_alt_0821_vor_teil8.exe`, 14.652.257 Byte) |
| **Startprüfung** | **08:2x erledigt** (die Fassung nach Teil 8): genau **1** Prozess mit Fenster, Titel **„Nebelseetal Remake“**, antwortet bei **+10/+20/+40 s**, **0** Fehlerberichte (WerFault), danach **0 offene Spielprozesse**, Startordner leer (Protokollzeile 86) |
| **Sicherung** | `docs/SICHERUNGEN.md` — 16 führende Papiere mit Prüfsummen (01:0x, projektunabhängige Kopie unter `D:\Arbeiten\Hermes\Nebelseetal_Protokoll\`) |
| **Zielregister** | Diese Sitzung `20261006_011522_6f090e` führt ihr Ziel **aktiv** (Teil 8 → jetzt Schritt 10); am 06.10. um 01:2x pausiert, um **08:08** mit Daniels „es geht weiter“ wieder auf `active` gesetzt — `--pruefen` → **rc=0, kein fremdes aktives Ziel** |
| **Kosten** | **06.10. um 08:25 gemessen: 0,95 EUR / 4,00 EUR** (Rest **+3,05 EUR**, Lage **„OK“**; um 01:02 waren es 0,80). Der **05.10.** endete bei **7,25 EUR = ÜBER_LIMIT**. **Daniels Freigabe gilt:** nur `deepseek-flash`, kein teures Modell, keine Kinder, **1,00 USD DeepSeek-Reserve unangetastet** |

`git log --oneline -3` · `git status --short` · `python tools/zieluebergabe.py --pruefen` → alles in Sekunden.

## 2. Der EINE nächste Schritt

**Schritt 9 ist FERTIG — Teil 1 bis Teil 8 sind gebaut (Teil 8: 8a Kartenfreischaltung ehrlich,
8b Version/Modus + Migration). Offen ist als NÄCHSTER Schritt nur noch Schritt 10.**
Der Auftraggeber hat „Stück für Stück“ entschieden: nach JEDEM Teil Einzeltest + einmal Sammellauf +
Protokollzeile + kleiner Commit.

**Teil 8 ist FERTIG (06.10.2026, 08:16–08:25):** **8a** — die erfundene **„Vermessung“** ist weg:
`_unlock_next_map` ist **gelöscht** (kein Aufrufer; fragte `"vermessung"` ab, die es unter den 21
Originalforschungen nicht gibt, und benutzte `MAX_ACTIVE_MAPS`, das nirgends definiert ist), das
Gebietspanel sagt jetzt die Wahrheit (neue Karten kommen über den **Kartenvorrat**, die fünf
Weltregionen sind keine Siedlungskarten), `d937d47`. **8b** — Speicherung/Migration:
`stand_version`/`mode` im Spielstand, Altstand **ohne Versionsfeld** lädt als `mode="legacy"`
**mit sichtbarem Warnhinweis** und **ohne jede Umrechnung**, neue Partien `mode="oeokonomie-1"`,
`_day_accum` wird mitgesichert, `e8edc1e`. **Der Modus ist bis Schritt 10 nur ein MERKER** (Wache
P32 prüft, dass er nirgends verglichen wird). Belege: `test_oekonomie_einhaengung` **390/0/1**
(neu P31/P32), Sammellauf **4061/0/22**, `.exe` gebaut + startgeprüft.

**Der NÄCHSTE Schritt: Schritt 10 — Ereignisschleife `tick_bis` + die AKTIVIERUNG** (Entwurf
Z. 791-1018; **erst jetzt** darf der Ökonomiemodus aktiviert werden, Entwurf Z. 1092). Dazu gehört
die Umstellung der `main`-Uhr auf `spielsekunden` (genau **eine** Stelle mit `spielzeit.faktor()`).
**Erst nach der Aktivierung** sind die Ökonomie-Regeln im Spiel wirksam; bis dahin läuft der
Altmodus unverändert. **Erwartet:** betroffener Einzeltest grün, Sammellauf ohne Fehler (**4061**
bestanden, 22 Befunde, 52 Dateien), **Protokollzeile** (Zeit aus `date`),
`python tools/protokoll_sichern.py --protokoll`, kleiner Commit; ändert sich `src/` oder
`data/*.json`, am Ende die `.exe` neu bauen und aus einem **anderen** Ordner startprüfen.

**Teil 7 ist FERTIG (06.10.2026):** **7a** — der Gratisgewinn ist gesperrt (`_trade` schenkte Rohstoffe
ohne Gegenleistung und lehnt seither ehrlich ab, `01fe939`). **7b** — der **bestätigte Kaufvertrag**
läuft: `_trade` öffnet die **Maske für Ware, Menge und Preis**, `bot_als_ort` übersetzt den Bot in
einen fremden Ort (**gemessen:** `bot_als_dict` führt `besitzer`, `dimension`, `einheiten`, `x`, `y`
**nicht**), `handel_mit_bot` lässt **nur den Kern** prüfen und beidseitig sperren (fehlt Gold oder
Karawane im Ortslager, kommt der Fehlbetrag als **Übergang aus dem Reich**), `_fremdvertrag_buchen`
lässt die **Ankunft entscheiden** (der Bot nimmt an, wenn der Preis seinen **Schwellenpreis** erreicht)
und bucht **genau einmal**; `f7dc77d`. Belege: `test_oekonomie_einhaengung` **352/0/1** (neu P30),
`test_durchspiel` **56/0/2**, Sammellauf **4023/0/22** über 52 Dateien.

**Beide `.exe`-Prüfungen sind erledigt** (die offene Frage aus Teil 7a ist damit geschlossen): die
Fassung aus Teil 7a ist **nachgeholt** startgeprüft (14.641.733 Byte, `524d6260…`, Zeile 80), und die
`.exe` nach Teil 7b ist gebaut **und** startgeprüft (**14.652.257 Byte**, `5dc00158…`, Dateizeitstempel
**00:59:17**, Zeile 82).

> **ERLEDIGT (06.10., 00:38–00:40): die Startprüfung der `.exe` aus Teil 7a ist nachgeholt und
> BESTANDEN** — 14.641.733 Byte, SHA256 `524d6260e28daf74…`, Fenstertitel **„Nebelseetal Remake"**,
> antwortet bei **+10/+20/+40 s**, **0** Fehlerberichte (WerFault), danach **0 offene Spielprozesse**,
> Startordner leer (Protokollzeile **80**, Commit `d05af8d`). Der Befehl war in der vorigen Sitzung
> **nicht** gelaufen (er hing in der Freigabe) — deshalb fehlte die Zeile dort absichtlich; jetzt
> steht sie **mit Beleg** da.

**Die alten Beschreibungen des Teils (jetzt erfüllt) stehen darunter weiter:**

**Danach die Teile 7-8:** `_trade` über das bestätigte Angebot aus 8b oder eine deutliche
„noch nicht verfügbar"-Meldung (nie der Alt-Gratisgewinn) — **ERLEDIGT** (7a gesperrt, 7b gebaut) ·
`_unlock_next_map` (die „Vermessung" entfällt) + Migration (Altspielstand ohne Versionsfeld →
`mode="legacy"` mit Warnhinweis, neue Partien `mode="oeokonomie-1"`) — **OFFEN, das ist Teil 8**;
**erst danach** Schritt 10 (`tick_bis` und die Aktivierung, Entwurf Z. 791-1018) — **vorher darf der
Ökonomiemodus NICHT aktiviert werden** (Entwurf Z. 1092).

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
* **Teil 7 — `_trade`: FERTIG (06.10.2026).** **7a** hat den Gratisgewinn gesperrt, **7b** den
  **bestätigten Kaufvertrag** gebaut (Maske für Ware, Menge und Preis · Handelskarawane · der Bot
  entscheidet bei der Ankunft) — `01fe939`, `f7dc77d`. **Nie** wieder der alte Gratisgewinn.
* **Teil 8 — `_unlock_next_map`** (die erfundene „Vermessung" entfällt) und **Speicherung/Migration**
  (Entwurf Z. 788): Altspielstand ohne Versionsfeld → `mode="legacy"` mit Warnhinweis, neue Partien
  `mode="oeokonomie-1"`, keine automatische Konvertierung ohne Daniels Wort —
  **DAS IST DER NÄCHSTE SCHRITT (erst auf Daniels Wort).**
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
| **9** | **`main`-Anbindung + Migration — FERTIG (Teil 1 bis Teil 8 gebaut)** | 9.1 `c099c4e` · 9.2 `1ce4ae3` · 9.3a `a0d432d` · 9.3b `65c41bf` · 9.4 `5a46ad7` · 9.5 `fab8611` · 9.6a `ad12376` · 9.6b/c `0e4a08a` · 9.6-Rest `35e1bd1` · 9.7a `01fe939` · 9.7b `f7dc77d` · **9.8a `d937d47` · 9.8b `e8edc1e`** · `test_oekonomie_einhaengung` **390/0/1**, `test_durchspiel` 56/0/2, Sammellauf
**4061/0/22** |
| 10 | `tick_bis` + **Aktivierung** | **offen — der nächste Schritt** |

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
| **Ein Merker MUSS nach `clear()/update()` gesetzt werden** | `eintrag.clear(); eintrag.update(m)` (das Muster aus Teil 4) **löscht alles**, was vorher am Eintrag hing: in Teil 7b wurde `eintrag["heimgekehrt"] = True` davor gesetzt und war danach **weg** — der Vertrag blieb in der Auftragsliste stehen und wäre bei jedem Takt erneut gebucht worden. Gefunden hat es die Prüfung („bei der Rückkehr … Aufträge 0"), nicht das Nachdenken. Regel: den Merker **immer nach** der Übernahme setzen. |
| **`self.state` gibt es nur in der APP-Klasse, nicht in `GameState`** | In `GameState` heißen die Felder `self.settlements`, `self.bots`, `self.current_map`, `self.units`, `self.resources`; `self.state` gibt es nur in `NebelseetalApp`. Der erste Probelauf von `bot_standort`/`_fremdvertrag_buchen` brach mit `AttributeError` ab — der **fensterlose Probelauf VOR dem Testschreiben** hat es gefunden. Regel: neue `GameState`-Methoden zuerst mit einem kleinen Skript anlaufen lassen. |
| **Ein Name ist KEIN Beweis für seine Felder** | Das Papier sagte „der Bot braucht seine Form als Ortsdict — **vorher prüfen**, ob `besitzer`, `dimension`, `vorraete`, `einheiten`, `x`, `y` in `bot_als_dict` stehen". Sie stehen **nicht** (gemessen: es ist die Form für `botkern`). Statt `bot_als_dict` zu erweitern (das hätte `botkern` eine zweite Wahrheit gegeben) gibt es die zweite, klar benannte Übersetzung `bot_als_ort`. |

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
* **Schritt 9, Teil 7a (Gratisgewinn gesperrt)** — `01fe939`, `test_oekonomie_einhaengung` **319/0/1**,
  `test_durchspiel` **52/0/2**, Sammellauf **3986/0/22** (00:2x, 134 s).
* **Schritt 9, Teil 7b (der bestätigte Kaufvertrag)** — `f7dc77d`, `test_oekonomie_einhaengung`
  **352/0/1** (neu **P30**: zwölf Ablehnungen ohne jede Buchung · Sperre beidseitig · Ankunft/Annahme ·
  belegte Ablehnung mit vollständiger Rückgabe · kein doppelter Abschluss · Gesamtbestand gerechnet ·
  Quelltextwachen), `test_durchspiel` **52 → 56/0/2** (ganzer Weg mit echten Werten),
  `test_handel_transaktion` **101/0/0**, `test_auftraege` 111/0/1, `test_botkern` 90/0/0,
  `test_gui_fehler` 24/0/1, `test_startspiel` 54/0/0, `test_gebaeude_wirkung` 120/0/1, Sammellauf
  **4023/0/22** über 52 Dateien (00:5x, 100 s); am **lebenden Fenster** gemessen (Maske „Handel mit
  Haug" mit Ware/Menge/Preis, Schwellenpreis 300, Knopf gesperrt ohne Handelskarawane).
* Die **`.exe` nach Teil 8** startet (**08:22:35**, **14.652.424 Byte**, SHA256 `c1523670…`;
  Protokollzeile 86) und die Vorgängerfassungen sind ebenfalls startgeprüft (Zeile 80 für 7a,
  Zeile 82 für 7b).
* Der Sammellauf wird **nur nach einer echten Änderung an `src/`** wiederholt.
* **Schritt 9, Teil 8a** — `d937d47`, `test_oekonomie_einhaengung` **369/0/1** (neu P31),
  `test_weltkarte` **82/0/0**, Sammellauf **4040/0/22**.
* **Schritt 9, Teil 8b** — `e8edc1e`, dieselbe Prüfdatei **390/0/1** (neu P32), Sammellauf
  **4061/0/22** über 52 Dateien (08:1x, 98 s).
* `test_bot_oekonomie.py` und `docs/audits/pruefung_schritt8.md` fehlen weiterhin (zwei gestoppte
  Kinder; Auftragstext in Protokollzeile 53).

## 7. Offene Entscheidungen für Daniel (nichts eigenmächtig geändert)

0. **Aus 8b (ENTSCHIEDEN und gebaut):** `handel_entscheiden` + Feld `entscheidung` (macht die belegte
   Ablehnungsregel S. 20 erreichbar) und die Wache in `auftraege.spieldaten_anwenden` für
   Fremdverträge sind in **Teil 7b eingebaut** (`f7dc77d`). **Offen bleibt nur:** *wann* der Bot
   ablehnt — gebaut ist der **Schwellenpreis** (`botkern.handelspreis`), belegt ist nur, **dass** es
   eine Ablehnung gibt. Streichbar, dann lehnt der Bot nie ab (toter Zweig wie im Entwurf).
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
7. **Kostendeckel:** heute **nicht** überschritten — **0,95 / 4,00 EUR** (um 08:25 gemessen, Lage
   „OK“, Rest **+3,05 EUR**); die Freigabe (nur `deepseek-flash`, kein teures Modell, keine Kinder,
   **Reserve 1,00 USD DeepSeek**) gilt weiter.

## 8. Wo die Details liegen (nur bei Bedarf lesen)

* Handbuch (Wahrheit): `docs/original/Spielanleitung_2009_Textfassung.txt`
* Ökonomie-Entwurf (die Vorgabe in 10 Schritten): `docs/audits/entwurf_spieloekonomie_sol_2026-10-05.txt`
* Handbuch-Abgleich: `docs/audits/handbuch_abgleich_2026-10-05.txt`
* Audits je Schritt: `docs/audits/pruefung_schritt3_4.md`, `…_schritt5.md`, `…_schritt6.md`, `…_schritt7.md`
* Stand/Historie: `docs/PROJEKT_STAND.md` (0c Tabelle, 0e Übergabe) · `docs/ENTWICKLUNGSPROTOKOLL.md`
* Werkzeuge: `tools/zieluebergabe.py` · `tools/protokoll_sichern.py` · `tools/build_exe.py`
* Sammellauf: `C:\Users\saras\AppData\Local\hermes\cache\scratch\sammellauf.py` (liest `run_tests.bat`)
* Startprüfung: `…\cache\scratch\exestart\startpruefung_1006_0100.ps1` (die neueste; Prozesse, Titel,
  WerFault, Startordner) — die Prüfung läuft als **eigener, einfacher Befehl** aus einem **anderen**
  Ordner
* Bau-Umgebung für die `.exe` (Zwischenspeicher, 24 h): `…\cache\scratch\nebel_bauvenv`
  (`uv venv --python 3.14.7` · `uv pip install pyinstaller`), Aufruf mit `--python …/Scripts/python.exe`
