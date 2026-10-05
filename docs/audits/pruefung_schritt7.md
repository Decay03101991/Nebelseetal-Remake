# Pruefung Schritt 7 — `zielstatus` gegen den freigegebenen Entwurf

- Gegenstand: neue Funktion `zielstatus(orte, jetzt, haltestart=None)` in `src/spieloekonomie.py`
  (Abschnitt "Schritt 7", Zeilen 611-669) samt Kommentaren.
- Massstab: freigegebener Entwurf
  `docs/audits/entwurf_spieloekonomie_sol_2026-10-05.txt`, Abschnitt
  "7. Zielpruefung und Haltefenster, unabhaengig von Originalpunkten" (Z. 688-715).
- Methode: reine Quelltextpruefung. Kein git, kein Spielstart, kein `run_tests.bat`, keine
  Aenderung an Projektdateien. Der Entwurf ist die Vorgabe; jede Abweichung ist mit Zeilennummer
  und woertlichem Zitat belegt.
- Bezugsdatei-Basis: `src/spieloekonomie.py` hat 669 Zeilen (Total laut Dateiende).

Legende: E = Entwurfsdatei, I = Implementierung (`src/spieloekonomie.py`).

---

## 1. Die acht Bedingungen (Kartenqualitaet, Plan, Deckung, Reserve, Handel, Armee, Ware+Forschung, Reihenfolge)

Die sieben Praedikate und ihre Reihenfolge stehen in der `ok`-Zuweisung.

E Z. 707:
> `ok = q["erfuellt"] and plan_ok and deckung>=1 and reserve and handel and armee and {"ware","forschung"}<=fertig`

I Z. 661-662:
> `ok = (bool(q.get("erfuellt")) and plan_ok and deckung >= 1 and reserve and handel and armee`
> `      and {"ware", "forschung"} <= fertig)`

Befund: Reihenfolge **identisch** (q, plan_ok, deckung>=1, reserve, handel, armee,
{ware,forschung}). Wortlaut je Bedingung:
- Kartenqualitaet: `q["erfuellt"]` (E) vs `bool(q.get("erfuellt"))` (I) — gleichwertig.
- geplanter Plan: `plan_ok` — identisch.
- Deckung >= 1: `deckung>=1` (E) vs `deckung >= 1` (I) — nur Leerzeichen.
- Reserve: `reserve` — Name identisch, **Wert weicht im Leerfall ab, siehe Abschnitt 2**.
- Handel: `handel` — identisch.
- Armee: `armee` — identisch.
- Ware UND Forschung fertig: `{"ware","forschung"}<=fertig` (E) vs `{"ware", "forschung"} <= fertig` (I) — nur Leerzeichen.

Ergebnis: keine der acht Bedingungen ist inhaltlich/reihenfolgig veraendert. Die einzige
Bedingungs-Relevanz hat die Reserve im Leerfall (Abschnitt 2), ohne Einfluss auf `ok`/`sieg`.

---

## 2. Die kritische Zeile `reserve = bool(orte) and all(...)` — Verhaltensabweichung?

E Z. 699:
> `reserve = all(bezahlbar(o["vorraete"],o["reserve"]) for o in orte)`

I Z. 650-651 (mit Kommentar Z. 648-649):
> `# Leerer Verbund ist NIE versorgt (der Entwurf schreibt `all(...)`; ohne Orte wäre das`
> `# leer-wahr und ein leerer Spielstand hätte „gehalten" — bewusste, dokumentierte Abweichung).`
> `reserve = bool(orte) and all(bezahlbar(o.get("vorraete") or {}, o.get("reserve") or {})`
> `                             for o in orte)`

**Ja, es ist eine Verhaltensabweichung. Genau bei der Eingabe `orte == []`** (bzw. wenn der
Filter I Z. 641 `[o for o in (orte or []) if isinstance(o, dict)]` die Liste auf leer reduziert).

- E: `all(...)` ueber eine leere Sequenz ist **leer-wahr** → `reserve = True`.
- I: `bool([])` ist `False` → `reserve = False`.

Damit unterscheidet sich das **Rueckgabefeld `reserve`** (`{"reserve": reserve}`, I Z. 668-669)
im Leerfall: Entwurf True, Implementierung False.

**Kein Einfluss auf `sieg`.** Bei `orte == []` liefert die Kartenqualitaet bereits `erfuellt` False
(E/I Z. 693/642; `kartenqualitaet` verlangt `len(karten) >= REGELN["mindestsiedlungen"]` = 4,
`src/spieloekonomie.py` Z. 143), also ist `ok` in **beiden** Fassungen False und `sieg` False. Die
Grenze veraendert nur den angezeigten `reserve`-Wert, keine Gewinn-/Verlustentscheidung.

