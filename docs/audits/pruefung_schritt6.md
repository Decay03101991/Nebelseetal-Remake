# Pruefung Schritt 6 — lokaler Forschungsstart (`forschung_start`, `forschung_abschluss`)

**Gegenstand:** die neuen Funktionen `forschung_start(ort, gebiet, wissen, jetzt, weitere_orte=())`
und `forschung_abschluss(ort, wissen, jetzt)` in `src/spieloekonomie.py`, Abschnitt
„Schritt 6 — Forschung JE SIEDLUNG“ (Code Z. **557-608**).

- Massstab (Vorgabe): `docs/audits/entwurf_spieloekonomie_sol_2026-10-05.txt`, Abschnitt
  „6. Lokaler Forschungsstart statt globaler Bibliotheksabkuerzung“, Codeblock Z. **656-683**,
  Prosadiff Z. **685**, Mitziehen Z. **686**.
- Mitgelesen (nur gelesen): `src/forschung.py` (`starten` Z. 109-155, None-Grenze Z. 139),
  `src/forschungspfad.py` (`erfuellt` Z. 179-202), `docs/audits/belege_forschung_je_siedlung.md`,
  Handbuchzitate (Z. 404, 423-424).
- Nur gelesen, nichts geaendert. Kein git, kein Spielstart, kein run_tests.bat.

**Kurzverdikt:** Die beiden Funktionen setzen den Entwurfscode **inhaltlich woertlich** um. Es
gibt **keine verhaltensrelevante Abweichung**. Die einzige strukturelle Abweichung ist der von
Entwurf Z. 685 ausdruecklich geforderte Zusatzblock (Code Z. 578-583) samt Signaturerweiterung
`weitere_orte` (Code Z. 557-558). **Fehlend** (kein Fehler, sondern offen) sind der main-Anschluss
und die neue Testdatei `test_lokale_forschung.py`.

---

## 1. Reihenfolge der Pruefungen

**Ergebnis: stimmt woertlich ueberein — keine Umstellung.**

| Pruefschritt | Entwurf | Code |
|---|---|---|
| Auftrag laeuft? | Z. 658 | Z. 570 |
| Gebiet bekannt? | Z. 660 | Z. 572 |
| Bibliotheksstufe holen | Z. 662 | Z. 574 |
| Voraussetzungen (`erfuellt`) | Z. 663 | Z. 575 |
| Dublettencheck (Zusatz aus Z. 685) | — (nicht im Codeblock) | Z. 578-583 |
| `kosten` | Z. 666 | Z. 584 |
| `verbrauchen` | Z. 667 | Z. 585 |
| `stand` + `starten` | Z. 668 / 670 | Z. 586 / 588 |
| `forschungsauftrag` setzen | Z. 673 | Z. 591 |

Der laufende Auftrag wird zuerst geprueft (Entw. Z. 658 `if neu["forschungsauftrag"] is not None:`
↔ Code Z. 570 `if neu.get("forschungsauftrag") is not None:`), das Gebiet danach (Entw. Z. 660
`if gebiet not in spieldaten.forschungen():` ↔ Code Z. 572 zeichengleich), dann
`bibliothek = gebaeude_wirkung.bibliothek_stufe([neu])` (Entw. Z. 662 ↔ Code Z. 574), dann
`ok, grund = forschungspfad.erfuellt(gebiet, wissen, bibliothek)` (Entw. Z. 663 ↔ Code Z. 575),
dann Kosten (Entw. Z. 666 ↔ Code Z. 584) und `verbrauchen` (Entw. Z. 667 ↔ Code Z. 585).

Die einzige Einfuegung ist der von Entwurf Z. 685 verlangte Dublettencheck (Code Z. 578-583). Er
sitzt zwischen Voraussetzungen und Kosten und bricht **vor** `verbrauchen` (Z. 585) ab — er kostet
also nichts. **Keine Reihenfolge-Abweichung**, nur eine Ergaenzung an der im Entwurf bezeichneten
Stelle („Vor forschung_start“).

