# Vollständiges Fehlerregister und Reparaturwege (GPT, 28.10.2026)

**Quellenhierarchie:** Originalspielanleitung (`docs/original/Nebelseetal_Spielanleitung_2009.pdf`, Deckblatt 01.09.2006) > Daniels ausdrücklich entschiedene Remake-Werte/Schritte > als **Vorschlag** markierte Preise/Zeiten. Die beigefügten `docs/`-Pläne und neuester Code-Stand sind entscheidend. Nur Hermes ändert gemeinsame Dateien. **„Befund“ bedeutet reproduziert, nicht behoben.** Alle Zeilen sind auf den übergebenen ZIP-Code-Stand bezogen, nicht auf zukünftige Commits.

## Bestätigte Fehler

### F01 — Reichs-/Ortsbestand wird doppelt als Geldquelle behandelt [KRITISCH, neue Reproduktion]
- **Quelle:** `src/main.py`: `GameState.tick` schreibt lokale Ertragsdifferenz auch nach `resources[res].amount` (um Z. 2069–2072). `ortsdeckung`, `reichsdeckung`, `verbrauche_am_ort`, `verbrauche_reichsweit` verwenden diese `resources` später als **zusätzliche** eigenständige Geldquelle (ca. Z. 903–998). Dasselbe Risiko besteht mit `population` + `bevoelkerung`.
- **Echte Probe:** `test_gpt_doppelkasse.py` baut einen Holzfäller auf Wald und tickt 3600 Spielsekunden. Im einzigen Ort entstehen nach Original **4 Holz**. Reichsanzeige wird ebenfalls auf **4** gesetzt. Danach akzeptieren sowohl lokaler als auch reichsweiter Zahlweg **7 Holz** – mehr als physisch vorhanden. Zwei Warenbestände wurden aus einer Ernte erzeugt; eine Buchung kann den Spiegel auseinanderziehen. Auch 5 tatsächliche Siedler + gespiegelte 5 werden zu fälschlichen 10 verfügbaren Siedlern addiert.
- **Fixweg (Hermes):** Zuerst Entscheidung für eine **einzige** führende Bestandsquelle je Spielmodus. Im Neumodus `oeokonomie-1` ausschließlich lokale `Settlement.vorraete` und `bevoelkerung` als physische Lager; Reichsübersicht als **berechnete Anzeige**, nicht eine zweite Kasse. `tick` soll keine zusätzliche freie Ernte schaffen; Tests gegen Produktion im Ort und UI-Summendarstellung nachziehen. Bei global wirklich erlaubten Aktionen klaren Ort/Quellmenge und echte Abbuchungsorte festlegen (z. B. Mana-Kosten nach Original nachprüfen). Für `legacy` getrennte, nicht-destruktive Behandlung und Save-Migration. Vorab Deckung, danach atomare Abbuchung, nie negativ. **Nicht** einfach nur die globale Zuwachsbuchung löschen, solange andere Leser davon abhängen.
- **Abnahme:** `test_gpt_doppelkasse.py --strict` grün (5 bisher fehlschlagende Erwartungen); 4 Holz nach 1 h, Zahlung 7 Holz verweigert, Siedler nicht doppelt; Save/Load, alle Ressourcenzähler, Bau/Transport/Handel/Kampfbeute prüfen.
- **Abhängigkeit:** F02 ist ein **Folgefehler desselben Kassenkonzepts**. Gemeinsamen Fix planen, sonst verbleiben Scheineinkünfte.

### F02 — Ortsfremder Bau ohne Karren durch globale Übergangskasse [HOCH, reproduziert]
- **Quelle:** `src/main.py`: `ortsdeckung()` und `verbrauche_am_ort()` ergänzen fehlendes Ortsholz aus `GameState.resources`, selbst bei `mode='oeokonomie-1'`.
- **Echte Probe:** Dorf A 0 Holz, Dorf B 100 Holz, Reichsressource 100 Holz. `ortsdeckung(A,{'holz':10})` meldet keine Fehlmenge; `verbrauche_am_ort(A,{'holz':10})` liefert `True`; B behält 100 Holz, der Reichszähler sinkt nur 100→90. Es existiert **kein** Karren-/Transportauftrag.
- **Fixweg:** Derselbe F01-Hauptpatch macht Ortsbau im Neumodus strikt ortsgebunden; nur eine abgeschlossene Transportmission erhöht das Ziellager. Übergangskasse `legacy` **nicht** ohne Migration entfernen. Bei globalen Aktionen Quelle/Empfänger und Recht auf Teilzahlungen explizit festlegen, damit keine „Fernkasse“ entsteht.
- **Abnahme:** `test_gpt_integrationsrisiken.py --strict` grün für die beiden Ortskassenproben; zusätzlich echter Versand mit Handkarren → Ankunft → Rückkehr; Fehlbuchung vor Ankunft weiterhin unmöglich.

