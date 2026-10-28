# Bewertung durch ChatGPT – Nebelseetal Remake

**Bewertungsdatum:** 28.10.2026  
**Beobachtungsstand:** Screenshots vom 23.10.2026  
**Tatsächlicher letzter Entwicklungstag:** 06.10.2026 (vom Auftraggeber ausdrücklich bestätigt)  
**Adressaten:** Auftraggeber und Hermes als leitender Projektkoordinator  
**Dokumenttyp:** unabhängige Projekt-, Spielkonzept-, Oberflächen- und Technikbewertung; **kein Entwicklungsauftrag und keine selbst vorgenommenen Codeänderungen**

> **Gesamturteil:** Nebelseetal Remake ist ein bemerkenswert systematisch wiederaufgebautes Strategiespiel mit einer erkennbaren Identität, guten technischen Grundlagen und einem starken, nachvollziehbar dokumentierten Entwicklungsprozess. Es ist aber **noch kein ausbalanciert abgeschlossenes Einzelspielerspiel**. Der wichtigste nächste Schritt ist nicht ein Grafik-Neubau, sondern die in der Projektübergabe ausdrücklich vorgesehene **Aktivierung der einheitlichen Ereignisschleife und Ökonomie**. Erst danach lassen sich Wirtschaft, Gegnerdruck, Handel, Krieg, Sieg und Spielfluss als Ganzes belastbar beurteilen.

## 1. Prüfgrundlage, Nachweisstufen und zeitliche Einordnung

### 1.1 Benutzte Quellen

**Primärmaterial:** acht Screenshots (`Kaserne_…`, `Lager_…`, `NachrichtenÜbersicht_…`, `Portal_…`, `Dorfzentrum_Siedlungskarte1_…`, `Dorfzentrum_Siedlungskarte2_…`, `DorfzentrumÜbersicht_…`, `KartenAnsicht_…`; jeweils vom 23.10.2026); `Nebelseetal_Remake.exe`, `Nebelseetal_Remake.bat`, `run_tests.bat`.

**Technische und konzeptionelle Dokumente:**

- `KONTEXT_PAKET.md` – **führende Übergabe, Stand 06.10.2026, 08:25**, vor allem Abschnitte 1–3, 5–8.
- `ENTWICKLUNGSPROTOKOLL_VOLLFASSUNG_2026-10-05_0820.md` – historischer Ablauf und belegte Prüfstände bis 05.10.; **nicht** alleiniger Nachweis des Standes vom 06.10.
- `PROJEKT_STAND.md` – fortgeschriebene Abschnitte **0c und 0e** (bis 06.10.2026) haben Vorrang vor älteren Abschnitten derselben Datei.
- `PLAN_AUS_HANDBUCH.md` – dokumentierter Soll-Ist-Abgleich der 24-seitigen Spielanleitung von 2009.
- `PLAN_Einzelspieler.md` – ursprüngliche Abnahmeziele und technische Risiken; historische Fehler sind nicht automatisch noch vorhanden.
- `PLAN_RASTER_8x7.md` – Kartenmaß-Entscheidung mit technischen Abhängigkeiten.
- `KARTEN_ENTWURF.md` und `MUSTERVORLAGEN.md` – optische und strategische Kartengrundlagen.
- `PLAN_ASTRA_EINSATZ.md` – historische Regeln für einen kostenkontrollierten Modelleinsatz; alte Guthabenangaben **nicht** als heutige Freigabe behandeln.

**Nicht direkt verfügbar:** vollständiges Git-Repository (`src/`, `data/`, `tests/`), originale PDF-Spielanleitung von 2009 und die im Kontextpaket genannten neueren Audits unter `docs/audits/`. Diese können bei Hermes lokal vorhanden sein. Aussagen aus ihnen sind nur **sekundär** über die übergebenen Dokumente nachgewiesen.

### 1.2 Tatsächlich selbst überprüft

- Die bereitgestellte EXE ist eine Windows-64-bit-PE-Datei mit **14.652.424 Byte**.
- Ihre SHA-256-Prüfsumme lautet **`c1523670aa307077fd8be3c0858d52a44a1a20a40c024f1d2275658c4276ac75`** und stimmt **bytegenau** mit dem in `KONTEXT_PAKET.md` dokumentierten Build vom 06.10.2026 überein. Der Datei-Uploadzeitstempel ist **nicht** das Builddatum.
- Die acht Screenshots wurden inhaltlich geprüft. Sie zeigen einen **geladenen Altspielstand**: In „Nachrichten“ steht ausdrücklich `Modus 'legacy'`, ohne Versionsfeld und **ohne Umrechnung**. Dies ist wesentlich für die Bewertung der Karten, Bestände und Siegmeldung.
- `Nebelseetal_Remake.bat` startet **`python "%~dp0src\main.py"`**, also den Entwicklungsquellcode, **nicht die EXE**. Als Benutzerstartdatei ohne Python/Projektordner ist sie daher ungeeignet.
- `run_tests.bat` ruft die Testdateien unter `tests/` mit Python auf. Diese Dateien wurden nicht mitgeliefert; die Prüfroutine lässt sich aus den vorliegenden Dateien **hier nicht erneut ausführen**.

**Belegstufen in diesem Bericht:** **[S]** unmittelbar am Screenshot oder an der vorliegenden Datei sichtbar; **[D]** in den Projektunterlagen dokumentiert, hier nicht unabhängig ausgeführt; **[H]** nachvollziehbare Hypothese/Prüfauftrag; **[E]** gestalterische oder spielmechanische Empfehlung. Weder erfolgreiche dokumentierte Tests noch ein gestartetes Fenster beweisen automatisch einen fehlerfreien kompletten Spieldurchlauf.

## 2. Was Nebelseetal sein soll – meine Rekonstruktion des Spielkonzepts

Nebelseetal war ein mittelalterlich-fantastisches **Echtzeit-Browserstrategiespiel**, nun als **offline lauffähiges, portables Windows-Einzelspielerspiel** gedacht. Entscheidender Anspruch ist **Originaltreue dort, wo die Quellen Regeln belegen**, verbunden mit vernünftigen Einzelspieler-Ergänzungen an Stellen, an denen einst menschliche Mitspieler nötig waren. Das originale Browsergefühl und dessen Icons/Farbsprache sollen erkennbar bleiben. Es ist **kein Auftrag, ein beliebiges neues Fantasy-Aufbauspiel zu entwickeln**.

