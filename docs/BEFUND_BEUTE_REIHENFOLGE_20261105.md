# Befund: Beute-Reihenfolge (Kampfregel 4) - gemessen am 05.11.2026

**Warum dieses Blatt existiert.** Die Kampfregel 4 ist am 03.11.2026 abgesegnet worden:
"beim Verladen der Beute wird zuerst Gold genommen, danach alle uebrigen Rohstoffe in fester
Reihenfolge". Bevor ich sie baue, habe ich nachgerechnet, was sie WIRTSCHAFTLICH bedeutet - denn
heute verteilt `kampfbericht.beute_staffel` die Beute **anteilig** auf alle Rohstoffe, und dieser
Unterschied ist nicht kosmetisch.

## 1. Die beiden Modelle

- **Heute (anteilig):** jeder Rohstoff bekommt seinen Anteil an der mitnehmbaren Menge; ein Rest
  wird nach dem groessten Bestand aufgefuellt. Bei 1000 je Rohstoff und Platz fuer 120 kommen je
  rund 30 mit.
- **Regel 4 (nach Rang):** Gold zuerst, dann die uebrigen in fester Reihenfolge, jeweils
  `floor(Vorrat x Anteil)`, bis die Karren voll sind. Was nicht mehr passt, bleibt liegen.

## 2. Was das konkret aendert (gerechnet, echte Vorratsgroessen)

| Fall | Vorrat | Platz | Heute | Regel 4 |
|---|---|---|---|---|
| Dorf reich, kleiner Karren | 2000 Gold / je 2000 Holz, Stein, Nahrung | 120 | 30 / 30 / 30 / 30 | **120 Gold, sonst nichts** |
| Dorf arm, grosser Zug | 50 Gold / je 800 Holz, Stein, Nahrung | 400 | 8 Gold + 132/130/130 | **30 Gold + 370 Holz** |
| Gold knapp | 30 Gold / je 1000 Holz, Stein | 200 | 2 / 100 / 98 | **18 Gold + 182 Holz** |

## 3. Die Folge, die man kennen muss

**Mit kleinen Karren kommt nach Regel 4 ausschliesslich Gold zurueck - kein Holz, kein Stein.**
Wer baut, braucht Holz und Stein; die kaemen dann nur noch aus eigener Foerderung und aus grossen
Zuegen. Das ist eine bewusste Politik (Gold ist der knappste Stoff), aber es ist eine
**Wirtschaftsentscheidung**, nicht nur eine Ladevorschrift.

Der fruehere Fehler, der zu diesem Thema fuehrte, war ein anderer: bis 31.10.2026 frass der
alphabetisch erste Rohstoff die ganze Ladung (Holz 80 / Stein 0 statt 50/30). Die anteilige
Verteilung hat das behoben. Regel 4 wuerde das Prinzip "einer nimmt alles" **absichtlich**
zurueckbringen - mit Gold als Erstling.

## 4. Was ich deshalb NICHT gemacht habe

Keinen Code geaendert. Die Regel ist gebaut, sobald Daniel sie bestaetigt - Formel, Testfaelle und
Einbauort stehen fest (`kampfbericht._anteil_verladen` und `beute_staffel`, Reihenfolge aus
`data/resources.json`). Bis dahin bleibt es beim anteiligen Verladen, und das steht auch so in der
ehrlichen Luecke des Kampfberichts ("nicht geregelt, hier alphabetisch").

**Offen und Daniel gehoert die Entscheidung:** Frage 8 in `docs/FRAGEN_AN_DANIEL_20261105.md`.
