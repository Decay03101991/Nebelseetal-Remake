# Auftrag an das starke Modell: GEGENPRUEFUNG des S-6b-Entwurfs (03.11.2026)

## Rolle

Du bist der **Gegenpruefer**. Ein anderes Modell hat einen Entwurf geliefert; du pruefst ihn gegen die
gemessenen Fakten und gegen bekannte aehnliche Systeme. Du entwirfst **nichts Neues** und aenderst
**keine Datei** - du sagst, was falsch ist, was fehlt und was fehlerhaft begruendet ist.

## Die gemessenen Fakten (Wahrheit; weicht der Entwurf davon ab, ist der ENTWURF falsch)

1. **Warenhaltung liegt NICHT in einer Datendatei.** Die Vorraete eines Bot-Dorfes stehen im
   Dataclass `BotDorf` (`src/main.py`), Feld `vorraete`, heute nur `gold, holz, metall, nahrung, stein`.
   `data/bot_wirtschaft.json` enthaelt dagegen **Schalter, Anlagen und Lagerdeckel**, keine Vorratsstaende.
   Alles, was der Entwurf als neuen Schluessel in `bot_wirtschaft.json` ablegt, ist an der falschen Stelle.
2. Gebucht wird ausschliesslich ueber `bot_kasse_buchen` / `bot_kasse_setzen`; die Bot-Kasse ist die
   SUMME der Dorf-Vorrate. Ein direkter Schreibzugriff auf `bot.vorraete[...]` ist verboten (er landet
   in einem Zwischenergebnis).
3. Leder, Wolle und Pferde sind **Anlagen-Ertrag** aus `data/buildings.json` (Schafszucht -> Wolle,
   Rinderfarm -> Nahrung und Leder, Pferdezucht -> Pferde, Jaeger -> Leder aus der Jagd), **keine
   Rezept-Waren**; `data/warenrezepte.json` fuehrt sie nicht.
4. Ertragszahlen stehen in `gelaende.ertrag_pro_stunde` (je Gelaendeart) und das Kartenprofil eines
   Dorfes in `data/originalkarten/katalog.json` (`original_attribute.felder`, Summe 100). Der Stundenertrag
   wird daraus GERECHNET (`bot_dorf_ertrag`), nicht gesetzt.
5. Siedlerkarren (`data/units.json`): Stellmacher, 200 Holz, 80 Metall, 150 Leder, 100 Wolle, 4 Pferde,
   5 Siedler, 300 Nahrung, Forschung Wagenbau 1. Stellmacher verlangt Forschung **Baukunst**.
6. Gruendung (`spieloekonomie.REGELN['gruendung']`): Gebuehr 320 Holz, 200 Stein, 150 Nahrung; Startpaket
   160 Holz, 100 Stein, 100 Nahrung; Mindestbestand 480 Holz, 300 Stein, 250 Nahrung in EINER
   Ausgangssiedlung; `karren` = Siedlerkarren; `forschung` = Wagenbau Stufe 1.
7. Daniels Vorgabe fuer die Bot-Wirtschaft (02.11.2026): **drei Anlagen je Grundrohstoff**, zusammen
   12/12/12/9 je Stunde und Dorf. Neue Anlagen muessen sich in dieses Bild fuegen.
8. Doerfer werden **nie** eingenommen, Angriffstruppen **nie** am Zielort stationiert.
9. Anzeige und Kern lesen dieselbe Funktion (Muster F-04) - kein zweiter Rechenweg.

## Was du pruefen sollst

1. **Ablage**: Sind die vorgeschlagenen Datenschluessel an der richtigen Stelle (Dataclass, Datendatei,
   Migration)? Was genau muss anders?
2. **Rechnung**: Rechne die Anlagenzahlen selbst nach - Ertrag je Stunde, Bedarf je Karren (150 Leder,
   100 Wolle, 4 Pferde), Wartezeit in Spieltagen bis zum ersten Karren. Sag, welche Zahlen der Entwurf
   erfindet und welche aus den Dateien folgen.