Die beabsichtigte Spielschleife lautet:

**Siedlung und Gelände verstehen → passende Rohstoffproduktion errichten → lokale Versorgung und Bevölkerung aufbauen → Forschung, Waren und Einheiten freischalten → zwischen eigenen Siedlungen mit Karren handeln/transportieren → gezielt weitere, spezialisierte Siedlungskarten wählen → Bots diplomatisch und militärisch begegnen → über einen längeren, nachvollziehbaren Wirtschafts- und Verteidigungsaufbau das Spielziel erreichen.**

Besondere Merkmale, die erhalten bleiben sollten:

1. **Standortentscheidungen mit Folgen:** Gelände, nicht eine generische Gebäude-Liste, bestimmt Erträge. Ein Nebelsee, Berg oder Wald muss strategisch anders wertvoll sein.
2. **Siedlungen sind nicht bloße Kopien:** die Startkarte ist ausgeglichener; weitere Karten haben klare wirtschaftliche Stärken und Engpässe. Das erfordert Handel und Transport.
3. **Originaldaten statt erfundener Einheiten:** laut Projekt 28 originale Einheiten, 17 Waren, 21 Forschungen, neun Rohstoffe und 20 Gebäude. Forschung, Ausbildungsgebäude und Ausrüstung müssen wirkliche Effekte haben.
4. **Kämpfe sind Ereignisse:** Vorphase, bis zu zehn Sequenzen, Fern- und Nahkampf, Mauern, Flucht, Verluste, Beute und archivierter Bericht; kein einzelner Zufallsvergleich.
5. **Bots ersetzen die Mehrspieler-Funktion:** nicht nur Namen in einer Liste, sondern sichtbare Wirtschafts-, Handels- und Militärentscheidungen auf leichten, mittleren und schweren Schwierigkeitsgraden.
6. **Der Limbus ist ein eigenes System:** 20 Dimensionen zu je 20 × 20 Koordinaten; eigene Welt/andere Welten und Manakosten sind **nicht** dasselbe wie lokale Siedlungsfelder oder der Kontinent.
7. **Spielzeit ist steuerbar, aber konsistent:** Echtzeit-Ursprung, beschleunigbar für Einzelspieler; sämtliche Fristen müssen denselben Takt verwenden.
8. **Eine stabile EXE:** offline, Speichern/Laden, alte Spielstände vorsichtig behandeln, optional mit Passworttor; kein Serverzwang.

**Der wichtigste gestalterische Maßstab:** Ressourcen- und Standortentscheidungen sollen interessanter sein als bloß möglichst schnell auf eine Punktzahl zu klicken. Genau diese Richtung wurde laut `PROJEKT_STAND.md`, 0c, vom Auftraggeber am 05.10. ausdrücklich festgelegt.

## 3. Gesamteinschätzung

Die folgenden Wertungen sind **redaktionelle Einschätzungen**, keine automatisierten Testergebnisse. Die technische Stabilität wurde nicht durch einen eigenen Windows-Dauertest verifiziert.

| Bereich | Einschätzung | Begründung |
|---|---:|---|
| Konzept, Eigenständigkeit und Originaltreue | **8,5/10** | Klare Identität; umfangreicher dokumentierter Handbuch-Abgleich; originalnahe Einheiten und Regeln. |
| Entwicklungsdisziplin und Nachvollziehbarkeit | **9/10** | Commits, Einzeltests, Gesamtläufe, Prüfzahlen, Sicherungen, ehrliche Fehlerprotokolle, Kostendisziplin. |
| Technische Grundstruktur (nach Dokumenten) | **7,5/10** | JSON-Datenschicht und viele getrennte Regelmodule; der letzte Integrationsschritt fehlt noch. |
| Strategische Tiefe als Entwurf | **8/10** | Gelände, lokale Lager, Transport, Engpässe, Forschung und Bots bilden ein gutes Fundament. |
| Tatsächlich belegte End-to-End-Spielreife | **5/10** | Ereignisschleife/Ökonomiemodus noch nicht aktiviert; dokumentierte Lücken bei Kampfverlust-Anbindung und Balance. |
| Benutzerführung und Lesbarkeit | **4,5/10** | Hohe Informationsdichte, winzige Schrift, lange Listen, ungenutzte Fensterfläche, wenig konkrete Fehlerhilfe. |
| Grafik und Wiedererkennungswert | **6/10** | Originalfarben und Icons unterstützen Nostalgie; Karten sind optisch eintönig und wichtige Signale schwer lesbar. |
| Siegziel, Pacing und Langzeitmotivation | **4,5/10** | Aktuelle 300-Punkte-Demogrenze kollidiert mit originaler Wall-Wertung; mehrere Fortschrittssysteme noch nicht als Partie erprobt. |

**Verdichtetes Urteil:** als **Wiederaufbauprojekt und technisches Fundament gut bis sehr gut**; als **fertiges Einzelspielerspiel derzeit eher eine fortgeschrittene, noch nicht ausbalancierte Vorversion**. Die Zahl **„6/10 als momentane Spielversion“** und **„8,5/10 als Projektarbeit“** ist eine persönliche Gesamtwertung, kein Fehlerprozentsatz. Der Schritt von „funktionierende Systeme“ zu „gutes Spiel“ steht noch bevor.

## 4. Bild-für-Bild-Bewertung

