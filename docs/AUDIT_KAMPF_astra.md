# Regelgutachten Kampf — astra, 04.10.2026

**Einsatz 1 des Plans `docs/PLAN_ASTRA_EINSATZ.md`.** Modell `gpt-6-astra`, ein Umlauf,
kleiner Kontext (~4.300 Token), keine Werkzeuge, Dauer 1 m 15 s, Kosten ~0,40 EUR.
Auftrag: Handbuchtext wörtlich + Beschreibung meines Ablaufs → jede Abweichung mit Zitat.

**Meine Nachprüfung:** Jedes Zitat habe ich am wörtlichen Handbuchtext
(`docs/original/Spielanleitung_2009_Textfassung.txt`, Seiten 20–23) nachgeschlagen. Unten steht
je Befund, was gilt und was geändert wurde.

---

## Bestätigte Fehler — geändert

### 1. Fernkampf war nicht gleichzeitig (astra-Nr. 8)
**Handbuch Seite 22:** „(Gleichzeitig bedeutet, das Verteidiger und Angreifer ZUERST feuern und
ANSCHLIEßEND die Verluste auf beiden Seiten berechnet werden)."
**Vorher:** Ich rechnete die Angreifer-Salve samt Toten ab und ließ erst danach den Verteidiger
schießen — gefallene Schützen schossen also nicht mehr.
**Jetzt:** Alle Schüsse beider Seiten werden zuerst bestimmt, danach wird Schaden verteilt. Ein
Schütze, der in derselben Salve fällt, hat geschossen.
**Belegt durch:** Prüfung „Fernkampf ist wirklich gleichzeitig".

