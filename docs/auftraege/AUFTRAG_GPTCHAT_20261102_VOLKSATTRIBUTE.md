# NEBELSEETAL REMAKE — AUFTRAG V-5 (UMSETZUNGSENTWURF FÜR VOLKSATTRIBUTE UND VERHALTENSBONI)

Stand: 02.11.2026, 15:05. Auftraggeber: Daniel. Paket: `AUFTRAG_GPTCHAT_20261102_VOLKSATTRIBUTE.zip`.

## WAS ICH BRAUCHE

Nebelseetal Remake ist ein lokales Einzelspieler-Remake eines Browserspiels (Python 3 + tkinter,
JSON-Spielstand, offline, kostenlos). Du spielst gegen **fünf Bots**. Jeder Bot hat eine **Fraktion**
und eine **Taktik**; für beide gibt es bereits Boni — aber sie stehen **nur als Text** in der
Oberfläche, sie **wirken nicht im Spiel**. Du lieferst den **Umsetzungsentwurf**, der sie wirkt:
welche Stellschraube, welche Formel, welche Wache.

Du lieferst **ein Dokument**. Du änderst keinen Code, behauptest keine Testläufe und erfindest keine
Zahl. Jede Zahl trägt ein Urteil: **BELEGT** (mit Quelle), **VORSCHLAG** (mit Begründung) oder
**NICHT BELEGT** (dann 0 setzen und fragen).

## DER AUFTRAG IN FÜNF TEILEN

A) **Wirkungsmodell** — welche Größe greift wo, additiv oder multiplikativ, welcher Deckel, was
   passiert bei Überschneidung (siehe unten: Silra und Krank bekommen zwei Boni auf dieselbe Größe).
B) **Verdrahtung je Effekt** — Datei, Funktion, Aufrufstelle. **EINE Lesestelle je Effekt** (im
   Projekt als F-04-Muster bekannt: Anzeige und Kern lesen dieselbe Funktion, sonst zeigt die
   Übersicht 5 %, während der Kern 0 % rechnet).
C) **Wachen** — je Effekt mindestens eine Prüfbedingung, Grenzfälle −1 / 0 / exakt Soll / +1, und
   eine **Gegenprobe** (eine absichtlich falsche Erwartung MUSS rot werden).
D) **Offene Entscheidungen** — Tabelle: Frage, Messlage, zwei bis drei Möglichkeiten MIT Folge,
   Empfehlung zuerst. Diese Entscheidungen gehören Daniel, nicht dir und nicht mir.
E) **Querwirkungen und Risiken** — was kippt das Balancing, was bricht bestehende Prüfungen, was
   ist mit dem Spieler (bekommt er auch Volksattribute?).

## IST-STAND (gemessen am Code, 02.11.2026)

**Volksattribute je Fraktion** — `src/bottaktik.py`, `VOLKSATTRIBUTE`, Zeilen 102–107.
Der Kommentar darüber sagt selbst: *die WIRKUNG auf Ertrag/Kampf/Reise ist hier NICHT verdrahtet*.

| Fraktion | Plus | Minus | Bots |
|---|---|---|---|
| menschlich | Holzertrag +5 % | Steinertrag −5 % | Haug, Brynhild |
| zwergisch | Steinertrag +5 % | Holzertrag −5 % | Grom |
| elfisch | Reisegeschwindigkeit +5 % | PA der Einheiten −5 % | Silra |
| monster | AT der Einheiten +5 % | Handelserlös −5 % | Krank |

**Taktikbonus je Bot** — `src/bottaktik.py`, `TAKTIKEN`, Feld `bonus` (Text, ebenfalls nicht verdrahtet):

| Bot | Taktikbonus |
|---|---|
| Haug | Beute +5 % |
| Brynhild | Verteidigung +5 % |
| Grom | Ausbau +5 % |
| Silra | Reisegeschwindigkeit +5 % |
| Krank | Angriff AT +5 % |

**Überschneidung, die du entscheiden musst:** Silra hat Reise +5 % aus dem Volk **und** +5 % aus der
Taktik; Krank hat AT +5 % **und** +5 %. Additiv wären das +10 %, multiplikativ +10,25 %, mit Deckel
weniger. Sag die Regel und begründe sie.

**Was schon existiert und benutzt werden muss (nichts davon neu bauen):**

- `bottaktik.volksattribute(bot)` (Zeile 115) liest die Fraktion aus `botkern.BOT_FRAKTIONEN` — die
  **eine** Quelle der Zuordnung Bot → Fraktion. Sie wird in `main.py` (Zeile 3042) einmalig gesetzt.
