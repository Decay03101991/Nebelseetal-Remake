# Mustervorlagen für Karten (geprüft)

**Quelle:** `deepseek-v4-pro`, 2–3 Minuten je Vorlage, Rohantworten in `docs/audits/muster_siedlung.txt`
und `docs/audits/muster_welt.txt` (je 0,04–0,12 USD — gegenüber astra Faktor 10 günstiger).

**Prüfung:** Beide Raster habe ich durch unsere eigenen Module laufen lassen: Feldzahl, Zählung je
Geländeart, Mindestbesatz, Sumpfgrenze und Höchstertrag. Ergebnis: **beide gültig.**

---

## Siedlungskarte 1: „Nebelseeufer" — Mana-Rush

Erzwingt: früh Tempel an den Nebelsee stellen, weil Mana dort **fünffach** fließt (5/h statt 1/h).
Dafür ist Stein knapp und bremst Militär und Mauern.

```
nebelsee  nebelsee  nebelsee  nebelsee  sumpf     sumpf   wald     huegel
nebelsee  nebelsee  nebelsee  grasland  grasland  wald    wald     berg
nebelsee  nebelsee  grasland  grasland  grasland  wald    steppe   huegel
nebelsee  grasland  grasland  grasland  wald      steppe  steppe   huegel
grasland  grasland  wald      steppe    huegel    berg    berg     sumpf
```

Zählung (nachgeprüft): Nebelsee 10 · Grasland 10 · Wald 6 · Steppe 4 · Hügel 4 · Berg 3 · Sumpf 3 = 40
Mindestbesatz erfüllt · Sümpfe 3 von höchstens 6

**Höchstertrag bei Vollausbau (meine Rechnung, bestes Gebäude je Feld):**
Mana **50/h** · Holz 32/h · Stein 20/h · Nahrung 40/h

*Die Vorlage selbst nannte Holz 24/h und Stein 20/h — sie rechnete nur mit dem Hauptgelände
(Holzfäller auf Wald). Auf Steppe liefert der Holzfäller aber 2/h, deshalb 32. Beides ist richtig,
meine Zahl ist die Obergrenze.*

**Größter Nachteil:** nur 3 Berg und 4 Hügel → höchstens 20 Stein/h. Mauern und Werkstätten
(24–32 Holz / 16–24 Stein laut Vorschlagspreis) gehen langsam. Ausgleich: Mana statt Stein skalieren.

## Siedlungskarte 2: „Erzadern" — Schwermetall-Wirtschaft

Erzwingt: die vielen Berge mit Steinmetz, Erz- und Goldmine belegen und daraus Schmiede und Militär
bauen. Holz und Nahrung sind rar und müssen streng eingeteilt werden.

```
berg   berg   berg   berg   huegel  huegel  wald     grasland
berg   berg   berg   huegel  huegel  wald    grasland  grasland
berg   berg   huegel  huegel  wald    steppe  sumpf     sumpf
berg   berg   berg   huegel  steppe  steppe  grasland  sumpf
berg   steppe  sumpf  sumpf  grasland grasland nebelsee huegel
```

Zählung (nachgeprüft): Berg 13 · Hügel 8 · Grasland 6 · Steppe 4 · Wald 3 · Sumpf 5 · Nebelsee 1 = 40
Mindestbesatz erfüllt · Sümpfe 5 von höchstens 6

**Höchstertrag bei Vollausbau (meine Rechnung):**
Stein **68/h** · Holz 20/h · Nahrung 24/h · Mana 5/h

*Die Vorlage nannte Stein 36/h, weil sie die 13 Bergfelder auf 5 Steinmetz / 5 Erzmine / 3 Goldmine
aufteilte (ein sinnvoller Spielplan). Wer alle Bergfelder mit Steinmetz belegt, kommt auf 68/h —
das ist die Obergrenze, nicht der Plan.*

**Größter Nachteil:** nur 3 Wald → 20 Holz/h, nur 6 Grasland → 24 Nahrung/h. Ausgleich: Stein und
Metall im Überschuss erzeugen und gegen Holz und Nahrung tauschen.

---

## Weltkarte (Limbus) — Vorlage mit einer Korrektur

Die Vorlage ordnete die sechs alten Weltnamen als **Felder in ein** 20×20-Raster. Das ist der
**falsche Bezug**: die sechs Namen waren **eigene Unterdomänen** (`midgard.nebelseetal.de` usw.),
also die **Dimensionen** selbst. Belegt durch die alte Portalseite:

> „Diese bestehen aus drei Zahlen. Die ersten beiden (X und Y) zeigen die Position Eurer Welt, auf
> einem zweidimensionalen Raster, **in Eurer Dimension** an. Die dritte Zahl (Z) zeigt die
> **Dimension** an, in der sich Eure Welt befindet. […] Es gibt 20 Dimensionen, in jeder Dimension
> sind 20 mal 20 Felder frei für Spielerwelten."

**Richtiges Modell (belegt):**

| Regel | Wert | Quelle |
|---|---|---|
| Dimensionen | 20 | portal.php 2005, Z. 22 |
| Felder je Dimension | 20 × 20 = 400 Spielerwelten | portal.php 2005, Z. 22 |
| Koordinaten einer Welt | (X, Y, Z) — X/Y in der Dimension, Z = Dimension | portal.php 2005 |
| In andere Dimension reisen | kostet **viel** Mana; erst in der eigenen Dimension suchen | portal.php 2005 |
| Koordinatenwechsel | 5.000 Mana aus **einer** Siedlung, höchstens einmal je 24 h | portal.php 2005, Z. 25 |
| Darstellung | eigene Welt **grün**, fremde **rot**, über einer Spiralnebelstruktur | portal.php + GameStar-Screenshot 1838856 |

Die konkreten Koordinaten der Vorlage sind damit nur noch für **eine** Dimension brauchbar
(Spielerwelten) — die sechs Namen gehören in die Dimensionenliste, nicht ins Raster.
Aufgabe für die nächste Sitzung: `data/welten.json` und `src/welt.py` auf dieses Modell umstellen.