3. **Kette**: Ist die Reihenfolge Baukunst -> Stellmacher -> Zuchten -> Wagenbau -> Karren -> Gruendung
   vollstaendig? Fehlt ein Glied, das den Bot blockiert (z. B. Baukunst nicht in den Forschungslisten)?
4. **Grenzfaelle**: Welche fehlen, welche sind falsch begruendet? Pruefe besonders den Fall "Karren
   fertig, Gebuehr fehlt" und "mehrere Doerfer gruendungsbereit".
5. **Vergleichssysteme (Vorgabe Daniel 03.11.2026)**: Wo der Entwurf etwas erfinden MUSS (Ertragszahlen,
   Obergrenzen, Prioritaeten), nenne **zwei bis drei bekannte aehnliche Systeme** (vergleichbare
   Aufbau- oder Browserspiele, Open-Source-Aufbauspiele, gaengige Wirtschaftssimulationen) und sage je
   Quelle, warum sie taugt und was daraus fuer Nebelseetal folgt. Gezielt, keine Linklisten.
6. **Pruefvorschlaege**: Welche der vorgeschlagenen Wachen pruefen wirklich? Wo fehlt die Gegenprobe?

## Grenzen

- Kein Code, keine Datei aendern, kein git.
- Keine Zahl erfinden: was du nicht aus den genannten Stellen ableiten kannst, ist `VORSCHLAG` mit Annahme.
- Deutsch, Markdown, Tabellen, keine Emojis.

## Antwortformat

Genau eine Markdown-Datei:

1. `## Urteil in drei Saetzen` (ist der Entwurf einbaubar: ja / mit Aenderungen / nein)
2. `## Fehler` (Tabelle: Stelle im Entwurf, was falsch ist, Beleg, Korrektur)
3. `## Nachgerechnete Zahlen` (Tabelle: Groesse, Rechnung, Ergebnis, Quelle)
4. `## Fehlende Glieder` (Liste mit Begruendung)
5. `## Vergleichssysteme` (Tabelle: System, warum taugt es, Uebertragung)
6. `## Pruefvorschlaege` (Tabelle: Wache, Zusage, Gegenprobe)
7. `## Was der Entwurf richtig macht` (kurz, damit die Sitzung es nicht wegwirft)

---

# DER ZU PRUEFENDE ENTWURF

## Kurzfassung
Der Bot erhält die Vorratsschlüssel Leder, Wolle und Pferde sowie einen Siedlerkarren je Dorf. Neue Bauplan-Einträge für Stellmacher, Schafszucht, Rinderfarm und Pferdezucht werden ergänzt. Die Waren entstehen als Anlagen-Ertrag, ohne neue Rezepte. Der Karrenbau wird vor der Gründung eingefügt, mit harten Bedingungen. Gründung erfolgt nur mit Siedlerkarren und Mindestbestand in einer Ausgangssiedlung.

## Datenschluessel
Tabelle: Datei, Schluessel, Typ, Vorgabewert, Bedeutung

| Datei | Schluessel | Typ | Vorgabewert | Bedeutung |
|---|---|---|---|---|
| data/bot_wirtschaft.json | leder | Zahl | 0 | Vorrat an Leder in der globalen Bot-Kasse (Summe aller Dorf-Vorräte) |
| data/bot_wirtschaft.json | wolle | Zahl | 0 | Vorrat an Wolle in der globalen Bot-Kasse |
| data/bot_wirtschaft.json | pferde | Zahl | 0 | Vorrat an Pferden in der globalen Bot-Kasse |
| data/bot_wirtschaft.json | siedlerkarren | Zahl | 0 | Anzahl gebauter Siedlerkarren je Bot-Dorf (kein globaler Kassenwert) |

Erläuterung: Die drei Waren werden additiv in die bestehende Vorratsliste aufgenommen. Der Vorgabewert 0 stellt sicher, dass alte Spielstände ohne Migration laden. Der Siedlerkarren wird je Dorf geführt, weil die Gründung aus einer bestimmten Siedlung einen Karren benötigt.

