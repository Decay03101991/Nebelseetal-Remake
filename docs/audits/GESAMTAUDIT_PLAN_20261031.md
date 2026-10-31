# Plan für den Gesamtaudit (starkes Modell) — gezielt statt „alles auf einmal“

**Stand:** 31.10.2026, 02:45 · `06aabcb` · **Auftrag Daniel:** „mindestens einmal ein großes Modell
unser Gesamtprojekt anschauen lassen … alles mit den Spiel bekannten Infos abgleichen — aber in einem
begrenzten Format, damit es keine unendlichen Kosten verursacht. Nicht unnötige Tokens verblasen,
sondern wirklich voranbringende Auswertungen und Wege für mich und das Spiel."

---

## 1. Warum NICHT ein großer Aufruf über alles

Gemessen, nicht geschätzt (Werkzeuge liegen im Projekt):

| Weg | Eingabe | Kosten | Urteil |
|---|---|---|---|
| **Dossier über das ganze Projekt** (`tools/gesamtaudit_dossier_bauen.py`) | **129.370 Zeichen ≈ 37.000 Prompt-Token** | 0,05–0,10 USD je Aufruf | als **Basis** gut, als Frage zu breit: ein Modell, das 40 Registerpunkte, 20 Gebäude, 28 Einheiten, 21 Forschungen und 13 Module gleichzeitig sieht, antwortet allgemein („prüft eure Quellen“) statt konkret |
| derselbe Lauf wurde am 31.10. um 02:36 gestartet und nach **15 s abgebrochen** | — | nur Prompt-Anteil, **kleiner einstelliger Cent-Betrag**, nicht gemessen | Daniel will keine generische Auswertung |

**Erkenntnis:** das Teure an diesen Läufen ist nicht die Antwort, sondern **Kontext, den das Modell
nicht braucht**. Jede Frage bekommt deshalb nur ihren **eigenen Ausschnitt** (10.000–25.000 Zeichen)
und einen **Auftrag mit Rechenpflicht** (Zahlen nachrechnen, nicht beschreiben).

Was **ich selbst** kostenlos und belegbar beantworte (dafür braucht es kein Modell):
Zeilennummern, Fundstellen, Teststand, Widersprüche zwischen Dateien, doppelte Systeme, „ist das schon
gebaut?“. Genau das ist in `docs/PRUEFUNG_ENTWURF_WEGZEIT_KAMPF_20261031.md` und
`docs/audits/BEWEGUNGSSYSTEME_LANDKARTE.md` bereits erledigt.

---

## 2. Die drei gezielten Audits (in dieser Reihenfolge)

Jedes Audit beantwortet **genau eine offene Entscheidung** aus dem Prüfbericht (§6) und liefert
Zahlen, die ich sofort in Code oder Dokument übernehmen kann.

### Audit 1 — Kampfmodell: welcher Teil kommt aus welcher Quelle? (→ Entscheidung E1)

* **Frage:** Das Projekt hat zwei Originalquellen für den Kampf (Handbuch 2009: LE/AT/PA/MU;
  neueres Forum-Original: Konstitution/Kampfwert/Rüstung/Erschöpfungsschwelle). Erstelle eine
  **eine** Regeltabelle, die für jeden Kampfschritt sagt, welche Quelle gilt und warum — und nenne
  die Stellen, an denen die beiden Quellen **unvereinbar** sind, mit der jeweils kleineren Änderung.
* **Ausschnitt:** `docs/quellen/Das_Kampfsystem_Neu_Original.odt` (Text, 6.759 Zeichen) +
  `docs/original/ORIGINAL_Kampf_und_Punkte.md` §2 (Kampf, ~4.000 Zeichen) + Handbuch
  Z. 1206–1338 (~5.000) + `kampf.py` `PROFILE` und `fuehre_schlacht`-Ablauf (~3.000) → **≈ 19.000 Zeichen**
* **Ausgabeformat:** Tabelle „Schritt | gilt | Quelle | Begründung“ (max. 14 Zeilen) + Liste
  „unvereinbar“ (max. 5) + 3 Sätze „was das für den Code bedeutet“.
* **Kosten:** ≈ 5.400 Prompt-Token + 12.000 Antwort-Token ≈ **0,03 USD**
* **Was ich damit tue:** E1 ist entschieden belegbar; danach Kampfteil des Entwurfs umschreiben.

### Audit 2 — Wegzeit, Auftragskosten und Portal-Mana als EIN Zahlensystem (→ E2, E4, E5)

* **Frage:** Baue aus den belegten Angaben (GS-Werte 5–35, „Dauer je Strecke“, Rückkehr doppelt,
  Drosselung in 10-%-Schritten, Gold/Nahrung-Kosten, Mana nach Entfernung, 5.000 Mana und 24 h für
  den Weltwechsel, Spieluhr ×180) **eine** Reiseformel und eine Kostentabelle und rechne drei
  Beispielreisen durch (nah 6 Felder, mittel 16, fern 32, je langsame und schnelle Einheit).
  Nenne für jede Zahl: belegt oder Vorschlag.