| Ansicht | Beobachtung und Stärke | Auffälligkeit / Empfehlung |
|---|---|---|
| **Dorfzentrum** | [S] Zwei Siedlungen, aktive Siedlung, lokale und Reichsbestände, Gebäudeübersicht, nächster Schritt. Sehr gute funktionale Ausgangsbasis. | [S/E] Lokaler Bestand und Reichsbestand stehen eng nebeneinander, obwohl sie **verschiedene Buchungstöpfe** sind. Sichtbarer Wechsel der aktiven Siedlung sollte noch stärker hervortreten; „Gebäude auf der Karte: 19/27“ braucht zugehörige Kapazitätsanzeige. |
| **Siedlungskarte 1** | [S] Gelände und Bauplätze sind anklickbar, Geländelegende vorhanden; die Startkarte ist ausgeglichener. | [S/E] Fast alle Gebäude sehen aus wie dasselbe Wohnhaus. Geländetyp, Gebäudeart, Ausbaustufe und Zugänglichkeit konkurrieren visuell. Ein Klick sollte zusätzlich Ertrag/Kosten/Voraussetzungen im Detailpanel zeigen. |
| **Siedlungskarte 2** | [S] Ressourcenprofil „steinreich“, ausgewähltes Feld F1, Aufwerten/Abreißen, sichtbare Wege. | [S/E] 8×5-Raster und mehrere ältere Bauzustände; **wegen des ausdrücklich geladenen `legacy`-Spielstands kein belegter Verstoß gegen die neu beschlossene 8×7-Generierung**. [H] Frische Neupartie getrennt testen. „Kriegerakademie auf Hügel (belegte Standortregel)“ ist als Altbestand/Standortausnahme sauber zu erklären. |
| **Lager** | [S] Alle Waren und Einheiten mit Originalsymbolen sichtbar, getrennte Gruppen. | [S/E] Sehr viele großflächige **Nullfelder**; fast die ganze Fläche ist Leerlauf. Standard: Besitz >0 und laufende Aufträge zuerst; vollständige Enzyklopädie/Nullbestände optional. Für jede Ware Herstellungsweg, Ortsbezug und Verwendungszweck anbieten. |
| **Kaserne** | [S] Icons, LE/AT/PA/TP/SK, Forschungssperren und ausbildungsbezogene Bauvoraussetzungen. | [S/E] Zeilen sind sehr schmal, Schrift winzig und Einheitenbeschreibung teilweise zu kryptisch. Ausbildung sollte immer **Menge, lokale Kosten, fehlende Waren, Dauer, Warteschlange und aktive Siedlung** nennen; gesperrte Schaltfläche direkt begründen. |
| **Nachrichten** | [S] Es gibt ehrliche Meldungen über fehlendes Lager, Voraussetzungen, Sieg und Altspielstand. | [S/E] Ein Dutzend fast identischer Meldungen „Bürgerwehr nicht ausgebildet: Lokales Lager reicht nicht“. Es fehlen konkrete Fehlbeträge, Filter, Gruppierung und Verknüpfung zur Lösung. Zudem konkurrieren Warnung, Erfolg und Info optisch. |
| **Portal** | [S] 20 Dimensionen, Koordinatengitter, benannte Nachbardimensionen, 5.000-Mana-Regel und andere Spieler/Bots. Die ursprüngliche Struktur ist erkennbar. | [S/H] Die **gesamte sichtbare 20×20-Fläche ist grün**, obwohl „eigene Welt grün“ erläutert wird. Das sieht nach 400 eigenen Positionen aus; Belegung und freies Feld sind nicht klar unterscheidbar. **Darstellungssemantik prüfen**, nicht automatisch Spielwelt-Daten ändern. |
| **Weltkarte** | [S] Gelände, Ortsmarker, Regionsnamen, Minikarte, Zoom und Legende vorhanden. | [S/E] Sehr kleine Kartenausschnitte im großen Fenster, teilweise überlagernde Regionsnamen und dicht gesetzte Icons; Ziel-/Kartenaktionen sind nicht sofort erkennbar. Größere Kartenfläche, klarere Auswahl und passende rechte Detailspalte. |

### 4.1 Was auf den Screenshots **nicht** als Bug einzutragen ist

**Das 8×5-Raster:** `PLAN_RASTER_8x7.md` und `PROJEKT_STAND.md` belegen die Entscheidung **8×7 = 56 Gesamtfelder, davon 40 bebaubar, nur Sumpf gesperrt**. Aber der Screenshot zeigt ausdrücklich einen **alten Spielstand**. Darin darf das alte 8×5-Raster erhalten bleiben. [H] Prüffall: Neupartie erzeugen, beide Kartengenerationen sauber getrennt laden, **Altkarte niemals still migrieren**.

**Die 1.000 Kriegspunkte ohne Truppen:** Die Dorfzentrumansicht nennt einen **Verteidigungswall Stufe 10**, und der Handbuchplan nennt dafür die originale Punkteformel **Stufe³**. Daher sind **10³ = 1.000 Kriegspunkte** regelkonform; mit Forschungspunkten 0 ergibt die originale Gesamtwertung **(1.000 + 0)/2 = 500**. Die Sidebar zeigt genau diese **500 Gesamtpunkte**. Es liegt **kein nachgewiesener Rechenfehler** vor. Das **Spielziel bei 300 Punkten** ist jedoch als heutiges Einzelspieler-Siegziel fragwürdig.

**Die wiederholten Lagerwarnungen:** Die aktive Siedlung 1 zeigt lokal nur **Metall und Nahrung** (neben Siedlern), während das Reich beispielsweise Holz besitzt. Deshalb kann „lokales Lager reicht nicht“ in dieser Situation **inhaltlich korrekt** sein. [H] Hermes muss zunächst Regeln, aktive Siedlung und fehlende genaue Ressource prüfen; **nicht** ungeprüft Ressourcen schenken oder den lokalen Speicher umgehen.

**„Handkarren benötigt Stellmacher“ trotz eines Stellmachers:** Der Stellmacher ist in der **Gesamtübersicht über beide Siedlungen** vorhanden; der Screenshot zeigt jedoch die erste Siedlung als aktiv. [H] Standortzuordnung prüfen, bevor ein Fehler behauptet wird.

## 5. Wichtigste konzeptionelle und technische Befunde

### B01 – Sieg ist derzeit zu billig bzw. falsch motivierend **[S+D+E, sehr hohe Priorität]**

