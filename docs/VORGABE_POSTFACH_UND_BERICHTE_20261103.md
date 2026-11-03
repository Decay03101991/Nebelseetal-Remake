# Vorgabe: Postfach, Kampfberichte und Angriffswarnung (Daniel, 03.11.2026, 19:00)

## Wortlaut

> „Außerdem wenn ein Spieler angegriffen wird,. soll er damit er es auch mitbekommt während der wegzeit
> zum spieler, der spieler einen roten rahmen um sein hauptspielfenster in hellem rot sieht. Nachdem der
> angriff vorüber ist bleibt dann nur noch der Bericht. Der Spieler erhält einen Verteidigungsbericht,
> sowie der Angreifer einen Angriffsbericht. Ein Erfolgreicher angriff egal ob spieler auf bot oder bot
> auf spieler erzeugt immer einen vollständigen kampfbericht über alle informationen des
> „angegriffenen“. Dafür sind die Postfächer gedacht. Dementsprechend übersichtlich gestaltet werden
> muss auch der Postkasten und die bots müssen die einkommenden infos auch möglichst weitgehend
> verwerten können. Daraus schließen ob ein weiterer angriff lohn usw. Genauso wie der spieler natürlich
> aus den Berichten eben das erfahren soll. Allerdings muss der spieler sich das selbst erschließen aus
> den Berichtinhalten.“

## Was daraus verbindlich folgt

| # | Regel | Anmerkung |
|---|---|---|
| 1 | Während ein Angriff **auf den Spieler** unterwegs ist, liegt ein **roter Rahmen in hellem Rot** um das Hauptfenster | nur solange die Wegzeit läuft; danach bleibt nur der Bericht |
| 2 | Der Angegriffene bekommt einen **Verteidigungsbericht**, der Angreifer einen **Angriffsbericht** | beide Seiten, bei Spieler→Bot **und** Bot→Spieler |
| 3 | Ein **erfolgreicher** Angriff erzeugt **immer** einen **vollständigen** Kampfbericht über **alle Informationen des Angegriffenen** | Wall, Garnison, Taktik, Vorräte, Beute, Verluste |
| 4 | Die **Postfächer sind der Ort** dafür | kein Bericht nur im Spiel-Log |
| 5 | Der **Postkasten muss übersichtlich** sein | Daniels Maßstab, nicht meiner |
| 6 | **Bots müssen eingehende Infos weitgehend verwerten** | daraus schließen, ob ein weiterer Angriff lohnt |
| 7 | Der **Spieler erschließt sich die Lage selbst** aus den Berichtinhalten | keine Empfehlung, keine Auswertung, kein „lohnt sich“ im Text |

## Zerlegung in Schnitte (V-1 bis V-5)

| Schnitt | Inhalt | Abhängigkeit |
|---|---|---|
| **V-1 Angriffswarnung** | Roter Rahmen um das Hauptfenster, solange ein feindlicher Angriff auf den Spieler unterwegs ist; Farbe als Zahl in einer Datendatei; kein Blinken (nicht gesagt, also nicht erfunden) | braucht den Zustand „Angriff auf den Spieler unterwegs“ |
| **V-2 Zwei Berichte** | `kampfbericht` liefert heute EINEN Bericht (`{"titel", "zeilen", "typ": "kampf"}`); künftig Bericht je Seite mit eigener Sicht: Angreifer sieht seine Verluste/Beute, Verteidiger sieht seine Verluste/Wall-Schaden | V-3 |
| **V-3 Vollständiger Bericht** | Bericht trägt alle Angaben des Angegriffenen (Wallstufe und -zustand, Garnison vor dem Kampf, Taktik, Vorräte, Beute, Verluste beider Seiten) | — |
| **V-4 Postkasten** | Übersicht: Art (Angriff, Verteidigung, Spionage, Gründung, System), Zeit, Betreff, Kurzfassung; Details aufklappbar; Farbe je Art (bestehende `nachrichten_farbe`) | V-2 |
| **V-5 Bot-Auswertung** | Bots lesen eingehende Berichte und leiten daraus ab, ob ein weiterer Angriff lohnt (eigene Schwelle, keine Zufallsentscheidung) | V-3, V-4 |

## Grenzen, die unverändert gelten

- **Dörfer werden nie eingenommen**, **Angriffstruppen nie am Zielort stationiert** (`docs/GESAMTKONZEPT_20261102.md`, Abschnitt 4).
- Der Bericht ist **kein Spionageersatz vor** dem Angriff: die Aufklärung bleibt der Weg, VORHER Wall und
  Garnison zu kennen. Nach einem erfolgreichen Angriff legt der Bericht offen, was der Verteidiger hatte.
- **Kein Text verrät eine Empfehlung.** Der Spieler liest Zahlen und Verluste und schließt selbst.
- Anzeigetexte tragen echte Umlaute, Kennungen bleiben ASCII (Schnitt T-1, Register 171).

## Offene Punkte, die Daniels Wort brauchen (gesammelt, nicht einzeln gefragt)

1. **Farbe des Rahmens**: Vorschlag `#ff6b6b` (helles Rot) in `data/angriffswarnung.json`, daneben die
   Rahmenbreite. Daniel kann beide Zahlen ohne Code stellen.
2. **Bericht bei gescheitertem Angriff**: Vorgabe nennt „erfolgreicher Angriff“. Vorschlag: auch ein
   gescheiterter Angriff erzeugt Berichte für beide Seiten (mit Verlusten, ohne Beute) — stiller
   Fehlschlag wäre für den Angegriffenen unerklärlich.
3. **Verteidigungsbericht auch bei Angriff auf ein Bot-Dorf des Spielers** (Nebendorf): Vorschlag ja.

## Einordnung in den Ablauf

Nach **S-6b (Siedlerkarren, Daniels Entscheidung 18:5x)** und **vor S-7 (Karawanen)**: die Berichte sind
die Grundlage, auf der S-7 und S-9 ihre Meldungen aufbauen. V-1 ist klein und kann mit V-2 in einem
Schnitt laufen; V-4 ist Optik (Vergleichsblatt zeigen, dann einbauen); V-5 ist Bot-Logik.