### F03 — Farm ohne Baukunst auf Grasland gebaut [HOCH, reproduziert]
- **Original:** Handbuch Siedlungs-Baumenü: frei ab Start sind **Holzfäller, Steinmetz, Jäger, Bibliothek, Haus**. Weitere Gebäude benötigen Kenntnisse in **Baukunst**.
- **Quelle:** `src/main.py`: `bauen_auf_karte(siedlung,'farm',feld)` prüft Feld, Gelände, Limit, nicht den Forschungsstand; UI `_karten_bauen()` ruft den Weg ohne Baukunst-Check auf. Test mit Grasland und 0 Baukunst ergibt `True`.
- **Fixweg:** Zentrale `bau_zulassen`-Prüfung **vor Feldmutation und Abbuchung**, die die erforderliche Forschungsstufe über die vorhandene Forschungsquelle ermittelt. Engine+GUI dieselbe Funktion verwenden, Baupreise/Feld/Limit weiter prüfen. Keine späteren Altbauten automatisch abreißen. Optional Bauaktion **atomar** gestalten (Bezahlung und Platzierung als eine Transaktion), damit ein abgelehnter Bau nichts verändert.
- **Abnahme:** `test_gpt_integrationsrisiken.py --strict` (Farm nicht baubar ohne Baukunst, Holzfäller frei, Sumpf gesperrt), zusätzlich Baukunst vorhanden → Farm möglich, ungenügende Ortspreise → keine Feldänderung.

### F04 — Mehrere ganze Tage in einem Tick nur als EIN Tag gezählt [HOCH, GPT-001]
- **Quelle:** `GameState.tick()`, um Z. 2091: `_day_accum += dt_seconds; if _day_accum >= 86400: ...; day += 1`.
- **Echte Probe:** 7 Tage (=604800 s) als ein einziger Tick: `day == 2` statt `8`, `_day_accum == 518400` statt `0`; Götterschutz bleibt aktiv, obwohl nach Handbuch nach 7 Tagen enden muss (wenn nicht bereits der erste Kriegspunkt ihn beendet). Dieselben 7 Tage als sieben Einzel-Ticks liefern `day == 8` und beendeten Schutz.
- **Fixweg:** `divmod(_day_accum + dt_seconds, 86400)` oder gleichwertige ganzzahlige Tagesanzahl statt `if`. Historische übergroße `_day_accum` in Altständen nicht ohne Migrationsprüfung uminterpretieren. Götterschutz für Null-Kriegspunkte und ersten Kriegspunkt separat prüfen.
- **Abnahme:** `test_gpt_tageswechsel.py --strict`, gemischte kleine/große Ticks, Speicherstand und Schutz; die 8 Befunde sind Varianten *einer* Ursache.

## Nachgewiesene Integrations-/Abnahme-Lücken (nicht als eigene Logikfehler ausgeben)

### A01 — EXE entspricht nicht letztem Quellcode [RELEASE-FREIGABE OFFEN]
- Die mitgelieferte EXE `c1523670...` entspricht der am 06.10. um 08:22 dokumentierten Version, während der neue Quellcode danach `tick_bis()` in `GameState.tick()` verdrahtet (ZIP-Commit `1c4dffa...`). Die Screenshots vom 23.10. zeigen nach Daniels Auskunft den damaligen Stand; keine jüngere Entwicklung.
- **Aktion:** Erst Hermes' laufenden Schritt fertigstellen, dann kontrolliert neu bauen, echte EXE aus fremdem Arbeitsverzeichnis starten und Hash/Commit/Testprotokoll festhalten. **Keine** Behauptung, neuere Quelle sei schon in aktueller EXE.