Im Nachrichtenbild steht sinngemäß: **„VORSCHLAG: Zielpunktzahl 300 erreicht – das Handbuch kennt keine Siegbedingung.“** Die Sidebar meldet **SIEG** bereits bei 500 Punkten, erzielt offenbar ausschließlich durch den Wall. Die **Punkteformel selbst ist korrekt**. Das Problem ist die **Schlussfolgerung „300 Punkte = Partie gewonnen“**: Sie belohnt im Extremfall einen hochgezogenen Wall stärker als die vom Auftraggeber gewollten Siedlungs- und Handelsentscheidungen.

**Empfehlung:** Originalpunkte vollständig beibehalten, **Siegziel davon trennen**. Ein plausibles Einzelspieler-Ziel benötigt mehrere Säulen, etwa Wirtschafts-/Versorgungsfähigkeit, **tatsächlich durchgeführte Transporte** zwischen eigenen Siedlungen, Forschung und eine militärische oder diplomatische Bewährungsprobe. Die genaue Endbedingung **nicht ohne Freigabe des Auftraggebers festschreiben**. Bis dahin ist „300 Punkte“ höchstens ein klar gekennzeichnetes **Testziel** – kein balanciertes Endspiel. Ein gespeicherter Legacy-Sieg darf bei einer neuen Regel nicht rückwirkend gelöscht oder umgerechnet werden.

### B02 – Ökonomie ist vorbereitet, aber die Ereignisschleife fehlt **[D, höchste technische Priorität]**

Das `KONTEXT_PAKET.md` sagt ausdrücklich: **Schritt 9 mit Teil 1 bis 8 ist fertig; Schritt 10 (`tick_bis` + Aktivierung) ist offen**. `mode="oeokonomie-1"` in neuen Spielständen ist **bis dahin nur ein Merker**, kein Beweis, dass der neue Modus schon aktiv läuft. Die gemeinsame Zeitumrechnung muss an **genau einer Stelle** hängen, und es darf nicht parallel ein alter und ein neuer Tick verbuchen.

**Folge:** Noch keine seriöse Behauptung, dass die gesamte Ökonomie unter echter Spielzeit bereits zuverlässig funktioniert. Das ist der erste Arbeitsauftrag für Hermes, **nicht** nur ein weiterer optionaler Test.

### B03 – Systemübergreifende Aktionen brauchen End-to-End-Tests **[D+H, sehr hoch]**

Die Dokumentation nennt selbst einen ehemals doppelten Truppenabzug beim Stationieren, inzwischen behoben, aber zusätzlich einen **bekannten Befund zum Lagerort stationierter Truppen**. Bereits gebaute Kampfverluste sind laut Projektstand noch nicht vollständig an die spielbare Oberfläche angeschlossen. Neue Routinen wie `ort_tick` können Ertrag verdoppeln, wenn der alte Weg parallel weiterläuft; die vorhandenen Tests sollen genau dies verhindern.

**Empfehlung:** Nicht bloß Funktionen isoliert testen, sondern realistische Sequenzen über UI, Spielzustand, Mission, Uhr, Speichern/Laden und Ergebnis. Einen bekannten Befund nicht zu „erledigt“ erklären, nur weil 4.061 Tests bestanden haben.

### B04 – Die Bedienung versteckt das eigentliche Strategiespiel **[S+E, hoch]**

Auf 1920er Screenshots sind manche Texte kaum lesbar; ungenutzter Leerraum dominiert die Fenster. Der **aktive Ort**, die **lokalen Ressourcen** und die **nächste notwendige Aktion** sind nicht durchgängig klar. Das sind nicht nur Schönheitsfehler: Bei einer Wirtschaft mit getrennten Ortslagern entscheiden diese Informationen direkt über die Handlungsfähigkeit.

**Empfehlung:** Keine komplette UI-Neuentwicklung, bevor Schritt 10 funktioniert. Anschließend gezielter Tkinter-Feinschliff mit größeren skalierbaren Fonts, konsistenter Breite, klarem rechten Detailbereich und kompakteren Informationslisten. Typische Testerfrage: „Kann ein neuer Spieler innerhalb von 60 Sekunden verstehen, warum Bürgerwehr hier nicht ausgebildet werden kann?“

### B05 – Bots und Krieg müssen spürbare Gegenkräfte bilden **[D+E, hoch]**

Das Remake soll den Sinn des ursprünglichen Multiplayer-Spiels in den Einzelspieler übertragen. Bots brauchen daher nachvollziehbare Produktions- und Militärentwicklung, Ziele und Unterschiede zwischen leicht/mittel/schwer. Wenn sie nur auf Klicks reagieren, entstehen Handelsmasken, aber keine lebendige Welt. Die Kriegsauswertung muss Verlust und Beute wirklich in die Garnisonen und Transporte übertragen. **Die genauen Kampfregeln bleiben aus dem Handbuch; die Balance der Bots ist eine eigene Designaufgabe.**

### B06 – Alte Spielstände werden vorbildlich vorsichtig behandelt **[S+D, Stärke mit Folgerisiko]**

Die Nachricht „legacy, nichts umgerechnet“ ist eine Stärke. Sie verhindert, dass eine neue Wirtschaft heimlich alte Erfolge und Gebäude verändert. Kritisch ist jedoch, dass ein Nutzer anschließend dieselben Menüs mit **unterschiedlicher Regelwelt** sehen kann. **Empfehlung:** dauerhaft sichtbares Statusfeld „Altspielstand / Legacy-Regeln“ plus „Neues Spiel mit neuer Ökonomie“; dokumentierte Importgrenze. **Keine stillen Konvertierungen.**

### B07 – Originaltreue ist gut, aber Beleg und Vorschlag dürfen nie vermischt werden **[D+E]**

Die Handbuch- und Kartenpapiere unterscheiden originale Werte (z. B. Kampf, Punkte, Limbus) von selbst geschätzten Baupreisen, Bot-Startbeständen, Bot-Handelsgrenzen und Siegbedingungen. Diese Disziplin muss im Code und in der UI bleiben. Konflikte zwischen frühen Planfassungen und dem **fortgeschriebenen Stand vom 06.10.** nicht wieder aufrollen: beispielsweise die alte „Vermessung“-Forschung ist ausdrücklich als erfunden entfernt worden.

