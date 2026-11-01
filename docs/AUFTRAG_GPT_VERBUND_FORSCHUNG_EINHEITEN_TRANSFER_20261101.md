# AUFTRAG 2 an das starke Chat-Modell — Verbund-Paket: Forschung, Einheiten, Dorftransfer

**Für:** Daniels großes GPT-Chat-Modell (Lesezugriff auf das öffentliche GitHub-Repo).
**Von:** Hermes (Weltenfresser), 01.11.2026. **Ergebnis:** EIN Markdown-Dokument, das Daniel zurückgibt.

## 0. Rolle, Grenze, Stand

Du bist **Entwerfer** für Spielregeln und Oberflächenabläufe, nicht Programmierer. Du lieferst ein
Papier mit **entscheidbaren Regeln und Randfällen**; ein anderer baut sie.

**Was seit dem letzten Auftrag gebaut ist** (damit du nicht Veraltetes vorschlägst):
- **S-1 fertig:** Jede Gründung setzt kostenlos Holzfäller (Wald), Steinmetz (Hügel/Berg) und Tempel
  (Nebelsee, sonst Steppe), je Stufe 1, ohne Siedlerkosten; die Meldung nennt Gelände, Feld und einen
  Ersatz, wenn das Wunschgelände fehlt. Der Tempel braucht dabei **keine** Baukunst, ein Nachbau schon.
- **S-2a fertig:** Der Menüpunkt „Karten“ ist weg, das Portal übernimmt; die Anzeige sagt
  **Weltkarte** und **Weltensprung** statt Dimension.
- Der Arbeitsstand liegt **lokal weiter als GitHub** (`main` dort = `954097aa` vom 31.10.). Jede
  Aussage über Code trägt Datei + Zeile **aus dem, was du wirklich gelesen hast**, sonst UNBEKANNT.

## 0a. Wer dein Papier umsetzt — und was das für dein Papier bedeutet

Umsetzer ist **Hermes mit dem Modell `deepseek-v4-flash`** (schnelles, kleines Modell), lokal auf
Windows, Projekt **Nebelseetal Remake**: Python 3.14 + tkinter, JSON-Spieldaten, kein Server, keine
Netzverbindung, kein Framework, Prüfstand mit **113 Prüfdateien** (ein voller Lauf dauert ~6 Minuten).
Jeder Schritt wird dort als **ein** Commit mit vollem Prüflauf und neu gebauter EXE abgeschlossen.

Daraus folgen für dich **harte Vorgaben** — ein Papier, das diese nicht einhält, ist für dieses Modell
nicht umsetzbar:

- **Entscheidbar statt diskutierbar:** eine Regel = ein Satz, der sich in Python ohne Auslegung prüfen
  lässt („wenn A und B, dann C, Meldung nennt Zahl X“). Keine „man könnte auch“-Passagen in den
  Regeln; Varianten nur dort, wo sie ausdrücklich zur Wahl stehen — mit **einer** Empfehlung.
- **Kein Rahmenwerk, keine neuen Abhängigkeiten:** nur Standardbibliothek (und höchstens das im
  Projekt vorhandene Pillow für Werkzeuge). Kein neues Datenbankschema, kein Migrationsplan für alte
  Spielstände (Daniel: Teststände dürfen brechen), kein Nebenläufigkeits- oder Cache-Design.
- **Kleine, getrennte Schritte:** jeder Teil muss in **einem** Arbeitsgang umsetzbar sein, mit eigener
  Prüfzusage. Ist ein Teil größer, zerlege ihn selbst in nummerierte Unterschritte.
- **Texte wörtlich liefern:** das Modell soll keine deutschen Sätze erfinden; jeder Spielertext kommt
  fertig aus deinem Papier, Platzhalter in {geschweiften Klammern}, keine vagen Wörter.
- **Ohne Fenster prüfbar:** jede Regel bekommt eine Zusage, die ohne Maus und Anzeige prüfbar ist
  (Werte rein, Werte raus). Was nur im Fenster sichtbar prüfbar ist, markierst du ausdrücklich so.
