# Pruefung Schritt 5 — gemeinsame Spieluhr (`ort_tick`, `fensterproduktion`)

**Gegenstand:** die neuen Funktionen `ort_tick(ort, ab, bis, forschung)` und
`fensterproduktion(orte, jetzt)` in `src/spieloekonomie.py`, Abschnitt
„Schritt 5 — gemeinsame Spieluhr: lokale Produktion und Fortschritt"

- Code: `src/spieloekonomie.py` Zeilen **486-536**
- Massstab (Vorgabe): `docs/audits/entwurf_spieloekonomie_sol_2026-10-05.txt`,
  Abschnitt „5. Gemeinsame Spieluhr", Codeblock Zeilen **597-634**, Prosadiffs
  Zeilen **636-648**
- Regeln: `data/spieloekonomie.json` Zeile 17 `"versorgung_stunden": 24`,
  Zeile 34 `"pilot_ausbildung_minuten": 20`
- Nur gelesen, nichts geaendert. Kein git, kein Spielstart, kein run_tests.bat.

**Kurzverdikt:** Die zwei Funktionen setzen den Entwurfscode **inhaltlich woertlich**
um. Es gibt **keine** inhaltliche Abweichung; die einzige verhaltensrelevante
Abweichung ist eine defensive Erweiterung in `fensterproduktion` (siehe Punkt 4/8-A2).
**Fehlend** (kein Fehler, sondern noch offen) sind `tick_bis` samt Ereignisschleife und
die main-Anbindung (Spielsekunden/Save-Load der Journale).

---

## 1. Reihenfolge der Buchungen (Produktion, Siedler, Werkstattwaren, Ausbildungsende)

**Ergebnis: stimmt woertlich ueberein.**

| Reihenfolge | Entwurf | Code |
|---|---|---|
| Produktion → `vorraete`/`produktion` | Z. 603-606 | Z. 499-502 |
| Siedlerzuwachs bis Grenze | Z. 607-609 | Z. 503-505 |
| Produktionsjournal (nur bei `bis > ab`) | Z. 610-611 | Z. 506-507 |
| Werkstattwaren → Lager + `fertigjournal` | Z. 612-615 | Z. 508-511 |
| Ausbildungsende → Einheit + `fertigjournal` | Z. 616-621 | Z. 512-517 |

Entwurf Z. 603: `for r,rate in ertrag.items():`
Code Z. 499: `for r, rate in ertrag.items():` — gleiche Position (Produktion zuerst).
Entwurf Z. 612: `for schlange in neu["werkstaetten"].values():`
Code Z. 508: `for schlange in neu["werkstaetten"].values():` — Werkstattwaren vor Ausbildungsende.
Entwurf Z. 616: `for a in neu["ausbildung"]:`
Code Z. 512: `for a in neu["ausbildung"]:` — Ausbildungsende zuletzt.
**Keine Umstellung.**

## 2. Merker UNBEDINGT gesetzt, wo der Entwurf nur bedingt setzt?

**Ergebnis: in Schritt 5 kommt dieser Fehlertyp NICHT vor.**

In `ort_tick` gibt es genau zwei Merker, beide bedingt, beide identisch zum Entwurf:

- Produktionsjournal — Entwurf Z. 610 `if bis > ab:` → Code Z. 506 `if bis > ab:`.
  Bei `bis == ab` schreibt **kein** Weg (Entwurf wie Code) eine Journalzeile.
- Ausbildungsmerker `gebucht` — Entwurf Z. 617 `if not a["gebucht"] and a["ende"] <= bis:`
  → Code Z. 513 `if not a["gebucht"] and a["ende"] <= bis:`. `a["gebucht"] = True` steht
  **innerhalb** dieser Bedingung (Entwurf Z. 620, Code Z. 516), nicht davor.

`fensterproduktion` setzt ueberhaupt keinen Merker. Andernorts (Schritt 3,
`transport_fortschritt` Z. 364 `m["geliefert_lokal"] = True`) existiert zwar ein
bedingungslos gesetzter Merker, der liegt aber **ausserhalb** dieses Gegenstands und war
bereits Gegenstand von `docs/audits/pruefung_schritt3_4.md`.

