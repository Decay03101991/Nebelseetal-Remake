# STAND 11.11.2026, 14:22 - Gesamtaudit gefahren: 32 Befunde, 30 bestaetigt, Bauplan in vier Stufen (Register 398 bis 402)

> Neuester Block. Darunter 13:38 (fuenf Entscheidungen; 392 bis 397), 13:25 (Frischstart-Paket wartet;
> 387), 10.11. 21:50 (G2/G3, Sammellauf, neue EXE; 381 bis 386).

**Der Gesamtaudit ist gefahren und nachgerechnet.** Vier Pruefgaenge parallel (deepseek-flash, read-only,
992 s), **32 Befunde**; jeder einzelne von mir selbst nachgemessen: **30 bestaetigt**, einer in der
behaupteten Form widerlegt (`K6` Sperrzeit - der Schluessel heisst `sperrzeit_stunden` und wird gelesen),
einer teilweise (`K8`). Dokument: `docs/audits/GESAMTAUDIT_20261111.md`. Kein `src/`- und kein
`data/`-Eingriff, kein Spielstart, die EXE `4124b335...` unberuehrt.

**Die vier schwersten, gemessen:**

- **Kampfbericht nennt die doppelte Beute** - `kampf._beute` 20/20 gegen gebucht 10/10 (`main.py:6243`).
- **Wallpunkte zwei Summen** - zwei Doerfer Wallstufe 2: je Dorf 16, `spielschicht.punkte` 8; betrifft das
  Messwerkzeug, aus dem die Registerzahl "3,5 Punkte je Spieltag" stammt.
- **`run_tests.bat` ist dauerhaft rot** - `tests/test_weltkarte.py` bricht mit `AttributeError: ...
  'welt_zelle'` ab, ohne ERGEBNIS-Zeile (selbst gelaufen 11.11.2026). Der Sammellauf ist nicht betroffen.
- **Ein Siedler wird nur den Bots abgezogen** - `spielschicht._baukosten` liefert `siedler: 1`, obwohl
  `siedler_bindung_aktiv()` False ist; `main.py:2982` nimmt den Posten beim Spieler heraus.

**Sechs oeffentliche Texte sagen Unwahres** (Register 401): `index.html` nennt Pakt/Rache als "nicht
eingebaut" (gebaut), sagt die Handelspunkte wuerden nicht gebucht (werden gebucht); `README.md` nennt ein
ZIP und eine EXE, die es nicht gibt (Version aus `data/version.json` ist `V_0.0.3`), den Speicherordner
eine Ebene zu hoch, und "20 Limbus-Dimensionen, 14 leer" (die Datei fuehrt **6**, keine leer);
`release_vorlage/*.txt` tragen noch V_0.0.1 und "rund 82 MB". **Das ist derselbe Stoff, den der
Claude-Auftrag zur Praesentation prueft** - hier die gemessene Grundlage.

**Bauplan (nach Daniels Test, in EINEM Zug mit G8, G9 und der Wall-Entscheidung):**
Stufe 1 die sieben Spieler-Fehler (K1, K3, U1, U2, U3, U4, U7) - Stufe 2 Pruefstand (K2, D8, D3/D4/D5,
D6/D7) - Stufe 3 die sechs Texte (P1 bis P6) - Stufe 4 Aufraeumen ohne Spielwirkung (K5, K6-Rest, K7, K8,
U5, U6, D1, D2, P7, P8).

**Guthaben (Register 403, von Daniel abgelesen 14:28):** **11,56 USD** Guthaben, **68,43 USD**
Gesamtverbrauch - **-0,34 / +0,34** seit 13:17. Darin: Register und Dokumente dieser Sitzung, der
Gesamtaudit mit vier Pruefgaengen samt Nachrechnung, sechs Commits. Opus ist Abo (nicht enthalten),
Sammellauf und EXE-Bau sind CPU-Zeit.

**Unveraendert offen:** Daniels Testbogen ist leer (Anleitung `976b9aac...`, Schreibordner nur `tor.json`);
die Skill-Aenderungen `0e5b3c84`/`9ce5a020` sind gestellt (Kennung `e44401db`) und warten auf
`/skills pending`.

# STAND 11.11.2026, 13:38 - Testbogen noch leer; fuenf Entscheidungen gefallen, Gesamtaudit laeuft (Register 388 bis 396)

> Neuester Block. Darunter 13:25 (Frischstart-Paket wartet; 387), 10.11. 21:50 (G2/G3, Sammellauf, neue
> EXE; 381 bis 386), 17:05 (Desktop geraumt, Guthaben; 379/380), 11:52 (Opus-Lauf; 372 bis 378).

**Sitzung 34 (13:25 bis 13:31):** Kopf geprueft - `46103e2` = `ls-remote origin main`, Arbeitsbaum nur
`cache/`. Uebergabe hashgleich gelesen (`d2dce233…`), die Desktop-Kopie geloescht, die Archivfassung
bleibt. Sitzung umbenannt in `11.11.26_V_0.0.3_Session_34` (Session_33 war die letzte belegte).

**Erste Aufgabe - der Bogen ist LEER, nichts ausgewertet:** `ANLEITUNG_UND_TESTBOGEN_FRISCHSTART.md`
auf dem Desktop hat weiterhin SHA256 `976b9aac…`, 7.209 Byte, mtime 10.11. 21:49; im Schreibordner
`~/.nebelseetal` liegt nur `tor.json`, also **kein** `savegame_slot*.json` - es wurde noch nicht
gespielt. **EXE und Anleitung bleiben unberuehrt** (Daniels Wort vom 11.11.).

**Zwei offene Fragen aus dem Abgleich beantwortet (Register 388/389), ohne Codeaenderung:**

- `punktestand()["krieg"]` **fuehrt** die Wallpunkte (Einheiten + `wall_kriegspunkte()`,
  `main.py:4131`). Folge: die erste Palisade (Stufe 1 = 1 Kriegspunkt) **beendet den Goetterschutz**
  im naechsten Takt - handbuchkonform (S. 6), aber eine Gestaltungsfrage an Daniel.
- Die Ansicht »Voraussetzungen« ist **vollstaendig** (21 von 21 Forschungen mit Bedingung) und erfuellt
  Handbuch S. 12.

**Neuer Befund G9 (Register 390):** `forschungspfad.schaltet_frei()` liefert `waren` / `einheiten` /
**`gebaeude`**, die Forschungs-Ansicht (`main.py:15671-15684`) verbaut nur `waren` und die unmittelbaren
Einheiten. Gemessen: `schaltet_frei("Baukunst")` = 0 Waren, 0 Einheiten, **14 Gebaeude** - `_teile`
bleibt leer, **die Zeile fehlt ganz**; auch `Verteidigungsanlagen` bleibt unsichtbar. **Nicht gebaut**,
weil ein `src/`-Eingriff Sammellauf und neue EXE nach sich zieht; das gehoert hinter Daniels Test.

**Registerluecke 336 (Register 391):** 384 Zeilen, hoechste Nummer 387, fehlend **272, 273 und 336**.
336 war nirgends notiert; der Inhalt ist nicht belegt. **Nicht umnummeriert** - naechste freie Sachzeile
ist **392**.

**Pruefungen dieser Sitzung:** `test_textqualitaet` **465/0** (141 Dokumente), `test_protokoll` 28/0/1
(bekannter Befund), `test_projektpfade` **131/0**. Kein `src/`- und kein `data/`-Eingriff - ein
Sammellauf ist **nicht** faellig.

**Daniels Antworten (13:38, EINE Runde, fuenf Fragen - Register 392 bis 396):**

1. **G8:** der Drosselungs-Regler sitzt **im Dialog »Auftrag anlegen« als Prozentwahl neben dem Ziel**.
2. **G9:** bauen **nach dem Test**, zusammen mit allem aus dem Bogen (ein Sammellauf, eine EXE).
3. **Palisade:** **Wallpunkte loesen den Goetterschutz nicht aus** - der Schutz endet nur bei echtem Kampf;
   die Anzeige fuehrt die Wallpunkte weiter.
4. **Skill-Vormerkungen** `0e5b3c84` und `9ce5a020`: **beide freigegeben**.
5. **Gesamtaudit:** **jetzt starten**, nur lesend, Repo bleibt unberuehrt.

**Naechster Schritt:** Gesamtaudit fahren, Befunde nach eigener Nachrechnung eintragen
(`docs/audits/GESAMTAUDIT_20261111.md`); sobald Daniels Bogen gefuellt ist, ihn auswerten - danach G8, G9
und die Wall-Aenderung in EINEM Zug bauen (Sammellauf, neue EXE, Desktop-Paket raeumen).

# STAND 11.11.2026, 13:25 - Frischstart-Paket wartet unberuehrt auf dem Desktop, Daniels Ergebnisse kommen heute (Register 387)

> Neuester Block. Darunter 10.11. 21:50 (G2/G3, Sammellauf, neue EXE; 381 bis 386), 17:05 (Desktop
> geraumt, Guthaben; 379/380), 11:52 (Opus-Lauf; 372 bis 378), 11:02 (Repo-Weg; 369).

**Daniels Wort (11.11.2026):** »die beiden bleiben unberuehrt am desktop meine ergebnisse liefere ich noch
heute«. Also: **EXE und Anleitung NICHT anfassen, nicht aufraeumen, nichts umbenennen.** Erst wenn seine
Antworten da sind, wird ausgewertet; **danach** geht die EXE vom Desktop (sein Wort vom 10.11.).

**Nachgeprueft (11.11., 13:17):** die zwei Dateien auf dem Desktop sind hashgleich zu dem, was Daniel
hochgeladen hat - EXE `4124b335065366fbcf8e1696edf3c3f1fa8045090b7a7791641b9e0214c67df8`
(83.342.035 Byte), Anleitung `976b9aacb263f1f9323097bcc7300b1a4c6ad4df83afefa5507ea05d047239aa`
(7.209 Byte, 60 Punktzeilen, noch **keine** Antworten). Im Schreibordner liegt weiterhin nur `tor.json` -
es wurde also noch nicht gespielt.

**Guthaben (Register 387, von Daniel abgelesen 13:17):** **11,90 USD** Guthaben, **68,09 USD**
Gesamtverbrauch - **-0,14 / +0,14** seit 10.11., 17:0x. Opus-Lauf nicht enthalten (Abo).

**Der naechste Schritt:** auf Daniels Bogen warten. Ist er gefuellt, **jeden Punkt als eigene
Registerzeile** mit Fundstelle (»Bogen B05«), leere Punkte benennen - nichts ergaenzen. Danach die EXE vom
Desktop nehmen und den Desktop ohne Nebelseetal-Rest belegen.

**Zwei Dinge brauchen danach Daniel:** (1) wo der Regler fuer die Drosselung sitzt (Befund G8, Register
383 - die Regel ist gebaut, aber im Spiel nicht bedienbar); (2) die Freigabe der aelteren
Skill-Vormerkungen `0e5b3c84` und `9ce5a020`.

# STAND 10.11.2026, 21:50 - G2 und G3 gebaut, 218/218 gruen, neue EXE liegt mit der Anleitung auf dem Desktop (Register 381 bis 386)

> Neuester Block. Darunter 17:05 (Desktop geraumt, Guthaben; 379/380), 11:52 (Opus-Lauf und Abgleich;
> 372 bis 378), 11:02 (Repo-Weg; 369), 10:28 (Testbogen und Paket; 367/368), 09:56 (Entscheidungen; 366).

**Daniels Entscheidungen (21:2x):** (1) Goetterschutz **eine Quelle** - 7 Tage ODER erster Kriegspunkt,
die Anzeige zieht nach. (2) **Drosseln verzoegert auch die Reise**. (3) **Beides vorher einbauen**, Test
beginnt spaeter - gesagt, getan.

**Gebaut (Register 381/382):** `spielschicht._goetterschutz_gilt` fragt das Kennzeichen `noob_protection`
aus dem Spielstand, nur Altstaende ohne Kennzeichen rechnen das Zeitfenster (`test_spielschicht`
**148/0**, drei neue Pruefungen). `auftraege.reisezeit_sekunden` bekommt `drosselung_prozent` und teilt
durch `Tempo = 1 - Drosselung/100` (Deckel 90), `starten` reicht durch, `offene_luecken` sagt die Wahrheit
(`test_auftraege` **143/0**, fuenf neue Pruefungen).

**Ehrlicher Nebenbefund (Register 383):** die Drosselung ist im Spiel **nicht bedienbar** - kein Aufrufer
ausserhalb `auftraege.py` setzt den Wert, auch kein Bot. Die Regel laeuft, ist aber im Test nicht
ausloesbar. Ein Bedienelement ist ein eigener Schnitt und braucht Daniels Entscheidung, wo es sitzt.

**Sammellauf (Register 384):** **218 von 218 gruen**, 0 rot, 2 ausgesetzt, **999 s**, 220 Dateien,
**9.448 Pruefungen**, 81 Befunde - gestartet NACH dem letzten Fix. Log
`docs/audits/sammellauf_20261110_2126.log`.

**Neue EXE (Register 385):** **83.342.035 Byte, SHA256 `4124b335065366fbcf8e1696edf3c3f1fa8045090b7a7791641b9e0214c67df8`**;
Altbau `a7035101…` in `archiv/builds/20261110_vor_g2_g3/`. Startpruefung: Passworttor sichtbar (PID 5768,
Responding True, Screenshot `docs/audits/exe_g2g3_start_20261110.png`), danach beendet, `game.lock`
entfernt, Schreibordner enthaelt nur `tor.json`.

**Desktop-Paket (Register 386):** **genau zwei Dateien** - die neue EXE und
`ANLEITUNG_UND_TESTBOGEN_FRISCHSTART.md` (7.209 Byte, `976b9aac…`) mit Block 0 bis G und einem **leeren
Block E fuer Daniels eigene Tests**. Frischstart vorbereitet: die drei alten Spielstaende und der
Geschichts-Merker liegen in `C:\Users\saras\.nebelseetal\archiv\vor_frischstart_20261110_2117\`.

**Der naechste Schritt:** Daniels Frischstart-Test abwarten; danach jeden beantworteten Punkt als eigene
Registerzeile mit Fundstelle (»Bogen B05«), leere Punkte benennen. **Danach gehoert die EXE wieder vom
Desktop entfernt** (Daniels Wort: »die nach dem test wieder vom desktop weg soll«).

# STAND 10.11.2026, 17:05 - Desktop geraumt, Guthaben eingetragen; naechster Schritt ist das Frischstart-Paket (Register 379/380)

> Neuester Block. Darunter 11:52 (Opus-Lauf und Abgleich; 372 bis 378), 11:02 (Repo-Weg; 369), 10:28
> (Testbogen und Paket; 367/368), 09:56 (die zwei Entscheidungen; 366).

**Daniels Auftrag (17:0x):** »ich brauche die zu testende exe auf dem desktop und die Tests die ich fuer dich
machen muss/soll plus raum fuer eigene tests. Bitte lass mich einen komplett frischen spielstand erstellen und
komplett von beginn an testen. Alles bitte in der neuen session.« Dazu: »dort soll nur noch die exe und die
anleitung sein«.

**Erledigt (Register 380):** die lose `LIESMICH.txt` und der Ordner `Nebelseetal_Spieltest_4\` sind nach
`D:\Arbeiten\Hermes\Desktop_Ablage\20261110_Spieltest4\` **verschoben** (nicht geloescht, Hashsummen davor
gesichert); `ls ~/Desktop` zeigt keinen Nebelseetal-Rest.

**Guthaben (Register 379, von Daniel abgelesen):** **12,04 USD** Guthaben, **67,95 USD** Gesamtverbrauch -
**-0,59 / +0,59** seit 09:35. Der Opus-Lauf ist darin **nicht** enthalten (Abo, kein USD gebucht).

**Die naechste Aufgabe ist das Frischstart-Paket** (Uebergabe 1704, Abschnitt 4a): Spielstaende aus
`C:\Users\saras\.nebelseetal\` sichern (`savegame_slot1..3.json`, `geschichte.json`; `tor.json` bleibt), die
vorhandene EXE (`a7035101…`, kein Neubau) auf den Desktop legen und **EINE** Anleitung schreiben, die den
Testbogen fuer den Weg von null enthaelt - mit einem **leeren Block fuer Daniels eigene Tests**. Danach
Startpruefung (Passworttor), `game.lock` entfernen, und Daniel in EINER Runde melden.

# STAND 10.11.2026, 11:52 - Opus-Prueflauf gefahren und abgeglichen: fuenf alte Befunde erledigt, sechs neue (Register 372 bis 378)

> Neuester Block. Darunter 11:02 (Repo-Weg; 369), 10:28 (Testbogen und Paket; 367/368), 09:56 (die zwei
> Entscheidungen; 366), 00:28 (neue EXE mit D-5b; 364) und 23:52 (D-5b gebaut; 361).

**Der Lauf ist durch.** Ein Aufruf, ausserhalb des Projekts, nur `WebFetch`, gegen das Repo am gepinnten
`b341d93`: **EXIT 0, 432,4 s, 10.894 Antwortzeichen**, 58.022 Cache-Neu- und 15.874 Ausgabe-Token (9.076
Denken). Abo-Lauf - das Werkzeug meldet 1,872 USD als API-Gegenwert, **abgebucht ist nichts**. Antwort:
`docs/audits/OPUS_PRUEFUNG_20261110_1115.md`, Messung `opus_usage_20261110_1115.json`.

**Zwei Werkzeugfehler kamen davor (Register 370), beide behoben:** `os.path.commonpath` warf
laufwerksuebergreifend `ValueError` (Temp C: gegen Projekt D:), und `shutil.which('claude')` liefert die
endungslose npm-Huelle, die `subprocess` nicht startet. Neue Wache `tests/test_opus_lauf_arbeitsordner.py`
**13/0**.

**Abgleich `docs/audits/ABGLEICH_OPUS_20261110.md`:** von den zwoelf alten Behauptungen sind **fuenf
erledigt** (2 zwei Kampfsysteme, 3 Gebaeude ohne Forschungspruefung, 4 Tageszaehlung, 6 Ausbildungskopplung,
10 Siegbedingung), **sechs bestaetigt** (1, 5, 8, 9, 11, 12), **eine offen** (7 Ansicht »Voraussetzungen«).
Alle sechs Rechenaufgaben nachgerechnet (`tools/opus_nachrechnen.py`); **ein Modellfehler:** die
»kleinste Loesung« ist 90, nicht 91 - 3^3+3^3+3^3+2^3+1^3 = 90, Gesamt 301, Forschungszeit 880 s.

**Sechs neue Befunde (373 bis 378), keiner ein Absturz:** G1 `kampf.py:5` verspricht eine
Rueckfallsicherung, die eine Wache verbietet · G2 zwei Goetterschutz-Regeln mit verschiedener Grundlage
(`main.py:7920` gegen `punkte.py:210`, in Betrieb ueber `spielschicht.py:845`) · G3 Drosselung wirkt auf die
Kosten, nicht auf die Reisezeit · G4 `ZIEL_PUNKTE_VERWORFEN` wird nirgends gelesen · G5
`BEUTE_ANTEIL_PROZENT` steht nur in Texten · G6 `dauer_sekunden` bricht ab, wenn kein Regeltext »Quadrat«
enthaelt (heute enthalten).

**Eingang abgelegt (Register 371):** Daniels Rueckgabe von Claude Opus 5.5 zum Testbogen liegt hashgeprueft
unter `docs/eingaenge/LLM_20261110_TESTBOGEN/` (5.571 Byte, `550ca2f6…`); sie enthaelt **keine Antworten**
(46 Punktzeilen, 46 leere Antwortspalten).

**Der naechste Schritt:** Spieltest 4 auswerten, sobald Daniels Bogen gefuellt ist
(`Nebelseetal_Spieltest_4\TESTBOGEN_Spieltest_4.md`, heute 11:2x noch hashgleich zur leeren Fassung
`6301d9e0…`, `Belege\` leer). **Zwei Entscheidungen liegen bei Daniel:** die Semantik des Goetterschutzes (G2)
und ob die Drosselung auf die Reisezeit wirken soll (G3). **Offen ausserdem:** vollstaendiger Gesamtaudit,
Vormerkungen `0e5b3c84`/`9ce5a020`, Ghul-Kacheln, elf C2-Gebaeude, Register 272/273, DeepSeek-Export 09.11.

# STAND 10.11.2026, 11:02 - Opus-Prueflauf auf den Repo-Weg umgestellt; der Test laeuft in der naechsten Sitzung (Register 369)

> Neuester Block. Darunter 10:28 (Testbogen und Paket vorbereitet; 367/368), 09:56 (die zwei
> Entscheidungen; 366), 00:28 (neue EXE mit D-5b; 364) und 23:52 (D-5b gebaut; 361).

**Daniels Entscheidung (11:0x):** **Weg A** - Claude Code ueber das Abo, kein Token-Preis - und
ausdruecklich: **das Modell arbeitet ueber die Repo, nicht lokal**.

**Umgesetzt:** `tools/opus_paket_bauen.py` holt jede benutzte Datei per HTTP aus dem veroeffentlichten Repo am
gepinnten Commit und schneidet die Funktionen aus dem BLOB; eine Herkunftstabelle im Paket nennt Abruf-URL und
SHA256 je Datei (**fuenf bytegleich**, `src/auftraege.py` nur in den Zeilenenden - Arbeitskopie CRLF, Blob LF,
inhaltlich gleich). `tools/opus_lauf.py` faehrt in einem **leeren Arbeitsordner ausserhalb des Projekts**, erlaubt
nur `WebFetch` und verbietet `Read`, `Grep`, `Glob`, `Bash`, `Write`, `Edit`.

**Paket:** `docs/audits/OPUS_PRUEFPAKET_20261110.md`, **41.026 Zeichen, 768 Zeilen, rund 11.400 Prompt-Token**.
**Der scharfe Lauf ist NICHT gelaufen** - keine `OPUS_PRUEFUNG_*.md` vorhanden. Er ist die erste Aufgabe der
naechsten Sitzung.

**Offen ausserdem:** Spieltest 4 (Daniel heute Abend, Bogen Fassung 2 im Ordner `Nebelseetal_Spieltest_4\`).
# STAND 10.11.2026, 10:28 - Spieltest 4 vorbereitet: EXE, Testbogen und Pruefpaket liegen bereit (Register 367)

> Block vom 10.11.2026, 10:28. Darunter 09:56 (die zwei Entscheidungen; 366), 00:28 (neue EXE mit D-5b; 364) und
> 23:52 (D-5b gebaut; 361).

**Was heute Abend passiert:** Daniel macht **Spieltest 4** auf `Nebelseetal_Pre_Release_V_0.0.3.exe`
(83341753 Byte, SHA256 `a7035101...`) und fuellt dabei den **Testbogen** aus. Beides liegt auf dem Desktop in
`Nebelseetal_Spieltest_4\` - die EXE hashgleich, der Bogen hashgleich zur Projektfassung, dazu ein Ordner
`Belege` fuer Bildschirmfotos und ein `LIESMICH.txt`.

**Der Bogen ist inzwischen Fassung 2** (Register 368): Daniel hat eine Ueberarbeitung von Claude
Opus 5.5 zurueckgegeben - **ohne Antworten**, aber mit zwei echten Verbesserungen: eindeutige Nummerierung
(`0.1` bis `0.4` fuer das Geraet statt `G1` bis `G4`, das `G` war doppelt vergeben) und eine Pruefzeile `A0`
fuer den Hash der EXE. SHA256 `4e368cf1142e789c...`.

**Der Bogen** hat 40 nummerierte Punkte in sieben Bloecken (Geraet, Start und Tor, Gestaltung D-5/D-5a/D-5b,
bekannte Grenzen, Spielablauf, freie Beobachtung, Fehler woertlich). Jeder Punkt wird beim Auswerten EINE
Registerzeile mit Fundstelle (z. B. „Bogen B07“).

**Fuer ein starkes Modell vorbereitet, NICHT gelaufen:** `docs/audits/OPUS_PRUEFPAKET_20261110.md`
(38.935 Zeichen, 743 Zeilen, rund 10.815 Prompt-Token) mit den zwoelf Behauptungen des Gesamtaudits vom
31.10.2026, einer Sichtung von heute und der Rechenpflicht zur Spieluhr x180. Gebaut von
`tools/opus_paket_bauen.py`, gefahren wuerde es mit `tools/opus_lauf.py --scharf`. **Der bezahlte Aufruf
wartet auf Daniels Zustimmung.**

**Naechster Schritt:** Testbogen auswerten (eine Registerzeile je Befund), dann die Befunde abarbeiten -
**nicht** vorab nachbessern, was auffallen koennte.
# STAND 10.11.2026, 09:56 - beide offenen Entscheidungen beantwortet (Register 366); Spieltest 4 liegt bei Daniel

> Block vom 10.11.2026, 09:56. Darunter 00:28 (neue EXE mit D-5b; 364), 23:52 (D-5b gebaut; 361) und 20:24 (D-5a; 356).

**Daniels Wort (10.11.2026, 09:56):** "ok nach Empfehlung" - damit sind beide Fragen aus der Uebergabe 0937 entschieden.

**Entschieden:** (1) Der Eckenradius des Goldrahmens bleibt **14 px**; Chris' gemessene 30 px braeuchten ein
3x3-Leisten-Layout (8 Bildlabels) und eine Anpassung von `test_weltkarte_rahmen`, das vier Bildleisten
fordert - ein eigener Schnitt, nicht der Weg zu Spieltest 4. (2) `docs/audits/GESAMTAUDIT_BEFUNDE_20261031.md`
wird als **Beleg aufgehoben**: die zwoelf Befundzeilen sind vollstaendig, abgebrochen ist nur der dritte Punkt
unter "Nicht beurteilbar". Herkunft und Grenze im neuen `docs/audits/PRUEFVERMERK_GESAMTAUDIT_HERKUNFT_20261110.md`;
die Datei ist damit versioniert.

**Repariert:** die D-5b-Zeile im Entwicklungsprotokoll trug den Platzhalter `%s` statt der Uhrzeit - jetzt 23:52.

**Naechster Schritt unveraendert:** **Spieltest 4 (Daniel)** auf `Nebelseetal_Pre_Release_V_0.0.3.exe`
(83.341.753 Byte, SHA256 `a7035101...`). Befunde zeilenweise ins Register, je Befund eine Zeile mit Fundstelle.
**Termin (Daniel, 10.11.2026):** er macht Spieltest 4 **heute Abend persoenlich** - bis dahin bleibt
`src/` und `data/` unangetastet, damit die Befunde zu genau dieser EXE gehoeren.

# STAND 10.11.2026, 00:28 - neue EXE mit D-5b: bereit fuer Spieltest 4 (Register 364)

> Block vom 10.11.2026, 00:28. Darunter 23:52 (D-5b gebaut; 361), 20:24 (D-5a; 356), 19:40 (neue EXE;
> 353), 19:08 (Layout-Schnitt; 351/352) und 18:15 (D-5 nachgebessert; 348).

**EXE:** `Nebelseetal_Pre_Release_V_0.0.3.exe`, **83.341.753 Byte**, SHA256
`a70351017ddc839925df95dd00ae3861dfcde519a4949f71d08be4428d8c0c5c` - am Dateisystem gemessen
und 00:31 von der Bauausgabe mit **denselben** Werten bestaetigt (kein abgeschriebener Wert).
Drin: D-5, Layout-Schnitt, D-5a und D-5b. Altbau in `archiv/builds/20261110_vor_d5b/`
(82.986.594 Byte, 4808fc7e...).

**Start geprueft:** Passworttor erscheint (PID 16320, `MainWindowHandle` 204801842, Responding
True), Screenshot `docs/audits/bilder/exe_d5b_start_20261110.png`; danach beide Prozesse
beendet, `game.lock` nach Sicherung entfernt.

**Sammellauf vor dem Bau:** **217 von 217 gruen**, 0 rot, 2 ausgesetzt, 1200 s, 9409 Pruefungen,
81 Befunde (`docs/audits/sammellauf_20261109_2356.log`, Register 362).

**Naechster Schritt:** **Spieltest 4 (Daniel)** auf dieser EXE - Befunde zeilenweise ins
Register, je Befund eine Zeile mit Fundstelle.
# STAND 09.11.2026, 23:52 - D-5b gebaut: Chris' Menue-Icons, Goldrahmen, Marktplatz-Kennzeichen (Register 361)

> Neuester Block. Darunter 20:24 (D-5a; 356), 19:40 (neue EXE; 353), 19:08 (Layout-Schnitt;
> 351/352), 18:15 (D-5 nachgebessert; 348) und 17:44 (D-5 gebaut; 347).

**Daniels Wort (eine Runde, 23:1x):** die neun Menue-Icons ersetzen - „Gebaeude auf der Karte
bleiben, wie sie sind“; Chris' Goldrahmen einbauen; `markt_handel` wird das Kennzeichen der
Marktplatz-Ansicht. farm_bauernhof wird die Farm, farm_windmuehle bleibt ungenutzt.

**Gebaut:** neun Menue-Icons 256 x 256 RGBA aus den gelieferten Kacheln (Altbestand hashgleich in
`archiv/design/20261109_c2_menue_icons_alt/`); `kachelrahmen_chris.png` 400 x 400 RGBA aus der
Schmiede-Kachel, Band **14 px** (am Original gemessen 3,35 Prozent), Mitte und Eck durchsichtig;
Eintrag `kachelrahmen.weltkarte` in `data/gebaeude_motive.json`, gelesen von
`main._lade_weltkarte_rahmen`, verbraucht in `_kartenrahmen_bauen` (C2-Rahmen = Rueckfall,
`ruhe` bleibt fuer den Rasterweg); `assets/bilder/marktplatz_kennzeichen_96.png` neben dem Titel.

**Ehrliche Grenze:** Eckenradius **14 px statt Chris' 30 px** - der bewaehrte 4-Leisten-Rahmen
braucht Eckblock = Bandbreite. 30 px braeuchten einen eigenen Schnitt (3x3-Leisten) und wuerden
`test_weltkarte_rahmen` brechen; das ist eine offene Entscheidung, keine Nachlaessigkeit.

**Wachen:** neu `tests/test_d5b_icons_und_rahmen.py` **33/0/1**. Gruen geblieben:
`test_weltkarte_rahmen` 34/0/1, `test_gebaeude_optik` 179/0/0, `test_gebaeude_icons` 56/0/0,
`test_gebaeude_motive` 104/0/1, `test_marktplatz_ansicht` 19/0/0, `test_portal_kopfleiste`
72/0/1, `test_portal_fremdblick` 18/0/1, `test_startspiel` 62/0/1, `test_auswahlrahmen_c2` 17/0/0.

**Belege:** `docs/audits/bilder/d5b_goldrahmen_karte_20261109.png` (Bildschirmfoto der
Portalansicht, DPI-korrekt abgenommen), `d5b_marktplatz_kennzeichen_20261109.png`,
`d5b_icons_alt_neu_20261109.png`.

**Offen:** Sammellauf nach diesem Eingriff, neue EXE (Daniel spielt ab der naechsten EXE -
Spieltest 4 wurde von 22:59 auf diese Fassung verschoben).

# STAND 09.11.2026, 20:24 - D-5a gebaut: die Weltkarte steht auf Chris' Farben (Register 356)

> Neuester Block. Darunter 19:40 (neue EXE; 353), 19:08 (Layout-Schnitt; 351/352), 18:15 (D-5
> nachgebessert; 348) und 17:44 (D-5 gebaut; 347).

**Daniel 20:0x (eine Runde mit Bildvergleich, beide wie empfohlen):** Farbwelt **B - Chris' Farbton,
Helligkeit fuer 20-px-Felder angehoben**; **Tannen bleiben** („nur die Farben in
data/gelaende.json, Zeichner unangetastet“).

**Messlage (aus den gelieferten Bildern, nicht abgeschrieben):** Median je Gelaendeart nach
Farbton-Regel. Woertlich (A) waere die Karte auf 20 px unlesbar - Wald Helligkeit 30, Berg 182.
Fassung B hebt die Helligkeit an und haelt den Ton: Grasland #64794A, Steppe #A98A5C, Wald #2E4527,
Huegel #6B563E, Berg #8E93A6, Nebelsee #41597A, Sumpf #474A34.

**Gebaut:** NUR `data/gelaende.json` (je Art `farbe` und `farbe_rand`, Herkunft im `_belegt`).
`weltkarte_malerei.py`, `portalraum.py` und die Legende sind unangetastet - sie lesen dieselbe
Quelle, darum faerbt sich die Legende mit.

**Nachgemessen:** Helligkeit 110,1 -> **118,9**, Streuung 28,6 -> **40,7** (genau das „lesbar“),
ausgefressene Lichter 0,00 -> **0,02 %**, fast schwarze Felder 0,00 %. **Lesbarkeit:** 64 % (heute),
63 % (A), **64 %** (B) der Feldmitten liegen naeher an ihrer eigenen Gelaendefarbe als an jeder
anderen - die Palette nimmt der Karte nichts.

**Wachen:** neu `tests/test_d5a_chris_farben.py` **17/0/1** (Helligkeitsband 50-185, Ordnung Wald
dunkelster / Berg hellster / Nebelsee blau, Paarabstand >= 20, Rand dunkler als die Flaeche, eine
Quelle). `test_weltkarte_malerei` **67/0/1** (vorher 63/4/1): zwei Pruefungen standen auf der alten
Palette und wurden auf die neue Wahrheit gestellt, mit Begruendung im Docstring - nicht der Code
zurueckgebogen.

**Sammellauf nach diesem Schritt** (`docs/audits/sammellauf_20261109_2025.log`): **216 von 216 gruen,
0 rot, 2 ausgesetzt, 1093 s**, 9376 Pruefungen (+17), 0 Fehler, 80 Befunde. **Offen: D-5b**
(Icons und Goldrahmen, F-39).

# STAND 09.11.2026, 19:40 - neue EXE gebaut: D-5 und der Layout-Schnitt sind drin (Register 353)

> Neuester Block. Darunter 19:08 (Layout-Schnitt; 351/352), 18:15 (D-5 nachgebessert; 348), 17:44
> (D-5 gebaut; 347) und 16:38 (Bildplan; 346).

**Kette nach Daniels Plan (18:4x):** Layout-Schnitt klein -> **neue EXE** -> Spieltest 4 (Daniel) ->
D-5a und D-5b.

**Altbau vorher archiviert:** `archiv/builds/20261109_vor_layoutschnitt/` mit `SHA256.txt`
(82.727.384 Byte, SHA256 `486ce93e...`; enthielt D-4, NICHT D-5).

**Bau (`tools/build_exe.py`, PyInstaller 6.22.3, Python 3.11.16):** Groesse **82.987.046 Byte (79,1
MB)**, SHA256 `b90ae5e6eb88a94bb060b5b007a786392c12d53e0305dc570a6dcd2533705333` - Masse und Hash NUR
aus der Bauausgabe. Genau eine EXE im Projektordner, `build/`, `dist/`, `.spec` und `__pycache__`
sind weg.

**Start geprueft (nicht nur Prozess):** die EXE zeigt das **Passworttor**, Fenstertitel „Nebelseetal
Remake“, PID 7812, `MainWindowHandle` 608371726, `Responding` True; Screenshot als Beleg.
Danach beide Prozesse beendet und die aus 15:19 liegen gebliebene `game.lock` (vorher gesichert)
entfernt - sonst blockiert sie einen spaeteren Start still.

**Jetzt ist Daniel dran:** Spieltest 4 mit dieser EXE. Danach D-5a (Weltkarte auf Chris' Farben und
Tannen, F-36) und D-5b (Icons und Goldrahmen, F-39).

# STAND 09.11.2026, 19:08 - Layout-Schnitt klein: die Portaltexte folgen der Spalte (Register 351)

> Neuester Block. Darunter 18:15 (D-5 nachgebessert; 348), 17:44 (D-5 gebaut; 347), 16:38 (Bildplan; 346)
> und 14:58 (Bildwelt Chris; 341-344).

**Daniel 18:4x:** „Layout schnitt ist ein eigenes thema aber kleiner halten und gut anpassen“
- **klein heisst: nur das Portal, nur der Text.** Kein Umbau der anderen Ansichten, keine waagerechte
Bildlaufleiste.

**Messlage (Probe im gemappten Fenster, nicht geschaetzt):** Standardfenster 1024 x 720, die
Inhaltsspalte ist **630 px** breit. Der Inhalt forderte **783 px** - die acht Textzeilen des Portals
liefen mit `wraplength=760` bis 763 px, dazu sass die Legendenzeile mit 637 px um 7 px zu breit. Rechts
wurde abgeschnitten.

**Gebaut (nur `src/main.py`):** EINE Quelle fuer die Textbreite. `PORTAL_TEXT_BREITE` (780, die
Entwurfsbreite), `PORTAL_TEXT_MINIMUM` (320) und `PORTAL_SPALTEN_RAND` (20) stehen als Konstanten;
`_textbreite(spalte)` rechnet ohne Fenster (testbar), `_spaltenbreite()` misst
`content_canvas.winfo_width()` und ist die EINZIGE Messstelle. Die acht `wraplength=760` der
Portal-Ansicht und das Kopfband lesen dieselbe Zahl. Der Farbkasten der Gelaende-Legende traegt 4
statt 6 px Abstand (7 x 2 px = 14 px Reserve).

**Nachgemessen:** 1024er Fenster -> Textbreite **610 px**, Band **610 x 117**, Inhalt fordert **630 von
630** (vorher 783). 900er Fenster -> Inhalt **623** statt 783. **Ehrliche Grenze:** unter 1024 px
Fensterbreite bleibt die Legendenzeile (603 px) und die Knopfzeile (493 px) breiter als die Spalte -
das ist ein eigener Schnitt (Legende umbrechen), nicht dieser.

**Belegt:** Wache `tests/test_portal_kopfleiste.py` **72 bestanden / 0 Fehler / 1 Befund** (neuer
Abschnitt 7: 630 -> 610, Deckel 780, Untergrenze 320, im gemappten Fenster kein Inhalt breiter als die
Spalte). Screenshots im Standardfenster: das Band ist vollstaendig, die sieben Legenden-Eintraege
stehen bis „Sumpf 10“ da. Sammellauf nach dem Commit (`docs/audits/sammellauf_20261109_1910.log`): **215 von 215 gruen,
0 rot, 2 ausgesetzt, 1124 s**, 9359 bestandene Pruefungen (+15 gegen 18:18), 0 Fehler, 79 Befunde.

**Nicht angefasst:** alle anderen Ansichten behalten `wraplength=760`; kein neues Modul, die
MODULKARTE bleibt gueltig.

# STAND 09.11.2026, 18:15 - D-5 nachgebessert: das Band wird verkleinert statt beschnitten (Register 348)

> Neuester Block. Darunter 17:44 (D-5 gebaut; 347), 16:38 (Bildplan; 346), 14:58 (Bildwelt Chris; 341-344)
> und 11:25 (D-4; 340).

**Befund beim Hinsehen (gemessen):** das Standardfenster ist 1024 x 720, die INHALTSSPALTE darin nur **630 px**
breit, die Inhalte wollen **800 px** (vor D-5 schon 783 - der Text war dort ebenfalls beschnitten); eine
waagerechte Bildlaufleiste gibt es nicht. Das 780 px breite Band wurde deshalb auf 610 px abgeschnitten.
Ab etwa 1280 px Fensterbreite war alles vollstaendig.

**Daniel 18:05:** "Band bei schmalem Fenster auf die Spaltenbreite VERKLEINERN, Original 780 x 150 bleibt die
Quelle, kein Beschnitt". Gebaut: `_kopfband_masse` + gemessene Spaltenbreite (`content_canvas.winfo_width()`) +
Pillow/`LANCZOS`; ohne Pillow bleibt das Original. **Nachgemessen:** 1024er Fenster -> Band **610 x 117**,
1500er Fenster -> **780 x 150**; die rechte Randspalte des verkleinerten Bildes ist pixelgleich mit der des
Originals - **nichts abgeschnitten**.

**Belegt:** Wache `tests/test_portal_kopfleiste.py` **57/0/1** (neuer Abschnitt 2b fuer die Verkleinerung).
Sammellauf nach dem Fix (`sammellauf_20261109_1818.log`): **215 von 215 gruen, 0 rot, 2 ausgesetzt,
1085 s**, 9344 Pruefungen, 0 Fehler, 79 Befunde. Last beim Start: ein fremder `shred`-Prozess haelt
~38-42 % einer CPU (dieselbe Last lag schon beim Lauf 17:12 an).

**Offen (eigener Schnitt, NICHT D-5):** die Inhaltsspalte selbst beschneidet im Standardfenster auch den Text -
das Layout (Spalte folgt dem Fenster oder waagerechte Bildlaufleiste) braucht Daniels Wort.

**Kostenablesung 18:15:** 13,21 USD Guthaben / 66,78 USD Gesamtverbrauch - **+0,20 USD** seit der Ablesung
zwischen 15:21 und 16:38 (Register 349, Buchhaltung).

# STAND 09.11.2026, 17:44 - D-5 steht: das Kopfband von Chris im Portal, farbige Form in der Weltliste (Register 347)

> Neuester Block. Darunter 16:38 (D-5 Detail: Bildplan; 346), 14:58 (Bildwelt Chris, 341-344, EXE-Bau) und
> 11:25 (D-4: gemalte Karte; 340).

**Daniels drei Woerter (16:58, eine Runde, Empfehlung zuerst - alle drei angenommen):** Kopfleiste = **Band**
`band_schmiede_dorf_ghule` **780 x 150 px, 0 % Beschnitt**; Banner der Weltliste = **farbige Form wie heute**,
kein Kachelausschnitt; Goldrahmen = **erst D-5b** mit den Icons (F-39), der C2-Rahmen bleibt in D-5.

**Gebaut (nur `src/main.py`, S3 bis S6 unveraendert):** Band ueber dem Titel, darunter EINE Trennlinie 2 px in
`#C68B42` (gemessener Median; die Farbe steht als Zeichenkette genau einmal im Code), je Weltzeile ein 6 x 18 px
Farbstreifen in der Bannerfarbe. Ohne Bilddatei bleibt ein **leerer Platz 780 x 150** stehen - kein Absturz, kein
erfundenes Bild. Karte, Portalraum und Spielregeln sind nicht angefasst.

**Belegt:** neue Wache `tests/test_portal_kopfleiste.py` **45/0/1**; Sammellauf `sammellauf_20261109_1712.log`
**215 von 215 gruen, 0 rot, 2 ausgesetzt, 1280 s** (9332 Pruefungen, 0 Fehler, 79 Befunde); Dokumentpruefungen
447/0 (135) - 28/0 (1 alter Befund) - 131/0 (64) - 26/0 - 49/0; `docs/MODULKARTE.md` neu erzeugt.

**Assets:** `assets/bilder/portal_kopfband_schmiede_dorf_ghule_780x150.png`, 254.385 Byte, SHA256 `3f5a0c69...`,
byte-gleich mit dem Schnitt im Archiv; Eintrag in `assets/bilder/README.md`.

**Offen bei Daniel:** Spieltest 4 mit `Nebelseetal_Pre_Release_V_0.0.3.exe` (D-4 enthalten; D-5 ist NICHT in dieser
EXE). Danach die Kette aus F-36/F-39: **D-5a** (Weltkarte auf Chris' Farben und Tannen), **D-5b** (Icons und
Goldrahmen).


> Neuester Block. Darunter 14:58 (Bildwelt Chris, Register 341-344, EXE-Bau) und 11:25 (D-4; 340).

**Was „Detail“ heisst (Daniel, zwischen 15:21 und 16:38):** nicht eine Detailansicht im Fenster, sondern **alle Angaben beisammen** -
welches Bild, wohin, wie gross, mit welchem Zuschnitt.

**Am Code gemessen** (nicht geschaetzt): Fenster 1024 x 720, Inhaltsbreite **780 px**, Karte 400 x 400 (20 px je
Feld), Burg auf dem Feld **18 px**, Wappen **8 px**, Weltkartenliste 6 Zeilen, Bannerfarben `#2ecc40` / `#e53935`.

**Geschnitten und belegt:** Kopfband `band_schmiede_dorf_ghule` **780 x 150 mit 0 % Beschnitt** (Empfehlung),
Alternative `band_ghule_lager` 780 x 152; Panoramen auf 780 x 200 kosten **33-45 % Hoehe**; Ladeseite
`ladeseite_haemmer` **780 x 287 mit 0 % Beschnitt**. Jedes Bild 230-390 KB. Massblatt
`archiv/design/20261109_chris_bildpaket/geschnitten/d5_massblatt_20261109.png` (840 x 2047) zeigt jedes Bild in
seiner Zielgroesse; die acht Schnitte liegen im selben Ordner (gitignoriert).

**Fehlendes, offen:** kein freistehendes Bannerbild (die Banner stecken IN den Kacheln), keine Bilder fuer zehn
Gebaeude, keine Fraktionsvarianten ausser Ghulen, kein Kartenbild - das ist **D-5a** (F-36).

**Drei Punkte warten auf Daniels Wort** (Empfehlung zuerst): Band oder Panorama als Kopfleiste; Banner in der
Weltliste als farbige Form oder als Kachelausschnitt; Goldrahmen jetzt in D-5 oder erst in D-5b. Danach: Bau,
Wache, Sammellauf.

**Kostenablesung dazwischen:** 13,41 USD Guthaben / 66,58 USD Gesamtverbrauch - **+0,05 USD** seit 15:06 (Register 345).

# STAND 09.11.2026, 14:58 - Die Bildwelt von Chris Fred Däubner ist protokolliert, abgelegt und zugeordnet (Register 341)

> Neuester Block. Darunter 11:25 (D-4: gemalte Karte; Register 340), 10:33 (F-35; 338), 10:04 (F-34; 337),
> 09:36 (fuenf Antworten; 335), 09:03 (EINE EXE; 334).

**Eingang:** die Lieferung „NEBELSEETAL png's“ (25 PNG, je 3500 x 3500, **420.166.487 Byte** = 420,2 MB) kam am
06.11.2026, 14:21 per TransferNow; am 09.11.2026 kam der Nachtrag 1 dazu (ZIP 69.147.227 Byte, SHA256
`34c6d68e…`, 31 Eintraege: 25 zugeordnete WebP, vier Uebersichten, `zuordnung.json`, das Dokument).

**Urheber, im Projekt benannt:** **Chris Fred Däubner** hat die Bilder mit KI fuer das Nebelseetal erzeugt,
danach selbst bearbeitet und aufgewertet und an Daniel geliefert (10 EUR fuer alle Bilder und das Logo).
Stilbestimmend fuer Malstil, Farbgebung, Seiten und Menues. Der Text des Nachtrags ist eine Auswertung von
Claude Opus 5.5 - die BILDER sind Chris' Arbeit.

**Ablage:** `archiv/design/20261109_chris_bildpaket/` (gitignoriert, nicht in der EXE) - `originale_transfernow/`
(25 PNG, Originalnamen), `Nachtrag_1_Design_Chris.zip`, `nachtrag1_entpackt/`, `SHA256SUMS.txt` (26 Zeilen)
und `SHA256SUMS_nachtrag1_entpackt.txt` (31 Zeilen). **25 von 25 Hashes Quelle gegen Kopie gleich**, erst
danach wurde der Desktop-Ordner geraeumt (verschoben, nicht vernichtet).

**Neu gemessen - und besser als im Nachtrag:** die Originalnummern lassen sich doch zuordnen. Ein
Graustufenvergleich nach Randabschnitt findet fuer jedes der 25 Bilder den Zwilling (**jeder Treffer
r >= 0,946**, zweitbester hoechstens 0,589); die Nummern 9 bis 33 sind ohne Luecke und ohne Doppelbelegung
verteilt, die drei Lieferteile sind die Bloecke 9-16, 17-24 und 25-33. Die Tabelle steht in
`docs/design/DESIGN_LIEFERUNG_CHRIS_20261109.md`, Abschnitt 4.

**Die offene Frage des Nachtrags ist beantwortet:** die Kacheln von Chris sind NICHT die verkleinerten
Projektbilder in `assets/icons/gebaeude/c2/` - bester Treffer ueber alle 11 Kacheln und 20 Projektbilder
**r = 0,318**, waeren es dieselben Bilder, laege der Wert bei 0,9. **Es wird nichts ersetzt.**
Farben nachgemessen (Median): Rahmengold #C68B42 (Richtwert #C9993F), Banner-Rot #7E301E (#8B2A22),
Ghule-Leuchten #7AAC4D (#7CFF4A) - die Richtwerte taugen als Naeherung, nicht als Pixelwert.

**Offen und bei Daniel (eine Runde):** (1) Karte nach Chris (satte Gruent oene, kein Kontur) gegen F-35
„Stil wie Stilprobe A“, das D-4 gebaut hat; (2) Bannerfarben rot/hell statt Fraktionsfarben in
`PORTAL_BANNER_FARBEN`; (3) zwei Rahmenstile (Projektbild 256 px gegen Goldrahmen im Bild); (4) ob der
Satz des Pakets „wo fruehere Vorschlaege abweichen, gelten die Bilder von Chris“ bindend sein soll.
Ausserdem: kurze schriftliche Nutzungsbestaetigung von Chris einholen.

**Nachtrag 15:06:** Chris ist **im Repo verlinkt** - Instagram `three_ghosts.mp4` auf seinen Wunsch, im
Abschnitt Rechte der `README.md` und in der Urhebertabelle des Belegdokuments; die Anhaengsel der Chat-Adresse
(`psln`, `utm_source=qr`) wurden nicht uebernommen. **Kostenablesung Daniels 15:06: 13,46 USD Guthaben /
66,53 USD Gesamtverbrauch** - gegen 13,80 / 66,19 um 10:41 also **+0,34 USD** fuer Sitzung 27 (D-4) und diese
Sitzung bis 15:06 (gemessen, Abrechnung bis 5 Minuten verzoegert).

**Daniels fuenf Antworten (15:13, Register 344, F-36 bis F-40):**

- **F-36 Karte:** Umbau auf Chris' Farben und Tannen als **eigener Schnitt NACH D-5**; die Karte bleibt
  vorerst so, wie D-4 sie gebaut hat.
- **F-37 Banner:** **rot mit hellem Symbol wird die neue Quelle** in `PORTAL_BANNER_FARBEN`; die
  Fraktionsfarben bleiben nur, wo eine Fraktion sie wirklich braucht.
- **F-38 Besucherseite:** `index.html` bekommt **keinen** Instagram-Link - der Link steht in `README.md`
  und im Designdokument.
- **F-39 Massstab:** der Satz des Pakets gilt **vollstaendig** - auch Bestehendes (Icons, Rahmen) wird auf
  Chris umgestellt, in der Reihenfolge nach D-5. Das sind eigene Schnitte mit Wachen, kein Nebenaustausch.
- **F-40 EXE:** Bau erst **nach Daniels Formatierung**, dann Spieltest 4.

**EXE gebaut (15:19, aus `39a3f32`):** `Nebelseetal_Pre_Release_V_0.0.3.exe`, **82.727.384 Byte (78,9 MB)**, SHA256
`486ce93eb769ae115f43c594e6ff628e514dcb259eb4589503b291f41614a4c5`, Bau 1 min 23 s. Der Altbau (82.706.188 Byte,
`cae20ebd…`) liegt in `archiv/builds/20261109_vor_d4/` mit `SHA256.txt` - archiviert, nicht ersetzt. **Nur
Prozessprobe:** zwei Prozesse (Bootloader und Kind), nach 12 s beendet, kein `game.lock`, kein Spielstand, in AppData
kein frischer Schreibvorgang. **Die EXE enthaelt D-4** - Spieltest 4 kann kommen.

**Reihenfolge ab jetzt:** Formatierung erledigt -> EXE-Bau erledigt -> **Spieltest 4 (Daniel)** -> **D-5** (Portal mit
den Panoramen und Bannern aus dieser Lieferung) -> **D-5a** Weltkarte (F-36) -> **D-5b** Icons und Rahmen (F-39).

# STAND 09.11.2026, 11:25 - D-4 gebaut: die gemalte Karte steht im Portal, 20 px je Feld, gerade (Register 340)

> Darunter 10:33 (F-35: +28 % hell, 20 px; Register 338), 10:04 (F-34; 337),
> 09:36 (fuenf Antworten; 335), 09:03 (EINE EXE; 334).

**Gebaut:** `_render_portal` zeichnet die Weltkarte nicht mehr Feld fuer Feld. **Die 400
Gelaenderechtecke und die 42 Gitterlinien sind weg** - die Karte kommt als EIN gemaltes Bild aus
`weltkarte_malerei.karte_malen(raster, 20)`: **400 x 400 px, 20 px je Feld, GERADE Draufsicht,
kein Rollbalken**. Das Bild liegt bei (0, 0) mit Anker NW und traegt den eigenen Tag `kartenbild`.

**Klick und Bild stimmen ueberein:** die Feldmitte liegt weiter bei `(x + 0,5) * 20`, damit Klick,
Marschlinien, Anker und Statuszeile dasselbe Feld treffen. Die Wache prueft beides: die Feldmitte
in px, den Klickweg (`_portal_klick`) und dass eine abweichende Gelaendeart im Bild an der Stelle
IHRES Feldes sitzt - in der Zeile UND in der Spalte.

**Rueckfall bleibt:** ohne Pillow (oder ohne belegtes Gelaende) zeichnet `_portal_karte_flach` die
flachen Felder samt Trennlinien wie vor D-4; es wird kein Gelaende erfunden. F-32 ist im selben
Commit dokumentiert (Satz im Docstring von `spielschicht.portalwechsel`).

**Wachen:** neu `tests/test_portal_gemalte_karte.py` **38/0/1**; `test_weltkarte_rahmen` **34/0/1**
(Abschnitt 3 auf die neue Wahrheit gestellt, Rueckfall-Zusage umgezogen); `test_weltbild_gelaende`
**95/0/0** (Quellwache: die Ansicht MALt, der Rueckfall faerbt). `docs/MODULKARTE.md` neu erzeugt
(war auf 63 Dateien/35369 Zeilen veraltet).

**Sammellauf 11:03 bis 11:25: 214 von 214 gruen, 0 rot, 2 ausgesetzt, 9.287 Pruefungen, 0 Fehler,
78 Befunde, 1.232 s** (`docs/audits/sammellauf_20261109_1103.log`), Summe der Einzeldauern 2.440 s,
x1,98.

**Offen:** Spieltest 4 (Daniel), neuer EXE-Bau (die EXE von 09:03 enthaelt D-4 nicht), D-5 bis D-8,
Register 272/273 (alte Luecke), zwei alte und eine neue Skill-Ergaenzung (`/skills pending`).

# STAND 09.11.2026, 10:33 - F-35 gebaut: +28 % hell, warmer Grund wie Stilprobe A, Karte gerade, 20 px (Register 338)

> Neuester Block. Darunter 10:04 (F-34: 48 px und heller; Register 337), 09:36 (fuenf Antworten; 335),
> 09:03 (EINE EXE; 334), 08:55 (S-6; 333).

**Daniel hat F-34 nachgeschaerft** (10:07): „Die Vorschau + 28 % ist ok aber halte fest das ich es vom
stil wie bei der Stilprobe A will aber das die karte gerade angezeigt wird wie bei vorschau + 28%“.

**Gebaut:** `HELLIGKEIT = 1.28` (die Vorschau-Stufe), neu `LICHT_ALPHA = 58` statt 46 fuer den warmen
Grund der Stilprobe A, `SCHATTEN_ALPHA` bleibt 20 - alle drei in `_einheitslicht`, also fuer Kacheln und
ganze Karten gleich. **Die Karte bleibt gerade (flache Draufsicht) und 20 px je Feld**; F-34s 48 px sind
damit ueberholt.

**Gemessen:** mittlere Helligkeit der Karte d01 **85 -> 110 von 255**; Malzeit 48 px kalt 1,023 s, 20 px
kalt 0,556 s. Wache **67/0/1** (Sollwert wird mit dem Faktor gerechnet, Schwellen unveraendert).

**Widerspruch, offen notiert:** Daniel sagte „eine weltkarte bleibt 10 x 10 groß bitte also 20 px“ - eine
Weltkarte ist aber **20 x 20 = 400 Felder** (`data/welten.json`, `portalraum.py:53`, Wache „400 Felder“).
Das Raster wurde NICHT geaendert; umgesetzt ist die Anzeige-Absicht (klein, 20 px, gerade).

**Sammellauf 10:10 bis 10:33: 213 von 213 gruen, 0 rot, 2 ausgesetzt, 9.246 Pruefungen, 0 Fehler,
76 Befunde, 1.355 s** (`docs/audits/sammellauf_20261109_1010.log`).

**Naechster Schritt: D-4** - `_render_portal` malt die Karte als EIN Bild mit **20 px je Feld**
(400 x 400 px, kein Rollbalken); Klick muss dasselbe Feld treffen. Dazu die F-32-Dokuzeile im selben Commit.

# STAND 09.11.2026, 10:04 - F-34 gebaut: flach, 48 px je Feld, heller wie die Stilprobe A (Register 337)

> Neuester Block. Darunter 09:36 (fuenf Antworten; Register 335), 09:03 (EINE EXE; Register 334),
> 08:55 (Portal S-6; Register 333).

**Daniel hat das Vergleichsblatt gesehen und entschieden** (09:44): „Nummer 2 Flach und 48 px je Feld
gefällt mir am besten nur etwas heller bitte wie bei Nummer 3“.

**Gebaut:** die Kante ist **48 px je Feld** (960 x 960 px) - die fruehere Antwort F-30 (20 px) ist damit
ueberholt, und die Ansicht braucht dafuer einen **Rollbalken** (offen, D-4). Der Ton ist heller: in
`src/weltkarte_malerei.py` steht jetzt `HELLIGKEIT = 1.20` und `SCHATTEN_ALPHA = 20` statt 42, beides in
`_einheitslicht` - EINE Stelle fuer Kacheln und ganze Karten.

**Gemessen:** mittlere Helligkeit der Karte d01 **85 -> 102 von 255** (Stufe „+20 %“ des Stufenblatts),
Malzeit 48 px kalt 0,865 s, warm 0,00000 s. **Die Wache ist nicht gelockert**: die zwei
Farbtreue-Pruefungen rechnen den Sollwert mit dem Faktor, Schwellen bleiben 26 und 60 - **67/0/1**.

**Sammellauf 09:49 bis 10:04: 213 von 213 gruen, 0 rot, 2 ausgesetzt, 9.246 Pruefungen, 0 Fehler,
76 Befunde, 879 s** (`docs/audits/sammellauf_20261109_0949.log`).

**Naechster Schritt: D-4** - `_render_portal` (`src/main.py:12353`) malt die Karte als EIN Bild mit 48 px
je Feld in einem Rollbalken; Klick, Marschlinien und Statuszeile muessen auf dasselbe Feld zeigen.
Dazu die offene F-32-Dokuzeile im selben Commit.

# STAND 09.11.2026, 09:36 - Fuenf Gestaltungs-Antworten: nur der Stil-Entscheid ist noch offen (Register 335)

> Neuester Block. Darunter 09:00 (EINE EXE gebaut; Register 334), 08:55 (Portal S-6; Register 333),
> 08:25 (Portal S-5; Register 332).

**Daniel hat alle fuenf Fragen beantwortet** (09.11.2026, 09:33, eine Runde): Kante bleibt **20 px je
Feld**, der Wald traegt **Tannen**, `spielschicht.portalwechsel` **bleibt** (und wird ausdruecklich als
Spielschicht-Funktion dokumentiert - offen, geht mit der naechsten `src/`-Aenderung), `letzter_wechsel`
**bleibt** als reine Aufzeichnung.

**Offen ist nur der Stil (F-29): „Beide Fassungen als Bild sehen, dann entscheiden.“** Dafuer liegt ein
Vergleichsblatt vor:
`archiv/design/20261109_vergleich_stil/vergleich_flach_vs_isometrisch_20261109.png` (2000 x 1160, drei
Felder: flach 20 px, flach 48 px, isometrische Stilprobe A, dazu Messwerte). **D-4 (Einbau der gemalten
Karte in `_render_portal`) wartet auf seine Wahl.**

Antworten wortgleich mit Folge-Spalte in `docs/design/PORTAL_MODELL_20261108.md` Abschnitt 10.
Kein Code geaendert, kein Sammellauf noetig.

# STAND 09.11.2026, 09:00 - EINE EXE gebaut (Stand a1ea781, S-5 und S-6 enthalten; Register 334)

> Neuester Block. Darunter 08:55 (Portal S-6, Wache am Fenster; Register 333), 08:25 (Portal S-5,
> keine Wartezeit; Register 332), 03:35 (S-4b; Register 331).

**`Nebelseetal_Pre_Release_V_0.0.3.exe` ist neu gebaut** (82.706.188 Byte, SHA256 `cae20ebd34fb…`),
aus dem Arbeitsbaum `a1ea781`, den der Sammellauf 08:36 bis 08:55 mit 213 von 213 gruen belegt hat.
PyInstaller 6.22.3 aus dem Projekt-venv, `--onefile --noconsole`, Symbol mit sechs Groessen.

**Der Vorgaengerbau ist ARCHIVIERT, nicht geloescht:** `archiv/builds/20261109_vor_s6/` (08.11.2026,
15:58, 82.693.324 Byte, SHA256 `4df7cc03…`, mit `SHA256.txt`). Damit haelt die Regel „genau eine EXE
im Projektordner“ und der alte Stand bleibt nachpruefbar.

**Nicht gestartet:** kein Spielprozess, kein `game.lock`, kein Schreiben in einen Spielstand - ein
Start haette Daniels Spieltest-Stand anfassen koennen. Eine Textprobe im Binaerstand beweist nichts
(das PYZ ist zlib-gepackt: 0 Treffer fuer alte UND neue Zeichenketten).

**Offen: Spieltest 4** (Daniel) sowie D-4 bis D-8 und die fuenf Fragen aus der Uebergabe 07:35.

# STAND 09.11.2026, 08:55 - Portal S-6: die Wache haengt am Fenster, zwei Umzuege hintereinander belegt (Register 333)

> Neuester Block. Darunter 08:25 (Portal S-5: keine Wartezeit; Register 332), 03:35 (S-4b; Register
> 331), 02:58 (D-3, die gemalte Testkarte; Register 330).

**Was an S-5 noch fehlte, war die Wache an der ANZEIGE.** Die alten Wachen pruefen den Kern; neu ist
`tests/test_portal_s5_keine_wartezeit.py` (**27/0/0**) mit drei Abschnitten: Quelle (kein
`_sperre_text`, `_render_portal` nennt `_letzter_wechsel_text` und „zuletzt gewechselt“, die
Buchstelle ruft `wechsel_erlaubt` per AST mit genau drei Werten), Kern (Signatur, kein
`_STUNDEN_SPERRE`, Wechsel von gerade eben erlaubt, Altaufruf `TypeError`) und echtes Tk-Fenster.

**Der eigentliche Punkt steht im Fenster:** ZWEI Umzuege hintereinander gelingen, jeder mit GENAU
einem Festpreis (25.000 -> 20.000 Mana, Dorf von 7/12 auf 9/12). Die Zeile sagt „zuletzt gewechselt:“
statt „Sperre:“, ohne Wechsel „noch nie gewechselt“, danach „vor wenigen Minuten“, ein Stempel von vor
drei Stunden „vor 3.0 h“, ein Zukunftsstempel wird benannt.

**Gegenprobe auf dem Altstand `649f080`: 7 bestanden, 18 FEHLER** - das alte Fenster zeigte
„Sperre: noch 24.00 h“, schrieb „Zurzeit nicht möglich: Erst nach 24 Stunden wieder möglich“ und liess
den zweiten Umzug nicht zu. Die drei alten src-Dateien wurden dafuer aus dem Commit geholt und danach
per `git checkout` zurueckgestellt.

**Sammellauf 08:36 bis 08:55: 213 von 213 gruen, 0 rot, 2 ausgesetzt, 9.246 Pruefungen, 0 Fehler,
76 Befunde, 1.023 s** (`docs/audits/sammellauf_20261109_0836.log`); 215 Dateien gefunden, die 27
neuen Pruefungen sind genau der Zuwachs gegen 9.219.

**Offen aus S-6: EINE EXE und Spieltest 4** - beides braucht Daniel (der Spieltest ist seine Hand).
Weiter offen: D-4 bis D-8 und die fuenf Fragen aus der Uebergabe 07:35.

# STAND 09.11.2026, 08:25 - Portal S-5: keine Wartezeit mehr, sechs Wachen umgedreht (Register 332)

> Neuester Block. Darunter 03:35 (S-4b: `_portal_wechsel` entfernt; Register 331), 02:58 (D-3, die
> gemalte Testkarte; Register 330), 01:50 (Portal S-1 bis S-4; Register 324 bis 326), 02:04 (D-1,
> D-2, W-D6; Register 327 bis 329).

**Der Weltensprung hat keine Wartezeit mehr - der Preis ist die einzige Bremse.** Daniels Entscheid
F-28 = C vom 08.11.2026 ist gebaut: `portalraum.wechsel_erlaubt(von_z, nach_z, mana)` prueft nur noch
bekannte Weltkarte und Mana. Die 24-Stunden-Pruefung samt Restzeit-Meldung ist entfernt, die
Konstante `_STUNDEN_SPERRE` ist GELOESCHT; der Wert `hoechstens_je_stunden` bleibt als Quelle und
Zeitzeugnis in `data/welten.json` stehen und wird nicht mehr gelesen. `beschreibung()` sagt jetzt
„und hat keine Wartezeit (Entscheidung F-28 = C)“.

**Der Zeitstempel bleibt, er sperrt nur nicht.** `state.letzter_wechsel` wird von `nach_wechsel`
weiter fortgeschrieben; die Portalzeile sagt statt „Sperre:“ jetzt „zuletzt gewechselt:“ und nennt
„noch nie gewechselt“ / „vor wenigen Minuten“ / „vor X h“ (auch ein Zeitstempel aus der Zukunft wird
benannt). Die Methode heisst dafuer `_letzter_wechsel_text` statt `_sperre_text`.

**Sechs Wachen sind UMGEDREHT, nicht geloescht** - jede prueft mit DEMSELBEN Aufruf das Gegenteil:
test_portalraum **72/0/0** (Signatur genau drei Werte, Altaufruf mit Zeitstempel MUSS `TypeError`
werfen, kein `_STUNDEN_SPERRE`, „keine Wartezeit“ in der Beschreibung), test_dorf_versetzen
**38/0/0** (zweiter Umzug gelingt sofort, wieder GENAU ein Festpreis, neue Position),
test_e2e_wege **132/0/1** (Kette 12: derselbe Wechsel von gerade eben ist mit genug Mana erlaubt,
der zweite Umzug im Spiel scheitert am Mana), test_spielschicht **145/0/1**, test_portal_uebersicht
**62/0/0**, test_weltkarten_anzeige **27/0/0**.

**Sammellauf 08:08 bis 08:25: 212 von 212 gruen, 0 rot, 2 ausgesetzt, 9.219 Pruefungen, 0 Fehler,
76 Befunde, 1.037 s** (`docs/audits/sammellauf_20261109_0808.log`) - der Zuwachs gegen 9.213 sind
genau die sechs neuen Pruefungen. Der Lauf war langsamer als der vorige (771 s), weil die Summe der
Einzeldauern von 1.524 auf 2.054 s stieg: die MASCHINE war langsamer, nicht die Parallelitaet
(x1,98 wie zuvor).

**Drei Funde beim Bau, offen benannt:** die Uebergabe 07:35 nannte drei rote Dateien - rot war auch
`tests/test_spielschicht.py` (eigener 24-h-Block); vier der fuenf Pruefdateien sind CRLF, das
vorbereitete LF-Hilfsskript haette lautlos nichts ersetzt (neu geschrieben, jeder Anker auf
Eindeutigkeit geprueft); `test_dorf_versetzen` prueft nach dem neuen zweiten Umzug auf `8/12`
zweimal die alte Position `7/12` und musste nachziehen.

**Naechster Schritt: S-6** - Wachen, voller Lauf, EINE EXE, Spieltest 4. Offen bleiben D-4 bis D-8
(Einbau der gemalten Karte, Burgen, Banner, Drachen, Fraktionsbilder, Logo) und die Fragen 1 bis 5
an Daniel (`docs/design/PORTAL_MODELL_20261108.md`, Uebergabe 07:35 Abschnitt 5).

# STAND 09.11.2026, 03:35 - Portal S-4b: die alte Buchstelle ist entfernt, ihre Wachen wachen an der neuen (Register 331)

> Neuester Block. Darunter 02:59 (D-3, die gemalte Testkarte; Register 330), 01:50 (Portal S-1 bis
> S-4; Register 324 bis 326), 02:04 (D-1, D-2, W-D6; Register 327 bis 329).

**`_portal_wechsel` ist weg - und mit ihr keine einzige Zusage.** Die Methode hatte seit S-4 keinen
Aufrufer mehr; sie ist samt Docstring aus `src/main.py` entfernt. Keine Funktion aus `portalraum`
faellt mit ihr weg: `wechsel_erlaubt` und `nach_wechsel` werden von `_dorf_versetzen` (S-3) und
`spielschicht.portalwechsel` weiter gebraucht.

**Die Wachen sind UMGESTELLT, nicht geloescht:** `test_durchspiel` Abschnitt 8 prueft jetzt, dass
die alte Buchstelle nicht zurueckkommt und der Weg ueber `_dorf_versetzen` laeuft; `test_e2e_wege`
Kette 12 spielt den ganzen Weg weiter (Mana aus eigenen Tempeln, GENAU ein Festpreis, Sperre) - nur
ueber die Buchstelle und auf ein FREIES Feld; `test_portal_uebersicht` misst die Sperre an
`_dorf_versetzen`; `test_weltkarten_anzeige`, `test_portal_ansicht_umzug` und
`test_portal_fremdblick` pruefen zusaetzlich, dass der Name in `main.py` nicht mehr vorkommt.

**Gegenprobe in der Kette:** der zweite Umzug scheitert erst am Mana (20 von 5.000), die Sperre
selbst wird an der Kernfunktion `wechsel_erlaubt` gemessen - nicht mit geschenktem Mana, weil die
Quellwache dieser Datei das Setzen von Spielzustand verbietet.

**Sammellauf 03:22 bis 03:35: 212 von 212 gruen, 0 rot, 2 ausgesetzt, 9.213 Pruefungen, 76 Befunde,
771 s** (`docs/audits/sammellauf_20261109_0322.log`) - die fuenf neuen Pruefungen sind der Zuwachs
gegen 9.208. Einzeln gruen: test_weltkarten_anzeige 27/0/0, test_portal_uebersicht 62/0/0,
test_portal_ansicht_umzug 27/0/0, test_portal_fremdblick 18/0/1, test_durchspiel 64/0/2,
test_e2e_wege 131/0/1, test_dorf_versetzen 38/0/0, test_portalraum 70/0/0,
test_portal_feld_belegung 40/0/0.

**Nebenbefund, nicht angefasst:** `spielschicht.portalwechsel` hat in `src/` keinen Aufrufer mehr,
nur die Pruefungen rufen sie - ein eigener Strang, der mit S-4b nichts zu tun hat.

# STAND 09.11.2026, 02:58 - D-3 gebaut: die Testkarte ist gemalt, der Stil-Entscheid liegt bei Daniel (Register 330)

> Neuester Block. Darunter 01:50 (Portal S-1 bis S-4; Register 324 bis 326), 02:04 (D-1 und die zwei
> Entscheidungen D-2/W-D6; Register 327 bis 329), 22:48 (Portal S-2/S-1), 23:20 (S-3).

**Eine gemalte Weltkarte liegt vor - im Spiel ist sie noch NICHT eingebaut.** Der malende Teil
steht in `src/weltkarte_malerei.py` (Pillow, kein tkinter): die 20 x 20-Gelaendematrix wird als
Farbfeld bikubisch hochgerechnet, darueber werden die Motive je Feld gemalt (zwei bis drei Tannen,
Gipfel, Duenen, Wellen, Schilf - je Feld mit eigener Saat aus seiner Lage), darueber EIN Licht und
ein leises Korn. Daniel hatte am 09.11.2026, 02:03 das flache Raster mit gemalten Kacheln
entschieden (Register 328).

**Gemessen (Belastungstest im echten Fenster, `tools/testkarte_fenster.py`, Weltkarte d01):**
48 px je Feld - kalt 0,742 s, aus dem Zwischenspeicher 0,00014 s, Tk-Grafik bauen 0,235 s (erste),
danach fuenf Zeichnungen 0,032 / 0,089 / 0,235 s (min/mittel/max). Bei den heutigen 20 px je Feld:
kalt 0,462 s, warm 0,00013 s. Die Karte ist EIN Bild - die Anzeige zeichnet heute 400 Rechtecke und
42 Rasterlinien je Ansicht.

**Wache:** `tests/test_weltkarte_malerei.py` **67 Pruefungen, 0 Fehler, 1 Befund** (sieben Arten aus
`data/gelaende.json` statt einer zweiten Farbtabelle; jede Kachel ueber 600 Farben mit Mittelton an
der Gelaendefarbe; Wald 1.361 dunkle Nadelgruen-Pixel gegen 112 im Grasland; ohne Pillow
`MalereiFehler` statt Ersatzbild; Zwischenspeicher und Determinismus; ganze Karte in Rastermassen).

**Ein Anlauf wurde verworfen, offen benannt:** Kachel fuer Kachel gemalt und die Raender
weichgezeichnet ergab ein Waffelmuster (angesehen). Der zweite Anlauf malt die Karte als EIN Bild.

**Offen:** der Einbau ins Spiel (D-4) wartet auf Daniels Urteil; die Testkarte liegt als PNG in
`archiv/design/20261109_d3_testkarte/`.

# STAND 09.11.2026, 01:50 - Portal S-1 bis S-4 gebaut UND belegt: Belegungskarte, Umzug gebucht, Feldklick in der Ansicht (Register 324 bis 326)

> Neuester Block. Darunter 21:52 (E1 Handelspreis; Register 323), 20:52 (Wall und Marktplatz;
> Register 321-322), 20:28 (Wall in der Rubrik Verteidigung), 18:50 (Opus als Werkzeug, drei Befunde;
> Register 314-320), 15:50 (Schritt 11, AST-Quellwache; Register 309), 14:55 (Spieltest 2;
> Register 307), 14:00 (Spieltest 1, Soft Lock, V-3; Register 306).

**Der Portal-Umzug hat jetzt seinen Unterbau - aber noch keinen Sprung.** Daniel hat die vier
Portal-Fragen F-25 bis F-28 beantwortet (F-26 = A: ein belegtes Feld wird abgelehnt), und die ersten
zwei der sechs Schnitte aus `docs/design/PORTAL_MODELL_20261108.md` sind gebaut.

1. **S-2 - der Koordinatenraum ist entschieden:** `Settlement` traegt zwei eigene Felder `welt_x`/
   `welt_y` fuer den Portalraum (0..19). `x`/`y` bleibt die Siedlungskarte, die beiden Raeume werden
   nie verrechnet (Widerspruch W-3). `_ort_feld` liest zuerst `welt_x`/`welt_y` und faellt nur bei
   alten Staenden auf `x`/`y` zurueck. **Abweichung vom Modell, ausdruecklich:** dort stand als
   Vorgabe 0/0 - das ist im 20 x 20-Raster ein GUELTIGES Feld. Der Vorgabewert ist deshalb `None`
   (noch nicht im Portal verortet), sonst waere ein Dorf auf Feld 0/0 von einem unverorteten nicht zu
   unterscheiden. Die Kennung `siedlung_kennung` bleibt unberuehrt (W-1 entschaerft).
2. **S-1 - die Belegungskarte im Kern:** `portalraum.feld_eintrag`, `belegungs_karte` und
   `feld_status` beantworten frei / belegt / ausserhalb mit deutschem Grund, gezaehlt je
   (Welt-Index, x, y) - zwei Welten mit demselben Feld kollidieren NICHT. Die Funktion liest keinen
   Spielstand; hereingereicht werden nur die belegten Felder (eigene Siedlungen, Bot-Doerfer aus
   `bottaktik.dorf_position`). Ein Eintrag ausserhalb des Rasters wirft `ValueError`, statt still zu
   verschwinden. Der Parameter `ausschluss` haelt fest, dass ein Dorf sich nicht selbst blockiert.

**Gemessen:** neue Wache `tests/test_portal_feld_belegung.py` **40 von 40 gruen** (mehr als die im
Modell veranschlagten 12 bis 16, weil auch die S-2-Felder und der Rueckfall fuer Altstaende mitgeprueft
werden). **Zwei Gegenproben:** auf dem Altstand bricht die Datei mit `AttributeError: module
portalraum has no attribute feld_status` ab; mit den Feldern, aber OHNE die neue Aufloesung in
`_ort_feld`, stehen **38 bestanden, 2 FEHLER** - genau die zwei S-2-Zusagen. **Sammellauf 22:30 bis
22:44: 209 von 209 gruen, 0 rot, 2 ausgesetzt, 9.075 Pruefungen, 784 s**
(`docs/audits/sammellauf_20261108_2230.log`); die 40 neuen Pruefungen sind genau der Zuwachs gegen
9.035. Nachbarn einzeln gruen: `test_portalraum` 70/0/0, `test_portal_uebersicht` 61/0/0,
`test_portal_fremdblick` 18/0/1, `test_speichern_robust` 95/0/5, `test_marsch_optik` 63/0/0.

3. **S-3 - der Umzug wird gebucht:** `_dorf_versetzen(name, x, y, welt)` prüft in fester
   Reihenfolge (Dorf da, nichts unterwegs, Welt bekannt, steht noch nicht dort, Feld frei, Mana,
   Sperre) und bucht dann GENAU EINMAL: Mana minus 5.000, `welt_x`/`welt_y`, die Welt des Dorfes
   und die gezeigte Welt. Bauten, Garnison, Waren und Karawanen werden nicht angefasst und reisen
   damit mit (F-27 = A). `_portal_belegte_felder()` übersetzt den Spielstand in Felder.
   **W-1 ist damit erledigt:** die Kennung bleibt gültig, weil der Umzug `x`/`y` nicht anfasst —
   kein Neu-Bilden, kein Nachziehen. Wache `tests/test_dorf_versetzen.py` **38/0/0**; Gegenprobe
   auf dem Altstand rot (Abbruch), Gegenprobe mit abgeschalteter Feldprüfung **32 bestanden,
   6 FEHLER** (genau die Feld- und Belegungszusagen).

4. **S-4 - die Ansicht (Daniels Antwort A):** der Knopf „Weltensprung“ in der Weltkartenliste ist
   WEG. Unter der Karte steht jetzt „Dorf versetzen“: ein Knopf je eigener Siedlung, ein Klick ins
   Feld, eine Zeile mit Feld, Gelände und STATUS samt Grund, und der Knopf „<Dorf> hierher versetzen
   (5.000 Mana)“ — gesperrt mit Grund (kein Feld, Feld nicht frei, Mana, Aufträge). Gebucht wird
   ausschließlich über `_dorf_versetzen` (S-3). **Fund dabei, behoben:** die Karte zeichnete eigene
   Dörfer auf `x`/`y` (Siedlungskarte) statt auf ihrer Portalposition — jetzt über `_ort_feld`.
   Wache `tests/test_portal_ansicht_umzug.py` **26/0/0**; Gegenprobe auf dem Altstand rot,
   Gegenprobe mit der alten Zeichnung **24 bestanden, 2 FEHLER**.

**Sammellauf Sitzung 24 (01:36 bis 01:49): 213 Dateien, 211 von 211 grün, 0 rot, 2 dokumentiert
zurückgezogen, 9.139 Prüfungen, 0 Fehler, 75 Befunde, 729 s**
(`docs/audits/sammellauf_20261109_0136.log`) — genau die erwarteten 9.139 (9.113 des Laufs 23:03
plus die 26 der S-4-Wache). Probe vor dem Start: die erste kleine Wache brauchte 7,5 s (kalter
erster Zugriff), die zweite 1,35 s; erst danach gestartet.

**Offen:** `_portal_wechsel` hat keinen Aufrufer mehr und fällt in **S-4b** samt seinen Wachen
(`test_durchspiel`, `test_e2e_wege`, `test_portal_uebersicht`, `test_weltkarten_anzeige`), die dabei
auf die Buchstelle umgestellt werden. Danach S-5 (24-Stunden-Prüfung aus `wechsel_erlaubt`, F-28 = C)
und S-6 (Wachen, voller Lauf, EXE).

**Registerluecke gefunden und geschlossen:** die Nummern 309 bis 323 standen nur in den
Protokollzeilen, im Register fehlten sie (hoechste Nummer war 308). Sie sind als Kurzfassung mit
Verweis auf die jeweilige Protokollzeile nachgetragen; offen bleiben die Nummern 272 und 273
(aeltere Luecke).

# STAND 08.11.2026, 21:52 - E1 gebaut: der Handelspreis haengt am Rohstoff (Register 323)

> Aelterer Block (durch 22:50 abgeloest). Darunter 20:52 (Wall und Marktplatz; Register 321-322), 20:28 (Wall in der Rubrik
> Verteidigung), 18:50 (Opus als Werkzeug, drei Befunde; Register 314-320), 15:50 (Schritt 11,
> AST-Quellwache; Register 309), 14:55 (Spieltest 2; Register 307), 14:00 (Spieltest 1, Soft Lock,
> V-3; Register 306).

**E1 ist fertig: jedes Rohstoff-Stueck hat seinen eigenen Preis.** Bis heute kostete JEDES Stueck
dasselbe - 300 Gold, der Preis einer Kampfeinheit. Jetzt rechnet `bot_handelpreis` aus dem, was das
Spiel schon fuehrt: Reserve und Schattenpreis des Bots (`botkern.oekonomie_angebot`), seinen Bedarf je
Stunde, seine Stufe und die Karte des Handelsorts. Ankunft, Kaufmaske und Verkaufsmaske fragen
DIESELBE Funktion; die Zeile ueber dem Preisfeld rechnet beim Warewechsel neu und zieht den Vorschlag
nach.

**Gemessen (Bot mit 400 Holz und 900 Gold):** Holz **0,45** Gold je Stueck, Stein 0,90, Gold 1,20.
Ein knapper Bot zahlt beim Einkauf **1,69** statt 0,45. Die Vorsitzung hatte mit demselben Code
0,46 / 0,92 / 1,22 abgelesen (Rundung, anderer Botzustand) - die Pauschale 300 ist in jedem Fall weg,
und 100 Holz bringen jetzt rund 45 Gold statt 30.000.

**Belegt:** neue Wache `tests/test_handelspreis_je_rohstoff.py` **22/0/0**; **Gegenprobe ohne
Verdrahtung 17 bestanden, 5 FEHLER**; Gegenprobe auf dem Altstand `1fd8d0c` rot. Eine alte Wache hielt
die Pauschale fest (`test_handelspunkte` tippte den Preis 1,0) - sie liest ihn jetzt aus derselben
Funktion und steht bei **38/0/0**. **Sammellauf 21:38 bis 21:51: 208 von 208 gruen, 0 rot,
9.035 Pruefungen, 758 s** (`docs/audits/sammellauf_20261108_2138.log`).

**Reihenfolge ab jetzt** (Daniels Antworten F-15 bis F-24, Akte
`docs/FRAGEN_AN_DANIEL_20261107.md`, Nachtrag 22:35): Portal-Modell mit vier Fragen (F-21) ->
Bibliothek versetzen (F-17) -> Pakt ueber die Gunst-Schwelle 40 (F-18) -> Quellenwoerter (F-15/F-16)
-> Postfach-Obergrenze (F-22) -> voller Sammellauf, EINE EXE, Spieltest 4 (F-24). Dazu offen wie
bisher: E3 Portal-Sperre in Spielzeit (Entscheidung 308) und zwei Skill-Ergaenzungen, die Daniels
Freigabe in der App brauchen (F-23).

# STAND 08.11.2026, 20:52 - Spieltest 3, Noten 3 und 5 gebaut: Wall in Verteidigung, Marktplatz auffindbar (Register 321-322)

> Aelterer Block (durch 21:52 abgeloest). Darunter 20:28 (Wall in der Rubrik Verteidigung; Register 321), 18:50 (Opus als
> Werkzeug, drei Befunde; Register 314-320), 15:50 (Schritt 11, AST-Quellwache; Register 309), 14:55
> (Spieltest 2; Register 307), 14:00 (Spieltest 1, Soft Lock, V-3; Register 306).

**Zwei der vier Test-3-Punkte sind gebaut, jeder mit eigener Wache und Gegenprobe.**

1. **Wall (Note 3, Register 321):** der Dorfwall steht an EINER Stelle - auf der Siedlungskarte in der
   Rubrik Verteidigung, ohne gewaehltes Feld. Das Dorfzentrum zeigt eine Zeile mit Zustand und dem Knopf
   „Wall verwalten“. Wache `tests/test_wall_verteidigung.py` **13/0/0**, Gegenprobe auf dem Altstand
   **8 bestanden, 5 FEHLER**.
2. **Marktplatz (Note 5, Register 322):** die Ansicht sagt, dass der Spieler hier verkauft, nennt die
   Handelskarawane im Ortslager mit Anzahl (oder dass ohne sie jeder Handel abgelehnt wird) und zeigt
   JEDEN Bot - wer nicht handelt, steht mit Handelsneigung und Grund da statt zu fehlen. Die Grenze 0,3
   stand vorher an vier Stellen getippt; sie ist jetzt `HANDELSNEIGUNG_MIN` mit `handelt_bot` /
   `handelt_grund` fuer Kern, Maske und Anzeige. Wache `tests/test_marktplatz_ansicht.py` **19/0/0**,
   Gegenprobe **10 bestanden, 9 FEHLER**.

**Sammellauf 20:38 bis 20:51: 207 von 207 gruen, 0 rot, 2 ausgesetzt, 9.015 Pruefungen, 763 s**
(`docs/audits/sammellauf_20261108_2038.log`). Der Lauf davor (20:13) war 206/206 bei 8.996 Pruefungen;
die 19 neuen Pruefungen sind genau die neue Wache.

**Was NICHT fertig ist (Test 3, Noten 4 und 8):**
1. **Portal per Klick auf ein freies Weltfeld** (Note 4): der Kern fehlt komplett - `_portal_wechsel`
   versetzt kein Dorf (gemessen, Z. 11747-11791 setzt nur `eigene_dimension`), ein `dorf_versetzen` gibt es nicht.
2. **Bibliothek versetzen** (Note 8): „eine Bibliothek je Siedlung“ ist ORIGINALREGEL; ein Versetzen als
   EINE Buchung haelt sie ein. **Frage 17 ist Daniels Entscheid** (Empfehlung: Versetzen als eine Buchung,
   Neubau auf Stufe 1) - ohne seine Bestaetigung wird nicht gebaut.
3. **E1 Handelspreis je Rohstoff** (Entscheidung 306): Patch-Plan in
   `docs/extern/antworten/20261108_1847_...md`; drei Stellen sind dort als UNGELESEN markiert (Herkunft von
   `stufe`, `karte`, `tagesbedarf`; Schluessel `ware` im Handelsvertrag; wo die Schwelle in der Maske steht).
4. **E3 Portal-Sperre in Spielzeit** (Entscheidung 308): vier `time.time()`-Stellen (Z. 11742, 11774,
   11779, 12343) plus Altstand-Reparatur beim Laden (Z. 8092).
5. Danach der volle Sammellauf und EINE EXE, dann Spieltest 4.

**Bei Daniel offen:** Frage 15 (neun Balance-Werte ohne Quelle), Frage 16 (sechs Datendateien ohne
Quellenangabe), Frage 17 (Bibliothek), Frage 18 (Pakt) - zu allen liegt eine Empfehlung vor, bestaetigt ist keine.

# STAND 08.11.2026, 20:28 - Spieltest 3, Note 3 gebaut: der Wall steht in der Rubrik Verteidigung (Register 321)

> Aelterer Block (durch 20:52 abgeloest). Darunter 18:50 (Opus als Werkzeug, drei Befunde; Register 314-320), 15:50 (Schritt 11,
> AST-Quellwache; Register 309), 14:55 (Spieltest 2; Register 307), 14:00 (Spieltest 1, Soft Lock, V-3;
> Register 306).

**Der Wall-Umzug aus dem Stash ist fertig** (`stash@{0}` aufgeloest, kein Zwischenstand mehr offen).
Der Dorfwall steht jetzt an EINER Stelle: auf der Siedlungskarte in der Rubrik Verteidigung, ohne
gewaehltes Feld. Das Dorfzentrum zeigt nur noch eine Zeile mit Zustand und dem Knopf „Wall verwalten“,
der die Karte direkt in der Rubrik Verteidigung oeffnet.

**VORHER GEMESSEN (Altstand `ca3efa4`):** der Mauerblock wurde zweimal gebaut (`_render_overview` im
Dorfzentrum UND die Wallzeile ueber der Karte); die Rubrikwahl stand HINTER der Feldpruefung, „Verteidigung“
war also nur nach einem Feldklick erreichbar, obwohl der Wall kein Kartenfeld belegt; hinter einem `return`
lag ein unerreichbarer Aufruf von `_mauer_reparatur_block` samt dem Spielersatz „Der Dorfwall belegt kein
Kartenfeld“ (der tote Code aus der Opus-Pruefung).

**GEMESSEN:** neue Wache `tests/test_wall_verteidigung.py` **13/0/0** - sie prueft die Quellstruktur per
`ast` (genau EINE Methode ruft `_mauer_reparatur_block`, die Wallzeile steht in der Spalte mit der
Baubereich-Auswahl) UND die sichtbare Folge in einem echten Fenster (Stufe, Zustand, Reparaturpreis ohne
Feld; in der Rubrik Produktion erscheint keine Wallzeile). **Gegenprobe gegen den Altstand: 8 bestanden,
5 FEHLER.** Der erste Anlauf der Wache war selbst zu schwach und ist verschaerft worden: „Stufe“ steht
auch in „Ausbaustufe“, und die Fensterpruefung setzte `karten_siedlung` nicht (Rueckfall „Noch keine
Siedlung gewaehlt“).

**Zwei alte Wachen hielten den Umzug fest und wurden am ANKER umgestellt, nicht gelockert:**
`test_gpt_baumenue_kategorien_fix04` verlangt den Satz „belegt kein Kartenfeld“ - er steht jetzt in
`_wall_block`, wo er hingehoert; `test_anzeigetexte_umlaute` fand „ueberwinden“ in einem neuen Anzeigetext
(jetzt „überwinden“).

**Sammellauf 20:13 bis 20:26: 206 von 206 gruen, 0 rot, 2 ausgesetzt, 8.996 Pruefungen, 773 s**
(`docs/audits/sammellauf_20261108_2013.log`). Der Lauf davor (20:14) war 2 rot - genau diese zwei Anker.

**Was NICHT fertig ist (Test 3, Noten 4, 5, 8):**
1. **Marktplatz auffindbar** (Note 5): Karawane als Voraussetzung nennen, den Zustand zeigen, ALLE Bots
   zeigen statt sie bei Neigung <= 0,3 zu verstecken.
2. **Portal per Klick auf ein freies Weltfeld** (Note 4): der Kern fehlt komplett - `_portal_wechsel`
   versetzt kein Dorf (gemessen, Z. 11747-11791 setzt nur `eigene_dimension`), ein `dorf_versetzen` gibt es nicht.
3. **Bibliothek versetzen** (Note 8): „eine Bibliothek je Siedlung“ ist ORIGINALREGEL; ein Versetzen als
   EINE Buchung haelt sie ein. **Frage 17 ist Daniels Entscheid, nicht meine** (Empfehlung liegt vor).
4. **E1 Handelspreis je Rohstoff** (Entscheidung 306, Patch-Plan in `docs/extern/antworten/20261108_1847_...md`);
   drei Stellen sind dort als UNGELESEN markiert (Herkunft von `stufe`, `karte`, `tagesbedarf`; Schluessel
   `ware` im Handelsvertrag; wo die Schwelle in der Maske steht).
5. **E3 Portal-Sperre in Spielzeit** (Entscheidung 308): vier `time.time()`-Stellen (Z. 11742, 11774, 11779,
   12343) plus Altstand-Reparatur beim Laden (Z. 8092).
6. Danach der volle Sammellauf und EINE EXE, dann Spieltest 4.

**Bei Daniel offen:** Frage 15 (neun Balance-Werte ohne Quelle), Frage 16 (sechs Datendateien ohne
Quellenangabe), Frage 17 (Bibliothek), Frage 18 (Pakt) - zu allen liegt eine Empfehlung vor, bestaetigt ist keine.

# STAND 08.11.2026, 18:50 - Opus-Lieferung abgelegt und geprueft; drei Befunde gebaut (Register 314-317)

> Aelterer Block (durch 20:28 abgeloest). Darunter 15:50 (Schritt 11, AST-Quellwache; Register 309), 14:55 (Spieltest 2;
> Register 307), 14:00 (Spieltest 1, Soft Lock, V-3; Register 306).

**Die Uebergabe 16:20 ist abgearbeitet, soweit sie ohne Daniel geht:** der ausstehende volle
Sammellauf ist gefahren (18:01: 203 von 204 gruen, 1 rot - die rote Wache widersprach Register 311 und
ist berichtigt; **18:42 nach allen Aenderungen: 205 von 205 gruen, 0 rot, 8.971 Pruefungen, 789 s**),
die Opus-Lieferung liegt im Repo und ist gegen den Code gemessen.

**Was NEU im Repo liegt (nur lesen, nichts davon ist Spielcode):**
`docs/extern/ANTWORT_OPUS_20261108.md` (5 Teile, SHA256 `09fd7992...`),
`docs/extern/SPIELTEST_OPUS_WEITERER_20261108.md` (8 Teile, SHA256 `7290c7f3...`) und
`docs/extern/PRUEFUNG_OPUS_20261108.md` (Gegenprobe: **17 von 19 Angaben zeichengenau bestaetigt**,
zwei Zaehlabweichungen ohne Folge). Daniels Desktop ist geraeumt; die Herkunft steht mit `MANIFEST.md`
unter `D:\Arbeiten\Hermes\Eingaenge61108_Opus_Spieltest\`.

**Opus ist ab jetzt ein Werkzeug (Daniel im Chat):** `tools/frage_opus.py` fragt Claude Opus 5.5
ueber das Abo, **nur lesend**, und legt jede Antwort unter `docs/extern/antworten/` ab - keine
Auftragsdatei mehr auf dem Desktop. Grenzen in `docs/OPUS_DELEGATION.md` (kein Schreiben, keine
Abbuchung, keine parallelen Laeufe, eine Frage je Lauf). **Erster Review mit Wert:** Opus hat den
eigenen Umbau `2f12471` geprueft - fuenf Punkte waren berechtigt und sind behoben (echter
Diebstahl-Erzeuger jetzt belegt, Docstring repariert, Pruefung 8d verschaerft), zwei sind als Grenze
notiert, zwei nach Messung zurueckgewiesen. **Nebenertrag:** der Patch-Plan fuer E1 liegt mit Ankern vor.

**Was GEBAUT ist (drei kleine Befunde, jede mit Gegenprobe):**
1. **S4** - ein ungelesener Diebstahlbericht verschwindet nicht mehr nach einem Spieltag
   (`data/nachrichten.json` + Rueckfall `postfach.py`), Wache `test_nachrichten_archiv` 56/0/0.
2. **S5** - die Ausbildungs-Vorschau rechnet immer mit Menge 1, der Preis steht also auch dann da, wenn
   nichts bezahlbar ist; der Knopf bleibt gesperrt (`tests/test_ausbildung_vorschau.py`, 9/0/0).
3. **S6** - Forschungs-Sperrtext nennt Soll und Ist in Worten und in derselben Reihenfolge
   ("Bibliothek Stufe 3 (hast 1)"); `test_forschungspfad` 124/0/0, `test_lokale_forschung` 47/0/0.

**Daniels Entscheidungen 17:52 sind als 306, 307, 308 im Register** (Handelspreis je Rohstoff,
Wall/Ausbau beenden den Goetterschutz, Portal-Sperre in Spielzeit). **Alle drei sind noch NICHT
gebaut** - sie sind der naechste Bauabschnitt.

**Der naechste Schritt (verbindlich, in dieser Reihenfolge):**
1. **E1 Handelspreis je Rohstoff** - `botkern.oekonomie_angebot` ist fertig und wird von KEINER
   Stelle aufgerufen (gemessen); der Spielerhandel nimmt pauschal 300 Gold (main.py Z. 5190/10583).
2. **Wall in die Siedlungskarte unter Verteidigung** (Daniels Wortlaut 16:35) - der tote Code
   `main.py` Z. 11644/11645 zeigt, warum die Reparatur nie auf der Karte stand.
3. **Portal per Klick auf ein freies Weltfeld** - `_portal_wechsel` versetzt heute KEIN Dorf
   (gemessen, Z. 11747-11791); Daniels Note 4 ist damit nicht Bedienung, sondern ein Fehler.
4. **Bibliothek versetzen** - "eine Bibliothek je Siedlung" ist ORIGINALREGEL
   (`data/buildings.json`, `_belegt_nur_auf`); ein Versetzen als EINE Buchung haelt sie ein.
5. **Marktplatz auffindbar** (Kasten "So handelst du", Karawanen-Zustand, alle Bots zeigen).
6. **E3 Portal-Sperre in Spielzeit** samt Altstand-Reparatur fuer `letzter_wechsel`.
7. Danach der volle Sammellauf und EINE EXE, dann Spieltest 4.

# STAND 08.11.2026, 15:50 - Schritt 11 fertig: die AST-Quellwache steht (Register 309)

> Neuester Block. Darunter 14:55 (Spieltest 2: Wall, Gelaende-Hinweis, Bibliothek; Register 307),
> 14:00 (Spieltest 1: Soft Lock gemessen, V-3; Register 306), 12:32 (Schritt 12; Register 303/304).

**Schritt 11 ist gebaut und belegt.** `tests/test_quelle_ast.py` prueft ueber `ast` alle 29
Ansichts-Methoden von `NebelseetalApp` (`_zeige*`, `_zeichne*`, `_render*`) auf Multiplikationen,
Divisionen und Vergleiche gegen eine Ganzzahl groesser 1. Docstrings und Kommentare zaehlen nicht.
**Vorher gemessen: 33 Stellen in 4 Methoden. Nachher: 29 Stellen in 2 Methoden** - die beiden
Pixelmethoden (`_render_portal`, `_zeichne_siedlungskarte`) stehen mit Grund in
`tests/quelle_ast_ausnahmen.json`; alles andere ist aus den Ansichten verschwunden.

**Was die Wache sofort gefunden hat:** `_heilkunde * 10` in der Dorfuebersicht (die Handbuchzahl
stand ein zweites Mal in der Anzeige - jetzt `forschung_wirkung.siedler_bonus_prozent`),
`rest / 60.0` (jetzt `main.minuten_text`) und fuenf Stellen mit `int(bot.trading * 100)` (jetzt
`main.prozent_text`). Beim Einbau fiel auf, dass `forschung_wirkung` in `main.py` gar nicht
importiert war - der GUI-Test meldete es sofort als NameError, nicht still.

**Die Wache hat eine Gegenprobe im eigenen Lauf:** auf erfundenem Quelltext werden `stufe * 2` und
`if stufe >= 3` erkannt, ein Vergleich gegen 1 nicht - sie kann also rot werden. Ergebnis **15/0/2**.
Eine veraltete Ausnahme (Methode ohne Treffer oder zu weit gefasst) wird als BEFUND gemeldet, damit
die Liste kein Freibrief wird.

# STAND 08.11.2026, 14:55 - Spieltest 2: Wall im Dorfzentrum, Gelaende-Hinweis, Bibliothek-Auskunft (Register 307)

> Neuester Block. Darunter 14:00 (Spieltest 1: Soft Lock gemessen, V-3, Register 306), 12:32
> (Schritt 12, Sammellauf parallel; Register 303, 304), 11:25 (Stand unveraendert, Guthaben).

**Daniel hat Test 2 mit der neuen EXE `b50d6f05` gespielt (Hash der gelieferten Datei geprueft) und
nach Schritt 5 abgebrochen.** Vier Schritte beantwortet: Schritt 1 Note 1, Schritt 2 Note 1 mit
Vorbehalt ("Los geht es" wirkte zunaechst wirkungslos, der Sprung kam nach Warten - die Maschine war
ueberlastet), **Schritte 3 und 4 Note 5**, Schritt 5 ohne Note mit Abbruch.

**Der Wall war nicht auffindbar.** Daniel: "kann ich egal wo keine Uebersicht finden von einem Wall
oder wo ich ihn ausbauen koennte". Er stand bis heute NUR auf der Siedlungskarte. Jetzt zeigt das
Dorfzentrum - die Ansicht, in der der Spieler landet - einen Wall-Kasten mit Stufe, Zustand und
**demselben** Reparaturblock wie die Karte (Preis, Dauer, Knopf), dazu die Herkunft der Stufen
(Forschung "Verteidigungsanlagen") und, wenn kein Wall steht, den Weg dorthin.

**"Kein Gebaeude baubar" war eine Auskunftsluecke.** Am Teststand nachgestellt: auf einem
Nebelsee-Feld gibt es in der Rubrik "Produktion" kein Gebaeude, und die Ansicht sagte nur "Keine
passenden Gebaeude in dieser Rubrik". Neu nennt sie das Gelaende, freie Felder anderer Art mit
Koordinaten ("Wald (A1), Grasland (E7)") und - wenn eine andere Rubrik auf demselben Feld baut -
diese Rubrik. **Was sich NICHT nachstellen liess, offen:** mit 242 Holz und 418 Stein waren Haus und
Tempel im echten Klickpfad sofort baubar; die einzige gemessene Sperre war die Bibliothek
(hoechstens 1 je Siedlung, im Teststand steht schon eine).

**"Die Bibliothek war komplett sinnlos auf einem Nebelsee" war eine falsche Auskunft der Anzeige.**
Die Dorfuebersicht meldete "Bibliothek liefert auf Nebelsee nichts" und meinte den ROHSTOFFERTRAG.
Eine Bibliothek erzeugt keine Rohstoffe, sie traegt die Forschung. Der Satz lautet jetzt "erzeugt
keine Rohstoffe (Aufgabe: ermoeglicht Forschung ...)", und die Obergrenze sagt, dass eine zweite
Bibliothek auf einer anderen Siedlung erlaubt ist.

**Ereignis-Flut gemessen, nicht geaendert:** 10 Spieltage ab Tag 5 ergeben **33 Nachrichten**
(21 Diplomatie-Ereignisse, 9 Gruendungen, 3 Kaempfe) - rund 3,3 je Spieltag, jede zusaetzlich in der
Statuszeile. Weniger Ereignisse oder ein Filter waeren eine Regel-Entscheidung Daniels.

Wache `tests/test_spieltest2_befunde.py` **14/0/2**. Offen aus Test 2: die Schritte 5 bis 11
(Handel, Pakt, Portal, Weltkarte, Punkte, Speichern, Beenden) sind UNGETESTET.

# STAND 08.11.2026, 14:00 - Spieltest 1: die Ursache des Soft Locks ist gemessen und die Anzeige sagt die Wahrheit (Register 306)

> Neuester Block. Darunter 12:32 (Schritt 12, Sammellauf parallel; Register 303, 304), 11:25 (Stand
> unveraendert, Guthaben), 01:40 (Spieltest-Paket, Register 301; Messwerte-Ablage, Register 302),
> 01:05 (Schritt 10, Register 299; Pakt-Knopf, Register 300).

**Der Soft Lock war nicht die Bibliothek - es war die Nahrungsnot.** Daniels Spielstand
(`~/.nebelseetal/savegame_slot1.json`, gespeichert 12:56) und der vorbereitete Teststand (Slot 2)
laden sauber, stehen aber BEIDE in Nahrungsnot: Ortslager Nahrung **0,0**, Bedarf **8,0 je Tag**,
eigene Ernte **0,0**. Der Bedarf kommt allein von EINER Handelskarawane, weil
`spieloekonomie.tagesbedarf_nahrung` JEDE Einheit im Ortslager zaehlt (Karren und Belagerungsgeraete
ausdruecklich mit). Die Sperre aus Entscheidung 70/74 blockt dann Bauen, Ausbauen, Ware, Forschung und
Ausbildung. Die Bibliothek auf dem Nebelsee war eine ERLAUBTE Standortregel (`data/buildings.json`,
`nur_auf` = Grasland/Steppe/Nebelsee) - sie war nur der Ort, an dem Daniel es bemerkt hat. **Damit ist
auch klar, warum Test 1 sofort stillstand: der Teststand ist gesperrt, bevor der Spieler etwas tut.**

**"Gruener Text, Wirkung null" war eine zweite Rechenstelle.** Die Sperre fragten die fuenf
Zahlstellen, die ANZEIGE nicht: das Baumenue schrieb in diesem Stand bei **14 von 14** Zeilen
"Baubar - Rohstoffe vorhanden" (heller Knopf), die Knoepfe fuer Forschung, Ware und Ausbildung waren
frei - der Klick brach dann ab, der Grund stand nur in der Statuszeile. Neu fragt die Anzeige dieselbe
Stelle wie der Klick: `main.bauanzeige_pruefung` (Modul, ohne Fenster pruefbar) fuer das Baumenue,
`_nahrungssperre` fuer Forschung, Werkstatt und Ausbildung. Ergebnis im nachgebauten Not-Stand: **0 von
14 baubar, jede Zeile mit dem Sperrtext**; Gegenprobe mit 5 Nahrung im Lager: wieder 2 von 14 baubar.
Wache `tests/test_spieltest1_befunde.py` **21/0/2**.

**Die zwei kleinen Befunde sind gebaut.** "Los geht es" fuehrt jetzt ueber `main.intro_ziel` zur
Fraktionswahl (frischer Start: Schritt 2 "Dein Volk"; geladener Stand: Dorfzentrum) statt nur den
Dialog zu schliessen. Die orange Wortmarke "Remake" unter dem Logo ist weg (Passworttor und
Ladebildschirm); Logo und gelbe Hinweiszahlen bleiben. `tools/teststand_vorbereiten.py` meldet einen
Stand, der in Nahrungsnot steht, in der Ausgabe UND im Postfach des Standes - es wird keine Nahrung
erfunden.

**Daniel hat entschieden (V-3, 14:02): beides.** Karren und Belagerungsgeraete essen nicht mehr mit - die Rolle steht in `data/units.json`, die Liste `rollen_ohne_verbrauch` in `data/nahrungsverbrauch.json`, gelesen in `spieloekonomie.isst_nicht_mit`. Gemessen: eine Handelskarawane allein ergibt jetzt Bedarf **0,0** statt 8,0; ein Krieger ergibt weiter 8,0 und Not. **Und** ein Nahrungsgebaeude bleibt in der Not baubar und zahlbar (`gelaende.erzeugt_nahrung` aus der Ertragstabelle in `data/buildings.json`; `_karten_bauen`, `_karten_ausbauen` und `bauanzeige_pruefung` lassen genau diese Gebaeude durch). Auf Wald ist in der Not nur der Jaeger baubar - er braucht keine Forschung und ist damit der Ausweg, den Entscheidung 70 nennt. Der Sperrtext nennt ihn jetzt auch (Satz aus der Datendatei). Wachen umgedreht: `test_nahrungsverbrauch` belegte vorher "Karren zaehlen mit" und belegt jetzt das Gegenteil, mit Grund im Docstring.

**Sammellauf 14:09 (nach dem Fix, mit -j 2): 198 von 199 gruen, 1 rot, 2 ausgesetzt, 8.900 Pruefungen, 63 Befunde, 708 s.** Der eine Rote war `test_geschenk_nachricht` - sie verlangte die Schenkungs-Botschaft in `savegame_slot1.json`, und genau den Slot hat Daniel beim Test 1 um 12:56 ueberschrieben. Am Code war nichts; die Pruefung sucht jetzt alle lokalen Slots und meldet bei fehlendem Nachweis einen BEFUND mit Ursache. **Sammellauf 14:23 (nach dem Fix, ohne Spielprozess): 199 von 199 gruen, 0 rot, 2 ausgesetzt, 8.900 Pruefungen, 64 Befunde, 561 s** (`docs/audits/sammellauf_20261108_1423.log`). Der Vergleich mit dem Lauf 14:09 (708 s, gleiche 201 Dateien, gleiche Urteile) misst den Lastunterschied: 147 s, Faktor 1,26 - kein Codeunterschied.

**NICHT behoben:** die Design-Note 4 ("zu wenig farbe und Zuviel braune hintergruende"). Eine Palette
zu erfinden waere geraten; sie braucht Daniels Richtung. Ebenfalls offen: die drei Punkte aus der
Vorgaengeruebergabe (Schritt 11 AST-Quellwache, Schritt 13 Daten-und-Quellen-Pruefung, R3-3/R3-4,
Besucherdokumente, F-20 = B), 43 Pruefdateien ohne `bericht()`, die zwei Skill-Vormerkungen und der
Projekt-Skill an der Groessengrenze.

# STAND 08.11.2026, 12:32 - Schritt 12 fertig: Sammellauf parallel und vollstaendig ausgewertet (Register 303, 304)

> Neuester Block. Darunter 11:25 (Stand unveraendert, Guthaben), 01:40 (Spieltest-Paket, Register 301;
> Messwerte-Ablage, Register 302), 01:05 (Schritt 10, Register 299; Pakt-Knopf, Register 300).

**Der Sammellauf faehrt parallel, und das Ergebnis ist dasselbe.** Aufruf
`tools/sammellauf.py -j 2` (Vorgabe bleibt 1 = wie bisher). Gemessen mit demselben Code und denselben
200 Dateien: **seriell 198 von 198 gruen, 0 rot, 2 ausgesetzt, 1.132 s**
(`docs/audits/sammellauf_20261108_1148.log`) gegen **parallel 198 von 198 gruen, dieselben Dateien,
8.874 Pruefungen, 62 Befunde, 820 s** (`docs/audits/sammellauf_20261108_1212.log`) - **312 s weniger,
Faktor 1,38**. Mehr geht auf diesem Rechner nicht: 2 Kerne, und die Pruefdateien sind CPU-gebunden
(die Einzeldauern steigen unter Last von 1.132 s auf 1.623 s). Die Zeile `x1,98` im parallelen Log ist
Auslastung, kein Modi-Vergleich.

**Der eigentliche Befund war die Vorbedingung.** `test_baseline` und `test_gui_fehler` schreiben beide
nach `src/savegame.json` und raeumen einander die Datei weg, sobald sie gleichzeitig laufen - nacheinander
war das nie zu sehen. Statt 199 Pruefdateien umzubauen, bekommt jede Datei ihren eigenen Spielordner
ueber `NEBEL_SPIELDATEN_ORDNER` (der offizielle Hebel aus `main.schreibordner`, den schon acht
Pruefdateien nutzen). Rauchtest mit genau den beiden Konfliktdateien: 3 von 3 gruen, 22 s statt 42 s,
und `src/savegame.json` entsteht nicht mehr.

**Zwei Werkzeuge tragen den Parallelbetrieb.** Der Messwerte-Index laeuft unter einer Sperrdatei (ohne
Sperre gingen in der Gegenprobe **7 von 40** Eintraegen verloren, mit Sperre keiner). Und die
Ergebnis-Auswertung verlangt kein Befunde-Feld mehr: `test_projektpfade` (129), `test_textqualitaet`
(444) und `test_rueckmarsch` (16) schrieben es nicht und wurden als "ohne ERGEBNIS-Zeile" gefuehrt -
**589 Pruefungen zaehlen jetzt mit**, und ein Fehler darin macht weiterhin rot. A-6 im Auftragsdokument
nennt die gemessene Grenze (8.874 Pruefungen, unter 1.200 s seriell) als VORSCHLAG.

**Messumstand, wichtig fuer die naechste Sitzung:** Daniel hat um 11:28:20 die EXE gestartet und gespielt (Kind-PID 14668, ); alle Laeufe dieser Sitzung liefen unter dieser Last. Die URTEILE sind belegt (gleiche Datei-Liste in beiden Modi, 0 Abweichungen), die ZEITEN sind Lastzeiten. Ein sauberer Lauf ohne Spiel steht noch aus und wird nicht durch Schaetzen ersetzt.

**Offen und als naechstes:** Schritt 11 (AST-Quellwache `tests/test_quelle_ast.py` - Ziel: keine
Ansicht rechnet selbst, Docstrings und Kommentare zaehlen nicht), Schritt 13
(`tests/test_daten_und_quellen.py`), R3-3 (C-6, I-10, C-4), R3-4 (I-2), Besucherdokumente, eigener
Schnitt aus F-20 = B; dazu Daniels Noten aus dem Spieltest (die EXE und die Anleitung von 01:16 liegen
unveraendert auf dem Desktop). Weiter offen: 43 Pruefdateien ohne `bericht()` (BEFUND), die zwei
Skill-Vormerkungen und der Projekt-Skill bei 98.356 Zeichen.

# STAND 08.11.2026, 11:25 - Stand unveraendert, Guthaben abgelesen, Uebergabe Fassung 2

> Neuester Block. Darunter 01:40 (Spieltest-Paket, Register 301; Messwerte-Ablage, Register 302),
> 01:05 (Schritt 10, Register 299; Pakt-Knopf, Register 300), 21:30 (R3-2, Register 298).

**Am Stand hat sich seit 01:40 nichts geaendert:** Kopf `84d63f7`, gepusht, Arbeitsbaum leer, beide
Sammellaeufe 0 rot. Die EXE, die Anleitung und der vorbereitete Spielstand liegen unveraendert auf dem
Desktop bzw. in Spielerslot 2; die Desktop-Kopie der EXE wurde um 01:43 zusaetzlich gestartet
(Fenster "Nebelseetal Remake", Passworttor) und wieder beendet, `game.lock` entfernt.

**Guthaben (Daniel 11:23): 6,58 USD / 63,41 USD** - gegenueber 00:27 (6,74 / 63,25) also 0,16 USD fuer
die zweite Haelfte der Sitzung; kein bezahlter Fremdaufruf. Das Guthaben bleibt der knappste Posten.

**Offen und als naechstes unveraendert:** Schritt 12 (Sammellauf messen/parallelisieren, Ausgangswert
1.176 s bei 199 Dateien), Schritt 11 (AST-Quellwache), Schritt 13 (Daten-und-Quellen-Pruefung), R3-3,
R3-4, Besucherdokumente, eigener Schnitt aus F-20 = B; dazu Daniels Noten aus dem Spieltest, sobald
sie vorliegen.

# STAND 08.11.2026, 01:40 - Spieltest-Paket geliefert (Register 301), Messwerte-Ablage gebaut (Register 302)

> Neuester Block. Darunter 01:05 (Schritt 10, Register 299, und Pakt-Knopf, Register 300), 21:30
> (R3-2, Register 298), 21:05 (R3-1, Register 297).

**Daniel kann jetzt testen.** Auf dem Desktop liegen `Nebelseetal_Pre_Release_V_0.0.3.exe`
(82.684.749 Bytes, SHA256 `1ebbdf93...`, Start geprueft: das Passworttor erscheint) und
`SPIELTEST_ANLEITUNG_20261108.txt` (21 Schritte, je Soll / Beobachtung / Note 1-5). Der vorbereitete
Stand fuer die spaeten Wege liegt in Spielerslot 2 (`~/.nebelseetal/savegame_slot2.json`, geladen in
einer frischen `GameState`: Tag 5, Wall Stufe 1 bei 60 Prozent, Handelskarawane, 5.120 Mana); gebaut
mit `tools/teststand_vorbereiten.py` ueber echte Wege, nur drei Startwerte mit GRUND.

**Messwerte sind jetzt Daten (Register 302).** `tests/harness.bericht()` schreibt bei jedem Lauf
`docs/audits/messwerte/<datei>_<JJJJMMTT_HHMM>.json` (Zeitstempel, Dauer, Rechner, Python-Fassung,
Zaehler, Namen der Pruefungen, gemessene Zahlen) und fuehrt `index.json` fort. Zahlen werden ueber
`harness.messwert(name, wert, einheit, quelle)` festgehalten. Der Ordner ist gitignoriert (199 Dateien
je Lauf gehoeren nicht ins Repo). **Gemessene Luecke (BEFUND):** 43 von 199 Pruefdateien haben einen
eigenen Bericht ohne Rahmen und schreiben keine Messwerte - beim naechsten Anfassen umstellen.

**Sammellauf nach dem Umbau (01:19 bis 01:39): 197 von 199 gruen, 0 rot**, 8.257 Pruefungen,
61 Befunde, 1.176 s (`docs/audits/sammellauf_20261108_0119.log`); die zwei nicht gruenen Dateien sind
AUSGESETZT wie zuvor.

**Offen und als naechstes:** Schritt 12 (Sammellauf messen/parallelisieren - Ausgangswert 1.176 s bei
199 Dateien; die Vorbedingung "keine Pruefdatei schreibt in einen gemeinsamen Pfad" gilt jetzt auch
fuer die Messwerte-Ablage), Schritt 11 (AST-Quellwache), Schritt 13 (Daten-und-Quellen-Pruefung), R3-3
(C-6, I-10, C-4), R3-4 (I-2), Besucherdokumente, eigener Schnitt aus F-20 = B.

# STAND 08.11.2026, 01:05 - Schritt 10 abgeschlossen (E2E-Wege, Register 299), Pakt-Knopf gebaut (Register 300)

> Neuester Block. Darunter 21:30 (R3-2, Register 298), 21:05 (R3-1, Register 297), 20:48 (Modellrunde 3
> geprueft, F-21 = A), 20:15 (B-2 Regelkreis, Register 296).
>
> Diese Sitzung laeuft auf Daniels Wortlaut vom 08.11.2026, 00:25 OHNE Rueckfragen, bis der Kontext voll
> ist; jede eigene Entscheidung steht mit Begruendung im Protokoll und in der Uebergabe.

**Schritt 10 steht (Register 299).** `tests/test_e2e_wege.py` fuehrt die zwoelf End-zu-End-Ketten auf den
ECHTEN Spielwegen (Rohstoff, Forschung, Ware, Ausbildung, Einsatz, Rueckkehr, Speichern/Laden in einer
zweiten App, Handel ueber die echte Maske, Heilung, Mauerreparatur, Vertrag, Portal) und prueft sich selbst
per `ast`: ausser der Spieluhr darf nur in vier Startwertfunktionen etwas am Spielstand geschrieben werden,
jede mit GRUND im Docstring. **GEMESSEN:** 130 bestanden, 0 Fehler, 0 Befunde in 153 s.

**Der Befund der Kette 11 ist erledigt (Register 300, Daniels Entscheidung 1).** `diplomatie.vertrag_anbieten`
hatte in `src/main.py` keinen Aufrufer - der Pakt war nur ueber den Kern erreichbar. Jetzt gibt es je Bot
einen Knopf **"Pakt anbieten"** in der Diplomatie-Ansicht. Ob er erscheint, entscheidet
`diplomatie.pakt_anbietbar` mit derselben Pruefstelle, die der Kern beim Buchen nimmt (`_vertrag_bedingungen`);
in der Ansicht steht keine Grenze und keine Rechnung. Gebucht wird ausschliesslich im Kern, die Saetze
stehen in `data/diplomatie.json` (`vertraege._gruende`). Wache `tests/test_pakt_knopf.py` **43/0/0**.

**Sammellauf (00:41 bis 01:01): 196 von 198 gruen, 0 rot**, 8.235 Pruefungen, 60 Befunde, 1.168 s
(`docs/audits/sammellauf_20261108_0042.log`); die zwei nicht gruenen Dateien sind AUSGESETZT wie zuvor.
Der Baum wird mit diesem Block committet und gepusht.

**Als Naechstes in dieser Sitzung (Reihenfolge Daniels):** eine `.exe` aus diesem Stand bauen, eine
`.txt`-Spieltestanleitung mit Soll/Beobachtung/Note je Schritt auf den Desktop legen und einen vorbereiteten
Spielstand fuer die spaeten Wege (Wall, Handel, Portal, Vertrag) bereitstellen; danach Pruefungen haerter und
messbarer machen (Messwerte als JSON mit Zeitstempel), Schritt 12 (Sammellauf messen/parallelisieren),
Schritt 11 (AST-Quellwache), Schritt 13 (Daten-und-Quellen-Pruefung), R3-3, R3-4.

# STAND 07.11.2026, 21:30 - R3-2 gebaut: Ereignisart am Botnamen (Befund I-1), VOR Schritt 10

> Neuester Block. Darunter 21:05 (R3-1 Spieltag-Laenge, Register 297), 20:48 (Modellrunde 3
> geprueft, F-21 = A), 20:15 (B-2 Regelkreis, Register 296).

**R3-2 steht (Register 298).** Der sichtbarste Fehler der dritten Modellrunde ist weg: die
Ereignisart hing an der POSITION des Bots im Takt (`_arten[_index % len(_arten)]`), nicht an seinem
Namen. Mit der Dateireihenfolge haug/grom/silra und der Bot-Reihenfolge Haug, Brynhild, Grom, Silra,
Krank bekam Brynhild die Art `grom` - daher die Meldung "Brynhild: Grom braucht Messer"; Grom bekam
`silra`, Silra bekam `haug`, Krank bekam `grom`.

**Jetzt gilt:** `diplomatie.ereignis_art_fuer_bot(bot)` ist die EINE Zuordnungsstelle. Sie sucht die
Art, deren Feld `name` dem Botnamen entspricht (Rueckfall: der Schluessel selbst; Vergleich ohne
Gross-/Kleinschreibung und Leerraum). **Ein Bot ohne passende Art bekommt KEIN Ereignis** - Brynhild
und Krank haben keine, und es wird keine fremde erfunden.

**GEMESSEN (echter Verlauf, fuenf Bots, ein Takt nach drei Spieltagen):** genau drei Ereignisse
(Haug/Grom/Silra), Postfach: "Haug: Haug verlangt Tribut", "Grom: Grom braucht Messer",
"Silra: Silra verkauft eine Auskunft" - keine Meldung nennt einen fremden Bot.

**Wachen:** neu `tests/test_ereignis_zuordnung.py` (**36/0/0**), darunter die Gegenprobe (Brynhild an
Position 1 bekommt keine Art, obwohl die alte Rotation dort die dritte Art gewaehlt haette) und drei
Titelpruefungen gegen `data/story.json`. Die alte Wache "die Art rotiert ueber die Dateireihenfolge"
ist **umgedreht**: `tests/test_diplomatie_ereignisse.py` verlangt jetzt, dass die Index-Rotation NICHT
mehr vorkommt (**74/0/0**).

**Damit sind R3-1 und R3-2 erledigt.** Der naechste Schritt ist wieder der Ablauf: **Schritt 10**
(E2E-Ketten auf zwoelf Wegen, `tests/test_e2e_wege.py`, 12 Wachen), danach Schritt 11 (AST-Quellwache),
Schritt 12 (Sammellauf messen und beschleunigen), Schritt 13 (Schlusspruefung
`tests/test_daten_und_quellen.py`), danach R3-3 (C-6, I-10, C-4) und R3-4 (I-2).

Arbeitsweise unveraendert: Register, Protokollzeile, Stand-Block, Commit, Push und nach jedem Schnitt
ein VOLLER SAMMELLAUF mit dem Projekt-venv.

**Sammellauf nach R3-2 (21:31 bis 21:47): 194 von 196 gruen, 0 rot**, 8.062 Pruefungen, 60 Befunde, 929 s (`docs/audits/sammellauf_20261107_2133.log`); die zwei nicht gruenen Dateien sind AUSGESETZT wie zuvor. Commit `251e609`, gepusht, Kopf = Remote, Arbeitsbaum leer.

**Zwei Antworten Daniels (22:07, F-22 und F-23):** die Skill-Ergaenzung ist freigegeben und eingetragen (Teil 8 woertlich aus der Vormerkung, Teil 9 neu); die Diplomatiefristen bleiben in Spieltagen - die dreifache Echtzeit seit R3-1 ist gewollt. **Guthaben (Daniel 22:07): 7,00 USD / 62,99 USD** (0,23 USD fuer diese Sitzung). Nachtrag in `docs/FRAGEN_AN_DANIEL_20261107.md`.

**Dauerregel Uebergabe (Daniel 22:38):** das Archiv ist der Arbeitsort, der Desktop bekommt die fertige Fassung als LETZTEN Schritt; wird eine aufgelegte Fassung noch geaendert, verschwindet die Desktop-Kopie sofort. Anhang-Cache geraeumt (55 alte Kopien, 53 hashgleich verschoben, 2 abgelegt). **Guthaben (Daniel 22:38): 6,94 USD / 63,05 USD.** Wortlaut in `docs/FRAGEN_AN_DANIEL_20261107.md` (Nachtrag 22:40).

# STAND 07.11.2026, 21:05 - R3-1 gebaut: EINE Spieltag-Laenge (86.400 s), Befund A-1 behoben

> Neuester Block. Darunter 20:48 (Modellrunde 3 geprueft, F-21 = A), 20:15 (B-2 Regelkreis,
> Register 296), 19:45 (KI-Auftrag Runde 3).

**R3-1 steht (Register 297).** Der Befund der dritten Modellrunde war echt: `data/diplomatie.json`
fuehrte **28.800 s** je Spieltag, `src/botkern.py` und `src/punkte.py` rechneten **86.400 s** - die als
"zwei Spieltage" dokumentierte Frist von 57.600 s waren in Wahrheit **0,67 Tage**.

**Jetzt gibt es die Zahl EINMAL:** `src/zeitbasis.py` → `SEKUNDEN_JE_TAG = 86400` (24 Spielstunden zu
3.600 s; das Handbuch 2009 rechnet den Goetterschutz in Tagen und Er traege je Stunde). `botkern` und
`punkte` lesen sie, `diplomatie` liest sie, `main.py` und `spieloekonomie.py` rechnen ihre
Tagesanteile damit. `data/diplomatie.json` fuehrt **keine** eigene Tageslaenge mehr (Schluessel
`spieltag_sekunden` entfernt, neuer Erklaerschluessel `_tageslaenge`).

**Umrechnung erhaelt die TAGESZAHL, nicht die Sekundenzahl:**

| Groesse | vorher | jetzt |
|---|---|---|
| Frist eines Ereignisses (2 Tage) | 57.600 | **172.800** |
| Haeufigkeit (3 Tage) | 86.400 | **259.200** |
| Vorlauf Rache (1 Tag) | 28.800 | **86.400** |
| Zwangspause nach Paktende (1 Tag) | 28.800 | **86.400** |
| Vertragsdauer (3 Tage, alle drei Arten) | 86.400 | **259.200** |
| Postfach-Frist (1 Tag, `data/nachrichten.json`) | 28.800 | **86.400** |

**Die Wache ist neu und strenger als der Befund:** `tests/test_spieltag_eine_quelle.py` (**31
Pruefungen, 0 Fehler**) geht per `ast` ueber alle **63 Module** in `src/` und verlangt: keine eigene
Tageslaenge (erlaubt ist nur `= zeitbasis.SEKUNDEN_JE_TAG`), kein Literal **28.800** und kein Literal
**86.400** ausserhalb von `zeitbasis.py`; keine Datendatei fuehrt 28.800; jede Zeit in
`data/diplomatie.json` ist ein Vielfaches von 86.400; die Grenze ist gemessen (86.399 s = Tag 0,
86.400 s = Tag 1). **Gegenprobe gemacht:** eine absichtlich eingesetzte zweite Tageslaenge wird als
Fehler gemeldet. Beim ersten Lauf hat die Wache **drei weitere Stellen** gefunden, die eine eigene
Zahl trugen (`bot_futter_buchen`, `_spielzeit_text`, `_day_accum` in `main.py`, der
Nahrungsverbrauch in `spieloekonomie.py`) - alle umgestellt. `_rename_settlement` rechnet jetzt
ausdruecklich `24 * 3600` **ECHTE** Stunden: das ist Rechnerzeit, kein Spieltag.

**Vier Bestandswachen umgestellt und gruen:** `test_diplomatie_rache` 53/0/0,
`test_diplomatie_ereignisse` 74/0/0, `test_diplomatie_vertraege` 68/0/0, `test_bot_diplomatie`
67/0/0. Die Zeitkonstanten der Pruefdateien kommen jetzt aus `zeitbasis`, nicht aus einer
abgeschriebenen Zahl.

**Folge, die Daniel kennen muss:** bei Spieluhrfaktor 180 ist ein Spieltag **8 Echtminuten**. Pakt,
Ereignisfrist und Rachevorlauf wirken damit dreimal so lange in Echtzeit wie vorher (Frist 16 statt
5,3 Echtminuten, Haeufigkeit 24 statt 8). Die Werte bleiben VORSCHLAG - jede Zeile laesst sich einzeln
kuerzen, ohne dass wieder eine zweite Tageslaenge entsteht.

**Guthaben (Daniel abgelesen, 21:04):** 7,23 USD / 62,76 USD - unveraendert seit 20:45, diese Sitzung
arbeitet rein lokal.**Sammellauf nach R3-1 (21:09 bis 21:24): 193 von 195 gruen, 0 rot**, 8.026 Pruefungen, 60 Befunde, 939 s (`docs/audits/sammellauf_20261107_2108.log`); die zwei nicht gruenen Dateien sind AUSGESETZT wie zuvor, die neue Wache `test_spieltag_eine_quelle` lief mit 31/0/0 mit. Commit `12d22b1`, gepusht, Kopf = Remote, Arbeitsbaum leer.


**Naechster Schritt:** **R3-2** - die Ereignisart am Botnamen festmachen (`src/main.py:7251` rotiert
ueber `_index % len(_arten)`, Folge: "Brynhild: Grom braucht Messer"), Wache ergaenzen. Danach
Schritt 10 bis 13 des Ablaufs (E2E-Ketten, AST-Quellwache, Sammellauf messen, Schlusspruefung).
Arbeitsweise unveraendert: Register, Protokollzeile, Stand-Block, Commit, Push und nach jedem Schnitt
ein VOLLER SAMMELLAUF mit dem Projekt-venv.

# STAND 07.11.2026, 20:48 - Modellrunde 3 geprueft, sieben Befunde bestaetigt, F-21 = A

> Neuester Block. Darunter 20:15 (B-2 Regelkreis, Register 296), 19:45 (KI-Auftrag Runde 3),
> 18:20 (B-1 Sollkurve, Register 295).

**Die Antwort von Claude Sonnet 5.5 ist da - als Text, ohne Dateien.** Ihr Werkzeuglimit war vor dem
Schreiben erreicht; die Teile E, F und H bleiben unter dem Mindestumfang. Als Lieferung ist Runde 3
damit **nicht erfuellt**, als Befundsammlung brauchbar: sie sagt selbst, was sie nicht gelesen hat, und
markiert geschaetzte Zeilen mit \"ca.\". Ablage: `docs/extern/Claude_Sonnet_Antwort_Runde3_20261107.txt`
(SHA256 `2bff4e92d85b51ae`), Bewertung: `docs/audits/PRUEFVERMERK_CLAUDE_RUNDE3_20261107.md`.

**Selbst am Code nachgemessen und bestaetigt (sieben):** I-1 Ereignisart nach dem Bot-INDEX
(`src/main.py:7251`, Meldung nennt den Bot, Titel kommt aus der Art → \"Brynhild: Grom braucht
Messer\"); A-1 zwei Spieltag-Laengen (`data/diplomatie.json:66-68` nennt 28.800 s, `botkern` und
`punkte` rechnen 86.400 s - die \"Frist von zwei Spieltagen\" 57.600 s ist in Wahrheit 0,67 Tage);
I-3 Haug und Silra ohne Gegenleistung (Grom hat eine); C-4 je Drache zwei Einheitenangaben (20/20 gegen
120/60/24, welche zaehlt ist UNGEMESSEN); I-10 `story.ausgang_text` nur im Test; C-6 \"VORSCHLAG:\" in
einer Spielermeldung (`src/punkte.py:301`); G-1 Register 272/273 fehlen.
**Widerlegt als Fehler:** B-5 (Handelspunkte nicht in `gesamtpunkte`) - im Code ausdruecklich als
Abweichung der 2009er Fassung begruendet.

**Zwei Aussagen der Antwort sind zu berichtigen:** Schritt 9 war beim Schreiben laengst gebaut
(`91a6525`), und ihr \"spielbar UNBEKANNT\" beschreibt die Sandbox ohne tkinter, nicht das Projekt (der
Sammellauf lief hier 20:18 mit 192/194 gruen).

**F-21 = A (Daniel 20:50):** R3-1 (A-1 Spieltag-Definition, 60 min) und R3-2 (I-1
Ereignis-Zuordnung, 30 min) laufen VOR Schritt 10, danach der Ablauf, danach R3-3 (C-6, I-10, C-4)
und R3-4 (I-2).

**Naechster Schritt:** **R3-1** - die Spieltag-Definition vereinheitlichen (86.400 s), die
Diplomatie-Zahlen in `data/diplomatie.json` umrechnen (Frist, Vorlauf, Pakt, Rachetopf) und eine Wache
bauen, die keine zweite Tageslaenge mehr zulaesst. Danach R3-2, dann Schritt 10 bis 13 des Ablaufs.
Arbeitsweise unveraendert: Register, Protokollzeile, Stand-Block, Commit, Push und nach jedem Schnitt
ein VOLLER SAMMELLAUF mit dem Projekt-venv.

# STAND 07.11.2026, 20:15 - B-2 Regelkreis gebaut (Register 296), erster A/B-Lauf abgelehnt

> Neuester Block. Darunter 19:45 (KI-Auftrag Runde 3, Schritt L), 18:20 (B-1 Sollkurve,
> Register 295), 17:45 (F-14 = B, Register 294).

**Schritt 9 des Ablaufs steht.** `tools/balance_kreis.py` hat jetzt vier Schritte, jeden einzeln:

- `--messung` - zehn Laeufe mit den Startwerten 1..10, zwoelf Spieltage, Stil breit. Laeuft in einem
  EIGENEN Prozess: `spieldaten` bindet die Projektwurzel beim Import, und `gelaende`,
  `gebaeude_wirkung` und `berater` halten sie als Modulkonstante - ein Umbiegen im laufenden Prozess
  waere eine halbe Sache.
- `--vorschlag` - HOECHSTENS ein Datenwert. Die Groesse mit dem groessten Fehlbetrag, dort das
  Gebaeude mit dem groessten Baugewicht, Schrittweite aus der Datei. BELEGT-Werte (Holzfaeller,
  Steinmetz, Jaeger, Haus) sind nie Kandidat.
- `--ab` - dieselben Startwerte mit und ohne Aenderung. Die Aenderung lebt nur in einer Kopie von
  `src/` und `data/`; `data/` des Projekts bleibt hashgleich (im Test belegt).
- `--urteil` - 20 Prozent Verbesserung der Zielabweichung, keine andere Groesse schlechter, erstes
  Gefecht nicht spaeter; schreibt `docs/balancing/URTEIL_<n>.md` fortlaufend.

Die drei Schwellen stehen in `data/regelkreis.json` (F-17 = A), nicht im Code - belegt: mit 5 statt
20 Prozent wird dasselbe A/B angenommen. Der Feedback-Eingang ist da (`docs/feedback/VORLAGE.md` mit
Was/Wann/Stand/Zahl/Gefuehl 1-5, `MELDUNGEN.json`, `--feedback` schreibt `BUENDEL.md`); ab drei
gleichen Schluesseln wird daraus ein Messauftrag.

**Erster vollstaendiger Durchlauf (26 s, protokolliert):** 3,500 Punkte je Spieltag gegen das Ziel
3,3 = 6,06 Prozent Abweichung. Alle vier Korridorgroessen liegen UNTER dem Band (Holz 0,8368,
Stein 0,7432, Nahrung 0,5216, Gold 0,5827). Vorschlag: kriegerakademie/holz 32 -> 29 (9,38 Prozent).
Im A/B bleibt die Zielabweichung bei 6,06 Prozent, Holz und Stein werden minimal schlechter
(0,8379 und 0,7438), das erste Gefecht liegt auf Tag 2,0 - **Urteil ABGELEHNT**, drei Gruende
benannt, `docs/balancing/URTEIL_1.md`.

**Befund fuer Daniel (kein Fehler des Schnitts):** eine einzelne Preisveraenderung von 10 Prozent
bewegt die Kennzahl nicht. Der Abstand zur Sollkurve kommt aus der SPIELERPOLITIK - der Automat
gibt Gold und Holz fuer Armee und Forschung aus, der Idealplan der Kurve gibt nichts aus und haeuft
deshalb das Vielfache an. Nach F-16 = A bleibt die Kurve Obergrenze, und das Urteil vergleicht nur
die VERAENDERUNG; genau so ist es gebaut. Die Frage, ob der Korridor absolut etwas aussagen soll,
ist damit nicht neu gestellt, sondern beantwortet.

**Wachen:** `tests/test_balance_urteil.py` 44/0/0 (die fuenf geforderten Faelle A bis E plus
Schwellen aus der Datei, BELEGT-Schutz, kein Schreiben in `data/`, Nummerierung der Urteilsdatei),
`tests/test_balance_kreis.py` 30/0/0 - dort ist Wache C umgedreht (Entscheidung im Docstring
genannt): B-2 LIEST `src/` jetzt, verlangt ist deshalb "keine Schreibstelle unter `src/`" per `ast`.

**Sammellauf nach diesem Schnitt: 0 rot.** 192 von 194 gruen (zwei `AUSGESETZT`), **7.995
Pruefungen, 0 Fehler, 60 Befunde, 1.003 s** (`docs/audits/sammellauf_20261107_2018.log`); die neuen
Wachen stehen mit 44/0/0 und 30/0/0 darin. Gepusht: `91a6525`, Remote gleich.

**Antworten 20:45:** Guthaben **7,23 USD / 62,76 USD** (Ablesung Daniel). **F-20 = B** - die
Vorschlagsquelle des Regelkreises wird erweitert, damit auch Schwellen der Spielerpolitik vorgeschlagen
werden duerfen; das ist ein EIGENER kommender Schnitt und nicht nebenbei gebaut, weil die Politik heute
im Code von `tools/spieltest_simulation.py` steht (`GEBAEUDE_REIHENFOLGE`, `STILE`,
`FORSCHUNGSZIELE`, `SCHRITT`) und erst als Datendatei (`data/spieltest_politik.json`) existieren muss.
B-2 bleibt bis dahin unveraendert - die Ablehnung war ein echtes Ergebnis.

**Naechster Schritt:** Schritt 10 des Ablaufs (A-1 E2E-Ketten auf zwoelf Wege erweitern, Vorlage
`tests/test_produktionskette_ohne_cheats.py`), danach 11 bis 13. Arbeitsweise unveraendert:
Register, Protokollzeile, Stand-Block, Commit, Push und nach jedem Schnitt ein VOLLER SAMMELLAUF
mit dem Projekt-venv. Kein Release vor S4 komplett (F-9); S5 gesperrt.

# STAND 07.11.2026, 19:45 - KI-Auftrag Runde 3 fuer Claude Sonnet 5.5 fertig (Schritt L)

> Neuester Block. Darunter 18:20 (B-1 Sollkurve, Register 295), 17:45 (F-14 = B, Register 294),
> 15:07 (Bot-Luecken S4-7, Register 293).

**Schritt L ist erledigt, vor den Schritten 9 bis 13** (seine Abhaengigkeit ist Schritt 3, der steht).
Der Auftrag fuer **Claude Sonnet 5.5** ist geschrieben: `docs/extern/Nebelseetal_LLM_Auftrag_Runde3_20261107.md`
(23.365 Byte, SHA256 `1d60b87cca014f8f`), Entwurf von `deepseek-v4-pro` (zwei Aufrufe), von mir geprueft
und um zwei Stuecke ergaenzt, die Daniel ausdruecklich verlangt hat:

- **Abschnitt 2a "Kritik-Auftrag":** der Lauf dient der Kritik, nicht der Bestaetigung; jeder Befund
  braucht einen Beleg, Vermutungen werden als solche gekennzeichnet, unbequeme Punkte sind erwuenscht.
- **Teil I "Geschichte, Logik und innere Stimmigkeit"** mit zehn Unterfragen - Chronik gegen
  Spielmechanik, Motive der vier Bots, Rolle der drei Drachen, Belohnungen ohne Begruendung,
  Zahlenlogik, schwache Texte, echte Entscheidungen mit Gewicht, Leerlauf und Sackgassen, Ton der
  Textsorten. Dazu Teil B (Mechanik gegen das Original) und C (Code) unveraendert im Lieferumfang.

**Paket auf dem Desktop:** `D:\Desktop\Nebelseetal_Paket_Runde3_20261107\` - sechs ZIPs
(01 Auftrag/Stand/Ablauf, 02 Code, 03 Daten, 04 Tests und Werkzeuge, 05 Konzept und Story,
06 Original-Handbuch), zusammen 2,80 MB, jedes unter der 8-MB-Grenze und mit `testzip` geprueft.

**Erweitert um 19:52:** das Dokument war kuerzer als die Fassung aus Runde 2 (23.365 gegen 34.065
Byte). Deshalb sind **Teil J (Spielgefuehl, Langzeitmotivation, Wiederspielwert, zehn Unterfragen)**
und ein **verbindlicher Mindestumfang** dazugekommen: je Teil mindestens acht befundete Punkte,
zusammen sechzig, je Punkt Beleg und Urteil, Rangliste je Teil, Selbstpruefung mit Liste der
unsicheren Befunde. Dokument jetzt **25.450 Byte**, SHA256 `558e66250e9eb5ca`; Paket 01 neu gebaut.

**Meldepflicht erfuellt:** Daniel ist auf den Entwurf und den Ordner ausdruecklich hingewiesen
(Absprache aus dem Ablauf, Abschnitt L).

**Naechster Schritt:** Schritt 9 des Ablaufs (B-2 Regelkreis) mit F-17 = A (20 Prozent Verbesserung,
10 Prozent Schrittweite, 3 gleiche Meldungen). F-16 = A: die Sollkurve bleibt Obergrenze, B-2
vergleicht nur Veraenderungen.

# STAND 07.11.2026, 18:20 - B-1 Sollkurve aus den Daten gebaut (Register 295)

> Neuester Block. Register 295. Darunter 294 (Drachen-Anzeige F-14 = B), 293 (Bot-Luecken S4-7),
> 292 (Handel in der Spielschicht), 291 (Verkaufsmaske).

**Schritt 8 des Ablaufs steht.** `tools/balance_kreis.py --sollkurve` spielt die BELEGTE Kette
(Holzfäller, Steinmetz, Bibliothek, danach im Kreis Farm/Goldmine, Haus bei Siedlernot) auf den
Geländefeldern der belegten Startkarte `original-036` Tag für Tag nach und schreibt daraus
`data/sollkurve.json`: je Spieltag Holz, Stein, Nahrung, Gold, Siedler und Gebäude als
`{ideal, unten, oben}` mit unten = Ideal × 0,7 und oben = Ideal × 1,1 (VORSCHLAG). Der Kopf trägt
`erzeugt_aus` mit sechs SHA256 - eine veraltete Kurve fällt damit sofort auf. Das Punkte-Ziel 3,3 je
Spieltag steht mit Quelle (V-3) in der Datei.

**Gemessen:** zwei Läufe sind zeichengleich; Holz +10 Prozent in einer Kopie der Datendatei hebt den
Holzkorridor (Tag 10) und lässt Stein unberührt; das Werkzeug schreibt nur `data/sollkurve.json`.
Wache `tests/test_balance_kreis.py` **29 Prüfungen, 0 Fehler**.

**Ein Fehler auf dem Weg:** die Gebäudenamen tragen in den Daten Umlaute (`Holzfäller`, `Jäger`), der
Plan rechnete mit `holzfaeller` - der Ertrag wurde nicht gefunden und Holz wuchs einen ganzen Spieltag
um 0 (stille Null, keine Meldung). Behoben über `_normal()` (Umlaute umschreiben, beide Seiten).

**Zwei benannte Lücken statt erfundener Zahlen:** die FORSCHUNGSKOSTEN stehen nicht in
`data/research.json` (nur Voraussetzungen) - Baukunst gilt deshalb ab dem Tag nach der Bibliothek als
erforscht, ausdrücklich als Annahme; und auf Berg/Hügel sind die Felder früh belegt, weitere Minen
finden keinen Platz (steht als Lücke in der Datei).

**Sammellauf:** 191 von 193 gruen, 0 rot, **7.949 bestandene Pruefungen, 60 Befunde, 955 s** (`docs/audits/sammellauf_20261107_1837.log`). Der Lauf davor war rot (66/1 in `test_bot_diplomatie.py`): der Verlauf wuerfelte ohne Saat, der Angriff blieb aus - behoben in der Pruefdatei (feste Saat, zehn Takte), drei Einzellaeufe danach 67/0/0 (Commit `5232137`).

**Grenze der Kurve:** sie ist eine OBERGRENZE aus den Daten (jedes Gebäude sofort baubar), kein
Erfahrungswert aus echten Partien. Ob sie gedrosselt werden soll (z. B. ein Gebäude je Spieltag), ist
**Frage F-16**.

**Nächster Schritt:** Schritt 9 des Ablaufs (B-2 Regelkreis: messen, vorschlagen, A/B, Urteil,
Feedback-Bundel), danach 10 bis 13.

# STAND 07.11.2026, 17:45 - Drachen-Bedrohung als Anzeige (F-14 = B), Antworten der Fragenrunde (Register 294)

> Neuester Block. Register 294. Darunter 293 (Bot-Luecken S4-7), 292 (Handel in der Spielschicht),
> 291 (Verkaufsmaske), 290 (Verkaufsrichtung im Kern).

**Daniels Antworten vom 07.11.2026, 17:40 sind eingearbeitet.** F-13 = A (Schwellenpreis bleibt
300 Gold), F-14 = B (Drachen nur melden, nicht meiden), F-15 = A (Reaktionsstufen bleiben). Zwei der
drei Antworten bestaetigen den dokumentierten Stand und aendern keine Datei; F-14 = B ist gebaut.

**Was F-14 = B geworden ist:** `drachen.bedrohung(ort, besiegt, pfad)` nennt den NAECHSTEN offenen
Drachen seiner Welt mit Manhattan-Abstand und einem Satz aus `data/drachen.json`. Reichweite 5 Felder
(aus der Datei), darueber hinaus schweigt die Meldung; auf dem eigenen Feld gilt ein eigener Satz
statt "0 Felder". Der Bot haengt den Satz an seine Meldung "kein Drachenangriff - ..." an. **Es gibt
KEINE Meidung:** weder Gruendung noch Marsch weichen Drachenfeldern aus, und die Funktion bucht
nichts - das ist als Wache im Quelltext festgehalten.

**Gemessen:** `tests/test_bot_diplomatie.py` jetzt **67 Pruefungen, 0 Fehler** (Abschnitt I neu);
Nachbarwachen gruen (`test_drachen` 88/0/0, `test_drachen_einhaengung` 96/0/0,
`test_drachen_zweite_phase` 22/0/1, `test_drachenschuppe` 32/0/0, `test_bottaktik` 48/0/0).

**Sammellauf:** 190 von 192 gruen, 0 rot, **7.919 bestandene Pruefungen, 60 Befunde, 954 s** (`docs/audits/sammellauf_20261107_1747.log`); die zwei nicht gruenen Dateien sind `AUSGESETZT`.

**Guthaben (Daniel 17:40):** 7,51 USD, Gesamtverbrauch 62,48 USD - 0,75 USD fuer S4-6c, S4-7 und die
zwei Sammellaeufe dieser Sitzung.

**Naechster Schritt:** Schritt 8 des Ablaufs (B-1 Sollkurve aus den Daten), danach 9 bis 13.
Arbeitsweise unveraendert: je Schnitt Register, Protokollzeile, Stand-Block, Commit, Push und ein
voller Sammellauf.

# STAND 07.11.2026, 15:07 - Bot-Luecken: Spaehung vor dem Raubzug, Reaktionsstufe der Bots (Register 293)

> Neuester Block. Register 293. Darunter 292 (Handel in der Spielschicht), 291 (Verkaufsmaske),
> 290 (Verkaufsrichtung im Kern), 289 (Befund G-8), 288 (Ereignisse).

**Schritt 7 des Ablaufs ist gebaut.** Zwei der drei Luecken waren offen, eine war es nicht:

1. **Spionage (neu):** `GameState._bots_spaehung` schickt die Kundschafter eines Bots gegen das
   geplante Ziel. Der Wall wird mit DERSELBEN Vorpruefung gemessen wie beim Spieler
   (`spionage.abwehr_pruefung`), die Aufklaerung kommt aus `spionage.aufklaerungswert` (SI+HE), eine
   abgewehrte Truppe verliert Einheiten ueber `spionage.verlust_der_truppe`. Gebucht wird GENAU EINE
   Spaehung je Dorf: Daniel hat am 02.11.2026 entschieden, dass ein Bericht NICHT alt wird - er gilt,
   bis ein neuer Bericht ueber dasselbe Dorf kommt. Ohne Bericht kostet die Spaehung den Zug; im
   naechsten Takt greift der Bot an. Die drei Gates (Demo-Regel, Goetterschutz, Pakt) sind an der
   Aufrufstelle bereits geprueft und gelten damit auch fuer die Spaehung.
2. **Reaktion (neu):** jeder Bot hat eine Bereitschaft aus seiner Taktik
   (`data/bot_diplomatie.json`: Pluenderer 1,2 / Waechterin 0,8 / Bastionier 0,8 / Spaeherin 1,0).
   Sie TEILT die vorhandenen Raubzug-Schwellen (`armee_schwelle`, `staerke_faktor` aus
   `data/bot_raubzug.json`) - gierig raubt frueher, vorsichtig spaeter. Liegt der Spieler um
   mindestens 50 Prozent vorn, wird jeder Bot vorsichtiger (Faktor x 0,9). Keine neue Regel, keine
   zweite Punkteformel (die Wache von S-7 prueft das).
3. **Drache (nicht neu):** das Drachen-Urteil der Bots gibt es seit W-14 (`drachen.bot_entscheidung`,
   `main._bots_drachenzug`, `data/drachen.json` Block `bots`, eigene Wache). Eine zweite Funktion
   `drachen.bedrohung(ort)` waere die zweite Wahrheit fuer dieselbe Frage und wurde deshalb NICHT
   gebaut - Frage F-14 an Daniel.

**Gemessen:** Wache `tests/test_bot_diplomatie.py` **51 Pruefungen, 0 Fehler**; echter Verlauf in der
App (Siedlung gruenden, Bot mit 40 Kriegern und 3 Kundschaftern, sechs Takte): Takt 1 spaeht genau
einmal, der Bericht steht danach in `bot.aufklaerung` UND im Kern-Stand, der naechste Angriff folgt,
eine zweite Spaehung findet nicht statt. Ein Fehler auf dem Weg: der Bericht wurde zuerst nur am Bot
geschrieben und im selben Takt von `bot_aus_dict` ueberschrieben - der Bot spaehte in JEDEM Takt
erneut. Behoben ueber den Kern-Stand (`start["aufklaerung"]`).

**Sammellauf:** 190 von 192 gruen, 0 rot, **7.903 bestandene Pruefungen, 60 Befunde, 938 s** (`docs/audits/sammellauf_20261107_1510.log`); die zwei nicht gruenen Dateien sind `AUSGESETZT` (dokumentiert zurueckgezogen). Der Lauf lief allein.

**Offene Fragen (F-14, F-15 in `docs/FRAGEN_AN_DANIEL_20261107.md`):** soll zusaetzlich ein
Meidungs-Urteil gegen den Drachen gebaut werden (F-14), und sind die Reaktionsstufen 0,8/1,0/1,2 als
VORSCHLAG richtig (F-15)?

**Naechster Schritt:** Schritt 8 des Ablaufs (B-1 Sollkurve aus den Daten), danach 9 bis 13.
Arbeitsweise unveraendert: je Schnitt Register, Protokollzeile, Stand-Block, Commit, Push und ein
voller Sammellauf.

# STAND 07.11.2026, 12:10 - Handel in der Spielschicht gebaut, Kennzahlenblatt zeigt eine Zahl (Register 292)

> Neuester Block. Register 292. Darunter 291 (Verkaufsmaske), 290 (Verkaufsrichtung im Kern),
> 289 (Befund G-8), 288 (Ereignisse), 287 (Startbilder), 286 (Rachetopf), 285 (S4-3).

**Schritt 6 ist komplett.** Die Messschicht (`src/spielschicht.py`) hat jetzt einen Handelsweg:
`verkauf_an_haendler` verkauft den Ueberschuss eines Rohstoffs an einen fremden Haendler. Alles ueber
den Kern - `spieloekonomie.handel_start` mit `karawane_seite="verkaeufer"`, danach
`spieloekonomie.handel_abschluss` fuer Ankunft und Rueckkehr -, der Preis aus `botkern.handelspreis`.
Gebucht werden `handels_erloes` und `letzter_handel` genau einmal je Vertrag.

**Gemessen, nicht behauptet:** eine Wache mit 34 Pruefungen (`tests/test_handel_spielschicht.py`,
**34/0/0**) belegt Buchung, Ladewache fuer alte Staende, Ablehnungen, fehlende Doppelbuchung und dass
die Schwelle der Messschicht die Schwelle des Spiels ist. Zehn Laeufe (5 Startwerte x 2 Stile) ueber
20 Spieltage: **10 von 10 zeigen `handelspunkte` 95,0** - das Fertig-Kriterium des Ablaufs ist damit
erfuellt. Ueber 12 Spieltage sind es **0 von 10**: die Handelskarawane kostet 500 Holz und 15 Pferde
und entsteht erst um Spieltag 17. Das ist kein Fehler, sondern die Dauer der Kette.

**Sammellauf:** 189 von 191 gruen, 0 rot, 7.851 bestandene Pruefungen, 60 Befunde, 1.214 s (`docs/audits/sammellauf_20261107_1216.log`).

**Zwei Sachen, die dabei sauber geworden sind:** der Beschaffungswert des Handelspreises steht jetzt
in `botkern.BESCHAFFUNGSKOSTEN`, `main.py` liest ihn von dort - App und Messschicht fuehren keine
zwei Zahlen mehr. Und die Regeln der Messschicht (Gold des Partners, Mindestvorrat, Abstand) stehen
in `data/handelsmessung.json` statt im Code.

**Offene Frage an Daniel (F-13, `docs/FRAGEN_AN_DANIEL_20261107.md`):** die Preisfunktion belegt jede
Einheit Rohstoff mit 300 Gold. Ein einziger Handel bringt damit 95 Handelspunkte - mehr als der ganze
uebrige Lauf (42 Gesamtpunkte). Das ist eine Balance-Frage, keine Rechenfrage; der Wert bleibt
zunaechst, wie er ist.

**Naechster Schritt:** Schritt 7 des Ablaufs (Bot-Luecken: Drache, Spionage, Reaktion), danach 8 bis
13. Arbeitsweise unveraendert: je Schnitt Register, Protokollzeile, Stand-Block, Commit, Push und ein
voller Sammellauf.

# STAND 07.11.2026, 01:35 - Verkauf steht in der Oberflaeche, Kennzahl fehlt noch (Register 291)

> Neuester Block. Register 291. Darunter 290 (Verkaufsrichtung im Kern), 289 (Befund G-8),
> 288 (Ereignisse), 287 (Startbilder), 286 (Rachetopf), 285 (S4-3), 280 (Kennzahlenblatt).

**Der Verkauf ist jetzt bedienbar.** In der Handelsmaske (Doppelklick auf einen Bot) steht unter
`Kaufvertrag schicken` der Knopf `Verkauf anbieten (eigene Ware)`. Er oeffnet die Verkaufsmaske:
Ware aus dem ORTSLAGER, Gold des Bots, Schwellenpreis (bis dahin nimmt der Bot an), eigene
Handelskarawane, Ladeplaetze. Ohne Ware oder ohne Karawane ist der Knopf gesperrt - gesperrt heisst
hier: es gibt nichts anzubieten, nicht: es fehlt eine Pruefung.

**Gemessen (Abschnitt G der Wache):** `_verkauf_ausfuehren` startet den Vertrag ohne Fenster,
`richtung` steht auf `verkauf`, und der Erloes wird bei der Rueckkehr gebucht (10 Holz zu 1 Gold ->
Erloes 10, Zaehler 250 -> 260). Wache insgesamt **37 Pruefungen, 0 Fehler**.

**Sammellauf:** 188 von 190 gruen, 0 rot, 7.816 Pruefungen, 953 s (`docs/audits/sammellauf_20261107_0017.log`).

**Was noch fehlt - 6c, und das ist eine echte Luecke:** `src/spielschicht.py` (die Schicht, die das
Kennzahlenblatt faehrt) hat keinen Handel und keine Bots. `handelspunkte` bleibt dort `null`, damit ist
das Fertig-Kriterium des Ablaufs (groesser 0 in einem von zehn Laeufen) NICHT erfuellt. Vorschlag fuer
den naechsten Schnitt, ohne neue Preisfunktion: die Spielschicht verkauft einen Ueberschuss an einen
fremden Haendler ueber DENSELBEN Kern (`spieloekonomie.handel_start` mit `karawane_seite="verkaeufer"`
und `handel_abschluss`), der Preis kommt aus `botkern.handelspreis` - also die Schwelle, die das Spiel
schon benutzt. Dann schreibt die Spielschicht `handels_erloes` und `letzter_handel` in ihren Zustand,
und das Kennzahlenblatt zeigt eine echte Zahl statt `null`.

**Naechster Schritt:** 6c bauen (Spielschicht-Handel), danach Schritt 7 (Bot-Luecken) und 8 bis 13.
Arbeitsweise unveraendert: je Schnitt Register, Protokollzeile, Stand-Block, Commit, Push und ein
VOLLER Sammellauf.

Offen ausserdem: die Buendelung der Besucherdokumente nach `BESUCHER.md` (Daniels Entscheidung 14:00,
Punkt 4) und die Frage F-11 (Motive der Spielansichten).

---

# STAND 07.11.2026, 00:35 - Verkaufsrichtung gebaut: der Spieler verkauft an Bots, der Erloes wird gebucht (Register 290)

> Neuester Block. Register 290. Darunter 289 (Befund G-8), 288 (Ereignisse), 287 (Startbilder),
> 286 (Rachetopf), 285 (S4-3 verdrahtet), 281 bis 283 (Runde 2, Spielkonzept, Repo geordnet),
> 280 (Kennzahlenblatt), 267 bis 279 (Abgleich, fixer Ablauf, S4 Teil 1).

**Daniel hat F-12 mit A beantwortet (00:05): Verkaufsrichtung bauen.** Damit ist der Handelsweg
erstmals EINNAHMESEITIG: der Spieler verkauft eigene Ware an einen Bot, der Bot zahlt aus seinem Gold,
und die Karre des SPIELERS faehrt - so steht es in der Vorversion 2006.

**Was gebaut ist:**

- **Kern (`spieloekonomie.handel_start`) bekommt `karawane_seite`** (Standard `kaeufer` = der
  bisherige Kaufweg, unveraendert). Beim Verkauf steht die Karawane beim Verkaeufer, die Mission
  startet dort und die Karre kehrt dorthin zurueck; die Seite steht im Vertrag und damit im Spielstand.
- **`GameState.verkauf_an_bot`** spiegelt `handel_mit_bot`: Ware aus dem ORTSLAGER, Deckung beim Bot
  (Gold), Handelskarawanen-Pflicht, Rueckladung - abgelehnt wird VOR jeder Buchung.
- **EINE Buchstelle** in `_fremdvertrag_buchen`: bei `abgerechnet_jetzt` und Richtung `verkauf` wird
  `handels_erloes += erloes` gebucht und `letzter_handel` auf den Zeitpunkt der Annahme gesetzt. Der
  KAUF bucht nichts - laut Quelle gibt es Punkte nur fuer eingenommenes Gold.
- **Felder additiv** in Speichern und Laden; ein alter Stand laedt mit 0.0.
- **Anzeige** uebergibt `gold_erloes`, `letzter_handel` (bei 0.0 als `None`, sonst verfaellt der Punkt
  ab Spielzeit 0) und `jetzt` an `punkte.auszeichnungen`.

**Zwei Fehler, die der Verlauf gefunden hat (beide behoben):**

1. `_fremdvertrag_buchen` suchte den Bot immer auf der VERKAEUFERSEITE und legte seinen Ort unter
   diesem Schluessel ab. Beim Verkauf ist der Bot der Kaeufer - sein Ortsdict ueberschrieb damit das
   Lager des Spielerorts, und der Vertrag wurde nie abgerechnet. Jetzt entscheidet die Vertragsrichtung
   ueber die Seite (Bot-Suche UND Ortsdict).
2. Die Anzeige las `werte.get('Händler')`, `punkte.auszeichnungen` liefert aber `Haendler` (ASCII):
   der Haendler-Wert war IMMER 0, auch mit gefuelltem Zaehler. Gefunden von der neuen Wache.

**Wache:** `tests/test_handelspunkte.py` **31 Pruefungen, 0 Fehler, 0 Befunde** - 100 Gold = 1.0 Punkt,
20 Gold = 0.2, Verfall 1 je 24 Spielstunden und nicht unter 0, echter Verkauf mit Erloes 100 und
1.0 Punkten, Karre kehrt zurueck, kein Nachbuchen bei weiterem Takt oder nach Speichern/Laden, alter
Stand ohne Feld laedt mit 0.0, Anzeige = Kern, Kauf bucht nichts.

**Sammellauf:** 188 von 190 gruen, 0 rot, 7.810 Pruefungen, 865 s (`docs/audits/sammellauf_20261106_2348.log`).

**Offen aus Schritt 6 (bewusst nicht in diesem Takt):**

1. **Der Knopf in der Handelsmaske** - der Verkauf ist bisher nur ueber `GameState.verkauf_an_bot`
   erreichbar, nicht ueber die Oberflaeche. Ohne ihn kann Daniel nicht verkaufen.
2. **6c: Handel in der Spielschicht** - `src/spielschicht.py` hat weder Handel noch Bots, das
   Kennzahlenblatt zeigt `handelspunkte` deshalb weiter `null`. Das Fertig-Kriterium des Ablaufs
   (groesser 0 in einem von zehn Laeufen) ist damit noch NICHT erfuellt.

**Naechster Schritt:** 6b abschliessen (Maske) und 6c bauen, dann Schritt 7 (Bot-Luecken) und 8 bis 13.
Arbeitsweise unveraendert: je Schnitt Register, Protokollzeile, Stand-Block, Commit, Push und ein
VOLLER Sammellauf.

Offen ausserdem: die Buendelung der Besucherdokumente nach `BESUCHER.md` (Daniels Entscheidung 14:00,
Punkt 4) und die Frage F-11 (Motive der Spielansichten).

---

# STAND 06.11.2026, 23:50 - Schritt 6 gemessen: der Erloes gehoert dem Verkaeufer, der Spieler kauft (Register 289, Frage F-12)

> Neuester Block. Register 289 (Befund, kein Code). Darunter 288 (Ereignisse Haug/Grom/Silra),
> 287 (Startbilder), 286 (Rachetopf), 285 (S4-3 verdrahtet), 281 bis 283 (Runde 2, Spielkonzept,
> Repo geordnet), 280 (Kennzahlenblatt), 267 bis 279 (Abgleich, fixer Ablauf, S4 Teil 1).

**Der Ablauf fuer Schritt 6 traegt nicht.** Er sieht vor, beim Abschluss eines Handelsvertrags
`vertrag erloes` auf einen Zaehler `handels_erloes` zu addieren. Am heutigen Code gemessen ist
`erloes` aber die Einnahme des **Verkaeufers**, und Verkaeufer ist der BOT: `GameState.handel_mit_bot`
uebergibt `asdict(quelle)` als Kaeufer an `spieloekonomie.handel_start`. Ein Kauf von 1 Holz zu
301 Gold bucht am Ort **minus 301 Gold** und beim Bot **plus 301 Gold**, `erloes` steht auf 301.0.
Die vorgesehene Buchung haette dem Spieler also Punkte fuer **ausgegebenes** Gold gegeben.

**Die Quelle verlangt das Gegenteil.** `docs/original/Spielanleitung_2005/punktesystem.php.txt`
Zeilen 34 bis 47: Handelspunkte gibt es fuer Gold, das man **durch Verkauf erwirtschaftet**
(100 Schwerter fuer 300 Gold = 3 Punkte). Fuer gekaufte Ware nennt sie nichts.

**Drei Messungen, alle am 06.11.2026 zwischen 23:35 und 23:45 mit dem Projekt-venv:**

- **Der Kauf bucht wie beschrieben:** Ort minus 301 Gold, Bot plus 301 Gold, `erloes` 301.0,
  `angenommen` und `abgerechnet` je genau einmal.
- **Die Gegenrichtung lehnt der Kern ab:** `ValueError: Karawane fehlt vor Ort`, weil `bot_als_ort`
  `einheiten: {}` setzt und `handel_start` die Karawane beim Kaeufer verlangt. Gibt man dem Bot
  seinen Wagenpark (`bot.lager`, ein bis zwei Karren je Bot) als `einheiten`, nimmt der Kern die
  Gegenrichtung an - es fehlen nur die Datenfuellung und eine Kauf-Entscheidung des Bots.
- **Das Kennzahlenblatt kann die Zahl nicht zeigen:** `tools/spieltest_simulation.py` faehrt
  `spielschicht.neuer_zustand`, und `src/spielschicht.py` (739 Zeilen) hat weder Handel noch Bots.
  `handelspunkte` bliebe dort `null`, auch mit richtiger Buchung.

**Nicht gebaut, bewusst:** keine Zeile Code fuer Schritt 6. Die Richtung ist eine Mechanik-Entscheidung
und liegt bei Daniel (Frage **F-12** in `docs/FRAGEN_AN_DANIEL_20261107.md`, drei Wege mit Folge und
Empfehlung: A Verkaufsrichtung bauen, B Umsatz bepunkten als bewusste Abweichung, C zurueckstellen
und mit Schritt 7 weitermachen).

**Belege:** Register 289 in `docs/PRUEFREGEL_ORIGINAL.md`; Protokollzeile 23:45 in
`docs/ENTWICKLUNGSPROTOKOLL.md`; Messkripte `messung_handelspunkte.py` und
`messung_handelspunkte2.py` im Hermes-Scratch (`%LOCALAPPDATA%\hermes\cache\scratch\`).

**Dokumentpruefungen vor dem Commit:** `test_textqualitaet` 441/0 (133 Dokumente), `test_protokoll`
28/0/1, `test_projektpfade` 129/0, `test_zieluebergabe` 26/0/0, `test_gpt_projektordnung_20261028`
5 OK, `test_anzeigetexte_umlaute` 49/0/0. Kein Sammellauf: es wurde kein Code geaendert - der
gehoert zum naechsten echten Schnitt.

**Naechster Schritt:** die Antwort auf F-12 abwarten (eine Runde, sofort gestellt, weil die Arbeit
dort blockiert). Bei A: 6a Felder `handels_erloes`/`letzter_handel` samt Speichern/Laden und Anzeige
(`punkte.auszeichnungen` mit `gold_erloes`, `letzter_handel` - bei 0.0 als `None`, sonst verfaellt
der Punkt ab Spielzeit 0), 6b Verkaufsrichtung im Kern, 6c Handels-Schritt in der Spielschicht.
Danach Schritt 7 (Bot-Luecken) und 8 bis 13. Arbeitsweise unveraendert: je Schnitt Register,
Protokollzeile, Stand-Block, Commit, Push und ein VOLLER Sammellauf.

Offen ausserdem: die Buendelung der Besucherdokumente nach `BESUCHER.md` (Daniels Entscheidung 14:00,
Punkt 4) und die Frage F-11 (Motive der Spielansichten).

---

# STAND 06.11.2026, 17:55 - Ablauf Schritt 5 fertig: Ereignisse Haug, Grom, Silra (Register 288)

> Neuester Block. Register 288. Darunter 287 (Startbilder), 286 (Rachetopf), 285 (S4-3 verdrahtet),
> 281 bis 283 (Runde 2, Spielkonzept, Repo geordnet), 280 (Kennzahlenblatt), 267 bis 279 (Abgleich,
> fixer Ablauf, S4 Teil 1, F-1 bis F-9).

**Die Nachbarn melden sich jetzt.** Drei Ereignisse mit Frist: Haug verlangt Tribut (990 Holz ODER
64 Gold), Grom tauscht (5 Messer gegen 20 Erz), Silra verkauft eine Auskunft (ein Zehntel des
Gold-Tagesertrags, mindestens 1 Gold). Annahme gibt 5 Gunst, Ablehnung oder Ablauf nimmt 5.

**Preise mit Quelle, Frist ohne.** Haug 990 Holz oder 64 Gold und der Rechenweg fuer Silra sind V-4
(990 ist der aufgerundete halbe Holz-Tagesertrag 989, 64 der halbe Gold-Tagesertrag 128/2); Groms
Tausch 5 Messer gegen 20 Erz ist Daniels Entscheidung F-1, die Zuordnung auf die vorhandene Ware
Messer ein VORSCHLAG mit Begruendung (eine Ware Werkzeug und den Rohstoff Eisen gibt es nicht, G-4).
Frist 57.600 s, Haeufigkeit 86.400 s und die Gunstwirkung sind VORSCHLAG - Handbuch 2009 und die
2006er Seiten nennen keine Frist.

**Was der Schnitt technisch festlegt:**

- **EINE Preisfunktion** (`diplomatie.ereignis_preis`): Ingame-Dialog, Diplomatie-Ansicht und Buchung
  fragen dieselbe Funktion, es gibt keine zweite Preisrechnung im Code (Wache G).
- **Buchung atomar am Ort** ueber beide Lager: mit 989 Holz wird NICHTS gebucht und der Bestand bleibt
  stehen (Wache C), mit 990 wird genau 990 abgebucht, die Gunst steht auf 55 und der Kontakt ist
  gebucht (Wache D).
- **Hoechstens EIN offenes Ereignis je Bot**, die Art rotiert ueber die Reihenfolge der Datendatei -
  kein Wuerfel im Takt, damit ein Lauf reproduzierbar bleibt. Auch das ERSTE Ereignis wartet die
  Haeufigkeit ab (drei Spieltage), sonst staenden am ersten Takt fuenf Dialoge auf einmal.
- **Alle Saetze stehen in der Datendatei** (`data/story.json`: Titel, Text, Satz bei Annahme, Satz bei
  Ablehnung, Grund-Saetze), alle Zahlen in `data/diplomatie.json`; `src/diplomatie.py` bleibt ASCII.

**Wache:** `tests/test_diplomatie_ereignisse.py` **74 Pruefungen, 0 Fehler, 0 Befunde** - Ablauf bei
57.599 s offen und bei 57.600 s verfallen, Ablehnung bei 989 Holz, genaue Buchung bei 990, Silra-Preis
1 bei 5 Gold am Tag und 12 bei 128, Grom-Tausch mit und ohne Messer, Quellwache Anzeige = Kern,
Haeufigkeit, alter Spielstand ohne Feld, echter Verlauf in der App.

**Am laufenden Fenster belegt:** der Takt oeffnet den Dialog von selbst (Screenshot `s45_overlay.png`:
Titel, Text, Preis, Knoepfe 990 Holz / 64 Gold / Ablehnen), die Diplomatie-Ansicht zeigt die Rubrik
Offene Ereignisse mit denselben Angaben (`s45_diplomatie2.png`).

**Sammellauf:** **187 von 189 gruen, 0 rot, 7.779 Pruefungen, 60 Befunde, 838 s**
(`docs/audits/sammellauf_20261106_1743.log`, allein gelaufen; 189 Dateien statt 188, weil die neue
Wache dazukommt, und 74 Pruefungen mehr als der Lauf um 16:59).

**Geld:** Daniel 17:35 - Guthaben **8,59 USD**, Gesamtverbrauch **61,40 USD** (16:07: 8,76 / 61,23).

**Naechster Schritt:** Ablauf Schritt 6 (Handelspunkte, Befund G-8) - eine Buchstelle beim Abschluss
eines Handelsvertrags (`spieloekonomie.handel_abschluss` liefert `vertrag["erloes"]`), Zaehler
`handels_erloes` und `letzter_handel`, Feld `abgerechnet` gegen Doppelbuchung ueber Speichern und
Laden, Anzeige uebergibt beide Werte an `punkte.auszeichnungen`; danach Schritt 7 (Bot-Luecken) und
8 bis 13 (Balancing, A-1, A-2, A-6, A-7, A-5). Arbeitsweise unveraendert: je Schnitt Register,
Protokollzeile, Stand-Block, Commit, Push und ein VOLLER Sammellauf.

Offen ausserdem: die Buendelung der Besucherdokumente nach `BESUCHER.md` (Daniels Entscheidung 14:00,
Punkt 4) und die neue Frage F-11 (Motive der Spielansichten, `docs/FRAGEN_AN_DANIEL_20261107.md`).

---
# STAND 06.11.2026, 17:10 - Startbilder: Panorama hinter Anmeldung und Ladebild, Logo statt Schriftzug (Register 287)

> Neuester Block. Register 287. Darunter 286 (Rachetopf), 285 (S4-3 verdrahtet), 281 bis 283
> (Runde 2, Spielkonzept, Repo geordnet), 280 (Kennzahlenblatt), 267 bis 279 (Abgleich, Ablauf, S4 Teil 1).

**Der Start sieht jetzt nach Spiel aus.** Daniels Auftrag von 16:37 ist gebaut: hinter dem
Anmeldebildschirm liegt ein Panorama aus SEINEN Referenzbildern (Elfen-Waldlandreich, 38 Prozent
Schleier fuer die Lesbarkeit), den Schriftzug "Nebelseetal" ersetzt unser Logo
(`assets/bilder/logo_nebelseetal_klein.png`, Urheber Chris Fred Daebner) - der ORIGINALE Schriftzug
bleibt unangetastet als Datei in `assets/original/logo.gif` liegen, als Referenz zum Original. Das
Ladebild behaelt sein Schild und bekommt ein Panorama dahinter (Menschen mit Ritter).

**Zwei echte Fehler dabei gefunden und behoben:** (1) Die Ladeansicht lief in einem **200x200** Fenster -
`zeige_loadingpage` wird VOR der App aufgerufen, und die Groesse wurde erst dort gesetzt; jetzt
1024x720, mittig. (2) Das **Schild verschwand**, sobald die Funktion zurueckkehrte: Tk raeumt ein
Bild weg, wenn keine Python-Referenz mehr darauf zeigt (jetzt `root._ladeschild`) - ohne den
Screenshot haette das niemand gesehen, die Pruefdatei war gruen.

**Wache:** `tests/test_startbilder.py` **24 Pruefungen, 0 Fehler** - Motive und Logo vorhanden, cover
ohne leeren Rand, abgedunkelt, Anmeldung mit Panorama + Logo im eigenen Kasten, Ladebild mit
Panorama + Schild, Rueckfall auf den Schriftzug wenn ein Bild fehlt, originaler Schriftzug erhalten.
**Belegt am laufenden Fenster** (Screenshots `%LOCALAPPDATA%\Temp\startbild_anmeldung.png` und
`startbild_laden.png`, per `computer_use` aufgenommen).

**Sammellauf:** **186 von 188 gruen, 0 rot, 7.705 Pruefungen** (`docs/audits/sammellauf_20261106_1640.log`, 1155 s).

**Geld:** Daniel 16:07 - Guthaben **8,76 USD**, Gesamtverbrauch **61,23 USD**.

**Naechster Schritt:** Ablauf Schritt 5 (Ereignisse Haug 990 Holz oder 64 Gold, Silra 12 Gold, Grom
5 Messer gegen 20 Erz, Frist 57.600 s, Annahme +5 / Ablehnung -5 Gunst, atomare Buchung am Ort), dann
Schritt 6 (Handelspunkte, Befund G-8). Offen: die Dokumentauftraege der Antworten 14:00
(Referenzbilder-Vermerk ist mit dem README erledigt, die Buendelung nach `BESUCHER.md` NICHT).

---
# STAND 06.11.2026, 16:30 - Ablauf Schritt 4 fertig: Rachetopf, Ankuendigung, Racheangriff (Register 286)

> Neuester Block. Register 286. Darunter 285 (S4-3 verdrahtet), 281 bis 283 (Runde 2, Spielkonzept,
> Repo geordnet), 280 (Kennzahlenblatt), 267 bis 279 (Abgleich, fixer Ablauf, S4 Teil 1, F-1 bis F-9).

**Schritt 4 des Ablaufs steht: Bots reagieren jetzt auf den Spieler.** Ein Topf je Bot waechst durch
Niederlagen und Funkstille, ab 3 folgt GENAU EINE Ankuendigung, und angegriffen wird erst, wenn die
eigene Armee 99 SK erreicht - freigegeben ueber den VORHANDENEN Weg (`naechster_angriff = 0`), also
ohne zweiten Angriffspfad. Die vier Entscheidungen Daniels sind eingebaut: Topf faellt nach einem
Bot-Sieg auf 0 (F-3), der Topf steigt AUCH unter einem Pakt, der Angriff feuert fruehestens
28.800 s nach dem Paktende, und Kontakt ist jede Interaktion (Handel, Angriff, Kampf, Geschenk) -
sie setzt den Zaehler neu.

**Zahlen (Urteil je Wert in Register 286):** Armee-Schwelle **99 SK** (V-5, nicht die 90 der
Wall-Schwelle), Topf-Schwelle **3**, **+1 je Niederlage**, **+1 je Spieltag ohne Kontakt**, Deckel
**5**, Vorlauf **28.800 s**: die letzten vier sind VORSCHLAG. Unter dem Goetterschutz ruht der Topf
(VORSCHLAG, G-1). Alle Texte liegen in `data/diplomatie.json` (`rache.ankuendigung`), nicht im Code.

**EINE neue Rechenstelle:** `einheiten.armee_schlagkraft` summiert SK x Anzahl - dieselbe Funktion
fuer Kern und Anzeige, keine zweite Armeestaerke im Code.

**Wache:** `tests/test_diplomatie_rache.py` **53 Pruefungen, 0 Fehler** - elf Abschnitte, darunter der
echte Verlauf: App gebaut, Bot mit 40 Kriegern (120 SK), Takt gefahren, Topf gefuellt, Ankuendigung
im Postfach, Vorlauf abgelaufen, Angriff freigegeben, KEINE zweite Ankuendigung.

**Sammellauf:** 15:52 bis 16:26, **185 von 187 gruen, 0 rot, 7.681 bestandene Pruefungen**
(`docs/audits/sammellauf_20261106_1552.log`). **Die Dauer (2.017 s) ist NICHT belastbar** - der Lauf
stand unter Nebenlast; einzeln gemessen kostet die Aenderung in `test_startspiel` 37 s gegen 31 s
ohne sie (20 Prozent), nicht das Zehnfache. Fuer A-6 gilt weiter die Grenze 1.800 s aus F-2.

**Geld:** Daniel 16:07 - Guthaben **8,76 USD**, Gesamtverbrauch **61,23 USD** (14:31: 8,87 / 61,12;
also 0,11 USD in diesem Abschnitt).

**Naechster Schritt:** Ablauf Schritt 5 - Ereignisse Haug (990 Holz oder 64 Gold), Silra (12 Gold),
Grom (5 Messer gegen 20 Erz), Frist 57.600 s, Annahme +5 / Ablehnung -5 Gunst, atomare Buchung am
Ort. Danach Schritt 6 (Handelspunkte, Befund G-8). Offen aus den Antworten 14:00: die
Dokumentauftraege (Referenzbilder-Vermerk im Repo, Buendelung nach `BESUCHER.md`).

---
# STAND 06.11.2026, 15:06 - Ablauf Schritt 3 fertig: Vertraege wirken, der Pakt bricht beim Absenden (Register 285)

> Neuester Block. Register 285. Darunter 281 bis 283 (Runde 2, Spielkonzept, Repo geordnet), 280
> (Kennzahlenblatt), 267 bis 279 (Abgleich Runde 1, fixer Ablauf, S4 Teil 1, Entscheidungen F-1 bis F-9).

**Schritt 3 des Ablaufs ist verdrahtet - die Vertragslogik wirkt jetzt im Spiel.** Bis heute Mittag
stand nur das Modul; jetzt fuehrt der Bot das Feld `vertraege` (additiv: ein alter Spielstand laedt
ohne es und hat damit keinen Pakt), `bot_als_dict`/`bot_aus_dict`/`bot_aus_stand` tragen es hin und
zurueck, und drei Stellen fragen die Diplomatie:

- **Der Spieler bricht den Pakt beim ABSENDEN eines Angriffs** (`_angriff_auftrag_starten`, vor
  `auftrag_starten`): Gunst -20, Rache +1 (gebucht ab Schritt 4), Meldung im Postfach. Kein Verbot -
  Daniels Entscheidung vom 14:00, die Absicht zaehlt, nicht die Ankunft.
- **Der Bot greift nicht an, solange der Pakt steht** (`main.py`, direkt neben `punkte.angreifbar`):
  `diplomatie.angriff_gesperrt` ist eine VORBEDINGUNG, die Punktrechnung bleibt unangetastet (G-1).
- **Auch der Diebstahl respektiert den Pakt** (`main.bot_diebstahl`) - die Mechanik ist heute aus,
  das Gate steht trotzdem da, damit sie beim Einschalten nicht ohne Schutz anlaeuft.

**Zwei Fehler auf dem Weg, beide behoben und benannt:** (1) `bot_als_dict` liegt in `GameState`,
nicht in `NebelseetalApp` - der erste Sammellauf lief mit `AttributeError` rot (`test_gesamtsieg`,
`test_gpt_kampf_botbeute_echte_kasse`); ich habe den Lauf verworfen, statt ihn zu erklaeren.
(2) Der Durchmarsch-Text trug die Ersatzschreibweise "gewaehrt"; er steht jetzt mit echtem Umlaut in
`data/diplomatie.json` (Regel: kein Spieltext im Code) - die Umlaut-Wache war gruen, sobald er dort lag.

**Wache:** `tests/test_diplomatie_vertraege.py` **68 Pruefungen, 0 Fehler** - acht Faelle des Ablaufs,
die zwei Entscheidungen von 14:00 (Bruch beim Absenden, Handelsabkommen bricht nicht mit), die
Quellwache fuer beide Aufrufstellen und ein ECHTER Verlauf (App gebaut, Siedlung gegruendet, Pakt-Bot
angegriffen, Postfach und Gunst geprueft).

**Sammellauf:** 14:44 bis 15:06, **184 von 186 gruen, 0 rot, 1325 s, 7.628 bestandene Pruefungen**
(`docs/audits/sammellauf_20261106_1449.log`). Die zwei Dateien ohne Ergebniszeile sind die bekannten zwei.

**Geld:** Daniel 14:31 - Guthaben **8,87 USD**, Gesamtverbrauch **61,12 USD** (13:49: 9,06 / 60,93;
also 0,19 USD seit dem letzten Ablesen).

**Naechster Schritt:** Ablauf Schritt 4 - Rachetopf (Entwurf mit allen Zahlen liegt im Scratch,
Register 284/285 sind die Vorgabe: Kontakt = jede Interaktion, Topf steigt auch unter Pakt, Angriff
fruehestens 28.800 s nach Paktende, nach Bot-Sieg 0). Danach Schritt 5 (Ereignisse Haug, Grom, Silra)
und Schritt 6 (Handelspunkte, G-8). Offen aus den Antworten 14:00: die Dokumentauftraege
(Referenzbilder-Vermerk im Repo, Buendelung nach `BESUCHER.md`).

---
# STAND 06.11.2026, 13:36 - Runde 2 gemessen, Spielkonzept steht, Repo geordnet (Register 281 bis 283)

> Neuester Block. Register 281 bis 283. Darunter 280 (Kennzahlenblatt), 267 bis 279 (Abgleich Runde 1,
> fixer Ablauf, S4 Teil 1, Entscheidungen F-1 bis F-9), 264 (Ziel).

**Runde 2 ist verarbeitet - und zwar gemessen, nicht geglaubt.** Die vier Antworten liegen in
`docs/eingaenge/LLM_20261106_runde2/` (Hashes beidseitig gleich, Desktop geraeumt, nichts geloescht),
die Auswertung in `docs/ABGLEICH_LLM_20261106_runde2.md`. Vier Befunde sind gegen UNSERE Dokumente:
die Abhaengigkeitstabelle nennt fuer Schritt 10 `3 bis 10` (Selbstabhaengigkeit, richtig `3 bis 9`)
und fuer Schritt 7 nur `5` - die Rache aus Schritt 4 fehlt; `durchmarsch` kommt in `src/` und `data/`
nirgends vor, die geplante Wache waere vor dem Einbau wertlos; `handel_abschluss` setzt `erloes` genau
einmal, aber ein Feld `abgerechnet` fehlt (Doppelbuchung ueber Speichern/Laden moeglich); `Kontakt`
wird im Ablauf benutzt, aber nirgends definiert. Elf Wachen werden verschaerft (dynamisch statt
Quelltextsuche), drei Aufbauzeit-Texte korrigiert, Schritt 9 bekommt die Regel, dass ein zusaetzlicher
Startwert mitspielen muss.

**EIN starker Aufruf** (`deepseek-v4-pro`, Dossier 14,3 KB, Streaming): 15.367 Zeichen Antwort,
193,9 s, 5.275 Prompt- und 15.952 Antwort-Token (11.429 Denk-Token), rund **0,07 USD**. Die Antwort
liegt hashgleich als `docs/SPIELKONZEPT_ENTWURF_V4PRO_20261106.md`.

**Das zentrale Spielkonzept steht:** `docs/SPIELKONZEPT.md` (13.002 Byte, 12 Kapitel) ist ab jetzt das
EINE fuehrende Dokument fuer Spielziel, Mechaniken, Zahlenmassstab und Belegpflicht - mit richtigem
Urteil je Aussage (das Modell hatte VORSCHLAEGE als BELEGT bezeichnet, das ist korrigiert), drei
Regeln zur Aktualitaet und fuenf offenen Fragen an Daniel. Dazu `docs/INDEX.md` als Wegweiser.

**Repo geordnet** (Daniel 13:20): 14 Auftraege nach `docs/auftraege/`, 14 Uebergaben und 8 Fragenakten
nach `docs/archiv/`, `index.html` auf **V_0.0.3** mit einem Abschnitt "Was dieses Spiel will" und dem
richtigen Download-Link (der alte `/releases/latest` zeigt bei reinen Pre-Releases ins Leere).
Bildcontent: drei Sammlungen (32 MB) auf Daniels Freigabe entfernt, seine 15 Referenzbilder unter
`assets/referenzbilder/` (Commit `f09b672`).

**Sammellauf:** sauberer Lauf 12:48 bis 13:11 **183 von 185 gruen, 0 rot, 1290 s, 7.557 Pruefungen**
(der Lauf davor war unter meiner Nebenlast 2.363 s mit zwei roten Dateien und ist nicht belastbar).
G-5 damit zum vierten Mal belegt: 1.800 s traegt, 1.400 s nicht.

**Geld:** Daniel 13:31 - Guthaben **9,13 USD**, Gesamtverbrauch **60,86 USD** (10:15: 9,50 / 60,49;
also 0,37 USD in dieser Sitzung, davon rund 0,07 USD der starke Aufruf).

**Naechster Schritt:** Ablauf Schritt 3 (Vertraege) - mit den verschaerften Wachen aus Runde 2, der
Definition von `Kontakt` vor dem Rachetopf und dem korrigierten Abhaengigkeitstext. Vorher sind fuenf
Fragen an Daniel offen (Abschnitt 12 des Spielkonzepts): Kontakt, Topf unter Pakt, Durchmarsch,
Paktwirkung, Prioritaet. Kein Release vor S4 komplett (F-9), KI-Auftrag Runde 3 erst nach S4 (F-8).

---

# STAND 06.11.2026, 12:06 - Ablauf Schritt 2 gebaut: Kennzahlenblatt (Register 280)

> Neuester Block. Register 280. Darunter 267 bis 279 (Abgleich, fixer Ablauf, S4 Teil 1 Gunst,
> Entscheidungen F-1 bis F-8), 264 (LLM-Antworten, Ziel), 263 (V_0.0.3), 262 (Sammellauf).

**Neu (Ablauf Schritt 2):** Jede Partie hinterlaesst jetzt eine Zeile, gegen die jede weitere
Aenderung messbar ist. `tools/spieltest_simulation.py --kennzahlen` schreibt 16 Pflichtschluessel
nach `docs/balancing/kennzahlen.jsonl` (eine Zeile je Partie, angehaengt, nichts ueberschrieben) und
die lesbare Tabelle `docs/balancing/KENNZAHLEN_<datum>.md`; die Rechenwege je Schluessel stehen in
`docs/balancing/README_KENNZAHLEN.md`. **`null` heisst nicht 0** - ein nie erreichter Meilenstein
bleibt `null`, und `handelspunkte` ist `null`, solange der Zaehler fehlt (Befund G-8, Schritt 6).
Meilensteine werden aus dem ZUSTAND gelesen (Haus steht, Ware liegt im Lager, Einheit im Heer),
nicht aus dem Auftrag - sonst misst man einen Wunsch.

**Determinismus ist hergestellt:** der Lauf bildet EINEN `random.Random(saat)` und gibt ihn an
jedes Gefecht weiter (`spielschicht.angriff(..., rng=)`). Vorher zog `kampf.fuehre_schlacht` je
Gefecht ein neues `random.Random()` - derselbe Startwert ergab andere Zahlen, und eine Vorher-Zahl
waere nichts wert gewesen. Gemessen: zwei Laeufe ueber 12 Spieltage sind Zeichen fuer Zeichen gleich
(2.596 Zeichen, Zeile 2.628 Byte).

**Erste Vorher-Zahl** (Saat 7, Stil breit, 12 Spieltage): erstes Haus **T2,486**, erste Bibliothek
**T0,042**, erste Ware **T7,833**, erster Krieger **T1,167**, erstes Gefecht **T2,0**, Ruhm **2**,
Beute **190** Rohstoffe in 6 Gefechten, eigene Verluste **0**, **Leerlauf 956.400 s von 1.036.800 s
(92 % der Partie ohne eine einzige erfolgreiche Aktion)**, laengste Strecke ohne neuen Meilenstein
**5,347 Spieltage**. Der Leerlauf ist die eigentliche Zahl dieser Messung: die Spielerpolitik steht
die meiste Zeit still ("alle Gebaeude der Kette stehen (je 2)", Ausbau zu teuer, Kurzschwert braucht
Waffentechnik 3). Das ist ein Befund ueber den AUTOMATEN, kein Spielfehler - und die Vorher-Zahl,
gegen die Schritt 8 (Sollkurve) und Schritt 9 (Regelkreis) antreten.

**Wache:** `tests/test_kennzahlenblatt.py` **21/0/0** (Pflichtschluessel vollstaendig, zwei Laeufe
identisch, `null` gegen `0`, `daten_hash` folgt dem Datenstand, Schreiben ausschliesslich unter
`docs/balancing/` - `data/` und `src/` bleiben Byte fuer Byte unberuehrt, halbe Zeile wird
abgelehnt). `tools/balancing_messung.py` nennt als Abschnitt 0 die juengste gemessene Partie und
warnt, wenn ihr `daten_hash` nicht mehr zu `data/` passt; es rechnet nichts nach.

**Naechster Schritt:** Ablauf Schritt 3 (S4-3 Vertraege: NAP sperrt Bot-Angriff UND Diebstahl an den
ZWEI echten Gates `main.py:7051` und `:6624` ueber `diplomatie.angriff_gesperrt`, Handelsabkommen
ueber den vorhandenen `spieloekonomie.handel_start`, Durchmarsch als reine Anzeige), dann 4
(Rachetopf, Schwelle 99 SK, nach Bot-Sieg 0 = F-3), 5 (Ereignisse, Grom 5 Messer gegen 20 Erz =
`metall` = F-1), 6 (Handelspunkte: Erloes aus `handel_abschluss` auf `handels_erloes` buchen, damit
das Kennzahlenblatt `handelspunkte` nicht mehr `null` zeigt). Je Schnitt Register, Protokollzeile,
Stand-Block, Commit und voller Sammellauf (`--parallel` zuerst messen, Grenze vorlaeufig 1.800 s =
F-2). Kein Release vor S4 komplett (F-9), KI-Auftrag Runde 2 erst nach S4 (F-8).

---

# STAND 06.11.2026, 11:10 - Abgleich und fixer Ablauf stehen, S4 Teil 1 Gunst gebaut (Register 267 bis 274)

> Neuester Block. Register 267 bis 274. Darunter 264 (LLM-Antworten, Ziel), 263 (V_0.0.3),
> 262 (Sammellauf), 261/260 (LLM-Auftrag, deutsche Zahlenanzeige).

**Neu:** Die vier Modellantworten sind abgeglichen (Claude Opus 5.5 vollstaendig, die drei anderen als
Extrakte mit Zeilenfundstelle) - `docs/ABGLEICH_LLM_20261106.md` mit **acht gemessenen Gegenbefunden
G-1 bis G-8**. Vier davon sind Befunde gegen unsere eigenen Dokumente oder gegen die Modelle: die
Angriffssperre ist `punkte.angreifbar` an `main.py:7051` und `:6624` (`versorgungsschutz.py` ist KEIN
Gate, zwei Modelle irrten gleich), die Rache-Schwelle ist **99 SK** (nicht 90, berichtigt), V-4 ist
ueber `tools/s0_tabellen.py:110-111` nachrechenbar (Rechenweg ins Dokument nachgetragen), Werkzeuge und
Eisen gibt es im Spiel nicht (Grom-Ereignis offen, F-1), **A-6 ist nicht erfuellt** (1552 s gegen
1.400 s), und die **Handelspunkte koennen nie steigen, weil `gold_erloes` nirgends geschrieben wird**
(der Handelsweg selbst ist fertig gebaut - die Behauptung dreier Modelle, er sei eine Sackgasse, ist
widerlegt).

**Der fixe Ablauf steht:** `docs/ABLAUF_LLM_20261106.md` - 13 Schritte plus Dokumentenschritt, je Ziel,
Dateien, Aenderung, Daten mit Herkunft, Wache mit Faellen, Fertig-Kriterium, Aufbauzeit-Effekt,
Abloesung, Risiko; dazu die Entscheidungen F-1 bis F-6 und drei Widerlegungspruefungen. Entworfen mit
**EINEM** vorbereiteten `deepseek-v4-pro`-Aufruf (28,7 KB Dossier, `max_tokens` 48.000, Streaming):
**0,11 USD gemessen** (9,85 auf 9,74). Der Entwurf wurde geprueft und an vier Stellen korrigiert.

**Schritt 1 ist gebaut:** `src/diplomatie.py` (EINE Lesestelle fuer Gunst und Status, Status wird
gerechnet und nie gespeichert), `data/diplomatie.json` (jede Zahl mit Quelle), Feld `gunst` am
`BotPlayer` ueber `bot_als_dict`/`bot_aus_dict`, geklemmt beim Laden; Anzeigezeile in
`_render_diplomacy`. Wache `tests/test_diplomatie.py` **33/0/0**. Protokoll von 320 auf 311 Zeilen
verdichtet, alle Kennungen und Pruefzahlen erhalten.

**Sammellauf:** zweiter voller Lauf nach dem Fix der Projektordnung **182 von 184 gruen, 0 rot, 1552 s,
7.536 Pruefungen, 60 Befunde** (`docs/audits/sammellauf_20261106_1040.log`). Der erste Lauf war rot, weil
die Vor-Fassung des Protokolls in `docs/` lag - sie gehoert nach
`archiv/dokumentation/protokoll_alte_fassungen/`.

**Geld:** Daniel 10:43 - Guthaben **9,44 USD**, Gesamtverbrauch **60,55 USD**; starkes Modell 0,11 USD
verbraucht. **Neu freigegeben: 3,00 USD** fuer `deepseek-v4-pro` (Register 274).

**Naechster Schritt:** den Ablauf abarbeiten - Schritt 2 Kennzahlenblatt, dann Vertraege (3), Rachetopf
(4), Ereignisse (5), Handelspunkte (6), Bot-Luecken (7), Balancing (8, 9), Abschluss (10 bis 13). Je
Schnitt Register, Protokollzeile, Stand-Block, Commit und voller Sammellauf.

---
# STAND 06.11.2026, 09:10 - Planung mit deepseek-v4-pro, geschuetzte Auftragsdatei (Register 264)

> Neuester Block. Register 264, Protokollzeile 09:04. Darunter 263 (V_0.0.3), 262 (Sammellauf),
> 261/260 (LLM-Auftrag, Zahlenanzeige).

**Neu (Daniel 09:04):** Die naechste Sitzung fuehrt das Zusammenfuehren der vier Modellantworten und das
Entwerfen des fixen Ablaufs mit **`deepseek-v4-pro`** aus - kostenbewusst in EINEM vorbereiteten Aufruf
(Dossier 20 bis 30 KB, `max_tokens` 48.000, Streaming, Zwischenschreiben; rund 0,039 USD je Aufruf,
Deckel 4,00 USD/Tag), mit Ruecksicht auf die schwache Laptop-Hardware und das schwankende WLAN. Zuerst
wird lokal und kostenlos verglichen, nie werden die vier Antworten roh geschickt. Die Desktop-Datei
`Nebelseetal_LLM_Auftrag_20261106.md` ist **geschuetzt**: sie wird erst nach dem stehenden Ablauf mit dem
neuesten Stand als neuer KI-Auftrag umgearbeitet, und Daniel ist dann ausdruecklich zu melden. Beides
steht als Abschnitt K und L in `docs/ABLAUF_20261107.md`.

**Geld:** Ablesung 09:04 - Guthaben **10,31 USD**, Gesamtverbrauch **59,68 USD** (0,37 USD seit 07:38).

**Naechster Schritt:** Protokoll verdichten (319 Zeilen), dann Abgleich der Antworten mit
`deepseek-v4-pro`, dann `docs/ABLAUF_LLM_20261106.md`, dann Umsetzung ab S4 Teil 1.

---
# STAND 06.11.2026, 08:53 - Vier LLM-Antworten liegen vor, neues Ziel (Register 264)

> Neuester Block. Register 264. Darunter 263 (Pre-Release V_0.0.3), 262 (Sammellauf), 261/260
> (LLM-Auftrag, deutsche Zahlenanzeige), 259 (Verlustbericht).

**Neu:** Der Auftrag `docs/extern/Nebelseetal_LLM_Auftrag_20261106.md` ist von **vier Modellen**
beantwortet und die Antworten liegen hashgeprueft im Projekt:
`docs/eingaenge/LLM_20261106/` - Claude Opus 5.5 (**46.259 Byte, 11 Schnitte, Teil 7a mit Z-1 bis Z-5
= von Daniel genehmigter Zusatz-Content**), UseAI Instant (86.957 Byte, 9 Schnitte, 11 Einwaende),
Grok 4.5 (25.066 Byte, OpenDocument, Schnitte als Tabellen) und Gemini (8.673 Byte, S4 in einem
Schnitt). `README.md` dort traegt Index, SHA256 je Datei, Rangfolge (Claude zuerst) und die vier
Prueffragen. Der Desktop-Ordner ist geraeumt, nichts geloescht.

**Neues Ziel (Daniel 06.11.2026):** aus den Antworten **schnellstens EINEN vorerst fixen Ablauf**
bauen, der das Spiel in den Zustand bringt, in dem **nur noch Balancing und Bugfixing** noetig sind -
damit das Spiel immer besser, fluessiger und stimmiger wird.

**Naechster Schritt:** die Antworten abgleichen (Claude vollstaendig, die anderen drei als Gegenprobe),
daraus den fixen Ablauf als eigenes Dokument schreiben und den ersten Schnitt (S4 Teil 1 Gunst und
Status) umsetzen. Je Schnitt Register, Protokollzeile, Stand-Block, Commit und Push.

---
# STAND 06.11.2026, 08:35 - V_0.0.3 gebaut, gestartet, Sammellauf gruen (Register 262/263)

> Neuester Block. Register 262 und 263. Darunter 261/260 (LLM-Auftrag, deutsche Zahlenanzeige),
> 259 (Verlustbericht), 258 (Sammellauf 181/183), 257 (S3).

**Neu:** Der Stand mit deutscher Zahlenanzeige ist im vollen Sammellauf: **181 von 183 Dateien gruen,
0 rot**, 7.502 Pruefungen, 1.612 s (`docs/audits/sammellauf_20261106_0755.log`) - sieben Pruefungen mehr
als im Lauf 06:59, das ist genau die neue Wache. Die **Pre-Release `V_0.0.3`** ist gebaut
(`tools/build_public_exe.py`, 409 s): EXE **102.098.672 Byte**, SHA256 `915fe8144eda...`, ZIP
**101.818.049 Byte**, SHA256 `4d1dad2cf4f2...`. Startprobe belegt: Fenster `Nebelseetal Remake`,
PID 15080, **Passwortsperre im Bild**, danach 0 Prozesse, verwaiste `game.lock` gesichert und entfernt,
Demo-Ordner ohne Spielstand. Die veroeffentlichte 0.0.2 bleibt unangetastet (Daniels Entscheidung).
Notizen: `docs/RELEASE_NOTES_PRE_RELEASE_V_0_0_3.md`.

**Naechster Schritt:** die naechste Sitzung sammelt die Antworten der externen Modelle ein (Daniel
postet sie im Lauf der Uebergabe), legt sie hashgleich nach `docs/eingaenge/LLM_<JJJJMMTT>/antworten/`
ab, gleicht sie gegeneinander ab und setzt den Gewinner in Schnitte um - beginnend mit **S4 Teil 1
(Gunst und Status)** nach `docs/ABLAUF_20261107.md` Abschnitt D. Der LLM-Auftrag selbst steht in
`docs/extern/Nebelseetal_LLM_Auftrag_20261106.md`. S5 bleibt gesperrt.

---
# STAND 06.11.2026, 08:05 - LLM-Auftragsdatei fertig, Anzeige in deutscher Schreibweise (Register 260/261)

> Neuester Block. Register 260 und 261. Darunter 259 (Verlustbericht, Flakiness-Wache), 258 (Sammellauf
> 181/183), 257 (S3 Verwundetenheilung).

**Neu:** Die fuenf offenen Fragen sind in EINER Runde beantwortet (`docs/FRAGEN_AN_DANIEL_20261107.md`):
EXE als **neuer Zaehler V_0.0.3** statt Ueberschreiben der veroeffentlichten 0.0.2, Heilungskosten im Kern
ungerundet aber in der Anzeige mit Komma, zwei bis drei Modelle fuer den LLM-Auftrag, Abloesen alter
Ablaeufe nur als eigener Schnitt mit Beleg, **S5 bleibt gesperrt**. Gebaut: `hilfen.zahl_de` als EINE
Schreibweise deutscher Zahlen, `_heilung_zeile_zeichnen` benutzt sie (vorher `%g`, also 0.75 statt 0,75);
Wache `test_verwundete` **52/0/0**. Dazu die **LLM-Auftragsdatei** `docs/extern/Nebelseetal_LLM_Auftrag_20261106.md`
(37.297 Byte): Spiel, Mechaniken, Codeaufbau, gebauter und geplanter Stand, sieben Abschlussbedingungen,
Balancing-Werkzeug-Bestand mit fuenf Luecken, Auftrag, Lieferformat, Ablagehinweise und die Warnung vor
ungepruefter Uebernahme. Der Vorgaenger `Nebelseetal_Infos_ExterneKI.txt` liegt hashgleich in
`docs/extern/archiv/` (nichts geloescht). `docs/ABLAUF_20261107.md` fuehrt B, C, H und I als gebaut.

**Geld:** Daniel hat um **07:38** abgelesen: Guthaben **10,68 USD**, Gesamtverbrauch **59,31 USD** -
gegen die Ablesung 05:44 (10,99 / 59,00) sind das **0,31 USD** in 1 h 54 min, im Rahmen der Erwartung.

**Naechster Schritt:** Schritt J des Ablaufs - voller Sammellauf ueber den neuen Stand, dann
Pre-Release `V_0.0.3` bauen (`tools/build_exe.py`, Name aus `data/version.json`), Startprobe mit
Fensterbeleg, Release mit Notizen und Assets, Repo pushen. Danach ist diese Sitzung die LETZTE: die
naechste Sitzung bekommt die Antworten der LLM und setzt sie nach Abgleich in Schnitte um; S4 Teil 1
(Gunst und Status) ist der erste fachliche Schritt danach.

---
# STAND 06.11.2026, 07:24 - S3 fertig, Verlustbericht als eigener Typ (Register 259)

> Neuester Block. Register 258 und 259. Darunter 257 (S3 gebaut), 256 (Gemini-Buendelung), S2-Lauf.

**Neu:** S3 (Verwundetenheilung) ist gebaut, geprueft und im vollen Sammellauf: 181 von 183 Dateien
gruen, 7495 Pruefungen, 0 Fehler, 60 Befunde. Block 5 ist ebenfalls fertig - Verluste erzeugen jetzt
eine Nachricht vom Typ `verlust` (der Typ stand seit S1 in `data/nachrichten.json`, der Erzeuger
fehlte), und die flatternde Wache `test_kartenwahl_bot` hat einen festen Startwert in der Pruefdatei.
Dazu liegen zwei neue Arbeitsblaetter: `docs/eingaenge/GEMINI_20261106/FILTER_20261107.md` (26
Gemini-Unterlagen in drei Koerben) und `docs/ABLAUF_20261107.md` (S3 bis S5 mit Wache,
Fertig-Kriterium und Aufbauzeit-Effekt).

**Naechster Schritt:** S4 Teil 1 (Gunst und Status) nach `docs/ABLAUF_20261107.md` Abschnitt D -
Felder ueber `bot_als_dict`/`bot_aus_dict`, Statusgrenzen 0-39/40-59/60-100, Anzeigezeile in
`_render_diplomacy`, Wache `tests/test_diplomatie.py`. Danach voller Sammellauf, Register, Protokoll,
Stand, Commit und Push. S5 bleibt gesperrt bis Daniels Freigabe.

---
# STAND 06.11.2026, 06:28 - S3 Verwundetenheilung gebaut (Register 257)

> Neuester Block. Register 257. Darunter 256 (Gemini-Buendelung, 06:03), S2-Lauf (05:56), S2-Bau (05:19).

**Neu:** S3 ist gebaut - 30 Prozent der Verluste je Einheitentyp werden verwundet (abgerundet), die
Heilung kostet 75 Prozent der Kostenposten ohne Siedler und ohne Ausruestung und dauert die Haelfte der
Ausbildungsdauer. Die Zahlen stehen in `data/verwundete.json`, die Rechnung in `src/verwundete.py`, das
Feld `verwundete` an `Settlement`; die Anzeige sitzt in der Kaserne und nennt jede Bedingung einzeln.
Wache `tests/test_verwundete.py`: 41 bestanden, 0 Fehler.

**Naechster Schritt:** der volle Sammellauf ueber den S3-Stand (182 Dateien, 35 bis 50 Minuten, mit
`.venv/Scripts/python.exe -X utf8 -u tools/sammellauf.py`), danach Block 5 (Verlustbericht als eigener
Typ `verlust`, Flakiness-Wache `test_kartenwahl_bot`) und S4 Teil 1. Jeder Schritt endet mit Register,
Protokoll, Stand-Block, Commit und Push.

---
# STAND 06.11.2026, 06:03 - Gemini-Unterlagen gebuendelt (Register 256)

> Neuester Block. Register 256. Darunter Design Content Nr. 3 (05:5x), S2-Lauf (05:56), S2-Bau (05:19).

**Neu:** `docs/eingaenge/GEMINI_20261106/` mit `eingang/` (6), `auftraege/` (6), `antworten/` (8) und
`auswertungen/` (6) sowie einem `README.md`, das jede Quelle beurteilt und die vier Prueffragen vor jeder
Uebernahme festhaelt. Der Plan zeigt auf die neuen Pfade.

**Naechster Schritt:** der neue Ablauf der Uebergabe 06:3x (Info-Filter, S3, kleine Auftraege, S4).

---

# STAND 06.11.2026, 05:59 - Design Content Nr. 3 abgelegt, Google-Antwort ausgewertet (Register 255)

> Neuester Block. Register 255. Darunter S2-Lauf (05:56), S2-Bau (05:19), S1b (03:47), S1 (03:22), S0 (03:02).

**Abgelegt, nichts gebaut:** fuenf Fraktionspanoramen (1637x640, hashgleich) in
`assets/hintergrund_content_20261106_fraktionen/`, der Google-Auftrag in `docs/eingaenge/`, die Antwort war
schon dort. Auswertung in `docs/eingaenge/EINORDNUNG_GEMINI_ANTWORT_AUFTRAG_20261106.md`: **Teil A brauchbar
als Testfall-Vorlage fuer S3** (ein Zahlenfehler: Fall 17 nennt 60 statt 50 Prozent), **Teil B brauchbar fuer
S4** (Kennungen laufen B1-B12 statt B1-B8), **Teil C unbrauchbar fuer die Anzeige** (C3/C4 nennen keine
fehlende Menge, C5 keine Restzeit).

**Desktop:** nur noch `Nebelseetal_Infos_ExterneKI.txt` (bleibt laut Daniel) und die Uebergabe.

---

# STAND 06.11.2026, 05:56 - S2 im Sammellauf geprueft, Gemini-Material abgelegt (Register 253/254)

> Neuester Block. Register 253/254, Protokollzeile 05:56. Darunter S2-Bau (05:19), S1b (03:47), S1 (03:22), S0 (03:02).

**Sammellauf 3 (S2):** 182 Dateien, 7448 Pruefungen, 1 Fehler, 60 Befunde, 2072 s. Die eine rote Datei
`test_kartenwahl_bot.py` ist im Einzellauf dreimal gruen - Flakiness (Zufall ohne festen Startwert), kein
Fehler des Schnitts. **Der Punkt bleibt offen und ist in der Uebergabe benannt.**

**Neu abgelegt (nichts davon gebaut):** `docs/eingaenge/GEMINI_WEITERE_VORSCHLAEGE_20261106.txt`,
`GEMINI_ANTWORT_AUFTRAG_20261106.txt`, `GEMINI_ALTERNATIVEN_20261106.md` und
`EINORDNUNG_GEMINI_VORSCHLAEGE_20261106.md`. Befund: der Vorschlag rechnet die Mauerreparatur mit
`16 * Stufe / 10` je Prozentpunkt - belegt und gebaut ist `/ 100`.

**Naechster Schritt:** S3 Verwundetenheilung nach V-2 (Block 5 des Nachtauftrags).

---

# STAND 06.11.2026, 05:19 - S2 gebaut: Mauerreparatur (Register 252)

> Neuester Block. Register 252, Protokollzeile 05:19. Nachtlauf. Darunter S1b (03:47), S1 (03:22), S0 (03:02).

**Was dieser Schnitt geaendert hat:** die Dorfmauer laesst sich reparieren - nachgerechnet, nicht geschaetzt.

| Stueck | Beleg |
|---|---|
| Rechenkern | `src/dorfwall.py`: `reparatur_preis`, `reparatur_sekunden`, `reparatur_pruefen`, `reparatur_starten`, `reparatur_tick`, `reparatur_abbrechen` |
| Felder am Ort | `Settlement.mauer_reparatur_start_zustand/start_zeit/ziel/ende/stufe` (5 Felder, save/load belegt) |
| Kern | `GameState.mauer_reparatur_starten`, `mauer_reparatur_weiter` im Tick |
| Abbruch | nach der Kampf-Buchung: ein Angriff bricht die Reparatur ab |
| Anzeige | `_mauer_reparatur_block` in der Verteidigungs-Rubrik: jede Bedingung EINZELN + naechster Schritt |
| Wache | `tests/test_mauerreparatur.py` - 46 bestanden, 0 Fehler, 0 Befunde |

**Zahlen (V-1):** je Prozentpunkt 16 * Stufe / 100 in Holz und Stein; 0 auf 100 kostet genau den Wallpreis mal
Stufe (Stufe 1: 16/16, Stufe 10: 160/160) und dauert 36000 Spielsekunden = 200 Sekunden echt.

**Ein Fehler beim Bauen, ehrlich benannt:** ein Schreibversuch mit `encoding=ascii` hat `dorfwall.py` geleert
(die Datei traegt echte Umlaute); aus der Sicherung vollstaendig wiederhergestellt.

**Naechster Schritt:** voller Sammellauf 3, danach S3 Verwundetenheilung (Zahlen aus V-2).

---

# STAND 06.11.2026, 03:47 - S1b gebaut: vier Menue-Teilgeschichten (Register 251)

> Neuester Block. Register 251, Protokollzeile 03:47. Nachtlauf. Darunter S1 (03:22) und S0 (03:02).

**Was dieser Schnitt geaendert hat:** vier kurze Geschichten erscheinen beim ersten Oeffnen ihrer Ansicht.

| Stueck | Beleg |
|---|---|
| Texte | `data/story.json` -> `menue_geschichten` (Forschung, Portal, Kaserne, Ruhmeshalle), neu geschrieben von uns |
| Lesestelle | `story.menue_geschichte(schluessel)` - Text nur aus der Datendatei |
| Einmal-Kennzeichen | `GameState.menue_geschichten_gesehen` (init, save, load mit `.get`-Fallback) |
| Anzeige | `_menue_geschichte_pruefen` in `_switch_view`, Ingame-Overlay mit einem Schliessen-Knopf |
| Wache | `tests/test_story_menue.py` - 42 bestanden, 0 Fehler, 0 Befunde |

**Portal ohne Antwortknoepfe** (Daniel, Runde 3 Frage 1): das Overlay hat genau einen Knopf, und der schliesst nur.

**Naechster Schritt:** voller Sammellauf 2 (deckt S1-Fix und S1b zusammen), danach S2 Mauerreparatur.

---

# STAND 06.11.2026, 03:22 - S1 gebaut: Postfach mit Archiv, Filter, Blaettern, Ruhm-Balken (Register 250)

> Neuester Block. Register 250, Protokollzeile 03:22. Nachtlauf. Der Block 03:02 darunter haelt S0.

**Was dieser Schnitt geaendert hat:** das Postfach zeigt nicht mehr nur die letzten 20 Nachrichten.

| Stueck | Beleg |
|---|---|
| Fachmodul mit Fristen, Kategorien, Seiten, Rang | `src/postfach.py` (neu) |
| Fristen und Kategorien als Daten | `data/nachrichten.json` (Frist 1 Spieltag = 28800 Spielsekunden) |
| Ruhm-Stufen | `data/ruhm.json` (0 / 10 / 40 / 160, Daniels Freigabe 03:1x) |
| Ansicht | `_render_messages` + `_ruhm_balken_zeichnen` in `src/main.py` (Filterzeile, 20 je Seite, Archiv, Balken als Canvas) |
| Ablauf | `postfach.ablauf_buchen` im `GameState.tick` |
| Wache | `tests/test_nachrichten_archiv.py` - 51 bestanden, 0 Fehler, 0 Befunde |

**Zwei Befunde beim Bauen:** eine Frist als Konstante im Code waere eine zweite Wahrheit (jetzt nur in der
Datendatei, Rueckfall 0 = laeuft nie ab); `kampf` steht in `ohne_ablauf` und kann darum nie verschoben werden -
die Verschiebe-Regel gilt fuer den Typ `verlust`, Kampfberichte bleiben fuer immer.

**Naechster Schritt:** voller Sammellauf 1, danach S1b (vier Menue-Teilgeschichten).

---

# STAND 06.11.2026, 03:02 - S0 gerechnet: fuenf Tabellen mit Rechenweg (Register 249)

> Neuester Block. Register 249, Protokollzeile 03:00. Kopf beim Schreiben: `14b6cb9`; der Commit dieses
> Schnitts folgt. Der Block 02:30 darunter haelt den Nachtauftrag. **Nachtlauf laeuft.**

**Was dieser Schnitt geaendert hat:** S0 ist gerechnet, nicht geschaetzt. `tools/s0_tabellen.py` liest
`data/baupreise.json`, `data/buildings.json`, `data/units.json`, `data/resources.json` und
`data/originalkarten/katalog.json` und schreibt `docs/S0_TABELLEN_20261107.md` (139 Zeilen, fuenf
Tabellen mit Rechenweg und Urteil).

| Tabelle | Kernzahl | Urteil |
|---|---|---|
| V-1 Reparatur | je Prozentpunkt 16*Stufe/100 Holz und Stein; 0 auf 100 = Wallpreis mal Stufe; 200 s echt | ABGELEITET |
| V-2 Heilung | 75 Prozent der `kosten` ohne `siedler` und ohne `waren`; Dauer 600 s bei Stufe 1 | ABGELEITET |
| V-3 Ruhm | Ansiedler 0 / Freisiedler 10 / Fuerst 40 / Herrscher 160 Punkte | VORSCHLAG |
| V-4 Ereignisse | mittleres Dorf je Spieltag: 1980 Holz, 1027 Stein, 1720 Nahrung, 128 Gold | ABGELEITET |
| V-5 Rache | 90 SK (Wallstufe 3), mit Reserve 99 SK | ABGELEITET |

**Befund beim Rechnen (wichtig fuer S3):** der Wortlaut "75 Prozent aller Kostenposten" haette auch
`siedler` getroffen - eine geheilte Einheit bindet ihren Siedler aber weiter, das waere eine
Doppelbindung. Siedler sind darum ausgenommen; die Regel steht in der Tabelle.

**Naechster Schritt:** S1 Postfach-Archiv und Ruhm-Balken (Block 2 des Nachtauftrags), danach S1b, S2.

---

# STAND 06.11.2026, 02:30 - Nachtauftrag festgelegt: fester Ablauf S0 bis S4, selbststaendig, Budget 4,00 USD (Register 246)

> Neuester Block. Register 246, Protokollzeile 02:20. Kopf beim Schreiben: `6e565c0` (gepusht, Remote
> gelesen); der Commit dieses Schnitts folgt. Der Block 02:00 darunter haelt die Auswertung der
> Gemini-Antworten. **Diese Sitzung endet hier; die naechste arbeitet die Nacht durch.**

**Was dieser Schnitt geaendert hat (nur Dokumente):** Daniel hat den Nachtauftrag freigegeben und sieben
Fragen beantwortet; die Uebergabe 02:30 enthaelt den festen Ablauf, an dem sich die naechste Sitzung
entlang arbeitet. **Gebaut ist weiterhin nichts.**

| Nr. | Schritt | Beleg |
|---|---|---|
| A | Sieben Antworten woertlich festgehalten | `docs/ENTSCHEIDUNGEN_DANIEL_20261106_GEMINI_ANTWORTEN.md`, Abschnitt Runde 3 |
| B | Fester Ablauf in neun Bloecken (0 Sitzung aufsetzen, 1 S0 Tabellen, 2 S1, 3 S1b, 4 S2, 5 S3, 6 S4 Teil 1, 7 Morgenbericht) | Uebergabe `UEBERGABE_NEBELSEETAL_20261106_0230.md`, Abschnitt 3 |
| C | Betriebsgrenzen festgeschrieben: ein Sammellauf je 20 bis 25 Minuten, nichts parallel, Push mit `GIT_ASKPASS` und drei Versuchen, kein Force-Push, keine EXE-Bauten | ebd. Abschnitt 5 |
| D | Drei erlaubte Abbruchgruende definiert (roter Lauf nach zwei Versuchen, echter Widerspruch, Budget oder 07:40) | ebd. Abschnitt 6 |
| E | **Modellbudget 4,00 USD** (0,25 USD je Aufruf), Skill-Freigabe pauschal erteilt | ebd. Abschnitte 4 und 10 |
| F | Dokumentwachen | `test_textqualitaet`, `test_protokoll`, `test_projektpfade`, `test_zieluebergabe` |
| G | **Externen-Info als Block 7 aufgenommen:** `Nebelseetal_Infos_ExterneKI.txt` auf dem Desktop, von einem grossen Modell erstellt, erst wenn alle Schritte geplant sind, bleibt dauerhaft liegen | Uebergabe 02:30, Block 7; Register 247 und 248 (Links zum Repo, aber ohne Zugriffsannahme) |

## Der EINE naechste Schritt

**Block 0 der Uebergabe: Sitzung aufsetzen** (Zieluebergabe pruefen, die vier Skill-Vormerkungen
`9a7f3335`, `5797a0fc`, `9120cc35`, `36452699` speichern und protokollieren), **dann Block 1: S0, die
fuenf gerechneten Tabellen** (Reparaturpreis je Wallstufe, Heilungspreis je Einheit, Ruhm-Raenge,
Ereigniszahlen, Rache-Schwelle) in `docs/S0_TABELLEN_20261107.md`. Danach ohne Rueckfrage weiter mit
**S1 Postfach und Ruhm-Balken**, **S1b vier Menue-Teilgeschichten**, **S2 Mauerreparatur**; S3 und S4
Teil 1 nur, wenn die Zeit reicht. Jeder Block endet mit Wache, vollem Sammellauf, Register, Protokoll,
Stand-Block, Commit und Push.

**Geld (von Daniel abgelesen, nicht geschaetzt):** 11,61 USD Guthaben, Gesamtverbrauch 58,38 USD
(Ablesung 06.11.2026, 02:12). Fuer die Nacht sind **hoechstens 4,00 USD** Modellaufrufe freigegeben
(Daniels Entscheidung 4); danach wird lokal weitergearbeitet.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf auf `main` | `6e565c0` (danach der Commit dieses Schnitts) | `git log --oneline -1` |
| Pruefdateien / Module | 179 / 60 | `ls tests/test_*.py`, `ls src/*.py` |
| Register / Protokoll / Stand-Bloecke | 248 (hoechste Nummer) / 296 (`wc -l`) / 94 | Zaehlung |
| Entscheidungen Daniels | 25 in drei Runden | drei `ENTSCHEIDUNGEN_DANIEL_20261106_*.md` |
| Nachtziel | S1, S1b, S2 mindestens; S3 und S4 Teil 1 bei Zeit; S5 gesperrt | Uebergabe 02:30, Abschnitt 3 |
| Wachen dieses Schnitts | Dokumentpruefungen gruen, kein Sammellauf noetig | Laeufe dieser Sitzung |

# STAND 06.11.2026, 02:00 - Gemini-Antworten geprueft, Plan S0 bis S5 steht, nichts gebaut (Register 244)

> Neuester Block. Register 244, Protokollzeile 01:59. Kopf beim Schreiben: `e86a0ee`; der Commit
> dieses Schnitts folgt. Der Block 00:57 darunter haelt die Auswertung des Gemini-Inputs, der Block
> 23:28 A1.

**Was dieser Schnitt geaendert hat (nur Dokumente, kein Code):** fuenf Antworten und die Menue-Teilgeschichten von Gemini und sein
Arbeitsweise-Feedback liegen hashgeprueft im Projekt und sind Zeile fuer Zeile gegen den Code geprueft;
Daniels neun Entscheidungen dazu sind festgehalten; der Abarbeitungsplan S0 bis S5 steht; die Uebergabe
fuer die naechste Sitzung ist geschrieben. **Gebaut ist nichts.**

| Nr. | Schritt | Beleg |
|---|---|---|
| A | Fuenf Antworten + Feedback abgelegt (hashgeprueft), fuenf Auftraege aus dem Desktop geraeumt | `docs/eingaenge/GEMINI_ANTWORTEN_20261106/`, `docs/auftraege/20261106/` |
| B | Neun Antworten Daniels woertlich mit Folge | `docs/ENTSCHEIDUNGEN_DANIEL_20261106_GEMINI_ANTWORTEN.md` |
| C | Jede Antwort gegen den Code geprueft: vier Codefehler und ein Rechenfehler belegt | `docs/PRUEFVERMERK_GEMINI_ANTWORTEN_20261106.md` |
| D | Abarbeitungsplan: S0 fuenf Tabellen, dann S1 bis S5, Etappen gesperrt bis A2 | `docs/PLAN_GEMINI_UMSETZUNG_20261106.md` |
| E | Uebergabe 02:00 geschrieben und abgelegt | Desktop + `D:\Arbeiten\Hermes\Uebergaben\20261106_0200\` |
| F | Dokumentwachen (kein Code angefasst, daher kein Sammellauf) | `test_textqualitaet`, `test_protokoll`, `test_projektpfade`, `test_zieluebergabe` |
| G | **Geminis Menue-Teilgeschichten geprueft (Register 245):** vier brauchbar, der Ton passt bei keinem (story.json: leicht, kein Pathos), zwei Antworten sind Mechaniken | `docs/PRUEFVERMERK_GEMINI_MENUESTORIES_20261106.md`, Plan-Abschnitt **S1b** |

## Der EINE naechste Schritt

1. **S0: fuenf gerechnete Tabellen** (Reparaturpreis je Wallstufe, Heilungspreis je Einheit,
   Ruhm-Schwellen, Ereigniszahlen, Rache-Schwelle), jede mit Rechenweg und Urteil - Daniel vorlegen,
   erst nach seinem Abnicken bauen.
2. **Dann S1: Postfach-Archiv (Filter, Archiv, Ablauf) und Ruhm-Balken.** Messlage: `_render_messages`
   (`src/main.py:13379`) zeigt nur die letzten 20 Eintraege; `punkte.auszeichnungen`
   (`src/punkte.py:417`) rechnet vier Auszeichnungen, ein Balken fehlt.
3. **Nach jedem Schnitt:** Registerzeile, Protokollzeile, Stand-Block, voller Sammellauf, commit und push.

**Geld (von Daniel abgelesen, nicht geschaetzt):** 11,61 USD Guthaben, Gesamtverbrauch 58,38 USD
(Ablesung 06.11.2026, 02:12; vorige Ablesung 11,86 / 58,13 - Differenz 0,25 USD, beide Quellen stimmen). In diesem Schnitt **kein bezahlter Modellauf**; die 4,00 USD fuer das
grosse Modell sind unangetastet und fuer S0/S1 nicht noetig.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf auf `main` | `e86a0ee` (danach der Commit dieses Schnitts) | `git log --oneline -1` |
| Pruefdateien / Module | 179 / 60 | `ls tests/test_*.py`, `ls src/*.py` |
| Register / Protokoll / Stand-Bloecke | 245 / 291 (`wc -l`) / 93 | Zaehlung |
| Gemini-Unterlagen | 5 Antworten + 1 Feedback, 5 Auftraege | Projektordner `docs/eingaenge/GEMINI_ANTWORTEN_20261106/`, `docs/auftraege/20261106/` |
| Offene Vorarbeit | 5 Tabellen (S0), 1 Mechanikfrage (Durchmarschrecht) | `docs/PLAN_GEMINI_UMSETZUNG_20261106.md` |
| Wachen dieses Schnitts | Dokumentpruefungen gruen, kein Sammellauf noetig | Laeufe dieser Sitzung |

# STAND 06.11.2026, 00:57 - Gemini-Input ausgewertet: gefiltert, geprueft, 16 Rohdateien archiviert, Projekt-Dokumente liegen (Register 242)

> Neuester Block. Register 242 und 243, Protokollzeilen 00:57 und 01:31. Kopf beim Schreiben: `3c5189a` (gepusht, Remote
> gelesen); der Commit dieses Schnitts folgt danach. Der Block 23:28 darunter haelt A1, der Block 19:25
> die Spieltests und W1.

**Was dieser Schnitt geaendert hat (nur Dokumente und Ablage, kein Code):** Daniels Auftrag aus
Abschnitt 3a der Uebergabe ist abgearbeitet - der Gemini-Input ist gegen den Code geprueft, das
Unbrauchbare liegt im Archiv, und im Projekt liegt eine Fassung, aus der gearbeitet werden kann.
**Aus dem Gemini-Input ist NICHTS uebernommen.**

| Nr. | Schritt | Beleg |
|---|---|---|
| A | Jede Aussage der Sammlung gegen Code und Daten gemessen (Datei und Zeile, oder Zahl mit Befehl) | Messungen dieser Sitzung, in den Dokumenten je Zeile als Beleg |
| B | **Vier Urteile der Vorsitzung widerlegt** - Dimensionen (6 statt 20, `_schnitt_w6`), Bots greifen die Spielersiedlung an (`main.py:6896`), Weltensprung gesperrt (`main.py:10857`), Rache-Gedaechtnis vorhanden (`bottaktik.py:345/483/566`) | `04_LUECKEN.md` Abschnitt 1 |
| C | **16 von 29 Rohdateien** nach `02_ARCHIV` verschoben, Hashes vor und nach dem Verschieben gleich; 13 Bloecke bleiben in `00_ROH` | `02_ARCHIV/README_ARCHIV.md`, Ausgabe des Verschiebeskripts |
| D | Projekt-Fassung geschrieben: `00_README`, `01_BRAUCHBAR` (B-1 bis B-10), `02_TEILWEISE` (T-1 bis T-7), `03_ABGELEHNT`, `04_LUECKEN`, `05_BEWERTUNG` | `docs/eingaenge/GEMINI_INPUT_20261106/` |
| E | Bewertung: sechs Stuecke zum Uebernehmen, fuenf teilweise, drei fallen weg, weil der Code die Frage beantwortet | `05_BEWERTUNG.md` Abschnitte A bis C |
| F | Neun Entscheidungen fuer Daniel gesammelt (eine Runde, nicht verstreut) | `docs/FRAGEN_AN_DANIEL_20261106_GEMINI.md` |
| G | Sammlung im Eingangsordner nachgezogen (Nachtrag in `VERWERTUNG.md` und `SAMMLUNG_UEBERSICHT.md`, drei Zeilen als KORREKTUR/WIDERLEGT/ERLEDIGT markiert) | Eingangsordner `20261105_GoogleKI_Ideensammlung` |
| H | Dokumentwachen gefahren, weil nur Dokumente geaendert wurden - **kein** Sammellauf noetig | `test_textqualitaet`, `test_protokoll`, `test_projektpfade`, `test_zieluebergabe` |

## Der EINE naechste Schritt

1. **Die Entscheidungsrunde aus `docs/FRAGEN_AN_DANIEL_20261106_GEMINI.md`** (neun Punkte, ein
   Formular). Ohne Antwort wird aus dem Gemini-Input nichts gebaut - Rangfolge Register 238.
2. **Spielseitig danach A1b:** `tools/spieltest_simulation.py` prueft vor dem Versuch (Lesestellen
   `einheit_bedingungen`/`ware_bedingungen` mit `schritt`), Zielzahl Fehlversuche < 50. Danach **A2**
   Messpflicht-Tabelle.
3. **Unabhaengig davon weiterlaufend:** nach jedem Schnitt Registerzeile, Protokollzeile, Stand-Block,
   voller Sammellauf, commit und push.

**Geld (von Daniel abgelesen, nicht geschaetzt):** 11,86 USD Guthaben, Gesamtverbrauch 58,13 USD
(Ablesung 06.11.2026 00:33). In diesem Schnitt **kein bezahlter Modellauf** - die 4,00 USD fuer das
grosse Modell sind unangetastet und werden erst nach der Filterung sinnvoll eingesetzt.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf auf `main` | `3c5189a` (danach der Commit dieses Schnitts) | `git log --oneline -1` |
| Pruefdateien / Module | 179 / 60 | `ls tests/test_*.py`, `ls src/*.py` |
| Register / Protokoll / Stand-Bloecke | 243 / 289 (`wc -l`) / 92 | Zaehlung |
| Sammlung | 29 Rohbloecke eingegangen, **13 in `00_ROH`**, 16 in `02_ARCHIV`, 8 Auszuege, 80 Urteilszeilen | Eingangsordner |
| Projekt-Fassung | sechs Dokumente, sechs zum Uebernehmen, fuenf teilweise, neun Entscheidungen | `docs/eingaenge/GEMINI_INPUT_20261106/` |
| Wachen dieses Schnitts | Dokumentpruefungen gruen (kein Code angefasst) | Laeufe dieser Sitzung |

# STAND 05.11.2026, 23:28 - A1 gebaut: Voraussetzungen stehen im Spiel, jede einzeln mit naechstem Schritt (Register 241)

> Neuester Block. Register 241, Protokollzeile 23:28. Kopf beim Schreiben: `33426b6`; der Commit
> dieses Schnitts folgt. Der Block 19:25 darunter haelt Spieltests und W1, der Block 17:40 die
> Veroeffentlichung 0.0.1.

**Was dieser Schnitt geaendert hat (reine Anzeige, kein Balancing):** der Spieler sieht an einer
gesperrten Aktion JEDE offene Bedingung einzeln und darunter, was zu tun ist. Vorher nannte die
Kaserne nur die erste Bedingung (die Forschung); die Ausruestung kam erst nach der Forschung ans
Licht - genau diese Reihenfolge kostete in L3/L4 283+156+82 Fehlversuche an Kurzschwertern und 488
blockierte Ausbildungen.

| Nr. | Schritt | Beleg |
|---|---|---|
| A | Messlage vorher: Kaserne nennt je Einheit EINE Bedingung, Werkstatt-Knopf nur grau | Sonde `cache/scratch/sonde_voraussetzungen2.py`, Log `sonde_voraus2.log` |
| B | Neue Lesestellen `spieloekonomie.einheit_bedingungen`, `ware_bedingungen` (mit mitgegebenem Bestand), `forschung_schritt`, `_ort_wert` | `test_voraussetzungsanzeige` 24/0/0 |
| C | Kaserne: Grund nennt jede Bedingung, darunter je Bedingung der Schritt - Forschung mit Holz und Spielstunden, Ware mit Werkstatt und Grund, Siedler mit Haus | Ansicht gerendert im Test, Abschnitt 6 |
| D | Werkstatt: der gesperrte Knopf traegt seinen Grund, die Begruendungszeile nennt den naechsten Schritt | ebd. (Knopftext „Kurzschwert: Waffentechnik Stufe 3 (erreicht: 2)“) |
| E | Kein zweiter Rechenweg: `ausruestung.fehlende` ist aus dem Hindernis verschwunden, alles laeuft ueber die eine Lesestelle (F-04) | Quelltext-Wache, Abschnitt 5 |
| F | Zeichnen nicht langsamer: 20 x Kaserne 4,9 s, 20 x Lager 7,6 s | eigene Messung nach dem Zusammenfassen der Zeilen |
| G | Voller Sammellauf nach dem Schnitt | `docs/audits/sammellauf_20261105_2315.log`: **176 von 179 gruen, 1 rot**, 7307 Pruefungen, 1319 s |
| H | Flatternder Rotfall: `test_gesamtsieg` 46/1/0 (Gefecht wuerfelt, zwei Verteidiger flohen ohne Verlust), sonst 10 von 11 Einzellaeufen gruen | Pruefdatei wuerfelt jetzt mit festem Startwert 4711 - danach 8 von 8 gruen (47/0/0) |
| I | Zwei Irrwege, beide behoben: alte `Nebelseetal_Pre_Release_V_0.0.1.exe` im Projektordner (Wache rot, nicht der Code) und eine eigene Messung WAEHREND des Laufs davor (Zeitlimit) | EXE hashgleich `efaf403b9446...` nach `archiv/altstaende/`; der dritte Lauf lief ohne Nebenarbeit |

## Der EINE naechste Schritt

1. **A1b: die Spieltest-Simulation prueft VOR dem Versuch.** Sie ist der Spieler im Messlauf und
   drueckt heute Knoepfe, die im Spiel gesperrt sind. Mit denselben zwei Lesestellen
   (`einheit_bedingungen`, `ware_bedingungen`) kann sie stattdessen den naechsten Schritt gehen
   (Forschung starten, Ware herstellen) und nur zaehlen, was WIRKLICH scheitert. Erst dann bewegt
   sich die Zielzahl des Arbeitsplans (Fehlversuche < 50). Danach **A2** Messpflicht-Tabelle
   (Spieltage bis Gebaeude n / Forschung n / erste Einheit / erster Weltwechsel / voll ausgebaut).
2. Offene Knoepfe: Ausbau am Stufenlimit und belegte Bauplaetze sperren (874 Fehlversuche waren der
   Anlass) - eigener kleiner Schnitt, sobald A1b gemessen ist.
   Zum Abschluss eines jeden Schnitts: Registerzeile, Protokollzeile, Stand-Block, voller
   Sammellauf, commit und push.

**Geld (von Daniel abgelesen, nicht geschaetzt):** 12,09 USD Guthaben, Gesamtverbrauch 57,90 USD
(Ablesung 05.11.2026 22:10). In diesem Schnitt wurde KEIN bezahlter Modellauf gefahren - die 4,00 USD
fuer das grosse Modell sind unangetastet. Sie sind fuer A1b/B1 vorgesehen; bei Anzeigetexten ist ein
blinder Modell-Patch teurer als die direkte Aenderung (Begruendung: der Patch haette gegen die
15.000-Zeilen-Datei geraten werden muessen).

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf auf `main` | `33426b6` (danach der Commit dieses Schnitts) | `git log --oneline -1` |
| Pruefdateien / Module | 179 / 60 | `ls tests/test_*.py`, `ls src/*.py` |
| Register / Protokoll / Stand-Bloecke | 241 / 288 / 91 | Zaehlung |
| Wachen dieses Schnitts | `test_voraussetzungsanzeige` 24/0/0, `test_anzeigetexte_umlaute` 49/0/0, `test_textqualitaet` 492/0, `test_projektpfade` 123/0, `test_durchspiel` 65/0/2, `test_ware_voraussetzung_eine_quelle` gruen | Laeufe dieser Sitzung |


# STAND 05.11.2026, 19:25 - Zwei Spieltest-Laeufe bezahlt und bewertet, Messgeraet repariert (Register 232/233)

> Neuester Block. Register 232 und 233, Protokollzeilen ab 19:20. Kopf beim Schreiben: `fa8e27c`,
> Arbeitsbaum sauber. Der Block 17:40 darunter haelt die Veroeffentlichung, der Block 15:40 die
> Entscheidungen aus Register 228.

**Der Ablauf dieser Runde, ehrlich:** der erste Simulationslauf nach der Uebergabe wurde NICHT
bezahlt - er zeigte 0 Einheiten und 0 Kaempfe. Erst die Ursachen (drei Stueck, alle im Messgeraet)
beheben, dann die zwei Laeufe fahren.

| Nr. | Schritt | Beleg |
|---|---|---|
| A | Erster Lauf geprueft, bevor Geld floss: 0 Einheiten, 0 Kaempfe, kein Grund im Bericht | Sonde: die Werkstatt-Schlange stand auf `dauer: None` |
| B | **Ursache 1:** `spielschicht.ware_fertigen` gab die Rezepte nicht weiter -> jede Ware ohne belegte Handbuchdauer wurde nie fertig (93 Kurzschwerter eingereiht, keine angekommen) | behoben, `test_spielschicht` **137/0/1** (6 neue Pruefungen, mit Kurzschwert statt Schwert) |
| C | **Ursache 2:** Baukette baute nie ein Haus (`wohnhaus` ist keine Kennung) und hatte keine Schafszucht, keinen Stellmacher, keine Erzmine -> keine Einheit, kein Kampf | behoben, `test_spieltest_erreicht_kampf` **16/0/0** (neu) |
| D | **Ursache 3:** Fehlversuche wurden still verschluckt; jetzt Grundbilanz im Bericht (Stelle, Anzahl, Grund) | Abschnitt im Lauf 1 |
| E | Lauf 1 (Stil breit, 8 Tage, Saat 7) + Modellurteil | 5 Einheiten, 2 Gefechte, 19 Punkte; `SPIELTEST_BEWERTUNG_20261105_L1.md`, **0,0305 USD** |
| F | Lauf 2 (Stil krieg, 10 Tage, Saat 23) + Modellurteil | 7 Einheiten, 5 Gefechte, 40 Punkte; `SPIELTEST_BEWERTUNG_20261105_L2.md`, **0,0333 USD** |
| G | Befunde verwertbar formuliert (7 Befunde, 4 Grenzen, Reihenfolge der naechsten Schnitte) | `docs/SPIELTEST_BEFUNDE_20261105.md` |
| H | Werkzeugbefund: `gesamtaudit_lauf.py --paket <pfad>` ignoriert den Pfad und sendet das volle Dossier | richtig ist `--paket --dossier <pfad> --ziel <datei>` (8.017 statt 129.371 Zeichen) |
| I | **Voller Sammellauf ueber den ganzen Stand** | 1.221 s: 176/178, 0 rot, 7.276 Pruefungen — und nach W1 nochmals **176/178, 0 rot, 7.284 Pruefungen, 1.353 s** (`docs/audits/sammellauf_20261105_1958.log`) |
| J | **W1 gebaut (Daniel 19:47): Waren kosten im Kern-Weg Geld UND Forschung** | `ware_fertigen` prueft ueber `spieloekonomie.ware_voraussetzung`, bucht Rezeptkosten atomar, Rueckbuchung bei Ablehnung; `test_spielschicht` **142/0/1** |
| K | **Angriff ohne Karren erlaubt, Beute dann 0** (Daniel 19:47) | Der Kern liess das immer zu (Karrenladung ist die Grenze), blockiert hatte nur die Simulation; Wache `test_spieltest_erreicht_kampf` **19/0/0**, Abschnitt 5 |
| L | Zwei NEUE Laeufe mit dem korrigierten Geraet bezahlt | L3 breit 10 Tage: 35 Punkte, 5 Gefechte, 0,0349 USD; L4 krieg 12 Tage: 40 Punkte, 11 Gefechte, 0,0362 USD; beide Urteile nennen **Waffentechnik Stufe 3** als Engstelle |
| M | **Version 0.0.2 gebaut, am Bildschirm geprueft, veroeffentlicht** (Daniel 19:47) | EXE 86.984.365 Byte, SHA256 `c9b45703ee12...`, ZIP 86.702.517 Byte; Release `v_0.0.2` am Commit `af2b272`, beide Assets, Passwortsperre im Bild, 0 Prozesse, `game.lock` entfernt |
| N | **Daniels Antworten der Uebergaberunde 21:15** (Register 236, `docs/ENTSCHEIDUNGEN_DANIEL_20261105_2115.md`) | 1) Voraussetzungen sichtbar zuerst; 2) grosses Modell liefert **fertige Pakete** (Code/Patches mit Wache); 3) **Modell-Budget 4,00 USD**; 4) Mana erst MESSEN, dann Kosten senken und Produktion erhoehen; 5) Forschungsdauern/-kosten senken (Quellen pruefen); 6) Start-Holz bleibt Originalzahl. **Mana-Messlage belegt:** Tempel 120 Mana/Spieltag, Weltwechsel 5.000 = ~41,7 Spieltage, Drachenjagd ~250 Spieltage |
| O | **Leitlinie Spielfluss: es muss ein Aufbauspiel bleiben** (Daniel 21:25/21:27, Register 237) | Aufbau bleibt der Kern, Springen und Kaempfen machen ihn nur erreichbar; wer Dauern/Kosten senkt, nennt in derselben Rechnung, wo die Zeit wieder gebunden wird; Messpflicht-Tabelle vorher/nachher; eine Verkuerzung des Aufbaus wird Daniel vorgelegt |
| P | **Rangfolge der Quellen neu und Entwicklungsablauf in sieben Phasen** (Daniel 21:43, Register 238/239) | `docs/ENTWICKLUNGSABLAUF_AB_20261105.md`: 1 Gesamtbalancing, 2 Daniels Entscheidung, 3 Original als RICHTWERT, 4 Vorschlag; Phasen 0 bis 7 mit Fertig-Kriterien und sechsteiliger Entscheidungsliste; kein Code vor der schriftlichen Entscheidung, Modell liefert fertige Pakete |
| Q | **Das Spiel als Ganzes vorgelegt: Mechanik-Landkarte, Bot-Ist-Stand, Arbeitsplan** (Daniel 22:00, Register 240) | `docs/GESAMTBILD_SPIEL_20261105.md` (15 Mechaniken, drei Spannungsboegen, Bot-Luecken mit Belegen, Zielbild, Ommage-Leitplanke) und `docs/ARBEITSPLAN_AB_20261105.md` (Stufen A bis D, 16 Stuecke mit Messzahl und Abhaengigkeit); gemessen: 74 `bot_*`-Funktionen, 69 davon in `main.py`, 29 Bot-Wachen |

**Geld:** 0,0305 + 0,0333 + 0,0349 + 0,0362 = **0,1349 USD gemessen** (ein L4-Versuch lief leer und
wiederholte sich einmal; dessen Kosten stehen nicht in der Abrechnung des Werkzeugs). Von den 3,16 USD
der Freigabe sind damit rund **3,02 USD frei**. Guthaben bei Daniel: 12,48 USD (Ablesung 19:48).

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf auf `main` | `af2b272` (Code dieses Schnitts, danach die Doku-Commits) | `git log --oneline -1` |
| Pruefdateien / Module | 178 / 60 | `ls tests/test_*.py`, `ls src/*.py` |
| Register / Protokoll / Stand-Bloecke | 279 / 287 / 90 | Zaehlung |
| Einzelwachen dieses Schnitts | `test_spielschicht` 142/0/1, `test_spieltest_erreicht_kampf` 19/0/0, `test_textqualitaet` 483/0, `test_projektpfade` 123/0, `test_zieluebergabe` 26/0/0 | Laeufe dieses Schnitts |
| Spieltest-Laeufe | 4 bezahlt (L1 bis L4); L3/L4 ohne Tick-Fehler | `docs/audits/SPIELTEST_LOG_20261105_L3_breit10.md`, `..._L4_krieg12.md` |
| Spieltest-Kosten | 0,0638 (L1/L2) + 0,0711 (L3/L4) = **0,1349 USD**, rund 3,02 USD der Freigabe frei | `gesamtaudit.log` |

## Der EINE naechste Schritt

0. **Phasen 0 bis 3 VOR dem Bauen** (Daniel 21:43, `docs/ENTWICKLUNGSABLAUF_AB_20261105.md`):
   messen (Phase 1), Zielbild mit Messzahl (2), EINE Entscheidungsrunde (3) — erst danach Paket und
   Einbau. Fuer den naechsten Schnitt heisst das: Zielzahl notieren (wie viele Fehlklicks soll die
   Voraussetzungsanzeige auf 0 bringen), dann bauen.
1. **Voraussetzungen sichtbar machen (B3/B4/B7)** — der einzige Punkt, den BEIDE Urteile unabhaengig
   nennen: 283+156+82 Kurzschwert- und 488 Kaempfer-Fehlversuche in L3, 516/491 in L4. Dazu gehoert
   die Anzeige Waffentechnik 3 (aktuell 2), Schmiede bauen, Lederrüstung produzieren und das
   Sperren wirkungsloser Knoepfe. Reine Anzeige, kein Balancing - und die Wache dazu ist
   `test_anzeigetexte_umlaute`.
2. **Kampfziel aus einem echten Bot-Dorf (B5)** — sonst bleibt der Kampf nicht beurteilbar (jedes
   Gefecht 16/10/12 Beute, 0 Verluste in allen Laeufen).
3. **Mana-Kette (B6)** — Mana ist in 12 Spieltagen 0. Kein Wert erfinden: offene Frage an Daniel, ob
   Tempel/Paladin im Messzeitraum vorkommen sollen.
4. **Version 0.0.2 veroeffentlichen** (Daniel 19:47): nach dem gruenen Sammellauf bauen, am Bildschirm
   pruefen, Release mit Notizen, Repo aktuell halten.
   Zum Abschluss eines jeden Schnitts: Registerzeile, Protokollzeile, Stand-Block, dann Sammellauf.

**Weiter offen:** Saat wirkungslos (feste Startkarte) - Verlaeufe unterscheiden sich nur ueber
`--stil`; Kampfziel ist ein fixes synthetisches Dorf; Mana und Pferde kommen in keinem Lauf vor;
Forschungsdauer je Stufe (Waffentechnik 3 braucht ~6 Spieltage) ist eine offene Balancing-Frage;
Skill-Nachtrag `laptop-cleanup` und der Nachtrag zu den Spieltest-Laeufen warten auf Daniels
Freigabe (`/skills pending`); Werkzeug-Fix Wagenbau-Stufen in `tools/balancing_messung.py` und die
Bot-Drachenregel stehen weiter offen.



# STAND 05.11.2026, 17:40 - Erste veroeffentlichte Fassung `Nebelseetal_Pre_Release_V_0.0.1.exe` gebaut, geprueft, Null-Zustand vorbereitet

> Neuester Block. Register 230, Protokollsektion HERMES-RELEASE-230. Kopf beim Schreiben: `a5fac01`,
> Commit dieses Schnitts danach.

**Was seit dem letzten Block passiert ist:**

| Nr. | Schritt | Beleg |
|---|---|---|
| A | Voller Sammellauf fuer den Stand nach Register 228 | **174 von 176 gruen, 0 rot**, 7.239 Pruefungen, 1257 s (`docs/audits/sammellauf_20261105_1630.log`) |
| B | **Befund:** das Bauwerkzeug las den Namen nie aus `data/version.json` | `tools/build_exe.py` neu mit `release_name()`; `tools/build_public_exe.py` zieht Name UND Version aus derselben Datei |
| C | Entwickler-EXE gebaut | `Nebelseetal_Pre_Release_V_0.0.1.exe`, 86.978.803 Byte, SHA256 `efaf403b9446...` |
| D | Veroeffentlichungs-EXE gebaut, Paket LEER | 86.983.205 Byte, SHA256 `f9ef7aaa14b0...`, `--pruefen` gruen, Demo-Speicherordner ohne Spielstand |
| E | Start am Bildschirm geprueft | Fenster + **Passwortsperre** im Bild belegt; beendet ueber die Fenster-PID, 0 Prozesse, verwaiste `game.lock` gesichert und entfernt |
| F | GitHub-Null-Zustand vorbereitet | kein gemeinsamer Vorfahre (lokal 619 / Remote 10 Commits); Remote-Stand als Tag `vor-nullzustand-20261105`, `index.html` unveraendert uebernommen |

**Nachtrag 18:05 - Push und Veroeffentlichung sind belegt:** der Token war gueltig (`ghp_`, push und
admin), der Haenger kam vom Credential-Helper - mit `GIT_ASKPASS` (Token aus der Credential-Datei,
nie auf der Kommandozeile) ging es sofort. `main` steht auf `2048ec6` (forced update von `63639d5`),
die alte Remote-Historie liegt als Tag `vor-nullzustand-20261105` auf GitHub, das Pre-Release
`v_0.0.1` ist **oeffentlich** (draft false, prerelease true) mit dem ZIP **86.701.024 Byte**
(Download-HEAD 200, Groesse stimmt) und den Release-Notizen (3.043 Zeichen).

**Weiter offen:** die Spieltest-Laeufe mit 3,16 USD sind nicht gestartet; die Session-Wache fuer
Cron-Jobs ist gebaut und der Cleanup-Bot wieder aktiv, der Skill-Nachtrag wartet auf Daniels Freigabe.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf auf `main` | `a5fac01` beim Schreiben | `git log --oneline -1` |
| Pruefdateien / Module | 176 / 60 | `ls tests/test_*.py`, `ls src/*.py` |
| Register / Protokoll | 269 / 278 Zeilen | Zaehlung |
| Voller Sammellauf | **gruen** (174/176, 0 rot, 1257 s) | `docs/audits/sammellauf_20261105_1630.log` |
| Entwickler-EXE | `Nebelseetal_Pre_Release_V_0.0.1.exe`, 86.978.803 Byte, SHA256 `efaf403b9446...` | `docs/audits/exe_bau_20261105_1705.log` |
| Veroeffentlichung | `release_public/Nebelseetal_Pre_Release_V_0.0.1.exe` + `.zip`, SHA256 `f9ef7aaa14b0...` | `docs/audits/public_bau_20261105_1725.log` |
| Guthaben (Daniel 15:06) | 13,16 USD Stand; 3,16 USD fuer Spieltests freigegeben, **nicht verbraucht** | Ablesung |

## Der EINE naechste Schritt
1. **GitHub-Push des Null-Zustands** (Tag `vor-nullzustand-20261105` zuerst, dann `main`; kein normaler
   Push moeglich, weil die Historien keinen gemeinsamen Vorfahren haben) und Release-Notizen als
   Pre-Release veroeffentlichen.
2. **Ein bis zwei Spieltest-Laeufe** (3,16 USD freigegeben) mit verschiedenem Verhalten; das Paket
   braucht die Skip-Anweisung, damit ein gescheiterter Test den Lauf NICHT beendet.
3. Danach das Repo **laufend aktuell halten** (Daniel 05.11.2026) und jede neue Spielversion
   ankuendigen.

# STAND 05.11.2026, 15:40 - Register 228 GEBAUT: Startkarte fest, erstes Dorf ab sechs Siedlungen, Bots geben mit Ruecklage auf

> Neuester Block. Der Block darunter (15:25) haelt die ENTSCHEIDUNGEN fest; dieser Block den gebauten
> Stand. Kopf beim Schreiben: `8e0e63f` (danach committet), Arbeitsbaum sauber. Protokollsektion
> HERMES-STARTSEITE-228, Register 229.

**Gebaut und einzeln belegt:**

| Nr. | Schnitt | Was gebaut ist | Beleg |
|---|---|---|---|
| A | Startkarte FEST | `_startkarte_ziehen` gibt fuer die erste Siedlung die belegte Standardkarte (`original-036`), gezogen wird nur bei Neugruendungen; `startkarte_gewaehlt` leer = Standardkarte (EINE Lesestelle) | `test_startkartenwahl` **28/0/0** |
| B | Bots Hauptdorf | `bot_doerfer_karten_zuweisen` setzt fuer das Hauptdorf `originalkarten.START_ID` - jeder Bot startet wie der Spieler | `test_bot_gruendung` 36/0/1, `test_kartenwahl_bot` **25/0/0** |
| C | Aufgeben ab sechs | neue EINE Quelle `GameState.aufgeben_grund`: erstes Dorf (Index 0) ab sechs Siedlungen, jedes andere ab zwei, eine einzige nie; Kern, App und Siedlungsliste fragen dieselbe Funktion, die Liste nennt den Grund | `test_startseite` **68/0/0** |
| D | Bots geben auf | `GameState.bot_siedlung_aufgeben`: Ruecklage der Gebuehr VOR dem Aufgeben, Zahlungsfaehigkeit der naechsten Gruendung aus `gruendungskosten()`, Sperre je Bot, Erinnerung an abgelehnte Karten, Abbruch nach drei Aufgaben, nie Haupt- oder letztes Dorf; der Bot-Takt ruft es nach der Gruendung | `test_bot_aufgeben` **45/0/1** (neu) |
| E | Daten und Dokumente | `data/bot_gruendung.json` Block `aufgeben` (24 h Sperre, Erinnerung 1, hoechstens 3), `data/startkarte.json` auf die feste Startkarte umgeschrieben, Register 229, Protokollsektion | `json.load` gruen, Dateien gelesen |

**Zwei alte Wachen sind mit der Entscheidung umgeschrieben, nicht der Code zurueckgebogen:** die
Pruefungen „Urteil vor dem Kauf“ und „kein Aufgeben im Bot-Takt“ sicherten die Uebergangsloesung aus
Register 227; sie pruefen jetzt Ruecklage, Sperre, Erinnerung und Zahlungsfaehigkeit.

**Ehrlich offen:** der volle Sammellauf fuer diesen Stand fehlt noch (Einzellaeufe und Dokumentwachen
sind gruen, das ist kein Sammellauf). Die Zahlen der Bot-Aufgabe (24 h, Erinnerung 1, hoechstens 3)
sind ein VORSCHLAG aus `data/bot_gruendung.json` und ohne Codeaenderung stellbar.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf auf `main` | `8e0e63f` beim Schreiben, Commit dieses Schnitts danach | `git log --oneline -1` |
| Commits | 616 vor dem Commit | `git rev-list --count HEAD` |
| Pruefdateien / Module | 176 / 60 (eine Wache neu) | `ls tests/test_*.py`, `ls src/*.py` |
| Register / Protokoll | 268 / 272 Zeilen | Zaehlung |
| Voller Sammellauf | **OFFEN** (letzter belegter Lauf 12:33: 172 von 174, 1341 s) | - |
| EXE | weiterhin `Nebelseetal_Pre_Release_V0.0.1.exe` - V0.0.2 offen | `data/version.json` |
| Guthaben (Daniel 15:06) | 13,16 USD Stand / 56,83 USD Gesamtverbrauch; davon 3,16 USD fuer Spieltest-Laeufe freigegeben | Ablesung |

## Der EINE naechste Schritt
1. **Voller Sammellauf** mit dem Projekt-venv: `.venv/Scripts/python.exe -X utf8 -u tools/sammellauf.py
   > docs/audits/sammellauf_20261105_<hhmm>.log 2>&1` (~22 min, nicht durch `tail` pipen). Rote
   Dateien einzeln nachfahren. Ein Lauf zaehlt nur, wenn er NACH dem letzten Fix startete.
2. **EXE `Nebelseetal_DemoVersion_V0.0.2.exe`** bauen (`data/version.json` auf 2), am Bildschirm
   pruefen (Fenster und Passwortsperre), ueber die Fenster-PID beenden, `game.lock` aufraeumen.
3. **Upload-Paket und GitHub**: `tools/build_public_exe.py --pruefen`, dann bauen und pushen (kein
   Force, `main` unberuehrt), Release-Notizen mit gekuerzter Ankuendigung der Spieltests.
4. **Ein bis zwei Spieltest-Laeufe** (3,16 USD freigegeben) mit verschiedenem Verhalten; Werkzeug
   braucht eine Skip-Anweisung, damit ein gescheiterter Test den Lauf NICHT beendet.
5. **laptop-cleanup-bot-Cronjob** zuletzt pruefen und wieder aktivieren.

# STAND 05.11.2026, 15:25 — Nachtrag zu Register 228: Daniels Antworten, zwei neue Schnitte vor dem Upload

> Neuester Block, Nachtrag zum Block darunter (15:10). Die Antworten sind AUFGENOMMEN, nicht gebaut.

**Vier Antworten auf die Fragenrunde vor der Uebergabe (Register 228):**

1. **Startkarte wieder FEST:** Spieler UND alle Bots starten mit derselben mittleren Karte
   (`original-036`). Die Zufallsziehung aus Register 227 gilt nur noch fuer NEUGruendungen.
2. **Aufgeben erst mit sechs Siedlungen:** das erste Dorf ist aufgebenbar, sobald sechs Siedlungen
   stehen - dann kann man aus den anderen Doerfern heraus neu gruenden und eine bessere Karte suchen.
   Solange gesperrt, nennt die Anzeige den Grund.
3. **Bots nach Original:** gruenden, beurteilen, aufgeben - aber sie muessen die Kosten erneut
   ansparen koennen. Gefordert ist eine geeignete Loesung gegen den gemessenen Rueckfall von vier auf
   ein Dorf (Ruecklage, Sperre, Erinnerung an abgelehnte Karten).
4. **3,16 USD** fuer ein bis zwei Spieltest-Laeufe mit verschiedenem Verhalten; die Daten muessen
   verwertbar formuliert sein. Ankuendigung im Pre-Release erlaubt, Spieltests NICHT Teil der EXE.

## Der EINE naechste Schritt
1. **Schnitt Register 228 bauen** (Startkarte fest, Freischaltung ab sechs Siedlungen, Bot-Aufgeben mit
   Ruecklage) - das aendert den Startablauf und die Kartenregel aus Register 227, also VOR dem
   Sammellauf und VOR der EXE.
2. Danach voller Sammellauf, dann EXE `Nebelseetal_DemoVersion_V0.0.2.exe`, dann Upload.


# STAND 05.11.2026, 15:10 — Register 222 und 225 GEBAUT; offen sind voller Sammellauf, EXE V0.0.2 und Upload

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen. Der Arbeitsstand ist
> committet (`38912d6`), die Einzellaeufe und die Dokumentwachen sind gruen, der VOLLE SAMMELLAUF
> fuer diesen Stand fehlt noch — er ist der erste Schritt der naechsten Sitzung.

**Gebaut in dieser Sitzung** (Einzelheiten Register 226 und 227, Protokollsektion HERMES-STARTSEITE-222):

| Schnitt | Was gebaut ist | Register | Beleg |
|---|---|---|---|
| Startfenster | Kartengruendungsseite als erste Ansicht, drei Schritte: Seite -> Volk -> Karte -> Gruendung | 226 | `test_startseite` 69/0/0 |
| Fraktion | Wahl EINMAL, danach gesperrt; `ast`-Wache auf genau EINE Zuweisung an `state.spieler_fraktion` | 226 | `test_voelkerwahl` 37/0/0 |
| Goldkosten | 14 Militaereinheiten minus 30 Prozent (Krieger 350 statt 500), belegte Abweichung | 227 | `test_ausbildungsauftraege` 59/0/0, `test_mengeneingabe` 69/0/0 |
| Karte | Zufallsziehung statt freier Wahl (Original `siedeln.php` Zeilen 10-13) | 227 | `test_startkartenwahl` 26/0/0 |
| Loeschen | Siedlung aufgeben: Lager, Einheiten und Bauten verloren, Karte zurueck in den Stapel, nur mit mehr als einer Siedlung | 227 | `test_startseite` |
| Bots | EINE gezogene Karte, Urteil gegen den Durchschnitt der Taktik VOR dem Kauf | 227 | `test_bot_gruendung` 36/0/1, `test_kartenwahl_bot` 25/0/0 |

**Ehrliche Grenze des Schnitts:** beim Spieler ist die Loeschung der Karte das Aufgeben der Siedlung
(Original). Die EINZIGE erste Siedlung laesst sich nicht aufgeben — ohne Siedlung gaebe es keine
Produktion, der Start mit einer schlechten ersten Karte waere ohne Ausweg. Bei den Bots urteilt der
Bot VOR dem Kauf; sein Verlust ist die verlorene Gruendungszeit, nicht der Rohstoff (Begruendung im
Register 227: das Aufgeben nach der Gruendung warf die Bots von vier Doerfern auf eines zurueck).

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf auf `main` | `38912d6` | `git log --oneline -1` |
| Commits | 614 | `git rev-list --count HEAD` |
| Arbeitsbaum | sauber | `git status --porcelain` |
| Pruefdateien / Module | 175 / 60 | `ls tests/test_*.py`, `ls src/*.py` |
| Register / Protokoll | 267 / 266 Zeilen | Zaehlung |
| Einzellaeufe dieser Sitzung | gruen (Tabelle oben), Dokumente 438/0 | Einzellauf-Logs |
| Voller Sammellauf | **OFFEN** (letzter belegter Lauf 12:33: 172 von 174, 1341 s) | — |
| Guthaben (Daniel 05.11.2026) | 13,16 USD Stand / 56,83 USD Gesamtverbrauch; **3,16 USD fuer grosse DeepSeek-Auftraege (Nebelseetal)** | Ablesung |
| EXE | weiterhin `Nebelseetal_Pre_Release_V0.0.1.exe` — V0.0.2 offen | `data/version.json` |

## Der EINE naechste Schritt
1. Voller Sammellauf mit dem Projekt-venv (`.venv/Scripts/python.exe -X utf8 -u tools/sammellauf.py`),
   rote Dateien einzeln nachfahren; der Lauf zaehlt nur, wenn er nach dem letzten Fix startete.
2. Danach EXE `Nebelseetal_DemoVersion_V0.0.2.exe` bauen (`data/version.json`: zaehler 2, label
   DemoVersion, alte EXE vorher sichern) und am Bildschirm pruefen (Fenster plus Passwortsperre).
3. Danach Upload-Paket (`tools/build_public_exe.py --pruefen`, Bau nach `release_public/`),
   Release-Notizen und Push ohne Force; Groesse und SHA256 nur aus der Ausgabe des Laufs.
4. Nach jedem Schritt eine Zeile ins Entwicklungsprotokoll (Sammellauf und Protokoll gehoeren zum Fix).

# STAND 05.11.2026, 11:40 — Endstand gruen, Pre-Release-EXE gebaut und am Bildschirm geprüft (Register 213 bis 221)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Die Runde ist abgearbeitet.** Alle fuenf Streitpunkte aus Daniels Entscheidungsblatt sind gebaut
und einzeln belegt; zwei davon haben das Spiel messbar veraendert, und das steht hier, nicht nur im
Code.

| Frage | Was gebaut ist | Register | Beleg |
|---|---|---|---|
| 6 | Die sechs **Hausfarben folgen den Wappentinkturen** (Chronik und `data/haeuser.json` gleich) | 213 | `test_hausfarben` 33/0/1 mit Gegenprobe |
| 8 | **Gold laedt zuerst** (Hoechstanteil), der Rest anteilig; Schalter `aktiv` stellt das alte Modell wieder her | 214 | `test_beute_vorrang` 29/0/1 |
| 1 | **Bots raeumen Ruinen** mit Karren und ohne Kampf; sie rechnen dabei mit IHRER Forschung | 215 | `test_bot_ruinenzug` 25/0/1 |
| 9 | **Die besiegte Ruine deckt ihren Sektor** — kein Angriff aus dieser Richtung, Anzeige in der Uebersicht | 216 | `test_ruinendeckung` 43/0/1 |
| 2 | **Zweite Atemphase**: 20 % unter halber Wache, vorher gemessen | 217 | `test_drachen_zweite_phase` 22/0/1 |

**Der wichtigste Befund des Tages (Frage 2, gemessen vor dem Bau):** die zweite Atemphase kippt den
sicheren Sieg am Drachen. Mit **300 Kriegern + 22 Katapulten** gewinnt man neu nur noch **3 von 100
Laeufen** (vorher 100/100, der zweite Atem nimmt 55 Mann). **Sicher ist der Sieg ab 400 Kriegern +
22 Katapulten.** Zweite Folge: die eigenen Verluste haengen jetzt **von der Truppengroesse** ab
(154 → 228 bei 400, → 338 bei 1000) — der frueher belegte Satz "Verluste sind groessenunabhaengig"
gilt nur noch ohne die Phase. Zahlen: `docs/SPIELBALANCING_TEST.md` Abschnitt 10.

**Zwei alte Wachen mussten mit der Entscheidung nachgezogen werden** (Schuppe-Kette und
Einghaengungs-Kette rechnen mit 400 Kriegern; die Atem-Zeile rechnet 8 % aus der Datendatei statt
eine getippte Zahl zu pruefen). Der Code wurde dafuer **nicht** zurueckgebogen.

**Nachgeschärft am 05.11.2026, 10:52 (Register 219):** der Beute-Vorrang steht auf **25 Prozent**
(Daniels Wahl, nicht die vorgeschlagenen 50) — der Vorrang ist damit leise: bei vier Rohstoffen
ist 25 Prozent genau der alte Anteil. Und die Ruine deckt **nur ihre eigene Koordinate**
(`DECKWEITE_FELDER = 0`) — eine Siedlung daneben ist nicht geschützt. Beides sind Zeilen in
Datendateien bzw. eine Konstante, keine Codeänderung nötig.

**Was ausdruecklich offen bleibt und Daniel gehoert:** der Hoechstanteil 50 % bei der Beute (Frage 8)
und die **Reichweite** der Ruinendeckung (Frage 9 — das Original nennt keine; die Ruine deckt ihren
ganzen Sektor bis zum Kartenrand). Beide sind Zeilen in Datendateien, ohne Codeaenderung aenderbar.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf auf `main` | `d91ff17` (Code) + Doku-Commits | `git log --oneline -1` |
| Commits | 605 | `git rev-list --count HEAD` |
| Arbeitsbaum | sauber | `git status --porcelain` |
| Pruefdateien | **174** (fuenf neue) | `ls tests/test_*.py` |
| Module | 60 (`src/ruinendeckung.py` neu, Modulkarte nachgezogen) | `ls src/*.py`, `test_projektpfade` 123/0 |
| Register / Protokoll | **220** / **252** Zeilen aktiv + 113 Zeilen Historie | Zaehlung; die 02./03.11.-Sektionen sind ausgelagert |
| Voller Sammellauf | **172 von 174 gruen, 0 rot, 1341 s** (die zwei uebrigen sind die seit 30.10. ausgesetzten Dateien) | `docs/audits/sammellauf_20261105_1120_nachordnung.log` |
| Guthaben (Daniel 11:23) | 13,68 USD Stand / 56,31 USD Gesamtverbrauch | Ablesung, Protokollzeile |
| Pre-Release-EXE | **`Nebelseetal_Pre_Release_V0.0.1.exe`**, 86.963.273 Byte (82,9 MB), SHA256 `4d1d0e5f…` | Bau `docs/audits/exe_bau_20261105_1130.log` |
| Start der EXE geprüft | Fenster (PID 7208, „Nebelseetal Remake“) und **Passwortsperre im Bild** | `computer_use`, Aufnahme `computer_use_150e1697f4…png` |
| Release-Namen | Schema `Nebelseetal_<Label>_V0.0.<Zähler>.exe` in `data/version.json` (nächste: `…_DemoVersion_V0.0.2.exe`) | Register 221 |

## Der EINE naechste Schritt

1. **Sammellauf gelesen:** `sammellauf_20261105_1120_nachordnung.log` = **172 von 174 grün, 0 rot, 1341 s**.
2. **EXE `V0.0.1` gebaut und geprüft — erledigt (Register 221).** 86.963.273 Byte, SHA256 `4d1d0e5f…`, Start am Bildschirm belegt.
3. **Schnitt Register 222 bauen:** Startfenster = Kartengründungsseite, Fraktionsfrage direkt nach
   Spielneubeginn, danach **kein Fraktionswechsel** mehr (eigene Wache).
4. **Schnitt Register 225 bauen (Daniels Entscheidungen vom 12:40):**
   (a) **Goldkosten der Militäreinheiten −30 %** (Krieger 500→350, Bogenschütze 1.000→700, Paladin 2.000→1.400,
   Kundschafter 250→175, Belagerung 750→525) — als bewusste Abweichung dokumentieren;
   (b) **Karten nach Original:** Zufallsziehung für Spieler UND Bots, eine unpassende Karte wird **gelöscht**,
   die **Gründungsressourcen sind verloren**, neu sparen — „es soll sich lohnen“.
   **Nicht gebaut:** die Beute-Quote (Register 225 Punkt 2) — sie würde die belegte Karrengrenze abschaffen.
5. **Danach** EXE `Nebelseetal_DemoVersion_V0.0.2.exe` bauen und prüfen, dann Upload-Paket und GitHub;
   anschließend Werkzeug-Fix (Wagenbau in `tools/balancing_messung.py`), Bot-Drachenregel, Protokoll-Repo privat.

---

# STAND 05.11.2026, 05:20 - Drachenkampf gemessen (Register 208)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Die drei Recherche-Vorschlaege sind jetzt entscheidbar, weil gemessen ist.** Bisher gab es kein
Werkzeug fuer den Drachen (`tools/balancing_messung.py` kennt ihn nicht). Neu:
`tools/drachen_balancing.py` rechnet mit der ECHTEN Schlacht, 100 Laeufe je Zelle, fester
Zufallskeim - dieselbe Zeile liefert immer dieselbe Zahl.

**Der Befund, der mehr wert ist als die Tabelle:** die Schwellen 700/950 gelten fuer
**Schlagkraft**, nicht fuer Kopfzahl. 700 SK = **234 Krieger**, 950 SK = **22 Katapulte**. Und an
genau dieser Schwelle **gewinnt man nie**: der Feueratem (8 % = 19 Krieger) schlaegt VOR der
Vorrunde zu, danach stehen 215 Krieger = 645 SK gegen 700 - die Truppen ziehen sich zurueck,
0 von 100 Laeufen. **Wer die Schwelle nur knapp erfuellt, verliert durch den Atem.**

**Sicherer Sieg ab 300 Kriegern und 22 Katapulten** (100 %). Belagerung ist die bindende Bedingung:
mit 11 Katapulten gewinnt keine Zelle, egal wie viele Krieger mitkommen. Die Verluste sind
groessenunabhaengig: rund 152-162 eigene Einheiten, ob 300 oder 1000 Krieger antreten - bei 300+22
sind das 50 % der Truppe.

**Folge fuer Vorschlag 2 (zweite Kampfphase):** mit 12 % statt 8 % Atem steigen die eigenen
Verluste von 154 auf 155 - **etwa eine Einheit**. Eine zweite Phase mit diesen Werten waere
Erzaehlung, keine Balance-Aenderung. Sie wuerde erst spuerbar, wenn sie die Vorrunde kippt oder
deutlich haerter brennt. Die Entscheidung gehoert Daniel (Frage 2), die Messung nimmt sie ihm nicht ab.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf auf `main` | W-17 (dieser Commit) | `git log --oneline -1` |
| Neues Werkzeug | `tools/drachen_balancing.py` | Rohlauf `docs/audits/drachen_balancing_20261105.log` |
| Messung | 36 Zellen x 100 Laeufe, fester Keim | Log |
| Sicherer Sieg | 300 Krieger + 22 Katapulte | Abschnitt 9 der Balancing-Doku |
| Sammellauf 04:11 | 165 von 169 gruen, 2 rot - beide behoben (121/0 und 426/0) | `docs/audits/sammellauf_20261105_0411.log` |
| Guthaben (Daniel 04:55) | 5,29 USD Stand / 54,70 USD Gesamtverbrauch | Ablesung |

## Der EINE naechste Schritt

1. **Frage 2 entscheiden** (zweite Kampfphase mit den gemessenen Zahlen) - oder Vorschlag 1 bauen
   (Erwartungswert im Bot-Urteil), der braucht keine Entscheidung.
2. Mini-Repo fuer das Protokoll (Register 202) mit der VOLLEN Historie, lueckenlos.
3. Kampfregeln 2, 4, 6 aus `cache/scratch/w13b_kampfregeln_entwurf.md`.

---

# STAND 05.11.2026, 04:50 - Drachenschuppe als Trophae mit Lagerfach (Register 207)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Die Drachenschuppe kommt jetzt wirklich an.** Bis eben hat der Drachenkampf sie ins Leere
gebucht: `data/drachen.json` fuehrte die Ware klein geschrieben (`"drachenschuppe"`), damit hatte sie
kein Lagerfach, und der Bericht sagte ehrlich "dafuer gibt es noch kein Lagerfach". Jetzt ist sie eine
**eigene Trophae** mit eigenem Fach, eigenem Bild und den Regeln, die Daniel genannt hat: keine Ware,
kein Rezept, nicht handelbar, zaehlt in keiner Formel.

**Wie es gebaut ist:** eigene Datendatei `data/trophaeen.json` (Regeln und Beschreibung),
`spieldaten.trophaeen()` und `spieldaten.lager_waren()` als Lesestellen, `main.LAGER_WARE_EINTRAEGE`
mit **18 Faechern** (17 Originalwaren + 1 Trophae). `WARE_EINTRAEGE` bleibt bei den 17 - deshalb
kann die Schuppe nirgends zum Rezept werden. Das Icon
`assets/icons/items/Drachenschuppe.png` ist selbst gezeichnet (Pillow, 64x82), keine fremde Datei.

**Eine Wache im Kern:** `spieloekonomie.handel_start` lehnt jede Ware ab, die nicht in den 17
Originalwaren steht. Ohne sie haette eine Trophae ueber einen Handelsvertrag doch zur Ware werden
koennen.

**Zwei alte Pruefungen mussten nachziehen** - nicht weil sie falsch waren, sondern weil sich die
Semantik absichtlich geaendert hat: `test_drachen_einhaengung` (c) erwartete die Meldung "noch ohne
Lagerfach" und prueft jetzt "Drachenschuppe erbeutet"; `test_drachen` las den kleinen Schluessel.

**Belegt:** `tests/test_drachenschuppe.py` **32 bestanden, 0 Fehler** mit (a)-(i), darunter eine
Gegenprobe und ein echter Handelsversuch, der scheitern MUSS. `test_drachen` 88/0/0,
`test_drachen_einhaengung` 96/0/0, Umlaut-Wache 49/0.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf auf `main` | W-16 (dieser Commit) | `git log --oneline -1` |
| Neue Wache | `tests/test_drachenschuppe.py` 32/0/0 | Testlauf |
| Lagerfaecher | 18 (17 Waren + 1 Trophae) | `spieldaten.lager_waren()` |
| Nachgezogene Wachen | `test_drachen` 88/0/0, `test_drachen_einhaengung` 96/0/0 | Testlaeufe |
| Voller Sammellauf | laeuft fuer diesen Stand als `docs/audits/sammellauf_*.log` | Log |
| Guthaben (Daniel 04:55) | 5,29 USD Stand / 54,70 USD Gesamtverbrauch | Ablesung |

## Der EINE naechste Schritt

1. **Die drei Recherche-Vorschlaege** (Erwartungswert im Bot-Urteil, zweite Kampfphase,
   Regeneration oder erneutes Erwachen) - erst nach einer **Balancing-Messung** mit
   `tools/balancing_messung.py`; die Zahlen gehoeren nach `docs/SPIELBALANCING_TEST.md`.
2. Mini-Repo fuer das Protokoll (Register 202) mit der VOLLEN Historie, lueckenlos.
3. Kampfregeln 2, 4, 6 aus `cache/scratch/w13b_kampfregeln_entwurf.md`.

Arbeitsweise unveraendert: **voller Sammellauf mit dem Projekt-venv**, Registerzeile und
Protokollzeile gehoeren zum Abschluss, Kommentarregel Variante A bei jedem neuen Code.

---

# STAND 05.11.2026, 03:53 - W-15 Haeuser und Wappenbeschreibungen (Register 206)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Sechs Haeuser tragen jetzt ihren Namen und ein Wappen, das es wirklich gibt.** Daniels Auftrag
war, die Wappenbeschreibungen auf die gelieferten Bilder umzuschreiben. Beim Nachsehen kam der
eigentliche Befund: die alten Saetze beschrieben Motive, die auf **keinem** der zehn Bilder stehen
(Wellenbalken, Hechtkamm, Widderhoerner, Schwanenfluegel, Stierhoerner, Geierfaecher, Flickenmuster)
und behaupteten einen Helm, den die Bilder nicht zeigen. Jedes zugeordnete Wappen wurde deshalb
einzeln angesehen und der Satz daraus neu geschrieben: Silberbach traegt eine goldene Krone auf
Weinrot, Hammerhall einen steinernen Turm auf Nachtblau, Sternenwacht einen goldenen Hirschkopf auf
Dunkelgruen, Schattenfaust einen schwarzen Raben vor dem Vollmond auf Violett, Knochenmoor einen
silbernen Wolfskopf ueber drei Berggipfeln auf Blau, Flickwerk zwei gekreuzte Schwerter auf
Karminrot. Jeder Satz sagt ausdruecklich, dass kein Helm gefuehrt wird.

**Eine Quelle statt Prosa:** `data/haeuser.json` (Name, Volk, Welt, Farben, Sitz, Burg, Wappen, Satz,
Kurzform), gelesen ueber `src/haeuser.py`. Die Voelkerwahl nennt zu jedem Volk seinen Hausnamen.

**Ehrliche Grenze:** die Hausfarben der Chronik decken sich nicht mit den Tinkturen der Wappen
(Menschen "Blau und Silber" gegen Weinrot und Gold). Beides steht offen im Text; die Angleichung ist
**Frage 6 an Daniel** und wird nicht selbst entschieden.

**Belegt:** `tests/test_haeuser_wappen.py` **61 bestanden, 0 Fehler** mit den Wachen (a)-(i) -
darunter eine Gegenprobe (ein erfundener alter Satz MUSS auffallen), die Gleichheit von Karten- und
Hauswappen und die Heimatwelt gegen `data/welt_fraktionen.json`. Umlaut-Wache 49/0.
Beide Chronik-Fassungen sind hashgleich `2a1df42f...`.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf auf `main` | W-15 (dieser Commit) | `git log --oneline -1` |
| Neue Wache | `tests/test_haeuser_wappen.py` 61/0/0 | Testlauf |
| Hausdaten | 6 Haeuser, 12 Bildpfade, alle vorhanden | `data/haeuser.json` |
| Chronik | beide Fassungen hashgleich `2a1df42f...` | `sha256sum` |
| Voller Sammellauf | fuer diesen Stand noch offen - laeuft nach diesem Commit | `docs/audits/` |

## Der EINE naechste Schritt

1. **Drachenschuppe als eigene Ware und Trophae** (Daniel 05.11.2026: eigene Auszeichnung, zaehlt am
   Ende nur als Trophae) - eigener Schritt mit Lagerfach und Anzeige.
2. Danach: die drei Recherche-Vorschlaege nach einer Balancing-Messung (`tools/balancing_messung.py`).
3. Mini-Repo fuer das Protokoll (Register 202) mit der VOLLEN Historie, lueckenlos.
4. Kampfregeln 2, 4, 6 aus `cache/scratch/w13b_kampfregeln_entwurf.md`.

---

# STAND 05.11.2026, 03:06 - Drachen-Nachtraege eingebaut (Register 205)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Sechs Nachrichten Daniels, sechs Aenderungen - alle geprueft.** Der Sieg gegen einen Drachen
bringt jetzt **34.000 Mana**: 4000 pauschal plus der Aufwand von drei Versuchen mit je zwei
Weltenspruengen, gerechnet aus dem ECHTEN Preis eines Sprungs (aendert der sich, zieht die
Belohnung mit - mit Wache belegt). Die Wache des Drachen bleibt **beschaedigt** stehen, ein
zweiter Angriff trifft weniger Verteidiger. Ein **Flammenzeichen** unter der Figur sagt nur,
dass schon jemand angegriffen hat, und verschwindet, wenn der Hort leer ist. **Bots** beurteilen
den Drachen mit Sicherheitsmarge, kennen Bonus und sichere Verluste, aber nicht die Wache.
Die **Ruine bleibt pluenderbar** (kein zweites Gefecht) und **sperrt danach ihre Koordinate**.
Jeder **Neubeginn** wuerfelt neue Plaetze auf denselben Welten.

**Belegt:** `tests/test_drachen_einhaengung.py` **96 bestanden, 0 Fehler** mit den Wachen
(a)-(i); Anzeige- und Bot-Texte durch die Umlaut-Wache (49/0). Voller Sammellauf: **165 von 167 gruen, 0 rot, 1450 s, 6.868 Pruefungen**
(`docs/audits/sammellauf_20261105_0310_voll.log`).

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf auf `main` | Drachen-Nachtraege (dieser Commit) | `git log --oneline -1` |
| Neue Wache | `tests/test_drachen_einhaengung.py` 96/0/0 | Testlauf |
| Voller Sammellauf (Projekt-venv) | 165 von 167 gruen, 0 rot, 1450 s, 6.868 Pruefungen | `docs/audits/sammellauf_20261105_0310_voll.log` |
| Register / Protokoll | 205 Zeilen / 331 Zeilen | `grep -cE '^\| [0-9]+ \|'`, `wc -l` |
| Guthaben (Daniel 02:48) | 5,77 USD Stand / 54,22 USD Gesamtverbrauch | Ablesung |
| Recherche | `docs/RECHERCHE_SPIELMECHANIKEN_20261105.md` (14 Vergleiche, 3 Vorschlaege) | Dokument |

## Der EINE naechste Schritt

1. **W-15 Haeuser:** Hausnamen und Wappenbeschreibungen auf die gelieferten Bilder umschreiben.
2. **Drachenschuppe als eigene Ware und Trophae** (Daniel 05.11.2026: eigene Auszeichnung,
   zaehlt am Ende nur als Trophae) - eigener Schritt mit Lagerfach und Anzeige.
3. **Die drei Recherche-Vorschlaege** pruefen (Erwartungswert im Bot-Urteil, zweite Kampfphase,
   Regeneration oder erneutes Erwachen) - erst nach Balancing-Messung, Entscheidung Daniel.
4. **Mini-Repo fuer das Protokoll** (Register 202) mit der VOLLEN Historie, lueckenlos.

Arbeitsweise unveraendert: **voller Sammellauf mit dem Projekt-venv**, Registerzeile und
Protokollzeile gehoeren zum Abschluss, Kommentarregel Variante A bei jedem neuen Code.

---
# STAND 05.11.2026, 01:52 - W-14 Teil 2 gebaut: die Drachen stehen im Spiel (Register 204)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Die Drachen sind verdrahtet.** W-14 Teil 1 hatte nur das Modul gebaut; jetzt haengen acht
Andockstellen daran: der Zustand (besiegte Drachen und ihre Horte im Spielstand), die Zielwahl
ueber den EINEN Angriffsweg, die Vorrunde gegen **Drachenwerte statt eines Walls** (Fusstruppen
700, Belagerung 950, unbrechbar), der **Feueratem** (8 Prozent der antretenden Fusstruppen,
eigene Berichtszeile), der Kampf gegen 204 Verteidiger, der **Beuteanteil nach Leistung** (letzter
Schlag +10 Prozent, ueber die EINE Buchstelle und begrenzt durch die Karrenladung), der eigene
**Bericht** (ohne Ueberlebende nur eigene Verluste und die Zahl der Verteidiger, kein Ausspaehen)
und die **Anzeige** als Figur je Drache, nach dem Sieg als Ruine.

**Belegt:** `tests/test_drachen_einhaengung.py` **76 bestanden, 0 Fehler** - mit allen sieben
Pflicht-Wachen der Uebergabe (Angriff unter der Schwelle kaempft nicht, Feueratem gebucht und im
Bericht, Beute genau einmal und nur der Anteil, ohne Ueberlebende keine Einheiten, kein
Ausspaehen, nach dem Sieg Ruine ohne zweiten Angriff, alter Spielstand laedt) und einer ECHTEN
Zeichnung der Portal-Ansicht. **Voller Sammellauf: 165 von 167 gruen, 0 rot, 1226 s**, 6.848 Pruefungen,
56 Befunde, kein Fehler.

**Zwei ehrliche Befunde:** der erste Entwurf liess den Drachen stehen, obwohl das Gefecht
gewonnen war - Massstab ist jetzt `kampfbericht.ausgeraeumt` (dieselbe Lesart wie W-13, weil
fliehende Verteidiger im Ort bleiben). Und der erste Sammellauf lief mit dem Hermes-Python und
meldete eine rote Datei (`test_gpt_originalkarten_historische_info`), weil dort `lxml` fehlt -
ein Geraetefehler, kein Spielfehler. Der Sammellauf gehoert mit `.venv/Scripts/python.exe`
gefahren, dann ist er gruen und rund 3 Minuten schneller.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf auf `main` | W-14 Teil 2 (dieser Commit) | `git log --oneline -1` |
| Neue Wache | `tests/test_drachen_einhaengung.py` 76/0/0 | Testlauf |
| Voller Sammellauf | 165 von 167 gruen, 0 rot, 1226 s, 6.848 Pruefungen | `docs/audits/sammellauf_20261105_0132_voll.log` |
| Pruefdateien / Module | 167 / 58 | `ls tests/test_*.py \| wc -l`, `ls src/*.py` |
| Register / Protokoll | 204 Zeilen / 324 Zeilen | `grep -cE '^\| [0-9]+ \|'`, `wc -l` |
| Guthaben (Daniel 01:25) | 6,13 USD Stand / 53,86 USD Gesamtverbrauch | Ablesung |

## Der EINE naechste Schritt

1. **W-15 Haeuser:** Hausnamen und Wappenbeschreibungen auf die gelieferten Bilder umschreiben.
2. **Kampfregeln 2, 4, 6** aus `cache/scratch/w13b_kampfregeln_entwurf.md` (Flucht unter 50
   Prozent, Wurf gegen 40 + 5 x Sequenz, Beute-Reihenfolge Gold zuerst, Mauerreparatur).
3. **Story-Einbau:** Chronik-Kapitel in `data/story.json` (Entwurf liegt im Scratch).

Arbeitsweise unveraendert: **voller Sammellauf mit dem Projekt-venv**, Registerzeile und
Protokollzeile gehoeren zum Abschluss, Kommentarregel Variante A bei jedem neuen Code.

**Offen bei Daniel (eine Runde am Abschluss):** welche DREI Welten die Drachen bekommen
(Vorschlag d02/d03/d05), ob die Drachenschuppe ein Lagerfach bekommt, ob der Rest des Hortes mit
dem Drachen verfallen soll (so ist es jetzt) und die Verdichtung des Protokolls.

---
# STAND 05.11.2026, 00:05 - W-13 gebaut (Gesamtsieg mit Endlosspiel), W-14 Teil 1 liegt bereit

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Der Gesamtsieg existiert jetzt im Spiel.** Daniel hat ihn am 04.11. definiert (Register 197): erreicht,
wenn jeder Bot und ALLE seine Doerfer mindestens einmal laut Kampfbericht ausgeraeumt wurden. W-13 setzt
das um: je ausgeraeumtem Dorf eine Buchung (`BotDorf.ausgeraeumt_seit`, gesetzt im EINEN Kampfweg
`GameState.kampf_am_ziel`), eine Auswertung in `punkte.gesamtsieg` und EINE Glueckwunschnachricht mit
fraktionsangepasster Geschichte aus `data/story.json` (sieben Texte, von `deepseek-v4-pro` geschrieben).
**Der Sieg beendet nichts** - `spielende` bleibt leer, die Spieluhr laeuft weiter (Endlosspiel).

**Echter Fehler dabei gefunden und behoben:** die Verluste des Verteidigers wurden bei einem Bot-Dorf NIE
gebucht. Der Block las `bot_ziel.army` - eine BERECHNETE Summe - und buchte in eine Kopie; gemessen: drei
Verluste im Bericht, Heer danach unveraendert sechs. Jetzt verteidigt die Garnison des angegriffenen
Dorfes (zweiter Teil von B-5), gebucht wird dort; ohne Dorf bucht `bot_armee_buchen`.

**W-14 Teil 1 liegt bereit, ist aber NICHT verdrahtet:** Daten, Modul und Pruefdatei fuer die Drachen (`test_drachen` 88/0/0). **Daniel hat am 05.11. die Verteidigung neu bestimmt:** deutlich mehr Einheiten - **120 Krieger + 60 Bogenschuetzen + 24 Paladine = 204** - und **statt eines Walls eigene Drachenwerte**: Schwelle Fusstruppen 700, Schwelle Belagerung 950, **unbrechbar** (Belagerung richtet keinen Wallschaden an), dazu ein **Feueratem** mit 8 % Verlusten unter den antretenden Fusstruppen. Die drei Drachenfiguren von Daniel sind freigestellt (weiss, blau, lila).

**Nachtrag 05.11.2026 (Daniel) - Drachen sind NUR Verteidiger:** keine Doerfer, ein starker Gegner mit vielen
Truppen und viel Beute. **Beuteanteil nach Leistung** (Variante A: jeder Angriff bucht seinen Anteil nach
zerstoerten Verteidigern, letzter Schlag +10 %) statt "letzter Schlag nimmt alles". **Transport wird
vorgerechnet** (`transport_bedarf`, `transport_text`), was nicht getragen wird bleibt liegen. **Epische Berichte,
aber ehrlich:** mit Ueberlebenden genaue Einheiten, ohne Ueberlebende nur eigene Verluste und die ZAHL der
Verteidiger. **Kein Ausspaehen** (`spionage_erlaubt` = False), dazu `angriffs_hinweis` und ein Satz in der Hilfe.


| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf auf `main` | Code-Stand `9fc4138` (W-13), darauf W-14 Teil 1 und die Doku-Commits | `git log --oneline` |
| Voller Sammellauf | **163 von 165 gruen, 0 rot, 1433 s**, 6.684 Pruefungen, 55 Befunde (die zwei uebrigen sind dokumentiert zurueckgezogen) | `docs/audits/sammellauf_20261104_2327.log` |
| Neue Wachen | `test_gesamtsieg` **47/0/0**, `test_drachen` **88/0/0** | eigene Laeufe |
| Register / Protokoll | **203** / **321 Zeilen** (eine ueber Ziel - Verdichtung offen, siehe unten) | `grep -c`, `wc -l` |
| Kosten grosse Modelle (Monat) | **0,4342 USD von 1,94 USD am 04.11.** (Anbieter-CSV, 10 Anfragen); November 01.-04. insgesamt 18,0858 USD (flash 13,4376 / v4-pro 4,6482); 5,00 USD Reserve fuer `deepseek-flash` unangetastet (Ablesung 23:56: 6,56 / 53,43 USD). Eigene Textlaeufe 0,1746 USD - Schaetzpreise waren 3- bis 10-fach zu niedrig, es gilt nur die CSV |
| Veroeffentlicht | Stand von `main` als Entwicklungsschritt gepusht: `63639d5`, **ohne neue EXE** - die Testversion 0.5.0-pre.1 bleibt | `git push origin pre-release:main`, `origin/main` geprueft |
| Figuren | `assets/bilder/drache_weiss.png`, `drache_blau.png`, `drache_lila.png` (256 px + 64 px); Originale unter `archiv/eingaben/20261104_drachenbilder/` | Register 201 |

## Der EINE naechste Schritt

**W-14 Teil 2: die Drachen ins Spiel bringen.** Zu verdrahten sind (a) die Kartenanzeige - kleine
Drachenfigur statt Burg, nach dem Sieg die **Ruine** (Daniel 04.11.2026: je Spielstand und Karte; das
Ruinenbild modelliert Daniel selbst, bis dahin Platzhalter), (b) die Zielwahl im Angriffsweg, (c) der Kampf
ueber `kampf.fuehre_schlacht` mit `drachen.verteidiger`/`drachen.wall`, (d) die Beute ueber die EINE
Buchstelle `kampfbericht.beute_am_ziel` (Vorschlag: um `beute_override` erweitern), (e) der Zustand
`drachen_besiegt` in `GameState.save/load`. Der Einbauplan mit Zeilenlagen liegt in
`docs/ENTWURF_W14_TEIL2_20261105.md` - **vor dem Bau entscheidet Daniel zwei Dinge:** welche DREI Welten
`docs/ENTWURF_W14_TEIL2_20261105.md` - **vor dem Bau entscheidet Daniel nur noch EINE Sache:**
welche DREI Welten (Vorschlag d02, d03, d05). Die **Verteidigung ist entschieden** (204 Einheiten,
Drachenwerte statt Wall, Feueratem). **Arbeitsweise: der volle Sammellauf, die Registerzeile und die
Protokollzeile gehoeren zum Abschluss.**
**Offene Punkte, die nicht untergehen duerfen:** (1) Farben der Drachenfiguren - Daniel: erstmal unwichtig,
spaeter anpassen; die Chronik nennt Episheus weiss / Tardas gruen / Salmur rot, geliefert sind weiss, blau,
lila. (2) Das Protokoll steht mit **321 Zeilen** eine Zeile ueber Ziel; die Verdichtung ist ein eigener
Schritt (Vorgaengerzeilen werden nicht nachts nebenbei zusammengelegt). (4) **Eigenes Mini-Repo fuer das Entwicklungsprotokoll** ist beauftragt und auf spaeter gelegt (Register 202); (3) Zwei Skill-Abschnitte warten in
der Freigabe-Liste (`18381d56`).

# STAND 04.11.2026, 22:00 - W-12 gebaut (sechs Welten), alle sechs Welten bespielbar, fuenf Antworten eingearbeitet

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Das Spiel fuehrt sechs Welten, und alle sechs sind bespielbar.** Die 14 leeren
Platzhalter-Dimensionen (d07 bis d20) sind entfernt; die sechs belegten Weltkarten (d01 Armageddon,
d02 Ragnaroek, d03 Utgard, d04 Midgard, d05 Valhalla, d06 Limbus) tragen ihre alten Kennungen, **alte
Spielstaende laden unveraendert**. Alle Textstellen, die 20 Dimensionen behaupteten, nennen jetzt sechs
Weltkarten - der Original-Stand bleibt als belegter Satz im Code, damit die Quellenlage nicht
verschwindet. **Die Frage "Limbus: Raum oder Welt?" brauchte keine Runde:** Register 98
(Daniel 01.11.2026) legt fest, dass "Limbus" Weltname bleibt und die Ebene "der magische Limbus"
heisst. **Nummernwiderspruch geradegezogen:** die Uebergabe nannte den Schnitt W-6; W-6 ist seit dem
03.11. der Nur-Lese-Blick in fremde Welten (Register 166). Der Schnitt heisst **W-12**.

**Daniel hat die fuenf offenen Fragen beantwortet** (Register 197, Wortlaut dort): Sieg ist ab jetzt
definiert (jeder Bot und alle seine Doerfer mindestens einmal laut Kampfbericht ausgeraeumt, danach
Endlosspiel und eine fraktionsangepasste Glueckwunsch-Nachricht); Drachen kommen zurueck, aber genau
einer je Karte in drei Welten, als Drachenfigur statt Burg, mit grosser Beute; Hausnamen und
Hausfarben werden uebernommen; **alle sechs Welten sind bespielbar** (sofort gebaut); die
Skill-Freigabe gilt nur fuer die Story-Schicht.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf auf `main` | Code-Stand `237c8ae`, darauf die Doku-Commits bis `93d104f` | `git log --oneline` |
| Limbus-Dimensionen | **6** (d01-d06), vorher 20 | `data/welten.json`, `portalraum.dim_zahl()` |
| Bespielbare Welten | **6 von 6** (vorher 2) | `data/welten.json` → `weltkarten_spielbar` |
| Register / Protokoll | **197** / **318 Zeilen** (Ziel 320, verdichtet aus 320) | `grep -c`, `wc -l` |
| Voller Sammellauf | **161 von 164 gruen, 0 rot, 1789 s**, 6.589 Pruefungen, 55 Befunde | `docs/audits/sammellauf_20261104_2123.log` |
| Einzeln nachgeholt | `test_produktionskette_ohne_cheats` **48/0/0 in 272 s** (im Lauf: Zeitlimit 420 s, kein Befund) | eigener Lauf |
| Umgestellte Pruefdateien | `test_welt` 43/0/0, `test_portalraum` 70/0/0, `test_portal_uebersicht` 61/0/0, `test_weltkarten_anzeige` 27/0/0, `test_weltbild_gelaende` 94/0/0 | Sammellauf |
| Unveraendert | 400 Felder je Weltkarte (20x20 Raster), 5.000 Mana/24 h Weltensprung, sechs Fraktionen mit Heimatwelten | `data/welten.json`, Register 164 |

## Der EINE naechste Schritt

**W-13: die Sieg-Auswertung bauen - der Gesamtsieg nach Daniels Definition.** Sieg heisst: **jeder Bot
und ALLE seine Doerfer wurden mindestens einmal laut Kampfbericht ausgeraeumt** (Register 197). Zu
bauen sind (a) eine Buchung je ausgeraeumtem Dorf im Kampfbericht-Weg (`src/kampfbericht.py`,
`src/auftraege.py`), (b) die Auswertung "sind alle Doerfer aller fuenf Bots erledigt" in `src/punkte.py`
neben E5, (c) die Glueckwunsch-Nachricht mit Fraktionsbezug, (d) **Endlosspiel danach**: der Sieg sperrt
nichts und beendet nichts. Der Storytext der Siegesnachricht ist ein EIGENER Teil (Modelllauf, Daniel
entscheidet vorher). **Arbeitsweise: der volle Sammellauf, die Registerzeile und die Protokollzeile
gehoeren zum Abschluss.** Das Protokoll wurde am 04.11. von 320 auf **318 Zeilen** verdichtet (drei
Bildcontent-Zeilen zu einer, zwei GitHub-Zeilen zu einer; Vorfassung unter
`docs/archiv/ENTWICKLUNGSPROTOKOLL_VOR_VERDICHTUNG_20261104.md`), **zwei Zeilen sind frei** - die
naechste Protokollzeile passt ohne neue Verdichtung.

**Danach in dieser Reihenfolge (von Daniel so entschieden):** die drei offenen Kampfregeln (2
Fluchtformel, 4 Beute-Reihenfolge Gold zuerst, 6 Mauerreparatur mit Bauzeit), dann **W-14 Drachen**
(eine Figur je Karte in drei Welten, Beute als VORSCHLAG 5.000 Gold, je 2.000 Holz/Stein/Nahrung und
eine Drachenschuppe, Zahlen in einer Datendatei), dann **W-15 Hausnamen und Wappenbeschreibungen**,
zuletzt der Story-Einbau aus `docs/CHRONIK_DER_WELT_20261104.md`.

# STAND 04.11.2026, 19:40 - Pre-Release 0.5.0-pre.1 veroeffentlicht, naechster Schritt W-6

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Der erste Pre-Release ist draussen.** `v0.5.0-pre.1` liegt auf GitHub: Testversion
`Nebelseetal_Remake.exe` (81,8 MB, SHA256 `75c24cc5...`), Paket 81,6 MB mit EXE und vier Infodateien,
Repository oeffentlich, Besucherseite unter https://decay03101991.github.io/Nebelseetal-Remake/.
Der Start ist geprueft (Passworttor auf leerem Profil, danach Spieloberflaeche), der Anhang anonym
nachgeladen (85.516.122 Bytes, `testzip` sauber). Das Repo traegt **nur** Spielcode, Daten, Bilder und
die Veroeffentlichungsdokumente - keine Tests, keine Werkzeuge, keine Entwicklungsdokumente.
**Veroeffentlichungszweig ist `pre-release`, Entwicklung bleibt `main`; in `src`, `data`, `assets` sind
beide identisch.** Das Verfahren fuer spaetere Repo-Aenderungen steht in der Uebergabe 19:10, Abschnitt C.

**Zur Geschichte:** Die Chronik der Welt ist als Entwurf fertig (11.211 Woerter, elf Teile, Register 188),
dazu ein Gesamtbild zum Lesen mit Herkunft je Baustein und **sieben Widerspruechen** (Register 186). Der
groesste davon: das Spiel erzaehlt einen Sieg, den es nach E5 nicht gibt.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf auf `main` | `6c58575` | `git log --oneline -1` |
| Veroeffentlichungszweig | `pre-release`, 595 Dateien, 76,6 MB | `git ls-tree -r pre-release` |
| Release | `v0.5.0-pre.1`, Pre-Release, Anhang 81,6 MB | GitHub-API |
| Register / Protokoll | **195** / 315 Zeilen | `grep -c`, `wc -l` |
| W-6 offen | 20 Dimensionen, 6 belegt, 14 leer | `data/welten.json` |
| Sammellauf 15:16 | 162 von 164 gruen, 0 rot, 1220 s | `docs/audits/sammellauf_20261104_1516.log` |
| Sammellauf 19:12 | **161 von 164, 1 rot** (`test_gpt_projektordnung`: `.gitignore` ohne `/archiv/`), 912 s | `docs/audits/sammellauf_20261104_1912.log` |
| Reparatur | `.gitignore` mit den Schutzregeln wiederhergestellt (Secrets, Spielstaende, `/archiv/`) plus Veroeffentlichungspakete; Datei danach gruen | Commit `6c58575` |
| Nachlauf nach der Reparatur | **162 von 164 gruen, 0 rot, 802 s** (2 dokumentiert zurueckgezogen, 6.677 Pruefungen, 55 Befunde) | `docs/audits/sammellauf_20261104_1921.log` |

## Der EINE naechste Schritt

**W-6: die 14 leeren Limbus-Dimensionen entfernen - das Spiel fuehrt sechs Welten.** `src/welt.py`
(`DIMENSIONEN`), `src/portalraum.py`, `auftraege.kosten_der_mission` (Mana je Dimensionsstufe), die
Portal-Ansicht und die Wachen `test_bot_welten`, `test_portalraum`, `test_portal_uebersicht` sind
betroffen; die sechs Fraktionen stehen in `data/welt_fraktionen.json`. **Vorher eine Entscheidung
klaeren:** Limbus ist im Handbuch der Raum, im Remake eine Welt mit Gnomen - Vorschlag: Limbus bleibt
Raum, die Gnome bewohnen feste Inseln darin. **Der volle Sammellauf, die Registerzeile und die
Protokollzeile gehoeren zum Abschluss.**

**Danach** die drei offenen Kampfregeln (2 Fluchtformel, 4 Beute-Reihenfolge Gold zuerst, 6
Mauerreparatur mit Bauzeit), dann **C** (fliessende Ansichten); `main.py` zerlegen und Skill kuerzen
folgen nach der Story (Daniels Entscheidung).

---

# STAND 04.11.2026, 15:40 - Story 2: die fuenf Bots sprechen (Register 184)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Die fuenf Nachbarn haben jetzt eine Stimme.** Der zweite Story-Teil ist gebaut: Haug, Brynhild, Grom,
Silra und Krank sagen zu Angriff, Verteidigung, Gruendung und Beute je ein bis zwei Saetze - Ton wie
Story 1 (abenteuerlich und leicht, kein Pathos). **Alle Texte stehen in `data/bot_stimmen.json`**, im
Code steht kein einziger davon (als Wache geprueft). Vier Meldungen des Spiels tragen die Stimme jetzt:
Angriff auf den Spieler, Verteidigung eines Bot-Dorfs (letzte Zeile des Kampfberichts), Dorfgruendung
eines Bots und der Raubzug Bot gegen Bot. Fehlt ein Eintrag, kommt der neutrale Satz aus der Datei -
nie ein Absturz, und der sachliche Bericht bleibt in jedem Fall stehen.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Neue Wache | `tests/test_stimmen.py` **115/0/0** | eigener Lauf |
| Gegenprobe | Textnachschlag abgeschaltet: **43 Pruefungen rot** (115 auf 72), `src/stimmen.py` per SHA256 unveraendert zurueck | eigener Lauf |
| Texte | 5 Bots x 4 Ereignisse x 2 Saetze = **40 Texte**, alle mit echten Umlauten | `data/bot_stimmen.json` |
| Anschluesse | `stimmen.mit_stimme` an drei Stellen (angriff, beute, gruendung), `stimmen.zeile` in `kampf_am_ziel` (verteidigung) | `src/main.py` |
| Rueckfall | unbekannter Bot, unbekanntes Ereignis, fehlende Datei = neutraler Satz bzw. leer, ohne Absturz | `tests/test_stimmen.py` Abschnitt 4 |
| Voller Sammellauf | **162 von 164 gruen, 0 rot, 6677 Pruefungen, 1220 s** (2 dokumentiert zurueckgezogen) | `docs/audits/sammellauf_20261104_1516.log` |
| Messapparat | zwei vorher rote Dateien waren Geraetefehler (lxml fehlte nach dem Laufzeitwechsel, `Tcl_Obj` in `cget`), beide repariert und einzeln gruen | Protokollzeile 16:1x |
| Pruefdateien / Register / Protokoll | **164** / **185** / **300 Zeilen** | `ls tests/test_*.py`, `grep -c`, `wc -l` |
| Modulkarte | **57 Dateien** (neu: `stimmen.py`) | `python tools/modulkarte_bauen.py` |
| Stand-Bloecke | **76** | `grep -c '^# STAND'` |

## Der EINE naechste Schritt

**W-6: die 14 leeren Limbus-Dimensionen entfernen - das Spiel fuehrt sechs Welten.** `src/welt.py`
(`DIMENSIONEN`), `src/portalraum.py`, `auftraege.kosten_der_mission` (Mana je Dimensionsstufe), die
Portal-Ansicht und die Wachen `test_bot_welten`, `test_portalraum`, `test_portal_uebersicht` sind
betroffen; die sechs Fraktionen stehen in `data/welt_fraktionen.json`. **Danach** die drei offenen
Kampfregeln (2 Fluchtformel, 4 Beute-Reihenfolge Gold zuerst, 6 Mauerreparatur mit Bauzeit), dann **C**
(fliessende Ansichten); `main.py` zerlegen und Skill kuerzen folgen nach der Story (Daniels Entscheidung).
**Der volle Sammellauf, die Registerzeile und die Protokollzeile gehoeren zum Abschluss jedes Schnitts.**

**Zweiter, grosser Auftrag in eigener Sitzung: der GitHub-Neuaufbau.** Daniel hat den letzten Upload
zurueckgenommen und den Projektstand neu beurteilt; das Repository wird neu aufgebaut und als ERSTER
Pre-Release veroeffentlicht (Akte: `docs/AUFTRAG_GITHUB_PRE_RELEASE_20261104.md`, Register 185). Die
Inhaltsliste ist noch unvollstaendig - **bis dahin wird am Repo nichts geaendert.**

---

# STAND 04.11.2026, 11:15 - Story 1: das Spiel erzaehlt jetzt (Register 183)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Der dritte Kernbefund der externen Pruefung ist bearbeitet: das Spiel hat eine Geschichte.**
Nach dem Laden erscheint einmalig ein Ingame-Dialog mit vier Saetzen (Weltbruch, fuenf Nachbarn,
Aufgabe), der Berater hat die Rubrik "Geschichte" mit einer Chronik, die mit dem Fortschritt von
einem auf sieben Kapitel waechst, und Sieg wie Niederlage haben eigene Texte. **Alle Texte stehen in
`data/story.json`** - im Code steht kein einziger Storytext, das ist als Wache geprueft.

Daniels Entscheidungen dazu (04.11.2026): Ton **abenteuerlich und leicht** (Variante B), EIN Intro
statt sechs Fassungen, Chronik im Berater, und in Story 2 sprechen die Bots (je ein bis zwei Saetze
fuer Angriff, Verteidigung, Gruendung, Beute).

| Gegenstand | Wert | Beleg |
|---|---|---|
| Neue Wache | `tests/test_story.py` **38/0/0** | eigener Lauf |
| Gegenprobe | Merker abgeschaltet: **2 Pruefungen rot**, `src/story.py` per SHA256 unveraendert zurueck | eigener Lauf |
| Texte | 4 Intro-Absaetze, 7 Chronik-Kapitel, Sieg und Niederlage - alle mit echten Umlauten | `data/story.json` |
| Chronik-Stufen | 0 Ankunft, 1 Siedlung, 2 Ware/Werkstatt, 3 Forschung, 4 Kampf, 5 zweites Dorf, 6 zweite Welt | `src/story.py: _stufe` |
| Ort des Intros | Ingame-Overlay nach dem Aufbau der Oberflaeche (kein `Toplevel`) | `main._geschichte_intro_zeigen` |
| Merker | `geschichte.json` neben dem Spielstand - Intro einmal je Installation | `story.intro_gesehen` |
| Modulkarte | 56 Dateien (neu: `story.py`) | `python tools/modulkarte_bauen.py` |
| Pruefdateien / Register | **163** / **183** | `ls tests/test_*.py`, `grep -c '^\| [0-9]'` |

## Der EINE naechste Schritt

**Story 2: die fuenf Bots sprechen.** Neue Datendatei `data/bot_stimmen.json` mit je ein bis zwei
Saetzen pro Bot und Ereignis (Angriff, Verteidigung, Gruendung, Beute, Spionage); die Meldungen des
Spiels nehmen den Text aus dieser Datei statt eines neutralen Satzes. Fertig ist der Schnitt, wenn
jede Bot-Meldung eine Stimme traegt, ein Bot ohne Eintrag weiterhin eine neutrale Meldung erzeugt
(kein Absturz) und eine Wache belegt, dass kein Text im Code steht. **Danach** die drei offenen
Kampfregeln (2, 4, 6), dann **C** (fliessende Ansichten); `main.py` zerlegen und Skill kuerzen folgen
nach der Story (Daniels Entscheidung). **Der volle Sammellauf, die Registerzeile und die
Protokollzeile gehoeren zum Abschluss jedes Schnitts.**

---

# STAND 04.11.2026, 10:45 - externe Projektpruefung verarbeitet (Register 182)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Ein fremdes Modell hat zum ersten Mal von aussen auf das Projekt geschaut** - auf Auftrag von Daniel,
mit einer Kostengrenze von 3 USD, ohne Dateizugriff (Daten nur als Text). Zwei Gutachten: Arbeitsweise
(13.791 Zeichen) und Spiel/Story/Code (10.037 Zeichen), zusammen 33.730 Token. **Der wichtigste Befund
ist gemessen und unangenehm:** 294 von 532 Commits (55 Prozent) aendern ausschliesslich Dokumente - die
Buchhaltung ist groesser als der Bau. Zweiter Befund: der Sammellauf kostet 9 bis 12 Minuten je
Code-Schnitt. Dritter: das Spiel hat kein Intro, ein Fremder findet keine Geschichte.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Gutachten | A 13.791 Zeichen, B 10.037 Zeichen, 33.730 Token, 287 s Modellzeit | `docs/PRUEFVERMERK_EXTERNE_PRUEFUNG_20261104.md` |
| Kernbefund 1 | **294 von 532 Commits aendern nur `docs/`** | `git log --pretty --name-only`, eigene Zaehlung |
| Kernbefund 2 | Sammellauf 162 Dateien, 9 bis 12 Minuten je Code-Schnitt | `docs/audits/` |
| Kernbefund 3 | kein Story-Intro im Code, nur Statuszeile und Beratertexte | `grep "Willkommen"` in `src/main.py` |
| Uebernommen | Teststufen smoke/kern/voll, Story 1 (Intro, Vorgeschichte, Siegtext), Story 2 (Bot-Stimmen, Fraktions-Kurztexte) | Pruefvermerk Abschnitt 2 |
| Abgelehnt (mit Grund) | Protokoll abschaffen, 20 Limbus-Dimensionen reduzieren, Kommentarpflicht abschaffen | Pruefvermerk Abschnitt 3 |
| Offen (Daniel entscheidet) | `main.py` zerlegen (13.479 Zeilen), Skill von 74.370 Zeichen kuerzen, Uebergabe zweiteilen | Pruefvermerk Abschnitt 5 |
| Pruefdateien / Register / Protokoll | **162** / **182** / **295 Zeilen** (Zielgroesse eingehalten) | `ls tests/test_*.py`, `grep -c '^\| [0-9]'`, `wc -l` |

## Der EINE naechste Schritt

**Teststufen fuer den Sammellauf** (der einzige Vorschlag der Pruefung, der sofort Zeit spart): eine
Stufe `smoke` fuer Dokument- und Daten-Aenderungen, `kern` fuer ein Modul und `voll` fuer Code-Schnitte,
ausgewaehlt nach den geaenderten Pfaden. Die Projektregel bleibt unangetastet: **ein Code-Schnitt gilt
nur mit vollem Lauf NACH dem letzten Fix**. Fertig ist der Schnitt, wenn es die drei Stufen gibt, eine
Wache belegt, dass `voll` weiter alle Pruefdateien faehrt, und ein Doku-Commit nachweislich unter drei
Minuten bleibt. Danach **Story 1** (Intro mit Weltbruch und Auftrag, Vorgeschichte, Siegtext).
**Der volle Sammellauf, die Registerzeile und die Protokollzeile gehoeren zum Abschluss jedes
Schnitts.**

---

# STAND 04.11.2026, 09:38 - S-12 und S-11: alle Felder, Kartenwahl nach Engpass (Register 180/181)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Zwei Schnitte in einem Zug, beide gemessen.** (1) **S-12:** der Huegel wird mitbelegt (Steinmetz,
dann Goldmine - beim Raecher Erzmine), und die Feldreserve fuer Haus, Bibliothek, Lager, Schmiede,
Akademie und Wall ist jetzt eine FELDLISTE statt einer Zahl. Der Unterschied ist gross: auf
`original-001` galten 19 freie Sumpffelder als erfuellte Reserve, danach fand kein Haus mehr Platz.
(2) **S-11:** die Kartenwahl waehlt nach dem ENGPASS der Taktik. Der Engpass wird gerechnet
(Bedarf eines Zyklus aus Siedlerkarren und Gruendung, geteilt durch den Ertrag der Mindestanlagen),
nicht geraten - Holz steht bei jeder Taktik vorn, Pferde sind mit vier Stueck gar kein Engpass.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Neue Wachen | `test_gesamtsieg` **47/0/0**, `test_drachen` **88/0/0** | eigene Laeufe |
| Gegenproben | Huegel-Fuellung aus **20 Pruefungen rot**; Taktik im Engpass ignoriert **5 rot**; beide Dateien per SHA256 unveraendert zurueck | eigene Laeufe |
| Voller Sammellauf | erster Lauf **157 von 162 gruen, 3 rot** (`sammellauf_20261104_0940.log`); nach dem Nachziehen der drei Wachen **160 von 162 gruen, 0 rot, 728 s**, 6.521 Pruefungen, 56 Befunde (`sammellauf_20261104_1000.log`) - die zwei nicht gruenen sind die ausgesetzten Dateien | `docs/audits/` |
| Messung 24 Spieltage | Dorfzahl **4/4/4/4/4** in beiden Schnitten; Anlagen je Dorf **63 bis 98** (vorher 52 bis 97) | `tools/bot_wirtschaft_messung.py` |
| Engpass-Paare | Pluenderer und Spaeherin holz/stein, Waechterin holz/wolle, Bastionier und Raecher holz/nahrung | `main.bot_taktik_engpass` |
| Pruefzusage S-11 | Pluenderer waehlt `original-006`, Waechterin `original-118b` bei DERSELBEN Kandidatenliste | `tests/test_s11_kartenwahl_engpass.py` |
| Bedarf eines Zyklus | 680 Holz, 550 Nahrung, 300 Stein, 150 Leder, 100 Wolle, 80 Metall, 4 Pferde | `spieloekonomie.gruendungskosten()` + `U["Siedlerkarren"]` |
| Schalter | `data/bot_wirtschaft.json`: `kartenwahl_stufe` = **engpass** (mittel/schwer/leicht bleiben waehlbar) | Datendatei |
| Pruefdateien / Register | **162** / **181** | `ls tests/test_*.py \| wc -l`, `grep -c '^\| [0-9]' docs/PRUEFREGEL_ORIGINAL.md` |
| Kampfregeln (gemessen) | **fuenf von acht stehen schon im Code** (1, 3, 5, 7, 8); offen: **2 Flucht, 4 Beute-Reihenfolge Gold zuerst, 6 Mauerreparatur mit Bauzeit** | `docs/AUDIT_KAMPFREGELN_20261104.md` |
| Offener Befund | Stein laeuft ueber (36.000 bis 61.000 je Bot), weil der Huegel nach Ertrag den Steinmetz traegt | `docs/MESSUNG_S12_ALLE_FELDER_20261104.md`, Abschnitt 3 |

## Der EINE naechste Schritt

**Das Entwicklungsprotokoll verdichten** (Daniels Antwort vom 04.11., 09:15: eigener Schritt nach
S-12, Zielgroesse unter 320 Zeilen). Verfahren nach Skill: die unveraenderte Fassung als eigene Datei
sichern und committen, die neue Fassung im Zwischenspeicher schreiben, mit
`tools/pruefe_protokoll.py --nach` pruefen (Rueckgabe 0), dann einsetzen - alle Commit-Kennungen und
Pruefzahlen bleiben erhalten. Danach die **acht Kampfregeln** in der Reihenfolge 1 bis 8
(`docs/ENTSCHEIDUNGEN_KAMPFREGELN_20261103.md`), dann **C** (Refresh fuer fuenf Ansichten).
**Der volle Sammellauf, die Registerzeile und die Protokollzeile gehoeren zum Abschluss jedes
Schnitts.**

---

# STAND 04.11.2026, 08:46 - S-8 Stufe 3: jede Bot-Taktik baut nach eigenem Plan (Register 179)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Die fuenf Bots bauen nicht mehr alle dasselbe.** Bis heute setzte `bot_doerfer_bebauen` in jedem
Bot-Dorf dieselbe Zahl je Gebaeude (26 bis 30 Anlagen), unabhaengig von der Taktik - die Karte blieb
halb leer. Jetzt hat jede Taktik MINDESTZAHLEN und eine Restfeld-Regel in
`data/bot_bauplan.json` (`anlagen_bauplaene`): erst die Mindestzahlen in ihrer Zone (Phase A, in
Runden, damit eine Anlage nicht den ganzen Berg nimmt), dann die freien Felder nach Ertrag (Phase C).
Zwei Sperren halten den Plan gesund: **9 Felder bleiben fuer den Gebaeude-Bauplan frei** (Haus,
Bibliothek, Lager, Schmiede, Akademie, Diebesgilde, Bogenbauer, Wall - sonst faende `bot_dorf_bauen`
keinen Platz und es gaebe keine Forschung, keine Kaserne, keine Truppen), und **das letzte
Bibliotheksfeld** bleibt unangetastet, weil eine Bibliothek nur auf Grasland, Steppe oder Nebelsee
stehen darf.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Neue Wache | `tests/test_s8_stufe3_bauplaene.py` **98/0/0** | eigener Lauf |
| Voller Sammellauf | **159 von 161 gruen, 0 rot, 520 s**, 6.330 Pruefungen, 56 Befunde (Start 08:59; die zwei nicht gruenen sind die dauerhaft ausgesetzten Dateien) | `docs/audits/sammellauf_20261104_0900.log` |
| Gegenprobe | **40 Pruefungen rot** (Plan-Block abgeschaltet), `data/bot_bauplan.json` per SHA256 unveraendert zurueck | eigener Lauf |
| Messung 24 Spieltage | Dorfzahl **4/4/4/4/4**, Anlagen je Dorf **52 bis 97** (vorher 26 bis 30) | `tools/bot_wirtschaft_messung.py`, `s8s3_final.json` |
| Taktik-Profile | Raecher **39** Erzminen / 8 Goldminen, Spaeherin **31** Pferdezuchten, Waechterin **21** Steinmetze, Bastionier 31 Goldminen | Anlagenzahl je Dorf |
| Metall in der Kasse | **12.172 bis 55.832** (vorher 11.435 bis 16.584) | Messung |
| Daten | `anlagen_bauplaene` mit fuenf Taktiken, Restfeld-Reihenfolge je Gelaende, Holzfaeller-Deckel 6 | `data/bot_bauplan.json` |
| Belegte Ertraege | Jaeger **2 Nahrung + 2 Leder** auf Wald, Zuchten **3** auf Grasland, Farm **4 / 2** | `data/buildings.json` (gemessen, nicht getippt) |
| Nachgezogene Wachen | `test_bot_nahrung` **48/0/0**, `test_bot_dorf_als_ort` **42/0/0**, `test_bot_warenkette` **36/0/1** (BEFUND: Berg-arme Karte, 5 Bergfelder fuer 8 Anlagen) | eigene Laeufe |
| Pruefdateien / Register | **161** / **179** | `ls tests/test_*.py \| wc -l`, `grep -c '^\| [0-9]' docs/PRUEFREGEL_ORIGINAL.md` |
| Fragen dieser Sitzung | **4 gestellt, 4 entschieden** (04.11.2026, rund 09:15) - Zuordnung der Taktiken so lassen, Erzmine bleibt vorne, Protokoll nach S-12 verdichten, Metall-Abnehmer nach S-11 | `docs/FRAGEN_AN_DANIEL_20261104.md` (Abschnitt Antworten) |
| Kopf | Vorgaenger `78a6d0d`; der Commit mit diesem Block ist der neue Kopf | `git log --oneline -1` |

## Der EINE naechste Schritt

**S-12: alle Felder nutzen.** Der Bauplan fuellt heute die Gelaendearten Wald, Grasland, Berg und
Steppe; Huegel bleibt fuer die ertraglosen Gebaeude frei, Sumpf und Nebelsee tragen nichts. S-12
erweitert die Restfeld-Regel so, dass ein Bot-Dorf jedes Feld belegt, das seine Taktik sinnvoll
fuellen kann, und belegt die Pruefzusage aus dem Konzept: die Zahl der Anlagen ist von Karte zu Karte
VERSCHIEDEN (sie ist es seit heute schon - 52 bis 97 -, aber Huegel und Sumpf sind noch offen).
Danach S-11 (Kartenwahl mit Feldverstaendnis). **Der volle Sammellauf, die Registerzeile und die
Protokollzeile gehoeren zum Abschluss jedes Schnitts.**

**Reihenfolge nach Daniels Antworten vom 04.11.2026 (rund 09:15):** S-12 -> Protokoll verdichten
(eigener Schritt, Zielgroesse unter 320 Zeilen; vorher die unveraenderte Fassung sichern und
committen) -> S-11 -> eigener Schnitt "Metall in Truppen" (Abnehmer fuer das gehortete Metall des
Raechers).

---

# STAND 03.11.2026, 23:2x - Weltkarte mit gemaltem Rahmen, Gelaendeton und Goldrand (Register 178)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Die Weltkarte sieht jetzt aus wie ein Kaestchen aus dem Original, nicht wie ein Farbgitter.** Um das
Gelaendekaestchen liegt der gemalte Kachelrahmen der C2-Lieferung als 9-Slice-Rahmen (Ecken fest, Kanten
gekachelt), die Felder tragen ihren Gelaendeton ohne harten schwarzen Umriss, das Gitter ist eine feine
dunkelbraune Trennlinie, und die Auswahl ist ein **Goldrand** statt eines blauen Kastens. Groesse und
Aufbau sind unveraendert: 400 x 400 px, 20 px je Feld, 10 x 10 Felder.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Neue Wache | `tests/test_weltkarte_rahmen.py` **32/0/1** | eigener Lauf |
| Gegenprobe | **6 Pruefungen rot** (Rahmen abgeschaltet, Goldrand zurueck auf Blau), `main.py` per SHA256 unveraendert zurueck | eigener Lauf |
| Nachbarn | `test_marsch_optik` 63/0/0, `test_portal_fremdblick` 18/0/1, `test_spionage` 146/0/0, `test_weltbild_gelaende` 135/0/0, `test_portal_uebersicht` 61/0/0, `test_overlay_ingame` 42/0/1 | eigene Laeufe |
| Rahmen | vier Bildleisten, Ecke **pixelgleich** mit `kachelrahmen_ruhe.png`, Rand **16 px** | `gebaeude_optik.rahmen_kanten` |
| Gitter | **44** Linien in `#2b1a12` (vorher 400 Umrisse `#111111`) | `main.RASTER_LINIE` |
| Auswahl | `#ffcc33` (Skin-Gold) auf `#1b0d06`; der blaue Rand `#38BDF8` ist weg | `_render_portal` |
| Bild-Beleg | `C:/Users/saras/AppData/Local/hermes/cache/scratch/weltkarte_rahmen_beleg.png` (ganzer Schirm, Rahmen und Goldrand sichtbar) | eigener Lauf mit `.venv`-Python |

## Zwei Befunde vor dem Bau (gemessen, nicht geraten)

1. **Die Ressourcenleiste taugt NICHT als Rahmen.** In ihrem Band stehen acht Symbole und acht leere
   Zahlenschilde (`data/ressourcenleiste.json`, acht Felder); als Rahmen gedehnt waeren sie verzerrt.
   Daniel hat deshalb den **Kachelrahmen als 9-Slice-Rahmen** freigegeben. Ein breiter eigener
   Kartenrahmen bleibt eine Bildlieferung.
2. **Drei bestehende Wachen mussten ihren Anker verschieben**: die Zeichenflaeche sitzt jetzt in einem
   Traeger, deshalb suchen `test_portal_fremdblick`, `test_spionage` und `test_marsch_optik` sie im Baum
   statt nur unter den direkten Kindern. Die Zusagen selbst sind unveraendert (genau eine Karte, dieselben
   Tags, Restzeit-Zeile UEBER der Karte).

## Der EINE naechste Schritt

**S-8 Stufe 3: die Taktik-Bauplaene** aus `D:/Arbeiten/Hermes/Notizen/S8_STUFE3_BAUPLAENE_20261103.md`
nach `data/bot_bauplan.json` (Mindestzahlen je Taktik, Restfelder nach Ertrag), **die Zahlen mit den
ECHTEN Werten nachrechnen** (Jaeger 2/2, Zuchten 3, Farm 4/2 - der Entwurf hatte drei Annahmen falsch),
dann 24 Spieltage mit `tools/bot_wirtschaft_messung.py` messen. Danach **S-12** (alle Felder nutzen).
**Der volle Sammellauf und die Protokollzeile gehoeren zum Abschluss jedes Schnitts.**

---

# STAND 03.11.2026, 22:55 - Overlay-Basis gebaut: Dialoge liegen INGAME, kein Desktop-Fenster mehr (Register 177)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Die drei haeufigsten Dialoge sind keine eigenen Fenster mehr.** Daniel (22:2x): keine Desktop-Zusatzfenster,
sondern Dialoge INGAME ueber dem Hauptfenster, Hintergrund abgedunkelt und durchscheinend. Gebaut ist die
Basis dafuer - eine Flaeche ueber dem Inhaltsbereich, ein vorgerendertes Abdunkelbild (Bildschirmabzug des
Inhalts plus Alpha-Schleier, weil Tk keine Transparenz je Widget kann), `grab_set` als Eingabesperre, Escape
und Klick daneben schliessen -, und darauf umgestellt sind **Dorf-Optionen, Truppen-Auswahl und
Spionagebericht**. Im Code stehen jetzt **7 statt 10** `Toplevel`.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Neue Wache | `tests/test_overlay_ingame.py` **42/0/1** | eigener Lauf |
| Voller Sammellauf | **157 von 159 gruen, 0 rot, 648 s** (Start 22:54), 6.189 Pruefungen, 54 Befunde; die zwei AUSGESETZT-Dateien sind dokumentiert zurueckgezogen | `docs/audits/sammellauf_20261103_2255.log` |
| Gegenprobe | **1 Pruefung rot** (Schliessen im Ansichtswechsel abgeschaltet), `main.py` per SHA256 unveraendert zurueck | eigener Lauf |
| Nachbarn | `test_spionage` 146/0/0, `test_portal_fremdblick` 18/0/1, `test_marsch_optik` 63/0/0, `test_doppelpuffer` 15/0/0, `test_baseline` 40/0/0, `test_startspiel` 62/0/1, `test_oberflaeche_original` 65/0/0 | eigene Laeufe |
| Umgestellte Dialoge | `_bot_dorf_optionen`, `_truppen_auswahl`, `_spionage_bericht_anzeigen` | `grep -n "tk.Toplevel(" src/main.py` |
| Zahlen | Deckkraft **140**, Kastenbreite **560**, Escape und Klick daneben an | `data/overlay.json` (Daniel stellt sie ohne Code) |
| Bild-Beleg | `C:/Users/saras/AppData/Local/hermes/cache/scratch/overlay_beleg.png` (Fenster 1280x820, Dialog offen, Inhalt scheint dunkel durch) | eigener Lauf mit `.venv`-Python |

## Was das Bau-Menue betrifft (Befund, nicht Wunschdenken)

Die Uebergabe nannte als ersten Dialog das **Bau-Menue**. Gemessen: es ist **kein `Toplevel`** - die
Bauauswahl liegt als Feld direkt in der Siedlungskarte (`_render_settlement_map`, Abschnitt "angebote").
Es gab dort also nichts umzustellen; an seiner Stelle ist der **Dorf-Optionen-Dialog** ingame gegangen
(der bei jedem Klick auf ein fremdes Dorf aufgeht und zur Truppen-Auswahl fuehrt).

## Der EINE naechste Schritt

**Die Weltkarte: Rahmen als Bildleiste (`main.leiste_zusammensetzen`) UND Felder mit Gelaendeton, feiner
Trennlinie und Goldrand fuer die Auswahl** - Groesse und Aufbau bleiben (Daniel 22:1x). Danach **S-8 Stufe 3**
(Taktik-Bauplaene aus `D:/Arbeiten/Hermes/Notizen/S8_STUFE3_BAUPLAENE_20261103.md` nach
`data/bot_bauplan.json`, Zahlen mit den ECHTEN Werten nachrechnen, 24 Spieltage messen). **Der volle
Sammellauf und die Protokollzeile gehoeren zum Abschluss jedes Schnitts.**

---

# STAND 03.11.2026, 22:20 - A gebaut: kein Flackern mehr beim Ansichtswechsel (Register 176)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Der Ansichtswechsel baut nicht mehr ab und dann auf, sondern baut NEU und tauscht erst dann.**
Damit ist das Flackern weg, das Daniel als "abgehakt" beschrieben hat - ohne dass eine der 23 Ansichten
angefasst wurde. Gemessene Ursache: `_render_view` leerte den Inhaltsbereich bei jedem Aufruf
(`widget.destroy()` je Kind) und fuellte ihn neu, an **46 Aufrufstellen**.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Neue Wache | `tests/test_doppelpuffer.py` **15/0/0** | eigener Lauf |
| Gegenprobe | **3 Pruefungen rot** (alter destroy-Zweig eingesetzt), Datei per SHA256 unveraendert zurueck | eigener Lauf |
| Bestehende Wachen | `test_baseline` 40/0/0, `test_oberflaeche_original` 65/0/0, `test_startspiel` 62/0/1 | eigene Laeufe |
| Voller Sammellauf | **156 von 158 gruen, 0 rot, 548 s** (Start 22:20), 6.146 Pruefungen | `docs/audits/sammellauf_20261103_2220.log` |

## Der Ablauf ab jetzt (Daniels Einordnung 22:2x, mit den neuen Auftraegen)

| # | Schritt | Warum hier |
|---|---|---|
| 1 | **A Doppel-Puffer** | ERLEDIGT 03.11.2026 (Register 176) - wirkt auf alle Ansichten |
| 2 | **Overlay-Basis + die drei haeufigsten Dialoge ingame** | Daniels Frage 1: keine Desktop-Fenster mehr. Zehn `Toplevel` sind der Vorrat; Bau-Menue, Truppen-Auswahl, Nachrichten zuerst |
| 3 | **Weltkarte: Rahmen als Bildleiste + Felder mit Gelaendeton und Goldrand** | Daniels Entscheidung; Groesse und Aufbau bleiben |
| 4 | **S-8 Stufe 3: Taktik-Bauplaene** in `data/bot_bauplan.json` (Mindestzahlen, Restfelder nach Ertrag) | **Entwurf liegt vor** (`D:/Arbeiten/Hermes/Notizen/S8_STUFE3_BAUPLAENE_20261103.md`, drei Annahmen berichtigt: Jaeger 2/2, Zuchten 3, Farm 4/2); Bau offen |
| 4b | **S-12 Alle Felder nutzen** (Daniel 22:2x) | der Bauplan fuellt die Karte, statt eine feste Zahl abzuarbeiten - `docs/KONZEPT_BOT_SPIELNUTZUNG_20261103.md` |
| 4c | **S-11 Kartenwahl mit Feldverstaendnis** | der Bot waehlt die Karte nach dem, was ihre Felder fuer SEINE Taktik bringen - nicht mehr Gold pauschal |
| 4d | **S-13 Abriss und Umbau fuer Bots** | der Spieler kann abreissen, der Bot heute nicht; Kernregeln und Sperren gelten mit |
| 4e | **S-14 entschieden: kein Gleichstand** | Bots behalten **drei Neugruendungen = vier Doerfer**; Ausgleich kommt aus besserem Spiel (S-11 bis S-13) |
| 4f | **S-15 Dorf aufgeben und neu gruenden** (Bot UND Spieler) | Daniel: ein Dorf vernichten und auf einer besseren Karte neu gruenden - sechs Gestaltungsfragen stehen im Konzept |
| 5 | **Die acht Kampfregeln 1 bis 8** | abgesegnet (Register 175), je Regel Wache + Sammellauf |
| 6 | **C: Refresh-Pfad fuer die fuenf haeufigsten Ansichten** | hier wird es wirklich fluessig; braucht B und die Overlay-Basis |
| 7 | V-1 bis V-5 (Berichte, Postfach), S-7 Karawanen, S-9 Stil, W-3, Story | wie gehabt |
| 8 | O-1b echte Hintergrundbilder | wartet auf Daniels Generator-Loesung (Midjourney abgebrochen) |

## Der EINE naechste Schritt

**Die Overlay-Basis bauen** (danach Bau-Menue, Truppen-Auswahl und Nachrichten darauf umstellen): ein
dunkles Alpha-Bild als Flaeche ueber dem Inhalt, darueber ein Kastenbild aus `gebaeude_optik`,
`grab_set` fuer die Eingabesperre, Escape schliesst. Der Sammellauf und die Protokollzeile gehoeren zum
Abschluss.

---

# STAND 03.11.2026, 22:1x - S-8 Stufe 2 (Feld-Prioritaeten, Erzmine 3) und die acht Kampfregeln entschieden

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**S-8 Stufe 2 gebaut:** `bot_doerfer_bebauen` setzt jede Anlage zuerst in ihre Zone (bevorzugtes
Gelaende) und teilt erst, wenn dort nichts mehr frei ist - so nimmt ein Holzfäller keine Steppe, die
eine Rinderfarm braucht. Die Zonen stehen als `feld_prioritaeten` in `data/bot_wirtschaft.json`
(wald/steppe/huegel/berg/grasland), hergeleitet aus den belegten Erträgen und aus Daniels
Jaeger-Vorgabe. **Erzmine auf 3** (Daniel 22:0x: mehrere Erzminen wie der Spieler, dasselbe fuer die
anderen Gebaeude - die allgemeine Erhoehung kommt mit Stufe 3).

| Gegenstand | Wert | Beleg |
|---|---|---|
| Dorfzahl nach 24 Spieltagen | **4/4/4/4/4** (unveraendert) | `tools/bot_wirtschaft_messung.py --tage 24` |
| Metall in der Kasse | **11.435 bis 16.584** (vorher 2.494 bis 5.388) | dieselbe Messung |
| Anlagen je Dorf | 30 (26 auf der Karte ohne freies Bergfeld - die Karte bestimmt es) | dieselbe Messung |
| Wachen | `test_bot_warenkette` 35/0/0, `test_bot_dorf_als_ort` 32/0/0, `test_s8_ertrag_aus_anlagen` 21/0/0, `test_bot_kartenprofil` 40/0/0 | eigene Laeufe |
| Voller Sammellauf fuer diesen Stand | **155 von 157 gruen, 0 rot, 482 s** (Start 22:05), 6.131 Pruefungen | `docs/audits/sammellauf_20261103_2205.log` |

**Die acht Kampfregeln sind abgesegnet** (Register 175, `docs/ENTSCHEIDUNGEN_KAMPFREGELN_20261103.md`):
fusstruppen_begriff, flucht_formel, beute_verteilung, beute_reihenfolge (**Gold zuerst**),
belagerungsturm_mauerschaden (1-4 minus Wallstufe), mauer_reparatur (aktiv, **mit Bauzeit**),
vorrunde_wiederholung, geraetebeute (Zerstoerung, 10 Prozent je Sequenz, max. 50). Nah-/Fernkampf
bekommt ein eigenes Kennzeichen je Einheit, weil `einheiten.ROLLEN` beide auf `kaempfer` abbildet.

## Einschaetzung Oberflaeche (Daniel 22:1x) - liegt vor

`docs/EINSCHAETZUNG_INGAME_FENSTER_20261103.md`: **beides ist moeglich.** (1) Ingame-Dialoge statt
Desktop-Fenster: JA - Overlay im Hauptfenster, Abdunkelung als vorgerendertes Alpha-Bild (Pillow ist da),
kein `Toplevel` noetig; heute stehen **10** Toplevel im Code. (2) Kein Neuaufbau je Klick: JA, in vier
Stufen - A Doppel-Puffer (klein, wirkt ueberall gegen Flackern), B Karte ohne Neuaufbau (Canvas-Objekte
einmal erzeugen, dann nur aendern), C Refresh-Pfad fuer die fuenf haeufigsten Ansichten (hier wird es
wirklich fluessig), D Rest. Ursache gemessen: `_render_view` zerstoert bei **46** Aufrufstellen alle
Widgets und baut sie neu. Weltkarte: drei Designvorschlaege im selben Dokument (Rahmen als Bildleiste,
Felder mit Gelaendeton und Goldrand, spaeter gemalte Kacheln).

## Daniels Entscheidungen zur Oberflaeche (22:2x) - jetzt der naechste Schnitt

| Frage | Entscheidung |
|---|---|
| Reihenfolge | **Oberflaeche zuerst**: A (Doppel-Puffer) **und** die Overlay-Basis mit den drei haeufigsten Dialogen - die acht Kampfregeln und S-8 Stufe 3 kommen danach |
| Weltkarte | **Rahmen als Bildleiste UND Felder mit Gelaendeton und Goldrand** (Vorschlag 3+2 zusammen) |

**Rezept fuer den naechsten Schnitt (aus `docs/EINSCHAETZUNG_INGAME_FENSTER_20261103.md`):**

1. **A - Doppel-Puffer in `_render_view`:** den Inhalt in ein NEUES, noch nicht gepacktes Frame bauen
   (die Renderer lesen `self.content`), dann altes Frame zerstoeren und das neue in einem Zug einsetzen.
   Damit verschwindet das Flackern bei allen 46 Aufrufstellen, ohne dass eine Ansicht angefasst wird.
   Pruefzusage: ein Ansichtswechsel hinterlaesst nie einen leeren Inhaltsbereich (Wache ueber
   `winfo_children()` vor und nach dem Wechsel), und die Zahl der Widgets ist vor/nach gleich.
2. **Overlay-Basis:** ein Baustein `_overlay_oeffnen(titel, bauer)` - dunkle Alpha-Flaeche als Bild
   (Pillow, `(0,0,0,140)`) ueber den ganzen Inhaltsbereich, darueber ein Kastenbild aus
   `gebaeude_optik`, `grab_set` fuer die Eingabesperre, Escape schliesst. Danach die drei haeufigsten
   `Toplevel`-Dialoge darauf umstellen (Bau-Menue, Truppen-Auswahl, Nachrichten).
3. **Weltkarte:** Rahmen mit `main.leiste_zusammensetzen` (Ecken fest, Kanten dehnbar) und Felder mit
   Gelaendeton, feiner Trennlinie, Goldrand fuer die Auswahl.

**Jeder Schritt: eigene Wache, voller Sammellauf, Registerzeile, Protokollzeile.**

## Der EINE naechste Schritt

**Die Oberflaeche: A (Doppel-Puffer) und die Overlay-Basis (Daniel 22:2x).** Danach die acht Kampfregeln
in der Reihenfolge 1 bis 8 - je Regel eine Wache, der Sammellauf und die
Protokollzeile. Vorher steht nur noch **S-8 Stufe 3** (Bauplan je Taktik in `data/bot_bauplan.json`,
Mindestzahlen plus Restfelder), weil es die Erzmine-Zahl endgueltig festlegt. **Der Sammellauf gehoert
zum Abschluss jedes Schnitts, und die Protokollzeile dazu ebenfalls.**

---

# STAND 03.11.2026, 21:20 - S-8 Stufe 1: Ertrag aus den GEBAUTEN Anlagen (Register 174)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Der Ertrag eines Bot-Dorfes kommt jetzt aus seinen Anlagen, nicht mehr aus dem Kartenprofil.**
Gemessen war vorher: ein Dorf mit 48 Holzfällern erntete genau so viel wie eines mit 5 - jede
Bauplan-Logik war damit wirkungslos, und Daniels Vorgabe (der Bot nutzt seine Karte mit Gebaeuden
sinnvoll) konnte nicht greifen. Gerechnet wird jetzt mit DERSELBEN Kernfunktion wie beim Spieler
(`wirtschaft.ertrag_gesamt`: je Feld die Anlage und ihr Gelaende, plus Grundeinkommen und Volksfaktor) -
eine Wahrheit fuer Kern und Anzeige (F-04). Das Kartenprofil ist nur noch **Vorschau** und **Rueckfall**
fuer Doerfer ohne jede Anlage (alte Spielstaende).

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf | `052ac0a` (S-8 Stufe 1), Arbeitsbaum leer | `git log --oneline -1`, `git status --porcelain` |
| Schalter | `data/bot_wirtschaft.json`: `ertrag_weg` **von `karte` auf `anlagen`**; `karte` und `felder` bleiben als Vergleich | Datei |
| Dorfzahl nach 24 Spieltagen | **4/4/4/2/4 -> 4/4/4/4/4** (Silra von 2 auf 4) | `docs/MESSUNG_S8_ERTRAG_AUS_ANLAGEN_20261103.md` |
| Holzvorrat Silra | **471 -> 34.136** (Hauptdorf Tag 24: 151 -> 7.610) | dieselbe Messung |
| Ertrag je Dorf | statt einseitigem Profil ausgeglichen: Haug Stein 1,90 -> **12,35**, Gold 1,50 -> **6,00** | dieselbe Messung |
| Neues Messwerkzeug | `tools/bot_wirtschaft_messung.py --tage 24 [--weg karte] [--aus datei]` | Werkzeug |
| Neue Wache | `tests/test_s8_ertrag_aus_anlagen.py` **21/0/0**, Gegenprobe **6 Pruefungen rot** | eigener Lauf |
| Nachgezogene Wachen | `test_bot_kartenprofil` **40/0/0**, `test_bot_takt_kern` **27/0/1**, `test_bot_warenkette` **35/0/0** | eigene Laeufe |
| Register | **174** | `grep -c '^| [0-9]' docs/PRUEFREGEL_ORIGINAL.md` |

## Drei Befunde, die der Umbau aufgedeckt hat (alle behoben)

1. **Ohne Erzmine erntete kein Bot-Dorf Metall** - das Metall kam vorher aus dem Kartenprofil, also aus
   dem Nichts. Ein Siedlerkarren kostet **80 Metall**; damit wurde kein Karren gebaut und **kein Bot
   gruendete** (Dorfzahl fiel zuerst auf 3/3/3/2/3). Behoben: **eine Erzmine** im Bauplan
   (`data/bot_wirtschaft.json`, VORSCHLAG fuer die Zahl 1, 3 Metall/h auf Berg).
2. **`bot_karren_bauen` buchte vor der Pruefung.** Ein Dorf, das schon einen Karren hatte, verlor bei
   jedem Aufruf **200 Holz** (erst bezahlen, dann ablehnen). Reihenfolge korrigiert; die Wache belegt:
   zweiter Karren kostet jetzt nichts. **Ob dieser Fehler den frueheren Holzschwund erklaert, ist NICHT
   belegt** - im Kartenprofil-Lauf blieb die Kasse gleich, weil dort fast nie genug Metall fuer die
   Buchung im Lager war.
3. **Die Gruendung nahm das REICHSTE Dorf als Quelle** und lehnte ab, wenn dort kein Karren stand - auch
   wenn zwei andere Doerfer einen hatten (Grom blieb bei drei Doerfern). Jetzt kommen nur Doerfer MIT
   Karren als Ausgangsdorf in Frage.

## Der EINE naechste Schritt

**S-8 Stufe 2: Feld-Prioritaeten je Gebaeude** (`docs/KONZEPT_BOT_BAUPLAN_20261103.md`, Stufe 2) - in
den Daten steht je Gebaeude, welches Gelaende es bevorzugt (Holzfaeller und Jaeger Wald, Rinderfarm und
Farm Grasland, Steinmetz und Erzmine Berg) und welches nur als Notloesung zaehlt. Ohne diese Prioritaeten
belegen Holzfaeller die Steppe-Felder und die Zuchten werden nicht mehr gebaut (gemessen). Danach Stufe 3
(Bauplan je Taktik mit Mindestzahlen). **Der Sammellauf gehoert zum Abschluss jedes Schnitts, und die
Protokollzeile dazu ebenfalls.**

## Daniels Antworten aus der Runde 21:45 (in dieser Reihenfolge abarbeiten)

| Frage | Entscheidung |
|---|---|
| Die acht Kampfregeln | **Entwurf jetzt** vom starken Modell vorbereiten, Daniel segnet die Liste in EINEM Durchgang ab (Auftrag `docs/auftraege/AUFTRAG_KAMPFREGELN_20261103.md`, Ziel `D:/Arbeiten/Hermes/Notizen/KAMPFREGELN_20261103.md`) |
| Erzmine im Bot-Bauplan | **mehrere Erzminen, genau wie der Spieler - dasselbe gilt fuer die anderen Gebaeude.** Also nicht die Zahl 1 festschreiben, sondern ueber Stufe 2/3 (Feld-Prioritaeten, dann Bauplan mit Mindestzahlen und Restfeldern) so viele bauen, wie die Karte traegt |
| Obergrenze je Dorf (S-8 Stufe 3) | **alle Felder, die die Taktik sinnvoll fuellt; Restfelder mit dem besten Ertrag** (Mindestzahlen statt Obergrenzen) |
| Ort der Taktik-Bauplaene | **dieselbe Datei erweitern** (`data/bot_bauplan.json`, dort liegt schon ein Bauplan) - EINE Quelle |
| O-1b echte Hintergrundbilder | **ZURUECKGESTELLT**: Midjourney wurde abgebrochen (Daniel: zu teuer), er sucht eine Loesung. O-1a bleibt, bis der Generator geklaert ist - **kein Auftragspaket fuer einen kostenpflichtigen Dienst ohne sein Wort** |

**Der naechste Denk-Auftrag laeuft** (acht Kampfregeln); danach **S-8 Stufe 2 und 3** (Feld-Prioritaeten,
dann Bauplan je Taktik mit Mindestzahlen und Restfeldern - dort wird auch die Zahl der Erzminen
festgelegt). Ausserdem offen: Silra-Diagnose ist mit S-8 Stufe 1 erledigt (Holz 471 -> 34.136), die
Berichte V-1 bis V-5 warten auf die acht Regeln.

# STAND 03.11.2026, 19:26 - Ablauf: Hintergrundbilder als O-1 vor den Postkasten

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Daniels Befund (19:2x):** manche Hintergruende sind „verzerrt und unscharf“. Gemessen, nicht geraten:

| Gegenstand | Wert |
|---|---|
| Hintergrundbilder | **538 x 222 px** (Seitenverhaeltnis 2,42 : 1) - dieselben Dateien wie die Menuebilder |
| Zielflaeche | **980 x 760 px** (1,29 : 1) |
| Skalierung | **3,42 x** hochgezogen, dazu 2,0 px Weichzeichnen und 38 % Abdunkeln |
| Folge | ein flaches Band in einer fast quadratischen Flaeche: cover schneidet die Seiten weg, die Vergroesserung macht es weich |

Das ist dieselbe Klasse Fehler wie die Ressourcenleiste im Oktober (ein BAND als dehnbare FLAECHE behandelt). **Der Fix ist ein eigener Schnitt O-1** und kommt an diese Stelle:

| # | Schritt | Inhalt | Warum an dieser Stelle |
|---|---|---|---|
| 1 | **S-6b Warenkette fuer Bots** (Teil 2) | Karrenbau im Bot-Takt, dann `siedlerkarren_pflicht: true`, Messung ueber 24 Spieltage | laeuft, Teil 1 (Warenhaltung, Ertrag aus der Karte) ist gebaut |
| 2 | **V-3 Vollstaendiger Kampfbericht** | alle Angaben des Angegriffenen; Garnison zum Angriffsmoment, Warteschlange getrennt und danach weiter | Fundament aller Berichte |
| 3 | **V-2 Angriffs- und Verteidigungsbericht** | je Seite eine Sicht, beide Wege | baut auf V-3 |
| 4 | **V-1 Angriffswarnung** | roter Rahmen (helles Rot) um das Hauptfenster waehrend der Wegzeit | klein, sofort sichtbar, W-4-Angriffe laufen schon |
| 5 | **O-1a Uebergang (ERLEDIGT 03.11.2026)** | Vergroesserung der Hintergrundbilder auf **1,25 x** begrenzt (statt 3,42 x), Rest der Flaeche in dunklem Grund (`gebaeude_optik.hintergrund_flaeche`). Bild bleibt scharf, ist aber kleiner als die Flaeche - **kein Ersatz fuer echte Bilder**, nimmt aber den unscharfen Eindruck sofort weg. Optik-Wachen 179/70/81 gruen | sofort machbar und billig gewesen |
| 6 | **V-4 Postkasten** | Uebersicht nach Art, Zeit, Betreff, Kurzfassung, Details aufklappbar | braucht V-2/V-3 (Arten und Felder) und O-1 (Hintergrund) |
| 7 | **V-5 Bot-Auswertung** | Bots lesen Berichte und schliessen daraus | braucht V-3 und V-4 |
| 8 | **S-7 Karawanen** | Transporte zwischen EIGENEN Doerfern | schreibt selbst ins Postfach |
| 9 | **S-9 Stil je Taktik** | was der Bot mit seinem Reichtum TUT | setzt S-6b und S-7 voraus |
| 9b | **O-1b echte Hintergrundbilder** | Prompts liegen fertig in `D:/Arbeiten/Hermes/Notizen/O1_BILDPROMPTS.md` (20 Motive, gemeinsamer Stilbaustein, Safe Area oben zwei Drittel, Negativ-Prompt). **Blockiert auf die Generatorfrage:** Pollinations liefert das falsche Motiv samt Wasserzeichen (belegt: Frau im Wald statt Lagerhalle, 886 x 665 statt 1600 x 1200), ComfyUI ist nicht installiert. Entscheidung noetig: lokale Installation (mehrere GB Modell) oder kostenpflichtiger Dienst | **nach hinten geschoben** (Entscheidung dieser Sitzung; Daniel 19:4x: „kann man notfalls auch nach hinten schieben“): Gameplay und Berichte wiegen schwerer, die Prompts warten ohne Verlust |
| 10 | **W-3 Kampf ueber Weltgrenzen** | teuer mit Deckel | Bau zuletzt von den Kaempfen |
| 11 | **Story (W-11)** | nur das Noetige, sechs Fraktionen | nebensaechlich, zuletzt |

**S-6b ist ERLEDIGT** (Sammellaeufe 153/155 und 154/156, 0 rot). Der naechste Schritt im Ablauf ist
**V-3 (vollstaendiger Kampfbericht)**; das Schema liegt beim starken Modell.

## Offener Befund: Bot-Doerfer sparen nicht fuer die Gruendung (gemessen 03.11.2026)

| Gegenstand | Wert |
|---|---|
| Gruendungs-Mindestbestand (Kern) | **480 Holz, 300 Stein, 250 Nahrung** (`spieloekonomie.gruendungskosten()`) |
| Silra nach 24 Spieltagen | 945 Gold, 1057 Stein, 1990 Nahrung, **189 Holz** - ein Dorf, fuenf Karren |
| Ursache | jeder Karren kostet 200 Holz; dazu Bauten und Forschung - das Dorf haelt nie 680 Holz gleichzeitig |
| Folge | Silra kann nicht gruenden, obwohl er nach Gold, Stein und Nahrung reich ist |

**Versuchte Loesung, verworfen:** eine Ruecklage in `bot_karren_bauen` (Karren nur, wenn danach noch der
Mindestbestand im Dorf liegt). Gemessen danach: Doerfer unveraendert 3/4/4/1/3, aber **Haug, Silra und
Krank bauen 0 Karren** - die Ruecklage verhindert den Karrenbau, ohne eine einzige Gruendung zu
ermoeglichen. Wieder zurueckgenommen; die Wachen sind gruen (23/0/0, 36/0/1).

**Das ist eine Wirtschaftsfrage, keine Karrenfrage** - und inzwischen gemessen:

| Versuch | Ergebnis |
|---|---|
| mehr Holzfaeller (3 -> **5**, Daniels Entscheidung 20:2x) | **keine Aenderung**: 3/4/4/1/3 Doerfer |
| Ruecklage im Karrenbau (danach muss die Gebuehr noch da sein) | **0 Karren** bei Haug, Silra, Krank - Dorfzahl unveraendert |
| 5 Holzfaeller **und** Ruecklage | genauso: 0 Karren, unveraendert |
| Holzverlauf Silra (5 Holzfaeller, 24 Tage) | Tag 3: **1** Holz, Tag 12: 53, Tag 24: 189 - nie ueber 190 |
| Wohin das Holz geht | **5 Karren** (1.000 Holz), **5 Forschungen** (Baukunst 2, Heimlichkeit 3, Wagenbau, Felderwirtschaft, Kriegskunst), **27 Anlagen** |

Der Ertrag reicht rechnerisch (20 Holz/h x 144 h = 2.880 Holz), aber Karren, Forschung und Bauten
verbrauchen ihn laufend. **Ohne eine Prioritaetsregel kommt kein Bot zur Gruendungsgebuehr** - die
Holzmenge allein loest es nicht.

**Die verbleibende Entscheidung:** soll die **Gruendung Vorrang vor Forschung und Bauen** bekommen
(dann pausieren Forschung und neue Anlagen, bis die 480 Holz beisammen sind)? Das ist der einzige
Weg, der nach dieser Messung noch wirkt - er aendert aber das Verhalten der Bot-Doerfer spuerbar.
Empfehlung: **ja, mit Deckel** - nur solange die Gruendung ansteht und die Hoechstzahl nicht erreicht ist.

# STAND 03.11.2026, 19:02 - Ablauf neu geordnet: S-6b vor S-7, Berichte vor Karawanen

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Zwei Vorgaben Daniels (18:53 und 19:00) verschieben die Reihenfolge.** (a) Der Bot muss den **Siedlerkarren** bauen wie der Spieler - damit wird die Warenkette (S-6b) zur Voraussetzung jeder Bot-Gruendung, statt spaeter zu kommen. (b) **Postfach und Kampfberichte** sind ein eigener Block (V-1 bis V-5, `docs/VORGABE_POSTFACH_UND_BERICHTE_20261103.md`) und gehoeren VOR die Karawanen: S-7 und S-9 schreiben selbst Meldungen ins Postfach und sollen nicht gegen ein Format bauen, das danach umgestellt wird.

| # | Schritt | Inhalt | Warum an dieser Stelle |
|---|---|---|---|
| 1 | **S-6b Warenkette fuer Bots** | Stellmacher, Leder, Wolle, Pferde beschaffbar machen; danach `siedlerkarren_pflicht` auf `true` | Daniels Entscheidung 18:53 - ohne Karren gruendet nach der Umstellung KEIN Bot; blockiert S-7, S-9 und die Ziele von W-4 |
| 2 | **V-3 Vollstaendiger Kampfbericht** | Bericht traegt alle Angaben des Angegriffenen (Wall, Garnison, Taktik, Vorraete, Beute, Verluste beider Seiten) | Fundament: ohne diesen Inhalt haben die naechsten drei Schritte nichts zu zeigen |
| 3 | **V-2 Angriffs- und Verteidigungsbericht** | je Seite eine eigene Sicht, beide Wege (Spieler->Bot, Bot->Spieler) | baut direkt auf V-3 |
| 4 | **V-1 Angriffswarnung** | roter Rahmen in hellem Rot um das Hauptfenster, solange ein Angriff auf den Spieler unterwegs ist; danach nur der Bericht | klein und sofort sichtbar; W-4-Angriffe laufen schon, der Spieler soll sie bemerken |
| 5 | **O-1a Uebergang (ERLEDIGT 03.11.2026)** | Vergroesserung der Hintergrundbilder auf 1,25 x begrenzt, Rest der Flaeche in dunklem Grund; Bild bleibt scharf statt 3,42 x aufgeblasen (`gebaeude_optik.hintergrund_flaeche`). **Kein Ersatz fuer echte Bilder**, nimmt aber den unscharfen Eindruck sofort weg | sofort machbar und billig |
| 5b | **V-4 Postkasten** | Uebersicht nach Art, Zeit, Betreff, Kurzfassung; Details aufklappbar | braucht V-2/V-3, weil erst dann feststeht, welche Arten und Felder zu zeigen sind |
| 6 | **V-5 Bot-Auswertung** | Bots lesen eingehende Berichte und schliessen daraus, ob ein weiterer Angriff lohnt | braucht V-3 (Inhalt) und V-4 (Ablage) |
| 7 | **S-7 Karawanen** | Transporte zwischen EIGENEN Doerfern, Reisekosten im Startdorf | schreibt selbst ins Postfach - jetzt in ein fertiges Format |
| 8 | **S-9 Stil je Taktik** | was der Bot mit seinem Reichtum TUT | setzt S-6b und S-7 voraus |
| 9 | **W-3 Kampf ueber Weltgrenzen** | teuer mit Deckel (Daniel 16:08) | Preis ist Denkarbeit, der Bau kommt zuletzt von den Kaempfen |
| 10 | **Story (W-11)** | nur das Noetige, den sechs Fraktionen angepasst | nebensaechlich, zuletzt |

**Der EINE naechste Schritt: S-6b** - der Bot baut den Siedlerkarren wie der Spieler. Erst messen, welche Waren und Gebaeude der Kern fuer einen Karren verlangt (`spieloekonomie.gruendungskosten()`, `warenrezepte.json`, Werkstattkette), dann die Bot-Wirtschaft nachziehen, dann `siedlerkarren_pflicht` auf `true` und ueber 24 Spieltage pruefen, dass jeder Bot vier Doerfer hat. Der Sammellauf gehoert zum Abschluss, das Protokoll traegt die Zeile dazu.

# STAND 03.11.2026, 18:47 - T-1: Ingame-Texte mit echten Umlauten (Register 171)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Alles, was der Spieler liest, traegt jetzt echte deutsche Rechtschreibung** - „wählen“ statt „waehlen“, „Gebäude“, „für“, „zurück“, „Kästchen“, „Menü“. Daniels Vorgabe (17:15) ist damit erfuellt: Knoepfe, Menues, Reiter, Dialoge, Tooltips, Meldungen, Postfach, Spiel-Log und die angezeigten Datenamen. **Kennungen, JSON-Schluessel, Dateinamen, Docstrings und Kommentare bleiben ASCII** - und Code-Bezuege in einer Meldung nennen weiter den Code-Namen.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `c87efcd` | `git log --oneline -1` |
| Messung VORHER | **521 Ersatzschreibweisen in 2.264 Anzeigetexten**, 42 Dateien | `tools/anzeigetexte_inventur.py` gegen `git show HEAD:src/...` |
| Messung NACHHER | **0** in 2.263 Anzeigetexten | `docs/ANZEIGETEXTE_INVENTUR.md` |
| Ersetzte Literale | **374** in 42 Dateien (Drittel 1: 90, Drittel 2: 154, `main.py`: 130) | `tools/anzeigetexte_umlaute_setzen.py` |
| Neue Wache | `tests/test_anzeigetexte_umlaute.py` **49/0/0**, Gegenprobe erzeugt eine Fundstelle | eigener Lauf |
| Voller Sammellauf | **152 von 154 gruen, 0 rot, 2 ausgesetzt, 6.047 Pruefungen, 467 s** (Start 18:35) | `docs/audits/sammellauf_t1_final.log` |
| Pruefdateien / Register | **154** / **171** | `ls tests/test_*.py`, `grep -c '^| [0-9]'` |
| Mitgezogene Wachen | zehn: auftraege, lokale_lager, warentransport, spionage (3x), baumenue_standorttipps, speichern_robust, botkern, bottaktik, voelkerwahl, spielschicht, portal_uebersicht, portal_fremdblick, startkartenwahl, dorfuebersicht, kampf_einhaengung, ausbildung_uebersicht, bot_raubzug_bot, originalkarten_baukasse, schild_nebenfenster, spielstand_gui, spielstandarchiv | je Lauf gruen |

**Zwei Werkzeuge statt Massenersetzung:** `tools/anzeigetexte_inventur.py` misst nur, was wirklich in eine Anzeige geht (Klassen A/B/C), `tools/anzeigetexte_umlaute_setzen.py` ersetzt auf der exakten Quellspanne mit Wortkarte und schuetzt Code-Bezuege. Beide teilen sich EINE Messung (Muster F-04).

## Der EINE naechste Schritt

**S-7 Karawanen** (Daniels Reihenfolge): Transporte zwischen den EIGENEN Doerfern ueber `auftraege.starten`, Reisekosten im Startdorf. Mit vier Doerfern je Bot wird der Nachschub noetig - ein Dorf ohne Nachschub hungert. Danach **S-9** (Stil je Taktik), **W-3** (teuer mit Deckel), **S-6b** (Warenkette fuer Bots, damit der Siedlerkarren Pflicht werden kann) und zuletzt die **Story** (W-11).

**Der Sammellauf gehoert zum Abschluss jedes Code-Schnitts** - nach diesem Stand ist er gruen gelaufen (467 s), und das Protokoll traegt die Zeile dazu.

# STAND 03.11.2026, 17:02 - S-6: Bots gruenden nach, vier Doerfer je Bot (Register 170)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Jeder Bot gruendet jetzt eigene Doerfer - bis zu vier, in seiner Heimatwelt, mit eigener Karte.**
Daniels Vorgabe war „Nachgruenden, 3 Gruendungen je Bot = 4 Doerfer“. Gebucht wird mit den Zahlen des
KERNS: `spieloekonomie.gruendungskosten()` liefert Gebuehr, Startpaket und Mindestbestand, die
Forschungsregel (Wagenbau 1) kommt aus `spieloekonomie.REGELN`. Gemessen im echten Startstand: nach
**24 Spieltagen hat jeder der fuenf Bots vier Doerfer** - vorher hatte ein Bot ein bis drei, und ein
Dorf zu gruenden war ueberhaupt nicht moeglich.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `a5f0da5` plus diese Aenderung | `git log --oneline -1` |
| Daten | `data/bot_gruendung.json`: `hoechstens_doerfer` 4, `sperre_stunden` 72, `siedlerkarren_pflicht` false | Datendatei |
| Wache | `tests/test_bot_gruendung.py` **36/0/1** | eigener Lauf |
| Gegenproben | Forschungspruefung aus -> **2 Fehler**; Hoechstzahl aus -> **5 Fehler** (Bots kamen auf 7-10 Doerfer); Datei beide Male hashgleich zurueck | eigener Lauf |
| Messung im Spiel | nach 24 Spieltagen **4 Doerfer je Bot**, alle in der Heimatwelt, 4 verschiedene Karten, 11 Gruendungs-Nachrichten im Postfach | `tests/test_bot_gruendung.py` Abschnitt 4 |
| Voller Sammellauf | **151 von 153 gruen, 0 rot, 2 ausgesetzt, 5.997 Pruefungen, 469 s** (Start 17:04) |
| Neue Vorgabe Daniel (17:15) | **Ingame-Texte mit echten Umlauten** („wählen“ statt „waehlen“); Kennungen und Kommentare bleiben ASCII. Schnitt **T-1** noch offen | `docs/VORGABE_INGAME_TEXTE_20261103.md` | `docs/audits/sammellauf_20261103_1704.log` |
| Pruefdateien / Register | **153** / **170** | `ls tests/test_*.py`, `grep -c '^| [0-9]'` |

**Die eine Abweichung, die Daniels Wort braucht:** der Kern verlangt fuer eine Gruendung einen
**Siedlerkarren**, und den kann ein Bot nicht bauen - seine Doerfer fuehren kein Leder, keine Wolle,
keine Pferde, weil die Bot-Wirtschaft keine Werkstattkette hat (gemessen). Der Schalter
`siedlerkarren_pflicht` steht deshalb auf `false`: Gebuehr und Startpaket werden voll bezahlt, die
fuenf Siedler des Karrens ziehen direkt aus dem Ausgangsdorf um. Sobald Bots eine Warenkette haben
(S-6b), wird der Schalter auf `true` gestellt - dann gilt die strenge Kernregel.

## Der EINE naechste Schritt

**T-1 zuerst: Ingame-Texte mit echten Umlauten** (Daniels Vorgabe 17:15). Erst das praezise
Inventurwerkzeug (`text=`, `insert(`, `_log(`, `messages.append` - nur was wirklich angezeigt wird),
dann Datei fuer Datei ersetzen, zuletzt `main.py`, mit einer Wache gegen die Ersatzschreibweisen. Jede
umgestellte Wache nennt die Entscheidung im Kommentar.

**Danach S-7 Karawanen**: Transporte zwischen den EIGENEN Doerfern (`auftraege.starten`, Reisekosten im
Startdorf). Mit vier Doerfern je Bot wird das noetig: ein Dorf ohne Nachschub hungert, und die
Rohstoffe liegen dort, wo die Karte sie hergibt - nicht dort, wo gebaut wird. Danach **S-9** (Stil je
Taktik), **W-3** (teuer mit Deckel, Daniels Entscheidung), **S-6b** (Warenkette fuer Bots, damit der
Siedlerkarren Pflicht werden kann) und zuletzt die **Story** (W-11).

**Der Sammellauf gehoert zum Abschluss jedes Code-Schnitts** - nach diesem Stand laeuft er.

# STAND 03.11.2026, 15:56 - W-4: Bots rauben auch untereinander (Register 169)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Ein starker Bot kann jetzt ein Dorf eines ANDEREN Bots ausrauben.** Daniels Vorgabe war, dass Bots
mit Einheiten und eigenen Doerfern Raubzuege um Ressourcen machen - „nicht nur gegen den Spieler, auch
gegeneinander“, aber nur in einer Welt, die spielaktiv ist. Der Bot greift dafuer dieselben Stellen an
wie beim Angriff auf den Spieler: `kampf.fuehre_schlacht` kaempft, `kampfbericht.beute_am_ziel` zieht
die Beute beim Zielort ab, `bot_armee_buchen` bucht die Verluste, und das Postfach bekommt einen
Bericht. Das Dorf wechselt nie den Besitzer, Truppen bleiben nie am Zielort - die zwei Regeln gelten
unveraendert.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `1a773bc` plus diese Aenderung | `git log --oneline -1` |
| Daten (alle Zahlen VORSCHLAG) | `data/bot_raubzug.json`: `armee_schwelle` 6, `doerfer_schwelle` 1, `staerke_faktor` 1,5, `nur_eigene_welt` true | Datendatei |
| Wache | `tests/test_bot_raubzug_bot.py` **39/0/0** | eigener Lauf, `docs/audits/raubzug_einzellauf.log` |
| Gegenproben | Weltfilter abgeschaltet -> **2 Fehler**; Beute-Buchung uebersprungen -> **1 Fehler**; Datei beide Male hashgleich zurueck | eigener Lauf |
| Umgestellte Wache | `test_bot_armee_je_dorf` 21/1/1 -> **22/0/1** (sie verlangte genau EINE Verlustbuchung; seit W-4 gibt es zwei Verluststellen) | eigener Lauf |
| Nachbarproben | `test_botkern` **101/0/0**, `test_bot_diebstahl` **46/0/1**, `test_bot_welten` **44/0/1**, `test_bot_ausbildung_je_ort` **20/0/1**, `test_bot_takt_scheiben` **34/0/1**, `test_startspiel` **62/0/1**, `test_durchspiel` **65/0/2**, `test_portal_fremdblick` **18/0/1**, `test_bot_wappen` **26/0/1**, `test_gpt_frischstart` OK (6 Tests) | eigene Laeufe |
| Entscheidungen Daniel (16:08) | W-3 teuer mit Deckel; Weltaufteilung bleibt; Wappen bleiben; Karte 8 px + Name beim Darueberfahren | Nachtrag 16:08 in `docs/VORGABEN_WELTEN_UND_BOTS_20261103.md` |
| Voller Sammellauf | **150 von 152 gruen, 0 rot, 2 ausgesetzt, 5.960 Pruefungen, 415 s** (Start 15:58) | `docs/audits/sammellauf_20261103_1558.log` |
| Pruefdateien / Register | **152** / **169** | `ls tests/test_*.py`, `grep -c '^| [0-9]'` |
| Berichtigung am Vorgaengerblock | Die Uebergabe war **10.557 Byte, SHA256 `35624259…`** (15:44 nachgemessen, hashgleich archviert) - der Block vom 15:25 nennt 10.485 Byte / `c0e5fafd`; die Datei wurde nach dem Schreiben des Blocks noch ergaenzt | `sha256sum`, `stat` |

**Befund, der die naechste Sitzung betrifft:** nach der Voelkerwahl traegt jeder Bot eine eigene
Fraktion und damit eine eigene Heimatwelt (W-5/W-9) - es steht dann genau EIN Bot je Welt. Ein Raubzug
Bot gegen Bot hat damit nur dann ein Ziel, wenn zwei Bots' Doerfer in DERSELBEN Welt stehen: vor der
Voelkerwahl ist das bei Haug und Brynhild (beide menschlich, Welt 4) der Fall, danach erst wieder mit
dem Nebendorf-Umzug (W-2). Der Code kann es, die Weltaufteilung gibt ihm derzeit selten ein Ziel -
das ist eine offene Frage an Daniel, keine Luecke im Schnitt.

## Der EINE naechste Schritt

**S-6 Nachgruenden** (Daniels Reihenfolge): drei Gruendungen je Bot, damit ein Bot vier Doerfer hat -
die Voraussetzung dafuer, dass die Weltkarte je Bot mehrere Doerfer zeigt (W-7) und ein Raubzug
ueberhaupt mehrere Ziele hat. Danach **S-7** (Karawanen zwischen eigenen Doerfern), **S-9** (Stil je
Taktik), zuletzt **W-3** (braucht Daniels Entscheidung: gesperrt oder teuer mit Deckel) und die
**Story** (W-11, nebensaechlich).

**Die Fragen der Runde sind beantwortet (Daniel, 16:08 - Nachtrag in `docs/VORGABEN_WELTEN_UND_BOTS_20261103.md`):**
W-3 wird **teuer mit Deckel** (nicht gesperrt, eigener Schnitt spaeter), die Weltaufteilung **bleibt**
(ein Bot je Welt, W-4 greift nur wo zwei Bots eine Welt teilen), die **Wappen bleiben** in der
Reihenfolge der Fraktionen, und die Karte bleibt bei 8 px - der Burg-Name kommt erst beim
Darueberfahren (kleiner Optik-Schritt, nicht Teil von W-4).

**Der Sammellauf gehoert zum Abschluss jedes Code-Schnitts** - der Lauf zu diesem Stand ist gruen
(Zeile oben) und startete nach dem letzten Code-Eingriff.

# STAND 03.11.2026, 15:25 - S-5 komplett, Sammellauf gruen, Uebergabe geschrieben

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Der Tag ist abgeschlossen und gruen:** 149 von 151 Pruefdateien gruen, 0 rot, 2 ausgesetzt,
5.920 Pruefungen in 332 s. Gebaut sind heute S-13 (Bot-Takt deterministisch, Diebstahl eingeschaltet)
und die fuenf Welten-Schnitte W-1, W-5/W-9, W-8, W-6/W-7 sowie S-5 komplett (S-5b Armee in den
Doerfern, S-5c Essen je Dorf, S-5a Ausbildung ueber die Warteschlange).

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf | `e82ce66` plus diese Doku, Arbeitsbaum leer | `git log --oneline -1` |
| Voller Sammellauf (Endstand) | **149 von 151 gruen, 0 rot, 2 ausgesetzt, 5.920 Pruefungen, 332 s** | `docs/audits/sammellauf_20261103_1516.log` |
| Pruefdateien / Register | **151** / **168** | `ls tests/test_*.py`, `grep -c '^| [0-9]'` |
| Uebergabe | `C:\Users\saras\Desktop\UEBERGABE_NEBELSEETAL_20261103_1525.md` (10.485 Byte, SHA256 `c0e5fafd…`) | Desktop |
| Guthaben | **12,59 / 47,40 USD** (13:43 von Daniel abgelesen) | Protokoll |

## Der EINE naechste Schritt

**W-4: Bots rauben auch untereinander** (Daniels Vorgabe): starke Bots mit Einheiten und eigenen
Doerfern machen Raubzuege - gegen den Spieler UND gegen andere Bots, aber nur in einer Welt, die
spielaktiv ist. Die Voraussetzungen stehen: die Armee liegt in den Doerfern (S-5b), die Ausbildung
laeuft ueber die Warteschlange (S-5a), die Weltzuordnung ist fest (W-5/W-9). Danach S-6
(Nachgruenden), S-7 (Karawanen), S-9 (Stil je Taktik), zuletzt **W-3** (braucht Daniels Entscheidung:
gesperrt oder teuer mit Deckel) und die **Story** (W-11, nebensaechlich).

**Vier offene Fragen** stehen in der Uebergabe, Abschnitt 8 (W-3, ein Volk ohne Bot, Wappen-Zuordnung,
Burg-Groesse auf der Karte).

**Der Sammellauf gehoert zum Abschluss jedes Code-Schnitts** - und die naechste Sitzung faengt mit
`git status` und `date` an, nicht mit dem Bauen.

# STAND 03.11.2026, 17:40 - S-5 komplett: der Bot bildet aus statt zu kaufen (Register 168)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**S-5 ist fertig.** Die Armee steht in den Doerfern (S-5b), jedes Dorf isst fuer seine eigene
Garnison (S-5c), und der Bot **bildet jetzt aus** statt zu kaufen (S-5a): er geht denselben Weg wie
der Spieler - Forschung, Ausbildungsstaette vor Ort, Siedler, Ausruestung, Kosten aus dem Dorflager -
und die Einheit entsteht nach der Ausbildungszeit in genau dem Dorf, das sie ausgebildet hat.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `fa66231` plus diese Aenderung | `git log --oneline -1` |
| Neue Wache | `tests/test_bot_ausbildung_je_ort.py` **20/0/1** | eigener Lauf |
| Gegenprobe | Auftrag nicht ins Dorf geschrieben -> **1 Fehler**, Datei hashgleich zurueckgesetzt | eigener Lauf |
| Umgestellte Wachen | `test_bot_dorf_wirtschaft` **54/0/0**, `test_bot_nahrung` **48/0/0**, `test_bot_armee_je_dorf` **22/0/1** | eigene Laeufe |
| Nachbarproben | `test_botkern` **101/0/0**, `test_oekonomie_uhr` **65/0/0**, `test_werkstatt` **118/0/1**, `test_durchspiel` **65/0/2** | eigene Laeufe |

## Der EINE naechste Schritt

**W-4: Bots rauben auch untereinander.** Heute waehlt `bot_angriffsplanung.waehle_ziel` Ziele nur
unter den Siedlungen des Spielers; Daniel will, dass starke Bots mit Einheiten und eigenen Doerfern
Raubzuege machen - gegen den Spieler UND gegen andere Bots, aber nur in einer Welt, die spielaktiv
ist. Danach **S-6** (Nachgruenden), **S-7** (Karawanen), **S-9** (Stil je Taktik), zuletzt **W-3**
(braucht Daniels Entscheidung: gesperrt oder teuer mit Deckel) und die **Story** (W-11).

**Der Sammellauf gehoert zum Abschluss jedes Code-Schnitts** - nach diesem Stand laeuft er.

# STAND 03.11.2026, 16:45 - S-5b/S-5c: die Armee steht in den Doerfern (Register 167)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Die Armee eines Bots haengt nicht mehr am Bot, sondern in seinen Doerfern — und jedes Dorf isst
fuer seine eigene Garnison.** Das ist die Voraussetzung fuer S-5a (Ausbildung je Ort): ohne diesen
Schritt haette eine Ausbildung im Dorf das Essen doppelt gezaehlt.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `f7e1d16` plus diese Aenderung | `git log --oneline -1` |
| Wache | `tests/test_bot_armee_je_dorf.py` **21/0/1** | eigener Lauf |
| Gegenprobe | Eigenschaft liefert `{}` -> **4 Fehler**, Datei hashgleich zurueckgesetzt | eigener Lauf |
| Umgestellte Wachen | `test_bot_nahrung` **47/0/0**, `test_bot_bedarf` **25/0/1**, `test_bot_diebstahl` **46/0/1**, drei GPT-Wachen OK | eigene Laeufe |
| Nachbardateien | `test_botkern` **101/0/0**, `test_s7_botverhalten` **46/0/0**, `test_bot_dorf_wirtschaft` **54/0/0**, `test_durchspiel` **65/0/2** | eigene Laeufe |

## Der EINE naechste Schritt

**S-5a: Ausbildung je Ort ueber die Warteschlange statt Kauf.** Der Kern hat sie schon
(`spieloekonomie.ausbildung_start`, `ausbildung_grenzen`, `Settlement.ausbildung` je Ort, und
`bot_dorf_als_ort` reicht sie durch) - der Bot umgeht sie nur. Jetzt darf er sie benutzen: die
Einheit entsteht im Dorf mit dem Einheiten-Gebaeude und steht danach im selben Dorf (S-5b ist dafuer
gebaut), gegessen wird dort (S-5c). Danach **W-4** (Bots rauben untereinander), **S-6/S-7/S-9**,
zuletzt **W-3** (braucht Daniels Entscheidung) und die **Story** (W-11, nebensaechlich).

**Der Sammellauf gehoert zum Abschluss jedes Code-Schnitts** - nach diesem Stand laeuft er.

# STAND 03.11.2026, 15:40 - W-6/W-7: Blick in fremde Welten, Doerfer je Welt (Register 166)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Der Spieler kann jetzt in fremde Welten SCHAUEN, ohne zu springen.** Ueber der Karte steht
'Ansehen:' mit der eigenen Welt und den Nummern der fuenf anderen; ein Klick zeigt deren Karte mit den
Burgen der dortigen Bots, die Kopfzeile sagt 'NUR ANSICHT', und unter der Karte steht, wie viele
Doerfer jeder Bot in dieser Welt hat. Angriff oder Spionage oeffnen sich dort NICHT - ein Auftrag
ueber die Weltgrenze ist bis zur Entscheidung W-3 gesperrt.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `c77f8dd` plus diese Aenderung | `git log --oneline -1` |
| Wache | `tests/test_portal_fremdblick.py` **18/0/1** | eigener Lauf |
| Gegenprobe | 'Ansehen' als echter Sprung -> **3 Fehler**, Datei hashgleich zurueckgesetzt | eigener Lauf |
| Nebenbefund behoben | Gruendungen standen in Welt 1 statt in der Welt des Spielers - beide Gruendungswege setzen sie jetzt, Laden repariert unmoegliche Welten | `src/main.py` |
| Nachbardateien | `test_startspiel` **62/0/1**, `test_weltbild_gelaende` **135/0/0**, `test_spionage` **146/0/0**, `test_durchspiel` **65/0/2** | eigene Laeufe |
| Story-Regel (W-11) | aus der Nebelseetal-Geschichte nur das Noetige, den sechs Fraktionen angepasst, Story nebensaechlich - eingeordnet ans ENDE der Liste | `docs/VORGABEN_WELTEN_UND_BOTS_20261103.md` |

## Der EINE naechste Schritt

**S-5 Ausbildung je Ort** (Daniels Reihenfolge von 12:20): Warteschlange statt Kauf. Reihenfolge im
Schnitt, vom Code selbst verlangt: **erst die Armee nach `dorf.einheiten` (S-5b)**, dann ausbilden
(S-5a), dann Essen je Dorf (S-5c) - sonst isst die Armee doppelt. Danach **W-4** (Bots rauben
untereinander), **S-6/S-7/S-9**, zuletzt **W-3** (braucht Daniels Entscheidung) und die **Story**.

**Der Sammellauf gehoert zum Abschluss jedes Code-Schnitts** - nach diesem Stand laeuft er.

# STAND 03.11.2026, 15:10 - W-8: Burgen und Wappen auf der Weltkarte (Register 165)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Jedes Dorf auf der Weltkarte ist jetzt zuzuordnen.** Statt des braunen Kastens mit X traegt jedes
Dorf die **Burg seiner Fraktion** und darunter ein kleines **Wappen-Abzeichen** - Hauptdorf und
Nebendoerfer desselben Bots dasselbe Paar, der Spieler sein eigenes. Die Bilder sind Daniels
Lieferung vom 01.11., die Zuordnung steht in einer Datendatei.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `88ca781` plus diese Aenderung | `git log --oneline -1` |
| Neue Regeldaten | `data/bot_wappen.json` - je Fraktion Burg + Wappen, zwei Groessen-Regler, Urteil VORSCHLAG | Datei |
| Wache | `tests/test_bot_wappen.py` **26/0/1** | eigener Lauf |
| Gegenprobe | Zeichnen abgeschaltet -> **1 Fehler** (0 von 4 Bildern), Datei hashgleich | eigener Lauf |
| Nachbardateien | `test_startspiel` **62/0/1**, `test_weltbild_gelaende` **135/0/0**, `test_spionage` **146/0/0**, `test_durchspiel` **65/0/2** | eigene Laeufe |
| Belegbilder | `docs/audits/wappen_uebersicht_20261103.png`, `portal_wappen_heimat_20261103.png`, `portal_wappen_fremdwelt_20261103.png` | eigene Aufnahmen |

## Der EINE naechste Schritt

**W-6/W-7: der Blick in fremde Welten.** Seit W-5/W-9 stehen die fuenf Bots in ihren Fuenf-Welten -
die Heimatkarte des Spielers zeigt damit nur noch seine eigenen Doerfer. Der Ueberblick ueber die
anderen Welten („der spieler ... sieht bereits die bots wenn er in die Uebersicht einer anderen welt
schaut“) und die Anzeige, wie viele Doerfer ein Bot in seiner Welt hat, fehlen noch. Danach **S-5
Ausbildung je Ort** (S-5b Armee ins Dorf zuerst), **W-4** (Bots rauben untereinander), **S-6/S-7/S-9**;
**W-3** braucht Daniels Entscheidung (gesperrt oder teuer mit Deckel).

**Der Sammellauf gehoert zum Abschluss jedes Code-Schnitts** - nach diesem Stand laeuft er.

# STAND 03.11.2026, 14:40 - W-5/W-9: fuenf Bots, Heimatwelt je Fraktion (Register 164)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Jeder Nutzer hat jetzt eine Herkunftswelt, und der Spieler startet in der Welt seines Volkes.**
Vorher wuerfelte die Zahl der Bots (1 bis 5) und die Startwelt war fuer jeden die feste Datenwelt
`d04`. Jetzt: fuenf Bots fest, je Fraktion genau eine Heimatwelt, Wahl des Volkes setzt die
Startwelt — ohne Midgard-Zwang im Code.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `331edd5` plus diese Aenderung | `git log --oneline -1` |
| Neue Regeldaten | `data/welt_fraktionen.json` (Fraktion -> Welt, VORSCHLAG mit Begruendung, NICHT BELEGT) | Datei |
| Wache | `tests/test_bot_welten.py` **44/0/1** | eigener Lauf |
| Gegenproben | Spielerwelt-Zeile entfernt -> **5 Fehler**; Bot-Zahl wieder gewuerfelt -> **1 Fehler**; Datei beide Male hashgleich | eigene Laeufe |
| Nachbardateien | `test_startspiel` **62/0/1**, `test_voelkerwahl` **37/0/0**, `test_botkern` **101/0/0**, `test_durchspiel` **65/0/2** | eigene Laeufe |
| Guthaben (13:43) | **12,59 / 47,40 USD**, seit 12:24 **0,21 USD** | Protokoll |

## Der EINE naechste Schritt

**W-8: Burgen und Wappen auf die Weltkarte.** Die sechs Burgen (`assets/icons/burgen/burg_01..06.png`)
und zehn Wappen (`assets/icons/wappen/wappen_01..10.png`) liegen fertig und freigestellt; heute zeichnet
die Karte einen braunen Kasten mit X, ohne Name, ohne Nummer. Danach **W-6/W-7** (Nur-Lese-Blick in
fremde Welten, Doerfer je Welt zaehlen), dann **S-5 Ausbildung je Ort** (S-5b Armee ins Dorf zuerst,
sonst isst sie doppelt), dann **W-4** (Bots rauben untereinander), dann S-6/S-7/S-9. **W-3** (Kampf
ueber Weltgrenzen) braucht Daniels Entscheidung: gesperrt oder teuer mit Deckel.

**Der Sammellauf gehoert zum Abschluss jedes Code-Schnitts** - nach diesem Stand laeuft er.

# STAND 03.11.2026, 13:52 - W-1: jedes Bot-Dorf steht nur auf seiner Weltkarte (Register 163)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Die Bots liegen jetzt in der Welt, in der sie entstanden sind — und die Karte luegt nicht mehr.**
Vorher stand jedes Bot-Dorf auf der nackten Vorgabe `dimension = 1` (Armageddon), waehrend die Heimat
des Spielers **Midgard (4)** ist; die Anzeige prueft die Welt gar nicht und zeigte fremde Doerfer auf
jeder Karte. Jetzt traegt jedes Dorf seine **Herkunftswelt**, entsteht in der Startwelt, und die Karte
zeigt nur, was auf ihr steht.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `3e9982c` plus diese Aenderung | `git log --oneline -1` |
| Neue Wache | `tests/test_bot_welten.py` **19/0/1** | eigener Lauf |
| Gegenprobe | Filterzweig abgeschaltet -> **4 Fehler**, Datei hashgleich zurueckgesetzt | eigener Lauf |
| Nachbardateien | `test_startspiel` **62/0/1**, `test_weltbild_gelaende` **135/0/0**, `test_spionage` **146/0/0**, `test_durchspiel` **65/0/2**, `test_bot_diebstahl` **46/0/1** - alle unveraendert gruen | eigene Laeufe |
| Guthaben (13:43, von Daniel abgelesen) | **12,59 / 47,40 USD** - seit 12:24 **0,21 USD** Verbrauch | `docs/ENTWICKLUNGSPROTOKOLL.md` |
| Offen aus Daniels Vorgaben | **W-2** Umzug eines Nebendorfs, **W-3** Preis/Sperre ueber Weltgrenzen (braucht Daniels Wort), **W-4** Bot gegen Bot | `docs/VORGABEN_WELTEN_UND_BOTS_20261103.md` |

## Der EINE naechste Schritt

**S-5 Ausbildung je Ort** (Daniels Reihenfolge von 12:20): Warteschlange statt Kauf
(`spieloekonomie.ausbildung_start`, die der Kern schon hat und der Bot umgeht). **Reihenfolge im
Schnitt ist gemessen, nicht geraten:** erst die Armee nach `dorf.einheiten` (S-5b), dann ausbilden
(S-5a) — der Docstring von `bot_dorf_tick` sagt es selbst: 'sobald S-5 Einheiten je Ort ausbildet,
muss die Armee dort hineinwandern (sonst isst sie zweimal)'. Danach S-6 Nachgruenden, S-7 Karawanen,
S-9 Stil je Taktik. **Der Sammellauf gehoert zum Abschluss jedes Code-Schnitts**, das Protokoll
traegt die Kennung.

# STAND 03.11.2026, 12:43 - S-13: der Bot-Takt haengt an festen Spielzeit-Punkten (Register 162)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Die Zeit ist jetzt eine Wahrheit — auch fuer die Bots.** Der Bot-Takt feuert nicht mehr, wenn die
Fliesskomma-Differenz reicht, sondern an FESTEN Spielstunden-Punkten: die Orte werden bis zum Punkt
gebucht, dann handelt der Bot auf genau diesem Stand. `1 x 3600 s` und `10 x 360 s` fahren dieselben
Zuege. Damit ist der Diebstahl (S-12) eingeschaltet - er war bis heute nur gebaut.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `55cd905` plus diese Aenderung | `git log --oneline -1` |
| Neue Wache | `tests/test_bot_takt_scheiben.py` **34/0/1** | eigener Lauf |
| Diebstahl-Wache | `tests/test_bot_diebstahl.py` **46/0/1** (Datei jetzt AKTIV, samt Goetterschutz) | eigener Lauf |
| Demo-Regel | `tests/test_s7_botverhalten.py` **46/0/0** | eigener Lauf |
| Gegenprobe | alte Bedingung zurueckgetauscht -> **5 Fehler**, Datei hashgleich zurueckgesetzt | eigener Lauf |
| Umgestellte Wachen | `test_gpt_fixrunde_ortslager_zeit_20261028`, `test_gpt_frischstart`, `test_gpt_bot_angriffsplanung`, `test_gpt_wall_bot_kampf` je OK (Diebstahl im `setUp` aus, Begruendung im Test) | eigene Laeufe |
| Voller Sammellauf 12:54 (ENDSTAND) | **144 von 146 gruen, 0 rot, 2 ausgesetzt, 5.786 Pruefungen, 314 s** | `docs/audits/sammellauf_20261103_1254.log` |
| Verworfen: Lauf 12:45 | **142 von 146, 2 rot** - beide rot aus EINEM Grund (der Diebstahl umging den Goetterschutz), behoben und in 12:54 gruen; nicht als roter Stand lesen | `docs/audits/sammellauf_20261103_1245.log` |
| Neue Vorgaben Daniels | `docs/VORGABEN_WELTEN_UND_BOTS_20261103.md` (Hauptdorf bleibt in seiner Welt, nur Nebendoerfer wechseln, Kampf ueber Weltgrenzen unbezahlbar, Bots rauben auch untereinander) | Chat 12:35 bis 12:40 |

## Der EINE naechste Schritt

**S-5 Ausbildung je Ort** (Daniels Reihenfolge von 12:20): Warteschlange statt Kauf
(`spielschicht.ausbilden`); damit zieht die Armee in die Doerfer und isst dort (`bot_futter_buchen`
isst heute nur im Hauptdorf, `dorf.einheiten` ist leer). Danach S-6 Nachgruenden, S-7 Karawanen, S-9
Stil je Taktik. **Der Sammellauf gehoert zum Abschluss jedes Code-Schnitts** - und das Protokoll
traegt die Kennung.

**Befunde, die dabei nicht untergehen duerfen** (gemessen 12:41, Belege in der Vorgaben-Datei):
`_bot_doerfer_im_raster` filtert NICHT nach Welt, und die sechs gelieferten Burgen
(`assets/icons/burgen/`) sind nicht auf der Karte - dort steht ein brauner Kasten mit X.

# STAND 03.11.2026, 12:25 - Sitzungsende: vier Entscheidungen, naechster Schnitt ist das Zeitmodell

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Der Stand ist gruen und die Richtung entschieden.** Voller Sammellauf 143 von 145 (0 rot), alle
Arbeit committet, kein Prozess offen. Die vier offenen Fragen hat Daniel beantwortet; sie gelten ab
jetzt und sind hier woertlich festgehalten.

| Nr | Frage | Antwort Daniel (woertlich) | Folge |
|---|---|---|---|
| 1 | Altname `deepseek-v4-flash` in der Config | "Ja, umstellen (Altname raus, ueberall derselbe Name)" | `auxiliary.mcp.model` = `deepseek-flash`, ueber die CLI gesetzt, Sicherung + Protokoll |
| 2 | Diebstahl-Zahlen (dünn ≤ 5, 3 %, 60/120, 12 h) | "So lassen (Schwelle 5, 3 %, 60/120, 12 h)" | `data/bot_diebstahl.json` bleibt wie es ist |
| 3 | Wie wird der Bot-Takt zeitlich deterministisch? | "Ereignis-Splitting wie beim Spieler (`spieloekonomie.tick_bis`) - groesserer Umbau, aber eine Wahrheit" | **naechster Schnitt:** Bot-Takt ueber `tick_bis` statt eigener Bucket-Logik |
| 4 | Naechster fachlicher Schnitt danach | "S-5 Ausbildung je Ort (Warteschlange statt Kauf; Armee zieht in die Doerfer und isst dort)" | nach dem Zeitmodell: S-5, dann S-6, S-7 |

## Der EINE naechste Schritt

**Bot-Takt auf `spieloekonomie.tick_bis` umstellen** (Daniels Entscheidung 3 von heute): die
Bot-Aktionen laufen dann durch DIESELBE Ereignis-Zerlegung wie die Spielersiedlungen, und
`1 × 3600 s` gegen `10 × 360 s` fuehrt zu denselben Takten. Erst danach kann `data/bot_diebstahl.json`
auf `aktiv: true` (S-12 steht fertig, Register 161) - und danach S-5 Ausbildung je Ort.

**Was dafuer zu beachten ist:** `tick_bis` arbeitet auf `orte` (dict) und `missionen` und liefert
`(orte, missionen, wissen, zeit, ereignisse)`; der Bot-Takt heute arbeitet auf `BotPlayer`-Objekten und
`self.settlements`. Die Umstellung braucht deshalb eine Uebersetzung in BEIDE Richtungen
(`bot_dorf_als_ort` / `bot_dorf_aus_ort` gibt es schon) und eine Wache, die genau die Gleichheit
`1 x 3600 == 10 x 360` fuer die Bot-Aktionen prueft - heute ist sie fuer den Spieler geprueft, nicht
fuer die Bots.

# STAND 03.11.2026, 11:45 - S-12: Diebstahl mit Bericht GEBAUT, Schalter bleibt AUS (Register 161)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Die Mechanik steht, die Zeit stimmt noch nicht.** Daniels Entscheidung 7 ("Ja, aber nur mit Bericht
im Postfach") ist gebaut: duenne Bots bestehlen wehrlose Orte, jeder Fall wird als Nachricht mit wer,
wann, was, wieviel ins Postfach gelegt. **Eingeschaltet ist sie nicht** - und der Grund ist gemessen,
nicht geraten.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `9865f73` plus diese Doku | `git log --oneline -1` |
| Voller Sammellauf | **143 von 145 gruen, 0 rot, 2 ausgesetzt, 5.742 Pruefungen, 429 s** (Start 11:43, nach dem letzten Fix) | `docs/audits/sammellauf_20261103_1143.log` |
| Pruefdateien / Register / Quelldateien | **145** / **161** / **55** | `ls tests/test_*.py`, `grep -c '^| [0-9]'`, `ls src/*.py` |
| Neue Wache | `tests/test_bot_diebstahl.py` **36/0/1** | eigener Lauf |
| Mechanik, gemessen | je Rohstoff 3 Prozent (1000/500/200 -> **30/15/6**), Deckel 60 je Rohstoff und 120 gesamt halten, Ziel nie unter 0, Bot-Hauptdorf bekommt genau die Mengen | `test_bot_diebstahl.py` |
| Bedingungen, gemessen | Garnison im Ziel -> **kein** Diebstahl; starker Bot (>5 Einheiten) -> **kein** Diebstahl; Sperre 12 h haelt, danach wieder; leerer Ort und Deckel 0 -> nichts | `test_bot_diebstahl.py` |
| Warum aus | Bot-Takt feuert je nach Tick-Zuschnitt einmal oder keinmal: **1 x 3600 s und 10 x 360 s** fuhren unterschiedlich viele Bot-Aktionen, sobald der Diebstahl das Spielerlager beruehrt (`test_gpt_fixrunde_ortslager_zeit` 98,79 gegen 105,0) | `data/bot_diebstahl.json`, Feld `warum_noch_aus` |

**Zwei Reparaturversuche, beide zurueckgenommen** (Reichsanzeige nachziehen; Takt nach ganzen
Abschnitten feuern): sie aenderten Verhalten, ohne das Problem zu loesen. Der saubere Weg ist ein
eigenes, scheiben-unabhaengiges Zeitmodell fuer Bot-Aktionen - **das ist die offene Entscheidung.**

## Der EINE naechste Schritt

**Bot-Takt auf feste Spielzeit-Punkte stellen** (statt "wenn die Fliesskomma-Differenz reicht"): jeder
Takt hat einen festen Abschnitt, 1 x 3600 s und 10 x 360 s fahren dieselben Takte. Erst damit sind
Bot-Aktionen scheiben-unabhaengig - und der Diebstahl kann eingeschaltet werden. Danach: **S-5
Ausbildung je Ort**, **S-6 Nachgruenden**, **S-7 Karawanen**.

# STAND 03.11.2026, 11:10 - S-11: der Journal-Deckel haelt (500 Zeilen je Ort, Register 160)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Das `produktionsjournal` waechst nicht mehr ins Unendliche.** Daniels Entscheidung 9: 500 Zeilen je
Ort, aelteste fallen weg - fuer Spieler UND Bots, denn beide schreiben durch dieselbe Stelle. Gedeckelt
wird an Ort und Stelle, damit das Versorgungsfenster und der Spionagebericht unveraendert weiterlesen.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `6aabe37` plus diese Doku | `git log --oneline -1` |
| Voller Sammellauf | **142 von 144 gruen, 0 rot, 2 ausgesetzt, 5.700 Pruefungen, 389 s** (Start 11:02, nach dem letzten Fix) | `docs/audits/sammellauf_20261103_1102.log` |
| Pruefdateien / Register / Quelldateien | **144** / **160** / **55** | `ls tests/test_*.py`, `grep -c '^| [0-9]'`, `ls src/*.py` |
| Neue Wache | `tests/test_journal_deckel.py` **23/0/1** | eigener Lauf |
| Deckel, gemessen | 600 Zeilen -> **500** (neueste bleibt, aelteste 100 weg); 520 Stunden-Spannen durch `ort_tick` -> genau **500**, erste Zeile ab 72.000 s; unter dem Deckel aendert sich nichts | `test_journal_deckel.py` |
| Versorgungsfenster danach | **24 von 24** Stundenzeilen vorhanden, dieselben Zahlen (Holz 327,6 / Stein 296,4 / Nahrung 288,0 / Gold 216,0) | `test_journal_deckel.py` |
| Bot-Weg (`ertrag_weg = karte`) | 520 Spannen -> **500** Zeilen, letzte Zeile traegt ihren `verbrauch` | `test_journal_deckel.py` |

**Ehrliche Grenzen:** (a) gedeckelt wird nur das Journal - Vorraete und alle anderen Buecher bleiben
unberuehrt; (b) ein Deckel KLEINER als das Versorgungsfenster wuerde dem Fenster Zeilen nehmen (bei 500
nicht der Fall: 500 Zeilen = rund 20 Spieltage bei stündlichem Takt); (c) alte Spielstaende mit mehr als
500 Zeilen werden erst beim naechsten Tick gekuerzt, nicht beim Laden.

## Der EINE naechste Schritt

**Diebstahl mit Postfach-Bericht** (Daniels Entscheidung 7): duenne Bots duerfen den abwesenden Spieler
bestehlen, **jeder Fall als Nachricht ins Postfach** (wer, wann, was, wieviel) - kein stiller Verlust.
Eigener Schnitt nach S-6 im Konzept. Danach: **S-5 Ausbildung je Ort** (Warteschlange statt Kauf - damit
zieht die Armee in die Doerfer und isst dort), **S-6 Nachgruenden** (3 je Bot), **S-7 Karawanen**.

# STAND 03.11.2026, 10:26 - S-10: der BEDARF je Rohstoff, die Kartenwahl steht auf "mittel" (Register 159)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Die Bots waehlen ihre Karten jetzt nach ihrem BEDARF.** Daniels Entscheidung 4 verlangte genau das:
erst einen Bedarf je Rohstoff bauen, dann `kartenwahl_stufe` von `schwer` auf `mittel` stellen. Bis
heute kannte das Spiel nur EINEN laufenden Verbrauch - Nahrung der Garnison (8 je Einheit und Tag);
alles andere wird sofort bezahlt. Jetzt rechnet `bot_rohstoffbedarf` den Bedarf je STUNDE (dieselbe
Einheit wie die Ertraege der Karten) aus dem, was das Spiel schon fuehrt.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `0e48fce` plus diese Doku | `git log --oneline -1` |
| Voller Sammellauf | **141 von 143 gruen, 0 rot, 2 ausgesetzt, 5.677 Pruefungen, 392 s** (Start 10:18, nach dem letzten Fix) | `docs/audits/sammellauf_20261103_1018.log` |
| Pruefdateien / Register / Quelldateien | **143** / **159** / **55** | `ls tests/test_*.py`, `grep -c '^| [0-9]'`, `ls src/*.py` |
| Neue Wache | `tests/test_bot_bedarf.py` **25/0/1** | eigener Lauf |
| Umgestellte Wachen | `test_kartenwahl_bot` **22/0/0** (Nutzen-Zweig jetzt explizit `stufe="schwer"`, neuer Abschnitt 6 fuer "mittel"), `test_bot_dorf_als_ort` **32/0/0** (Karte fuer die Zaehlung fest gesetzt) | eigene Laeufe |
| Bedarf, gemessen | 10 Einheiten = 80 Nahrung/Tag = **3,3333/h**; offener Gauner-Auftrag = **10,4167 Gold/h** + 0,0417 Siedler/h; Baukunst Stufe 1 = **2,0833 Holz/h**, Stufe 2 = 4,1667; zwei Dolche = 0,1667 Metall/h | `test_bot_bedarf.py` |
| Wirkung auf die Karte | **3 von 5 Bots** bekommen mit "mittel" eine andere Karte als mit der reinen Gold-Regel; die Mangel-Achse entscheidet (Probe: `original-108`) | `test_kartenwahl_bot.py` |

**Ehrliche Grenzen:** (a) der Bedarf ist eine **Planungsgroesse** (was das Dorf in 24 h bezahlen will),
keine Verbrauchsmessung - verbrauchte Mengen stehen weiter im `produktionsjournal`; (b) **Bauten zaehlen
nicht** mit (einmalige Ausgabe, eigene Entscheidung noetig); (c) die Aenderung wirkt nur auf die
**Kartenwahl**, nicht auf die Wirtschaft; (d) das Fenster (24 h) ist eine VORSCHLAG-Zahl in
`data/bot_bedarf.json` - das Original nennt keinen Planungshorizont.

## Der EINE naechste Schritt

**Journal-Deckel: `produktionsjournal` auf 500 Zeilen je Ort** (Daniels Entscheidung 9), Spieler UND
Bots gleich, aelteste Zeilen fallen weg, mit Wache: der Deckel greift und das Versorgungsfenster rechnet
weiter. Danach in dieser Reihenfolge: **Diebstahl mit Postfach-Bericht** (Entscheidung 7), **S-5
Ausbildung je Ort** (Warteschlange statt Kauf - damit zieht die Armee in die Doerfer und isst dort),
**S-6 Nachgruenden**, **S-7 Karawanen**.

# STAND 03.11.2026, 08:46 - S-4: die Bots FORSCHEN, ihre Taktiken trennen sich (Register 158)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Aus "gebaut bleibt 0" und "geforscht bleibt 0" sind echte Staende geworden.** Ein Bot-Dorf forscht
jetzt mit SEINEN Rohstoffen, durch DIESELBE Funktion wie der Spieler (`spieloekonomie.forschung_start`):
Voraussetzungskette geprueft, Preis aus dem Dorflager gebucht, Dauer aus den Spieldaten, Abschluss
genau einmal. Die Reihenfolge kommt aus dem Stil der Taktik (`data/bot_forschung.json`, Daniels
Entscheidung 2). Erst damit wird `nach_baukunst` nutzbar - Wall, Lager, Schmiede, Akademie und
Diebesgilde stehen jetzt hinter Baukunst, nicht hinter einem Verbot.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `35df468` plus diese Doku | `git log --oneline -1` |
| Voller Sammellauf | **140 von 142 gruen, 0 rot, 2 ausgesetzt, 5.653 Pruefungen, 385 s** (Start 08:38, auf dem CODE-Stand von S-4) | `docs/audits/sammellauf_20261103_0838.log` |
| Pruefdateien / Register / Quelldateien | **142** / **158** / **55** | `ls tests/test_*.py`, `grep -c '^| [0-9]'`, `ls src/*.py` |
| Neue Wache | `tests/test_bot_forschung.py` **57/0/1** | eigener Lauf |
| Umgestellte Wachen | `test_bot_bauen` **35/0/2** (S-4-Befund aufgeloest), `test_bot_takt_kern` **26/0/1** (prueft den Kern-Aufruf mit Wissensstand) | eigene Laeufe |
| Wirkung, gemessen | 120 Bot-Takte x 5 Bots (30 Spielstunden) in **2,43 s**; danach: Pluenderer Baukunst 1 / Heimlichkeit 1 / Wagenbau 1 / Felderwirtschaft 3 / Kriegskunst 2 (Lager, Schmiede, Akademie), Waechterin Baukunst 3 / Verteidigungsanlagen 3 (Wall, Bogenbauer), Bastionier Baukunst 3 / Felderwirtschaft 3 / Verteidigungsanlagen 1 (Wall, Schmiede), Spaeherin Heimlichkeit 3 (Diebesgilde, Bogenbauer), Raecher Kriegskunst 3 (Schmiede, Akademie) | Dauerspiel-Probe |
| Kosten/Dauer belegt | Stufe 1 = **50 Holz**, je Stufe das Doppelte; Dauer = Stufe zum Quadrat in Stunden; gemessen: Baukunst Stufe 1 kostet genau 50 Holz aus dem Dorflager | `spieldaten.forschungs_kosten`, `test_bot_forschung.py` |

**Ehrliche Grenzen:** (a) die Bibliothek eines Bots bleibt auf **Stufe 1** - Ausbauen ist noch nicht
gebaut, deshalb sind alle Forschungen mit "Bibliothek 2/3/5/6" gesperrt und stehen als
`nach_bibliothek` in der Datendatei; (b) die Forschung wirkt nur ueber den **Kern-Weg** des Takts
(`bot_dorf_tick` bekommt jetzt den Wissensstand) - auf dem Vorgabe-Weg `ertrag_weg = karte` rechnet
der Bot weiter mit dem Kartenprofil, dort aendert Forschung den Ertrag **nicht**; (c) die Reihenfolge
je Taktik ist eine begruendete Setzung dieser Sitzung, keine Originalregel; (d) **Ausbilden** (S-5)
fehlt weiter - die Bots haben jetzt Akademie und Gilde, aber noch keine Warteschlange.

## Der EINE naechste Schritt

**Bedarf je Rohstoff** (Daniels Entscheidung 4): den Verbrauch je Rohstoff fuehren und messen. Erst
damit darf `kartenwahl_stufe` auf `mittel` gestellt werden - heute faellt `mittel` auf die Gold-Regel
zurueck, weil das Spiel keinen Bedarfsbegriff kennt. Danach in dieser Reihenfolge: **Journal-Deckel**
500 Zeilen je Ort (Entscheidung 9), **Diebstahl mit Postfach-Bericht** (Entscheidung 7), **S-5
Ausbildung je Ort** - und damit die Voraussetzung dafuer, dass die Bot-Armee aus den Doerfern statt
aus der Kasse kommt.

# STAND 03.11.2026, 04:08 - S-3: die Bots BAUEN, ihre Siedler stehen an einem Ort (Register 156)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Aus "gebaut bleibt immer 0" sind echte Gebaeude geworden.** Ein Bot-Dorf baut jetzt durch
DIESELBE Funktion wie der Spieler (`spielschicht.bauen`): freies Feld, Gelaende-Eignung, Preis aus
`data/baupreise.json`, Abbuchung aus seinem eigenen Dorflager. Die Reihenfolge kommt aus dem Stil
der Taktik (`data/bot_bauplan.json`). Dazu ein Befund, der beim Bauen sofort biss: ein Bot fuehrte
Siedler an ZWEI Stellen (Rohstoff im Lager und Bevoelkerung) - jetzt nur noch in `bevoelkerung`,
und die Armee bezahlt ihre Siedler von dort.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `056e693` plus diese Aenderung (Commit folgt) | `git log --oneline -1` |
| Voller Sammellauf | **139 von 141 gruen, 0 rot, 2 ausgesetzt, 5.592 Pruefungen, 281 s** (Start 04:03, auf dem CODE-Stand dieser Aenderung) | `docs/audits/sammellauf_20261103_0403.log` |
| Pruefdateien / Register / Quelldateien | **141** / **156** / **55** | `ls tests/test_*.py`, `grep -c '^| [0-9]'`, `ls src/*.py` |
| Neue Wache | `tests/test_bot_bauen.py` **32/0/2** | eigener Lauf |
| Wirkung, gemessen | 48 Bot-Takte in **1,65 s**; jeder der fuenf Bots **15 Gebaeude** (12 Grundanlagen + 2 Haeuser + 1 Bibliothek), `dorf.gebaut` = 3, Bevoelkerung **20** (10 + 2 x 5 aus den Haeusern), Armee 4-8 aus dem Siedlerzuwachs; ein Haus kostet genau **80 Holz / 50 Stein** | `test_bot_bauen.py`, Dauerspiel-Probe |

**Ehrliche Grenzen:** (a) `nach_baukunst` (Wall, Lager, Schmiede, Akademie, Diebesgilde, Bogenbauer)
wird NICHT gebaut - die belegte Regel `regeln.ohne_forschung_baubar` nennt nur Holzaeller,
Steinmetze, Jaeger, Bibliothek und Haeuser, und Bots forschen noch nicht (S-4); (b) das **Lager**
traegt in `data/buildings.json` "keine belegt", steht aber nicht in dieser Regel - der Plan laesst
es vorsichtshalber hinter Baukunst, statt eine belegte Regel zu umgehen; (c) **Ausbauen** (Stufen)
ist noch nicht gebaut, nur Bauen; (d) die fuenf Stile unterscheiden sich beim Bauen heute nicht,
weil ihnen die Forschungsregel dieselben zwei Gebaeude laesst - das aendert S-4.

## Der EINE naechste Schritt

**S-4: die Bots FORSCHEN** - mit eigenen Rohstoffen, derselben Voraussetzungskette und derselben
Dauer wie der Spieler (`spielschicht.forschung_starten`, `forschung`-Modul, `forschungsauftrag` je
Ort). Erst damit wird `nach_baukunst` nutzbar, unterscheiden sich die Taktiken wirklich, und der
Kern-Tick bekommt seine Forschungsboni (heute geht dort ein leeres dict hinein).

Danach: **S-5** Ausbildung (Warteschlange je Ort, ersetzt den Kauf), **S-6** Nachgruenden (3 je Bot),
**S-7** Karawanen, **S-8** Reisekosten, **S-9** Stil je Taktik. **Fuer Daniel liegt genau eine
Entscheidung bereit:** `ertrag_weg` in `data/bot_wirtschaft.json` - `"karte"` (Vorgabe, B-4) oder
`"felder"` (Kern wie beim Spieler, Karte bestimmt dann nur die Bauplaetze).

# STAND 03.11.2026, 03:56 - S-2b: der Bot-Takt KANN auf dem Kern laufen - Vorgabe bleibt die Karte (Register 155)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Zwei Wirtschaften, ein Schalter.** Der Bot erntete weiter mit dem Kartenprofil mal Stunden, der
Spieler mit dem Kern aus seinen Feldern. Jetzt gibt es `ertrag_weg` in `data/bot_wirtschaft.json`:
`karte` (Vorgabe, **B-4** von Daniel) oder `felder` (derselbe Weg wie der Spieler, ueber
`spieloekonomie.ort_tick`). Der Felder-Weg ist gebaut und geprueft - **eingeschaltet ist er nicht**,
weil er eine Daniels-Entscheidung aendern wuerde.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `c9e698e` plus diese Aenderung (Commit folgt) | `git log --oneline -1` |
| Voller Sammellauf | **138 von 140 gruen, 0 rot, 2 ausgesetzt, 5.555 Pruefungen, 388 s** (Start 03:49, auf dem CODE-Stand dieser Aenderung; Protokoll- und Stand-Zeilen danach sind ohne Code) | `docs/audits/sammellauf_20261103_0349.log` |
| Pruefdateien / Register / Quelldateien | **140** / **155** / **55** | `ls tests/test_*.py`, `grep -c '^| [0-9]'`, `ls src/*.py` |
| Neue Wache | `tests/test_bot_takt_kern.py` **26/0/1** (der Befund ist die offene Entscheidung selbst) | eigener Lauf |
| Der gemessene Unterschied | Kartenprofil gegen Felder: `original-036` Holz **14,06** / Gold **5,7** gegen **12,35** / **9,0**; `original-096` **12,92** / **3,3** gegen **12,35** / **9,0**; `original-087` **12,16** / **3,6** gegen **12,35** / **4,5** (zwergisch) | `tests/test_bot_takt_kern.py` |
| Kern-Modus im echten Takt | 48 Bot-Takte in **1,3 s**, 12 Anlagen je Dorf, Siedlerzuwachs **0 -> 10**, 47 Journalzeilen je Dorf, keine Ausnahme | Dauerspiel-Probe mit umgestelltem Schalter |

**Warum der Schalter statt eines Umbaus:** mit drei Anlagen je Rohstoff liefert der Kern JEDER Karte
denselben Grundertrag (12,35/13,65/12,0/9,0 zwergisch) - die Karte bestimmte dann nur noch, was
gebaut werden KANN. Daniels Vorgabe B-4 lautet aber "die Karte bestimmt den Ertrag". Also: beide
Wege leben, die Datendatei entscheidet, kein Code. **Ein Wort von Daniel** (`"ertrag_weg": "felder"`)
schaltet um.

**Ehrliche Grenzen:** (a) der Kern bucht Nahrung nur fuer eine eigene Garnison (`dorf.einheiten`);
die Armee bleibt in `bot.army` und isst ueber `bot_futter_buchen` im Hauptdorf - bildet S-5
Einheiten je Ort aus, muss die Armee dorthin wandern, sonst isst sie zweimal; (b) die Forschung geht
als leeres dict in den Tick (S-4 fehlt), also ohne Forschungsboni; (c) Zeiten dieses Blocks aus
`date`/`stat`, nicht geschaetzt.

## Der EINE naechste Schritt

**S-3: der Bot BAUT und baut AUS - wie der Spieler.** Vorher muss ein Widerspruch aufgeloest werden,
der beim Bauen sofort beisst: ein Bot fuehrt Siedler an ZWEI Stellen - `BotDorf.bevoelkerung` (Kern,
waechst) und `vorraete["siedler"]` (Kaufweg, feste 10 aus dem Start). Die belegten Bau- und
Einheitenpreise verlangen Siedler. Vorschlag: Siedler nur noch in `bevoelkerung` fuehren, alte
Staende beim Laden uebernehmen, Kauf und Bau von dort bezahlen. Danach der Bauplan je Taktik in
`data/`.

# STAND 03.11.2026, 03:46 - S-2: die Bot-Armee isst, die Kaufbremse haelt (Register 154)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Aus drei fertigen Helfern ist eine Wirkung geworden.** Ein Bot-Dorf bucht seit heute den
Nahrungsverbrauch seiner Armee (dieselbe Rechnung wie beim Spieler, 8 je Einheit und Spieltag),
haelt die Kaufbremse ein (Tagesbedarf plus Reserve) und bekommt beim ersten Takt seinen Bauplan
gesetzt. Gebucht wird nur im Hauptdorf - ein Bot hat EINE Armee, nicht je Dorf eine Garnison.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `80eca7a` plus diese Aenderung (Commit folgt), Arbeitsbaum vorher leer | `git log --oneline -1`, `git status --porcelain` |
| Voller Sammellauf | **137 von 139 gruen, 0 rot, 2 ausgesetzt, 5.529 Pruefungen, 382 s** (Lauf 03:39, auf dem CODE-Stand dieser Aenderung; die Dokumentzeilen danach sind ohne Code) | `docs/audits/sammellauf_20261103_0339.log` |
| Pruefdateien / Register / Quelldateien | **139** / **154** / **55** | `ls tests/test_*.py`, `grep -c '^| [0-9]'`, `ls src/*.py` |
| Neue Wache | `tests/test_bot_nahrung.py` **44/0/1** (der Befund ist gewollt: kein `siedler` aus der Ernte) | eigener Lauf |
| Wirkung, gemessen | 100 Einheiten = **800/Tag = 33,33 je Stunde**; Spieler (`ort_tick`) und Bot (`bot_futter_buchen`) auf denselben Verbrauch; Grenzfaelle **Soll deckt / Soll - 1 blockt / Soll + 1 deckt**; 200 Bot-Takte in **4,3 s** ohne eine unterdeckte Zeile | `tests/test_bot_nahrung.py`, Dauerspiel-Probe |

**Eigener Befund und behoben:** `bot_doerfer_bebauen` war NICHT idempotent - jeder Bot-Takt haette
drei weitere Anlagen je Rohstoff nachgelegt (nach 4 Takten 48 statt 12). Jetzt wird je Gebaeude nur
der fehlende Rest gesetzt (12 Anlagen, zweiter Aufruf 0). Eine alte Wache (`test_bot_dorf_als_ort`)
wurde rot, weil `bot_doerfer_karten_zuweisen` den Bauplan jetzt selbst setzt; sie prueft den Stand
danach und die Idempotenz - der Code wurde nicht zurueckgebogen.

**Ehrliche Grenzen (stehen auch in Register 154):** (a) der Anzeige-Weg `bot_dorf_ertrag` rechnet
weiter mit dem Kartenprofil, der Kern mit den Feldern - die Luecke schliesst erst S-2b; (b) die
Ernte liefert keinen Posten `siedler`, die belegten Preise verlangen ihn, also kauft ein Bot heute
nur aus seinem Startvorrat (loest S-5, Ausbildung je Ort); (c) das Hauptdorf isst allein, waehrend
die Kaufbremse die GANZE Kasse sieht (Nachschub ist S-7, Karawanen); (d) das
`produktionsjournal` waechst wie beim Spieler unbegrenzt (eine Zeile je Stunde und Ort).

## Der EINE naechste Schritt

**S-2b: der Takt laeuft ganz auf `ort_tick`** (Ernte, Siedlerzuwachs, Journal aus dem Kern) und
`bot_dorf_ertrag` rechnet denselben Weg wie der Kern. **Achtung, hier haengt eine Entscheidung
dran** (Frage 8.1 der Uebergabe): mit drei Anlagen je Rohstoff liefert der Kern fuer JEDE Karte
denselben Grundertrag - die Karte bestimmt dann nur, was gebaut werden KANN. Das ist eine
Aenderung gegenueber **B-4** ("die Karte bestimmt den Ertrag", Daniels Vorgabe). Vorschlag: den
Felder-Weg bauen, aber hinter einem Schalter in `data/bot_wirtschaft.json` (`ertrag_weg`), Vorgabe
zunaechst `karte` - dann entscheidet Daniel mit EINEM Wort, ohne Codeaenderung.

Danach in der Reihenfolge des Konzepts: **S-3** Bauen/Ausbauen nach Taktik, **S-4** Forschung,
**S-5** Ausbildung, **S-6** Nachgruenden (3 je Bot), **S-7** Karawanen, **S-8** Reisekosten,
**S-9** Stil je Taktik.

# STAND 03.11.2026, 02:45 - V-6: die Bot-Kartenwahl folgt jetzt einer Regel (Register 151)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**`botkern.oekonomie_kartenwahl` ist angeschlossen.** Die Funktion stand fertig im Kern und hatte
keinen Aufrufer - die Karte eines Bot-Dorfes kam allein aus der Gold-Regel. Jetzt entscheidet die
Stufe aus `data/bot_wirtschaft.json` (`kartenwahl_stufe`, heute `schwer` = hoechster Portfolio-Nutzen)
unter denselben drei reproduzierbaren Kandidaten; der Bot geht mit seinem Portfolio und seinen
Stundenertraegen hinein. Die Gold-Regel bleibt Rueckfall, damit kein Dorf ohne Karte und ohne Ertrag
bleibt.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `d754624`, Arbeitsbaum leer | `git log --oneline -1`, `git status --porcelain` |
| Voller Sammellauf | **135 von 137 gruen, 0 rot, 2 ausgesetzt, 5.448 Pruefungen, 415 s** | `docs/audits/sammellauf_20261103_0239.log` |
| Pruefdateien / Register / Quelldateien | **137** / **151** / **55** | `ls tests/test_*.py`, `grep -c '^| [0-9]'`, `test_projektpfade` |
| Neue Wache | `tests/test_kartenwahl_bot.py` **19/0/0** | eigener Lauf |
| Wirkung, gemessen | 3 Doerfer in **0,03 s**; Abweichung zur Gold-Regel bei **2 von 5** Bots (Grom: 2. Dorf `original-096` statt `original-087`); dieselbe Karte als ZWEITE Wahl **1,5349** statt **3,3118** wert | `test_kartenwahl_bot.py` |

**Ehrliche Grenze:** der Pfad "mittel" der Regel braucht einen BEDARF je Rohstoff - das Spiel fuehrt
nirgends einen Verbrauch. Deshalb steht die Stufe auf `schwer`; **welche Stufe gelten soll, ist
Daniels Entscheidung** (eine Zeile in der Datendatei, kein Code).

## Der EINE naechste Schritt

**Demo-Release vorbereiten** - der eingefrorene Umfang ist gebaut: Kernkreis, Spionage, Voelker- und
Kartenwahl am Start, Volksboni mit Wirkung, Bot-Kartenwahl nach Regel. Vorher Daniels Freigabe.
Danach: Kopplung Punkte/Kanaele und Balance-Messung (beide brauchen den Teiler-Entscheid),
Marktplatz-Motiv, und Bots gruenden weiterhin NICHT nach (offener Punkt: wann und womit).

# STAND 03.11.2026, 02:30 - V-5: die Volks- und Taktikboni WIRKEN (Register 149/150)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Aus der Anzeige ist eine Wirkung geworden.** Sechs Voelker und fuenf Taktiken hatten Plus und
Minus, gerechnet hat damit nichts. Seit heute rechnen Er traege (Bot und Spieler), Reisezeit, AT,
PA, Beute, Handelserloes und Ausbaupreis mit - die Zahlen stehen in `data/boni.json`, die
Datenschicht ist `src/boni.py`, die Anzeigetexte bleiben in `data/voelker.json` (eine Wache
vergleicht beide, damit sie nicht auseinanderlaufen).

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `71abeba`, Arbeitsbaum leer | `git log --oneline -1`, `git status --porcelain` |
| Voller Sammellauf | **134 von 136 gruen, 0 rot, 2 ausgesetzt, 5.429 Pruefungen, 369 s** | `docs/audits/sammellauf_20261103_0224.log` |
| Pruefdateien / Register / Quelldateien | **136** / **150** / **55** | `ls tests/test_*.py`, `grep -c '^| [0-9]'`, `test_projektpfade` 113/0/0 |
| Neue Wache | `tests/test_boni.py` **82/0/0**, Gegenprobe `aktiv: false` -> 7 Fehler | eigener Lauf |
| Guthaben | von Daniel 01:44 abgelesen: **4,63 USD**, gesamt 45,36 USD. Budget der Sitzung 3 USD (21:18), davon rechnerisch 1,82 USD offen; Kontostand NICHT neu abgelesen | `docs/ENTWICKLUNGSPROTOKOLL.md` |

**Daniels Entscheidungen (Fragenrunde 01:47-01:52):** Ueberschneidung **additiv** (5 % + 5 % =
+10 %, nicht 10,25 %); Hoehe bleibt **5 %**; Taktikbonus gilt, solange die Taktik steht, nach einem
Wechsel **48 h gesperrt**; der **Spieler** bekommt dieselben Volksboni wie ein Bot; Gnome "Ausbau
+5 %" wirkt als **-5 % Gebaeudepreise**.

**13 Wirkungen, ehrlich gezaehlt:** 12 wirken (Holz/Stein/Nahrung/Gold je Volk, Reise und PA
elfisch, AT und Handel Trolle, PA Ghule, Baukosten und AT Gnome, dazu Beute Haug, Verteidigung
Brynhild, Reise Silra, AT Krank). **Eine wirkt nicht: Groms "Ausbau +5 %"** - die Bots haben keine
Bauwirtschaft; sie steht als `ohne_anker` in der Datei und wird nicht erfunden. AT wirkt nur im
Nahkampf; bei kleinen Preisen frisst die Ganzzahl-Rundung den Rabatt (8 Stein bleibt 8).

**Eigener Befund und behoben:** `spieler_fraktion` wurde beim LADEN nie zurueckgelesen - ein
geladener Stand verlor sein Volk (und damit seit heute die Wirkung). **Vom Sammellauf gefunden:**
drei Wachen (Bot-Wirtschaft, Kartenprofil, Spionage) wurden rot, weil sie Anzeige und Kern mit dem
alten Aufruf ohne `bot` verglichen; die Zusicherung "Anzeige = Kern" bleibt, sie ist jetzt mit
demselben Bot formuliert.

## Der EINE naechste Schritt

**Demo-Release vorbereiten** - der eingefrorene Demo-Umfang ist damit gebaut: Kernkreis, Spionage,
Voelker- und Kartenwahl am Start, Volksboni mit Wirkung. Vorher Daniels Freigabe. Danach die
offenen Punkte aus der letzten Uebergabe: Anschluss `botkern.oekonomie_kartenwahl` (hat keinen
Aufrufer), Kopplung Punkte/Kanaele und Balance-Messung (beide brauchen den Teiler-Entscheid),
Marktplatz-Motiv.

# STAND 03.11.2026, 01:08 - A2: sechs Voelker, der Spieler waehlt (Register 148)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Der Spieler hat jetzt ein Volk.** Sechs Fraktionen stehen in `data/voelker.json`: menschlich,
zwergisch, elfisch, Trolle, Ghule, Gnome - Trolle, Ghule und Gnome ersetzen die fruehere Fraktion
"monster" (Daniel 03.11.2026). Der Spieler waehlt im Dorfzentrum VOR der Kartenwahl; die fuenf Bots
bekommen die uebrigen Voelker, jedes genau einmal. Die Wahl steht im Spielstand und bleibt als Zeile
"Dein Volk: ..." sichtbar.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `8180140` plus dieser Schritt | `git log --oneline -1` |
| Datenquelle | sechs Fraktionen mit Plus, Minus, Beschreibung und Quelle je Wert | `data/voelker.json` |
| Code liest die Datei | Datenschicht `src/voelker.py` liest `data/voelker.json`; `bottaktik` fragt dort nach (es darf selbst keine Datei oeffnen); ohne Datei alter Rueckfallsatz | `src/voelker.py`, `src/bottaktik.py` |
| Neues Modul | `src/voelker.py`, Modulkarte auf 54 Dateien nachgezogen | `docs/MODULKARTE.md` |
| Verteilung | `verteile_fraktionen` - Bots nach Namen, Voelker in Datei-Reihenfolge, keine Doppelung | ebd. |
| Wache | `tests/test_voelkerwahl.py` **37/0/0** | eigener Lauf |
| Gegenprobe | Verteilung abgeschaltet -> rot (1 Fehler), Datei danach hashgleich | eigener Lauf |
| Umgestellte Wachen | `test_s7_botverhalten` ("genau die vier Fraktionen") und `test_botkern` ("monster") tragen die neue Entscheidung im Docstring | eigene Laeufe |
| Pruefdateien / Register | **135** / **148** | `ls tests/test_*.py`, `grep -c '^| [0-9]'` |
| Voller Sammellauf | **133 von 135 gruen, 0 rot, 2 ausgesetzt, 5.351 Pruefungen, 415 s** | `docs/audits/sammellauf_20261103_0118.log` |

**Ehrlich zur Wirkung:** die Boni sind eine ANZEIGE. Kein Ertrag, keine Reise und kein Kampfwert rechnet
heute mit dem Volk - das ist Auftrag V-5 und braucht Daniels Pruefung des Entwurfs.

**Ehrlich zur Wache:** die erste Fassung zaehlte fuenf Bots fest. Der Startzustand hat je nach Lage zwei
bis fuenf Bots - die Wache war damit wackelig und prueft jetzt die REGEL (jeder vorhandene Bot traegt
eine Fraktion aus der Verteilung, keine doppelt) statt einer Zahl.

## Der EINE naechste Schritt

**Volksboni verdrahten (Auftrag V-5)** - der Entwurf liegt vor und ist geprueft. Vorher braucht es
Daniels Entscheid zu den Fragen aus V-5 (Ueberschneidung Silra/Krank, Hoehe der Wirkung, Sperrzeit).
Danach: Kopplung Punkte/Kanaele (C), Balance-Messung (D), zuletzt Demo-Release (Freigabe Daniel).

**Marktplatz:** braucht ein Motiv von Daniel (Motiv 2 "Kuppelbau" ist im Handbuch als nicht entscheidbar
vermerkt).

**Demo-Umfang ist eingefroren (Daniel 02.11.2026):** Kernkreis + Spionage + Voelker- und Kartenwahl
am Start. Mit Register 148 ist die Voelkerwahl gebaut, die Kartenwahl mit Register 147 - es fehlt nur
noch die Wirkung der Volksboni.

# STAND 03.11.2026, 00:37 - A2-Vorstufe: der Spieler waehlt seine Startkarte (Register 147)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Die Startkarte war fest verdrahtet, jetzt waehlt der Spieler.** Solange keine Siedlung steht und
nichts gewaehlt ist, steht im Dorfzentrum ein eigener Block "Waehle deine Startkarte": drei mittlere
Karten mit ihren drei Achsen (Holz/Stein/Agrar) und einem Knopf je Karte. Der Block ERSETZT das
Dorfzentrum nicht - Pflichtkarte und Gruendungsknopf bleiben, und der Knopf gruendet ohne Wahl mit der
Standardkarte `original-036`. Die Kandidaten sind je Startsaat reproduzierbar, alle Zahlen stehen in
`data/startkarte.json`, die Wahl landet im Spielstand (`startkarte_gewaehlt`).

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `fd734ae` plus dieser Schritt | `git log --oneline -1` |
| Entwurf (starkes Modell) | `deepseek-v4-pro`, 30.987 Token (23.963 Denk), 13.824 Zeichen in 194 s | `docs/design/STARTKARTE_ENTWURF_20261103.md`, `docs/audits/usage_startkarte_20261103.json` |
| Eigene Korrekturen am Entwurf | Modell nahm Objekte statt Dicts an (`alle()` liefert Dicts); die Maske war als `TODO` offen und wurde selbst gebaut | `src/originalkarten.py`, `src/main.py` |
| Wache | `tests/test_startkartenwahl.py` **28/0/0** | eigener Lauf |
| Gegenprobe | Aufruf zurueck auf `startkarte(...)` -> **26 bestanden, 2 Fehler**, Datei danach hashgleich (`983f7df0...`) | eigener Lauf |
| Mitgezogen | `test_gebaeude_icons` 56/0/0, `test_ansicht_hintergrund` 81/0/0, `test_baseline` 40/0/0 | eigene Laeufe |
| Vom Sammellauf korrigiert | der erste Anlauf ersetzte das Dorfzentrum - `test_startspiel` und `test_gpt_pflicht_starthilfe_fix04f` wurden rot; jetzt ist die Wahl ein Block, die Zaehlwachen bleiben bei 3 | `tests/test_startspiel.py` 62/0/1, `test_gpt_pflicht_starthilfe_fix04f` 9 Tests OK |
| Pruefdateien / Register | **134** / **147** | `ls tests/test_*.py`, `grep -c '^| [0-9]'` |
| Voller Sammellauf | **132 von 134 gruen, 0 rot, 2 ausgesetzt, 5.307 Pruefungen, 295 s** | `docs/audits/sammellauf_20261103_0049.log` |

**Der stehende Aufruf bleibt:** `_found_settlement()` und `_erste_siedlung_gruenden()` ohne Argument
gruenden weiterhin sofort mit der Standardkarte - 16 Pruefdateien mit 22 Aufrufstellen haengen daran.

**Ebenfalls fertig, aber NICHT eingebaut: der Voelkerwahl-Entwurf.** `deepseek-v4-pro` hat auf das Paket
`docs/auftraege/VOELKER_paket_20261103.md` in 124 s einen Entwurf geliefert (17.421 Zeichen, 18.203
Token) - `docs/design/VOELKER_ENTWURF_20261103.md`. Daniel hat die sechs Fraktionen vorgegeben
(menschlich, zwergisch, elfisch, Trolle, Ghule, Gnome; die drei neuen ERSETZEN "monster"). Offen ist
seine Entscheidung zu Plus/Minus der drei neuen Fraktionen - jede Zahl dafuer waere sonst geraten.

## Der EINE naechste Schritt

**Den Voelkerwahl-Entwurf pruefen und einbauen** (A2): Daniels Entscheid zu Plus/Minus von Trollen,
Ghulen und Gnomen einholen, dann `data/voelker.json` mit Quelle je Wert anlegen, die Fraktion in den
Spielstand bringen (heute `botkern.BOT_FRAKTIONEN` fest, 4 Fraktionen fuer 5 Bots, `menschlich` doppelt),
die Startwahl ins Startfenster neben die Kartenwahl setzen und die fuenf Bots die uebrigen Fraktionen
bekommen lassen - ohne Doppelung. Danach voller Sammellauf, Protokollzeile, ein Commit.

**Danach:** Volksboni verdrahten (Auftrag V-5 liegt vor, wartet auf Daniels Pruefung), Kopplung
Punkte/Kanaele (C), Balance-Messung (D), zuletzt Demo-Release (Freigabe Daniel).
**Marktplatz:** braucht ein Motiv von Daniel (Motiv 2 "Kuppelbau" ist im Handbuch als nicht entscheidbar
vermerkt) - ohne Zuordnung wird dort nichts gebaut.

**Demo-Umfang ist eingefroren (Daniel 02.11.2026):** Kernkreis + Spionage + Voelker- und Kartenwahl
am Start. Alles andere kommt NACH dem ersten Demo-Upload.

# STAND 03.11.2026, 00:05 - Stufe M-6: die Forschungszeilen passen ins Fenster (Register 146)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Der Befund aus Register 145 ist behoben.** Die Forschungszeile wurde von links nach rechts gepackt:
Name, Stufe und Beschreibung zuerst, Forschen-Knopf und Sperrgrund danach. Bei langen Beschreibungen
schob der Text die rechte Seite aus dem Fenster - im echten Fenster (1460 x 940, Inhaltsbreite 1052 px)
brauchten 14 von 14 Zeilen zwischen 1076 und 1903 px. Jetzt wird die rechte Seite ZUERST gepackt (der
Knopf bleibt ganz rechts) und die Beschreibung bricht mit `wraplength` um; Sperrgrund und
Freischalt-Text ebenso.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `2326863` plus dieser Schritt | `git log --oneline -1` |
| Messung vorher | 14 von 14 Zeilen ueber dem Platz: 1076 bis 1903 px bei 1052 px Inhaltsbreite | eigene Messfahrt (`winfo_reqwidth` je Kind) |
| Messung nachher | 21 von 21 Zeilen ohne Ueberlauf, kein Kind liegt ausserhalb (`winfo_x + winfo_width`) | eigene Messfahrt |
| Wache | `tests/test_ansicht_hintergrund.py` **81/0/0** (vorher 74; neuer Abschnitt 9) | eigener Lauf |
| Gegenprobe | Knopf wieder `side=LEFT` -> **79 bestanden, 2 Fehler**; Datei danach hashgleich (`84d62944...`) | eigener Lauf |
| Ansicht im Fenster | Forschung, Zeilen vollstaendig lesbar | `docs/design/M6_FORSCHUNG_ZEILEN_20261102.png` |
| Pruefdateien / Register | **133** / **146** | `ls tests/test_*.py`, `grep -c '^| [0-9]'` |
| Voller Sammellauf | **131 von 133 gruen, 0 rot, 2 ausgesetzt, 5.278 Pruefungen, 335 s** | `docs/audits/sammellauf_20261102_2356.log` |

**Ehrlich zum ersten Bild-Beleg:** `docs/design/M5_FORSCHUNG_20261102.png` zeigt den Zustand VOR der
Behebung (abgeschnittene Beschreibungen) - es ist der Beleg zum Befund. `M6_FORSCHUNG_ZEILEN_20261102.png`
zeigt denselben Bildschirm nach der Behebung.

## Der EINE naechste Schritt

**Die uebrigen Textfelder der Ansichten, stueckweise - weiter mit Lager/Marktplatz** (Vorgabe Daniel
02.11.2026: "dann die uebrigen Textfelder", "stueck fuer stueck"). Erledigt sind Dorfzentrum, Forschung
und die drei Ausbildungsstaetten samt Warteschlange (Register 139, 142, 144, 145). Offen: Lager/
Marktplatz, Diplomatie, Nachrichten, Portal. Fuer diese Ansichten gibt es noch KEINEN Gebaeudehintergrund;
dort ist die Reihenfolge: erst `_ansicht_hintergrund` anlegen, dann die harten `tk.Label(... bg=...)`-
Bloecke auf `_kasten_label` umstellen, Tabellen deckend lassen, je Ansicht ein Eintrag in
`tests/test_ansicht_hintergrund.py`, voller Sammellauf, Protokollzeile, ein Commit.

**Offene Frage an Daniel dazu:** diese vier Ansichten sind fast nur Tabellen - sollen sie ueberhaupt ein
Gebaeudemotiv als Hintergrund bekommen (Empfehlung: Lager und Marktplatz ja, Diplomatie und Nachrichten
nein, Portal pruefen), oder bleiben sie reine Datenansichten mit harten Bloecken?

**Demo-Umfang ist eingefroren (Daniel 02.11.2026):** Kernkreis + Spionage + Voelker- und Kartenwahl
am Start. Alles andere kommt NACH dem ersten Demo-Upload.

**Danach in dieser Reihenfolge:** Voelkerwahl am Start (A2), Kartenwahl fuer den SPIELER, Volksboni
verdrahten (A), Anschluss `botkern.oekonomie_kartenwahl`, Kopplung Punkte/Kanaele (C),
Balance-Messung (D), zuletzt Demo-Release (Freigabe Daniel).

# STAND 02.11.2026, 23:45 - Stufe M-5: Titel und Einleitung der Forschung liegen als weiche Felder auf dem Bild (Register 145)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Die Forschung war die letzte Ansicht mit Bibliotheks-Hintergrund, die noch harte Balken trug.** Titel
("Forschung") und Einleitungssatz liegen jetzt als abgerundete Felder auf dem Motiv; die Forschungszeilen
darunter bleiben ein deckender Block.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `9f2d300` plus dieser Schritt | `git log --oneline -1` |
| Umgestellte Zeilen | 2 in `main._render_research` (Titel, Einleitung) | ebd. |
| Wache | `tests/test_ansicht_hintergrund.py` **74/0/0** (vorher 67; neuer Abschnitt 8) | eigener Lauf |
| Gegenprobe | Titel zurueckgebaut -> **71 bestanden, 3 Fehler**; Datei danach hashgleich (`7d27229a...`) | eigener Lauf |
| Ansicht im Fenster | Forschung mit Bibliotheksmotiv | `docs/design/M5_FORSCHUNG_20261102.png` |
| Pruefdateien / Register | **133** / **145** | `ls tests/test_*.py`, `grep -c '^| [0-9]'` |
| Voller Sammellauf | **131 von 133 gruen, 0 rot, 2 ausgesetzt, 5.276 Pruefungen, 332 s** | `docs/audits/sammellauf_20261102_2347.log` |

**BEFUND, gemessen und NICHT in diesem Schritt behoben:** die Forschungszeilen laufen ueber den rechten
Rand. In der Ansicht Forschung brauchen 14 von 14 Zeilen mehr Platz als die 1052 px Inhaltsbreite des
Fensters (1076 bis 1903 px; gemessen als Summe der `winfo_reqwidth` aller Kinder einer Zeile). Folge:
die Beschreibungen werden abgeschnitten, und bei den gesperrten Forschungen liegt der Grund-Text unter
dem "Forschen"-Knopf. Ursache ist die Pack-Reihenfolge der Zeile (die Knoepfe kommen NACH den linken
Texten), nicht die Umstellung der Textfelder. Im Bild-Beleg ist der Zustand zu sehen.

## Der EINE naechste Schritt

**Die Forschungszeilen in Ordnung bringen** (BEFUND aus Register 145): die rechte Seite einer Zeile
(Knopf, Restzeit, Sperrgrund) zuerst packen, dem Beschreibungstext eine `wraplength` geben, die sich aus
der Inhaltsbreite ergibt, und die Zeile messbar pruefen (Summe der `winfo_reqwidth` <= Inhaltsbreite,
wie in der Messfahrt dieser Sitzung). Danach voller Sammellauf, Protokollzeile, ein Commit.

**Danach weiter mit den uebrigen Textfeldern, stueckweise** - Lager/Marktplatz, Diplomatie, Nachrichten,
Portal. Fuer diese Ansichten gibt es noch KEINEN Gebaeudehintergrund; dort ist die Reihenfolge: erst
`_ansicht_hintergrund` anlegen, dann die harten `tk.Label(... bg=...)`-Bloecke auf `_kasten_label`
umstellen, Tabellen deckend lassen, je Ansicht ein Eintrag in `tests/test_ansicht_hintergrund.py`,
voller Sammellauf, Protokollzeile, ein Commit. **Offene Frage an Daniel:** sollen diese vier Ansichten
ueberhaupt ein Gebaeudemotiv als Hintergrund bekommen (sie sind fast nur Tabellen)?

**Demo-Umfang ist eingefroren (Daniel 02.11.2026):** Kernkreis + Spionage + Voelker- und Kartenwahl
am Start. Alles andere kommt NACH dem ersten Demo-Upload.

**Danach in dieser Reihenfolge:** Voelkerwahl am Start (A2), Kartenwahl fuer den SPIELER, Volksboni
verdrahten (A), Anschluss `botkern.oekonomie_kartenwahl`, Kopplung Punkte/Kanaele (C),
Balance-Messung (D), zuletzt Demo-Release (Freigabe Daniel).

# STAND 02.11.2026, 23:40 - Stufe M-4: die Warteschlange der Ausbildung traegt weiche Textfelder (Register 144)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Der Kopf der Warteschlange und ihre zwei Hinweiszeilen liegen jetzt als abgerundete Felder auf dem
Gebaeudemotiv.** "In Arbeit: N Auftrag/Aufträge - insgesamt noch ...", der Leerfall "Keine Aufträge in
Arbeit." und die Reihenfolge-Erklaerung. Die Auftragszeilen selbst bleiben ein DECKENDER Block - sie
sind die Tabelle - und dieser Block entsteht nur noch, wenn wirklich Auftraege laufen (vorher blieb bei
leerer Schlange ein leerer Balken im Bild).

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `ee63126` plus dieser Schritt | `git log --oneline -1` |
| Umgestellte Zeilen | 3 in `main._ausbildung_warteschlange_zeichnen` (Kopf, Leerfall, Reihenfolge) | ebd. |
| Wache | `tests/test_ansicht_hintergrund.py` **67/0/0** (vorher 44; neuer Abschnitt 7 mit Quelltext- und GUI-Probe) | eigener Lauf |
| Gegenprobe | Kopfzeile zurueckgebaut -> **65 bestanden, 2 Fehler**; Datei danach hashgleich (`4f1fa54e...`) | eigener Lauf |
| Ansicht im Fenster | Kaserne mit zwei laufenden und einem wartenden Auftrag | `docs/design/M4_WARTESCHLANGE_20261102.png` |
| Pruefdateien / Register | **133** / **144** | `ls tests/test_*.py`, `grep -c '^| [0-9]'` |
| Voller Sammellauf | **131 von 133 gruen, 0 rot, 2 ausgesetzt, 5.264 Pruefungen, 340 s** | `docs/audits/sammellauf_20261102_2334.log` |

**Ehrlich zum Beleg:** der erste Screenshot der Vorschau nannte eine von Hand gesetzte, erfundene
Einheiten-Kennung ("Kaempfer"). Die Zeilen nennen in Wahrheit den Anzeigenamen aus `data/units.json`
("Kämpfer"); das Bild wurde mit dem echten Namen neu aufgenommen. Kein Mangel im Spiel - ein Fehler in
meinen Vorschau-Daten.

## Der EINE naechste Schritt

**Die uebrigen Textfelder der Ansichten, stueckweise - weiter mit Lager/Marktplatz** (Vorgabe Daniel
02.11.2026). Die Warteschlange der Ausbildung ist erledigt (Register 144). Als naechstes: Lager und
Marktplatz, danach Diplomatie, Forschung (Restzeilen), Nachrichten und Portal. Fuer diese Ansichten gibt
es noch KEINEN Gebaeudehintergrund - dort ist die Reihenfolge: erst `_ansicht_hintergrund` anlegen (wie in
Dorfzentrum, Forschung und den drei Ausbildungsstaetten), dann die harten `tk.Label(... bg=...)`-Bloecke
auf `_kasten_label` umstellen, Tabellen deckend lassen, je Ansicht ein Eintrag in
`tests/test_ansicht_hintergrund.py`, voller Sammellauf, Protokollzeile, ein Commit.

**Demo-Umfang ist eingefroren (Daniel 02.11.2026):** Kernkreis + Spionage + Voelker- und Kartenwahl
am Start. Alles andere kommt NACH dem ersten Demo-Upload.

**Danach in dieser Reihenfolge:** Voelkerwahl am Start (A2), Kartenwahl fuer den SPIELER, Volksboni
verdrahten (A), Anschluss `botkern.oekonomie_kartenwahl`, Kopplung Punkte/Kanaele (C),
Balance-Messung (D), zuletzt Demo-Release (Freigabe Daniel).

# STAND 02.11.2026, 22:55 - Stufe M-3: maximiertes Fenster in Ordnung - Leiste unverzerrt, Hintergrund bis zum Rand (Register 143)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Daniels Befund vom Desktop-Screenshot ist behoben.** Die Ressourcenleiste skaliert nicht mehr mit
der Fensterbreite: die Symbole bleiben in Originalgroesse, die zusaetzliche Breite entsteht durch
Wiederholung der gemalten Landschaft, die Hoehe bleibt 140 px. Der Gebaeudehintergrund liegt nicht
mehr fest bei 980 x 760, sondern fuellt den Inhaltsbereich und wird bei jeder Groessenaenderung in
der Zielgroesse neu gebaut.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `badba55` plus dieser Schritt | `git log --oneline -1` |
| Leiste | `rest_auffuellen: kacheln`; Skala bleibt 1,0, Hoehe 140 px, Luecken werden wiederholt | `data/ressourcenleiste.json`, `main.leiste_zusammensetzen` |
| Wache Leiste | Symbolkachel bei 2560/3440 px **pixelgleich** zum Original (Abweichung 0,00) | `tests/test_ressourcenleiste.py` **43/0/1** |
| Hintergrund | `relwidth=1/relheight=1`, `<Configure>` -> `_hintergrund_anpassen` -> `_hintergrund_bauen` (64-px-Schritte, 120 ms Ruhe) | `main._ansicht_hintergrund` |
| Wache Hintergrund | Abschnitt 6: Flaeche relativ gebunden, neues Mass 1664 x 960 baut ein Bild dieser Groesse | `tests/test_ansicht_hintergrund.py` **53/0/0** |
| Messung im maximierten Fenster | Leistenflaeche 1536 x 140, Leistenbild 1536 x 140, Hintergrundflaeche 1142 x 868 = Inhaltsbereich | eigene Messfahrt |
| Ansicht | Screenshot maximiert und Leiste bei 3832 px | `docs/design/M3_MAXIMIERT_20261102.png`, `docs/design/LEISTE_3832_NEU_20261102.png` |
| Pruefdateien / Register | **133** / **143** | `ls tests/test_*.py`, `grep -c '^| [0-9]'` |
| Voller Sammellauf | **131 von 133 gruen, 0 rot, 2 ausgesetzt, 5.250 Pruefungen, 326 s** (23:04) | `docs/audits/sammellauf_20261102_2304.log` |
| Wache Luecken | `tests/test_leisten_luecken.py` **27/0/0** (Periode 48 px: die Luecke ist eine Wiederholung, keine Dehnung) | eigener Lauf |

**Was dabei entschieden wurde:** die P-3-Regel ("oberhalb von `skala_max` waechst das ganze Band
gleichmaessig bis `skala_hart`") ist mit Daniels Befund ueberholt. Die alten Wachen nagelten das
Wachstum fest und wurden mit Begruendung umgestellt - nicht der Code zurueckgebogen.

## Der EINE naechste Schritt

**Die uebrigen Textfelder der Ansichten, stueckweise** (Vorgabe Daniel 02.11.2026). Kandidaten in
dieser Reihenfolge: Warteschlange der Ausbildung (Kopfzeile und die zwei Hinweiszeilen),
Lager/Marktplatz, Diplomatie, Forschung (Restzeilen), Nachrichten und Portal.

Zu tun: je Ansicht die harten `tk.Label(... bg=self.skin["bg"])`-Bloecke auf `_kasten_label`
umstellen, Tabellen deckend lassen, Wachen nicht auf Wortlaut biegen sondern mitziehen, je Ansicht
ein Eintrag in `tests/test_ansicht_hintergrund.py`, voller Sammellauf, Protokollzeile, ein Commit.
Arbeitsweise: ein Schritt = ein Commit = ein gruener voller Sammellauf.

**Demo-Umfang ist eingefroren (Daniel 02.11.2026):** Kernkreis + Spionage + Voelker- und Kartenwahl
am Start. Alles andere kommt NACH dem ersten Demo-Upload.

**Danach in dieser Reihenfolge:** Voelkerwahl am Start (A2), Kartenwahl fuer den SPIELER, Volksboni
verdrahten (A), Anschluss `botkern.oekonomie_kartenwahl`, Kopplung Punkte/Kanaele (C),
Balance-Messung (D), zuletzt Demo-Release (Freigabe Daniel).

# STAND 02.11.2026, 22:40 - Stufe M-2: die Kastenoptik steht in Kaserne, Stellmacher und Diebesgilde (Register 142)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Die drei Ausbildungsstaetten sehen aus wie Dorfzentrum und Forschung.** Titel, Einleitung,
Siedlerwarnung und der Spionage-Abschnitt liegen als abgerundete, weiche Felder auf dem
Gebaeudemotiv; zwischen den Feldern ist das Bild zu sehen. Die Tabellen (Einheiten, Warteschlange)
bleiben deckende Bloecke - genau die Trennung, die Daniel beschrieben hat.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `569fd36` plus dieser Schritt | `git log --oneline -1` |
| Umgestellte Bloecke | 8: Titel, Einleitung, "Keine Einheit", Siedlerwarnung (2 Zeilen), Spionage-Ueberschrift, Dorfzeile, Schwellen-Erklaerung | `main._render_ausbildung`, `_siedler_warnung_zeichnen`, `_spionage_abschnitt` |
| Zahlen | alle aus `data/gebaeude_motive.json` (Radius, Deckkraft, Farbe) | ebd. |
| Wache | `tests/test_ansicht_hintergrund.py` **44/0/0** (neu: Abschnitt 5 fuer alle drei Ansichten) | eigener Lauf |
| Nebengeprueft | `test_kaserne_ohne_gebaeude` 11/0/0, `test_siedler_warnung` 29/0/0, `test_gebaeude_icons` 56/0/0, `test_ausbildungsauftraege` 59/0/0 | eigene Laeufe |
| Ansicht im Fenster | Screenshot der Diebesgilde mit Feldern und sichtbarem Motiv | `docs/design/KASTEN_DIEBESGILDE_20261102.png` |
| Pruefdateien / Register | **133** / **142** | `ls tests/test_*.py`, `grep -c '^| [0-9]'` |

**Ehrlich zur Optik:** die Felder sind abgerundet, aber sie wirken noch immer wie Balken - ein
weicher Verlauf ist bei 8 px Radius kaum zu sehen. Der naechste Feinschliff gehoert zu den uebrigen
Textfeldern; ein eigenes Darstellungs-Papier dafuer ist noch nicht geschrieben.

## Der EINE naechste Schritt

**Die uebrigen Textfelder der Ansichten, stueckweise** (Vorgabe Daniel 02.11.2026). Kandidaten in
dieser Reihenfolge: Warteschlange der Ausbildung (Kopfzeile und die zwei Hinweiszeilen),
Lager/Marktplatz, Diplomatie, Forschung (Restzeilen), Nachrichten und Portal.

Zu tun: je Ansicht die harten `tk.Label(... bg=self.skin["bg"])`-Bloecke auf `_kasten_label`
umstellen, Tabellen deckend lassen, Wachen nicht auf Wortlaut biegen sondern mitziehen, je Ansicht
ein Eintrag in `tests/test_ansicht_hintergrund.py` (Hintergrund zuerst, mindestens zwei Felder,
Text noch da), voller Sammellauf, Protokollzeile, ein Commit.
Arbeitsweise: ein Schritt = ein Commit = ein gruener voller Sammellauf.

**Demo-Umfang ist eingefroren (Daniel 02.11.2026):** Kernkreis + Spionage + Voelker- und Kartenwahl
am Start. Alles andere kommt NACH dem ersten Demo-Upload.

**Danach in dieser Reihenfolge:** Voelkerwahl am Start (A2), Kartenwahl fuer den SPIELER, Volksboni
verdrahten (A), Anschluss `botkern.oekonomie_kartenwahl`, Kopplung Punkte/Kanaele (C),
Balance-Messung (D), zuletzt Demo-Release (Freigabe Daniel).

# STAND 02.11.2026, 21:45 - Stufe M-1: Truppenbewegungen sind auf der Weltkarte sichtbar (Register 141)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Jeder laufende Auftrag hat jetzt eine Linie im Gelaendekaestchen.** Sichtbar ist nur das
Oeffentliche: Startfeld, Zielfeld, die Linie und die Bewegung darauf - als grobe Restzeit in einer
Zeile ueber der Karte und im Klickfenster (Vorgabe Daniel, Register 140). Truppenart, Anzahl,
Karren und die genaue Geschwindigkeit bleiben verborgen; laeuft ein Marsch auf eine EIGENE Siedlung
zu, steht die Wegzeit genau da. Entworfen hat die Darstellung das starke Modell (`deepseek-v4-pro`)
in drei Fassungen; eingebaut ist Fassung A.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `959e04a` plus dieser Schritt | `git log --oneline -1` |
| Entwurf (starkes Modell) | 278 Zeilen, drei Fassungen mit exakten Zahlen, Empfehlung A, Umsetzungsplan | `docs/design/MARSCH_ENTWURF_20261102.md`, `docs/audits/usage_m1_20261102.json` |
| Messung des Laufs | 10 Aufrufe, 757.216 Prompt-Token (656.640 aus dem Cache), 20.385 Antwort-Token, 12.585 Denk-Token | ebd. `usage_m1_20261102.json` |
| Vergleichsblatt | drei Fassungen, oben doppelt gross und unten in Originalgroesse (20 px je Feld) | `docs/design/MARSCH_VERGLEICH_20261102.png`, `tools/marsch_vergleich.py` |
| Zahlen der Anzeige | Symbol 6 px `#F59E0B`, Linie 2 px, Rueckreise `#38BDF8`, Marker hohl 8 px `#DAA520`, Takt 400 ms, Stufen 1/3/6 h, Toleranz 6 px | `data/marsch_optik.json`, `src/marsch_optik.py` |
| Zeichnen | vier Canvas-Objekte je Marsch, Tags `marsch` und `marsch_<n>`, Alte werden beim Rendern geloescht | `main._marsche_zeichnen` |
| Klick | erst Dorf, dann Marsch (6-px-Band um die Linie), dann Feld | `main._portal_klick`, `main._marsch_an` |
| Wache | `tests/test_marsch_optik.py` **63/0/0** | eigener Lauf |
| Voller Sammellauf | **131 von 133 gruen, 0 rot, 2 ausgesetzt, 5.224 Pruefungen, 357 s** (21:55) | `docs/audits/sammellauf_20261102_2155.log` |
| Pruefdateien / Register | **133** / **141** | `ls tests/test_*.py`, `grep -c '^| [0-9]'` |

**Zwei Befunde, offen benannt:** (1) `Settlement.x/y` liegt im ALTEN `MAPS`-Raster (20 nur bei
`kontinent`), dass das Portal-Raster dieselben Felder meint, ist nicht belegt - deshalb steht die
Aufloesung an einer einzigen Stelle (`main._marsch_felder`) und die Lesart ist VORSCHLAG.
(2) Bot-Doerfer tragen ihre Position erst nach `bot_doerfer_auffrischen_alle`; vorher liegt jedes
Dorf auf 0/0, und jede Wache, die ohne diesen Schritt zaehlt, prueft ein leeres Bild.

## Der EINE naechste Schritt

**Kastenoptik in Kaserne, Stellmacher und Diebesgilde** (Daniels Wahl aus der Fragenrunde 02.11.2026),
danach die uebrigen Textfelder der Ansichten - Vorgabe: stueckweise. Der Vorzustand ist gebaut und
geprueft (Register 139): das Gebaeudemotiv ist der Hintergrund, die Texte stehen in abgerundeten
Feldern davor; die drei Ausbildungsstaetten haben die Textfelder noch NICHT.

Zu tun: je Ansicht die Textbloecke auf `gebaeude_optik.kasten_bild` umstellen (wie Dorfzentrum und
Forschung), Zahlen nur aus `data/gebaeude_motive.json`, alte Wachen auf Wortlaut und Groesse
mitziehen, Pruefdatei erweitern, voller Sammellauf, Protokollzeile, ein Commit.
Arbeitsweise: ein Schritt = ein Commit = ein gruener voller Sammellauf.

**Demo-Umfang ist eingefroren (Daniel 02.11.2026):** Kernkreis + Spionage + Voelker- und Kartenwahl
am Start. Alles andere kommt NACH dem ersten Demo-Upload.

**Danach in dieser Reihenfolge:** uebrige Textfelder, Voelkerwahl am Start (A2), Kartenwahl fuer den
SPIELER, Volksboni verdrahten (A), Anschluss `botkern.oekonomie_kartenwahl`, Kopplung Punkte/Kanaele
(C), Balance-Messung (D), zuletzt Demo-Release (Freigabe Daniel).

# STAND 02.11.2026, 20:59 - Stufe B-6: das Gebaeudemotiv ist der Hintergrund, Texte stehen davor (Register 139)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Das gemalte Bild traegt jetzt die Ansicht - und zwar hinter dem Inhalt.** Dorfzentrum, Forschung
(Bibliothek) und die drei Ausbildungsstaetten legen das Motiv als eigene Flaeche an, die ZUERST
entsteht; die Texte liegen als abgerundete, fast deckende Felder mit warmem Braun und feinem Goldrand
darueber. Das Bild ist zurueckgenommen (38 % Abdunkelung, 2 px Weichzeichnen), damit der Text der
Vordergrund bleibt. Alle Zahlen stehen in `data/gebaeude_motive.json`.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `6bb6714`, darauf dieser Schritt | `git log --oneline -1` |
| Vergleichsblatt | drei Fassungen, Daniel hat **B** gewaehlt; danach "zu blickfangend" -> Bild zurueckgenommen | `docs/design/HINTERGRUND_VERGLEICH_20261102.png`, `tools/hintergrund_vergleich.py` |
| Flaeche | `gebaeude_optik.hintergrund_flaeche` deckt (cover, mittig beschnitten), optional weichgezeichnet/abgedunkelt | `src/gebaeude_optik.py` |
| Textfelder | `gebaeude_optik.kasten_bild` (abgerundet, Verlauf oben 248 / unten 205, Goldrand), `main._kasten_label` | ebd., `src/main.py` |
| Daten | `ansicht_hintergrund`: abdunkeln 38 %, weichzeichnen 2 px, Radius 14, Farbe 22/17/12 | `data/gebaeude_motive.json` |
| Ansichten | Dorfzentrum (`lager`), Forschung (`bibliothek`), Kaserne/Stellmacher/Diebesgilde (je Gebaeude); `_gebaeude_kopf` nur Rueckfall | `src/main.py` |
| Wache | `tests/test_ansicht_hintergrund.py` **29/0/0**; `test_gebaeude_icons` umgestellt **56/0/0** | eigene Laeufe |
| Pruefdateien / Register | **132** / **139** | `ls tests/test_*.py`, `grep -c` |

## Der EINE naechste Schritt

**Truppenbewegungen auf der Weltkarte sichtbar machen** (Vorgabe Daniel 02.11.2026, Vorbild Lords
Mobile; in der Fragenrunde ausdruecklich **vor** die Demo gesetzt). Heute zeigt das Portal-Kaestchen
Gelaende und die fremden Doerfer, aber keinen Marsch.

**Sichtbarkeitsregel (Vorgabe Daniel, Register 140) - sie ist der Kern des Schritts:**
sichtbar sind Startfeld, Zielfeld, die Linie und eine **grobe** Restlaufzeit. NICHT sichtbar sind
Truppenart, Anzahl, Karren und Ausruestung ("Ein einzelner handkarren erzeugt das gleiche
bewegungssymbol wie eine ganze armee"), und die genaue Geschwindigkeit bleibt verborgen, damit sie
die Einheit nicht verraet ("sieht man nur die grobe Wegzeit"). **Ausnahme (Nachtrag Daniel): laeuft
ein Marsch auf eine EIGENE Siedlung zu, wird die Wegzeit GENAU genannt** - "weil ich selbst betroffen
bin und die zeiten einschaetzen kann als spieler"; Truppenart und Anzahl bleiben auch dann verborgen,
die Geschwindigkeitsstufe wird nicht ausgewiesen. **Ein marschierender Verband ist kein Spionageziel**
- Spionage zielt auf ein Dorf. Eigene Auftraege bekommen auf der Karte dieselbe Darstellung; ihre
Einzelheiten stehen im Auftragsbuch/Postfach.

Zu tun: je laufendem Auftrag eine Linie im Kaestchen (eigenes Zeichen-Tag, Muster `portalbote`),
Anzeige aus `state.auftraege` gespeist (keine zweite Auftragsliste), Restzeit in groben Stufen,
Klick auf eine Linie zeigt, was oeffentlich ist (von, nach, Restzeit) - keine Truppenliste;
Pruefdatei mit Grenzfaellen (kein Auftrag = keine Linie, Ankunft = Linie weg, zwei Marsche
gleichzeitig, Uhr rueckwaerts), voller Sammellauf, Protokollzeile, ein Commit.

**Vorgehen (Vorgabe Daniel 02.11.2026): diesen Schritt plant und baut das GROSSE MODELL
(deepseek-v4-pro)** - vor allem die visuelle Darstellung waehrend der Bewegung (Symbol, Linie,
Puls/Richtung, Groesse) soll es entwerfen, nicht nur den Code schreiben. Erst ein kurzes
Darstellungs-Papier mit zwei, drei Fassungen (Bild), dann umsetzen. Kosten im Blick behalten
(hart 4 EUR/Tag ueber alle Modelle), Kontostand vorher nennen.
Arbeitsweise: ein Schritt = ein Commit = ein gruener voller Sammellauf.

**Demo-Umfang ist eingefroren (Daniel 02.11.2026, Fragenrunde):** Kernkreis + Spionage + Voelker- und
Kartenwahl am Start. Alles andere kommt NACH dem ersten Demo-Upload.

**Danach in dieser Reihenfolge:** Kastenoptik in Kaserne/Stellmacher/Diebesgilde (Daniels Wahl), dann
die uebrigen Textfelder der Ansichten, dann Voelkerwahl am Start (A2), Kartenwahl fuer den SPIELER,
Volksboni verdrahten (A), Anschluss `botkern.oekonomie_kartenwahl`, Kopplung Punkte/Kanaele (C),
Balance-Messung (D), zuletzt Demo-Release (Freigabe Daniel).

# STAND 02.11.2026, 20:20 - Stufe B-5: Postfach und Spionage, gekoppelt an die Einheitenwerte (Register 138)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Es gibt jetzt ein Postfach mit Spionageberichten - und der Bericht haengt an den Einheiten.**
Wer ein fremdes Dorf ausspionieren will, schickt Kundschafter der Diebesgilde; ihre Werte
SI (Sinnesschaerfe) und HE (Heimlichkeit) ergeben den Aufklaerungswert, und der entscheidet, wie
viel der Bericht zeigt. Reicht die Aufklaerung nicht fuer den Wall, prallt der Auftrag ab: Verluste,
kein Bericht. Auf der Weltkarte stehen die fremden Doerfer jetzt als anklickbare Zeichen - ein Klick
bietet "Angriff planen" und "Spionage", beide fuehren in die Truppenauswahl.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `deeae88` (Arbeitsbaum leer), darauf dieser Schritt | `git log --oneline -1` |
| Neue Auftragsart | `spionieren` (fuenfte Art); nur fremdes Ziel, nur Spionageeinheiten, KEINE gemischte Truppe | `auftraege.py` |
| Aufklaerungswert | SI + HE je Einheit: Streuner 60, Gauner 95, Dieb 135, Meisterdieb 150, Kundschafter 175, Waldlaeufer 185; Kaempfer/Karren 0 | `spionage.aufklaerungswert`, `data/units.json` |
| Staffelung des Berichts | Truppen 25, Vorraete 50, Wall 75, Karte 100, Taktik 150 (VORSCHLAG) | `data/spionage.json` |
| Wall-Abwehr | Wallstufe x 20 x Zustand/100 (VORSCHLAG); abgewehrt = 50 % Verluste, kein Bericht | `spionage.abwehr_eines_dorfes`, `abwehr_pruefung` |
| Frist | **keine** - ein Bericht bleibt aktuell, bis ein neuer ueber dasselbe Dorf kommt (Vorgabe Daniel); er nennt seinen Stand und warnt, dass spaeter eintreffende Truppen fehlen | `data/spionage.json`, `spionage.bericht_zeilen` |
| Anzeige | Nachrichtentyp `spionage` (violett #A97BD6), Knopf "Spionagebericht oeffnen", eigener Veraltet-Hinweis | `main._render_messages`, `_spionage_bericht_anzeigen` |
| Weg im Fenster | Weltkarte (Portal-Kaestchen): fremde Doerfer als Zeichen, Klick -> Optionen -> Truppenauswahl; zweiter Einstieg Diebesgilde | `main._portal_klick`, `_bot_dorf_optionen`, `_truppen_auswahl` |
| Angriff auf ein Dorf | nimmt jetzt Wall und Wallzustand DIESES Dorfes | `main.kampf_am_ziel` (`ziel["dorf_name"]`) |
| Wache | `tests/test_spionage.py` **144/0/0**; drei Gegenproben wurden rot und die Dateien hashgleich zurueckgeschrieben | eigene Laeufe |
| Umgestellte alte Wachen | `test_auftraege` (vier -> fuenf Arten, "spionieren" war dort das Beispiel fuer eine unbekannte Art), `test_portal_uebersicht` (Klick laeuft ueber `_portal_klick`) | mit Begruendung im Kommentar |
| Voller Sammellauf | **129 von 131 gruen, 0 rot, 2 ausgesetzt, 5.131 Pruefungen, 287 s** (20:33) | `docs/audits/sammellauf_20261102_2027.log` |
| Pruefdateien / Register | **131** / **138** | `ls tests/test_*.py`, `grep -c` |

## Der EINE naechste Schritt

**Optik: die gemalten Gebaeudebilder werden der HINTERGRUND ihrer Ansicht, nicht ein Bild oben
drueber** (Vorgabe Daniel 02.11.2026, Screenshot in `docs/eingaben/20261102_Beispielansicht_Erklaerung_Hintergrund.png`).
Heute zeichnet `main._gebaeude_kopf` die Szene als 538 x 222 grosses Bild UEBER dem Inhalt
(Dorfzentrum, Bibliothek, Kaserne/Stellmacher/Diebesgilde). Richtig ist: die Szene liegt hinter dem
Inhalt und fuellt die Ansicht; die Textbloecke bleiben als kleine, DECKENDE Kaesten lesbar, dazwischen
bleibt das Bild sichtbar (Daniels Wortlaut: "kleinere textbloecke die nicht transparent sind und der
rest so transparent das moeglichst viel vom bild durchkommt"). Zu tun: eine Hintergrund-Ebene je
Ansicht, drei Fassungen als Vergleichsbild vorlegen (Vorgabe Daniel: Optik erst zeigen), Pruefdatei
fuer die Lesbarkeit der Textkaesten, voller Sammellauf, Protokollzeile, ein Commit.
Arbeitsweise: ein Schritt = ein Commit = ein gruener voller Sammellauf.

**Danach in dieser Reihenfolge:** Truppenbewegungen auf der Weltkarte sichtbar machen (Vorgabe Daniel
02.11.2026, Vorbild Lords Mobile - eigene und fremde Marsche mit Richtung und Restzeit), Voelkerwahl am
Start (A2, sechs Voelker), Volksboni verdrahten (A, 13 Wirkungen), Kartenwahl fuer den SPIELER beim
Gruenden, Anschluss `botkern.oekonomie_kartenwahl`, Kopplung Punkte/Kanaele (C), Balance-Messung (D).

# STAND 02.11.2026, 19:46 - Stufe B-4: die Karte bestimmt den Ertrag (Register 137)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Jedes Bot-Dorf traegt jetzt eine Karte, und die Karte bestimmt seinen Ertrag.** Der Kartenwert wird aus
den FELDERN der Karte und den belegten Ertraegen je Gebaeude und Gelaende gerechnet - der starke Rohstoff
traegt viel, die schwaecher produzierbaren wenig oder gar nichts. Gold ist der Engpass: von 127 Karten
traegt genau eine kein Gold.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `dd3e4ed` (Arbeitsbaum leer), darauf dieser Schritt | `git log --oneline -1` |
| Regel | `bot_karten_katalog`, `bot_kartenprofil`, `bot_kartenwahl`, `bot_doerfer_karten_zuweisen`, `bot_karten_uebersicht` | `src/main.py` |
| Traeger | `BotDorf.karte` (additiv; leer = alter Stand, bekommt die Karte beim ersten Bot-Takt) | ebd. |
| Kartenwahl | drei Kandidaten reproduzierbar aus Name und Dorfnummer, **Gold zuerst** (Daniel), Gleichstand ueber Gesamtwert und Kennung | `bot_kartenwahl` |
| Datendatei | `karten_aktiv`, `karten_teiler` 10 (VORSCHLAG), `karten_kandidaten` 3 | `data/bot_wirtschaft.json` |
| Gemessen | goldreichste Karte Gold 90 (original-001); **genau EINE Karte ohne Gold** (original-125); Werte je Rohstoff 0 bis 200 | Katalog + Profil |
| Wache | `tests/test_bot_kartenprofil.py` **37/0/0**; B-3-Wachen weiter gruen (52/0/0, 29/0/0, 33/0/0) | eigene Laeufe |
| Voller Sammellauf | **128 von 130 gruen, 0 rot, 2 ausgesetzt, 4.977 Pruefungen, 294 s** (19:18) | `docs/audits/sammellauf_20261102_1918.log` |
| Pruefdateien / Register | **130** / **137** | `ls tests/test_*.py`, `grep -c` |

## Der EINE naechste Schritt

**Postfach und Spionage** (Vorgabe Daniel, Vorbild Lords Mobile): der Spionageauftrag als eigene
Auftragsart, ein Bericht im Postfach, bezahlt aus Truppen, Gold und Reisezeit, und die Anzeige, die
Wallstufe, Taktik, Truppen, Items und Vorraete NUR dort zeigt. Die Schnittstellen stehen
(`bot_doerfer_uebersicht` offen, `bot_doerfer_spionagebericht` mit Karten- und Ertragsdaten); zu tun
sind der Auftrag, das Postfach und die Anzeige, eine Pruefdatei mit Grenzfaellen, ein voller
Sammellauf, eine Protokollzeile und ein Commit.
Arbeitsweise: ein Schritt = ein Commit = ein gruener voller Sammellauf.

**Danach in dieser Reihenfolge:** Voelkerwahl am Start (A2, sechs Voelker), Anschluss von
`botkern.oekonomie_kartenwahl` an die Bot-Wahl nach Stufe, Verdrahtung der 13 Volksboni (A), Kopplung
Punkte und Kanaele (C), Balance-Messung (D).

# STAND 02.11.2026, 18:42 - Gesamtkonzept formuliert, Baustein fuer GitHub (Register 136)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Das Gesamtkonzept steht als Dokument.** Der eine Absatz aus dem Konzept (K-1, Abschnitt 10) ist zu einem
ausformulierten Papier geworden: was das Spiel ist, woraus es rechnet, was aus welchem Vorbild kommt, und
was noch fehlt - dazu ein fertiger Text fuer die spaetere GitHub-Beschreibung. Vorgabe Daniel: erst
formulieren, dann zeigen.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `8c38228` (Arbeitsbaum leer), darauf dieser Schritt | `git log --oneline -1` |
| Dokument | `docs/GESAMTKONZEPT_20261102.md`, 11 Abschnitte, 9.493 Zeichen | `wc -c` |
| Kern | Inhalt aus Nebelseetal (Handbuch 2009), Raum aus Lords Mobile - nicht mehr und nicht weniger | Abschnitt 3 |
| Zahlen | 28 Einheiten, 17 Waren, 21 Forschungen, 127 Karten, 20 Dimensionen - jede mit Beleg abgezaehlt | Abschnitt 8 |
| Ehrlich offen | Kartenwahl je Gruendung, Voelkerwahl und 13 Volksboni, Spionage/Postfach, Bots gruenden nicht nach | Abschnitt 9 |
| GitHub-Text | About-Absatz plus README-Einstieg, fertig zum Einfuegen (noch NICHT veroeffentlicht) | Abschnitt 11 |
| Korrekturen Daniel (18:55) | **Doerfer werden NIE eingenommen** (nur angreifen, ausspionieren, ausraeumen); **Angriffstruppen nie am Zielort stationiert** (Angriff zu einem Zeitpunkt, dann Bericht, dann Rueckmarsch) | Abschnitte 1, 2, 4, 11; Konzept K-1 Abschnitt 10 |
| Voller Sammellauf | **127 von 129 gruen, 0 rot, 2 ausgesetzt, 4.940 Pruefungen, 309 s** (18:56) | `docs/audits/sammellauf_20261102_1856.log` |
| Dokumentpruefungen | `test_textqualitaet` **325/0** (96 Dokumente), `test_projektpfade` **105/0**, `test_protokoll` 22/0/1, `test_zieluebergabe` 26/0 | eigene Laeufe |
| Pruefdateien / Register | **129** / **136** | `ls tests/test_*.py`, `grep -c` |

## Der EINE naechste Schritt

**Kartenprofil je Bot-Dorf (Konzept Abschnitt 11, Vorgabe Daniel 02.11.2026): bei jeder Gruendung drei
Karten zur Wahl, die Karte bestimmt den maximal getragenen Rohstoff und die schwaecher produzierbaren,
Gold hat Vorrang; die Bots bilden diese Wahl ueber `botkern.oekonomie_kartenwahl` nach.** Zu tun: eine
Datendatei mit Kartenprofilen (starker, mittlere, schwacher Rohstoff), `bot_dorf_ertrag` liest das Profil
des Dorfes statt einer festen Rate, das Dorf haelt seine Karte, die Bot-Wahl bekommt ihren Aufrufer,
Pruefdatei mit Grenzfaellen, voller Sammellauf, Protokollzeile, ein Commit.
Arbeitsweise: ein Schritt = ein Commit = ein gruener voller Sammellauf.

**Danach in dieser Reihenfolge:** Postfach und Spionage (die Schnittstelle steht schon), Voelkerwahl am
Start (A2, sechs Voelker), Verdrahtung der 13 Volksboni (A), Kopplung Punkte und Kanaele (C),
Balance-Messung (D).

# STAND 02.11.2026, 18:21 - Protokoll geteilt: Historie geschlossen, neues Heft ab heute (Register 135)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Vorgabe Daniel 02.11.2026: das Protokoll laeuft in einem neuen Dokument weiter.** Es gibt jetzt zwei
Hefte - eines mit der Historie bis heute, eines ab heute. Die Historie ist WORTGLEICH uebernommen (nichts
gekuerzt, nichts umgeschrieben), das aktive Heft beginnt mit dem 02.11.2026 und steht wieder weit unter
der Zielgroesse.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `d05e5c4` (Arbeitsbaum leer), darauf dieser Schritt | `git log --oneline -1` |
| Geschichtsheft | `docs/ENTWICKLUNGSPROTOKOLL_HISTORIE_BIS_20261101.md` - **300 Zeilen**, geschlossen, wortgleich | `wc -l` |
| Aktives Heft | `docs/ENTWICKLUNGSPROTOKOLL.md` - **80 Zeilen** ab 02.11.2026 (KARTE-01/02, BOTDORF-01/02/03) | `wc -l` |
| Werkzeug | `tools/pruefe_protokoll.py`: 46 Commit-Kennungen, 0 unbekannt, **nichts verloren** gegen die Vor-Verdichtung | eigener Lauf |
| Wachen mitgezogen | `test_gpt_projektordnung` (ein aktives Heft + das Geschichtsheft), `test_protokoll` (Vollstaendigkeit gegen BEIDE), `test_gpt_portable_uebergabe`, `protokoll_sichern`, `projekt_ordnung_audit` | Quelltext der Wachen |
| Wache | `test_protokoll` **22/0/1**, `test_textqualitaet` **322/0** (95 Dokumente), `test_projektpfade` **105/0** | eigene Laeufe |
| Voller Sammellauf | **127 von 129 gruen, 0 rot, 2 ausgesetzt, 4.940 Pruefungen, 261 s** (18:16) | `docs/audits/sammellauf_20261102_1816.log` |
| Pruefdateien / Register | **129** / **135** | `ls tests/test_*.py`, `grep -c` |

## Der EINE naechste Schritt

**Das Gesamtkonzept ausformulieren (Vorgabe Daniel 02.11.2026).** Der Absatz in
`docs/KONZEPT_DORF_TAKTIKEN_20261102.md`, Abschnitt 10, ist der Keim: Nebelseetal liefert Einheiten,
Kampf, Gebaeude samt ihren Funktionen, Dorfgruendung und die Karten; Lords Mobile liefert ausschliesslich
das Springen auf Koordinaten und die Anzeige der Doerfer auf diesen Koordinaten. Daraus wird der Baustein
fuer die spaetere GitHub-Beschreibung - erst formulieren, dann zeigen.
Arbeitsweise: ein Schritt = ein Commit = ein gruener voller Sammellauf.

**Danach in dieser Reihenfolge:** Kartenprofil je Bot-Dorf (Konzept Abschnitt 11, Vorgabe Daniel vom
02.11.2026), Postfach und Spionage (Vorbild Lords Mobile), Voelkerwahl am Start (A2, sechs Voelker),
Verdrahtung der Volksboni (A), Kopplung Punkte und Kanaele (C), Balance-Messung (D).
**Hygiene:** erledigt - das Protokoll ist geteilt (Register 135); die alte Zeile im B-3-Block
(Protokoll auslagern) ist damit abgeloest.

# STAND 02.11.2026, 18:10 - Stufe B-3: Wirtschaft je Bot-Dorf (Register 134)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Die Bots wirtschaften.** Jedes Bot-Dorf hat ein eigenes Lager und erwirtschaftet je Stunde drei Anlagen
je Grundrohstoff; die Kasse eines Bots ist nur noch die SUMME seiner Doerfer. Ein Spielstand von vorher
laedt ohne Fehler und verliert nichts.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `4741076` (Arbeitsbaum leer), darauf dieser Schritt | `git log --oneline -1` |
| Regel | `bot_dorf_ertrag`, `bot_kasse`, `bot_kasse_setzen`, `bot_kasse_buchen`, `bot_doerfer_ernten` | `src/main.py` |
| Datendatei | `data/bot_wirtschaft.json` (Schalter, Anlagen je Dorf, Lagerdeckel 20.000) | ebd. |
| Ertrag | drei Anlagen je Grundrohstoff: **12 Holz / 12 Stein / 12 Nahrung / 9 Gold** je Stunde und Dorf (Daniel 02.11.2026) | `bot_dorf_ertrag` |
| Anzeige | Spionagebericht je Dorf mit Vorrat und Ertrag aus derselben Funktion; offene Uebersicht weiter ohne Vorrate | `bot_doerfer_spionagebericht` |
| Wache | `tests/test_bot_dorf_wirtschaft.py` **52/0/0** | eigener Lauf |
| Voller Sammellauf | **127 von 129 gruen, 0 rot, 2 ausgesetzt, 4.933 Pruefungen, 276 s** (18:04-18:08) | `docs/audits/sammellauf_20261102_1804.log` |
| Pruefdateien / Register | **129** / **134** | `ls tests/test_*.py`, `grep -c` |
| Offen | Kartenprofil je Dorf (Vorgabe Daniel, Konzept Abschnitt 11), Postfach/Spionage, Voelkerwahl (A2), Boni (A), Kopplung (C), Balance (D), Protokoll 344 Zeilen auslagern | Konzept K-1 |

## Der EINE naechste Schritt

**Das Gesamtkonzept ausformulieren (Vorgabe Daniel 02.11.2026).** Der Absatz in
`docs/KONZEPT_DORF_TAKTIKEN_20261102.md`, Abschnitt 10, ist der Keim: Nebelseetal liefert Einheiten,
Kampf, Gebaeude samt ihren Funktionen, Dorfgruendung und die Karten; Lords Mobile liefert ausschliesslich
das Springen auf Koordinaten und die Anzeige der Doerfer auf diesen Koordinaten. Daraus wird der Baustein
fuer die spaetere GitHub-Beschreibung - erst formulieren, dann zeigen.
Arbeitsweise: ein Schritt = ein Commit = ein gruener voller Sammellauf.

**Danach in dieser Reihenfolge:** Kartenprofil je Bot-Dorf (Konzept Abschnitt 11, Vorgabe Daniel vom
02.11.2026), Postfach und Spionage (Vorbild Lords Mobile), Voelkerwahl am Start (A2, sechs Voelker),
Verdrahtung der Volksboni (A), Kopplung Punkte und Kanaele (C), Balance-Messung (D). **Hygiene:** das
Protokoll steht mit 344 Zeilen ueber der Zielgroesse 320 - auslagern, nicht streichen.

# STAND 02.11.2026, 16:58 - Stufe B-2: Dorf-Verhalten aus der Lage (Register 133)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Die Doerfer haben jetzt ein Verhalten.** Jedes Bot-Dorf bekommt eine feste Position und waehlt
sein Verhalten aus vier Lagen (Naehe, Staerke, Wall, Niederlage) - als festes Paket, mit 48 Stunden
Sperrzeit. Die Wahl ist deterministisch, nichts wird gewuerfelt.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `98a9988` (Arbeitsbaum leer), darauf dieser Schritt | `git log --oneline -1` |
| Regel | `bottaktik.dorf_position`, `TAKTIK_GEWICHTE`, `dorf_taktik_bewerten/waehlen/setzen` | `src/bottaktik.py` |
| Bruecke | `GameState.bot_doerfer_auffrischen` im Bot-Takt eingehaengt | `src/main.py` |
| Anzeigegrenze | offen: Name, Position, Fraktion, Volkswerte - Taktik UND Wallstufe nur im Spionagebericht | `bot_doerfer_uebersicht` / `bot_doerfer_spionagebericht` |
| Wache | `tests/test_dorf_taktiken.py` **33/0/0** | eigener Lauf |
| Voller Sammellauf | **126 von 128 gruen, 0 rot, 2 ausgesetzt, 4.883 Pruefungen, 299 s** (16:51-16:56) | `docs/audits/sammellauf_20261102_1651.log` |
| Pruefdateien / Register | **128** / **133** | `ls tests/test_*.py`, `grep -c` |
| Offen | Wirtschaft je Dorf (B-3), Postfach/Spionage, Voelkerwahl (A2), Boni verdrahten (A) | Konzept K-1 |

## Der EINE naechste Schritt

**Stufe B-3: die Wirtschaft je Dorf.** Bisher ist der Vorrat des Bots EINE Kasse; je Dorf eigene
Vorraete, Erträge und Wall. Zu tun: eine Lesestelle fuer den Dorf-Ertrag (Kern und Anzeige aus
derselben Funktion), die Bot-Kasse als Summe der Doerfer (keine zweite Buchfuehrung), Migration
alter Spielstaende ueber die Vorgabewerte von `BotDorf`, Pruefdatei mit Grenzfaellen, voller
Sammellauf, Protokollzeile, ein Commit.
Arbeitsweise: ein Schritt = ein Commit = ein gruener voller Sammellauf.

**Danach in dieser Reihenfolge:** Postfach und Spionage (Vorbild Lords Mobile, Vorgabe Daniel),
Voelkerwahl am Start (A2, sechs Voelker), Verdrahtung der Volksboni (A), Kopplung Punkte/Kanaele
(C), Balance-Messung (D). **Hygiene:** das Protokoll steht mit 334 Zeilen ueber der Zielgroesse 320
- auslagern, nicht streichen.

# STAND 02.11.2026, 17:15 - Stufe B-1: Bots tragen Doerfer (Register 132)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Die Voraussetzung fuer Dorf-Taktiken steht.** Jeder Bot traegt jetzt je Dorf einen eigenen
Datensatz (Taktik-Slot, Wall, Ausbauzaehler); die Doerfer entstehen aus den bisherigen
Siedlungsnamen, das erste ist das Hauptdorf. Ein alter Spielstand laedt ohne Ausnahme und verliert
nichts.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `74587fb` (Arbeitsbaum leer), darauf dieser Schritt | `git log --oneline -1` |
| Neu | `main.BotDorf`, `BotPlayer.doerfer`, `bot_doerfer_sicherstellen`, `bot_aus_stand` | `src/main.py` |
| Eingetragen | Kartenaufbau (`generate_map`) und Spielstand-Laden | beide Stellen im Quelltext |
| Wache | `tests/test_bot_doerfer.py` **27/0/1** (Befund = bewusster Zwischenstand) | eigener Lauf |
| Nebenbefunde | `test_s7_botverhalten` 45/0/0, `test_gpt_bot_angriffsplanung` 16/16 OK | eigene Laeufe |
| Voller Sammellauf | **125 von 127 gruen, 0 rot, 2 ausgesetzt, 4.850 Pruefungen, 284 s** (17:14-17:22) | `docs/audits/sammellauf_20261102_1714.log` |
| Pruefdateien / Register | **127** / **132** | `ls tests/test_*.py`, `grep -c` |
| Offen (bewusst) | Dorf-Vorraete sind noch NICHT fuehrend; Wirtschaft je Dorf = B-3 | Befund in der Wache |

## Der EINE naechste Schritt

**Stufe B-2: jedem Bot-Dorf eine Position auf der Karte und einen fuellbaren Taktik-Slot geben**
(Konzept `docs/KONZEPT_DORF_TAKTIKEN_20261102.md`, Abschnitte 2 und 4): die Wahlregel fuers Verhalten
aus der Lage ableiten (Naehe zum Spieler, eigene Staerke, Wallzustand, letzte Niederlage), Sperrzeit
beachten, die Wahl deterministisch aus dem Seed ziehen und die Taktik-Tabelle je Fraktion als
Datendatei anlegen. Danach B-3 (Wirtschaft je Dorf) und erst dann die Kopplung an die Volksboni.
Zu tun: Werte in `data/` (keine Literale im Code), Pruefdatei mit Grenzfaellen, voller Sammellauf,
Protokollzeile, ein Commit.
Arbeitsweise: ein Schritt = ein Commit = ein gruener voller Sammellauf.

**Offen ausserdem:** das Protokoll steht mit 325 Zeilen ueber der Zielgroesse 320 - nach Daniels
Regel wird AUSGELAGERT (nicht gestrichen); das gehoert in den Aufraeumschritt (Punkt 9). Die Anzeige
der Doerfer im Spiel und die Voelkerwahl (Stufe A2) folgen nach B.

# STAND 02.11.2026, 16:00 - Leisten-Luecken gedeckelt (Register 131)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Punkt 3 des Ablaufplans ist erledigt.** Die Ressourcenleiste streckt ihre Luecken nicht mehr
beliebig: die Dehnung ist auf 1,35 gedeckelt, bei Bedarf waechst das ganze Band gleichmaessig
(treue Vergroesserung ohne Naht), ein Rest wird symmetrisch verteilt.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `f7f2a51` (Arbeitsbaum leer), darauf dieser Schritt | `git log --oneline -1` |
| Befund vorher | Lueckendehnung **1,86** bei 2560 px, 2,81 bei 3000, **3,75** bei 3440 | eigene Messung an `leiste_zusammensetzen` |
| Werte | `luecke_max` 1,35, `skala_hart` 1,75, `rest_auffuellen` gleichmaessig | `data/ressourcenleiste.json` |
| Nachher | 1440-2320 px fuellen ganz, 2560 px Skala 1,653 (fuellt genau), 3440 px Raender 367/367 | eigene Messung, `tests/test_leisten_luecken.py` 22/0/0 |
| Umgestellte Wachen | `test_ressourcenleiste.py` **41/0/1**: Skala waechst bis `skala_hart`; Symbolfeld seitengetreu statt pixelgleich | eigener Lauf, Begruendung im Test |
| Sichtvergleich | `docs/audits/leisten_vergleich_20261102.png` (ALT/NEU, 2560 und 3440) | `tools/leisten_vergleich.py` |
| Voller Sammellauf | **124 von 126 gruen, 0 rot, 2 ausgesetzt, 4.824 Pruefungen, 541 s** (15:13-15:22) | `docs/audits/sammellauf_20261102_1513.log` |
| Pruefdateien / Register | **126** / **131** | `ls tests/test_*.py`, `grep -c` |

## Der EINE naechste Schritt

**Punkt 6: S-8-Bilanz und `weltkarten_seed` festschreiben** (Freigabe Daniels 02.11.2026, Register 93
und 94): der Weltensprung kostet **500 Mana plus 100 Gold** statt der heute gebuchten 5.000 Mana - der
belegte Originalwert 5.000 bleibt als Beleg und Konfigurationswert daneben stehen, nichts wird
geloescht -, und `weltkarten_seed` bekommt fuer die Demo einen FESTEN Wert in `data/welten.json`.
Zu tun: die eine Buchungsstelle des Sprungs umstellen (Kern UND Anzeige lesen denselben Wert), den
Belegwert unangetastet lassen, Seed setzen, je eine Pruefdatei mit Grenzfaellen (-1 / 0 / exakt Soll /
+1), voller Sammellauf, Protokollzeile, ein Commit.
Arbeitsweise: ein Schritt = ein Commit = ein gruener voller Sammellauf.

**Bei Daniel liegt** weiterhin Punkt 2 (Bilder im Fenster abnehmen, 10 Minuten) und die
Wappen-Zuordnung (Punkt 4). **Punkt 5** (Volksattribute und Verhaltensboni) wird seit 15:25 vom
STARKEN MODELL (deepseek-v4-pro) entworfen und umgesetzt - das GPT-Chat-Abo ist beendet, sein
Auftragspaket ist vom Desktop genommen und liegt weiter als Datei unter `docs/auftraege/`.

# STAND 02.11.2026, 13:50 - Auswahlrahmen der C2-Lieferung gezeichnet (Register 130)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Der Auswahlrahmen ist erledigt.** Auf dem gewaehlten Feld der Siedlungskarte liegt jetzt das
GELIEFERTE Bild `kachelrahmen_auswahl.png` voll deckend; der gezeichnete goldene Rahmen aus
`karten_optik_fein.auswahl_plan_fein` wird nur noch als Rueckfall gezeichnet, wenn das Bild fehlt.
Damit ist Punkt 1 des Ablaufplans aus der Uebergabe abgeschlossen.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `fe4ed27` (Arbeitsbaum leer), darauf dieser Schritt | `git log --oneline -1`, `git status --porcelain` |
| Neu | Auswahlrahmen = geliefertes Bild, Bildobjekt in Durchgang 4 (zuletzt) | Register 130, `src/main.py` `_zeichne_siedlungskarte` |
| Deckkraft | Auswahl **100** Prozent (`kachelrahmen.deckkraft_auswahl_prozent`, neu), Ruhe **35** (`deckkraft_prozent`) | `data/gebaeude_motive.json`, am Bildcache gemessen |
| Wache | `tests/test_auswahlrahmen_c2.py` **17/0/0**; Gegenprobe mit abgeschaltetem Bildzweig **12/2** | eigener Lauf |
| Umgestellte Wache | `tests/test_startspiel.py` **62/0/1**: genau EIN Auswahlrahmen (Bild ODER gezeichnet), vorher 6 gezeichnete | eigener Lauf |
| Sichtvergleich | `docs/audits/auswahlrahmen_vergleich_20261102.png` (1986 x 720, drei Fassungen, echte Zeichenflaeche) | `tools/auswahlrahmen_vergleich.py` |
| Voller Sammellauf | **123 von 125 gruen, 0 rot, 2 ausgesetzt, 4.800 Pruefungen, 294 s** (13:45-13:50, auf dem ENDSTAND nach allen Dokumentzeilen) | `docs/audits/sammellauf_20261102_1345.log` |
| Pruefdateien / Register | **125** / **130** | `ls tests/test_*.py`, `grep -c` |
| Offen an Daniel | Auswahlrahmen wirkt auf dem Kontaktblatt wuchtiger als der gezeichnete - Deckkraft 100 oder z. B. 70? | `docs/FRAGEN_AN_DANIEL_20261102_1345.md` |

## Der EINE naechste Schritt

**Leisten-Luecken bei sehr breiten Fenstern schliessen** (Punkt 3 des Ablaufplans, Uebergabe
Abschnitt 4): die Landschaft wiederholt sich in der Ressourcenleiste, wenn das Fenster breiter wird.
Zu tun: mit zwei weiten Fensterbreiten messen (`main._leisten_stuecke` / `main.leiste_zusammensetzen`),
die Lueckenstuecke so bauen, dass Ecken und Symbolfelder pixelgleich bleiben und nur die Luecken
dehnen, eine Wache mit zwei Breiten ergaenzen, Sichtvergleich als Kontaktblatt unter `docs/audits/`,
danach voller Sammellauf, Protokollzeile und ein Commit.
Arbeitsweise: eine Pruefdatei je Bedingung, voller Sammellauf, Protokollzeile, ein Commit.

**Bei Daniel liegt** Punkt 2 (Bilder im Fenster abnehmen: Icons, Bauknoepfe, Hintergrund, Leiste,
10 Minuten) und die Zuordnung der Wappen zu den fuenf Bots (Punkt 4); Freigaben brauchen Punkt 5
und 6. Der Restweg bis zur Demo bleibt bei etwa 6-8 Arbeitstakten.

# STAND 02.11.2026, 11:31 - SITZUNGSENDE: Laptop-Neustart (WLAN, Tastatur)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Sitzung beendet, nicht angehalten** (WLAN bricht ab, Tastatur haengt): alle Hintergrundprozesse
sind beendet, das Spiel ist geschlossen, der Arbeitsbaum ist leer, die drei offenen
Skill-Einreihungen sind verworfen - **nichts ist ungespeichert.**
Uebergabe fuer die naechste Sitzung: `docs/UEBERGABE_20261102_1115.md` (Kopie auf dem Desktop,
hashgleich). Der Ablaufplan bis zur Demo steht dort Abschnitt 4.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf | `5a2f119`, Arbeitsbaum **leer** | `git status --porcelain` |
| Letzter Sammellauf | **122 von 124 gruen, 0 rot, 4.783 Pruefungen, 420 s** (10:25) | `docs/audits/sammellauf_20261102_1025.log` |
| Start | `.venv` mit Pillow 13.0.0, alte py-Kette als Rueckfall | `tests/test_start_mit_pillow.py` 10/0/0 |
| Restweg Demo | **6-8 Arbeitstakte**, davon 2 mit Daniels Freigabe | Uebergabe Abschnitt 4 |

## Der EINE naechste Schritt

**Den Auswahlrahmen der C2-Lieferung zeichnen** (Uebergabe Abschnitt 3): messen, wer zuletzt zeichnet
(`_zeichne_siedlungskarte`), den gezeichneten goldenen Rahmen nur als Rueckfall benutzen, den
gelieferten `kachelrahmen_auswahl.png` mit voller Deckkraft auf das gewaehlte Feld legen,
Sichtvergleich als Kontaktblatt unter `docs/audits/`, Wache ergaenzen, voller Sammellauf,
Protokollzeile, ein Commit.
Arbeitsweise: Pruefdatei ergaenzen, voller Sammellauf, Protokollzeile, ein Commit.

# STAND 02.11.2026, 10:32 - Start mit Projekt-venv: Pillow da, Bilder scharf (Register 129)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `2f043dc` (Protokoll 291 Zeilen); dieser Commit bringt venv, Batch und die neue Wache | `git log --oneline -1` |
| venv | `.venv` = Astral CPython 3.11.16 + **Pillow 13.0.0**, `import tkinter, PIL` geprueft | `.venv/Scripts/python.exe -c "import PIL;print(PIL.__version__)"` |
| Start-Batch | nimmt zuerst `%~dp0.venv\Scripts\python.exe` (mit tkinter+Pillow-Pruefung), alte Kette bleibt Rueckfall | `START_SPIEL_WINDOWS.bat` |
| Im venv gemessen | Menue-Icon vorhanden, **Leistenbild vorhanden**, Hintergrund 538 x 222 | eigener Lauf, 10:22-10:32 |
| Neue Wache | `tests/test_start_mit_pillow.py` **10/0/0** (Reihenfolge im Batch, Rueckfall, venv-Import, gitignore) | eigener Lauf |
| Sammellauf | **122 von 124 gruen, 0 rot, 420 s** | `docs/audits/sammellauf_20261102_1025.log` |
| Aufgeraeumt | Python 3.15.2 unter `AppData\Local\Python` entfernt (122 MB, `py -0p` kannte es nicht) | `du -sh`, `ls` |
| Register / Pruefdateien | **129 Punkte**, **124 Pruefdateien** | `grep -cE`, `ls tests/test_*.py \| wc -l` |

## Der EINE naechste Schritt

**Auswahlrahmen der C2-Lieferung zeichnen** - `kachelrahmen_auswahl.png` steht in
`data/gebaeude_motive.json` und wird geladen, aber der gezeichnete goldene Rahmen aus
`karten_optik_fein` liegt darueber. Zu tun: messen, wer zuletzt zeichnet (`_zeichne_siedlungskarte`),
den gezeichneten Rahmen nur als Rueckfall benutzen, den gelieferten Auswahlrahmen mit voller Deckkraft
auf das gewaehlte Feld legen, Sichtvergleich als Kontaktblatt unter `docs/audits/`, Wache in
`tests/test_gebaeude_motive.py` oder eigener Datei, voller Sammellauf, Protokollzeile, ein Commit.
Arbeitsweise: Pruefdatei ergaenzen, voller Sammellauf, Protokollzeile, ein Commit.

## Reihenfolge danach

1. Icons und Hintergrund im Fenster abnehmen - drei Bilder unter `docs/audits/gebaeude_icons_fenster_*`
   (jetzt mit scharfen Bildern, weil das venv Pillow hat).
2. Wappen den fuenf Bots zuordnen; Burgen zu Weltkarten nur als gekennzeichneter Vorschlag.
3. S-8 Bilanz (500 Mana + 100 Gold, Register 93), danach `weltkarten_seed` fest (Register 94).
4. Demo-Gates G-01..G-07 vor jedem Upload; die Demo wird LEER ausgeliefert.
5. **EXE ist vom 01.11. 19:01** - vor einer Demo neu bauen und startgeprueft starten.

## Fallstricke, in diesem Schritt belegt

- **Ein `.bat` mit `%`-Pfaden und doppelten Marken ist empfindlich: Anker auf `\r\n:marke\r\n` setzen.**
  Ein `replace(':start_astral\r\n', ...)` traf zuerst das `goto :start_astral` MITTEN in der
  if-Kette und zerlegte das Batch. Erst der Anker mit fuehrendem Zeilenumbruch trifft die Marke.
  Vor dem Schreiben sichern und die Marken danach zaehlen (hier: vier Startmarken, jede mit `goto :ende`).
- **Ein venv ohne Pillow-Pruefung waere schlimmer als keins:** das Batch prueft `import tkinter, PIL`,
  bevor es dem venv traut - sonst startet ein halbfertiges venv und die Bilder fehlen wieder still.
- **`.venv` gehoert in `.gitignore` und NICHT ins Paket.** Sonst wandern 50+ MB Fremddateien ins Repo
  oder in die Demo; `git check-ignore -q .venv` ist die Wache dafuer.

# STAND 02.11.2026, 10:21 - Protokoll 291 Zeilen, Detailzeilen ausgelagert (Register 128)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `23f579f` (Verdichtung verworfen); dieser Commit loest sie strukturell | `git log --oneline -1` |
| Ergebnis | **291 Zeilen** statt 469, Ziel unter 320 erreicht - **ohne** Umformulierung | `wc -l docs/ENTWICKLUNGSPROTOKOLL.md` |
| Detaildokument | `docs/PROTOKOLL_DETAIL_2026-10.md`: 05.10. Tag 2 (87 Zeilen) und 31.10. UMSETZUNG-02 (97 Zeilen) wortgleich, 192 Zeilen | `wc -l` |
| Verlustpruefung | 46 Kennungen, **0 unbekannt**, alle Pruefzahlen der 02.11.-Sicherung vorhanden (Protokoll + Detail) | `tools/pruefe_protokoll.py` |
| Dokumentpruefungen | `test_protokoll` **16/0/1** (Zielgroessen-Befund weg), `test_textqualitaet` **307/0** (90 Dokumente), `test_projektpfade` 105/0, `test_zieluebergabe` 26/0 | eigener Lauf |
| Register / Pruefdateien | **128 Punkte**, **123 Pruefdateien** | `grep -cE`, `ls tests/test_*.py \| wc -l` |

## Der EINE naechste Schritt

**Projekt-venv mit Pillow anlegen und `START_SPIEL_WINDOWS.bat` darauf umstellen** (Daniels Entscheidung
02.11.2026, 10:2x): der Startpfad (Astral CPython 3.11.16) hat kein Pillow, deshalb fehlen
Ressourcenleiste und alle Bilder in voller Qualitaet. Zu tun: `.venv` mit derselben Python-Version
anlegen (`uv venv --python <3.11.16>`), `pillow` hinein, im Batch ZUERST `.venv\Scripts\pythonw.exe`
versuchen und die bisherige Kette als Rueckfall lassen; Waage: `python -c "import PIL"` im venv,
Startprobe aus dem Batch, `.venv` in `.gitignore` und im EXE-Bau ausgeschlossen; danach voller
Sammellauf, Protokollzeile, ein Commit.
Arbeitsweise: Pruefdatei ergaenzen, voller Sammellauf, Protokollzeile, ein Commit.

## Offen

1. **Auswahlrahmen** der C2-Lieferung zeichnen (naechster Fachschritt danach).
2. Icons/Hintergrund im Fenster abnehmen - drei Bilder unter `docs/audits/gebaeude_icons_fenster_*`.
3. **Python 3.15.2** in `AppData\Local\Python` entfernen (Daniel hat zugestimmt).
4. Wappen den fuenf Bots; Burgen zu Weltkarten nur als Vorschlag.
5. S-8 Bilanz (Register 93), `weltkarten_seed` fest (Register 94).
6. Demo-Gates G-01..G-07; Demo wird LEER ausgeliefert. **EXE vom 01.11. 19:01** - vor einer Demo neu bauen.

## Fallstricke, in diesem Schritt belegt

- **Auslagern ist die ehrliche Verdichtung.** Ein Wortlaut, der in eine eigene Datei wandert, ist
  nicht verloren; ein Wortlaut, den ein Modell zu Stichworten verkuerzt, ist es. Wenn eine Zielgroesse
  drueckt: verschieben, nicht zusammenstreichen.
- **Die Projektpruefung vergleicht gegen die Fassung vom 05.10., nicht gegen gestern.** Wer gegen
  gestern pruefen will, braucht die eigene Sicherung - und muss Protokoll UND Detaildokument addieren,
  sonst meldet er falschen Verlust (genau das faengt das Schreibskript vorher ab).
- **Summenzeilen brauchen die Kennungen IM Text.** Wandern Zeilen in ein Detaildokument, muessen ihre
  Kennungen und Pruefzahlen in der Summenzeile mitreisen, sonst wird `test_protokoll` rot, obwohl
  nichts verloren ist.

# STAND 02.11.2026, 10:15 - Protokoll-Verdichtung verworfen, Weg ist strukturell (Register 127)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `f7be01c` (Kaserne-Fix); dieser Commit bringt nur Dokumente (Register 127) | `git log --oneline -1` |
| Versuch | Protokoll 468 -> Ziel 320 Zeilen, `deepseek-v4-pro`, abschnittsweise | Register 127 |
| Ergebnis | 287 Zeilen, alle 45 Kennungen echt, alle Pruefzahlen da - **aber Tabellenzeilen zu Stichwortketten zusammengezogen**; zwei echte Verluste (`954097a`, `777 / 300 / 21`), 44 von 86 Absatz-Anfaengen weg | `tools/pruefe_protokoll.py --nach` + eigener Vergleich gegen die 02.11.-Sicherung |
| Entscheidung | **verworfen**; `docs/ENTWICKLUNGSPROTOKOLL.md` bleibt bei 468 Zeilen, Sicherung `9445ad7` ist wieder Ist-Stand | dieser Commit |
| Verbrauch starkes Modell | 82.917 Prompt- / 77.967 Antwort-Token (rund 65.000 Denken) in drei Abschnittsaufrufen; zwei Abbrueche mit je rund 60.000 Prompt-Token; Kosten noch nicht abgelesen | `usage`-Zeilen im Lauf-Log |
| Register / Pruefdateien | **127 Punkte**, **123 Pruefdateien** | `grep -cE`, `ls tests/test_*.py \| wc -l` |

## Der EINE naechste Schritt

**Auswahlrahmen der C2-Lieferung zeichnen** - der gelieferte `kachelrahmen_auswahl.png` liegt schon in
`data/gebaeude_motive.json` und wird geladen, aber der gezeichnete goldene Rahmen aus
`karten_optik_fein` liegt darueber, sodass die Lieferung nicht wirkt. Zu tun: messen, wer zuletzt
zeichnet (`_zeichne_siedlungskarte`), den gezeichneten Rahmen nur als Rueckfall benutzen (ohne Pillow),
den gelieferten Auswahlrahmen mit voller Deckkraft auf das gewaehlte Feld legen, Sichtvergleich als
Kontaktblatt (`docs/audits/`), Wache in `tests/test_gebaeude_motive.py` oder eigener Datei, voller
Sammellauf, Protokollzeile, ein Commit.
Arbeitsweise: Pruefdatei ergaenzen, voller Sammellauf, Protokollzeile, ein Commit.

## Offene Entscheidungen fuer Daniel (gesammelt, EINE Runde)

1. **Pillow in die Spiel-Laufzeit?** Der Startpfad (Astral CPython 3.11.16) hat keines; `uv pip install`
   ist dort gesperrt (`externally managed`). Empfehlung: Projekt-venv mit Pillow anlegen und
   `START_SPIEL_WINDOWS.bat` darauf umstellen (dann sind Leiste, Motive und Icons scharf) - Alternative:
   alles beim Tk-Rueckfall lassen (sichtbar, aber groeber).
2. **Ressourcenleiste ohne Pillow** loesen (Kachelbau mit Tk-Mitteln) - nur noetig, wenn Punkt 1 nicht
   kommt.
3. **Protokoll-Struktur**: Detailzeilen des 05.10. und 31.10. nach `docs/PROTOKOLL_DETAIL_2026-10.md`
   auslagern, im Protokoll Summenzeile + Verweis. Das ist der einzige Weg unter 320 Zeilen, der nichts
   weglaesst.
4. **Python 3.15.2** in `AppData\Local\Python` (122 MB, vom Python-Manager ungefragt geladen) entfernen.

## Reihenfolge danach

1. Auswahlrahmen (naechster Schritt).
2. Icons und Hintergrund im Fenster abnehmen - drei Bilder unter `docs/audits/gebaeude_icons_fenster_*`.
3. Wappen den fuenf Bots zuordnen; Burgen zu Weltkarten nur als gekennzeichneter Vorschlag.
4. S-8 Bilanz (500 Mana + 100 Gold, Register 93), danach `weltkarten_seed` fest (Register 94).
5. Demo-Gates G-01..G-07 vor jedem Upload; die Demo wird LEER ausgeliefert.
6. **EXE ist vom 01.11. 19:01** - vor einer Demo neu bauen und startgeprueft starten.

## Fallstricke, in diesem Schritt belegt

- **Ein starkes Modell kuerzt dort, wo es am billigsten ist - nicht dort, wo es am wenigsten kostet.**
  Zeilen zusammenzuziehen ist einfach, Text zu verdichten ist Arbeit. Deshalb: die Zusage "keine Zahl
  verloren" ist NICHT die Zusage "kein Inhalt verloren". Gegenprobe muss immer der Sinn sein, nicht nur
  der Zahlenabgleich.
- **Ein 230.000-Zeichen-Auftrag mit 100.000 Zeichen Antwort passt in keinen einzelnen Aufruf.** Der
  erste Versuch endete nach 300 s Socket-Timeout, der zweite mit 0 Zeichen (Denken frisst `max_tokens`).
  Abschnittsweise arbeiten ist richtig - aber je Abschnitt mit der Regel "eine Zeile je Schritt",
  sonst entstehen Stichwortketten.
- **`vorher` heisst vorher sichern UND pruefen, wogegen man nachher vergleicht:** die Projektpruefung
  vergleicht gegen die Fassung vom 05.10., nicht gegen die von heute. Fuer echte Vollstaendigkeit
  selbst gegen die 02.11.-Sicherung vergleichen (dieser Schritt hat es getan und zwei Verluste
  gefunden, die die Projektpruefung nicht sieht).

# STAND 02.11.2026, 09:51 - Kaserne-Ansicht ohne Gebaeude abgesichert (Register 126)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `97fa2aa` (Pillow-Rueckfall); dieser Commit bringt den KeyError-Fix, Register 126 und die neue Pruefdatei | `git log --oneline -1` |
| Befund | `Kaserne` steht im Menue, sobald die Akademie auf IRGENDEINER Siedlung steht; die Ansicht liest aber die AKTIVE Siedlung - ohne Gebaeude dort `KeyError: 'guenstigste'` | nachgestellt, Wache `test_kaserne_ohne_gebaeude` |
| Fix | Fruehfall von `spieloekonomie.siedler_reserve` liefert dieselben Schluessel wie der Normalfall (`engste`, `guenstigste`, `teuerste`) | `grep -n "guenstigste" src/spieloekonomie.py` |
| Neue Pruefdatei | **11 von 11 gruen**; Gegenprobe mit dem alten Stand: **6 Fehler** inkl. `KeyError('guenstigste')`, Datei-Hash danach wieder gleich | eigener Lauf |
| Sammellauf | **121 von 123 gruen, 0 rot, 2 ausgesetzt, 4.767 Pruefungen, 407 s** (09:44-09:51) | `docs/audits/sammellauf_20261102_0944.log` |
| Register / Pruefdateien | **126 Punkte**, **123 Pruefdateien** | `grep -cE`, `ls tests/test_*.py \| wc -l` |
| Irrweg | die Protokoll-Sicherung lag in `docs/` - `test_gpt_projektordnung_20261028` verlangt dort GENAU EINE aktive Protokolldatei; jetzt in `archiv/dokumentation/protokoll_alte_fassungen/`, hashgleich (`9116a9ab`) | eigener Lauf, 09:43 |
| Guthaben | Daniel 09:07: **8,25 USD** Kontostand, **41,74 USD** Gesamtverbrauch; Tagesbudget starkes Modell **3 USD** | Daniel, 09:07 |
| Offen (Freigabe) | Pillow in die Spiel-Laufzeit / Projekt-venv; Ressourcenleiste ohne Pillow; das ungenutzte Python 3.15.2 (122 MB) entfernen | eigene Messung |

## Der EINE naechste Schritt

**Das Entwicklungsprotokoll verdichten** (466 Zeilen, Regel: unter 320) - die unveraenderte Fassung
ist als `9445ad7` committed und liegt zusaetzlich in
`archiv/dokumentation/protokoll_alte_fassungen/ENTWICKLUNGSPROTOKOLL_VOR_VERDICHTUNG_20261102.md`
(hashgleich `9116a9ab`). Der starke Modellaufruf (deepseek-v4-pro) schreibt eine NEUE Datei
ausserhalb des Projekts; sie wird erst uebernommen, wenn `tools/pruefe_protokoll.py --nach <datei>`
Rueckgabe 0 liefert, alle 46 Commit-Kennungen mit `git cat-file -e` existieren und alle 205
Pruefzahlen wieder vorkommen. Danach: neue Fassung einsetzen, Zwischendatei entfernen,
Protokollzeile ueber die Verdichtung selbst, voller Sammellauf, ein Commit.
Arbeitsweise: Pruefdatei ergaenzen, voller Sammellauf, Protokollzeile, ein Commit.

## Reihenfolge danach

1. **Pillow-Entscheidung** (Daniel): Projekt-venv mit Pillow und Start-Batch darauf; danach die
   Ressourcenleiste ohne Pillow als Rueckfall.
2. Icons und Hintergrund im Fenster abnehmen - drei Bilder unter `docs/audits/gebaeude_icons_fenster_*`.
3. Auswahlrahmen der C2-Lieferung; die acht Einzelsymbole aus `assets/icons/leiste/symbole/` ungenutzt.
4. Wappen den fuenf Bots zuordnen; Burgen zu Weltkarten nur als gekennzeichneter Vorschlag.
5. S-8 Bilanz (500 Mana + 100 Gold, Register 93), danach `weltkarten_seed` fest (Register 94).
6. Demo-Gates G-01..G-07 vor jedem Upload; die Demo wird LEER ausgeliefert.
7. **EXE ist vom 01.11. 19:01** - vor einer Demo neu bauen und startgeprueft starten.

## Fallstricke, in diesem Schritt belegt

- **Ein Fruehfall muss ALLE Schluessel der Funktion liefern.** Der abgekuerzte `return` in
  `siedler_reserve` sparte zwei Felder, und der Anzeigecode griff genau eines davon. Wache dafuer ist
  der Vergleich der Schluesselmengen zweier echter Faelle - nicht das Nachbauen einer Wunschliste.
- **Ein Test, der nach dem Namen einer DATEI sucht, bricht bei jeder zweiten Fassung.** Die
  Protokoll-Sicherung gehoert nach `archiv/dokumentation/protokoll_alte_fassungen/`, NICHT nach
  `docs/` (dort erlaubt `test_gpt_projektordnung_20261028` nur `ENTWICKLUNGSPROTOKOLL.md`).
- **`git rm` vor dem Kopieren pruefen:** erst Hash der Kopie vergleichen, dann entfernen - die
  Fassung steckt zusaetzlich im Commit `9445ad7`.

# STAND 02.11.2026, 09:29 - Gebaeude-Optik sichtbar auch ohne Pillow (Register 125)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `bfed4de` (Icons eingebaut); dieser Commit bringt den Pillow-Rueckfall, Register 125 und die Fensterbilder | `git log --oneline -1` |
| Befund | Startpfad (`START_SPIEL_WINDOWS.bat`, Astral CPython 3.11.16) hat **kein Pillow**: vorher `Menue-Knoepfe mit Bild: []`, `leiste_zusammensetzen -> None` | eigene Messung mit genau diesem Interpreter, 09:10 |
| Nach dem Fix | mit demselben Interpreter: Menue-Icon **20 px**, Hintergrund **538 x 222** | eigene Messung, 09:20 |
| Pruefdatei | **56 von 56 gruen** (zwei neue Wachen: Pillow fuer zwei Aufrufe abgeschaltet) | eigener Lauf |
| Sammellauf | **120 von 122 gruen, 0 rot, 2 ausgesetzt, 4.761 Pruefungen, 401 s** (09:21-09:28) | `docs/audits/sammellauf_20261102_0921.log` |
| Fensterbilder | Dorfzentrum, Bauauswahl, Forschung - echte Oberflaeche mit eigenem Testspielstand | `docs/audits/gebaeude_icons_fenster_*_20261102.png` |
| Register / Pruefdateien | **125 Punkte**, **122 Pruefdateien** | `grep -cE`, `ls tests/test_*.py \| wc -l` |
| Guthaben | Daniel 09:07: **8,25 USD** Kontostand, **41,74 USD** Gesamtverbrauch; Tagesbudget fuer das starke Modell **3 USD** | Daniel, 09:07 |
| Offen (Freigabe) | Pillow in die Spiel-Laufzeit (Projekt-venv oder uv-Interpreter) und Loesung fuer die Ressourcenleiste ohne Pillow; das ungenutzte Python 3.15.2 unter `AppData\Local\Python` (122 MB) entfernen | eigene Messung |

## Der EINE naechste Schritt

**Die Kaserne-Ansicht darf ohne Gebaeude am aktiven Ort nicht abstuerzen** - der Fehler ist aelter als
dieser Schritt und beim Bau der Pruefdatei aufgefallen: `_siedler_warnung_zeichnen`
(aufgerufen aus `_render_ausbildung`) liest `reserve["guenstigste"]`, und
`spieloekonomie.siedler_reserve` liefert diesen Schluessel NICHT, wenn am aktiven Ort kein Gebaeude
steht (Fruehfall `if not bedarf: return {...}` ohne `guenstigste`). Nachgestellt: Siedlung mit
Kriegerakademie, aktive Siedlung ohne Gebaeude, Menuepunkt "Kaserne" -> `KeyError`.
Zu tun: den Schluessel im Fruehfall mitliefern (der Docstring der Funktion beschreibt die Rueckgabe,
also gehoert er in die Funktion), Wache dazu (Siedlung ohne Gebaeude -> Ansicht rendert), voller
Sammellauf, Protokollzeile, ein Commit.
Arbeitsweise: Pruefdatei ergaenzen, voller Sammellauf, Protokollzeile, ein Commit.

## Reihenfolge danach

1. **Pillow-Entscheidung** (Daniel): Projekt-venv mit Pillow und Start-Batch darauf, damit Leiste und
   Bilder scharf sind; danach die Ressourcenleiste ohne Pillow als Rueckfall.
2. Icons und Hintergrund im Fenster abnehmen - die drei Bilder unter `docs/audits/` zeigen den Stand.
3. Auswahlrahmen der C2-Lieferung (der goldene gezeichnete Rahmen liegt derzeit ueber dem gelieferten);
   die acht Einzelsymbole aus `assets/icons/leiste/symbole/` sind ungenutzt.
4. Wappen den fuenf Bots zuordnen; Burgen zu Weltkarten nur als gekennzeichneter Vorschlag.
5. S-8 Bilanz (500 Mana + 100 Gold, Register 93), danach `weltkarten_seed` fest (Register 94).
6. Demo-Gates G-01..G-07 vor jedem Upload; die Demo wird LEER ausgeliefert.
7. Protokoll steht bei **466 Zeilen** (Ziel unter 320) - Verdichten mit Sicherung vorher.
8. **EXE ist vom 01.11. 19:01** - vor einer Demo neu bauen und startgeprueft starten.

## Fallstricke, in diesem Schritt belegt

- **Ein gruener Sammellauf sagt nichts ueber den STARTWEG.** Alle 4.761 Pruefungen liefen mit dem
  Hermes-Python (Pillow vorhanden) - das Spiel startet aber mit einem anderen Interpreter ohne
  Pillow. Bei Bild-Funktionen deshalb immer einmal mit DEM Interpreter messen, den das Start-Batch
  aufruft (`py -0p` zeigt die Laufzeiten, `python.exe -c "import PIL"` die Wahrheit).
- **Rueckfall statt Absturz, aber sichtbar statt still.** Ein `None`-Ergebnis ohne Rueckfall heisst:
  das Bild FEHLT, ohne Fehlermeldung. Das ist die unangenehmste Sorte Fehler - gruen und leer.
- **`uv pip install` in die uv-Laufzeit geht nicht:** `externally managed`. Sauberer Weg ist eine
  Projekt-venv; das Aendern des Start-Batches ist Daniels Entscheidung.
- **WindowsApps-`python.exe` ist der Python-Manager, kein Python.** Ein Aufruf startet ungefragt einen
  Download (hier Python 3.15.2). Fuer Messungen immer den echten Interpreterpfad nehmen.

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

> **GELTENDER STAND 03.11.2026, 21:20 (Hermes).** Diese Ueberschrift ist der Wiedereinstiegspunkt, den
> `tools/zieluebergabe.py` liest; die Liste darunter ist **HISTORIE der GPT-Runde vom 28.10.2026** und
> **nicht mehr** der Fahrplan. Geltend: Hermes fuehrt das Projekt seit 30.10.2026 zurueck, und der
> neueste Stand steht GANZ OBEN in dieser Datei (Block **S-8 Stufe 1**, Register 174: Ertrag aus den
> gebauten Anlagen; naechster Schritt S-8 Stufe 2, Feld-Prioritaeten).
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

**Nachtrag 18:30 - Skip-Mechanik gebaut, Uebergabe 1828 abgelegt:** ein gescheiterter Spielschritt
beendet den Spieltest nicht mehr. `tools/spieltest_simulation.py` sammelt Fehler mit Tag, Stelle und
Grund in `log["uebersprungen"]`, laeuft weiter und bricht erst bei 200 Fehlern in Folge ab
(`MAX_TICK_FEHLER_FOLGE`); der Bericht hat einen eigenen Abschnitt dafuer. Wache
`tests/test_spieltest_skip.py` **17/0/0** (Durchhalten, Liste, Bericht, Gegenprobe ohne Fehler,
Dauerfehler-Abbruch). Probelauf ueber 2 Spieltage geschrieben, Paket P1 5.386 Zeichen (~0,0248 USD je
Lauf). **Uebergabe** `UEBERGABE_NEBELSEETAL_20261105_1828.md` liegt auf dem Desktop und hashgleich in
`D:\Arbeiten\Hermes\Uebergaben\20261105_1828\` (`14581d4e...`). Offen bleibt der volle Sammellauf
nach dieser Werkzeug-Aenderung und die bezahlten Spieltest-Laeufe.
