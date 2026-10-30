# FIX05 – Prüfbefunde der isolierten Projektkopie (28.10.2026)

**Geltung:** Dies ist eine technische Befundliste, KEIN weiteres Entwicklungsprotokoll und
KEINE neue Roadmap. Hermes entscheidet über Übernahme und Priorität. Basis: das vom Nutzer
bereitgestellte ZIP `Nebelseetal_Remake_28.10.26.zip` einschließlich originaler lokaler
`.git`-Metadaten; die Produktordner auf dem Windows-Rechner wurden nicht geändert.

## Nachweise vor Eingriff

- 87 aktive `tests/test_*.py` **einzeln** über Python 3.13.5 + Xvfb unter Linux gestartet:
  **84 Exitcode 0, 3 Exitcode 1** (mit grafischer virtueller Anzeige; dies ist kein
  physischer Windows-Test). Alte Fälle sind als separates Testskript und nicht als
  einzelne Assertionen gezählt.
- `test_gpt_portable_uebergabe.py`: verlangte verbotenerweise ein EXE-freies Root,
  obwohl das Projekt eine bestätigte Entwickler-EXE im Root hat. Test ist durch
  Aktualisierung der Testannahme korrigiert; Build und Gleichheit zur aktuellen
  Python-Fassung sind ausdrücklich nicht getestet.
- `test_oekonomie_kern_unabhaengig.py`: **bleibt offen**. Lädt `data/gelaende.json`
  und erwartet `kartenmass`/alte 8×7-Saatgeneratoren; `KeyError: 'kartenmass'`.
  Kein Fehlerbeleg gegen das neue Originalkarten-System, aber ein aktuell kaputter
  aktiver Test und fehlender unabhängiger 10×10-Ökonomie-Nachfolger.
- `test_protokoll.py`: **ursprünglich** gescheitert, weil beim ersten isolierten
  Prüfstart die `.git`-Daten nicht extrahiert waren. Nach ausschließlich aus DEMSELBEN
  Nutzer-ZIP übernommener originaler `.git`-Historie: **15 bestanden, 0 Fehler,
  2 Befunde**; alle 27 im Protokoll erkannten Commit-Kennungen über `git cat-file`
  nachgewiesen. Befunde: Protokoll 488 Zeilen bei Zielgröße 320 und 24
  umformulierte/nicht wortgleich auffindbare historische Absatzanfänge.
- `git rev-parse HEAD` der **ZIP-lokalen** Historie:
  `1c4dffa3cf1c47c9c4963e9782b34272fcca29d1` – kein Remote `origin` in dieser
  ZIP-Git-Konfiguration; nichts über die GitHub-Kopie ableitbar. NICHT committen,
  cherry-picken, pushen oder Git-Historien mischen.
- Aktive Python-Dateien AST-parsebar: 166 untersuchte `.py` einschließlich
  Hilfs-/Testdateien, 0 Syntaxfehler. Keine vollständige Rechtschreibprüfung.
  Ein `SyntaxWarning` wegen Backslash in `tools/originalkarten_grafiken_bauen.py`
  wurde im Arbeitsdelta korrigiert.

## Kartendaten: unabhängig aus den Dateien gegengeprüft

- 18 JSON-Dateien unter `data/` geparst; keine Parsefehler.
- `data/originalkarten/katalog.json`: **127 Karten mit eindeutigen IDs**, je
  **100** aktive Felder; alle 127 referenzierten historischen Quellgrafiken
  und 127 generierten 640×640-Spielgrafiken existieren und erfüllen ihre
  Katalog-/Manifest-SHA256. Bei den **117** Karten mit quellseitig auf 100
  summierten Feldwerten entsprechen die gezählten Spielterrainarten den
  Originalkontingenten, auch für Arten mit Anzahl 0.
- **10 Karten** mit historisch angegebenen Gesamtwerten ungleich 100:
  `original-009`, `original-043`, `original-038b`, `original-059`,
  `original-072`, `original-073`, `original-076`, `original-078`,
  `original-081`, `original-095`.
  Das sind Quellen-/Vergleichslücken, keine Erlaubnis zur selbständigen Korrektur.
- **25 Sichtprüfungen** bleiben offen; IDs, Originalbilder und Warnungen stehen in
  `docs/quellen/ORIGINALKARTEN_25_SICHTPRUEFUNG_OFFEN_FIX05.csv`.
  SHA256-Übereinstimmung beweist NICHT, dass ein automatisches Raster zur
  historischen Karte visuell richtig interpretiert wurde.

## Produktbefund / Abhilfe FIX05

- `src/spielzeit.py` schrieb Tempo-Änderungen direkt nach `data/spielzeit.json`.
  Dies ist im gepackten Ein-Datei-Windows-Build kein zuverlässiger dauerhafter
  Schreibort. Der Code speichert jetzt atomar in einer separaten privaten Datei
  `spielzeit_einstellung.json` im aktuellen Spielstands-/Profilordner;
  das Quellen-JSON ist nur noch die unveränderte Werksvorgabe.
  Im öffentlichen Modus bestimmt `src/public_start.py` den bereits isolierten
  Laufzeitordner, im Entwickler-Modus gilt weiterhin das lokale Standardprofil.
  Alte Anpassungen der `data/spielzeit.json` bleiben als Startvorgabe lesbar.
- `src/main.py` fängt einen Schreibfehler in der Zeitfaktor-Bedienoberfläche
  ab und zeigt eine Fehlermeldung statt fälschlich erfolgreiche Speicherung.
- Der neue Regressionstest prüft Privatspeicher, Persistenz nach Cache-Reset,
  Isolation, beschädigte Daten, abgebrochene atomare Speicherung und
  reale Tkinter-Schaltfläche. Keine automatischen Dateilöschungen im Projekt.

## Bekannte Grenzen / Folgemaßnahmen für Hermes

1. Nur Hermes darf gegen seine aktuelle Roadmap, beiden Windows-Git-Ordner,
   echte Windows-EXE und Veröffentlichungsstände diffen/freigeben.
2. Älteren 8×7-Test **fachlich neu schreiben** (independent 10×10 terrain/economy),
   statt ihn blind zu löschen oder als bestanden auszugeben.
3. Den kompletten Windows-Testlauf inklusive frischem öffentlichen Profil und
   Entwicklerprofil ausführen; neue EXE aus Code bauen, real speichern/laden und
   nach Freigabe Testrelease aktualisieren.
4. Originalkarten-Sichtkontrolle 25 Stück, Bot-Wirtschaft, Kampfkern,
   Siedlung/Forschung/Produktion/Karren-E2E und Speicherarchiv-Retention bleiben offen.
5. Historische Rechte und Remote-Release-/Tag-/Commit-SHA unabhängig prüfen;
   Web-/API-Abruf war hier nicht belastbar möglich. Nutzerbestätigungen separat belassen.
6. Alle Altaufgaben der bestehenden Hermes-Roadmap bleiben erhalten;
   diese Liste hebt sie nicht auf.

## Vollständiger Kontrolllauf nach FIX05

Erneuter Lauf über alle 88 aktiven Testskripte: **87 Exitcode 0, 1 Exitcode 1**.
Einziger fehlgeschlagener Fall `tests/test_oekonomie_kern_unabhaengig.py` (historisches
8×7-Modell, erwartet nicht mehr vorhandenes `kartenmass`). Außerdem 6/6 neue
Tempo-Regressionen bestanden, darunter Tk-Button. Der abschließende Testmatrix-
Export liegt im externen Delta-Paket unter `PRUEFBELEGE/TESTMATRIX_FIX05.json`.
Keine Windows-EXE neu gebaut.
