# Nebelseetal Remake unter Windows ausprobieren

> **Experimenteller Entwicklungsstand – kein freigegebener Release.** Für einen Start ist aktuell Python erforderlich. Eine fertig getestete EXE wird hier noch nicht zum Download angeboten.

## Voraussetzungen

- Windows 10 oder 11
- Installiertes **Python 3** (der frühere Entwicklungsstand ist mit **Python 3.14** dokumentiert)
- **Tkinter** (bei einer normalen Python-Installation für Windows in der Regel enthalten)
- Genügend Platz, um das Repository als ZIP zu entpacken

## Anleitung ohne Git-Kenntnisse

1. Das [GitHub-Repository](https://github.com/Decay03101991/Nebelseetal-Remake) aufrufen.
2. Auf den grünen **Code**-Knopf und dann **Download ZIP** klicken.
3. Das ZIP in einen **normalen eigenen Ordner** entpacken, zum Beispiel in `Dokumente\Nebelseetal-Test`. Nicht direkt aus der ZIP-Datei starten.
4. Falls Python noch fehlt: [Python für Windows](https://www.python.org/downloads/windows/) installieren. Danach in einer Eingabeaufforderung `python --version` ausführen.
5. Optional prüfen, ob Tkinter funktioniert: `python -m tkinter`. Es sollte ein kleines Testfenster erscheinen; dieses danach schließen.
6. Im entpackten Projektordner `Nebelseetal_Remake.bat` doppelklicken. Wenn sich kein Fenster öffnet, die Fehlersuche unten verwenden.
7. Beim ersten Start ein **eigenes Passwort** festlegen. Bei späteren Starts wird es lokal abgefragt.

**Alternative bei Fehlersuche:** Öffne im Projektordner die Adressleiste des Windows-Explorers, gib `cmd` ein und bestätige. Im geöffneten Fenster ausführen:

```bat
python src\main.py
```

Dadurch bleiben mögliche Fehlermeldungen im Fenster sichtbar. Das ist nur ein Testweg, kein Installationsprogramm.

## Bekannte Einschränkungen

- Manche Spielsysteme sind noch nicht vollständig miteinander verbunden.
- Die Benutzeroberfläche, Gegner und Wirtschaft sind noch nicht abschließend getestet.
- Spielstände aus unterschiedlichen Entwicklungsständen können Warnungen auslösen oder nicht vollständig kompatibel sein.
- Das individuelle lokale Passwort ist kein sicherer Kopierschutz für frei einsehbaren Python-Code.
- Eine früher intern gebaute EXE ist **nicht** automatisch eine geprüfte Downloadversion. Nutze keine unbekannten alten EXE-Dateien aus Projekt- oder Archivordnern.

## Fehler melden

Erstelle unter [Issues](https://github.com/Decay03101991/Nebelseetal-Remake/issues/new/choose) einen Fehlerbericht. Bitte gib Windows-Version, Python-Version, einen möglichst kurzen reproduzierbaren Ablauf und die genaue Fehlermeldung an.

**Keine Passwörter, geheimen Schlüssel oder Spielstände mit privaten Daten hochladen.**
