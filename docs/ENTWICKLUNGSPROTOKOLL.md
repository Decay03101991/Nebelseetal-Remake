# Entwicklungsprotokoll — Nebelseetal Remake (ab 02.11.2026) - neues Heft ab 17.11.2026, 20:32

**Wozu:** Daniel schreibt das Entstehen des Spiels mit. Kurz und mit Beleg: die wichtigsten Schritte und ihre Kennungen — kein Tagebuch.
**Regeln für dieses Protokoll:**
- Nach jedem groben Schritt eine Zeile — immer hinten anhängen.
- Genau eine Zeile je grobem Schritt (das hält es übersichtlich).
- Fehler und Irrwege gehören hinein.
- Sicherungen stehen nicht hier (die gehören nach `archiv/dokumentation/projektunterlagen_historisch/SICHERUNGEN.md`).
- Kosten nur gemessen, nie geschätzt.
- Im oeffentlichen Repo steht hier nur der GROBE Schritt; die Einzelheiten stehen als Kommentar neben dem Code (Daniel, 04.11.2026).
- Zielgröße: deutlich unter 320 Zeilen. Wird sie überschritten, wird ein NEUES Heft begonnen (Daniel, 06.11.2026) — das alte wandert vollständig ins Archiv, nichts wird gekürzt.

**Heftwechsel statt Verdichtung (Vorgabe Daniel 06.11.2026, zweiter Wechsel 17.11.2026).** Dieses Heft beginnt am 17.11.2026, 20:14 mit dem LETZTEN Eintrag des vorigen Hefts, damit die Naht lückenlos ist. Die früheren Hefte liegen unverändert und vollständig, nichts gelöscht, nichts gekürzt (Daniel 17.11.2026: Protokoll auslagern, 353 Zeilen überschritten die Zielgröße von 320):

| Heft | Inhalt | Pfad |
|---|---|---|
| Protokoll bis 06.11.2026 | alles vom 02.11.2026 bis 06.11.2026, 13:49 (319 Zeilen) | `archiv/dokumentation/protokoll_alte_fassungen/ENTWICKLUNGSPROTOKOLL_BIS_20261106.md` |
| Protokoll bis 17.11.2026 | alles vom 06.11.2026, 13:49 bis 17.11.2026, 20:14 (353 Zeilen) | `archiv/dokumentation/protokoll_alte_fassungen/ENTWICKLUNGSPROTOKOLL_BIS_20261117.md` |
| Historie bis 01.11.2026 | Tag 1 bis zum Schnitt am 02.11.2026 | `docs/ENTWICKLUNGSPROTOKOLL_HISTORIE_BIS_20261101.md` |
| Historie 02.11. bis 03.11.2026 | die Sektionen HERMES-KARTE-01 bis HERMES-BOTDORF-06 | `docs/ENTWICKLUNGSPROTOKOLL_HISTORIE_20261102_bis_20261103.md` |
| Vorfassung 05.10.2026 | der Stand vor der ersten Verdichtung | `archiv/dokumentation/protokoll_alte_fassungen/ENTWICKLUNGSPROTOKOLL_VOR_VERDICHTUNG_2026-10-05.md` |

**Wegweiser:** der Einstieg in alle Dokumente steht in `docs/INDEX.md`. Die Wache `tests/test_protokoll.py` prüft, dass dieses Heft klein bleibt, dass jedes Heft zusammen vollständig ist und dass die Naht stimmt (erster Eintrag hier = letzter Eintrag dort).

## Vorgeschichte
Alles vor dem 17.11.2026, 20:14 steht im Heft `archiv/dokumentation/protokoll_alte_fassungen/ENTWICKLUNGSPROTOKOLL_BIS_20261117.md` (und davor in `…_BIS_20261106.md` sowie den beiden Historienheften, siehe Tabelle oben). Dieses Heft führt ab dem 17.11.2026, 20:14 weiter.

| Zeit | Schritt | Ergebnis / Belege |
|---|---|---|
| 20:14 | **Befund: die Registerkette endet am 12.11.2026 bei Zeile 542 - die Nummern 543 bis 649 stehen nur im Protokoll (gemessen, nicht uebernommen)** | **Messung:** `docs/PRUEFREGEL_ORIGINAL.md` endet mit Zeile `| 542 |`, letzte Aenderung 12.11.2026 22:04 (Commit `206560d`), 707.780 Byte. Die hoechste Zeilennummer der Tabelle ist **542**. Eine Suche nach `^| 6[0-4][0-9] |` ueber den GANZEN Projektbaum liefert **0 Treffer** - die in Protokoll und Uebergaben zitierten Nummern 543 bis 649 (z. B. „Register 647“ fuer F-91) haben **keine Tabellenzeile**. **Auswirkung:** wer „Register 649“ nachschlagen will, findet nichts; die Zusage „Register und Protokoll gehoeren zum Fix“ ist ab 543 nur zur Haelfte erfuellt. **Nicht geaendert:** die Registerdatei wird von `src/kampf.py`, `src/spieloekonomie.py` und mehreren Werkzeugen gelesen - ein Anbau ohne Daniels Wort waere ein Eingriff in eine fuehrende Datei. **Vorschlag:** entweder die 107 fehlenden Zeilen nachtragen oder eine Kopfzeile, die die Fortsetzung im Protokoll nennt. |
| 20:2x | **F8 gebaut: vier Fensterwachen melden bei zu kleinem Bildschirm „nicht pruefbar“ statt rot** (Register 651) | Daniels Wort (einzeln gestellt): „Ja - Flaeche messen, bei zu kleinem Fenster nicht pruefbar melden“. Neue Hilfe `harness.flaeche_gross_genug(root, breite, hoehe)` misst das ECHTE Fenster und schreibt bei zu kleiner Flaeche einen Befund mit verlangt / gemessen / Schirmgroesse; die vier Wachen rufen sie vor ihren Geometrie-Zusagen (`test_siedlungsansicht_a9` an zwei Fensterstellen, `_a10` im Kern samt zwei Aufrufern, `test_dorfzentrum_ansicht`, `test_dorfzentrum_geometrie`). Bei normalem Schirm unveraendert scharf: a9 **39/0/0**, a10 **48/0/0**, dorfzentrum_ansicht **47/0/1**, dorfzentrum_geometrie **39/0/1**. Gegenprobe der Hilfe: 1200 x 800 -> gross, 4000 x 3000 -> Befund (Fenster 1400 x 900, Schirm 800 x 600). |
| 20:32 | **Heftwechsel: das Heft vom 06.11. bis 17.11. ist vollstaendig im Archiv, neues Heft mit Naht begonnen** (Daniel 17.11.2026: Protokoll auslagern) | 353 Zeilen lagen ueber der Zielgroesse 320. Archivheft `archiv/dokumentation/protokoll_alte_fassungen/ENTWICKLUNGSPROTOKOLL_BIS_20261117.md` (**287.506 Byte, 353 Zeilen**, nichts gekuerzt); erster Eintrag hier ist woertlich der letzte dort. Wache `tests/test_protokoll.py` umgestellt: Archivhefte werden gezaehlt (Glob `ENTWICKLUNGSPROTOKOLL_BIS_*.md`), die Naht gilt gegen das juengste, Inhalt und Belegbarkeit gegen alle zusammen - vorher **27 bestanden, 1 Fehler** (Naht), nachher **28 bestanden, 0 Fehler, 1 Befund**. `tools/pruefe_protokoll.py` zaehlt die Hefte schon per Glob, keine Aenderung noetig. Register 652. |
