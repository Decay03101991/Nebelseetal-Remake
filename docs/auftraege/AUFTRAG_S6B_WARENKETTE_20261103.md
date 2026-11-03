# Auftrag an das starke Modell: S-6b Warenkette fuer Bots (03.11.2026)

## Rolle

Du bist Spieldesigner und Regel-Autor fuer ein lokales Remake des Browserspiels Nebelseetal (Python,
Einzelspieler gegen fuenf Bots). Du entwirfst **Regeln und Datenschluessel**, du schreibst **keinen
Code** und aenderst **keine Datei im Projekt**.

## Ziel dieses Auftrags

Der Bot soll einen **Siedlerkarren bauen** koennen - genau wie der Spieler -, damit er mit
`siedlerkarren_pflicht: true` gruenden kann. Entwirf, **welche Datenschluessel und welche Schritte**
dafuer noetig sind, so dass die Sitzung sie ohne weitere Rueckfrage einbauen kann.

## Belegter Ist-Stand (gemessen, nicht geschaetzt - bitte nicht neu erfinden)

**Was der Kern fuer einen Siedlerkarren verlangt** (`data/units.json`, Einheit `Siedlerkarren`):

- Gebaeude: **Stellmacher** (Kennung `stellmacher`, verlangt Forschung **Baukunst**)
- Kosten: 200 Holz, 80 Metall, **150 Leder**, **100 Wolle**, **4 Pferde**, 5 Siedler, 300 Nahrung
- Voraussetzung: Forschung **Wagenbau**, Stufe 1

**Gruendungsregel** (`spieloekonomie.REGELN['gruendung']`):

- Gebuehr (4 x Hauspreis): 320 Holz, 200 Stein, 150 Nahrung
- Startpaket (2 x Hauspreis): 160 Holz, 100 Stein, 100 Nahrung
- Mindestbestand (Gebuehr + Paket) muss VOR der Gruendung in EINER Ausgangssiedlung liegen:
  **480 Holz, 300 Stein, 250 Nahrung**
- `karren` = `Siedlerkarren`, `forschung` = `Wagenbau` Stufe 1

**Woher Leder, Wolle und Pferde kommen** (`data/buildings.json`, Feld `wirkung`) - es sind KEINE
Rezept-Waren, sondern **Anlagen-Ertrag**:

| Gebaeude | Kennung | erzeugt |
|---|---|---|
| Schafszucht | `schafszucht` | Wolle |
| Rinderfarm | `rinderfarm` | Nahrung und Leder |
| Pferdezucht | `pferdezucht` | Pferde |
| Jaeger | `jaeger` | Nahrung und Leder (Jagd) |

`data/warenrezepte.json` fuehrt zu Leder, Wolle und Pferden **nichts** - sie verhalten sich wie Holz
oder Stein (Ertrag je Stunde aus einer Anlage).

**Was dem Bot heute fehlt:**

- `BotDorf.vorraete` fuehrt nur `gold, holz, metall, nahrung, stein` (keine Waren, keine Tiere).
- `data/bot_bauplan.json` kennt den **Stellmacher nicht** (`grep -c stellmacher` = 0) und keine der
  drei Zuchten.
- `data/bot_wirtschaft.json` nennt Leder, Wolle und Pferde nicht.
- `src/werkstatt.py` nennt den Siedlerkarren nicht.
- Ein Bot gruendet heute ohne Karren (`siedlerkarren_pflicht: false`).

**Wie die Bot-Wirtschaft heute rechnet** (damit dein Entwurf dazu passt):

- `bot_dorf_ertrag` liefert den Stundenertrag eines Bot-Dorfes aus seinem Kartenprofil
  (`data/originalkarten/katalog.json`, Felder je Gelaendeart) - die EINE Lesestelle fuer Kern und
  Anzeige.
- Ernten laufen ueber `bot_dorf_wirtschaften` / `bot_dorf_ertrag`, gebucht wird ueber
  `bot_kasse_buchen` / `bot_kasse_setzen` (die Kasse ist die SUMME der Dorf-Vorrate).
- Gebaut wird aus `data/bot_bauplan.json`: je Taktik eine Liste von Gebaeuden mit Obergrenzen.
- Forschungen laufen ueber `bot_dorf_forschungsliste` und `data/bot_forschung.json`.
- Gruenden: `GameState.bot_dorf_gruenden` prueft `spieloekonomie.gruendungskosten()` und
  `REGELN['gruendung']`.

## Was du entwerfen sollst

1. **Datenschluessel** (Namen und Bedeutung), damit ein Bot-Dorf Leder, Wolle und Pferde halten und
   ernten kann. Additiv, alte Spielstaende muessen ohne Migration laden. Sag genau, in welcher Datei
   welcher Schluessel steht und welchen Vorgabewert er hat.
2. **Bauplan-Eintraege**: welche Anlagen (Kennungen) je Taktik, in welcher Reihenfolge, mit welcher
   Obergrenze - und **warum diese Zahl** (Ertrag je Stunde aus dem Kartenprofil, Bedarf fuer einen
   Karren, Wartezeit bis zum ersten Karren in Spieltagen). Nenne die Rechnung, nicht nur das Ergebnis.
3. **Ablauf im Bot-Takt** (Reihenfolge der Schritte): ernten, bauen, forschen, Karren bauen, gruenden.
   Wo genau kommt der Karrenbau hin, welche Bedingungen muessen gelten (Forschung, Gebaeude, Waren,
   Siedler), was passiert, wenn etwas fehlt.
4. **Grenzfaelle**: zu wenig Siedler, Waren fehlen teilweise, mehrere Doerfer gleichzeitig
   gruendungsbereit, Karren fertig aber Gebuehr fehlt, Bot verliert das Dorf mit dem Stellmacher.
5. **Pruefvorschlaege** (kein Code, nur Zusagen): welche Wachen beweisen, dass die Kette wirkt, und
   welche Gegenprobe zeigt, dass sie wirklich prueft (eine Wache, die nie rot war, ist unbelegt).
6. **Was NICHT geaendert werden darf** und warum dein Entwurf das einhaelt: Doerfer werden nie
   eingenommen, Angriffstruppen nie am Zielort stationiert, Anzeige und Kern lesen dieselbe Funktion,
   Anzeigetexte tragen echte Umlaute (Kennungen bleiben ASCII).

## Grenzen

- **Kein Code, keine Datei im Projekt aendern, kein git-Befehl.** Du liest nur.
- Keine Zahl erfinden: wenn du eine Zahl nicht aus den genannten Dateien ableiten kannst, schreib
  `VORSCHLAG` dazu und nenne die Annahme.
- Keine zweite Handliste: alles, was in `data/*.json` steht, wird von dort gelesen.
- Deutsch, Markdown, Tabellen, **keine Emojis**, keine Gedichte.

## Antwortformat

Genau **eine** Markdown-Datei mit diesen Abschnitten:

1. `## Kurzfassung` (5 Zeilen)
2. `## Datenschluessel` (Tabelle: Datei, Schluessel, Typ, Vorgabewert, Bedeutung)
3. `## Bauplan` (Tabelle je Taktik: Anlage, Anzahl, Begruendung mit Rechnung)
4. `## Ablauf im Bot-Takt` (nummerierte Schritte mit Bedingungen)
5. `## Grenzfaelle` (Tabelle: Fall, Verhalten, Begruendung)
6. `## Pruefvorschlaege` (Wache, Zusage, Gegenprobe)
7. `## Offene Punkte` (was nur Daniel entscheiden kann, mit Empfehlung zuerst)
