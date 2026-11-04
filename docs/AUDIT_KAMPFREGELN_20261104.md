# Audit: welche der acht Kampfregeln stehen schon im Code? (04.11.2026)

**Wozu:** Die acht Kampfregeln sind am 03.11.2026 abgesegnet worden (Register 175,
`docs/ENTSCHEIDUNGEN_KAMPFREGELN_20261103.md`), "gebaut wird in der Reihenfolge 1 bis 8". Der
Stand-Block fuehrt sie als offenen Schritt. Bevor gebaut wird, ist hier GEMESSEN, was schon da ist -
sonst baut man Regeln ein zweites Mal (die Lehre aus den Bauvoraussetzungen vom 30.10.2026).

**Verfahren:** jede Regel gegen eine benannte Stelle im Code gehalten (Funktion und Zeile), Urteil
BELEGT (gebaut) / TEILS / OFFEN. Keine Regel ohne Code-Beleg.

| # | Regel | Ort im Code | Urteil | Beleg |
|---|---|---|---|---|
| 1 | `fusstruppen_begriff` - Fusstruppen sind alle Nahkaempfer, Fernkaempfer zaehlen nicht zur Vorrunden-Schlagkraft, Kampfende wenn alle Nahkaempfer weg | `src/kampf.py` `_nah()`/`_fern()`, Vorrunde `foot_sk = sum(E.schlagkraft(u["name"]) for u in _nah(A))`, Abbruch `if not _alle(V) or not _nah(A)`, Ausgang ueber `not _nah(A)` | **BELEGT** | Zeilen 83-96 (`_nah`, `_fern`), 248-252 (Fussttruppen-Schwelle), 348-357 (Abbruch und Ausgang) |
| 2 | `flucht_formel` - unter 50 % einsatzfaehiger Nahkaempfer wuerfelt die Seite 1-100, Erfolg bei <= 40 + 5 x Sequenz, dann flieht die GANZE Armee (Ausgang `flucht`) | - | **OFFEN** | Kein Wurf dieser Art in `kampf.py`; die Formel `40 + 5 * sequenzen` steht nur in `_sieggeraete` (Zeile 137) und gehoert zu Regel 8. Ausgang `flucht` kommt in `kampf.py` nicht vor. |
| 3 | `beute_verteilung` - Beutesatz 100/60/30/10 nach Wallzustand, anteilig nach Vorratsmenge, gedeckelt durch die Karrenladung | `src/kampfbericht.py` `beute_staffel()` + `beute_lage()` + `BEUTE_STAFFEL_PROZENT` | **BELEGT** | `beute_staffel` Zeile 227-262; Deckel `min(kapazitaet, int(gesamt * anteil))` |
| 4 | `beute_reihenfolge` - reicht die Ladung nicht, wird in der Reihenfolge Gold, Metall, Stein, Holz, Nahrung, Leder, Wolle, Pferde entnommen | `src/kampfbericht.py` `beute_staffel()` verteilt heute `for stoff in sorted(vorhanden)` - also ALPHABETISCH | **OFFEN** | Zeile 262; in `kampfbericht.py` Zeile 459 steht die Reihenfolge nur als TEXT in `vorschlaege()`, nicht als Rechnung |
| 5 | `belagerungsturm_mauerschaden` - Turm 1-4 minus Wallstufe (Katapult 2-13), je Turm einzeln gewuerfelt, positiver Rest geht vom Zustand ab | `src/kampf.py` Mauerschaden-Block + `einheiten.mauer_schaden()` (TP_min/TP_max aus `data/units.json`) | **BELEGT** | `kampf.py` Zeile 297-302: `max(0, rng.randint(minimum, maximum) - stufe)` je Waffe |
| 6 | `mauer_reparatur` - aktive Reparatur MIT Bauzeit, 1 Prozentpunkt Zustand kostet 1 Prozent der Baukosten der aktuellen Wallstufe, keine automatische Reparatur | - | **OFFEN** | `src/dorfwall.py` kennt keine Reparatur (`grep -n "reparatur\|reparieren"` leer); der Wallzustand wird nur gelesen und nach Kaempfen gesetzt |
| 7 | `vorrunde_wiederholung` - Vorrunde genau EINMAL je Schlacht, bei Scheitern unentschieden und keine Beute; bei Zustand 0 gilt die Vorrunde als bestanden, wenn die Belagerungs-Mindestanforderung erfuellt ist | `src/kampf.py` Vorrunden-Block | **BELEGT** | Zeile 243-262: eine Schwellenpruefung je Aufruf, `vorrunde_bestanden` genau einmal gesetzt; die Pruefung rechnet mit `faktor = zustand / 100.0`, also auch bei 0 Prozent |
| 8 | `geraetebeute` - Karren und Belagerungswaffen werden zerstoert, nicht erbeutet: 10 Prozent je verstrichener Sequenz (aufgerundet je Typ), hoechstens 50 Prozent | `src/kampf.py` `_sieggeraete()` | **BELEGT** | Zeile 130-140: `min(50, ...)`-Deckel, Wurf `40 + 5 * sequenzen` fuer das Entkommen je Stueck |

## Ergebnis

**Fuenf von acht Regeln stehen schon im Code** (1, 3, 5, 7, 8). **Drei sind offen: 2, 4, 6.**
Der naechste Bau in der abgesegneten Reihenfolge ist damit **Regel 2 (Flucht)**, danach 4
(Beute-Reihenfolge Gold zuerst) und 6 (Mauerreparatur mit Bauzeit).

**Warum die Reihenfolge trotzdem 2 -> 4 -> 6 bleibt:** Regel 2 braucht einen neuen Ausgang `flucht`
und die Rueckgabe der Einheiten an den Aufrufer (`kampf_am_ziel`, `einsatz_zurueck`); Regel 4 ist eine
reine Rechenaenderung in `beute_staffel`; Regel 6 braucht eine neue Aktion in der Oberflaeche
(Reparatur mit Bauzeit). Von klein nach gross waere 4 -> 6 -> 2; Daniel hat 1 bis 8 abgesegnet, die
Reihenfolge ist seine Entscheidung.

## Was diese Datei NICHT behauptet

- Sie prueft die Regeln NICHT in der Schlacht (keine Simulation), sondern ihre Stelle im Code. Ob die
  Wuerfe im Detail stimmen, pruefen die Wachen (`test_kampf`, `test_kampfbericht`,
  `test_gpt_kampf_forum_neu`).
- Regel 7 "bei Zustand 0 Prozent gilt die Vorrunde als bestanden, wenn die Belagerungs-Mindest-
  anforderung erfuellt ist" ist als Code vorhanden; ob die Reihenfolge der beiden Schwellen der
  Daniels-Wortlaut genau entspricht, ist NICHT einzeln nachgemessen.