Kleinere Woertlich-Abweichung: Entw. Z. 658 indiziert direkt `neu[...]`, Code Z. 570 nutzt
`.get(...)` (siehe §8 A2).

## 2. Wird das Material GENAU EINMAL bezahlt?

**Ergebnis: genau einmal — stimmt woertlich ueberein.**

- Entwurf: Z. 667 `neu = verbrauchen(neu,kosten,jetzt)`; Kommentar Z. 669
  „Material wurde schon transaktional bezahlt; nicht erneut an starten übergeben.“; Z. 670
  `ok,grund = forschung.starten(gebiet,stand,jetzt,bibliothek>0,None)`.
- Code: Z. 585 `neu = verbrauchen(neu, kosten, jetzt)`; Kommentar Z. 587 „Material ist oben schon
  transaktional bezahlt → `forschung.starten` darf nichts abziehen.“; Z. 588
  `ok, grund = forschung.starten(gebiet, stand, jetzt, bibliothek > 0, None)`.

Die Behauptung „mit `None` zieht `starten` nichts ab“ ist in `src/forschung.py` belegbar: Die
Abbuchung steht unter der Grenze **Z. 139** `if vorhandene_rohstoffe is not None:` und findet nur
dort statt (**Z. 144-145** `vorhandene_rohstoffe[rohstoff] = vorhandene_rohstoffe.get(rohstoff, 0)
- menge`). Mit `None` wird dieser Block uebersprungen -> keine zweite Abbuchung. Keine andere
Stelle in `forschung_start` bucht Material. **Ergo: exakt eine Zahlung.**

## 3. Auftrag am ORT und Stufe erst beim ABSCHLUSS?

**Ergebnis: stimmt woertlich ueberein.**

- Auftrag am Ort: Entw. Z. 673 `neu["forschungsauftrag"] = {"gebiet":gebiet,**stand[gebiet]["auftrag"]}`
  ↔ Code Z. 591 zeichengleich (mit Leerzeichen). Der Auftrag haengt am **zurueckgegebenen Ort**,
  nicht an `wissen`.
- Stufe erst beim Abschluss: `forschung_start` schreibt **nie** eine Stufe; der lokale `stand`
  (Code Z. 586) traegt nur den Ausgangsstand `wissen.get(gebiet, 0)`. Die Stufe erhoeht allein
  `forschung_abschluss` (Code Z. 605) — Entw. Z. 680. ✔

## 4. Entwurf Z. 685, Zeile fuer Zeile

Entwurf Z. 685 woertlich:
„Adapter muss außerdem gleichzeitige Forschung derselben Zielstufe in verschiedenen Städten
verhindern, sonst doppelte Kosten ohne Wissensgewinn. Vor forschung_start alle eigenen
Ortsauftraege auf dasselbe gebiet/erreichte Zielstufe prüfen und ablehnen. Unterschiedliche
Gebiete dürfen in unterschiedlichen Bibliotheken laufen.“

Code Z. 578-583:
```
ziel = wissen.get(gebiet, 0) + 1
for anderer in weitere_orte or ():
    a = (anderer or {}).get("forschungsauftrag")
    if a and a.get("gebiet") == gebiet and a.get("zielstufe") == ziel:
        raise ValueError(...)
```

- **Satz 1+2** (dieselbe Zielstufe verhindern; auf „dasselbe gebiet/erreichte Zielstufe“ pruefen):
  Der Code prueft genau das Paar — `a.get("gebiet") == gebiet` **und** `a.get("zielstufe") == ziel`
  (Z. 581). Der Abbruch liegt **vor** `verbrauchen` (Z. 585), die „doppelten Kosten“ entstehen
  nicht. -> **erfuellt.**
- **Satz 3** (unterschiedliche Gebiete erlaubt): Bedingung Z. 581 verlangt Gebietsgleichheit, andere
  Gebiete passieren -> **erfuellt.**