* **Ausschnitt:** Handbuch Z. 1103–1141 + Z. 1185–1194 + `portal.php.txt` (3.155) +
  `auftraege.py` Konstanten + `data/units.json` GS-Spalte + Produktionsraten aus
  `data/resources.json` → **≈ 16.000 Zeichen**
* **Ausgabeformat:** 1 Formel, 1 Kostentabelle (Gold/Nahrung/Mana je Einheit und Feld), 6
  Beispielzeilen mit Spielstunden **und** Echtzeit bei ×180, 3 offene Punkte.
* **Kosten:** ≈ 4.600 Prompt + 12.000 Antwort ≈ **0,03 USD**
* **Was ich damit tue:** E2/E5 werden zur Rechenaufgabe statt zur Geschmacksfrage; die Tabelle wird
  `data/` (nicht Code) und ist prüfbar.

### Audit 3 — Spielbarkeit der belegten Zahlen bei ×180 (→ E5, Siegbedingung)

* **Frage:** Prüfe die **belegten** Raten (Produktion je Gebäude und Gelände, Siedlerzuwachs 1/h,
  Forschungsdauer Stufe², Ausbildungszeiten, Punkte je Einheit, Wallstufe³) gegen die Spieluhr ×180
  und Daniels Ziel „eine Partie in überschaubarer Zeit“. Wo wird etwas trivial, wo unspielbar?
  Schlage die **kleinste** Änderung vor, die keine Originalzahl verändert (z. B. Zeitfaktor,
  Zielpunktzahl, Startbedingungen) — mit Rechnung.
* **Ausschnitt:** `data/resources.json` Erträge + `data/buildings.json` Erträge/Preise +
  `data/research.json` Kosten + `data/units.json` Punkte + Handbuch Punkte-/Schutzseiten +
  `src/punkte.py` Konstanten → **≈ 20.000 Zeichen**
* **Ausgabeformat:** Tabelle „Größe | belegter Wert | Wirkung bei ×180 | Urteil (spielbar/trivial/
  unspielbar)“ (max. 10 Zeilen) + 3 konkrete Stellschrauben mit Zahlen + 1 Empfehlung.
* **Kosten:** ≈ 5.700 Prompt + 12.000 Antwort ≈ **0,03 USD**
* **Was ich damit tue:** E5 (300 Punkte) wird mit Rechnung entschieden, nicht nach Gefühl.

**Gesamtbudget:** ≈ **0,09–0,12 USD** für alle drei, gemessen über `usage_*.json` in
`D:\Arbeiten\Hermes\Kosten\`. Obergrenze **0,20 USD**; wird sie erreicht, stoppt der Lauf (Stillstand
und Längenprüfung sind eingebaut). Daniels Freigabe für das starke Modell: **3 EUR**, verbraucht
bisher **≈ 0,07 USD**.

---

## 3. Werkzeuge, die dafür schon stehen

| Werkzeug | Zweck |
|---|---|
| `tools/gesamtaudit_dossier_bauen.py` | baut Dossier mit festem Zeichenbudget; druckt Token- und Kostenschätzung **vor** dem Aufruf |
| `tools/gesamtaudit_lauf.py` | EIN Aufruf, Streaming, Stillstandsschwelle 240 s, `max_tokens` 48.000, schreibt das Ergebnis **während** des Laufs, misst die Kosten in `usage_gesamtaudit_*.json` |
| `tools/sammellauf.py` | reproduzierbarer Prüflauf über ALLE Prüfdateien mit ehrlicher Zählung (RC **und** ERGEBNIS-Zeile) |

Für die drei gezielten Audits wird `gesamtaudit_lauf.py` je Frage mit **Ausschnitt statt Gesamtdossier**
aufgerufen (Option `--dossier <datei>` ist dafür noch zu ergänzen — kleine Änderung, kein Risiko).

---

## 4. Was ausdrücklich NICHT gefragt wird

* keine Datei-für-Datei-Code-Review (das macht `tools/sammellauf.py` + Prüfdateien),
* keine UI-Bewertung (dafür gibt es Bildschirmabgleiche und Daniels eigenes Urteil),
* keine Wiederholung von Registerpunkten 1–40 (die gelten als geprüft),
* keine Quellensuche im Netz (die Quellen liegen im Projekt),
* keine Änderung am Code durch das Modell — es liefert **Papiere**, ich baue und prüfe.

---

## 5. Reihenfolge und Abhängigkeit

1. **Audit 2 (Wegzeit/Kosten)** zuerst — es hängt an keiner anderen Entscheidung, und E2 blockiert
   jede Umsetzung von Bewegung.
2. **Audit 1 (Kampfmodell)** — braucht E3 (ein Bewegungssystem) nicht, aber die Beute-Regel aus A2
   fließt in A1 ein.
3. **Audit 3 (Spielbarkeit)** zuletzt — es setzt voraus, dass die Zahlen aus A2 als System stehen.

*Geschrieben 31.10.2026, 02:45. Alle Zahlen in §1 sind gemessen (`tools/gesamtaudit_dossier_bauen.py`
hat 129.370 Zeichen ausgegeben), nicht geschätzt.*