- `bottaktik.verhaltensbonus_aktiv(bot, jetzt)` (Zeile 126) ist gebaut und geprüft, wird aber von
  **keinem** Produktionscode aufgerufen (nur von `tests/test_s7_botverhalten.py`). Der befristete
  Bonus steht in `bot["verhaltensbonus"] = {"text": …, "bis": jetzt + 48 h}`.
- `bottaktik.offene_luecken()` (ab Zeile 515) benennt beide Lücken selbst — dort steht der VORSCHLAGStatus, den du ablösen sollst.

**Bekannte Stellschrauben im Kern (bitte im Paket nachprüfen, nicht blind übernehmen):**

| Wirkung | Stellschraube |
|---|---|
| Erträge (Holz, Stein, Nahrung, Leder) | `gelaende.ertrag_pro_stunde` liest `data/buildings.json`; Boni laufen über `forschung_wirkung` |
| Reisegeschwindigkeit | `auftraege` (Dauer = 2 · Distanz / Geschwindigkeit), Sekunden je Feld |
| AT / PA / SK | `einheiten.angriff`, `einheiten.verteidigung`, `einheiten.schlagkraft` |
| Kampf | `kampf.fuehre_schlacht` (genau EINE Kampffunktion), Wallvorrunde mit SK |
| Beute | `kampfbericht.beute_am_ziel` und `beute_staffel` (EINE Formel, deckelt auf Karrenladung) |
| Handel / Transport | `spieloekonomie.handel_start`, `transport_start`, `ladung_der_gruppe` |
| Verteidigung | `dorfwall.kennwerte`, Wallstufen im Kampf |
| Ausbau | `gebaeude_wirkung` (Stufe je Feld), `data/buildings.json` |

## REGELN, DIE NICHT VERHANDELBAR SIND

1. **Keine Zahl ohne Quelle.** Handbuch 2009 ist die Richtschnur, die 2006er Seiten zeigen die
   Entwicklung; was dort nicht steht, ist VORSCHLAG mit Rechnung.
2. **Eine Wahrheit je Größe.** Kein zweiter Rechenweg neben dem Kern; die Anzeige liest dieselbe
   Funktion wie die Buchung.
3. **Nichts löschen.** Abgelöste Fassungen und Belegzahlen bleiben stehen und werden als abgelöst
   gekennzeichnet.
4. **`main.py` hat ZWEI große Klassen** (`GameState` und `NebelseetalApp`). `self.state` gibt es nur
   in der App — ein Vorschlag, der das verwechselt, ist unbrauchbar.
5. **Code in `.py` ist ASCII** (ae/oe/ue/ss), nur Anzeigetexte dürfen Umlaute tragen.
6. **Keine erfundenen Prüfdateinamen.** Wenn du eine Wache vorschlägst, nenne die Zusicherung, nicht
   einen Dateinamen, den du nicht kennst — oder schreib UNBEKANNT.
7. **Sag, was du nicht weißt.** UNBEKANNT und UNGEPRÜFT sind erwünschte Antworten.

## ANTWORTFORMAT

Eine Datei `ENTWURF_VOLKSATTRIBUTE_20261102.md`, deutsch, Markdown, keine Emojis, Tabellen.
Reihenfolge: A, B (je Effekt eine Zeile in der Tabelle), C, D, E, dann ein Abschnitt
**Nicht beantwortet** mit allem, was du nicht belegen konntest.

Für Teil B ist das die Pflicht-Tabelle (13 Zeilen — jede Wirkung einzeln):

| # | Effekt | Stellschraube (Datei:Funktion) | Formel | Kern buchet | Anzeige liest | Wache | Urteil |
|---|---|---|---|---|---|---|---|

Für Teil D ist das die Pflicht-Tabelle:

| Frage | Messlage | Möglichkeit A (Folge) | Möglichkeit B (Folge) | Empfehlung |
|---|---|---|---|---|

## VERPACKUNG (hart)

- **Höchstens 8 MB je ZIP.** Größer ist nicht herunterladbar — dann teilen, nicht quetschen.
- Die Datei **direkt anhängen**. Ein Link auf eine Chat-Seite, ein `blob:`-Verweis oder ein
  Sandbox-Pfad (`/mnt/data/…`) ist keine Lieferung und wird nicht angenommen.
- Ein Lieferschein am Anfang der Antwort: Dateiname, Zeilenzahl, drei Kernaussagen in je einem Satz.
