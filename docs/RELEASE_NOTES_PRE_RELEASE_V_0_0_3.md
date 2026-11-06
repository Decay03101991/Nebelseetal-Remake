# Nebelseetal Remake — Fassung `Nebelseetal_Pre_Release_V_0.0.3.exe`

**Dritte veroeffentlichte Fassung**, Schnitt nach S3. Daniel 05.11.2026: jede neue Spielversion wird
angekuendigt, das Repo bleibt laufend aktuell. Daniel 06.11.2026 (Frage 1 der Runde): **neuer Zaehler**
statt Ueberschreiben der bereits heruntergeladenen `V_0.0.2`.

## Was sich gegenueber 0.0.2 geaendert hat

| Bereich | Aenderung | Sichtbar im Spiel? |
|---|---|---|
| Verwundetenheilung (S3) | 30 Prozent der Verluste je Einheitentyp werden verwundet (abgerundet); Heilung kostet 75 Prozent der Kostenposten ohne Siedler und ohne Ausruestung und dauert die Haelfte der Ausbildungszeit. Heilung laeuft in der vorhandenen Warteschlange der Kaserne | **ja** - neue Zeile je Einheit mit Verwundeten, Preis, Dauer und Heilknopf |
| Mauerreparatur (S2) | Reparatur je Prozentpunkt (Preis V-1, 360 Spielsekunden je Punkt), Rohstoffe beim Start atomar gebucht, Zustand steigt im Tick, Kampf bricht ab, Reparatur und Ausbau sperren sich | **ja** - Wallansicht |
| Postfach (S1, S1b) | Fristen, Filter, Archiv, Blaettern (20 je Seite), Ruhm-Balken, vier Menuegeschichten | **ja** |
| Verlustbericht | Eigener Nachrichtentyp `verlust` bei jeder Verlustbuchung, mit Ort und Mengenaufzaehlung, unabhaengig vom Schalter der Heilung | **ja** - Postfach |
| Anzeige deutscher Zahlen | Heilpreise und Heildauer zeigen Komma statt Punkt (0,75 Pferde; 262,5 Gold) - der Kern bleibt ungerundet | **ja** - Kaserne |
| Fuenf gerechnete Tabellen (S0) | `tools/s0_tabellen.py` rechnet V-1 bis V-5 aus den Projektdaten, jede Zahl mit Rechenweg | nein - Entwicklungswerkzeug |
| Pruefstand | Flakiness-Wache `test_kartenwahl_bot` mit festem Startwert geheilt (3 von 3 Laeufen gruen) | nein |

## Pruefstand dieser Fassung

- Voller Sammellauf: **181 von 183 Dateien gruen, 0 rot**, 7.502 bestandene Pruefungen, 60 Befunde,
  **1.612 s** (`docs/audits/sammellauf_20261106_0755.log`, 07:55:28 bis 08:22:22). Die zwei Dateien
  ohne Ergebniszeile laufen mit Rueckgabewert 0 (dieselbe Eigenart wie `test_rueckmarsch`).
- Einzelwachen dieses Schnitts: `test_verwundete` **52/0/0** (davon sieben Pruefungen zur deutschen
  Zahlenanzeige), `test_nachrichten_archiv` 51/0/0, `test_kartenwahl_bot` 25/0/0,
  `test_textqualitaet` 516/0 (158 Dokumente), `test_projektpfade` 127/0, `test_protokoll` 25/0/1.
- Veroeffentlichte EXE: **102.098.672 Byte**,
  SHA256 `915fe8144eda11a501333c2249d028c47fa625bc30adbb033df88dde35f34595`
- Veroeffentlichungs-ZIP: **101.818.049 Byte**,
  SHA256 `4d1dad2cf4f27886f0397b860ba6f57131fbef5d16fcf09012d5e580d57c039a`
- Am Bildschirm gestartet: Fenster `Nebelseetal Remake` (PID 15080, Fenstertitel gelesen),
  **Passwortsperre** im Bild belegt (Titel, Feld `Passwort`, Knopf `Spielstarten`), danach ueber die
  Fenster-PID beendet (0 Prozesse). Verwaiste `game.lock` (PID 15080) gesichert und entfernt.
- Die Demo wird **leer** ausgeliefert: eigener Speicherordner `...\Nebelseetal_Remake\Demo`, nach dem
  Start nur `archiv/` und `tor.json`, **kein Spielstand**; `tools/build_public_exe.py --pruefen` gruen.
- Die EXE ist gegenueber 0.0.2 um rund 15 MB groesser (Fraktionspanoramen und neue Daten aus dem
  Schnitt der Nacht); die Groesse stammt aus dem Bau dieser Fassung, nicht aus einer Abschrift.

## Was die Spieltests zu dieser Fassung sagen

Die vier bezahlten Spieltest-Urteile der 0.0.2 nennen dieselbe Engstelle: **Waffentechnik Stufe 3**
sperrt das Kurzschwert und damit den ersten Kaempfer; Holz ist die zweite Bremse, Mana bleibt auch nach
12 Spieltagen bei 0, und die **Handelspunkte bleiben 0** (der Handelsweg ist gebaut, im Spielbetrieb
aber nicht erreichbar). Einzelheiten: `docs/SPIELTEST_BEFUNDE_20261105.md`.

## Bekannte Grenzen

- Die Startkarte ist fest; ein anderer Startwert (`--saat`) aendert den Verlauf derzeit nicht.
- S4 (Diplomatie) und S5 (Siedlungsumzug) sind **nicht** enthalten; S5 ist ausdruecklich gesperrt.
- Die Antworten der externen Modelle auf `docs/extern/Nebelseetal_LLM_Auftrag_20261106.md` liegen noch
  nicht vor; die naechste Fassung wird den Abgleich enthalten.