**Fall „ANDERE Zielstufe desselben Gebiets“:**
- Was der Entwurf sagt: Er bindet die Ablehnung ausdruecklich an das Paar „dasselbe gebiet/erreichte
  Zielstufe“. Ein gleiches Gebiet mit **anderer** Zielstufe nennt der Entwurf **nicht** als
  Ablehnungsgrund -> nach dem Wortlaut **erlaubt**.
- Was der Code tut: gleiche UND-Bedingung (Z. 581) -> er erlaubt eine gleiche Gebiet mit anderer
  Zielstufe ebenfalls. **Woertlich uebereinstimmend, keine Abweichung.**
- Beobachtung (kein Abweichungsbefund): Da `ziel` aus dem **einen** uebergebenen `wissen` abgeleitet
  wird (Z. 578), liefert dasselbe Gebiet stets dieselbe Zielstufe; der Fall „gleiches Gebiet, andere
  Zielstufe“ ist mit globalem `wissen` praktisch nicht erreichbar. Eine Luecke entstuende nur, wenn
  der Aufrufer je Ort **unterschiedliches** `wissen` uebergibt — das regelt der Entwurf nicht
  (siehe §10c).

**Anbindungs-Abhaengigkeit:** „alle eigenen Ortsauftraege“ kann die Funktion nicht selbst
aufzaehlen; sie prueft genau die uebergebenen `weitere_orte` (Z. 579). Die Vollstaendigkeit dieser
Liste ist Pflicht des Aufrufers (main-Anbindung) -> offen (§9), **keine Abweichung**.

## 5. Merker UNBEDINGT gesetzt, wo der Entwurf nur bedingt setzt?

**Ergebnis: NEIN — dieser Fehlertyp kommt in Schritt 6 nicht vor.**

In beiden Funktionen wird kein Bool-Merker gefuehrt. Alle Schreibvorgaenge sind bedingt:

- `neu["forschungsauftrag"] = ...` (Code Z. 591) steht **nach** `if not ok: raise ValueError(grund)`
  (Z. 589-590), also nur bei Erfolg.
- `kenntnis[a["gebiet"]] = max(...)` (Z. 605), `neu["forschungsauftrag"] = None` (Z. 606) und der
  `fertigjournal`-Append (Z. 607) stehen **innerhalb** der Bedingung
  `if a and a["startzeit"] + a["dauer_stunden"] * 3600 <= jetzt:` (Z. 604).

Der bedingungslos gesetzte Merker aus Schritt 3 (`transport_fortschritt`, Code Z. 365
`m["geliefert_lokal"] = True`) liegt **ausserhalb** dieses Gegenstands.

## 6. Wird der uebergebene Ort veraendert (Seiteneffekt)?

**Ergebnis: NEIN — beide Funktionen geben Kopien zurueck.**

- `forschung_start`: Z. 569 `neu = copy.deepcopy(ort)`; Z. 585 bindet `neu` auf das deepcopy-Ergebnis
  von `verbrauchen` (das selbst in Z. 277 `neu = copy.deepcopy(ort)` kopiert); Z. 592 `return neu`.
  Der uebergebene `ort` wird nie in place veraendert.
- `forschung_abschluss`: Z. 602 `neu, kenntnis = copy.deepcopy(ort), dict(wissen)`; Z. 608
  `return neu, kenntnis`.
- Auch `forschung.starten` veraendert nur den **lokalen** `stand` (forschung.py Z. 148-153), nie den
  Ort.

## 7. `max` beim Abschluss / doppeltes Abschliessen?

**Ergebnis: stimmt woertlich ueberein; nichts verdoppelt sich.**

Entw. Z. 680 `kenntnis[a["gebiet"]] = max(kenntnis.get(a["gebiet"],0),a["zielstufe"])` ↔ Code Z. 605
zeichengleich (nur Leerzeichen). Doppeltes Abschliessen kann **nichts doppeln**: Nach dem ersten
Abschluss setzt Z. 606 `neu["forschungsauftrag"] = None`; ein zweiter Aufruf liest
`a = neu.get("forschungsauftrag")` = `None` (Z. 603) und ueberspringt die Bedingung Z. 604. Selbst
wenn dieselbe Stufe erneut angewandt wuerde, macht `max` sie nicht groesser.

