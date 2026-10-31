# Spieltest-Befund 31.10.2026 — was die Simulation wirklich zeigt

**Anlass:** Zwei Läufe von `deepseek-v4-pro` sollten das Spiel bewerten (`BEFUND_SPIELTEST_GROSSES_MODELL*.md`).
Beide kamen zum Schluss „Engstelle Gold, Spieler steckt fest“. **Dieser Befund ist falsch — und zwar aus
drei Gründen, die alle in MEINEM Messwerkzeug lagen, nicht im Spiel.** Diese Datei hält den Beweis fest,
damit niemand die Modellantworten als Fehlerbericht ins Projekt trägt.

## 1. Was am Spiel nachgemessen stimmt (Kette funktioniert)

Probe mit `spielschicht` (Karte `original-036`, Saat 7), Ausgabe wörtlich:

```
holzfaeller auf wald (Feld 0): True -> Holzfäller auf Wald: 4 Holz/Stunde
bibliothek auf grasland (Feld 64): True -> Bibliothek auf Grasland (belegte Standortregel).
Forschung Baukunst: True -> Forschung Baukunst Stufe 1 gestartet (1 h, Kosten {'holz': 50})
goldmine auf berg (Feld 12): True -> Goldmine auf Berg: 3 Gold/Stunde
farm auf grasland (Feld 73): True -> Farm auf Grasland: 4 Nahrung/Stunde
kriegerakademie auf huegel (Feld 19): True -> Kriegerakademie auf Hügel (belegte Standortregel)
Bauten: {'0': 'holzfaeller', '1': 'holzfaeller', '64': 'bibliothek', '12': 'goldmine',
         '73': 'farm', '19': 'kriegerakademie'}
```

Die Kette **Holzfäller → Bibliothek → Forschung „Baukunst“ → Goldmine/Farm/Kriegerakademie** läuft.
Ein Spieler, der auf das Gelände achtet, kommt an Gold. Die Karte hat genug passende Felder
(11 Grasland, 18 Steppe, 13 Berg, 12 Hügel).

## 2. Drei Fehler im Messwerkzeug (alle behoben, `tools/spieltest_simulation.py`)

| Nr | Fehler | Wirkung im Lauf | Behebung |
|---|---|---|---|
| 1 | Bauliste enthielt **keine Goldmine und keine Ausbildungsstätte** | Gold blieb 0, kein Kampf — sah wie ein Spielfehler aus | Goldmine + Kriegerakademie in die Reihenfolge |
| 2 | Gebäude-Kennungen sind **ohne Umlaut** (`holzfaeller`), verglichen wurde mit `holzfäller` | Zähler „höchstens 2 je Gebäude“ traf nie → 10× Holzfäller | Vergleich über `gelaende.finde_gebaeude` |
| 3 | `gelaende.bau_moeglich` liefert ein **Tupel** `(erlaubt, Grund)`; `if bau_moeglich(...)` ist darum **immer wahr** | jedes Gebäude landete auf Feld 0 im Wald, alle Bauten scheiterten | Tupel auspacken und `ergebnis[0]` prüfen |

Nach den Behebungen (8 Spieltage): **12 Gebäude**, Gold 1.131, Nahrung 1.614, Forschung 51 Punkte,
Gesamtpunkte 25 — die Wirtschaft läuft.

## 3. Was jetzt noch NICHT passiert: keine Einheit

Auch mit Gold und Akademie entstehen **keine Einheiten**. Grund (im Code nachgesehen):
`spieloekonomie.ausbildung_start` verlangt neben Gold und Siedlern die **Ausrüstung im Warenlager**
(`ausruestung.fehlende(...)`), also Kurzschwert/Lederrüstung aus der Werkstatt — und die Werkstatt
braucht ihre eigene Kette (Metall, Gerberei, Forschung). Das ist **kein Fehler**, sondern die
belegte Produktionskette; es heißt aber: **bis zum ersten Kämpfer ist der Weg lang**, und genau das
ist eine echte Spielbarkeitsfrage für Daniel (nicht für das Modell).

## 4. Wie die beiden Modellantworten zu lesen sind

* Beide beschreiben **die Folgen meines kaputten Verlaufs**, nicht Fehler des Spiels.
* Ihre Vorschläge (Startgold 200, billigere Goldmine, Tutorial, Starteinheiten) sind **Design-Wünsche**,
  keine Bugfixes. Sie bleiben diskutabel — aber die Begründung „Gold ist nicht erreichbar“ trägt nicht.
* Beide haben dasselbe getan wie ein guter Prüfer: sie haben die **eine offene Frage** gestellt
  („Fehler der Politik oder fehlende Bauoptionen?“). Die Antwort steht oben: die Politik.

**Kosten der beiden Fehlläufe:** 0,0275 + 0,0289 = **0,0564 USD** — verbucht, kein Schaden am Code.

## 5. Nächster Schritt

Simulation mit dem korrigierten Werkzeug erneut laufen lassen und **erst dann** ein Modell fragen —
sonst bezahlt man eine Bewertung, die auf einem Artefakt beruht.