## 3. `gebucht` beim Ausbildungsende genau EINMAL und nur wenn `ende <= bis`?

**Ergebnis: stimmt woertlich ueberein.**

Entwurf Z. 617: `if not a["gebucht"] and a["ende"] <= bis:`
Code Z. 513: `if not a["gebucht"] and a["ende"] <= bis:`

Beide Bedingungen sind vorhanden: `not a["gebucht"]` (verhindert Doppelbuchung) **und**
`a["ende"] <= bis` (keine Buchung vorab). `a["gebucht"] = True` wird genau einmal je
durchlaufenem Eintrag gesetzt (Code Z. 516, Entwurf Z. 620). Ein zweiter Lauf ueber
denselben Zeitraum (Test 7c) sieht `gebucht is True` und bucht nichts nach. Die Einheit
entsteht aus `neu["einheiten"][name] = neu["einheiten"].get(name, 0) + 1` (Code Z. 515,
Entwurf Z. 619), der Journalzeitpunkt ist `a["ende"]` (nicht `bis`) — beide gleich.

## 4. Zeitanteilige Rechnung in `fensterproduktion` (Zeile, die nur halb ins Fenster reicht)

**Ergebnis: JA, der Code rechnet zeitanteilig — stimmt woertlich ueberein.**

Entwurfsstelle: **Z. 624-634**, Kernzeilen Z. 630 und Z. 633.

| Entwurf | Code | Pruefung |
|---|---|---|
| Z. 625 `start = jetzt-REGELN["versorgung_stunden"]*3600` | Z. 527 `start = jetzt - REGELN["versorgung_stunden"] * 3600` | gleich; `REGELN["versorgung_stunden"]`=24 (json Z. 17) |
| Z. 629 `dauer = zeile["bis"]-zeile["ab"]` | Z. 531 `dauer = zeile["bis"] - zeile["ab"]` | gleich |
| Z. 630 `anteil = max(0,min(jetzt,zeile["bis"])-max(start,zeile["ab"]))` | Z. 532 `anteil = max(0.0, min(jetzt, zeile["bis"]) - max(start, zeile["ab"]))` | gleich (nur `0`→`0.0`) |
| Z. 631 `if dauer > 0 and anteil > 0:` | Z. 533 `if dauer > 0 and anteil > 0:` | gleich |
| Z. 633 `out[r] = out.get(r,0)+n*anteil/dauer` | Z. 535 `out[r] = out.get(r, 0) + n * anteil / dauer` | **gleich; der Faktor `anteil/dauer` ist die Zeitanteilsrechnung** |

Zahl fuer Zahl (Fensterbreite 24 h = 86400 s; lauf nachgerechnet, reine Arithmetik):

- Testlage 9b: eine Journalzeile `ab=0, bis=86400, mengen={"holz":96.0}`, `jetzt=43200`
  → `anteil = min(43200,86400) - max(-43200,0) = 43200`; `96.0*43200/86400 = 48.0`
  (halbe Menge, halbes Fenster). Entwurfsformel Z. 630/633 ergibt denselben Wert.
- Testlage 10b: Zeilen `0..3600 holz 4.0` und `3600..7200 holz 8.0`, `jetzt=5400`
  → Zeile 1 voll (`4.0`), Zeile 2 `anteil = 5400-3600 = 1800`, `8.0*1800/3600 = 4.0`
  → Summe `8.0`. Die halb hineinreichende Zeile zaehlt genau halb.

Der Code uebernimmt `anteil/dauer` exakt aus dem Entwurf; **keine Momentaufnahme, keine
volle Zeile.**

## 5. Rueckwaerts-Spanne wird abgelehnt

**Ergebnis: stimmt woertlich ueberein.**

Entwurf Z. 598-599:
`if bis < ab:` / `raise ValueError("Spielzeit darf nicht zurücklaufen.")`
Code Z. 494-495:
`if bis < ab:` / `raise ValueError("Spielzeit darf nicht zurücklaufen.")`

