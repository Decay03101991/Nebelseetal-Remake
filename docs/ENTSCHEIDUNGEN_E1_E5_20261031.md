# Entscheidungsblatt E1–E5 — bitte kurz ankreuzen

> ## ENTSCHEIDEN AM 31.10.2026 (Daniel) — dieses Blatt ist damit erledigt
>
> | # | Entscheidung |
> |---|---|
> | **E1** | **Neueste Fassung ist das Original**; wo die neuere nur **Werte** nennt und die ältere die **Mechanik** beschreibt, gilt **Mechanik alt + Zahlen neu** (ZUSAMMENFÜHRUNG). Der Kampf bleibt beim neueren Forum-Original, Wall/Beute/Geräteverlust/Punkte kommen aus dem Handbuch. |
> | **E2** | **Faktor 2** (`Dauer = 2 · Distanz / GS`) als Arbeitsformel — ausdrücklich **anpassbar**; Daniels eigene Zahlen sind verwerfbar, wenn Quellen etwas vorgeben. |
> | **E3** | **Zwei Bewegungssysteme:** Umsetzung folgt; der Altpfad wird über `auftraege.starten` geleitet, nichts gelöscht (Landkarte: `docs/audits/BEWEGUNGSSYSTEME_LANDKARTE.md`). |
> | **E4** | **Beute gestaffelt:** Mauer steht → wenig; Mauer schon eingerissen → viel; keine Verteidiger → voller Bestand bis zur Karrenladung. Prozentwerte = VORSCHLAG, im Spieltest balancieren. Der 50-%-Deckel ist damit **ersetzt**. |
> | **E5** | **Kein Sieg** (das Original hat keine Siegbedingung, Handbuch S. 3). Stattdessen **Bewertung/Auszeichnungen** (Forschung, Krieg, Wirtschaft). **Dimensionen** kosten keine Zeit, werden zu **Ländereien**. |
>
> **Zusatz Daniels:** Die Geschichte/Legende soll **möglichst aus Originaltexten** kommen. Die
> Original-Hintergrundgeschichte ist gefunden und wörtlich gesichert:
> `docs/quellen/ORIGINAL_HINTERGRUNDGESCHICHTE.md` (drei Drachenbrüder, Erschaffung des Nebelseetals,
> Salmurs Magie, das Chaos — Website-Archiv 11.09.2007).
>
> Die Analyse unten bleibt als Begründung stehen.

**Stand:** 31.10.2026, 03:05 · `06aabcb`+ · **Grundlage:** `docs/PRUEFUNG_ENTWURF_WEGZEIT_KAMPF_20261031.md`
(jede Aussage mit Quelle) und `docs/audits/BEWEGUNGSSYSTEME_LANDKARTE.md` (Zeilennummern).
**Wozu:** Ohne diese fünf Entscheidungen darf nichts an Bewegung, Kampf, Beute oder Punkten gebaut
werden — jede wäre sonst eine dritte Wahrheit neben zwei vorhandenen.

Jede Frage hat eine **Empfehlung**. Ein „einverstanden“ genügt; nichts hier ist endgültig, solange
nicht gebaut ist.

---

## E1 — Welches Kampfsystem gilt?

Es gibt zwei Originalquellen, die sich widersprechen:

| | Handbuch 2009 | Neueres Forum-Original |
|---|---|---|
| Einheitenwerte | LE, AT, PA, RS, TP, MU, SK | Konstitution %, Kampfwert-Spanne, Rüstung, Fernkampfwert, Erschöpfungsschwelle |
| Wo | `docs/original/Spielanleitung_2009_Textfassung.txt` | `docs/quellen/Das_Kampfsystem_Neu_Original.odt` |
| Im Code | `src/kampf_alt_handbuch_2009.py` (**Rückfall**, nicht importiert) | `src/kampf.py` (**aktiv**, 15 Profile, 14 Prüfdateien grün) |

**Optionen**
* **A — Forum-Original bleibt, Handbuch liefert Wall/Beute/Geräteverlust/Punkte** (heute so)
* B — zurück zum Handbuch-Modell (LE/AT/PA) → 15 Profile und 14 Prüfdateien werden ersetzt
* C — Mischmodell mit eigenen Werten → das wäre eine Erfindung, nicht mehr original

**Empfehlung: A.** Das Forum-Original ist die **jüngere** Quelle, das Handbuch schweigt zu Beute und
Geräteverlust (die kommen ohnehin aus dem Handbuch). Ein Wechsel auf B kostet mehrere Tage und
bringt keine neue Originaltreue.

---

## E2 — Reiseformel: Faktor 1 oder 2?

