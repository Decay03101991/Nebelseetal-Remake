# Prompt-Paket für die großen Modelle — Stand 31.10.2026, 04:30

**Zweck:** Alles, was vor dem Abgeben der Prompts feststehen muss, an EINER Stelle — welche Pakete es
gibt, was sie kosten, was sie beantworten, in welcher Reihenfolge sie laufen und was mit der Antwort
passiert. **Kein Prompt ist verschickt.** Daniel gibt frei.

---

## 1. Übersicht: fünf Pakete, gemessene Größen

| # | Paket | Datei | Umfang | Prompt-Token | Kosten je Lauf* | Beantwortet |
|---|---|---|---|---|---|---|
| A1 | Kampf: Quelle je Schritt + gestaffelte Beute | `docs/audits/auftraege/A1_kampfmodell.md` | 41.066 Zeichen | ≈ 11.700 | **0,037 USD** | E1, E4 |
| A2 | Wegzeit, Auftragskosten, Dimensionen als Ländereien | `docs/audits/auftraege/A2_wegzeit.md` | 20.749 Zeichen | ≈ 5.900 | **0,034 USD** | E2, E5 (Portal) |
| A3 | Spielbarkeit bei ×180 + Bewertung statt Sieg | `docs/audits/auftraege/A3_spielbarkeit.md` | 43.448 Zeichen | ≈ 12.400 | **0,038 USD** | E5 (Sieg/Auszeichnungen) |
| A4 | Antrieb ohne Mitspieler + Legende aus Originaltexten | `docs/audits/auftraege/A4_einzelspieler.md` | 43.513 Zeichen | ≈ 12.400 | **0,038 USD** | Spielgefühl, Geschichte |
| X | **Externe Gegenprüfung (ChatGPT, Abo)** | `docs/audits/AUFTRAG_EXTERNE_PRUEFUNG_20261031.md` + Kopie auf dem Desktop | 43.764 Zeichen | — | **0,– (Abo)** | Unabhängige zweite Meinung |

\* gerechnet mit 0,66 USD/Mio Prompt und 1,98 USD/Mio Antwort (gemessene DeepSeek-Preise),
angenommen 15.000 Antwort-Token. **Summe A1–A4: ≈ 0,147 USD** von den neu freigegebenen **3 EUR**.

**Warum so geschnitten:** Ein Gesamtdossier über alles kostet 129.370 Zeichen ≈ 37.000 Prompt-Token
(gemessen mit `tools/gesamtaudit_dossier_bauen.py`) und liefert allgemeine Antworten. Jedes Paket
bekommt nur seinen Ausschnitt (20.000–43.000 Zeichen) **plus Rechenpflicht** plus festes
Ausgabeformat — das ist derselbe Betrag pro Lauf wie ein Bruchteil des Gesamtdossiers, aber
verwertbar.

---

## 2. Was in jedem Paket steckt (und was bewusst NICHT)

Jedes Paket enthält:
* **Rahmen und Vorgaben** (Rolle, „neueste Fassung ist das Original", „Mechanik alt + Zahlen neu",
  Daniels Entscheidungen, Belegpflicht, Spieluhr ×180).
* **Nur seine Quellen** (Handbuchzeilen, Vorversion 2006, Forum-Original, Code-Auszüge, Datentabellen).
* **Den Umsetzungsstand vom 31.10.** — was bereits gebaut und geprüft ist, damit das Modell **prüft
  statt zu erfinden**.
* **Ein Ausgabeformat mit Obergrenze** (Tabellen, höchstens N Zeilen, je Aussage Quelle oder
  VORSCHLAG).

Nicht enthalten (bewusst, kostet nur Kontext): der gesamte Quellcode (20.772 Zeilen), UI-Diskussionen,
das Prüfregister komplett (nur in X als Kurzliste), Chatverläufe.

---

## 3. Ablauf (verbindlich)

```bash
# 1. Paket prüfen (Zahlen stehen oben, Datei liegt fest)
python -X utf8 tools/gesamtaudit_schnitte_bauen.py     # baut/aktualisiert alle vier Pakete

# 2. EIN Lauf, Ergebnis in eine eigene Datei, Kosten werden gemessen
python -X utf8 tools/gesamtaudit_lauf.py \
  --auftrag docs/audits/auftraege/A2_wegzeit.md \
  --ziel    docs/audits/BEFUND_A2_WEGZEIT_20261031.md

# 3. Ergebnis prüfen: > 0 Zeichen, Tabellen vorhanden, Kosten aus
#    D:\Arbeiten\Hermes\Kosten\usage_gesamtaudit_*.json ablesen und hier eintragen
```