## Bauplan
Die genauen Taktiknamen stehen in `data/bot_bauplan.json`. Da die Gründungsanforderungen für alle Taktiken identisch sind, erhalten alle Taktiken dieselben neuen Einträge. Die Reihenfolge innerhalb der Bauplan-Liste: `stellmacher` vor `schafszucht`, `rinderfarm`, `pferdezucht`.

Tabelle je Taktik: Anlage, Anzahl, Begründung mit Rechnung

| Anlage (Kennung) | Anzahl (Obergrenze) | Begruendung mit Rechnung |
|---|---|---|
| stellmacher | 1 | Wird einmal benötigt, um Siedlerkarren zu bauen; verlangt Forschung Baukunst. |
| schafszucht | 1 | Bedarf pro Karren: 100 Wolle. VORSCHLAG Ertrag: 1 Wolle/h. Wartezeit mit 1 Anlage: 100 h = 4,2 Tage (Formel T = Bedarf / (n * E * 24)). |
| rinderfarm | 3 | Bedarf pro Karren: 150 Leder. VORSCHLAG Ertrag: 0,5 Leder/h. Mit 1 Anlage: 300 h = 12,5 Tage. Mit 3 Anlagen: 150 h = 6,25 Tage. Gewuenschte maximale Wartezeit 5 Tage, daher aufrunden(150 / (0,5 * 24 * 5)) = 3. |
| pferdezucht | 1 | Bedarf pro Karren: 4 Pferde. VORSCHLAG Ertrag: 0,25 Pferde/h. Mit 1 Anlage: 16 h = 0,67 Tage. |

Die tatsächlichen Ertragswerte stammen aus `data/originalkarten/katalog.json`. Die oben genannten Erträge sind VORSCHLAG und müssen durch die echten Katalogdaten ersetzt werden. Die Obergrenzen sind entsprechend neu zu berechnen: `n = aufrunden(Bedarf / (Ertrag_pro_Stunde * 24 * gewuenschte_Wartezeit_Tage))`.

## Ablauf im Bot-Takt
1. Ernten: `bot_dorf_wirtschaften` bucht die Erträge aller vorhandenen Anlagen, inklusive Leder (Rinderfarm, Jaeger), Wolle (Schafszucht) und Pferde (Pferdezucht). Bedingung: Anlage vorhanden, sonst kein Ertrag.
2. Bauen: Aus `data/bot_bauplan.json` wird das nächste Gebäude gemäß Taktik und Reihenfolge gebaut, sofern Ressourcen vorhanden. Neue Priorität: wenn Baukunst erforscht und Stellmacher-Obergrenze nicht erreicht, Stellmacher bauen; danach Schafszucht, Rinderfarm, Pferdezucht bis Obergrenze. Bedingung: Forschung Baukunst für Stellmacher, sonst normale Baupriorität.
3. Forschen: `bot_dorf_forschungsliste` wählt die nächste Forschung, insbesondere Wagenbau Stufe 1 vor dem Karrenbau. Bedingung: Forschungsvoraussetzungen erfüllt.
4. Karren bauen: Wenn Forschung Wagenbau Stufe 1, Stellmacher vorhanden, Vorräte Leder >= 150, Wolle >= 100, Pferde >= 4, Siedler >= 5, Holz >= 200, Metall >= 80, Nahrung >= 300, dann einen Siedlerkarren bauen: Ressourcen abziehen und `siedlerkarren` im Dorf um 1 erhöhen. Nur einmal pro Takt. Wenn etwas fehlt, Schritt überspringen, keine Teilabzüge.
5. Gruenden: `GameState.bot_dorf_gruenden` prüft `REGELN['gruendung']`: Mindestbestand 480 Holz, 300 Stein, 250 Nahrung in einer Ausgangssiedlung und `siedlerkarren` >= 1. Wenn erfüllt, Ressourcen und Karren verbrauchen, neues Dorf gründen.

