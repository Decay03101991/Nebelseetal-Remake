# PRÜFVERMERK: Herkunft und Grenze der Datei `GESAMTAUDIT_BEFUNDE_20261031.md`

**Stand:** 10.11.2026, 09:56. **Gegenstand:** `docs/audits/GESAMTAUDIT_BEFUNDE_20261031.md`, 4.206 Byte,
mtime 09.11.2026, 23:55.
**Entscheidung Daniels:** 10.11.2026, „ok nach Empfehlung“ — die Datei wird als Beleg aufgehoben, nicht
verworfen (Register 366).

**Zweck:** Dieser Vermerk sagt, was in dem Befundpapier brauchbar ist und was nicht. Er ersetzt keinen Lauf
und keine Prüfung; er verhindert nur, dass ein abgebrochenes Papier später für ein vollständiges Audit
gehalten wird.

## 1. Wie das Papier entstanden ist

Am 09.11.2026 gegen 23:53 wurde `tools/gesamtaudit_lauf.py` mit `--help` aufgerufen, um die Aufrufzeile zu
lesen. Das Werkzeug kennt kein `--help`: es startete sofort den bezahlten Aufruf an deepseek-v4-pro
(Prompt 132.205 Zeichen, rund 37.773 Token, `max_tokens` 48.000). Der Lauf wurde nach rund zwei Minuten
beendet, weil die Ausgabe durch `head` lief und die Leitung schloss. Offen benannt in
`docs/PRUEFREGEL_ORIGINAL.md`, Register 363.

## 2. Was brauchbar ist

Zwölf vollständige Befundzeilen, Nr 1 bis 12, je mit Mechanik, CODE-BELEG, QUELL-BELEG, Urteil, Empfehlung
und Aufwand. Am 10.11.2026 nachgesehen: die Tabelle ist vollständig, jede Zeile hat alle sieben Spalten.

**Grenze dieser Zeilen:** sie sind die Selbstauskunft eines Modells und **nicht** am Code nachgeprüft.
Urteile wie DOPPELT, WIDERSPRUCH oder FEHLT sind Behauptungen des Modells, keine Messung dieser Sitzung.
Wer eine Zeile verwendet, prüft sie vorher am Code — so, wie es Register 363 verlangt.

## 3. Was nicht brauchbar ist

Der Abschnitt „Nicht beurteilbar“ bricht mitten im dritten Punkt ab. Die letzte Zeile lautet:

```
- End-to-End-Balance (alle Kartentypen, Seeds,
```

Damit ist das Papier **kein vollständiges Gesamtaudit**: der Schluss fehlt, und ob das Modell noch weitere
Punkte nennen wollte, ist unbekannt. Ein vollständiger Lauf ist damit nicht ersetzt.

## 4. Folge

- Die Datei bleibt liegen, ist ab jetzt **versioniert** und wird nicht mehr als unversionierter Rest im
  Arbeitsbaum geführt.
- Kein Test liest sie; sie ist kein Teil des Sammellaufs.
- Die Textprüfung (`tests/test_textqualitaet.py`) nimmt sie aus, weil ihr Name mit `GESAMTAUDIT_` beginnt —
  rohe Modellantworten gelten dort als Belege.
- **Kosten:** der Aufruf ist im Tagessaldo von Register 365 enthalten und lässt sich aus zwei Ablesungen
  nicht herausrechnen; es wird keine Zahl behauptet.