- **Knapp statt vollständig:** Tabellen, keine Wiederholungen, keine Zusammenfassung am Ende.

## 1. Die belegten Tatsachen (nichts davon raten, nichts davon ändern)

| Gegenstand | Stand (belegt) |
|---|---|
| Dörfer | **höchstens sechs je Spieler, global über alle Weltkarten**; jedes Dorf hat eine eigene 10 × 10 Karte und ein eigenes Ortslager |
| Ortslager | Rohstoffe und Waren liegen **im Dorf**, nicht in einer Reichskasse; die Reichsanzeige ist nur die Summe der Dörfer |
| Start je Dorf | 10 Siedler / 100 Holz / 100 Stein für das erste Dorf; die Kolonie bekommt ihr eigenes Startpaket |
| Bibliothek | **eine je Siedlung** (Handbuch 2009, S. 12); ohne Bibliothek ist die Forschung vor Ort **Stufe 0**; eine laufende Forschung sperrt die **ganze Siedlung** (Handbuch Z. 423-424) |
| Forschungsdauer | neue Stufe² in Stunden, Kosten verdoppeln sich je Stufe (Handbuch S. 12/13) |
| Forschung im Verbund | Ein Zweitdorf forscht **nicht** automatisch mit (M-4). Mit eigener Bibliothek **übernimmt es den Forschungsstand des Verbunds** und darf ihn durch eigenen Ausbau übertreffen; eine im Zweitdorf erledigte Forschung übernimmt das Hauptdorf automatisch („Ein Forschungsstand“) |
| Einheiten (M-5) | Ein Dorf stellt eine Einheit nur her, wenn **seine eigene Kriegerakademie-Stufe ≥ der im Verbund für diese Einheit erreichten Stufe** ist; **Stationieren ist überall frei** (M-6), auch für Einheiten, die das Dorf selbst nicht bauen kann; **stationierte Truppen verteidigen mit** |
| Transfer (M-9/M-10, Anhang 3) | **genau ein Dorf je Vorgang**; Einstieg ist ein **Klick auf ein freies Feld** der Weltkarte, dann Dorfauswahl aus denen mit genug Rohstoffen; **kein Koordinaten-Dropdown**; Kosten **Mana** (VORSCHLAG 500) plus „ein wenig Gold“ beim Weltensprung; **gesperrt, solange etwas unterwegs ist**; die Kosten holt ein **simulierter Trupp** ab (kurz, keine Zeit), **Postfach bestätigt** die neue Koordinate |
| Umzug mit Aufträgen | Das Dorf reist mit allem; **laufende Aufträge bekommen die neue Position**, ihr Weg wird neu gerechnet; bei zu weitem Wechsel **Warnung** vor überlangen Laufzeiten, die der Spieler bewusst in Kauf nimmt |
| Weltkarten | sechs Namen: Armageddon, Ragnarök, Utgard, Midgard, Valhalla, Limbus; bespielbar zuerst **Midgard** und **Valhalla**, Start in Midgard; 20 × 20 Felder |
| Bots | sechs, je ein Dorf, feste Position, **kein Angriff** in dieser Stufe |

## 2. Deine Aufgabe — vier Teile

### Teil 1 — Wo lebt der „Forschungsstand des Verbunds“?
Zwei Bauformen zur Wahl, mit Folgen, dann **eine Empfehlung**:
- **A) ein eigenes Feld im Spielstand** (`verbund_forschung`), das jede Bibliothek beim Bau übernimmt
  und das jede erledigte Forschung fortschreibt.
- **B) abgeleitet**: die Verbundsstufe je Gebiet ist immer das **Maximum** der Dorfstände.

Beantworte für deine Empfehlung: Was passiert beim **Abriss** der einzigen Bibliothek, die eine Stufe
trug? Beim **Laden** eines Altstands ohne das Feld? Bei **zwei** Bibliotheken, die dieselbe Forschung
gleichzeitig starten? Bei einer Forschung, die im Zweitdorf **höher** ist als im Hauptdorf? Wer darf
eine **teurere** Stufe bezahlen, wenn der Verbund sie schon hat?