### A02 — Durchspiel/Balance nicht hinreichend belegt [RISIKO, kein bewiesener Einzeldefekt]
- Originalraten im Code stimmen in Stichproben (77 Kontrollen), aber das beweist **nicht**, dass ein Spieler Holz, Stein, Nahrung, Metall, Leder, Wolle, Pferde und Mana in jeder erlaubten Baufolge in sinnvoller Menge erreichen kann. Daniels beobachtete Sackgassen sind ernst zu nehmen; einzelne davon können aus F01/F02 folgen.
- **Aktion:** Für neue Startspiele alle Kartentypen, einige deterministische Seeds, 0/1/6/24/72 Spielstunden und typische Bau-/Forschungsfolgen simulieren. Vergleiche Ort vs. Reich, offene Felder, fehlende Waren, Warteschlangen und Karrenverfügbarkeit. Testziel ist **Planbarkeit**, nicht Unbesiegbarkeit jeder ungünstigen Entscheidung. Warnhinweise statt kostenlose Rettungsrohstoffe. Nur **Vorschlagspreise/Dauern** anhand gemessener Pacing-Ziele kalibrieren; nie Originalstundenraten still ändern.

### A03 — Sieggrenze 300 Punkte gegen Originalwallpunkte [DESIGNPRÜFUNG]
- Originalregel ist `Kriegspunkte += Wallstufe³`, Gesamtpunkte `(Krieg+Forschung)/2`. Stufe 10 bringt also **korrekt 1000 Kriegspunkte**, kein Wertefehler. Ein Sieg bei 300 Gesamtpunkten ist dagegen eine Remake-Zielzahl und kann die Mehrsiedlungs-Wirtschaft zu früh beenden.
- **Aktion:** Hermes soll die Erreichbarkeit über einen echten Spieldurchlauf messen; höchstens eine Entscheidungsvorlage für Daniel, kein selbstständiges Regelüberschreiben.

### A04 — Kartenvorrat-Projektwiderspruch [ENTSCHEIDUNG OFFEN]
- Dokumentation nennt „Startkarte + 10 Karten“, die geprüften Vorlagen ergeben „Startkarte + 9“ = 10 Kartentypen (8×7, 40 Baufelder). **Nicht** still eine Karte erfinden oder die Historie umschreiben. Im neuen laufenden Projekt prüfen, ob explizit bereits behoben.

### A05 — Nicht vollständige plattformgerechte Endabnahme [TESTLÜCKE]
- 21 ältere Basistests wurden einzeln versucht: 18 Exit 0, zwei GUI-Tests brauchten Display, einer Windows `TEMP`; ein angefangener Xvfb-Sammellauf wurde nicht abgeschlossen. Das sind **keine bestätigten Spielefehler**, aber keine Grundlage für ein freigegebenes Build.
- **Aktion:** `run_tests.bat` auf Windows; echte 15-Minuten-Partie, Neustart, Laden, Sieg/Niederlage, Transport+Kampf, Langzeit-/Mehrtick-Test, Leerlauf/Freeze-/Prozesszahl prüfen.

## Ausdrücklich KEINE Fehler
- 8×5 auf alten `legacy`-Screenshots, obwohl die neue Vorgabe 8×7 lautet: Legacy-Karte kann bewusst unverändert sein. **8×7 nur für neue Partien verifizieren.**
- 1000 Kriegspunkte durch einen Verteidigungswall Stufe 10: **korrekte Originalrechnung**.
- 28 Originaleinheiten, 17 Waren, 21 Forschungen und die getesteten Produktionserträge: nach den unabhängigen Kontrollen aktuell konsistent. Die vollständigen Laufzeitwirkungen jeder Einheit sind **nicht** damit bewiesen.

## Wichtigste Dateien / Prüfungen
- `01_TESTS/tests/test_gpt_doppelkasse.py` → F01 (Normalmodus 4 OK / 5 Befunde, strict 5 erwartete Fehler)
- `01_TESTS/tests/test_gpt_integrationsrisiken.py` → F02/F03 (Normalmodus 4 OK / 3 Befunde, strict 3 erwartete Fehler)
- `01_TESTS/tests/test_gpt_tageswechsel.py` → F04 (Normalmodus 13 OK / 8 Befunde, strict erwartete Fehler)
- `01_TESTS/tests/test_gpt_originaltreue.py` → Originaldaten (77 OK)
- `01_TESTS/tests/test_gpt_produktion_truppen_kette.py` → Daten-/Kettenplausibilität (171 OK)
- `01_TESTS/tests/test_gpt_versorgungsdiagnose.py` → Diagnose (15 OK)
- `03_BELEGE/` alle echt erfassten Ausgaben.
