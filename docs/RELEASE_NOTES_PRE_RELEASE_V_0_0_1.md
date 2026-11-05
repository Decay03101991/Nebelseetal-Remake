# Nebelseetal Remake — Fassung `Nebelseetal_Pre_Release_V_0.0.1.exe`

**Das ist die erste veroeffentlichte Fassung des Spiels.** Alles davor sind Entwicklungszustaende und
Historie; sie stehen in den Entwicklungsdaten und sind nicht Teil dieser Veroeffentlichung.

Daniel 05.11.2026, buchstabengenau: der Dateiname lautet `Nebelseetal_Pre_Release_V_0.0.1.exe`.

## Was das ist

Ein Einzelspieler-Remake des eingestellten deutschen Browserspiels Nebelseetal: eine Siedlung
gruenden, produzieren, forschen, ausruesten, ausbilden, kaempfen, punkten - offline, ohne Konto, ohne
Server, unter Windows.

## Was in dieser Fassung steckt

| Bereich | Stand |
|---|---|
| Start | Kartengruendungsseite als erstes Fenster, drei Schritte (Seite - Volk - Karte), Fraktion genau einmal waehlbar |
| Startkarte | fuer Spieler und alle Bots dieselbe mittlere Karte (`original-036`); Neugruendungen ziehen aus dem Katalog |
| Siedlungen | aufgeben (Karte loeschen) mit Verlust von Lager, Einheiten und Bauten; das ERSTE Dorf erst ab sechs Siedlungen |
| Bots | gruenden nach, beurteilen die Karte und geben ein Dorf wieder auf - mit Ruecklage der Gebuehr, Sperre und Erinnerung |
| Wirtschaft | 127 Originalkarten, Erzeuger je Gelaende, Werkstaetten, Waren, Nahrungsverbrauch, Karren mit Wagenbau-Bonus |
| Kampf | Vorrunde, Wallstufen, Beute nach Karrenladung (Gold zuerst), Drachen als Weltpunkte |
| Balance | Goldkosten der 14 Militaereinheiten um 30 Prozent gesenkt (belegte Abweichung, `docs/quellen/ABWEICHUNGEN_2006_zu_2009.md` Abschnitt 7) |

## Pruefstand dieser Fassung

- Voller Sammellauf: **174 von 176 Dateien gruen, 0 rot**, 7.239 bestandene Pruefungen, 1.257 s
  (`docs/audits/sammellauf_20261105_1630.log`). Die zwei nicht gruenen Dateien sind die seit dem
  30.10.2026 dokumentiert ausgesetzten.
- Entwickler-EXE: `Nebelseetal_Pre_Release_V_0.0.1.exe`, 86.978.803 Byte,
  SHA256 `efaf403b94465df3330a00ae741dc96377bd263ed6c44a5e5f89a1bf21aec17d`, am Bildschirm gestartet
  (Fenster und Passwortsperre belegt).
- Veroeffentlichte EXE: `release_public/Nebelseetal_Pre_Release_V_0.0.1.exe`, 86.983.205 Byte,
  SHA256 `f9ef7aaa14b0417cefcefb11203423144cae65a15e00ac3bedbb63c3503bd482`, mit Passwortsperre am
  Bildschirm geprueft (Screenshot der Sperre, danach ueber die Fenster-PID beendet).
- Die Demo wird **leer** ausgeliefert: `tools/build_public_exe.py --pruefen` meldet das leere Paket,
  der eigene Speicherordner `...\Nebelseetal_Remake\Demo` enthaelt keinen Spielstand.

## Bekannte Grenzen

- Kein Netzwerk, kein Mehrspieler, keine Cloud - Einzelspieler gegen fuenf Bots.
- Das Originalmaterial (Karten, Anleitung) stammt aus einer eingestellten Seite; die Rechtefrage ist
  vor einer breiten Veroeffentlichung zu klaeren.
- Die Admin-Oberflaeche steckt im Quelltext, ist in der oeffentlichen EXE aber gesperrt
  (`src/public_start.py`); das ist eine Sperre, keine Sicherheitsgrenze.

## Start

ZIP in einen leeren Ordner entpacken, `Nebelseetal_Pre_Release_V_0.0.1.exe` starten, eigenes Passwort
festlegen. Python ist nicht noetig.
