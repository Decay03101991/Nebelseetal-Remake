# Entwurf: Spielziel, Handel und Kartenauswahl (Vorgabe Daniel 05.10.2026, 16:1x)

**Zweck:** Daniels neue Richtungsvorgabe festhalten, den Ist-Zustand messen und einen Vorschlag mit
Zahlen vorlegen. **Jede Zahl hier ist VORSCHLAG** — die Entscheidung ist Daniels.

---

## 1. Daniels Vorgabe (wörtlich)

> es soll nicht darauf aufbauen, wer schneller ist gewinnt, sondern taktische handel zwischen eigenen
> siedlungen und die auswahl der richtigen karten (was schon teuer sein muss, eine neue karte
> besiedeln zu dürfen, inklusive minimum rohstoff Guthaben das man braucht um eine neue Siedlung
> gründen zu können. ) Also anfangs ist schon wichtig schnell alle verfügbaren karten mit jeweils den
> rohstoff vorteilen zu sichern die man am ende nutzt um durch handel verschiedene städte zu stärken.
> Nur auf der anfangs map soll es ausgeglichene Rohstoffe geben um theoretisch alles zu produzieren.
> In den möglichen karten von neu Gründungen soll es nur 2 oder 3 start map ähnlich ausgeglichene
> karten geben, die anderen karten sollen eher Minen und Steinmetze bevorzugen oder Farmen oder holz
> oder mischungen aus zweien und von dem dritten fast nichts. aber es muss so gebalanced sein, dass
> Rohstoffproduktion und handel die grundlage für stabile starke truppen aufbau und entwicklung sowie
> forschung bieten.

## 2. Was das ändert

| Punkt | Bisher | Neu (Vorgabe) |
|---|---|---|
| Sieg | Punkteziel 300 — faktisch ein Wettlauf | **kein Wettlauf**: Aufbau, Kartenwahl und Handel entscheiden |
| Startkarte | zufälliger Kartentyp | **ausgeglichen** (theoretisch alles produzierbar) |
| Karten für Neugründungen | zufällig aus 5 Typen mit Gewichten | **fester Vorrat**: 2–3 ausgeglichene, die übrigen spezialisiert |
| Neugründung | **kostenlos** (`main._found_settlement` prüft keinen Preis) | **teuer** + **Mindest-Rohstoffguthaben** |
| Handel | Transport-Modul vorhanden (`src/auftraege.py`) | **Kern des Spiels**: eigene Siedlungen stärken sich gegenseitig |
| Karten sichern | kein Vorrang | früh alle verfügbaren Karten mit ihren Vorteilen sichern |

## 3. Ist-Zustand (gemessen, nicht geschätzt)

| Sache | Stand | Beleg |
|---|---|---|
| Kartentypen | **5**: Waldreiche Karte, Steinreiche Karte, Weideland, Nebelseeufer, Ausgeglichene Karte | `data/gelaende.json`, `kartentypen.listen` |
| Typwahl | per **Saat zufällig**, Gewichte 20/20/20/10/30 — **kein Vorrat, kein Vorrang**, die Startkarte ist zufällig | `src/gelaende.py`, `karten_typ(seed)` |
| Geländemischung je Typ | je Karte Schwerpunkte, aber **kein Typ schließt einen Rohstoff wirklich aus** | `kartentypen.listen[*].gewichte` |
| Neugründung | **kostenlos**; nur eine Obergrenze und die Kartenregel „niemals zwei gleiche" | `main._found_settlement`, `SIEDLUNGEN_MAXIMUM = 6` |
| Mindestguthaben | **gibt es nicht** | kein Preis im Code |
| Sieg/Niederlage | Punkteziel 300 (Schritt 31) — **jetzt vorläufig**, weil diese Vorgabe es ablöst | `src/punkte.py`, `main.spielausgang` |

## 4. Vorschlag Kartenvorrat (VORSCHLAG — Daniel entscheidet)

**Startkarte (immer die erste Siedlung): ausgeglichen** — von jedem Gut etwas, Mindestbesatz gesichert.

Für die **Neugründungen** ein **fester Vorrat** (ohne Wiederholung, damit jede Karte wirklich etwas
Eigenes ist). Vorschlag mit 6 Siedlungen (`SIEDLUNGEN_MAXIMUM = 6`, belegt: sechs Welten):