### B08 – Auslieferungsform sauber trennen **[S, mittel bis hoch]**

Die BAT-Datei startet `src/main.py` mit Python und ist damit ein **Entwicklerstarter**. Die portable EXE ist das eigentliche Spielerprodukt. **Empfehlung:** `dev_start.bat` eindeutig benennen und nur intern beilegen; die Spielerausgabe enthält möglichst die EXE und benötigte Dokumentation, **keinen** Python-Zwang. Die `run_tests.bat` ist nur im vollständigen Quellrepository sinnvoll. Auslieferung zusätzlich in sauberem Windows-Verzeichnis ohne Projektumgebung testen.

## 6. Priorisierte Arbeitsanweisung für Hermes

### P0 – Erst die belegte, noch offene Integration abschließen

**P0.1 – Arbeitsstand sichern und nur die letzte gültige Übergabe benutzen.** `KONTEXT_PAKET.md` zuerst, `PROJEKT_STAND.md` Abschnitte 0c/0e als historische Detailquelle; `git status --short`, exakte EXE-Prüfsumme und Git-Commit notieren. Kein paralleler ungeprüfter Agentenlauf, kein Umschreiben der bisherigen Protokollhistorie. Das offizielle Gesamtziel aus `PROJEKT_STAND.md` **unverändert** lassen.

**P0.2 – Schritt 10 ausführen, nicht neu erfinden.** Die bei Hermes lokal liegende Referenz `docs/audits/entwurf_spieloekonomie_sol_2026-10-05.txt`, **Zeilen 791–1018** für `tick_bis` und **Aktivierungsstelle um Zeile 1092**, ist laut Projektübergabe maßgeblich. `spielzeit.faktor()` genau **einmal** als Zeitquelle verwenden; lokale Erträge, Ausbildungen, Werkstätten, Forschungen, Transporte, Handel und Bots zentral vorwärtsführen. Keine zweite Ernte, kein zweites Abschließen. Legacy-Partien bleiben Legacy.

**P0.3 – Akzeptanzprüfung Schritt 10:**

1. **Neues Spiel:** kein Start mit falschen Alt-Ressourcen; aktive Ortslager; erwartete Startkarte, Felderzahl **8×7 = 56** und genau **40 bebaubare Felder** nach geltendem Kartenvertrag.
2. **Zeitrechnung:** in einem definierten Test laufen 1, 10 und 60 Spielminuten mit identischem wirtschaftlichen Gesamtergebnis, egal ob in einem großen oder vielen kleinen Ticks; nach Speichern/Laden ohne Doppelbuchung.
3. **Warteschlange:** ausgebildete Einheit und hergestellte Ware stehen **erst nach der Dauer** im richtigen Ortslager; Auftrag verschwindet genau einmal, UI aktualisiert sich.
4. **Transport:** Start deckt Fracht und Karren, Ankunft bucht Fracht einmal im Ziel, Rückkehr bucht die Karren einmal in der Quelle; Spielstand-Rundlauf mitten auf der Strecke.
5. **Handel:** bestätigter Kaufvertrag mit Bot, angenommene **und abgelehnte** Angebote; keine kostenlose Ware, kein doppeltes Abbuchen, Rückgabe bei Ablehnung.
6. **Gegner & Forschung:** Bot-Zustand/Forschung nach mehreren Spieltagen verändert sich; Götterschutz respektiert die Originalregel; keine Forschung parallel in derselben Siedlung, soweit das der dokumentierte Vertrag vorsieht.
7. **Altspielstand:** den Screenshot-Zustand mit 8×5 und `legacy` laden, ausdrücklich ohne Umrechnung; daneben eine echte Neupartie mit neuem Modus anlegen. Die Modi und Dateien dürfen sich nicht gegenseitig überschreiben.
8. **Testdisziplin:** Einzeltests + der vollständige Sammellauf; 22 dokumentierte **Befunde** klassifizieren, nicht als „22 Fehler“ behaupten. Danach Commit, Protokollzeile, gesicherter Vor-Build, EXE-Neubau und **Start aus einem anderen Ordner**. **Erst danach** den Entwicklungsabschnitt als abgeschlossen melden.

### P1 – Aus Funktionen ein tatsächlich gutes Spiel machen

**P1.1 Sieg/Niederlage neu abstimmen.** Originale Forschungspunkte und Kriegspunkte **unverändert** behalten; separat ein mehrstufiges Einzelspielerziel festlegen. Vorschlag zur **Diskussion, nicht automatisch implementieren**: (a) zwei wirtschaftlich unterschiedliche Siedlungen dauerhaft versorgen, (b) eigene Transportverbindung erfolgreich nutzen, (c) ausgewählte Forschung/Produktionsziele erreichen, (d) eine anspruchsvolle Bot-Situation bewältigen, (e) einen höheren Zielzustand über ein Haltefenster stabil halten. Vorher Simulationsdaten für 30/60/120 Spielminuten erheben. Der Nutzer soll weiterhin als Händler, Forscher oder Feldherr spielen können, ohne zwangsläufig immer denselben Weg gehen zu müssen.

**P1.2 Kampfverluste und Missionen vollständig verdrahten.** `src/kampf.py` und `docs/ENTWURF_KAMPFVERLUSTE.md` anhand des Originalhandbuchs abgleichen. Einzelverluste, Flucht, Karren- und Belagerungsverluste und Rückkehr in den Spielzustand buchen; fast ausgeglichene Schlachten müssen tatsächliche Opfer haben können. Sieger dürfen Beute nur im Rahmen überlebender Transportkapazität mitnehmen. Verlierer verlieren nicht pauschal alle Truppen. Ein **reproduzierbarer Simulationsvergleich** mit mehreren Saatwerten ist aussagekräftiger als ein einzelner Kampf.

**P1.3 Aktive Siedlung und lokale Kosten eindeutig machen.** Bei jeder Bau-, Forschungs- und Ausbildaktion eine Vorschau: **Ort**, **Kosten**, **verfügbar lokal**, eventueller ausdrücklich erlaubter **Reichs-Übergang**, **Fehlbetrag**, **Voraussetzung**, **Dauer**. Beispiele: „Siedlung 1: 15 Holz fehlen lokal; Siedlung 2 besitzt 449,3 Holz. Transport erforderlich“ – nur wenn Regel und Datenlage das tatsächlich hergeben. Kein erfundenes Ersetzen durch Reichsgold.

