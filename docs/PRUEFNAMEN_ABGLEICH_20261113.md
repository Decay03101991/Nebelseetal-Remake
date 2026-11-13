# PRUEFNAMEN-ABGLEICH DER VIER STREICHKANDIDATEN (F-74)

**Auftrag:** Daniel, 12.11.2026 (F-74, Register 568), woertlich: „Nichts loeschen — erst
Pruefnamen-Abgleich je Datei“. Die Regel, die daraus folgt: **eine Datei darf nur dann gestrichen
werden, wenn die neue Datei mindestens 90 Prozent ihrer Pruefnamen abdeckt.**

**Grundlage:** `docs/auftraege/PAKET_15B_PRUEFDATEIEN_20261112.csv` (Spalte `src_module`) fuer die
Partnerwahl, der Quelltext der Dateien fuer die Pruefnamen selbst.

**Zwei Masse, beide gemessen:**
1. **Woertlich** — derselbe Pruefname steht in der neuen Datei (exakte Zeichenkette).
2. **Inhaltlich** — ein Pruefname der neuen Datei beschreibt dasselbe (Wortueberschneidung der
   Pruefnamen mindestens 0,7 nach Jaccard). Das zweite Mass ist das fairere: zwei Dateien pruefen
   selten mit demselben Satz.

---

## 1. Die vier Kandidaten und ihre Partner

| Kandidat | Pruefnamen | bester Partner (Pruefungen) | woertlich | inhaltlich | 90-Prozent-Regel |
|---|---|---|---|---|---|
| `test_ressourcenleiste` | 42 | `test_ressourcenleiste_t08` (70) | 0 von 42 | **4 von 42 = 9,5 %** | **NICHT erfuellt** |
| `test_ansicht_hintergrund` | 71 | `test_gebaeude_icons` (32) | 0 von 71 | 0 von 71 = 0 % | **NICHT erfuellt** |
| `test_bot_wappen` | 22 | `test_bot_welten` (24) | 0 von 22 | 0 von 22 = 0 % | **NICHT erfuellt** |
| `test_dorfzentrum_ist_lager` | 79 | `test_dorfzentrum_ansicht` (44) | 0 von 79 | 0 von 79 = 0 % | **NICHT erfuellt** |

**Ergebnis: keine der vier Dateien darf gestrichen werden.** Es wurde nichts geloescht.

---

## 2. Was die Zahlen bedeuten

**`test_ressourcenleiste` (9,5 Prozent) ist der einzige echte Nachfolgefall.** `test_ressourcenleiste_t08`
ist die T08-Fassung mit 70 Pruefungen und prueft denselben Gegenstand (Ressourcenleiste, Anzeige,
Rundung). Aber sie deckt nur vier der 42 alten Namen inhaltlich ab — die alte Datei prueft Dinge, die
T08 nicht mehr prueft (oder anders herum). **Vor einem Streichen muessten diese vier Namen einzeln
uebertragen und die restlichen 38 gesichtet werden.** Das ist Arbeit, nicht ein Loeschvorgang.

**Die anderen drei haben inhaltlich `null` Deckung.** Das heisst nicht, dass die Partner schlecht
sind — es heisst, dass sie **einen anderen Gegenstand** pruefen:
- `test_ansicht_hintergrund` prueft die gemalten Ansichts-Hintergruende (Panorama, Schleier, 1:1-
  Schnitt, Kastenoptik). `test_gebaeude_icons` prueft Menue-Icons. Aehnliche Module, anderer Zweck.
- `test_bot_wappen` prueft die Wappen der fuenf Bots. `test_bot_welten` prueft die Bot-Welten.
- `test_dorfzentrum_ist_lager` prueft die Entscheidung S-2c (Dorfzentrum IST das Lager: Kennung
  `lager`, `max_je_siedlung` 1, nicht abreissbar, eine Ansicht). Die neuen Dorfzentrum-Wachen pruefen
  Masse und Aufbau — **nicht** diese Entscheidung. Sie ist damit nicht ersetzbar, sondern ergaenzt.

---

