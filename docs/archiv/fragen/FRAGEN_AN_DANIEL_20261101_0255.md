# Fragen an Daniel — 01.11.2026, 02:57 (gesammelt, in EINEM Formular)

Diese vier Punkte standen in der Übergabe 02:02, Abschnitt 6. Sie sind hier gesammelt, weil Daniel
schläft; die **Empfehlung steht jeweils zuerst** und ist im Code bis zur Antwort als VORSCHLAG
gekennzeichnet. Kein Punkt blockiert die Arbeit.

## 1. Transferkosten: welche Währung?

* **A) Mana** — Empfehlung: der Tempel erzeugt Mana, der Reiseort ist der Tempel, damit schließt sich
  der Kreis. Die Höhe wird im Spieltest eingestellt (Daniels Antwort: Mana neu kalkulieren).
* B) Gold — dann konkurriert die Reise mit Gebäuden und Forschung um dasselbe Gut.
* C) Mana und Gold gemischt — zwei Engpässe gleichzeitig; teurer im Spieltest zu justieren.

## 2. Bot-Umfang

* **A) 2–3 Taktiken, 1–3 Dörfer je Bot** — Empfehlung: der Entwurf
  `docs/design/SPIELSPANNUNG_UND_BOTTAKTIK_20261101.md` ist genau darauf gerechnet (Rechenbudget,
  Sichtbarkeit, Prüfdateien). Sechs eigene Dörfer gegen sechs Bots bleibt auf dem Laptop flüssig.
* B) mehr Dörfer und Taktiken — mehr Rechenzeit und mehr Anzeige; erst nach einer Messung sinnvoll.
* C) Bots erst nur mit Koordinaten, Taktiken später — schnellster Weg, aber ohne Wirkung auf den
  Spieler (Daniels Kernwunsch bleibt offen).

## 3. Götterschutz-Dauer

* **A) so lassen wie im Code, nur anzeigen** — Empfehlung: der Schutz endet nach 7 Tagen oder dem
  ersten Kriegspunkt (`src/main.py`, `punkte.goetterschutz_tage`). Belegt, keine neue Zahl nötig.
  Reisen ist laut Daniels Antwort 2 erlaubt, sobald der Schutz verlassen ist.
* B) neu festlegen — dann ist es eine neue Zahl ohne Quelle, die im Spieltest justiert werden muss.
* C) abschaffen — dann reist man ab Tag 1, und der Aufbau verliert seinen Schutz.

## 4. Kartenziehung (alte Entscheidung 10: Wahl aus drei Karten)

* **A) nach dem Dorf-Umbau** — Empfehlung: die Kartenwahl hängt künftig an Mana, Bauplätzen und Lage
  im Limbus (Modell M-8). Solange der Dorf-Umbau läuft, würde die Ziehung zweimal umgebaut.
* B) davor — dann muss sie nach dem Umbau noch einmal angefasst werden.
* C) erst zur DEMO — spart jetzt Arbeit, verschiebt aber eine bereits entschiedene Mechanik.

## Zusatzbefund aus dieser Sitzung (keine Frage, nur Hinweis)

Der Entwurf des starken Modells nennt acht Widersprüche im Code, die vor dem Dorf-Umbau entschieden
werden sollten — die drei wichtigsten:

1. **Tempel ab Gründung gegen Baukunst:** `data/buildings.json` verlangt für den Tempel Baukunst;
   Daniels Entscheidung sagt, der Siedlungskarren bringt ihn mit. Auflösung nach Empfehlung:
   Ausnahme **nur** bei der Gründungssetzung, Nachbau verlangt weiter Baukunst.
2. **Mana-Erzeugung gegen Transferpreis:** 5 Mana/h am Nebelsee bedeuten 1.000 Stunden bis zu einem
   5.000-Mana-Transfer. Das ist der Grund, warum Mana neu kalkuliert werden muss (Daniels Antwort).
3. **Bots ohne Koordinaten:** jede Entfernung ist heute die Kartenmitte, also geschätzt. Das löst erst
   der Bot-Schnitt (S-7); bis dahin steht der Hinweis in jeder Auftragsmeldung.