**P1.4 Karte als Entscheidungsinstrument behandeln.** Spezialkarten schon bei der Gründung in einer vergleichbaren Übersicht: wichtige Erträge, mögliche Engpässe, bebaubare Felder, Preis und benötigte Logistik. **Nicht** zur Standardkarte zurückvereinheitlichen, weil Handel gerade von den Unterschieden lebt. Prüfen, ob „Start + zehn Koloniekarten“ als Pool-Vertrag erfüllt wird; eine Angabe von **neun verbleibenden Karten nach bereits vergebener Kolonie** wäre dabei korrekt.

**P1.5 Gegnerverhalten testbar machen.** Drei definierte Bot-Profile: leicht gibt lange Reaktionszeit; mittel nutzt Ressourcen und einzelne Angriffe sinnvoll; schwer optimiert standortbezogene Wirtschaft und reagiert auf die Position des Spielers. Die genauen Zahlen sind Balancing-Vorschläge. Ein Bot-Log soll **warum** er handelt, ausreichend kurz und bei Bedarf einsehbar erklären.

### P2 – Oberfläche und Atmosphäre polieren

1. **Schriftgröße und Skalierung:** durchgängig größere Fonts, einstellbarer UI-Zoom; 100 %, 125 %, 150 % Windows-Skalierung prüfen. Rot auf Dunkelrot in Navigation und winzige Goldschrift auf Braun sind verbesserungswürdig. Originalpalette erhalten, Kontrast erhöhen.
2. **Weniger Leerlauf, mehr Übersicht:** Kartenansichten sollen verfügbaren Platz ausnutzen; Lager standardmäßig nur Bestand und laufende Produktion zeigen, Nullwerte über Filter. Nachrichten nach Art (Kampf, Wirtschaft, Forschung, Fehler, Hinweise) gruppieren und Serienfehler zusammenfassen.
3. **Klare grafische Gebäudetypen:** wenn die Originalassets keine Unterscheidung bieten, kleine **zusätzliche Symbole** (z. B. Axt, Spitzhacke, Turm, Buch) als Overlay verwenden; **keine fremden Grafiken als angeblich original ausgeben**. Ausbaustufen mit kleinen Stufenmarkierungen, nicht nur winzigen Punkten.
4. **Portal-Darstellung:** nur die tatsächlich eigene Welt grün markieren, falls das die Originalregel ist; freie Positionen, fremde Welten und unbekannte Felder eindeutig unterscheiden. 20×20-Raster ist die Dimension, nicht die Siedlungskarte.
5. **Onboarding:** erster Spielstart zeigt eine kleine, abschaltbare Kette von **fünf sinnvollen Schritten** mit direkter Verlinkung: Feld wählen → erstes Einkommen → lokale Ressourcen → Forschung/Ausbildung → zweite Karte/Transport. Nie in eine separate, seitenlange Anleitung auslagern, wenn die Oberfläche den Hinweis am richtigen Ort geben kann.
6. **Originalatmosphäre:** vorhandenes Titelbild, altmodisches Menü, Originalicons und braun-goldene Farbsprache erhalten. **Modernisieren heißt hier besser bedienen, nicht die Identität austauschen.**

## 7. Konkrete Testfälle, die Hermes neu anlegen sollte

| ID | Fall | Erwarteter Nachweis |
|---|---|---|
| T01 | Legacy-Save von vor dem 8×7-Umbau laden | 8×5 unverändert; sichtbarer Legacy-Hinweis; keine unerwartete Veränderung nach Speichern/Laden. |
| T02 | Frische Partie, zwei neue Siedlungen | Jede neue Karte 8×7, 56 Felder, 40 bebaubar; Sumpf gesperrt; Karten verschieden, Kartenpool korrekt reduziert. |
| T03 | Zwei Wall-Szenarien Stufe 9 und 10 | Kriegspunkte **729** bzw. **1.000** nach Originalregel; Gesamtpunktformel korrekt; Siegentscheidung separat bewertet. |
| T04 | Bürgerwehr in aktivem Ort ohne Holz, Reich hat Holz | Klare Angabe der fehlenden Ressource; Buchung nur gemäß definierter Ortslager-/Übergangsregel; keine verdeckte Gratisversorgung. |
| T05 | Ausbildung startet vor Speichern und endet danach | Genau eine Einheit am richtigen Ort, einmaliger Kostenabzug, richtige Dauer. |
| T06 | Transport während Autosave und manuellem Laden | Kein Güterduplikat, keine verlorenen Karren, keine doppelte Ankunft. |
| T07 | Bot-Handel lehnt bei Ankunft ab | Beide Vertragspartner bekommen gesperrte Werte regelkonform zurück; kein doppelter Abschluss. |
| T08 | Kampf mit knappem Kräfteverhältnis und drei Saatwerten | Beidseitige Verluste und fliehende bzw. überlebende Einheiten konsistent; Aufstellung nach Kampf aktualisiert; Bericht deckungsgleich. |
| T09 | Götterschutz vor und nach erstem Kriegspunkt | Bei erstem Kriegspunkt korrekt beendet; Wallpunkte zählen, wenn sie gemäß Originalregel Kriegspunkte sind. |
| T10 | 15-minütiger beschleunigter Durchlauf, mehrfach speichern | Keine GUI-Hänger/Abstürze, keine doppelten Aufträge, monotone Spielzeit. Zusätzlich längerer Soak-Test sinnvoll. |
| T11 | EXE in leerem Windows-Benutzerprofil aus Fremdverzeichnis starten | Kein Python erforderlich; Passworttor, Laden/Speichern und Ressourcen funktionieren; Pfad mit Leerzeichen erlaubt. |
| T12 | Große Fenster/Skalierung/kleines Display | Kein abgeschnittener Knopf, lesbare Fehlermeldungen, Auswahl und Navigation per Tastatur soweit praktikabel. |

