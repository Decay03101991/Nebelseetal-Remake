# Nebelseetal Remake — Fassung `Nebelseetal_Pre_Release_V_0.0.4.exe`

**Vierte veroeffentlichte Fassung.** Sie ist der Schnitt nach T1 bis T7 (Gestaltung), G8 (Drosselung),
K1 (Beute), U2/U3 (Anzeige), der Startseite Variante 1 — und mit **C1** zum ersten Mal mit dem
Weltensprung-Preis, den Daniel am 01.11.2026 entschieden hat.

Daniel 05.11.2026: jede neue Spielversion wird angekuendigt, das Repo bleibt laufend aktuell.
Daniel 06.11.2026: **neuer Zaehler** statt Ueberschreiben einer bereits heruntergeladenen Fassung.
Daniel 18.11.2026: „ich will ein stimmiges Gesamtbild auf GitHub“ — deshalb sind Startseite, README,
Chronik und diese Notizen auf demselben Stand.

## Was sich gegenueber 0.0.3 geaendert hat

| Bereich | Aenderung | Sichtbar im Spiel? |
|---|---|---|
| **C1 Weltensprung** (Register 664) | Ein Weltensprung kostet **500 Mana plus 100 Gold** statt 5.000 Mana — der belegte Originalwert bleibt in `data/welten.json` stehen, der Spielwert steht als eigener Block daneben. Ohne Gold kein Sprung; die Meldung nennt den fehlenden Betrag. Portalansicht und Knopf zeigen beide Preise | **ja** — Portal, „hierher versetzen“ |
| **Gestaltung T1 bis T7** | Ressourcenleiste mit Bildrahmen und Endstuecken, Lagerkacheln in festen Massen (206 x 83), Dorfzentrum, In-Game-Fenster, Menueleiste, Auswahlrahmen | **ja** |
| **G8 Drosselung** | Reisen lassen sich verlangsamen: laenger unterwegs, weniger Gold | **ja** — Auftrag anlegen |
| **K1 Beute** | Beute am Ziel mit Vorrangregel und Karrenladung | **ja** — Kampfbericht |
| **U2/U3 Anzeige** | Deutsche Zahlen (Komma statt Punkt), einheitliche Statuszeilen | **ja** |
| **Startseite Variante 1** | Neue Besucherseite mit sechs Haeusern, sechs Welten, Chronik-Verweisen | nein — `index.html` im Repo |
| **Pruefstand** | Wachen auf den neuen Preis umgestellt und um eine eigene Wache erweitert (`test_wechselpreis_spielwert`) | nein |

## Pruefstand dieser Fassung

- **Voller Sammellauf: 240 von 240 gruen, 0 rot, 2 ausgesetzt** (dieselben zwei dokumentierten:
  `test_oekonomie_kern_unabhaengig`, `test_weltkarte`), **242 Dateien, 12.505 Pruefungen, 0 Fehler,
  100 Befunde** (`docs/audits/sammellauf_20261118_1901.log`).
- Der Lauf startete NACH dem letzten Fix; Register 664/665 und die Protokollzeilen gehoeren dazu.

## Bekannte Grenzen (ehrlich, unveraendert)

- **Kein fertiges Spiel.** Vorabversion zum Ausprobieren und Fehlersammeln, ohne Kompatibilitaetszusage.
- **Zwei Pruefdateien sind dauerhaft ausgesetzt**, ein Termin zur Wiederaufnahme ist unbekannt.
- **Design folgt im Dezember** — siehe unten.
- Der Bildschirmfoto-Platzhalter auf der Startseite ist noch leer: **das Foto kommt von Daniel**.
- Kein Sieg, sondern Ruhm: vier Auszeichnungen. Die Partie endet nicht mit einem Siegbildschirm.

## Was im Dezember nachgeliefert wird (Ankuendigung)

Die Gestaltung ist **noch nicht vollstaendig**. Bestellt sind **18 Bilddateien** in acht Gruppen
(Kopfbänder, Kennzeichen, Rahmen, Hintergruende, zwei Ladebilder, drei Portraits, drei Wappen,
zwei Leisten-Endstuecke); die Sollwerte stehen in `data/bildpaket_dezember.json`, die Bestellliste in
`docs/BILDPAKET_DEZEMBER_2026.md`, die Abnahme laeuft ueber `tools/bildpaket_pruefen.py`.
**Dazu sechs neue Haus-Wappen**, die bis zum Aufladen des Bildmodells blockiert sind.

Bis dahin zeichnet das Spiel an jeder dieser Stellen eine **gezeichnete Ersatzflaeche** — es fehlt
Gestaltung, keine Funktion. Wer jetzt testet, testet also das Spiel, nicht das endgueltige Aussehen.

## Dateien dieses Releases (gemessen am 18.11.2026)

| Datei | Groesse | SHA256 |
|---|---|---|
| `Nebelseetal_Pre_Release_V_0.0.4.exe` | **84.126.514 Byte** (80,2 MB) | `4fd298d00a37bc41cc7e56910127a77814fdf12a92e8035614bc27689c37707a` |
| `Nebelseetal_Pre_Release_V_0.0.4.zip` | **83.862.403 Byte** (83,9 MB) | siehe `SHA256SUMS.txt` im ZIP |

Die EXE wurde am 18.11.2026, 20:41 gebaut (`tools/build_exe.py`, Projekt-venv mit PyInstaller 6.22.3)
und **gestartet und angesehen**: sie zeigt die Passwortsperre („Dieses Spiel ist passwortgeschützt“,
Feld, Knopf „Spiel starten“, Notausgang ueber `tor.json`). Danach beendet, `game.lock` entfernt.

Das ZIP enthaelt die EXE, `START_HIER.txt`, `BEKANNTE_GRENZEN.txt`, `FEHLER_MELDEN.txt`,
`SYSTEMANFORDERUNGEN.txt` und `SHA256SUMS.txt`.