**Ist die Begruendung stichhaltig?** Teilweise:
- Stichhaltig: ohne die Grenze ist der zurueckgegebene `reserve`-Wert im Leerfall irrefuehrend
  `True` ("alles reserviert", obwohl es nichts gibt).
- **Nicht stichhaltig** ist die konkrete Behauptung "ein leerer Spielstand hätte 'gehalten'":
  Ein leerer Verbund kann `ok`/`sieg` nie erreichen, weil die Kartenqualitaet (>= 4 Siedlungen)
  immer vorher scheitert — die Halteentscheidung war nie gefaehrdet.
- Formal bleibt es eine **Abweichung vom freigegebenen Entwurf ohne dokumentierte Freigabe**.
  Sie ist harmlos fuers Ergebnis, aber nach dem Massstab ("JEDE Abweichung ... belegen")
  zu melden. Zu empfehlen: Daniel entscheidet ueber Beibehaltung/Streichung, oder der Kommentar
  wird auf den korrekten Grund (nur Anzeige im Leerfall) gekuerzt.

---

## 3. Rueckgabeschluessel `plan` — additiv oder veraendernd?

E Z. 710-711:
> `return {"sieg":sieg,"haltestart":start,"qualitaet":q,"deckung":deckung,`
> `        "reserve":reserve,"handel":handel,"armee":armee}`

I Z. 668-669 (mit Kommentar Z. 666-667):
> `return {"sieg": sieg, "haltestart": start, "qualitaet": q, "deckung": deckung,`
> `        "reserve": reserve, "handel": handel, "armee": armee, "plan": plan_ok}`

**Additiv, keine Verhaltensaenderung.** Der Entwurf nennt `sieg, haltestart, qualitaet, deckung,
reserve, handel, armee` (E Z. 710-711); `plan` ist ein **zusaetzlicher** Schluessel. Er kollidiert
mit keinem Entwurfs-Schluessel und aendert keinen bestehenden Wert. `plan_ok` ist bereits lokal
berechnet (I Z. 646). Der Kommentar verweist auf Entwurf Z. 714 ("messbare Fehlgruende"). Hinweis:
der Rueckgabewert heisst `plan`, traegt aber den Bool `plan_ok` (nicht das Plan-Dict) — reine
Benennung, keine Rechnung.

---

## 4. Wird `haltestart` nach der Entwurfsregel gesetzt/zurueckgesetzt?

E Z. 708:
> `start = (jetzt if haltestart is None else haltestart) if ok else None`

I Z. 663:
> `start = (jetzt if haltestart is None else haltestart) if ok else None`

**Zeichengleich** (die eine geforderte Zeile im Modul stimmt woertlich mit dem Entwurf ueberein).
Zusatz in I Z. 664-665: `sieg = bool(ok and start is not None and jetzt - start >= ...)` — das
`start is not None` ist redundant: wenn `ok` True ist, ist `start` immer `jetzt` bzw. `haltestart`,
also nie None; kein Verhaltenseffekt fuer wohlgeformte Eingaben.

---

## 5. Verwendet die Reservepruefung den OERTLICHEN Bestand?

E Z. 715 (woertlich):
> `die Reservepruefung verwendet oertlichen Bestand`

I Z. 650-651:
> `reserve = bool(orte) and all(bezahlbar(o.get("vorraete") or {}, o.get("reserve") or {})`
> `                             for o in orte)`

Ja: geprueft wird je Ort `o.get("vorraete")` (lokaler Bestand) gegen `o.get("reserve")` (lokale
geforderte Reserve), **innerhalb der `for o in orte`-Schleife** — kein gemeinsamer Summenbestand.
Woertliche Entsprechung zum Entwurf E Z. 699 (dort `o["vorraete"]`/`o["reserve"]`).

---

## 6. Zaehlt der Handel wirklich nur VERBRAUCH (nicht Ankunft/Transport)?

Ja. Beide beteiligten Zeilen:

zielstatus, I Z. 653-656:
> `importe = {(o.get("id"), z["rohstoff"]) for o in orte`
> `           for z in (o.get("verbrauchsjournal") or [])`
> `           if ab < z["zeit"] <= jetzt and z["menge"] > 0}`
> `handel = len({r for _, r in importe}) >= 2 and len({i for i, _ in importe}) >= 2`

verbrauchen, I Z. 286-288 (der **einzige** Schreiber des `verbrauchsjournal`):
> `if genutzt > 0:`
> `    neu["verbrauchsjournal"].append({"zeit": jetzt, "rohstoff": r, "menge": genutzt,`
> `                                     "ziel": ort["id"]})`