### Teil 2 — S-3 Forschungsübernahme: die Regeln
Eine Tabelle mit **mindestens zwölf Randfällen**: je Zeile `Fall | Regel (was passiert) | Begründung |
Zusage für eine Prüfdatei`. Pflichtfälle: kein Dorf mit Bibliothek; Bibliothek gebaut, während im
Hauptdorf geforscht wird; Forschung startet im Dorf mit **niedrigerer** Bibliotheksstufe; Forschung
fertig, während das Dorf abgerissen/umgezogen wird; Spielstand laden; Dorf mit Bibliothek Stufe 0;
Forschung eines Gebiets, das der Verbund schon auf Stufe X hat; Kostenquelle (immer das Ortslager des
startenden Dorfes).

### Teil 3 — S-4 Einheitenregel: die Regeln
Tabelle mit **mindestens acht Randfällen** zum Satz `eigene Akademiestufe ≥ Verbundsstufe der
Einheit`: Dorf ohne Akademie; Akademie genau auf Verbundsstufe; Akademie eine Stufe **höher**;
Einheit, die im Verbund noch **nie** gebaut wurde; Stationieren einer fremden Einheit; stationierte
Truppen verteidigen; Meldungstext muss **beide Zahlen** nennen; Sonderfall Siedlerkarren/Kundschafter.
Nenne ausdrücklich, was **nicht** verlangt wird: keine Forschung, kein Gold im Reich, keine zweite
Kostenstelle.

### Teil 4 — S-6 Dorftransfer: der Ablauf
Ein **Schritt-für-Schritt-Ablauf** in der Reihenfolge, in der der Spieler klickt, mit allem, was die
Oberfläche zeigen muss und was den Vorgang sperrt: Feld wählen → welches Dorf (nur die mit genug
Rohstoffen) → Kostenanzeige → Bestätigung → Herold holt die Kosten → Postfach → neue Koordinate auf
der Karte → was mit laufenden Aufträgen passiert → welche Warnung wann erscheint → was passiert,
wenn mittendrin gesperrt wird (Auftrag gestartet, Götterschutz, zu wenig Mana, Ziel belegt).
Je Schritt: `Schritt | Was der Spieler sieht | Was der Kern prüft | Was NICHT passieren darf`.
Dazu die **Sperrliste** als Tabelle: `Sperre | Bedingung | Meldung (deutsch, mit Zahl)`.

## 3. Formregeln

- **Deutsch**, Tabellen, keine Emojis, **250–350 Zeilen**, kein Vorwort, kein Schlussgeplänkel.
- Jede Aussage mit Urteil: **BELEGT** (steht in Abschnitt 1) / **VORSCHLAG** (deine Empfehlung) /
  **UNBEKANNT** (fehlt — dann `UNBEKANNT — von Hermes zu liefern`, niemals eine Zahl erfinden).
- **Keine erfundenen Zahlen.** Wo eine Zahl fehlt (Transferkosten, Mana, Akademiestufen), schreib
  `UNBEKANNT` und nenne, wer sie liefert.
- Keine Codeblöcke, kein Pseudocode, keine Dateipfade erfinden.
- Abschnitte in dieser Reihenfolge: 1 Forschungsstand (Bauform + Empfehlung), 2 Regeln S-3,
  3 Regeln S-4, 4 Ablauf S-6, 5 Texte (Meldungen und Ablehnungen, je eine Zeile, **die Zahl steht im
  Satz**), 6 Prüfplan (je Regel eine Wache: Name + was sie zusichert + welche alte Wache dadurch rot
  wird), 7 Offene Fragen an Daniel (höchstens 8, Empfehlung zuerst), 8 Was ich nicht wissen kann.

## 4. Was Hermes mit dem Papier tut

Ich prüfe jede Regel gegen den echten Code und die belegten Handbuchstellen, entscheide, was in S-3,
S-4 und S-6 gebaut wird, und trage die Prüfzusagen als echte Wachen in `tests/` ein. Was du als
`UNBEKANNT` markierst, wird **nicht** gebaut, sondern Daniel vorgelegt.