## 3. Was heute schon mit zwei dieser Dateien geschehen ist

Zwei der vier Kandidaten sind am 13.11.2026 **angefasst** worden, weil der Dorfzentrum-Umbau (Nr. 16
Teil A) ihre Aussagen beruehrt hat. Beide Aenderungen stehen mit Begruendung im Kopf der Datei:

| Datei | Aenderung | Wache danach |
|---|---|---|
| `test_ansicht_hintergrund` | Die Widgetzahl im Dorfzentrum wird rekursiv gezaehlt (die Spalte liegt jetzt in einer Leinwand). Inhalt unveraendert. | **81/0/0** |
| `test_dorfzentrum_ist_lager` | Drei Quelltextwachen zeigen jetzt auf `_dz_lager` statt auf `_render_storage`; die Entscheidung D-07 (EINE Lageransicht) wird als „beide Wege benutzen dieselbe Rasterfunktion“ geprueft. Inhalt unveraendert. | **82/0/0** |

**Beide Dateien sind damit gruen und aktuell** — sie sind heute kein Streichkandidat mehr, sondern
eine gepflegte Wache.

---

## 4. Befund: die 90-Prozent-Regel ist mit freien Pruefnamen kaum erfuellbar

Das ist der eigentliche Fund dieses Abgleichs. Pruefnamen sind **freie deutsche Saetze**
(„die Kachel ist 118 px breit“, „das Dorfzentrum ruft die Lagerverwaltung auf“). Zwei Dateien, die
denselben Gegenstand pruefen, formulieren ihn fast immer anders. Woertlich sind es deshalb **0 Prozent**
— und auch inhaltlich bleibt es bei 0 bis 10 Prozent.

Damit ist die Regel in ihrer jetzigen Form **kein Mass fuer Doppelung, sondern ein Mass fuer
gleiche Formulierung**. Sie schuetzt zuverlaessig davor, versehentlich zu loeschen — sie erlaubt aber
auch nie eine Loeschung, auch wenn inhaltlich alles doppelt waere.

**Vorschlag (Frage F-83 unten):** den Abgleich zusaetzlich auf den **geprueften Gegenstand** stuetzen —
je Pruefname eine Zuordnung zu einer Funktion oder einem Datenfeld (aus `PRUEF_BETRIFFT` und dem
Quelltext lesbar), und die 90 Prozent auf diese Zuordnung rechnen. Dann misst die Regel Doppelung
statt Wortlaut.

---

## 5. Fragen an Daniel (Sammelrunde, eine Runde)

- **F-83:** Soll der Pruefnamen-Abgleich auf den **geprueften Gegenstand** umgestellt werden (Funktion
  oder Datenfeld je Pruefname), statt auf den Wortlaut? Vorschlag: ja — sonst ist die 90-Prozent-Regel
  nie erfuellbar, wie die vier Messungen oben zeigen.
- **F-84:** `test_ressourcenleiste` ist der einzige Fall mit echter Naehe (9,5 Prozent, Nachfolger
  `test_ressourcenleiste_t08` mit 70 Pruefungen). Soll ich die 42 Pruefnamen einzeln sichten und die
  fehlenden vier bis zehn in T08 uebertragen — ohne die alte Datei zu loeschen?
- **F-85:** Sollen `test_ansicht_hintergrund`, `test_bot_wappen` und `test_dorfzentrum_ist_lager`
  endgueltig von der Streichliste genommen werden? Nach dieser Messung pruefen sie eigenstaendige
  Gegenstaende, die keine andere Datei abdeckt.


---

## 6. Die Antworten von Daniel (13.11.2026) und was daraus folgt

| Frage | Antwort (Wortlaut) | Stand |
|---|---|---|
| **F-83** | „Ja — zusätzlich auf den geprüften Gegenstand stützen (Funktion oder Datenfeld je Prüfname), 90 % darauf rechnen“ | Werkzeug wird gebaut (Sitzung 44) |
| **F-84** | „Ja, sichten — alte Datei bleibt“ | Sichtungsdokument folgt, Datei bleibt |
| **F-85** | „Ja, alle drei von der Liste nehmen — die Dateien bleiben“ | **erledigt, siehe 6.1** |