## 8. Bibliotheksausbau einer beschaeftigten Bibliothek

**Ergebnis: in DIESEM Modul nicht geregelt (gehoert zu main/Anbindung) — kein Fehler.**

- In `src/spieloekonomie.py` existiert **keine** Ausbau-Funktion (Volltextsuche: `ausbau` nur in
  Kommentaren; `bibliothek` nur als `gebaeude_wirkung.bibliothek_stufe` Z. 574 sowie in Kommentaren
  und Docstrings). Der Entwurfscodeblock Z. 656-683 regelt den Ausbau ebenfalls nicht.
- Die Handbuchsperre „...in der Siedlung, in der geforscht wird, weder die Bibliothek ausbauen...“
  (Handbuch Z. 423-424, zitiert in `belege_forschung_je_siedlung.md` Z. 32) und die in Entwurf
  Z. 686 geforderte neue Pruefung „Ausbau einer beschäftigten Bibliothek abgelehnt“ gehoeren zur
  main-Anbindung bzw. zum Bau-Pfad — **nicht in diesen Modulabschnitt**.

## 9. Was der Entwurfsabschnitt fordert und im Modul FEHLT (offen, kein Fehler)

1. **main-Anschluss** — Entw. Z. 651 „Anschluss main._start_research und forschung_fortschreiben“.
   In `src/main.py` gibt es **keinen** Treffer fuer `forschung_start`/`forschung_abschluss`
   (Volltextsuche). Die alte `spielschicht.forschung_starten` (Z. 390) ist **nicht** der neue Weg
   (sie zahlt ueber `zustand["ressourcen"]` und `GW.forschung_erlaubt`). -> offen.
2. **Neue Testdatei** — Entw. Z. 686 „neue test_lokale_forschung.py“. In `tests/` existiert nur
   `test_lokale_lager.py`; `test_lokale_forschung.py` **fehlt**. -> offen.
3. **Neue Pruefungen** (Entw. Z. 686: „zweite Forschung in derselben Bibliothek abgelehnt, in
   zweiter Bibliothek anderes Gebiet erlaubt; Ausbau einer beschäftigten Bibliothek abgelehnt“)
   haben keine Testdatei. -> offen.
4. **„Universelle Basis50 bleibt ausdrücklich Vorschlag“** (Entw. Z. 686) — in diesem Modul nicht
   geregelt; die Kosten kommen aus `forschung.kosten` -> `spieldaten.forschungs_kosten`
   (forschung.py Z. 56-58). -> offen/aussen.
5. **Mitzieh-Tests** (Entw. Z. 686): `test_forschung.py`, `test_forschungspfad.py`,
   `test_forschung_wirkung.py`, `test_gui_fehler.py` existieren, pruefen aber nicht zwingend die
   neuen Funktionen, solange die main-Anbindung fehlt. -> offen.
6. **Grundsatzfrage** „Forschungsstufe je Siedlung oder global“ ist laut
   `belege_forschung_je_siedlung.md` (Abschnitt „SCHWEIGT DAS HANDBUCH“, Z. 228-229) offen; der
   Code behandelt `wissen` als uebergebenen Stand (Code Z. 552-554). -> offen.

## 10. Zaehlung: woertlich uebereinstimmend / abweichend / nicht geregelt

### a) woertlich uebereinstimmend — 10 Zusagen

