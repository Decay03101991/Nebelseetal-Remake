# Nebelseetal Remake — Fassung `Nebelseetal_Pre_Release_V_0.0.2.exe`

**Zweite veroeffentlichte Fassung**, Schnitt direkt nach `V_0.0.1`. Daniel 05.11.2026: jede neue
Spielversion wird angekuendigt, das Repo bleibt laufend aktuell.

## Was sich gegenueber 0.0.1 geaendert hat

| Bereich | Aenderung | Sichtbar im Spiel? |
|---|---|---|
| Kern-Weg der Warenfertigung | `spielschicht.ware_fertigen` prueft jetzt die Forschungsvoraussetzung (dieselbe Lesestelle wie der GUI-Weg) und bucht die Materialkosten atomar, mit Rueckbuchung bei Ablehnung | nein - der Bedienweg im Spiel nutzte schon den geprueften Pfad; korrigiert ist der gemeinsame Kern fuer Tests und Spieltest-Simulation |
| Angriff ohne Handkarren | erlaubt, Beute dann leer (die Karrenladung ist die Grenze, belegt im Handbuch) | nein - der Kern liess das immer zu, blockiert hatte nur das Messwerkzeug |
| Spieltest-Werkzeug | Baukette vollstaendig (Haus, Schafszucht, Stellmacher, Erzmine, Schmiede, Naehstube), Fehlversuche mit Grund im Bericht, Forschungsziele bis zu den Warenvoraussetzungen, Stil-Schalter breit/krieg | nein - Entwicklungswerkzeug |

## Pruefstand dieser Fassung

- Voller Sammellauf: **176 von 178 Dateien gruen, 0 rot**, 7.284 bestandene Pruefungen, 1.353 s
  (`docs/audits/sammellauf_20261105_1958.log`). Die zwei Dateien ohne Ergebniszeile laufen mit
  Rueckgabewert 0 (dieselbe Eigenart wie `test_rueckmarsch`).
- Einzelwachen dieses Schnitts: `test_spielschicht` 142/0/1, `test_spieltest_erreicht_kampf` 19/0/0
  (neu), `test_textqualitaet` 477/0, `test_projektpfade` 123/0, `test_zieluebergabe` 26/0/0.
- Veroeffentlichte EXE: 86.984.365 Byte,
  SHA256 `c9b45703ee1229ae41fdd718df56f18e0393e921d50c457c5f158972f6e5e624`
- Veroeffentlichungs-ZIP: 86.702.517 Byte,
  SHA256 `9ac208259d7e4155194838cb29052e8b52d99e77ed76a99f0ef585c649e1eb08`
- Am Bildschirm gestartet: Fenster `Nebelseetal Remake`, **Passwortsperre** im Bild belegt, danach
  ueber die Fenster-PID beendet (0 Prozesse), verwaiste `game.lock` gesichert und entfernt.
- Die Demo wird **leer** ausgeliefert: eigener Speicherordner `...\Nebelseetal_Remake\Demo`, Paket
  ohne Spielstand (`tools/build_public_exe.py --pruefen` gruen).

## Was die Spieltests zu dieser Fassung sagen

Zwei bezahlte Laeufe mit starkem Modell (0,0349 und 0,0362 USD) und zwei davor: alle vier Urteile
nennen dieselbe Engstelle - **Waffentechnik Stufe 3** sperrt das Kurzschwert und damit den ersten
Kaempfer (in einem Lauf 283+156+82 Fehlversuche, 488 blockierte Ausbildungen). Holz ist die zweite
Bremse (Tag 1 sechs Holz), Mana bleibt auch nach 12 Spieltagen bei 0. Einzelheiten, Zahlen und
Vorschlaege: `docs/SPIELTEST_BEFUNDE_20261105.md`.

## Bekannte Grenzen

- Die Startkarte ist fest; ein anderer Startwert (`--saat`) aendert den Verlauf derzeit nicht.
- Das Angriffsziel der Spieltest-Simulation ist ein festes Dorf: Beute und Verluste sind dort
  immer gleich, der Kampf ist damit nicht beurteilbar.
- Mana, Pferde und Handel kommen in keinem gemessenen Lauf vor.
- Die Balance der Forschungsdauern ist offen (Waffentechnik 3 braucht rund sechs Spieltage).

## Start

`Nebelseetal_Pre_Release_V_0.0.2.exe` starten, Passwort eingeben, neues Spiel beginnen. Der
Spielstand liegt unter `%LOCALAPPDATA%\Nebelseetal_Remake\Demo`.
