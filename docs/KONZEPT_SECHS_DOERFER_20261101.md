# Modell: Sechs Dörfer, Portalplatz, Tempelpflicht und eigenständiger Aufbau

**Daniels Vorgabe vom 01.11.2026** — hier vollständig aufgearbeitet, damit der Umbau in einer
eigenen Sitzung ohne Suchen beginnen kann. **Nichts davon ist gebaut.** Dieses Dokument ist das
Modell und die Fragenliste; erst nach Daniels Antworten wird umgesetzt.

---

## 1. Was Daniel will, in seinen Worten zerlegt

1. **Jede Karte und jede Siedlungsneugründung bekommt einen eigenen Portalplatz** — ein Feld
   neben dem Hauptdorf.
2. **Von Gründung an steht ein Tempel**, der eine **garantierte Grundmenge Mana** erzeugt.
3. **Karten ohne Manafelder sind für ihre Dörfer benachteiligt** — das ist gewollt, keine Lücke.
4. **Sechs eigene Dörfer**, strategisch positioniert: drei bleiben und verteidigen den
   Gesamtbestand, drei greifen an — oder jede andere Aufteilung.
5. **Der Siedlungskarren liefert bei der Gründung mit**: Siedler, Grundrohstoffe und **drei
   Gebäude** — Holzfäller (möglichst auf Wald), Steinmetz (möglichst auf Hügel oder Berg),
   Tempel (möglichst auf Nebelsee; ohne Nebelsee auf Steppe).
6. **Jedes Dorf baut sich eigenständig auf.** Ein Zweitdorf braucht **eine eigene Bibliothek**, um
   den Forschungsstand des Hauptdorfs zu übernehmen; danach darf es dort weiterforschen, auch
   gleichzeitig in einem anderen Gebiet.
7. **Gebäudestand-Regel:** Ein Dorf kann eine Einheit erst herstellen, wenn **seine eigene**
   Kriegerakademie die Stufe des Hauptdorfs erreicht hat.
8. **Lagern und Stationieren ist überall erlaubt** — das Hauptdorf darf Paladine ins Zweitdorf
   stellen, obwohl dort erst Bürgerwehr freigeschaltet ist.
9. Im Hauptdorf ist der **erste Fortschritt Pflicht**: ein Holzfäller und ein Steinmetz.

---

## 2. Was davon schon im Code steht (gemessen)

| Baustein | Stand heute | Belegstelle |
|---|---|---|
| Grenze von **6 Siedlungen** | **vorhanden** | `main.SIEDLUNGEN_MAXIMUM = 6`, geprüft in `_found_settlement` |
| Kolonie-Gründung mit Kartenvorrat, Weltfeld, Preis, Mindestbestand | **vorhanden** | `_kolonie_gruenden` (Z. 4137 ff.), Kern `vergabe`/`absicht` |
| Siedlerkarren als Gründungsbedingung | **vorhanden** | Kolonie-Maske verlangt Karren und Mindestguthaben |
| Tempel erzeugt Mana | **vorhanden, mit Originalwerten** | `data/buildings.json`: `tempel` → `Nebelsee 5/h`, `alle Gelände außer Sumpf 1/h`; Voraussetzung `Baukunst` |
| Bibliothek je Ort, Forschung je Ort | **vorhanden** | `spieloekonomie.forschung_start(ort, …)`, Bibliotheksstufe **dieses** Ortes |
| Parallele Forschung in zwei Dörfern | **vorhanden, aber geregelt** | `forschung_start(…, weitere_orte)`: verschiedene Gebiete dürfen parallel laufen, **dieselbe Zielstufe nicht** (sonst doppelt zahlen, einmal lernen) |
| Kriegerakademie-Stufe je Ort | **vorhanden** | `gebaeude_wirkung.ausbildungsstaette([ort], einheit)` liefert Stufe **vor Ort** |
| Stationieren zwischen eigenen Dörfern | **vorhanden** | Auftragsart `stationieren` in `auftraege.auftragsarten()` |
| Einheiten im Ortslager, Transport, Ladung | **vorhanden** | `Settlement.einheiten`, `ladung_der_mission`, Wagenbau-Bonus (Register 73) |
| **Siedlungs-Versetzung (Portal)** | **BELEGT vorhanden, aber ungenutzt** | `portalraum.py`: Koordinatenwechsel im Limbus (X, Y, Z), **5.000 Mana**, **höchstens einmal je 24 Stunden**, durchgeführt von **EINER** Siedlung — Quelle: Portal-Anleitung 2005 (portal.php), Handbuch 2009 S. 80–83 |
| Portal zwischen Dimensionen, 20 × 400 Felder | **vorhanden** | `welt.py`, `portalraum.py` |
| Portalplatz als Feld auf der Siedlungskarte | **fehlt** | es gibt kein eigenes Portalgebäude je Siedlung |

