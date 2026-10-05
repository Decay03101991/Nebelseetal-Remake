# Auftrag: Alle Vorgaben gegen das Spielhandbuch 2009 abgleichen

**Erstellt:** 05.10.2026 durch den Koordinator. **Auftraggeber:** Daniel Kössl.
**Daniels Wortlaut:** „gleiche das alles mit den vorgaben im Spielhandbuch ab."

## 1. Deine Rolle

Du bist **Prüfer**, nicht Autor. Du änderst **keine** Projektdatei außer der einen Ausgabedatei
(Abschnitt 6). Kein `git`, kein Commit. Lesen ist ausdrücklich erlaubt und erwünscht — lesen **musst**
du.

## 2. Der Prüfgegenstand (drei Quellen gegeneinander)

| Kürzel | Was | Wo |
|---|---|---|
| **HB** | das **Original-Handbuch 2009** — die Richtschnur, die alles entscheidet | `docs/original/Spielanleitung_2009_Textfassung.txt` (durchsuchbare Textfassung derselben Anleitung) · zusätzlich `docs/original/ORIGINAL_Einheiten_Waren_Rohstoffe.md`, `docs/original/ORIGINAL_Kampf_und_Punkte.md`, `docs/original/Spielanleitung_2005/**` |
| **PAPIER** | der neue Spielökonomie-Entwurf eines starken Modells | `docs/audits/entwurf_spieloekonomie_sol_2026-10-05.txt` (1140 Zeilen, Gliederung A–H) |
| **CODE** | unsere Datendateien und Konstanten | `data/gelaende.json`, `data/buildings.json`, `data/baupreise.json`, `data/units.json`, `data/research.json`, `data/items.json`, `data/gebaeude_wirkung.json`, `data/spielzeit.json`, `data/welt*.json` · `src/*.py` (Konstanten) |

## 3. Was du tun sollst

**Für jede Zahl und jede Regel**, die das PAPIER verwendet **oder ändert**, und **für jede belegte
Angabe in CODE**, die das PAPIER berührt:

1. Suche die **wörtliche Handbuchstelle**. Nenne **Datei + Zeilennummer + Zitat**.
2. Urteile in genau einer dieser vier Klassen:
   * **BELEGT-KONFORM** — Handbuch sagt genau dasselbe.
   * **WIDERSPRUCH** — Handbuch sagt etwas anderes. Nenne beide Fassungen wörtlich und sage, welche
     gilt (**das Handbuch gewinnt**).
   * **NICHT BELEGT** — das Handbuch schweigt. Dann muss der Wert im PAPIER/CODE ausdrücklich als
     `VORSCHLAG` gekennzeichnet sein; fehlt die Kennzeichnung, ist **das** der Befund.
   * **UNKLAR** — die Stelle ist mehrdeutig. Zitiere sie und sage, was unklar bleibt.
3. Sei **vollständig bei den Zahlen**, aber knapp im Text. Keine Wiederholungen.

**Pflichtliste — diese Punkte auf jeden Fall prüfen:**

* Startwerte (100 Holz, 100 Stein, 10 Siedler), Siedlergrenze 10 + 5 je Haus, 1 Siedler je Stunde.
* **Sechs Siedlungen** gleichzeitig (PAPIER behauptet, das sei direkt belegt — prüfe das!).
* Die **Ertragstabelle** (alle neun Rohstoffe, alle Gebäude/Gelände) gegen das PAPIER **und** gegen
  `data/buildings.json` — insbesondere: Rinderfarm, Schafszucht, Pferdezucht, Jäger, Steinmetz,
  Erzmine, Goldmine, Farm, Holzfäller, Tempel, Bibliothek.
* **Welche Gebäude ohne Forschung** baubar sind (Handbuch nennt eine Liste) — gegen CODE.
* **Baupreise** und die **Kosten des Siedlerkarrens** (das PAPIER nennt: 200 Holz, 80 Metall, 150
  Leder, 100 Wolle, 4 Pferde, 5 Siedler, 300 Nahrung).
