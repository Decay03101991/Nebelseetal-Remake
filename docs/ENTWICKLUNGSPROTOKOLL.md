# Entwicklungsprotokoll — Nebelseetal Remake (ab 02.11.2026) - neues Heft ab 06.11.2026, 14:20

**Wozu:** Daniel schreibt das Entstehen des Spiels mit. Kurz und mit Beleg: die wichtigsten Schritte und ihre Kennungen — kein Tagebuch.
**Regeln für dieses Protokoll:**
- Nach jedem groben Schritt eine Zeile — immer hinten anhängen.
- Genau eine Zeile je grobem Schritt (das hält es übersichtlich).
- Fehler und Irrwege gehören hinein.
- Sicherungen stehen nicht hier (die gehören nach `archiv/dokumentation/projektunterlagen_historisch/SICHERUNGEN.md`).
- Kosten nur gemessen, nie geschätzt.
- Im oeffentlichen Repo steht hier nur der GROBE Schritt; die Einzelheiten stehen als Kommentar neben dem Code (Daniel, 04.11.2026).
- Zielgröße: deutlich unter 320 Zeilen. Wird sie überschritten, wird ein NEUES Heft begonnen (Daniel, 06.11.2026) — das alte wandert vollständig ins Archiv, nichts wird gekürzt.

**Heftwechsel statt Verdichtung (Vorgabe Daniel 06.11.2026).** Dieses Heft beginnt am 06.11.2026 mit dem LETZTEN Eintrag des vorigen Hefts, damit die Naht lückenlos ist. Die früheren Hefte liegen unverändert und vollständig, nichts gelöscht, nichts gekürzt:

| Heft | Inhalt | Pfad |
|---|---|---|
| Protokoll bis 06.11.2026 | alles vom 02.11.2026 bis 06.11.2026, 13:49 (319 Zeilen) | `archiv/dokumentation/protokoll_alte_fassungen/ENTWICKLUNGSPROTOKOLL_BIS_20261106.md` |
| Historie bis 01.11.2026 | Tag 1 bis zum Schnitt am 02.11.2026 | `docs/ENTWICKLUNGSPROTOKOLL_HISTORIE_BIS_20261101.md` |
| Historie 02.11. bis 03.11.2026 | die Sektionen HERMES-KARTE-01 bis HERMES-BOTDORF-06 | `docs/ENTWICKLUNGSPROTOKOLL_HISTORIE_20261102_bis_20261103.md` |
| Vorfassung 05.10.2026 | der Stand vor der ersten Verdichtung | `archiv/dokumentation/protokoll_alte_fassungen/ENTWICKLUNGSPROTOKOLL_VOR_VERDICHTUNG_2026-10-05.md` |

**Wegweiser:** der Einstieg in alle Dokumente steht in `docs/INDEX.md`. Die Wache `tests/test_protokoll.py` prüft, dass dieses Heft klein bleibt, dass jedes Heft zusammen vollständig ist und dass die Naht stimmt (erster Eintrag hier = letzter Eintrag dort).

## Vorgeschichte
Alles vor dem 06.11.2026, 13:49 steht im Heft `archiv/dokumentation/protokoll_alte_fassungen/ENTWICKLUNGSPROTOKOLL_BIS_20261106.md` (und davor in den beiden Historienheften, siehe Tabelle oben). Dieses Heft führt ab dem 06.11.2026 weiter.

| Zeit | Schritt | Ergebnis / Belege |
|---|---|---|
| 13:49 | **Guthaben (von Daniel abgelesen) und Uebergabe dieser Sitzung** | Daniel 13:49: Guthaben **9,06 USD**, Gesamtverbrauch **60,93 USD** (09:04 zu Sitzungsbeginn: 10,31 / 59,68 - also 1,25 USD in dieser Sitzung, davon 0,11 USD der Ablauf-Entwurf der Vorsitzung und rund 0,07 USD der Konzept-Aufruf). Uebergabe `UEBERGABE_NEBELSEETAL_20261106_1355.md` liegt (Byte-Zahl und SHA256 werden beim Abholen beidseitig mit `sha256sum` geprueft, nicht aus diesem Text uebernommen) auf dem Desktop und hashgleich in `D:\Arbeiten\Hermes\Uebergaben\20261106_1355\`; naechste Sitzung `06.11.26_V_0.0.3_Session_9`. Offen und ausdruecklich benannt: der Push nach GitHub (blockiert, braucht Zustands-Zustimmung) und die gestagte Skill-Aktualisierung (`8e7a9b56`). |
| 14:20 | **Neues Protokoll-Heft begonnen, altes vollständig ins Archiv** (Daniel 06.11.2026) | Das bisherige Heft (319 Zeilen, 06.11.2026 13:49) liegt unverändert als `archiv/dokumentation/protokoll_alte_fassungen/ENTWICKLUNGSPROTOKOLL_BIS_20261106.md`; der erste Eintrag hier ist wörtlich der letzte Eintrag dort (Naht lückenlos). Verweise: Tabelle im Kopf und `docs/INDEX.md`. Wache `tests/test_protokoll.py` umgestellt: Vollständigkeit und Belegbarkeit gelten für aktives Heft + Historienhefte + Archiv ZUSAMMEN; neu geprüft wird die Naht (erster Eintrag = letzter Eintrag des Archivs) und dass das Archiv selbst existiert. `tools/pruefe_protokoll.py` zählt das Archiv mit. |
| 14:35 | **Logo des Spiels in der Besucheransicht, Urheber im Repo genannt** (Vorgabe Daniel 06.11.2026) | Das Banner mit dem Schriftzug NEBELSEETAL hat **Herr Chris Fred Däubner** für Daniel Kössl entworfen - das steht jetzt an drei Stellen: auf der Besucherseite (`index.html`, unter dem Logo und in der Fußzeile), in `README.md` (Bild im Kopf, Abschnitt Rechte mit Urheberrecht) und in `assets/referenzbilder/README.md`. Ablage: Original `assets/referenzbilder/Logo_Nebelseetal_20261106.png` (3500 x 3500, freigestellt, 6,6 MB, SHA256 `a6ac2e1c372c…`), web-optimiert `assets/bilder/logo_nebelseetal_klein.png` (1.294 KB) und `.webp` (309 KB, 1600 x 754). Vorerst NUR in der Besucheransicht - wo es sonst genutzt wird, entscheidet Daniel später. |