### Korrektur eines eigenen Fehlers

In `docs/KONZEPT_ABGLEICH_20261101.md` stand, ein Versetzen der Siedlung gebe es „im Original
nicht“. **Das ist falsch.** `portalraum.py` führt den belegten **Koordinatenwechsel** (5.000 Mana,
1× je 24 h, eine Siedlung). Der Abgleich ist an dieser Stelle zu berichtigen: es gibt ein
Originalritual, es ist nur nicht im Spiel erreichbar. Daniels Wunsch ist damit **näher am Original
als gedacht** — ein frei wählbares Ziel ohne Ritual wäre die Abweichung, das Ritual selbst nicht.

---

## 3. Das Modell in Bausteinen

**M-1 Portalplatz je Siedlung.** Jede Siedlung bekommt ab Gründung ein **reserviertes Feld**
neben dem Dorfzentrum. Auf ihm steht das Portal; es ist der Ort, von dem ein Koordinatenwechsel
ausgeht. Kein anderes Gebäude kann dort gebaut werden.

**M-2 Tempelpflicht ab Gründung.** Die Gründung setzt den Tempel — nicht der Spieler. Er trägt den
**garantierten Grundertrag**: 5 Mana/h auf Nebelsee, 1 Mana/h auf jedem anderen Gelände außer
Sumpf. Karten ohne Manafeld haben damit 1/h statt 5/h: **benachteiligt, aber nicht ausgeschlossen**
(Daniels Vorgabe).

**M-3 Was der Siedlungskarren mitbringt.** Bei jeder Gründung liefert der Karren: die
Startressourcen des Dorfes, **einen Holzfäller** (bevorzugt auf Wald), **einen Steinmetz**
(bevorzugt auf Hügel oder Berg) und **den Tempel** (bevorzugt Nebelsee, sonst Steppe). Die
Platzwahl ist Geländevorliebe, kein Zwang: findet sich kein Wunschgelände, nimmt die Gründung das
beste freie Feld und **sagt es in der Meldung**.

**M-4 Eigenständigkeit der Dörfer.** Ein Zweitdorf forscht **nicht** automatisch mit. Es braucht
eine eigene Bibliothek; deren Stufe bestimmt, welche Forschungsstufen dort möglich sind. Der
**Forschungsstand** (welche Gebiete wie weit) bleibt Verbundwissen — sonst müsste jedes Dorf
dieselbe Forschung doppelt zahlen. Offen: ob ein Dorf ohne Bibliothek den Stand nur *lesen* darf
(siehe Frage 4).

**M-5 Gebäudestand-Regel für Einheiten.** Herstellen darf ein Dorf eine Einheit nur, wenn
`eigene Kriegerakademie-Stufe ≥ Stufe, die im Verbund für diese Einheit erreicht ist`. Das ist
genau Daniels Formulierung: gleiche Stufe wie das Hauptdorf, dann sofort dieselben Einheiten.

**M-6 Stationieren ist frei.** Jedes Dorf lagert und stationiert jede Einheit, auch solche, die es
selbst nicht bauen kann. Das ist heute schon so (Ortslager + Auftragsart `stationieren`) und bleibt
unangetastet.