**Reihenfolge:** **A2 zuerst** (hängt an keiner anderen Entscheidung, blockiert die Bewegung),
dann **A1** (Beute fließt in A1 ein), dann **A3** (setzt die Zahlen aus A2 voraus), zuletzt **A4**
(Spielgefühl/Geschichte, unabhängig).

**Harte Regeln für jeden Lauf:**
* `max_tokens` **48.000** (bei 16.000 ging alles im Nachdenken verloren → 0 Zeichen, 0,034 USD verbrannt).
* **Stillstandsschwelle** 240 s statt festem Timeout (große Modelle dürfen lange denken).
* **Antwortlänge > 0 prüfen** — sonst war es nur Nachdenken.
* **Einen Lauf nicht abbrechen, solange er denkt.**

---

## 4. Was mit den Antworten passiert

| Antwort | Weg |
|---|---|
| **WIDERSPRUCH / FEHLT / ERFUNDEN** mit Datei:Zeile | wird Prüfung in `tests/` + Änderung; Registerpunkt fortschreiben |
| **ZUSAMMENFÜHRUNG** (Mechanik alt + Zahlen neu) | wird als solches im Register markiert, nicht als Original verkauft |
| **VORSCHLAG** | geht Daniel zur Entscheidung, dann als VORSCHLAG im Code gekennzeichnet |
| **Nicht belegbar** | bleibt offen, wird nicht geraten |

Kein Modell darf Code schreiben — es liefert Papiere, gebaut und geprüft wird hier.

---

## 5. Stand der Umsetzung (was die Pakete schon einrechnen)

| Entscheidung | Stand 31.10., 04:30 |
|---|---|
| E2 Reiseformel Faktor 2 | **gebaut**: `auftraege.SEKUNDEN_JE_FELD = 7200` · `test_auftraege` 111/0/1 |
| E4 gestaffelte Beute | **gebaut**: `kampfbericht.beute_staffel` (10/30/60/100 %) · `test_beute_staffel` 18/0/1 |
| Götterschutz bis 299 Punkte | **als Funktion gebaut**: `punkte.angreifbar`, `punkte.goetterschutz_band` · `test_goetterschutz_band` 23/0/1 · **Verdrahtung in die Bot-Angriffe fehlt** |
| E5 kein Sieg / Bewertung | offen: `punkte.VORSCHLAG_ZIEL_PUNKTE = 300` steht noch im Code |
| E5 Dimensionen als Ländereien | offen (Datenmodell unverändert) |
| E3 ein Bewegungssystem | offen: Altpfad `_welt_bewegen` (main.py Z. 5690) läuft noch neben `auftraege.py` |
| Bot-Pfad Beute | **gebaut**: der Bot-Angriff bucht jetzt `kampfbericht.beute_staffel` (main.py, Zweig „angreifen") |
| Bot-Punkte | **erfunden**: `bot.punkte = rng.randint(0,300)` (`botkern.py` Z. 150) → Rangliste/Bewertung gegen Bots ist Zufall (Register 46) |

**Regression nach diesen Umbauten:** 9 berührte Prüfdateien **9/9 grün, 504 Prüfungen, 0 Fehler, 52 s**;
**vollständiger Lauf FINAL: 94 Dateien, 93 grün, 0 rot, 1 ausgesetzt, 3.504 Prüfungen, 511 s**
(`docs/audits/sammellauf_20261031_0425.log`).

---

## 6. Was Daniel noch entscheiden sollte, bevor die Pakete laufen

1. **Reihenfolge freigeben** (Empfehlung: A2 → A1 → A3 → A4).
2. **Budget:** 3 EUR freigegeben, geplant ≈ 0,15 USD für alle vier. Obergrenze im Skript: Stillstand +
   Längenprüfung; ein Abbruch kostet nur den Prompt-Anteil.
3. **X (ChatGPT)**: braucht die öffentlichen Pfade — Stand liegt im Branch `stand-20261031`. Wenn du
   willst, zuerst den Branch als Pull Request nach `main` ziehen, damit die Pfade auf `main` stimmen.

*Alle Zahlen in §1 sind gemessen (`tools/gesamtaudit_schnitte_bauen.py` druckt Zeichen, Token und
USD je Paket), nicht geschätzt.*