## Grenzfaelle
Tabelle: Fall, Verhalten, Begruendung

| Fall | Verhalten | Begruendung |
|---|---|---|
| Zu wenig Siedler | Karrenbau wird übersprungen, keine Ressourcen werden reserviert. Sobald Siedler >= 5, wird im nächsten Takt gebaut. | Vermeidet Blockade des gesamten Takts; keine Teilabzüge erhält Übersicht. |
| Waren fehlen teilweise | Karrenbau wird übersprungen, vorhandene Waren bleiben unangetastet. Sobald alle Waren vollständig sind, wird gebaut. | Keine Teilabzüge, die Produktion läuft weiter. |
| Mehrere Doerfer gruendungsbereit | Es wird nur ein Karren pro Takt gebaut. Priorität: Dorf mit höchstem Überschuss über dem Mindestbestand oder die erste Dorf-ID. Andere warten. | Verhindert gleichzeitige Ressourcenverknappung; Reihenfolge ist deterministisch. |
| Karren fertig, Gebuehr fehlt | Karren bleibt im Dorf, wird nicht verbraucht. Gruendung wird verschoben, bis Gebuehr in einer Ausgangssiedlung liegt. | Karren ist kein Verbrauchsgut für andere Zwecke; kein Verlust. |
| Bot verliert Dorf mit Stellmacher | Tritt nicht ein, da Doerfer nie eingenommen werden. Falls durch externe Mechanik, muss in anderem Dorf neuer Stellmacher gebaut werden (sofern Baukunst erforscht). | Regelwerk sieht keine Eroberung vor; Entwurf hält das ein. |

## Pruefvorschlaege
Tabelle: Wache, Zusage, Gegenprobe

| Wache | Zusage | Gegenprobe |
|---|---|---|
| Baukette | Nach Erreichen von Baukunst wird innerhalb von X Takten ein Stellmacher gebaut. | Vor Baukunst darf kein Stellmacher in der Bauliste stehen; Wache muss vorher rot sein, sonst prüft sie nicht. |
| Warenproduktion | Nach Bau von Schafszucht, Rinderfarm, Pferdezucht steigen Leder, Wolle, Pferde im Vorrat. | Entfernt man eine Anlage oder setzt den Ertrag auf 0, darf sich der entsprechende Vorrat nicht erhöhen. |
| Karrenbau | Sobald alle Bedingungen erfüllt sind, wird ein Siedlerkarren gebaut und die Waren werden abgezogen. | Setzt man Leder auf 149, bleibt der Karrenbau aus; Wache muss vorher rot sein und nach Erreichen von 150 grün. |
| Gruendungspflicht | Der Bot gründet nie ohne Siedlerkarren, wenn `siedlerkarren_pflicht: true`. | Setzt man den Siedlerkarren auf 0, findet keine Gruendung statt, selbst wenn Mindestbestand vorhanden. |

## Offene Punkte
1. Exakte Obergrenzen je Taktik: hängen von den tatsächlichen Ertragswerten in `data/originalkarten/katalog.json` ab. Empfehlung: Rinderfarm 3, Schafszucht 1, Pferdezucht 1, Stellmacher 1 als Ausgangspunkt.
2. Karrenbestand: Soll der Siedlerkarren je Dorf oder global geführt werden? Empfehlung: je Dorf, weil Gründung aus einer bestimmten Siedlung erfolgt.
3. Mehrere Gruendungen: Darf der Bot mehrere Karren gleichzeitig bauen? Empfehlung: nein, maximal einer pro Takt.
4. Anzeige: Sollen Leder, Wolle, Pferde in der globalen Kasse angezeigt werden? Empfehlung: ja, über bestehende Anzeigelogik (eine Lesestelle).
5. Priorisierung im Bauplan: Müssen die neuen Anlagen in allen Taktiken gleich priorisiert werden? Empfehlung: ja, weil die Gruendungsanforderungen identisch sind.