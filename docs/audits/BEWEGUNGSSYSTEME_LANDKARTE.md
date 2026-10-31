# Landkarte der zwei Bewegungssysteme (`main.py`)

**Stand:** 31.10.2026, `06aabcb` · **Prüfer:** Hermes (neue Sitzung) · **Anlass:** Der Wegzeit-Entwurf
behauptete „`movements` ist heute immer leer“. Das ist falsch: es laufen **zwei** Bewegungssysteme
nebeneinander, mit **zwei Formeln, zwei Beuteregeln und zwei Kampfregeln**. Diese Karte hält jede
Stelle mit Zeilennummer fest, damit Daniel E3 entscheiden kann, ohne den Code zu lesen.

---

## System A — Aufträge/Missionen (`src/auftraege.py`, Paket W7)

Das ist der **vollständige, geprüfte** Weg. Er kennt Einheiten-Auswahl, GS, Karrenladung, Rückkehr,
Ankunft, Bericht und Kampf.

| Baustein | Stelle |
|---|---|
| Modul, Stand `2026-10-04.1` | `src/auftraege.py` Z. 44 |
| Liste der Missionen im Spielstand | `main.py` Z. 855 `self.auftraege = auftraege.neue_liste()` |
| Start (Prüfung von Art, Bestand, Karren, Verbot in fremden Siedlungen) | `auftraege.starten`, aufgerufen `main.py` Z. 1961 (Methode `auftrag_starten`, Z. 1939) |
| Reisezeit-Formel | `auftraege.reisezeit_sekunden` Z. 133–147: **`d / GS · 3600 s`**, also **1 Feld je GS-Punkt und Stunde** |
| Rückkehr | `HIN_UND_RUECK_FAKTOR = 2.0` Z. 55 (belegt: Handbuch S. 19) |
| Bindung an die langsamste Einheit | `_geschwindigkeit` Z. 115–119 (VORSCHLAG) |
| Ladungsgrenze | `ladung_der_mission` Z. 150 |
| Fortschritt, Ankunft, Bericht | `main.auftraege_fortschreiben` Z. 1970–2045, je Spieltick aus `main.tick` Z. 2451 |
| Angriff am Ziel | `main.kampf_am_ziel` Z. 2047 — Wallvorrunde über `kampfbericht.vorrunde`, Beute über `kampfbericht.beute` |
| Anzeige „Laufende Aufträge“ | `main._render_overview` Z. 3490–3500 (`auftraege.fortschritt`) |
| Speichern/Laden | Z. 2492 (`"auftraege"`) / Z. 2660 |
| Start eines Angriffs aus der Oberfläche | `self.state.auftrag_starten("angreifen", …)` Z. 5829 |
| Prüfdateien | `tests/test_kampf_einhaengung.py`, `tests/test_gpt_zeit_auftragsketten.py`, `tests/test_auftraege.py` |

**Was hier fehlt** (belegt, aber nicht angeschlossen): Auftragskosten Gold/Nahrung, Mana für fremde
Siedlungen, Drosselung in 10-%-Schritten (`auftraege.py` Z. 57–59 vorhanden, Z. 514 „nicht
angeschlossen“, Reisekosten leer Z. 536).

---

## System B — Weltkarten-Bewegung (Altpfad, `main.py`)

Ein zweiter, älterer Weg: Truppen ziehen **feldweise** über die Weltkarte. Er kennt **keine**
Einheiten-Auswahl, **keine** GS, **keine** Karren.

| Baustein | Stelle |
|---|---|
| Speicher | `main.py` Z. 798 `self.movements = []`, gespeichert Z. 2473, geladen Z. 2598 |
| Auslöser | Klick auf ein **Nachbarfeld**, wenn „Truppen von hier bewegen“ aktiv ist: `_on_map_click` Z. 5645, Aufruf Z. 5666 |
| Aktion | `_welt_bewegen` Z. 5690–5720: **alle** Einheiten mit `count > 0` werden mitgenommen (keine Auswahl) |
| Formel | Z. 5698–5699: `abstand = |dx|+|dy|`, `dauer = max(2, abstand*5)` **Minuten** → beim Nachbarfeld **5 Spielminuten je Feld, unabhängig von GS** |
| Ankunft | `_tick_loop` Z. 6937–6973, je Tick geprüft |
| Beute bei Ankunft | Z. 6953–6957: **10–40 % je Rohstoff, zufällig, ohne Karren, ohne Ladungsgrenze** |
| Kampf bei Ankunft | Z. 6958–6962: mit **40 % Wahrscheinlichkeit** ein „Kampf“ gegen einen zufälligen Bot, Verlust **1–4 zufällige Einheiten** — ohne Wall, ohne Schlagkraft, ohne `kampf.fuehre_schlacht` |
| Anzeige | Restzeit je Bewegung auf der Weltkarte, Z. 5483–5494 |
| Rückkehr | Z. 6965–6968: Einheiten kommen **sofort** zurück (keine Rückreise-Dauer) |

---

## Die fünf Widersprüche zwischen A und B

| # | Gegenstand | System A (Aufträge) | System B (Weltkarte) |
|---|---|---|---|
| 1 | Reisezeit | `d / GS` Stunden, langsamste Einheit bremst | 5 Spielminuten je Feld, GS wirkungslos |
| 2 | Wer reist | ausgewählte Einheiten + Karren | **alle** Einheiten zuhause, ohne Karren |
| 3 | Beute | nur mit Karren, gedeckelt durch **Ladung** (`kampfbericht.beute` Z. 202–242) | 10–40 % zufällig, **ohne** Karren |
| 4 | Kampf | `kampf.fuehre_schlacht` + `kampfbericht.vorrunde` (Wall, Sequenzen, Verluste) | Münzwurf: 40 % „Kampf“, 1–4 zufällige Einheiten weg |
| 5 | Rückweg | doppelte Reisezeit (belegt, Handbuch S. 19) | keine Rückreise, Einheiten sind sofort da |

**Folge, wenn nichts entschieden wird:** eine neue Wegzeit-Formel wäre die **dritte** Wahrheit.
Deshalb steht E3 („nur `auftraege.py` behalten, Altpfad abklemmen“) im Prüfbericht **vor** jeder
Umsetzung von Wegzeit oder Beute.

---

## Empfehlung (keine Änderung ohne Daniels Wort)

1. **System A bleibt** — es ist der geprüfte, belegte Weg und wird von Angriff, Transport und Handel benutzt.
2. **System B wird abgeklemmt**, nicht gelöscht: `_welt_bewegen` und `_tick_loop`-Ankunft bleiben als
   toter Code mit Hinweiskommentar stehen, `state.movements` bleibt im Spielstand lesbar (alte Stände).
   Die Weltkarte behält Auswahl, Route, Anzeige — aber der Zug wird über `auftraege.starten` gestartet,
   damit GS, Karren und Wall gelten.
3. Prüfzusage für den Umbau: `test_weltkarte`, `test_gpt_zeit_auftragsketten`, `test_auftraege`,
   `test_kampf_einhaengung` bleiben grün, und eine neue Prüfung belegt, dass ein Weltkartenzug
   **nicht mehr** ohne Karren Beute erzeugt.

*Alle Zeilenangaben am 31.10.2026 gegen `src/main.py` und `src/auftraege.py` geprüft.*