**M-7 Strategie mit sechs Dörfern.** Verteidigen heißt: Truppen stationiert lassen, Vorräte im Dorf
halten, Wall ausbauen. Angreifen heißt: aus einem Dorf mit kurzer Entfernung zum Ziel marschieren
(Sofortangriff-Umbau, Entscheidung 1, gehört dazu). Beides zusammen ergibt Daniels Aufteilung
drei zu drei.

**M-8 Kartenwahl wird zur strategischen Entscheidung.** Der Nutzen einer Karte hängt künftig an
drei Dingen: Mana (Tempelertrag), Bauplätze für Holzfäller und Steinmetz, und die Lage im Limbus
(Entfernung zu Zielen). Die Kolonie-Maske muss das **vor** der Zahlung zeigen.

---

## 4. Was der Umbau an bestehendem Code berührt

| Stelle | Änderung |
|---|---|
| `_erste_siedlung_gruenden` / `_kolonie_gruenden` | Tempel, Holzfäller, Steinmetz automatisch setzen, Portalplatz reservieren, Meldung nennt was gesetzt wurde und wo |
| `data/buildings.json` | neues Gebäude `portal` (kein Preis, nur Platz) **oder** Reservierungsregel im Kartenmodell — Entscheidung nötig (Frage 1) |
| `gelaende.bau_moeglich` / `bauen_auf_karte` | Portalplatz gegen Bebauung sperren |
| `spieloekonomie.forschung_start` | Regel „Dorf ohne Bibliothek darf nicht starten“ ist da; Übernahme des Verbundstands beim Bau der Bibliothek ist neu |
| `ausbildung_grenzen` / `_ausbildungs_hindernis` | zweite Schranke: Akademiestufe gegen Verbundsstufe |
| `_kolonie_gruenden` | Anzeige: Mana-Grundertrag, verfügbare Wunschfelder, Portalplatz frei/belegt |
| Koloniepreis | heute ohne Gebäude und Startressourcen — muss neu bilanziert werden |
| Prüfdateien | neue: Gründung setzt drei Gebäude, Tempel liefert Mana auch ohne Manafeld, Portalplatz bleibt frei, Einheitenregel, Stationieren kreuz und quer; betroffene bestehende: `test_startspiel`, `test_durchspiel`, `test_originalkarten_baukasse`, `test_lokale_forschung` |

---

## 5. Offene Fragen — bitte VOR dem Umbau klären

1. **Portalplatz: eigenes Gebäude oder reserviertes Feld?**
   *A) eigenes Gebäude `portal` auf einem reservierten Feld (Empfehlung — sichtbar, prüfbar,
   kein Sonderfall im Baumenü)* · B) nur eine Reservierung, unsichtbar bis zum ersten Wechsel ·
   C) das Dorfzentrum selbst ist der Portalplatz.
2. **Tempel ab Gründung — auch forschungsfrei?** Der Tempel verlangt heute `Baukunst`. Wenn er ab
   Gründung steht, ist das eine Ausnahme.
   *A) Ausnahme nur bei der Gründungssetzung, Nachbau verlangt weiter Baukunst (Empfehlung)* ·
   B) Tempel generell ohne Forschung · C) Baukunst Stufe 1 wird bei Gründung mitgeliefert.
3. **Mana-Garantie: fester Betrag je Dorf oder Tempelertrag?**
   *A) Tempelertrag nach Gelände, 5/h auf Nebelsee, 1/h sonst — benachteiligte Karten bleiben
   benachteiligt (Empfehlung, entspricht deiner Vorgabe)* · B) jedes Dorf bekommt unabhängig vom
   Gelände eine Sockelmenge, z. B. 2/h · C) Garantie nur bis zum ersten Ausbau.
4. **Forschungsübernahme:** Darf ein Dorf **ohne** Bibliothek den Verbundstand sehen und nutzen
   (nur nicht weiterforschen)?
   *A) ja, sehen und nutzen, forschen erst mit Bibliothek (Empfehlung)* · B) nein, ohne Bibliothek
   gilt Stufe 0 vor Ort · C) Kompromiss: sehen ja, nutzen erst ab Bibliothek Stufe 1.
