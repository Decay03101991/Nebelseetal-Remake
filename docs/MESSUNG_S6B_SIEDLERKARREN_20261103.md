# Messung S-6b: Was der Bot für einen Siedlerkarren wirklich braucht (03.11.2026, 19:0x)

## Daniels Entscheidung (Wortlaut)

> „Ein bot muss genau wie der spieler erstmal einen Siedlerkarren bauen und die nötigen ressourcen
> haben bevor er gründen kann genau wie der spieler mit der abweichung das er ein bot ist“

Damit ist `siedlerkarren_pflicht` in `data/bot_gruendung.json` **auf `true` zu stellen** - aber erst,
wenn ein Bot den Karren wirklich bauen kann. Diese Messung zeigt, was dafür fehlt.

## Was der KERN verlangt (belegt, nicht geschätzt)

`data/units.json`, Einheit `Siedlerkarren` (Kategorie Karren):

| Gegenstand | Wert |
|---|---|
| Gebäude | **Stellmacher** |
| Kosten | 200 Holz, 80 Metall, **150 Leder**, **100 Wolle**, **4 Pferde**, 5 Siedler, 300 Nahrung |
| Voraussetzung | Forschung **Wagenbau**, Stufe 1 |

`spieloekonomie.REGELN['gruendung']` nennt denselben Karren und dieselbe Forschung:

| Regel | Wert |
|---|---|
| `karren` | `Siedlerkarren` |
| `forschung` | `Wagenbau`, `stufe` 1 |
| Gebühr (4 x Hauspreis) | 320 Holz, 200 Stein, 150 Nahrung |
| Startpaket (2 x Hauspreis) | 160 Holz, 100 Stein, 100 Nahrung |
| Mindestbestand (Gebühr + Paket) | **480 Holz, 300 Stein, 250 Nahrung** in EINER Ausgangssiedlung |

`data/buildings.json`: **Stellmacher** (`stellmacher`) baut die Karren (Handkarren, Einspänner,
Zwei-, Handelskarawane, Siedlerkarren) und verlangt **Baukunst**.

## Was dem Bot heute fehlt (gemessen an den Datendateien)

| Prüfung | Ergebnis | Beleg |
|---|---|---|
| Bot-Bauplan kennt den Stellmacher | **nein** | `grep -c stellmacher data/bot_bauplan.json` = 0 |
| Bot-Wirtschaft kennt Waren (Leder, Wolle, Pferde) | **nein** | `data/bot_wirtschaft.json` nennt keine davon |
| `werkstatt.py` kennt den Siedlerkarren | **nein** | `Siedlerkarren` kommt in `src/werkstatt.py` nicht vor |
| Bot-Dorf-Vorräte | nur `gold, holz, metall, nahrung, stein` | `bot_dorf_ertrag` / `BotDorf.vorraete` |

**Der eigentliche Blocker ist nicht der Karren, sondern die Warenhaltung:** ein Bot-Dorf führt heute
keine Waren. Damit kann es weder Leder noch Wolle noch Pferde haben - und ohne die gibt es keinen
Karren.

## Was S-6b deshalb umfassen muss (Reihenfolge)

1. **Warenhaltung für Bot-Dörfer**: `BotDorf.vorraete` um `leder`, `wolle`, `pferde` erweitern (additiv,
   alte Spielstände laden ohne Migration), Buchung nur über `bot_kasse_buchen`/`bot_kasse_setzen`.
2. **Werkstattkette im Bot-Bauplan**: Stellmacher plus die Gebäude, die Leder, Wolle und Pferde
   liefern (noch zu messen: `data/buildings.json` + `warenrezepte.json` - welche Anlage erzeugt was).
3. **Warenherstellung oder Handel für Bots**: dieselbe Rezeptquelle wie der Spieler
   (`warenrezepte.json`), keine zweite Handliste.
4. **Karrenbau als Bot-Aktion**: Kosten und Voraussetzung aus `units.json` + `REGELN['gruendung']`,
   fünf Siedler aus dem Ausgangsdorf, Forschung Wagenbau 1.
5. **Erst dann** `siedlerkarren_pflicht: true` und die Messung über 24 Spieltage (jeder Bot vier
   Dörfer, mit Karren).

## Offene Messlücke (nächster Schritt vor dem Bau)

Welche Gebäude Leder, Wolle und Pferde erzeugen und welche Forschung sie verlangen, steht noch nicht
gemessen in diesem Dokument. Das ist der erste Schritt der Bau-Sitzung: `data/buildings.json` nach
den Wirkungen durchsuchen (`leder`, `wolle`, `pferd`), dann die Kette aus `warenrezepte.json`
ableiten - **keine Handliste tippen**, die Quelle ist die Datei.

## Grenzen

- Dörfer werden nie eingenommen, Angriffstruppen nie am Zielort stationiert.
- Die fünf Siedler des Karrens ziehen aus dem Ausgangsdorf um - das macht S-6 schon.
- Kein Sonderweg „Bot zahlt Gold statt Waren“: Daniels Vorgabe ist die echte Kette, die Abweichung
  ist nur, dass ein Bot sie selbst beschafft.
