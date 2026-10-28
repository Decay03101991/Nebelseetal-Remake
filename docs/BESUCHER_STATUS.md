# Nebelseetal Remake – Entwicklungsstatus für Besucher

**Stand dieser Zusammenfassung: 28.10.2026.** Grundlage ist die bereitgestellte Kopie des Hermes-Hauptprojekts; die letzten konkret belegten Entwicklungsprotokoll-Einträge darin stammen vom **06.10.2026, zuletzt 08:49 Uhr**. Die erstmalige GitHub-Veröffentlichung ist **kein zusätzlicher Funktions- oder Releasetest**.

> Dieses Dokument ordnet den veröffentlichten Projektstand ein. Die isolierte GPT-Vorausarbeit vom 28.10.2026 ist **nicht automatisch** Bestandteil des veröffentlichten Spielcodes. Aussagen über die frühere EXE und frühere Prüfläufe sind historische Ergebnisse und keine heutige Abnahme.

## Spielbereiche

| Bereich | Stand im veröffentlichten Hauptprojekt | Noch offen / Einschränkung |
|---|---|---|
| Spielstart und Passwort | Startskript und lokales Passworttor sind implementiert; jeder Nutzer legt sein eigenes Passwort fest | Lokale Passwortprüfung lässt sich bei offenem Quellcode umgehen; kein zentraler Zugangsschutz |
| Welt und Siedlungskarten | Karten- und Siedlungssystem, Geländeregeln, mehrere Siedlungen sowie grafische Ansichten sind vorhanden | Darstellung und Kartenbalance noch nicht vollständig von Menschen abgenommen; historische Planstände können abweichen |
| Gebäude und Rohstoffe | Gebäude, Grundproduktion, Ortslager und Reichsbestände sind programmiert | Ein Teil der Wirtschaftslogik nutzt noch Übergangspfade; vollständiger Durchlauf steht aus |
| Waren und Ausbildung | Werkstätten, Warenaufträge, Ausbildung und zeitgesteuerte Abschlüsse sind vorhanden | Zusammenspiel mit Vorräten, Zeit und Aufträgen insgesamt noch zu prüfen |
| Forschung | Zeitgesteuerte Forschung einschließlich Ortsbezug ist implementiert | End-to-End-Prüfung im gesamten Spielablauf fehlt |
| Handel und Transporte | Orts- und Fremdhandelsfunktionen sowie Verträge existieren; frühere Gratisgewinne wurden gesperrt | Missionsseite / Handelsvorgänge und Bots nutzen laut letztem Protokoll zum Teil noch Echtzeit statt einheitlicher Spielzeit |
| Kampf und Spielende | Kampfberechnung, Berichte, Punkte und Sieg-/Niederlagebedingungen sind programmiert | Vollständige Balance und ein durchgängiger Spieltest sind nicht abschließend belegt |
| Computergegner (Bots) | Bot-Kern und erste Handlungslogik sind vorhanden | Ausgereifte Bot-Ökonomie, belastbare Strategie und Belagerungsverhalten sind noch nicht als abgeschlossen belegt |
| Speichern und Laden | JSON-Spielstände, Schutzmechanismen und Behandlung älterer Spielstände sind vorgesehen / getestet | Komplette Durchspiel- und Kompatibilitätsabnahme noch offen |
| Oberfläche und Grafiken | Karten-, Menü-, Icon- und Lageransichten sind vorhanden | UI-Gestaltung, Lesbarkeit und Originaltreue benötigen weitere Abnahme |
| Windows-EXE | Für ältere lokale Entwicklungsstände sind Builds und Startprüfungen protokolliert | **Kein freigegebener, für Besucher getesteter Release**; ein aktueller Windows-Build ist separat zu erstellen und zu prüfen |

## Letzter dokumentierter technischer Meilenstein im Hauptprojekt

Im offiziellen `docs/ENTWICKLUNGSPROTOKOLL.md` (Eintrag 89 vom 06.10.2026) ist festgehalten:

- `GameState.tick` nutzt für die Ortsseite die Ereignisberechnung `spieloekonomie.tick_bis`.
- Ortserträge, Ausbildung, Werkstattwaren, Forschung und Siedlerzuwachs werden dadurch in Ereignisschritten berechnet.
- Der damalige Sammellauf wurde mit **4.096 erfolgreichen Prüfungen, 0 gemeldeten Fehlern und 22 Befunden über 52 Testdateien** protokolliert.
- **Offen geblieben** waren die einheitliche Uhr für Missionen, Transporte, Handel und Bots sowie die abschließende Aktivierung des neuen Ökonomiemodus.

Diese Zahlen stammen aus dem **historischen Projektprotokoll**. Sie sind ausdrücklich **keine neue Prüfung des heute hochgeladenen GitHub-Stands**.

## Was als Nächstes ansteht

1. Einheitliche Spielzeit für Missionen, Transport, Handel und Bots herstellen, dann den neuen Ökonomiemodus kontrolliert aktivieren.
2. Den zentralen Dorfzentrums-/Lagerbereich anhand der bereits erfassten Anforderungen überarbeiten.
3. Bot-Wirtschaft, Kampf-/Belagerungslogik, Karten, UI und Spielbalance vollständig prüfen.
4. Einen vollständigen Ablauf von neuem Spiel bis Sieg/Niederlage mit Speichern und Laden testen.
5. Erst dann einen aktuellen Windows-Build erzeugen, auf Windows unabhängig prüfen und als GitHub Release veröffentlichen.

**Wichtig zur Reihenfolge:** Diese Liste macht keine neue Entwicklungsplanung für Hermes. Die verbindliche Reihenfolge und Integration bleiben bei der bestehenden Hauptkoordination und ihren Projektunterlagen.

## Nachweise und Verlauf

- [Offizielles Entwicklungsprotokoll](ENTWICKLUNGSPROTOKOLL.md) – laufendes Kurzprotokoll mit Belegen und Fehlern
- [Historische vollständige Protokollfassung](ENTWICKLUNGSPROTOKOLL_VOLLFASSUNG_2026-10-05_0820.md)
- [Projektstand und Übergabe](PROJEKT_STAND.md) – auch mit historischen Standteilen
- [Projektkontext](KONTEXT_PAKET.md) – Projektübergabe, teilweise älter als die neuesten Protokolleinträge
- [Weg zur EXE](WEG_ZUR_EXE.md) – Kriterien für eine spätere Freigabe

Der Status hier muss bei jeder veröffentlichten funktionalen Änderung gegen den tatsächlichen Hauptstand, die neuen Prüfungen und das Entwicklungsprotokoll nachgeführt werden.