1. Pruefreihenfolge Auftrag -> Gebiet -> Bibliothek -> Voraussetzungen -> Kosten (Entw. 658-666 ↔ Code 570-584)
2. `verbrauchen` vor `starten` (Entw. 667 ↔ Code 585)
3. `starten(..., None)` -> keine zweite Abbuchung (Entw. 670 ↔ Code 588; Grenze forschung.py 139)
4. Auftrag am Ort (Entw. 673 ↔ Code 591)
5. Stufe erst beim Abschluss (Entw. 680 ↔ Code 605)
6. `max` beim Abschluss (Entw. 680 ↔ Code 605)
7. Abschlussbedingung `startzeit + dauer_stunden*3600 <= jetzt` (Entw. 679 ↔ Code 604)
8. Auftrag loeschen (Entw. 681 ↔ Code 606) und `fertigjournal`-Zeile (Entw. 682 ↔ Code 607)
9. Deepcopy + Rueckgabe ohne Seiteneffekt (Entw. 657/677 ↔ Code 569/602)
10. `stand`-Konstruktion (Entw. 668 ↔ Code 586)

### b) abweichend — 4 Textstellen (keine Verhaltensabweichung bei gueltigen Daten)

- **A1 (Signatur):** Entw. Z. 656 `def forschung_start(ort, gebiet, wissen, jetzt):` ↔ Code
  Z. 557-558 `def forschung_start(ort: dict, gebiet: str, wissen: dict, jetzt: float, weitere_orte:
  list = ()) -> dict:`. Der Zusatzparameter `weitere_orte` ist von Entwurf Z. 685 ausdruecklich
  gefordert; die Typannotationen sind kosmetisch.
- **A2 (defensive Lesart):** Entw. Z. 658 `neu["forschungsauftrag"]` ↔ Code Z. 570
  `neu.get("forschungsauftrag")`; Entw. Z. 678 `a = neu["forschungsauftrag"]` ↔ Code Z. 603
  `a = neu.get("forschungsauftrag")`. Bei vorhandenem Schluessel identisches Verhalten; ohne
  Schluessel wirft der Entwurfscode `KeyError`, der Code liest `None`.
- **A3 (Zusatzblock):** Der Dublettencheck Code Z. 578-583 samt Hilfsvariable `ziel` (Z. 578) steht
  nicht im Entwurfscodeblock, ist aber von Entw. Z. 685 gefordert. Entw. Z. 666 rechnet
  `kosten = forschung.kosten(wissen.get(gebiet,0)+1)` inline; der Code zieht denselben Wert in
  `ziel` und nutzt ihn zusaetzlich fuer den Check -> **gleicher Wert**.
- **A4 (kosmetisch):** Typannotationen und Docstrings ergaenzt (Code Z. 557-568, 595-601); der
  Entwurf nennt nackte Signaturen.

### c) im Entwurf nicht geregelt / offen — 6 Punkte

- Ausbau der beschaeftigten Bibliothek (gehoert zu main) — §8.
- main-Anschluss `_start_research`/`forschung_fortschreiben` — §9.1.
- Testdatei `test_lokale_forschung.py` und ihre neuen Pruefungen — §9.2/9.3.
- „Universelle Basis50“ — §9.4.
- Wirksamkeit der Mitzieh-Tests ohne Anbindung — §9.5.
- Grundsatzfrage Stufe global/je Siedlung — §9.6.

---

## Verdikt

- **Schwerste Abweichung:** keine verhaltensrelevante. Die schwerste **strukturelle** Abweichung ist
  der von Entwurf Z. 685 geforderte Zusatzblock (Code Z. 578-583) samt Signaturerweiterung
  `weitere_orte` (Code Z. 557-558); der Rest ist woertlich uebereinstimmend.
- **Material genau einmal bezahlt** (Code Z. 585 + 588, `None`-Grenze `forschung.py` Z. 139),
  **Auftrag am Ort**, **Stufe erst beim Abschluss**, **kein unbedingter Merker**, **kein
  Seiteneffekt**, **`max` doppelt nichts** — alles woertlich gemaess Entwurf.
- **Der Fall „anderes Gebiet“** ist in beiden Fassungen erlaubt; der Fall „gleiches Gebiet, andere
  Zielstufe“ ist in beiden Fassungen erlaubt (Entwurf bindet die Ablehnung an das Paar) und mit dem
  einen `wissen` praktisch nicht erreichbar — woertlich uebereinstimmend.
- **Offen (kein Fehler):** main-Anschluss und `test_lokale_forschung.py`.