### 6.1 Drei Kandidaten sind von der Streichliste genommen (F-85, Register 594)

**Gestrichen von der Liste, Dateien unangetastet:**

| Datei | Pruefungen | Warum sie bleibt |
|---|---|---|
| `test_ansicht_hintergrund` | 71 | Panorama, Schleier und Kastenoptik — Deckung 0 %, keine andere Datei prueft das |
| `test_bot_wappen` | 22 | Wappen der fuenf Bots — Deckung 0 %, eigener Gegenstand |
| `test_dorfzentrum_ist_lager` | 79 | Entscheidung S-2c — Deckung 0 %, eigener Gegenstand |

**Auf der Liste bleibt allein `test_ressourcenleiste`** (42 Pruefnamen, Nachfolger
`test_ressourcenleiste_t08`, inhaltlich 4 von 42 = 9,5 %). Sie wird mit F-84 gesichtet, nicht
gestrichen.

**Was ausdruecklich NICHT geaendert wurde:** `docs/auftraege/PAKET_15B_PRUEFDATEIEN_20261112.csv` ist
eine Messung vom 12.11.2026 (39 Streichkandidaten nach Laufzeit) und bleibt als Beleg stehen — die
Liste, die hier fortgeschrieben wird, ist die inhaltliche aus diesem Dokument, nicht die nach Dauer.


---

## 7. Der Abgleich auf den GEGENSTAND ist gebaut (F-83, Register 595)

**Werkzeug:** `tools/pruefnamen_abgleich.py` (neu, 13.11.2026). Es liest je Pruefdatei jede
Zusicherung (`check`, `ok`, `ck`, `hcheck`, `assert`) und sammelt **die Bezeichner, die in der
Bedingung wirklich gelesen werden** — Funktionen und Datenfelder wie `spieloekonomie.WARENREZEPTE`
oder `main.rueckmarsch_eintrag`. Zwei Pruefungen gelten als deckungsgleich, wenn sich diese Mengen
mit **Jaccard ab 0,6** ueberschneiden. Ausgegeben werden beide Masse: Wortlaut und Gegenstand.

```
python -X utf8 tools/pruefnamen_abgleich.py <kandidat> <partner> [--jaccard 0.6] [--schwelle 90] [--json]
```
Rueckgabe 0 = Schwelle auf den Gegenstand erreicht, 1 = nicht erreicht (so kann die Regel maschinell
geprueft werden statt von Hand).

**Neue Zahlen (gemessen, `docs/audits/pruefnamen_gegenstand_20261113.json`):**

| Kandidat | Pruefungen | Wortlaut | **Gegenstand** | Partner | 90 % |
|---|---|---|---|---|---|
| `test_ressourcenleiste` | 42 | 0,0 % | **21,4 % (9)** | `test_ressourcenleiste_t08` | nicht erreicht |
| `test_ansicht_hintergrund` | 71 | 0,0 % | **0,0 %** | `test_gebaeude_icons` | nicht erreicht |
| `test_bot_wappen` | 22 | 0,0 % | **22,7 % (5)** | `test_bot_welten` | nicht erreicht |
| `test_dorfzentrum_ist_lager` | 82 | 0,0 % | **0,0 %** | `test_dorfzentrum_ansicht` | nicht erreicht |

**Was das aendert:** die inhaltliche Messung (Wortueberschneidung) hatte `test_ressourcenleiste` bei
9,5 % und die drei anderen bei 0 % gesehen. Auf den Gegenstand gerechnet steigen zwei Kandidaten
(21,4 % und 22,7 %) — die Schwelle von 90 % erreicht aber **keiner**. Damit ist die Streichung
weiterhin nicht belegt; die drei eigenstaendigen Dateien sind von der Liste genommen (Abschnitt 6.1),
`test_ressourcenleiste` ist gesichtet (F-84, `docs/SICHTUNG_PRUEFNAMEN_RESSOURCENLEISTE_20261113.md`).
