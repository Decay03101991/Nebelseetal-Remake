# 03 Abgelehnt und archiviert - mit Grund

Was hier steht, wird **nicht wieder vorgelegt** - es sei denn Daniel verlangt es ausdruecklich.
Die vollstaendige Begruendung je Abschnitt steht in `VERWERTUNG.md` der Sammlung (80 Zeilen).

## 1. Von Daniel selbst abgelehnt (woertlich)

| Gegenstand | Wortlaut | Folge |
|---|---|---|
| Transporte abfangen | «ich will nicht das man transporte abfangen kann vorerst. Evtl wird es mal eingebaut je nach dem was wir benötigen laut balancing.» | nicht gebaut; nur mit eigener Entscheidungsrunde |
| Wirtschafts- und Transportabschnitt (Bloecke 5 und 6) | «gefällt mir wirtschaft und transport komplett gar nicht» | ganze Bloecke im Archiv |

## 2. Widerspricht der belegten Originalregel

| Gegenstand | Grund |
|---|---|
| Stein-Schere-Papier-Matrix, waehlbare Formationen, Initiative-Rundenmatrix fuer 28 Einheiten | das Original regelt Kaempfe mit Vorrunde, Wall, Zweikampf, Erschoepfung (`kampf.fuehre_schlacht` ist der EINZIGE Kampfweg) |
| Ausruestung je Einheit im Spielstand speichern | Ausruestung wird bei der Ausbildung **verbraucht** (`ausruestung.verbrauchen`) |
| Goetterschutz kaufen | belegtes Punkteband statt Kaufpreis (siehe T-3) |
| Truppenlimit 100 je Dorf | harte Grenze sind Siedler und Haeuser |
| Siedler je Gebaeude / Teilbesetzung | Daniels Entscheidung vom 31.10.2026 (Frage 5 = B: Bauten binden keine Siedler) |

## 3. Zweite Wahrheit neben gebautem Code (F-04-Muster)

Jeder dieser Vorschlaege haette eine zweite Rechnung, Tabelle oder Ablage neben einer bestehenden
erzeugt: `src/produktions_logik.py`, `data/gebaeude.json`, `data/portale.json`,
`laufende_transporte`, `beute_prio` je Ware, `flucht_schwelle`, `src/kampf_logik.py`,
`src/wall_belagerung.py`, `src/goetterschutz_logik.py`, `hole_forschungs_effekt`,
`postfach.json`, `nachbarn.json`, `src/nachbar_ki.py`, `data/weltkarte.json`.
**Regel, die daraus fuer jeden Modell-Auftrag folgt:** jeder Vorschlag nennt die Datei, die er
**erweitert** - ein neues Modul fuer eine geloeste Aufgabe ist ein Fehler, kein Fortschritt.

## 4. Umgebung, die es hier nicht gibt

- **Serverthemen** (Koenigreiche, Websockets, REST, Anti-Cheat, Chat-Server, Asynchron-Kampf):
  das Remake ist lokal und Einzelspieler.
- **WSL** (Pfad-Sicherheit Windows/WSL, WSL-Testskript): `grep -rilE "wsl" src/ tools/` = kein Treffer;
  Entwicklung und Pruefung laufen nativ auf Windows.
- **Admin-Konsole im Spiel mit Master-Passwort**: Testabkuerzungen gehoeren nach `tools/`, eine
  Hintertuer kollidiert mit leerer Demo und Passwortsperre.
- **Spielstand-XOR**: der Spieler darf sein Spiel aendern; die Passwortsperre `tor.py` gibt es.
- **Feature-Branches statt `main`**: Daniels Regel - jeder Schnitt ein Commit, Register, Protokoll,
  voller Lauf, Push auf `main`.
- **UI-Umbau in fuenf `gui_*.py`** (ttk-Notebook, Emojis, ungueltige Farben `#gold`/`#green`):
  die Struktur der Oberflaeche entscheidet Daniel; Emojis widersprechen der Projektregel.
- **Laufzeitdaten in `data/`** (Drachen-Koordinaten beim Start schreiben): bricht die Regel, dass
  die Demo leer ausgeliefert wird.

## 5. Archiviert: sechzehn Rohdateien wandern nach `02_ARCHIV`

Grund je Datei: **keine Zeile mit einer noch offenen brauchbaren Idee** - alles ist entweder schon
gebaut (SCHON SO), widerlegt (ABGELEHNT) oder Umgebung, die es hier nicht gibt (ARCHIV).
Verschoben, nicht geloescht; die Begruendung steht weiter in `VERWERTUNG.md`.

| Rohdatei | Grund in einem Satz |
|---|---|
| `20261105_2149_GoogleKI_Beute_Priorisierung_Code.txt` | zweite Beute-Prioritaet neben `data/beute_vorrang.json` |
| `20261105_2149_GoogleKI_Sechs_Welten.txt` | Frage seit 04.11.2026 erledigt (sechs Dimensionen, `_schnitt_w6`) |
| `20261105_2150_GoogleKI_Fluchtformel_Code.txt` | Rueckzug je Einheit existiert; 60 Prozent waere eine erfundene Zahl |
| `20261105_2150_GoogleKI_Mauerreparatur_Code.txt` | Trefferpunkt-Modell gegen den Prozent-Wall (Thema lebt als B-4) |
| `20261105_2152_GoogleKI_Ausruestungssystem.txt` | Ausruestung wird verbraucht, nicht gespeichert |
| `20261105_2153_GoogleKI_Spielstand_Schutz.txt` | Einzelspieler, XOR ist keine Sicherheit |
| `20261105_2154_GoogleKI_Admin_Konsole.txt` | Hintertuer gegen leere Demo und Passwortsperre |
| `20261105_2155_GoogleKI_Gebaeude_Produktion.txt` | zweite Gebaeudedatei und zweiter Produktionsweg |
| `20261105_2156_GoogleKI_Transport_Portale.txt` | feste Tick-Matrix und Transportliste neben `welt.entfernung` |
| `20261105_2321_GoogleKI_Canvas_Weltkarte.txt` | 512 px widerspricht dem 20x20-Portalgitter; Weltkarte ist gebaut |
| `20261105_2321_GoogleKI_UI_Architektur.txt` | UI-Struktur entscheidet Daniel; Emojis und Farben unzulaessig |
| `20261105_2322_GoogleKI_Kaserne_Ausbildung.txt` | Ausbildung mit Warteschlange und Ausruestung ist gebaut |
| `20261105_2324_GoogleKI_Forschungssystem.txt` | Forschung mit Voraussetzungen und Wirkungen ist gebaut |
| `20261105_2326_GoogleKI_Gebaeude_Ausbau.txt` | Ausbaustufen mit `max_stufe` sind gebaut |
| `20261105_2328_GoogleKI_Nachzuegler_A.txt` | Wall in Trefferpunkten, Emoji-Kampflogs (Thema als B-4) |
| `20261105_2328_GoogleKI_Nachzuegler_B.txt` | kaufbarer Goetterschutz gegen die belegte Regel |

**Was in `00_ROH` bleibt:** dreizehn Bloecke, die mindestens eine offene Idee tragen
(Diplomatie, Diplomatie-Events, Postfach, Mauerreparatur/Beute/Flucht, Etappen/Umzug, Wegzeit,
Nachbarn-Rache, Ruhm, Code-Hygiene, Lords-Mobile-Vergleich).