**Prüfdaten:** mit festen Zufallssamen und **echten Startwerten** beginnen, nicht alles künstlich auf 100.000 setzen. Bei Wirtschaftsaktionen zusätzlich **Erhaltungsgleichungen** für Güter, Gold und Karren prüfen. UI-Tests sollen prüfen, was ein Nutzer tatsächlich anklickt, nicht nur, ob ein Modul importiert werden kann.

## 8. Wichtige technische Ratschläge an den leitenden Agenten

### Architektur

- Eine **Regelquelle** je Zahl: originalbelegte Werte aus `data/`, einheitliche Wirtschaftsberechnung, ein Taktgeber. UI zeigt den Kernzustand, sie „berechnet“ keine zweite Wirtschaft.
- `GameState` und die Tkinter-App nicht durcheinanderbringen: Der Projektbericht nennt einen bereits behobenen Fehler mit `self.state` am falschen Objekt. Bestehende geprüfte Verantwortlichkeiten nutzen.
- Ein Auftrag besitzt einen klaren Lebenszyklus: `erstellt → gestartet/gebucht → unterwegs/in Bearbeitung → abgeschlossen/abgelehnt → archiviert`, **jeder Übergang höchstens einmal**.
- UI-Fehlermeldungen sollten strukturiert aus dem Kern kommen: `aktion`, `ort`, `fehlende_ressourcen`, `voraussetzung`, `naechste_moeglichkeit`. Texte werden zentral formatiert, nicht an mehreren Stellen zusammengebastelt.
- Speichern **versionsgebunden**, atomar und mit unveränderter Vorfassung/Backup; Legacy und neuer Modus ausdrücklich unterscheiden. Das Projekt dokumentiert frühere offene Risiken bei gleichzeitigen Schreibern und Dateidauerhaftigkeit – aktuelle Implementierung am Quellcode prüfen, statt alte Vorbehalte als erwiesenen Ist-Fehler zu behandeln.

### Sicherheit und Auslieferung

- Das dokumentierte Passworttor (PBKDF2) ist eine **Zugangshürde**, kein verlässlicher Schutz gegen Extraktion oder Modifikation einer lokal verteilten EXE. Kein Versprechen einer „unknackbaren“ Datei. Falls Spielstandschutz gewünscht ist, braucht es ein separat spezifiziertes Konzept; Passwort-/Schlüsselwerte **nie** in Berichten oder Logs offenlegen.
- Originalbilder und -texte: **Nutzungsrechte klären**, besonders falls das Remake öffentlich verteilt werden soll. Fund im Webarchiv ist nicht automatisch eine Verbreitungslizenz. Diese Empfehlung behauptet **keine** bestehende Rechtsverletzung.
- Build und laufende Sitzung sauber trennen. Geprüfte EXE nicht überschreiben, bevor ein Vor-Build gesichert ist. EXE-Hash und Git-Commit in einer Release-Notiz koppeln.

### Koordination, Qualität und Kosten

- **Keine unnötige Komplettneuschreibung** in anderer Sprache/Engine; der Nutzen rechtfertigt derzeit nicht das Risiko. Tkinter ist für dieses nostalgische, menülastige Spiel verwendbar, solange die Bedienung verbessert wird.
- **Ein kleiner Schritt, ein Test, ein Gesamtlauf, eine Protokollzeile, ein Commit:** diese bewährte Regel beibehalten. Befunde aus dem Sammellauf **einzeln klassifizieren** (bekannter Gap, Vorschlag, Testwarnung, echter Fehler).
- Prüfläufe und Commits sind stärker als Selbstberichte von Unteragenten. Die aufwendigen Fehlererfahrungen im Kontextpaket nicht vergessen (Doppelbuchungen, altes Objekt in UI, versehentlich verschwundene Protokollzeilen, Altregeln in Tests).
- In `PLAN_ASTRA_EINSATZ.md` stehen **historische** Modellkosten und Guthaben. Im **maßgeblichen** Kontextpaket vom 06.10. steht die zuletzt erteilte Freigabe: **nur `deepseek-flash`, keine teuren Modelle, keine Unteragenten, 1 USD DeepSeek-Reserve**, bei Tagesdeckel. Dieses alte Budget ist **keine neue oder aktuelle Zahlungsfreigabe**. Vor größeren kostenpflichtigen Läufen neue Freigabe einholen; wiederverwendbare lokale Tests bevorzugen.
- Den vollständigen Handbuchtext im lokalen Projekt bei jeder Änderung originalbelegter Regeln nachschlagen. Ein älterer Entwurf, der Limbus oder Sieg anders interpretiert, darf die 06.10.-Entscheidungen nicht heimlich überschreiben.

## 9. Minimaler Meilensteinplan bis zur ersten wirklich guten Partie

| Meilenstein | Ergebnis | Abnahme durch Auftraggeber |
|---|---|---|
| **M1 – Wirtschaft aktiv** | Schritt 10 integriert, frische Ökonomie läuft, Speicherstände sicher, keine Doppelbuchungen. | Ein 20–30-minütiger Aufbau mit sichtbaren Ortslagern und einer Herstellung/Ausbildung. |
| **M2 – Logistik sinnvoll** | Spezialisierte zweite Siedlung und eigener Transport erzeugen tatsächlichen Nutzen. | Der Spieler kann den Vorteil und den Preis des Transports ohne Handbuch erklären. |
| **M3 – Gegner/Kampf wirksam** | Bots handeln und reagieren, Kampfschäden/Beute gelangen korrekt in den Zustand. | Ein echter Angriff und ein Gegenangriff mit erklärbarem Bericht. |
| **M4 – Ziel und Balance** | Originalpunkte korrekt, eigenständige Sieg-/Niederlagebedingung und sinnvolles Pacing. | Zwei unterschiedliche erfolgreiche Strategien; kein früher Sofortsieg nur durch Wallpunkte. |
| **M5 – Verständlich und veröffentlichbar** | Lesbare Oberfläche, klare Meldungen, funktionsfähige portable EXE, keine Entwicklerstarter-Verwechslung. | Neuspieler kann ohne Hermes ein Spiel beginnen, speichern und sinnvoll fortsetzen. |