| | heute im Code (`auftraege.py` Z. 133–147) | Vorschlag des Entwurfs |
|---|---|---|
| Formel | `Dauer = d / GS` Stunden | `Dauer = 2 · d / GS` Stunden |
| 6 Felder, GS 5 | 1,2 h = **24 s** Echtzeit bei ×180 | 2,4 h = **48 s** |
| 32 Felder, GS 5 | 6,4 h = **2:08 min** | 12,8 h = **4:16 min** |
| 32 Felder, GS 35 | 0,91 h = **18 s** | 1,83 h = **37 s** |

**Empfehlung: Faktor 2 nur, wenn die Karte groß bleibt** (20×20 mit Zielen bis 32 Feldern) — sonst
sind weite Angriffe in unter 20 Sekunden da und der Verteidiger hat keine Vorwarnzeit. **Zusatzfrage
in derselben Entscheidung:** kostet ein Dimensionswechsel **Zeit** (Vorschlag: 20 Felder) oder nur
Mana (Quelle: Mana nach Entfernung)? Meine Empfehlung: **nur Mana** — für Zeit gibt es keinen Beleg.

---

## E3 — Zwei Bewegungssysteme: eines abschalten?

`main.py` hat zwei Wege, Truppen zu bewegen (Einzelheiten in der Landkarte):

* **Aufträge** (`auftraege.py`): GS, Karrenladung, Rückkehr, Wall, Kampf — **geprüft**.
* **Weltkarten-Zug** (`_welt_bewegen` Z. 5690): 5 Spielminuten je Feld **ohne GS**, Beute 10–40 %
  **ohne Karren**, 40 % Münzwurf-Kampf mit 1–4 zufälligen Verlusten.

**Empfehlung: Weltkarten-Zug über `auftraege.starten` leiten, Altcode stehen lassen, nichts löschen.**
Sonst gibt es nach der neuen Formel **drei** Wahrheiten.

---

## E4 — Beuteanteil: 50 % Deckel oder nur Karrenladung?

Das Handbuch sagt nur: **nur Transportkarren plündern**. Einen Anteil nennt es nicht. Im Code steht
`BEUTE_ANTEIL_PROZENT = 50` **nur als Text** (`auftraege.py` Z. 70); gerechnet wird ohne Deckel
(`kampfbericht.beute` Z. 202–242).

**Empfehlung: 50 % Deckel einschalten.** Ein Handkarren (Ladung 40) kann sonst eine kleine Siedlung
anteilig leerlaufen lassen, ohne dass der Angegriffene eine Chance hat. Es bleibt ein VORSCHLAG —
wenn du „original“ willst, bleibt es bei der reinen Ladungsgrenze.

---

## E5 — Portal und Siegbedingung

* **Portal:** die Quelle sagt, der Wechsel verschiebt **die ganze Welt** (alle Siedlungen), und das
  Mana muss **in einer** Siedlung liegen (`portal.php.txt` Z. 23–35). Der Entwurf wollte **eine**
  Siedlung verschieben. **Empfehlung: Quelle folgen** (ganze Welt), weil sonst Koordinaten und
  Laufwege aller Siedlungen auseinanderfallen.
* **Sieg bei 300 Gesamtpunkten:** deine frühere Wahl. Mit der Original-Punkteformel bringt allein
  **Wallstufe 10 = 1.000 Kriegspunkte = 500 Gesamtpunkte** — der Sieg wäre durch Mauerbau erreichbar.
  **Empfehlung: Ziel auf 1.000 Gesamtpunkte** und zusätzlich „Sieg nur mit Kriegspunkten aus Kämpfen,
  nicht aus Verteidigungsanlagen“ prüfen. Alternative: 300 behalten und die Wallpunkte nicht in die
  Gesamtpunktzahl zählen (weicht aber vom Handbuch ab).

---

## Was ich sofort nach deiner Antwort baue (in dieser Reihenfolge)

1. **E2** → eine Formel in `auftraege.py`, Prüfzusage: `test_gpt_zeit_auftragsketten` + neue Prüfung
   mit sechs Beispielreisen (Zahlen aus dem Entwurf, nachgerechnet).
2. **E3** → Weltkarten-Zug über `auftraege.starten`, Prüfzusage: `test_weltkarte`,
   `test_auftraege`, `test_kampf_einhaengung` bleiben grün.
3. **E4** → Deckel in `kampfbericht.beute`, Prüfzusage: neue Prüfung „Beute ≤ 50 % und ≤ Ladung“.
4. **E1** → Kampfteil des Entwurfs umschreiben (kein Code), dann Beute-/Punkte-Anzeige.
5. **E5** → Zielzahl und Portalregel ändern, Prüfzusage: `test_punkte_einhaengung`.

**Ohne Entscheidung** kann ich weiter nur Papiere und Prüfungen liefern — nicht Mechanik.

*Geschrieben 31.10.2026, 03:05. Alle Zahlen nachgerechnet, alle Zeilenangaben geprüft.*