* **Sumpf unbebaubar**, **Bibliothek nur auf Grasland/Steppe/Nebelsee**, Geländearten (sieben).
* **Forschung**: die 21 Gebiete, Dauer = Stufe², Kostenverdopplung, Voraussetzungen, Wechselwirkung
  Bibliothek/Ausbildungsstätten. Gibt es im Handbuch **„Vermessung"** oder ein anderes Mittel, weitere
  Karten zu erhalten? (CODE fragt heute einen Schlüssel ab, den es nicht gibt.)
* **Punkte**: Forschungsstufen hoch drei; Kriegspunkte = Einheitenwerte + Wallstufe hoch drei; Gesamt =
  (Krieg + Forschung) / 2; geht der **Ruf** ein?
* **Götterschutz**: sieben Tage, endet er mit dem ersten Kriegspunkt?
* **Kampf/Beute**: Vorrunde und Wallschwellen, zehn Sequenzen, Flucht, **Beutemenge** (das PAPIER
  nennt 50 % der Lager, gedeckelt durch die Karrenladung).
* **Portal/andere Dimensionen**: 5.000 Mana aus **einer** Siedlung, höchstens einmal je 24 Stunden.
* **Handel**: Sagt das Handbuch etwas über **Handel zwischen den eigenen Siedlungen**? Über Warenpreise?
  Über den Marktplatz? Zitiere jede Stelle, die du findest — oder sage ausdrücklich, dass keine da ist.
* **Zeitfenster und Überfall**: Sagt das Handbuch etwas darüber, dass eine Siedlung angreifbar ist,
  **während ihre Truppen unterwegs sind**, und dass Angreifer mit **Karren** Rohstoffe **mitnehmen**?
  (Daniels Vorgabe vom 05.10.2026 beschreibt genau solche Ketten. Prüfe, was belegt ist und was nicht.)
* **Zeitfaktor ×180** (1 Spielstunde = 20 echte Sekunden): nicht belegt, aber im Datenblatt als
  `belegt: false` gekennzeichnet? Stimmt das noch?
* Die **Vorschlagszahlen des PAPIERS** (Siedlungsgebühr 320/200/150, Startpaket 160/100/100,
  Mindestbestand 480/300/250; Spezialistenschwelle 1,4; Portfoliofaktor 1,0; drei ausgeglichene Karten;
  Vergabefenster 24 Spielstunden; Haltefenster 24 Spielstunden; Pilotrezepte 20 Minuten) — jede muss
  als **VORSCHLAG mit Ableitung** erkennbar sein. Nenne jede, bei der das fehlt.

Zusätzlich: **widerspricht das PAPIER irgendwo dem Handbuch?** Liste jeden solchen Satz mit Zitat aus
beiden Quellen auf. Das ist der wichtigste Teil dieser Prüfung.

## 4. Was du NICHT tun sollst

* Nichts ändern, nichts löschen, nicht committen.
* Keine Zahl „aus dem Gefühl" ergänzen. Findest du keine Stelle: **NICHT BELEGT** schreiben.
* Keine achte Geländeart, keine neuen Forschungsgebiete vorschlagen.
* Nicht behaupten, du hättest etwas geprüft, was du nicht gelesen hast.

## 5. Ausgabe (genau eine Datei)

```
D:\Arbeiten\Nebelseetal_Remake\docs\audits\handbuch_abgleich_2026-10-05.txt
```

Format: eine **Tabelle** mit den Spalten

`Gegenstand | Quelle (Datei:Zeile) + Zitat | Urteil | Was zu tun ist`

* Deutsch, **höchstens 700 Zeilen**. Am Ende ein Abschnitt **„Die zehn wichtigsten Abweichungen"**
  (nach Schwere sortiert) und ein Abschnitt **„Was das Handbuch nicht regelt"**.
* Jede Zeile mit Zitat — ohne Handbuchstelle kein Urteil.
* Kennzeichne am Kopf, wenn du eine Datei nicht gelesen hast.

Antworte am Ende nur mit: `FERTIG <Zeilenzahl>`.