| Nr | Karte | Schwerpunkt (viel) | Fast nichts |
|---|---|---|---|
| 0 | **Startkarte** | alles (ausgeglichen) | Sumpf (unbebaubar) |
| 1 | Ausgeglichene Karte (2. Startkarte) | alles | Sumpf |
| 2 | Ausgeglichene Karte (3. Startkarte) | alles | Sumpf |
| 3 | Stein & Erz | Berg, Hügel | Nahrung, Wolle, Leder, Pferde |
| 4 | Farmland | Grasland, Steppe | Stein, Metall, Gold |
| 5 | Wald & Weide (Mischung aus zwei) | Wald, Grasland | Stein, Metall, Gold |

(„Fast nichts" heißt: die Gewichte sind dort auf ein Minimum gesetzt, **nicht** auf null — sonst wäre
die Mindestbesatz-Regel verletzt und die Karte unbewohnbar.)

## 5. Vorschlag Gründungskosten (VORSCHLAG — Daniel entscheidet)

Abgeleitet aus den **belegten** Baupreisen (Haus 80 Holz + 50 Stein): eine neue Siedlung ist der
größte Bau im Spiel, soll also deutlich mehr kosten als ein Haus — und **danach** muss noch etwas
übrig sein, sonst verhungert die neue Stadt sofort.

* **Preis:** 400 Holz · 400 Stein · 200 Nahrung · 1 Siedler (Siedler sind Bevölkerung, Handbuch S. 11)
* **Zusätzlich verlangt (Mindestguthaben VOR der Gründung):** 500 Holz · 500 Stein · 300 Nahrung —
  die neue Siedlung startet also nicht mit leeren Lagern.
* **Zusätzlich verlangt:** die Forschung **„Vermessung"** (so ist es schon geregelt) und eine
  **freie Karte** aus dem Vorrat.

## 6. Offene Entscheidungen (an Daniel)

1. **Wann ist gewonnen?** (a) kein Sieg, nur Niederlage — wie das Original, der Aufbau ist das Ziel ·
   (b) Sieg, wenn **alle Karten besiedelt** sind und zusätzlich ein hohes Punktziel erreicht ist ·
   (c) Punkteziel behalten, aber deutlich höher setzen.
2. **Wie viele Karten/Siedlungen?** 6 (belegt) oder weniger?
3. **Gründungskosten** wie in Abschnitt 5 — oder andere Zahlen?
4. **Kartenvorrat** wie in Abschnitt 4 — oder andere Aufteilung (z. B. 4 spezialisierte)?

## 7. Nächste Bauschritte (erst nach Daniels Entscheidung)

1. Startkarte erzwingen (`gemischt`) und den Kartenvorrat für Neugründungen als feste Liste in
   `data/gelaende.json` (`kartentypen.vorrat`) — Neugründungen ziehen der Reihe nach, nicht zufällig.
2. Die Typen so umbauen, dass ein Rohstoff wirklich **fast** fehlt (Gewicht auf Minimum), ohne die
   Mindestbesatz-Regel zu verletzen.
3. Gründungskosten + Mindestguthaben in `data/` und in `main._found_settlement`; Anzeige „fehlt noch
   …" im Siedlungsmenü.
4. Handel zwischen eigenen Siedlungen als Träger des Spiels ausbauen (Warenpreise je Siedlung aus
   den Kartenvorteilen).
5. Erst danach die Sieg-/Niederlagebedingung endgültig festlegen und die `.exe` neu bauen.

---

## 8. Nachtrag: drei weitere Vorgaben Daniels (05.10.2026, 16:2x — wörtlich)

> „weiter: Natürlich soll man nicht gewinnen wenn man nur unvorteilhafte karten auswählt. Schwierigere
> Bots müssen das wissen und danach handeln"

> „leicht mittel schwer reicht"

Daraus folgt für den Entwurf:

1. **Die Qualität der Kartenwahl entscheidet mit.** Wer nur unvorteilhafte Karten besiedelt, darf
   **nicht** gewinnen können. Das Ziel braucht deshalb eine **messbare** Kopplung an den Ertrag/wert
   der eigenen Siedlungen (nicht nur eine Punktzahl aus Forschung und Krieg).
2. **Bots kennen die Ökonomie.** Je Schwierigkeitsstufe bewerten sie Karten, planen Neugründungen,
   handeln — und bestrafen einen Spieler, der schlechte Karten nimmt (früher auf die guten Karten,
   Preisdruck im Handel).
3. **Drei Schwierigkeitsstufen genügen:** leicht / mittel / schwer.

**Der vollständige Auftrag an das starke Modell steht in `docs/AUFTRAG_SOL_SPIELOEKONOMIE.md`** —
mit allen Randbedingungen, dem gemessenen Ist-Zustand und der geforderten Gliederung A–H.