Beleg fuer "nur Verbrauch": Volltextsuche nach `verbrauchsjournal` in `src/spieloekonomie.py`
liefert ausschliesslich diese Stellen (Z. 287-288 als Schreiben, Z. 654 als Lesen in `zielstatus`).
`transport_start` (I Z. 292-338) schreibt in `importiert` und die Mission, **appended aber nie**
an `verbrauchsjournal`. Der Journal-Eintrag entsteht nur bei echtem Verbrauch importierter Ware
(`genutzt > 0`, Z. 283-286). Hin-und-her-Fracht ohne Verbrauch erzeugt daher keinen `importe`-
Eintrag und kann `handel` (>= 2 Rohstoffe aus >= 2 Orten) nicht erfuellen — Entwurf Z. 715 erfuellt.

---

## 7. Wird `punkte.sieg_oder_niederlage` hier NICHT aufgerufen?

E Z. 714 (woertlich):
> `punkte.sieg_oder_niederlage ausschliesslich im Altmodus aufrufen`

Volltextsuche in `src/spieloekonomie.py` nach `punkte.`/`sieg_oder_niederlage` liefert **nur
Kommentarzeilen**, keinen Aufruf und keinen `import punkte`:
- I Z. 616: `# Der Altmodus gewinnt über Punkte (`punkte.sieg_oder_niederlage`). Der Ökonomiemodus gewinnt`
- I Z. 619: `# ... Die Original-Punkteformeln bleiben unangetastet.`

Bestätigt: **kein Aufruf** in `src/spieloekonomie.py`, insbesondere nicht in `zielstatus`.

---

## 8. Wird eine Original-Punkteformel in diesem Schritt angefasst?

