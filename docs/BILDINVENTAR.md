# Bildinventar und Altlastenpruefung

Stand 28.10.2026. Dieses Inventar wurde **aus den Dateien**, nicht aus Vermutungen erstellt. Ein maschinenlesbarer Vollbericht inkl. SHA-256 und bytegleichen Gruppen liegt unter `archiv/manifeste/BILDER_VOLLE_DATEILISTE.json`.

## Befund

- Insgesamt **578** Bilddateien in `assets`, `docs/original`, `docs/quellen` erfasst.
- Einteilung: Laufzeit-/Asset-Kandidat: 222, Quell-/Originalreferenz: 356.
- Bei **347** dieser Bilder fand die einfache statische Wortsuche keinen direkten Dateinamen im Python-/JSON-Quellbestand. **Das ist kein Beweis fuer Unbenutztheit**, da Bilder dynamisch geladen werden koennen.
- **44** Gruppen bytegleicher Bilder gefunden. Diese Dateien wurden **nicht blind geloescht**: Mehrere Namen koennen fuer bestehende Referenzen gebraucht werden.
- Vorhandene Icon-Quellblaetter aus `Einheiten Icons/` und `Item Icons/` befinden sich nun geordnet in `assets/quellbilder/einheiten/` und `assets/quellbilder/waren/`. Die zugehoerigen Tests/Werkzeuge wurden angepasst.
- Gamestar-Baumenue-Screenshot bleibt bewusst an `docs/nebelseetal_gamestar2.jpg`, damit der vorhandene GitHub-Link erhalten bleibt.
- Das Ladebild und das Symbol sind **Quellbilder**; die abgeleiteten aktiven Grafiken befinden sich weiterhin unter `assets/loadingpage` und `assets/icons`.

## Kandidaten ohne eindeutigen direkten Quelltextnamen (nur manuelle Pruefung)

- `assets/icons/loading_bg.jpg`
- `assets/icons/dragon.ico`

## Naechster Arbeitsschritt

Vor jedem Loeschen pruefen: Wird die Datei ueber Datenfelder, dynamische Dateinamen, Buildwerkzeuge, Tests oder die UI gebraucht? Bild in altem Screenshot vorhanden, aber kein UI-Einsatz? Dann **als Designreferenz erhalten**, nicht unbesehen ins aktuelle Spiel kopieren. Historische Originalgrafiken moeglicherweise urheberrechtlich geschuetzt – Nutzung/Weitergabe separat klaeren.


## Nachtrag 28.10.2026 – originale Spielfeldgrafiken

- **127** zusätzliche aktive 640×640-PNGs unter `assets/karten/spielfeld/`, SHA-256-Verknüpfung in `data/originalkarten/grafik_manifest.json`; aus denselben 127 historischen Bildern unter `assets/karten/original/` abgeleitet. **Absichtliche Ableitungen**, keine löschbaren Dubletten.
- Alle früheren synthetischen Gelaende-Malpläne sind im aktiven Siedlungs-Renderer deaktiviert, Gebäude und Overlays bleiben.
- Das Inventar/der Altbericht vor diesem Nachtrag erfasste nur ältere Bilder, nicht diese 127 Ableitungen. 25 Quellraster visuell noch offen.
