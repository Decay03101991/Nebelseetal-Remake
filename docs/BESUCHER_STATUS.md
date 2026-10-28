# Spielstatus fuer Besucher

**Stand 28.10.2026: experimenteller konsolidierter Entwicklungsstand GPT-FIX02; kein Release.**

Diese lokal verpackte Fassung ist **nicht automatisch** auf GitHub veroeffentlicht. Die oeffentliche GitHub-Version wurde von Daniel zu einem frueheren Stand hochgeladen. Ein Upload dieser Fassung erfolgt nach ausdruecklichem Wunsch **erst nach Abschluss der Fehlerarbeiten und Sicherheitspruefung**.

| Bereich | Gepruefter Stand | Noch offen |
|---|---|---|
| 127 Originalkarten, 10x10 | Als echte Bilder aktiv; 100 Kartenfelder klickbar | 25 Raster manuell grafisch abnehmen |
| Ortslager, Baukosten, Forschungsregeln | Gezielte GUI-/Wirtschaftstests erfolgreich, Kosten kommen aus dem Ortslager | Historische Baumenue-Grafik und uebrige alte Pruefungen abgleichen |
| Handel, Kampf, Ausbildung, Transport, Werkstatt | Ausgewaehlter End-to-End-Test: 64 bestanden, 0 Fehler, 2 Befunde | Botstrategie, weitere reale Spielszenarien und Windows-Abnahme |
| Spielerslots und Speichern/Laden | Gezielte Regressionen bestanden | Vollstaendige Windows-Bedienpruefung |
| Windows EXE | Bauablauf vorbereitet | Noch keine neu erstellte/gepruefte Windows-EXE |

Insgesamt wurden 25 **ausgewaehlte** Testdateien erfolgreich ausgefuehrt, einschliesslich 4 neuer Originalkarten-Baukassen-Kontrollen. Das ist **nicht** die gesamte Testsuite und kein Freigabenachweis.

Details: [Aktueller Entwicklungsstand](AKTUELLER_STAND.md), [Baumenue-Referenz](BAUMENUE_ABGLEICH.md), [Entwicklungsprotokoll](ENTWICKLUNGSPROTOKOLL.md).
