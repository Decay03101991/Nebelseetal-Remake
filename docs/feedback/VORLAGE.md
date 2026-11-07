# Feedback-Vorlage - was Daniel meldet und wie es gemessen wird

Ablauf Schritt 9 (B-2). Zweck: ein Gefuehl ist ein Befund, aber erst eine Zahl ist ein Auftrag.
Die Vorlage macht aus "das fuehlt sich falsch an" eine Zeile, die man nachfahren kann.

## So wird gemeldet

In `docs/feedback/MELDUNGEN.json` kommt je Beobachtung ein Eintrag mit **fuenf Feldern**:

| Feld | Bedeutung | Beispiel |
|---|---|---|
| `was` | der Schluessel - kurz, in denselben Worten wie beim letzten Mal (gleicher Schluessel = dasselbe Thema) | `"zu wenig Holz am Anfang"` |
| `wann` | Spieltag und Uhrzeit der Beobachtung | `"Spieltag 2, 14:30"` |
| `stand` | Version und Kopf-Commit, damit die Meldung zuordenbar bleibt | `"V 0.0.3, ef57bf1"` |
| `zahl` | was auf dem Schirm stand (Bestand, Dauer, Anzahl) - **keine Schaetzung** | `"Holz 12, Zimmermann grau"` |
| `gefuehl` | 1 bis 5 (1 = stoert sehr, 5 = passt) | `2` |

```json
{
  "meldungen": [
    {"was": "zu wenig Holz am Anfang", "wann": "Spieltag 2, 14:30",
     "stand": "V 0.0.3, ef57bf1", "zahl": "Holz 12", "gefuehl": 2}
  ]
}
```

## Was daraus wird

```
.venv/Scripts/python.exe -X utf8 tools/balance_kreis.py --feedback
```

Das schreibt `docs/feedback/BUENDEL.md`: je Schluessel die Anzahl der Meldungen, den
Gefuehlsdurchschnitt und ob daraus ein **Messauftrag** wird.

- **Ab 3 Meldungen mit demselben Schluessel** wird ein Messauftrag daraus - unabhaengig davon,
  wie gut die Kennzahlen aussehen. Ein Tester-Buendel sticht eine reine Kennzahl.
- **Unter 3 Meldungen** bleibt es eine Einzelbeobachtung: sie steht im Buendel, aber niemand
  baut dafuer etwas um.
- **Was der Agent nicht tut:** er entscheidet nicht, was eine Meldung bedeutet. Er bündelt,
  misst (Regelkreis) und legt das Ergebnis als `docs/balancing/URTEIL_<n>.md` vor. Annehmen
  oder ablehnen entscheidet Daniel.

## Warum das Gefuehl mitgezaehlt wird

Der Regelkreis kalibriert auf das Automatenspiel, nicht auf Menschen. Eine Zahl kann sich
verbessern, waehrend sich das Spiel schlechter anfuehlt. Deshalb steht neben jeder Kennzahl die
Gefuehlszahl der Meldungen, und bei Widerspruch (Kennzahl besser, Gefuehl schlechter) gilt der
Mensch - das steht als Risiko in `docs/ABLAUF_LLM_20261106.md`, Abschnitt 9.
