# Befund: Siedler, Bots und die Langzeit-Ökonomie (gemessen 31.10.2026)

**Anlass.** Daniel nach dem Balancing-Test: „das mit der siedlergrenze gibt mir irgendwie zu denken
wir müssen kuken was wir mit der siedler nutzung noch falsch machen wenn es sich nicht richtig ausgeht.
Vllt liegt es daran das wir auf einzelspieler gegen bots umstellen? oder warum haben wir zwar eine
siedler obergrenze kommen aber nicht mit den siedler zahlen zurecht?“

**Kurzantwort: Die Siedlergrenze ist original und in Ordnung. Das Problem liegt bei den BOTS.**

---

## 1. Die Siedlerregel ist belegt und wird richtig gerechnet

| Regel | Wert | Quelle |
|---|---|---|
| Start einer Siedlung | 10 Siedler | Handbuch 2009, Z. 233 („Jeder Spieler beginnt das Spiel mit 10 Siedlern, 100 Holz und 100 Steinen“) |
| Zuwachs | 1 Siedler je Stunde bis zur Grenze | Handbuch 2009, Z. 361 |
| Grenze je Siedlung | 10, +5 je Haus | Handbuch 2009, Z. 362–363 |
| Höchstzahl Siedlungen | 6 | Handbuch 2009, Z. 53 |
| Eine Einheit kostet | 1 Siedler (Karren 1–20) | `data/units.json`, Feld `kosten.siedler` |

Daraus: 10 Häuser je Siedlung → 60 Siedler → **maximal 360 Einheiten im Reich**. Das ist die
Originalrechnung, nicht unser Fehler.

## 2. Der Fehler: Bots haben keine Wirtschaft

Gemessen (`main.GameState()`, Karte erzeugt, 30 Spieltage Bot-Takte simuliert):

| Bot | Armee nach 30 Spieltagen | Gold | Siedler |
|---|---|---|---|
| Haug | **1** Kurzbogenschütze | 35 | 9 |
| Brynhild | **1** Streuner | 42 | 9 |
| Krank | **4** Streuner | 26 | 6 |

Ursachen, jede im Code belegt:

1. **Bots produzieren nichts.** Ihre Vorräte entstehen einmalig aus
   `botkern.VORSCHLAG_START_VORRAETE` (`bot_vorrat_anlegen`, main.py) und wachsen nie nach.
2. **Bots haben keine Siedlerwirtschaft.** Sie bekommen 10 Siedler geschenkt und verlieren einen je
   Einheit; Nachwuchs gibt es nicht.
3. **Ein Bot kauft höchstens EINE Einheit je Stundentakt** (`bot_armee_aufstellen`) — bei leeren
   Vorräten also fast nie.
4. **Bots haben keinen Wall** (`wall_stufe` 0) — die Wallschwellen des Handbuchs wirken dadurch nur
   gegen den Spieler, nie für ihn.

**Folge für das Spielgefühl:** Der Spieler steht nach sieben Spieltagen bei ~168.000 Rohstoffen, die
Bots bei ein paar Dutzend. Ein Angriff mit 40 Kriegern (Kosten: 20.000 Gold) trifft auf 1–4 Gegner.
Die *Siedlergrenze* ist deshalb nicht der Engpass — der Gegner ist keiner.

## 3. Was daraus folgt (Vorschlag, keine Entscheidung)

1. **Bots bekommen eine echte Wirtschaft:** eigene Siedlungen mit Erträgen aus `data/buildings.json`,
   Siedlerwachstum 1/h bis zur Grenze, Einheitenkauf wie beim Spieler (belegte Preise, Siedler
   verbrauchend), Wallausbau nach Punkten.
2. **Bots bekommen einen Wall**, damit die belegten Schwellen (Handbuch S. 21) auch für den Spieler
   gelten.
3. **Erst danach** ist die Frage „reicht meine Armee“ überhaupt sinnvoll zu stellen — heute ist die
   Antwort immer ja.

## 4. Nebenbefund: die Wallschwellen sind korrekt gelesen

Handbuch 2009, Z. 1175–1211 (Tabelle): **Bollwerk (10) = 1.000 Schlagkraft Fußtruppen UND 1.000
Schlagkraft Belagerungswaffen.** Der Beispielsatz (Z. 1215–1217) bestätigt beide Spalten:
„Eine verstärkte Mauer deren Zustand nur noch 50 % beträgt, kann mit 245 Schlagkraftpunkten von
Fußtruppen und 350 Schlagkraftpunkten von Belagerungswaffen erstürmt werden“ — Stufe 7 hat 490/700,
die Hälfte ist 245/350.

`data/buildings.json` führt genau diese Zahlen; `src/kampf.py` prüft beide Schwellen (SK der
Nahkämpfer und SK der Belagerungswaffen). **Es gibt hier keinen Fehler** — Daniels Erinnerung
(„1.000 ist die Belagerungs-Schlagkraft“) ist die halbe Wahrheit: die 1.000 stehen in *beiden*
Spalten.