### 2. Der Verteidiger stürmte mit (astra-Nr. 12)
**Handbuch Seite 22:** „Als nächstes stürmen die angreifenden Nahkampfeinheiten nacheinander zu
einer zufälligen verteidigenden Nahkampfeinheit." — und: „Nach alle angreifenden Einheiten
gekämpft haben, beginnt die nächste Kampfsequenz."
**Vorher:** Nach den Angreifern ließ ich auch jeden verteidigenden Nahkämpfer einen eigenen
Zweikampf beginnen — doppelte Angriffe.
**Jetzt:** Nur der Angreifer stürmt. Der Verteidiger schlägt ausschließlich **innerhalb** des
Zweikampfs zurück (dort ist „anschließend die jeweils andere Einheit dran").
**Belegt durch:** Prüfung „im Nahkampf stürmt nur der Angreifer".

### 3. Zweikampf war ein einzelner Schlag (astra-Nr. 15)
**Handbuch Seite 22/23:** „Die beiden Einheiten kämpfen solange, bis eine der beiden tot ist,
oder flieht." Und: „Der Zweikampf zweier Einheiten läuft in Kampfrunden ab."
**Jetzt:** `_zweikampf` läuft abwechselnd in Runden, bis eine Seite tot oder geflohen ist;
Reihenfolge nach MU, bei Gleichstand der Verteidiger.
**Belegt durch:** Prüfung „mehrere Schläge im selben Zweikampf".

### 4. Nahkampf wich nicht auf Fernkämpfer aus (astra-Nr. 13)
**Handbuch Seite 22:** „Sind keine verteidigenden Nahkampfeinheiten mehr übrig werden die
verteidigenden Fernkampfeinheiten angegriffen."
**Vorher:** Ich brach ab, wenn keine Nahkampfziele mehr da waren.
**Jetzt:** Ausweichen auf die Fernkämpfer des Verteidigers.
**Belegt durch:** Prüfung „Nahkampf weicht auf Fernkämpfer aus".

### 5. Falsche Abbruchbedingung (astra-Nr. 20)
**Handbuch Seite 22:** „Die Schlacht ist vorbei, sobald eine der beiden Armeen keine
Nahkampfeinheiten mehr hat, oder 10 Kampfsequenzen vorüber sind."
**Vorher:** Ich prüfte auf Fußtruppen (Nahkampf **und** Fernkampf).
**Jetzt:** Abbruch, wenn eine Seite keine **Nahkampf**einheiten mehr hat.

### 6. Nur der Angreifer verlor Gerät (astra-Nr. 26)
**Handbuch Seite 23:** „Der Verlierer verliert einen Teil seiner **stationierten** bzw.
mitgeschickten Karren und Belagerungswaffen."
**Vorher:** Nur beim Angreifer behandelt.
**Jetzt:** Beide Seiten; beim Verteidiger dessen stationierte Karren
(`verteidiger_karren`), Ergebnis in `geraete_verloren_verteidiger`.

### 7. Erschöpfung im falschen Takt (astra-Nr. 16)
**Handbuch Seite 23:** „Der Sieger eines Zweikampfes … Seine Angriffs- und Abwehrfähigkeit sinkt
bis zum Ende der Schlacht um einen Punkt, bei mehreren Zweikämpfen summiert sich die
Erschöpfung."
**Vorher:** Ich zog 1 AT/PA nach jedem **Schlag** ab.
**Jetzt:** Genau einmal je **gewonnenem Zweikampf**, summiert über die Schlacht.

**Wirkung, gemessen:** 200 Bürgerwehr greifen 1 Paladin an → Angreifer siegt in **einer**
Sequenz (58 gefallen). Das ist der Satz des Handbuchs: „So ist es möglich, auch starke Einheiten
mit der entsprechenden Übermacht an schwachen Einheiten zu besiegen." Vorher konnte die Masse
das nicht.

### 8. Keine Siegbedingung im Grenzfall (astra-Nr. 22)
**Handbuch Seite 23 widerspricht sich:** Der Kampf endet, wenn eine Armee keine Nahkampfeinheiten
mehr hat — als Sieger genannt werden aber nur „alle verteidigenden Einheiten tot oder geflohen"
bzw. „alle angreifenden Fußtruppen tot oder geflohen".
**Jetzt:** Umgesetzt wird der Wortlaut; greift danach keine Siegbedingung, ist die Schlacht
unentschieden und der Grund steht in `unsicher` im Bericht. **Offene Entscheidung für Daniel.**

## Geprüft, aber kein Fehler

- **Geflohene im Kampf (astra-Nr. 19):** astra vermutete, Geflohene könnten weiterkämpfen. Tun
  sie nicht — `_lebt()` schließt Geflohene aus, alle Aktions- und Ausgangsprüfungen nutzen es.
- **Unentschieden ohne Beute (astra-Nr. 23):** bereits umgesetzt.
- **Fluchtchance 40 % + 5 % je Sequenz (astra-Nr. 27):** entspricht dem Wortlaut.
- **Flucht ab LE unter 5, Rückkehr nach der Schlacht (astra-Nr. 18, 28):** entspricht.

## Zulässige Vereinfachungen (bleiben, sind gekennzeichnet)

- **Fernkampfschüsse:** Zufallsziel, ein Schuss je Schütze und Sequenz — das Handbuch nennt
  keine Schusszahl.
- **Ersatzwert für Geflohene:** LE bis 0 mit Mindestschaden 1 — Handbuch: „erleidet der getroffene
  trotzdem einen Schadenspunkt" ✓ belegt.
- **Fußtruppen-Definition** (Nahkampf + Fernkampf) — das Handbuch benutzt den Begriff, ohne ihn zu
  definieren; im Code als `ANNAHME` ausgewiesen.
- **Fluchtformel** (Wurf 1–100 größer als MU = Flucht) — Handbuch nennt nur die Tendenz.

## Was astra nicht prüfen konnte

astra-Nr. 3: Die Einheitenwerte (fehlendes MU bei Karren/Belagerung) waren nicht Teil des
Ausschnitts und daher für das Modell nicht prüfbar. Diese Werte stehen belegt in
`data/unit_stats.json`; die betroffenen Einheiten kämpfen nicht (Rolle, keine fehlende Zahl).

**Fazit:** 8 bestätigte Abweichungen, alle korrigiert und mit je eigener Prüfung abgesichert.
Die Zahl der Kampfprüfungen stieg von 33 auf 42, der Gesamtprüflauf auf 120.
