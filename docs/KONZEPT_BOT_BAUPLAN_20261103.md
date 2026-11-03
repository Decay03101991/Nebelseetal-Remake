# Konzept: Der Bot nutzt seine Karte wie der Spieler (S-8, Entwurf 03.11.2026)

**Vorgabe Daniel (03.11.2026):**
> Der bot sollte allerdings auch einige Jäger auf Wald felder stellen und seine karte mit gebäuden einfach
> sinnvoll nutzen je nach taktik die er verfolg. Das ganze wird sehr komplex werden ist aber wichtig damit
> bots wirkliche gegner sind und später auch wirklich handlungsfähig auf ähnlicher basis wie der spieler
> ist. Allerdings werden wir das sogut es geht einmal entwerfen und einbauen aber sinnvoll nach und nach
> ausbauen weil wir diese fähigkeitserweiterungen für bots später immer weiter ausbauen werden um das
> spielerlebnis zu verbessern

**Rang:** ENTWURF. Wird in Stufen gebaut, nicht in einem Schnitt.

## 1. Das gemessene Problem (nicht geschaetzt)

Drei Messungen dieser Sitzung zeigen, dass die Bot-Wirtschaft heute **nicht** an der Karte haengt:

| Messung | Ergebnis |
|---|---|
| Holzfäller 3 -> 5 (`anlagen_je_gebaeude`) | Dorfzahl unveraendert 3/4/4/1/3 |
| Holzfäller auf 99 (alle passenden Felder) | Erträge unveraendert (13,6 bzw. 22,3 Holz/h), aber **Rueckfall-Ertrag ohne Karte 396 Holz/h** und **Rinderfarm, Schafszucht, Pferdezucht wurden nicht mehr gebaut** (die Holzfäller belegten die Steppe-Felder) |
| Silra mit 5 Holzfällern und 13,6 Holz/h | Vorrat wuchs nur um 11 Holz je Spieltag; nach 24 Tagen 189 von 480 noetigen Holz |

**Ursache 1: der Ertrag kommt aus dem Kartenprofil, nicht aus den Anlagen.**
`bot_kartenprofil(karte)` rechnet Felder x Ertrag - unabhaengig davon, ob die Anlagen wirklich stehen.
Ein Dorf mit 48 Holzfällern erntet genau so viel wie eines mit 5. Damit ist jede Bauplan-Logik
wirkungslos: die Anlagen sind Bedingung, nicht Ursache.

**Ursache 2: die Anlagenzahl ist eine pauschale Zahl je Gebaeude**, gleich fuer jeden Bot und jede Karte.
Sie kann die Karte nicht ausnutzen und nimmt zugleich Feldern weg, die andere Anlagen brauchen
(Holzfäller auf Steppe gegen Rinderfarm).

**Ursache 3: es gibt keine Feld-Prioritaet.** `gebaeude_je_dorf` ist eine Liste; die Reihenfolge
entscheidet, wer die guten Felder bekommt - aber niemand sagt, welches Gebaeude welches Gelaende
BEVORZUGT.

## 2. Ziel

Ein Bot bewirtschaftet seine 10x10-Karte **wie der Spieler**:

- Jedes Feld traegt hoechstens eine Anlage (gilt schon).
- Der **Ertrag kommt aus den gebauten Anlagen auf ihren Feldern** (`gelaende.ertrag_pro_stunde` je Feld).
- Welche Anlagen gebaut werden, folgt aus **Taktik + Bedarf**, nicht aus einer festen Zahl.
- Verschiedene Taktiken bauen verschieden (ein Haendler baut Handelsgueter, ein Krieger Waffen und Wall).

## 3. Die Bausteine, in dieser Reihenfolge

### Stufe 1 - Ertrag aus den Anlagen (Fundament, ohne das nichts wirkt)

`bot_dorf_ertrag` rechnet kuenftig aus `dorf.bauten`: je Feld die Anlage und ihr Gelaende, summiert
ueber alle Felder. Das Kartenprofil bleibt **nur** als Vorschau ("was gaebe die Karte her"), nicht als
Ertrag. Folge: wer mehr Anlagen baut, erntet mehr - bis die Karte voll ist.