Die Meldung ist zeichengleich. `bis == ab` ist ausdruecklich erlaubt (keine Ausnahme,
Entwurf wie Code durch `bis < ab` / `bis > ab` begruendet; Test 8c). Der Entwurf regelt
keine Rueckwaerts-Pruefung in `fensterproduktion`; der Code setzt dort auch keine — passt.

## 6. Greift `ort_tick` unnoetig auf GLOBALE Groessen zu?

**Ergebnis: NEIN — der Entwurf verlangt lokal (je Ort), der Code rechnet lokal.**

`ort_tick` bekommt `ort`, `ab`, `bis`, `forschung` und arbeitet ausschliesslich auf dem
uebergebenen Ort:

- Code Z. 497 `wirtschaft.ertrag_gesamt([neu], forschung)` — **Liste mit genau `neu`**,
  nicht alle Orte.
- Code Z. 503 `gebaeude_wirkung.bevoelkerungsgrenze([neu])` — nur `neu`.
- Code Z. 504 `gebaeude_wirkung.siedler_zuwachs_pro_stunde([neu], forschung)` — nur `neu`.
- Code Z. 508 `for schlange in neu["werkstaetten"].values()` — nur die Werkstaetten
  dieses Ortes.
- Code Z. 512 `for a in neu["ausbildung"]:` — nur die Ausbildung dieses Ortes.

Es wird **keine** main-Groesse (kein Spielzustand, keine Gesamtvorraete, keine globale
Uhr) beruehrt. Die einzige Modulkonstante `REGELN` wird nur in `fensterproduktion`
benutzt (Code Z. 527) — genau wie im Entwurf (Z. 625). `ort_tick` beruehrt `REGELN`
**nicht**. **Keine globale Beruehrung, keine Zeile zu nennen.**

## 7. Fehlende Funktion/Zusagen des Entwurfsabschnitts Schritt 5

Als **fehlend** benannt (nicht als Fehler):

1. `tick_bis` — der Entwurf verlangt sie ausdruecklich in Schritt 5:
   Z. 647 „Dieser Algorithmus braucht eine neue reine tick_bis-Funktion und einheitliche
   Ereigniskennungen; vor dessen Fertigstellung darf Ökonomiemodus NICHT aktiviert
   werden." Der Entwurfscode dazu steht weiter hinten (Z. 942-984, `ereigniszeiten`/
   `tick_bis`). In `src/spieloekonomie.py` endet die Datei bei Zeile 536 mit
   `fensterproduktion`; **`tick_bis` ist nicht implementiert** (Volltextsuche:
   kein `def tick_bis` im Quellbaum).
2. Die main-Anbindung — Entwurf Z. 636-644 verlangt `GameState.__init__`/`tick`/`save`/
   `load` ueber `self.spielsekunden`, Partie-Saat, sowie Save/Load der „lokalen Lager/
   Aufträge/Journale" (Z. 641). Im Quellbaum existiert **kein** `spielsekunden` und
   **kein** `produktionsjournal` ausserhalb von `spieloekonomie.py` selbst.
3. Die Ereignisschleife / „einheitliche Ereigniskennungen" (Z. 645-647) — haengt an
   `tick_bis`, ebenfalls nicht vorhanden.

Solange 1-3 fehlen, darf der Oekonomiemodus nach eigenem Entwurf (Z. 647) nicht
aktiviert werden; die beiden hier gepruefte Funktionen sind laut Entwurf „unmittelbar
einsetzbar", ersetzen aber die Ereignisschleife nicht.

## 8. Zaehlung: woertlich uebereinstimmend / abweichend / nicht geregelt

### a) woertlich (auch semantisch) uebereinstimmend — 20 Zusagen

