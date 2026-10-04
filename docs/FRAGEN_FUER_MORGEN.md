# Für morgen früh (Daniel) — Stand 04.10.2026, 23:00

**Kurz:** Das Spiel läuft als `.exe`, ist passwortgeschützt, und sechs neue Bausteine sind fertig
geprüft. Offen ist vor allem **ein** Schritt: diese Bausteine in die Oberfläche einhängen.

## 1. Was du jetzt schon machen kannst

- **Spielen**: `D:\Arbeiten\Nebelseetal_Remake\Nebelseetal_Remake.exe` (Doppelklick). Beim ersten
  Start hast du dein Passwort gesetzt (22:43) — das verlangt es jetzt bei jedem Start.
- **Notausgang**, falls du es vergisst: die Datei `C:\Users\saras\.nebelseetal\tor.json` löschen →
  das Spiel verlangt beim nächsten Start ein **neues** Passwort, der Spielstand bleibt.
- **Prüfen, dass alles läuft**: `run_tests.bat` im Projektordner doppelklicken (braucht einen
  angemeldeten Desktop; dauert einige Minuten).

## 2. Fragen an dich (bitte kurz entscheiden, dann arbeite ich weiter)

1. **Ausbaustufen von Bibliothek und Ausbildungsstätten**: belegt ist nur, dass es Stufen gibt.
   Ich habe **5** eingetragen (Wall: die belegten 10). So lassen oder andere Zahl?
2. **Ausbildungsdauer**: das Handbuch nennt keine. Ohne deine Zahl bleibt sie bei 0,5 Minuten, und
   die Stufe der Ausbildungsstätte senkt noch nichts Messbareres.
3. **Höhe des Verteidigungsboni** des Walls: nicht belegt, zurzeit +50 % je Stufe (alte Zahl).
4. **Weitere Karten** schaltet jetzt die Forschung **„Vermessung"** frei (vorher hing das an einem
   erfundenen Portal-Gebäude). Einverstanden — oder soll das Portal es wieder übernehmen?
5. **Forschungstempo**: Handbuch = Stufe² Stunden (Stufe 10 also 100 Stunden). Das ist für ein
   Einzelspielerspiel sehr lang — soll ich es so einhängen oder gestaucht (z. B. Faktor 1/5)?
6. **Sieg-/Niederlagebedingung**: nennt das Handbuch nicht. Der Vorschlag steht in
   `src/punkte.py` (klar als Vorschlag gekennzeichnet) — bitte abnehmen oder ändern.
7. **Oberfläche**: das Original-Menü ist belegt (Übersicht · Portal · Diplomatie · …). Soll ich es
   in der belegten Reihenfolge nachbauen (Netz-Einträge wie Forum/Chat bleiben draußen)?
8. **Werkstatt-Tempo**: verkürzt eine höhere Werkstattstufe die Herstellungszeit? Das Handbuch
   belegt nur, DASS es Stufen gibt (und nennt die 20 Minuten nur für das Schwert-Beispiel). Im
   Modul steht dafür ein gekennzeichneter Vorschlag von **10 % je Stufe** — so lassen oder anderen
   Wert?
9. **Portal-Kosten**: belegt sind **5.000 Mana** für einen Dimensionswechsel (aus einer Siedlung,
   höchstens einmal je 24 h). `src/welt.py` enthält außerdem einen älteren **Vorschlag** mit
   Entfernungsformel. Welche der beiden soll das Spiel benutzen? (Ich würde die belegten 5.000
   nehmen und die Formel als Vorschlag stehen lassen.)
10. **Rundung der Gesamtpunkte**: belegt ist „Gesamt = die Hälfte aus Forschungs- und Kriegspunkten",
    aber nicht, was bei einer **ungeraden** Summe passiert. Im Modul wird **abgerundet** (3 → 1) und
    das ist als Vorschlag gekennzeichnet. Abrunden, aufrunden oder kaufmännisch?
11. **Götterschutz**: belegt sind **7 Tage** (umgesetzt) und dass er laut Handbuch **mit dem ersten
    Kriegspunkt endet** (noch nicht umgesetzt). Soll ich das nachziehen?
12. **Kartenmaß auflösen** (Widerspruch in unseren eigenen Daten, von astra gefunden): `data/gelaende.json`
    nennt **8 Spalten × 5 Reihen = 40 Felder** und gleichzeitig **56 Felder** („40 Bauplätze, die übrigen
    Wege/Wasser"). Beides zusammen geht nicht. Mein Vorschlag: **8 × 7 = 56 Felder, davon 40 bebaubar** —
    damit stimmen beide Zahlen und das Raster bleibt schmal. Oder sollen es 8 × 5 = 40 Felder sein (dann
    streichen wir die Wege/Wasser-Felder)?
13. **Siedlungskarte**: Auf den drei Original-Fotos ist **keine** Siedlungskarte zu sehen (zweimal
    unabhängig von astra geprüft) — unser Entwurf ist also **unsere eigene Gestaltung**. Soll ich die
    vorgeschlagene Draufsicht mit selbst gezeichneten Symbolen umsetzen (so steht es in
    `docs/KARTEN_ENTWURF.md`), oder hast du noch ein Originalbild mit der echten Siedlungskarte?

## 3. Was in der Nacht noch entstanden ist

- `.exe` gebaut und **startgeprüft** (Pfad mit Leerzeichen, Fenster, sauberes Schließen,
  Fehler dabei gefunden: die EXE fand ihre Datendateien nicht → behoben).
- **Passworttor** (`src/tor.py`, 61 Prüfungen).
- **W4b-6**: die 21 Originalforschungen sind im Spiel, und Forschung wirkt jetzt auf **alle neun**
  Rohstoffe (belegte Prozentsätze statt erfundener).
- **Zehn Kinder-Module**, jedes mit eigener Prüfdatei, zusammen **958 grüne Prüfungen**:
  `forschung_wirkung` 94 · `werkstatt` 118 · `portalraum` 69 · `punkte` 76 · `kampfbericht` 108 ·
  `spielschicht` 133 · `botkern` 90 · `speichern` 95 · `oberflaeche_original` 64 · `auftraege` 111.
  **Jedes von mir selbst nachgerechnet**, nicht geglaubt (und im Menü-Modul dabei ein echter Fehler
  im Kind-Test gefunden und behoben).
- **Kein Brett der Kinder mehr** (deine Anweisung, 04.10.2026): sie melden ihr Ergebnis im
  Abschlussbericht, ich führe zusammen. `docs/BOARD.md` bleibt als Tagebuch für dich.
- Das **Entwicklungsprotokoll** ist fortgeschrieben (Abschnitte G, H, I) samt gemessenen Kosten.

## 4. Was noch fehlt bis „fertig"

Die Module sind gebaut und geprüft, aber `main.py` benutzt sie noch nicht: Waren, Kampf, Aufträge,
Portalansicht, Punkte/Sieg, robustes Speichern, Bots. Das ist **der nächste Schritt** — eine
Fachschicht bündelt sie, dann hängen wir sie in die Oberfläche und bauen die `.exe` neu.
Einzelheiten: `docs/PROJEKT_STAND.md`, Abschnitt 5 und 6.