**Pruefzusage:** zwei Doerfer mit derselben Karte, eines mit 5 und eines mit 12 Holzfällern, ernten
unterschiedlich viel; ein Dorf ohne Anlagen erntet nichts.

### Stufe 2 - Feld-Prioritaeten je Gebaeude (Daten, kein Code)

In `data/bot_wirtschaft.json` (oder einer eigenen Datei) steht je Gebaeude, welche Gelaendearten es
**bevorzugt** und welche es nur als Notloesung nimmt:

```
holzfaeller:  bevorzugt wald, notfalls steppe (niedriger Ertrag)
jaeger:       bevorzugt wald, notfalls huegel
rinderfarm:   bevorzugt grasland, notfalls steppe
steinmetz:    bevorzugt berg, notfalls huegel
farm:         bevorzugt grasland, notfalls steppe
```

Damit kann ein Holzfäller keine Steppe belegen, die eine Rinderfarm besser braucht.

**Pruefzusage:** ein Dorf mit 3 Wald- und 3 Steppe-Feldern baut Holzfäller auf Wald und die Rinderfarm
auf Steppe; keine Anlage steht auf einem Feld, das eine bevorzugte Anlage braucht.

### Stufe 3 - Bauplan je Taktik (Daten)

Je Taktik eine geordnete Liste "was zuerst, wenn Platz und Vorrat da sind" - mit **Mindestzahlen**
statt fester Obergrenzen:

```
kriegerisch:  holzfaeller 3, farm 3, steinmetz 2, jaeger 2, schmiede 1, kaserne 1, wall ...
haendlerisch: holzfaeller 3, farm 3, goldmine 2, markt 1, naehstube 1 ...
defensiv:     holzfaeller 3, farm 3, steinmetz 3, wall, wachturm ...
```

Der Bot baut, was die Taktik verlangt, solange Felder frei sind - und **danach** fuellt er mit dem
besten verfuegbaren Ertrag auf (Restfelder).

**Pruefzusage:** zwei Bots mit derselben Karte, aber verschiedenen Taktiken, haben unterschiedliche
Anlagen; jeder hat die Mindestzahlen seiner Taktik.

### Stufe 4 - Bedarf statt Wunsch (spaet)

Der Bot rechnet seinen **Bedarf** aus dem Ziel (Gruendung: 680 Holz; Armee: X Eisen; Forschung: Y) und
baut so viele Anlagen, wie er dafuer braucht - begrenzt durch die Karte. Das ist der Punkt, an dem
"handlungsfaehig wie der Spieler" erreicht ist.

## 4. Was dabei NICHT passiert

- Doerfer werden nie eingenommen, Truppen nie am Zielort stationiert.
- Keine erfundenen Erträge: alles aus `gelaende.ertrag_pro_stunde` und `data/*.json`.
- Keine Zahl im Code, die Daniel nicht genannt hat.

## 5. Risiken

| Risiko | Gegenmittel |
|---|---|
| Ertrag aus Anlagen aendert die Balance aller bisherigen Messungen | Stufe 1 zuerst allein bauen, alle Bot-Wachen nachziehen, voller Sammellauf |
| Ein Bot baut 48 Holzfäller und nichts anderes | Stufe 2 (Prioritaeten) und Stufe 3 (Mindestzahlen je Taktik) direkt danach |
| Alte Spielstaende haben keine Feld-Anlage-Zuordnung | `dorf.bauten` ist schon je Feld gefuehrt; Rueckfall auf das Kartenprofil, wenn `bauten` leer ist |

## 6. Offene Fragen an Daniel

1. Sollen die Taktik-Bauplaene in `data/bot_bauplan.json` stehen (dort liegt schon ein Bauplan) oder in
   einer neuen Datei `data/bot_taktik_bauplan.json`? **Empfehlung:** dieselbe Datei erweitern, damit es
   EINE Quelle bleibt.
2. Wie viele Anlagen darf ein Bot **hoechstens** je Dorf bauen - alle freien Felder, oder eine Obergrenze
   je Taktik? **Empfehlung:** alle Felder, die die Taktik sinnvoll fuellt; Restfelder mit dem besten
   Ertrag.