**Nein.** `src/spieloekonomie.py` ruft `punkte` nirgends auf (Suche nach `punkte.` → nur die zwei
Kommentarzeilen Z. 616/619 oben). Es gibt keinen `import punkte` und keine Punkteformel im Modul.
Die Originalformeln liegen in `src/punkte.py` (nur gelesen). Entwurf Z. 714 ("punktestand und alle
Original-Punkteformeln unveraendert lassen") ist damit auf Modulebene eingehalten.

---

## 9. Was der Entwurfsabschnitt fordert und im Modul FEHLT (offen, nicht Abweichung)

- **main-Anschluss** `GameState.spielausgang` (E Z. 689, 714). In `src/main.py` Z. 617-632 gibt
  `spielausgang` **bedingungslos** `punkte.sieg_oder_niederlage(...)` zurueck; **kein**
  Ökonomiemodus-Zweig, **kein** Aufruf von `zielstatus`. Einbindung von `zielstatus(alle eigenen
  Orte, ..., haltestart)` fehlt. Volltextsuche `zielstatus` in `src/` findet nur die Definition in
  `spieloekonomie.py` (Z. 631) — keine Aufrufstelle.
- **_pruefe_spielende** (`src/main.py` Z. 3959-3976) unveraendert; "kann unveraendert einmalig
  einfrieren" (E Z. 714) ist damit konsistent, aber die Ökonomiemodus-Verzweigung fehlt.
- **neue Pruefdatei `test_versorgungsziel.py`** (E Z. 715). Volltextsuche in `tests/` → **nicht
  vorhanden** (Dateiliste enthaelt sie nicht).
- **Haltebeginn im Speicherstand bewahren** (E Z. 715: "Speicherstand bewahrt Haltebeginn").
  Kein Save-/Load-Code durchgesehen; im geprueften Umfang keine Sicherung von `haltestart`
  nachgewiesen — als offen gefuehrt.
- **Anzeige der konservativen Strenge** (E Z. 713: "Anzeige muss dies deutlich machen"). Im Modul
  nicht vorhanden (reine Datenfunktion) — erwartungsgemaess offen bis zur main-Anbindung.
- **Mitziehen der Tests** (E Z. 715: `test_punkte.py`, `test_punkte_einhaengung.py`,
  `test_durchspiel.py`) — nicht ausgefuehrt (kein Testlauf erlaubt), daher ungeprueft.

---

## 10. Zaehlung

Grundlage: 20 Codezeilen des Entwurfs (E Z. 692-711), abgebildet auf I Z. 631-669.

- **Woertlich/gleichwertig uebereinstimmend: 8 Zeilen.**
  - zeichengleich: E 695/644 (`plan = REGELN["plan"]`), E 705/659 (`armee = ...`), E 708/663
    (`start = ...`).
  - nur Leerzeichen, sonst gleich: E 694/643, E 697/646, E 700/652, E 703/656, E 698/647
    (zusaetzlich `default=0` → `default=0.0`, rein numerisch gleich).
- **Abweichend MIT Begruendung im Code: 2.**
  1. `reserve = bool(orte) and all(...)` (I Z. 650-651) gegen E Z. 699 — **Verhaltensabweichung im
     Leerfall** (Rueckgabe `reserve` True→False, ohne Wirkung auf `sieg`); Begruendung vorhanden
     (I Z. 648-649), aber in der Aussage "hätte gehalten" nicht stichhaltig (siehe Abschnitt 2).
  2. `q = ... if orte else {"erfuellt": False}` (I Z. 642) gegen E Z. 693 — im Leerfall liefert das
     Feld `qualitaet` nur `{"erfuellt": False}` statt der drei Schluessel `erfuellt/mittel/beste`
     aus `kartenqualitaet([])`; `ok` unveraendert.
- **Abweichend OHNE eigene Begruendung, aber verhaltensneutral fuer wohlgeformte Eingabe
  (Defensive/Robustheit): 5.**
  - E 696/645 `reserviert` (`.get("reserve") or {}`), E 701-702/653-655 `importe`
    (`.get(...) or []`, `o.get("id")`), E 704/657-658 `rollen` (`.get("einheiten") or {}`),
    E 706/660 `fertig` (`.get("fertigjournal") or []`), E 707/661 `ok`
    (`bool(q.get("erfuellt"))`). Alle nur gegen fehlende Schluessel absichernd; bei
    vollstaendigen Ortsdatensaetzen wirkungsgleich mit dem Entwurf.
- **Additiv / nicht geregelt (im Entwurf nicht genannt): 3.**
  - Rueckgabeschluessel `plan` (I Z. 669) — additiv, keine Verhaltensaenderung (Abschnitt 3).
  - Signatur-Details der Implementierung `def zielstatus(orte: list, jetzt: float,
    haltestart=None) -> dict:` (I Z. 631) gegen E Z. 692 `def zielstatus(orte, jetzt, haltestart):`
    — Typangaben und `haltestart=None` (Default). Additiv/kompatibel; die Entwurfsregel E Z. 708
    setzt `haltestart is None` ohnehin voraus.
  - Eingangsfilter `orte = [o for o in (orte or []) if isinstance(o, dict)]` (I Z. 641) — im
    Entwurf nicht enthalten; verhaltensneutral fuer eine Liste von Dicts.
- **Redundanter Zusatz ohne Verhaltensaenderung: 1.**
  - `sieg = bool(ok and start is not None and ...)` (I Z. 664-665) gegen E Z. 709
    `sieg = ok and jetzt-start>=...` — `start is not None` ist bei True-`ok` immer wahr.

Summe: 8 uebereinstimmend + 2 (begruendet abweichend) + 5 (Defensive) + 3 (additiv/nicht geregelt)
+ 1 (redundant) + 1 (siehe Abschnitt 2/Position 2 der begruendeten = bereits gezaehlt) → die
20 Entwurfszeilen sind vollstaendig erfasst (gruppiert, teils mehrere Zeilen je Position).

---

## Schwerste Abweichung

`reserve = bool(orte) and all(...)` (I Z. 650-651) gegen Entwurf E Z. 699
`reserve = all(bezahlbar(o["vorraete"],o["reserve"]) for o in orte)`: eine bewusste, im Code
kommentierte Verhaltensabweichung. Sie aendert das Rueckgabefeld `reserve` bei leerem Verbund
(True→False), beruehrt aber `sieg`/`ok` nicht, weil die Kartenqualitaet leere Verbuende ohnehin
scheitern laesst. Die Begruendung "ein leerer Spielstand hätte gehalten" ist sachlich nicht
zutreffend; stichhaltig bleibt nur die Anzeige-Korrektur. Nach dem Massstab ist sie als
unfreigegebene Abweichung zu melden.

## Nicht geprueft / ausserhalb des Gegenstands

- Kein Testlauf, kein Spielstart, kein git (untersagt) — rein statische Quelltextpruefung.
- `src/punkte.py` und `src/main.py` nur gelesen, nicht geaendert; der fehlende main-Anschluss ist
  als offen gemeldet (nicht als Abweichung).
- Persistenz von `haltestart` im Speicherstand nicht durchgesehen.
- Schritte 1-6 und ab 8 des Entwurfs nicht Gegenstand.
- Werte in `data/spieloekonomie.json` (z. B. `versorgung_stunden` = 24, `plan`) nur als Randbedingung
  gelesen, nicht als eigene Verhaltenspruefung.