1. Rueckwaerts-Spanne + Meldung (Entw. 598-599 ↔ Code 494-495)
2. `copy.deepcopy(ort)` (600 ↔ 496)
3. Ertrag aus `wirtschaft.ertrag_gesamt([neu], forschung)`, Kleinschreibung (601 ↔ 497)
4. `produktion = {}` angelegt (602 ↔ 498)
5. Menge `rate*(bis-ab)/3600` (604 ↔ 500)
6. Gutschrift in `vorraete` = Jourmalmenge (605 ↔ 501)
7. `produktion[r] = menge` (606 ↔ 502)
8. `grenze = gebaeude_wirkung.bevoelkerungsgrenze([neu])` (607 ↔ 503)
9. Zuwachs × `(bis-ab)/3600` (608 ↔ 504)
10. `min(grenze, bevoelkerung+zuwachs)` (609 ↔ 505)
11. Journalzeile nur bei `bis > ab` (610-611 ↔ 506-507)
12. `for schlange in neu["werkstaetten"].values()` (612 ↔ 508)
13. `werkstatt.fertige_waren(schlange, bis)` (613 ↔ 509)
14. Waren ins Lager (614 ↔ 510)
15. `fertigjournal` ware, `zeit=bis` (615 ↔ 511)
16. Ausbildungsbedingung `not gebucht and ende<=bis` (617 ↔ 513)
17. Einheit +1 (619 ↔ 515)
18. `a["gebucht"] = True` (620 ↔ 516)
19. `fertigjournal` einheit, `zeit=a["ende"]` (621 ↔ 517)
20. Fensterformel `start=jetzt-REGELN["versorgung_stunden"]*3600`, `anteil=...`,
    `out += n*anteil/dauer` (625/629-633 ↔ 527/531-535)

### b) abweichend — 3 Textstellen (keine Abweichung im Ergebnis bei gueltigen Daten)

- **A1 (kosmetisch):** Entwurf Z. 630 `max(0, ...)` ↔ Code Z. 532 `max(0.0, ...)`.
  Nur Zahltyp, gleiches Ergebnis.
- **A2 (verhaltensrelevant nur bei fehlenden Schluesseln):** Entwurf Z. 628
  `for zeile in ort["produktionsjournal"]:` ↔ Code Z. 530
  `for zeile in ort.get("produktionsjournal") or []:`; Entwurf Z. 632
  `for r,n in zeile["mengen"].items():` ↔ Code Z. 534
  `for r, n in (zeile.get("mengen") or {}).items():`.
  Bei einem Ort ohne `produktionsjournal` (bzw. Zeile ohne `mengen`) liefert der Code
  `{}`/ueberspringt, der Entwurfscode wuerde `KeyError` werfen. Dieses Verhalten ist im
  Entwurf **nicht geregelt** (siehe c), die Erweiterung ist in der Dokumentation der
  Funktion (Code Z. 521-525) begruendet und vom Test 11a/b abgedeckt. **Dies ist die
  einzige verhaltensrelevante Abweichung des Schritts.**
- **A3 (kosmetisch):** Entwurf nennt nackte Signaturen `def ort_tick(ort, ab, bis,
  forschung):` (Z. 597) und `def fensterproduktion(orte, jetzt):` (Z. 624); Code ergaenzt
  Typannotationen und Docstrings (Code Z. 486, 521). Reine Dokumentation.

### c) im Entwurf nicht geregelt (daher NICHT als Abweichung gefuehrt) — 4 Punkte

- Verhalten, wenn der Schluessel `produktionsjournal` fehlt (Entwurf setzt ihn voraus).
- Verhalten, wenn einer Journalzeile `mengen` fehlt.
- Zeitbasis: dass `ab`/`bis`/`jetzt` in **Sekunden** gezaehlt werden (nur aus dem Kontext,
  nicht im Codeblock ausgesagt).
- Herkunft/Wert von `REGELN["versorgung_stunden"]` (= 24) — steht in
  `data/spieloekonomie.json` Z. 17, nicht im Codeblock.

---

## Verdikt

- **Schwerste Abweichung:** A2 — `fensterproduktion` liest `produktionsjournal`/`mengen`
  defensiv (Code Z. 530/534 statt Entwurf Z. 628/632). Nur bei fehlenden Schluesseln
  verhaltensrelevant; bei gueltigen Daten identisch zum Entwurf.
- **Reihenfolge, `gebucht`-Merker, Rueckwaerts-Sperre, Lokalitaet und die zeitanteilige
  Fensterformel stimmen woertlich mit dem Entwurf ueberein.**
- **Fehlend (offen, kein Fehler):** `tick_bis` samt Ereignisschleife und die
  main-Anbindung (Spielsekunden, Save/Load der Journale), Entwurf Z. 636-648.