5. **Was kostet eine Kolonie künftig?** Heute: Gebühr plus Mindestguthaben plus Karren, ohne
   Gebäude.
   *A) Preis bleibt, Gebäude und Startressourcen kommen obendrauf (Empfehlung, keine neue Zahl
   erfinden)* · B) Preis sinkt, weil der Karren mehr mitbringt · C) Preis wird neu bilanziert,
   nachdem die Erträge gemessen sind.
6. **Startressourcen je Gründung: welche Menge?**
   *A) die belegten Startwerte des Handbuchs (10 Siedler, 100 Holz, 100 Stein) je Dorf
   (Empfehlung — belegt, keine Erfindung)* · B) ein Vielfaches, weil ein Zweitdorf mehr braucht ·
   C) vom Kartennutzen abhängig.
7. **Portalwechsel-Kosten:** belegt sind 5.000 Mana und 1× je 24 Stunden für eine Siedlung.
   *A) genau so übernehmen, Tempel finanziert es (Empfehlung — belegt)* · B) billiger, weil sechs
   Dörfer sonst nie wechseln · C) je Dorf eine eigene Abklingzeit statt einer für den Spieler.
8. **Verteidigungsstrategie:** Sollen stationierte Truppen in einem Dorf **automatisch** mit
  kämpfen, wenn es angegriffen wird?
   *A) ja, sie zählen zur Verteidigung dieses Dorfes (Empfehlung — sonst wäre Stationieren sinnlos)*
   · B) nur die eigenen Einheiten des Dorfes verteidigen · C) der Spieler entscheidet je Dorf.
9. **Sechs Dörfer — jetzt schon erreichbar?** Die Grenze steht bei 6; der Kartenvorrat und die
   Gebühr begrenzen praktisch früher.
   *A) so lassen (Empfehlung)* · B) Gründung billiger machen, damit sechs realistisch sind ·
   C) sechs erst nach einer Forschung freigeben.
10. **Reihenfolge:** Soll der Umbau **vor** oder **nach** dem Angriffs-Umbau (Entscheidung 1)
    laufen?
    *A) erst Angriff reist, dann die sechs Dörfer (Empfehlung — der Angriff ist die Grundlage jeder
    Drei-gegen-drei-Strategie)* · B) erst die Dörfer · C) parallel in zwei Paketen.

---

## 6. Vorgeschlagene Umsetzungsschnitte (nach den Antworten)

1. **S-1 Datenmodell**: Portalplatz im Kartenmodell, Tempel/Holzfäller/Steinmetz bei Gründung,
   Startressourcen. Eigene Prüfdatei: Gründung setzt genau diese drei Gebäude, Portalplatz bleibt
   unbebaubar.
2. **S-2 Anzeige**: Kolonie-Maske zeigt Mana-Grundertrag und Wunschfelder vor der Zahlung.
3. **S-3 Einheitenregel**: Akademiestufe gegen Verbundsstufe, Meldung nennt beide Zahlen.
4. **S-4 Forschungsübernahme**: Bibliothek übernimmt den Verbundstand, Parallelforschung bleibt
   geregelt wie heute.
5. **S-5 Portalwechsel**: das belegte Ritual ins Spiel holen (5.000 Mana, 1×/24 h), mit dem
   Portalplatz als Ausgangspunkt.
6. **S-6 Bilanz**: sechs Dörfer durchrechnen (Mana, Holz, Stein, Siedler) und im Spieltest prüfen,
   bevor die Demo kommt.

Jeder Schnitt endet wie gewohnt: Prüfdatei, Register, Protokoll, voller Sammellauf, EXE mit
Startprüfung, ein Commit.

---

## 7. Was dieses Dokument NICHT ist

Keine Freigabe, keine Umsetzung, keine erfundene Zahl. Die belegten Werte (Tempel 5/1 Mana je
Stunde, 5.000 Mana je Wechsel, 1×/24 h, 10 Siedler/100 Holz/100 Stein Startwerte, 6 Siedlungen)
stehen mit Quelle da; alles Übrige sind Vorschläge und warten auf Daniels Antworten.