**Wichtig:** Diese Meilensteine sind eine **Empfehlung für die Zeit nach Schritt 10** und ersetzen die bisherige Hermes-Roadmap nicht automatisch. Hermes soll zuerst seine **bereits verbindlich festgelegte offene Aufgabe** abschließen, danach Änderungen mit dem Auftraggeber priorisieren.

## 10. Offene Entscheidungen, die Hermes nicht eigenmächtig treffen soll

1. **Was ist langfristig ein Sieg?** Reiner Punktesieg, gestuftes Wirtschafts-/Forschungs-/Militärziel, mehrere Spielmodi oder eine frei weiterspielbare Sandbox? **Meine Empfehlung:** Sandbox plus optionales anspruchsvolles Kampagnenziel; 300 Punkte als Testmarker kennzeichnen.
2. **Wie sichtbar soll Kampf laufen?** Sofort berechneter Bericht und optional Schritt-für-Schritt-Wiedergabe sind sinnvoll; keine Änderung der belegten Kampfreihenfolge.
3. **Wie stark darf die Einzelspieler-Zeitbeschleunigung sein?** Aktuell steht oben `Tempo ×180`, `1 Std = 20 s`; mathematisch ist das konsistent, für neue Spieler kann es zu hektisch sein. Tempoauswahl sollte leicht und jederzeit erreichbar bleiben.
4. **Wieviel Bequemlichkeit bei lokalen Lagern?** Echten Transport nicht durch automatischen Reichsbestand entwerten. Nur Übergangsmechaniken verwenden, die ausdrücklich Teil der Migrations-/Legacy-Regeln sind.
5. **Sollen Originalnetz-Menüpunkte wie Forum/Chat/Spieler werben/Logout weiter sichtbar sein?** Auf den Screenshots sind sie noch da, der Einzelspielerplan sah echte Netzfunktionen als entbehrlich. Entweder sinnvoll lokal umdeuten oder konsequent aus dem aktiven Menü nehmen; keine toten Links.
6. **Welche Optik ist unverhandelbar?** Originalfarben und charakteristische Icons erhalten; Verbesserungen bei Lesbarkeit, Gebäudedifferenzierung und Kartengröße gezielt freigeben.

## 11. Kurze Übergabe an Hermes – verbindlicher Bewertungsimpuls

> **Hermes, dieses Dokument ist eine externe Bewertung, kein Befehl, wahllos alles umzubauen.** Grundlage ist der nachweisbar identische EXE-Build vom **06.10.2026** und die Bildbeobachtung vom **23.10.2026**; die gezeigte Partie ist **Legacy**. Dein maßgeblicher nächster Schritt bleibt **Schritt 10: `tick_bis`, einheitliche Uhr und Aktivierung der neuen Ökonomie** nach dem lokalen Entwurf. Berichte vor einer Änderung, welche Tests du für die komplette Ereignisschleife, Altspielstände, Ortslager, Transport, Ausbildung, Handel und Bots ergänzt. **Nicht als Bugs melden:** 8×5 in einem Legacy-Save oder 1.000 Kriegspunkte aus einem Wall Stufe 10. **Sehr wohl priorisieren:** zu frühes/unklares Siegziel, nicht erklärte lokale Ressourcenknappheit, fehlende systemübergreifende Kampfverluste, redundante Warnungen und schwache Karten-/Portal-Lesbarkeit. Nach Abschluss von Schritt 10 den echten Verlauf einer Neupartie prüfen, dann mit dem Auftraggeber über Ziel/Balance entscheiden. Originalregeln bleiben Originalregeln; Vorschläge werden als Vorschläge dokumentiert. Bestehende Tests, Commits, Sicherungen, Modell-/Kostenregeln und das unveränderte Gesamtziel behalten Gültigkeit.

## 12. Schlussfazit

**Ja: Dieses Spiel lohnt sich aus meiner Sicht weiterzuentwickeln.** Sein stärkster Vorzug ist nicht die Grafik, sondern die Kombination aus alter Nebelseetal-Identität, standortabhängiger Wirtschaft, lokalem Transport, originalem Kampfregelsystem und einer ungewöhnlich transparenten Entwicklungsdokumentation. Damit kann ein eigenständiges Einzelspieler-Strategiespiel entstehen.

**Was ich zuerst verbessern würde:**

1. **Schritt 10 belastbar abschließen** – sonst bleiben die verschiedenen gelungenen Systeme nebeneinander stehen.
2. **Spielziel und Punkte trennen** – damit ein Verteidigungswall nicht schon das strategische Spiel beendet.
3. **Die lokale Wirtschaft verständlich machen** – der Spieler muss wissen, welche Ressource **wo** fehlt und was er dagegen tun kann.
4. **Kämpfe, Transporte und Bots wirklich ineinandergreifen lassen** – erst daraus entsteht Spieltiefe.
5. **Danach** Lesbarkeit, Kartenansicht und Atmosphäre verbessern – ohne das alte Nebelseetal auszutauschen.

**Die größte Gefahr ist zurzeit nicht fehlender Code, sondern vorschnelles „fertig“:** Ein nachgewiesener Start, tausende grüne Einzeltests und eine hübsche Karte sind wertvoll. Ein gutes Strategiespiel ist es dann, wenn ein Spieler über mehrere Sitzungen verständliche, schwierige Entscheidungen treffen, deren Folgen sehen und eine vollständige Partie fehlerfrei zu Ende führen kann.

---

**Nachweisgrenze:** Ich habe die bereitgestellten Bild- und Textdateien und den EXE-Hash überprüft, aber **keine Windows-Laufzeitprüfung**, **keinen vollständigen Quellcode-Audit**, **keinen reproduzierten 4.061-Test-Sammellauf** und **keinen vollständigen Langzeitdurchlauf** durchgeführt. Alles, was diese Prüfungen voraussetzt, ist oben ausdrücklich als Dokumentationsaussage, Annahme oder neuer Prüfauftrag bezeichnet. Diese Ehrlichkeit ist Teil der Bewertung.
